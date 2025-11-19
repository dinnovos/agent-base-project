from datetime import datetime, timedelta
from jose import jwt
import bcrypt
import logging
from src.core.config import settings

logger = logging.getLogger(__name__)

# Bcrypt rounds: 12 is default (secure but slow), 10 is faster for development
# In production, use 12-14 rounds. In development, 10 is acceptable.
BCRYPT_ROUNDS = 10  # Adjust based on environment


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Args:
        password: Plain text password
        
    Returns:
        str: Hashed password
        
    Note:
        Uses BCRYPT_ROUNDS for salt generation.
        Lower rounds = faster but less secure.
        Recommended: 10 for dev, 12-14 for production.
    """
    logger.debug(f"Hashing password with {BCRYPT_ROUNDS} rounds")
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=BCRYPT_ROUNDS)
    hashed = bcrypt.hashpw(password_bytes, salt)
    logger.debug("Password hashed successfully")
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hashed password.
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password to compare against
        
    Returns:
        bool: True if password matches, False otherwise
        
    Note:
        This operation is intentionally slow (bcrypt design).
        Typical time: 100-300ms depending on rounds used.
    """
    logger.debug("Verifying password")
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    result = bcrypt.checkpw(password_bytes, hashed_bytes)
    logger.debug(f"Password verification result: {result}")
    return result


def create_access_token(data: dict) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
