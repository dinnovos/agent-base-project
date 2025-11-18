from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Base user schema with common fields."""
    username: str = Field(..., min_length=3, max_length=150)
    email: EmailStr
    first_name: Optional[str] = Field(None, max_length=150)
    last_name: Optional[str] = Field(None, max_length=150)


class UserCreate(UserBase):
    """Schema for user creation."""
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    """Schema for user update (all fields optional)."""
    username: Optional[str] = Field(None, min_length=3, max_length=150)
    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(None, max_length=150)
    last_name: Optional[str] = Field(None, max_length=150)
    password: Optional[str] = Field(None, min_length=8)
    is_active: Optional[bool] = None


class UserRead(UserBase):
    """Schema for user output."""
    id: int
    is_active: bool
    is_staff: bool
    is_superuser: bool
    date_joined: datetime
    last_login: Optional[datetime]

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str


class PasswordChange(BaseModel):
    """Schema for password change."""
    current_password: str
    new_password: str = Field(..., min_length=8)
