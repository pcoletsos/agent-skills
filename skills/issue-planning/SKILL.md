---
name: issue-planning
description: Turn rough project goals or feature requests into milestone-backed, execution-ready task contracts with authoritative sources, explicit boundaries, blocker and resume rules, handoff evidence, dependencies, branches, validation, and acceptance criteria.
version: 0.3.0
status: draft
---

# Issue Planning Skill

## Purpose

Decompose a goal into a small set of reviewable issues that another person or agent can execute, pause, resume, validate, and hand off without reconstructing intent from chat history.

## Use When

- Initiating an epic, feature set, migration, or multi-step workstream.
- A user asks to plan work, break it into issues, or prepare a milestone checklist.
- Work will cross sessions, people, agents, repositories, or review boundaries.
- An existing issue is too ambiguous to execute safely.

## Do Not Use When

- Debugging one isolated bug whose scope, source, and validation are already clear.
- Writing a session log or end-of-session summary; use a handoff skill instead.
- Creating issues immediately when the user requested a plan for review first.

## Inputs To Check

- User request and named decision owner.
- Live tracker state: existing issues, milestones, parent issues, and dependencies.
- Repository-local workflow, branch, review, and source-of-truth rules.
- Roadmaps, specifications, accepted decision records, and relevant implementation evidence.
- Permissions and actions that require explicit human approval.

## Procedure

1. **Verify live planning state**
   - Search for duplicates and already completed work.
   - Read the relevant issue timeline or comments when they may refine the title.
   - Use live tracker state over stale planning documents.

2. **Name the requester and decision owner**
   - Record who requested the work and who can resolve scope or acceptance decisions.
   - Do not assume that the implementer owns product, security, or publication decisions.

3. **Define the desired outcome**
   - State what must exist or be true when the workstream is complete.
   - Distinguish review-ready output from fully approved or deployed completion.

4. **Record authoritative sources**
   - List the files, issues, specifications, datasets, or systems the executor must use.
   - State what must not be invented.
   - Define which source wins when sources conflict, or make the conflict a blocker.

5. **Create milestone-backed work units**
   - Group work into chronological, functional milestones.
   - Assign every non-trivial issue to an active milestone or the repository's backlog equivalent.
   - Keep each issue independently reviewable and testable.
   - Merge tiny cohesive changes; do not create issue bloat.

6. **Write a seven-part task contract for every issue**
   - Requester / decision owner.
   - Desired outcome.
   - Authoritative sources.
   - Acceptance criteria.
   - Scope and boundaries, including ask-first actions.
   - Blocker question path and exact resume condition.
   - Output handoff and required receipts or evidence.
   - Read `references/task-contract-template.md` when drafting the detailed specifications.

7. **Map dependencies and ownership**
   - Record parent/child and blocking relationships explicitly.
   - Identify the next reviewer or owner after implementation.
   - For cross-agent work, keep one accountable parent and give each delegate a bounded return path.

8. **Align branches and delivery artifacts**
   - Use the repository's branch convention when one exists.
   - If an issue ID is not available yet, use a clear `<id>` placeholder rather than inventing one.
   - State whether the expected handoff is a comment, document, commit, pull request, deployment, or decision.

9. **Separate acceptance from validation**
   - Acceptance criteria describe observable outcome or behavior.
   - Validation lists commands, tests, inspections, or evidence used to prove those criteria.
   - Do not use “tests pass” as the only product acceptance criterion.

10. **Define blocked and resume behavior**
    - Treat missing authority, conflicting sources, materially divergent interpretations, and irreversible or external actions as blockers.
    - Require one focused question on the canonical task record.
    - Record the last safe state and an objective resume condition.
    - Stop scoped execution until the answer arrives; resume the same task instead of creating a replacement.

11. **Present before creating**
    - Show the blueprint and call out assumptions, open decisions, and proposed milestones.
    - Do not create tracker items through an API until the user explicitly approves creation, unless their request already clearly authorizes creating them.

## Output Format

Render a concise Markdown blueprint:

```markdown
# Epic Planning Blueprint

## Desired outcome
...

## Milestone roadmap

### Milestone 1: <name>
- Issue A: <action-oriented title>

## Detailed issue specifications

### Issue A: <title>
- Requester / decision owner: ...
- Desired outcome: ...
- Authoritative sources: ...
- Scope and boundaries: ...
- Dependencies: ...
- Milestone: ...
- Branch: ...
- Acceptance criteria: ...
- Validation: ...
- If blocked: ...
- Output handoff / receipts: ...
```

Use `references/task-contract-template.md` for the complete issue body and review checklist.

## Rules

- Preserve repository-local policy over generic examples in this skill.
- Keep verified facts separate from assumptions and recommendations.
- Never expand an agent's authority through a task plan.
- Put secrets, credentials, private transcripts, and sensitive source content outside public issue bodies.
- Make blockers decision-grade: one question, why it blocks, and what answer resumes work.
- Do not mark a task fully complete when human review, approval, publication, deployment, or another required handoff remains.
- Avoid hardcoding one tracker, branch convention, label taxonomy, or agent runtime as a universal default.

## Global Skill Change Policy

This is a shared global skill. Do not add repository-specific details or credentials. Change its behavior only in a dedicated pull request with the repository-required version bump, changelog entry, registry update, and validation.
