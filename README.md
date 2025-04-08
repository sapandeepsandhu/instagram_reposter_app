# Instagram Reposter

A powerful application for scheduling and automating Instagram posts. This application allows you to download media from various sources and schedule them for posting to Instagram at specified times.

## Features

- **Instagram Account Management**: Securely store and manage multiple Instagram accounts
- **Media Download**: Download media from URLs and prepare them for posting
- **Post Scheduling**: Schedule posts for specific times
- **Automated Posting**: Automatically post media to Instagram at scheduled times
- **Post Status Tracking**: Monitor the status of scheduled and posted content
- **Secure Credential Storage**: Encrypt Instagram credentials for enhanced security

## Architecture

The application consists of three main components:

1. **Backend API**: FastAPI-based REST API for managing accounts, media, and schedules
2. **Task Queue**: Celery-based task queue for handling asynchronous operations
3. **Frontend UI**: React-based user interface for interacting with the application

## Prerequisites

- Python 3.8+
- PostgreSQL
- Redis
- Node.js 14+ (for frontend)

## Installation

### Backend Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/instagram-reposter.git
   cd instagram-reposter
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Initialize the database:
   ```bash
   alembic upgrade head
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd ui
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Build the frontend:
   ```bash
   npm run build
   ```

## Configuration

Create a `.env` file in the root directory with the following variables:

```
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/instagram_reposter

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your_secret_key
ENCRYPTION_KEY=your_encryption_key

# API
API_HOST=0.0.0.0
API_PORT=8000
```

## Running the Application

### Start the Backend API

```bash
cd backend
uvicorn app.main:app --reload
```

### Start the Celery Worker

```bash
cd backend
celery -A app.tasks.instagram_tasks worker --loglevel=info
```

### Start the Celery Beat Scheduler

```bash
cd backend
celery -A app.tasks.instagram_tasks beat --loglevel=info
```

### Start the Frontend

```bash
cd ui
npm start
```

## API Documentation

Once the application is running, you can access the API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
instagram_reposter/
├── backend/
│   ├── app/
│   │   ├── database/
│   │   │   ├── crud.py
│   │   │   ├── models.py
│   │   │   └── session.py
│   │   ├── routes/
│   │   │   ├── accounts.py
│   │   │   ├── media.py
│   │   │   └── scheduler.py
│   │   ├── tasks/
│   │   │   └── instagram_tasks.py
│   │   ├── utils/
│   │   │   ├── downloader.py
│   │   │   ├── encryption.py
│   │   │   └── instagram.py
│   │   ├── config.py
│   │   └── main.py
│   ├── Dockerfile
│   └── requirements.txt
├── ui/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── ...
├── celeryconfig.py
├── requirements.txt
└── README.md
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - The web framework
- [Celery](https://docs.celeryproject.org/) - Distributed task queue
- [Instagrapi](https://github.com/adw0rd/instagrapi) - Instagram API client
- [SQLAlchemy](https://www.sqlalchemy.org/) - SQL toolkit and ORM
# instagram_reposter_app
