from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from routes import api_router
from db.database import init_models
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Interactive Writing Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust as needed for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Include all API routes under the /api prefix
app.include_router(api_router, prefix="/api")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = "we are in"
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        print("WebSocket connection closed.")
        
@app.on_event("startup")
async def startup_event():
    init_models()
    print("Database initialized and tables created.")
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
