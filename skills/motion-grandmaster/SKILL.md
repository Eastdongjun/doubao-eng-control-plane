---
name: motion-grandmaster
description: "Aesthetic direction and production design for motion across product interaction, brand systems, websites, launch moments, kinetic typography, spatial transitions, animation, and video. Use for 动效设计、交互动效、微动效、页面转场、品牌动效、动态视觉、动态排版、标题序列、镜头、节奏、缓动、弹簧、物理感、材质运动、滚动叙事、手势、加载、反馈、签名时刻、Motion Token、动效规范、故事板、动画原型、动效审美评审、Motion、Anime.js、React Spring、AutoAnimate、SVG.js、ManimGL、Lottie、Rive、Lenis、Three.js、React Three Fiber、Motion Canvas、React Native Reanimated、CSS、WebGL，or when motion must feel intentional, distinctive, accessible, performant, system-compliant, and production-ready rather than merely animated."
---

# Motion Grandmaster

Direct time, attention, energy, and change as one coherent visual language. Use motion to explain, orient, persuade, express, and make moments memorable—never to fill silence.

## Operating doctrine

1. **Stillness is a motion decision.** Begin by deciding what must move, what may move, and what must remain stable.
2. **Aesthetic thesis before presets.** Define the motion personality, emotional arc, temporal hierarchy, and signature behavior before selecting libraries or easing curves.
3. **Purpose before spectacle.** Every movement must clarify causality, continuity, hierarchy, progress, physical manipulation, narrative, or brand meaning.
4. **Attention is a budget.** Frequent and task-critical interactions receive restraint; identity-defining and rare moments may receive greater expression.
5. **Time is composition.** Judge rhythm, pause, overlap, counterpoint, acceleration, and sequence as deliberately as typography and layout.
6. **Material implies motion.** Weight, friction, elasticity, viscosity, rigidity, depth, and light behavior must agree. Do not mix incompatible physical metaphors casually.
7. **Continuity preserves comprehension.** Show where objects come from, what they become, and where attention should go next.
8. **Brand has kinetic behavior.** Translate brand attributes into repeatable temporal traits, not a logo sting pasted onto generic UI animation.
9. **Trends are research material.** Study their lineage, mechanisms, current use, and expiry risk. Liquid glass, hyperreal 3D, kinetic type, Y2K motion, editorial scroll, generative particles, and other looks are options—not defaults.
10. **Existing systems are binding.** Approved motion tokens, component behavior, accessibility rules, and brand standards are read-only unless the user authorizes a scoped change.
11. **Prototype the actual temporal risk.** Static keyframes cannot prove timing, continuity, gesture, compositing, or runtime performance.
12. **Reduced motion preserves meaning.** Adapt the transition while retaining state, causality, hierarchy, and completion evidence.
13. **Sound and haptics are not decoration.** Use them only when context, permission, repetition, latency, and accessibility support them.
14. **A memorable moment needs contrast.** If everything performs, nothing feels authored.
15. **Production truth matters.** A beautiful reference is not a solution until it survives target content, device, input, performance, and implementation constraints.
16. **Libraries implement; they do not art-direct.** Reuse the existing stack first, select one primary owner for each behavior, and never let a demo or preset define the project’s motion language.

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
| Work inside an approved motion system | Conformance | authority baseline, token/pattern mapping, deviations, QA |
| Decide how a product or brand should move | Motion direction | taste profile, reference field, motion thesis, aesthetic dials |
| Add motion to a task or component | Interaction motion | purpose, trigger, continuity, timing, states, reduced-motion behavior |
| Create a memorable product moment | Signature moment | narrative beat, visual mechanism, restraint plan, prototype, success evidence |
| Design a brand or campaign sequence | Expressive motion | concept, storyboard/animatic, type/camera/material/sound grammar |
| Build a motion design system | Motion system | principles, tokens, patterns, governance, examples, migration |
| Create scrolling or spatial storytelling | Choreography | scene architecture, attention path, transitions, pacing, control |
| Choose a production technique | Technical direction | fidelity needs, engine route, asset plan, performance budget, fallback |
| Review existing motion | Critique | intent-based aesthetic and functional findings, severity, remedies |
| Hand off animation | Delivery | spec, curves/springs, assets, state logic, reduced motion, acceptance |
| Take motion end to end | Motion blueprint | all relevant stages with approval gates |

Select one primary mode. Do not impose cinematic research on routine application work or reduce a brand-defining sequence to UI transition tokens.

## Establish the motion frame

Collect or infer:

- Audience, context, task, and business/brand outcome
- Project type: application, website, product launch, brand, campaign, installation, title sequence, data story, or hybrid
- Frequency, duration, consequence, interruption, and input relationship
- Existing design, brand, motion system, token registry, version, and authority
- Client references, anti-references, admired motion, disliked motion, vocabulary, and appetite for novelty
- Desired emotional trajectory and motion ambition: quiet / polished / distinctive / authored / spectacular
- Temporal reference: timeless, historical, current, emerging, nostalgic, or deliberately anti-trend
- Platform, viewport, frame rate, device class, input, audio context, and runtime
- Content variability, localization, accessibility, reduced-motion, and performance needs
- Available rendering, browser, code, video, audio, and inspection tools
- Approval decision and smallest truthful proof required

Write a motion intent:

> For [audience] during [moment], make [change or message] feel [qualities] through [temporal/material principles], while preserving [stable context] and avoiding [failure].

## Run the core workflow

### 0. Classify the work and lock authority

- Distinguish **interaction motion** from **narrative animation**. Interaction motion responds to user or system state in real time; narrative animation shapes a time-based sequence. A project may contain both, but they require different controls and tests.
- For complete applications, prioritize comprehension, responsiveness, continuity, accessibility, and frequency. Allocate expressive motion only to moments that define identity or improve understanding.
- For brand, editorial, campaign, title, cultural, or visual-first work, allocate deeper research, composition, and art direction.
- Record the governing design/motion system, source-of-truth order, approved tokens, component contracts, and authorization owner.
- Treat shared motion tokens and global behavior as read-only. Use `reuse -> compose -> permitted local variant -> proposed extension -> authorized shared change`.
- Read [motion-system-and-token-governance.md](references/motion-system-and-token-governance.md) when a system exists or reusable motion is being created.

### 1. Discover taste and research the motion field

- Learn taste from concrete clips, products, films, title sequences, performances, interfaces, graphics, music, physical materials, and anti-references. Ask what quality causes the reaction.
- Separate personal taste, intended brand personality, audience expectation, category convention, and implementation appetite.
- For named movements, periods, cultures, unfamiliar motion languages, or claims about what is current, perform live research when network tools are available. Distinguish source artifact, later interpretation, current revival, and cliché.
- Build a diverse reference field across functional product motion, graphic motion, cinema/editing, typography, physical material, sound/rhythm, and adjacent art. Do not let one social feed define the field.
- Extract mechanisms rather than copying shots: rhythm, hierarchy, continuity, spatial logic, mass, deformation, palette behavior, type movement, camera, edit, sound relationship, and emotional arc.
- Stop when new sources no longer change the direction space, risk, or motion grammar.
- Scale effort: light reference calibration for routine flows; focused comparative research for signature moments; deep field research for identity-defining or culturally specific work.
- Read [aesthetic-direction-and-research.md](references/aesthetic-direction-and-research.md) before choosing a high-ambition or trend-led direction.

### 2. Write the motion thesis

- Define the brand/product’s kinetic personality in behavioral terms.
- Set aesthetic dials: restrained/expressive, precise/organic, light/heavy, crisp/viscous, continuous/cut, calm/urgent, flat/spatial, synchronized/polyphonic, literal/abstract, familiar/novel.
- Define motion invariants: traits that remain consistent across scales.
- Define temporal hierarchy: what moves first, most, longest, and least.
- Identify one signature move, one supporting rhythm, and one rule of stillness.
- Define anti-goals and reference traps.
- Produce two or three materially different theses only when the decision justifies comparison; one compliant baseline is enough for low-risk conformance work.

### 3. Compose time and attention

- Build beats before frames: anticipation, action, reaction, settle, hold, release.
- Establish tempo, duration families, pauses, overlaps, stagger logic, acceleration profile, and density.
- Use hierarchy to sequence attention, not decorative cascades.
- Maintain stable anchors during change so the user can track identity and location.
- For longer sequences, design acts, contrast, escalation, breath, climax, and resolution.
- Read [timing-rhythm-and-choreography.md](references/timing-rhythm-and-choreography.md) for temporal composition, stagger, scrolling, and narrative structure.

### 4. Define physicality, material, and spatial logic

- Choose the implied material and its response: rigid, hinged, paper-like, elastic, magnetic, inertial, liquid, gaseous, granular, optical, or deliberately abstract.
- Align acceleration, deformation, blur, parallax, reflection, refraction, shadow, and sound with the chosen material.
- Preserve topology and object identity through transformation unless rupture is the concept.
- Use springs for interruptible, state-seeking behavior; use duration/easing for authored time; use simulation only when physical variation matters.
- Avoid decorative physics that fights the interaction model.
- Read [physicality-material-and-transition.md](references/physicality-material-and-transition.md) before designing spatial, glass, elastic, particle, or transformation-heavy motion.

### 5. Design interactive motion and signature moments

- Specify trigger, input coupling, latency, progress, constraint, cancellation, reversal, completion, and interruption.
- Keep direct manipulation responsive and interruptible.
- Use transition motion to explain source, destination, hierarchy, and change in scope.
- Match celebration to significance and frequency.
- Reserve signature moments for high-value transitions such as first success, creation, reveal, milestone, identity handoff, or launch—not routine toggles.
- Limit a product to a small family of recognizable moves; a signature moment must still belong to the system.
- Read [interactive-motion-and-signature-moments.md](references/interactive-motion-and-signature-moments.md) for component behavior, gestures, feedback, and authored moments.

### 6. Direct typography, camera, editing, sound, and haptics

- Treat kinetic type as language in time: legibility, reading order, duration, articulation, emphasis, and voice.
- Give the camera a role: observer, participant, guide, witness, or performer. Do not move it without narrative or spatial purpose.
- Use cuts for rupture, compression, surprise, and juxtaposition; use continuous moves for causality, immersion, and spatial understanding.
- Align sound and haptics with event significance, material, rhythm, environment, repetition, and user control.
- Read [kinetic-type-camera-and-sound.md](references/kinetic-type-camera-and-sound.md) for expressive sequences, launch films, title work, and multisensory direction.

### 7. Build the motion system

- Convert the thesis into principles, semantic tokens, component patterns, narrative patterns, and examples.
- Define duration, easing/spring, delay, stagger, distance, scale, opacity, blur, depth, rotation, and orchestration tokens only when each represents a repeatable role.
- Map tokens to purpose and frequency, not arbitrary numbers.
- Specify entrances, exits, changes, shared elements, feedback, loading, progress, attention, error, success, and spatial transitions.
- Define reduced-motion and low-performance variants at the pattern level.
- Do not introduce values outside an approved token set merely because they look close. A tokenized duration scale does not permit arbitrary 173 ms or 247 ms instances without an authorized exception.

### 8. Select the production route and prototype

- Inspect the existing framework, package manager, lockfile, motion dependencies, and runtime constraints before introducing a tool.
- Prefer static behavior, CSS, or Web Animations when they truthfully solve the need. Otherwise route by behavior: Motion for general component/layout motion; Anime.js for framework-independent timelines and DOM/SVG choreography; React Spring for continuous React physics; AutoAnimate for simple structural layout changes; SVG.js for custom vector geometry.
- Treat ManimGL as an auxiliary rendered-explanation route. Use Motion Primitives, Lucide Animated, dotLottie, Rive, Lenis, Three.js/React Three Fiber, Motion Canvas, or React Native Reanimated only when their conditional trigger and safeguards are satisfied.
- Select one primary engine for each behavior. Add only non-overlapping auxiliaries, and do not install the registry as a stack.
- Prototype timing, continuity, interruption, compositing, text, real assets, and representative devices.
- Use keyframes/storyboards to approve composition; use animatics to approve sequence; use interactive prototypes to approve real-time behavior; use runtime profiling to approve production.
- Define asset ownership, export settings, responsive/crop rules, fallback, and versioning.
- Read [open-source-motion-library-registry.md](references/open-source-motion-library-registry.md) before retrieving, installing, copying, or combining a motion library.
- Read [tools-production-and-handoff.md](references/tools-production-and-handoff.md) for engine routing and implementation contracts.

### 9. Critique, adapt, and verify

- Review in order: purpose, comprehension, aesthetic thesis, temporal hierarchy, physical coherence, brand fit, interaction, accessibility, performance, and craft.
- Compare alternatives using the same content, viewport, duration, and context.
- Test reduced motion, low power, slow devices, background/foreground changes, interruption, repeated use, localization, and input differences.
- Remove motion that adds latency, confusion, fatigue, nausea, instability, or attention theft.
- Read [accessibility-performance-and-qa.md](references/accessibility-performance-and-qa.md) before approval.

## Aesthetic jury

For high-ambition work, score each direction from 1–5 and explain evidence:

- **Necessity:** would the movement still exist if fashion disappeared?
- **Specificity:** does it belong to this brand, message, and moment?
- **Temporal composition:** are rhythm, pause, overlap, contrast, and resolution authored?
- **Physical coherence:** do weight, material, depth, light, and sound agree?
- **Continuity:** can viewers track causality, identity, and attention?
- **Emotional precision:** does it create the intended feeling without coercion or excess?
- **Memorability:** is there a recognizable move or temporal signature?
- **Restraint:** is there enough stillness for the expressive moments to matter?
- **System fit:** can the concept scale without becoming generic or chaotic?
- **Production truth:** does the proof survive real content, runtime, accessibility, and performance?

Reject a direction that fails necessity, comprehension, accessibility, or production truth even if its average score is high.

## Compose the deliverable

Lead with the motion recommendation. Include:

1. Motion intent and ambition level
2. Known / observed / inferred / assumed
3. Taste profile and research synthesis when warranted
4. Motion thesis, aesthetic dials, invariants, and anti-goals
5. Temporal hierarchy and choreography
6. Physical/material/spatial rules
7. Interaction or narrative specification
8. Motion tokens and system mapping
9. Prototype, engine, asset, and performance plan
10. Reduced-motion and accessibility behavior
11. Jury verdict, risks, open decisions, and acceptance evidence

Use [artifact-templates.md](references/artifact-templates.md) for motion briefs, theses, storyboards, token sets, interaction specs, jury scorecards, and handoff.

## Quality gates

- **Purpose gate:** every movement has a named functional, narrative, or brand purpose.
- **Taste gate:** high-ambition work is grounded in client evidence and a sufficiently broad reference field.
- **Thesis gate:** the direction has coherent kinetic traits, hierarchy, signature, stillness, and anti-goals.
- **Composition gate:** beats, rhythm, pauses, overlaps, and attention sequence are deliberate.
- **Physical gate:** acceleration, material, depth, deformation, light, and sound do not contradict each other.
- **Interaction gate:** real-time motion is responsive, interruptible, reversible, and state-correct.
- **System gate:** approved tokens and patterns are used without unauthorized drift.
- **Tooling gate:** the existing stack was inspected; each dependency has a necessary, non-overlapping role; source, package, compatibility, version, license, lifecycle ownership, and fallback are recorded.
- **Symbol gate:** every deliverable is free of emoji decoration unless explicitly requested; any icons reuse the approved set or a project-consistent SVG grammar.
- **Accessibility gate:** meaning survives reduced motion, absent sound/haptic, and assistive use.
- **Performance gate:** target devices and runtime meet the agreed budget without masking latency.
- **Production gate:** the actual temporal behavior—not only static frames—has been reviewed.

## Anti-patterns

- Do not begin with an animation library, preset, or trend name.
- Do not install a collection of motion libraries speculatively, or give two engines ownership of the same element, property, state lifecycle, or frame loop.
- Do not import a library demo’s timing, physics, spacing, color, typography, iconography, or visual treatment as the project’s aesthetic system.
- Do not animate every visible object or stagger every list.
- Do not use bounce as a synonym for personality.
- Do not mix elastic, inertial, liquid, and rigid behavior without an intentional material system.
- Do not use motion to hide slow software or delay available actions.
- Do not let background spectacle compete with reading or task completion.
- Do not make scroll progress, hover, autoplay, sound, or gesture the only way to access meaning.
- Do not treat reduced motion as “remove everything” when continuity and state still need explanation.
- Do not create unique timing values for each component when semantic tokens exist.
- Do not copy a reference shot, living creator’s signature, brand ident, or title sequence.
- Do not confuse technical complexity with aesthetic quality.
- Do not claim production readiness from a storyboard, mockup, or smooth recording alone.
- Do not use emoji as decorative shorthand or interface iconography without an explicit user request, and do not mix icon families or visual grammars within one project.
