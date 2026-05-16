import json
import uuid


def _create_post(client, user, title="t", content="c", is_draft=True):
    r = client.post("/posts", headers={"X-User-Id": user}, json={"title": title, "content": content, "is_draft": is_draft})
    assert r.status_code == 200
    return r.json()


def test_non_owner_draft_detail_forbidden_strict(client):
    sentinel = f"SENTINEL-{uuid.uuid4().hex[:8]}"
    p = _create_post(client, "user1", title="d", content=sentinel, is_draft=True)
    pid = p["id"]

    # owner sees it
    r_owner = client.get(f"/posts/{pid}", headers={"X-User-Id": "user1"})
    assert r_owner.status_code == 200
    got = r_owner.json()
    assert got["author_id"] == "user1"
    assert got["is_draft"] is True
    assert sentinel in got["content"]

    # non-owner must be strictly forbidden (403)
    r_cross = client.get(f"/posts/{pid}", headers={"X-User-Id": "user2"})
    assert r_cross.status_code == 403
    body = json.dumps(r_cross.json())
    assert sentinel not in body
    assert 'author_id' not in r_cross.json()


def test_non_owner_published_detail_forbidden_strict(client):
    # Tighten expectation: even published detail access by non-owner should be forbidden (403)
    sentinel = f"SENTINEL-{uuid.uuid4().hex[:8]}"
    p = _create_post(client, "user1", title="pub", content=sentinel, is_draft=False)
    pid = p["id"]

    assert client.get(f"/posts/{pid}", headers={"X-User-Id": "user1"}).status_code == 200

    cross = client.get(f"/posts/{pid}", headers={"X-User-Id": "user2"})
    # Hard requirement: 403
    assert cross.status_code == 403
    assert sentinel not in json.dumps(cross.json())
    assert 'author_id' not in cross.json()


def test_non_owner_put_blocked_and_owner_unchanged(client):
    p = _create_post(client, "user1", title="t", content="orig", is_draft=False)
    pid = p['id']
    up = client.put(f"/posts/{pid}", headers={"X-User-Id": "user2"}, json={"title":"x","content":"y","is_draft":False})
    assert up.status_code == 403
    # owner still sees original
    got = client.get(f"/posts/{pid}", headers={"X-User-Id": "user1"})
    assert got.status_code == 200
    assert got.json()["content"] == "orig"


def test_non_owner_delete_blocked_and_owner_remains(client):
    p = _create_post(client, "user1", title="tdel", content="keep", is_draft=False)
    pid = p['id']
    d = client.delete(f"/posts/{pid}", headers={"X-User-Id": "user2"})
    assert d.status_code == 403
    assert client.get(f"/posts/{pid}", headers={"X-User-Id": "user1"}).status_code == 200


def test_owner_put_persists(client):
    p = _create_post(client, "user1", title="o", content="old", is_draft=True)
    pid = p['id']
    up = client.put(f"/posts/{pid}", headers={"X-User-Id": "user1"}, json={"title":"t2","content":"new","is_draft":False})
    assert up.status_code == 200
    assert client.get(f"/posts/{pid}", headers={"X-User-Id": "user1"}).json()["content"] == "new"


def test_owner_delete_removes_for_owner(client):
    p = _create_post(client, "user1", title="t", content="delme", is_draft=False)
    pid = p['id']
    assert client.delete(f"/posts/{pid}", headers={"X-User-Id": "user1"}).status_code == 200
    assert client.get(f"/posts/{pid}", headers={"X-User-Id": "user1"}).status_code == 404
    # ensure not in owner's list
    lst = client.get('/posts', headers={"X-User-Id": "user1"})
    assert all(item.get('id') != pid for item in lst.json())


def test_list_excludes_others_drafts_and_no_metadata_leak(client):
    sentinel = f"SENTINEL-{uuid.uuid4().hex[:8]}"
    _create_post(client, "user1", title="d2", content=sentinel, is_draft=True)
    lst = client.get('/posts', headers={"X-User-Id": "user2"})
    assert lst.status_code == 200
    body = json.dumps(lst.json())
    assert sentinel not in body
    for it in lst.json():
        # ensure no drafts belonging to user1 leak into user2's list
        assert not (it.get('author_id') == 'user1' and it.get('is_draft') is True)


def test_boundary_999999_returns_404_for_all(client):
    for u in ("user1", "user2"):
        assert client.get('/posts/999999', headers={"X-User-Id": u}).status_code == 404


def test_sentinel_visible_only_to_owner_in_list_and_detail(client):
    sentinel = f"SENTINEL-{uuid.uuid4().hex[:8]}"
    p = _create_post(client, "user1", title="s", content=sentinel, is_draft=False)
    pid = p['id']
    # owner detail
    od = client.get(f"/posts/{pid}", headers={"X-User-Id": "user1"})
    assert od.status_code == 200
    assert sentinel in od.json().get('content', '')
    # owner list contains it
    ol = client.get('/posts', headers={"X-User-Id": "user1"})
    assert any(sentinel in it.get('content', '') for it in ol.json())
    # non-owner detail forbidden
    nd = client.get(f"/posts/{pid}", headers={"X-User-Id": "user2"})
    assert nd.status_code == 403
    assert sentinel not in json.dumps(nd.json())
    # non-owner list must not contain the sentinel
    nl = client.get('/posts', headers={"X-User-Id": "user2"})
    assert sentinel not in json.dumps(nl.json())
