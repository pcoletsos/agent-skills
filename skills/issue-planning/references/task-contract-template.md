# Execution-Ready Task Contract

Use this template for detailed issues that must survive a handoff between people, sessions, or agents. Remove optional prompts that do not apply.

```markdown
## Requester / decision owner

- Requester: <person, team, or parent issue>
- Decision owner: <who can resolve scope and acceptance decisions>

## Desired outcome

<State the concrete result. Say whether the task ends at review-ready, approved, deployed, or another explicit state.>

## Authoritative sources

- <source and why it is authoritative>
- <source>

Source rules:

- Do not invent <facts, content, interfaces, or decisions>.
- If <sources> conflict, <named source> wins / stop and ask the decision owner.

## Scope and boundaries

In scope:

- <bounded work>

Out of scope:

- <excluded work>

Ask first:

- <external, destructive, irreversible, security-sensitive, publication, deployment, billing, credential, or customer-facing action>

## Dependencies and delivery

- Parent or source issue: <issue or none>
- Depends on: <issues, decisions, or none>
- Milestone: <active milestone or backlog equivalent>
- Branch: <repository-defined branch or `<id>` placeholder>
- Expected artifact: <comment, document, commit, pull request, deployment, or decision>

## Acceptance criteria

- [ ] <observable outcome>
- [ ] <observable outcome>

## Validation

- <command, test, inspection, or evidence>
- <command, test, inspection, or evidence>

## If blocked

- Ask one focused question on this task record.
- Explain why the answer is required.
- Record the last safe state and any changes already made.
- Stop actions whose validity depends on the answer.
- Resume this same task when: <objective condition>.

## Output handoff / receipts

- Artifact location: <path, issue, pull request, or URL>
- Evidence required: <diff, checks, screenshots, logs, decision record, or summary>
- Next reviewer or owner: <person, team, or agent>
- Completion state: <review-ready or fully complete>
```

## Planning Review Checklist

- [ ] Existing tracker items and milestone state were checked.
- [ ] The decision owner is named.
- [ ] Sources are authoritative and conflict behavior is explicit.
- [ ] Acceptance criteria describe outcomes; validation describes proof.
- [ ] Boundaries identify ask-first actions without granting new authority.
- [ ] The blocker rule contains one question path and a resume condition.
- [ ] Dependencies, branch, artifact location, and next owner are explicit.
- [ ] Review-ready work is not mislabeled as fully complete.
