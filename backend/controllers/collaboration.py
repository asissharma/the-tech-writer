# controllers/collaboration.py

# Dummy implementation for real-time collaboration.
# In practice, you would use WebSocket endpoints to manage sessions.
active_sessions = {}

def join_collaboration(user_id: str, document_id: str) -> dict:
    """
    Adds a user to a collaborative editing session for a specific document.
    """
    if document_id not in active_sessions:
        active_sessions[document_id] = []
    active_sessions[document_id].append(user_id)
    return {"document_id": document_id, "user_id": user_id, "status": "Joined collaboration."}

def leave_collaboration(user_id: str, document_id: str) -> dict:
    """
    Removes a user from the collaborative session.
    """
    if document_id in active_sessions and user_id in active_sessions[document_id]:
        active_sessions[document_id].remove(user_id)
    return {"document_id": document_id, "user_id": user_id, "status": "Left collaboration."}

def broadcast_update(document_id: str, update: dict) -> dict:
    """
    Broadcasts an update to all participants in a collaborative session.
    In a full implementation, this would send the update via a WebSocket.
    """
    return {"document_id": document_id, "update": update, "status": "Update broadcasted."}
