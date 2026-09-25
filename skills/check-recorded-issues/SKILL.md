---
name: check-recorded-issues
description: Inspect, audit, filter, and cross-reference recorded issues, bug reports, and action trackers across GitHub and local repository registers.
version: 0.1.0
status: draft
---

# Check Recorded Issues Skill

## Purpose
Examine, filter, and reconcile recorded issues, action items, and open questions across GitHub Issues and local repository tracking registers (`action-tracker.md`, `open-points-register.md`, `opportunity-backlog.md`, or project-specific issue registers).

---

## When to Use
- A user asks:
  - "What are the recorded issues?"
  - "Check open issues"
  - "What is blocked?"
  - "Audit issue tracker"
  - "Show high priority items"
  - "Show issues in Milestone X"
- You need to prioritize the next engineering task based on project milestones and priorities.
- You need to audit consistency between GitHub issues and local markdown tracking tables.
- Shorthand conversational triggers: `"check issues"`, `"blocked issues"`, `"audit issues"`, `"prio issues"`.

---

## Fast Automated Execution

If the repository provides a companion CLI script (`scripts/check_recorded_issues.py` or `.agents/skills/check-recorded-issues/scripts/check_issues.py`):

```bash
# 1. Executive Summary (total, open, closed, priority counts, milestones, blockers)
python scripts/check_recorded_issues.py

# 2. View all open issues with metadata table
python scripts/check_recorded_issues.py --open

# 3. Filter strictly to blocked and needs-input issues
python scripts/check_recorded_issues.py --blocked

# 4. Filter by priority tier (now / next / later)
python scripts/check_recorded_issues.py --prio now

# 5. Filter by milestone name (case-insensitive substring)
python scripts/check_recorded_issues.py --milestone "Phase A"

# 6. Reconcile GitHub issues against local action tracker
python scripts/check_recorded_issues.py --audit

# 7. Output machine-readable JSON (useful for subagents or automated pipelines)
python scripts/check_recorded_issues.py --open --json
```

---

## Manual Inspection Procedure

If the CLI script is unavailable or custom inspection is needed:

1. **Query Active GitHub Issues**:
   - Run `gh issue list --state all --limit 100 --json number,title,state,labels,milestone,updatedAt,url`.
   - Categorize issues by priority (`prio:now`, `prio:next`, `prio:later`), type (`type:*`), and milestone.
   - Flag blockers (`state:blocked`, `needs:client-input`).

2. **Inspect Local Tracking Registers**:
   - Locate and inspect local markdown registers in `docs/` or `.agents/` (e.g., `action-tracker.md`, `open-points-register.md`, `backlog.md`).
   - Parse action items, owners, target dates, and statuses.

3. **Reconciliation & Integrity Audit**:
   - Identify closed GitHub issues still marked as open in local trackers.
   - Identify actions marked as Done in trackers whose GitHub issue is still Open.
   - Identify action items lacking an associated GitHub issue link.

4. **Format Findings**:
   - Output structured tables with issue numbers, titles, priority, milestone, and blocker flags.
   - Recommend the top 3 immediate action items for the current session.

---

## Output Report Formats

### 1. Executive Summary Format
```markdown
# Recorded Issues Executive Summary
- **Total Tracked Issues**: X
- **Open Issues**: Y
- **Closed Issues**: Z
- **Active Blockers / Needs Input**: N

## Priority Breakdown (Open Issues)
| Priority | Count | Target Action |
|---|---|---|
| `now` | ... | Immediate implementation focus |
| `next` | ... | Upcoming milestone scope |
| `later` | ... | Deferred / backlog review |

## 🛑 Active Blockers & Items Needing Input
| Issue | Title | Reason / Flag | Milestone |
|---|---|---|---|
| [#29](...) | Title | state:blocked, needs:client-input | Phase A |
```

### 2. Reconciliation Audit Format
```markdown
# Issue Tracker Reconciliation Audit
- **Actions Parsed in Tracker**: X
- **Actions Mapped to GitHub Issues**: Y
- **Status Discrepancies Detected**: N

## ⚠️ Status Discrepancies
| AC ID | Issue | Action Title | Tracker Status | GitHub State | Audit Finding |
|---|---|---|---|---|---|
| `AC14` | #21 | Title | Done | OPEN | Tracker says Done but GitHub is OPEN |
```

---

## Operating Rules
- **No Em Dashes**: Never use em dashes in any response text or reports.
- **Read-Only Inspection**: Inspecting issues must not alter issue states or delete records unless explicitly requested.
- **Privacy Enforcement**: Do not leak personal client identifiers, credentials, or private contact details in public reports.

---

## Global Skill Change Policy
This is a shared, global skill. Do NOT add repo-specific details or credentials. Any modifications to this skill's behavior must be performed in a dedicated Pull Request within the `agent-skills` repository, requiring a version bump and an entry in `CHANGELOG.md`.
