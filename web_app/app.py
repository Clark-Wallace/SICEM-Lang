"""
Simple Flask web frontend for Slang session handshake.
Endpoints:
  /         - Home page with links
  /hang     - Form to initiate a hang session
  /catch    - Form to respond to a hang session
  /status   - Query session metadata
"""
import os
import json
import re
from functools import wraps
from flask import Flask, request, render_template, make_response, abort, Response, stream_with_context
import time
from dotenv import load_dotenv

from session_manager import create_session, confirm_session, get_session, _load_sessions, _save_sessions

app = Flask(__name__, template_folder='templates')
load_dotenv()
# JWT secret for signing and verifying tokens
JWT_SECRET = os.getenv('SLANG_JWT_SECRET')

import jwt

def require_jwt(f):
    """Decorator to require a valid JWT in the Authorization header."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not JWT_SECRET:
            abort(500, description='JWT_SECRET not set')
        token = None
        auth_header = request.headers.get('Authorization', '')
        if auth_header:
            parts = auth_header.split()
            if len(parts) == 2 and parts[0].lower() == 'bearer':
                token = parts[1]
        # Fallback to query parameters
        if not token:
            token = request.args.get('token') or request.args.get('api_key')
        if not token:
            abort(401, description='Missing JWT token')
        try:
            jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        except Exception:
            abort(401, description='Invalid or expired token')
        return f(*args, **kwargs)
    return decorated

def require_role(role):
    """Decorator to require a specific role claim in the JWT."""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not JWT_SECRET:
                abort(500, description='JWT_SECRET not set')
            auth_header = request.headers.get('Authorization', '')
            parts = auth_header.split()
            if len(parts) != 2 or parts[0].lower() != 'bearer':
                abort(401, description='Missing or invalid Authorization header')
            token = parts[1]
            try:
                claims = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            except Exception:
                abort(401, description='Invalid or expired token')
            roles = claims.get('roles', []) or []
            if role not in roles:
                abort(403, description='Insufficient role privileges')
            return f(*args, **kwargs)
        return decorated
    return decorator

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hang', methods=['GET', 'POST'])
@require_jwt
@require_role('hang')
def hang():
    if request.method == 'POST':
        source = request.form.get('source')
        target = request.form.get('target')
        payload_text = request.form.get('payload')
        try:
            payload = json.loads(payload_text)
        except Exception:
            return render_template('hang.html', error='Invalid JSON payload'), 400
        session_id = create_session([source, target], payload)
        # Build hang.slang
        lines = []
        lines.append('system: Handshake')
        lines.append('function: hang')
        lines.append(f'agent: {source}')
        lines.append('intent: invite_to_session')
        lines.append('context:')
        lines.append(f'  session_id: "{session_id}"')
        lines.append('  participants:')
        lines.append(f'    - "{source}"')
        lines.append(f'    - "{target}"')
        lines.append(f'  payload: {json.dumps(payload)}')
        lines.append(f'output: session:{session_id}')
        content = '\n'.join(lines) + '\n'
        response = make_response(content)
        response.headers['Content-Type'] = 'text/plain'
        response.headers['Content-Disposition'] = f'attachment; filename=hang_{session_id}.slang'
        return response
    return render_template('hang.html')

@app.route('/catch', methods=['GET', 'POST'])
@require_jwt
@require_role('catch')
def catch():
    if request.method == 'POST':
        handshake_text = request.form.get('handshake')
        profile_json = request.form.get('profile')
        try:
            m = re.search(r'session_id:\s*"([^"]+)"', handshake_text)
            if not m:
                raise ValueError('session_id not found')
            session_id = m.group(1)
            confirm_session(session_id)
        except Exception as e:
            return render_template('catch.html', error=str(e)), 400
        # Build catch.slang
        name = json.loads(profile_json).get('name', '')
        lines = []
        lines.append('system: Handshake')
        lines.append('function: catch')
        lines.append(f'agent: {name}')
        lines.append('intent: accept_session')
        lines.append('context:')
        lines.append(f'  session_id: "{session_id}"')
        lines.append('output: status:confirmed')
        content = '\n'.join(lines) + '\n'
        response = make_response(content)
        response.headers['Content-Type'] = 'text/plain'
        response.headers['Content-Disposition'] = f'attachment; filename=catch_{session_id}.slang'
        return response
    return render_template('catch.html')

@app.route('/status', methods=['GET'])
@require_jwt
@require_role('status')
def status():
    session_id = request.args.get('session')
    if not session_id:
        return 'Missing session parameter', 400
    sess = get_session(session_id)
    if not sess:
        return f'Session {session_id} not found', 404
    return json.dumps(sess, indent=2), 200

# Real-time Server-Sent Events for session progress and chat
@app.route('/events')  # GET SSE stream for session events
@require_jwt
@require_role('status')
def events():
    session_id = request.args.get('session')
    if not session_id:
        abort(400, description='Missing session parameter')
    def event_stream():
        last_index = 0
        while True:
            sess = get_session(session_id)
            if not sess:
                yield f"event: error\ndata: {{\"message\": \"Session not found\"}}\n\n"
                break
            events_list = sess.get('events', [])
            if len(events_list) > last_index:
                for ev in events_list[last_index:]:
                    data = json.dumps(ev)
                    yield f"event: {ev.get('type', 'message')}\n"
                    yield f"data: {data}\n\n"
                last_index = len(events_list)
            time.sleep(1)
    return Response(stream_with_context(event_stream()), content_type='text/event-stream')

@app.route('/session/<session_id>')
@require_jwt
@require_role('status')
def session_dashboard(session_id):
    # Render live session dashboard
    return render_template('session.html', session_id=session_id)

@app.route('/message', methods=['POST'])
@require_jwt
def post_message():
    # Post a chat message to a session
    data = request.get_json() or {}
    session_id = data.get('session') or request.args.get('session')
    sender = data.get('sender')
    content = data.get('message')
    if not session_id or not sender or not content:
        abort(400, description='Missing session, sender, or message')
    # Append chat event
    sessions = _load_sessions()
    if session_id not in sessions:
        abort(404, description=f'Session {session_id} not found')
    ts = time.time()
    event = { 'type': 'chat', 'timestamp': ts, 'sender': sender, 'content': content }
    sessions[session_id].setdefault('events', []).append(event)
    _save_sessions(sessions)
    return ('', 204)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))