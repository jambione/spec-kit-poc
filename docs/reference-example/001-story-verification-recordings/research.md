# Research: Story Verification Recordings

**Feature**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md) | **Date**: 2026-11-12

Each entry: **Decision**, **Rationale**, **Alternatives considered**.

---

## R1. How Playwright recorder output becomes the verification file

**Decision**: Run the Playwright recorder (`codegen`) with **`--target jsonl`**, which writes one
JSON object per recorded action, then convert that output into our verification file format
(`contracts/verification-file.schema.json`).

**Rationale**
- The recorder already has everything developers need: a browser, action capture, locator
  generation and **assertion tools** (assert visibility, text, value and checked state).
- The JSONL generator emits structured data rather than code. Each line holds the action
  `name` (e.g. `click`, `fill`, `assertText`), its values (`text`, `value`, `checked`, `url`,
  `key`, `options`), the raw `selector`, and a structured **`locator`** object
  (`{ "kind", "body", "options", "next" }`). Converting that is a mapping problem, not a parsing
  problem.
- Confirmed in Playwright 1.63 source: the `jsonl` language generator is registered in the
  recorder's language set alongside JavaScript, Python, Java and C#.

**Caveat**: `jsonl` isn't in the documented `--target` list in the CLI help, which means it
could change without notice. Mitigations:
- Pin the Playwright version.
- Keep recorded JSONL samples as test fixtures (task T007), so an upgrade that changes the
  format fails tests instead of silently producing bad files.
- Isolate all JSONL knowledge in one converter class.

**Alternatives considered**
- *Parse the C# code that codegen generates*: rejected. It means parsing code (Roslyn) for a
  data problem, and generated code changes style between versions.
- *Write a custom recorder* (injected script + our own toolbar): rejected for v1. It's weeks of
  work to rebuild what the Playwright recorder already does well.
- *Make the JSONL itself the file format*: rejected. It contains internal selector syntax and
  page GUIDs, isn't designed to be hand-edited, and isn't a stable contract for us
  (constitution VIII).

## R2. Mapping recorder actions to steps

**Decision**: Map these JSONL actions. Anything else is reported as unsupported (FR-022).

| JSONL `name` | Step `action` | Notes |
|---|---|---|
| `openPage` (first), `navigate` | `navigate` | URL reduced to a path (FR-019); a later `openPage` = new tab → unsupported in v1 |
| `click` | `click` | `clickCount: 2` → `dblclick` |
| `fill` | `fill` | Value replaced with a secret reference if the field looks like a password (R5) |
| `press` | `press` | `key` copied |
| `check` / `uncheck` | `check` / `uncheck` | |
| `select` | `select` | `options` copied |
| `assertText` | `expectText` | `substring: true` → `match: "contains"`, else `exact` |
| `assertValue` | `expectValue` | |
| `assertChecked` | `expectChecked` | |
| `assertVisible` | `expectVisible` | |
| `closePage` | (ignored) | |
| `setInputFiles`, `assertSnapshot`, others | unsupported | Listed to the developer |

`expectHidden` and `expectPath` aren't produced by the recorder; developers add them by hand,
which the format allows (spec clarification).

The first JSONL line is a header (recording options), not an action. The converter skips it.

## R3. Mapping recorder locators to targets

**Decision**: Map these locator `kind` values. Chains, frames, `has`/`and`/`or` filters and
other kinds are unsupported in v1.

| Locator `kind` | Target | Playwright .NET call at replay |
|---|---|---|
| `role` (+ `options.name`, `options.exact`) | `{ "role", "name", "exact" }` | `Page.GetByRole(...)` |
| `test-id` | `{ "testId" }` | `Page.GetByTestId(...)` |
| `label` | `{ "label" }` | `Page.GetByLabel(...)` |
| `placeholder` | `{ "placeholder" }` | `Page.GetByPlaceholder(...)` |
| `text` | `{ "text" }` | `Page.GetByText(...)` |
| `alt` | `{ "altText" }` | `Page.GetByAltText(...)` |
| `title` | `{ "title" }` | `Page.GetByTitle(...)` |
| `default` (CSS) | `{ "css" }` | `Page.Locator(...)`; validation warning (FR-017) |
| `nth` / `first` / `last` as `next` | `"nth": n` (first = 0, last = -1) | `.Nth(n)` / `.Last` |

The recorder already prefers role, test ID and label locators, which matches constitution VIII.
**Spike T007 confirms the exact `kind`, `body` and `options` values** against real output
before the converter is written.

## R4. Variables and secrets

**Decision**: Placeholders inside string values: `{{var:NAME}}` and `{{secret:NAME}}`, resolved at
run time from the environment variables `VERIFY_VAR_<NAME>` and `VERIFY_SECRET_<NAME>`. The file
declares the names it uses (`variables`, `secrets`) so missing values are caught before a
browser starts (FR-013). Secret values are masked in all output.

**Rationale**: Environment variables work the same locally and in every CI system, and the
pipeline's secret store can supply them.

**Alternatives**: A local secrets file (rejected: easy to commit by mistake). Direct key vault
integration (deferred: depends on the real pipeline, which is in PROJECT-CONTEXT).

## R5. Detecting passwords at record time

**Decision**: JSONL `fill` actions don't include the input's type. The converter treats a
`fill` as a secret when its target's name, label or placeholder matches
`password|passcode|pin|secret|token` (case-insensitive). It then replaces the value with
`{{secret:<NAME>}}` (the name derived from the label, e.g. `PASSWORD`) and tells the developer.
The temporary JSONL file is deleted after conversion. Validation (FR-016) adds a second check
for literal values that look like secrets.

**Rationale**: It covers standard sign-in forms with no extra developer effort. Its limit (a
password field with an unusual label) is caught by the developer's prompt review and by PR
review of the file.

**Alternative**: Query the field's `type` attribute during recording. Rejected: the recorder
runs in its own process, and we can't hook into it without a custom recorder (R1).

## R6. Sign-in with SSO

**Decision**: Optionally start each run from a saved, signed-in browser session: Playwright
**storage state**, a JSON file path given in `VERIFY_STORAGE_STATE`. Producing that file
(e.g. a pipeline sign-in step) is environment-specific and stays out of v1 scope.
Username/password sign-in is just recorded steps with a secret.

## R7. Restricting navigation to the environment (FR-014)

**Decision**: Route document requests through `Context.RouteAsync`. Abort any top-level document
request whose host isn't the environment's host or in its `allowedHosts` list (needed for SSO
identity providers). An aborted navigation fails the step with "navigation to <host> blocked".

## R8. Replay engine and assertions

**Decision**: Use `Microsoft.Playwright` for .NET with Playwright's web-first assertions
(`Assertions.Expect(...)`: `ToHaveTextAsync`, `ToContainTextAsync`, `ToHaveValueAsync`,
`ToBeCheckedAsync`, `ToBeVisibleAsync`, `ToBeHiddenAsync`, and `Expect(page).ToHaveURLAsync`) with
the per-step timeout. Each file runs in a fresh browser context with tracing on. On failure:
screenshot plus `trace.zip`.

**Rationale**: The assertions auto-wait (FR-009), and Playwright's strict mode already fails
when a locator matches several elements (edge case).

## R9. Pipeline report format

**Decision**: JUnit XML (one `testsuite` per run, one `testcase` per file, failure message =
failed step), written by our own small writer. GitHub Actions, Azure DevOps and Jenkins all
read JUnit XML.

## R10. Library choices

| Need | Decision | Note |
|---|---|---|
| CLI parsing | `System.CommandLine` | Constitution default; pin the version |
| JSON Schema validation | `JsonSchema.Net` | Validates against the same schema file we publish |
| Tests | xUnit with plain `Assert` | FluentAssertions v8+ requires a commercial licence; the constitution allows plain asserts |
| Local test target | Static HTML pages served by an in-test ASP.NET Core host | Constitution III: tests never use a shared environment |
