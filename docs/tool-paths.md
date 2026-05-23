# Tool Integration & Config Directories

AI coding agents inspect specific paths to find local rules, custom tools, and instruction skills. Because these paths are inconsistent across vendors, you must place your symlinks or copies in the exact locations expected by your target tool.

This document maps out the canonical directories for **Codex**, **Claude Code**, **Antigravity (Gemini)**, and **GitHub Copilot**.

---

## 🗺 System Directory Map

AI agents can read skills from either **Global Paths** (shared across all projects on your machine) or **Local Paths** (isolated to a single git repository).

```
~ (User Home)
├── .agents/skills/              ◄─── Codex (Global)
├── .claude/skills/              ◄─── Claude Code (Global)
└── .gemini/antigravity/skills/  ◄─── Antigravity (Global)

~/repos/projects/my-project/
├── .agents/skills/              ◄─── Codex (Local)
├── .claude/skills/              ◄─── Claude Code (Local)
├── .agent/skills/               ◄─── Antigravity (Local)
└── .github/skills/              ◄─── GitHub Copilot (Local)
```

---

## 🛠 Tool-Specific Configurations

### 1. Codex
*   **Global Path**: `~/.agents/skills/`
*   **Local Path**: `<repo>/.agents/skills/`
*   **Integration Guide**: Codex dynamically scans both paths on startup. It resolves naming conflicts by prioritizing the local repository-specific folder.

### 2. Claude Code
*   **Global Path**: `~/.claude/skills/`
*   **Local Path**: `<repo>/.claude/skills/`
*   **Integration Guide**: Claude Code loads these markdown files directly into its system prompt context. Keep the instructions extremely concise to conserve input tokens.

### 3. Antigravity (Gemini)
*   **Global Path**: `~/.gemini/antigravity/skills/`
*   **Local Path**: `<repo>/.agent/skills/`
*   **Integration Guide**: Antigravity treats files in these folders as active skills. You can verify loaded skills using the internal `/skills` command in supported interfaces.

### 4. GitHub Copilot Agents
*   **Global Path**: `~/.config/copilot/skills/`
*   **Local Path**: `<repo>/.github/skills/` or `<repo>/.agents/skills/`
*   **Integration Guide**: GitHub Copilot project-level agents scan the `.github/` folder for instructions. Symlinking global skills here helps Copilot align with standard guidelines.

---

## 🚀 Scripted Symlinking Example

To automate skill loading in a new project workspace, you can add a simple script or alias in your shell configuration (e.g. `~/.zshrc`):

```bash
# Add this function to your shell config
function link-agent-skill() {
  local SKILL_NAME=$1
  if [ -z "$SKILL_NAME" ]; then
    echo "Usage: link-agent-skill <skill-name>"
    return 1
  fi
  
  local GLOBAL_PATH="$HOME/repos/projects/agent-skills/skills/$SKILL_NAME"
  local LOCAL_DIR=".agents/skills"
  
  if [ ! -d "$GLOBAL_PATH" ]; then
    echo "Error: Global skill '$SKILL_NAME' does not exist."
    return 1
  fi
  
  mkdir -p "$LOCAL_DIR"
  ln -vs "$GLOBAL_PATH" "$LOCAL_DIR/$SKILL_NAME"
}
```

Then, in any new project directory, simply run:
```bash
link-agent-skill repo-triage
link-agent-skill pr-review
```
