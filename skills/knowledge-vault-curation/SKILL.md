---
name: knowledge-vault-curation
description: Guidelines and workflows for Obsidian-first and Markdown-first personal knowledge management (PKM) vault curation.
version: 0.1.0
status: draft
---

# Knowledge Vault Curation

## Purpose
Enforce consistency, high usability, and bidirectional link health in an Obsidian-first or Markdown-first personal knowledge vault by standardizing note structure, naming conventions, and file routing.

## Use When
- Organizing study notes, certification trackers, program indices, glossaries, or bookmarks in a Markdown vault.
- Performing data ingestion, importing local documents, or restructuring existing Markdown directories.
- Maintaining bidirectional links or Map of Content (MOC) indexes in a personal knowledge management (PKM) vault.

## Do Not Use When
- Managing a complex software codebase where the primary assets are source code files rather than Markdown documentation.
- Working with flat single-document project wikis that do not support Obsidian-style directory hierarchies or bidirectional links.

## Inputs To Check
- Existing vault folder structure at the vault/repository root.
- Existing Map of Content (MOC) indexes under an `_indexes/` folder.
- Reusable page templates under a `templates/` folder.

## Procedure
1.  **Deduplicate Before Creation**:
    *   Perform a search (using file listing or text search) on the target folder and index files for similar titles or concepts.
    *   If a canonical note already exists, update and extend that note instead of creating a duplicate file.
2.  **Determine Primary Classification & Directory**:
    *   Route content to its canonical folder based on entity type:
        *   `certifications/`: Professional certifications and credential requirements.
        *   `exams/`: Official exam pages, skill measures, schedules, and renewal references.
        *   `programs/`: Multi-course learning paths, professional certificates, or specializations.
        *   `courses/`: Single courses, tutorials, or standalone classes.
        *   `modules/`: Granular modules or course units.
        *   `resources/`: Supporting references, links collections, glossaries, and shared guides.
        *   `credentials/`: Local archived files (PDFs, images) proving badges or completions.
        *   `inbox/`: Temporary intake, raw links, or unresolved items.
        *   `_indexes/`: Main indices and section navigation (Maps of Content).
3.  **Apply Naming Rules**:
    *   Ensure the filename is completely lowercase and uses hyphen-separated words (e.g. `aws-solutions-architect.md` or `learning-path-python.md`).
    *   Prefer official codes (e.g., `az-900.md`, `saa-c03.md`) when known.
    *   Do not include dates in durable filenames; reserve date prefixes (e.g., `2026-05-24-link-capture.md`) strictly for temporary inbox files.
4.  **Format Note Structure**:
    *   Create new files from closest templates or structure using standard Markdown note headings (defined in **Output Format**).
    *   Ensure a comprehensive **Source** block is added or preserved to track source metadata.
5.  **Establish Bidirectional Links**:
    *   Use relative Markdown links (e.g., `[AWS Program](../programs/aws-learning.md)`) to connect related entities.
    *   Add reciprocal links to the connected certifications, exams, programs, or courses to ensure smooth browsing.
6.  **Update Indexes**:
    *   Update the corresponding index page in `_indexes/` immediately upon adding a new durable note to keep navigation paths fresh.

## Output Format
Durable notes must be written in GitHub Flavored Markdown and conform to the following preferred structural layout:

```markdown
# [Note Title]

## Source
- **Title**: [Original Source Title]
- **URL**: [Direct URL if applicable]
- **Repository**: [Source Repository name if imported locally]
- **Provider**: [e.g. Microsoft Learn, Coursera, AWS]
- **Content Type**: [e.g. Course, Certification, Reference Document]
- **Date Captured**: [YYYY-MM-DD]
- **Last Reviewed**: [YYYY-MM-DD]

## Summary
Provide a concise, 2-3 sentence overview of the note's purpose, key takeaways, and why it is valuable to a future reader.

## Notes
- Detailed, practical takeaways.
- Focus on bulleted lists, short paragraphs, and direct language.
- Avoid copying large blocks of raw source text.

## Related
- [Certification Track](file:///absolute/path/to/cert.md)
- [Exam Guide](file:///absolute/path/to/exam.md)
```

## Rules
- **No Wiki Links**: Prefer standard relative Markdown links (`[Link Text](../path/file.md)`) to maximize cross-platform compatibility and HTML portability.
- **Maintain Shallow Directories**: Avoid nesting folders deeper than two levels beneath the vault root. Route ambiguous or multi-topic items to `resources/` or `inbox/`.
- **Source Integrity**: Every durable note must preserve the source URL, provider, platform, and capture date in its `## Source` block. Never delete this block when updating a note.

## Global Skill Change Policy
This is a shared, global skill. Do NOT add repo-specific details or credentials. Any modifications to this skill's behavior must be performed in a dedicated Pull Request within the `agent-skills` repository, requiring a version bump and an entry in `CHANGELOG.md`.
