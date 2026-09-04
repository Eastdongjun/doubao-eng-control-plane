# Physicality, Material, and Transition

Use this module for spatial transitions, springs, deformation, particles, glass/liquid effects, depth, direct manipulation, or object transformations.

## Contents

- [Material hypothesis](#material-hypothesis)
- [Physical parameters](#physical-parameters)
- [Spatial continuity](#spatial-continuity)
- [Transformations](#transformations)
- [Glass, transparency, and fluid surfaces](#glass-transparency-and-fluid-surfaces)
- [Particles and generative systems](#particles-and-generative-systems)
- [Light, blur, and depth](#light-blur-and-depth)
- [Physical critique](#physical-critique)

## Material hypothesis

Choose a coherent material behavior:

| Material model | Motion traits | Visual traits | Common failure |
|---|---|---|---|
| Rigid/structural | decisive, little deformation | crisp edges, stable geometry | feels dead when every change snaps |
| Paper/layered | planar slide, fold, reveal | occlusion, shadow, edge | arbitrary card shuffling |
| Elastic | overshoot, compression, recoil | deformation, stored energy | toy-like bounce everywhere |
| Inertial | momentum, friction, settle | continuous velocity | long drift and weak control |
| Magnetic | attraction, snapping, field response | proximity emphasis | unexplained acceleration |
| Viscous/liquid | lag, flow, merge, surface tension | refraction, stretch, soft boundary | illegibility and expensive compositing |
| Granular/particle | dispersion, aggregation | many small elements | noise without object identity |
| Optical/light | fade, bloom, diffraction, color shift | light-dependent appearance | glow as generic decoration |
| Abstract/graphic | authored cut, wipe, scale, mask | form-driven | no relationship to task or brand |

The model can be stylized; it must still behave consistently enough to teach expectation.

## Physical parameters

Define perceptually:

- Mass and inertia
- Stiffness and damping
- Friction and resistance
- Elasticity and deformation
- Gravity or directional bias
- Collision and boundary behavior
- Velocity continuity
- Depth and perspective

Tune numbers in the target runtime. Do not infer production physics from a video reference alone.

## Spatial continuity

Preserve:

- Source and destination relationship
- Object identity
- Stable anchors
- Directional logic
- Layer order and occlusion
- Focus and interaction availability
- Velocity continuity during interruption

Shared-element transitions require identity mapping, geometry measurement, content continuity, and fallbacks for mismatched or absent elements.

## Transformations

Choose:

- Morph: same conceptual object changes form
- Crossfade: content changes without spatial claim
- Move/resize: object persists through layout change
- Mask/reveal: information appears through a controlled boundary
- Cut: discontinuity is meaningful or speed matters
- Dissolve/particle: identity decomposes and reconstitutes
- Camera transition: viewpoint changes within one space

Do not morph unrelated objects merely because geometry permits it.

## Glass, transparency, and fluid surfaces

Validate:

- Background dependency and contrast
- Refraction/distortion logic
- Edge and thickness cues
- Parallax and depth response
- Hit targets and semantic boundaries
- Text legibility through every frame
- Overdraw, blur, compositing, battery, and fallback
- Reduced-transparency and reduced-motion preferences

Use glass as a material relationship among layers, not as a blur filter on every container.

## Particles and generative systems

Specify:

- Emission source and meaning
- Quantity and lifespan
- Field/force behavior
- Object or data relationship
- Determinism and seeding
- Responsiveness to input
- Performance ceiling
- Static/reduced alternative

Avoid ambient particle noise that steals attention or makes content harder to read.

## Light, blur, and depth

- Motion blur should express velocity, not mask low frame rate.
- Shadow and reflection must respond consistently to depth and light.
- Parallax should preserve readability and avoid vestibular discomfort.
- Depth-of-field is a camera cue; use it only when focus hierarchy benefits and text remains clear.
- Bloom and glow require contrast discipline and color management.

## Physical critique

Ask:

1. What material does this imply?
2. Where does the energy come from?
3. What resists, deforms, or settles?
4. What remains anchored?
5. Does light/depth support the same model?
6. Does interruption conserve continuity?
7. Is the metaphor useful after repeated use?
