from typing import Optional
from sqlalchemy.orm import Session
from src.models.user import User
from src.core.security import verify_password, create_access_token
from src.services.user_service import get_user_by_email, update_last_login


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """
    Authenticate a user by email and password.
    Returns the user if credentials are valid, None otherwise.
    """
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    if not user.is_active:
        return None

    # Update last login
    update_last_login(db, user.id)

    return user


def create_user_token(user: User) -> str:
    """
    Create a JWT access token for a user.
    Token payload contains user email as 'sub'.
    """
    token_data = {"sub": user.email}
    access_token = create_access_token(token_data)
    return access_token
