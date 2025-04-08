from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import accounts, media, scheduler
from .database.session import engine
from .database import models

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Instagram Reposter API",
    description="API for managing Instagram reposting functionality",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(accounts.router, prefix="/api/accounts", tags=["accounts"])
app.include_router(media.router, prefix="/api/media", tags=["media"])
app.include_router(scheduler.router, prefix="/api/scheduler", tags=["scheduler"])

@app.get("/")
async def read_root():
    """Root endpoint to verify API is running."""
    return {
        "status": "online",
        "message": "Welcome to the Instagram Reposter API",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
