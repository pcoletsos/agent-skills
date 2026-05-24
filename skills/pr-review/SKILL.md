---
name: pr-review
description: Review pull requests or code changes for quality, maintainability, architectural fit, test coverage, security risks, and clarity.
version: 0.2.0
status: draft
---

# Pull Request Review Skill

## Purpose
Examine a set of code changes (diffs, staged modifications, or active PR files) to evaluate correctness, alignment with project architectures, code quality, test presence, security risks, and documentation completeness.

## Use When
- Asked to "Review this PR," "Check my changes," or "Analyze this git diff."
- Running pre-commit validation to ensure your own changes are pristine before proposing.
- Auditing third-party contributions to a codebase.

## Do Not Use When
- The changes are non-code documentation edits (e.g. only markdown `.md` files changed).
- Reviewing architectural decisions before code is actually written (use `architecture-review` instead).

## Inputs To Check
- Staged git diff: `git diff --staged` or specific PR files.
- Configuration files: `.eslintrc`, `tsconfig.json`, `linter configurations`.
- Core test outcomes: local test suites and code coverage figures.

## Procedure
1.  **Understand Intent**: Read the PR description, the linked issue, and the branch context to identify what problem this change is attempting to solve.
2.  **Inspect Changed Files**: Track changed files. Group them into core logic, configuration changes, test additions, and documentation.
3.  **Agent Git Hygiene Checks**: Validate that the PR branch name strictly matches the format `<actor>/<type>/<scope>/<task>-<id>` and that the PR title adheres to the Conventional Commits specification.
4.  **Evaluate Technical Correctness**:
    *   Look for logic errors, edge-case failures, unhandled exceptions, and memory leaks.
    *   Verify lint rules and type safety check success.
5.  **Check Architectural Fit**: Ensure changes respect modular boundaries, do not add circular dependencies, and utilize established library methods rather than writing redundant utilities.
6.  **Check Tests**: Verify that code changes are accompanied by appropriate unit or integration tests. Ensure code coverage is not degraded.
7.  **Verify Security & Privacy Risks (Strict Privacy Gate)**: Scan PR diffs for sensitive data leaks (e.g. hardcoded secrets, local cookie caches, database dumps, child names/faces, API keys, or private URLs).
8.  **Unedited Raw Output Verification**: If the PR contains any LLM run tracking directories (e.g. `runs/draft-vN/`), verify that the raw output files (`02-output-raw.md`) remain 100% unmodified and authentic.
9.  **Verify Documentation Impact**: Ensure public API changes, new tools, or environmental variables are documented in the README or respective docs.
10. **Structure Findings**: Group review findings strictly by severity (Critical, Warning, Minor, Suggestion).

## Output Format
Render a clean Markdown PR review report:
```markdown
# Pull Request Review Report

## 🔍 Context & Summary
- **PR Purpose**: ...
- **Total Files Impacted**: ...

## 📊 Evaluation Summary
- **Correctness**: Pass/Fail
- **Test Coverage**: Satisfactory/Deficient
- **Security Check**: Clean/Vulnerabilities Found

## 🛠 Detailed Findings

### 🔴 Critical Issues
- **[filename:L12-15]**: Detailed reason why this breaks the system or has high risk.

### 🟡 Warnings
- **[filename:L80]**: Outlining minor bugs, bad styling, or deprecation risks.

### 🟢 Suggestions & Architectural Notes
- **[filename]**: Refactoring suggestions or minor performance tips.
```

## Rules
- **Do NOT spend time on formatting nitpicks** (e.g. spaces vs tabs, variable names) if a code linter is already active in the repo. Rely on the automated linter.
- Be concise. Focus on clear, high-signal technical explanations over polite wordiness.
- **Privacy Gate Halting**: If any credential, API token, session cookie, private URL, or children's PII is discovered inside a PR diff, you must immediately set the PR review outcome to **FAIL**, flag the location, and instruct the author to redact it before continuing.
- **Audit Integrity Protection**: Any edits to files tracking raw LLM generation outputs (`02-output-raw.md`) must be rejected outright as a critical structural violation to keep the audit trail pristine.
- **Hygiene Compliance**: Fail or block merging for any pull request whose branch name or commit format violates the actor feature-branching or Conventional Commits layout.

## Global Skill Change Policy
This is a shared, global skill. Do NOT add repo-specific details or credentials. Any modifications to this skill's behavior must be performed in a dedicated Pull Request within the `agent-skills` repository, requiring a version bump and an entry in `CHANGELOG.md`.
