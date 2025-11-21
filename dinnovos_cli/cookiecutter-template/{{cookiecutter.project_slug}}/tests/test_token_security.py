"""
Tests para verificar la seguridad y funcionamiento de los tokens JWT.
"""
import pytest
import time
from datetime import datetime, timedelta
from jose import jwt
from src.core.config import settings


class TestTokenGeneration:
    """Pruebas para la generación de tokens."""
    
    def test_login_returns_valid_token(self, client):
        """Verificar que login retorna un token válido."""
        # Primero registrar un usuario
        register_response = client.post(
            "/auth/register",
            json={
                "email": "tokentest@example.com",
                "username": "tokentest",
                "password": "SecurePassword123",
                "first_name": "Token",
                "last_name": "Test"
            }
        )
        assert register_response.status_code == 201
        
        # Luego hacer login
        login_response = client.post(
            "/auth/login",
            json={
                "email": "tokentest@example.com",
                "password": "SecurePassword123"
            }
        )
        assert login_response.status_code == 200
        data = login_response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        
        # Verificar que el token es válido
        token = data["access_token"]
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        assert payload["sub"] == "tokentest@example.com"
        assert "exp" in payload
    
    def test_token_expiration(self, client):
        """Verificar que los tokens tienen fecha de expiración."""
        # Registrar usuario
        client.post(
            "/auth/register",
            json={
                "email": "exptest@example.com",
                "username": "exptest",
                "password": "SecurePassword123",
                "first_name": "Exp",
                "last_name": "Test"
            }
        )
        
        # Login
        login_response = client.post(
            "/auth/login",
            json={
                "email": "exptest@example.com",
                "password": "SecurePassword123"
            }
        )
        
        token = login_response.json()["access_token"]
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        # Verificar que la expiración es aproximadamente 30 minutos
        # El payload["exp"] es un timestamp Unix (segundos desde epoch)
        exp_timestamp = payload["exp"]
        now_timestamp = datetime.utcnow().timestamp()
        diff_minutes = (exp_timestamp - now_timestamp) / 60
        
        # Permitir 2 minutos de diferencia (para variaciones en ejecución)
        assert 28 < diff_minutes < 32


class TestTokenValidation:
    """Pruebas para la validación de tokens."""
    
    def test_invalid_token_rejected(self, client):
        """Verificar que tokens inválidos son rechazados."""
        response = client.get(
            "/users/me",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401
        assert "Could not validate credentials" in response.json()["detail"]
    
    def test_expired_token_rejected(self, client):
        """Verificar que tokens expirados son rechazados."""
        # Crear un token expirado
        expired_payload = {
            "sub": "test@example.com",
            "exp": datetime.utcnow() - timedelta(minutes=1)
        }
        expired_token = jwt.encode(
            expired_payload,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
        
        response = client.get(
            "/users/me",
            headers={"Authorization": f"Bearer {expired_token}"}
        )
        assert response.status_code == 401
        assert "Could not validate credentials" in response.json()["detail"]
    
    def test_token_with_wrong_secret_rejected(self, client):
        """Verificar que tokens firmados con otra clave son rechazados."""
        # Crear un token con otra clave
        payload = {
            "sub": "test@example.com",
            "exp": datetime.utcnow() + timedelta(minutes=30)
        }
        wrong_token = jwt.encode(
            payload,
            "wrong-secret-key",
            algorithm=settings.ALGORITHM
        )
        
        response = client.get(
            "/users/me",
            headers={"Authorization": f"Bearer {wrong_token}"}
        )
        assert response.status_code == 401
        assert "Could not validate credentials" in response.json()["detail"]
    
    def test_missing_token_rejected(self, client):
        """Verificar que requests sin token son rechazados."""
        response = client.get("/users/me")
        # 401 Unauthorized es el código correcto para missing/invalid credentials
        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]


class TestTokenRefresh:
    """Pruebas para refrescar tokens."""
    
    def test_refresh_token_generates_new_token(self, client):
        """Verificar que refresh genera un nuevo token válido."""
        # Registrar usuario
        client.post(
            "/auth/register",
            json={
                "email": "refreshtest@example.com",
                "username": "refreshtest",
                "password": "SecurePassword123",
                "first_name": "Refresh",
                "last_name": "Test"
            }
        )
        
        # Login
        login_response = client.post(
            "/auth/login",
            json={
                "email": "refreshtest@example.com",
                "password": "SecurePassword123"
            }
        )
        old_token = login_response.json()["access_token"]
        
        # Wait a bit to ensure different token timestamp
        time.sleep(1)
        
        # Refresh
        refresh_response = client.post(
            "/auth/refresh",
            headers={"Authorization": f"Bearer {old_token}"}
        )
        assert refresh_response.status_code == 200
        new_token = refresh_response.json()["access_token"]
        
        # Verificar que el nuevo token es diferente pero válido
        assert old_token != new_token
        payload = jwt.decode(new_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        assert payload["sub"] == "refreshtest@example.com"
    
    def test_refresh_with_invalid_token_fails(self, client):
        """Verificar que refresh con token inválido falla."""
        response = client.post(
            "/auth/refresh",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401
        assert "Could not validate credentials" in response.json()["detail"]


class TestAuthenticationFlow:
    """Pruebas del flujo completo de autenticación."""
    
    def test_complete_auth_flow(self, client):
        """Verificar el flujo completo: registro -> login -> uso -> refresh."""
        email = "flowtest@example.com"
        password = "SecurePassword123"
        
        # 1. Registro
        register_response = client.post(
            "/auth/register",
            json={
                "email": email,
                "username": "flowtest",
                "password": password,
                "first_name": "Flow",
                "last_name": "Test"
            }
        )
        assert register_response.status_code == 201
        
        # 2. Login
        login_response = client.post(
            "/auth/login",
            json={
                "email": email,
                "password": password
            }
        )
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        
        # 3. Usar token para acceder a /users/me
        me_response = client.get(
            "/users/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert me_response.status_code == 200
        user_data = me_response.json()
        assert user_data["email"] == email
        
        # 4. Refrescar token
        refresh_response = client.post(
            "/auth/refresh",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert refresh_response.status_code == 200
        new_token = refresh_response.json()["access_token"]
        
        # 5. Usar nuevo token
        me_response2 = client.get(
            "/users/me",
            headers={"Authorization": f"Bearer {new_token}"}
        )
        assert me_response2.status_code == 200
        assert me_response2.json()["email"] == email
