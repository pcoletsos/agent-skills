# Local Overlay: [Skill Name] Overlay

Extends: [[Skill Name]](file:///Users/pcoletsos/repos/projects/agent-skills/skills/[skill-folder-name]/SKILL.md)

This overlay file injects repository-specific details, guidelines, and commands to override or extend the global skill logic.

---

## 🏗 Repository Context
Provide specific environment info:
- **Programming Languages / Frameworks**: (e.g. Next.js App Router, TypeScript, Python 3.11)
- **Local Test Commands**: (e.g. `npm run lint`, `npm run build`)
- **Key Files**: (e.g. `docs/design-reset-audit.md`, `site/lib/site-content.ts`)

---

## 🎛 Local Procedure Adjustments
Detail modifications to the global procedure:
1.  Before step 2 of the global checklist, perform this local check: ...
2.  Override step 4 of the global procedure with: ...

---

## 🚦 Local Boundary Controls (Negative Constraints)
Add specific local constraints:
- Do NOT run automated migrations unless explicitly approved by the user.
- Focus strictly on modifying components within the `/site/` subdirectory.
