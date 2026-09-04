# Layout Boundary and Safe-Area Governance

Use this module whenever work is rendered on more than one viewport, contains sticky or fixed regions, horizontal scrolling, full-bleed treatments, dense navigation, edge-aligned content, or a runnable HTML interface. Activate it for design critique and implementation QA as well as production.

The governing rule is:

> Non-decorative content must remain inside an explicit safe area. Only intentional decorative or structural layers may touch or cross a boundary without an inset.

This is not a preference for generous whitespace. Unsafe edge contact can break the grid, content hierarchy, focus visibility, touch behavior, clipping model, responsive contract, and perceived finish at the same time.

## 1. Classify the boundary and the object

Audit four boundary types separately:

1. **Viewport boundary:** the visible browser, device, window, slide, frame, or exported page edge.
2. **Page or region boundary:** the content canvas, header, rail, section, panel, dialog, sheet, footer, or contrasting color field.
3. **Component boundary:** the internal edge of a button, field, row, card, chart, navigation item, or other reusable component.
4. **Scroll or clipping boundary:** any ancestor using `overflow`, masking, clipping, sticky/fixed positioning, carousel behavior, off-canvas placement, or horizontal scrolling.

Treat these objects as protected non-decorative content:

- Headings, body text, captions, labels, numbers, metadata, and legal or status text
- Informative images, charts, data marks, diagrams, and meaningful media crops
- Functional or state-carrying icons, controls, focus rings, badges, active indicators, and affordances
- Brand marks when recognition depends on their complete form and clear space
- Any element required to understand, navigate, decide, recover, or act

Component boundaries protect internal content as well as the component box. In text-bearing controls, audit the placeholder or selected value, prefix/suffix, clear action, validation mark, native or SVG affordance, and focus indicator separately. A field can sit safely inside the page while its own value is visually pressed against its border.

The following may touch or cross a boundary only when the design intent is explicit:

- Background color or material fields
- Rules, separators, reading progress, and grid scaffolding
- Pure ornament, ambient texture, cropped decorative shapes, and non-informative masks
- Full-bleed media whose crop is intentional and does not remove meaning
- A full-width interaction surface whose internal content still obeys the component inset

Do not infer that an object is decorative because it uses `aria-hidden`. An icon can be redundant to assistive technology and still carry visible functional weight. Conversely, do not measure a background rectangle as protected content merely because it is implemented as an element.

## 2. Resolve safe-area authority

Use this order:

1. Approved page, layout, component, and safe-area tokens
2. Platform rules such as `env(safe-area-inset-*)`, device cutouts, window controls, or host chrome
3. Approved component anatomy and clear-space contracts
4. A documented project-local exception
5. A conservative fallback only when no authority exists

Never replace an approved inset with a visually close value. Never create a new shared spacing token merely to repair one boundary defect.

When no system exists, use a 4 px grid and start with:

- `16px` as a hard content floor for compact rails, controls, and utility regions
- `20px` as the preferred small-screen page/major-region inset
- `24px` or more for larger page regions when density and content allow

For selects and other value-bearing triggers without an approved component contract, start with `16px` content inset. Reserve the full trailing composition of value-to-icon gap, icon width, and right inset rather than treating the arrow as overlay decoration. Determine the desktop intrinsic width from the localized placeholder/default and longest built-in option, then add those approved internal zones. At narrow widths, cap the control to the owning region and wrap or recompose the group without reducing its internal safe area or clipping the visible value.

These are fallback starting points, not universal style prescriptions. A denser component can use an approved smaller internal inset, while a brand, editorial, or reading surface may need substantially more. Optical comfort can still fail after a numeric pass.

Record the resolved value and its authority for each audited zone. The test is not “does this look roughly padded?” but “does the measured geometry honor the governing inset?”

## 3. Build the audit matrix

Test the states that can change edge behavior:

- Wide desktop
- A width immediately above and below material breakpoints
- Target mobile width
- Narrow supported mobile width, normally `320px` when the project has no higher declared minimum
- Initial/top state
- Page end
- Both ends of every horizontal scroller
- Sticky/fixed regions before and after they engage
- Open menus, dialogs, sheets, drawers, tooltips, and keyboards where relevant
- Focus-visible state, text expansion/zoom, long content, localization, empty/error/loading states
- Reduced motion when motion changes placement or clipping

Do not call a mobile audit complete after mechanically stacking desktop regions. Recomposition can change the responsible container, safe-area token, reading order, touch target, or scroll axis.

## 4. Run the browser geometry audit

For runnable HTML, use the Python entry point so missing runtimes and browser dependencies become authorization requests rather than bare errors:

```text
python scripts/run_boundary_audit.py <file-or-url> --output BOUNDARY-REPORT.json
```

Useful options:

```text
--viewports 1440x1000,900x900,390x844,320x700
--zones "main>header,main>section,main>footer,nav,aside,[data-boundary-zone]"
--min-inset 16
--ignore ".approved-full-bleed,[data-edge-audit-ignore]"
--browser <chrome-or-chromium-path>
--output boundary-audit.json
```

The script performs this logic:

1. Open the actual file or URL in Chromium.
2. Wait for DOM readiness, bounded font settlement, and the configured stabilization delay.
3. Compare `body.scrollWidth` and `documentElement.scrollWidth` with the viewport width.
4. Measure every visible text line with `Range.getClientRects()` instead of relying only on element boxes.
5. Measure meaningful SVG, image, canvas, video, and explicitly marked audit content.
6. Find the nearest audit zone and resolve its approved or fallback inset.
7. Intersect content geometry with clipping and scroll ancestors.
8. Ignore content that is completely outside a scroller's visible area, but fail content whose glyphs or meaningful geometry are only partially visible.
9. Measure left, right, top, and bottom gaps to the responsible zone and horizontal gaps to the viewport.
10. Repeat at page end and at the end of horizontal scroll containers.
11. Report the viewport, state, object, zone, measured gaps, expected inset, clipping ancestor, and severity.

Automation is evidence, not the verdict by itself. Follow it with screenshot inspection because perceived edge tension, focus-ring clearance, mixed-script side bearings, shadow clipping, and intentional visual bleed require judgment.

The entry point checks Node.js, Playwright, a usable browser executable, and required browser system libraries. When one is missing it writes `status: authorization_required`, exit code `3`, the exact scoped installation command, environment impact, fallback loss, and a user-facing authorization question. The Agent must present that request and wait for explicit approval before installation. After approval, install only the authorized item and rerun the same matrix.

## 5. Treat partial visibility as a separate failure

Horizontal navigation and carousels often pass document-overflow checks while still showing half a label or clipping the last glyph against the viewport.

Use these rules:

- Completely offscreen items inside an intentional scroller are not edge violations by themselves.
- Partially visible text, icons, data, or controls are violations unless the partial object is an explicit, comprehensible affordance and no meaningful glyph or control is clipped.
- Placeholder or selected-value text touching a field edge is a component-boundary failure even when the control itself fits the viewport. An overlaid select arrow does not excuse a reduced trailing text safe area.
- If a “peek” communicates more content, reveal a bounded surface, image edge, or masked container—not half a word, number, icon, or focus target.
- Provide start and end scroll padding so the first and last complete items can rest inside the safe area.
- Do not shrink touch targets or type below the approved minimum merely to make every item fit.
- Keep horizontal adjustment isolated to the horizontal scroller. Verify that revealing the active item does not alter page `scrollY` or reset the active section.

Avoid using `scrollIntoView()` without proving both axes. It can move the page vertically while trying to reveal an item horizontally. Prefer scroller-local `scrollLeft`/`scrollTo` logic or an equivalent axis-isolated implementation, then test initial and terminal states.

## 6. Classify findings

Use these verdicts:

- **Blocker:** required content/control is unreachable, fully clipped, or outside the supported viewport; document overflow blocks normal use.
- **High:** meaningful text, icon, focus, data, or control is partially clipped; an active state cannot rest inside the safe area; horizontal correction changes the wrong axis.
- **Medium:** measured content gap is below the governing inset; the responsible region lacks an explicit safe-area contract; desktop and mobile use inconsistent unapproved boundary logic.
- **Low:** numeric conformance passes but optical edge tension, mixed-script side bearings, visual mass, or decorative bleed still reduces finish.

A runnable artifact is not `Ready` while blocker, high, or unresolved token-governance failures remain. Medium findings require correction or an approved, documented exception.

## 7. Repair in the responsible layer

Use this sequence:

1. Identify the nearest container that owns the boundary.
2. Confirm the governing token, component rule, safe-area value, and breakpoint behavior.
3. Restore the inset at that container or recompose the region.
4. For value-bearing controls, size from localized default and option content, then reserve explicit start inset, text-to-affordance gap, affordance width, and end inset.
5. For scroll regions, add start/end breathing room and verify complete resting positions.
6. Preserve minimum touch targets, text size, reading measure, and focus clearance.
7. Remove axis-coupled scrolling and arbitrary corrective transforms.
8. Re-run geometry checks and inspect screenshots at the same states.

Do not repair systemic edge failures with per-child magic margins, negative offsets, text scaling, hidden overflow, arbitrary `calc()` values, or a breakpoint that only matches the current screenshot. Do not convert a local exception into a shared token without authorization.

## 8. Record evidence

Use a compact ledger:

| Viewport/state | Object | Responsible zone | Measured gaps | Required inset | Finding | Fix | Retest |
|---|---|---|---|---|---|---|---|
| `390x844 / initial` | last nav label | sticky top nav | right `6.6px` | `16px` | partial edge contact | add end padding; hide full item until visible | pass |
| `1440x1000 / initial` | rail issue text | desktop rail | right `6.5px` | `16px` | below safe area | widen rail using approved grid value | pass |

Preserve, when proportional:

- Browser/runtime and entry point
- Viewports and states
- Zone selector or design-frame mapping
- Resolved inset authority
- JSON audit output
- Representative before/after screenshots
- Manual optical verdict
- Approved exceptions and owner

## 9. Manual fallback

Use this fallback only after the dependency-authorization request has been presented and the user explicitly declines or defers installation, or when the capability cannot legally or technically be installed. Record that choice and keep browser geometry `unproven`.

Then:

1. Open the actual artifact at the audit matrix widths.
2. Enable rulers, layout overlays, or computed-style inspection where possible.
3. Measure the nearest meaningful content on all four sides of each major zone.
4. Inspect scroll containers at both ends and focus every material control.
5. Compare the measured values with the token/component contract.
6. Capture screenshots and record untested states explicitly.

Do not claim geometric verification from source inspection alone. CSS declarations can be overridden, affected by font metrics, changed by runtime content, or invalidated by sticky and overflow behavior. A missing runtime may not be hidden behind this fallback without first giving the user an informed choice.
