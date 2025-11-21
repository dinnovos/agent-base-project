from datetime import datetime
from pydantic import BaseModel


class TimestampMixin(BaseModel):
    """Mixin for models with timestamp fields."""
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
