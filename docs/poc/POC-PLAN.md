# POC Plan: AI-DLC with GitHub Spec Kit

## Goal
Show, by building a real internal tool ([Story Verification Recordings](../demo/feature-brief.md)), that an AI-driven lifecycle (Copilot drafts, humans
approve at gates) using GitHub Spec Kit can **cut ambiguity and rework, keep quality at our
standard and leave a clear audit trail**. Finish with a go / no-go / adapt recommendation.

## Scope
| In | Out |
|---|---|
| One project end to end: record → JSON verification file → Playwright replay → report | Rolling the tool out to other teams |
| Lifecycle doc, constitution, PR gates, CI checks | Changes to other teams' processes |
| GitHub Copilot (agent mode) + Spec Kit 1.4.0 + .NET 8 + Playwright for .NET | Other AI tools |
| Metrics + a team retrospective | Formal security review (flagged as a follow-up) |

## Timeline (about 3 weeks, part-time)

| Week | Activities | Exit criteria |
|---|---|---|
| **0 (1–2 days)** | Confirm the "AI DLC" definition with the sponsor. Check Copilot licences and agent mode access. Install prerequisites. | Sponsor agrees with the lifecycle doc in principle |
| **1** | Tailor the constitution to real team standards. Dry-run Inception and planning (specify → clarify → plan → tasks). Settle the recording approach in `research.md`. | Approved spec, plan and tasks on a dry-run branch |
| **2** | Build with the real roles (PO, TL, Dev, QA): first the JSON format and replay runner (the lowest-risk slice), then recording. Collect metrics. | Merged PR with approvals G2–G5 visible; a verification file replays against the sample app |
| **3** | Rehearse the demo, run the demo, hold a retro, write the recommendation. | Demo delivered; recommendation doc |

## Success criteria / metrics

Record these during the dry run and the real run (copy the table into the PR or a sheet).

| Metric | How to measure | Target / signal |
|---|---|---|
| Lead time, brief to merged PR | Timestamps of first commit → merge | Compare with a similar past feature |
| Ambiguities caught before code | Count of `[NEEDS CLARIFICATION]` + clarify questions | > 0 = value shown |
| Requirement coverage | FRs with ≥1 test ÷ total FRs | 100% |
| Rework after code review | Review comments that needed a code change | Lower than the team's usual |
| AI output kept | Rough % of generated code kept without major rewrite | ≥ 70% |
| Gate overhead | Minutes spent per gate review | ≤ 15 min per gate for a small feature |
| Developer sentiment | Retro 1–5 score: "I'd use this on my next feature" | ≥ 4 |

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Spec Kit / Copilot change fast (e.g. `/speckit.x` → `/speckit-x`) | Version pinned (1.4.0); upgrade on purpose |
| Process feels heavy for small changes | Size-based paths (AI-DLC.md §5) |
| Specs drift from code after v1 | Use `/speckit-converge`; decide in the retro whether specs are living documents |
| Copilot goes off track during the live demo | Pre-recorded build step + fallback dry-run branch |
| Security / compliance questions about AI | Brief security early; no real data in prompts |
| Recording is harder than replay (capturing expected outcomes, stable locators) | Build replay first with hand-written files; decide the recording approach in `research.md`; a thin recorder is enough for the demo |
| Sign-in and test data differ per environment | Raised as Clarify questions; credentials only via environment variables or secret store |
| "AI DLC" means something different to the sponsor | Week 0 alignment; lifecycle doc is easy to rename and rearrange |

## Deliverables
1. This repo: lifecycle doc, constitution, PR template, CI gates, demo script.
2. A merged feature PR showing the full trail (G2–G5).
3. Metrics table + retrospective notes.
4. A one-page recommendation: adopt / adapt / drop, with a rollout plan if adopting.

## Open decisions for the sponsor
- [ ] Is there an existing company SDLC this must align with?
- [ ] Who plays PO / TL / QA for the real run?
- [ ] Which application and environment should the tool be proven against after the sample app?
