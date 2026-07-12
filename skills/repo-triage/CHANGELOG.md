# Changelog

## 0.2.1

- date: 2026-07-12
- source repo or source task: agent-skills
- reason for change: Standardize inspection of active state with "what next?" command integration.
- summary of change: Updated state inspection to leverage the unified decision tree check for what-next shortcuts.
- expected behavior change: Agents will recommend single immediate actions based on git status and issue backlog matching.
- risk: Low

## 0.2.0

- date: 2026-05-24
- source repo or source task: Existing Skills Hardening (Milestone #2)
- reason for change: Enhance agent security posture, prevent session context loss, and handle conversational what-next shortcuts.
- summary of change: Integrated strict privacy validation steps, loaded memory logs check, and integrated "what next?" command workflow.
- expected behavior change: Agent will abort on credentials leak, read historical decisions/memory context, and suggest immediate singular actions for what-next triggers.
- risk: Low

## 0.1.1

- date: 2026-05-23
- source repo or source task: agent-skills repository hardening
- reason for change: rigidly forcing exactly three actions was too constrained
- summary of change: relaxed next-action count from exactly 3 to top 3-5; added example output reference
- expected behavior change: agent will recommend between 3 and 5 actions and have a reference example
- risk: low

## 0.1.0

Initial draft.

Global skill changes must describe:
- date
- source repo or source task
- reason for change
- summary of change
- expected behavior change
- risk
