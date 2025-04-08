from instagrapi import Client
from instagrapi.exceptions import LoginRequired
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class InstagramClient:
    def __init__(self, credentials: Dict[str, str]):
        """Initialize Instagram client with credentials."""
        self.client = Client()
        self.credentials = credentials
        self._login()
    
    def _login(self):
        """Login to Instagram using provided credentials."""
        try:
            self.client.login(
                username=self.credentials['username'],
                password=self.credentials['password']
            )
            logger.info(f"Successfully logged in as {self.credentials['username']}")
        except Exception as e:
            logger.error(f"Failed to login to Instagram: {str(e)}")
            raise
    
    def upload_media(self, media_path: str, caption: Optional[str] = None) -> bool:
        """Upload media to Instagram."""
        try:
            # Check if media is image or video
            if media_path.lower().endswith(('.jpg', '.jpeg', '.png')):
                media = self.client.photo_upload(media_path, caption=caption)
            elif media_path.lower().endswith(('.mp4', '.mov')):
                media = self.client.video_upload(media_path, caption=caption)
            else:
                raise ValueError("Unsupported media format")
            
            logger.info(f"Successfully uploaded media: {media.id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to upload media: {str(e)}")
            return False
    
    def get_user_info(self) -> Dict:
        """Get information about the logged-in user."""
        try:
            return self.client.account_info()
        except Exception as e:
            logger.error(f"Failed to get user info: {str(e)}")
            raise
    
    def logout(self):
        """Logout from Instagram."""
        try:
            self.client.logout()
            logger.info("Successfully logged out from Instagram")
        except Exception as e:
            logger.error(f"Failed to logout: {str(e)}")
            raise 