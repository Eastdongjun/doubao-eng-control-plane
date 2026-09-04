# Progressive loading and reference-routing decision

This document governs two different forms of progressive loading:

1. **Skill knowledge loading:** which Design Grandmaster references an Agent reads for a task.
2. **Interface/data loading:** how a designed product reveals code, data, media, fonts, or states over time.

Do not confuse them. Knowledge routing protects context and decision quality; interface loading protects comprehension, stability, accessibility, and performance.

## Contents

1. Loading doctrine
2. Task classification
3. Reference decision matrix
4. Recommended bundles
5. Stop and expansion rules
6. Interface/data loading verdict
7. Decision record template
8. Routing audit

## 1. Loading doctrine

- Load `SKILL.md` when the skill triggers. Do not bulk-load all references.
- Load a reference only when its trigger is present, its decision is unresolved, or its validation evidence is required.
- Existing design-system authority, the actual artifact, and user-supplied evidence come before generic knowledge references.
- Read each selected reference completely. Do not skim fragments and claim the method was applied.
- Expand the set only when a new material risk or decision appears.
- Stop loading when the selected set covers the decisions needed for the current deliverable. More context is not automatically more rigor.

For a simple critique, one or two references may be enough. A high-risk redesign spanning brand, coded implementation, mixed typography, responsive boundaries, and handoff can justifiably load several. The rule is decision coverage, not a fixed count.

## 2. Task classification

At task start, mark each domain `required`, `conditional`, or `not needed`:

- Existing system conformance and visual inheritance
- Taste, aesthetic research, trend, and external theme
- Brand and visual craft
- Layout freshness and composition
- Typography and mixed-script craft
- Atomic system and component structure
- UX strategy, interaction, content, accessibility
- Responsive, motion, data, and interface loading
- Boundary safety
- Prototype/production validation
- Critique, handoff, revision addressing, and sources

Use `required` only when the current task will make or validate that domain's decision. Use `conditional` when evidence may expose the need. Do not load a reference merely because its topic is adjacent.

## 3. Reference decision matrix

| Reference | Load when | Do not load merely because |
|---|---|---|
| `design-system-conformance.md` | An approved design system, Token set, component library, or governed extension exists | The artifact uses CSS variables |
| `visual-inheritance-typography-and-layout.md` | Redesigning an existing product, auditing coded visual drift, or preserving an established language | A new page uses typography |
| `aesthetic-discovery-research.md` | Taste is unresolved; historical, cultural, unfamiliar, premium, or research-led direction is required | The user asks for a clean page |
| `aesthetic-governor.md` | Visual ambition is premium/authored/inevitable or the first plausible direction is not enough | Every routine product screen |
| `visual-trend-atlas.md` | A named period/trend or claim of currentness affects direction | A reference happens to look fashionable |
| `external-theme-translation.md` | The user supplies/selects an independently maintained theme | The category resembles a known theme |
| `visual-craft-grammar.md` | Color, composition, image, interaction expression, or inspiration synthesis is a central decision | Only a small token-compliant component change is needed |
| `layout-intelligence-and-freshness.md` | No visual authority exists, layout feels generic/dated, or materially different structures must compete | A stable approved template is reused correctly |
| `mixed-script-typography-and-creative-composition.md` | CJK/Latin/numeral/icon baselines, editorial hierarchy, image/text composition, masks, positioning, pseudo-elements, or repeated visual tuning are material | A single plain text correction has no layout effect |
| `brand-and-visual-language.md` | Extracting brand truth or defining type, color, imagery, icon, voice, or art direction | Brand rules are already binding and no brand decision changes |
| `atomic-design-system.md` | Creating/restructuring tokens, components, patterns, states, or governance | Styling a one-off artifact without reusable system scope |
| `experience-strategy.md` | Journey, service, emotional arc, or cross-channel experience decisions are required | A bounded visual QA task has no journey impact |
| `interaction-cognition-emotion.md` | Affordance, feedback, cognitive load, recovery, behavioral psychology, or uncertainty/waiting needs design | Static visual composition only |
| `accessibility-content-inclusion.md` | Content, semantics, keyboard/screen reader, localization, RTL, zoom, or inclusive behavior is in scope | Accessibility is assumed solved by a component library without evidence |
| `responsive-motion-data.md` | Responsive transformation, motion system, data visualization, perceived performance, or interface/data loading is material | A static single-viewport graphic is being reviewed |
| `layout-boundary-safety.md` | Runnable multi-viewport UI, sticky/fixed regions, horizontal scroll, full bleed, dense navigation, clipping, or edge-contact review exists | A non-runnable direction note has no geometry claim |
| `artifact-production-validation.md` | Producing HTML, interactive prototypes, decks, motion, or other renderable artifacts | Delivering only a research memo |
| `critique-prototype-handoff.md` | Formal critique, prototype plan, engineering handoff, implementation QA, or readiness verdict is required | Early ideation has no approval claim |
| `visual-location-and-revision-map.md` | Runnable page/screen work will be delivered or receive local visual revisions | A pure strategy document has no visual regions |
| `artifact-templates.md` | A repeatable formal artifact or sidecar record must be emitted | Free-form working notes are enough |
| `canonical-sources.md` | Current standards, canonical implementations, or research-source selection matters | No external factual claim is made |
| `progressive-loading-routing.md` | The task spans multiple domains, routing is ambiguous, or loading/performance itself is under review | A single obvious route is already stated by `SKILL.md` |

## 4. Recommended bundles

These are starting sets, not mandatory packages.

### Governed redesign

Load:

- `design-system-conformance.md`
- `visual-inheritance-typography-and-layout.md`
- Add `mixed-script-typography-and-creative-composition.md` when typography or composition changes
- Add `layout-boundary-safety.md` for runnable responsive work
- Add `visual-location-and-revision-map.md` at delivery

### New high-visual website without approved authority

Load:

- `aesthetic-discovery-research.md`
- `layout-intelligence-and-freshness.md`
- `visual-craft-grammar.md`
- `mixed-script-typography-and-creative-composition.md`
- `artifact-production-validation.md` when building
- `layout-boundary-safety.md` and `visual-location-and-revision-map.md` before delivery

Add `aesthetic-governor.md` only when ambition/risk requires formal visual jury passes. Add `visual-trend-atlas.md` only when a named temporal language affects the work.

### Product feature inside a mature system

Load:

- `design-system-conformance.md`
- `interaction-cognition-emotion.md` if behavior changes
- `accessibility-content-inclusion.md` if semantics/content/input/localization changes
- `critique-prototype-handoff.md` for formal handoff or QA

Do not load deep aesthetic research unless visual authority is genuinely unresolved.

### Editorial or bilingual composition repair

Load:

- `mixed-script-typography-and-creative-composition.md`
- `visual-inheritance-typography-and-layout.md` when inheriting an existing language
- `layout-intelligence-and-freshness.md` when structure is generic or dated
- `layout-boundary-safety.md` for runnable responsive output
- `visual-location-and-revision-map.md` for iterative delivery

### Interface/data progressive loading review

Load:

- `responsive-motion-data.md`
- `interaction-cognition-emotion.md`
- `accessibility-content-inclusion.md`
- `artifact-production-validation.md` for runnable evidence
- `layout-boundary-safety.md` when placeholders, late content, or scroll regions can alter geometry

## 5. Stop and expansion rules

Expand the reference set when:

- A binding authority, external theme, or cultural/trend claim appears.
- Real content exposes mixed-script, wrapping, hierarchy, or localization failure.
- The artifact becomes runnable and makes responsive, loading, interaction, or geometry claims.
- A local revision touches a shared component/token or changes another viewport/state.
- The intended ambition rises from correct/polished to distinctive/authored/inevitable.

Stop and work when:

- Every material decision has a governing reference or project authority.
- Additional references repeat principles without changing the plan, risks, or evidence required.
- The next uncertainty can only be resolved by inspecting content, code, rendering, users, or current external evidence.

Do not use reference loading as a substitute for examining the artifact.

## 6. Interface/data loading verdict

When “progressive loading” refers to the product, classify each delayed resource or region:

| Class | Examples | Default treatment |
|---|---|---|
| Critical meaning/action | Primary heading, price, form state, main action, consent, error | Server-render/preload/prioritize; do not hide behind decorative loading |
| Structural | Layout shell, reserved media box, navigation, table columns | Render stable geometry first; reserve final dimensions |
| Supporting | Secondary article list, recommendations, annotations | Load after critical content with truthful local state |
| Decorative | Ambient media, texture, nonessential motion | Defer, reduce, or omit under constrained conditions |
| User-requested | Tabs, expanded detail, heavy visualization | Load on intent with immediate feedback, cancellation/retry where relevant |

Assign one verdict per resource/region:

- `eager`: required for first comprehension or safe interaction.
- `priority`: load early but may follow the stable shell.
- `deferred-visible`: load when approaching the viewport with reserved geometry.
- `on-intent`: load after a user request; preserve focus, status, cancellation, and recovery.
- `optional`: omit under reduced-data, low-power, or failure without harming the task.
- `forbidden-delay`: legal, safety, price, state, or action information whose delay would mislead or block agency.

For each verdict record dependency, trigger, placeholder, reserved dimensions, announcement, timeout, error/retry, cache/staleness, cancellation, metrics, and reduced-data behavior.

Reject:

- Skeletons that resemble completed content or conceal a stall.
- Late insertion that moves controls or changes the reading target.
- Lazy-loading above-the-fold critical content only to improve a metric superficially.
- Placeholder heights guessed from one viewport or language.
- Essential information available only after hover, animation, or an unannounced request.
- Infinite loading without position, progress, end state, recovery, or accessible alternatives.

## 7. Decision record template

```markdown
# Progressive Loading Decision — [task/artifact]

Task / artifact / version / date / decision owner

## Skill knowledge routing
| Domain decision | Required? | Reference loaded | Why | Evidence/output enabled |
|---|---|---|---|---|
| | Required / Conditional / No | | | |

## Interface/data loading
| Region/resource | User value | Dependency | Verdict | Trigger | Stable placeholder/space | A11y status | Failure/retry | Reduced-data |
|---|---|---|---|---|---|---|---|---|
| | | | eager / priority / deferred-visible / on-intent / optional / forbidden-delay | | | | | |

## Risks and checks
Layout shift / reading-order change / interaction readiness / stale data / timeout / cancellation / analytics

## Verdict
Ready / Ready with conditions / Not ready
```

Emit this record when the user asks for a loading decision, when interface loading materially affects UX, or when a multi-domain task needs an auditable reference-loading rationale. Do not burden every small design task with it.

## 8. Routing audit

Before releasing the skill:

- Every reference file is classified in the decision matrix.
- New references define a clear trigger and a clear non-trigger.
- `SKILL.md` links directly to every reference it expects an Agent to load.
- Recommended bundles remain minimal and do not become mandatory full-load presets.
- Interface loading is routed to UX, accessibility, responsive/performance, production validation, and geometry evidence as needed.
- The routing document changes when reference responsibilities change.
