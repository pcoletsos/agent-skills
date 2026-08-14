# Changelog

## 0.2.0

- **Date**: 2026-08-14
- **Source Repos**: `pixel-perfect-project`
- **Reason for Change**: The `what next?` "Ready for New Work" case surfaces the whole open-issue backlog as prose. Comparing candidates to decide which agent or model should take each one wanted a structured, at-a-glance view instead.
- **Summary of Change**: Added `what next table?` (aliases `what next tb?`, `what next in table?`), which runs the same state-gathering and decision tree as `what next?` but renders a multi-candidate result (an issue backlog, several open PRs) as a Markdown table with a per-candidate Difficulty rating (`Low`/`Medium`/`High`, judged on scope, judgment, and risk-and-reach) and a one-clause justification. Falls back to the standard bulleted format when there is only one candidate.
- **Expected Behavior Change**: Agents recognize the new trigger phrases and, whenever a recommendation involves comparing more than one candidate, output a table instead of prose.
- **Risk**: None. Additive; existing `what next?` triggers, decision tree, and output are unchanged.

## 0.1.1

- **Date**: 2026-07-12
- **Source Repos**: `agent-skills`
- **Reason for Change**: Standardize and specify the unified decision tree logic for the conversational `what next?` query.
- **Summary of Change**: Added detailed procedure steps and fallback behavior for `what next?` including detached HEAD, local changes, out-of-sync branches, and open PR lifecycle states.
- **Expected Behavior Change**: Agents will perform detailed git state analysis and follow a strict prioritization heuristic to suggest single logical actions.
- **Risk**: None.

## 0.1.0

- **Date**: 2026-05-24
- **Source Repos**: `creator-knowledge-pipeline`, `homelab-infra`, `career-playbook`
- **Reason for Change**: Extract standardized conversational shorthand Git workflows into a global reusable skill.
- **Summary of Change**: Created the initial `0.1.0` draft of `agent-conversational-git` with standard branching formatting and command mappings.
- **Expected Behavior Change**: Agents can parse and execute shorthand prompts conversationally across all repositories that link this skill.
- **Risk**: None. Starts in draft status.
