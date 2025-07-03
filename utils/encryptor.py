
import base64
import os

def generate_encrypted_url(filename: str, user_id: int) -> str:
    # Simple base64 encoding with salt (not secure for real use)
    salt = os.urandom(8)
    raw = f"{filename}:{user_id}".encode() + salt
    return base64.urlsafe_b64encode(raw).decode() 