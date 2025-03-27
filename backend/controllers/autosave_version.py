import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from db.models import AutosavedDraft, DocumentVersion

def autosave_draft(user_id: str, draft: str, db: Session, draft_id: str = None) -> dict:
    """
    Autosaves a draft for a given user into the database.
    If a draft_id is provided and exists, the draft is updated.
    Otherwise, a new draft is created with a new unique draft_id.

    Args:
        user_id (str): The identifier for the user.
        draft (str): The draft content.
        db (Session): A SQLAlchemy session.
        draft_id (str, optional): The unique identifier of the draft to update.

    Returns:
        dict: A response containing the user_id, the draft_id, and a status message.
    """
    if draft_id:
        existing = db.query(AutosavedDraft).filter(
            AutosavedDraft.user_id == user_id,
            AutosavedDraft.draft_id == draft_id
        ).first()
    else:
        existing = None

    if existing:
        existing.draft = draft
        existing.timestamp = datetime.utcnow()
        db.commit()
        return {"user_id": user_id, "draft_id": draft_id, "status": "Draft updated successfully."}
    else:
        new_draft_id = draft_id if draft_id else str(uuid.uuid4())
        new_draft = AutosavedDraft(user_id=user_id, draft_id=new_draft_id, draft=draft)
        db.add(new_draft)
        db.commit()
        return {"user_id": user_id, "draft_id": new_draft_id, "status": "Draft autosaved successfully."}

def get_draft(user_id: str, db: Session, draft_id: str = None) -> dict:
    """
    Retrieves autosaved drafts for a given user.
    If draft_id is provided, retrieves that specific draft; otherwise, retrieves all drafts.

    Args:
        user_id (str): The identifier for the user.
        db (Session): A SQLAlchemy session.
        draft_id (str, optional): The unique identifier of the draft to retrieve.

    Returns:
        dict: A response containing the draft(s) or a status message if no draft is found.
    """
    if draft_id:
        draft = db.query(AutosavedDraft).filter(
            AutosavedDraft.user_id == user_id,
            AutosavedDraft.draft_id == draft_id
        ).first()
        if not draft:
            return {"user_id": user_id, "draft_id": draft_id, "status": "No draft found."}
        return {"user_id": user_id, "draft_id": draft_id, "draft": draft.draft, "timestamp": draft.timestamp}
    else:
        drafts = db.query(AutosavedDraft).filter(AutosavedDraft.user_id == user_id).all()
        if not drafts:
            return {"user_id": user_id, "status": "No drafts found."}
        return {
            "user_id": user_id,
            "drafts": [
                {"draft_id": d.draft_id, "draft": d.draft, "timestamp": d.timestamp} for d in drafts
            ],
        }

def save_version(user_id: str, version: int, content: str, db: Session) -> dict:
    """
    Saves a specific version of a document for the given user.
    """
    new_version = DocumentVersion(user_id=user_id, version=version, content=content)
    db.add(new_version)
    db.commit()
    return {"user_id": user_id, "version": version, "status": "Version saved successfully."}

def get_version(user_id: str, version: int, db: Session) -> dict:
    """
    Retrieves a specific version of a document for the given user.
    """
    version_entry = db.query(DocumentVersion).filter(
        DocumentVersion.user_id == user_id,
        DocumentVersion.version == version
    ).first()
    if not version_entry:
        return {"user_id": user_id, "version": version, "status": "Version not found."}
    return {"user_id": user_id, "version": version, "content": version_entry.content, "timestamp": version_entry.timestamp}
