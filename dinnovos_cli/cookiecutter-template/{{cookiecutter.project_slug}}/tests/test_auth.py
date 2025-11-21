import pytest
from fastapi import status


def test_register_user(client, test_user_data):
    """Test user registration."""
    response = client.post("/auth/register", json=test_user_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == test_user_data["email"]
    assert data["username"] == test_user_data["username"]
    assert "password" not in data  # Password should not be returned
    assert "id" in data


def test_register_duplicate_email(client, test_user_data):
    """Test registration with duplicate email."""
    # Register first user
    client.post("/auth/register", json=test_user_data)

    # Try to register with same email
    response = client.post("/auth/register", json=test_user_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "email already registered" in response.json()["detail"].lower()


def test_register_duplicate_username(client, test_user_data):
    """Test registration with duplicate username."""
    # Register first user
    client.post("/auth/register", json=test_user_data)

    # Try to register with same username but different email
    duplicate_user = test_user_data.copy()
    duplicate_user["email"] = "different@example.com"
    response = client.post("/auth/register", json=duplicate_user)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "username already taken" in response.json()["detail"].lower()


def test_login_success(client, test_user_data):
    """Test successful login."""
    # Register user
    client.post("/auth/register", json=test_user_data)

    # Login
    login_data = {
        "username": test_user_data["email"],  # OAuth2 uses 'username' field
        "password": test_user_data["password"]
    }
    response = client.post("/auth/token", data=login_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, test_user_data):
    """Test login with wrong password."""
    # Register user
    client.post("/auth/register", json=test_user_data)

    # Try to login with wrong password
    login_data = {
        "username": test_user_data["email"],
        "password": "wrongpassword"
    }
    response = client.post("/auth/token", data=login_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_login_nonexistent_user(client):
    """Test login with non-existent user."""
    login_data = {
        "username": "nonexistent@example.com",
        "password": "password123"
    }
    response = client.post("/auth/token", data=login_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
