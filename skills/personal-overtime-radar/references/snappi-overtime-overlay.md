# Snappi Overtime Overlay Reference

This reference documents the organizational parameters, target spreadsheet structures, and quick-pasting workflows for Snappi timesheet reconciliation.

---

## 1. Employee Profile
- **Employee Name**: Panagiotis Koletsos
- **Employee ID**: `SHN000191`
- **Department**: Technology / Architecture
- **Contract Baseline**: Mon-Thu 09:30 - 17:00, Fri 09:30 - 16:30

---

## 2. Target Spreadsheet Structure
- **Target File**: `NEW_Overtimes_Technology.xlsx` (hosted on Snappi SharePoint Online)
- **Target Tab**: `Sheet2`
- **Columns Layout**:
  - Column A: Row index or employee identifier
  - Column B: Date formatted as `DD/MM/YYYY`
  - Column C: Overtime duration formatted as decimal half-hours (`0.0` or `.5`)
  - Column D: Justification (lowercase, 2 to 4 words, project-attributed)

---

## 3. Direct Clipboard Staging (1-Click Workflow)
Because the Microsoft Graph API token operates with read-only permissions on corporate sites, the fastest and safest mechanism to update the live SharePoint workbook is via system clipboard:

1. The script formats the reconciled rows into Tab-Separated Values (TSV):
   ```tsv
   DD/MM/YYYY\tX.X\tjustification text
   ```
2. The TSV string is piped into `pbcopy`:
   ```bash
   printf "%s" "$TSV_DATA" | pbcopy
   ```
3. The user opens `NEW_Overtimes_Technology.xlsx` in their browser, selects the starting cell in Column B, and presses `Cmd+V`.
