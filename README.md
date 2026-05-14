# Blog API IDOR Task

This pack is a test-authoring exercise. The API has a straightforward authorization bug, and the goal is to write tests that catch it without breaking normal user behavior.

## Tasks In This Pack

| Item | What it is | Status |
|---|---|---|
| Substrate | FastAPI blog API with an IDOR bug | Done |
| Rubric | 11 items total | Done |
| Prompt | `prompt.txt` for the test-writing agent | Done |
| Reasoning | `reasoning.txt` threat model and scoring notes | Done |
| Deep dive | `DEEP_DIVE.md` walkthrough for humans | Done |
| Build context | `image_build/` Docker image input | Done |

## Quick Context

The API is small on purpose. It has five endpoints and uses an `X-User-Id` header for auth:

- `POST /posts` creates a post
- `GET /posts` lists posts
- `GET /posts/{id}` reads one post
- `PUT /posts/{id}` updates a post
- `DELETE /posts/{id}` deletes a post

The bug is simple: ownership checks are missing. That means one user can reach another user's content. The test suite needs to catch that behavior and also make sure owners can still use the API normally.

## Calibration Results

Calibration has not been run yet, so this is still a placeholder section. Once it runs, I’ll fill in the actual numbers here.

Target band for Qwen 3.5 is 25-50 percent. This version is intentionally a bit more inferential than the first cut, so the model has to discover the ownership boundary instead of being handed the exact failure mode.

| Model | N | Mean reward | Saturation rate | Pass-rate | Distribution |
|---|---:|---:|---:|---:|---|
| Claude Opus (frontier) | 12 | pending | pending | pending | pending |
| Gemini 3.1 Pro (secondary) | 4 | pending | pending | pending | pending |

### Gemini N=10 Stability

I’m keeping this section in place even before calibration so the final report has the right shape.

| Threshold | pass@1 | pass@3 | pass@5 | pass@10 |
|---|---:|---:|---:|---:|
| Reward threshold A | pending | pending | pending | pending |
| Reward threshold B | pending | pending | pending | pending |

## Per-Rubric Catch Rates

These are the 12-run catch rates I’ll use after calibration. The ladder should show a mix of easy, medium, and hard items rather than everything collapsing to the same score.

| Rubric | Catch rate over N=12 | Notes |
|---|---:|---|
| RUB-001 | pending | draft redaction |
| RUB-002 | pending | metadata isolation |
| RUB-003 | pending | list filtering |
| RUB-004 | pending | update ownership |
| RUB-005 | pending | delete ownership |
| RUB-006 | pending | owner can read |
| RUB-007 | pending | owner can update |
| RUB-008 | pending | owner can delete |
| RUB-009 | pending | owner can list |
| RUB-010 | pending | 404 boundary |
| RUB-011 | pending | sentinel marker check, top-of-frontier candidate |

## Discrimination Ladder

The rubric is supposed to have a clear spread:

- Front-of-frontier items should be easy for stronger models.
- Mid-tier items should separate models that understand the access-control story from models that only skim it.
- The hardest item should still be possible, but not trivial.

That mix is what makes the task useful. If every item lands in the same bucket, the rubric is too flat.

## Verdict

Verdict: pending calibration.

Once the runs are in, this will say one of:

- `DISCRIMINATIVE`
- `UNDER-CALIBRATED`
- `FLAKY`

My expectation is that the task should end up in the discriminative range, but I’m not calling it yet without the actual runs.

## Image Tag and Digest

| Field | Value |
|---|---|
| Image tag | `ai266/aspen-blogapi:idor-v1` |
| Digest | `sha256:b4ac9d79d943ebc2194bffc586b6db07fb0f71b508fdd45e65dc6fcf53f7b7e5` |
| Platform | `linux/amd64` |
| Base image | `python:3.12-slim` |

## Aspen Gotchas

- The image is the working environment, so the Docker build has to be right.
- There is no in-sandbox verifier for the hidden behavior; the smoke test is the load-bearing check.
- Prompt quality matters a lot. If the prompt gives away the structure, the task becomes easier than it should be.
- The test suite has to protect against over-blocking as well as the leak itself.
- Keep old pipeline-name strings out of the submission.

## Folder Layout

```
aspen__blogapi_unauthorized_read_001/
├── prompt.txt
├── task_config.json
├── reasoning.txt
├── README.md
├── DEEP_DIVE.md
└── image_build/
    ├── Dockerfile
    ├── requirements.txt
    ├── pytest.ini
    ├── blogapi/
    │   ├── __init__.py
    │   └── main.py
    └── tests/
        ├── conftest.py
        ├── test_smoke.py
        └── exfiltration/
```

## Before Submission

- Push the Docker image to the private `ai266/` registry.
- Fill in calibration numbers here once the runs finish.
- Make sure peer QC is happy with the file structure and rubric shape.
