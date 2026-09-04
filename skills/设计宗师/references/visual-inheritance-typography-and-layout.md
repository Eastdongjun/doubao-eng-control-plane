# Visual Inheritance, Typography, and Layout Control

Use this module for redesigns, visual refactors, coded UI changes, brand refreshes inside an existing product, or any task where the result must inherit an established design language. The purpose is to distinguish system truth from repeated drift, preserve the visual equity that matters, and improve typography and layout without inventing an unauthorized replacement system.

## Contents

1. Freeze authority before redesign
2. Inventory the visual language
3. Find commonality and assign expression weight
4. Create an inheritance contract
5. Audit coded values
6. Direct typography through brand, UI, and UX
7. Control alignment and mixed-script composition
8. Judge spacing as relationships
9. Compose layout through three lenses
10. Verify inheritance and craft

## 1. Freeze authority before redesign

Record the approved specification, token package, Figma library, component library, brand assets, shipped product version, owners, and precedence. Classify each source as authoritative, approved local, shipped observation, deprecated, conflicting, or unknown.

Apply these defaults:

- Redesign authorization is not authorization to create a new design system.
- A new page, local component, CSS variable, theme object, or utility alias can still create a new rule. Naming it “local” does not make it harmless.
- Do not create, rename, rescale, re-alias, or reinterpret tokens, type styles, color roles, grids, elevations, radii, icons, or motion rules without explicit scoped approval.
- Separate a proposed future system from the product changes that can ship under the current system.
- Treat frequent hard-coded values as evidence to investigate, not automatic design truth.

If authority is missing or contradictory, preserve the least-destructive common grammar, label uncertainty, and seek a decision before changing identity-defining or shared rules.

## 2. Inventory the visual language

Inspect design and code together.

### Design sources

- Variables, styles, libraries, components, variants, local overrides, detached instances
- Page and template grids, content widths, gutters, breakpoints, density modes
- Type families, fallbacks, semantic styles, numerals, leading, tracking, paragraph spacing
- Primitive, semantic, component, brand, theme, and mode colors
- Radius, border, divider, elevation, blur, translucency, texture, and material
- Icon family, stroke/fill logic, image/illustration treatment, motion and sound

### Code sources

- CSS custom properties, preprocessors, theme objects, utility configuration, token packages
- Literal colors, gradients, opacities, font sizes, line heights, letter spacing, spacing, dimensions, radii, borders, shadows, filters, transforms, timing, and easing
- Component defaults, variants, pseudo-states, responsive rules, themes, modes, and platform branches
- Inline styles, SVG presentation values, canvas/WebGL constants, generated styles, and third-party defaults
- Actual computed styles at representative states and viewports

For each consequential value, record source, semantic role, surfaces, recurrence, state/mode coverage, token mapping, and authority status.

## 3. Find commonality and assign expression weight

Do not average every observed value. First remove known unauthorized drift, experiments, deprecated artifacts, browser defaults, and one-off emergency fixes from the inheritance candidate set.

Use this precedence:

`approved authority -> semantic consistency -> recurrence -> surface coverage -> brand salience -> current maintained use`

Approved rules win without scoring. Unauthorized values do not become valid through repetition. Use the weighted evidence model only when the approved system is incomplete or several shipped expressions conflict.

| Evidence dimension | Default weight | Question |
|---|---:|---|
| Authority and approval | 30 | Is it explicitly approved or owned? |
| Semantic consistency | 20 | Does the value keep the same role across contexts? |
| Recurrence | 15 | Is it repeated intentionally rather than copied accidentally? |
| Surface and state coverage | 15 | Does it work across pages, components, themes, and states? |
| Brand salience | 15 | Does it materially carry recognition or personality? |
| Current maintained use | 5 | Is it present in the current product rather than legacy residue? |

Score each dimension from `0` to `5`, multiply by its weight share, and retain the evidence beside the score. The number organizes investigation; it does not grant permission.

Classify the result:

- **A — identity anchor:** approved or strongly evidenced; preserve unless change is explicitly authorized
- **B — system grammar:** recurrent and semantically stable; inherit and map to approved roles
- **C — contextual expression:** useful in a bounded product, campaign, density, or content context
- **D — weak signal:** inconsistent, narrow, or insufficiently evidenced; do not generalize
- **X — drift or conflict:** unauthorized, near-token, semantically wrong, inaccessible, or contradictory; remove or escalate

Create separate weights for each design dimension. A product may have strong typography inheritance but weak shadow consistency; one average score would hide that difference.

## 4. Create an inheritance contract

Before high-fidelity redesign or coding, write:

| Dimension | Governing source | Inheritance class | Locked roles | Selectable range | Known drift | Authorized change |
|---|---|---|---|---|---|---|
| Color | | | | | | |
| Typography | | | | | | |
| Grid/layout | | | | | | |
| Spacing/density | | | | | | |
| Shape/surface | | | | | | |
| Icon/image | | | | | | |
| Motion | | | | | | |

For each proposed change state whether it is:

- Reuse of an approved rule
- Recomposition of approved parts
- Selection of an approved mode or variant
- Product-local expression within existing constraints
- Proposed exception awaiting authorization
- Proposed future system change kept outside the shipping implementation

If many desired changes require exceptions, reject or narrow the direction before weakening the system.

## 5. Audit coded values

Resolve every consequential coded value to one of:

1. Approved token and correct semantic role
2. Approved component or platform rule
3. Authorized product-local value
4. Documented technical calculation or environment exception
5. Unauthorized drift that must not ship

Audit all states, modes, breakpoints, overlays, portals, charts, SVG, focus rings, validation, disabled content, and third-party components. A clean default screenshot can hide extensive drift.

### Color

- Map every literal and generated color to an approved semantic role.
- Inspect alpha composition, gradient stops, shadows, borders, selection, focus, charts, icons, and images, not only flat fills.
- A hex value that equals a token still fails when it bypasses the token or uses the wrong semantic role.
- Do not introduce a new palette because the redesign direction needs colors the system does not authorize.

### Other visual values

Apply the same membership and role check to typography, spacing, dimensions, radius, border, shadow, blur, opacity, z-index, icon size, motion, and breakpoints.

Treat a new reusable CSS custom property or theme entry as a token proposal. Do not create it silently.

## 6. Direct typography through brand, UI, and UX

Review every typographic decision through three lenses.

### Brand lens

- Does the type voice express the brand without relying on the logo?
- Which family, contrast, proportion, case, numeral, punctuation, or display behavior is recognition-critical?
- Is distinctiveness concentrated in appropriate moments rather than imposed on routine controls?
- Does the hierarchy feel native to the brand rather than copied from a current template?

### UI lens

- Are roles stable across screens, components, states, and responsive modes?
- Are labels, controls, tables, data, captions, links, errors, and disabled states legible at actual density?
- Do weight, size, color, and spacing combine intentionally instead of competing?
- Are type styles tokenized and limited to real semantic roles?

### UX lens

- Can the user identify context, status, primary information, consequence, and next action in the intended reading sequence?
- Does the hierarchy reduce decision effort rather than merely look dramatic?
- Does long, short, localized, dynamic, empty, and error content preserve meaning?
- Are critical terms, costs, permissions, risks, and recovery paths visible without visual noise?

Build a role ledger:

| Role | User job | Brand voice | Family/fallback | Approved style token | Measure/wrap | Emphasis rule |
|---|---|---|---|---|---|---|

Use the fewest roles that preserve meaning. Do not create a new text style for a single screen, and do not use tiny, light, low-contrast, all-caps, or widely tracked text as a substitute for hierarchy.

## 7. Control alignment and mixed-script composition

Prevent wrong alignment by inspecting:

- Shared left/right edges, centers, cap lines, baselines, columns, and container axes
- Optical centering for icons, numerals, punctuation, circular forms, and asymmetric marks
- Baseline compatibility between CJK, Latin, Arabic, numerals, symbols, units, and inline icons
- Full-width and half-width punctuation, line-breaking, orphaned punctuation, non-breaking groups, and fallback-font metric changes
- Table alignment, decimal alignment, dates, units, prices, codes, and comparison rows
- Heading wraps, widow/orphan behavior, truncation, clamping, tooltip or expansion behavior

Do not “fix” alignment with arbitrary offsets. Correct structure, token selection, font metrics, line box, or component anatomy first. Any optical correction must be bounded, documented, and tested across content and scale.

Judge type hierarchy at three distances:

- **First read:** context, dominant message, and primary action are identifiable
- **Scan:** sections, labels, comparison points, and status can be located quickly
- **Close read:** rhythm, punctuation, alignment, wrapping, and mixed-script craft remain stable

## 8. Judge spacing as relationships

Separate:

- Inline and icon-label spacing
- Intra-component spacing
- Inter-component and group spacing
- Paragraph and text-block spacing
- Section spacing
- Page/container margins and gutters

Evaluate relational rhythm before individual numbers:

- Related elements usually sit closer than unrelated groups.
- Internal spacing, group spacing, and section spacing must be perceptibly distinct when they serve different hierarchy levels.
- Line height, paragraph spacing, and block spacing must work together; increasing all three produces loose, fragmented reading.
- Letter spacing must respect typeface, script, case, size, weight, and rendering. Do not apply one tracking value to all scripts or roles.
- Density must match task frequency and content complexity. Spacious marketing rhythm should not leak into operational tables; dense product rhythm should not flatten a brand moment.
- Repeated vertical gaps should create a stable rhythm across real content, not only the ideal mockup.

Use approved spacing and typography tokens first. If the existing system cannot produce a comfortable relationship, document the exact conflict and propose the smallest scoped change; do not tune raw values until it looks right.

## 9. Compose layout through three lenses

### Brand layout

Preserve recognizable composition traits: scale contrast, grid behavior, negative-space character, image relationship, signature alignment, and controlled irregularity.

### UI layout

Maintain component anatomy, predictable control placement, responsive constraints, state stability, and implementation efficiency.

### UX layout

Sequence information and actions according to the user’s decision, frequency, risk, and recovery needs. Put evidence near the choice it changes. Keep persistent context stable.

Resolve conflicts explicitly:

- Brand emphasis may own a signature moment but must not obscure the primary task.
- Business emphasis must be visible when material but cannot impersonate user priority or hide cost and consequence.
- A visually balanced composition can still fail if reading order, grouping, control proximity, or focus order is wrong.
- A perfectly aligned grid can still feel uncomfortable when text measure, density, and negative-space roles are incoherent.

Use one declared focal priority per task state unless comparison itself requires parallel emphasis. Let secondary and background information remain available without competing.

## 10. Verify inheritance and craft

Review:

1. Approved baseline and inheritance contract
2. Style-value ledger and weighting evidence
3. Token and component mapping in design and code
4. Color, type, spacing, surface, icon, and motion drift
5. First-read, scan, and close-read hierarchy
6. Alignment overlays, baseline behavior, and mixed-script content
7. Real content, localization, zoom, responsive modes, themes, and edge states
8. Brand recognition, routine UI clarity, and task completion

Block release when:

- A shared or reusable visual rule was created without authorization.
- Consequential coded values cannot be mapped to an approved role or documented exception.
- Repeated drift has been mistaken for a system rule.
- Typography hierarchy, alignment, wrapping, line height, tracking, or spacing fails representative content.
- The redesign looks coherent in isolation but no longer belongs to the original product.

Conformance is necessary but not sufficient. The final result must inherit the approved language and improve composition within it.
