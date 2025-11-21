from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ProfileBase(BaseModel):
    """Base profile schema with common fields."""
    time_zone: Optional[str] = Field(None, max_length=200)
    language: str = Field(default="en", max_length=50)
    preferences: Optional[str] = None


class ProfileCreate(ProfileBase):
    """Schema for profile creation."""
    pass


class ProfileUpdate(BaseModel):
    """Schema for profile update (all fields optional)."""
    time_zone: Optional[str] = Field(None, max_length=200)
    language: Optional[str] = Field(None, max_length=50)
    preferences: Optional[str] = None
    is_active: Optional[bool] = None


class ProfileRead(ProfileBase):
    """Schema for profile output."""
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
