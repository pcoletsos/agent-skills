---
name: skill-name
description: Clear, trigger-friendly description of when an agent should use this skill.
version: 0.1.0
status: draft
---

# Skill Name

## Purpose
Describe in 1-2 sentences the exact objective and high-level goal of this skill.

## Use When
- Clear trigger condition 1.
- Clear trigger condition 2.
- Specific keywords or context matches.

## Do Not Use When
- Situations where this skill is inappropriate or out of scope.
- Conflicting tasks that should use a different skill.

## Inputs To Check
- File paths, dependencies, configurations, or databases to inspect before running the procedure.
- Environment variables or project settings that might impact behavior.

## Procedure
1.  **Step One**: Describe the first explicit action using active verbs.
2.  **Step Two**: Describe the second action.
3.  **Step Three**: Explain how to refine or validate the intermediate state.

## Output Format
Define the precise artifact, markdown, code blocks, or file layout the agent must output. For example:
```markdown
### Summary
...
### Checklist
...
```

## Rules
- **Rule 1**: Absolute negative constraint or hard boundary (e.g. "Do NOT edit files").
- **Rule 2**: Specific formatting requirement.

## Global Skill Change Policy
This is a shared, global skill. Do NOT add repo-specific details or credentials. Any modifications to this skill's behavior must be performed in a dedicated Pull Request within the `agent-skills` repository, requiring a version bump and an entry in `CHANGELOG.md`.
