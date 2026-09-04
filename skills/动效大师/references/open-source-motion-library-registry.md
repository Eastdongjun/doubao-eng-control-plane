# Open-source Motion Library Registry

Use this registry only after the motion thesis, system authority, behavior contract, and proof target are known. It is a routing system for implementation, not a catalog of visual styles.

The selected default core is M1, M2, M3, M4, and M11. M16 is an auxiliary production route. Every other listed library is conditional.

## Contents

- [Registry rules](#registry-rules)
- [Default core](#default-core)
- [Auxiliary route](#auxiliary-route)
- [Conditional routes](#conditional-routes)
- [Decision sequence](#decision-sequence)
- [Combination and ownership rules](#combination-and-ownership-rules)
- [Agent retrieval protocol](#agent-retrieval-protocol)
- [Aesthetic and system guardrails](#aesthetic-and-system-guardrails)
- [Licensing, assets, and security](#licensing-assets-and-security)
- [Acceptance checklist](#acceptance-checklist)

## Registry rules

1. **Reuse before adding.** If the project already has a capable, maintained motion engine, prefer it unless there is a documented gap.
2. **Native before dependency.** Use CSS transitions, CSS animations, or the Web Animations API when they truthfully solve the behavior.
3. **One primary owner.** Assign one engine to each element, property, interaction lifecycle, and frame loop.
4. **Minimum stack.** Select one primary route and only the smallest compatible auxiliary needed for a proven gap.
5. **No bulk installation.** The registry does not authorize installing every library, copying every preset, or adding dependencies before inspecting the project.
6. **Current verification.** Before installation, verify the official repository, current documentation, package name, compatibility, release status, and license.
7. **Respect the project.** Preserve the existing package manager, lockfile, framework conventions, design tokens, motion tokens, accessibility rules, and performance budget.
8. **Record the decision.** Capture source URL, selected package and version, license, purpose, owner, fallback, and verification date.
9. **Library is not taste.** A library may implement motion, but it may not decide the motion thesis, visual style, material model, timing hierarchy, or brand expression.
10. **Proof before expansion.** Validate one representative behavior before extending a tool across the project.

## Default core

These libraries are approved default candidates, not automatic dependencies.

| ID | Library | Official source and package | Best fit | Do not use as |
|---|---|---|---|---|
| M1 | Motion | [motiondivision/motion](https://github.com/motiondivision/motion); `motion`, or `motion-v` for Vue | General web and React/Vue component motion, layout transitions, gestures, scroll-linked behavior, and authored sequences | A reason to animate every component or replace existing project tokens |
| M2 | Anime.js | [juliangarnier/anime](https://github.com/juliangarnier/anime); `animejs` | Framework-agnostic DOM, SVG, JavaScript-object, and timeline choreography | A second owner for properties already controlled by a framework animation engine |
| M3 | React Spring | [pmndrs/react-spring](https://github.com/pmndrs/react-spring); `@react-spring/web`, optionally `@react-spring/three` | Continuous, interruptible, state-seeking, gesture-coupled, or physics-led React motion | A default for fixed authored timing that is better expressed by duration and easing |
| M4 | AutoAnimate | [formkit/auto-animate](https://github.com/formkit/auto-animate); `@formkit/auto-animate` | Low-complexity add, remove, reorder, and layout-change transitions | Brand motion, complex choreography, or a substitute for explicit state design |
| M11 | SVG.js | [svgdotjs/svg.js](https://github.com/svgdotjs/svg.js); `@svgdotjs/svg.js` | Custom SVG construction, path manipulation, geometry, and project-specific vector motion | Permission to invent a second icon language or animate decorative SVG without purpose |

### Default-core routing

- Use Motion for the general product or website motion layer when its framework support fits.
- Use Anime.js when a framework-independent timeline, DOM sequence, or custom SVG/object choreography is the central problem.
- Use React Spring when continuous physical response and interruption are more important than exact authored duration.
- Use AutoAnimate only for simple structural transitions where explicit choreography would add needless complexity.
- Use SVG.js when custom vector geometry is intrinsic to the concept, not merely because the output format is SVG.

If two default-core tools appear equally suitable, prefer the one already present in the project. If neither is present, prefer the smallest route that proves the behavior with the lowest ownership and maintenance cost.

## Auxiliary route

| ID | Library | Official source and package | Role | Boundary |
|---|---|---|---|---|
| M16 | ManimGL | [3b1b/manim](https://github.com/3b1b/manim); `manimgl` | Explanatory mathematics, data, systems, and algorithm animation rendered as authored video | Not a UI runtime; do not confuse it with the separate Manim Community package named `manim` |

Use ManimGL when the project needs precise explanatory motion whose truth is a rendered sequence rather than an interactive interface. Keep fonts, narration, music, imagery, and output rights separate from the code license.

## Conditional routes

Conditional routes require a concrete project fit, an explicit implementation reason, and current verification.

| ID | Library or route | Official source and package | Trigger | Required safeguard |
|---|---|---|---|---|
| M6 | Motion Primitives | [ibelick/motion-primitives](https://github.com/ibelick/motion-primitives); source/registry components | A React/Tailwind project needs inspectable motion primitives that can be adapted to its system | Treat as source adoption, map every value to approved components and tokens, retain required notices, and never paste blindly |
| M8 | Lucide Animated | [pqoqubbw/icons](https://github.com/pqoqubbw/icons); source/registry components | The approved project icon language is Lucide-compatible and an animated icon improves state comprehension | Preserve one icon family, grid, stroke, optical size, color, and motion grammar |
| M9 | dotLottie Web | [LottieFiles/dotlottie-web](https://github.com/LottieFiles/dotlottie-web); `@lottiefiles/dotlottie-web`, `@lottiefiles/dotlottie-react`, or platform equivalent | The project already has an authored `.lottie` or compatible animation asset and needs efficient playback, themes, or state-machine support | Verify asset rights, renderer behavior, fallback, text strategy, loading, reduced motion, and semantic alternative |
| M10 | Rive Web Runtime | [rive-app/rive-wasm](https://github.com/rive-app/rive-wasm); usually `@rive-app/webgl2`, with `@rive-app/canvas` or `@rive-app/canvas-lite` when justified | An interactive vector, character, or state machine needs authored inputs and runtime response | Require a governed `.riv` asset, documented inputs, fallback, canvas semantics, cleanup, and performance tests; do not introduce deprecated `@rive-app/webgl` |
| M12 | Lenis | [darkroomengineering/lenis](https://github.com/darkroomengineering/lenis); `lenis` | A narrative, editorial, portfolio, or immersive experience needs deliberate scroll behavior | Preserve native navigation, keyboard behavior, deep links, reduced motion, interruption, and a no-enhancement fallback |
| M13 | Three.js and React Three Fiber | [mrdoob/three.js](https://github.com/mrdoob/three.js), [pmndrs/react-three-fiber](https://github.com/pmndrs/react-three-fiber); `three`, optionally `@react-three/fiber` | Spatial, 3D, shader, material, or scene behavior is central to the experience | Provide semantic DOM alternatives, loading strategy, device/GPU profiling, context-loss handling, reduced motion, and a non-3D fallback |
| M15 | Motion Canvas | [motion-canvas/motion-canvas](https://github.com/motion-canvas/motion-canvas); scaffold with `npm init @motion-canvas@latest`, packages include `@motion-canvas/core` and `@motion-canvas/2d` | A code-driven explanatory, vector, data, or educational sequence must render as video | Treat it as a production pipeline rather than UI runtime; control fonts, audio, media rights, deterministic rendering, and output settings |
| M17 | React Native Reanimated | [software-mansion/react-native-reanimated](https://github.com/software-mansion/react-native-reanimated); `react-native-reanimated` | A React Native application needs gesture-coupled, native-thread, or high-performance interface motion | Verify the current React Native compatibility matrix, Worklets/build requirements, platform behavior, and reduced-motion handling |

Do not add a conditional route merely because its demos look polished. A named need, runtime fit, ownership plan, and fallback must exist first.

## Decision sequence

Use this sequence for every implementation decision:

1. Identify the user, business, comprehension, or brand purpose of the motion.
2. Lock the approved design system, motion tokens, component contracts, and authority.
3. Inspect the existing framework, package manager, lockfile, runtime, motion dependencies, and build constraints.
4. Ask whether static design, instant state change, CSS, or Web Animations already proves the behavior.
5. If an existing engine covers the need, reuse it and avoid adding another abstraction.
6. If a gap remains, classify it:
   - General component/layout/gesture motion: M1
   - Framework-independent authored timeline or DOM/SVG choreography: M2
   - Continuous React physics: M3
   - Simple structural layout changes: M4
   - Custom vector geometry: M11
   - Rendered mathematical or systems explanation: M16
   - Specialized component, asset, scroll, spatial, video, or native runtime: the matching conditional route
7. Compare bundle cost, lifecycle ownership, semantics, accessibility, interruption, responsiveness, performance, team maintainability, and license.
8. Select one primary engine and document any auxiliary with a non-overlapping responsibility.
9. Build the smallest representative proof using real content and tokens.
10. Expand only after reduced motion, cleanup, state correctness, and representative-device performance pass.

## Combination and ownership rules

### Motion with AutoAnimate

Use AutoAnimate only on isolated list or layout containers that Motion does not already own. Do not let both libraries animate the same child transform, layout change, or enter/exit lifecycle.

### Anime.js with SVG.js

SVG.js may own vector construction and geometry while Anime.js owns an authored timeline. Declare which tool writes each attribute or transform, and avoid competing update loops.

### React Spring with Three.js or React Three Fiber

Use `@react-spring/three` when spring state must drive scene properties. Do not add a separate DOM engine to control the same scene state unless ownership is isolated.

### Motion with dotLottie or Rive

Motion may control surrounding DOM transitions while the asset runtime owns its internal timeline or state machine. Do not manipulate internal and external transforms on the same visual layer without an explicit composition wrapper.

### Lenis with a motion engine

Lenis may provide a scroll source while the selected engine maps progress to motion. Use one animation-frame coordinator, clean up all subscriptions, preserve direct user interruption, and disable enhancement for reduced motion when appropriate.

### Multiple frame loops

Avoid concurrent uncontrolled request-animation-frame loops. Establish one coordinator or isolate independent surfaces, pause offscreen work, and tear down listeners, observers, canvases, timelines, and GPU resources.

## Agent retrieval protocol

An Agent may retrieve and integrate a library only through this protocol:

1. Read the project manifest, lockfile, framework configuration, build scripts, existing motion dependencies, and relevant design/motion documentation.
2. Identify the exact behavior the existing stack cannot express cleanly.
3. Open the official repository and current official documentation. Verify repository ownership, package name, supported runtime, current release, installation requirements, and license.
4. Inspect compatibility with the project’s framework and package versions. Do not infer compatibility from a search result or old tutorial.
5. State the proposed primary engine, optional auxiliary, rejected alternatives, ownership boundaries, and expected cost.
6. Use the package manager already selected by the project. Preserve its lockfile and workspace conventions.
7. Install only the packages needed for the approved proof. Pin a compatible version according to project policy; do not silently switch package managers or upgrade unrelated dependencies.
8. For source/registry components, inspect every copied file, dependency, style value, accessibility behavior, and license notice. Refactor it into the project system before use.
9. Build a minimal representative implementation with cleanup, cancellation, reduced motion, loading/error behavior, and semantic fallback.
10. Test actual intermediate frames, repeated triggers, interruption, resize, localization, low-performance conditions, and target input methods.
11. Record source URL, version or commit, license, retrieved files, modifications, verification date, fallback, and known limitations in the project source ledger.
12. If live network, rendering, or profiling tools are unavailable, label the result as a proposed route rather than a verified integration.

## Aesthetic and system guardrails

- Start from the project’s motion thesis, not a library demo or preset gallery.
- Preserve approved color, typography, spacing, radius, elevation, icon, component, and motion tokens.
- Use the project’s duration, easing, spring, distance, blur, scale, depth, and choreography roles; do not import arbitrary preset values.
- Preserve the project’s kinetic personality, material model, spatial logic, temporal hierarchy, and stillness rule across all engines.
- Treat demo components as implementation references, not art direction.
- Reject a technically convenient effect that creates visual drift, excessive frequency, conflicting physics, unreadable type, or attention theft.
- Keep functional and expressive layers distinct. Product feedback remains fast and legible even when rare signature moments are more authored.
- Keep SVG icon motion consistent with the approved icon family; do not use animated icons as decoration.
- Reduced motion must preserve state, causality, hierarchy, progress, and completion evidence.

## Licensing, assets, and security

- The registry records projects whose code repositories were MIT-licensed at the review date, but every project must verify the exact package, version, included files, and current license again.
- A code license does not grant rights to demo footage, illustrations, fonts, music, voice, logos, brand assets, `.lottie` files, `.riv` files, generated media, or third-party examples.
- Keep copyright notices and attribution required by the selected version.
- Treat packages, source registries, post-install scripts, transitive dependencies, and build plugins as code entering the project. Review them according to project security policy.
- Do not copy visual treatments, signature sequences, or recognizable brand motion merely because the implementation repository is open source.
- Do not publish API keys, private assets, client files, internal URLs, or proprietary motion source files with an example or registry component.

## Acceptance checklist

- [ ] Motion purpose and non-motion alternative are documented.
- [ ] Existing stack and approved systems were inspected first.
- [ ] Native CSS/Web Animations and existing dependencies were considered.
- [ ] One primary engine owns each behavior and property.
- [ ] Every auxiliary has a non-overlapping, necessary role.
- [ ] Official source, package, version, compatibility, and license were verified.
- [ ] No library demo or preset defines the project’s aesthetic direction.
- [ ] All values map to approved design and motion tokens.
- [ ] Cleanup, cancellation, interruption, and repeated triggering are correct.
- [ ] Reduced motion and semantic fallback preserve meaning.
- [ ] Target-device performance and multiple frame loops were inspected.
- [ ] Asset, font, audio, media, and brand rights were checked separately.
- [ ] The project source ledger records origin, modifications, and limitations.
