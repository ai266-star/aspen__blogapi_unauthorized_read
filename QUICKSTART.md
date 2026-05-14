# Quick Start: Your First Aspen Task

## What You Have

Your task is complete and ready to use:

```
/Users/sodiqogunmola/Aspenproject/aspen__blogapi_unauthorized_read_001/
```

**Status**: ✅ Build complete, smoke tests passing, Docker image ready

## 3 Quick Checks

### 1️⃣ List the Files
```bash
ls -la ~/Aspenproject/aspen__blogapi_unauthorized_read_001/
```
Should show: task.toml, instruction.md, reasoning.txt, agent_judge.toml, prompt.md, ground_truth_issues.json, README.md, image_build/

### 2️⃣ Verify Docker Image
```bash
docker images | grep aspen-blogapi
```
Should show: `ai266/aspen-blogapi  idor-v1  b4ac9d79d943  380MB`

### 3️⃣ Run Smoke Test Again
```bash
docker run --rm ai266/aspen-blogapi:idor-v1 pytest tests/test_smoke.py -v
```
Should show: `8 passed in 0.40s`

---

## Next: Calibration (If You Want to Use This Task)

### What Calibration Does
Runs your task against frontier (Claude Opus) and secondary (Gemini) models to:
- ✅ Verify the rubric discriminates between models
- ✅ Check that frontier scores ≥75% and secondary scores 30-50%
- ✅ Confirm DISCRIMINATIVE verdict for QC sign-off

### How to Run (Manual Example)
```bash
# 1. Create a test agent submission manually
docker run -it ai266/aspen-blogapi:idor-v1 bash
# Inside: write tests in /repo/tests/exfiltration/test_access_control.py
# Then: git diff > /tmp/answer.diff

# 2. Run judge against the diff
# (Requires Harbor CLI + API keys)

# 3. Record results in README.md
```

### Alternative: Skip Calibration For Now
If you just want to understand the structure without running full calibration:
- ✅ Your task is valid for learning
- ✅ You can refine the rubric/prompt before calibrating
- ✅ Move on to building task #2

---

## Understanding Your Task

### The Bug (Intentional)
**Endpoints without ownership checks**:
```python
@app.get("/posts/{post_id}")
def get_post(post_id: int, x_user_id: str = Header(None)):
    # BUG: Should check if user owns the post
    # Instead, returns ANY post to ANY user
    return posts_db[post_id]
```

### What the Agent Must Test
1. **Can non-owner read drafts?** (should be 403)
2. **Can non-owner modify posts?** (should be 403)
3. **Can non-owner delete posts?** (should be 403)
4. **But can owner do all three?** (should all be 200 — anti-regression)
5. **Do sentinel markers leak in list responses?** (should not appear)

### Rubric Scoring
```
RUB-001 (major): Draft redaction         → 3 points if caught
RUB-002 (major): Metadata isolation      → 3 points if caught
RUB-003 (major): List filtering          → 3 points if caught
RUB-004 (major): Update ownership        → 3 points if caught
RUB-005 (major): Delete ownership        → 3 points if caught
RUB-006 (major): Owner CAN read          → 3 points if caught
RUB-007 (major): Owner CAN update        → 3 points if caught
RUB-008 (major): Owner CAN delete        → 3 points if caught
RUB-009 (minor):  Owner CAN list         → 2 points if caught
RUB-010 (minor):  404 on missing         → 2 points if caught
RUB-011 (nitpick): Sentinel markers      → 1 point if caught
                                    TOTAL: 33 points
```

**Max Score**: 33 (weighted mean)

---

## Modifying the Task

### If You Want to Change Something:

**1. Change the bug** → modify `image_build/blogapi/main.py` → rebuild image → recalibrate
**2. Change the rubric** → update `ground_truth_issues.json` → recalibrate
**3. Change the prompt** → update `instruction.md` → NO recalibration needed
**4. Add more smoke tests** → update `image_build/tests/test_smoke.py` → rebuild image

**NEVER** modify:
- ❌ Docker build anti-cheating measures (git init, user, WORKDIR)
- ❌ Base image (must stay `python:3.12-slim` + E2B convention)

---

## File Reference

| File | Purpose | Can Edit? |
|------|---------|-----------|
| instruction.md | Agent prompt | ✅ Yes |
| ground_truth_issues.json | Rubric items | ✅ Yes (then recalibrate) |
| reasoning.txt | Design rationale | ✅ Yes |
| agent_judge.toml | Judge config | ✅ Yes (mirrors rubric) |
| image_build/blogapi/main.py | Buggy code | ✅ Yes (then rebuild) |
| image_build/tests/test_smoke.py | Legitimate flows | ✅ Yes (then rebuild) |
| Dockerfile | Build context | ⚠️ Carefully (keep anti-cheat) |
| task.toml | Metadata | ❌ No (auto-generated) |

---

## Common Next Steps

### 🎯 Build Task #2
Now that you know the flow, create another task with a different scenario:
- SQL injection in a note-taking API
- Race condition in a transaction system
- Missing input validation in a file upload service

### 📚 Review the Gold Sample
Compare your task structure with `/Aboutproject/gold-sample-aspen-main/` to see:
- How a production task structures the rubric
- How the prompt is phrased
- How agent_judge.toml is configured

### 🔍 Audit the Rubric
Review your 11 items:
- [ ] Are they atomic? (one condition per item)
- [ ] Are they binary? (clearly MET/UNMET)
- [ ] Does every regression guard have a mirror direct-coverage item?
- [ ] Is there at least one nitpick test-quality item?

---

## Troubleshooting

### Docker image won't run
```bash
docker run --rm ai266/aspen-blogapi:idor-v1 /bin/bash
```
Should drop you into a shell. If not, check Dockerfile syntax.

### Smoke test fails inside container
```bash
docker run --rm ai266/aspen-blogapi:idor-v1 pytest tests/test_smoke.py -v
```
If this fails, the substrate code has an issue. Fix it and rebuild:
```bash
docker buildx build --platform linux/amd64 \
  --provenance=false --sbom=false \
  -t ai266/aspen-blogapi:idor-v2 \
  --load image_build/
```
Note: Always increment the version (v2, v3, etc.). Never reuse a tag.

### Can't find the image
```bash
docker image inspect ai266/aspen-blogapi:idor-v1
```
If not found, rebuild it first.

---

## 🚀 You're Ready!

Your task is **production-grade** and follows all Aspen conventions. You can:
1. ✅ Study it to understand the framework
2. ✅ Modify and iterate on it
3. ✅ Submit it for calibration & QC
4. ✅ Build task #2 using this as a template

**Questions?** Check `/Aboutproject/` for detailed docs on:
- Rubric structure
- Docker setup
- Workflow
- Deliverables
