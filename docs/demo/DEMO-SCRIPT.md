# Demo Script: AI-DLC with Spec Kit + GitHub Copilot

**Length:** about 55 min live (or 25 min with the build and review steps shown from the dry run)
**Audience:** engineering team and leads
**Feature:** [Story Verification Recordings](feature-brief.md), a .NET 8 + Playwright tool

> **Reference:** [`docs/reference-example/`](../reference-example/README.md) shows what good
> output looks like for each step. Use it to judge Copilot's output at each gate, or walk
> through it if the live run goes wrong.

> **Tip:** Do a full dry run the day before on a branch named `dry-run/*`, **including one review
> round for US1** (step 6). Keep that branch as a **fallback**: if Copilot is slow or goes off
> track live, switch to it and walk through the artifacts that are already there.

---

## 0. Prerequisites (set up before the demo)

| Need | Check |
|---|---|
| VS Code with the GitHub Copilot + Copilot Chat extensions, signed in | Copilot Chat opens; **Agent** mode is available |
| .NET 8 SDK | `dotnet --version` → 8.x |
| Python 3.11+ (runs the Spec Kit helper scripts) | `python --version` |
| Spec Kit CLI (optional; the repo is already initialized) | `uv tool install specify-cli` → `specify --version` (POC pinned at 1.4.0) |
| Git + push access to this repo | `git push` works |
| Review, Attack & Fix extension (already installed in this repo) | Typing `/speckit-review` in Copilot Chat lists 6 commands |
| Review gate commands set for your stack | `.specify/extensions/review/review-config.yml` → `gate.command` and `gate.targeted` run on your machine |

Open the repo in VS Code and open **Copilot Chat → Agent mode**. Typing `/speckit` should list
the Spec Kit skills (they come from `.github/skills/`).

---

## 1. Set the scene (3 min)

Show [`docs/ai-dlc/AI-DLC.md`](../ai-dlc/AI-DLC.md) section 2 (the phase diagram).
> "AI drafts, humans decide. Every arrow is a Copilot command; every [G] is a person approving
> in a PR."

## 2. Foundation: the constitution (4 min)

Open `.specify/memory/constitution.md`.
> "These are our engineering rules: .NET 8, Playwright, test-first, security, logging. Copilot checks every
> plan against them. We wrote them once, using `/speckit-constitution`."

(Optional live amendment, if time allows:)
```
/speckit-constitution Add a principle: every verification file must declare a schemaVersion.
```

## 3. Inception: intent to spec (8 min)

**G1.** Show [`feature-brief.md`](feature-brief.md): "This is what a PO hands us."

**Context.** Show [`PROJECT-CONTEXT.md`](../poc/PROJECT-CONTEXT.md) filled in for your
application and environment, and run the readiness check:
```bash
bash scripts/check-context.sh
```

**Specify.** In Copilot Chat:
```
/speckit-specify Build Story Verification Recordings as described in docs/demo/feature-brief.md, for the target application, environment and JSON format requirements in docs/poc/PROJECT-CONTEXT.md. When a developer finishes a user story or defect fix, they record what they expect to happen with the Playwright recorder, marking expected outcomes with its assertion tools. The recording becomes a readable JSON verification file linked to the story or defect ID and stored with the code change so it is reviewed in the same pull request. An automated runner replays the file against the environment that has the developer's code and checks every expected outcome, reporting pass/fail per step with evidence (expected vs found, screenshot on failure), and can gate a pipeline. Treat every OPEN item in PROJECT-CONTEXT.md as a [NEEDS CLARIFICATION] marker; do not guess them.
```
Point out:
- a new branch `001-…` and `specs/001-…/spec.md` were created
- user stories with priorities (P1/P2…) and Given/When/Then acceptance scenarios
- numbered **functional requirements** (FR-001…) and **success criteria**
- **`[NEEDS CLARIFICATION]`** markers: "The AI flags what the brief didn't say, instead of guessing."

**Clarify.**
```
/speckit-clarify
```
Let the PO in the room answer Copilot's questions (the OPEN items from the context file, plus
anything else it found). Show the answers
written into the spec's **Clarifications** section.

**G2: spec approval.** Commit and push, then open a **draft PR**:
```bash
git add specs && git commit -m "spec(001): story verification recordings spec [G2]" && git push -u origin HEAD
```
Show the PR template's gate checklist. The PO and TL approve, which completes G2.

## 4. Construction: plan and tasks (10 min)

**Plan.** Now (and only now) we give technical direction:
```
/speckit-plan Use the stack, repository location, pipeline and runner language from docs/poc/PROJECT-CONTEXT.md (default: .NET 8 with Microsoft.Playwright for .NET, a dotnet tool CLI with record, run and validate commands, xUnit tests). Recording uses the Playwright recorder (codegen): research in research.md how its output, including recorded assertions, becomes the JSON verification file, and pick the simplest reliable approach. Design the JSON verification file from the format requirements in the spec as a versioned JSON Schema in contracts/. Base URL and credentials come from environment variables or the pipeline secret store, never from the file. Output a console summary, JUnit XML for pipelines, and screenshots plus a Playwright trace on failure, with a non-zero exit code on any failed step. Automated tests run against a small local sample page, never the shared environment. Include a task to install Playwright browsers in CI.
```
Show:
- `plan.md`, especially the **Constitution Check** table: "Copilot audited its own design against our rules."
- `research.md` (how Playwright recorder output becomes the JSON file)
- `data-model.md` and `contracts/` (the **JSON verification file schema**: this is the contract)
- `quickstart.md`

**G3:** the TL approves the plan in the PR.

**Tasks.**
```
/speckit-tasks
```
Show `tasks.md`: tasks grouped by user story, `[P]` marks tasks that can run in parallel, tests
come before implementation, and each task names exact file paths.

**Analyze (consistency check).**
```
/speckit-analyze
```
> "Before we write any code, a cross-check: is every requirement covered by a task? Does
> anything contradict the constitution?" Fix any CRITICAL findings.

**G4:** tasks approved.

## 5. Build (10 min, or show a recording)

```
/speckit-implement
```
While it runs, narrate: tests are written first (Principle III), and tasks are ticked off in
`tasks.md`. Then:
```bash
dotnet build && dotnet test
```
**The payoff moment:** record a verification with the Playwright recorder against your
application, show the JSON file, then replay it against the environment. Replay it against a
build where the behaviour is broken (or edit an expected value) to show a failed step with its
screenshot. (Use the exact commands from the generated `quickstart.md`.)

If gaps remain:
```
/speckit-converge
```

Don't push yet: the code goes through the review loop first.

## 6. Review, Attack & Fix (8 min, or show it from the dry-run branch)

Spec Kit stops at implement. This is the step our extension adds. See
[`extensions/review/README.md`](../../extensions/review/README.md) for the full loop.

**Hook.** At the end of `/speckit-implement`, Spec Kit asks *"Run the critic review on what was
just implemented?"*
> "Spec Kit is offering our quality step automatically. We'll run it, but in a fresh chat."

**Critic.** Open a **new Copilot chat** (agent mode), choose your **strongest reasoning model**
in the model picker, and run:
```
/speckit-review-code US1
```
While it runs:
> "This chat didn't write the code, so it has no stake in it. It has to prove every defect with
> a failing test. No test, no finding."

Show:
- `specs/001-…/review/US1/round-1/findings.md`: numbered findings with severity, file:line, scenario and required fix
- the new test file it created (`tests/US1_review_r1_Tests.cs`), with `dotnet test` showing those tests **red**

**Adversary (optional, if time allows).** US1 touches secrets and parses files, so it counts as
critical. In a **second new chat**, run this alongside the critic:
```
/speckit-review-attack US1
```
Show `attack.md`: hostile inputs (oversized files, unicode, secrets in output) as failing tests.

**CI gate, before the fix.** In the terminal:
```bash
bash scripts/check-gates.sh origin/main
```
It fails and lists the open BLOCKER/MAJOR findings.
> "Right now this PR can't merge. CI reads the findings file."

**Rulings: the human moment.** Back in a chat:
```
/speckit-review-rule US1
```
Copilot merges duplicates and asks about anything ambiguous, with a recommendation each time
(for example *"Should unknown fields in a verification file be rejected or ignored?"*). **Let the
PO or Tech Lead answer live.** Show the answers recorded under `## Rulings`.
> "AI proposes, we decide. The fixer has to follow these rulings."

**Fixer.** In a **new chat**, with a standard coding model:
```
/speckit-review-fix US1
```
Show the finding statuses changing to `FIXED`, the earlier red tests now **green**, and
`fix-report.md`.

**CI gate, after the fix.** Commit, then run:
```bash
bash scripts/check-gates.sh origin/main
```
It passes now.

**Final audit (show from the dry run).** `/speckit-review-audit` writes `review/audit.md`: each
requirement marked MET / PARTIAL / MISSING / MANUAL, with its test or file:line as evidence, plus
`manual-checklist.md`.

**G5:** push and show CI (`ai-dlc-gates` + `dotnet-build-test`) going green, with the findings
and audit in the PR. A reviewer approves.

**If the review chat is slow:** switch to the dry-run branch and walk through its `review/`
folder. Don't wait on it live.

## 7. Traceability and wrap-up (5 min)

- In the PR's commit history and review timeline, show the audit trail: G2 → G3 → G4 → review findings and rulings → G5.
- Trace one line: **brief → the "replay" requirement (FR-0xx) → task T0xx → its test → code**.
- Close the loop: "This tool becomes the last step of our own lifecycle. Every future story ends
  with a verification file, and gate G6 replays it against the environment."
- Show the metrics captured during the dry run ([POC-PLAN.md](../poc/POC-PLAN.md#success-criteria--metrics)).
- Close with the recommendation and next steps.

---

## Likely questions and suggested answers

| Question | Answer |
|---|---|
| "Isn't this just more documents?" | The specs are short, AI-drafted and reviewed in minutes. They replace the back-and-forth that normally happens *after* the code is written. |
| "What if the AI is wrong?" | That's why there are gates. Fix the spec or plan and regenerate; don't patch code by hand. |
| "Does this work on existing code?" | Yes. Run `/speckit-specify` for a change on an existing codebase; `/speckit-converge` compares code against the spec. Worth a follow-up POC on a real repo. |
| "Is our code/data safe?" | It uses Copilot under our existing GitHub agreement. Spec Kit itself is a local CLI plus prompt files, and it doesn't call any external service. |
| "Doesn't AI review its own code badly?" | The critic runs in a **new chat** without the builder's reasoning, and must **prove** each defect with a failing test. A person makes the rulings and still reviews the PR. |
| "Won't the review loop slow us down?" | It runs per user story and is capped at 2 rounds. The adversary only runs for critical code. It replaces review comments and QA defects that would otherwise come later. |
| "What if the reviewer is wrong?" | The fixer can mark a finding `DISPUTED` with evidence, and the developer rules. CI only blocks unresolved BLOCKER/MAJOR findings. |
| "Bug fixes too?" | A lighter path: see AI-DLC.md §5. Spec Kit also has an optional `bug` extension. |
