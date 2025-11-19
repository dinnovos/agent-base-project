from typing import Optional
import logging
import time
from sqlalchemy.orm import Session
from src.models.user import User
from src.core.security import verify_password, create_access_token
from src.services.user_service import get_user_by_email, update_last_login

logger = logging.getLogger(__name__)


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """
    Authenticate a user by email and password.
    Returns the user if credentials are valid, None otherwise.
    
    Args:
        db: Database session
        email: User email
        password: Plain text password
        
    Returns:
        User object if authentication successful, None otherwise
        
    Note:
        This function is intentionally slow due to bcrypt password verification.
        Typical time: 100-300ms for password hashing.
    """
    start_time = time.time()
    logger.info(f"Authentication attempt for email: {email}")
    
    # Get user from database
    user = get_user_by_email(db, email)
    if not user:
        logger.warning(f"Authentication failed: User not found - {email}")
        return None
    
    logger.debug(f"User found: {email}, verifying password...")
    
    # Verify password (this is the slow part - bcrypt by design)
    password_start = time.time()
    if not verify_password(password, user.password):
        password_time = time.time() - password_start
        logger.warning(f"Authentication failed: Invalid password - {email} (took {password_time:.2f}s)")
        return None
    password_time = time.time() - password_start
    logger.debug(f"Password verified successfully (took {password_time:.2f}s)")
    
    # Check if user is active
    if not user.is_active:
        logger.warning(f"Authentication failed: User inactive - {email}")
        return None

    # Update last login
    logger.debug(f"Updating last login for user: {email}")
    update_last_login(db, user.id)

    total_time = time.time() - start_time
    logger.info(f"Authentication successful for {email} (total time: {total_time:.2f}s)")
    return user


def create_user_token(user: User) -> str:
    """
    Create a JWT access token for a user.
    Token payload contains user email as 'sub'.
    """
    token_data = {"sub": user.email}
    access_token = create_access_token(token_data)
    return access_token
