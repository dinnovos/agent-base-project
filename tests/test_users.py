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


def test_get_current_user(client, test_user_data):
    """Test getting current user information."""
    token = get_auth_token(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/users/me", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == test_user_data["email"]
    assert data["username"] == test_user_data["username"]


def test_get_current_user_no_token(client):
    """Test accessing protected route without token."""
    response = client.get("/users/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_current_user_invalid_token(client):
    """Test accessing protected route with invalid token."""
    headers = {"Authorization": "Bearer invalidtoken123"}
    response = client.get("/users/me", headers=headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_user(client, test_user_data):
    """Test updating user information."""
    token = get_auth_token(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}

    # Get user ID
    response = client.get("/users/me", headers=headers)
    user_id = response.json()["id"]

    # Update user
    update_data = {
        "first_name": "Updated",
        "last_name": "Name"
    }
    response = client.patch(f"/users/{user_id}", json=update_data, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["first_name"] == "Updated"
    assert data["last_name"] == "Name"


def test_user_cannot_update_other_user(client, test_user_data):
    """Test that users cannot update other users' information."""
    # Create and login first user
    token1 = get_auth_token(client, test_user_data)

    # Create second user
    test_user_data2 = test_user_data.copy()
    test_user_data2["email"] = "user2@example.com"
    test_user_data2["username"] = "testuser2"
    client.post("/auth/register", json=test_user_data2)

    # Try to update second user with first user's token
    headers = {"Authorization": f"Bearer {token1}"}
    update_data = {"first_name": "Hacked"}
    response = client.patch("/users/2", json=update_data, headers=headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN
