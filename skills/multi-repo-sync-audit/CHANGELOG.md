# Changelog

## 0.1.0

Initial draft.

Global skill changes must describe:
- date: 2026-08-25
- source repo or source task: agent-skills
- reason for change: Initial creation of the multi-repo preflight sync and PR health audit skill.
- summary of change: Defined scope discovery, read-only remote fetch, local working tree / stash audit, upstream comparison, and GitHub CLI PR / CI checks.
- expected behavior change: Enables agents to audit multi-repo sync status and open PRs across workspaces before beginning work.
- risk: Low (purely read-only / non-destructive procedure).
