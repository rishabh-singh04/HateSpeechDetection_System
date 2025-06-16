# conftest.py
import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# Add project root to PYTHONPATH
from app.main import app
from app.db.base import Base

@pytest.fixture(scope="module")
def test_app():
    # Override any test configurations here if needed
    yield app

@pytest.fixture(scope="module")
def test_client(test_app):
    with TestClient(test_app) as client:
        yield client

@pytest.fixture
def db_session():
    # Setup in-memory SQLite database
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    yield session
    
    # Teardown
    session.close()
    Base.metadata.drop_all(engine)

@pytest.fixture
def auth_headers(test_client):
    # Mock login response
    return {
        "Authorization": "Bearer mock_token",
        "Content-Type": "application/json"
    }