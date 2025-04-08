from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Integer, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from .session import Base

class PostStatus(str, enum.Enum):
    PENDING = "pending"
    SCHEDULED = "scheduled"
    POSTED = "posted"
    FAILED = "failed"

class InstagramAccount(Base):
    __tablename__ = "instagram_accounts"

    id = Column(String, primary_key=True)
    username = Column(String, unique=True, index=True)
    encrypted_credentials = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_used = Column(DateTime, nullable=True)

    # Relationships
    media_posts = relationship("MediaPost", back_populates="account")

class MediaPost(Base):
    __tablename__ = "media_posts"

    id = Column(String, primary_key=True)
    source_url = Column(String)
    media_type = Column(String)  # "image", "video", "carousel"
    caption = Column(String, nullable=True)
    account_id = Column(String, ForeignKey("instagram_accounts.id"))
    status = Column(SQLEnum(PostStatus), default=PostStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    posted_at = Column(DateTime, nullable=True)
    error_message = Column(String, nullable=True)

    # Relationships
    account = relationship("InstagramAccount", back_populates="media_posts")
    scheduled_posts = relationship("ScheduledPost", back_populates="media_post")

class ScheduledPost(Base):
    __tablename__ = "scheduled_posts"

    id = Column(String, primary_key=True)
    media_post_id = Column(String, ForeignKey("media_posts.id"))
    scheduled_time = Column(DateTime)
    is_processed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)

    # Relationships
    media_post = relationship("MediaPost", back_populates="scheduled_posts") 