---
name: speckit-review-rule
description: Merge duplicate findings and record the developer's binding rulings on
  anything ambiguous
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: spec-kit-poc
  source: extension:review
---

# Review Rule Skill

# Rulings

**Role**: the decision step. AI proposes, **the developer decides** (AI-DLC: humans approve). Recommended model: your strongest reasoning model (`models.rule`).

## User Input

```text
$ARGUMENTS
```

The input names the **scope**.

## Steps

1. Run `python3 .specify/extensions/review/scripts/python/review_state.py paths --scope "<scope>" --role review`, and read `findings` plus `attack.md` in the same `round_dir` if it exists.
2. **Merge duplicates.** The critic and adversary often find the same defect. Keep one finding, set the other's status to `DUPLICATE` and add a line: `Duplicate of F-00x`.
3. **Find what needs a ruling**:
   - a test that contradicts the spec, or a spec that looks wrong
   - strict vs lenient behaviour (parsing, validation, limits) that the spec doesn't settle
   - a severity that looks too high or too low
   - a finding that would require changing a public contract
   - anything the fixer could reasonably resolve in two different ways
4. **Ask the developer.** Present each item as one short question with your recommendation first, labelled "(Recommended)". Ask up to 4 at a time. Don't decide on their behalf.
5. Append the confirmed rulings under `## Rulings` in the critic's `findings` file:
   `- **R-1** (F-003, A-002): <ruling>. <one-line rationale>.`
   For a finding ruled out of scope, set its status to `WONTFIX` and cite the ruling.
6. If a ruling changes the spec, also append a proposed spec change to `round_dir/spec-changes.md`. The spec itself is changed only through the normal spec PR (gate G2).

## Report (≤150 words)
Duplicates merged, rulings recorded (one line each), findings left for the fixer, and the next step: `/speckit-review-fix <scope>`.
