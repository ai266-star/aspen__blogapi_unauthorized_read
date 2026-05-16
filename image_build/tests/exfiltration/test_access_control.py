"""Access-control regression tests for unauthorized blog post access.

These tests are intentionally strict: they should fail until the API blocks
cross-user GET/PUT/DELETE access and preserves owner flows.
"""

from uuid import uuid4
import json


def create_post(client, user_id, *, title, content, is_draft=False):
    return client.post(
        "/posts",
        headers={"X-User-Id": user_id},
        json={"title": title, "content": content, "is_draft": is_draft},
    )


def get_post(client, user_id, post_id):
    return client.get(f"/posts/{post_id}", headers={"X-User-Id": user_id})


def update_post(client, user_id, post_id, *, title, content, is_draft=False):
    return client.put(
        f"/posts/{post_id}",
        headers={"X-User-Id": user_id},
        json={"title": title, "content": content, "is_draft": is_draft},
    )


def delete_post(client, user_id, post_id):
    return client.delete(f"/posts/{post_id}", headers={"X-User-Id": user_id})


def test_non_owner_get_published_post_does_not_expose_owner_metadata(client):
    sentinel = f"SENTINEL-{uuid4().hex}"
    create_response = create_post(
        client,
        "user1",
        title="Published post",
        content=sentinel,
        is_draft=False,
    )
    assert create_response.status_code == 200
    post_id = create_response.json()["id"]

    owner_response = get_post(client, "user1", post_id)
    assert owner_response.status_code == 200
    assert owner_response.json()["author_id"] == "user1"
    assert owner_response.json()["content"] == sentinel

    cross_user_response = get_post(client, "user2", post_id)
    assert cross_user_response.status_code == 403
    assert cross_user_response.json().get("author_id") != "user1"
    assert sentinel not in json.dumps(cross_user_response.json())


def test_non_owner_cannot_update_another_users_post(client):
    create_response = create_post(
        client,
        "user1",
        title="Editable post",
        content="original content",
        is_draft=False,
    )
    assert create_response.status_code == 200
    post_id = create_response.json()["id"]

    forbidden_update = update_post(
        client,
        "user2",
        post_id,
        title="Hacked title",
        content="hacked content",
        is_draft=False,
    )
    assert forbidden_update.status_code == 403

    owner_view = get_post(client, "user1", post_id)
    assert owner_view.status_code == 200
    assert owner_view.json()["title"] == "Editable post"
    assert owner_view.json()["content"] == "original content"


def test_non_owner_cannot_delete_another_users_post(client):
    create_response = create_post(
        client,
        "user1",
        title="Deletable post",
        content="keep me",
        is_draft=False,
    )
    assert create_response.status_code == 200
    post_id = create_response.json()["id"]

    forbidden_delete = delete_post(client, "user2", post_id)
    assert forbidden_delete.status_code == 403

    owner_view = get_post(client, "user1", post_id)
    assert owner_view.status_code == 200
    assert owner_view.json()["id"] == post_id
    assert owner_view.json()["content"] == "keep me"


def test_owner_can_update_own_post_and_persist_changes(client):
    create_response = create_post(
        client,
        "user1",
        title="Owner update",
        content="old content",
        is_draft=True,
    )
    assert create_response.status_code == 200
    post_id = create_response.json()["id"]

    update_response = update_post(
        client,
        "user1",
        post_id,
        title="Owner update v2",
        content="new content",
        is_draft=False,
    )
    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Owner update v2"
    assert update_response.json()["content"] == "new content"

    follow_up_read = get_post(client, "user1", post_id)
    assert follow_up_read.status_code == 200
    assert follow_up_read.json()["title"] == "Owner update v2"
    assert follow_up_read.json()["content"] == "new content"
    assert follow_up_read.json()["author_id"] == "user1"


def test_owner_can_delete_own_post_and_remove_it_from_owner_view(client):
    create_response = create_post(
        client,
        "user1",
        title="Owner delete",
        content="delete me",
        is_draft=False,
    )
    assert create_response.status_code == 200
    post_id = create_response.json()["id"]

    delete_response = delete_post(client, "user1", post_id)
    assert delete_response.status_code == 200

    follow_up_read = get_post(client, "user1", post_id)
    assert follow_up_read.status_code == 404

    owner_list = client.get("/posts", headers={"X-User-Id": "user1"})
    assert owner_list.status_code == 200
    assert all(post["id"] != post_id for post in owner_list.json())