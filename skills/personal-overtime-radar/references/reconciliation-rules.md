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

## 2. In-Office Presence Model (Zero-Cut Policy)

When physical presence at an office location is detected (Corporate Hub Athens, Stadiou HQ, or Ioannina Office):

1. **Zero Hour Cuts**:
   - Do NOT deduct internal idle gaps (> 45 minutes).
   - In-person discussions, informal whiteboard reviews, architecture syncs, and stepping away from the laptop count as valid working time while remaining on premises.
2. **Contiguous Overtime Span**:
   - If the user was present at the office during normal working hours, after-hours overtime begins immediately at the contractual cutoff (17:00 Mon-Thu, 16:30 Fri).
   - The span extends continuously until the final departure timestamp (recorded by evening sleep on packing up, Wi-Fi disconnect, or evening Git commit).
3. **No Averaging Down (Half-Hour Ceiling)**:
   - Trailing minutes are never rounded down or averaged down.
   - If trailing active minutes exceed 1.0 minute past a half-hour mark, round up to the next half-hour increment (`.0` or `.5`).
   - Examples:
     - `17:00 - 19:05` (2h 05m) -> `2.5h` (never cut down to 2.0h)
     - `17:00 - 19:35` (2h 35m) -> `3.0h` (never cut down to 2.5h)
     - `17:00 - 20:54` (3h 54m) -> `4.0h` (never cut down to 3.5h)

---

## 3. Remote / Home Model (Option 2 Balanced Model)

When work is performed remotely:

1. **Cluster Threshold**: Combine discrete sessions separated by an idle gap of 150 minutes or less (with a 20-minute active session buffer) into a unified evening span.
2. **Idle Gap Deduction**: Any single unsegmented gap exceeding 45 minutes without recorded human input (`ui_events`, clicks, keystrokes, active power assertions) is treated as away time and deducted from total active duration.
3. **Short Session Discard**: Any standalone after-hours session shorter than 20 minutes (0.33 hours) is discarded as incidental check-ins.
4. **Rounding Cutoff (5.5-Minute Rule)**:
   - Round to the next half-hour only if trailing active minutes exceed the half-hour mark by more than 5.5 minutes:
     - `1h 00m` to `1h 05m` -> `1.0h`
     - `1h 06m` to `1h 35m` -> `1.5h`
     - `1h 36m` to `2h 05m` -> `2.0h`
5. **Weekend Minimum Threshold**:
   - If total active weekend work is under 1.0 hour, omit the entire day.
   - If 1.0 hour or more, round to the nearest 30-minute increment.

---

## 4. Justification Authoring Standards (Kranias Style)

Justifications must adhere to internal organizational expectations:
- **Format**: Short, lowercase, direct (2 to 4 words).
- **Mandatory Project Attribution**: Never record generic terms like "confluence sync" or "hld review" alone. Always cite the specific project name (e.g., `hld sync biometrics`, `prd review payments`, `office alignment kyc reliance`).
- **Priority (Choice A)**:
  - For office days: highlight on-site sync or project alignment (`office alignment <project>`, `on site architecture sync`).
  - If an after-hours meeting occurred (Teams call, design alignment), use the meeting title or discussion focus.
- **Alternative (Choice B)**: Provide an alternative justification highlighting underlying engineering, code review, or architecture deliverable (`hld sync <project>`, `prd review <project>`).
