"""Users router."""

from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
def list_users():
    """List all users."""
    return {"users": []}


@router.post("/")
def create_user():
    """Create a new user."""
    return {"message": "User created"}
