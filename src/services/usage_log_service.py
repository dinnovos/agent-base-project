from typing import Optional, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import desc
from src.models.usage_log import UsageLog
from src.schemas.usage_log import UsageLogCreate, UsageLogUpdate


def create_usage_log(db: Session, user_id: int, usage_data: UsageLogCreate) -> UsageLog:
    """
    Create a new usage log entry.
    
    Args:
        db: Database session
        user_id: ID of the user
        usage_data: UsageLogCreate schema with token usage data
        
    Returns:
        Created UsageLog object
    """
    db_usage_log = UsageLog(
        user_id=user_id,
        main_call_tid=usage_data.main_call_tid,
        node_call_tid=usage_data.node_call_tid,
        description=usage_data.description,
        model=usage_data.model,
        inputs=usage_data.inputs,
        outputs=usage_data.outputs,
        total=usage_data.total
    )
    db.add(db_usage_log)
    db.commit()
    db.refresh(db_usage_log)
    return db_usage_log


def get_usage_log_by_id(db: Session, usage_log_id: int) -> Optional[UsageLog]:
    """Get usage log by ID."""
    return db.query(UsageLog).filter(UsageLog.id == usage_log_id).first()


def get_usage_logs_by_user(db: Session, user_id: int, limit: int = 100, offset: int = 0) -> List[UsageLog]:
    """
    Get all usage logs for a specific user.
    
    Args:
        db: Database session
        user_id: ID of the user
        limit: Maximum number of records to return
        offset: Number of records to skip
        
    Returns:
        List of UsageLog objects
    """
    return db.query(UsageLog).filter(
        UsageLog.user_id == user_id
    ).order_by(desc(UsageLog.created_at)).limit(limit).offset(offset).all()


def get_usage_logs_by_user_and_model(
    db: Session, 
    user_id: int, 
    model: str,
    limit: int = 100, 
    offset: int = 0
) -> List[UsageLog]:
    """
    Get usage logs for a specific user and model.
    
    Args:
        db: Database session
        user_id: ID of the user
        model: Model name to filter by
        limit: Maximum number of records to return
        offset: Number of records to skip
        
    Returns:
        List of UsageLog objects
    """
    return db.query(UsageLog).filter(
        UsageLog.user_id == user_id,
        UsageLog.model == model
    ).order_by(desc(UsageLog.created_at)).limit(limit).offset(offset).all()


def get_usage_logs_by_date_range(
    db: Session,
    user_id: int,
    start_date: datetime,
    end_date: datetime,
    limit: int = 100,
    offset: int = 0
) -> List[UsageLog]:
    """
    Get usage logs within a date range for a specific user.
    
    Args:
        db: Database session
        user_id: ID of the user
        start_date: Start date for filtering
        end_date: End date for filtering
        limit: Maximum number of records to return
        offset: Number of records to skip
        
    Returns:
        List of UsageLog objects
    """
    return db.query(UsageLog).filter(
        UsageLog.user_id == user_id,
        UsageLog.created_at >= start_date,
        UsageLog.created_at <= end_date
    ).order_by(desc(UsageLog.created_at)).limit(limit).offset(offset).all()


def get_total_tokens_by_user(db: Session, user_id: int) -> dict:
    """
    Get total token usage statistics for a user.
    
    Args:
        db: Database session
        user_id: ID of the user
        
    Returns:
        Dictionary with total_inputs, total_outputs, and total_tokens
    """
    logs = db.query(UsageLog).filter(UsageLog.user_id == user_id).all()
    
    total_inputs = sum(log.inputs or 0 for log in logs)
    total_outputs = sum(log.outputs or 0 for log in logs)
    total_tokens = sum(log.total or 0 for log in logs)
    
    return {
        "total_inputs": total_inputs,
        "total_outputs": total_outputs,
        "total_tokens": total_tokens,
        "log_count": len(logs)
    }


def get_total_tokens_by_user_and_model(db: Session, user_id: int, model: str) -> dict:
    """
    Get total token usage statistics for a user and specific model.
    
    Args:
        db: Database session
        user_id: ID of the user
        model: Model name to filter by
        
    Returns:
        Dictionary with total_inputs, total_outputs, and total_tokens
    """
    logs = db.query(UsageLog).filter(
        UsageLog.user_id == user_id,
        UsageLog.model == model
    ).all()
    
    total_inputs = sum(log.inputs or 0 for log in logs)
    total_outputs = sum(log.outputs or 0 for log in logs)
    total_tokens = sum(log.total or 0 for log in logs)
    
    return {
        "total_inputs": total_inputs,
        "total_outputs": total_outputs,
        "total_tokens": total_tokens,
        "log_count": len(logs),
        "model": model
    }


def update_usage_log(db: Session, usage_log_id: int, usage_data: UsageLogUpdate) -> Optional[UsageLog]:
    """
    Update a usage log entry.
    
    Args:
        db: Database session
        usage_log_id: ID of the usage log to update
        usage_data: UsageLogUpdate schema with updated data
        
    Returns:
        Updated UsageLog object or None if not found
    """
    db_usage_log = get_usage_log_by_id(db, usage_log_id)
    if not db_usage_log:
        return None
    
    update_data = usage_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_usage_log, field, value)
    
    db.commit()
    db.refresh(db_usage_log)
    return db_usage_log


def delete_usage_log(db: Session, usage_log_id: int) -> bool:
    """
    Delete a usage log entry.
    
    Args:
        db: Database session
        usage_log_id: ID of the usage log to delete
        
    Returns:
        True if deleted, False if not found
    """
    db_usage_log = get_usage_log_by_id(db, usage_log_id)
    if not db_usage_log:
        return False
    
    db.delete(db_usage_log)
    db.commit()
    return True


def delete_usage_logs_by_user(db: Session, user_id: int) -> int:
    """
    Delete all usage logs for a user.
    
    Args:
        db: Database session
        user_id: ID of the user
        
    Returns:
        Number of deleted records
    """
    count = db.query(UsageLog).filter(UsageLog.user_id == user_id).delete()
    db.commit()
    return count


def delete_old_usage_logs(db: Session, days: int = 90) -> int:
    """
    Delete usage logs older than specified days.
    
    Args:
        db: Database session
        days: Number of days to keep (default: 90)
        
    Returns:
        Number of deleted records
    """
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    count = db.query(UsageLog).filter(UsageLog.created_at < cutoff_date).delete()
    db.commit()
    return count
