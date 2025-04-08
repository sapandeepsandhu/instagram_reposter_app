#!/bin/bash

# Run script for Instagram Reposter

# Set the directory to the project root
cd "$(dirname "$0")/.."

# Function to display help
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo "Run script for Instagram Reposter"
    echo ""
    echo "Options:"
    echo "  -h, --help       Show this help message"
    echo "  -b, --backend    Run the backend API"
    echo "  -w, --worker     Run the Celery worker"
    echo "  -s, --scheduler  Run the Celery beat scheduler"
    echo "  -f, --frontend   Run the frontend"
    echo "  -a, --all        Run all components"
    echo "  -d, --docker     Run all components using Docker Compose"
    echo ""
    echo "Examples:"
    echo "  $0 --backend     Run the backend API"
    echo "  $0 --all         Run all components"
}

# Parse command line arguments
if [ $# -eq 0 ]; then
    show_help
    exit 0
fi

case "$1" in
    -h|--help)
        show_help
        exit 0
        ;;
    -b|--backend)
        echo "Running backend API..."
        cd backend
        uvicorn app.main:app --reload
        exit 0
        ;;
    -w|--worker)
        echo "Running Celery worker..."
        cd backend
        celery -A app.tasks.instagram_tasks worker --loglevel=info
        exit 0
        ;;
    -s|--scheduler)
        echo "Running Celery beat scheduler..."
        cd backend
        celery -A app.tasks.instagram_tasks beat --loglevel=info
        exit 0
        ;;
    -f|--frontend)
        echo "Running frontend..."
        cd ui
        npm start
        exit 0
        ;;
    -a|--all)
        echo "Running all components..."
        # Start backend in the background
        cd backend
        uvicorn app.main:app --reload &
        BACKEND_PID=$!
        
        # Start Celery worker in the background
        celery -A app.tasks.instagram_tasks worker --loglevel=info &
        WORKER_PID=$!
        
        # Start Celery beat scheduler in the background
        celery -A app.tasks.instagram_tasks beat --loglevel=info &
        SCHEDULER_PID=$!
        
        # Start frontend
        cd ../ui
        npm start
        
        # Kill background processes when frontend is closed
        kill $BACKEND_PID $WORKER_PID $SCHEDULER_PID
        exit 0
        ;;
    -d|--docker)
        echo "Running all components using Docker Compose..."
        docker-compose up
        exit 0
        ;;
    *)
        echo "Unknown option: $1"
        show_help
        exit 1
        ;;
esac 