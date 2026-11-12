# Feature Specification: Story Verification Recordings

**Feature Branch**: `001-story-verification-recordings`

**Created**: 2026-11-12

**Status**: Approved (G2): *reference example*

**Input**: User description: "Build Story Verification Recordings as described in docs/demo/feature-brief.md, for the target application, environment and JSON format requirements in docs/poc/PROJECT-CONTEXT.md. When a developer finishes a user story or defect fix, they record what they expect to happen with the Playwright recorder, marking expected outcomes with its assertion tools. The recording becomes a readable JSON verification file linked to the story or defect ID and stored with the code change so it is reviewed in the same pull request. An automated runner replays the file against the environment that has the developer's code and checks every expected outcome, reporting pass/fail per step with evidence (expected vs found, screenshot on failure), and can gate a pipeline."

## Clarifications

### Session 2026-11-12

- Q: How does the runner sign in to the environment? → A: Credentials are never stored in the file. A typed password is replaced with a named secret reference at record time, and the secret's value is supplied at run time. For SSO, the runner can start from a saved, signed-in browser session supplied at run time. **(assumed)**
- Q: How is test data handled when a recording depends on data that only exists on the developer's machine? → A: Values that differ between environments are stored as named variables and supplied at run time. Creating or seeding data is out of scope for v1. **(assumed)**
- Q: Can one story have several verification files? Can files be hand-edited? → A: Yes to both. One file holds one scenario. A story or defect can have several files. Files are meant to be readable and hand-editable, and are validated before every run.
- Q: How is the target environment chosen? → A: By environment name (for example `qa`), mapped to a base URL in settings, or by an explicit base URL. Files hold only paths relative to the base URL. **(assumed)**
- Q: How does Playwright recorder output become the JSON file? → A: The recorder runs in its JSONL output mode, and the tool converts that output into the verification file format (see `research.md`).
- Q: What happens to verification files after release? → A: Out of scope for v1. They stay in the repository with the code.
- Q: Which browsers must pass? → A: Chromium is required. Firefox and WebKit can be selected per run. **(assumed)**
- Q: How are timing and flaky steps handled? → A: Each step waits for its target automatically, up to a per-step timeout (default 10 seconds). There are no automatic retries in v1, so a failure is reported as a failure.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Replay a verification file against an environment (Priority: P1)

A developer or a pipeline runs an existing verification file against a chosen environment. Each
step is replayed in a real browser, and every expected outcome is checked. The run reports
pass/fail per step, keeps evidence for failures, and ends with an exit status a pipeline can use.

**Why this priority**: Replay is the core value: it proves behaviour in the environment that has
the change. It also works with hand-written files, so it can be delivered and used before
recording exists.

**Independent Test**: Hand-write a verification file for a local sample page, run it, and see a
pass. Change an expected value, run it again, and see a failed step with evidence.

**Acceptance Scenarios**:

1. **Given** a valid verification file whose expectations match the application, **When** it is run against an environment, **Then** every step is reported as passed and the run exits successfully.
2. **Given** a verification file where one expected text doesn't match the page, **When** it is run, **Then** that step is reported as failed with the expected and found values, a screenshot and a trace are saved, later steps are reported as skipped, and the run exits with a failure status.
3. **Given** a verification file that references a secret or variable, **When** it is run with that value supplied, **Then** the value is used, and it never appears in output, logs or reports.
4. **Given** a verification file that references a secret or variable, **When** it is run without that value supplied, **Then** the run stops before opening a browser and names the missing value.
5. **Given** an environment name, **When** a run starts, **Then** the base URL comes from settings for that name, and every path in the file is resolved against it.

---

### User Story 2 - Record a verification with the Playwright recorder (Priority: P2)

As the last step of a story or defect, a developer starts a recording session for a work item
ID. The Playwright recorder opens on their locally running application. They walk through the
scenario and use the recorder's assertion tools to mark what they expect to see. When they
close the recorder, a verification file is written, ready to commit.

**Why this priority**: Recording is what makes verifications quick to create, but it depends on
the file format and runner from User Story 1 to be useful.

**Independent Test**: Record a short scenario on the local sample page (navigate, fill, click,
assert text), then run the resulting file with User Story 1 and see it pass without edits.

**Acceptance Scenarios**:

1. **Given** a work item ID and a starting URL, **When** the developer records a scenario with at least one assertion and closes the recorder, **Then** a verification file is written to the agreed location, linked to that work item, and passes validation.
2. **Given** the developer typed a password during recording, **When** the file is written, **Then** the typed value is replaced with a named secret reference, and the developer is told which secret name to supply at run time.
3. **Given** a recording with no assertions, **When** the recorder is closed, **Then** no file is written, and the developer is told that at least one expected outcome is required.
4. **Given** the recorder produced an action or locator the format doesn't support, **When** the file is written, **Then** the developer gets a warning naming each unsupported step, and the file is only written if the developer confirms.
5. **Given** a recording made against `http://localhost:5000`, **When** the file is written, **Then** it contains only paths (for example `/cart`), not the local host.

---

### User Story 3 - Validate verification files in a pull request (Priority: P3)

A reviewer or CI checks that every verification file in a change is well-formed: it matches the
schema, it is linked to a valid work item ID, it contains no secrets or absolute URLs, and its
locators follow the preferred order. No browser is needed.

**Why this priority**: It keeps files reviewable and safe before they are ever replayed, but
replay and recording deliver more value first.

**Independent Test**: Run validation on a folder containing one valid file, one file with a
hard-coded password, and one file with a missing work item ID. Exactly the two bad files are
reported, each with the reason.

**Acceptance Scenarios**:

1. **Given** a folder of verification files, **When** validation runs, **Then** each invalid file is reported with its path, the step (if any) and the reason, and the command exits with a failure status if any file is invalid.
2. **Given** a file containing a literal value that matches a known secret pattern or an absolute URL, **When** validation runs, **Then** the file is rejected.
3. **Given** a file that uses a CSS locator where a role, label or test ID was possible, **When** validation runs, **Then** a warning is reported, but the file is not rejected.

---

### User Story 4 - Gate a pipeline on verification results (Priority: P3)

After a change is deployed to an environment, the pipeline runs all verification files for the
change against that environment. The pipeline fails if any verification fails, and the results
appear in the pipeline's standard test report.

**Why this priority**: This closes the loop (gate G6), but it is configuration on top of User
Stories 1 and 3.

**Independent Test**: In a pipeline, run a folder with one passing and one failing file. The
pipeline step fails, and the test report shows one pass and one failure with its evidence
attached.

**Acceptance Scenarios**:

1. **Given** a folder of verification files, **When** they are run in the pipeline, **Then** a standard test report (one test case per file, one failure message per failed step) is produced, along with failure evidence.
2. **Given** all files pass, **When** the run finishes, **Then** the pipeline step succeeds.
3. **Given** a run is limited to a work item ID, **When** it runs, **Then** only files linked to that work item are executed.

### Edge Cases

- The environment is unreachable or returns an error page: the run fails at the first step with a clear "environment unreachable" message, not as an assertion failure.
- A step's target never appears: the step fails after its timeout and reports which locator wasn't found.
- A locator matches more than one element: the step fails, says how many elements matched, and suggests a more specific locator.
- The recorder session is closed before any action: nothing is written, and the developer gets a message.
- A file has a newer major schema version than the tool supports: validation fails and names the supported version.
- The recording opens a second tab or a pop-up: v1 rejects it at conversion with an "unsupported: multiple pages" warning.
- A file is run against an environment where the user is already signed in (shared session): sign-in steps may behave differently. Runs always start from a fresh browser context unless a saved session is explicitly supplied.

## Requirements *(mandatory)*

### Functional Requirements

**Verification file**

- **FR-001**: A verification file MUST describe one scenario as an ordered list of steps, where each step is either an action or an expected outcome.
- **FR-002**: A verification file MUST include a format version, a unique ID, the linked work item (ID, type: story or defect, and title), a scenario title, the author and the recording date.
- **FR-003**: A verification file MUST contain no credentials, no environment-specific host names, and no absolute URLs. Values that vary MUST be named variable or secret references.
- **FR-004**: Element targets MUST be described by role and accessible name, label, placeholder, test ID, text, alt text or title. A CSS selector MAY be used only as a last resort.
- **FR-005**: The format MUST be published as a machine-readable schema kept in the repository, and MUST be readable and editable by a person.

**Replay**

- **FR-006**: Users MUST be able to run one file, or every file in a folder, against an environment selected by name or by base URL.
- **FR-007**: The runner MUST validate each file (FR-016) before running it, and MUST NOT run an invalid file.
- **FR-008**: The runner MUST check each expected outcome: text shown (exact or contains), field value, checked state, element visible, element hidden, and current page path.
- **FR-009**: The runner MUST wait for each step's target up to a configurable per-step timeout (default 10 seconds).
- **FR-010**: On a failed step, the runner MUST record the step, the expected value, the found value, a screenshot and a browser trace. The remaining steps of that file MUST be reported as skipped.
- **FR-011**: The runner MUST report pass/fail/skipped per step and per file on the console, and MUST write a standard test report that pipelines can read.
- **FR-012**: The runner MUST exit with a success status only if every file passed.
- **FR-013**: The runner MUST resolve variables and secrets from the run-time environment, MUST stop before starting a browser if any are missing, and MUST NOT print secret values anywhere.
- **FR-014**: The runner MUST only navigate to the selected environment's host. Navigation to any other host MUST fail the step.
- **FR-015**: The runner MUST support Chromium, and MUST allow Firefox or WebKit to be selected per run.

**Validation**

- **FR-016**: Users MUST be able to validate one file or a folder without a browser. Validation MUST check the schema, the work item ID pattern, that there are no absolute URLs, and that there are no literal values that look like secrets.
- **FR-017**: Validation MUST warn, without failing, when a CSS locator is used.

**Recording**

- **FR-018**: Users MUST be able to start a recording for a work item ID and a starting URL, which opens the Playwright recorder.
- **FR-019**: When the recorder is closed, the recording MUST be converted into a verification file. The start URL's host is removed, so steps hold paths only.
- **FR-020**: Values typed into password fields MUST be replaced with a named secret reference before the file is written.
- **FR-021**: A recording without at least one expected outcome MUST NOT be saved.
- **FR-022**: Unsupported recorded actions or locators MUST be listed to the developer, and the file is only written if they confirm.
- **FR-023**: Files MUST be saved under a configurable folder (default `verifications/<work item ID>/`), with a file name derived from the scenario title.

**Pipeline**

- **FR-024**: Users MUST be able to limit a run to files linked to a given work item ID.
- **FR-025**: The project MUST include an example pipeline step that runs verifications against an environment and publishes the report and evidence.

### Key Entities

- **Verification File**: One scenario for one work item. Holds the metadata (FR-002), the declared variables and secret names, and the ordered steps.
- **Step**: One action (navigate, click, fill, press, check, uncheck, select) or one expected outcome (text, value, checked, visible, hidden, path). Has a target where relevant.
- **Target**: How an element is found: role and name, label, placeholder, test ID, text, alt text, title, or (last resort) CSS, plus an optional position when several elements match.
- **Run Settings**: The environment name or base URL, the browser, the timeout, and where secrets and variables come from. Never stored in the file.
- **Run Result**: The per-file and per-step outcome, with timings and failure evidence.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A developer can record a typical story's verification (5–15 steps, at least 1 expected outcome) in under 5 minutes, including writing the file.
- **SC-002**: At least 90% of verifications recorded in the POC replay against the target environment with no manual edits.
- **SC-003**: A reviewer can state what a verification checks, from the file alone, in under 1 minute (checked during the POC review).
- **SC-004**: 100% of failed runs include the failed step, expected and found values, and a screenshot.
- **SC-005**: Zero secrets appear in committed verification files, console output or reports (checked by validation and by a review of POC outputs).
- **SC-006**: Validating 100 files takes under 5 seconds on a developer machine.

## Assumptions

- Values marked **(assumed)** come from the reference assumptions in `docs/reference-example/README.md`. A real run takes them from `docs/poc/PROJECT-CONTEXT.md`.
- The target application is a browser-based web app reachable from developer machines and from the pipeline.
- Developers can run the application locally to record against it.
- Each environment has test accounts and data suitable for verification. v1 doesn't create data.
- Mobile apps, API-only checks, performance testing, visual (pixel) comparison and a hosted dashboard are out of scope (feature brief).
