# POC Plan: AI-DLC with GitHub Spec Kit

## Goal
Show, with one realistic .NET feature, that an AI-driven lifecycle (Copilot drafts, humans
approve at gates) using GitHub Spec Kit can **cut ambiguity and rework, keep quality at our
standard and leave a clear audit trail**. Finish with a go / no-go / adapt recommendation.

## Scope
| In | Out |
|---|---|
| One feature end to end ([Leave Requests](../demo/feature-brief.md)) | Production deployment |
| Lifecycle doc, constitution, PR gates, CI checks | Changes to other teams' processes |
| GitHub Copilot (agent mode) + Spec Kit 1.4.0 + .NET 8 | Other AI tools |
| Metrics + a team retrospective | Formal security review (flagged as a follow-up) |

## Timeline (about 3 weeks, part-time)

| Week | Activities | Exit criteria |
|---|---|---|
| **0 (1–2 days)** | Confirm the "AI DLC" definition with the sponsor. Check Copilot licences and agent mode access. Install prerequisites. | Sponsor agrees with the lifecycle doc in principle |
| **1** | Tailor the constitution to real team standards. Do a dry run of the full flow on the sample feature. Note friction. | Dry-run branch with all artifacts + working API |
| **2** | Run the flow with the real roles (PO, TL, Dev, QA) on the same feature, or on a small real backlog item. Collect metrics. | Merged PR with approvals G2–G5 visible |
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
| "AI DLC" means something different to the sponsor | Week 0 alignment; lifecycle doc is easy to rename and rearrange |

## Deliverables
1. This repo: lifecycle doc, constitution, PR template, CI gates, demo script.
2. A merged feature PR showing the full trail (G2–G5).
3. Metrics table + retrospective notes.
4. A one-page recommendation: adopt / adapt / drop, with a rollout plan if adopting.

## Open decisions for the sponsor
- [ ] Is there an existing company SDLC this must align with?
- [ ] Who plays PO / TL / QA for the real run?
- [ ] Pilot on the sample feature only, or also on a real backlog item?
