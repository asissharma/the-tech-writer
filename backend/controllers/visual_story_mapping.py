# controllers/visual_story_mapping.py
from datetime import datetime
from sqlalchemy.orm import Session
from db.models import StoryMap

def save_story_map(user_id: str, story_map: dict, db: Session) -> dict:
    """
    Saves a visual story map for the user in the database.
    
    This feature is useful for authors who want to visually plan their narratives. 
    A story map might include nodes representing key events, characters, or settings,
    and connections that illustrate relationships between these elements.
    
    Args:
        user_id (str): The identifier for the user.
        story_map (dict): The visual story map data (e.g., nodes, connections).
        db (Session): A SQLAlchemy session.
        
    Returns:
        dict: A response containing the saved story map and a status message.
    """
    # Check if a story map already exists for the user
    existing_map = db.query(StoryMap).filter(StoryMap.user_id == user_id).first()
    if existing_map:
        existing_map.map_data = story_map
        existing_map.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(existing_map)
        saved_map = existing_map
    else:
        new_map = StoryMap(user_id=user_id, map_data=story_map)
        db.add(new_map)
        db.commit()
        db.refresh(new_map)
        saved_map = new_map

    return {
        "user_id": user_id,
        "story_map": saved_map.map_data,
        "status": "Story map saved successfully."
    }

def get_story_map(user_id: str, db: Session) -> dict:
    """
    Retrieves the visual story map for the user from the database.
    
    This allows users to reload their narrative plans and modify them as needed.
    
    Args:
        user_id (str): The identifier for the user.
        db (Session): A SQLAlchemy session.
        
    Returns:
        dict: A response containing the user's story map or a default map if none exists.
    """
    story_map = db.query(StoryMap).filter(StoryMap.user_id == user_id).first()
    if story_map:
        return {"user_id": user_id, "story_map": story_map.map_data}
    else:
        # Return a default empty story map if none exists
        return {
            "user_id": user_id,
            "story_map": {"nodes": [], "connections": []},
            "status": "No story map found."
        }
