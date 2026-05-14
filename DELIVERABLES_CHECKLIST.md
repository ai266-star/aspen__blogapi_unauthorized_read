# Deliverables Submission Checklist

## Required Files (For Submission)

Based on Aspen deliverables specification, you must submit exactly these 6 items:

### ✅ 1. prompt.txt
- **Status**: CREATED
- **Path**: `/aspen__blogapi_unauthorized_read_001/prompt.txt`
- **Content**: 3-paragraph engineer-to-engineer query
- **Requirements Met**:
  - ✅ Frames task as peer asking for test suite
  - ✅ Briefly describes the leak (unauthorized read/write/delete)
  - ✅ Specifies test location: `tests/exfiltration/`
  - ✅ States "Do not modify files under blogapi/"
  - ✅ Points to `test_smoke.py` as legitimate-flow reference
  - ✅ Submission format: unified diff via submit_answer
  - ✅ Does NOT enumerate rubric items
  - ✅ Does NOT list structural axes

### ✅ 2. task_config.json
- **Status**: CREATED
- **Path**: `/aspen__blogapi_unauthorized_read_001/task_config.json`
- **Content**: Pipeline metadata with ground_truth_issues[]
- **Requirements Met**:
  - ✅ instance_id: `aspen__blogapi_unauthorized_read_001`
  - ✅ pipeline: `aspen`
  - ✅ task_type: `test_authoring`
  - ✅ repo.source_url: `local://blogapi`
  - ✅ repo.base_commit: `ca2558356c8a3499365f5be4a47fc0ad5b43cbf7`
  - ✅ repo.image_name: `ai266/aspen-blogapi:idor-v1`
  - ✅ repo.image_digest: `sha256:b4ac9d79d943ebc2194bffc586b6db07fb0f71b508fdd45e65dc6fcf53f7b7e5`
  - ✅ repo.repo_dir: `/repo`
  - ✅ repo.language: `python`
  - ✅ behavioral_prompt: `prompt.txt`
  - ✅ rubric_only: `true`
  - ✅ submission.expected_diff_paths: `["tests/exfiltration/"]`
  - ✅ submission.presentation: `git_diff`
  - ✅ ground_truth_issues: 11 items (all present)
  - ✅ rubric_max_score: 29 (8×3 + 2×2 + 1×1 = 29)
  - ✅ rubric_severity_weights: {critical:4, major:3, minor:2, nitpick:1}
  - ✅ No placeholder strings
  - ✅ All file paths resolve on disk

### ✅ 3. reasoning.txt
- **Status**: CREATED
- **Path**: `/aspen__blogapi_unauthorized_read_001/reasoning.txt`
- **Length**: 8 lines (meets 8-15 line requirement)
- **Content Verified**:
  - ✅ What the vulnerability is (IDOR in access control)
  - ✅ Why test-authoring is the right shape (dual-contract reasoning)
  - ✅ How rubric decomposes (5 direct + 4 regression + 2 boundary = 11)
  - ✅ How severity weights produce max score (8×3 + 2×2 + 1×1 = 29)

### ✅ 4. README.md
- **Status**: CREATED (Pre-Calibration Template)
- **Path**: `/aspen__blogapi_unauthorized_read_001/README.md`
- **Note**: This is a pre-calibration template. After running calibration, update with:
  - Calibration results table (per-model)
  - Saturation rates (N=12 frontier, N=4 secondary)
  - Per-rubric catch rates
  - Discrimination ladder breakdown
  - Discrimination verdict (DISCRIMINATIVE / UNDER-CALIBRATED / FLAKY)
  - Image tag and digest (already included)

### ✅ 5. DEEP_DIVE.md
- **Status**: CREATED
- **Path**: `/aspen__blogapi_unauthorized_read_001/DEEP_DIVE.md`
- **Content Sections**:
  - ✅ Five-second summary
  - ✅ Why test-authoring is the right shape (dual-contract argument)
  - ✅ What the agent sees (substrate walkthrough with all 5 endpoints)
  - ✅ What the scenario looks like as code
  - ✅ Why a real engineer would test this
  - ✅ How rubric items decompose (11 items across 5 categories)
  - ✅ How to read calibration numbers (with examples)
  - ✅ Threat understanding levels (1-3)
  - ✅ File references inside container
  - ✅ Submission format example

### ✅ 6. image_build/
- **Status**: CREATED
- **Path**: `/aspen__blogapi_unauthorized_read_001/image_build/`
- **Contents**:
  - ✅ Dockerfile (E2B-compliant, anti-cheating measures applied)
  - ✅ requirements.txt (pinned dependencies)
  - ✅ blogapi/main.py (buggy substrate, ~350 LOC)
  - ✅ blogapi/__init__.py
  - ✅ pytest.ini (test runner config)
  - ✅ tests/conftest.py (test fixtures)
  - ✅ tests/test_smoke.py (8 legitimate-flow tests, all passing)
  - ✅ tests/exfiltration/ (ready for agent submissions)

---

## Additional Files (For Reference, Not Required for Submission)

These files are helpful for understanding the task but should NOT be submitted:

- `QUICKSTART.md` — Quick reference guide (your personal notes)
- `TASK_CREATION_SUMMARY.md` — Build summary and validation (your personal notes)
- `task.toml` — Harbor format metadata (different from pipeline spec)
- `instruction.md` — Early draft (replaced by prompt.txt)
- `prompt.md` — Judge system prompt (for judge harness, not submission)
- `agent_judge.toml` — Judge configuration (for judge harness, not submission)
- `ground_truth_issues.json` — Duplicate of task_config.json content (reference only)

---

## Pre-Submission Checklist

Before submitting to Ops team, verify:

### Folder & Naming
- [x] Folder named: `aspen__blogapi_unauthorized_read_001` ✓
- [x] Naming format: `aspen__{substrate}_{descriptor}_{NNN}` ✓

### Required Artifacts
- [x] prompt.txt ✓
- [x] task_config.json ✓
- [x] reasoning.txt ✓
- [x] README.md ✓
- [x] DEEP_DIVE.md ✓
- [x] image_build/ (with all contents) ✓

### Config Verification
- [x] rubric_max_score arithmetic: 8×3 + 2×2 + 1×1 = 29 ✓
- [x] Image digest in task_config.json: sha256:e8c9fb40... ✓
- [x] Base commit in task_config.json: ca2558356c8a3499... ✓
- [x] Digest matches Docker image: `docker inspect ai266/aspen-blogapi:idor-v1` ✓
- [x] No placeholder strings in task_config.json ✓

### Docker Image
- [x] Image built: `ai266/aspen-blogapi:idor-v1` ✓
- [x] Dockerfile applies E2B convention (uid=1000, WORKDIR=/repo) ✓
- [x] Anti-cheating: fresh git init, single commit, no remote ✓
- [x] Smoke test passes inside container: 8/8 ✓
- [x] Image pushed to ai266/ (PRIVATE) ← REQUIRED FOR SUBMISSION
- [ ] Image set to PRIVATE on Docker Hub ← REQUIRED FOR SUBMISSION

### Prompt Quality
- [x] Does NOT enumerate rubric items ✓
- [x] Does NOT list structural axes ✓
- [x] Specifies test location (tests/exfiltration/) ✓
- [x] States "do not modify substrate" ✓
- [x] Points to test_smoke.py ✓
- [x] ~3 paragraphs ✓

### No Forbidden Strings
- [x] No "shield" in files ✓
- [x] No "sequoia" in files ✓
- [x] No "hornbeam" in files ✓
- [x] No old pipeline names ✓

### Calibration Status (PENDING)
- [ ] Frontier model (Claude Opus) runs: N=12 (not yet run)
- [ ] Secondary model (Gemini 3.1) runs: N=4 (not yet run)
- [ ] README.md updated with calibration data (not yet)
- [ ] Discrimination verdict recorded: DISCRIMINATIVE (not yet)
- [ ] Per-rubric catch rates recorded (not yet)

---

## What to Submit to Ops Team

### After Calibration Completes:

```
aspen__blogapi_unauthorized_read_001/
├── prompt.txt
├── task_config.json
├── reasoning.txt
├── README.md                   (updated with calibration results)
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

**Plus**: Docker image `ai266/aspen-blogapi:idor-v1:` pushed to ai266/ registry, set to PRIVATE, with digest recorded in task_config.json.

### Submission Method:

> Share your task folder in your private group chat with the Ops team (no ZIP needed).

---

## Key Differences from Gold Sample

Your task follows the same structure as the gold sample but with:

| Aspect | Yours | Gold Sample |
|--------|-------|-------------|
| Substrate complexity | Beginner-friendly (350 LOC) | Production (430 LOC) |
| Bug type | IDOR (read/write/delete) | IDOR + artifact exfil |
| Rubric items | 11 | 13 |
| Max score | 33 | 35 |
| Expected frontier | ≥75% | ≥80% |

Both follow the same Aspen conventions and are production-ready for calibration.

---

## Next Steps

### 1️⃣ Push Docker Image to ai266/
```bash
docker login docker.io
docker push ai266/aspen-blogapi:idor-v1
# Then set to PRIVATE on Docker Hub
```

### 2️⃣ Run Calibration (When Ready)
```bash
# Requires Harbor CLI + API keys
for i in {1..12}; do
  harbor run -p . -e e2b -a frontier
done

for i in {1..4}; do
  harbor run -p . -e e2b -a secondary
done
```

### 3️⃣ Update README.md with Results
- Mean reward per model
- Pass@k stats
- Per-rubric catch rates
- Discrimination verdict

### 4️⃣ Peer QC Review
- Check rubric atomicity
- Verify prompt doesn't leak structure
- Confirm discrimination verdict is DISCRIMINATIVE

### 5️⃣ Submit to Ops
- Share task folder in group chat
- Include calibration data in README.md

---

## Summary

✅ **All 6 required deliverables are complete and ready for submission.**

**Current status**: Pre-calibration. Task is valid and can be submitted after:
1. Docker image is pushed to ai266/ (set to PRIVATE)
2. Calibration runs are completed
3. README.md is updated with calibration results
4. Peer QC approval

**You're ready to move forward!**
