# Implementation Plan: Story Verification Recordings

**Branch**: `001-story-verification-recordings` | **Date**: 2026-11-12 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/001-story-verification-recordings/spec.md`

**Status**: Approved (G3): *reference example*

## Summary

Build a .NET command-line tool, `storyverify`, with three commands:
- **`record`** opens the Playwright recorder in JSONL mode for a work item, then converts the
  recording into a JSON verification file.
- **`run`** validates files and replays them with Playwright against an environment. It reports
  per step, keeps failure evidence and writes JUnit XML.
- **`validate`** checks files against the published schema and the safety rules, without a
  browser.

All format, validation, conversion and execution logic lives in a core library tested against
local sample pages. An example GitHub Actions workflow shows the gate (G6).

## Technical Context

**Language/Version**: C# on .NET 8 (LTS), nullable enabled

**Primary Dependencies**: `Microsoft.Playwright` (pinned), `System.CommandLine`, `JsonSchema.Net`, `System.Text.Json`

**Storage**: Files only: verification files (`verifications/**.verify.json`), settings (`storyverify.json`), run output (`verify-results/`)

**Testing**: xUnit (plain asserts). Integration tests run the CLI against static sample pages served by an in-test ASP.NET Core host

**Target Platform**: Windows, macOS and Linux developer machines (recording needs a desktop session); Linux CI agents (replay runs headless)

**Project Type**: CLI tool (`dotnet tool`) + core library

**Performance Goals**: Validate 100 files in < 5 s (SC-006). Replay overhead per step < 200 ms beyond the application's own response time

**Constraints**: No secrets in files or output (constitution V); paths only, no hosts, in files (VIII); navigation limited to the environment's hosts (FR-014)

**Scale/Scope**: Tens to low hundreds of verification files per repository; 5–30 steps per file

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-checked after Phase 1 design: still passes.*

| Principle | How this plan complies | Status |
|---|---|---|
| I. Spec Before Code | Spec approved at G2; tasks.md generated before code | ✅ |
| II. Humans Approve, AI Drafts | Gates G3/G4 on this plan and tasks; no `[NEEDS CLARIFICATION]` left in spec | ✅ |
| III. Test-First | Every user story phase in tasks.md starts with failing tests; integration tests use local sample pages only | ✅ |
| IV. Simple, Layered Design | Two projects (Core + Cli) + two test projects; no extra frameworks; logic in Core, Cli is thin | ✅ |
| V. Secure by Default | Schema validation before every run; secrets as references resolved from env vars and masked; password fills replaced at record time; host allow-list | ✅ |
| VI. Observable | `ILogger<T>` structured logging; per-step results; screenshot + trace on failure; JUnit XML; exit codes | ✅ |
| VII. Traceable | Work item ID required in every file; commits reference task IDs | ✅ |
| VIII. Verification Files Are a Contract | Versioned JSON Schema in `schemas/` and `contracts/`; `schemaVersion` field; resilient targets preferred, CSS warned | ✅ |

## Project Structure

### Documentation (this feature)

```text
specs/001-story-verification-recordings/
├── plan.md              # This file
├── research.md          # Phase 0: recorder JSONL approach and mappings
├── data-model.md        # Phase 1: entities and rules
├── quickstart.md        # Phase 1: end-to-end validation steps
├── contracts/
│   ├── verification-file.schema.json   # The file format (the contract)
│   ├── example.verify.json             # A complete example file
│   └── cli.md                          # Commands, options, exit codes, env vars
└── tasks.md             # Phase 2 (/speckit-tasks)
```

### Source Code (repository root)

```text
StoryVerify.sln
storyverify.json                       # settings: environments, paths, work item pattern
schemas/
└── verification-file.v1.schema.json   # published copy of contracts/verification-file.schema.json
src/
├── StoryVerify.Core/
│   ├── Model/            # VerificationFile, Step, Target, WorkItem (System.Text.Json types)
│   ├── Schema/           # embedded schema + SchemaValidator
│   ├── Validation/       # FileValidator: schema, work item pattern, URL/secret/CSS rules
│   ├── Settings/         # RunSettings, SettingsLoader (storyverify.json + env vars)
│   ├── Placeholders/     # {{var:}} / {{secret:}} resolution and masking
│   ├── Recording/        # RecorderLauncher (codegen --target jsonl), JsonlConverter, SecretDetector
│   ├── Execution/        # Runner, StepExecutor, TargetResolver, HostGuard
│   └── Reporting/        # ConsoleReporter, JUnitWriter, EvidenceWriter
└── StoryVerify.Cli/
    ├── Program.cs
    └── Commands/         # RecordCommand, RunCommand, ValidateCommand
tests/
├── StoryVerify.Core.UnitTests/
│   └── Fixtures/         # recorded JSONL samples (from spike T007), valid/invalid files
└── StoryVerify.Cli.IntegrationTests/
    ├── SampleSite/       # static HTML pages: login, form, cart
    └── SampleSiteHost.cs # in-test ASP.NET Core static file host
verifications/
└── PROJ-123/
    └── sample-login.verify.json       # example, runs against SampleSite in CI
.github/workflows/
└── verify.yml            # example gate: run verifications against an environment
```

**Structure Decision**: Single solution, with a core library and a thin CLI. This is the minimum
that keeps logic testable without the CLI (constitution IV). The schema lives in one source
(`schemas/`), is embedded into Core at build time, and is mirrored in `contracts/` for review.

## Phase 0: Research

See [research.md](research.md). All clarifications are resolved. Key decisions:
- Recorder in `--target jsonl` mode plus a converter (R1–R3)
- `{{var:}}` / `{{secret:}}` placeholders from environment variables (R4)
- Label-based password detection (R5)
- Optional storage state for SSO (R6)
- Host guard via routing (R7)
- Playwright web-first assertions (R8)
- JUnit XML (R9)

## Phase 1: Design

- **Data model**: [data-model.md](data-model.md)
- **Contracts**: [verification-file.schema.json](contracts/verification-file.schema.json), [example.verify.json](contracts/example.verify.json), [cli.md](contracts/cli.md)
- **Validation guide**: [quickstart.md](quickstart.md)

## Complexity Tracking

No constitution violations. Nothing to justify.
