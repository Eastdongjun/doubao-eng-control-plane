# Mixed-script typography and creative composition

Use this reference when Chinese, Latin letters, numerals, punctuation, icons, editorial text, or imagery must share a precise visual system; when a layout needs stronger typographic authorship; or when masks, positioning, pseudo-elements, overlap, cropping, or unusual reading paths are being considered.

## Contents

1. Diagnose before tuning
2. Mixed-script baseline system
3. Spatial order
4. Typographic layout
5. Image-and-text composition
6. Creative composition grammar
7. Responsive and accessible transformation
8. Three-pass convergence loop
9. Acceptance record

## 1. Diagnose before tuning

Separate four kinds of failure before changing values:

| Failure | Evidence | Correct response |
|---|---|---|
| Metric | Baseline, cap height, x-height, ideographic em box, numeral or icon metrics conflict | Choose compatible fonts/features or create a bounded role rule |
| Hierarchy | Readers cannot distinguish first read, scan path, and close read | Reassign roles, scale contrast, placement, and grouping |
| Rhythm | Inline, line, paragraph, block, section, or page intervals feel unrelated | Rebuild the spacing ladder and vertical rhythm |
| Composition | Text and image masses do not create a purposeful focal path | Change canvas, axes, crop, overlap, sequence, or negative space |

Do not begin with isolated `top`, `left`, `letter-spacing`, `line-height`, or `transform` nudges. First capture the real strings, fonts that actually resolved, target viewports, wrapping, writing direction, and intended reading order. Treat browser rendering and screenshots as evidence; source declarations alone do not prove alignment.

## 2. Mixed-script baseline system

### 2.1 Define roles, not one universal baseline

Establish separate but related roles for:

- CJK body and UI text
- Latin body and UI text
- Display/editorial text
- Numerals: proportional, tabular, old-style, or lining
- Punctuation and symbols
- Inline SVG icons
- Superscript, subscript, units, dates, prices, codes, and compact metadata

Use one typographic role for one semantic purpose. A financial table can use tabular lining numerals while an editorial quotation uses proportional old-style numerals; this is intentional role separation, not inconsistency.

### 2.2 Inspect the metric chain

For each role, record:

- Requested family and the font that actually rendered for Han, Latin, numerals, punctuation, and symbols
- Weight availability and whether synthetic bold or italic appeared
- CJK em box, Latin cap height/x-height, ascent, descent, and visible overshoot
- Default numeral style and OpenType support
- Line-gap behavior and fallback changes across platforms
- Icon viewBox, visible bounds, stroke weight, and optical center

Do not assume that equal `font-size` means equal visual size. Do not mix unrelated fallback fonts merely because every glyph is present. Choose a fallback chain whose stroke density, proportions, counters, terminals, and vertical metrics remain compatible.

### 2.3 Author mixed runs deliberately

- Set the language on the document and on materially different runs with `lang`; let shaping and punctuation rules use the correct language.
- Use `font-variant-numeric: tabular-nums` for columns that require comparison; use proportional numerals in prose unless the design role says otherwise.
- Use OpenType features only after verifying support and fallback behavior. Record semantic aliases rather than scattering raw `font-feature-settings`.
- Keep dates, values, units, signs, and currency symbols together when splitting would alter meaning. Use nonbreaking behavior selectively; never create large overflow-prone unbreakable strings.
- Define whether Chinese and Latin punctuation follow the surrounding language, editorial house style, or data syntax. Avoid accidental mixtures of full-width and half-width punctuation.
- Use `text-autospace` only as progressive enhancement after browser and content testing. Do not rely on it as the sole source of CJK–Latin or CJK–numeral spacing.
- Do not insert arbitrary spaces around every Latin or numeric run. Establish a content rule or a bounded inline component when separation is semantically or optically required.

### 2.4 Align icons and exceptional inline objects

Start inline SVG icons with a consistent grid, visible bounds, stroke, `1em` sizing strategy, and `vertical-align` role. Align to the intended text role, not the geometric center of the CSS box.

A small optical correction is allowed only when all are true:

1. The font and icon roles are stable.
2. The correction is expressed through an approved component or semantic token.
3. It survives supported platforms, zoom, and text scaling.
4. It does not hide a wrong line-height, viewBox, or fallback font.

Never apply a global `top`, negative margin, or transform to all Latin, numerals, or icons.

## 3. Spatial order

Build spacing as nested relationships rather than a flat list of gaps:

1. **Glyph and inline:** tracking, word/character boundary, icon gap, value/unit gap.
2. **Line:** leading, multi-line alignment, wrap indentation, baseline rhythm.
3. **Paragraph:** paragraph separation and list rhythm.
4. **Component:** label/control/help/error relationships and internal safe area.
5. **Group:** title/deck/body/action and image/caption relationships.
6. **Section:** chapter transition, density change, and narrative pause.
7. **Page:** outer safe area, focal mass, and overall tempo.

Use approved spacing tokens, but evaluate combinations optically. Token compliance does not guarantee a comfortable relationship. When a valid token pair looks wrong, first check typography, grouping, container width, alignment, content role, and font metrics. Propose a scoped exception only after those causes are excluded; never invent near-token values as a silent repair.

Create a vertical-rhythm ledger for text-heavy work:

| Relationship | Role/token | Actual content tested | Desktop | Mobile | Verdict |
|---|---|---|---|---|---|
| Heading → deck | | | | | |
| Deck → body | | | | | |
| Paragraph → paragraph | | | | | |
| Image → caption | | | | | |
| Section → section | | | | | |

## 4. Typographic layout

### 4.1 Compose reading modes

- **First read:** one dominant proposition, image, fact, or action must win within a thumbnail or two-second glance.
- **Scan:** headings, labels, numbers, rules, and repeated axes reveal structure without reading every sentence.
- **Close read:** line length, leading, contrast, paragraph rhythm, links, notes, and citations sustain comprehension.

Do not let every title, statistic, label, and image compete at the same visual weight. Assign explicit `primary`, `supporting`, `utility`, and `ambient` roles.

### 4.2 Control text measures and rag

- Judge Chinese line length by characters and Latin prose by characters/words, then verify the actual bilingual paragraph rather than applying one nominal width.
- Inspect the shape of the rag, orphaned punctuation, isolated short final lines, headings with a single hanging character, numeric/unit splits, and bilingual line starts.
- Prefer content, width, font role, or controlled line-break opportunities over manual `<br>` tags. Use editorial line breaks only when the copy is stable and provide a responsive alternative.
- Use balanced wrapping selectively for short display text; do not apply it to long prose or interfaces where unpredictable wrapping harms alignment.

### 4.3 Use alignment intentionally

Choose the governing axis for every text block: logical start, centered statement, baseline grid, cap/ideographic edge, or deliberate hanging punctuation. Optical alignment may differ from box alignment, but the exception must be visible, repeatable, and bounded.

Centered body copy, fully justified mixed-script text, scattered absolute-positioned labels, and alternating left/right alignment require a positive editorial reason. They are not automatic signs of creativity.

## 5. Image-and-text composition

Before styling, classify the image role:

- Evidence or product information
- Narrative subject
- Atmosphere or texture
- Structural field
- Decorative accent

Meaningful images keep an understandable crop, caption/source where needed, alt text, and a protected focal region. Decorative images may bleed, mask, or crop more aggressively but must not obscure reading or interaction.

Compose image and text through one dominant relationship:

- Shared edge or baseline
- Counterweight across a field
- Text inset within a quiet image region
- Image interruption of a text rhythm
- Caption/annotation orbit
- Controlled overlap with a protected reading plane

Test the crop with realistic aspect ratios, focal points, localization, text expansion, and mobile recomposition. Do not place text over an image merely because a gradient can make it technically legible.

## 6. Creative composition grammar

Creative layout is a controlled exception system, not unrestricted positioning.

### 6.1 Layer contract

Classify every layer as:

1. **Semantic content:** remains in document order and accessible structure.
2. **Interactive content:** remains focusable, operable, and unobscured.
3. **Structural composition:** grid, region, crop container, or positioning context.
4. **Decorative expression:** masks, pseudo-elements, textures, rules, ambient forms.

Only decorative expression may exist solely in `::before` or `::after`. Never put required copy, state, data, instructions, or actions in generated content. Keep pseudo-elements `pointer-events: none` unless they are part of a correctly implemented control owned by the element.

### 6.2 Positioning contract

For each absolutely or fixed-positioned element, record:

- Owning positioned ancestor
- Anchor edge or focal point
- Collision boundary and safe area
- Stacking context and overlap order
- Content-length assumption
- Desktop and mobile transformation
- Zoom, keyboard, sticky, and reduced-motion behavior where relevant

Reject positioning whose only rationale is matching one screenshot. Prefer grid placement, named grid lines, and container-relative anchors before viewport coordinates. Keep meaningful content in logical reading order even when visually rearranged.

### 6.3 Masks, clips, and pseudo-elements

- Use a mask to express a concept, reveal hierarchy, or integrate image and type—not to hide weak composition.
- Preserve a fallback when mask support, image loading, contrast, or reduced-data mode changes the result.
- Keep informative subjects and text outside destructive clip regions; test extreme aspect ratios.
- Define whether an off-canvas shape is decorative or structural. Decorative overflow belongs to a clipped owner and may not create document overflow.
- Use pseudo-elements for fields, lines, counters, quiet depth, and controlled highlights. Keep their token, stacking, overflow, and responsive rules explicit.
- Audit contrast at every point where a moving, loaded, or responsive background can pass behind text.

## 7. Responsive and accessible transformation

Do not shrink or mechanically stack an authored desktop composition. For each breakpoint decide what is:

- Preserved as the signature
- Reordered to protect reading
- Converted from overlap to flow
- Cropped differently
- Simplified or removed because it is decorative
- Replaced with a more direct interaction

Verify at `320px`, target mobile width, target desktop width, and immediately around material breakpoints. Test browser zoom, text expansion, long Chinese and Latin strings, font loading failure, keyboard focus, and high-contrast/reduced-motion modes.

Visual reordering must not produce a contradictory DOM, focus, or screen-reader order. If the expressive composition cannot remain comprehensible without exact positioning or an image, it is too fragile for essential information.

## 8. Three-pass convergence loop

Use three deliberate passes before open-ended polishing. Do not count every CSS edit as a design iteration.

### Pass A — structure

- Lock real content, information weights, DOM/reading order, canvas, grid, focal mass, text measures, image roles, and mobile transformation.
- Review in grayscale and at thumbnail size.
- Stop if the first-read path or density curve is wrong; decoration cannot repair it.

### Pass B — typography and rhythm

- Confirm actual font fallback, mixed-script baselines, numeral roles, line breaks, leading, paragraph/group/section intervals, and image-caption relationships.
- Compare representative Chinese-only, Latin-only, mixed, numeric-heavy, and long-content states.
- Stop if any role requires repeated one-off offsets.

### Pass C — expression and optical QA

- Add masks, positioning, pseudo-elements, imagery treatment, color, material, and micro-detail within the layer contract.
- Inspect overlap, clipping, stacking, contrast, interaction, breakpoints, loading, reduced modes, and ordinary product states.
- Permit only bounded optical corrections with an owner and rationale.

After Pass C, classify every remaining issue as structural, metric, rhythm, or optical. If the same class reappears twice, return to the responsible pass rather than accumulating patches. A fourth pass is a regression review, not a new aesthetic direction. More than four visual correction passes requires a short root-cause record before continuing.

## 9. Acceptance record

For significant typography or creative-composition work, record:

- Font files/fallbacks actually rendered and platforms checked
- Mixed-script strings, numeric formats, punctuation, icons, and extreme content tested
- First-read, scan, and close-read verdicts
- Text measures, wraps, orphan/rag findings, and spacing ledger
- Image roles, focal/crop behavior, caption/source, and responsive transformation
- Positioned/masked/pseudo-element layer contracts and fallbacks
- Desktop/mobile/zoom/loading/reduced-mode evidence
- Remaining optical exceptions, owner, scope, and rationale

Assign `Ready` only when the composition survives realistic content and supported modes without one-off patch accumulation.
