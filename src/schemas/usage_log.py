from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class UsageLogBase(BaseModel):
    """Base usage log schema with common fields."""
    main_call_tid: str = Field(default="main_001", max_length=200)
    node_call_tid: str = Field(default="node_001", max_length=200)
    description: Optional[str] = None
    model: Optional[str] = Field(None, max_length=200)
    inputs: Optional[int] = Field(None, ge=0)
    outputs: Optional[int] = Field(None, ge=0)
    total: Optional[int] = Field(None, ge=0)


class UsageLogCreate(UsageLogBase):
    """Schema for usage log creation."""
    pass


class UsageLogUpdate(BaseModel):
    """Schema for usage log update (all fields optional)."""
    main_call_tid: Optional[str] = Field(None, max_length=200)
    node_call_tid: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    model: Optional[str] = Field(None, max_length=200)
    inputs: Optional[int] = Field(None, ge=0)
    outputs: Optional[int] = Field(None, ge=0)
    total: Optional[int] = Field(None, ge=0)


class UsageLogRead(UsageLogBase):
    """Schema for usage log output."""
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class UsageLogStats(BaseModel):
    """Schema for usage statistics."""
    total_inputs: int
    total_outputs: int
    total_tokens: int
    log_count: int
    model: Optional[str] = None

    class Config:
        from_attributes = True
