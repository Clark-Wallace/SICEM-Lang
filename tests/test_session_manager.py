import pytest
from cryptography.fernet import Fernet
import session_manager

@pytest.fixture(autouse=True)
def tmp_sessions_file(tmp_path, monkeypatch):
    # Redirect SESSION_FILE to a temp file for isolation
    temp = tmp_path / "sessions.json"
    monkeypatch.setattr(session_manager, 'SESSION_FILE', str(temp))
    yield
    # No cleanup needed: fixture uses a fresh file each test

def test_create_and_get_session():
    sid = session_manager.create_session(['A', 'B'], {'foo': 'bar'})
    sess = session_manager.get_session(sid)
    assert sess is not None
    assert sess['participants'] == ['A', 'B']
    assert sess['status'] == 'pending'
    assert 'created' in sess
    assert sess['payload'] == {'foo': 'bar'}

def test_confirm_complete_expire_and_list():
    sid = session_manager.create_session(['X'], {'task': 'do'})
    # Confirm
    session_manager.confirm_session(sid)
    sess = session_manager.get_session(sid)
    assert sess['status'] == 'confirmed'
    assert 'confirmed' in sess
    # Complete
    session_manager.complete_session(sid)
    sess = session_manager.get_session(sid)
    assert sess['status'] == 'completed'
    assert 'completed' in sess
    # Expire
    session_manager.expire_session(sid)
    sess = session_manager.get_session(sid)
    assert sess['status'] == 'expired'
    assert 'expired' in sess
    # List sessions
    all_sessions = session_manager.list_sessions()
    assert sid in all_sessions
    assert isinstance(all_sessions, dict)

def test_invalid_session_operations():
    fake = 'non-existent'
    with pytest.raises(KeyError):
        session_manager.confirm_session(fake)
    with pytest.raises(KeyError):
        session_manager.complete_session(fake)
    with pytest.raises(KeyError):
        session_manager.expire_session(fake)
    
def test_encrypted_sessions(tmp_path, monkeypatch):
    # Test that sessions are encrypted when SLANG_ENC_KEY is set
    secret = Fernet.generate_key().decode()
    monkeypatch.setenv('SLANG_ENC_KEY', secret)
    # Redirect SESSION_FILE to temp
    temp = tmp_path / 'enc_sessions.json'
    monkeypatch.setattr(session_manager, 'SESSION_FILE', str(temp))
    # Create a session
    sid = session_manager.create_session(['X'], {'foo': 'bar'})
    # Underlying file should not contain plaintext 'foo'
    raw = temp.read_bytes()
    assert b'foo' not in raw
    # Loading via get_session should decrypt correctly
    sess = session_manager.get_session(sid)
    assert sess['payload']['foo'] == 'bar'