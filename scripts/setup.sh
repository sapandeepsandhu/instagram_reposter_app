#!/bin/bash

# Setup script for Instagram Reposter

# Set the directory to the project root
cd "$(dirname "$0")/.."

# Function to display help
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo "Setup script for Instagram Reposter"
    echo ""
    echo "Options:"
    echo "  -h, --help       Show this help message"
    echo "  -b, --backend    Setup the backend"
    echo "  -f, --frontend   Setup the frontend"
    echo "  -a, --all        Setup all components"
    echo ""
    echo "Examples:"
    echo "  $0 --backend     Setup the backend"
    echo "  $0 --all         Setup all components"
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
        echo "Setting up backend..."
        
        # Create virtual environment
        echo "Creating virtual environment..."
        python -m venv venv
        
        # Activate virtual environment
        echo "Activating virtual environment..."
        source venv/bin/activate
        
        # Install dependencies
        echo "Installing dependencies..."
        pip install -r requirements.txt
        
        # Create .env file if it doesn't exist
        if [ ! -f .env ]; then
            echo "Creating .env file..."
            cp .env.example .env
            echo "Please edit .env file with your configuration"
        fi
        
        # Initialize database
        echo "Initializing database..."
        cd backend
        alembic upgrade head
        cd ..
        
        echo "Backend setup complete!"
        exit 0
        ;;
    -f|--frontend)
        echo "Setting up frontend..."
        
        # Check if Node.js is installed
        if ! command -v node &> /dev/null; then
            echo "Node.js is not installed. Please install Node.js first."
            exit 1
        fi
        
        # Install dependencies
        echo "Installing dependencies..."
        cd ui
        npm install
        cd ..
        
        echo "Frontend setup complete!"
        exit 0
        ;;
    -a|--all)
        echo "Setting up all components..."
        
        # Setup backend
        $0 --backend
        
        # Setup frontend
        $0 --frontend
        
        echo "All components setup complete!"
        exit 0
        ;;
    *)
        echo "Unknown option: $1"
        show_help
        exit 1
        ;;
esac 