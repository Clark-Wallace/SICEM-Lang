"""
session_tool.py:
Utility wrappers around session_manager for handshake session lifecycle.
"""
from session_manager import create_session, confirm_session, get_session, complete_session, expire_session, list_sessions

def new_session(participants: list, payload: dict) -> str:
    """
    Create and record a new handshake session.

    :param participants: List of participant IDs (strings).
    :param payload: Dictionary of invite metadata.
    :returns: Generated session_id.
    """
    return create_session(participants, payload)

def confirm_existing_session(session_id: str):
    """
    Confirm a pending handshake session.

    :param session_id: The session ID to confirm.
    """
    confirm_session(session_id)

def lookup_session(session_id: str) -> dict:
    """
    Retrieve session details by session_id.

    :param session_id: The session ID.
    :returns: Session metadata dictionary or None.
    """
    return get_session(session_id)
 
def complete_session_tool(session_id: str):
    """
    Mark a session as completed via the session manager.
    """
    complete_session(session_id)

def expire_session_tool(session_id: str):
    """
    Mark a session as expired via the session manager.
    """
    expire_session(session_id)

def list_all_sessions() -> dict:
    """
    Return all sessions and their metadata.
    """
    return list_sessions()