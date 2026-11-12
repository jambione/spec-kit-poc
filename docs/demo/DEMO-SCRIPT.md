# Demo Script: AI-DLC with Spec Kit + GitHub Copilot

**Length:** about 45 min live (or 20 min with pre-recorded build steps)
**Audience:** engineering team and leads
**Feature:** [Team Leave Requests](feature-brief.md), a .NET 8 Web API

> **Tip:** Do a full dry run the day before on a branch named `dry-run/*`. Keep that branch as a
> **fallback**: if Copilot is slow or goes off track live, switch to it and walk through the
> artifacts that are already there.

---

## 0. Prerequisites (set up before the demo)

| Need | Check |
|---|---|
| VS Code with the GitHub Copilot + Copilot Chat extensions, signed in | Copilot Chat opens; **Agent** mode is available |
| .NET 8 SDK | `dotnet --version` → 8.x |
| Python 3.11+ (runs the Spec Kit helper scripts) | `python --version` |
| Spec Kit CLI (optional; the repo is already initialized) | `uv tool install specify-cli` → `specify --version` (POC pinned at 1.4.0) |
| Git + push access to this repo | `git push` works |

Open the repo in VS Code and open **Copilot Chat → Agent mode**. Typing `/speckit` should list
the Spec Kit skills (they come from `.github/skills/`).

---

## 1. Set the scene (3 min)

Show [`docs/ai-dlc/AI-DLC.md`](../ai-dlc/AI-DLC.md) section 2 (the phase diagram).
> "AI drafts, humans decide. Every arrow is a Copilot command; every [G] is a person approving
> in a PR."

## 2. Foundation: the constitution (4 min)

Open `.specify/memory/constitution.md`.
> "These are our engineering rules: .NET 8, test-first, security, logging. Copilot checks every
> plan against them. We wrote them once, using `/speckit-constitution`."

(Optional live amendment, if time allows:)
```
/speckit-constitution Add a principle: all public API endpoints must be versioned under /api/v1.
```

## 3. Inception: intent to spec (8 min)

**G1.** Show [`feature-brief.md`](feature-brief.md): "This is what a PO hands us."

**Specify.** In Copilot Chat:
```
/speckit-specify Build a Team Leave Requests capability. Employees submit leave requests (start date, end date, type: vacation/sick/other, optional reason), view their own requests and status (pending/approved/rejected/cancelled), and cancel requests that have not started. Managers view pending requests for their team and approve or reject them (comment required on reject). An employee cannot have two overlapping active requests. Out of scope: leave balances, holiday calendars, notifications, UI. Success: a manager processes a request in under 1 minute; no overlapping leave is approved.
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
Let the PO in the room answer Copilot's questions (half days? past dates? self-approval? cancelling
approved leave?). Show the answers written into the spec's **Clarifications** section.

**G2: spec approval.** Commit and push, then open a **draft PR**:
```bash
git add specs && git commit -m "spec(001): leave requests spec [G2]" && git push -u origin HEAD
```
Show the PR template's gate checklist. The PO and TL approve, which completes G2.

## 4. Construction: plan and tasks (10 min)

**Plan.** Now (and only now) we give technical direction:
```
/speckit-plan .NET 8 ASP.NET Core Minimal API in src/LeaveRequests.Api, EF Core with SQLite, xUnit unit tests in tests/LeaveRequests.UnitTests and WebApplicationFactory integration tests in tests/LeaveRequests.IntegrationTests. Keep domain rules (overlap, state transitions) in a plain Domain folder. Fake authentication via a header (X-User-Id, X-User-Role) is acceptable for the POC.
```
Show:
- `plan.md`, especially the **Constitution Check** table: "Copilot audited its own design against our rules."
- `data-model.md` (the LeaveRequest entity and its state machine)
- `contracts/` (the API contract) and `quickstart.md`

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
If gaps remain:
```
/speckit-converge
```

**G5:** push and show CI (`ai-dlc-gates` + `dotnet-build-test`) going green; a reviewer approves.

## 6. Traceability and wrap-up (5 min)

- In the PR's commit history and review timeline, show the audit trail: G2 → G3 → G4 → G5.
- Trace one line: **brief → FR-005 (no overlaps) → task T0xx → test `…Overlap…` → code**.
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
| "Bug fixes too?" | A lighter path: see AI-DLC.md §5. Spec Kit also has an optional `bug` extension. |
