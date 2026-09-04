# Tools, Production, and Handoff

Use this module after the motion thesis and behavior are defined. Select tools by the temporal and runtime problem, not popularity.

## Contents

- [Technique routing](#technique-routing)
- [Selection criteria](#selection-criteria)
- [Proof ladder](#proof-ladder)
- [Implementation specification](#implementation-specification)
- [Asset pipeline](#asset-pipeline)
- [Prototyping and inspection](#prototyping-and-inspection)
- [Engine-specific cautions](#engine-specific-cautions)
- [Handoff meeting](#handoff-meeting)

## Technique routing

| Need | Likely route | Notes |
|---|---|---|
| Simple state, hover, focus, enter/exit | CSS transitions/animations or Web Animations | smallest runtime; respect existing framework |
| General component, layout, gesture, or scroll-linked motion | Motion | default candidate when the framework fit and existing stack support it |
| Framework-independent DOM, SVG, object, or timeline choreography | Anime.js | useful for authored sequencing without assigning framework state twice |
| Continuous, interruptible, state-seeking React physics | React Spring | choose when physical response matters more than exact authored duration |
| Simple add, remove, reorder, or layout change | AutoAnimate | isolated structural enhancement; not a brand-motion layer |
| Custom vector construction and geometry | SVG.js | preserve the project’s SVG and icon grammar |
| Authored vector asset playback | dotLottie Web | conditional; validate asset rights, renderer, text, fallback, and semantics |
| Stateful interactive vector or character | Rive Web Runtime | conditional; document state-machine inputs, canvas semantics, cleanup, and fallback |
| Narrative or immersive scroll behavior | Lenis with one selected motion engine | conditional; preserve native control, interruption, deep links, and reduced motion |
| Spatial, 3D, shader, or material work | Three.js, optionally React Three Fiber | conditional; justify cost and profile GPU, memory, loading, and context loss |
| Code-driven explanatory vector or data video | Motion Canvas | conditional rendered pipeline; control fonts, audio, media rights, and output |
| Mathematical, system, or algorithm explanation video | ManimGL | auxiliary rendered route; not an interface runtime |
| React Native interface and gesture motion | React Native Reanimated | conditional; verify the current RN compatibility and build requirements |

This is routing, not a mandated stack. Reuse an existing capable engine before adding one. Read [open-source-motion-library-registry.md](open-source-motion-library-registry.md) for the selected core, conditional triggers, combination rules, and retrieval protocol.

GSAP, Remotion, p5.js, platform-native APIs, or another project-selected engine may still be supported when they already govern the project or the user explicitly selects them after current license and compatibility review. They are not default additions from this open-source registry.

## Selection criteria

- Real-time versus fixed timeline
- User-interruptible versus authored
- DOM semantics and accessibility
- State-machine complexity
- Text and localization
- Asset and design-tool pipeline
- 2D versus 3D, vector versus raster
- Browser/device support
- Bundle, CPU, GPU, memory, battery, and network budgets
- Deterministic rendering and capture
- Team expertise, maintainability, and licensing
- Lifecycle ownership, cleanup, and competing animation-frame loops
- Existing dependencies, package manager, lockfile, and upgrade policy

## Proof ladder

Use the smallest artifact that proves the decision:

1. Beat sheet proves structure.
2. Storyboard proves composition and sequence.
3. Animatic proves timing and edit.
4. Motion study proves material or signature behavior.
5. Interactive prototype proves input coupling, interruption, focus, and state.
6. Runtime prototype proves performance and integration.
7. Production QA proves actual assets, content, devices, and fallbacks.

Do not use a polished video recording to claim interactive responsiveness.

## Implementation specification

For each behavior include:

```text
ID and purpose:
Trigger and preconditions:
Elements and hierarchy:
Initial / active / final states:
Timing tokens or spring parameters:
Sequencing / overlap / stagger:
Transform origin / path / depth:
Input coupling and interruption:
Cancellation / reversal:
Responsive behavior:
Reduced-motion variant:
Low-performance fallback:
Assets and rights:
Instrumentation:
Acceptance evidence:
```

## Asset pipeline

Record:

- Source file and owner
- License/rights and expiry
- Version and export settings
- Color space, alpha, resolution, frame rate, and compression
- Font embedding and text localization
- Responsive crop or layout
- Loading strategy and placeholder
- Runtime renderer and fallback
- Change and approval history

Avoid bundling unlicensed references into production.

## Prototyping and inspection

- Use representative content and longest translations.
- Test at target scale and frame rate.
- Inspect actual intermediate frames, not only endpoints.
- Test repeated triggering and rapid reversal.
- Profile on representative low and high devices.
- Verify background/foreground, resize, orientation, and reduced-motion changes.
- Capture evidence: recording, profiler trace, state tests, and known limitations.

## Engine-specific cautions

- CSS/layout: prefer transform and opacity when they preserve semantics; do not force everything onto the compositor if visual truth needs layout.
- Motion: scope component ownership, layout measurement, gesture subscriptions, and exit lifecycles; map values to project tokens.
- Anime.js: clean up timelines and targets; do not compete with framework or CSS ownership of the same properties.
- React Spring: select spring behavior for a real physical or interruptible reason; avoid tuning arbitrary per-component values outside the motion system.
- AutoAnimate: isolate containers and verify reflow, focus, virtualized lists, and interaction with explicit enter/exit motion.
- SVG.js: retain viewBox, semantics, responsive geometry, and the approved icon/vector grammar.
- dotLottie: verify renderer differences, masks, effects, text, scaling, loading, asset rights, and semantic alternative.
- Rive: document state inputs and fallback; avoid hiding core controls inside an inaccessible canvas.
- Lenis: preserve native navigation and interruption, use one frame coordinator, and provide a no-enhancement path.
- Three.js/React Three Fiber: provide DOM semantics and keyboard alternatives; handle resolution, loading, context loss, resource disposal, and reduced motion.
- Motion Canvas and ManimGL: provide captions/transcript when relevant and verify deterministic rendering, fonts, media rights, color, and output settings.
- React Native Reanimated: verify current Worklets/build requirements, thread ownership, cleanup, platform differences, and reduced-motion behavior.

## Handoff meeting

Review:

1. Intent and thesis
2. Full-speed and slow playback
3. Interaction/state contract
4. Token mapping
5. Reduced motion and fallback
6. Asset source and rights
7. Performance budget
8. Acceptance tests and ownership

The implementer should be able to reproduce the intended temporal quality without guessing from a single easing label.
