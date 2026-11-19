# Changelog

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
