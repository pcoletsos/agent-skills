---
name: python-uv-hygiene
description: Procedures for managing Python virtual environments, dependencies, and validation tasks using the uv package manager.
version: 0.1.0
status: draft
---

# Python UV Hygiene

## Purpose
Standardize Python workspace setups, dependency declarations, and local test runners using the ultra-fast `uv` package manager to ensure clean, reproducible runtime environments across all client projects.

## Use When
- Initializing or maintaining a Python project repository.
- Adding, updating, or removing Python library dependencies or virtual environment environments.
- Executing local testing, linting, or CLI help command verifications in a Python project.

## Do Not Use When
- Managing a non-Python repository (e.g. pure Javascript/Node.js, Rust, Go, or raw Markdown/Obsidian repositories).
- Operating in projects that are strictly bound to legacy managers (such as Conda, Poetry, or Pipenv) unless explicitly transitioning them to `uv`.

## Inputs To Check
- Presence of `pyproject.toml` at the project root.
- Presence of a tracked `uv.lock` lockfile.
- Target virtual environment folder (usually `.venv`).

## Procedure
1.  **Synchronize Workspace**:
    *   To prepare a clean checkout or restore dependencies, run:
        ```bash
        uv sync --frozen
        ```
    *   If development or testing helpers are required, add the appropriate extra flags:
        ```bash
        uv sync --extra dev --frozen
        ```
2.  **Add/Modify Dependencies**:
    *   Declare new runtime dependencies in the `project.dependencies` array inside `pyproject.toml`.
    *   Declare development-only tools, test frameworks (e.g. `pytest`), and testing fixtures in the `dependency-groups` or `project.optional-dependencies` (dev extra) sections of `pyproject.toml`.
    *   Regenerate the locked file by running:
        ```bash
        uv lock
        ```
    *   Do not manually edit or corrupt `uv.lock`.
3.  **Run Tests and Validation**:
    *   Always validate environment changes by running the test suite via:
        ```bash
        uv run pytest
        ```
    *   For command-line tools or modules, verify entry points using:
        ```bash
        uv run python -m [module_name] --help
        ```
4.  **Keep Virtual Environment Clean**:
    *   Ensure `.venv/` is fully listed in `.gitignore` to prevent committing virtual environments to version control.
    *   Avoid using global package installation commands (`pip install`) within the local environment boundary.

## Output Format
When executing a sync or dependency modification task, output a brief summary in the following markdown layout:

```markdown
### Python Dependency Update: [Action Performed]

- **Status**: Workspace Synchronized
- **Lockfile**: Updated `uv.lock`
- **Dependencies Modified**:
  - `[package-name]` (Added to `dependencies` / `dev-dependencies`)
- **Validation Run**: `uv run pytest` (Passed: [X] / [Y] tests)
```

## Rules
- **Pyproject is Source of Truth**: The `pyproject.toml` file must always remain the single source of truth for all project configurations and dependencies.
- **Track Lockfile**: The `uv.lock` lockfile must always be committed and tracked in git to ensure deterministic, frozen checkouts across environments.
- **Isolate Extras**: Never add heavy development-only, test-fixture, scraping, or benchmarking dependencies directly to the primary runtime dependencies list. Keep them strictly segregated in development extras.

## Global Skill Change Policy
This is a shared, global skill. Do NOT add repo-specific details or credentials. Any modifications to this skill's behavior must be performed in a dedicated Pull Request within the `agent-skills` repository, requiring a version bump and an entry in `CHANGELOG.md`.
