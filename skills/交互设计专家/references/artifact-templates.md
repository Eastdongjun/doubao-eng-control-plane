# Artifact Templates

Copy only the sections needed for the current decision. Keep stable IDs when artifacts cross teams.

## Contents

- [Interaction brief](#interaction-brief)
- [User flow specification](#user-flow-specification)
- [State matrix](#state-matrix)
- [Interaction contract](#interaction-contract)
- [Usability test plan](#usability-test-plan)
- [Interaction QA checklist](#interaction-qa-checklist)

## Interaction brief

```markdown
# Interaction Brief

## Decision
- Decision:
- Owner:
- Target date:

## Intent
When [actor] needs to [task] in [context], enable [outcome] with [qualities], while preventing or recovering from [failure].

## Evidence
| Claim | Type | Source | Confidence | Design consequence |
|---|---|---|---|---|

## Context
- Frequency / urgency:
- Error consequence / reversibility:
- Platform and input:
- Governing design system:
- Constraints:

## Scope
- In:
- Out:
- Open:
```

## User flow specification

```markdown
# Flow [FLOW-ID]: [Name]

## Frame
- Actor:
- Trigger:
- Preconditions:
- Outcome:
- Completion evidence:

## Paths
| Step ID | User intent | Action | System response | Resulting state | Alternate / failure | Recovery |
|---|---|---|---|---|---|---|

## Continuity
- Cancel:
- Back:
- Interrupt / resume:
- Cross-device / collaboration:

## Risks and decisions
| ID | Risk or open decision | Evidence needed | Owner | Due |
|---|---|---|---|---|
```

## State matrix

```markdown
# State Matrix: [Object / View / Pattern]

| State ID | Entry condition | Visible content | Available actions | Focus / announcement | Exit | Persistence | Event |
|---|---|---|---|---|---|---|---|

## Invariants
-

## Failure classes
| Failure | Detection | Explanation | Preserve | Recovery | Escalation |
|---|---|---|---|---|---|
```

## Interaction contract

```markdown
# Interaction [IX-ID]: [Name]

- Actor and intent:
- Trigger:
- Preconditions:
- Input and validation:
- Immediate response:
- State transition:
- Feedback:
- Persistence:
- Failure:
- Cancel / retry / undo:
- Permission / privacy:
- Keyboard / focus / announcement:
- Reduced-motion behavior:
- Analytics:

## Acceptance examples
1. Given ...
```

## Usability test plan

```markdown
# Usability Test Plan

## Decision
- Decision:
- Belief:
- Uncertainty:
- Threshold:
- Resulting action:

## Participants and context
- Segments:
- Experience:
- Accessibility:
- Device/environment:

## Tasks
| Task | Starting state | Intent prompt | Observe | Success | Critical error |
|---|---|---|---|---|---|

## Evidence
| Observation | Interpretation | Severity | Confidence | Recommendation |
|---|---|---|---|---|
```

## Interaction QA checklist

```markdown
# Interaction QA

- [ ] Primary, alternate, cancel, and recovery paths work
- [ ] Loading, empty, partial, error, offline, and permission states are truthful
- [ ] Duplicate actions, interruption, refresh, and stale data are handled
- [ ] Keyboard order, focus, names, states, and announcements are correct
- [ ] Touch/pointer/gesture behavior and alternatives work
- [ ] Zoom, text expansion, localization, and reduced motion remain usable
- [ ] Approved components, patterns, and tokens are used
- [ ] Events represent the implemented behavior and avoid sensitive leakage

## Findings
| Severity | Location | Expected | Observed | Evidence | Owner |
|---|---|---|---|---|---|
```
