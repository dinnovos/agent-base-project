from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.models.base import Base


class UsageLog(Base):
    __tablename__ = 'usage_logs'

    id = Column(Integer, primary_key=True, index=True)

    main_call_tid = Column(String(200), default="main_001", nullable=False)
    node_call_tid = Column(String(200), default="node_001", nullable=False)
    
    description = Column(Text, nullable=True)
    model = Column(String(200), nullable=True)
    
    inputs = Column(Integer, nullable=True)
    outputs = Column(Integer, nullable=True)
    total = Column(Integer, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    
    user = relationship("User", foreign_keys=[user_id])
