# Consuming Agent Skills

This guide explains how to import and consume skills from the central `agent-skills` repository into your active development repositories. We support three integration modes (the **90/8/2 Model**): **Linked-Global**, **Local Overlay**, and **Forked-Local**.

---

## 🔗 1. Linked-Global Mode (90% of Use Cases)

In this mode, the target repository points directly to a global skill folder via a filesystem symlink. This guarantees that any updates made to the central `agent-skills` repo are instantly available to the project.

### Structural Layout:
```
my-active-project/
├── .agents/
│   └── skills/
│       └── repo-triage ───► (Symlink to: ~/repos/projects/agent-skills/skills/repo-triage)
├── src/
└── README.md
```

### ⚠️ IMPORTANT: Individual Symlinks Only
Always symlink **individual skill folders**, never the parent `skills/` directory itself. 
*   **Correct**: `ln -s ~/repos/projects/agent-skills/skills/repo-triage .agents/skills/repo-triage`
*   **Incorrect**: `ln -s ~/repos/projects/agent-skills/skills .agents/skills`

Linking the parent directory exposes *all* skills to the agentic environment at once, causing massive context bloat and increasing the risk of false-positive prompt triggers.

### Setup Commands:
```bash
# Navigate to your target repository
cd ~/repos/projects/my-active-project

# Create the local skills container directory
mkdir -p .agents/skills/

# Symlink a specific skill (e.g., repo-triage)
ln -s ~/repos/projects/agent-skills/skills/repo-triage .agents/skills/repo-triage
```

---

## 🎛 2. Local Overlay Mode (8% of Use Cases)

An overlay extends a global skill with repo-specific parameters (like framework choices, specific test commands, or database names) without editing the global skill files.

The local agent reads the global `SKILL.md` first to load the core procedure, and then reads a local overlay file to adjust the boundary settings.

### Structural Layout:
```
my-active-project/
├── .agents/
│   └── skills/
│       ├── repo-triage ───► (Symlink to: ~/repos/projects/agent-skills/skills/repo-triage)
│       └── repo-triage-overlay.md  <-- Local file containing repo-specific rules
```

### Example Overlay structure:
```markdown
# Local Overlay: repo-triage-overlay

Extends: [repo-triage](file:///Users/pcoletsos/repos/projects/agent-skills/skills/repo-triage/SKILL.md)

## Repo Context
- Target Stack: Next.js (App Router), TypeScript, Tailwind CSS.
- Core Tests: `npm run lint` and `npm run build`.

## Overridden Rules
- Always prioritize issues marked with the `critical-bug` label before inspecting feature milestones.
```

*See [templates/overlay-template.md](file:///Users/pcoletsos/repos/projects/agent-skills/templates/overlay-template.md) to quickly bootstrap a new overlay.*

---

## 🍴 3. Forked-Local Mode (2% of Use Cases)

Forking is the permanent physical duplication of a skill folder. It severs the link to the global repository. Use this only when a project has exceptionally complex requirements that diverge completely from standard procedures.

### Structural Layout:
```
my-active-project/
├── .agents/
│   └── skills/
│       └── repo-triage/       <-- Complete physical copy of the skill folder
│           ├── SKILL.md       <-- Custom instructions edited locally
│           └── CHANGELOG.md
```

### Setup Commands:
```bash
# Navigate to your target repository
cd ~/repos/projects/my-active-project

# Create directory
mkdir -p .agents/skills/

# Copy the skill directory physically (no symlink)
cp -r ~/repos/projects/agent-skills/skills/repo-triage .agents/skills/repo-triage
```

### When to Fork:
*   The project uses custom internal agent orchestrators that require incompatible YAML schema fields.
*   The workflow relies on unique manual stages or proprietary compliance checks that are prohibited from being shared globally.
