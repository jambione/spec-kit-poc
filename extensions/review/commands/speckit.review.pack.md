---
description: "Write a ≤150-line context pack for one scope (user story or phase) before implementing or reviewing it"
---

# Context Pack

**Role**: mechanical summarizer. Recommended model: a fast, low-cost model (see `models.pack` in `.specify/extensions/review/review-config.yml`).

## User Input

```text
$ARGUMENTS
```

The input names the **scope**: a user story (`US1`), a phase (`Phase 3`) or a task range (`T019-T031`). If it is empty and this runs as a `before_implement` hook, use the scope the developer asked `/speckit-implement` to build. If there's still no scope, ask for one in a single question.

## Steps

1. Run `python3 .specify/extensions/review/scripts/python/review_state.py pack-path --scope "<scope>"` and read its JSON (`context_pack`, `template`, `max_lines`, `feature_dir`). If `exists` is true, say so and stop, unless the developer asked to refresh it.
2. From `feature_dir`, read **only the sections** of `tasks.md`, `spec.md`, `plan.md`, `data-model.md` and `contracts/` that this scope needs. Also read `.specify/memory/constitution.md` principle headings and any `## Rulings` in earlier `review/**/findings.md` files that touch the same files.
3. Fill the template into `context_pack`, staying within `max_lines` lines:
   - Quote contracts, field names, constants, error codes and requirement lines **verbatim**. Never paraphrase a normative rule.
   - List exact file paths and the public signatures the scope calls into, not implementations.
   - Add the targeted test command and the full gate command from `review-config.yml`.
   - Under **Sources**, list `document#section` for everything summarized.
4. Invent nothing. If something the scope needs is missing from the documents, list it under Sources as `MISSING:`.

## Report (≤100 words)
The pack path, its line count, and any `MISSING:` items. Tell the developer that every later command for this scope reads the pack first.
