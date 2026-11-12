# AI-Driven Development Lifecycle (AI-DLC)

> **Status:** POC draft v0.1. This is a vendor-neutral lifecycle proposed for the team. If the
> company adopts its own lifecycle, rename the phases and gates below; the tooling mapping stays
> the same.

## 1. What this is, in one paragraph

AI-DLC is our normal delivery lifecycle (requirements → design → build → test → release),
rearranged so that **AI drafts and humans decide**. GitHub Copilot produces the first version of
every artifact (spec, plan, tasks, code). People review, correct and approve that version at a
fixed set of **gates**, and every approval is recorded in Git. **GitHub Spec Kit** is the tool
that turns each step into a repeatable Copilot command with a standard output file.

## 2. Phases at a glance

```
 ┌──────────────── INCEPTION ────────────────┐ ┌──────────── CONSTRUCTION ────────────┐ ┌─ OPERATIONS ─┐
 Intent ─► Specify ─► Clarify ─► [G2 Spec]  ─► Plan ─► [G3] ─► Tasks ─► Analyze ─► [G4] ─► Implement ─► [G5 PR] ─► [G6 Release]
  [G1]     (AI)       (AI+team)   approve       (AI)    approve  (AI)     (AI)    approve    (AI+dev)    review     deploy
```

| Phase | Purpose | Spec Kit command(s) | Output (in `specs/<NNN-feature>/`) | Gate |
|---|---|---|---|---|
| **0. Foundation** (once per project) | Agree on the rules | `/speckit-constitution` | `.specify/memory/constitution.md` | Tech Lead approves |
| **1. Inception: Intent** | Why are we doing this, and for which app and environment? | (none: people write the brief and fill in `docs/poc/PROJECT-CONTEXT.md`; check with `scripts/check-context.sh`) | Feature brief / GitHub issue + project context | **G1** PO + TL |
| **1. Inception: Specify** | What should it do? (no tech) | `/speckit-specify <brief>` | `spec.md` | |
| **1. Inception: Clarify** | Remove ambiguity | `/speckit-clarify` (optional), `/speckit-checklist` (optional) | `spec.md` (Clarifications section), `checklists/*.md` | **G2** PO + Tech Lead |
| **2. Construction: Design** | How will we build it? | `/speckit-plan <tech direction>` | `plan.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md` | **G3** Architect / TL |
| **2. Construction: Break down** | What are the steps? | `/speckit-tasks`, then `/speckit-analyze` | `tasks.md`, analyze report | **G4** TL |
| **2. Construction: Build** | Write tests, then code | `/speckit-implement` (then `/speckit-converge` if gaps remain) | Source + tests, tasks checked off | **G5** PR review |
| **3. Operations** | Ship and run | (not covered by Spec Kit: CI/CD pipeline) | Build, deployment, monitoring | **G6** Release owner |

## 3. Roles

| Role | In this lifecycle they… |
|---|---|
| **Product Owner (PO)** | Writes the intent, answers clarification questions, approves G1 and G2 |
| **Tech Lead / Architect** | Owns the constitution, approves G2 (feasibility), G3 and G4 |
| **Developer** | Drives Copilot through the commands, reviews and edits AI output, owns the PR |
| **QA** | Checks that acceptance scenarios are testable at G2 and reviews test coverage at G5 |
| **Reviewer** | A second developer (not the author) who approves G5 |
| **GitHub Copilot (agent mode)** | Drafts every artifact. Approves nothing. |

## 4. How gates work in practice

Each gate is a **pull request** (or a PR review checkpoint) on the feature branch:

1. `/speckit-specify` creates the branch `NNN-feature-name` and `spec.md`.
2. **Spec PR (G2):** open a *draft* PR with only `specs/NNN-*/spec.md`. The PO and TL review it
   in GitHub. Comments become edits (by hand or by re-running Copilot). Approval = G2.
3. **Plan + Tasks (G3/G4):** push `plan.md` and `tasks.md` to the same PR and request the TL's
   review. You can combine G3 and G4 into one review for small features.
4. **Code (G5):** Copilot implements, the developer reviews locally, pushes, CI runs, and a
   reviewer approves.
5. **Release (G6):** merge to `main`, then the normal pipeline deploys.

The **PR template** (`.github/pull_request_template.md`) has a checkbox per gate, and the
**`ai-dlc-gates` CI workflow** blocks merges where code changes have no spec, plan and tasks.

### The developer's last step: a verification recording

The POC project ([feature brief](../demo/feature-brief.md)) builds the tool that closes this
lifecycle. Once it exists, the gates change like this:

| Gate | Today | With Story Verification Recordings |
|---|---|---|
| **G5 Code** | Reviewer reads code and tests | The PR also contains a JSON verification file, recorded by the developer, showing what they expect to happen. The reviewer reads it alongside the code. |
| **G6 Release** | Pipeline green, manual sign-off | The pipeline replays the verification file with Playwright against the environment that has the change. A failed step blocks the release. |

This applies to both user stories and defects: a defect's verification file is its regression
proof.

## 5. Paths by change size

| Change type | Path |
|---|---|
| New feature / significant change | Full lifecycle (G1–G6) |
| Small enhancement (< 1 day) | Specify → Plan → Tasks in one PR, a single combined G2–G4 review |
| Bug fix | Issue → fix + regression test (+ verification file, once the tool exists) → G5 (no spec needed; link the issue) |
| Spike / research | No gates. Results go into `research.md` of the related feature |

## 6. Working agreements for AI use

- **Review everything.** Read every AI-generated line before approving; you are the author of
  record.
- **Edit the spec, not the code,** when behaviour is wrong because a requirement was wrong. Then
  regenerate the downstream artifacts.
- **No secrets or customer data in prompts.** Use synthetic examples.
- **Keep prompts in the record.** Paste the exact `/speckit-*` arguments you used into the PR
  description ("Prompt log" section).
- **Stop when stuck.** If Copilot loops or drifts, clarify the spec or plan rather than re-prompting the code.

## 7. Metrics collected during the POC

See [`docs/poc/POC-PLAN.md`](../poc/POC-PLAN.md#success-criteria--metrics).
