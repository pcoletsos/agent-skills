# Architecture Philosophy: Reusable Agent SOPs

AI agents are powerful, but they perform best when constrained by highly optimized, battle-tested guidelines. We treat agent instructions as **code**. Just like writing software libraries, agent instructions should be modular, versioned, decoupled, and DRY (Don't Repeat Yourself).

This document outlines the core architectural and behavioral philosophy behind the `agent-skills` repository.

---

## 🧩 1. Skills are Standard Operating Procedures (SOPs)

A skill is not a codebase; it is a **Standard Operating Procedure (SOP)**. 
When an agent is assigned a task (e.g., checking code quality, designing an issue milestone, summarizing a work session), it should not rely solely on its default weights or broad web-scraped patterns. Instead, it should pull a targeted skill designed for that exact task.

By defining SOPs:
*   We ensure **repeatable excellence**: agents execute complex tasks the same way every time.
*   We prevent **prompt drift**: as LLMs are upgraded, keeping explicit local constraints keeps behavior predictable.
*   We enable **rapid onboarding**: new agent frameworks or instances can instantly read the skill folders and operate at a veteran standard.

---

## 📈 2. Leveling Up Globally Through Real Work

The best agent instructions are not designed in a vacuum; they are forged in real-world software engineering. 
When you pair-program with an agent in a specific project and discover a better way to structure a handoff or design a PR review, **that improvement belongs in the global repository**.

By refining a global skill:
*   An improvement made while working on one repository automatically upgrades the intelligence of the agents working across *all* of your other repositories.
*   We create a compounding "flywheel" effect—every completed task has the potential to make your global agent suite permanently smarter.

---

## 🚫 3. Strict Boundary Control (No Global Pollution)

While global leveling up is powerful, it carries a significant risk: **context leakage**. 
If a project-specific path, a proprietary database name, or a local package dependency creeps into a global skill, it will break agent behavior in other unrelated projects.

*   **Rule**: Keep global skills abstract and functional.
*   **Solution**: Use repo-local overlays for specific context. A global skill should describe *how to think* and *what process to follow*, while the local overlay provides *what files to look at* and *what local limits to obey*.

---

## 🔗 4. The Write-Through Nature of Symlinks

When developers consume global skills, they frequently do so using filesystem symlinks (`ln -s`). 
Symlinks are incredibly efficient, but they possess a dangerous property: **write-through behavior**.

*   Because a symlink is a pointer, if a developer instructs an agent to "improve this local skill instruction," the agent will write directly back to the global skill in the `agent-skills` repository!
*   If this is done carelessly, it can pollute the global repository with project-specific code and commit messages.
*   **The Guard**: We enforce separate, isolated Git flows. Any modification to a global skill must be verified, versioned, and committed as a dedicated PR in the `agent-skills` workspace, not as a side-effect of local feature development.

---

## 🚪 5. Escapes Hatches: Overlays and Forks

Every rule has an exception. A rigid system that cannot bend will inevitably be bypassed or deleted. We solve this by providing two explicit architectural escape hatches:

```
                  ┌──────────────────────┐
                  │ Global Skill (100%)  │
                  └──────────┬───────────┘
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
   [Local Overlays]                    [Forked-Local]
   Keep global logic;                  Break away entirely;
   inject local parameters.            copy & diverge.
```

1.  **Overlays**: The global skill is preserved, but local files append specific parameters (e.g., specific folder paths to ignore, preferred lint commands).
2.  **Forks**: If a repository has highly unique, custom needs that make global integration impossible, the developer has full permission to copy the skill physically and delete the symlink. This local fork diverged permanently, protecting the global repository from unwanted edge cases.
