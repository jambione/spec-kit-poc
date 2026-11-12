---
description: "Final audit: check the whole repo against the spec and write the manual-check list"
---

# Final Audit

**Role**: spec-conformance reviewer. Recommended model: your strongest reasoning model (`models.audit`). Run it once, after all scopes are implemented and fixed, before the PR goes to gate G5.

## User Input

```text
$ARGUMENTS
```

## Steps

1. Get `FEATURE_DIR` from `python3 .specify/scripts/python/check_prerequisites.py --json --paths-only`.
2. Run `python3 .specify/extensions/review/scripts/python/review_state.py summary`. If `unresolved_blocking` isn't empty, list it and stop: those must be fixed or ruled first.
3. Check **spec conformance only**. For each functional requirement (FR-xxx), success criterion (SC-xxx) and acceptance scenario in `spec.md`, find the code **and** the test that cover it. Use the coverage table in `tasks.md` as the map; open code only to confirm.
4. Run the full gate (`gate.command` in `review-config.yml`) once.
5. Write `FEATURE_DIR/review/audit.md` with a table, `Requirement | Status (MET / PARTIAL / MISSING / MANUAL) | Evidence (test name or file:line) | Note`, followed by the gate result.
6. Write `FEATURE_DIR/review/manual-checklist.md` from every `MANUAL-CHECK` in the findings, plus every requirement marked MANUAL. Each item is a checkbox a person can tick.
7. If anything is PARTIAL or MISSING, suggest `/speckit-converge` to add tasks for it.

## Do not
Change code or tests. Review style. Invent requirements.

## Report (≤150 words)
Counts of MET / PARTIAL / MISSING / MANUAL, the gate result, the two file paths, and whether the feature is ready for gate G5.
