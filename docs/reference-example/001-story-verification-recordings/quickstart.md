# Quickstart: validate Story Verification Recordings end to end

Run these after `/speckit-implement` to prove each user story works. Commands assume the repo
root, and that the tool is run from source (`dotnet run --project src/StoryVerify.Cli --`)
as `storyverify`.

## 0. Build and install browsers

```bash
dotnet build
dotnet test
pwsh src/StoryVerify.Cli/bin/Debug/net8.0/playwright.ps1 install chromium
```

`dotnet test` starts the sample site itself. It must pass with no network access to any shared
environment (constitution III).

## 1. Validate (User Story 3)

```bash
storyverify validate docs/reference-example/001-story-verification-recordings/contracts/example.verify.json
```
Expected: exit code `0`, no errors.

```bash
storyverify validate tests/StoryVerify.Core.UnitTests/Fixtures/invalid/
```
Expected: exit code `2`, one `ERROR` line per invalid fixture, each naming the reason.

## 2. Replay (User Story 1)

Start the sample site (the integration tests use the same pages):

```bash
dotnet run --project tests/StoryVerify.Cli.IntegrationTests -- --serve-sample-site --urls http://localhost:5055
```

In a second terminal:

```bash
export VERIFY_SECRET_PASSWORD='sample-password'
storyverify run verifications/PROJ-123 --base-url http://localhost:5055
```
Expected: every step `PASSED`, exit code `0`, `verify-results/junit.xml` written.

**Failure path:** change an expected `text` in `verifications/PROJ-123/sample-login.verify.json`
and run again. Expected: that step `FAILED` showing expected vs found, later steps `SKIPPED`,
exit code `1`, and a screenshot and `trace.zip` under `verify-results/<file-id>/`.

**Missing secret:** `unset VERIFY_SECRET_PASSWORD` and run again. Expected: exit code `3`, the
message names `PASSWORD`, and no browser is started.

## 3. Record (User Story 2): needs a desktop session

```bash
storyverify record --work-item PROJ-200 --type story --title "Sign in shows the account page" --url http://localhost:5055/login
```
In the recorder:
1. Fill in the email and password, then click **Sign in**.
2. Use **Assert text** on the account heading.
3. Close the recorder.

Expected:
- The file is written to `verifications/PROJ-200/sign-in-shows-the-account-page.verify.json`.
- The password value in it is `{{secret:PASSWORD}}`.
- The paths have no `localhost`.
- The console says to supply `VERIFY_SECRET_PASSWORD`.

Then replay it with step 2's `run` command: it passes with no edits (SC-002).

**No assertion:** record again without any assertion. Expected: exit code `5` and nothing written.

## 4. Pipeline gate (User Story 4)

Push a branch that changes a file under `verifications/`. The `verify` workflow:
- validates all files
- runs them against the sample site in CI (or the configured environment)
- publishes `junit.xml` and the evidence as artifacts
- fails if any verification fails
