from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from src.models.user import User
from src.models.profile import Profile
from src.schemas.user import UserCreate, UserUpdate
from src.core.security import hash_password, verify_password
from src.services.plan_service import get_default_plan
from src.core.logging import logger


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Get user by ID."""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email."""
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Get user by username."""
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user_data: UserCreate) -> User:
    """Create a new user with associated profile and default plan."""
    # Hash the password
    hashed_password = hash_password(user_data.password)

    # Get default "Free" plan
    default_plan = get_default_plan(db)
    if not default_plan:
        logger.error("Default 'Free' plan not found in database")
        raise ValueError("Default plan not found. Please contact administrator.")

    # Create user
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        password=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        plan_id=default_plan.id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Create default profile
    db_profile = Profile(
        user_id=db_user.id,
        language="en"
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_user)

    logger.info(f"User {db_user.username} created with plan '{default_plan.name}' (ID: {default_plan.id})")
    return db_user


def update_user(db: Session, user_id: int, user_data: UserUpdate) -> Optional[User]:
    """Update user information."""
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None

    update_data = user_data.dict(exclude_unset=True)

    # Hash password if provided
    if "password" in update_data:
        update_data["password"] = hash_password(update_data["password"])

    for field, value in update_data.items():
        setattr(db_user, field, value)

    db.commit()
    db.refresh(db_user)
    return db_user


def deactivate_user(db: Session, user_id: int) -> Optional[User]:
    """Deactivate a user."""
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None

    db_user.is_active = False
    db.commit()
    db.refresh(db_user)
    return db_user


def activate_user(db: Session, user_id: int) -> Optional[User]:
    """Activate a user."""
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None

    db_user.is_active = True
    db.commit()
    db.refresh(db_user)
    return db_user


def update_last_login(db: Session, user_id: int) -> None:
    """Update user's last login timestamp."""
    db_user = get_user_by_id(db, user_id)
    if db_user:
        db_user.last_login = datetime.utcnow()
        db.commit()


def change_password(db: Session, user_id: int, current_password: str, new_password: str) -> bool:
    """
    Change user password after verifying current password.
    Returns True if successful, False if current password is incorrect.
    """
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return False
    
    # Verify current password
    if not verify_password(current_password, db_user.password):
        return False
    
    # Update to new password
    db_user.password = hash_password(new_password)
    db.commit()
    return True


def change_user_plan(db: Session, user_id: int, plan_id: int) -> Optional[User]:
    """
    Change user's plan (admin function).
    
    Args:
        db: Database session
        user_id: ID of the user
        plan_id: ID of the new plan
        
    Returns:
        Updated User object or None if user/plan not found
    """
    from src.services.plan_service import get_plan_by_id
    
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        logger.warning(f"User {user_id} not found for plan change")
        return None
    
    db_plan = get_plan_by_id(db, plan_id)
    if not db_plan:
        logger.warning(f"Plan {plan_id} not found for user {user_id}")
        return None
    
    old_plan_name = db_user.plan.name if db_user.plan else "Unknown"
    db_user.plan_id = plan_id
    db.commit()
    db.refresh(db_user)
    
    logger.info(f"User {db_user.username} plan changed from '{old_plan_name}' to '{db_plan.name}'")
    return db_user
