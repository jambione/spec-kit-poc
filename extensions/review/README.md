# Spec Kit extension: Review, Attack & Fix

Adds the step Spec Kit is missing: **checking the code after `/speckit-implement`**. A critic
and an adversary have to **prove** each defect with a failing test. The developer rules on
anything ambiguous, and a fixer works through the findings. Findings are committed with the
feature, and CI blocks the PR while serious ones are unresolved.

## The loop (per user story or phase)

```
/speckit-implement US1
      │
      ▼
/speckit-review-pack US1      (optional) ≤150-line context pack: cheaper, more focused reviews
      │
      ▼
/speckit-review-code US1  ‖  /speckit-review-attack US1   (attack only for critical code; run in parallel)
      │   failing tests + findings.md / attack.md
      ▼
/speckit-review-rule US1      (if anything is ambiguous) developer decides; rulings are binding
      │
      ▼
/speckit-review-fix US1       regression test first, then fix; status per finding
      │
      ▼
commit → (round 2 only if the fix broadly touched critical code; max 2, then escalate)

…all scopes done → /speckit-review-audit → review/audit.md + manual-checklist.md → PR (G5)
```

## Commands

| Command | Role | Recommended model | Writes |
|---|---|---|---|
| `/speckit-review-pack <scope>` | Summarizer | fast | `review/context/<scope>.md` |
| `/speckit-review-code <scope>` | Critic | strongest reasoning | `review/<scope>/round-N/findings.md` + one test file |
| `/speckit-review-attack <scope>` | Adversary | strongest reasoning | `review/<scope>/round-N/attack.md` + one test file |
| `/speckit-review-rule <scope>` | Rulings (developer decides) | strongest reasoning | `## Rulings` in findings.md |
| `/speckit-review-fix <scope>` | Fixer | standard coding | code + tests, finding statuses, `fix-report.md` |
| `/speckit-review-audit` | Spec-conformance audit | strongest reasoning | `review/audit.md`, `review/manual-checklist.md` |

All paths are inside the feature folder (`specs/NNN-feature/`). **Hooks**: Spec Kit offers to run
`pack` before `/speckit-implement` and `code` after it. Both are optional prompts.

## Finding format

```markdown
### F-003 · MAJOR · src/StoryVerify.Core/Validation/FileValidator.cs:88
- **Defect**: Absolute URLs inside `select.options` aren't rejected.
- **Scenario**: options: ["https://evil.example/x"] passes validate (FR-003).
- **Required fix**: Apply the URL rule to every string value, including arrays.
- **Test**: `US1_review_r1_Tests.Select_option_with_absolute_url_is_rejected`
- **Status**: OPEN
```

Severity: `BLOCKER` · `MAJOR` · `MINOR`. Status: `OPEN` → `FIXED` | `NOT-FIXED: …` |
`DISPUTED: …` | `WONTFIX` (by ruling) | `DUPLICATE`. **CI fails while any BLOCKER/MAJOR is
OPEN, NOT-FIXED or DISPUTED.**

## Using it with GitHub Copilot

| Practice | Why |
|---|---|
| **A new Copilot Chat (agent mode) per command** | The critic and adversary review the code without the builder's reasoning in their context, and each chat stays small |
| **Pick the recommended model** in Copilot's model picker before each command (`models:` in the config) | Reasoning-heavy roles (review, attack, rulings, audit) benefit from the strongest model; packs and fixes don't need it. Copilot doesn't switch models per command automatically |
| **Run `code` and `attack` in two chats at once** for critical scopes | They write to separate files (`findings.md`, `attack.md`) and separate test files |
| **The developer rules and commits** | Copilot proposes; people decide (AI-DLC). The fixer never commits |
| **Findings are committed** under `specs/<feature>/review/` | Reviewers see them in the PR, and CI enforces them |
| **Reports ≤200 words; files referenced by path** | Keeps every chat short and focused |

## Other AI agents (optional)

Copilot is the default. The commands are plain Markdown prompts with no Copilot-specific
syntax, so Spec Kit registers them for whichever agent integration the repo uses. With an agent
that supports separate sub-agents and a model per agent, each role (pack, code, attack, fix,
audit) can run as its own agent with the model listed under `models:`. See the main README,
"AI agents", for how to switch.

## Install

```bash
specify extension add --dev ./extensions/review
```

Then edit `.specify/extensions/review/review-config.yml`: set the gate commands, the test
folder, the test-file pattern and the critical paths for your stack.

## Helper script

`scripts/python/review_state.py` handles the bookkeeping, so prompts don't have to:
- `start-round`: opens the next round, records the diff base, and enforces the round limit (exit 3)
- `paths`: prints the paths for the latest round and creates the findings file from the template
- `pack-path`: prints where the context pack goes
- `summary`: counts findings
- `check`: the CI gate (exit 1 on unresolved BLOCKER/MAJOR)
