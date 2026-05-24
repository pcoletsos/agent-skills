---
name: issue-planning
description: Turn rough project goals or feature requests into structured milestones, clean GitHub issue descriptions, and precise acceptance criteria.
version: 0.2.0
status: draft
---

# Issue Planning Skill

## Purpose
Deconstruct a high-level system goal, user request, or feature roadmap into logical milestones, detailed issue lists, dependency trees, and explicit acceptance criteria.

## Use When
- Initiating a new development epic or feature set.
- A user states: "Let's plan this out," "Break this work down into issues," or "Write a milestone checklist."
- You need to structure your development workflow prior to opening pull requests.

## Do Not Use When
- Debugging a single, isolated bug with a known resolution path.
- Generating developer logs or session summaries (use `agent-session-handoff`).

## Inputs To Check
- Existing roadmap files (e.g. `docs/github-plan.md` or wiki entries).
- Live milestones on GitHub (using `gh api` or `gh milestone list` if connected).
- Project documentation and user specifications.

## Procedure
1.  **Clarify Desired Outcomes**: Synthesize the user's instructions and system context to formulate a single, unambiguous "definition of done" for the entire epic.
2.  **Define Milestones (Milestone Hygiene)**: Group logical feature blocks into chronological phases (milestones). Ensure that every non-trivial issue is explicitly mapped to a specific milestone (e.g., `Milestone 1`) or routed to a catch-all `Backlog` milestone so that no issues remain unassigned. Each milestone should represent a deployable, functional unit of value.
3.  **Generate Crisp Issues with Branch Alignment**:
    *   For each work unit, create a descriptive, action-oriented title (e.g., "feat(auth): implement token refresh flow").
    *   Draft a concise description outlining the technical implementation details and specify a target branch structure mapped strictly to the git hygiene schema (`<actor>/<type>/<scope>/<task>-<id>`).
4.  **Establish Acceptance Criteria**: Every issue **MUST** have a bulleted list of explicit, testable criteria (e.g., "Verify that the database has column X," "Linter passes synchronously").
5.  **Map Dependencies**: Clearly flag which issues depend on others. Use standard parent/child indicators to construct a clean dependency path.
6.  **Optimize Issue Count**: Avoid "issue bloat." Group small, highly cohesive tweaks into a single, cohesive issue rather than flooding the board with dozens of trivial items. Prefer small, reviewable, and testable work items.

## Output Format
Render a clean Markdown issue blueprint:
```markdown
# Epic Planning Blueprint

## 🎯 High-Level Goal
...

## 🗺 Milestone Roadmap

### 📦 Milestone 1: [Name]
*Status: Target Date / Order*
- **Issue #1**: [Title]
- **Issue #2**: [Title]

---

## 🛠 Detailed Issue Specifications

### Issue A: [Title]
- **Scope**: What specific module or files are affected.
- **Implementation Strategy**: Concise list of required files/procedures.
- **Dependencies**: Resolves after Issue B is completed.
- **Acceptance Criteria**:
  - [ ] Criterion 1
  - [ ] Criterion 2
```

## Rules
- Keep issues scoped to independent units that can be code-reviewed in under 15 minutes.
- Do NOT auto-create issues via API without presenting the blueprint to the user for explicit approval first.
- **Mandatory Milestones**: Every planned work item must be assigned to an active milestone or explicitly designated as part of the `Backlog`. Floating or unassigned issues are not permitted.
- **Explicit Branch Specs**: Include the exact branch naming structure directly within each issue's specification to maintain a tight coupling between issue planning and development hygiene.

## Global Skill Change Policy
This is a shared, global skill. Do NOT add repo-specific details or credentials. Any modifications to this skill's behavior must be performed in a dedicated Pull Request within the `agent-skills` repository, requiring a version bump and an entry in `CHANGELOG.md`.
