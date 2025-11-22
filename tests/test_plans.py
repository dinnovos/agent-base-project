import pytest
from src.models.plan import Plan
from src.models.user import User
from src.services.plan_service import (
    get_plan_by_id,
    get_plan_by_name,
    get_all_plans,
    get_default_plan,
    create_plan,
    update_plan,
    deactivate_plan,
    activate_plan
)
from src.schemas.plan import PlanCreate, PlanUpdate


def test_create_plan(db_session):
    """Test creating a new plan."""
    plan_data = PlanCreate(
        name="Premium",
        description="Plan premium con límites extendidos",
        query_limit=50,
        query_window_hours=24,
        is_active=True
    )
    
    plan = create_plan(db_session, plan_data)
    
    assert plan.id is not None
    assert plan.name == "Premium"
    assert plan.query_limit == 50
    assert plan.query_window_hours == 24
    assert plan.is_active is True


def test_get_plan_by_id(db_session, test_plan):
    """Test getting a plan by ID."""
    plan = get_plan_by_id(db_session, test_plan.id)
    
    assert plan is not None
    assert plan.id == test_plan.id
    assert plan.name == test_plan.name


def test_get_plan_by_name(db_session, test_plan):
    """Test getting a plan by name."""
    plan = get_plan_by_name(db_session, "Free")
    
    assert plan is not None
    assert plan.name == "Free"
    assert plan.query_limit == 5
    assert plan.query_window_hours == 24


def test_get_default_plan(db_session, test_plan):
    """Test getting the default Free plan."""
    plan = get_default_plan(db_session)
    
    assert plan is not None
    assert plan.name == "Free"


def test_get_all_plans(db_session, test_plan):
    """Test getting all active plans."""
    # Create another plan
    plan_data = PlanCreate(
        name="Pro",
        description="Plan profesional",
        query_limit=20,
        query_window_hours=24,
        is_active=True
    )
    create_plan(db_session, plan_data)
    
    plans = get_all_plans(db_session)
    
    assert len(plans) >= 2
    assert all(plan.is_active for plan in plans)


def test_update_plan(db_session, test_plan):
    """Test updating a plan."""
    update_data = PlanUpdate(
        query_limit=10,
        description="Plan gratuito actualizado"
    )
    
    updated_plan = update_plan(db_session, test_plan.id, update_data)
    
    assert updated_plan is not None
    assert updated_plan.query_limit == 10
    assert updated_plan.description == "Plan gratuito actualizado"
    assert updated_plan.name == "Free"  # Name should not change


def test_deactivate_plan(db_session):
    """Test deactivating a plan."""
    # Create a plan to deactivate
    plan_data = PlanCreate(
        name="ToDeactivate",
        description="Plan to be deactivated",
        query_limit=15,
        query_window_hours=24,
        is_active=True
    )
    plan = create_plan(db_session, plan_data)
    
    deactivated_plan = deactivate_plan(db_session, plan.id)
    
    assert deactivated_plan is not None
    assert deactivated_plan.is_active is False


def test_activate_plan(db_session):
    """Test activating a plan."""
    # Create an inactive plan
    plan_data = PlanCreate(
        name="ToActivate",
        description="Plan to be activated",
        query_limit=15,
        query_window_hours=24,
        is_active=False
    )
    plan = create_plan(db_session, plan_data)
    
    activated_plan = activate_plan(db_session, plan.id)
    
    assert activated_plan is not None
    assert activated_plan.is_active is True


def test_user_plan_relationship(db_session, test_plan):
    """Test that users are correctly associated with plans."""
    from src.services.user_service import create_user
    from src.schemas.user import UserCreate
    
    user_data = UserCreate(
        username="planuser",
        email="planuser@example.com",
        password="password123",
        first_name="Plan",
        last_name="User"
    )
    
    user = create_user(db_session, user_data)
    
    assert user.plan_id is not None
    assert user.plan is not None
    assert user.plan.name == "Free"
    assert user.plan.query_limit == 5
    assert user.plan.query_window_hours == 24


def test_plan_users_relationship(db_session, test_plan):
    """Test that plans can access their users."""
    from src.services.user_service import create_user
    from src.schemas.user import UserCreate
    
    # Create multiple users with the same plan
    for i in range(3):
        user_data = UserCreate(
            username=f"user{i}",
            email=f"user{i}@example.com",
            password="password123",
            first_name=f"User{i}",
            last_name="Test"
        )
        create_user(db_session, user_data)
    
    # Refresh plan to get updated relationships
    db_session.refresh(test_plan)
    
    assert len(test_plan.users) >= 3
    assert all(isinstance(user, User) for user in test_plan.users)
