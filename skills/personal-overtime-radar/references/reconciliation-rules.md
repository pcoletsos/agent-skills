# Reconciliation & Calculation Rules

This document defines the mathematical models, clustering heuristics, payroll rounding rules, and justification standards used by the Personal Overtime Radar.

---

## 1. Baseline Working Hours & Overtime Cutoffs

- **Monday to Thursday**:
  - Regular Working Hours: 09:30 - 17:00
  - Overtime Eligibility: Work performed strictly after 17:00.
- **Friday**:
  - Regular Working Hours: 09:30 - 16:30
  - Overtime Eligibility: Work performed strictly after 16:30.
- **Weekends & Official Public Holidays**:
  - Non-working days.
  - All eligible active work is categorized as overtime, subject to the weekend threshold.

---

## 2. Option 2: Balanced Model (Gap Clustering)

To balance contiguous engineering flow with fairness:
1. **Cluster Threshold**: Combine discrete sessions separated by an idle gap of 150 minutes or less (with a 20-minute active session buffer) into a unified evening span.
2. **Idle Gap Deduction**: Any single unsegmented gap exceeding 45 minutes without recorded human input (`ui_events`, clicks, keystrokes, active power assertions) is treated as away time and deducted from total active duration.
3. **Short Session Discard**: Any standalone after-hours session shorter than 20 minutes (0.33 hours) is discarded as incidental check-ins.

---

## 3. Strict 30-Minute Payroll Increment Rounding

Payroll systems require hours in half-hour increments: `.0` or `.5`.

### A. Roundup Threshold (5.5-Minute Cutoff Rule)
Round to the next half-hour only if trailing active minutes exceed the half-hour mark by more than 5.5 minutes:
- `1h 00m` to `1h 05m` -> `1.0h`
- `1h 06m` to `1h 35m` -> `1.5h`
- `1h 36m` to `2h 05m` -> `2.0h`

### B. Weekend & Holiday Minimum Threshold
On non-working days (Saturdays, Sundays, and public holidays):
- If the day's total active time is less than 1.0 hour, omit the entire day.
- If the day's total active time is 1.0 hour or more, round to the nearest 30-minute increment and include in the claim.

---

## 4. Justification Authoring Standards (Kranias Style)

Justifications must adhere to internal organizational expectations:
- **Format**: Short, lowercase, direct (2 to 4 words).
- **Mandatory Project Attribution**: Never record generic terms like "confluence sync" or "hld review" alone. Always cite the specific project name (e.g., `hld sync biometrics`, `prd review payments`, `reconciliation flow design`).
- **Priority (Choice A)**: If an after-hours meeting occurred (Teams call, design alignment), use the meeting title or discussion focus as Choice A.
- **Alternative (Choice B)**: Provide an alternative justification highlighting underlying engineering, code review, or architecture deliverable.
