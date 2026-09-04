# Systems, Handoff, and QA

Use this module for work governed by an existing design system, for reusable interaction patterns, and before implementation approval.

## Contents

- [Authority baseline](#authority-baseline)
- [Conformance ladder](#conformance-ladder)
- [Pattern specification](#pattern-specification)
- [Handoff bundle](#handoff-bundle)
- [Acceptance examples](#acceptance-examples)
- [Design QA](#design-qa)
- [Deviation log](#deviation-log)

## Authority baseline

Record:

- Governing system and version/date
- Source-of-truth order
- Component library and supported platforms
- Shared token registry
- Approved patterns and known exceptions
- Accessibility standard and test responsibility
- Who may authorize local and shared changes

When sources conflict, do not silently choose. Apply the recorded authority order and log the conflict.

## Conformance ladder

Use:

1. Reuse an approved component or pattern.
2. Compose approved parts.
3. Use a documented property or local variant.
4. Propose a scoped extension with rationale and impact.
5. Change shared behavior or tokens only after explicit authorization.

Shared Design Tokens are read-only by default. This includes primitive, semantic, component, motion, spacing, typography, color, elevation, radius, and other governed values. An approximate visual match is not token conformance.

## Pattern specification

For every reusable pattern define:

- Purpose and non-purpose
- Anatomy and semantic structure
- Entry and exit
- Properties and supported variants
- States and transitions
- Content constraints
- Input modes and platform adaptation
- Keyboard, focus, announcements, and reduced motion
- Loading, empty, error, permission, interruption, and recovery
- Token/component mapping
- Data and event dependencies
- Examples, counterexamples, and migration
- Owner, status, and review rule

## Handoff bundle

Include:

- Interaction intent
- Linked flow and stable IDs
- State matrix
- Behavior contracts
- Content and validation rules
- Responsive/platform differences
- Accessibility annotations
- Data latency, permission, and failure assumptions
- Analytics events and properties
- Acceptance examples
- Approved deviations and open decisions

Do not use annotations to restate what is already obvious visually. Annotate what cannot be inferred from a static screen.

## Acceptance examples

Prefer concrete examples:

```text
Given [precondition and state]
When [actor action or system event]
Then [visible response and state change]
And [persistence / focus / announcement / event]
But [invariant that must remain true]
```

Cover risk-based cases, not every permutation.

## Design QA

Test the implemented experience against:

1. Primary and alternate paths
2. Realistic, extreme, empty, and invalid content
3. Slow, failed, offline, stale, and partial responses
4. Duplicate action, interruption, refresh, and resume
5. Permission and role differences
6. Keyboard, focus, semantics, and assistive announcements
7. Pointer/touch and representative viewport/device behavior
8. Localization, text expansion, zoom, and RTL where relevant
9. Reduced motion and contrast settings
10. Analytics event accuracy and privacy
11. Approved component, pattern, and token conformance

Classify findings:

- **Blocker:** prevents a critical task, causes harm/data loss, or creates a severe access barrier.
- **High:** likely failure or misleading behavior with no clear recovery.
- **Medium:** significant friction, inconsistency, or edge-case failure.
- **Low:** polish issue with limited outcome impact.

## Deviation log

For each deviation capture:

```text
Rule or token:
Observed behavior:
Scope:
Reason:
User/business impact:
Accessibility/performance impact:
Authorization:
Owner and expiry:
Migration or rollback:
```

Unapproved deviations are defects, not creative choices.
