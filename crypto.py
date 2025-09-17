import hashlib
import hmac
import os

def generate_salt():
    """Generate a random salt for password hashing."""
    return os.urandom(16).hex()

def hash_password(password: str, salt: str = None) -> tuple[str, str]:
    """
    Hash a password using SHA256 with a salt.
    Returns tuple of (hashed_password, salt).
    """
    if salt is None:
        salt = generate_salt()
    
    # Convert password to bytes and combine with salt
    password_bytes = password.encode('utf-8')
    salt_bytes = bytes.fromhex(salt)
    
    # Create hash using HMAC with SHA256
    hashed = hmac.new(salt_bytes, password_bytes, hashlib.sha256).hexdigest()
    return hashed, salt

def verify_password(password: str, stored_hash: str, salt: str) -> bool:
    """Verify a password against its hash."""
    calculated_hash, _ = hash_password(password, salt)
    return hmac.compare_digest(calculated_hash, stored_hash)