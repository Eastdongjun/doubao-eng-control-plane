# Interactive Motion and Signature Moments

Use this module for product UI, direct manipulation, gestures, feedback, state transitions, onboarding, milestones, and product-defining moments.

## Contents

- [Interactive motion contract](#interactive-motion-contract)
- [Responsiveness](#responsiveness)
- [Functional purposes](#functional-purposes)
- [Frequency matrix](#frequency-matrix)
- [Common interactions](#common-interactions)
- [Gesture motion](#gesture-motion)
- [Signature moments](#signature-moments)
- [Signature-moment design](#signature-moment-design)

## Interactive motion contract

Specify:

```text
ID:
Purpose:
Trigger:
Preconditions:
Input coupling:
Primary mover:
Stable anchor:
State transition:
Timing or spring:
Interruption / retarget:
Cancel / reverse:
Completion evidence:
Sound / haptic:
Reduced motion:
Low-performance fallback:
Analytics or test:
```

## Responsiveness

- Give immediate visible response to input.
- Separate input acknowledgment from completion.
- Keep direct manipulation under continuous user control.
- Preserve velocity and position when retargeting.
- Allow cancellation before commitment and reversal after safe commitment.
- Avoid blocking input for decorative settle unless state integrity requires it.

## Functional purposes

Use motion to:

- Explain cause and effect
- Preserve spatial continuity
- Show hierarchy or scope
- Preview consequence
- Communicate progress and waiting
- Direct attention to a change
- Confirm state
- Support error and recovery
- Teach an unfamiliar gesture or model

If static change communicates equally well with less cost, keep it static.

## Frequency matrix

| Frequency / consequence | Default treatment |
|---|---|
| High frequency, low consequence | immediate, quiet, short, often no entrance |
| High frequency, high consequence | responsive with explicit status and reliable recovery |
| Low frequency, low consequence | small expressive allowance |
| Low frequency, high consequence | deliberate, legible, restrained, preview and confirmation |
| Rare milestone | authored signature moment if meaningful |

## Common interactions

### Enter and exit

- Tie entrance to source, hierarchy, or spatial model.
- Exit should explain destination or removal.
- Do not replay full entrances on routine return.

### Loading and progress

- Acknowledge immediately.
- Prefer content-preserving or skeleton behavior when structure is stable.
- Use determinate progress only when the measure is truthful.
- Allow backgrounding, cancellation, retry, and completion notification when appropriate.

### Error and recovery

- Direct attention without shaking the entire interface.
- Keep the failed object and remedy visible.
- Preserve input and position.
- Use motion to connect message to cause, not dramatize blame.

### Success and celebration

- Match scale to effort, meaning, and rarity.
- Complete the product state before or with the celebration.
- Permit continued action; do not hold users hostage to applause.

## Gesture motion

Define threshold, axis, resistance, preview, commitment, cancellation, snap, overscroll, haptic, and alternative. Respect system gestures and scroll.

## Signature moments

A signature moment is a small, repeatable piece of product identity in time. It should:

- Occur at a meaningful transition
- Reveal product or brand truth
- Remain understandable without prior explanation
- Use a distinctive but system-compatible mechanism
- Survive reduced motion and modest devices
- Be rare enough to retain contrast

Candidate moments:

- First successful creation
- Transformation from input to value
- Reveal of an important result
- Completion of a difficult journey
- Transition between product modes or identities
- Shared/collaborative handoff
- Brand entrance in a launch or onboarding context

## Signature-moment design

1. Name the emotional and functional beat.
2. Identify the object whose change carries meaning.
3. Preserve one stable anchor.
4. Choose a material/temporal metaphor that belongs to the brand.
5. Design the mundane state before and after.
6. Prototype three rough temporal structures, not three polished skins.
7. Test comprehension, emotional response, repetition, accessibility, and runtime.
8. Convert the chosen behavior into system rules and restraint boundaries.

Limit a product to one primary signature family and a few supporting echoes. Do not turn every component into a mascot performance.
