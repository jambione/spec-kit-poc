---
name: speckit-review-fix
description: 'Fixer: work through the findings, regression test first for BLOCKER/MAJOR,
  obey rulings, update each finding''s status'
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: spec-kit-poc
  source: extension:review
---

# Review Fix Skill

# Fix

**Role**: worker. Recommended model: a standard coding model (`models.fix`). Start a **new chat**.

## User Input

```text
$ARGUMENTS
```

The input names the **scope**.

## Setup

Run `python3 .specify/extensions/review/scripts/python/review_state.py paths --scope "<scope>" --role review`. The work list is `findings`, plus `attack.md` in the same `round_dir` if it exists. Read the `context_pack` first.

## Rules

- **Rulings are binding.** The `## Rulings` section overrides your own judgment and the original finding.
- Skip findings marked `DUPLICATE` or `WONTFIX`.
- **BLOCKER/MAJOR**: make sure a failing test exists (the reviewer's, or write a regression test). Confirm it fails, then fix the code, then confirm it passes.
- **MINOR**: fix directly. Add a test only if it's cheap.
- **Never delete or weaken** a reviewer's or adversary's test, unless a ruling explicitly says so.
- If the spec itself looks wrong, append a proposed change to `round_dir/spec-changes.md`. Don't silently diverge from the spec.
- Read only the files named in the findings and their direct dependencies.
- While iterating, run targeted tests (`gate.targeted`). At the end, run the full gate (`gate.command`) once. If `gate.flaky_runs` > 0, run the affected tests that many times.

## Update each finding's status

In `findings` / `attack.md`, set every finding's `Status` to one of:
- `FIXED`, followed by the commit-ready description of the change
- `NOT-FIXED: <reason>`, which needs the developer's attention
- `DISPUTED: <file:line evidence>`, if you believe the finding is wrong. The developer must rule on it.

Write a short `fix-report.md` in `round_dir`: one line per finding ID, the final gate result, and any public API changes.

## Do not
Commit (the developer commits after checking the gate). Edit files outside the findings' scope.

## Report (≤200 words)
- one line per finding ID with its status
- the gate result
- public API changes
- the next step: commit; then, if the fix touched critical code broadly, run `/speckit-review-code <scope>` for round 2 (max 2 rounds). Otherwise the scope is done.
