---
name: agent-conversational-git
description: Standardized conversational shorthand commands mapping directly to atomic Git workflows.
version: 0.1.0
status: draft
---

# Agent Conversational Git Flow

## Purpose
Standardize conversational prompts to execute deterministic, safe, and hygiene-compliant Git operations when pairing with an LLM agent.

## Use When
- The pairing agent is executing local task cycles (branching, committing, pushing, opening PRs, merging).
- The user uses conversational shorthand triggers like `what next?`, `start <task>`, `record it`, `ship it`, `finish it`.

## Do Not Use When
- Performing complex rebases, cherry-picks, or resolving merge conflicts that require custom manual interventions.
- Operating on repositories that do not use a standard feature-branching or Pull Request workflow.

## Inputs To Check
- Local Git status (`git status`).
- Active local branch (`git branch --show-current`).
- Associated GitHub issues or project milestones.

## Procedure
1.  **Map Conversational Prompts**:
    Execute the exact sequence of Git/system actions corresponding to the received shorthand prompt:
    *   **`what next?`**:
        1. Run `git status` to identify uncommitted changes or active branch.
        2. Run `git log -n 5` or check local task tracker.
        3. Recommend the single next logical action (e.g. "Run `start <task>` to open a branch" or "Run `ship it` to propose your changes").
    *   **`start <task>`**:
        1. Reuse an existing issue or create a new issue for tracking.
        2. Identify the correct branch name using the rules in the **Rules** section.
        3. Create and switch to the branch: `git checkout -b <branch-name>`.
    *   **`record it`**:
        1. Stage relevant changes.
        2. Commit changes using a clean message or a Conventional Commit title if it is the final commit.
    *   **`publish it`**:
        1. Push the current branch to origin: `git push -u origin <branch-name>`.
    *   **`propose it`**:
        1. Open or update a Pull Request on origin (e.g., using GitHub CLI `gh pr create` or web interface).
        2. Provide a structured description outlining the goal, changes, and rationale.
    *   **`land it`**:
        1. Validate that all local and CI checks pass.
        2. Squash-merge the current Pull Request into the default branch using a Conventional Commit title.
    *   **`ship it`**:
        1. Execute `record it` (local commit).
        2. Execute `publish it` (push to origin).
        3. Execute `propose it` (open/update PR).
    *   **`finish it for #<id>`**:
        1. Execute `record it` (commit).
        2. Execute `publish it` (push).
        3. Execute `propose it` (open/update PR targeting the specified issue id).
        4. Execute `land it` (squash-merge).

## Output Format
Upon executing any shorthand prompt, output a clear, concise bulleted summary of:
1.  **Actions Performed**: The Git commands or status updates executed.
2.  **Current Git State**: Active branch name, commit hash, and remote tracking status.
3.  **Next Recommended Action**: The next step in the conversational workflow.

Example:
```markdown
### Conversational Git Status: [Command Executed]

- **Branch Created**: `codex/feat/pipeline/extractor-12`
- **Remote Tracking**: Set to `origin/codex/feat/pipeline/extractor-12`
- **Next Step**: Implement the pipeline extractor components, then call `record it`.
```

## Rules
- **Branch Naming Standard**: All feature branches must strictly follow the format: `<actor>/<type>/<scope>/<task>-<id>`
  - `actor`: `codex`, `claude`, `copilot`, `gemini`, `local`, `human`
  - `type`: `feat`, `fix`, `chore`, `docs`, `test`, `refactor`
  - `scope`: A concise folder, module, or package name representing the boundary (e.g., `pipeline`, `infra`, `ui`, `core`).
- **PR Conventional Commits**: PR titles and final squash commits must adhere to Conventional Commits format: `<type>(<scope>): <short description>`.
- **No Direct Commits to Default Branch**: Never implement or commit non-trivial changes directly on the main/default branch.

## Global Skill Change Policy
This is a shared, global skill. Do NOT add repo-specific details or credentials. Any modifications to this skill's behavior must be performed in a dedicated Pull Request within the `agent-skills` repository, requiring a version bump and an entry in `CHANGELOG.md`.
