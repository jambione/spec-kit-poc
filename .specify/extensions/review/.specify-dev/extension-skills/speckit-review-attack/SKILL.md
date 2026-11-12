---
name: speckit-review-attack
description: 'Adversary: try to break security- or interop-critical code with hostile
  inputs; failing tests are the findings'
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: spec-kit-poc
  source: extension:review
---

# Review Attack Skill

# Attack (Adversary)

**Role**: breaker. Recommended model: your strongest reasoning model (`models.attack`). Use it **only** for critical scopes: authentication, secrets, parsing untrusted input, file formats or wire protocols, public APIs, data migrations. Run it in its **own chat**, in parallel with `/speckit-review-code` on the same round.

## User Input

```text
$ARGUMENTS
```

The input names the **scope**. Ask one question if it's missing.

## Setup

Run `python3 .specify/extensions/review/scripts/python/review_state.py paths --scope "<scope>" --role attack`. If there's no round yet, run `start-round --scope "<scope>"` first (exit `3` = round limit: stop and escalate). Use `findings` (this is `attack.md`), `test_file`, `context_pack`, `base` and `head` from the JSON.

## Goal

**Break** the code in scope. Don't review style or spec wording; the critic does that.

## Attack menu (pick what applies)

- Malformed, truncated, oversized and empty input; wrong types; duplicate keys
- Boundary values and overflow; negative or zero counts; unicode (combining characters, RTL, emoji, normalization)
- Replay, reordering, duplication and tampering of messages or files
- Messages in the wrong state or from the wrong role
- Brute force and missing rate limits
- Resource exhaustion: unbounded lists, maps, buffers or retries; floods; slow consumers
- Races between cancel, retry, disconnect and in-flight work; cancellation mid-operation
- Clock jumps (through an injected clock, if the code has one)
- Secrets leaking into logs, errors, reports or files
- Differential checks where two implementations must agree (e.g. schema vs validator)

## Rules

- Write tests **only** in `test_file`. Modify nothing else.
- Each test asserts behaviour that the spec **requires**, or that safety obviously requires. Failing tests are the findings.
- Use timeouts so a hang fails instead of blocking the run.
- Run only your test file while working.
- Write each failing test as a finding in `findings`, with IDs `A-001`, `A-002`, …, in the template's block format with `Status: OPEN`.

## Do not
Commit. Change production code. Edit any file except `findings` and `test_file`.

## Report (≤200 words)
Number of failing tests, one line per failure, one line on what held up, and the findings path.
