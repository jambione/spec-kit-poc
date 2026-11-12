# CLI Contract: `storyverify`

Installed as a .NET tool (`dotnet tool install`). Every command writes structured logs to
stderr and results to stdout.

## `storyverify record`

Opens the Playwright recorder on the running application. When the recorder closes, writes a
verification file.

| Option | Required | Description |
|---|---|---|
| `--work-item <ID>` | ✅ | e.g. `PROJ-123`; must match `workItemPattern` |
| `--type <story\|defect>` | ✅ | |
| `--title <text>` | ✅ | Scenario title; also used for the file name |
| `--url <url>` | ✅ | Starting URL on the local app, e.g. `http://localhost:5000/cart` |
| `--work-item-title <text>` | | Defaults to `--title` |
| `--author <name>` | | Defaults to `git config user.name` |
| `--browser <chromium\|firefox\|webkit>` | | Default `chromium` |
| `--yes` | | Accept unsupported-step warnings without prompting |

Behaviour (FR-018 to FR-023):
1. Runs the recorder: `codegen --target jsonl --output <temp file> <url>`.
2. Converts the output. The URL's host is removed, passwords become `{{secret:…}}`, and
   unsupported steps are listed.
3. Refuses to save if there's no expected-outcome step.
4. Writes `verifications/<ID>/<slug>.verify.json`, validates it, and prints the path plus any
   secret names to supply at run time.
5. Deletes the temp file.

## `storyverify run [paths...]`

Validates and replays files. `paths` can be files or folders (default: `verificationsPath`).

| Option | Description |
|---|---|
| `--env <name>` | Environment from `storyverify.json` |
| `--base-url <url>` | Overrides the environment's base URL (or `VERIFY_BASE_URL`) |
| `--work-item <ID>` | Only run files linked to this work item (FR-024) |
| `--browser <chromium\|firefox\|webkit>` | Default `chromium` |
| `--timeout <ms>` | Per-step timeout; default `10000` |
| `--headed` | Show the browser (local debugging) |
| `--output <dir>` | Results folder; default `verify-results/` |

Exactly one of `--env` or `--base-url`/`VERIFY_BASE_URL` is required.

Output in `--output`:
- `junit.xml`: one `testcase` per file
- `<file-id>/screenshot.png` and `<file-id>/trace.zip` for each failed file
- `summary.json`: the RunResult (data-model.md)

## `storyverify validate [paths...]`

Checks files without a browser (FR-016, FR-017). Prints `ERROR` and `WARN` lines with the file
path and step number.

## Exit codes

| Code | Meaning |
|---|---|
| `0` | Success: all files valid / all passed / recording saved |
| `1` | At least one verification failed (run) |
| `2` | At least one file invalid (validate, run) |
| `3` | Configuration error: missing environment, base URL, variable or secret; unsupported schema version |
| `4` | Environment unreachable |
| `5` | Recording not saved (no expectation, cancelled, conversion error) |

## Environment variables

| Variable | Purpose |
|---|---|
| `VERIFY_BASE_URL` | Base URL when `--env` isn't used |
| `VERIFY_VAR_<NAME>` | Value for `{{var:NAME}}` |
| `VERIFY_SECRET_<NAME>` | Value for `{{secret:NAME}}` (masked in all output) |
| `VERIFY_STORAGE_STATE` | Path to a Playwright storage state file (signed-in session) |

## `storyverify.json` (settings, committed)

```json
{
  "verificationsPath": "verifications",
  "workItemPattern": "^[A-Z][A-Z0-9]+-\\d+$",
  "defaultTimeoutMs": 10000,
  "environments": {
    "dev":     { "baseUrl": "https://dev.example.internal" },
    "qa":      { "baseUrl": "https://qa.example.internal", "allowedHosts": ["login.example-idp.com"] },
    "staging": { "baseUrl": "https://staging.example.internal" }
  }
}
```
*(Host names are placeholders. Real values come from PROJECT-CONTEXT §2.)*
