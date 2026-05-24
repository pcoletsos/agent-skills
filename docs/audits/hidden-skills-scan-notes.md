# Hidden Skills Scan Notes

## Scan Method Used

1.  **Git Directory Identification:** Used the system command `find /Users/pcoletsos/repos -type d -name .git -prune` to recursively locate all git repositories.
2.  **Tracked Files Discovery:** For each discovered repository, executed `git ls-files` to inspect tracked files only, filtering for markdown (`*.md`), rules (`.cursorrules`, `.clinerules`), and agent-specific files (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `CONTRIBUTING.md`).
3.  **Content Analysis:** Ran a Python-based analyzer to parse file structures, extract sections (Purpose, Core Rules, Standard Workflows, Shorthand commands), and look for keywords like `agent`, `workflow`, `privacy`, `Obsidian`, and `shorthand`.
4.  **Classification and Scoring:** Automated comparison of extracted patterns against existing global skills in `agent-skills/skills/` using a structural classification script.

## Exact Repos Root Scanned

*   `/Users/pcoletsos/repos`

## Commands Run

```bash
# Repo search
find /Users/pcoletsos/repos -type d -name .git -prune

# Individual repo tracked files (within python loop)
git ls-files
```

## Folders Excluded

*   `.git/`
*   `node_modules/`
*   `.venv/`
*   `venv/`
*   `__pycache__/`
*   `dist/`
*   `build/`
*   `target/`
*   `.next/`
*   `.turbo/`
*   `coverage/`
*   `vendor/`
*   `tmp/`
*   `logs/`
*   `.pytest_cache/`
*   `.vscode/`
*   `.idea/`

## Repos Included

A total of 59 local repositories were successfully scanned under the root, including:
*   `projects/creator-knowledge-pipeline`
*   `projects/homelab/homelab-infra`
*   `projects/homelab/homelab-assets`
*   `projects/prompt-hub`
*   `projects/edge-workspaces-url-extractor`
*   `projects/clarity`
*   `projects/koletsos-portfolio`
*   `projects/awesome-n8n-templates`
*   `projects/llm-prompt-manager`
*   `projects/real-dedupe-renamer`
*   `knowledge/learning-vault`
*   `knowledge/career-playbook`
*   `knowledge/pcoletsos-architecture-lab`
*   `knowledge/shared-personal-finance`
*   `knowledge/storage-strategist`
*   `knowledge/arch-memos-and-labs`
*   `work/career-douka`
*   `work/career-lele`
*   `work/aliki-douka-writing-system`
*   (Plus 40 other utility, references, and fork repositories)

## Repos Skipped

*   `/Users/pcoletsos/repos/projects/agent-skills`: Skipped to prevent scanning the destination repository itself. Used exclusively as reference context.

## Limitations

*   **File Size Cap:** Evaluated only files up to 50KB to maintain token capacity.
*   **Command Output Truncation:** Highly verbose repository check logs were filtered to prevent output bloat.

## Anything That Needs Manual Review

*   **Overlay Structure:** Verify how the homelab-specific K3s/NUC validation parameters will merge with a global deployment skill once implemented.
*   **Career Playbook Scripts:** Inspect the integration of `python scripts/rebuild_company_indexes.py` with standard git-hooks or workflows before formalizing the local career rules.
