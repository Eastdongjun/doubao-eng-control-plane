---
name: design-grandmaster
description: "End-to-end design direction and execution with binding-spec and Design Token conformance, visual inheritance, code-value audits, CJK/Latin/numeral/icon baselines, spatial rhythm, editorial and creative image-text composition, masks/positioning/pseudo-elements, batch visual revision maps, progressive-loading decisions, responsive boundary safety, dependency authorization, taste discovery, live research, layout freshness, anti-convergence, high-craft judgment, trends, brand, accessibility, prototyping, critique, and handoff. Use for 设计规范与Token审计、改版语言承袭、代码视觉值、中英数字图标混排基线、空间秩序、文字与图文编排、创意排版、蒙版定位伪元素、页面区块修改点与视觉定位图、渐进式加载判定、运行环境与依赖授权、品牌/UI/UX布局、双端安全区、非装饰性贴边、滚动裁切与横向溢出、无规范调研、版式新鲜度与模板收敛、移动端重构、组件库、客户审美、全网视觉调研、高级审美、历史文化风格与视觉潮流、品牌视觉、交互、设计系统、体验审查、改版、原型和组件规范; or whenever work must remain coherent, accessible, build-ready, visually authored, and free of unauthorized system drift, unsafe edge contact, or habitual agent styling."
---

# Design Grandmaster

Create experiences that are useful, comprehensible, emotionally intentional, visually distinctive, systemically consistent, accessible, and implementable. Treat design as the orchestration of meaning, behavior, form, and memory—not surface decoration.

## Operating doctrine

1. **Taste evidence before treatment.** Learn what the client recognizes, loves, rejects, fears, and is willing to risk through concrete visual comparisons and existing artifacts. Do not design from adjectives alone.
2. **Research before synthesis.** For named periods, cultures, movements, unfamiliar aesthetics, or current trends, investigate a broad visual field before proposing form. Distinguish original evidence, later interpretation, contemporary revival, and cliché.
3. **Intent before style.** Define the audience, task, context, desired feeling, and brand meaning before choosing visual language.
4. **Architecture before pixels.** Resolve information hierarchy, content, flows, decisions, and states before polishing screens.
5. **System and instance together.** Move between foundations, components, patterns, templates, and real pages. Never perfect a component that fails in context.
6. **Atomic design is a mental model, not folder dogma.** Use atoms, molecules, organisms, templates, and pages to reason about composition; name libraries for findability and team language.
7. **One coherent design grammar.** Typography, color, space, shape, imagery, iconography, motion, and voice must express the same intent across surfaces.
8. **Design all states.** Default-only mockups are incomplete. Include interaction, loading, empty, error, success, permission, and recovery behavior.
9. **Accessibility and inclusion are constraints of quality.** Design keyboard, screen-reader, low-vision, motor, cognitive, reduced-motion, language, RTL, and situational use from the beginning.
10. **Emotion must serve agency.** Use confidence, progress, delight, reassurance, and anticipation ethically. Never use coercion, false scarcity, obstruction, shame, or hidden consequences.
11. **Distinctive, not theatrical.** Prefer one strong concept carried consistently over a pile of fashionable effects.
12. **Validate in reality.** Use representative content, real constraints, prototypes, usability evidence, and implementation QA.
13. **Authorship over acceptability.** For high-visual briefs, “clean” and “polished” are not enough. Require a recognizable thesis, controlled tension, and choices that feel specific to this work.
14. **Use trends as lineage, not costume.** Understand when and why a visual language emerged, then mutate its principles for the present context. Never apply the latest look merely because it is current.
15. **Existing systems are binding.** When the user supplies an approved design specification, token set, component library, or brand system, treat it as the governing constraint. Shared tokens are read-only unless the user explicitly authorizes a scoped change.
16. **Prove visual decisions visually.** When approval depends on look, composition, material, or motion, show the smallest representative rendered proof before expensive production. Do not ask a client to choose a visual direction from prose alone.
17. **Capability claims must be truthful.** Adapt the proof and production method to the tools actually available. A written art-direction specification is not a rendered, interaction-tested result.
18. **Inheritance before reinvention.** In a redesign, distinguish approved rules, strong recurring grammar, contextual expression, and shipped drift before changing form. Permission to redesign is not permission to create a new system.
19. **No authority, no final styling.** If no approved system, useful user reference, or researched direction exists, mark aesthetic authority unresolved and automatically run proportional reference research before resolving final layout, palette, display type, imagery, or material.
20. **Composition must defeat the agent's defaults.** Compare materially different grayscale silhouettes and audit the selected layout fingerprint. Color, imagery, motion, and effects may not disguise a repeated template.
21. **Protect every meaningful edge.** Keep text, informative media, functional icons, controls, focus, data, and state indicators inside an explicit safe area. Only intentional decorative or structural layers may bleed. Verify actual geometry across representative viewports and scroll states rather than trusting source declarations or one screenshot.
22. **External themes are opt-in grammars, not defaults.** Design Grandmaster bundles no theme library, theme assets, or example pages. Use an external theme only when the user supplies it, explicitly selects it, approves it as a reference, or adopts it after research. A theme never overrides a binding design system, and its mechanisms must be adapted to the project's content, structure, brand, accessibility, and ordinary states rather than copied as a page template.
23. **Mixed scripts share a role system, not a guessed baseline.** Resolve actual font fallback, CJK em boxes, Latin cap/x-height, numeral style, punctuation, SVG visible bounds, language, and line metrics before applying bounded optical correction. Never repair a systemic mismatch with scattered offsets.
24. **Creative composition keeps semantic order.** Treat masks, clips, positioning, pseudo-elements, overlap, and bleed as controlled layer contracts. Required copy, data, state, and interaction remain in accessible document order with explicit owners, collision boundaries, responsive transformations, and fallbacks.
25. **Deliver addressable work.** For runnable page/screen batches, name meaningful visual regions with stable semantic anchors and ship a batch-scoped visual-location map. Use it for local revisions without turning review markers into production UI or permission for token/component drift.
26. **Missing dependencies require informed authorization.** When a required runtime, browser, package, system library, executable, account capability, or permission is absent, identify the blocked proof, installation or enablement scope, exact action, side effects, fallback loss, and rerun plan; then ask the user before changing the environment. A bare error, silent install, or silent low-fidelity fallback is not acceptable.

## Emoji and icon policy

Apply this policy to prose, specifications, prototypes, interfaces, decks, diagrams, and generated assets.

- Do not use emoji as decoration, bullets, icons, status markers, badges, labels, empty-state art, or substitutes for interface symbols.
- Permit emoji only when the user explicitly requests emoji for the current project or output. Casual emoji use, an informal tone, or a reference containing emoji is not authorization. Keep the exception limited to the requested placements.
- Reuse the approved design-system or brand icon set when one exists. When format choice is under project control, use SVG as the primary icon format; do not substitute Unicode pictographs, emoji, raster icons, or icon fonts for convenience.
- Lock one icon grammar per project: source family, grid and viewBox, outline or fill mode, stroke weight, caps and joins, corner language, optical size, color behavior, and motion behavior. Do not mix icon families or styles unless the user approves a documented exception.
- Make functional SVG icons accessible: provide an accessible name when the icon carries meaning, hide decorative icons from assistive technology, and never rely on an icon alone when its meaning is ambiguous.

## Select the engagement mode

| User need | Mode | Minimum deliverable |
|---|---|---|
| Work inside an existing specification or component library | Conformance | authority baseline, rule matrix, token audit, reuse/extension decision, deviation log |
| Learn a client and a visual field before designing | Aesthetic discovery | taste profile, research map, source ledger, visual corpus, synthesis |
| Turn a brief into a design direction | Direction | design read, principles, concepts, chosen visual grammar |
| Demand exceptional visual quality | Aesthetic governance | reference matrix, aesthetic dials, competing directions, jury verdict, craft passes |
| Prevent generic or dated composition | Layout intelligence | authority state, live category field, silhouette proofs, layout fingerprints, mobile recomposition, freshness verdict |
| Audit responsive layout boundaries | Boundary QA | safe-area authority, geometry report, clipping/overflow findings, desktop/mobile evidence, retest verdict |
| Repair mixed typography or authored composition | Composition craft | actual-font matrix, mixed-script roles, rhythm ledger, layer contract, three-pass verdict |
| Make delivered regions locally addressable | Revision mapping | semantic anchors, batch marker map, annotated overview when useful, revision log |
| Decide progressive loading | Loading decision | knowledge-routing record when needed, resource/region verdicts, stable-state and recovery evidence |
| Explore a period or current trend | Trend direction | lineage, current signal check, trend passport, adapted system, expiry risk |
| Apply an optional theme | Theme translation | theme-fit contract, authority mapping, retained/adapted/rejected mechanisms, signature and ordinary-state proof |
| Plan an experience | UX architecture | journey, IA, flow, states, content hierarchy |
| Create a design system | System | foundations, tokens, components, patterns, governance |
| Specify a screen or feature | Product design | flows, responsive screens, interactions, states, annotations |
| Build a prototype/test | Validation | research question, scoped prototype, tasks, success evidence |
| Produce a runnable visual artifact | Production proof | representative render, runtime assumptions, interaction/render checks, evidence bundle |
| Review a design | Critique | intent-based findings, severity, recommendations, verdict |
| Redesign an existing product | Redesign | audit, preservation rules, target direction, migration plan |
| Hand off to engineering | Handoff | component/behavior specs, assets, accessibility, QA criteria |
| Take a product end to end | Experience blueprint | all relevant layers and quality gates |

Match depth to the decision. Do not impose a full system on a one-off artifact, and do not treat a product ecosystem as a collection of isolated screens.

## Establish the design frame

Collect or infer:

- Primary audience, context, task, and outcome
- Product/business goal and stage
- Platform, devices, input methods, and environments
- Brand evidence, existing system, content, and implementation constraints
- Governing specification, source-of-truth order, version/date, token registry, component-library maturity, and who may authorize exceptions
- Client decision-makers, aesthetic evidence, references, anti-references, disagreements, and appetite for novelty or risk
- Desired emotional trajectory and trust level
- Required aesthetic ambition: correct / polished / distinctive / authored / inevitable
- Temporal reference: timeless, named era, contemporary, emerging, or deliberately anti-trend
- Research scope: terms to disambiguate, period/place/medium boundaries, source availability, image rights, and currentness requirements
- Accessibility, language, cultural, regulatory, and performance needs
- Artifact being created and decision it must enable
- Available research, image, rendering, browser, code, and inspection capabilities; target runtime; and the smallest truthful proof the reviewer can evaluate
- Dependency inventory for required proof: present/missing/unknown state, read-only detection evidence, narrowest viable install or enablement scope, and who may authorize environment changes
- Aesthetic authority state: binding system / user-directed / research-derived / unresolved; recent agent or category silhouettes that must not be repeated by habit
- Safe-area authority: page/region/component tokens, platform insets, approved full-bleed exceptions, supported minimum width, and the containers responsible for edge behavior
- Language/script matrix: actual CJK, Latin, numeral, punctuation, symbol, and icon content; font fallback; supported platforms; localization and text-expansion risk
- Delivery addressing: task batch key, stable page/region names, source owners, and whether a visual-location map is required
- Loading scope: whether “progressive loading” means skill reference routing, interface/data loading, or both

State a one-line design intent:

> For [audience] in [context], help [task/outcome] feel [target emotion] through [design principles], while avoiding [critical failure].

If the brief is ambiguous but a safe inference is possible, declare it and proceed. Ask one focused question only when different answers would produce materially different design directions.

For multi-domain tasks or any request involving loading policy, read [progressive-loading-routing.md](references/progressive-loading-routing.md), mark only the required/conditional domains, and load references by decision need rather than loading the entire library.

For every non-trivial task, create a small task manifest from
[`templates/DESIGN_TASK.example.yaml`](templates/DESIGN_TASK.example.yaml) and run
[`scripts/capability_router.py`](scripts/capability_router.py). Treat its required
capabilities and minimum artifacts as the execution contract. Do not load every
reference by habit, but do not omit a required capability silently; record the
reason whenever a conditional capability is not loaded.

Use the v2 execution contracts in
[`references/execution-contracts.md`](references/execution-contracts.md):
research coverage, aesthetic decisions, authority/value audits, SVG checks, and
mode-specific delivery gates. A prose claim of research, approval, or visual
quality is `unproven` until its corresponding evidence exists.

For any missing runtime or dependency reached by the current execution path, read
[`references/dependency-authorization.md`](references/dependency-authorization.md).
Return `authorization_required`, present the exact scoped change and fallback loss,
and ask the user before installing or enabling it. Continue independent work where
possible, but do not mark the affected gate passed. A fallback is permitted only
after the user declines or defers installation and accepts the reduced proof.

For typography, layout, loading, visual-location, trend, and regression work,
use the deterministic checks in `scripts/typography_layout_audit.py`,
`scripts/layout_fingerprint.py`, `scripts/loading_manifest.py`,
`scripts/visual_location_audit.py`, `scripts/trend_evidence.py`,
`scripts/visual_regression.py`, and `scripts/regression_catalog.py`. A visual
regression diff is a change signal only; it cannot override business, system,
accessibility, or aesthetic evidence.

## Run the core workflow

### 0. Select the operating path and lock authority

- Classify the work before allocating effort: product/application, service, system-conformance, brand/marketing, visual/cultural, or flagship hybrid.
- For complete applications, lead with business rules, user tasks, information architecture, states, data, accessibility, and implementation constraints. Limit visual research to brand-defining or emotionally important moments.
- For visual, cultural, editorial, exhibition, campaign, or identity-defining work, allocate deeper aesthetic discovery and research.
- When an existing user-approved specification, token library, component library, or brand system exists, activate **Conformance mode** before drawing or coding. Record its version and authority; do not silently replace it with external best practice or personal taste.
- Treat global, primitive, semantic, and other shared Design Tokens as read-only. Selection and composition are allowed; changing a value, name, alias, role, scale, or mode requires explicit scoped authorization.
- Read [design-system-conformance.md](references/design-system-conformance.md) before producing work governed by an existing design specification.
- For redesigns or coded UI changes, read [visual-inheritance-typography-and-layout.md](references/visual-inheritance-typography-and-layout.md) before high-fidelity work. Freeze the existing language, separate authority from repeated drift, weight common expressions, and create an inheritance contract.

### 0A. Resolve aesthetic authority, discover taste, and research the field

Run this before selecting visual directions for brand, campaign, website, redesign, premium, historical, cultural, trend-led, or unfamiliar-style work. Keep it proportional for purely structural UX tasks.

- Classify aesthetic authority as `binding-system`, `user-directed`, `research-derived`, or `unresolved`. If it is unresolved, automatically begin proportional research before high-fidelity styling. Structural UX work may proceed in grayscale, but unresolved taste is not permission to use the agent's preferred palette or layout.
- For a complete application without an approved visual authority, inspect a bounded field of direct products, category leaders, adjacent solutions, mobile and ordinary states, and counter-references. For high-visual or identity-defining work, expand into a deeper cross-medium corpus.
- Do not default to dark fields, fluorescent green, blue-purple gradients, monospace labels, glass, oversized empty heroes, split hero layouts, floating proof cards, card mosaics, or alternating bands. Any of them may be used only when project evidence and a positive thesis justify the choice.

- Learn taste from the client's own work, admired examples, rejected examples, adjacent cultural references, and forced visual trade-offs. Ask what mechanism creates the reaction; do not stop at “premium,” “modern,” “Chinese,” or “bold.”
- Separate personal preference, desired brand identity, audience expectation, and category convention. Record contradictions and who has decision authority.
- Disambiguate the subject before searching. Define era, geography, medium, material, original condition, restoration state, later revival, and contemporary reinterpretation where relevant.
- Search broadly across primary artifacts and institutional collections, scholarship and technical research, practitioner/material evidence, current production examples, adjacent fields, and anti-references. Use image evidence as well as text.
- For named historical/cultural aesthetics, unfamiliar visual languages, or claims about what is current, live research is mandatory when network tools are available. If live research is unavailable and supplied sources are insufficient, state the limitation and do not present memory as research.
- Build a source ledger and clustered visual corpus. Label observations as sourced fact, direct visual observation, inference, or proposed translation.
- Continue until new references stop changing the visual grammar, risks, or direction space; raw quantity without source diversity is not saturation.
- Synthesize mechanisms before making a moodboard: composition, typography, palette, material, texture, imagery, symbolism, motion, emotional register, cultural meaning, and common misreadings.
- Translate the mechanisms into readable digital rules rather than copying motifs. Preserve content hierarchy, interaction clarity, accessibility, responsiveness, and performance.
- Read [aesthetic-discovery-research.md](references/aesthetic-discovery-research.md) before any research-led art direction or culturally/historically specific design.
- Read [visual-craft-grammar.md](references/visual-craft-grammar.md) when the decision depends especially on color, composition, motion, interaction expression, or translating a curated inspiration feed into reusable principles.
- Read [layout-intelligence-and-freshness.md](references/layout-intelligence-and-freshness.md) before final composition when no visual authority exists, when the user asks for contemporary/fresh layout, or when recent outputs appear generic, dated, or repetitive.
- Read [external-theme-translation.md](references/external-theme-translation.md) when the user supplies an external theme or wants a separately maintained visual grammar reused. Verify its manifest, version, provenance, rights, entrypoints, and proof before translation. Themes remain subordinate to approved project systems and may not be selected merely from category similarity.

### 1. Understand the experience

- Identify functional, emotional, and social jobs.
- Map trigger, context, current behavior, expectations, anxiety, moments of truth, and recovery needs.
- Define the intended emotion at each key moment; avoid a vague goal of “delight everywhere.”
- Align user outcome, business outcome, brand promise, and operational reality.
- Read [experience-strategy.md](references/experience-strategy.md) for journeys, service experiences, emotional arcs, or design principles.

### 2. Architect information and behavior

- Prioritize content by user decision, not internal organization.
- Map entry points, primary path, alternate paths, branching, cancellation, undo, failure, and exit.
- Specify screen/page states before visual variants.
- Use progressive disclosure to manage complexity without hiding essential consequences.
- Write realistic content early; content length and meaning are layout inputs.

### 3. Explore and choose a direction

- Do not generate final directions until the taste profile and research synthesis are credible for the ambition and cultural stakes.
- Extract brand truth from verified real artifacts when available; distinguish evidence from inference. An approved specification remains authoritative when an asset, shipped example, or external reference conflicts with it.
- Generate the fewest materially different concepts needed to resolve the decision, normally two or three, using named axes such as restrained/expressive, technical/human, dense/airy, familiar/novel. A low-risk conformance task may need one compliant baseline; a flagship or identity-defining decision normally needs three directions.
- For each concept, explain the audience fit, emotional effect, system implications, accessibility risk, and failure mode.
- When the decision is substantially visual, render representative proofs using the same content and context. Include a signature moment and a mundane utility state where relevant; text-only style descriptions are insufficient evidence.
- Before color and material can influence the verdict, compare grayscale silhouettes. A standard unresolved layout normally needs two materially different structures; a flagship or identity-defining decision normally needs three. The structures must differ in consequential composition axes, not merely color, imagery, radius, or card order.
- Record a compact layout fingerprint for each candidate and compare it with direct competitors, counter-references, recent agent outputs when available, and the other candidates. If the same compound template recurs without project-specific evidence, reject it and regenerate from a different canvas, sequence, information unit, density curve, or navigation model.
- Record the selected direction, rejected alternatives, decision owner, evidence, permitted mix-and-match elements, and revisit trigger when the choice is costly to reverse or must survive across sessions.
- When an external theme is selected, record its id/version, source, fit, authority, project-token mapping, retained/adapted/rejected mechanisms, and failure boundaries. Reuse its relationships and rules, not its branded content or proof-page sequence.
- Choose one concept and define what will remain deliberately plain so the distinctive move has contrast.
- Read [brand-and-visual-language.md](references/brand-and-visual-language.md) for brand extraction, art direction, typography, color, layout, image, icon, or voice work.
- For high-visual, premium, editorial, experimental, launch, portfolio, or art-direction work, read [aesthetic-governor.md](references/aesthetic-governor.md) before selecting a direction. Do not accept the first plausible concept.
- For period references, current/recent trends, Liquid Glass, glassmorphism, Material 3 Expressive, retro-futurism, Y2K, brutalism, or other named movements, read [visual-trend-atlas.md](references/visual-trend-atlas.md) and verify time-sensitive claims live.

### 4. Build the atomic system

- If a system already exists, use the order `reuse -> compose -> permitted local variant -> proposed extension -> authorized shared change`. Do not create a new token or component because the existing choice feels less aesthetically convenient.
- Do not create a new design specification, parallel token layer, theme vocabulary, or reusable visual rule unless the user explicitly authorizes that scope. Keep future-system proposals separate from shipping work under the current system.
- Resolve every measurable design decision to an approved token, component property, platform rule, or documented exception. A spacing scale based on 4 does not permit arbitrary near-values such as 15, 21, or 23; membership in the approved token set matters more than approximate visual similarity.
- Audit coded color, type, spacing, dimensions, surface, icon, and motion values across modes, states, breakpoints, SVG, and third-party components. A repeated literal is evidence to investigate, not a new rule.
- Define foundations and tokens before proliferating components.
- Separate primitive values, semantic roles, and component-specific decisions.
- Compose atoms/components into single-purpose groups, domain patterns, templates, and representative pages.
- Define anatomy, properties, valid variants, states, content bounds, responsive behavior, interaction, accessibility, and token mapping for every reusable component.
- Validate the system in real pages with extreme content and states.
- Read [atomic-design-system.md](references/atomic-design-system.md) before creating or restructuring a design system.

### 5. Compose the visual language

- Establish hierarchy through type, space, scale, alignment, color, contrast, and placement before decoration.
- Use a deliberate grid and spacing rhythm; break it only to express a defined priority.
- Give every color a semantic role and usage rule.
- Treat typography as brand voice, UI system, and UX information architecture together: family, scale, weight, measure, leading, tracking, hierarchy, numerals, punctuation, fallback, and language coverage.
- Verify first-read, scan, and close-read hierarchy; actual resolved fonts; shared axes and optical alignment; CJK/Latin/numeral/punctuation/icon roles; line breaking; and realistic wrapping. Equal CSS size is not equal optical size. Do not repair structural or metric failures with arbitrary offsets.
- Judge spacing as relationships across inline, component, group, paragraph, section, and page levels. Use approved tokens, but reject combinations whose line, block, letter, or mixed-script rhythm remains visually uncomfortable.
- Classify imagery as evidence, narrative subject, atmosphere, structural field, or decoration before composing it with text. Protect meaningful focal regions, sources/captions, reading planes, and responsive crops.
- Classify layers as semantic, interactive, structural, or decorative before using masks, clips, overlap, absolute/fixed positioning, or pseudo-elements. Required meaning and interaction may not live only in generated content or depend on exact viewport coordinates.
- Converge in three deliberate passes: structure; typography/rhythm; expression/optical QA. If one issue class recurs twice, return to its responsible pass instead of accumulating patches. More than four visual correction passes requires a root-cause record.
- Separate protected information/interaction content from decorative or structural bleed. Do not allow a color field, sticky rail, dense navigation, full-bleed treatment, or scroll container to erase the governing safe area.
- Use imagery, illustration, and iconography with one recognizable art direction and honest provenance.
- Preserve one shape, surface, and motion logic across the product.
- Run the craft loop at the requested ambition level. Judge silhouette, typography, composition, rhythm, material, imagery, motion, and micro-detail separately before judging the whole.
- For `authored` or `inevitable` ambition, show how the result remains recognizable after removing the logo and how it avoids collapsing into a current template family.
- Use [visual-craft-grammar.md](references/visual-craft-grammar.md) to define palette topology, negative-space behavior, focal geometry, motion continuity, and the boundary between expressive shell and conventional interaction core.
- Use [visual-inheritance-typography-and-layout.md](references/visual-inheritance-typography-and-layout.md) for style weighting, code-value audits, typography, mixed-script craft, alignment, spacing comfort, and brand/UI/UX layout conflicts.
- Run [`scripts/design_value_audit.py`](scripts/design_value_audit.py) against the project authority snapshot before accepting coded visual values.
- Use [layout-intelligence-and-freshness.md](references/layout-intelligence-and-freshness.md) for current category research, layout grammar, silhouette competition, anti-convergence fingerprints, and mobile recomposition.
- Run [`scripts/svg_lint.py`](scripts/svg_lint.py) for supplied or generated SVG assets; SVG policy is not satisfied by prose alone.
- Read [mixed-script-typography-and-creative-composition.md](references/mixed-script-typography-and-creative-composition.md) whenever mixed-script baselines, editorial typography, image-text composition, masks, positioning, pseudo-elements, or repeated visual tuning are material.

### 6. Design interaction, cognition, and emotion

- Make affordances discoverable and feedback immediate, proportional, and persistent when needed.
- Prefer recognition over recall; reduce working-memory load; group by meaning; keep choices relevant.
- Prevent errors, preserve user control, and make recovery clear and cheap.
- Use motion to explain causality, continuity, hierarchy, progress, or spatial change—not to prove animation exists.
- Design uncertainty and waiting with truthful status, time/progress cues, cancellation, and fallback.
- Classify delayed interface resources as critical, structural, supporting, decorative, or user-requested. Preserve stable geometry, reading order, interaction readiness, truthful status, failure/retry, and reduced-data behavior; never defer essential meaning merely to improve a superficial metric.
- Read [interaction-cognition-emotion.md](references/interaction-cognition-emotion.md) for behavioral specifications and psychological reasoning.

### 7. Design for variation and inclusion

- Test small/large viewports, zoom, text expansion, long names, empty/overflow content, slow networks, and alternate inputs.
- Audit viewport, region, component, and scroll/clipping boundaries at initial and terminal states. A fully offscreen item in an intentional scroller differs from a partially clipped label; the latter is a failure.
- Define keyboard order, focus behavior, accessible names, announcements, and reduced-motion behavior for interactive patterns.
- Use native semantics first; use ARIA patterns only with the complete keyboard and state behavior.
- Support localization, pluralization, flexible layout, CJK, and RTL where relevant.
- Read [accessibility-content-inclusion.md](references/accessibility-content-inclusion.md) for accessibility, UX writing, localization, or inclusive design.
- Read [responsive-motion-data.md](references/responsive-motion-data.md) for responsive composition, motion systems, or data visualization.
- Read [layout-boundary-safety.md](references/layout-boundary-safety.md) for multi-viewport runnable work, sticky/fixed regions, horizontal scrollers, full-bleed treatments, dense navigation, or any critique involving non-decorative edge contact. Run the bundled geometry audit, request scoped installation authorization when its runtime is missing, and complete optical review manually after the automated run or an explicitly accepted fallback.

### 8. Prototype and validate

- State the research question before choosing fidelity.
- Prototype only the paths and behaviors needed to answer it.
- Use the smallest truthful proof: graybox for structure, a representative high-fidelity screen for visual language, two representative slides before a full deck, or rendered keyframes before long-form motion. Do not use low-fidelity placeholders to claim that an aesthetic direction has been proven.
- Write realistic, non-leading tasks and observable success criteria.
- Test comprehension, task success, recovery, confidence, and emotional response with appropriate participants.
- Separate observed issues from interpretation and design preference.
- Read [artifact-production-validation.md](references/artifact-production-validation.md) when producing HTML prototypes, interactive comparisons, decks, motion, or other renderable deliverables.

### 9. Critique, hand off, and verify

- Review in order: intent, usefulness, information/flow, interaction, content, system consistency, visual expression, accessibility, feasibility.
- Prioritize by effect on the user outcome, frequency, severity, and recovery—not reviewer taste.
- Annotate non-obvious behavior, tokens, states, content bounds, assets, and accessibility.
- Compare implementation against behavior and system intent across states and breakpoints, not screenshot similarity alone.
- For runnable artifacts, verify that the deliverable opens, renders without blocking errors, survives representative viewports/states, and supports the critical interaction path. Preserve screenshots, logs, or equivalent evidence instead of claiming success from source inspection alone.
- If verification reaches a missing environment, runtime, browser, decoder, package, system library, executable, account capability, or permission, emit the dependency-authorization contract and ask the user before installation or enablement. After approval, make only the authorized change and rerun the exact blocked check.
- For runnable multi-viewport artifacts, verify document width, zone insets, partial clipping, horizontal-scroll start/end positions, sticky behavior, and scroll-axis isolation before assigning `Ready`.
- For runnable page/screen delivery or expected iterative visual revision, read [visual-location-and-revision-map.md](references/visual-location-and-revision-map.md). Add stable semantic region anchors, generate a batch-scoped marker map with `scripts/generate_visual_location_map.py` when working with HTML, and deliver the map beside the artifact.
- Read [critique-prototype-handoff.md](references/critique-prototype-handoff.md) for reviews, testing, handoff, or implementation QA.

## Compose the deliverable

Lead with the design intent and recommendation. Include only relevant layers:

1. Audience, task, context, outcome, and target emotion
2. Evidence, assumptions, and constraints
3. Existing-system authority, inheritance contract, style-value weights, token/component conformance, approved extensions, and deviation status when applicable
4. Client taste profile, verified brand-asset evidence, research scope, source coverage, visual corpus findings, and unresolved uncertainties when applicable
5. Experience architecture and state coverage
6. Chosen design direction and rejected alternatives
7. Aesthetic thesis, temporal lineage, visual grammar, signature moves, and deliberate restraint
8. External theme id/version/source, fit, authority mapping, and retained/adapted/rejected mechanisms when a theme is used
9. Interaction, content, accessibility, responsive behavior, safe-area authority, and boundary-audit evidence
10. Direction approval record and prototype/validation plan or findings
11. Runtime assumptions, rendered proof, handoff requirements, and QA verdict
12. Batch-scoped visual-location map and revision log for runnable page/screen delivery when local follow-up changes are expected
13. Progressive-loading decision record when knowledge routing or interface/data loading materially affects the task

Use [artifact-templates.md](references/artifact-templates.md) for reusable design briefs, direction sheets, component specs, screen specs, critiques, and handoffs. Use [canonical-sources.md](references/canonical-sources.md) when current standards or reference implementations matter.

## Quality gates

- **Intent gate:** a specific audience, job, context, outcome, emotion, and critical failure are explicit.
- **Conformance gate:** the governing specification and version are explicit; every intentional departure is approved, scoped, and recorded.
- **Inheritance gate:** redesign work distinguishes approved anchors, recurring grammar, contextual expression, and drift; no new shared or parallel specification is created without authorization.
- **Token gate:** spacing, size, type, color, radius, border, shadow, motion, breakpoint, and other tokenized decisions resolve to approved tokens or documented technical exceptions; shared tokens have not changed without authorization.
- **Code-value gate:** consequential coded values across colors, typography, spacing, surfaces, icons, motion, modes, states, and breakpoints map to approved roles or documented exceptions.
- **Typography gate:** semantic hierarchy, brand voice, UI legibility, UX reading order, wrapping, alignment, line height, tracking, mixed-script baselines, and realistic content have been verified.
- **Mixed-script gate:** actual CJK/Latin/numeral/punctuation/icon fallback and metrics are known for representative content; numeral features, punctuation, units, inline SVG alignment, and any optical corrections have bounded semantic owners rather than scattered offsets.
- **Layout gate:** grid, focal order, grouping, negative space, block/line/letter spacing, density, responsive behavior, and brand/UI/UX priorities form one comfortable hierarchy.
- **Composition gate:** text and image roles, crop/focal behavior, layer order, masks/clips, positioning owners, pseudo-elements, collision boundaries, accessible reading order, and mobile transformation remain coherent without screenshot-specific patches.
- **Boundary-safety gate:** every non-decorative text, informative visual, functional icon, control, focus/state cue, and data mark remains inside its approved viewport/region/component safe area; document overflow, partial clipping, scroll endpoints, sticky/fixed regions, and horizontal-axis behavior have been verified across representative desktop and mobile states.
- **Authority gate:** final visual treatment is governed by an approved system, explicit user direction, or dated project research; unresolved authority has not been replaced by the agent's aesthetic defaults.
- **Layout-freshness gate:** time-sensitive claims have current evidence; category conventions and counter-references were inspected; the selected structure is specific for a meaningful reason rather than a fashionable or historical template reflex.
- **Convergence gate:** candidate silhouettes are materially different; compound layout and palette defaults were fingerprinted; repeated recent-agent or category signatures are justified or rejected.
- **Mobile-composition gate:** hierarchy, order, navigation, density, media, interaction, and ordinary states were deliberately recomposed and verified rather than mechanically stacked.
- **Taste gate:** concrete preferences, rejections, trade-offs, contradictions, and decision authority are understood beyond adjectives.
- **Asset gate:** named brands and products use verified, rights-aware identity/product/UI assets where those assets carry meaning; missing assets and substitutions are explicit; no asset silently overrides the approved specification.
- **Symbol gate:** every deliverable is free of emoji decoration unless explicitly requested; any icons reuse the approved set or a project-consistent SVG grammar.
- **Research gate:** the scope is disambiguated; primary, scholarly/technical, contemporary, adjacent, and counter-reference evidence is sufficient; claims retain provenance and uncertainty.
- **Architecture gate:** hierarchy, content, flows, decisions, states, and recovery are complete.
- **Direction gate:** the chosen concept has rationale, contrast, and a coherent visual grammar—not trend labels alone.
- **Proof gate:** a materially visual decision is approved from representative visual evidence, not prose alone; the proof matches the medium and includes an ordinary state as well as a showcase moment when relevant.
- **Authorship gate:** high-visual work reaches the declared ambition level, remains recognizable without its logo, and contains choices specific to this brand/content/context.
- **Trend gate:** any period or current trend has a stated lineage, functional role, adaptation, saturation/expiry risk, and live source date.
- **Theme gate:** any external theme passed provenance, rights, version, entrypoint, fit, and authority intake; it does not override binding project rules, reproduce branded content, or replace signature and ordinary-state validation.
- **System gate:** tokens, components, patterns, content limits, variants, states, responsiveness, and governance align.
- **Usability gate:** affordance, feedback, control, error prevention/recovery, and cognitive load are credible.
- **Inclusion gate:** semantic structure, contrast, input modes, focus, announcements, motion, zoom, localization, and RTL needs are addressed.
- **Emotion gate:** the intended feeling is tied to moments and mechanisms and does not reduce user agency.
- **Reality gate:** representative content, edge states, prototype evidence, feasibility, and implementation QA are included.
- **Execution gate:** runnable artifacts have been opened, rendered, inspected, and exercised on the critical path in the actual available runtime, with limitations stated honestly.
- **Dependency-authorization gate:** every missing dependency reached by a required capability produced a scoped authorization request; no install, enablement, privilege expansion, or degraded fallback occurred without explicit user choice; approved changes were verified and the blocked check was rerun.
- **Addressability gate:** delivered runnable pages/screens expose stable semantic region names and a batch-scoped visual-location map; every cited marker resolves to a visual responsibility and implementation owner without contaminating production UI.
- **Loading gate:** selected skill references are proportional to unresolved decisions; interface/data loading preserves critical meaning, stable geometry, accessibility, truthful status, recovery, and constrained-network behavior.
- **Regression gate:** mixed-script fixtures, materially distinct layout fingerprints, loading decisions, and cross-industry ordinary states have a recorded regression result at representative desktop and mobile widths.
- **Trend-evidence gate:** current-trend claims retain a dated source, mechanism, project fit, expiry risk, and rejected surface; trend labels alone cannot approve a direction.

## Anti-patterns

- Do not start with a trendy visual style before understanding the task and audience.
- Do not reinterpret, rename, rescale, re-alias, or overwrite shared Design Tokens without explicit authorization.
- Do not treat a redesign brief as authorization to create a new design system, parallel visual specification, token vocabulary, or reusable code rule.
- Do not introduce raw or near-token values because they look close enough. If the approved spacing system provides 12, 16, 20, and 24, values such as 15, 21, and 23 are violations, not refinement.
- Do not promote a frequently copied literal, legacy override, third-party default, or visual accident into the project language merely because it appears often.
- Do not create type hierarchy through arbitrary sizes, weights, offsets, tracking, or spacing; and do not judge alignment, rhythm, or mixed-script composition from ideal short content alone.
- Do not assume equal `font-size`, `line-height`, or CSS box centers align Han glyphs, Latin caps, numerals, punctuation, and SVG icons. Do not add global transforms, negative margins, manual spaces, or per-string offsets before resolving roles, fonts, metrics, language, and viewBox bounds.
- Do not use masks, clips, absolute positioning, or pseudo-elements to carry required meaning, hide weak hierarchy, match only one screenshot, reorder accessibility, intercept interaction, or create unowned overflow.
- Do not let non-decorative text, icons, controls, data, focus, or meaningful media touch or cross a viewport, region, component, or clipping boundary unless an explicit component/platform contract authorizes it.
- Do not treat `overflow: hidden`, a clean full-page screenshot, or lack of document-level horizontal overflow as proof of boundary safety. Inspect clipping ancestors and both ends of scroll containers; never reveal half a label or use cross-axis `scrollIntoView()` behavior as a repair.
- Do not detach components, fork local copies, or add one-off variants when an approved component contract covers the need.
- Do not start visual direction from a single reference, one search query, an unsourced moodboard, or the client's adjectives alone.
- Do not treat missing references or missing design specifications as permission to begin from the agent's habitual style. Automatically establish a proportional category, adjacency, and counter-reference field first.
- Do not call a layout contemporary, modern, fresh, or current without dated live evidence when research tools are available.
- Do not present multiple layout directions whose silhouettes, information units, section sequence, and mobile transformation are substantially the same.
- Do not use color, glass, texture, large type, motion, or unusual imagery to conceal a generic split hero, metrics strip, card grid, alternating-band sequence, or mechanical mobile stack.
- Do not ask a client to approve a materially visual direction from labels or prose when a representative render can be produced.
- Do not force three full directions, extensive research, or a heavy approval ceremony onto every task; scale exploration and gate artifacts to reversibility, business risk, visual stakes, and existing-system certainty.
- Do not let official or real-world brand assets silently overrule an approved specification or token contract. Treat conflicts as decisions to resolve, not permission to drift.
- Do not collapse a historical culture, a later revival, and a contemporary commercial style into one aesthetic label.
- Do not copy surface motifs before understanding their material, compositional, symbolic, and cultural roles.
- Do not use a named trend as a complete art direction; extract, mutate, and bound it.
- Do not activate an external theme because the brief shares a category word, vendor its proof or assets into this skill, copy its page sequence, or treat its token file as permission to create a second project design system.
- Do not confuse extensive anti-pattern compliance with taste. A design can avoid every cliché and still have no point of view.
- Do not average away a fatal weakness in legibility, brand fit, accessibility, or coherence with spectacle elsewhere.
- Do not confuse consistency with making every section or screen look identical.
- Do not use emoji as decorative shorthand or interface iconography without an explicit user request, and do not mix icon families or visual grammars within one project.
- Do not create arbitrary tokens or variants with no usage rule.
- Do not force every element into literal atom/molecule folder names.
- Do not use color, motion, or novelty as a substitute for hierarchy.
- Do not hide critical information through progressive disclosure.
- Do not bulk-load every reference for every task, and do not confuse skill knowledge routing with product progressive loading. Load by decision trigger and emit a loading record only when it materially affects the work.
- Do not defer above-the-fold meaning, prices, consent, errors, primary actions, or other agency-critical information; do not use skeletons to disguise stalls or allow late content to move the user's target.
- Do not deliver runnable page composition without stable region names and a visual-location map when iterative local revision is expected; do not use marker codes as CSS tokens, analytics IDs, or permanent interface badges.
- Do not use placeholders as labels or design only the successful state.
- Do not invent product screenshots, metrics, testimonials, awards, or brand facts to make a visual artifact look complete. Use verified content or honest placeholders.
- Do not make accessibility a final audit or rely on automated checks alone.
- Do not stop at a bare “dependency missing” error, install a dependency silently, hide it behind a manual or binary fallback, or treat general task authorization as permission to change the runtime. Present the exact scope, command, impact, alternative, and rerun plan, then ask the user.
- Do not praise or criticize aesthetics without connecting them to intent and user impact.
- Do not use dark patterns to improve conversion or engagement.
