# Flows, States, and Behavior

Use this module for feature flows, multi-step tasks, asynchronous operations, permissions, destructive actions, or any experience whose behavior cannot be understood from one static screen.

## Contents

- [Flow grammar](#flow-grammar)
- [State inventory](#state-inventory)
- [Interaction contract](#interaction-contract)
- [Asynchronous behavior](#asynchronous-behavior)
- [Destructive and high-consequence actions](#destructive-and-high-consequence-actions)
- [Interruption and continuity](#interruption-and-continuity)
- [Traceability](#traceability)

## Flow grammar

Represent a flow with:

- `Entry`: how and why the actor arrives
- `Precondition`: what must already be true
- `Intent`: the immediate outcome
- `Action`: the actor’s operation
- `Decision`: choice based on information or rule
- `System step`: invisible or automated processing
- `State`: persistent condition of an object or task
- `Feedback`: evidence of response or status
- `Exit`: completion, abandonment, cancellation, or handoff
- `Recovery`: return to a safe, intelligible state after failure

Map at least:

1. Primary path
2. Likely alternate path
3. Permission or eligibility failure
4. Validation or business-rule failure
5. Network/system failure
6. Cancellation or backtracking
7. Interruption and resume
8. Completion and next meaningful action

## State inventory

Use only relevant states, but make omission deliberate:

| Layer | Candidate states |
|---|---|
| View | initializing, loading, ready, empty, partial, stale, error, offline |
| Object | draft, valid, invalid, queued, processing, complete, failed, archived, deleted |
| Control | default, hover, focus, pressed, selected, disabled, busy |
| Permission | unknown, requesting, granted, denied, expired, revoked |
| Submission | idle, validating, sending, accepted, rejected, retryable, conflicted |
| Destructive action | proposed, warned, confirmed, executing, undoable, finalized, failed |

Do not merge system states that require different explanation or recovery.

## Interaction contract

For each consequential behavior write:

```text
ID:
Actor and intent:
Trigger:
Preconditions:
Input and validation:
Immediate response:
State transition:
Feedback and duration:
Persistence:
Failure classes:
Cancel / retry / undo / recovery:
Permission and privacy:
Analytics event:
Acceptance examples:
```

## Asynchronous behavior

Specify:

- Whether the action is optimistic, pessimistic, queued, or backgrounded
- What becomes disabled and what remains available
- Whether duplicate requests are possible and how they are deduplicated
- Progress semantics: indeterminate, determinate, step-based, or time estimate
- What happens on navigation, refresh, sign-out, device change, or reconnect
- How stale data, partial success, conflicts, and late responses are represented
- Retry policy, idempotency, cancellation, notification, and final reconciliation

Never use a spinner as the entire specification.

## Destructive and high-consequence actions

Choose protection based on severity, reversibility, frequency, and user intent:

- Clear consequence before action
- Safer default and scoped selection
- Preview or impact summary
- Inline confirmation for low-frequency risk
- Typed or repeated confirmation only for exceptional irreversible harm
- Delay or cooling-off period when warranted
- Undo, recovery window, export, version history, or administrator restoration

Do not stack friction indiscriminately. Prefer reversible systems over ceremonial confirmation.

## Interruption and continuity

Preserve:

- Draft input and selected scope
- Current object and position
- Completed steps and pending decisions
- Upload or processing status
- Explanation of what changed while away
- Safe resume, restart, or discard choices

For multi-device or collaborative work, define source of truth, conflict resolution, presence, version history, and notification.

## Traceability

Use stable IDs when work crosses teams:

`Outcome -> Task -> Flow -> Interaction -> State -> Rule -> Event -> Metric -> Acceptance test`

Every event must support a decision or operational need. Every acceptance test must correspond to a visible behavior or invariant.
