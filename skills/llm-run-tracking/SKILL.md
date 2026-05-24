---
name: llm-run-tracking
description: Conventions for maintaining a structured audit-trail of LLM execution runs, inputs, raw outputs, and downstream action items.
version: 0.1.0
status: draft
---

# LLM Run Tracking

## Purpose
Maintain a transparent, durable, and highly structured audit trail of LLM execution prompts, raw model outputs, summary analysis, and action items for iterative generation and analysis tasks.

## Use When
- Performing iterative text generation, manuscript auditing, code refactoring analysis, or data transformations using LLM prompts.
- Tracking model performance, prompt refinement steps, and prompt efficacy over multiple revisions.
- Storing local evaluation benchmarks or qualitative reviews of model responses.

## Do Not Use When
- Running simple, transient chat operations or one-off exploratory queries that do not alter repository code, content, or processes.
- Executing automated integration test suites where individual run logging is handled by a standard testing framework.

## Inputs To Check
- The specific target entity or draft version being analyzed (e.g. `draft-v1`, `module-v2`).
- The project analysis workspace or reserved folder (e.g., `analysis/` or `docs/analysis/`).
- The central model runs index log file (e.g., `model-runs-log.md`).

## Procedure
1.  **Identify Target Version**:
    Determine the unique name and version of the target document, draft, or code component being run (e.g., `draft-v1`).
2.  **Create Per-Run Workspace**:
    Create a dedicated directory under the designated analysis folder following this structure:
    `runs/<target-entity>-vN/` (e.g. `runs/draft-v1/`).
3.  **Compile Run Metadata (`00-run-meta.md`)**:
    Record vital execution details:
    *   Execution date and timestamp.
    *   Model name and parameter settings (e.g., temperature, top-p).
    *   Prompt version or file reference.
    *   Status of the run (e.g., success, incomplete, error).
4.  **Preserve Input Prompt (`01-input.md`)**:
    Paste the complete, unmodified prompt text, context payload, and instruction blocks exactly as sent to the LLM.
5.  **Store Raw Output (`02-output-raw.md`)**:
    Paste the complete, unmodified model output. Do NOT format, edit, or clean up the response.
6.  **Synthesize Takeaways (`03-summary.md`)**:
    Document key findings, quality evaluations, pattern observations, or gaps identified by the model.
7.  **Map Next Actions (`04-actions.md`)**:
    Draft concrete downstream tasks, editing checklists, or follow-up questions resulting from the run.
8.  **Register Run in Central Log (`model-runs-log.md`)**:
    Add an entry to the central runs log register, referencing the run folder path, model used, and a high-level outcome summary.

## Output Format
Each run directory must contain precisely five files structured as follows:

### 1. `00-run-meta.md`
```markdown
# Run Metadata - [Target Entity vN]

- **Date**: [YYYY-MM-DD HH:MM]
- **Model**: [e.g. Gemini 3.5 Flash]
- **Parameters**: [e.g. Temperature 0.2]
- **Status**: [Completed | Failed]
```

### 2. `01-input.md`
```markdown
# Raw Input Prompt

[Exact raw text of the input prompt and source context payload]
```

### 3. `02-output-raw.md`
```markdown
# Raw Model Output

[Exact raw, unedited text of the model response]
```

### 4. `03-summary.md`
```markdown
# Analysis Summary

- **Core Takeaways**: [Key findings or quality observations]
- **Identified Gaps**: [Shortcomings or missed items]
```

### 5. `04-actions.md`
```markdown
# Downstream Actions

- [ ] [Specific item to fix or refactor]
- [ ] [Follow-up question or clarification]
```

## Rules
- **No Editing of Raw Output**: The `02-output-raw.md` file must strictly preserve the raw model response. Never modify, censor, or reformat the output in this file to maintain audit integrity.
- **Privacy Gates**: Review and redact any sensitive personal identifiers, credentials, API tokens, or proprietary data from both the input and raw output files before committing them.
- **Durable File Prefixing**: Files within the run directory must adhere strictly to the `00-`, `01-`, `02-`, `03-`, and `04-` numbering schema to enforce standard sequencing.

## Global Skill Change Policy
This is a shared, global skill. Do NOT add repo-specific details or credentials. Any modifications to this skill's behavior must be performed in a dedicated Pull Request within the `agent-skills` repository, requiring a version bump and an entry in `CHANGELOG.md`.
