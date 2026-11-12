# Feature Brief: Story Verification Recordings (Gate G1 input)

> This is the **intent** for the POC project. It is deliberately short and leaves questions
> open, so `/speckit-clarify` has real ambiguity to find and resolve.

## Problem
When a developer finishes a user story or a defect fix, "it works" is checked by hand, on their
machine, once. Nobody else can see what the developer expected to happen, and nothing re-checks
it after the code is deployed to an environment. Regressions and "works on my machine" defects
are found late, by QA or by users.

## Who it's for
- **Developers**, who finish a story or defect and want to prove it works.
- **QA / reviewers**, who want to see exactly what the developer verified.
- **The delivery pipeline**, which needs an automatic pass/fail check against the environment
  that has the developer's code.

## What we want (v1)
1. **Record.** As the last step of their work, a developer records what they expect to happen:
   they walk through the scenario in a browser, and mark the outcomes they expect (for example
   "this message appears", "this value is shown", "I land on this page").
2. **Save as a file.** The recording is saved as a readable **JSON verification file** that is
   linked to the user story or defect ID and stored with the code change, so it is reviewed in
   the same pull request.
3. **Replay.** An automated Playwright-based runner reads the JSON file and replays it against a
   chosen environment (the one that has the developer's code), checking each expected outcome.
4. **Report.** The run produces a clear pass/fail result per step, with enough evidence
   (which step failed, what was expected, what was found, a screenshot) to act on it.
5. **Gate.** The runner can be used in the pipeline so a story or fix is not treated as done
   until its verification file passes against the environment.

## Out of scope for v1
Mobile apps, API-only checks, performance/load testing, visual (pixel) comparison, a hosted
dashboard, replacing the existing QA regression suite.

## Success measures
- A developer can record a verification for a typical story in under 5 minutes.
- A recorded file replays against a deployed environment with no manual edits.
- A reviewer can tell from the JSON alone what was verified.

## Open questions (intentionally left for Clarify)
- How does the runner sign in to the environment, and where do credentials live (never in the
  JSON file)?
- How is test data handled, when a recording depends on data that only exists on the
  developer's machine?
- Can one story have several verification files? Can a file be edited by hand after recording?
- Which environments can a file run against (dev, test, staging), and how is the base URL chosen?
- What happens to verification files after the story is released: do they join a regression set
  or get archived?
- Which browsers must be supported?
- How are flaky steps (timing, animations) handled: retries, waits, or failure?
