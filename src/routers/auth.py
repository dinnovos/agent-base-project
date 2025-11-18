from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.db.session import get_db
from src.schemas.user import UserCreate, UserRead, UserLogin
from src.schemas.token import Token
from src.services.auth_service import authenticate_user, create_user_token
from src.services.user_service import create_user, get_user_by_email, get_user_by_username
from src.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=Token)
def login_json(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Login endpoint with JSON body.
    Returns JWT access token on successful authentication.
    """
    user = authenticate_user(db, email=credentials.email, password=credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_user_token(user)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user.
    Creates user and associated profile.
    """
    # Check if email already exists
    if get_user_by_email(db, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Check if username already exists
    if get_user_by_username(db, user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )

    # Create user
    user = create_user(db, user_data)
    return user


@router.post("/refresh", response_model=Token)
def refresh_token(
    current_user = Depends(get_current_user)
):
    """
    Refresh the access token.
    Requires a valid current token to generate a new one.
    """
    access_token = create_user_token(current_user)
    return {"access_token": access_token, "token_type": "bearer"}
