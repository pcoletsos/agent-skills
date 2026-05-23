# Consuming Agent Skills

This guide explains how to import, configure, and consume skills from the central `agent-skills` repository into your active development repositories.

---

## 🎯 Recommended Consumption Model

To keep our workflows highly structured and avoid custom configuration sprawl, we recommend the **90/8/2 Model**:

- **Linked-Global (90%)**: Use by default. Directly links standard skills without duplicating code.
- **Overlay (8%)**: Use when the global skill is mostly correct but requires repository-specific boundaries or metadata (e.g. test frameworks, package names).
- **Forked-Local (2%)**: Reserved strictly as a last resort exception when a project demands radically different agent behaviors or schemas.

---

## 🏗️ Three Consumption Modes Explained

### 1. Linked-Global
*   **Definition**: A direct filesystem symlink pointing from your project's local config folder to a global skill folder.
*   **Use Case**: Default behavior for reusable skills like `repo-triage`, `pr-review`, etc.
*   **Setup**: Allows a project to dynamically receive all global updates instantly.

### 2. Overlay
*   **Definition**: A local repository extension configured alongside a symlinked global skill.
*   **Use Case**: Used when a global skill's baseline procedure is correct, but the repository needs custom local parameters (e.g., target stack, linter configuration).

### 3. Forked-Local
*   **Definition**: A physical copy of the global skill folder placed directly in the repository's configuration path.
*   **Use Case**: Used only when a repository has unique, custom behaviors or specialized orchestrations that can never be generalized.
*   **Trade-off**: The skill will no longer receive any updates from the global repository.

---

## ⚠️ The Behavior of Symlinks

When operating with Linked-Global or Overlay modes, remember these critical behaviors of filesystem symlinks (`ln -s`):

1. **Editing a symlinked file/folder edits the global skill**: If an agent or human editor makes changes to a file inside the symlinked skill directory, those edits apply directly to the original files in your global `agent-skills` repository. Be careful not to pollute global skills with local context.
2. **Deleting files inside a symlinked skill folder affects the global skill**: Deleting a file under the symlinked folder deletes the file from the global `agent-skills` repository.
3. **Deleting the symlink itself does NOT delete the global skill**: You can safely delete the symbolic link file or symlinked directory representation from your child repository's filesystem without harming the global files.

---

## 🔌 Tool Paths & Configurations

Depending on the agent or development environment you use, configure one of the following directories.

### Global vs. Local Config Directories

| Tool | Global Path (Home Directory) | Local Path (Repository Root) |
| :--- | :--- | :--- |
| **Codex / portable Agent Skills** | `~/.agents/skills/` | `<repo>/.agents/skills/` |
| **Claude Code** | `~/.claude/skills/` | `<repo>/.claude/skills/` |
| **Antigravity (Gemini)** | `~/.gemini/antigravity/skills/` | `<repo>/.agent/skills/` |
| **GitHub Copilot-style skills** | *(N/A)* | `<repo>/.github/skills/` or `<repo>/.agents/skills/` |

---

## 🔗 Setup & Example Symlink Commands

Always symlink **individual skill folders**, never the parent `skills/` folder. Symlinking the entire `skills/` directory exposes every skill at once, causing extreme context bloat and risk of prompt triggers.

To link an individual skill (e.g., `repo-triage`), run:

```bash
# 1. Create the target folder in your repository (example for Codex)
mkdir -p .agents/skills/

# 2. Symlink the individual skill folder
ln -s ~/repos/projects/agent-skills/skills/repo-triage .agents/skills/repo-triage
```

---

## 📁 Recommended Child Repo Layout

When configuring a child repository with various agentic frameworks and overlays, organize it using the following structure:

```
<repo>/
├── .agent/              <-- Local folder for Antigravity (Gemini)
│   └── skills/
├── .agents/             <-- Local folder for Codex / general tools
│   └── skills/
├── .claude/             <-- Local folder for Claude Code
│   └── skills/
├── .github/             <-- GitHub folder (e.g. Copilot custom skills)
│   └── skills/
├── skills-overrides/    <-- Directory containing custom local markdown overlays
└── .skillrc.yaml        <-- Local configuration mapping overlay boundaries
```

---

## ⚙️ Example `.skillrc.yaml` File

A `.skillrc.yaml` file resides at the child repository root to coordinate local configurations, overlay references, or execution parameters without altering the global skill.

```yaml
# Local Skill Configurations
repo: "my-custom-project"
version: "1.0.0"

skills:
  repo-triage:
    enabled: true
    mode: overlay
    overlay_path: "skills-overrides/repo-triage-overlay.md"
    params:
      tech_stack: ["Next.js", "TypeScript", "TailwindCSS"]
      test_cmd: "npm run test"
      lint_cmd: "npm run lint"

  pr-review:
    enabled: true
    mode: linked-global
```

---

## ⚖️ When to Update Global vs. Create Overlay

Use the following guidelines to decide where to introduce a change:

### Update the Global Skill:
- The change fixes a general bug, typo, or structural error in a procedure.
- The workflow step is universally applicable (e.g., adding an "E2E tests" checklist item to `pr-review`).
- You are improving a methodology that benefits all developer workspaces.

### Create a Local Overlay:
- The change is specific to a technology stack not used globally (e.g. specialized mobile configs).
- The behavior involves private credentials, company-specific hostnames, or internal tooling paths.
- The rule is highly experimental and you want to test it locally first.

---

## 🚀 Separate PR Rule for Global Skill Changes

All modifications to files within the global `skills/` directory **MUST** be performed in a dedicated, isolated Pull Request in the `agent-skills` repository.

- **Do NOT** bundle a global skill enhancement with local feature development or bug fixes in a consuming repository.
- Bundling edits poses the risk of introducing unintended behavioral regressions globally or polluting the shared workspace with local contexts.
- Each global update requires a version increment, updating the skill's local `CHANGELOG.md`, and keeping the `registry.yaml` registry in sync.
