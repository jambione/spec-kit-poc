# Project Context: fill in before `/speckit-specify`

> **Why this file exists:** the POC tooling is generic. The real details (which application,
> which environment, what the JSON looks like) belong to *your* project, and they feed the
> Spec Kit steps. Copilot reads this file during specify, clarify and plan.
>
> **How to fill it in:** replace every `TODO:` with your answer. If you don't know yet, write
> `OPEN: <your best guess or question>`. Copilot turns `OPEN:` items into clarification
> questions instead of guessing. Check readiness with:
>
> ```bash
> bash scripts/check-context.sh
> ```
>
> This file is part of gate **G1 (Intent)**: the brief plus this context, approved by the PO and
> Tech Lead.

**Never put secrets here** (passwords, tokens, connection strings). Name the secret and where it
lives instead, for example "QA login password: pipeline secret `QA_USER_PASSWORD`".

---

## Decided

| Decision | Value | Notes |
|---|---|---|
| Recording tool | **Playwright recorder** (`codegen`) | The developer records actions and expected outcomes (the recorder's assert tools) in the browser. |
| AI coding agent | GitHub Copilot (agent mode) | |
| Team stack | .NET | |

---

## 1. Target application (the repository under test)

The application whose stories and defects get verification files.

| Item | Answer |
|---|---|
| Repository URL / name | TODO: |
| What the application is (one line) | TODO: |
| Front-end technology (e.g. Blazor, Razor Pages, MVC, Angular, React) | TODO: |
| How a developer runs it locally (command + URL) | TODO: |
| Does the UI use stable test hooks (`data-testid`, ARIA roles/labels)? | TODO: |
| Where verification files should live (in the app repo? path?) | TODO: |
| Where the tool itself should live (this POC repo, the app repo, a shared repo) | TODO: |
| Work item system and ID format (e.g. Azure Boards `AB#1234`, Jira `PROJ-123`, GitHub `#123`) | TODO: |
| A good pilot story or defect to record first | TODO: |

## 2. Environment under test

Where the runner replays verification files after the developer's code is deployed.

| Item | Answer |
|---|---|
| Environment name(s) (e.g. dev, QA, staging) | TODO: |
| Base URL per environment (or the variable that holds it) | TODO: |
| How a change reaches the environment (pipeline, schedule, manual) | TODO: |
| How the runner knows which environment has the developer's code (branch → env mapping, PR env, etc.) | TODO: |
| Sign-in method (none, username/password, SSO/Entra ID, MFA) | TODO: |
| Test account(s) and where their credentials are stored (name only) | TODO: |
| Test data: shared, seeded per run, or created by the recording itself? | TODO: |
| Network access from the pipeline to the environment (public, VPN, self-hosted agent) | TODO: |
| Browsers that must pass (Chromium, Firefox, WebKit/Edge) | TODO: |

## 3. Existing Playwright and pipeline setup

| Item | Answer |
|---|---|
| Is there an existing Playwright suite? Language (.NET / TypeScript)? Repo? | TODO: |
| Should the runner plug into it, or stand alone? | TODO: |
| CI/CD system (GitHub Actions, Azure DevOps, Jenkins, …) | TODO: |
| Where results should show up (PR check, pipeline report, work item comment) | TODO: |
| Runner language (default: .NET via `Microsoft.Playwright`) | TODO: |

## 4. JSON verification file format

The format your team wants to keep. Describe the **requirements**; the exact schema is
designed during `/speckit-plan` (it goes in `specs/<feature>/contracts/`).

| Item | Answer |
|---|---|
| Required metadata (e.g. story/defect ID, title, author, date, app version) | TODO: |
| Step types needed (navigate, click, fill, select, check, upload, wait, …) | TODO: |
| Expected-outcome (assertion) types needed (text visible, value equals, URL, element visible/hidden, count, …) | TODO: |
| Locator preference (role/label/test ID first; CSS/XPath allowed?) | TODO: |
| Variables / placeholders (base URL, test data, secrets referenced by name) | TODO: |
| Must people be able to hand-edit the JSON after recording? | TODO: |
| One file per story, or several scenarios per file? | TODO: |
| Must it convert from Playwright recorder output, or does the recorder write it directly? | TODO: |
| Any existing format or example to match (paste or link below) | TODO: |

### Example (optional)

Paste an example of the JSON you have in mind, even a rough one. Leave it empty if you want
Copilot to propose one during planning.

```json
TODO: optional example, or delete this block
```

## 5. People (for the gates)

| Role | Name |
|---|---|
| Product Owner (G1, G2) | TODO: |
| Tech Lead / Architect (G2, G3, G4) | TODO: |
| Developer(s) | TODO: |
| QA | TODO: |
| Reviewer (G5) | TODO: |
