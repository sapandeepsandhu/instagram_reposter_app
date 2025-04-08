from celery import Celery
from sqlalchemy.orm import Session
from ..database import crud, models
from ..database.session import SessionLocal
from ..utils.instagram import InstagramClient
from ..utils.encryption import decrypt_credentials
import logging
import os
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Celery
celery_app = Celery('instagram_tasks')
celery_app.config_from_object('celeryconfig')

@celery_app.task(bind=True, max_retries=3)
def process_scheduled_post(self, schedule_id: str):
    """Process a scheduled post and upload it to Instagram."""
    db = SessionLocal()
    try:
        # Get scheduled post
        scheduled_post = crud.get_scheduled_post(db, schedule_id)
        if not scheduled_post:
            logger.error(f"Scheduled post {schedule_id} not found")
            return
        
        # Get media post
        media_post = crud.get_media_post(db, scheduled_post.media_post_id)
        if not media_post:
            logger.error(f"Media post {scheduled_post.media_post_id} not found")
            return
        
        # Get Instagram account
        account = crud.get_instagram_account(db, media_post.account_id)
        if not account:
            logger.error(f"Instagram account {media_post.account_id} not found")
            return
        
        # Decrypt credentials
        credentials = decrypt_credentials(account.encrypted_credentials)
        
        # Initialize Instagram client
        client = InstagramClient(credentials)
        
        # Upload media to Instagram
        success = client.upload_media(
            media_path=media_post.local_path,
            caption=media_post.caption
        )
        
        if success:
            # Update media post status
            crud.update_media_post_status(
                db=db,
                media_post_id=media_post.id,
                status=models.PostStatus.POSTED
            )
            
            # Mark scheduled post as processed
            scheduled_post.is_processed = True
            scheduled_post.processed_at = datetime.utcnow()
            db.commit()
            
            logger.info(f"Successfully posted media {media_post.id} to Instagram")
        else:
            raise Exception("Failed to upload media to Instagram")
            
    except Exception as e:
        logger.error(f"Error processing scheduled post {schedule_id}: {str(e)}")
        
        # Update retry count
        scheduled_post.retry_count += 1
        db.commit()
        
        # Retry task if max retries not reached
        if scheduled_post.retry_count < scheduled_post.max_retries:
            self.retry(exc=e, countdown=300)  # Retry after 5 minutes
        else:
            # Mark media post as failed
            crud.update_media_post_status(
                db=db,
                media_post_id=media_post.id,
                status=models.PostStatus.FAILED,
                error_message=str(e)
            )
            
    finally:
        db.close()

@celery_app.task
def cleanup_old_media():
    """Clean up old media files that have been posted."""
    db = SessionLocal()
    try:
        # Get all posted media older than 24 hours
        old_media = db.query(models.MediaPost).filter(
            models.MediaPost.status == models.PostStatus.POSTED,
            models.MediaPost.posted_at < datetime.utcnow() - timedelta(days=1)
        ).all()
        
        for media in old_media:
            try:
                # Delete local file
                if os.path.exists(media.local_path):
                    os.remove(media.local_path)
                logger.info(f"Cleaned up media file: {media.local_path}")
            except Exception as e:
                logger.error(f"Error cleaning up media file {media.local_path}: {str(e)}")
                
    finally:
        db.close() 