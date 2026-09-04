# Accessibility and Inclusive Interaction

Use this module for every approval of interactive behavior. Scale the written detail to risk, but never omit the underlying requirements.

## Semantics first

- Use native elements and platform controls when they match the behavior.
- Preserve logical source order and programmatic relationships.
- Give controls accessible names that describe action or destination.
- Expose role, state, value, requirement, error, and expanded/selected status.
- Add ARIA only when native semantics cannot express the pattern; implement the entire expected keyboard and state contract.

## Keyboard and focus

Specify:

- Tab order and grouping
- Arrow-key behavior where a composite widget requires it
- Enter, Space, Escape, Home/End, and shortcut behavior
- Visible focus across all themes and surfaces
- Focus entry, initial placement, trap conditions, return, and restoration
- Behavior after insert, delete, error, navigation, and async update

Never move focus merely to announce a status. Use appropriate live-region behavior.

## Perception and alternatives

- Do not communicate state through color alone.
- Provide text or structural alternatives for icon, image, chart, sound, haptic, and motion meaning.
- Preserve content and operation at zoom and text enlargement.
- Support contrast modes and user font or display settings where the platform permits.
- Avoid flashing and unsafe spatial motion.
- Honor reduced-motion settings with a meaningful state change, not a broken experience.

## Motor and touch

- Provide adequate targets and separation.
- Avoid precision-only interactions.
- Support cancellation before activation and reversal after accidental action.
- Provide alternatives to path-based gestures, multi-pointer gestures, dragging, and device motion.
- Avoid time limits where possible; allow extension and preserve work.

## Cognitive and language inclusion

- Use direct, specific language and stable terminology.
- Put instructions before the action and errors near their cause.
- Avoid memory-dependent codes or time pressure without alternatives.
- Show progress and allow review in complex tasks.
- Support localization expansion, CJK, RTL, pluralization, names, dates, numbers, and addresses.
- Avoid idioms and culturally narrow metaphors in critical interaction.

## Dynamic updates

Classify updates:

- Silent visual refresh
- Polite status
- Assertive critical alert
- Focus-changing navigation
- User-requested result set

Announce only what helps the user continue. Excessive live announcements create a different access barrier.

## Accessibility acceptance evidence

Require:

- Keyboard-only completion of the primary and recovery paths
- Focus order and focus return inspection
- Semantic tree/name/state inspection
- Zoom/reflow and text expansion
- Reduced-motion behavior
- Representative screen-reader task check for custom or high-risk patterns
- Error identification and recovery
- Target-size and non-precision alternative review

Conformance claims require evidence from the implemented artifact, not the design file alone.
