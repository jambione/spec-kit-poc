<!--
Sync Impact Report
- Version: 1.1.0 → 1.2.0 (Playwright recorder is the capture tool; target application,
  environment and JSON format details move to docs/poc/PROJECT-CONTEXT.md)
- Previous: 1.0.0 → 1.1.0 (retargeted to the Story Verification Recordings tool; added VIII)
- Principles added: VIII. Modified: III, IV, V, VI
- Sections added: Technology Standards, AI-DLC Workflow & Quality Gates, Governance
- Templates reviewed: plan-template.md (Constitution Check reads these principles) ✅
- Follow-up TODOs: replace POC defaults with real team standards before wider rollout
-->

# Spec Kit POC Constitution

This is the project's rulebook. GitHub Copilot reads it at every Spec Kit step, and every spec,
plan, task list and pull request must follow it. Lifecycle details live in
[`docs/ai-dlc/AI-DLC.md`](../../docs/ai-dlc/AI-DLC.md).

## Core Principles

### I. Spec Before Code (NON-NEGOTIABLE)
Every change to production code traces back to an approved spec in `specs/<NNN-feature>/`.
The order is fixed: `spec.md` → `plan.md` → `tasks.md` → code. Each artifact is approved at its
gate before the next one is generated. Code without a spec does not get merged, except for
changes that qualify for the bug-fix path in the lifecycle document.

### II. Humans Approve, AI Drafts
AI (GitHub Copilot) drafts specs, plans, tasks and code. A named person approves each gate.
AI output is never merged without human review, and the reviewer owns what they approve.
Any unresolved `[NEEDS CLARIFICATION]` marker blocks its gate.

### III. Test-First
Tests are written from the spec's acceptance scenarios before the implementation, and must fail
first (red, then green, then refactor). Every functional requirement (FR-xxx) is covered by at
least one automated test. Core logic (file model, validation, step execution) needs unit tests;
every CLI command needs an integration test that runs it against a local sample page.
Tests never depend on an external or shared environment.

### IV. Simple, Layered .NET Design
- Start with the simplest structure that works (YAGNI). Use a core library, a CLI and test
  projects unless the plan justifies more in its Complexity Tracking section.
- Keep core rules (file validation, step and assertion execution) out of the CLI layer, in
  plain classes that can be tested on their own.
- Use dependency injection through the built-in container. No service locators and no static
  mutable state.
- Don't add a pattern or library unless the plan explains why it's needed.

### V. Secure by Default
- Verification files are untrusted input: validate them against the schema before running, and
  fail with a clear message naming the file and the problem.
- Credentials, tokens and passwords never appear in verification files, logs, screenshot
  metadata, specs or prompts. They come from environment variables or the pipeline secret store,
  and typed secrets are masked at record time.
- The runner only navigates to the configured environment's allowed hosts.
- Never record or log real personal data; use synthetic test data.

### VI. Observable
Use structured logging through `ILogger<T>` with message templates (no string interpolation).
Every run reports pass/fail per step, and on failure keeps evidence: expected vs found, a
screenshot and a Playwright trace. Exit code is 0 only when every step passes, and results are
also written in a format pipelines can read (JUnit XML).

### VII. Traceable
Commits and PRs reference the feature folder (for example `specs/001-story-verification`). Task IDs
(T001…) appear in commit messages where practical. Git history plus PR approvals form the audit
trail, so don't squash away gate approvals.

### VIII. Verification Files Are a Contract
The JSON verification file is a public, versioned format. Its exact shape comes from the format
requirements in `docs/poc/PROJECT-CONTEXT.md` and is designed in the plan, but it always has a
published JSON Schema and a version marker, links to its story or defect ID, and stays readable
by a person in a pull request. Steps use resilient locators (role, label, test ID) before CSS or XPath. A file holds no
environment-specific values: base URL and credentials are supplied at run time. Breaking changes
to the format need a new schema version and a migration note.

## Technology Standards

| Area | Standard |
|---|---|
| Runtime | .NET 8 LTS (move to the current LTS when the team does), C# with nullable reference types enabled |
| Recording | Playwright recorder (`codegen`), including its assertion tools |
| Browser automation | Playwright; runner language per `PROJECT-CONTEXT.md` (default `Microsoft.Playwright` for .NET). Browsers as the spec requires |
| Project specifics | Target application, environment, pipeline and JSON requirements live in `docs/poc/PROJECT-CONTEXT.md`; specs and plans must not contradict it |
| CLI | A `dotnet tool` using `System.CommandLine` (the plan may justify another parser) |
| File format | JSON via `System.Text.Json`; JSON Schema kept in the repo under `schemas/` |
| Tests | xUnit, FluentAssertions (or plain asserts); automated tests replay against a small local sample page, never a shared environment |
| Style | `dotnet format` clean; warnings treated as errors in `Release` |
| Layout | `src/<Project>/`, `tests/<Project>.UnitTests/`, `tests/<Project>.IntegrationTests/`, `verifications/` for verification files, one `.sln` at the repo root |

## AI-DLC Workflow & Quality Gates

| Gate | Artifact | Approver(s) | Blocking criteria |
|---|---|---|---|
| G1: Intent | Feature brief / issue + `PROJECT-CONTEXT.md` | Product Owner + Tech Lead | Problem, users and success measure stated; `scripts/check-context.sh` passes |
| G2: Spec | `spec.md` | Product Owner + Tech Lead | No `[NEEDS CLARIFICATION]` left; requirements are testable |
| G3: Plan | `plan.md`, `data-model.md`, `contracts/` | Tech Lead / Architect | Constitution Check passes; any complexity is justified |
| G4: Tasks | `tasks.md` (+ `/speckit-analyze` report) | Tech Lead | Every FR maps to a task; no CRITICAL analyze findings |
| G5: Code | Pull request | 1+ reviewer (not the author) | CI green; tests for every FR; PR checklist complete |
| G6: Release | Merge to `main` / deploy | Release owner | Pipeline green; demo done or sign-off given |

## Governance

- This constitution overrides conflicting conventions. When they conflict, the constitution wins
  and the conflict is raised in the PR.
- Amendments are made by PR to this file using `/speckit-constitution`, approved by the Tech
  Lead, and versioned with SemVer (MAJOR: a principle removed or redefined; MINOR: a principle
  added; PATCH: wording only).
- Reviewers check compliance using the PR template checklist.
- Runtime guidance for Copilot lives in `.github/copilot-instructions.md`.

**Version**: 1.2.0 | **Ratified**: 2026-11-12 | **Last Amended**: 2026-11-12
