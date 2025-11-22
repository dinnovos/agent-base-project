from typing import Optional, List
from sqlalchemy.orm import Session
from src.models.plan import Plan
from src.schemas.plan import PlanCreate, PlanUpdate


def get_plan_by_id(db: Session, plan_id: int) -> Optional[Plan]:
    """
    Get a plan by its ID.
    
    Args:
        db: Database session
        plan_id: ID of the plan
        
    Returns:
        Plan object or None if not found
    """
    return db.query(Plan).filter(Plan.id == plan_id).first()


def get_plan_by_name(db: Session, name: str) -> Optional[Plan]:
    """
    Get a plan by its name.
    
    Args:
        db: Database session
        name: Name of the plan
        
    Returns:
        Plan object or None if not found
    """
    return db.query(Plan).filter(Plan.name == name).first()


def get_all_plans(db: Session, include_inactive: bool = False) -> List[Plan]:
    """
    Get all plans.
    
    Args:
        db: Database session
        include_inactive: Whether to include inactive plans (default: False)
        
    Returns:
        List of Plan objects
    """
    query = db.query(Plan)
    if not include_inactive:
        query = query.filter(Plan.is_active == True)
    return query.order_by(Plan.query_limit).all()


def get_default_plan(db: Session) -> Optional[Plan]:
    """
    Get the default "Free" plan.
    
    Args:
        db: Database session
        
    Returns:
        Free Plan object or None if not found
    """
    return get_plan_by_name(db, "Free")


def create_plan(db: Session, plan_data: PlanCreate) -> Plan:
    """
    Create a new plan.
    
    Args:
        db: Database session
        plan_data: PlanCreate schema with plan data
        
    Returns:
        Created Plan object
    """
    db_plan = Plan(
        name=plan_data.name,
        description=plan_data.description,
        query_limit=plan_data.query_limit,
        query_window_hours=plan_data.query_window_hours,
        is_active=plan_data.is_active
    )
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan


def update_plan(db: Session, plan_id: int, plan_data: PlanUpdate) -> Optional[Plan]:
    """
    Update a plan.
    
    Args:
        db: Database session
        plan_id: ID of the plan to update
        plan_data: PlanUpdate schema with updated data
        
    Returns:
        Updated Plan object or None if not found
    """
    db_plan = get_plan_by_id(db, plan_id)
    if not db_plan:
        return None
    
    update_data = plan_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_plan, field, value)
    
    db.commit()
    db.refresh(db_plan)
    return db_plan


def deactivate_plan(db: Session, plan_id: int) -> Optional[Plan]:
    """
    Deactivate a plan (soft delete).
    
    Args:
        db: Database session
        plan_id: ID of the plan to deactivate
        
    Returns:
        Deactivated Plan object or None if not found
    """
    db_plan = get_plan_by_id(db, plan_id)
    if not db_plan:
        return None
    
    db_plan.is_active = False
    db.commit()
    db.refresh(db_plan)
    return db_plan


def activate_plan(db: Session, plan_id: int) -> Optional[Plan]:
    """
    Activate a plan.
    
    Args:
        db: Database session
        plan_id: ID of the plan to activate
        
    Returns:
        Activated Plan object or None if not found
    """
    db_plan = get_plan_by_id(db, plan_id)
    if not db_plan:
        return None
    
    db_plan.is_active = True
    db.commit()
    db.refresh(db_plan)
    return db_plan
