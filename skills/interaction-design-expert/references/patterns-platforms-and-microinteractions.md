# Patterns, Platforms, and Microinteractions

Use this module when selecting controls, adapting across devices, designing gestures or shortcuts, or adding microinteractions.

## Contents

- [Pattern selection test](#pattern-selection-test)
- [Common pattern cautions](#common-pattern-cautions)
- [Forms and data entry](#forms-and-data-entry)
- [Search, filtering, and selection](#search-filtering-and-selection)
- [Platform adaptation](#platform-adaptation)
- [Gesture contract](#gesture-contract)
- [Microinteraction anatomy](#microinteraction-anatomy)

## Pattern selection test

For each proposed pattern, evaluate:

1. Does the user recognize the object and action?
2. Does the control’s native semantic match the action?
3. Is the action frequent, time-sensitive, reversible, or destructive?
4. Is the choice binary, exclusive, multiple, ordered, free-form, or command-like?
5. Must options remain visible for comparison?
6. Does the pattern work with keyboard, touch, zoom, assistive technology, and localization?
7. Does an approved system pattern already solve it?
8. What learning, implementation, and maintenance cost does a custom pattern add?

## Common pattern cautions

- **Modal:** use for a focused decision that cannot safely coexist with the underlying context. Avoid modal chains.
- **Drawer/sheet:** use for contextual, temporary work when origin remains meaningful. Define focus, dismissal, and back behavior.
- **Tabs:** use for peer sections users may switch among. Do not use as a disguised stepper.
- **Stepper:** use when order or prerequisites matter. Permit review and correction.
- **Accordion:** use to manage optional detail, not hide the primary task.
- **Toast:** use for transient, non-blocking feedback. Never make it the only record of a critical failure.
- **Tooltip:** use for supplemental explanation. It must not contain essential or interactive content without an accessible alternative.
- **Drag and drop:** add visible handles, drop targets, keyboard operations, announcements, cancel, and undo.
- **Infinite scroll:** justify against orientation, return, comparison, accessibility, and footer access.
- **Command palette:** provide search, grouping, shortcuts, scope, disabled explanations, and safe execution.

## Forms and data entry

- Ask only for information needed now.
- Group by user meaning and sequence, not data schema.
- Keep labels persistent; placeholders are examples, not labels.
- Explain format and consequence before entry.
- Validate at the moment feedback becomes useful without punishing incomplete input.
- Preserve values after recoverable failure.
- Place error messages near the field and provide a summary when scale requires it.
- Define autofill, paste, masking, units, locale, mobile keyboard, and privacy behavior.
- For long forms, communicate progress by meaningful sections, save state, and allow return.

## Search, filtering, and selection

Specify query scope, tokenization, typo behavior, ranking, recency, empty results, partial results, loading, history, and privacy.

For filters define:

- Default and persisted state
- OR/AND behavior within and across groups
- Result counts and disabled combinations
- Apply-immediately versus explicit apply
- Clear-one and clear-all
- Mobile presentation and keyboard behavior
- URL/shareability and back-button behavior

## Platform adaptation

Preserve task and meaning while adapting mechanics:

- Navigation depth and back behavior
- Pointer versus touch target density
- Hover availability
- Keyboard and shortcut conventions
- System sheets, pickers, share surfaces, and permission prompts
- Safe areas, orientation, resize, multi-window, and virtual keyboard
- Haptics and sound policies
- Offline/background execution

Do not create superficial pixel parity across platforms when native behavior differs materially.

## Gesture contract

Define:

- Discoverability and visible affordance
- Start condition, threshold, axis, velocity, and cancellation
- Constraint, resistance, overscroll, and boundary
- Preview of consequence
- Completion and reversal
- Haptic/audio/visual feedback
- Keyboard/button alternative
- Conflict with scrolling, zoom, browser, or assistive gestures

## Microinteraction anatomy

A microinteraction contains:

1. Trigger
2. Rules
3. Feedback
4. Loops and modes

Judge it by purpose:

- Clarifies causality
- Confirms input
- Prevents or explains error
- Maintains spatial continuity
- Communicates progress
- Teaches a new behavior
- Rewards a meaningful milestone

Remove it when it delays frequent work, competes with content, masks latency, becomes repetitive, or depends on motion with no alternative.
