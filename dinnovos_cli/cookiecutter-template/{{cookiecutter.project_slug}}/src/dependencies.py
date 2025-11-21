from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from src.core.config import settings
from src.db.session import get_db
from src.models.user import User
from src.services.user_service import get_user_by_email
from src.services.usage_log_service import check_chatbot_rate_limit
from src.schemas.token import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """
    Dependency to get the current authenticated user from JWT token.
    Raises HTTPException if token is invalid or user not found.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception

    user = get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )

    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency to ensure current user is active.
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user


def get_current_staff_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency to ensure current user is staff.
    """
    if not current_user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user


def get_current_superuser(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency to ensure current user is superuser.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user


def verify_chatbot_rate_limit(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency to check if user has exceeded chatbot query rate limit.
    Uses existing UsageLog records to count queries by main_call_tid.
    Raises HTTPException if limit is exceeded.
    Returns the current user if within limits.
    """
    can_query, queries_used, queries_remaining = check_chatbot_rate_limit(db, current_user.id)
    
    if not can_query:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "message": f"Rate limit exceeded. You have used {queries_used} of {settings.CHATBOT_QUERY_LIMIT} queries in the last {settings.CHATBOT_QUERY_WINDOW_HOURS} hours.",
                "queries_used": queries_used,
                "queries_limit": settings.CHATBOT_QUERY_LIMIT,
                "window_hours": settings.CHATBOT_QUERY_WINDOW_HOURS,
                "queries_remaining": 0
            },
            headers={"X-RateLimit-Limit": str(settings.CHATBOT_QUERY_LIMIT),
                     "X-RateLimit-Remaining": "0",
                     "X-RateLimit-Reset": str(settings.CHATBOT_QUERY_WINDOW_HOURS)}
        )
    
    return current_user
