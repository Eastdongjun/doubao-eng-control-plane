# Visual location and revision map

Use this reference for runnable pages, redesigns, multi-screen artifacts, visual QA, handoff, or any delivery expected to receive local follow-up changes. The goal is to make every meaningful visual region addressable across conversations without turning implementation selectors into an unstable annotation system.

## Contents

1. Contract
2. Semantic source anchors
3. Batch marker format
4. Generate the map
5. Visual proof
6. Revision protocol
7. Delivery template
8. Quality rules

## 1. Contract

Create one visual-location map per task batch when the work changes or reviews page composition. Deliver it beside the runnable artifact. The map must connect:

`human-visible region -> batch marker -> page/viewport -> semantic source anchor -> implementation owner`

Do not number arbitrary rectangles from top to bottom without meaning. Name regions by their role in the experience, such as `global-header`, `home.hero`, `home.market-summary`, `article.related-reading`, or `checkout.payment-actions`.

The map is a revision interface, not a new design system. It must not introduce visual tokens, layout values, component variants, or production analytics identifiers.

## 2. Semantic source anchors

Prefer an existing stable page/section/component identifier. For HTML, add a review-safe semantic anchor only when needed:

```html
<section data-vloc="home.hero" data-vloc-name="首页主叙事区">
  ...
</section>
```

Rules:

- Use lowercase dot-separated semantic paths: `[page].[region].[subregion]`.
- Keep names stable while the region keeps the same responsibility; do not rename because its color or position changed.
- Do not encode CSS values, viewport positions, iteration numbers, or personal names in the source anchor.
- Apply anchors to meaningful layout regions, not every wrapper, icon, paragraph, or decorative pseudo-element.
- Repeated items belong to a named collection; identify an individual item only when it has independent revision value.
- Existing project identifiers remain authoritative. Do not duplicate or replace stable Figma frame names, component names, test IDs, CMS block IDs, or application routes.
- `data-vloc` must not become an application behavior dependency. Remove it from production only if the project requires stripping review metadata and the sidecar map retains another stable source locator.

For Figma or non-HTML work, record the page/frame/layer path or the tool's stable node identifier. For component frameworks, include the component/file owner in addition to the rendered anchor.

## 3. Batch marker format

Generate visible revision markers with:

```text
VLM-{BATCH}-{PAGE}-{REGION}-{NN}
```

Example:

```text
VLM-260813A-HOME-HERO-01
```

- `BATCH`: compact task batch chosen once for the current delivery, normally date plus a short sequence or task slug.
- `PAGE`: short stable page/screen key.
- `REGION`: short semantic region key.
- `NN`: collision suffix, not visual order authority.

The generated marker belongs to the delivery batch. The semantic source anchor persists across batches. This distinction lets a reviewer cite an exact delivery while implementation retains stable names.

## 4. Generate the map

For HTML artifacts, mark the meaningful regions and run:

```powershell
python scripts/generate_visual_location_map.py path/to/page.html --batch 260813A --output VISUAL-LOCATION-MAP-260813A.md
```

Optional arguments set the project and page labels. Run once per page and merge maps only when the batch contains multiple pages; preserve unique marker codes.

The generator reads `data-vloc`, `data-vloc-name`, and stable `id` anchors. Prefer explicit `data-vloc` for page regions. A generated document is a starting index: add implementation owner, viewport/state, visual evidence, and revision notes during delivery.

If no runnable HTML exists, create the same document manually from Figma frames, screenshots, slides, or other rendered artifacts.

## 5. Visual proof

When the user is expected to point at regions visually, deliver at least one annotated overview for each materially different responsive composition. Place the marker near the region without obscuring content, interaction, or key geometry. Use a restrained annotation layer separate from the design itself.

The annotated overview is evidence, not production UI. Do not permanently render marker badges inside the product. The sidecar Markdown map remains the textual source of truth.

Record separate marker rows when one semantic region has materially different desktop and mobile composition, or use the same marker with explicit viewport evidence when responsibility and source owner remain identical.

## 6. Revision protocol

When a reviewer cites a marker:

1. Resolve the marker in the delivered map.
2. Confirm the semantic source anchor and implementation owner.
3. Restate the requested local change and its affected viewports/states.
4. Check whether the change propagates through a shared component or token.
5. Refuse silent local patches that would violate a binding system; propose the correct scoped owner.
6. Re-render the changed region plus one upstream/downstream context region.
7. Update status, revision summary, evidence, and any changed marker mapping.

Do not treat “local visual change” as permission to fork a component, add a raw value, or break responsive behavior.

## 7. Delivery template

```markdown
# Visual Location Map — [project / batch]

Batch / date / artifact version / entry point / design-system version

## How to reference
Use the complete marker, for example: `VLM-260813A-HOME-HERO-01`.

## Locations
| Marker | Semantic name | Page/state | Source anchor | Implementation owner | Viewport evidence | Status |
|---|---|---|---|---|---|---|
| | | | | | | Ready / Changed / Needs review |

## Revision log
| Marker | Request | Scope | System impact | Result | Evidence |
|---|---|---|---|---|---|
| | | | None / component / token proposal | | |

## Unmapped or unstable regions
Region / reason / action / owner
```

## 8. Quality rules

- Every marker resolves to one understandable visual responsibility and one source owner.
- Names describe purpose, not current appearance or screen coordinates.
- Markers cover major layout regions and revision hot spots without annotating decorative noise.
- Desktop/mobile divergence and important states are explicit.
- The map and annotated proof match the delivered artifact version.
- Marker overlays never contaminate production screenshots presented as the final design.
- A revision updates the map when ownership, semantics, or composition changes.
- The map is shipped with the artifact rather than retained only in the Agent's conversation context.
