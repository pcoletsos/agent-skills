# Changelog

## 0.3.0 - 2026-11-20

- **Source Task**: Daily incremental overtime gap analysis and isolated multi-column telemetry evidence sheet.
- **Reason for Change**: Support daily automated runs that analyze missing days (single day or weekend backlogs) while keeping the reporting sheet strictly noise-free matching company template, and storing comprehensive forensic proof on a separate sheet.
- **Summary of Change**:
  - Implemented `daily_overtime_tracker.py` with automatic gap detection scanning `NEW_Overtimes_Technology.xlsx` up to yesterday.
  - Added isolated `Telemetry_Evidence` sheet with 17 forensic audit columns: Date, Day, Location, Network Proof (Wi-Fi SSID/Gateway), Sign-on timestamp, Contract cutoff (17:00), Sign-off/Departure timestamp, Laptop closed/sleep timestamp, Total active span, Raw overtime hours, Payroll overtime hours, Policy applied, Transcripts and agendas analyzed, Teams chats and emails analyzed, Primary apps and repos, Synthesized justification, and Proof status.
  - Kept `Sheet2` strictly clean with 6 columns, dynamic Day formula (`=IF(C{r}<>0,CHOOSE(WEEKDAY(C{r},1),"Sunday", ...))`), Aptos Narrow font, and thin borders.
  - Added power and lid sleep tracking from `pmset -g log` to extract exact evening departure and arrival home timestamps.
  - Integrated meeting ledger cards (`05_MEETINGS/ledger/`) and live Teams/email feeds for practitioner justification synthesis.
- **Expected Behavior Change**: Daily scheduled automation can run unattended, identify missing days, compute accurate overtime with full forensic backing, and update both the clean reporting sheet and the detailed audit sheet.
- **Risk**: Low. Safe `.bak` backup created prior to workbook mutation; dry-run mode available.

## 0.2.1 - 2026-11-19

- **Source Task**: Align deliverable workbook and clipboard staging with company master template (`NEW_Overtimes_Technology.xlsx`).
- **Reason for Change**: Seamless monthly appending and synchronization into the authoritative HR SharePoint workbook without manual column remapping or broken formulas.
- **Summary of Change**:
  - Aligned workbook export with `NEW_Overtimes_Technology.xlsx` schema: `Sheet1` (lookup lists), `Sheet2` with Row 1 guidance, Row 2 headers (`SN`, `Name`, `Date`, `Day`, `Hours of Extra Work`, `Justification`), dynamic Day formula (`=IF(C{r}<>0,CHOOSE(WEEKDAY(C{r},1),"Sunday", ...))`), Aptos Narrow font, thin borders, and bottom `=SUM()` formula.
  - Added `append_to_existing_workbook()` to automatically update or append the audited month into `~/Downloads/NEW_Overtimes_Technology.xlsx` (with automatic `.bak` safety backups) while preserving earlier months (September) and manual entries.
  - Updated `stage_to_clipboard()` to stage all 6 tab-separated columns (`SN\tName\tDate\tDay\tHours of Extra Work\tJustification`) into macOS `pbcopy` for direct `Cmd+V` paste into SharePoint.
  - Enhanced reason synthesis with sprint engineering milestones and meeting ledger integration (`05_MEETINGS/ledger/`).
- **Expected Behavior Change**: Overtime exports now match the exact company template and can be directly appended into the master file each month.
- **Risk**: Low. Safe `.bak` backup created before modifying any existing file.

## 0.2.0 - 2026-11-19

- **Source Task**: In-office presence detection and zero-cut overtime reconciliation policy.
- **Reason for Change**: Prevent reduction of overtime hours when working at the office due to internal idle gaps, fragmented clustering, or downward rounding.
- **Summary of Change**:
  - Implemented multi-layered office presence detection using historical `/var/log/wifi.log*` DHCP gateway parsing (`10.25.150.1`, `10.25.0.1`, `10.15.0.1`, `10.10.190.1`) and live interface sweeps (`ipconfig getsummary en0`, `en7`).
  - Added In-Office Zero-Cut Policy: on verified office days, overtime begins immediately at contractual cutoff (17:00 Mon-Thu, 16:30 Fri), internal idle gaps are not deducted, and hours are not averaged down (half-hour ceiling rounding).
  - Added multi-repository authored Git commit extraction and `pmset` evening departure sleep detection to corroborate sessions when Screenpipe encounters capture gaps.
  - Added `--force-office` and `--office-days` CLI parameters for explicit overrides.
  - Added `Location` column to Markdown summaries, Excel workbooks, and clipboard staging.
- **Expected Behavior Change**: Overtime performed on-site at Snappi offices is automatically identified, credited continuously from contract cutoff to departure, and rounded up to the nearest half-hour without deduction.
- **Risk**: Low. Read-only telemetry inspection; preserves Option 2 Balanced Model for remote days.

## 0.1.0 - 2026-10-23

- **Source Task**: Automated overtime audit and reconciliation flow for Panagiotis Koletsos.
- **Reason for Change**: Initial creation of a personal skill to audit, reconcile, and format after-hours engineering overtime across macOS telemetry, Screenpipe intervals, and calendar entries.
- **Summary of Change**: Created `personal-overtime-radar` with Option 2 Balanced Model rules, 30-minute payroll increment rounding, weekend 1.0h threshold, Kranias-style project-attributed justifications, and automated clipboard staging.
- **Expected Behavior Change**: Agents can now audit any date span, query local Screenpipe and ASL power logs, generate compliant overtime reports, create Excel workbooks, and stage rows to macOS clipboard (`pbcopy`).
- **Risk**: Low. Read-only telemetry inspection with local Excel and clipboard staging; zero write operations to external systems without confirmation.
