# Changelog

## 0.1.0 - 2026-10-23

- **Source Task**: Automated overtime audit and reconciliation flow for Panagiotis Koletsos.
- **Reason for Change**: Initial creation of a personal skill to audit, reconcile, and format after-hours engineering overtime across macOS telemetry, Screenpipe intervals, and calendar entries.
- **Summary of Change**: Created `personal-overtime-radar` with Option 2 Balanced Model rules, 30-minute payroll increment rounding, weekend 1.0h threshold, Kranias-style project-attributed justifications, and automated clipboard staging.
- **Expected Behavior Change**: Agents can now audit any date span, query local Screenpipe and ASL power logs, generate compliant overtime reports, create Excel workbooks, and stage rows to macOS clipboard (`pbcopy`).
- **Risk**: Low. Read-only telemetry inspection with local Excel and clipboard staging; zero write operations to external systems without confirmation.
