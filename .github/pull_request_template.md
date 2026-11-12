## Summary
<!-- What does this PR do? One or two sentences. -->

**Feature folder:** `specs/NNN-feature-name/`
**Change path:** <!-- Full lifecycle | Small enhancement | Bug fix (link issue) -->

## AI-DLC gates
<!-- Tick a gate only once the named approver has approved it in this PR (or a linked one). -->
- [ ] **G1 Intent:** feature brief / issue linked: <!-- #issue or link -->
- [ ] **G2 Spec:** `spec.md` approved by PO + Tech Lead; no `[NEEDS CLARIFICATION]` left
- [ ] **G3 Plan:** `plan.md` Constitution Check passes; approved by Tech Lead / Architect
- [ ] **G4 Tasks:** `tasks.md` covers every FR; `/speckit-analyze` has no CRITICAL findings
- [ ] **G5 Code:** CI green; each FR has at least one test; reviewed by someone other than the author

## Constitution check (reviewer)
- [ ] Tests written first and cover the acceptance scenarios (III)
- [ ] Domain rules kept out of endpoints; no unjustified patterns or libraries (IV)
- [ ] Input validated, ProblemDetails errors, no secrets or personal data in logs (V)
- [ ] Structured logging, `/health` endpoint (VI)

## Prompt log
<!-- Paste the exact /speckit-* commands and arguments you used, in order. -->
```
/speckit-specify ...
/speckit-plan ...
```

## AI usage notes
<!-- Where did you override or rewrite Copilot output, and why? (Feeds the POC metrics.) -->
