# Minimal conftest - test fixtures
import pytest
from fastapi.testclient import TestClient
from blogapi.main import app, posts_db


@pytest.fixture
def client():
    """Test client with reset database."""
    posts_db.clear()
    return TestClient(app)
