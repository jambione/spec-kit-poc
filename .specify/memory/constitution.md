<!--
Sync Impact Report
- Version: 0.0.0 → 1.0.0 (initial ratification for the AI-DLC + Spec Kit POC)
- Principles added: I–VII
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
least one automated test. Business logic needs unit tests; every HTTP endpoint needs an
integration test using `WebApplicationFactory`.

### IV. Simple, Layered .NET Design
- Start with the simplest structure that works (YAGNI). Use one Web API project plus test
  projects unless the plan justifies more in its Complexity Tracking section.
- Keep domain rules (validation, state transitions) out of controllers and endpoints, in plain
  classes that can be tested on their own.
- Use dependency injection through the built-in container. No service locators and no static
  mutable state.
- Don't add a pattern or library (MediatR, AutoMapper, generic repositories and so on) unless
  the plan explains why it's needed.

### V. Secure by Default
- Validate all input at the API boundary and return RFC 7807 `ProblemDetails` for errors.
- Keep secrets out of source control, prompts and spec files. Use User Secrets locally and the
  platform secret store elsewhere.
- Endpoints require authorization unless the spec explicitly says otherwise.
- Never log personal data (names, emails, free-text reasons).

### VI. Observable
Use structured logging through `ILogger<T>` with message templates (no string interpolation).
Each request is traceable by correlation ID. Expose a health check at `/health`.

### VII. Traceable
Commits and PRs reference the feature folder (for example `specs/001-leave-requests`). Task IDs
(T001…) appear in commit messages where practical. Git history plus PR approvals form the audit
trail, so don't squash away gate approvals.

## Technology Standards

| Area | Standard |
|---|---|
| Runtime | .NET 8 LTS (move to the current LTS when the team does), C# with nullable reference types enabled |
| API | ASP.NET Core Minimal APIs or Controllers (the plan decides), OpenAPI via `Microsoft.AspNetCore.OpenApi` |
| Data | EF Core. Use SQLite or InMemory for the POC; the production provider is decided in the plan |
| Tests | xUnit, FluentAssertions (or plain asserts), `Microsoft.AspNetCore.Mvc.Testing` |
| Style | `dotnet format` clean; warnings treated as errors in `Release` |
| Layout | `src/<Project>/`, `tests/<Project>.UnitTests/`, `tests/<Project>.IntegrationTests/`, one `.sln` at the repo root |

## AI-DLC Workflow & Quality Gates

| Gate | Artifact | Approver(s) | Blocking criteria |
|---|---|---|---|
| G1: Intent | Feature brief / issue | Product Owner | Problem, users and success measure are stated |
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

**Version**: 1.0.0 | **Ratified**: 2026-11-12 | **Last Amended**: 2026-11-12
