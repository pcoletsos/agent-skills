# Hidden Skills Inventory

## Summary

*   **Repos root scanned:** `/Users/pcoletsos/repos`
*   **Repos scanned:** 60
*   **Files inspected:** 1,296
*   **Total candidates found:** 10
*   **High-priority global skill candidates:** 3
*   **Likely updates to existing global skills:** 4
*   **Likely overlays:** 1
*   **Repo-local rules that should not be globalized:** 2

## Scan Root

*   **Agent-skills root:** `/Users/pcoletsos/repos/projects/agent-skills`
*   **Repos root scanned:** `/Users/pcoletsos/repos`
*   **Repos included:** 59 local repositories representing nested folders under `/Users/pcoletsos/repos/` (`projects/`, `work/`, `knowledge/`, `references/`, `scratch/`)
*   **Repos skipped:** 1 (`agent-skills` itself, used only as global reference context)

---

## Top Recommendations

Here are the top 10 candidates to act on first, ranked by priority and impact:

| # | Candidate Name | Category | Priority | Score (R/M/R) | Source Repos | Suggested Action |
|---|---|---|---|---|---|---|
| 1 | **Conversational Agent Git Flow / Shorthand Prompts** | global-skill-candidate | **High** | 5 / 5 / 2 | `creator-knowledge-pipeline`, `homelab-infra`, `career-playbook` | Create new global skill `agent-conversational-git` |
| 2 | **Obsidian-First Knowledge Vault Curation** | global-skill-candidate | **High** | 5 / 5 / 1 | `learning-vault`, `career-playbook`, `shared-personal-finance` | Create new global skill `knowledge-vault-curation` |
| 3 | **Structured LLM Generation & Analysis Tracking** | global-skill-candidate | **High** | 5 / 4 / 1 | `aliki-douka-writing-system` | Create new global skill `llm-run-tracking` |
| 4 | **Strict Repository Privacy Gates** | existing-skill-improvement | **High** | 5 / 5 / 1 | `creator-knowledge-pipeline`, `career-playbook`, `homelab-infra` | Update `repo-triage` and `pr-review` |
| 5 | **Agent Branch Naming and Git Hygiene Conventions** | existing-skill-improvement | **High** | 5 / 5 / 1 | `creator-knowledge-pipeline`, `homelab-infra`, `llm-prompt-manager` | Update `pr-review` and `issue-planning` |
| 6 | **Repository Decision & Memory Logs** | existing-skill-improvement | **High** | 5 / 5 / 1 | `learning-vault`, `career-playbook`, `pcoletsos-architecture-lab` | Update `agent-session-handoff` and `repo-triage` |
| 7 | **Architecture Diagram Curation & Versioning** | existing-skill-improvement | **Medium** | 5 / 4 / 1 | `homelab-infra`, `pcoletsos-architecture-lab` | Update `tech-stack-visual` and `architecture-review` |
| 8 | **Python Dependency & Sync Hygiene Using UV** | global-skill-candidate | **Medium** | 5 / 4 / 2 | `creator-knowledge-pipeline`, `sbstck-dl`, `storage-strategist` | Create new global skill `python-uv-hygiene` |
| 9 | **Homelab Cluster Service Onboarding Overlay** | overlay-candidate | **Medium** | 2 / 4 / 3 | `homelab-infra` | Create overlay on general deployment skill or keep local |
| 10 | **Grounded Career Listing Intake Workflow** | repo-local-rule | **Low** | 2 / 5 / 2 | `career-playbook`, `career-douka`, `career-lele` | Keep as repo-local rule |

*Score key: Reusability / Maturity / Risk (1-5 scale)*

---

## Candidate Global Skills

### 1. agent-conversational-git
*   **Source Repos:** `projects/creator-knowledge-pipeline`, `projects/homelab/homelab-infra`, `knowledge/career-playbook`, `work/career-douka`, `work/career-lele`, `projects/real-dedupe-renamer`, `knowledge/quiz-crafter`
*   **Source Files:** `CONTRIBUTING.md`, `AGENTS.md`, `CLAUDE.md`
*   **Summary:** Defines a standardized conversational vocabulary mapping shorthand commands (e.g. `what next?`, `start <task>`, `record it`, `publish it`, `propose it`, `land it`, `ship it`, `finish it`) directly to predictable, atomic Git commands (status checks, branch creation, structured committing, pushing, PR opening, squash-merging).
*   **Why it should become global:** This workflow is highly robust and consistently utilized across almost all of the developer's repositories. Moving it into a global skill gives any pairing agent an immediate, executable understanding of how to run local workflow loops conversationally.
*   **Risks:** Branch conventions (`codex/` vs `actor/`) or project-specific PR description requirements might need overlays.
*   **Suggested first version scope (0.1.0):** Implement standard mappings for the shorthand commands, a base branching rule, and Conventional Commit title validation.

### 2. knowledge-vault-curation
*   **Source Repos:** `knowledge/learning-vault`, `knowledge/career-playbook`, `work/career-douka`, `work/career-lele`, `knowledge/shared-personal-finance`, `work/aliki-douka-writing-system`
*   **Source Files:** `AGENTS.md`, `CONTRIBUTING.md`
*   **Summary:** Comprehensive rules for Obsidian-first/Markdown-first personal knowledge management (PKM) vault maintenance. Focuses on file structure rules (lowercase hyphen-separated names), shallow folders, Relative Markdown bidirectional links over wikilinks, strict duplicate avoidance, a standardized metadata block at the top of notes, Map of Content (MOC) index updates, and routing ambiguous inputs to an `inbox/` directory.
*   **Why it should become global:** Vault curation is a massive recurring pattern in the user's workspace, appearing across both personal and work repositories. Globalizing this skill ensures any LLM agent curating notes or documentation adheres to a flawless, standard Obsidian-safe layout.
*   **Risks:** Specific folder mappings (like `certifications/` vs `01-cv/`) are domain-specific and should be handled via repo overlays.
*   **Suggested first version scope (0.1.0):** Define base Markdown note shapes (`# Title`, `## Source`, `## Summary`, `## Notes`, `## Related`), relative linking mechanics, lowercase naming hygiene, and deduplication/search rules.

### 3. llm-run-tracking
*   **Source Repo:** `work/aliki-douka-writing-system`
*   **Source File:** `AGENTS.md`
*   **Summary:** A highly structured process for tracking and logging LLM prompt execution and analysis runs on text drafts, keeping a durable audit trail under folders named `runs/draft-vN/` containing `00-run-meta.md` (run metadata), `01-input.md` (unmodified prompt/input text), `02-output-raw.md` (raw unmodified output), `03-summary.md` (distilled takeaways), and `04-actions.md` (downstream tasks), coupled with a central `model-runs-log.md` register.
*   **Why it should become global:** This is an outstanding practice for AI agents performing content editing, generation, or deep code analysis, ensuring transparency and repeatability of LLM outputs across runs.
*   **Risks:** Folder structures could clutter the repo if not managed; should be recommended for projects that explicitly involve iterative LLM generation.
*   **Suggested first version scope (0.1.0):** Define folder naming rules, standard templates for run assets, and audit register update procedures.

### 4. python-uv-hygiene
*   **Source Repos:** `projects/creator-knowledge-pipeline`, `references/forks/sbstck-dl`, `knowledge/storage-strategist`
*   **Source Files:** `CONTRIBUTING.md`, `CLAUDE.md`, `AGENTS.md`
*   **Summary:** A structured workflow for maintaining Python project dependencies using the ultra-fast `uv` package manager. Mandates using `pyproject.toml` as source of truth, tracking `uv.lock` for frozen syncs, separating developer dependencies into extras, and running validation scripts (`uv sync --frozen`, `uv run pytest`, `uv run python -m [module] --help`).
*   **Why it should become global:** Standardizes Python workspace maintenance across all projects using the modern `uv` toolkit.
*   **Risks:** App names or specific test runners (pytest, unittest) must remain configurable.
*   **Suggested first version scope (0.1.0):** Standard sync and test validation guidelines, dependency segregation instructions.

---

## Existing Skill Improvements

### 1. repo-triage (Current: v0.1.1)
*   **Improvements Found:**
    *   **"what next?" command integration:** Integrate support for the shorthand `what next?` request as a native trigger, executing a rapid scan of Git status and open issues/milestones to suggest a singular immediate action.
    *   **Repository Memory Logs check:** Add a rule to verify the presence of `DECISIONS.md` and `MEMORY.md` (and load their context) during triage, preventing session-context loss.
    *   **Strict Privacy Gate validation:** Check for the presence of credentials, real databases, cookie files, or raw content transcripts in active folders, blocking triage if a leak is identified.
*   **Real Repo Pattern Source:** `creator-knowledge-pipeline`, `homelab-infra`, `learning-vault`

### 2. pr-review (Current: v0.1.0)
*   **Improvements Found:**
    *   **Agent Git Hygiene checks:** Validate branch naming conventions (`<actor>/<type>/<scope>/<task>-<id>`) and PR Conventional Commit formatting before PR submission or squash-merge.
    *   **Strict Privacy Gate verification:** Include a checklist to scan PR diffs for sensitive data leaks (real credentials, private URLs, child names/faces, API keys).
    *   **Unedited Raw Output rule:** Verify that LLM analysis artifacts or raw generation logs (if tracked) remain completely unedited, keeping the audit trail pristine.
*   **Real Repo Pattern Source:** `creator-knowledge-pipeline`, `homelab-infra`, `aliki-douka-writing-system`

### 3. issue-planning (Current: v0.1.0)
*   **Improvements Found:**
    *   **Issue-First branching alignment:** Ensure that issue creation maps directly to a target branch format (`codex/feat/scope/task-<id>`) to keep work scoped and decoupled.
    *   **Milestone Hygiene:** Mandate that every non-trivial issue must belong to a thematic milestone or a catch-all `Backlog` milestone, ensuring no issues float unassigned.
*   **Real Repo Pattern Source:** `creator-knowledge-pipeline`, `homelab-infra`

### 4. agent-session-handoff (Current: v0.1.0)
*   **Improvements Found:**
    *   **Memory & Decision Log Updates:** Enforce updating `DECISIONS.md` when structural/workflow conventions change, and `MEMORY.md` for new stable runtime assumptions, ensuring zero-loss state transfers across agent boundaries.
    *   **`progress.md` maintenance:** Check for a repo-local `progress.md` file and keep it updated with current statuses, blockers, and next steps as part of the session handoff.
*   **Real Repo Pattern Source:** `learning-vault`, `career-playbook`, `pcoletsos-architecture-lab`

### 5. tech-stack-visual (Current: v0.1.0) / architecture-review (Current: v0.1.0)
*   **Improvements Found:**
    *   **Durable Diagram Rendering:** Treat committed diagrams (Mermaid, Excalidraw, PNGs) under `docs/architecture/diagrams/vN/` as first-class, versioned documentation, rather than transient build outputs.
    *   **Image Sizing Standards:** Incorporate rules for social/documentation dimensions (e.g. LinkedIn dimensions) when generating architecture or technical graphics.
*   **Real Repo Pattern Source:** `homelab-infra`, `pcoletsos-architecture-lab`

---

## Overlay Candidates

### 1. homelab-service-onboarding (Overlay for deployment/validation workflows)
*   **Source Repo:** `projects/homelab/homelab-infra`
*   **Source Files:** `AGENTS.md`, `docs/operations/runbooks/service-onboarding-checklist.md`
*   **Summary:** Provides concrete validation and onboarding checklist for cluster microservices, specifying K3s on `takis-nuc` as the default runtime boundary, run command `kubectl kustomize clusters/takis-nuc`, and tracking state changes in `current-state.md` and `runtime-memory.md`.
*   **Why it is an overlay:** These rules contain private local hostnames (`takis-nuc`) and environment-specific paths. They represent a classic overlay candidate that overlays a global `service-onboarding` skill with homelab-specific commands and host paths.

---

## Repo-Local Rules

### 1. Grounded Career Intake Workflow
*   **Source Repos:** `knowledge/career-playbook`, `work/career-douka`, `work/career-lele`
*   **Source Files:** `AGENTS.md`, `00-setup/grounded-intake-workflow.md`, `00-setup/README.md`
*   **Why it should remain local:** This workflow is heavily tied to career search layouts (`01-cv/`, `05-companies/`, `06-applications/`), connection ID patterns (`NET-<COMPANY>-NN`), and specialized python scripts (`python scripts/rebuild_company_indexes.py`). Keeping it local prevents global pollution while ensuring rigorous execution.

### 2. Kids-Related Privacy Policy
*   **Source Repo:** `work/aliki-douka-writing-system`
*   **Source File:** `AGENTS.md`
*   **Why it should remain local:** Enforces strict media guidelines (no child faces, full names, or location details; prefer toys-only, blur, or hands-only) for public children-focused brand materials. Highly specific to the brand publishing domain.

---

## Duplicates and Common Patterns

1.  **Conversational Prompt Commands:** Exactly the same conversational prompts (`start <task>`, `record it`, `ship it`, etc.) are defined across `creator-knowledge-pipeline`, `homelab-infra`, `career-playbook`, `career-douka`, and `career-lele`.
2.  **Read Order & Live Sources:** The exact same "Read First" sequences (linking CONTRIBUTING.md and AGENTS.md) and "GitHub is Live Source of Truth" statements exist in `homelab-infra`, `creator-knowledge-pipeline`, `career-playbook`, `llm-prompt-manager`, and others.
3.  **Obsidian Folder Structure Style:** Naming (lowercase, hyphen-separated), relative linking, and MOC curation are highly duplicated between `learning-vault`, `career-playbook`, `career-douka`, and `career-lele`.

---

## Suggested Next Actions

1.  **Extract `agent-conversational-git`:**
    *   *Action:* Create a dedicated PR to add `agent-conversational-git` as a new draft global skill under `skills/agent-conversational-git/`.
    *   *Rationale:* This standardizes the shorthand git prompt vocabulary across all repositories, removing duplicate descriptions from individual `AGENTS.md`/`CONTRIBUTING.md` files.
2.  **Create `knowledge-vault-curation`:**
    *   *Action:* Create a new global skill `knowledge-vault-curation` to standardise markdown vault operations.
3.  **Harden existing `pr-review` and `repo-triage`:**
    *   *Action:* In a separate PR, update the global `pr-review` and `repo-triage` skills with "Strict Privacy Gate" checks and "Git Branch Hygiene" checks extracted from `creator-knowledge-pipeline`.
4.  **Implement Homelab Overlay:**
    *   *Action:* Configure `homelab-infra` to import a global `service-onboarding` skill and apply its local K3s/NUC validation parameters as an overlay.
