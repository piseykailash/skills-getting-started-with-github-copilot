"""
Pytest configuration and fixtures for FastAPI tests
"""
import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add src directory to path to import app module
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app


@pytest.fixture
def client():
    """
    Fixture that provides a TestClient for making requests to the FastAPI app.
    """
    return TestClient(app)


@pytest.fixture
def sample_activity_data():
    """
    Fixture providing sample activity data for testing.
    """
    return {
        "activity_name": "Chess Club",
        "email": "test@mergington.edu"
    }
