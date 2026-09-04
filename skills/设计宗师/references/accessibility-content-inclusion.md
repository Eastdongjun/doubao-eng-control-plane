# Accessibility, Content, and Inclusion

Use this module from the start of design, not as a final compliance pass.

## Accessibility frame

Design across the WCAG principles:

- **Perceivable:** text alternatives, adaptable structure, contrast, resize/reflow, captions where relevant
- **Operable:** keyboard, focus, target size, time, motion, navigation
- **Understandable:** language, consistency, error prevention/help, predictable behavior
- **Robust:** semantic structure, accessible names/roles/states, assistive-technology compatibility

Default web target is WCAG 2.2 AA unless a different requirement is declared. Legal compliance varies by jurisdiction; flag legal conclusions for specialist review.

## Semantic-first component design

- Choose the native element that matches the action before styling.
- Define accessible name, role, value/state, description, and announcements.
- Specify focus order, visible focus, keyboard behavior, and focus movement after open/close, validation, navigation, and asynchronous change.
- Use ARIA only when native semantics are insufficient; implementing a role without its keyboard/state contract is incomplete.
- Test with keyboard and at least the relevant screen-reader/platform combination.

## Visual and motor access

- Normal text contrast at least 4.5:1 and large text at least 3:1 for WCAG AA; non-text UI indicators generally need 3:1 where the criterion applies.
- Do not communicate state by color alone.
- Preserve content and function at 200% text resize and required reflow/zoom conditions.
- Keep focus indicators visible and unobscured.
- Provide adequate target size and separation; use platform standards and WCAG 2.2 criteria as the floor.
- Provide alternatives to drag, path-based, hover-only, multi-touch, or device-motion interactions.
- Respect reduced motion and avoid flashing or vestibular triggers.

## Cognitive accessibility

- Use plain, concrete language and stable terminology.
- Keep instructions near the action and preserve them during the task.
- Avoid memory-heavy authentication or repeated data entry when alternatives exist.
- Break complex tasks into meaningful stages with visible progress and review.
- Allow sufficient time, pause/extend controls, and save progress where feasible.
- Make errors specific, constructive, and recoverable.
- Avoid unexpected context changes and sensory overload.

## UX writing

Design content as part of interaction:

- Button labels describe the result (`Save changes`, not `OK`).
- Headings answer the page's primary question.
- Labels remain visible; placeholders show examples only.
- Empty states explain why, impact, and meaningful next action.
- Errors state problem, affected field/action, correction, and preserved work.
- Confirmations state what happened and what can happen next.
- High-stakes actions use explicit objects and consequences.
- Links make sense out of context; avoid “click here.”

Define voice as mechanics with do/don't examples and adapt tone to context: calm for error, clear for risk, restrained for success, supportive for learning.

## Inclusive representation

- Avoid defaulting professional roles, families, bodies, abilities, names, or technology access to one norm.
- Use representative research and imagery without tokenism.
- Support chosen names, pronouns, flexible identity fields, and culturally appropriate formats where relevant.
- Distinguish permanent disability, temporary impairment, and situational limitation; good support often helps all three.
- Evaluate who benefits, who is burdened, who may be excluded, and who lacks appeal or recovery paths.

## Internationalization and localization

- Externalize complete strings; do not concatenate fragments.
- Use locale-aware dates, numbers, currency, units, plurals, names, and addresses.
- Design flexible containers for expansion and contraction; avoid fixed-width text.
- Validate CJK line breaking, font fallback, vertical metrics, and input.
- Use logical layout properties and mirrored flow for RTL; do not mirror directional meaning blindly.
- Localize imagery, examples, legal text, support, and cultural references—not strings alone.
- Do not place essential text inside images.

## Accessibility annotation

For handoff, annotate:

- Semantic element/role
- Accessible name and description
- Heading/landmark structure
- Keyboard behavior and focus order/movement
- State/value and live announcements
- Error association
- Touch target and responsive/reflow behavior
- Reduced-motion alternative
- Alt text or decorative status

## Validation

Automated checks find only a subset. Combine design inspection, code scanning, keyboard testing, screen-reader testing, zoom/reflow, contrast, forced-colors/high-contrast where relevant, reduced motion, and testing with disabled participants for consequential flows.
