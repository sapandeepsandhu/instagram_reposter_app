from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os
import json
from typing import Dict

# Get encryption key from environment variable or generate one
ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY', Fernet.generate_key())
fernet = Fernet(ENCRYPTION_KEY)

def encrypt_credentials(credentials: Dict[str, str]) -> str:
    """
    Encrypt Instagram credentials.
    
    Args:
        credentials: Dictionary containing username and password
        
    Returns:
        Encrypted credentials as a string
    """
    try:
        # Convert credentials to JSON string
        credentials_str = json.dumps(credentials)
        
        # Encrypt the credentials
        encrypted_data = fernet.encrypt(credentials_str.encode())
        
        # Convert to base64 string for storage
        return base64.b64encode(encrypted_data).decode()
        
    except Exception as e:
        raise Exception(f"Failed to encrypt credentials: {str(e)}")

def decrypt_credentials(encrypted_credentials: str) -> Dict[str, str]:
    """
    Decrypt Instagram credentials.
    
    Args:
        encrypted_credentials: Encrypted credentials string
        
    Returns:
        Dictionary containing username and password
    """
    try:
        # Decode from base64
        encrypted_data = base64.b64decode(encrypted_credentials)
        
        # Decrypt the data
        decrypted_data = fernet.decrypt(encrypted_data)
        
        # Parse JSON back to dictionary
        return json.loads(decrypted_data.decode())
        
    except Exception as e:
        raise Exception(f"Failed to decrypt credentials: {str(e)}")
