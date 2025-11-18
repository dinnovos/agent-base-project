from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.db.session import get_db
from src.models.user import User
from src.schemas.profile import ProfileRead, ProfileUpdate
from src.services.profile_service import get_profile_by_user_id, update_profile
from src.dependencies import get_current_user

router = APIRouter(prefix="/profiles", tags=["Profiles"])


@router.get("/me", response_model=ProfileRead)
def get_current_user_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get current user's profile.
    """
    profile = get_profile_by_user_id(db, current_user.id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )

    return profile


@router.patch("/me", response_model=ProfileRead)
def update_current_user_profile(
    profile_data: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update current user's profile.
    """
    profile = update_profile(db, current_user.id, profile_data)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )

    return profile
