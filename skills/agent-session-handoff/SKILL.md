---
name: agent-session-handoff
description: Summarize an active development session so that a subsequent AI agent or developer can seamlessly and safely resume execution.
version: 0.1.0
status: draft
---

# Agent Session Handoff Skill

## Purpose
Compile a precise, comprehensive workspace summary detailing completed edits, commands run, testing outcomes, open design dilemmas, and next actions to ensure zero context loss when passing the session to another agent.

## Use When
- Terminating your current execution turn or closing a pair-programming session.
- Stalling on a complex block and returning control to the user.
- Saving session state inside a walkthrough or handoff markdown file.

## Do Not Use When
- Reviewing pull requests that are already completed and ready to land (use `pr-review`).
- Triaging a new codebase you have not edited yet (use `repo-triage`).

## Inputs To Check
- Current session logs, shell history, and file edits.
- Staged and unstaged git changes: `git status`, `git diff`.
- Test results from the current run.

## Procedure
1.  **Summarize Completed Changes**: Write a high-level summary of what was accomplished during this session.
2.  **Compile Files Touched**: List all created, modified, or deleted files. Provide relative paths.
3.  **List Executed Commands**: Record the exact commands executed (e.g. build scripts, compilation steps, database runs).
4.  **List Tests Run**: Detail what test suites were executed, which passed, and which failed.
5.  **Document Open Questions**: Call out any design ambiguities, unresolved bugs, or missing clarifications that require user feedback.
6.  **Flag Immediate Risks**: Identify high-risk factors (e.g., breaking changes, untested legacy modules, uncommitted configurations).
7.  **Map Next Recommended Steps**: Write a chronological checklist of actions the subsequent agent should execute first.
8.  **Declare Uncertainty**: Never hide confusion or guess outcomes. If you are unsure of a dependency or the validity of a test, explicitly declare it.

## Output Format
Render a clean Markdown handoff report:
```markdown
# Agent Session Handoff Report

## 🏁 Session Summary
*High-level summary of goals met during this session.*

## 📂 Code Modifications
- **[NEW]** `relative/path/to/file` - Summary of purpose.
- **[MODIFY]** `relative/path/to/file` - Core edits made.

## 💻 Commands & Tests Executed
```bash
# exact commands run
```
- **Test Outcomes**: Pass/Fail (Include details on failed suites).

## 🛑 Critical Risks & Uncertainties
- **Breaking Changes**: ...
- **Unverified Assumptions**: ...

## ❓ Open Questions (Requires User Feedback)
1. ...

## ⏭ Next Steps (Chronological)
- [ ] Next action 1 (Pick up here)
- [ ] Next action 2
```

## Rules
- **Be completely transparent.** If a build is broken or a test is failing, place that at the very top of the handoff report.
- Do NOT guess file names or status. Check `git status` directly before writing the handoff.

## Global Skill Change Policy
This is a shared, global skill. Do NOT add repo-specific details or credentials. Any modifications to this skill's behavior must be performed in a dedicated Pull Request within the `agent-skills` repository, requiring a version bump and an entry in `CHANGELOG.md`.
