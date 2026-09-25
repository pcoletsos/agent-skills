---
name: prose-style-guide
description: Enforce human-authentic, anti-AI writing standards for agent response text, articles, drafts, notes, and communications. Strictly prohibits em dashes and AI cliches.
version: 0.1.0
status: draft
---

# Prose Style Guide (Anti-AI & Human-Authentic Writing)

## Purpose

Enforce human-authentic, anti-AI writing standards across all agent-generated response text, articles, blog posts, documentation, notes, and professional communications. The primary directive is eliminating artificial, bot-like writing habits, with a strict and non-negotiable prohibition on em dashes.

## Use When

- Drafting or proposing response text to users, colleagues, recruiters, or clients.
- Authoring articles, essays, briefs, Substack drafts, or LinkedIn posts.
- Writing or refactoring documentation, READMEs, knowledge vault notes, or guides.
- Summarizing technical findings, architecture decisions, or meeting notes.

## Do Not Use When

- Writing pure executable code, configuration files, raw JSON, or shell scripts where punctuation has strict syntactic meaning.
- Handling raw external text imports or quoted third-party citations where the original source text must be preserved verbatim.

## Inputs To Check

- Topic brief, user request, or context notes.
- Target publication or communication channel (e.g. Substack, LinkedIn, technical vault note, direct message).
- Target audience profile (e.g. senior practitioners, engineering leadership, recruiter).

## Procedure

1. **Lead with Direct Value**:
   - State the core thesis or answer in the opening sentence.
   - Cut preamble, throat-clearing pleasantries, and meta-commentary (e.g. avoid "Certainly! I'd be happy to explain...").

2. **Strictly Enforce the Em Dash Prohibition**:
   - **Never** output em dashes (`—` or `--` used in place of an em dash).
   - Scan all generated text before presenting it. If an em dash is found, replace it using one of four natural alternatives:
     - **Commas**: for lightweight parenthetical pauses.
     - **Parentheses**: for secondary context, clarifying details, or examples.
     - **Colons**: for introductions, explanations, or lists.
     - **Separate Sentences**: break the thought into two distinct, punchy sentences (often the strongest choice).

3. **Strip Bot Cliches and Buzzwords**:
   - Avoid performative filler and generic corporate verbs (e.g. "delve", "testament", "tapestry", "beacon", "game-changer", "harness", "supercharge", "paramount").
   - Eliminate sycophantic praise or ungrounded superlative adjectives.

4. **Vary Sentence Rhythm Naturally**:
   - Mix short, declarative statements with structured compound sentences.
   - Use plain, precise nouns and active verbs.

5. **Self-Audit Before Delivery**:
   - Check: Are there any em dashes (`—` or `--`) anywhere in the output? If yes, eliminate them.
   - Check: Does this sound like an experienced human practitioner talking directly to a peer?
   - Check: Is every paragraph carrying unique, concrete information rather than padding?

## Output Format

All generated prose must be formatted cleanly in standard Markdown without stylistic ornamentation:

```markdown
### [Direct Heading]

[Direct thesis or opening answer without conversational filler.]

- [Point 1]: [Concrete explanation using commas, parentheses, or colons.]
- [Point 2]: [Short, punchy sentences without em dashes.]

[Actionable takeaway or concluding thought.]
```

## Rules

- **Absolute Prohibition on Em Dashes**: Em dashes are treated as an immediate signature of unreviewed AI generation. They are completely banned.
- **Natural Punctuation Only**: Rely on standard commas, periods, colons, semicolons, and parentheses.
- **Show Tradeoffs**: Ground assertions in technical tradeoffs, edge cases, and real constraints rather than sweeping generalizations.
- **No Sycophancy**: Do not flatter the reader or use empty conversational fillers.

## Global Skill Change Policy

This is a shared, global skill. Do NOT add repo-specific details or credentials. Any modifications to this skill's behavior must be performed in a dedicated Pull Request within the `agent-skills` repository, requiring a version bump and an entry in `CHANGELOG.md`.
