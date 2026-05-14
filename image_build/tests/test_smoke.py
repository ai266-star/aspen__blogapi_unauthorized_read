"""
Smoke test: Legitimate blog API flows that should continue working.
Tests that users can create, read, and manage their own posts.
"""
import pytest
from fastapi.testclient import TestClient
from blogapi.main import app, posts_db


@pytest.fixture
def client():
    """Create a test client."""
    # Reset DB before each test
    posts_db.clear()
    posts_db.update({})
    return TestClient(app)


def test_health_check(client):
    """Verify API is healthy."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_user1_create_own_post(client):
    """User1 can create their own post."""
    response = client.post(
        "/posts",
        json={"title": "My Post", "content": "Hello world", "is_draft": False},
        headers={"X-User-Id": "user1"}
    )
    assert response.status_code == 200
    post = response.json()
    assert post["title"] == "My Post"
    assert post["author_id"] == "user1"
    assert post["is_draft"] is False


def test_user1_read_own_post(client):
    """User1 can read their own post."""
    # Create post as user1
    create_response = client.post(
        "/posts",
        json={"title": "My Secret", "content": "Private stuff", "is_draft": True},
        headers={"X-User-Id": "user1"}
    )
    post_id = create_response.json()["id"]
    
    # Read it back
    response = client.get(f"/posts/{post_id}", headers={"X-User-Id": "user1"})
    assert response.status_code == 200
    assert response.json()["content"] == "Private stuff"


def test_user1_list_posts_shows_published(client):
    """User1 can list posts (should see published posts)."""
    # Create a published post
    client.post(
        "/posts",
        json={"title": "Published", "content": "Public content", "is_draft": False},
        headers={"X-User-Id": "user1"}
    )
    
    response = client.get("/posts", headers={"X-User-Id": "user1"})
    assert response.status_code == 200
    posts = response.json()
    assert len(posts) >= 1


def test_user1_update_own_post(client):
    """User1 can update their own post."""
    # Create post
    create_response = client.post(
        "/posts",
        json={"title": "Original", "content": "Old content"},
        headers={"X-User-Id": "user1"}
    )
    post_id = create_response.json()["id"]
    
    # Update it
    update_response = client.put(
        f"/posts/{post_id}",
        json={"title": "Updated", "content": "New content", "is_draft": False},
        headers={"X-User-Id": "user1"}
    )
    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Updated"


def test_user1_delete_own_post(client):
    """User1 can delete their own post."""
    # Create post
    create_response = client.post(
        "/posts",
        json={"title": "Temp", "content": "To delete"},
        headers={"X-User-Id": "user1"}
    )
    post_id = create_response.json()["id"]
    
    # Delete it
    response = client.delete(f"/posts/{post_id}", headers={"X-User-Id": "user1"})
    assert response.status_code == 200
    
    # Verify it's gone
    get_response = client.get(f"/posts/{post_id}", headers={"X-User-Id": "user1"})
    assert get_response.status_code == 404


def test_unauthorized_without_user_id(client):
    """Requests without user ID are rejected."""
    response = client.get("/posts")
    assert response.status_code == 401


def test_invalid_user_id(client):
    """Requests with invalid user ID are rejected."""
    response = client.get("/posts", headers={"X-User-Id": "unknown_user"})
    assert response.status_code == 401
