# SUBMISSION STRUCTURE

**Folder to share with Ops team:**

```
aspen__blogapi_unauthorized_read_001/
│
├── prompt.txt                     ← SUBMIT (3-paragraph prompt)
├── task_config.json               ← SUBMIT (metadata + rubric)
├── reasoning.txt                  ← SUBMIT (threat model + weights)
├── README.md                       ← SUBMIT (status + calibration when ready)
├── DEEP_DIVE.md                   ← SUBMIT (outsider on-ramp)
│
└── image_build/                   ← SUBMIT (entire Docker build context)
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

**Plus (separate from folder):**
- Docker image pushed to `ai266/aspen-blogapi:idor-v1` (PRIVATE)

---

## What NOT to Submit

Do NOT include these in the submission folder:

```
❌ QUICKSTART.md              (your personal reference)
❌ TASK_CREATION_SUMMARY.md   (your personal notes)
❌ DELIVERABLES_CHECKLIST.md  (this checklist)
❌ task.toml                  (Harbor format, not Aspen spec)
❌ instruction.md             (superseded by prompt.txt)
❌ prompt.md                  (judge system prompt, internal only)
❌ agent_judge.toml           (judge harness config, internal only)
❌ ground_truth_issues.json   (already in task_config.json)
```

---

## Ready to Share With Ops?

### Before Submitting:

- [x] Docker image is pushed to ai266/ and set to PRIVATE
- [ ] Calibration is complete (N=12 frontier, N=4 secondary)
- [ ] README.md is updated with:
  - Per-model results (mean reward, pass rates)
  - Per-rubric catch rates
  - Discrimination verdict: **DISCRIMINATIVE** (or UNDER-CALIBRATED if needed)
- [ ] Peer QC has reviewed and approved
- [ ] No placeholder strings remain in any config file

### Submission Command:

```bash
# Share the folder in your private group chat with Ops
# (no ZIP file needed)

# Example chat message:
# "I've completed aspen__blogapi_unauthorized_read_001. 
#  Docker image: ai266/aspen-blogapi:idor-v1 (PRIVATE)
#  Calibration: DISCRIMINATIVE
#  Ready for HDM/HDL sign-off."
```

---

## File Purposes at a Glance

| File | Purpose | Required? |
|------|---------|-----------|
| prompt.txt | Agent sees this | ✅ YES |
| task_config.json | Pipeline metadata & rubric | ✅ YES |
| reasoning.txt | Design rationale | ✅ YES |
| README.md | Status + calibration results | ✅ YES |
| DEEP_DIVE.md | Outsider-friendly walkthrough | ✅ YES |
| image_build/ | Docker build context | ✅ YES |
| Docker image | Pushed to ai266/ | ✅ YES |
| --- | --- | --- |
| QUICKSTART.md | Your personal reference | ❌ NO |
| TASK_CREATION_SUMMARY.md | Your personal notes | ❌ NO |
| DELIVERABLES_CHECKLIST.md | This file (for your reference) | ❌ NO |
| task.toml | Harbor format (not submission) | ❌ NO |
| instruction.md | Old version, use prompt.txt | ❌ NO |
| prompt.md | Judge internal use | ❌ NO |
| agent_judge.toml | Judge internal use | ❌ NO |

---

## One-Line Summary

**You have 6 required deliverables ✅ ready to submit after running calibration and pushing the Docker image.**
