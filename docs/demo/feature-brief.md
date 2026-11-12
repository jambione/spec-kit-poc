# Feature Brief: Team Leave Requests (Gate G1 input)

> This is the **intent** a Product Owner would write. It is deliberately short and leaves a few
> questions open, so the demo can show Spec Kit finding and resolving ambiguity
> (`/speckit-clarify`).

## Problem
Employees request time off by email today. Managers lose track of requests, there is no record
of approved leave, and people sometimes book overlapping time off without anyone noticing.

## Who it's for
- **Employees** who want to request time off and see the status.
- **Managers** who approve or reject requests for their team.

## What we want (v1)
1. An employee can submit a leave request with a start date, end date, leave type (vacation,
   sick, other) and an optional reason.
2. An employee can see their own requests and the status of each (pending / approved /
   rejected / cancelled).
3. An employee can cancel a request that has not started yet.
4. A manager can see pending requests for their team and approve or reject them, with a comment
   when rejecting.
5. The system prevents an employee from having two overlapping active requests.

## Out of scope for v1
Leave balances / accruals, public holiday calendars, email notifications, a UI (API only).

## Success measure
A manager can process a request in under 1 minute, and no overlapping leave gets approved.

## Open questions (intentionally left for Clarify)
- Can someone request half days?
- Can a request be in the past (e.g. sick leave logged afterwards)?
- Can a manager approve their own request?
- What happens to an approved request when the employee cancels it?
