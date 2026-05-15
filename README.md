# Blog API IDOR Task

This repository contains a small FastAPI blog service with an intentional ownership-check gap. The exercise asks contributors to author tests that prove the missing authorization and also prevent over-correction.

Quickstart

1. Build the test image (from `image_build/`):

```bash
cd image_build
docker build -t ai266/aspen-blogapi:idor-v1 .
```

2. Run the service (optional for local testing):

```bash
docker run --rm -p 8000:8000 ai266/aspen-blogapi:idor-v1
# then run pytest from the project root to execute the smoke tests against a running server
```

3. The judge expects a git diff containing new tests under `tests/exfiltration/`.

Image metadata

| Field | Value |
|---|---|
| Image tag | `micro1ai/aspen-blogapi:idor-v1` |
| Digest | `sha256:b4ac9d79d943ebc2194bffc586b6db07fb0f71b508fdd45e65dc6fcf53f7b7e5` |
| Platform | `linux/amd64` |

What to submit

- `prompt.txt` — instructions for an agent to write tests.
- `task_config.json` — pipeline metadata and rubric.
- `reasoning.txt` — threat model and scoring rationale.
- `DEEP_DIVE.md` — human-oriented overview and test guidance.
- `image_build/Dockerfile` — build instructions for the sandbox image.

Folder layout

```
aspen__blogapi_unauthorized_read/
├── prompt.txt
├── task_config.json
├── reasoning.txt
├── README.md
├── DEEP_DIVE.md
└── image_build/
    ├── Dockerfile
    └── ...
```

Next steps

- If you want, run the calibration harness and paste results here; I can summarize and suggest rubric tweaks.
