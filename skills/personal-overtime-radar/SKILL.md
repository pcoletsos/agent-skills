---
name: personal-overtime-radar
description: Audit, calculate, and reconcile personal engineering and architecture overtime across local macOS telemetry, Screenpipe activity intervals, power logs, Git commits, and calendar feeds.
version: 0.1.0
status: draft
---

# Personal Overtime Radar

## Purpose
Perform an end-to-end audit, forensic reconciliation, and payroll-ready formatting of after-hours engineering, architecture, and meeting work using multi-layered local telemetry and calendar activity.

## Use When
- Auditing after-hours work across a specific calendar month, date range, or past rolling 10 to 30 days.
- User requests: "calculate my overtime", "audit overtime", "update my overtime list", "how much overtime did I do in October", "generate overtime report", or asks what to claim for recent evening sessions.
- Verifying physical office presence and active work hours at the end of a workday or week.
- Preparing payroll claims for timesheet submission (such as Excel workbooks or clipboard staging for internal tables).

## Do Not Use When
- Managing standard during-hours project task tracking or Jira issue estimation.
- Tracking billing hours for third-party contractor invoices without local workstation telemetry.
- Editing or mutating company payroll databases or SharePoint tables directly without explicit user review.

## Inputs To Check
- **Screenpipe Local Database**: `~/.screenpipe/db.sqlite` (contains UI events, window titles, and raw OCR frames).
- **macOS Power Management Logs**: `/var/log/powermanagement/*.asl` and `pmset -g log` (wake/sleep states, user assertions).
- **Network Interface Telemetry**: Wi-Fi SSID, BSSID, and DHCP lease logs via `system_profiler SPAirPortDataType` or `ipconfig getsummary en0`.
- **Local Git Activity**: Commit logs and authored diffs across active repository directories (e.g., `~/repos`).
- **Calendar & Mail Feeds**: Microsoft 365 or Outlook CLI (`m365 outlook message list`, `m365 outlook event list`) for after-hours calls and sent mail.
- **Contract Baseline Schedule**:
  - Monday to Thursday: 09:30 - 17:00 (overtime threshold starts at 17:00).
  - Friday: 09:30 - 16:30 (overtime threshold starts at 16:30).
  - Weekends & Public Holidays: Full non-working days (all eligible active work is overtime).

## Procedure

1. **Telemetry Ingestion & Filtering**:
   - Query `activity_intervals` and `ui_events` from `~/.screenpipe/db.sqlite` for the target date range.
   - Cross-check UI activity intervals with macOS wake/display assertions to eliminate passive background execution while the user was away or the machine was asleep.
   - Flag any gap greater than 45 minutes without recorded human input (`ui_events` or active assertions) as idle time and deduct it.

2. **Session Clustering (Option 2 Balanced Model)**:
   - Combine discrete active sessions separated by gaps of 150 minutes or less (with a 20-minute active session buffer) into contiguous work blocks.
   - Isolate after-hours spans occurring past the contractual cutoffs (post-17:00 Mon-Thu, post-16:30 Fri).
   - On weekends or holidays, evaluate the entire day's active spans.

3. **Payroll Increment Rounding**:
   - Discard any session shorter than 20 minutes (0.33h) as incidental check-ins.
   - For weekends and holidays, enforce a strict minimum threshold of 1.0 hour. Omit weekend days with less than 1.0 hour of active work.
   - Round net active overtime hours to strict 30-minute payroll increments (`.0` or `.5`):
     - Round up to the next half-hour only if trailing active minutes exceed the half-hour mark by more than 5.5 minutes (e.g., 1h 36m -> 1.5h; 1h 38m -> 2.0h).
     - Otherwise, truncate to the preceding half-hour increment.

4. **Justification Synthesis (Kranias Style)**:
   - Generate short, lowercase justifications (2 to 4 words).
   - If an after-hours meeting occurred (Teams call, design sync), prioritize the meeting as the primary justification (Choice A).
   - If the session was solo architecture or coding, name the specific project deliverable (e.g., `hld sync biometrics`, `prd review payments`, `reconciliation flow design`). Never use generic terms like "confluence sync" without naming the target project.
   - Provide two distinct options (Choice A and Choice B) for each active date so the user can select their preferred framing.

5. **Workbook Staging & Clipboard Transfer**:
   - Generate a local Excel workbook on the user's Desktop (`~/Desktop/SNAPPI_<Month>_<Year>_Overtime.xlsx`) containing active dates, hours, and justification choices.
   - Load the tab-delimited (TSV) rows directly into the macOS system clipboard using `pbcopy` so the user can paste directly into the live company SharePoint workbook in one keystroke (`Cmd+V`).

## Output Format
Render the audit findings using this structured markdown layout:

```markdown
### ⏱️ Overtime Audit Summary: <Date Range>
- **Total Days Audited**: `<count>`
- **Active Overtime Days**: `<count>`
- **Total Overtime Hours**: `<total>h`

### 📋 Reconciled Overtime Breakdown

| Date | Day | Active Span | Net Hours | Choice A (Priority) | Choice B (Alternative) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| DD/MM/YYYY | Mon | 17:00 - 19:30 | 2.5h | teams sync architecture | hld sync cards |
| DD/MM/YYYY | Fri | 16:30 - 20:00 | 3.5h | uat testing alignment | release verification |

### 🚀 Staged Deliverables
- **Desktop Workbook**: `~/Desktop/SNAPPI_<Month>_<Year>_Overtime.xlsx`
- **Clipboard Status**: Loaded into macOS clipboard (`pbcopy`). Ready to paste into SharePoint.
```

## Rules
- **Zero Hallucinated Overtime**: Every reported session must be grounded in verified SQLite UI events, power assertions, or Git commits.
- **Contract Cutoff Rigor**: Never count work before 17:00 (Mon-Thu) or before 16:30 (Fri) as overtime.
- **Strict 30-Minute Resolution**: Every output duration must end in `.0` or `.5`. Discard any 20-minute (0.33h) residual values.
- **Weekend Threshold**: Strictly discard weekend days totaling under 1.0 hour of active work.
- **Mandatory Project Names**: Confluence and specification entries must explicitly name the underlying project.
- **Privacy by Design**: Do not write, patch, or push overtime records to public repositories or shared corporate wikis without explicit interactive user approval.

## Global Skill Change Policy
This is a personal agent skill managed under personal version control. Do NOT commit private corporate secrets or credentials into public repositories. Parameterize company names, SSIDs, and employee identifiers. Any modifications to this skill's rules or calculation formulas require a SemVer increment and an update to `CHANGELOG.md`.
