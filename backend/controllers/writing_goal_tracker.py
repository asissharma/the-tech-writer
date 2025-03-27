# controllers/writing_goal_tracker.py
from sqlalchemy.orm import Session
from db.models import WritingGoal

def set_writing_goal(user_id: str, goal: int, db: Session) -> dict:
    """
    Sets or updates the writing goal for a user.
    
    Args:
        user_id (str): The user's unique identifier.
        goal (int): The target word count the user wants to achieve.
        db (Session): A SQLAlchemy database session.
        
    Returns:
        dict: A response with the user ID, goal, and status.
    """
    writing_goal = db.query(WritingGoal).filter(WritingGoal.user_id == user_id).first()
    if writing_goal:
        writing_goal.goal = goal
        db.commit()
        db.refresh(writing_goal)
    else:
        writing_goal = WritingGoal(user_id=user_id, goal=goal)
        db.add(writing_goal)
        db.commit()
        db.refresh(writing_goal)
    return {"user_id": user_id, "goal": writing_goal.goal, "status": "Writing goal set successfully."}

def get_writing_goal(user_id: str, db: Session) -> dict:
    """
    Retrieves the writing goal for a user.
    
    Args:
        user_id (str): The user's unique identifier.
        db (Session): A SQLAlchemy database session.
        
    Returns:
        dict: A response containing the user's writing goal, or a message if none is set.
    """
    writing_goal = db.query(WritingGoal).filter(WritingGoal.user_id == user_id).first()
    if writing_goal:
        return {"user_id": user_id, "goal": writing_goal.goal}
    else:
        return {"user_id": user_id, "goal": None, "status": "No writing goal set."}

def track_writing_progress(text: str, user_goal: int) -> dict:
    """
    Tracks the writing progress by comparing the current word count to the target goal.
    
    Args:
        text (str): The text written by the user.
        user_goal (int): The target word count.
        
    Returns:
        dict: A response with the current word count, goal, and progress percentage.
    """
    word_count = len(text.split())
    progress = (word_count / user_goal) * 100 if user_goal > 0 else 0
    return {
        "word_count": word_count,
        "goal": user_goal,
        "progress_percentage": progress
    }
