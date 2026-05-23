## Skill Affected
- [ ] repo-triage
- [ ] pr-review
- [ ] architecture-review
- [ ] issue-planning
- [ ] agent-session-handoff
- [ ] tech-stack-visual
- [ ] New Skill: `[insert name]`

## Change Type
- [ ] **Class A**: Minor typo, link, or grammar fix (no version bump needed)
- [ ] **Class B**: Behavior/procedure change (requires version bump & changelog update)

## Context & Source
*   **Source Repository/Task**: (e.g. koletsos-portfolio / refactor authentication)
*   **Problem/Motivation**: Describe the agent error or optimization opportunity discovered in real-world use.

## Proposed Modifications
*   **What was changed**: Summary of edits made to instructions, checklists, or prompts.
*   **Why does this belong globally?** Why is this generic enough to benefit all repositories?
*   **Why not a local overlay?** Explain why this shouldn't be handled by a project-specific overlay instead.

## Behavior Impact & Risk
*   **Expected Behavior Change**: How will an agent act differently after this change?
*   **Regression Risk**: Could this confuse agents in other language environments? How did you mitigate this?

## Checklist
- [ ] Core instructions updated in `SKILL.md`
- [ ] `CHANGELOG.md` entry added for Class B changes
- [ ] Version bumped in YAML header of `SKILL.md` and in `registry.yaml`
- [ ] No client/proprietary credentials or paths included
