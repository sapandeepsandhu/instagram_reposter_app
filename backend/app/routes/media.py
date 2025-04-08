from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from ..database import crud, models
from ..database.session import get_db
from ..utils.downloader import media_downloader
import uuid

router = APIRouter()

class MediaDownloadRequest(BaseModel):
    url: HttpUrl
    caption: Optional[str] = None
    account_id: str

class MediaPostResponse(BaseModel):
    id: str
    source_url: HttpUrl
    media_type: str
    caption: Optional[str]
    status: models.PostStatus
    created_at: datetime
    posted_at: Optional[datetime]
    error_message: Optional[str]

@router.post("/download", response_model=MediaPostResponse)
async def download_media(
    request: MediaDownloadRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Download media from Instagram URL."""
    try:
        # Process the download
        result = await media_downloader.process_instagram_url(
            url=request.url,
            account_id=request.account_id,
            caption=request.caption
        )
        
        # Get the created media post
        media_post = crud.get_media_post(db, result["media_post_id"])
        
        return MediaPostResponse(
            id=media_post.id,
            source_url=media_post.source_url,
            media_type=media_post.media_type,
            caption=media_post.caption,
            status=media_post.status,
            created_at=media_post.created_at,
            posted_at=media_post.posted_at,
            error_message=media_post.error_message
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process media download: {str(e)}"
        )

@router.get("/{media_id}", response_model=MediaPostResponse)
async def get_media_status(media_id: str, db: Session = Depends(get_db)):
    """Get status of a media post."""
    media_post = crud.get_media_post(db, media_id)
    if not media_post:
        raise HTTPException(status_code=404, detail="Media not found")
    
    return MediaPostResponse(
        id=media_post.id,
        source_url=media_post.source_url,
        media_type=media_post.media_type,
        caption=media_post.caption,
        status=media_post.status,
        created_at=media_post.created_at,
        posted_at=media_post.posted_at,
        error_message=media_post.error_message
    )
