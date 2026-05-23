---
name: repo-triage
description: Review a software repository, inspect project state, read issues/milestones, identify blockers, and recommend next implementation steps.
version: 0.1.0
status: draft
---

# Repo Triage Skill

## Purpose
Examine a new or active software repository to map its structure, evaluate current development status, identify blocks or architectural anomalies, and propose the next 3 high-impact development actions.

## Use When
- Opening a repository for the first time in a session.
- A user asks: "What should I do next?", "What is the status of the repo?", or "Analyze this project."
- You need to determine the correct entry points and architecture boundaries.

## Do Not Use When
- You are already deep inside an approved implementation plan.
- The task is highly specific and one-off (e.g. "Fix the typo on line 43 of index.html").

## Inputs To Check
- Root directory files: `README.md`, `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `package.json`, etc.
- Documentation folders: `/docs`, `/wiki`.
- Issues & Milestones: If API tools are connected (e.g. GitHub CLI `gh issue list`), inspect them.

## Procedure
1.  **Inspect Structure**: List the contents of the repository root. Identify the location of application code vs. configurations.
2.  **Read Onboarding Files**: View the contents of `README.md`, `AGENTS.md`, `CLAUDE.md`, and `memory.md` if present. Understand local rules and guidelines.
3.  **Inspect Active State**:
    *   Run `git status` or check current branch information.
    *   Query open issues/milestones to understand live backlogs.
4.  **Group Work Areas**: Organize codebase findings into these dimensions:
    *   **Bugs**: System failures, syntax errors, regressions.
    *   **Architecture**: Decoupling, dependencies, tech debt.
    *   **Implementation**: Open feature requirements, code modifications.
    *   **Docs**: Outdated, missing, or cluttered manuals.
    *   **Tests & Automation**: Broken CI/CD, missing coverages.
5.  **Identify Blockers**: Highlight any missing variables, broken dependencies, unauthenticated tokens, or vague requirements stopping progress.
6.  **Formulate Recommendations**: Recommend exactly **three (3)** next actions, ordering them logically from dependencies first to downstream features last.

## Output Format
Render a clean Markdown triage report:
```markdown
# Repository Triage Report

## 🗺 Codebase Mapping
- **Primary Tech Stack**: ...
- **Code Directory**: [path]
- **Docs Directory**: [path]

## 📊 Development State
- **Active Branch**: `...`
- **Milestones**: ...

## 🧩 Categorized Work Items
- **Bugs**: ...
- **Architecture**: ...
- **Implementation**: ...
- **Docs**: ...
- **Tests & Automation**: ...

## 🛑 Active Blockers
1. ...

## 🚀 Recommended Next Actions
1. **Action One**: ...
2. **Action Two**: ...
3. **Action Three**: ...
```

## Rules
- **NEVER** modify or edit source files during the triaging phase.
- Do NOT run tests or build steps unless explicitly instructed to verify a bug.
- Keep the recommendations strictly to exactly three (3) actions. Do not overwhelm the user.

## Global Skill Change Policy
This is a shared, global skill. Do NOT add repo-specific details or credentials. Any modifications to this skill's behavior must be performed in a dedicated Pull Request within the `agent-skills` repository, requiring a version bump and an entry in `CHANGELOG.md`.
