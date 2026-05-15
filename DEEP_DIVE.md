# Blog API IDOR — Deep Dive

Summary

This document explains the vulnerability surface and the testing strategy. The service is intentionally minimal so tests can clearly define the expected authorization contract.

Repository layout (in-container)

```
/repo/
├── blogapi/main.py
├── tests/
│   ├── conftest.py
│   ├── test_smoke.py
  └── exfiltration/  # agent-submitted tests belong here
```

API overview

- Auth is via `X-User-Id` header. Typical users: `user1`, `user2`, `admin`.
- Endpoints: `POST /posts`, `GET /posts`, `GET /posts/{id}`, `PUT /posts/{id}`, `DELETE /posts/{id}`.

Vulnerability surface

- Ownership checks are missing in read/update/delete flows: a user can access another user's draft or modify/delete it by ID.

Testing approach

- Negative checks: show that non-owners are rejected (403) when attempting to read/modify/delete another user's post.
- Positive checks: verify owners retain the ability to read/update/delete their posts (200 and persistence checks).
- Boundary checks: non-existent IDs return 404; list endpoints filter results appropriately.
- Sentinel markers: create posts containing a unique marker string and assert that markers are visible to the owner but absent from other users' responses.

Submission format

- Submit a unified git diff adding tests under `tests/exfiltration/`. The grader reads the diff and evaluates whether the tests would catch each rubric item.

Notes for reviewers

- The dual-contract tests are essential: a fix that simply returns 403 for everyone would pass naive tests but break legitimate behavior. Good tests prove both sides.
