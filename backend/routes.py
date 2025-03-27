from fastapi import APIRouter, Query, Body, UploadFile, File, Depends
from controllers import (
    text_analysis,
    ai_suggestions,
    plagiarism_detection,
    autosave_version,
    visual_story_mapping,
    voice_to_text,
    writing_goal_tracker,
    collaboration,
)
from pydantic import BaseModel
from typing import Optional,List
from controllers import autosave_version
from db.database import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.concurrency import run_in_threadpool
from controllers import text_analysis
from controllers import visual_story_mapping
from controllers import voice_to_text
from controllers import writing_goal_tracker

api_router = APIRouter()

@api_router.websocket("/ws/text-analysis")
async def websocket_text_analysis(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Receive text data from the client
            text = await websocket.receive_text()
            # Offload analysis to a threadpool so that the event loop is not blocked.
            print('in')
            result = await run_in_threadpool(text_analysis.analyze_text, text)
            print('out')
            # Send back the analysis result as JSON
            await websocket.send_json(result)
            print(result)
    except WebSocketDisconnect:
        print("WebSocket connection closed.")

# Define the request model
class GenerateRequest(BaseModel):
    prompt: str
    history: Optional[List[str]] = []
    system_instruction: Optional[str] = None

# AI Suggestions Endpoint (POST request)
@api_router.post("/suggest", summary="Generate text using Gemini or Open Source model")
async def suggest_endpoint(
    request: GenerateRequest,
    source: str = Query("gemini", description="Model source: 'gemini' or 'open_source'")
):
    # Pass the request object and source flag to the controller
    suggestion = ai_suggestions.generate_suggestion(request, source)
    return suggestion


# Plagiarism Detection Endpoint using POST
@api_router.post("/plagiarism", summary="Check text for plagiarism using Gemini")
async def check_plagiarism_endpoint(request: GenerateRequest = Body(...)):
    return plagiarism_detection.check_plagiarism(request)



# Endpoint to autosave a draft (create or update based on draft_id)
@api_router.post("/autosave", summary="Autosave a draft for a user")
async def autosave_endpoint(
    user_id: str = Body(..., embed=True, description="User identifier"),
    draft: str = Body(..., embed=True, description="Draft content"),
    draft_id: str = Body(None, embed=True, description="Unique draft identifier (optional)"),
    db: Session = Depends(get_db)
):
    return autosave_version.autosave_draft(user_id, draft, db, draft_id)

# Endpoint to retrieve a draft or all drafts for a user.
@api_router.get("/draft", summary="Retrieve autosaved draft(s) for a user")
async def get_draft_endpoint(
    user_id: str = Query(..., description="User identifier"),
    draft_id: str = Query(None, description="Unique draft identifier (optional)"),
    db: Session = Depends(get_db)
):
    return autosave_version.get_draft(user_id, db, draft_id)

# Endpoint to save a specific version of a document
@api_router.post("/save_version", summary="Save a specific version of a document")
async def save_version_endpoint(
    user_id: str = Body(..., embed=True, description="User identifier"),
    version: int = Body(..., embed=True, description="Version number"),
    content: str = Body(..., embed=True, description="Content for this version"),
    db: Session = Depends(get_db)
):
    return autosave_version.save_version(user_id, version, content, db)

# Endpoint to retrieve a specific version of a document
@api_router.get("/get_version", summary="Retrieve a specific version of a document")
async def get_version_endpoint(
    user_id: str = Query(..., description="User identifier"),
    version: int = Query(..., description="Version number"),
    db: Session = Depends(get_db)
):
    return autosave_version.get_version(user_id, version, db)


@api_router.post("/save_story_map", summary="Save a visual story map")
async def save_story_map_endpoint(
    user_id: str = Body(..., embed=True, description="User identifier"),
    story_map: dict = Body(..., embed=True, description="Story map data"),
    db: Session = Depends(get_db)
):
    return visual_story_mapping.save_story_map(user_id, story_map, db)

@api_router.get("/get_story_map", summary="Retrieve a visual story map")
async def get_story_map_endpoint(
    user_id: str = Query(..., description="User identifier"),
    db: Session = Depends(get_db)
):
    return visual_story_mapping.get_story_map(user_id, db)


# Voice-to-Text Endpoint (POST)
@api_router.post("/voice_to_text", summary="Convert voice data to text")
async def convert_voice_to_text(
    file: UploadFile = File(..., description="Audio file for voice-to-text conversion"),
    file_format: str = Query(..., description="Format of the audio file (e.g., mp3, wav, flac, aiff)")
):
    audio_data = await file.read()
    return voice_to_text.convert_voice_to_text(audio_data, file_format)


@api_router.post("/set_goal", summary="Set or update the writing goal")
async def set_goal_endpoint(
    user_id: str = Body(..., embed=True, description="User identifier"),
    goal: int = Body(..., embed=True, description="Target word count"),
    db: Session = Depends(get_db)
):
    return writing_goal_tracker.set_writing_goal(user_id, goal, db)

@api_router.get("/get_goal", summary="Retrieve the current writing goal")
async def get_goal_endpoint(
    user_id: str = Query(..., description="User identifier"),
    db: Session = Depends(get_db)
):
    return writing_goal_tracker.get_writing_goal(user_id, db)

@api_router.get("/track_progress", summary="Track writing progress")
async def track_progress_endpoint(
    text: str = Query(..., description="Text to analyze for word count"),
    user_id: str = Query(..., description="User identifier"),
    db: Session = Depends(get_db)
):
    goal_response = writing_goal_tracker.get_writing_goal(user_id, db)
    if goal_response.get("goal") is None:
        return {"error": "No writing goal set for user."}
    user_goal = goal_response["goal"]
    return writing_goal_tracker.track_writing_progress(text, user_goal)


# Collaboration Endpoints
@api_router.post("/join_collaboration", summary="Join a collaborative editing session")
async def join_collaboration(
    user_id: str = Body(..., embed=True, description="User ID"),
    document_id: str = Body(..., embed=True, description="Document ID")
):
    return collaboration.join_collaboration(user_id, document_id)

@api_router.post("/leave_collaboration", summary="Leave a collaborative editing session")
async def leave_collaboration(
    user_id: str = Body(..., embed=True, description="User ID"),
    document_id: str = Body(..., embed=True, description="Document ID")
):
    return collaboration.leave_collaboration(user_id, document_id)

@api_router.post("/broadcast_update", summary="Broadcast an update to a collaborative session")
async def broadcast_update(
    document_id: str = Body(..., embed=True, description="Document ID"),
    update: dict = Body(..., embed=True, description="Update data")
):
    return collaboration.broadcast_update(document_id, update)
