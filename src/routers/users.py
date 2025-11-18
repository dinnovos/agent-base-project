from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.db.session import get_db
from src.models.user import User
from src.schemas.user import UserRead, UserUpdate, PasswordChange
from src.services.user_service import get_user_by_id, update_user, change_password
from src.dependencies import get_current_user, get_current_superuser

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserRead)
def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Get current user information.
    """
    return current_user


@router.patch("/me", response_model=UserRead)
def update_current_user_info(
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update current user information.
    Users cannot modify sensitive fields like is_active.
    """
    # Non-superusers cannot modify sensitive fields
    if not current_user.is_superuser:
        if user_data.is_active is not None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot modify is_active field"
            )

    user = update_user(db, current_user.id, user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


@router.post("/me/change-password", status_code=status.HTTP_200_OK)
def change_user_password(
    password_data: PasswordChange,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Change current user's password.
    Requires current password for verification.
    """
    success = change_password(
        db,
        current_user.id,
        password_data.current_password,
        password_data.new_password
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    return {"message": "Password changed successfully"}
