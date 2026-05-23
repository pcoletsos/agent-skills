# Global Skill Change Policy

Global agent skills are active code. Because multiple active repositories and diverse agent frameworks load these skills dynamically, modifications can trigger unexpected changes in agent behavior across all your workspaces.

To prevent erratic behavior and context leakage, we enforce a strict **Pull Request and Governance Policy** for the `agent-skills` repository.

---

## 🚫 1. No Mixed PRs (Strict Decoupling)

Under no circumstances should modifications to files under the `skills/` directory of the `agent-skills` repository be bundled with feature code or bug fixes in a consuming repository's Pull Request.

*   ❌ **Violating Flow**: You are working on a bug in `koletsos-portfolio`. You discover an issue with how `pr-review` behaves. You modify the symlinked `skills/pr-review/SKILL.md` and commit the change directly inside your `koletsos-portfolio` feature branch.
*   ✅ **Compliant Flow**: You identify a behavior error in `pr-review`. You open a terminal, switch to the `agent-skills` workspace, create a dedicated branch, modify the skill, write a detailed changelog entry, push, and merge the skill PR *first*. You then resume your feature work in `koletsos-portfolio`.

---

## 🚦 2. The Change Classification Matrix

We categorize modifications into two classes, each requiring different review rigor:

### Class A: Minor Typo or Syntax Fixes
*   **Examples**: Correcting grammatical spelling errors, fixing broken Markdown links, or improving formatting/rendering in agent viewers.
*   **Policy**: Low risk. Can be pushed directly to `main` (if local only) or submitted via a simple, quick PR. Does **not** require a version bump.

### Class B: Behavior or Procedural Modifications
*   **Examples**: Adding new checklists, deleting structural sections, changing guardrail rules, altering trigger conditions, or updating expected outputs.
*   **Policy**: High risk. **Must** use a branch and Pull Request. Requires an entry in the skill's local `CHANGELOG.md` file and a Semantic Versioning (SemVer) version bump.

---

## 📝 3. Commit and PR Specifications

When opening a Pull Request to modify a global skill, the authoring agent **MUST** complete the [skill-pr-template.md](file:///Users/pcoletsos/repos/projects/agent-skills/templates/skill-pr-template.md) and explicitly address these questions:

1.  **Why does this belong globally?**
    Explain why this change benefits other repositories. If it only benefits one project, it is rejected and should be implemented as a local overlay.
2.  **What is the behavior change?**
    Describe how an agent's execution or logic will differ before and after this change.
3.  **What is the regression risk?**
    Assess if this new instruction could confuse agents working in other languages, frameworks, or smaller sandbox environments.

---

## 🔄 4. Version Bumping Standards

We follow Semantic Versioning (SemVer) for skills:
*   **MAJOR bump (1.0.0, 2.0.0)**: Breaking procedural change. Completely restructures the skill flow, requires updating local consumer overlays, or alters the core purpose of the skill.
*   **MINOR bump (0.2.0, 0.3.0)**: Adds new checklists, steps, or rules while keeping the core purpose and output format backward-compatible.
*   **PATCH bump (0.1.1, 0.1.2)**: Clarifies existing steps, fixes formatting bugs, or refines phrasing to prevent agent confusion.
