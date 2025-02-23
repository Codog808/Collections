# session_manager.py
import uuid
from threading import Lock
from app import PostgresMaster  # Import your context manager

# Global dictionary to store active sessions.
active_sessions = {}
session_lock = Lock()

def create_session(db_config):
    """
    Create a persistent DB session by instantiating PostgresMaster and manually entering its context.
    """
    session_id = str(uuid.uuid4())
    master = PostgresMaster(
        db_config.host,
        db_config.port,
        db_config.user,
        db_config.password,
        db_config.database
    )
    # Manually open the connection (bypassing 'with' so it stays open).
    master.__enter__()
    with session_lock:
        active_sessions[session_id] = master
    return session_id

def get_session(session_id):
    """
    Retrieve an active session by its session_id.
    """
    with session_lock:
        return active_sessions.get(session_id)

def close_session(session_id):
    """
    Close and remove a session.
    """
    with session_lock:
        master = active_sessions.pop(session_id, None)
    if master:
        master.__exit__(None, None, None)

