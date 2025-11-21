import pytest
from fastapi import status


def get_auth_token(client, test_user_data):
    """Helper function to register and login a user."""
    client.post("/auth/register", json=test_user_data)
    login_data = {
        "username": test_user_data["email"],
        "password": test_user_data["password"]
    }
    response = client.post("/auth/token", data=login_data)
    return response.json()["access_token"]


def test_get_user_profile(client, test_user_data):
    """Test getting user profile."""
    token = get_auth_token(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/profiles/me", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "id" in data
    assert "user_id" in data
    assert data["language"] == "en"  # Default language


def test_update_user_profile(client, test_user_data):
    """Test updating user profile."""
    token = get_auth_token(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}

    # Update profile
    update_data = {
        "time_zone": "America/New_York",
        "language": "es",
        "preferences": '{"theme": "dark"}'
    }
    response = client.patch("/profiles/me", json=update_data, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["time_zone"] == "America/New_York"
    assert data["language"] == "es"
    assert data["preferences"] == '{"theme": "dark"}'


def test_profile_created_on_user_registration(client, test_user_data):
    """Test that profile is automatically created when user registers."""
    token = get_auth_token(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}

    # Check that profile exists
    response = client.get("/profiles/me", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["language"] == "en"
