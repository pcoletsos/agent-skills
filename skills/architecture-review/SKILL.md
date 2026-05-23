---
name: architecture-review
description: Review architectural design, module boundaries, package coupling, dependency flows, and long-term codebase maintainability.
version: 0.1.0
status: draft
---

# Architecture Review Skill

## Purpose
Analyze the structural boundaries, data layers, dependency couplings, and interface contracts of a system to verify that proposed edits align with clean, maintainable, and scalable software design practices.

## Use When
- Designing a major new feature or subsystem.
- A user asks: "How should I structure this new module?" or "Can you review our design patterns?"
- Refactoring complex components that contain excessive coupling or tech debt.

## Do Not Use When
- Doing basic code quality audits or checking for syntax correctness (use `pr-review`).
- Doing simple repository triaging (use `repo-triage`).

## Inputs To Check
- Existing design documents under `/docs` or the repository wiki.
- Configuration dependencies in `package.json`, `Cargo.toml`, or configuration modules.
- Folder layouts and boundary interfaces.

## Procedure
1.  **Identify Current Architecture**: Inspect directories and read architectural docs to determine the system's design pattern (e.g. Model-View-Controller, clean architecture, hexagonal, micro-services, mono-repo).
2.  **Examine Coupling & Boundaries**: Audit the code to identify circular dependencies, tight coupling, leaky abstractions, or shared-state violations.
3.  **Evaluate Strategic Fit**:
    *   Assess if proposed edits fit cleanly within the existing structural patterns.
    *   Look for potential "architecture drift"—where incremental changes quietly violate original design rules.
4.  **Prioritize Small, Incremental Steps**: Prefer making small, self-contained adjustments to code structures over massive, high-risk, multi-file refactorings.
5.  **Separate Tactical from Strategic Recommendations**:
    *   **Tactical**: Immediate, high-signal, risk-free adjustments needed to unblock a feature or fix a bug under the current architecture.
    *   **Strategic**: Long-term structural upgrades, migration paths, or refactoring designs that require deep planning and multi-stage reviews.

## Output Format
Render a clean Markdown architecture report:
```markdown
# Architecture Review Report

## 🏗 Structural Blueprint
- **Design Pattern**: (e.g. Clean architecture with repository pattern)
- **Primary Modules**: ...
- **Data Flow**: ...

## 🔍 Structural Observations
- **Coupling Risks**: ...
- **Boundary Violations**: ...

## 🚀 Recommended Approach

### 🛠 Tactical Steps (Immediate)
- [ ] Refactor interface X to accept generic parameters...
- [ ] Separate db models from frontend props...

### 🔭 Strategic Directions (Long-Term)
- Migrate from monolithic structure to domain folders...
```

## Rules
- **Do NOT propose sweeping architectural overhauls for simple tasks.** Maintain a high respect for the existing author's design decisions unless they explicitly violate functional requirements.
- Focus strictly on high-cohesion and low-coupling principles.

## Global Skill Change Policy
This is a shared, global skill. Do NOT add repo-specific details or credentials. Any modifications to this skill's behavior must be performed in a dedicated Pull Request within the `agent-skills` repository, requiring a version bump and an entry in `CHANGELOG.md`.
