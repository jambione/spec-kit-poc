# Copilot instructions for this repository

This repo follows a **spec-driven, AI-assisted lifecycle (AI-DLC)** using GitHub Spec Kit.

- **Read first:** `.specify/memory/constitution.md` (rules that can't be broken) and
  `docs/ai-dlc/AI-DLC.md` (phases and gates).
- **Order of work:** constitution → `/speckit-specify` → `/speckit-clarify` → `/speckit-plan` →
  `/speckit-tasks` → `/speckit-analyze` → `/speckit-implement`. Do not write production code
  for a feature unless `specs/<feature>/spec.md`, `plan.md` and `tasks.md` exist.
- **Stack:** .NET 8, C#, nullable enabled, ASP.NET Core, EF Core, xUnit,
  `WebApplicationFactory` for integration tests. Solution file at the repo root; code in `src/`,
  tests in `tests/`.
- **Tests first:** write failing tests from the acceptance scenarios before the implementation.
- **Don't** invent requirements. If something is ambiguous, add `[NEEDS CLARIFICATION: …]` to the
  spec instead of guessing.
- **Don't** put secrets, real personal data or connection strings with credentials in code,
  specs or prompts.
- Use `ILogger<T>` message templates (no string interpolation in log calls) and return
  `ProblemDetails` for errors.
- When you complete a task from `tasks.md`, mark it `[X]` and mention its ID in the commit message.
