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
- [ ] **G5 Verification file:** recorded and included under `verifications/` *(applies once the tool from feature 001 exists)*

## Constitution check (reviewer)
- [ ] Tests written first and cover the acceptance scenarios (III)
- [ ] Core rules kept out of the CLI layer; no unjustified patterns or libraries (IV)
- [ ] Verification files validated before running; no secrets or personal data in files or logs (V)
- [ ] Per-step results, failure evidence, correct exit code (VI)
- [ ] Verification file format changes are schema-versioned (VIII)

## Prompt log
<!-- Paste the exact /speckit-* commands and arguments you used, in order. -->
```
/speckit-specify ...
/speckit-plan ...
```

## AI usage notes
<!-- Where did you override or rewrite Copilot output, and why? (Feeds the POC metrics.) -->
