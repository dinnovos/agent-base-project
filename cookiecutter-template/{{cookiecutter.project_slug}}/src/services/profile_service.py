from typing import Optional
from sqlalchemy.orm import Session
from src.models.profile import Profile
from src.schemas.profile import ProfileCreate, ProfileUpdate


def get_profile_by_user_id(db: Session, user_id: int) -> Optional[Profile]:
    """Get profile by user ID."""
    return db.query(Profile).filter(Profile.user_id == user_id).first()


def create_profile(db: Session, user_id: int, profile_data: ProfileCreate) -> Profile:
    """Create a new profile for a user."""
    db_profile = Profile(
        user_id=user_id,
        time_zone=profile_data.time_zone,
        language=profile_data.language,
        preferences=profile_data.preferences
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


def update_profile(db: Session, user_id: int, profile_data: ProfileUpdate) -> Optional[Profile]:
    """Update profile information."""
    db_profile = get_profile_by_user_id(db, user_id)
    if not db_profile:
        return None

    update_data = profile_data.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_profile, field, value)

    db.commit()
    db.refresh(db_profile)
    return db_profile
