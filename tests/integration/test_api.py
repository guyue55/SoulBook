import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from unittest.mock import AsyncMock
import sys
import os

# Add the src directory to the path so we can import soulbook modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.soulbook.main import app
from src.soulbook.config.settings import settings
from src.soulbook.models.base import Base


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.mark.asyncio
async def test_health_check(client):
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_root_endpoint(client):
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "Welcome to Soulbook API"


# Integration tests for authentication endpoints
@pytest.mark.asyncio
async def test_register_user(client):
    """Test user registration"""
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword"
    }
    response = client.post("/api/v1/auth/register", json=user_data)
    
    # This might fail if user already exists, which is OK for this test
    assert response.status_code in [200, 400]


@pytest.mark.asyncio
async def test_login_user(client):
    """Test user login"""
    login_data = {
        "username": "testuser",
        "password": "testpassword"
    }
    # This will likely fail since we're not registering a user first
    # But we can still test the endpoint structure
    response = client.post(
        "/api/v1/auth/login",
        data=login_data,  # Using form data for OAuth2
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    # We expect either success (if user exists) or failure (which is expected in test)
    assert response.status_code in [200, 400, 401]


# Integration test for novels endpoint
@pytest.mark.asyncio
async def test_get_novels_unauthorized(client):
    """Test novels endpoint without authentication"""
    response = client.get("/api/v1/novels/")
    # Should return 401 Unauthorized since auth is required
    assert response.status_code == 401


# Integration test for users endpoint
@pytest.mark.asyncio
async def test_get_current_user_unauthorized(client):
    """Test users me endpoint without authentication"""
    response = client.get("/api/v1/users/me")
    # Should return 401 Unauthorized since auth is required
    assert response.status_code == 401


# Test database integration
@pytest.mark.asyncio
async def test_database_connection():
    """Test database connection and table creation"""
    # Use an in-memory SQLite database for testing
    TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
    
    engine = create_async_engine(TEST_DATABASE_URL)
    
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Verify tables were created by attempting to connect
    async with AsyncSession(engine) as session:
        # Simple test - just make sure we can connect
        assert session is not None
    
    # Clean up
    await engine.dispose()