# Skill Authoring Guide

Writing high-signal, reliable agent skills is an exercise in **deterministic instruction design**. AI agents process instructions literally. Vague phrasing, redundant steps, and excessive polite filler lead to context bloat, wasted tokens, and erratic agent behavior.

This guide provides the core principles for designing and authoring premium-grade global agent skills.

---

## 📐 1. The Anatomy of a Skill

A skill consists of three core components:
1.  **YAML Frontmatter**: Provides the agentic runtime with metadata about the skill's identity, version, and trigger rules.
2.  **SKILL.md**: The core Markdown document containing executable procedures and constraints.
3.  **References Folder (`references/`)**: Holds non-instructional context such as architectural diagrams, markdown logs, or sample layouts. Keep the instructions out of this folder to prevent agent confusion.

---

## ✍️ 2. Formatting standard: The 9-Section Contract

Every `SKILL.md` must implement these exact nine sections to maintain structural consistency:

### 1. Header & Metadata
Starts with the standard YAML block followed by the Primary `# Heading`.
```yaml
---
name: sample-skill
description: Activates when executing a specific specialized operation.
version: 0.1.0
status: draft
---
# Sample Skill Name
```

### 2. Purpose
A concise, 1-2 sentence statement of what high-level goal this skill accomplishes.

### 3. Use When
A highly explicit, bulleted list of triggers. This helps the orchestrator (or the agent itself) know when to load this file.

### 4. Do Not Use When
Clear boundaries indicating when the skill is **not** appropriate, helping to prevent false positive activations.

### 5. Inputs To Check
What context, files, environment variables, or databases the agent must inspect *before* running the procedure.

### 6. Procedure
The core step-by-step checklist. Use active verbs (e.g., "Inspect," "Compile," "Validate") and avoid passive voice (e.g., "The files should be looked at").

### 7. Output Format
Specify exactly what artifact, terminal output, or markdown layout the agent must generate, including code block languages or structure blocks.

### 8. Rules
Hard constraints and negative boundaries (e.g., "NEVER edit project files," "Do not suggest more than 3 items").

### 9. Global Skill Change Policy
A reminder pointing the agent to the separate PR policy and local changelog updates.

---

## 🎯 3. Writing Rules for Agent Instructions

To maximize execution reliability, write your Markdown text using these guidelines:

### A. Use Imperative, Precise Commands
*   ❌ **Bad**: "You should probably try to look at the project dependencies to check if something might be outdated."
*   ✅ **Good**: "Examine `package.json` or `requirements.txt` to identify outdated package dependencies."

### B. Establish Explicit Negative Constraints (Negative Guardrails)
LLMs are eager to please and frequently over-deliver (hallucinate or over-engineer). Always establish what the agent **must NOT do**.
*   *Example*: "Do NOT execute shell commands that modify files unless explicitly instructed by the user."
*   *Example*: "Do NOT include corporate credentials or specific database connection strings."

### C. Separate Reference Material from Executables
Agents get confused when reference examples are mixed directly into the procedural steps. 
*   Place raw mock inputs, logs, or large textual samples inside the `/references` subdirectory.
*   Link to these files using markdown links rather than embedding them inside the main procedural checklist.
