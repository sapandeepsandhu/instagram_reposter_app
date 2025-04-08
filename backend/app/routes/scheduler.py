from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from ..database import crud, models
from ..database.session import get_db
from ..tasks.instagram_tasks import process_scheduled_post
import uuid

router = APIRouter()

class SchedulePostRequest(BaseModel):
    media_post_id: str
    scheduled_time: datetime

class ScheduledPostResponse(BaseModel):
    id: str
    media_post_id: str
    scheduled_time: datetime
    is_processed: bool
    created_at: datetime
    processed_at: Optional[datetime]
    retry_count: int

@router.post("/schedule", response_model=ScheduledPostResponse)
async def schedule_post(request: SchedulePostRequest, db: Session = Depends(get_db)):
    """Schedule a post for later."""
    try:
        # Create scheduled post
        scheduled_post = crud.create_scheduled_post(
            db=db,
            schedule_id=str(uuid.uuid4()),
            media_post_id=request.media_post_id,
            scheduled_time=request.scheduled_time
        )
        
        # Schedule Celery task
        process_scheduled_post.apply_async(
            args=[scheduled_post.id],
            eta=scheduled_post.scheduled_time
        )
        
        return ScheduledPostResponse(
            id=scheduled_post.id,
            media_post_id=scheduled_post.media_post_id,
            scheduled_time=scheduled_post.scheduled_time,
            is_processed=scheduled_post.is_processed,
            created_at=scheduled_post.created_at,
            processed_at=scheduled_post.processed_at,
            retry_count=scheduled_post.retry_count
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to schedule post: {str(e)}"
        )

@router.delete("/schedule/{schedule_id}")
async def cancel_scheduled_post(schedule_id: str, db: Session = Depends(get_db)):
    """Cancel a scheduled post."""
    if crud.delete_scheduled_post(db, schedule_id):
        return {"message": f"Scheduled post {schedule_id} cancelled"}
    raise HTTPException(status_code=404, detail="Scheduled post not found")

@router.get("/schedule/{schedule_id}", response_model=ScheduledPostResponse)
async def get_schedule_status(schedule_id: str, db: Session = Depends(get_db)):
    """Get status of a scheduled post."""
    scheduled_post = crud.get_scheduled_post(db, schedule_id)
    if not scheduled_post:
        raise HTTPException(status_code=404, detail="Scheduled post not found")
    
    return ScheduledPostResponse(
        id=scheduled_post.id,
        media_post_id=scheduled_post.media_post_id,
        scheduled_time=scheduled_post.scheduled_time,
        is_processed=scheduled_post.is_processed,
        created_at=scheduled_post.created_at,
        processed_at=scheduled_post.processed_at,
        retry_count=scheduled_post.retry_count
    )
