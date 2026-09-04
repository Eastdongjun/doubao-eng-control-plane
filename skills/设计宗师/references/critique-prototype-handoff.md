# Critique, Prototype, Handoff, and QA

Use this module to evaluate design quality, validate uncertain behavior, and preserve intent through implementation.

## Critique order

Review in layers so visual taste does not mask structural failure:

1. Intent: audience, task, outcome, emotion, constraints
2. Usefulness: right problem and scope
3. Information architecture and content hierarchy
4. User flow, states, error/recovery, permissions
5. Interaction and cognitive load
6. Content clarity and tone
7. System consistency and reuse
8. Visual expression and brand
9. Accessibility and inclusion
10. Technical/operational feasibility

For each finding provide:

- Location and observed behavior
- User/business effect
- Evidence or principle
- Severity: blocker / high / medium / low
- Specific recommendation
- Owner or decision needed

Separate facts, interpretations, and preferences. Include genuine strengths only when specific.

Summarize action using three bands in addition to severity:

- **Keep:** effective mechanisms that should survive revision
- **Fix:** contradictions or defects that block the intended outcome
- **Quick wins:** bounded improvements with high impact relative to effort

Do not let quick wins displace systemic fixes, and do not use “Keep” as generic praise.

## Redesign protocol

Before changing:

- Audit brand equity, information architecture, navigation, content, accessibility, analytics, SEO, component system, and signature interactions.
- Choose preserve, evolve, or overhaul.
- State what cannot change silently: URLs, navigation labels, legal/consent text, analytics identifiers, logo, core workflows.
- Modernize from lowest-risk/highest-leverage layers: typography, spacing, color calibration, component consistency, key compositions, then structural replacement.
- Plan token/component/content migration and implementation sequencing.

## Prototype plan

```markdown
Research question:
Target participants and context:
Assumption/decision:
Fidelity and rationale:
Interactive scope:
Static/faked scope:
Starting state and reset:
Tasks and success evidence:
Behavior/quotes/confidence to observe:
Accessibility accommodations:
Analysis and decision threshold:
```

Use realistic scenarios that do not name the control. Prototype failure and recovery when these are material to the decision.

## Design handoff contract

Include:

- Requirement/flow links and design rationale
- Responsive layouts and content priority
- Component instances, variants, and token references
- Interaction triggers, sequence, timing, focus, and interruption
- Default/loading/empty/error/success/permission/offline states
- Content, truncation, validation, and localization rules
- Accessibility annotations
- Asset format, crop, density, and rights
- Analytics hooks when tied to behavior
- Known gaps, decisions, owners, and acceptance evidence

Do not annotate obvious pixels while omitting non-obvious behavior.

## Pre-handoff QA

Check:

- File/frame/layer naming and cleanup
- Library components rather than unexplained detached copies
- Tokens/styles/variables rather than arbitrary overrides
- No raw or near-token values in token-governed properties; every exception is approved and documented
- Shared token names, values, aliases, roles, scales, and modes match the frozen project baseline
- Realistic final content and extreme lengths
- Complete states and interactions
- Responsive and zoom behavior
- Viewport/region/component safe areas, partial clipping, document overflow, scroll endpoints, and sticky/fixed boundary behavior
- Contrast, focus, keyboard, semantics, accessible names, announcements, touch targets, reduced motion
- Exportable assets and implementation notes
- Requirement coverage and explicit approval status

Verdict must be `Ready`, `Ready with conditions`, or `Not ready` with blockers and owners.

## Rendered artifact review

For HTML, interactive prototypes, decks, motion, or exported visual artifacts, review the executed result as well as the source:

- Open the actual entry point or export in the target runtime.
- Capture representative screens/frames after fonts, assets, data, and intentional entrance motion settle.
- Inspect blocking console/network errors and missing assets.
- Exercise the critical path, reset/recovery, and material controls.
- Check representative viewports, modes, content extremes, keyboard/focus, and reduced motion.
- Record what was manually inspected, automated, untested, or unavailable.

Use [artifact-production-validation.md](artifact-production-validation.md) for the evidence bundle and medium-specific proof.

## Implementation QA

Compare design and build across:

- Information and reading order
- Layout at representative widths and zoom
- Tokens, type, color, spacing, shape, icon, image
- Token identity and semantic mapping, including detection of literal values that merely approximate approved tokens
- Component behavior and all states
- Keyboard, focus, screen reader, motion preference
- Content overflow and localization
- Non-decorative boundary safety and horizontal-scroll axis isolation
- Loading, latency, errors, offline/timeout
- Performance and layout stability
- Analytics/identifiers only when part of the contract

Classify differences as defect, intentional implementation decision, design gap, or environment constraint. Treat unauthorized shared-token mutation and unexplained raw-value drift as release defects. Record accepted deviations with scope, approver, and review date so they do not become accidental precedent.
