import pytest
import asyncio
import sys
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.main import app
from src.db.session import get_db
from src.models.base import Base

# Use SelectorEventLoop on Windows for psycopg compatibility
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Test database URL - use PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:zUBMRKsAxGvyImaTOkvJgvcEVduPWJjT@autorack.proxy.rlwy.net:50610/railway"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for test session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test with transaction rollback."""
    # Start a transaction
    connection = engine.connect()
    transaction = connection.begin()
    
    # Create session bound to this transaction
    session = TestingSessionLocal(bind=connection)
    
    try:
        yield session
    finally:
        session.close()
        # Rollback the transaction to undo all changes
        transaction.rollback()
        connection.close()


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with overridden database dependency."""
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user_data():
    """Sample user data for testing."""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123",
        "first_name": "Test",
        "last_name": "User"
    }
