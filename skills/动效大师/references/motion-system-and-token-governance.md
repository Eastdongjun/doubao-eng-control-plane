# Motion System and Token Governance

Use this module when an existing system governs the work or when motion must scale across components, products, or teams.

## Contents

- [Authority baseline](#authority-baseline)
- [Token protection](#token-protection)
- [Token architecture](#token-architecture)
- [Motion principles](#motion-principles)
- [Pattern families](#pattern-families)
- [Conformance ladder](#conformance-ladder)
- [Change proposal](#change-proposal)
- [Governance](#governance)

## Authority baseline

Record:

- Governing brand and design-system versions
- Motion principles and approved examples
- Token source, supported modes, and implementation packages
- Component behavior contracts
- Platform-native rules
- Accessibility and performance policies
- Authority for exceptions and shared changes

When sources conflict, apply the recorded source-of-truth order and log the conflict. Do not silently replace a user-approved rule with an external trend or personal preference.

## Token protection

Treat shared tokens as read-only by default, including:

- Duration
- Easing and spring
- Delay and stagger
- Distance and spatial offset
- Scale and rotation
- Opacity and blur
- Depth and perspective
- Path and morph behavior
- Haptic and sound roles
- Reduced-motion variants

Using an arbitrary near-value is still a violation. If approved durations are `100`, `160`, `240`, and `400 ms`, values such as `173` or `247 ms` require a documented, authorized exception.

## Token architecture

Prefer:

1. **Primitive:** raw reusable values
2. **Semantic:** purpose and perceptual role
3. **Component/pattern:** alias to semantic role with local constraints

Example:

```json
{
  "motion": {
    "duration": {
      "instant": "{duration.100}",
      "responsive": "{duration.160}",
      "transition": "{duration.240}",
      "expressive": "{duration.400}"
    },
    "easing": {
      "enter": "{cubic.productiveOut}",
      "exit": "{cubic.productiveIn}",
      "move": "{cubic.standard}"
    }
  }
}
```

Names should communicate purpose, not numeric value alone. Do not create a token until a repeatable semantic role exists.

## Motion principles

Write three to six principles that distinguish the system. Each principle needs:

- Intent
- Observable behavior
- Use cases
- Counterexample
- Accessibility/performance implication
- Reference implementation or prototype

Avoid generic principles such as “smooth,” “delightful,” or “natural” without behavioral meaning.

## Pattern families

Define only relevant families:

- Input acknowledgment
- State change
- Enter/exit
- Shared-element or spatial transition
- Loading/progress
- Error/recovery
- Attention
- Success/celebration
- Navigation and mode change
- Data change
- Drag/gesture
- Brand entrance and signature moment
- Narrative scene transition

For each pattern specify purpose, trigger, primary mover, stable anchor, token mapping, interruption, reduced-motion variant, performance fallback, and acceptance evidence.

## Conformance ladder

1. Reuse approved pattern and token.
2. Compose approved patterns.
3. Use an explicitly permitted local variant.
4. Propose a scoped extension with evidence.
5. Change a shared token or global behavior only after explicit authorization.

## Change proposal

```text
Current rule/token:
Problem and evidence:
Why composition or local variant is insufficient:
Proposed change:
Affected components/products:
Accessibility/performance impact:
Migration and fallback:
Decision owner:
Authorization:
Review/expiry:
```

## Governance

- Maintain a motion inventory and ownership.
- Review new patterns against purpose, frequency, thesis, tokens, accessibility, and performance.
- Deprecate rather than silently replace.
- Provide migration examples and automated token checks where practical.
- Test representative patterns in real contexts, not a gallery alone.
- Revisit trends separately from stable system semantics.
