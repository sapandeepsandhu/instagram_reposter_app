#!/bin/bash

# Database migration script for Instagram Reposter

# Set the directory to the project root
cd "$(dirname "$0")/.."

# Check if alembic is installed
if ! command -v alembic &> /dev/null; then
    echo "Alembic is not installed. Installing..."
    pip install alembic
fi

# Function to display help
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo "Database migration script for Instagram Reposter"
    echo ""
    echo "Options:"
    echo "  -h, --help       Show this help message"
    echo "  -u, --upgrade    Upgrade database to the latest version"
    echo "  -d, --downgrade  Downgrade database to the previous version"
    echo "  -c, --create     Create a new migration"
    echo "  -s, --status     Show current migration status"
    echo ""
    echo "Examples:"
    echo "  $0 --upgrade     Upgrade to the latest version"
    echo "  $0 --create \"add user table\"  Create a new migration"
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
    -u|--upgrade)
        echo "Upgrading database to the latest version..."
        cd backend
        alembic upgrade head
        exit 0
        ;;
    -d|--downgrade)
        echo "Downgrading database to the previous version..."
        cd backend
        alembic downgrade -1
        exit 0
        ;;
    -c|--create)
        if [ -z "$2" ]; then
            echo "Error: Migration message is required"
            echo "Usage: $0 --create \"migration message\""
            exit 1
        fi
        echo "Creating new migration: $2"
        cd backend
        alembic revision --autogenerate -m "$2"
        exit 0
        ;;
    -s|--status)
        echo "Showing current migration status..."
        cd backend
        alembic current
        exit 0
        ;;
    *)
        echo "Unknown option: $1"
        show_help
        exit 1
        ;;
esac 