# Criterion Justification

## Access Control — Catch the Vulnerability (5 items)

### RUB-001: Draft Isolation
**Importance**: Proves non-owners cannot read draft content; core confidentiality protection.

### RUB-002: Metadata Isolation
**Importance**: Ensures author details and internal metadata don't leak in cross-user reads; prevents side-channel leakage.

### RUB-003: List Filtering
**Importance**: Prevents drafts from appearing in shared list responses; maintains privacy at bulk-read level.

### RUB-004: Update Ownership
**Importance**: Blocks unauthorized POST modifications; prevents integrity violations.

### RUB-005: Delete Ownership
**Importance**: Prevents unauthorized DELETEs; ensures data availability for rightful owners.

---

## Regression Guards — Don't Break Legitimate Use (4 items)

### RUB-006: Owner Read Anti-Overblock
**Importance**: Ensures legitimate owner reads of own drafts still work; catches over-aggressive blocking.

### RUB-007: Owner Update Anti-Overblock
**Importance**: Ensures legitimate owner updates persist correctly; validates fix doesn't disable writes.

### RUB-008: Owner Delete Anti-Overblock
**Importance**: Ensures legitimate owner deletions work; validates fix doesn't disable removal.

### RUB-009: Owner List Anti-Overblock
**Importance**: Ensures list endpoint remains usable; validates fix doesn't break bulk-read for authorized users.

---

## Boundary Condition & Test Quality (2 items)

### RUB-010: 404 vs 403 Distinction
**Importance**: Separates missing resources from forbidden access; reveals implementation discipline.

### RUB-011: Sentinel Marker Non-Leakage
**Importance**: Proves test quality and data isolation rigor; catches sophisticated cross-user leakage at response level.
