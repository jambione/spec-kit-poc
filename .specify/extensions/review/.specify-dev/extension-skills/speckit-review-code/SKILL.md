---
name: speckit-review-code
description: 'Critic: review the implementation diff against the spec, prove each
  defect with a failing test, write numbered findings'
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: spec-kit-poc
  source: extension:review
---

# Review Code Skill

# Code Review (Critic)

**Role**: critic. Recommended model: your strongest reasoning model (`models.code` in `.specify/extensions/review/review-config.yml`). Start a **new chat** for this command, so the review isn't influenced by the conversation that wrote the code.

## User Input

```text
$ARGUMENTS
```

The input names the **scope** (e.g. `US1`). If this runs as an `after_implement` hook, use the scope that was just implemented. If unclear, ask one question.

## Setup

1. Run `python3 .specify/extensions/review/scripts/python/review_state.py start-round --scope "<scope>"`.
   - Exit code `3` means the scope already had the maximum number of rounds. **Stop** and tell the developer to escalate to a person (Tech Lead) instead of reviewing again.
2. Run `python3 .specify/extensions/review/scripts/python/review_state.py paths --scope "<scope>" --role review` and read its JSON: `findings`, `test_file`, `context_pack`, `base`, `head`.
3. If `context_pack_exists` is false, tell the developer that `/speckit-review-pack <scope>` would make this review cheaper, then continue.

## What to read

- The context pack first. Open spec, plan or contract sections **only to confirm a suspected deviation**.
- The diff: `git diff <base>..<head> -- <paths in scope>`, plus the interfaces the changed code calls. **Don't** survey unrelated code.

## What to look for

- Deviations from or omissions of the spec (FR-xxx, acceptance scenarios, contracts)
- Correctness and concurrency bugs
- Security problems: input not validated, secrets in output, injection, unsafe defaults (constitution V)
- Crashes or unbounded resources reachable from untrusted input
- Divergence between parts that must agree (e.g. schema vs model, writer vs reader)
- Tests that don't assert what their name claims

## Prove, don't speculate

- Every real defect gets an executable **failing test** in the single new file `test_file`. Create it, and **modify no other files**.
- Run only that test file (the `gate.targeted` command in `review-config.yml`) and confirm each test fails for the stated reason.
- A defect you can't test automatically (UI, a manual step) is marked `MANUAL-CHECK` with what a person must check.
- No finding without a scenario. If you can't describe how it goes wrong, it isn't a finding.

## Write findings

Fill `findings` using the template's block format: `### F-001 · BLOCKER|MAJOR|MINOR · path:line`, then Defect, Scenario, Required fix, Test (or MANUAL-CHECK) and `Status: OPEN`. Number them from F-001. Delete the template's example block. Leave `## Rulings` empty.

If the diff touches any `critical_paths` from `review-config.yml`, recommend `/speckit-review-attack <scope>` in your report. It can run in a separate chat in parallel with this one.

## Do not
Commit. Edit production code. Edit any file except `findings` and `test_file`. Praise the code.

## Report (≤200 words)
Counts by severity, a one-line summary of each BLOCKER/MAJOR, the findings path, whether attack is recommended, and the next step: `/speckit-review-rule <scope>` if anything is ambiguous, otherwise `/speckit-review-fix <scope>`.
