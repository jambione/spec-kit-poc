# Team Session: AI-DLC with Spec Kit

**Agenda and speaker script for introducing the team to the AI-Driven Development Lifecycle
(AI-DLC) and GitHub Spec Kit, using our POC project as the example.**

| | |
|---|---|
| Length | 60 minutes (a 30-minute version is at the end) |
| Audience | Developers, QA, Product Owner, Tech Lead |
| Format | Talk + live demo in VS Code with GitHub Copilot |
| Goal | The team understands the lifecycle, has seen it work on our project, and agrees to run the POC |
| Slides | [`AI-DLC-Spec-Kit-Team-Session.pptx`](AI-DLC-Spec-Kit-Team-Session.pptx): 25 slides with speaker notes, following this script |

---

## 1. Meeting invite (copy and paste)

> **Subject:** AI-DLC + Spec Kit: how we could build software with AI (60 min)
>
> We're running a proof of concept of an **AI-Driven Development Lifecycle**: GitHub Copilot
> drafts the spec, plan, tasks and code, and we review and approve each step. The tool doing the
> structure is **GitHub Spec Kit**.
>
> The POC project is **Story Verification Recordings**: when you finish a story or defect, you
> record what you expect to happen with the Playwright recorder, it's saved as a JSON file, and a
> Playwright runner replays it against the environment that has your code.
>
> **Agenda**
> 1. Why we're looking at this (5 min)
> 2. AI-DLC: the lifecycle (10 min)
> 3. Spec Kit: the tool (10 min)
> 4. How they fit together for us (5 min)
> 5. Live demo on the POC project (20 min)
> 6. POC plan, what we'll measure, what we need from you (5 min)
> 7. Questions (5 min)
>
> No preparation needed. If you want a head start, skim `docs/ai-dlc/AI-DLC.md` in the
> `spec-kit-poc` repo.

---

## 2. Agenda at a glance

| Time | Segment | Show on screen | Goal |
|---|---|---|---|
| 0:00 | **1. Why we're here** | This file, section 4.1 | Agree on the problem |
| 0:05 | **2. What AI-DLC is** | `docs/ai-dlc/AI-DLC.md` §1–3 | Understand phases, gates, roles |
| 0:15 | **3. What Spec Kit is** | `.github/skills/`, `.specify/` | Understand commands and outputs |
| 0:25 | **4. How they fit for us** | `AI-DLC.md` §2 table, constitution, PR template | See where gates live |
| 0:30 | **5. Live demo** | VS Code + Copilot Chat ([DEMO-SCRIPT.md](../demo/DEMO-SCRIPT.md)) | See it work on our project |
| 0:50 | **6. POC plan and asks** | `docs/poc/POC-PLAN.md` | Agree next steps and owners |
| 0:55 | **7. Q&A** | Section 6 below | Address concerns |

---

## 3. Before the session (presenter checklist)

**The day before**
- [ ] `docs/poc/PROJECT-CONTEXT.md` filled in; `bash scripts/check-context.sh` passes.
- [ ] Full dry run of [DEMO-SCRIPT.md](../demo/DEMO-SCRIPT.md) steps 3–5 on a `dry-run/…` branch.
      **Keep that branch.** It's your fallback if Copilot is slow live.
- [ ] Optional: screen-record the `/speckit-implement` step from the dry run (it can take several
      minutes).
- [ ] Note 2–3 metrics from the dry run (time per step, number of clarification questions,
      tasks generated) to quote in segment 6.

**30 minutes before**
- [ ] VS Code open on the repo, on `main` (or the POC branch). Font size up (Ctrl/Cmd +).
- [ ] Copilot Chat open in **Agent** mode; type `/speckit` to confirm the commands appear.
- [ ] Tabs open: `AI-DLC.md`, `constitution.md`, `feature-brief.md`, `PROJECT-CONTEXT.md`,
      `pull_request_template.md`, this file.
- [ ] The demo prompts from DEMO-SCRIPT.md ready to paste (copy them into a scratch file).
- [ ] Notifications off.

---

## 4. Speaker script

Each segment has **Show** (what's on screen), **Say** (suggested words; adapt freely) and
**Transition** (the line into the next segment).

### 4.1 Why we're here (0:00–0:05)

**Show:** this section, or just your face.

**Say:**
> "Most of us already use Copilot for autocomplete and quick questions. What we don't have is a
> *way of working* with AI: who decides what gets built, how we check what the AI produced, and
> how we know later why something was built the way it was.
>
> Today I'll show you two things. First, **AI-DLC**, an AI-Driven Development Lifecycle. It's our
> normal lifecycle, rearranged so AI does the first draft of everything and people approve it at
> fixed checkpoints. Second, **Spec Kit**, an open-source tool from GitHub that turns that
> lifecycle into commands in Copilot Chat.
>
> And I'll show it on a real project we need: **Story Verification Recordings**."

Then describe the POC project in two sentences:
> "When you finish a story or defect, you record what you expect to happen with the Playwright
> recorder. That becomes a JSON file in your PR, and a Playwright runner replays it against the
> environment that has your code, so 'it works on my machine' becomes 'it's proven in QA'."

Ask the room (30 seconds):
> "Quick show of hands: who's had a story bounce back from QA for something you thought you'd
> tested?"

**Transition:** "So, first, the lifecycle."

---

### 4.2 What AI-DLC is (0:05–0:15)

**Show:** `docs/ai-dlc/AI-DLC.md`, section 1, then the diagram in section 2.

**Say:**
> "The one-line version is: **AI drafts, humans decide.**
>
> There are three phases, which you'll recognise.
> - **Inception** is the *what and why*. Copilot drafts the requirements from a short brief. Then
>   it lists what's unclear, and the PO answers.
> - **Construction** is the *how*. Copilot drafts the design, breaks it into tasks, writes the
>   tests first and then the code.
> - **Operations** is *ship and run*: our normal pipeline.
>
> Between every step there's a **gate**: a named person approves before the next step starts.
> In practice a gate is just a pull request review. Nothing exotic."

Walk through the gates table quickly (point at each):
> "G1: the PO approves the intent. G2: the PO and Tech Lead approve the spec. G3: the architect
> approves the plan. G4: the TL approves the task list. G5: normal code review plus CI. G6:
> release."

**Show:** section 3 (Roles).
> "Note the last row: Copilot drafts everything and **approves nothing**. You're the author of
> record for anything you approve."

**Show:** section 5 (Paths by change size).
> "And it scales down. A bug fix doesn't need a spec; it needs the issue, a fix and a
> regression test. We're not adding paperwork to a one-line change."

**Key message to land:** the gates move the arguments to *before* the code is written, when
they're cheap.

**Transition:** "That's the process. Spec Kit is what makes it repeatable instead of a wiki page
nobody reads."

---

### 4.3 What Spec Kit is (0:15–0:25)

**Show:** Copilot Chat; type `/speckit` and let the list appear.

**Say:**
> "Spec Kit is a free, open-source toolkit from GitHub. It installs into the repo as a set of
> **commands** for Copilot, plus **templates** and a few helper scripts. There's no server and no
> extra licence; it runs on the Copilot we already have."

Walk the commands in order (have this list visible, or point at the README table):

| Command | Say |
|---|---|
| `/speckit-constitution` | "Our engineering rules, written once. Copilot checks every plan against them." |
| `/speckit-specify` | "Turns a short brief into a structured spec: user stories, acceptance scenarios, numbered requirements. No technology yet." |
| `/speckit-clarify` | "Copilot asks *us* questions about gaps instead of guessing." |
| `/speckit-plan` | "*Now* we bring in technology. It produces the design, data model and contracts." |
| `/speckit-tasks` | "Breaks the plan into ordered tasks, tests first, with file paths." |
| `/speckit-analyze` | "A consistency check: is every requirement covered by a task, and does anything break the constitution?" |
| `/speckit-implement` | "Works through the tasks and writes the tests and code." |
| `/speckit-converge` | "Compares the code against the spec and adds tasks for anything missing." |

**Show:** `.specify/memory/constitution.md` (scroll slowly).
> "This is our constitution. It's in plain English: test-first, security rules, and, for this
> project, that the JSON file is a versioned contract and never contains secrets. Copilot's plan
> has to include a Constitution Check table showing it followed these."

**Show:** an example of where outputs land: `specs/NNN-feature/` (from the dry-run branch).
> "Every step writes a markdown file into one folder per feature. They're normal files in Git,
> reviewed in normal PRs. Six months from now, *why* something was built is in the repo next to
> the code."

**If someone asks "why not just write a spec.md?"** (there's a slide for it, right after the
commands):
> "You can, and a disciplined team gets part of the way. Spec Kit adds the template, the
> command prompts that tell Copilot what to do at each step, the scripts that number features
> and refuse to plan without a spec, and the chain from spec to plan to tasks to code, checked
> against our rules. The CLI is only the installer; the value is what it installs."

**Show:** the "Closing the quality gap" and "A finding, proven" slides.
> "Spec Kit checks documents carefully before code, but after `/speckit-implement` there's
> nothing automated. So we added a Review, Attack & Fix extension. A critic reviews the diff and
> has to prove every defect with a failing test. For critical code, an adversary tries to break
> it. Anything ambiguous comes to us to decide. A fixer writes the regression test first, then
> the fix. CI won't merge while a serious finding is open, and after two rounds it escalates to a
> person instead of looping."

**Transition:** "So how do these two fit together for us?"

---

### 4.4 How they fit for us (0:25–0:30)

**Show:** the table in `AI-DLC.md` section 2 (phase → command → output → gate).

**Say:**
> "Each AI-DLC phase is one or two Spec Kit commands, and each gate is a PR approval. Three
> things in the repo hold it together."

Point at each:
1. **`docs/poc/PROJECT-CONTEXT.md`:** "Our specifics: which app, which environment, what we want
   the JSON to look like. Anything we don't know yet is marked OPEN, and Copilot turns it into a
   question instead of guessing. A script checks it's filled in. That's our G1."
2. **`.github/pull_request_template.md`:** "A checkbox per gate, and a prompt log so reviewers see
   exactly what we asked Copilot."
3. **CI (`ai-dlc-gates`):** "If a PR changes code without a spec, plan and tasks, or still has
   unresolved questions in the spec, the check fails. Bug-fix branches are exempt."

**Then the meta-point:**
> "And notice what we're building. Once Story Verification Recordings exists, *it becomes the
> last step of this same lifecycle*: every story's PR carries a recording (G5), and the pipeline
> replays it against the environment before release (G6). The POC builds the tool that closes
> the loop."

**Show:** the "What good output looks like" and "A verification file, up close" slides
(from [`docs/reference-example/`](../reference-example/README.md)).
> "Before we run it live, here's the target. We wrote a reference spec, plan and tasks by hand:
> four user stories, 25 testable requirements, a plan that passes all eight of our rules, and 51
> tasks with every requirement covered. That's the bar we'll hold Copilot's output to at each
> gate. And this is what a developer's verification file looks like: readable in a PR, linked
> to the work item, secrets by name only, paths instead of hosts."

**Transition:** "Enough slides. Let's run it."

---

### 4.5 Live demo (0:30–0:50)

**Follow [DEMO-SCRIPT.md](../demo/DEMO-SCRIPT.md)**, using this timing:

| Minutes | Demo step | What to say while it runs |
|---|---|---|
| 0:30–0:33 | Show the brief and the context file; run `bash scripts/check-context.sh` | "This is G1: intent plus our specifics." |
| 0:33–0:38 | `/speckit-specify` (paste the prompt) | "Watch for `[NEEDS CLARIFICATION]`: it's flagging what we didn't say." |
| 0:38–0:42 | `/speckit-clarify`; let the PO answer 2–3 questions live | "This conversation normally happens in QA, three weeks later." |
| 0:42–0:46 | `/speckit-plan` (paste the prompt); open `plan.md` → Constitution Check, `research.md`, `contracts/` | "The JSON schema is a contract we review *before* any code exists." |
| 0:46–0:48 | `/speckit-tasks`; scroll `tasks.md` | "Tests first, file paths, `[P]` means it can run in parallel." |
| 0:48–0:50 | **Switch to the dry-run branch** for implement: show the code, `dotnet test`, a JSON verification file, a replay | "I ran implement earlier because it takes a few minutes. Here's the result." |

**If something goes wrong:** say "this is exactly why there are gates," and switch to the dry-run
branch. Walk through the files already generated there. Don't debug live.

**Transition:** "So what are we actually proposing?"

---

### 4.6 POC plan and asks (0:50–0:55)

**Show:** `docs/poc/POC-PLAN.md`: Timeline, then Success criteria.

**Say:**
> "Three weeks, part-time. Week 1 we finish the spec and plan with real approvers. Week 2 we
> build: replay first, then recording. Week 3 we demo the result and make a recommendation:
> adopt, adapt or drop.
>
> We'll measure: lead time, how many ambiguities were caught before code, requirement coverage,
> how much AI output we kept, and how long each gate took. And at the end, a simple question:
> would you use this on your next story?"

Quote 2–3 numbers from your dry run here if you have them.

**The asks (make these explicit, with names):**
1. A **PO** for G1/G2 and to answer clarify questions. (About 2 hours across the POC.)
2. A **Tech Lead** for G2–G4 reviews. (About 2–3 hours.)
3. **One or two developers** to build with Copilot in week 2.
4. **QA** to review the acceptance scenarios and try a recording in week 3.
5. Anyone who knows the **target environment** (sign-in, test data, network) to help finish
   `PROJECT-CONTEXT.md` sections 2 and 3.

**Transition:** "Questions?"

---

### 4.7 Q&A (0:55–1:00)

Use section 6 below. Close with:
> "Everything you saw is in the `spec-kit-poc` repo: the lifecycle, the rules, the demo script
> and this agenda. I'll send the link. Thanks."

---

## 5. 30-minute version

| Time | Segment | Change from the full version |
|---|---|---|
| 0:00 | Why we're here | 3 min |
| 0:03 | AI-DLC + Spec Kit together | 7 min: the diagram in `AI-DLC.md` §2 and the command table from 4.3 only |
| 0:10 | Demo | 12 min: run `/speckit-specify` + `/speckit-clarify` live; show plan, tasks and implementation from the dry-run branch |
| 0:22 | POC plan and asks | 4 min |
| 0:26 | Q&A | 4 min |

---

## 6. Likely questions

| Question | Answer |
|---|---|
| "Isn't this just more documents?" | The documents are AI-drafted and reviewed in minutes. They replace the back-and-forth that normally happens after code is written: in review, in QA, in production. |
| "Who's responsible if the AI gets it wrong?" | Whoever approved it at the gate, same as a code review today. Copilot never approves anything. |
| "Will this slow down small changes?" | No. Bug fixes and small enhancements have lighter paths (`AI-DLC.md` §5). The full flow is for features. |
| "Does it work on our existing code, not just new projects?" | Yes. Specs describe a change, and Copilot reads the existing code when planning. Running it on our real repo is part of this POC. |
| "Is our code safe?" | It uses Copilot under our existing GitHub agreement. Spec Kit is files in the repo plus a local CLI; it doesn't send anything anywhere itself. Credentials never go in specs, prompts or verification files (constitution V). |
| "What is AI-DLC officially?" | The term was popularised by an AWS methodology, but it doesn't need AWS. We use the general idea: AI drafts, humans approve at gates. Our version is in `AI-DLC.md` and we can change it. |
| "Why not just write a spec.md ourselves?" | You can, but you'd be rebuilding what Spec Kit installs: the template, the step-by-step command prompts, the scripts and checks, and the chain from spec to plan to tasks to code. The `specify` CLI is only the installer; the value is in those files. |
| "Doesn't AI review its own code badly?" | That's why the critic runs in a **new chat**, without the builder's reasoning, and has to **prove** each defect with a failing test. No test, no finding. And a person still makes the rulings and does the final PR review. |
| "Why Spec Kit and not just prompting Copilot?" | Repeatability. Same steps, same templates, same output files every time, for every developer, and an audit trail in Git. |
| "Why record with Playwright instead of writing tests?" | Recording is faster for the developer and captures what *they* expected. The JSON is readable in the PR, and the runner turns it into a repeatable check against the real environment. |
| "What happens to the verification files after release?" | That's an open question for the POC (in the feature brief). Options: they join a regression set, or get archived. |
| "What if the recorder output doesn't match our JSON format?" | It won't directly: the recorder produces test code. How we convert it is a planning decision, documented in `research.md`. |
| "What does it cost?" | No new licences: Spec Kit is free and open source, and we already have Copilot. The cost is people's time at the gates, which is one of the things we're measuring. |
