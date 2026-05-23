# AGENTS.md

> **Operating Manual for AI Agents working inside the `agent-skills` repository.**

Welcome, agent. You are contributing to the source of truth for reusable global agent skills. Because other systems pull directly from this repository to guide their autonomous decisions, you must maintain a highly disciplined, precise, and modular mindset. 

Read these rules carefully before making any edits.

---

## 🛑 Core Agent Directives

1.  **Maintain Global Genericism**:
    *   Treat this repo as the absolute source of truth for reusable, global skills.
    *   **NEVER** put client-specific names, private paths, internal hostnames, corporate repository details, or proprietary credentials in global skills.
    *   Keep all instructions, folders, and scripts generalized. If an example is needed, use standard mock formats (e.g., `my-project`, `user-db`).
    *   If you are unsure whether a rule belongs in a global skill, put it in an **overlay template** or local repo documentation.

2.  **Strict Separate PR Policy**:
    *   Changes to global skills must occur in dedicated, standalone Pull Requests.
    *   Do not bundle a skill enhancement with feature development or bug fixes in a consuming repository. 

3.  **Behavior-Changing Edits Require Changelogs & Bumps**:
    *   Any change to a skill's instructions, prompts, or procedures requires updating the corresponding skill's `CHANGELOG.md` under `skills/<skill-name>/CHANGELOG.md`.
    *   Increment the version number following Semantic Versioning (SemVer) rules. Start new drafts at `0.1.0`.

4.  **No Heavy Frameworks**:
    *   Do not write complex orchestrations, heavy shell script packages, or massive sync CLI wrappers unless explicitly requested by the USER.
    *   Keep the repository's primary focus on crisp, lightweight Markdown documentation and easy-to-read schema files.

5.  **Keep Instructions Short, Atomic, and Testable**:
    *   Prefer declarative bulleted lists over lengthy conversational paragraphs.
    *   Design each skill to perform exactly **one** distinct operation.
    *   Write checklists with clear criteria so an agent can verify their own output.

6.  **Registry Upkeep**:
    *   Whenever you add, delete, rename, or update the version/status of a skill, you **MUST** update [registry.yaml](file:///Users/pcoletsos/repos/projects/agent-skills/registry.yaml) immediately to maintain synchronization.

---

## 🛠 File Layout Rules

Ensure new skills conform to this structural standard:

```
skills/<skill-name>/
├── SKILL.md          <-- Markdown skill instructions (with YAML frontmatter)
├── CHANGELOG.md      <-- Local SemVer version changelog
└── references/       <-- Heavy context, examples, templates (no instructions)
    └── README.md
```

### SKILL.md Structure:
Every `SKILL.md` must start with this YAML header:
```yaml
---
name: skill-name
description: Clear, action-oriented trigger description.
version: X.Y.Z
status: draft | active | deprecated
---
```

Followed immediately by:
*   `# Skill Name`
*   `## Purpose`
*   `## Use When`
*   `## Do Not Use When`
*   `## Inputs To Check`
*   `## Procedure`
*   `## Output Format`
*   `## Rules`
*   `## Global Skill Change Policy`

---

## 🚀 Shorthand Prompt Commands

If a user prompts you using these commands, execute the designated sequence:

*   **`create skill <name>`**: Initialize a new skill using `/templates/skill-template/`, add it to `registry.yaml`, and present the proposed draft.
*   **`bump skill <name> <patch|minor|major>`**: Run the version increment sequence, update the local `CHANGELOG.md`, and update `registry.yaml`.
*   **`validate registry`**: Run the self-check sequence to make sure all skills under `skills/` match their declarations in `registry.yaml`.
