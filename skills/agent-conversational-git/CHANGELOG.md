# Changelog

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
