# Data Model: Story Verification Recordings

**Plan**: [plan.md](plan.md) | **Schema**: [contracts/verification-file.schema.json](contracts/verification-file.schema.json)

## VerificationFile

One scenario for one work item. Stored as `verifications/<workItem.id>/<slug>.verify.json`.

| Field | Type | Required | Rules |
|---|---|---|---|
| `schemaVersion` | string | ✅ | `"1.0"`. The major version must be supported by the tool |
| `id` | string | ✅ | Unique in the repo; lowercase `a-z0-9-`, e.g. `proj-123-apply-discount` |
| `title` | string | ✅ | 5–120 characters; the scenario in plain language |
| `workItem` | WorkItem | ✅ | See below |
| `author` | string | ✅ | Who recorded it (name or handle) |
| `recordedAt` | string | ✅ | ISO 8601 date-time |
| `description` | string | | Optional notes for reviewers |
| `variables` | string[] | | Names used as `{{var:NAME}}`; `UPPER_SNAKE_CASE` |
| `secrets` | string[] | | Names used as `{{secret:NAME}}`; `UPPER_SNAKE_CASE` |
| `steps` | Step[] | ✅ | 1–200 steps; at least one expected-outcome step (FR-021) |

**Rules across fields**
- Every `{{var:X}}` / `{{secret:X}}` used in a step must be declared, and every declared name must
  be used.
- No string may contain `://` (absolute URL) (FR-003).
- No literal value may look like a secret, e.g. `password=…` or a long random token (FR-016).

## WorkItem

| Field | Type | Required | Rules |
|---|---|---|---|
| `id` | string | ✅ | Must match `workItemPattern` in `storyverify.json` (default `^[A-Z][A-Z0-9]+-\d+$`) |
| `type` | `"story"` \| `"defect"` | ✅ | |
| `title` | string | ✅ | The work item's title |

## Step

A single action or expected outcome. Exactly one `action` per step.

| `action` | Kind | Required fields | Optional |
|---|---|---|---|
| `navigate` | action | `path` (starts with `/`) | |
| `click` | action | `target` | |
| `dblclick` | action | `target` | |
| `fill` | action | `target`, `value` | |
| `press` | action | `target`, `key` | |
| `check` / `uncheck` | action | `target` | |
| `select` | action | `target`, `options` (string[]) | |
| `expectText` | expected outcome | `target`, `text` | `match`: `exact` (default) \| `contains` |
| `expectValue` | expected outcome | `target`, `value` | |
| `expectChecked` | expected outcome | `target`, `checked` (bool) | |
| `expectVisible` | expected outcome | `target` | |
| `expectHidden` | expected outcome | `target` | |
| `expectPath` | expected outcome | `path` | `match`: `exact` (default) \| `startsWith` |

All steps can also have `note` (a reviewer comment) and `timeoutMs` (overrides the default).

## Target

How an element is found. Exactly one locator field, plus an optional `nth`.

| Field | Meaning | Preference |
|---|---|---|
| `role` + `name` (+ `exact`) | ARIA role and accessible name | 1 (best) |
| `label` | Associated label text | 1 |
| `testId` | `data-testid` (or configured attribute) | 1 |
| `placeholder` | Input placeholder | 2 |
| `text` | Visible text | 2 |
| `altText` | Image alt text | 2 |
| `title` | `title` attribute | 2 |
| `css` | CSS selector | 3 (last resort; validation warning) |
| `nth` | 0-based position when several match; `-1` = last | |

## RunSettings (never stored in a verification file)

Loaded from `storyverify.json`, then environment variables, then CLI options (later sources
override earlier ones).

| Setting | Source | Default |
|---|---|---|
| `environments.<name>.baseUrl` | settings file | none |
| `environments.<name>.allowedHosts` | settings file | `[]` (the base URL's host is always allowed) |
| Base URL override | `VERIFY_BASE_URL` / `--base-url` | none |
| Browser | `--browser` | `chromium` |
| Step timeout | `defaultTimeoutMs` / `--timeout` | `10000` |
| Verifications folder | `verificationsPath` | `verifications` |
| Work item pattern | `workItemPattern` | `^[A-Z][A-Z0-9]+-\d+$` |
| Storage state (SSO) | `VERIFY_STORAGE_STATE` | none |
| Variables / secrets | `VERIFY_VAR_<NAME>` / `VERIFY_SECRET_<NAME>` | none |

## RunResult

```
RunResult
├── environment, baseUrl, browser, startedAt, duration
└── files[]: FileResult
    ├── path, id, workItemId, status (passed | failed | invalid), duration
    ├── evidence: screenshotPath?, tracePath?
    └── steps[]: StepResult
        └── index, action, status (passed | failed | skipped), duration,
            expected?, found?, message?
```

## State transitions

```
File:  discovered → validated ─┬─ invalid  (not run; reported)
                               └─ running → passed | failed
Step:  pending → running → passed | failed
       pending → skipped  (an earlier step in the same file failed)
```
