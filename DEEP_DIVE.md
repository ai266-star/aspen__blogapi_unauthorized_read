# Blog API IDOR: The Full Picture

## Five-Second Summary

A blog API has an authorization bug. Users can get access they should not have, and you need to write a test suite that catches this leak but also proves that legitimate users (who do own posts) can still do their thing.

---

## Why This Task Exists (And Why Test-Authoring Matters)

Let me give you the reasoning. Authorization bugs are tricky because there are many ways to fix them *correctly*:

- Add middleware that checks permissions before any endpoint runs
- Put explicit checks in each endpoint
- Use decorators to guard functions
- Implement role-based access control (RBAC)
- Use database row-level security

All of these approaches work. But they look totally different in the code. So instead of asking "can you fix this bug," we ask "can you write tests that *specify* what the fix must do?"

Here's where it gets interesting: You could write tests that just say "non-owners get 403." Someone could then "fix" the bug by denying access to *everyone*. That would pass your tests but completely break the application. 

The real skill is writing tests that do *both*:
1. **Catch the leak**: Non-owners actually get rejected
2. **Prevent over-blocking**: Owners can still use the API normally

That's the dual-contract. A test suite with both is discriminative. One that only checks one side is useless.

---

## What You're Looking At

### The Repository

Inside the Docker container:

```
/repo/
├── blogapi/main.py         (350 lines, has the IDOR bug)
├── tests/
│   ├── conftest.py         (pytest setup, fixtures)
│   ├── test_smoke.py       (8 tests of legitimate flows)
│   └── exfiltration/       (← where agents write tests)
├── pytest.ini
└── requirements.txt
```

The main.py file is intentionally buggy. The conftest.py and test_smoke.py define what "legitimate API usage" looks like.

### The API (5 Endpoints)

Authentication is via the `X-User-Id` header. Valid users: `user1`, `user2`, `admin`. No passwords, just claims an identity.

**POST /posts** — Create a post:
```
POST /posts HTTP/1.1
X-User-Id: user1
Content-Type: application/json

{
  "title": "My First Post",
  "content": "Some interesting text",
  "is_draft": true
}

Response 200:
{
  "id": 1,
  "title": "My First Post",
  "content": "Some interesting text",
  "author_id": "user1",
  "is_draft": true,
  "created_at": "2026-05-10T12:00:00"
}
```

**GET /posts** — List all posts:
```
GET /posts HTTP/1.1
X-User-Id: user1

Response 200:
[
  {"id": 1, "title": "My First Post", "author_id": "user1", "is_draft": true},
  {"id": 2, "title": "Someone Else's Draft", "author_id": "user2", "is_draft": true},
  ...
]
```

(BUG: Shows other users' drafts!)

**GET /posts/{id}** — Read a single post:
```
GET /posts/2 HTTP/1.1
X-User-Id: user1

Response 200 (SHOULD BE 403!):
{"id": 2, "title": "Someone Else's Draft", "author_id": "user2", ...}
```

(BUG: No ownership check!)

**PUT /posts/{id}** — Modify a post:
```
PUT /posts/2 HTTP/1.1
X-User-Id: user1
Content-Type: application/json

{"title": "Hacked!", "content": "Oops", "is_draft": false}

Response 200 (SHOULD BE 403!):
{"id": 2, "title": "Hacked!", ...}
```

(BUG: User1 just hijacked user2's post!)

**DELETE /posts/{id}** — Delete:
```
DELETE /posts/2 HTTP/1.1
X-User-Id: user1

Response 200 (SHOULD BE 403!):
{"message": "Post deleted"}
```

(BUG: Post is gone, and it wasn't even user1's post!)

---

## Why Someone Would Actually Test This

You're the API maintainer. A user files this bug report:

> "I created a draft post, and while testing the API, I noticed I could read other people's drafts by guessing their post IDs. I was able to edit them too. This is a serious issue."

Your first reaction: Panic. This is a real authorization leak.

Your second reaction: Wait, I have no tests for this. If I add fixes, how do I know I didn't break legitimate use cases?

So you need a test suite that:
- ✅ **Proves the vulnerability exists** (non-owners are blocked)
- ✅ **Proves legitimate use still works** (owners can read/edit/delete their own posts)
- ✅ **Covers edge cases** (what about non-existent posts? Public vs. draft?)

A model that writes this kind of comprehensive suite understands the threat, not just the surface-level API.

---

## How the Rubric Breaks Down

### The 5 "Catch the Leak" Items (15 points)

These test that the vulnerability is fixed:

1. **Draft isolation** (RUB-001): User1 cannot GET user2's draft post. Should return 403, not 200.
   - Test: Create draft as user2, try to read as user1, assert 403.

2. **Metadata doesn't leak** (RUB-002): Even published posts shouldn't leak internal metadata when accessed by non-owners.
   - Test: GET someone else's post, verify author_id field is either absent or redacted.

3. **List endpoint filtering** (RUB-003): GET /posts should not include other users' content in the response.
   - Test: Create drafts for user1 and user2, list as user1, verify only your drafts appear.

4. **Update blocked** (RUB-004): User1 cannot PUT (modify) user2's post. Should return 403.
   - Test: Create as user2, try to modify the title as user1, assert 403.

5. **Delete blocked** (RUB-005): User1 cannot DELETE user2's post. Should return 403, and post must still exist.
   - Test: Delete as user1, assert 403, verify post still exists in database.

### The 4 "Don't Break Legitimate Use" Items (12 points)

These test that fixes don't over-block:

6. **Owner can read** (RUB-006): User2 *can* read their own draft. Must return 200 with content.
7. **Owner can update** (RUB-007): User2 *can* modify their own post. Must return 200.
8. **Owner can delete** (RUB-008): User2 *can* delete their own post. Must return 200 and post disappears.
9. **Owner can list** (RUB-009): Any user can call GET /posts and get their posts back (even if filtered).

### The 2 "Boundary & Quality" Items (3 points)

10. **404 vs 403 distinction** (RUB-010): Non-existent posts return 404, not 403 or 500. This is a boundary condition test.

11. **Data doesn't leak in responses** (RUB-011): If you create posts with sentinel strings (like "SUPER_SECRET_MARKER_12345"), verify those strings don't appear in responses from other users. This is a test-quality assertion.

---

## Understanding Model Performance

After running calibration, you'll see numbers like:

```
Model              N    Mean Score  Saturation
Claude Opus       12    0.85         8/12
Gemini 3.1        4     0.42         1/4
```

**Mean Score of 0.85** = Average of 25/29 points. That's strong. Catches most items.

**Saturation of 8/12** = 8 out of 12 runs hit 100% (29/29). Shows consistency.

**Per-rubric breakdown** (N=12 frontier runs):
```
RUB-001 (draft redaction)     11/12 (92%)  ← Easy, frontier saturated
RUB-002 (metadata isolation)  10/12 (83%)  ← Easy
RUB-003 (list filtering)      9/12  (75%)  ← Medium
RUB-004 (update ownership)    7/12  (58%)  ← Hard
RUB-005 (delete ownership)    6/12  (50%)  ← Hard
RUB-006 (owner can read)      9/12  (75%)  ← Medium (regression)
RUB-007 (owner can update)    8/12  (67%)  ← Medium
RUB-008 (owner can delete)    7/12  (58%)  ← Hard
RUB-009 (owner can list)      10/12 (83%)  ← Easy (regression)
RUB-010 (404 boundary)        5/12  (42%)  ← Hard
RUB-011 (sentinel markers)    2/12  (17%)  ← Very hard (top-of-frontier)
```

If the spread looks like this, the task is **DISCRIMINATIVE**. Different models show different strengths. Frontier saturates the easy items, gets 50-83% on the medium ones, and barely touches the hard stuff.

---

## What a Good Test Looks Like

Let's say you're testing RUB-001 (draft redaction):

**Good test**:
```python
def test_non_owner_cannot_read_draft():
    # User2 creates a draft
    draft = client.post("/posts", 
        json={
            "title": "Secret Draft",
            "content": "Only for me",
            "is_draft": True
        },
        headers={"X-User-Id": "user2"}
    ).json()
    
    # User1 tries to read it
    response = client.get(f"/posts/{draft['id']}", 
        headers={"X-User-Id": "user1"})
    
    # Must return 403, not 200
    assert response.status_code == 403, \
        f"Expected 403, got {response.status_code}"
```

**Bad test**:
```python
def test_api_works():
    response = client.get("/posts")
    assert response.status_code in [200, 403]  # Too vague
```

The good test specifically exercises the vulnerability (draft + cross-owner) and asserts the right boundary (403). The bad test is so generic it would pass even if the bug exists.

---

## Submission Format

When you're done, submit a unified diff. Git format:

```
diff --git a/tests/exfiltration/test_access_control.py b/tests/exfiltration/test_access_control.py
new file mode 100644
--- /dev/null
+++ b/tests/exfiltration/test_access_control.py
@@ -0,0 +1,150 @@
+# Your test code here
+def test_non_owner_cannot_read_draft():
+    ...
```

The judge reads your tests as text (never runs them) and grades based on whether they would catch each rubric item.

---

## Key Takeaway

This task is testing whether you can think in dual-contract terms:
- **What should fail?** (Non-owner access)
- **What should succeed?** (Owner access)
- **What are the edge cases?** (404 vs 403, data leakage, etc.)

Write tests that answer all three. That's how you score well on this task.
