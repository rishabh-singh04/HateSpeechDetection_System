# tests/test_api.py
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_moderate_endpoint():
    response = client.post("/moderate", json={"text": "Test hate speech"})
    assert response.status_code == 200
    assert "action" in response.json()