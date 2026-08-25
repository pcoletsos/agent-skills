---
name: multi-repo-sync-audit
description: Audit multi-repository sync status, uncommitted local changes, stashes, and open GitHub PRs/CI health across workspace directories.
version: 0.1.0
status: draft
---

# Multi-Repository Sync & PR Health Audit

## Purpose
Perform a safe, non-destructive pre-flight audit across multiple local Git repositories to identify multi-device handoff gaps, uncommitted changes, stashes, unsynced upstream commits, and open GitHub Pull Request statuses before starting work.

## Use When
- Starting a development session across a multi-repository workspace or switching between development machines.
- Running a pre-flight synchronization check to detect unpushed local work, unpulled remote changes, or forgotten stashes.
- Auditing the health, CI/CD check status, and mergeability of open GitHub Pull Requests across several projects.
- The user requests: "Run a pre-flight repo sync check", "Audit my repos for unpushed work", "Check multi-repo status", or requests a scan of a `repos` directory.

## Do Not Use When
- Operating on a single isolated repository during active feature development (use standard Git commands or `agent-conversational-git`).
- Performing code review or architectural assessments on a single project (use `pr-review` or `repo-triage`).
- Destructively mutating repository state (e.g., automated rebasing, resetting, or force-pushing across repos).

## Inputs To Check
- **Target Root Directory**: Workspace directory containing repositories (defaults to `repos` or current working directory).
- **Scope Exclusion Patterns**: Path segments or directory patterns to strictly ignore (e.g., paths containing `**/vf/**` or configured vendor/archive directories).
- **Tool Availability & Authentication**: Verify `git` is accessible and `gh` CLI authentication status via `gh auth status` for PR inspection.

## Procedure
1.  **Discovery & Scope Filtering**:
    *   Recursively search the target directory (e.g., `repos`) to discover all directories containing a `.git` directory or file (submodules/worktrees).
    *   Apply exclusion patterns strictly: skip and ignore any repository where any path segment matches configured exclusion rules (e.g., any parent folder named `vf`, matching `**/vf/**`).
2.  **Safe Remote Tracking Update (Read-Only)**:
    *   In each discovered repository, execute `git fetch --all --prune --quiet` (or `git fetch --prune --quiet`) to synchronize remote-tracking branches.
    *   Do NOT execute `git pull`, `git merge`, or `git checkout` during this audit.
3.  **Local & Tracking State Audit**:
    *   **Working Tree**: Inspect for uncommitted changes (staged, unstaged, or untracked files) using `git status --short`.
    *   **Stashes**: Inspect the stash list using `git stash list`.
    *   **Branch & Upstream Comparison**: Determine current branch (`git branch --show-current`) and compare local HEAD with its upstream tracking branch (`git rev-list --left-right --count HEAD...@{upstream}` or `git status -sb`):
        *   **Behind**: Remote tracking branch has commits not present locally (unpulled work from other machines).
        *   **Ahead**: Local branch has commits not yet pushed to remote.
        *   **Diverged**: Both local and remote branches contain unique commits (potential merge conflict).
        *   **No Upstream**: Local branch is not tracking a remote branch.
        *   **Up-to-date**: Local branch matches upstream tracking branch.
4.  **GitHub Pull Request & CI/CD Inspection**:
    *   For repositories with a configured GitHub remote, query open Pull Requests using the GitHub CLI:
        ```bash
        gh pr list --state open --json number,title,headRefName,statusCheckRollup,isDraft,mergeable
        ```
    *   Evaluate and categorize PR status:
        *   🟢 **Ready to Merge**: All CI checks passed/green, mergeable with no conflicts, and non-draft.
        *   🔴 **CI Failed / Conflict**: One or more failing checks or merge conflicts requiring triage.
        *   🟡 **Pending / Draft**: Checks in progress, reviews pending, or marked as a draft PR.
5.  **Compile & Categorize Report**:
    *   Calculate summary counts: total scanned repositories, repos needing sync/local action, and active open PRs.
    *   Assemble actionable findings into structured tables and list all fully clear repositories.

## Output Format
Render the multi-repository audit findings using this Markdown structure:

```markdown
### 📊 Quick Summary
- **Repositories Scanned**: `<count>`
- **Repos Needing Sync / Local Action**: `<count>`
- **Active Open PRs**: `<count>`

### 1. ⚠️ Action Required: Branch Sync & Local Gaps
*(Show ONLY repositories with uncommitted edits, stashes, or unsynced branches)*

| Repository | Current Branch | Working Tree / Stashes | Sync Status | Action Needed / Command |
| :--- | :--- | :--- | :--- | :--- |
| `path/to/repo` | `main` | `Clean` | `Behind by 2` | `git pull` (pull work from other machine) |
| `path/to/repo2` | `feature/abc` | `Dirty (2 files)` | `Ahead by 1` | Commit & `git push` (publish local commits) |
| `path/to/repo3` | `fix/xyz` | `Clean (1 stash)` | `Up-to-date` | Inspect stash: `git stash list` |

### 2. 🔀 Open Pull Requests & CI/CD Status
*(Show ONLY repositories with open PRs)*

| Repository | PR # & Title | Branch | CI / Checks | State & Recommended Action |
| :--- | :--- | :--- | :--- | :--- |
| `path/to/repo` | `#12 Fix auth token` | `fix/token` | 🟢 Passing | **Ready to Merge** (land the PR) |
| `path/to/repo2` | `#45 Add export API` | `feat/export` | 🔴 Failed | **CI Failure** (inspect failed run) |
| `path/to/repo3` | `#8 Refactor layout` | `refactor/ui` | 🟡 Pending | Checks in progress / In review |

### 3. ✅ Fully Synced & Clear
- `path/to/repo4`
- `path/to/repo5`
```

*Note: If no repositories have pending local actions or open PRs, output "None" under the respective table section.*

## Rules
- **Non-Destructive Audit**: Never execute destructive commands, automated commits, merges, pulls, rebases, or pushes during the audit. Use `git fetch` solely to refresh remote metadata.
- **Strict Scope Exclusion**: Always exclude specified path segments (such as any directory containing `vf` in its path) during repository discovery.
- **Graceful Tool Degradation**: If `gh` CLI is not installed, unauthenticated, or remote is not GitHub, document the state in the report and complete the local Git audit without crashing.
- **Maintain Global Genericism**: Do not hardcode machine-specific local absolute paths, private credentials, or organization tokens into global instructions.

## Global Skill Change Policy
This is a shared, global skill. Do NOT add repo-specific details or credentials. Any modifications to this skill's behavior must be performed in a dedicated Pull Request within the `agent-skills` repository, requiring a version bump and an entry in `CHANGELOG.md`.
