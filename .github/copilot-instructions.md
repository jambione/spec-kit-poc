# Copilot instructions for this repository

This repo follows a **spec-driven, AI-assisted lifecycle (AI-DLC)** using GitHub Spec Kit.

- **Read first:** `.specify/memory/constitution.md` (rules that can't be broken) and
  `docs/ai-dlc/AI-DLC.md` (phases and gates).
- **Order of work:** constitution → `/speckit-specify` → `/speckit-clarify` → `/speckit-plan` →
  `/speckit-tasks` → `/speckit-analyze` → `/speckit-implement`. Do not write production code
  for a feature unless `specs/<feature>/spec.md`, `plan.md` and `tasks.md` exist.
- **Product:** Story Verification Recordings: developers record expected behaviour with the
  **Playwright recorder** (codegen), it becomes a JSON verification file, and a Playwright runner
  replays it against an environment.
- **Project specifics** (target repository, environment, pipeline, JSON format requirements) are
  in `docs/poc/PROJECT-CONTEXT.md`. Use them; never invent them. Treat any `OPEN:` or `TODO:`
  item there as `[NEEDS CLARIFICATION]`.
- **Stack (default, unless PROJECT-CONTEXT.md says otherwise):** .NET 8, C#, nullable enabled,
  `Microsoft.Playwright` for .NET, a `dotnet tool` CLI, `System.Text.Json`, xUnit. Solution file at the repo root; code in `src/`, tests in `tests/`.
- **Verification files** are a versioned contract (constitution VIII): keep the JSON Schema and
  the model in sync, prefer role/label/test-id locators, and never write secrets or
  environment-specific URLs into them.
- **Tests first:** write failing tests from the acceptance scenarios before the implementation.
- **Don't** invent requirements. If something is ambiguous, add `[NEEDS CLARIFICATION: …]` to the
  spec instead of guessing.
- **Don't** put secrets, real personal data or connection strings with credentials in code,
  specs or prompts.
- Use `ILogger<T>` message templates (no string interpolation in log calls). Errors name the
  file and step that failed.
- When you complete a task from `tasks.md`, mark it `[X]` and mention its ID in the commit message.
