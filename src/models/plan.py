from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.models.base import Base


class Plan(Base):
    """
    Plan model representing subscription plans with rate limiting configurations.
    Each user is associated with a plan that defines their query limits.
    """
    __tablename__ = 'plans'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(String(500), nullable=True)
    query_limit = Column(Integer, nullable=False, comment="Maximum number of queries allowed")
    query_window_hours = Column(Integer, nullable=False, comment="Time window in hours for query limit")
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationship
    users = relationship("User", back_populates="plan")

    def __repr__(self):
        return f"<Plan(id={self.id}, name='{self.name}', query_limit={self.query_limit}, window={self.query_window_hours}h)>"
