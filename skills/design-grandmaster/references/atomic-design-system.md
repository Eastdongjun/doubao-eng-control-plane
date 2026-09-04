# Atomic Design System

Use this module for reusable interface systems, component libraries, tokens, and governance.

## Atomic model

Use the five levels concurrently:

- **Atoms:** irreducible functional UI elements such as label, icon, input, button
- **Molecules:** small single-purpose assemblies such as a labeled field or search control
- **Organisms/patterns:** recognizable sections or domain interactions composed from smaller parts
- **Templates:** structural layouts that define content hierarchy and placement
- **Pages:** real instances with representative content, permissions, data, states, and edge cases

Do not treat this as a linear production sequence or mandatory naming scheme. Many teams are more findable with `Foundations -> Components -> Patterns -> Templates`. Preserve the compositional logic even when the labels change.

## System layers

### Foundations

- Brand principles and experience principles
- Color, typography, spacing, grid, radius, border, elevation, icon, imagery, motion
- Accessibility, content, localization, responsive, and platform rules

### Tokens

Use layers:

1. **Primitive:** raw palette/scale values such as `blue.600`, `space.4`
2. **Semantic:** purpose such as `color.action.primary`, `space.layout.compact`
3. **Component:** exceptional local roles such as `button.primary.background.hover`

Components should consume semantic tokens by default. Add component tokens only when a recurring component decision cannot be expressed cleanly through semantics. Never let token names encode a transient appearance where a purpose exists.

For every token document name, value/mode, role, usage, forbidden use, and code/Figma mapping.

When an approved token system already exists, consume it as a read-only contract. Do not change shared token values, aliases, names, roles, scales, or modes without explicit scoped authorization. Do not use raw or near-token values to tune an instance by eye. A 4-unit foundation does not authorize every multiple of 4; the published token set and semantic role remain authoritative. Read [design-system-conformance.md](design-system-conformance.md) through the routing in `SKILL.md` for baseline locking, audits, and exceptions.

### Components

Define a component contract:

- Purpose and when/not to use
- Anatomy and slot names
- Required and optional content
- Properties and valid combinations
- Default, hover, focus, active, selected, disabled, loading, error, success, read-only states as relevant
- Keyboard, pointer, touch, screen-reader behavior
- Content limits, truncation/wrapping, localization
- Responsive/adaptive behavior
- Token mapping
- Examples and do/don't guidance
- Code parity and test expectations

Avoid mathematical variant explosions. Model independent properties, exclude invalid combinations, and split components when responsibilities diverge.

### Patterns

Patterns encode task and domain behavior: search, authentication, filtering, checkout, permission request, destructive action, data entry, review/approval. Document sequence, content, states, policy, accessibility, and analytics—not only composition.

### Templates and pages

Templates define hierarchy and responsive regions. Pages test the system with:

- Realistic short and long content
- Empty, loading, error, success, and permission states
- Different roles and data volume
- Small/large screens, zoom, and localization
- Light/dark/high-contrast modes when supported

Pages are where system contradictions become visible.

## Naming and organization

- Name by purpose (`Date picker`, `Approval header`) rather than shape (`Rounded card 2`).
- Use shared vocabulary across Figma, code, analytics, documentation, and product requirements.
- Keep layers and slots semantic.
- Distinguish global components from domain patterns.
- Record ownership and maturity: experimental, beta, stable, deprecated.

## Source of truth and parity

Declare source of truth for tokens, components, and documentation. Treat the approved token package/specification as value and semantic truth, and rendered code as behavioral evidence. A shipped mismatch is drift until approved; it does not silently rewrite token intent. Automate synchronization when practical. Audit Figma/code drift, raw and near-token values, token overrides, detached components, duplicate aliases, and inaccessible forks.

## Component lifecycle

1. Local need proven in real product context
2. Pattern comparison and reuse decision
3. API/anatomy/states/accessibility design
4. Figma and code implementation
5. Documentation and tests
6. Pilot adoption
7. Stable release and measurement
8. Change/deprecation/migration

Promote a local pattern when reuse and shared behavior justify the governance cost. Do not centralize every coincidence.

## Governance

- Define contribution criteria, reviewers, decision rights, and service levels.
- Require product-context evidence for new components.
- Require explicit authorization before changing any shared token contract; distinguish local exceptions, new shared tokens, and breaking changes.
- Version changes and publish migrations for breaking behavior.
- Measure coverage, adoption, exceptions, accessibility status, and design-code drift.
- Give teams an escape hatch with documented reason and review date.
- Retire duplicates and stale patterns; a system is curated, not accumulated.

## System health gate

- Foundations have role-based rules, not value lists.
- Components cover behavior and states, not just appearance.
- Patterns match real product tasks.
- Accessibility behavior is testable.
- Representative pages stress the system.
- Figma, code, and documentation agree.
- Contribution and deprecation paths exist.
