from sqlalchemy.orm import Session
from . import models
from datetime import datetime
from typing import List, Optional

def create_instagram_account(db: Session, account_id: str, username: str, encrypted_credentials: str) -> models.InstagramAccount:
    db_account = models.InstagramAccount(
        id=account_id,
        username=username,
        encrypted_credentials=encrypted_credentials
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

def get_instagram_account(db: Session, account_id: str) -> Optional[models.InstagramAccount]:
    return db.query(models.InstagramAccount).filter(models.InstagramAccount.id == account_id).first()

def get_instagram_accounts(db: Session, skip: int = 0, limit: int = 100) -> List[models.InstagramAccount]:
    return db.query(models.InstagramAccount).offset(skip).limit(limit).all()

def update_instagram_account(db: Session, account_id: str, is_active: bool = None) -> Optional[models.InstagramAccount]:
    db_account = get_instagram_account(db, account_id)
    if db_account:
        if is_active is not None:
            db_account.is_active = is_active
        db_account.last_used = datetime.utcnow()
        db.commit()
        db.refresh(db_account)
    return db_account

def delete_instagram_account(db: Session, account_id: str) -> bool:
    db_account = get_instagram_account(db, account_id)
    if db_account:
        db.delete(db_account)
        db.commit()
        return True
    return False

# Media Post operations
def create_media_post(
    db: Session,
    post_id: str,
    source_url: str,
    account_id: str,
    media_type: str = "unknown",
    caption: Optional[str] = None
) -> models.MediaPost:
    db_post = models.MediaPost(
        id=post_id,
        source_url=source_url,
        media_type=media_type,
        caption=caption,
        account_id=account_id
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_media_post(db: Session, post_id: str) -> Optional[models.MediaPost]:
    return db.query(models.MediaPost).filter(models.MediaPost.id == post_id).first()

def update_media_post_status(
    db: Session,
    post_id: str,
    status: models.PostStatus,
    error_message: Optional[str] = None
) -> Optional[models.MediaPost]:
    db_post = get_media_post(db, post_id)
    if db_post:
        db_post.status = status
        if status == models.PostStatus.POSTED:
            db_post.posted_at = datetime.utcnow()
        if error_message:
            db_post.error_message = error_message
        db.commit()
        db.refresh(db_post)
    return db_post

# Scheduled Post operations
def create_scheduled_post(
    db: Session,
    schedule_id: str,
    media_post_id: str,
    scheduled_time: datetime
) -> models.ScheduledPost:
    db_schedule = models.ScheduledPost(
        id=schedule_id,
        media_post_id=media_post_id,
        scheduled_time=scheduled_time
    )
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

def get_scheduled_post(db: Session, schedule_id: str) -> Optional[models.ScheduledPost]:
    return db.query(models.ScheduledPost).filter(models.ScheduledPost.id == schedule_id).first()

def delete_scheduled_post(db: Session, schedule_id: str) -> bool:
    db_schedule = get_scheduled_post(db, schedule_id)
    if db_schedule:
        db.delete(db_schedule)
        db.commit()
        return True
    return False

def get_pending_scheduled_posts(db: Session) -> List[models.ScheduledPost]:
    return db.query(models.ScheduledPost)\
        .filter(models.ScheduledPost.is_processed == False)\
        .filter(models.ScheduledPost.scheduled_time <= datetime.utcnow())\
        .all() 