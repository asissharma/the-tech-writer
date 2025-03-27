# db/models.py
from sqlalchemy import Column, Integer, String, Text, DateTime,JSON
from datetime import datetime
from db.database import Base

class AutosavedDraft(Base):
    __tablename__ = "autosaved_drafts"
    
    id = Column(Integer, primary_key=True, index=True)
    draft_id = Column(String, unique=True, index=True)  # Unique identifier for the draft
    user_id = Column(String, index=True)
    draft = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)


class DocumentVersion(Base):
    __tablename__ = "document_versions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    version = Column(Integer)
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

class StoryMap(Base):
    __tablename__ = "story_maps"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    map_data = Column(JSON)  # Stores nodes, connections, and other map details
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class WritingGoal(Base):
    __tablename__ = "writing_goals"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, unique=True)
    goal = Column(Integer)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)