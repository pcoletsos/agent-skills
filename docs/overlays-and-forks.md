# Escaping Rigidness: Overlays and Forks

Systems that enforce absolute global rigidity eventually break. Software projects are inherently diverse: a frontend project in Next.js has vastly different operational goals than an Infrastructure-as-Code project in Terraform or a scratch python tool.

To support this diversity without polluting the global `agent-skills` database, we provide two explicit escape hatches: **Local Overlays** and **Local Forks**.

---

## 🎛 1. Local Overlays (Extend & Preserve)

An overlay is the preferred mechanism for customizing a skill. It allows a project to **inherit 100% of the global procedure** while feeding the agent repo-specific parameters (such as preferred frameworks, unique lint rules, or folder structures).

### How it Works:
1.  The agent identifies that a skill (e.g. `pr-review`) is active.
2.  The agent reads the symlinked `skills/pr-review/SKILL.md` to load the standard procedure.
3.  The agent checks for a sibling file named `pr-review-overlay.md` in the local repository's skill folder.
4.  If found, the agent merges the local instructions, allowing them to override or append specific global steps.

### Example Folder Structure:
```
my-web-app/
└── .agents/
    └── skills/
        ├── pr-review ──► (Symlink to agent-skills/skills/pr-review)
        └── pr-review-overlay.md  <-- Project-specific overlay file
```

### Writing a Clean Overlay:
Keep overlays small, focusing exclusively on:
*   Project-specific file paths (e.g. "Ignore directories `/vendor/` or `/dist/`").
*   Custom command targets (e.g. "Run `npm run lint` and `npm run build`").
*   Unique design constraints (e.g. "We strictly follow the V1 content schema defined in `docs/schema.yaml`").

*Use the starter skeleton at [templates/overlay-template.md](file:///Users/pcoletsos/repos/projects/agent-skills/templates/overlay-template.md) to build overlays.*

---

## 🍴 2. Local Forks (Break Away Completely)

Forking is the physical copy-pasting of a global skill folder into your local repository, severing any connection to the global repository.

### How it Works:
```bash
# Severs the global connection and creates a local physical folder
rm .agents/skills/pr-review
cp -r ~/repos/projects/agent-skills/skills/pr-review .agents/skills/pr-review
```

### When to Fork (The 2% Exception Rule):
You should only fork a skill under extreme circumstances:
1.  **Framework Incompatibility**: The project uses custom internal agent orchestrators that require custom frontmatter fields or structured JSON formats incompatible with the standard global YAML keys.
2.  **Absolute Context Divergence**: The project's build, test, and release cycle is so unique (e.g., embedded firmware programming or legacy mainframe systems) that applying standard web/software procedures is impossible.
3.  **Strict Security Compartmentalization**: The project is subject to high-security compliance or non-disclosure agreements that prohibit referencing any external/shared tools.

---

## ⚖️ How to Choose

Use this simple score sheet to decide the appropriate mode:

| If your requirement is... | Overlay | Fork |
| :--- | :---: | :---: |
| *Adding project-specific test or lint commands* | ✅ | ❌ |
| *Excluding specific folders from triaging* | ✅ | ❌ |
| *Targeting particular schema or component boundaries* | ✅ | ❌ |
| *Writing custom JSON parser rules for an in-house tool* | ❌ | ✅ |
| *Handling proprietary client NDAs requiring total isolation* | ❌ | ✅ |
| *Altering the core purpose of a skill* | ❌ | ✅ |
