"""Profiles router."""

from fastapi import APIRouter

router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.get("/")
def list_profiles():
    """List all profiles."""
    return {"profiles": []}


@router.post("/")
def create_profile():
    """Create a new profile."""
    return {"message": "Profile created"}
