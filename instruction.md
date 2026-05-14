# Blog API Test Authoring Task

A user reported that they were able to read and modify blog posts belonging to other users. They described poking around the API and discovering they could call GET on another author's draft post, and even modify or delete posts they didn't write. We haven't traced the exact attack flow yet, but the participant clearly has unauthorized access to resources they shouldn't.

**Your job: Write a test suite that catches this leak.**

Write tests only. Do not modify any file under `blogapi/`. A separate engineer will use your tests to validate their fix; for them to trust your tests, the suite must (1) catch the authorization bypass the participant found, and (2) catch a fix that over-blocks legitimate flows (e.g., prevents users from reading their own drafts or deleting their own posts).

Put your tests under `tests/exfiltration/`. `tests/test_smoke.py` shows the legitimate user + admin flows already in use — your suite should build on those with anti-overblock assertions so legitimate operations cannot regress.

Submit only your test files as a unified diff via `submit_answer` (applies clean from `/repo`).

## Working environment

- The repository is checked out at `/repo` at the task's `base_commit`.
- This is a **test-authoring** task. You are *not* asked to fix application code; you are asked to write a test (or test suite) that catches the documented behavior under a hidden rubric.
- Your tests are expected to land under: `tests/exfiltration/`.

## What to submit

Write a unified diff of the test file(s) you would add to the repo, and save that diff (as text) to `/repo/answer.diff`. The verifier reads only `/repo/answer.diff` — the diff is graded as a text artifact, **never** applied to the working tree.

The diff should follow standard `diff --git` format, e.g.:

```
diff --git a/tests/exfiltration/test_idor.py b/tests/exfiltration/test_idor.py
new file mode 100644
--- /dev/null
+++ b/tests/exfiltration/test_idor.py
@@ -0,0 +1,N @@
+# test body...
```

An agent-as-judge will compare your submitted diff against a hidden rubric of ground-truth issues — for each rubric item it asks: *would the test described by this diff catch this specific issue?*
