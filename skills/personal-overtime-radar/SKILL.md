---
name: personal-overtime-radar
description: Audit, calculate, and reconcile personal engineering and architecture overtime across local macOS telemetry, Screenpipe activity intervals, power logs, Git commits, network presence, and calendar feeds.
version: 0.2.1
status: draft
---

# Personal Overtime Radar

## Purpose
Perform an end-to-end audit, forensic reconciliation, and payroll-ready formatting of after-hours engineering, architecture, and meeting work using multi-layered local telemetry, physical office network detection, and calendar activity.

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
- **Physical Office Network Telemetry**:
  - Historical: Gateway IP addresses logged in `/var/log/wifi.log` and `/var/log/wifi.log.*.bz2`.
  - Live: `ipconfig getsummary en0`, `en7` (SSID `Corporate_Hub`, `Snappi_Stadiou`, `Snappi_Ioannina`, Option 224 `FGT90G...`).
  - Office Gateways: `10.25.150.1` (Corporate Hub Athens Wi-Fi), `10.25.0.1` (Corporate Hub Wired Dock), `10.15.0.1` (Stadiou HQ), `10.10.190.1` (Ioannina).
- **Screenpipe Local Database**: `~/.screenpipe/db.sqlite` (activity intervals, window titles, and UI events).
- **macOS Power Management Logs**: `pmset -g log` and `/var/log/powermanagement/*.asl` (departure sleeps, assertions, user wake).
- **Local Git Activity**: Commit logs and authored diffs across active repositories in `~/repos/SNAPPI/*` and `~/repos/engineering/*`.
- **Calendar & Mail Feeds**: Microsoft 365 CLI (`m365 outlook message list`, `m365 outlook event list`) for after-hours calls and sent mail.
- **Contract Baseline Schedule**:
  - Monday to Thursday: 09:30 - 17:00 (overtime threshold starts at 17:00).
  - Friday: 09:30 - 16:30 (overtime threshold starts at 16:30).
  - Weekends & Public Holidays: Full non-working days (all eligible active work is overtime).

## Procedure

1. **Telemetry Ingestion & Office Presence Detection**:
   - Parse `/var/log/wifi.log*` and query live network interfaces (`ipconfig getsummary`) to identify which dates were spent at an office location versus remote.
   - Query `activity_intervals` and `ui_events` from `~/.screenpipe/db.sqlite`.
   - Corroborate with local Git commit timestamps and macOS power management departure sleep logs (`pmset -g log`).

2. **In-Office Zero-Cut Model (Office Days)**:
   - When on-site office presence is detected on a workday:
     - **No hour cuts**: Do NOT deduct internal idle gaps (> 45 minutes). In-person collaboration, whiteboard discussions, and stepping away from the laptop count as working time on premises.
     - **Contiguous span**: Overtime starts at the contract cutoff (17:00 Mon-Thu, 16:30 Fri) and runs continuously until the recorded departure timestamp.
     - **No averaging down (Half-Hour Ceiling)**: Trailing minutes are never rounded down. Any session extending past a half-hour mark (with a 1-minute buffer) rounds up to the next half-hour increment (`.0` or `.5`).

3. **Option 2 Balanced Model (Remote Days)**:
   - For remote working days:
     - Combine discrete active sessions separated by gaps of 150 minutes or less (with a 20-minute active session buffer) into contiguous work blocks.
     - Deduct unsegmented gaps greater than 45 minutes without recorded human input.
     - Discard sessions shorter than 20 minutes (0.33h).
     - On weekends and holidays, enforce a strict minimum threshold of 1.0 hour.
     - Round using the 5.5-minute cutoff rule (rounds down if trailing minutes are <= 5.5 min past whole or half hour).

4. **Justification Synthesis (Kranias Style)**:
   - Generate short, lowercase justifications (2 to 4 words).
   - For office days: highlight on-site delivery or alignment (Choice A: `office alignment <project>`, Choice B: `hld sync <project>`).
   - If an after-hours meeting occurred (Teams call, design sync), prioritize the meeting as the primary justification.
   - If the session was coding or solo architecture, name the specific project deliverable (e.g. `kyc reliance`, `payments`, `cards`, `biometrics`).

5. **Workbook Staging, Master Template Synchronization & Clipboard Transfer**:
   - Generate a local Excel deliverable on the user's Desktop (`~/Desktop/SNAPPI_<Month>_<Year>_Overtime.xlsx`) strictly matching the company template (`NEW_Overtimes_Technology.xlsx`):
     - `Sheet1`: Employee lookup list (`SN (List)`, `Name (list)`).
     - `Sheet2`: Exact 6-column structure (`SN`, `Name`, `Date`, `Day`, `Hours of Extra Work`, `Justification`), Row 1 guidance, Row 2 headers, Day formula `=IF(C{r}<>0,CHOOSE(WEEKDAY(C{r},1),"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")," ")`, Aptos Narrow font, thin borders, and bottom `=SUM()` row.
     - `Audit Breakdown`: Detailed engineering audit trail (Date, Day, Location, Active Span, Raw Hours, Payroll Hours, Reason).
   - If `~/Downloads/NEW_Overtimes_Technology.xlsx` (or `--append-to <path>`) is present:
     - Automatically creates a `.bak` backup.
     - Synchronizes/merges the audited month chronologically starting at the employee's block.
     - Preserves all earlier months (e.g. September) and earlier manual entries without data loss.
   - Load the tab-delimited (TSV) rows directly into the macOS system clipboard using `pbcopy` matching all 6 columns (`SN\tName\tDate\tDay\tHours of Extra Work\tJustification`) so the user can paste directly into SharePoint in one keystroke (`Cmd+V`).

## Output Format
Render the audit findings using this structured markdown layout:

```markdown
### ⏱️ Overtime Audit Summary: <Date Range>
- **Audited Span**: `<Start>` to `<End>`
- **Active Overtime Days**: `<count>` (`<office_count>` Office, `<remote_count>` Remote)
- **Total Overtime Hours**: `<total>h`

### 📋 Reconciled Overtime Breakdown

| SN | Name | Date | Day | Hours of Extra Work | Justification |
| :--- | :--- | :--- | :--- | :--- | :--- |
| SHN000191 | Panagiotis Koletsos | DD/MM/YYYY | Thu | 0.5h | snappi x vodafone epay payments mechanism |
| SHN000191 | Panagiotis Koletsos | DD/MM/YYYY | Mon | 2.0h | epay payments integration natech discussion |

### 🚀 Staged Deliverables
- **Desktop Deliverable**: `~/Desktop/SNAPPI_<Month>_<Year>_Overtime.xlsx`
- **Master Workbook**: `~/Downloads/NEW_Overtimes_Technology.xlsx` (synchronized with backup at `.bak`)
- **Clipboard Status**: Staged in macOS clipboard (`pbcopy`). Ready for `Cmd+V` in SharePoint.
```

## Rules
- **Zero Hallucinated Overtime**: Every reported session must be grounded in verified SQLite UI events, power assertions, Git commits, or office network gateways.
- **In-Office Zero-Cut Guarantee**: Never deduct internal idle gaps or average down hours when physical presence at the office is verified.
- **Contract Cutoff Rigor**: Never count work before 17:00 (Mon-Thu) or before 16:30 (Fri) as overtime.
- **Strict 30-Minute Resolution**: Every output duration must end in `.0` or `.5`.
- **Weekend Threshold**: Strictly discard remote weekend days totaling under 1.0 hour of active work.
- **Mandatory Project Names**: Confluence and specification entries must explicitly name the underlying project.
- **Privacy by Design**: Do not write, patch, or push overtime records to public repositories or shared corporate wikis without explicit interactive user approval.

## Global Skill Change Policy
This is a personal agent skill managed under personal version control. Do NOT commit private corporate secrets or credentials into public repositories. Parameterize company names, SSIDs, and employee identifiers. Any modifications to this skill's rules or calculation formulas require a SemVer increment and an update to `CHANGELOG.md`.
