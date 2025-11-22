from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class PlanBase(BaseModel):
    """Base schema for Plan with common attributes."""
    name: str = Field(..., min_length=1, max_length=100, description="Plan name")
    description: Optional[str] = Field(None, max_length=500, description="Plan description")
    query_limit: int = Field(..., gt=0, description="Maximum number of queries allowed")
    query_window_hours: int = Field(..., gt=0, description="Time window in hours for query limit")


class PlanCreate(PlanBase):
    """Schema for creating a new plan."""
    is_active: bool = Field(default=True, description="Whether the plan is active")


class PlanUpdate(BaseModel):
    """Schema for updating a plan. All fields are optional."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    query_limit: Optional[int] = Field(None, gt=0)
    query_window_hours: Optional[int] = Field(None, gt=0)
    is_active: Optional[bool] = None


class PlanRead(PlanBase):
    """Schema for reading a plan from the database."""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
