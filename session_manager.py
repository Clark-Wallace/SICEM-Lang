import json
import os
import time
from uuid import uuid4

SESSION_FILE = "sessions.json"

def _load_sessions():
    """
    Load sessions from disk. If SLANG_ENC_KEY is set, decrypt the data.
    """
    key = os.getenv('SLANG_ENC_KEY')
    if os.path.exists(SESSION_FILE):
        data = open(SESSION_FILE, 'rb').read()
        if key:
            from cryptography.fernet import Fernet
            try:
                f = Fernet(key.encode())
                decrypted = f.decrypt(data)
                return json.loads(decrypted.decode())
            except Exception:
                raise RuntimeError('Failed to decrypt session data')
        else:
            try:
                return json.loads(data.decode())
            except json.JSONDecodeError:
                return {}
    return {}

def _save_sessions(data):
    """
    Save sessions to disk. If SLANG_ENC_KEY is set, encrypt the data.
    """
    key = os.getenv('SLANG_ENC_KEY')
    raw = json.dumps(data, indent=2).encode()
    if key:
        from cryptography.fernet import Fernet
        f = Fernet(key.encode())
        cipher = f.encrypt(raw)
        with open(SESSION_FILE, 'wb') as f_out:
            f_out.write(cipher)
    else:
        with open(SESSION_FILE, 'w') as f_out:
            f_out.write(raw.decode())

def create_session(participants, payload):
    """
    Create a new handshake session.
    participants: list of participant IDs (strings)
    payload: dict of invite metadata
    Returns: session_id (string)
    """
    data = _load_sessions()
    session_id = str(uuid4())
    ts = time.time()
    # Initialize session with metadata and progress events
    data[session_id] = {
        "participants": participants,
        "status": "pending",
        "created": ts,
        "payload": payload,
        "events": [
            {"type": "progress", "timestamp": ts, "content": "Session created"}
        ]
    }
    _save_sessions(data)
    return session_id

def confirm_session(session_id):
    """
    Confirm an existing handshake session.
    Raises KeyError if session not found.
    """
    data = _load_sessions()
    if session_id not in data:
        raise KeyError(f"Session {session_id} not found")
    # Update status and record confirmation time
    ts = time.time()
    data[session_id]["status"] = "confirmed"
    data[session_id]["confirmed"] = ts
    # Append progress event for confirmation
    data[session_id].setdefault("events", []).append(
        {"type": "progress", "timestamp": ts, "content": "Session confirmed"}
    )
    _save_sessions(data)

def get_session(session_id):
    """
    Retrieve session details by session_id.
    Returns dict or None.
    """
    data = _load_sessions()
    return data.get(session_id)

def complete_session(session_id):
    """
    Mark a session as completed.
    Raises KeyError if session not found.
    """
    data = _load_sessions()
    if session_id not in data:
        raise KeyError(f"Session {session_id} not found")
    ts = time.time()
    data[session_id]["status"] = "completed"
    data[session_id]["completed"] = ts
    # Append progress event for completion
    data[session_id].setdefault("events", []).append(
        {"type": "progress", "timestamp": ts, "content": "Session completed"}
    )
    _save_sessions(data)

def expire_session(session_id):
    """
    Mark a session as expired.
    Raises KeyError if session not found.
    """
    data = _load_sessions()
    if session_id not in data:
        raise KeyError(f"Session {session_id} not found")
    ts = time.time()
    data[session_id]["status"] = "expired"
    data[session_id]["expired"] = ts
    # Append progress event for expiration
    data[session_id].setdefault("events", []).append(
        {"type": "progress", "timestamp": ts, "content": "Session expired"}
    )
    _save_sessions(data)

def list_sessions():
    """
    List all sessions with their metadata.
    Returns a dict of session_id -> metadata.
    """
    return _load_sessions()
    
def add_event(session_id: str, event_type: str, content: str, metadata: dict = None):
    """
    Append an event to the session's event list.
    """
    data = _load_sessions()
    if session_id not in data:
        raise KeyError(f"Session {session_id} not found")
    ts = time.time()
    event = {"type": event_type, "timestamp": ts, "content": content}
    if metadata is not None:
        event["metadata"] = metadata
    data[session_id].setdefault("events", []).append(event)
    _save_sessions(data)