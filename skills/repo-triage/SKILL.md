---
name: repo-triage
description: Review a software repository, inspect project state, read issues/milestones, identify blockers, and recommend next implementation steps.
version: 0.2.1
status: draft
---

# Repo Triage Skill

## Purpose
Examine a new or active software repository to map its structure, evaluate current development status, identify blocks or architectural anomalies, and propose the top 3-5 high-impact development actions.

## Use When
- Opening a repository for the first time in a session.
- A user asks: "What should I do next?", "What is the status of the repo?", "Analyze this project", or uses the shorthand `"what next?"` conversational command.
- You need to determine the correct entry points and architecture boundaries.

## Do Not Use When
- You are already deep inside an approved implementation plan.
- The task is highly specific and one-off (e.g. "Fix the typo on line 43 of index.html").

## Inputs To Check
- Root directory files: `README.md`, `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `package.json`, etc.
- Repository Memory Logs: `DECISIONS.md` and `MEMORY.md` if present.
- Documentation folders: `/docs`, `/wiki`.
- Issues & Milestones: If API tools are connected (e.g. GitHub CLI `gh issue list`), inspect them.
- Privacy Check Targets: Scan active directories for potential credentials, database files (e.g. SQLite `.db`), local cookie files, or raw content transcripts that could be private.

## Procedure
1.  **Inspect Structure**: List the contents of the repository root. Identify the location of application code vs. configurations.
2.  **Read Onboarding and Memory Files**: View the contents of onboarding documents (`README.md`, `AGENTS.md`, `CLAUDE.md`) and memory logs (`DECISIONS.md`, `MEMORY.md` if present). Ingest local conventions, structural boundaries, and stable runtime decisions to prevent session-context loss.
3.  **Inspect Active State & shorthand requests**:
    *   Run local Git status and checks (`git status --short --branch`, etc.).
    *   Query open issues/milestones using native platform GitHub tools/plugins or `gh` CLI commands to understand live backlogs.
    *   If triggered by the shorthand `"what next?"` command, execute the unified decision tree (checking for detached HEAD, local changes, branch sync status, committed work, open PRs/checks, stale branches, and open issues) to recommend a single, immediate high-impact action.
4.  **Strict Privacy Gate Validation**: Verify that there are no active secrets, SQLite database files, local `.cookie` files, or raw content/chat transcripts stored in tracked/active folders.
5.  **Group Work Areas**: Organize codebase findings into these dimensions:
    *   **Bugs**: System failures, syntax errors, regressions.
    *   **Architecture**: Decoupling, dependencies, tech debt.
    *   **Implementation**: Open feature requirements, code modifications.
    *   **Docs**: Outdated, missing, or cluttered manuals.
    *   **Tests & Automation**: Broken CI/CD, missing coverages.
6.  **Identify Blockers**: Highlight any missing variables, broken dependencies, unauthenticated tokens, or vague requirements stopping progress.
7.  **Formulate Recommendations**: Recommend the **top 3-5** next actions, ordering them logically from dependencies first to downstream features last.

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
- Keep the recommendations strictly to the top 3-5 actions. Do not overwhelm the user.
- **Privacy Halt**: If any potential credentials, database files (e.g. `.db`), session cookies, or raw transcripts are found exposed in the directory, halt triage execution immediately, report the exact file path to the user, and prompt them to secure or gitignore it.
- **Load Memory Context**: Always load and check `MEMORY.md` and `DECISIONS.md` if they exist to understand historical design choices and maintain execution continuity.

## Global Skill Change Policy
This is a shared, global skill. Do NOT add repo-specific details or credentials. Any modifications to this skill's behavior must be performed in a dedicated Pull Request within the `agent-skills` repository, requiring a version bump and an entry in `CHANGELOG.md`.
