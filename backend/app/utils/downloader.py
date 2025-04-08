import aiohttp
import os
import logging
from typing import Optional
from urllib.parse import urlparse
import mimetypes

logger = logging.getLogger(__name__)

class MediaDownloader:
    def __init__(self, download_dir: str = "downloads"):
        """Initialize media downloader with download directory."""
        self.download_dir = download_dir
        os.makedirs(download_dir, exist_ok=True)
    
    async def download_media(self, url: str, filename: Optional[str] = None) -> str:
        """
        Download media from URL.
        
        Args:
            url: URL of the media to download
            filename: Optional filename to save as
            
        Returns:
            Path to the downloaded file
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        raise Exception(f"Failed to download media: HTTP {response.status}")
                    
                    # Get content type
                    content_type = response.headers.get('Content-Type', '')
                    
                    # Generate filename if not provided
                    if not filename:
                        ext = mimetypes.guess_extension(content_type) or '.tmp'
                        filename = f"{os.urandom(8).hex()}{ext}"
                    
                    # Ensure filename is safe
                    filename = os.path.basename(filename)
                    filepath = os.path.join(self.download_dir, filename)
                    
                    # Download the file
                    with open(filepath, 'wb') as f:
                        while True:
                            chunk = await response.content.read(8192)
                            if not chunk:
                                break
                            f.write(chunk)
                    
                    logger.info(f"Successfully downloaded media to {filepath}")
                    return filepath
                    
        except Exception as e:
            logger.error(f"Error downloading media from {url}: {str(e)}")
            raise
    
    def cleanup_file(self, filepath: str):
        """Delete a downloaded file."""
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                logger.info(f"Cleaned up file: {filepath}")
        except Exception as e:
            logger.error(f"Error cleaning up file {filepath}: {str(e)}")
            raise
