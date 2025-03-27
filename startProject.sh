#!/bin/bash

# Define project directories
PROJECT_DIR="D:/codes/personal projects/theTechWriter"
BACKEND_DIR="$PROJECT_DIR/backend"
FRONTEND_DIR="$PROJECT_DIR/frontend"
VENV_DIR="$BACKEND_DIR/venv"  # Virtual environment path
LOG_FILE="$PROJECT_DIR/startup.log"

# Clear old logs
> "$LOG_FILE"

# Function to start FastAPI backend with virtual environment
start_backend() {
    echo "Starting FastAPI backend..." | tee -a "$LOG_FILE"
    cd "$BACKEND_DIR" || { echo "Backend directory not found!" | tee -a "$LOG_FILE"; exit 1; }

    # Check if virtual environment exists
    if [ -d "$VENV_DIR" ]; then
        source "$VENV_DIR/Scripts/activate" || { echo "Failed to activate virtual environment!" | tee -a "$LOG_FILE"; exit 1; }
        echo "Virtual environment activated." | tee -a "$LOG_FILE"
    else
        echo "Virtual environment not found! Creating one..." | tee -a "$LOG_FILE"
        python -m venv "$VENV_DIR"
        source "$VENV_DIR/Scripts/activate"
        echo "Virtual environment created and activated." | tee -a "$LOG_FILE"
    fi

    # Install dependencies if missing
    pip install -r requirements.txt | tee -a "$LOG_FILE"
    
    # Run FastAPI server
    uvicorn main:app --reload &>> "$LOG_FILE" & 
    echo "FastAPI backend running." | tee -a "$LOG_FILE"
}

# Function to start React frontend
start_frontend() {
    echo "Starting React frontend..." | tee -a "$LOG_FILE"
    cd "$FRONTEND_DIR" || { echo "Frontend directory not found!" | tee -a "$LOG_FILE"; exit 1; }

    # Install dependencies if missing
    npm install | tee -a "$LOG_FILE"
    
    # Run React server
    npm start &>> "$LOG_FILE" &
    echo "React frontend running." | tee -a "$LOG_FILE"
}

# Run functions
start_backend
start_frontend

# Wait a few seconds before confirming success
sleep 3  

echo "✅ Project is up and running!" | tee -a "$LOG_FILE"
