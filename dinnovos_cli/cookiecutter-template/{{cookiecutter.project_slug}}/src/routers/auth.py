"""Authentication router."""

from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login():
    """Login endpoint."""
    return {"message": "Login endpoint"}


@router.post("/logout")
def logout():
    """Logout endpoint."""
    return {"message": "Logout endpoint"}
