---

description: "Task list for Story Verification Recordings (reference example)"
---

# Tasks: Story Verification Recordings

**Input**: Design documents from `/specs/001-story-verification-recordings/`

**Prerequisites**: [plan.md](plan.md), [spec.md](spec.md), [research.md](research.md), [data-model.md](data-model.md), [contracts/](contracts/)

**Status**: Approved (G4): *reference example*

**Tests**: Required. Constitution III makes tests mandatory and test-first. In every phase, the
test tasks come before the implementation tasks and must fail first.

**Organization**: Tasks are grouped by user story, so each story can be built, tested and demoed
on its own.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: The user story the task belongs to (US1–US4)
- Every task names exact file paths

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Solution skeleton, pinned dependencies, and the de-risking spike

- [ ] T001 Create `StoryVerify.sln` with `src/StoryVerify.Core`, `src/StoryVerify.Cli` (`PackAsTool`, `ToolCommandName` = `storyverify`), `tests/StoryVerify.Core.UnitTests`, `tests/StoryVerify.Cli.IntegrationTests`; add `Directory.Build.props` (net8.0, `Nullable` enabled, `TreatWarningsAsErrors` in Release)
- [ ] T002 [P] Add pinned package references: `Microsoft.Playwright`, `System.CommandLine`, `JsonSchema.Net` (Core/Cli); `xunit`, `xunit.runner.visualstudio`, `Microsoft.NET.Test.Sdk` (tests); `Microsoft.AspNetCore.App` framework reference (integration tests)
- [ ] T003 [P] Add `.editorconfig`; confirm `dotnet format --verify-no-changes` passes
- [ ] T004 [P] Copy `contracts/verification-file.schema.json` to `schemas/verification-file.v1.schema.json` and embed it as a resource in `src/StoryVerify.Core/StoryVerify.Core.csproj`
- [ ] T005 [P] Add `storyverify.json` with placeholder environments (see contracts/cli.md); add `verify-results/` to `.gitignore`
- [ ] T006 Add a "Install Playwright Chromium" step (`pwsh src/StoryVerify.Cli/bin/Release/net8.0/playwright.ps1 install --with-deps chromium`) after build in `.github/workflows/ci.yml`
- [ ] T007 **Spike (risk R1):**
  - Run the recorder through the .NET driver (`Microsoft.Playwright.Program.Main(["codegen", "--target", "jsonl", "--output", <file>, <url>])`) against a simple page.
  - Record four sessions: sign in + assert text; select + check; opening a second tab; file upload. Save them as `tests/StoryVerify.Core.UnitTests/Fixtures/recorder/*.jsonl`.
  - Write the actual `kind`/`body`/`options` values into research.md R3.
  - **If `jsonl` isn't accepted by the pinned version, stop and raise it at G3.**

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: File model, schema validation, settings, placeholders and the local sample site.
Every story depends on these.

**⚠️ CRITICAL**: No user story work starts until this phase is complete.

- [ ] T008 [P] Create sample pages `tests/StoryVerify.Cli.IntegrationTests/SampleSite/login.html`, `account.html`, `cart.html` and `form.html`. Use roles, labels, `data-testid` attributes, a password field, a discount code that changes the total, a select and a checkbox
- [ ] T009 Create `tests/StoryVerify.Cli.IntegrationTests/SampleSiteHost.cs`: an xUnit fixture serving `SampleSite/` on a random port with ASP.NET Core static files, plus a `--serve-sample-site --urls <url>` entry point (used by quickstart.md)
- [ ] T010 [P] Write serialization round-trip tests (including `contracts/example.verify.json`, every step type, and every target kind) in `tests/StoryVerify.Core.UnitTests/Model/ModelSerializationTests.cs`
- [ ] T011 [P] Implement model types with step polymorphism on `action` (System.Text.Json) in `src/StoryVerify.Core/Model/VerificationFile.cs`, `WorkItem.cs`, `Step.cs` and `Target.cs`
- [ ] T012 [P] Write settings precedence tests (file → environment variables → CLI options; unknown environment → error) in `tests/StoryVerify.Core.UnitTests/Settings/SettingsLoaderTests.cs`
- [ ] T013 Implement `RunSettings` and `SettingsLoader` in `src/StoryVerify.Core/Settings/`
- [ ] T014 [P] Write placeholder tests in `tests/StoryVerify.Core.UnitTests/Placeholders/PlaceholderTests.cs`: `{{var:}}`/`{{secret:}}` resolution from `VERIFY_VAR_*`/`VERIFY_SECRET_*`, missing names listed together, and masking of secret values
- [ ] T015 Implement `PlaceholderResolver` and `SecretMasker` in `src/StoryVerify.Core/Placeholders/`
- [ ] T016 [P] Add invalid fixtures in `tests/StoryVerify.Core.UnitTests/Fixtures/invalid/`: absolute URL, hard-coded password, no expectation, bad work item ID, two locators, schema version 2.0, undeclared variable, unused secret. Write `tests/StoryVerify.Core.UnitTests/Validation/FileValidatorTests.cs` covering each error and the CSS warning
- [ ] T017 Implement `SchemaValidator` (embedded schema, JsonSchema.Net) and `FileValidator` in `src/StoryVerify.Core/Validation/`. Rules beyond the schema: work item pattern, secret-looking literals, declared vs used names, CSS warning, supported major version
- [ ] T018 Add the CLI skeleton in `src/StoryVerify.Cli/Program.cs`: root command, `ILogger` console logging to stderr, and an `ExitCode` enum matching contracts/cli.md in `src/StoryVerify.Core/ExitCode.cs`

**Checkpoint**: Files can be loaded, validated and resolved, and the sample site runs.

---

## Phase 3: User Story 1 - Replay a verification file against an environment (Priority: P1) 🎯 MVP

**Goal**: `storyverify run` replays hand-written files against an environment, with per-step
results, evidence and exit codes.

**Independent Test**: quickstart.md §2: a hand-written file passes against the sample site,
then fails with evidence after one expected value is changed.

### Tests for User Story 1 ⚠️ write first, confirm they fail

- [ ] T019 [P] [US1] `TargetResolver` tests in `tests/StoryVerify.Cli.IntegrationTests/Execution/TargetResolverTests.cs`: each target kind finds the intended element on the sample site, and `nth` 0 and -1 work
- [ ] T020 [P] [US1] Passing-run test in `tests/StoryVerify.Cli.IntegrationTests/RunCommandTests.cs`: all steps passed, exit 0, `junit.xml` and `summary.json` written
- [ ] T021 [P] [US1] Failing-run test in `RunCommandTests.cs`: wrong `expectText` → that step failed with expected and found values, later steps skipped, `screenshot.png` and `trace.zip` written, exit 1
- [ ] T022 [P] [US1] Secrets test in `RunCommandTests.cs`: a missing secret → exit 3 before any browser starts; with the secret supplied, its value never appears in stdout, stderr, `junit.xml` or `summary.json`
- [ ] T023 [P] [US1] Edge-case tests in `RunCommandTests.cs`: navigation to another host is blocked and the step fails; an unreachable base URL → exit 4; a locator matching several elements fails and reports the count

### Implementation for User Story 1

- [ ] T024 [US1] Implement `TargetResolver` (target → `GetByRole`/`GetByLabel`/`GetByTestId`/`GetByPlaceholder`/`GetByText`/`GetByAltText`/`GetByTitle`/`Locator`, then `Nth`/`Last`) in `src/StoryVerify.Core/Execution/TargetResolver.cs`
- [ ] T025 [US1] Implement `StepExecutor`: every action and expectation in data-model.md using Playwright `Assertions.Expect`, with the per-step timeout. In `src/StoryVerify.Core/Execution/StepExecutor.cs`
- [ ] T026 [US1] Implement `HostGuard` (abort document requests outside the base URL host and `allowedHosts`) in `src/StoryVerify.Core/Execution/HostGuard.cs`
- [ ] T027 [US1] Implement `Runner` in `src/StoryVerify.Core/Execution/Runner.cs`:
  - discover and validate files; resolve placeholders, stopping early if any are missing
  - give each file a fresh context, using `VERIFY_STORAGE_STATE` if set, with tracing on
  - skip the remaining steps after a failure
  - save evidence via `src/StoryVerify.Core/Reporting/EvidenceWriter.cs`
- [ ] T028 [P] [US1] Implement `ConsoleReporter` (per-step PASSED/FAILED/SKIPPED, expected vs found, secrets masked) in `src/StoryVerify.Core/Reporting/ConsoleReporter.cs`
- [ ] T029 [P] [US1] Implement `JUnitWriter` and `summary.json` output in `src/StoryVerify.Core/Reporting/JUnitWriter.cs`
- [ ] T030 [US1] Implement `run` with `--env`, `--base-url`, `--browser`, `--timeout`, `--headed` and `--output`, mapping results to exit codes, in `src/StoryVerify.Cli/Commands/RunCommand.cs`
- [ ] T031 [US1] Add `verifications/PROJ-123/sample-login.verify.json` (sign in + account page + discount) targeting the sample site

**Checkpoint**: The MVP: verification files can be replayed against any environment, and US1 is
demoable on its own.

---

## Phase 4: User Story 2 - Record a verification with the Playwright recorder (Priority: P2)

**Goal**: `storyverify record` opens the recorder and writes a valid, replayable file.

**Independent Test**: quickstart.md §3: record on the sample site, then the file replays with
no edits.

### Tests for User Story 2 ⚠️ write first, confirm they fail

- [ ] T032 [P] [US2] `JsonlConverter` tests using the T007 fixtures, in `tests/StoryVerify.Core.UnitTests/Recording/JsonlConverterTests.cs`: the header line is skipped, each action maps per research R2, each locator per R3, hosts are stripped to paths, and new tabs/uploads are reported as unsupported
- [ ] T033 [P] [US2] `SecretDetector` tests in `tests/StoryVerify.Core.UnitTests/Recording/SecretDetectorTests.cs`: password, PIN and token labels become `{{secret:NAME}}` with the name derived from the label; ordinary fields are unchanged
- [ ] T034 [P] [US2] `record` tests using a fake `IRecorderLauncher` that replays a fixture, in `tests/StoryVerify.Cli.IntegrationTests/RecordCommandTests.cs`:
  - no assertion → exit 5 and nothing written
  - unsupported steps need `--yes`
  - the file path is `verifications/<ID>/<slug>.verify.json`
  - the written file passes `validate`
  - the temp JSONL is deleted

### Implementation for User Story 2

- [ ] T035 [US2] Implement `JsonlConverter` in `src/StoryVerify.Core/Recording/JsonlConverter.cs`
- [ ] T036 [US2] Implement `SecretDetector` in `src/StoryVerify.Core/Recording/SecretDetector.cs`
- [ ] T037 [US2] Implement `IRecorderLauncher` and `RecorderLauncher` (calls `Microsoft.Playwright.Program.Main` with `codegen --target jsonl --output <temp>`; blocks until the recorder closes) in `src/StoryVerify.Core/Recording/RecorderLauncher.cs`
- [ ] T038 [US2] Implement `record` in `src/StoryVerify.Cli/Commands/RecordCommand.cs`: options per contracts/cli.md, author from `git config user.name`, slug from the title, confirmation of unsupported steps, write and validate the file, print the secret names to supply
- [ ] T039 [US2] Manual check on a desktop machine: run quickstart.md §3, time it (SC-001), confirm the replay needs no edits (SC-002), and record the results in the PR

**Checkpoint**: US1 and US2 both work on their own.

---

## Phase 5: User Story 3 - Validate verification files in a pull request (Priority: P3)

**Goal**: `storyverify validate` checks files without a browser, locally and in CI.

**Independent Test**: quickstart.md §1.

### Tests for User Story 3 ⚠️ write first, confirm they fail

- [ ] T040 [P] [US3] Validate-command tests in `tests/StoryVerify.Cli.IntegrationTests/ValidateCommandTests.cs`: the invalid fixtures folder → exit 2 with one `ERROR` line per file, including path and step number; a CSS target → `WARN` with exit 0; valid files → exit 0
- [ ] T041 [P] [US3] Performance test: generate 100 valid files and assert validation takes < 5 s (SC-006), in `tests/StoryVerify.Cli.IntegrationTests/ValidatePerformanceTests.cs`

### Implementation for User Story 3

- [ ] T042 [US3] Implement `validate` in `src/StoryVerify.Cli/Commands/ValidateCommand.cs`
- [ ] T043 [US3] Add a step that runs `storyverify validate verifications/` to `.github/workflows/ci.yml`

**Checkpoint**: Every PR's verification files are validated automatically.

---

## Phase 6: User Story 4 - Gate a pipeline on verification results (Priority: P3)

**Goal**: The pipeline runs verifications against an environment and fails on any failure (G6).

**Independent Test**: quickstart.md §4.

### Tests for User Story 4 ⚠️ write first, confirm they fail

- [ ] T044 [P] [US4] Test that `--work-item PROJ-123` runs only files linked to `PROJ-123`, in `tests/StoryVerify.Cli.IntegrationTests/RunCommandTests.cs`

### Implementation for User Story 4

- [ ] T045 [US4] Implement the `--work-item` filter in `src/StoryVerify.Core/Execution/Runner.cs` and `src/StoryVerify.Cli/Commands/RunCommand.cs`
- [ ] T046 [US4] Create `.github/workflows/verify.yml`:
  - build the tool and install Chromium
  - run against the sample site by default, or against `--env <input>` on `workflow_dispatch`
  - map `VERIFY_SECRET_*` from repository secrets
  - upload `verify-results/` and publish `junit.xml`
- [ ] T047 [US4] Check the gate end to end: a PR with a deliberately wrong expectation fails `verify.yml` and shows the failed step in the test report; then revert it

**Checkpoint**: All user stories work on their own.

---

## Phase 7: Polish & Cross-Cutting Concerns

- [ ] T048 [P] Write `docs/verifications.md` (how to record, run and validate; secrets and variables; troubleshooting) and link it from `README.md`
- [ ] T049 [P] Turn on the G5 "Verification file" checkbox in `.github/pull_request_template.md` and the G5/G6 rows in `docs/ai-dlc/AI-DLC.md` (remove the "once the tool exists" notes)
- [ ] T050 Security pass: run the full test suite with a known secret value and grep all output and artifacts for it (expect none); confirm temp JSONL files are deleted (SC-005)
- [ ] T051 Run quickstart.md end to end and paste the results into the PR

---

## Dependencies & Execution Order

- **Setup (Phase 1)**: start immediately. **T007 (spike) first**; it can change the plan.
- **Foundational (Phase 2)**: needs Setup. Blocks every story.
- **US1 (Phase 3)**: needs Foundational. The MVP.
- **US2 (Phase 4)**: needs Foundational and the T007 fixtures. Can run in parallel with US1, but its manual check (T039) replays with US1.
- **US3 (Phase 5)**: needs Foundational only (T017 holds the rules); can run in parallel with US1.
- **US4 (Phase 6)**: needs US1 (the runner) and US3 (the CI validate step).
- **Polish (Phase 7)**: after the stories you're shipping.

Within each story: tests → models/core → command → checkpoint.

## Parallel Example: User Story 1

```text
Together (different files):  T019, T020, T021, T022, T023   # tests
Then:                        T024 → T025 → T026 → T027      # core execution, in order
Together:                    T028, T029                     # reporters
Then:                        T030 → T031
```

## Implementation Strategy

1. **Setup + spike (T001–T007).** If the spike fails, go back to G3 before writing anything else.
2. **Foundational (T008–T018).**
3. **US1 → stop and demo** with hand-written files. This alone proves "verified in the environment".
4. **US2**: recording, the developer-facing part.
5. **US3 + US4**: PR validation and the pipeline gate.
6. **Polish.**

## Requirement Coverage (what `/speckit-analyze` checks)

| Requirement | Tasks |
|---|---|
| FR-001, FR-002 | T004, T010, T011, T016, T017 |
| FR-003 | T016, T017, T032, T035 |
| FR-004 | T011, T019, T024 |
| FR-005 | T004, T017 |
| FR-006 | T020, T030 |
| FR-007 | T016, T027 |
| FR-008, FR-009 | T019, T021, T025 |
| FR-010 | T021, T027 |
| FR-011 | T020, T028, T029 |
| FR-012 | T018, T020, T021, T030 |
| FR-013 | T014, T015, T022, T027 |
| FR-014 | T023, T026 |
| FR-015 | T027, T030 |
| FR-016 | T016, T017, T040, T042 |
| FR-017 | T016, T017, T040 |
| FR-018 | T037, T038 |
| FR-019 | T032, T035 |
| FR-020 | T033, T036 |
| FR-021 | T034, T038 |
| FR-022 | T032, T034, T035, T038 |
| FR-023 | T034, T038 |
| FR-024 | T044, T045 |
| FR-025 | T046, T047 |
| SC-001, SC-002 | T039 |
| SC-004 | T021 |
| SC-005 | T022, T050 |
| SC-006 | T041 |
| SC-003 | Measured in the POC review (not automatable) |

## Notes

- Commit after each task or logical group, with the task ID in the message (constitution VII).
- Tick tasks `[X]` as they're completed. The CI gate check reports done/open counts.
- Stop at any checkpoint to demo the story on its own.
