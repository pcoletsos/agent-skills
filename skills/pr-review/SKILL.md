---
name: pr-review
description: Review pull requests or code changes for quality, maintainability, architectural fit, test coverage, security risks, and clarity.
version: 0.1.0
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
3.  **Evaluate Technical Correctness**:
    *   Look for logic errors, edge-case failures, unhandled exceptions, and memory leaks.
    *   Verify lint rules and type safety check success.
4.  **Check Architectural Fit**: Ensure changes respect modular boundaries, do not add circular dependencies, and utilize established library methods rather than writing redundant utilities.
5.  **Check Tests**: Verify that code changes are accompanied by appropriate unit or integration tests. Ensure code coverage is not degraded.
6.  **Verify Security & Privacy Risks**: Check for hardcoded secrets, input sanitization failures, injection vulnerabilities, and context/PII leakages.
7.  **Verify Documentation Impact**: Ensure public API changes, new tools, or environmental variables are documented in the README or respective docs.
8.  **Structure Findings**: Group review findings strictly by severity (Critical, Warning, Minor, Suggestion).

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

## Global Skill Change Policy
This is a shared, global skill. Do NOT add repo-specific details or credentials. Any modifications to this skill's behavior must be performed in a dedicated Pull Request within the `agent-skills` repository, requiring a version bump and an entry in `CHANGELOG.md`.
