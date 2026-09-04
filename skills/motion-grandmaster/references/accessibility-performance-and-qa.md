# Accessibility, Performance, and QA

Use this module before approving any motion for release.

## Contents

- [Reduced motion](#reduced-motion)
- [Vestibular and seizure safety](#vestibular-and-seizure-safety)
- [Sensory alternatives](#sensory-alternatives)
- [Performance budget](#performance-budget)
- [Performance design](#performance-design)
- [Motion QA matrix](#motion-qa-matrix)
- [Critique order](#critique-order)
- [Severity](#severity)
- [Acceptance evidence](#acceptance-evidence)

## Reduced motion

Determine why the motion exists:

- **Decorative:** remove or replace with static emphasis.
- **Spatial orientation:** use a short crossfade, instant state change with persistent cues, or reduced-distance transition.
- **Causality:** preserve source/destination relationship with minimal transformation.
- **Progress/status:** retain truthful status without looping spectacle.
- **Narrative:** provide user control, pause, summary, or alternate static sequence.
- **Direct manipulation:** preserve control and state; reduce inertial or parallax effects.

Honor system preferences and allow product-level control when motion intensity, duration, autoplay, or flashing warrants it.

## Vestibular and seizure safety

Review:

- Large-field pan, zoom, rotation, parallax, and depth
- Rapid acceleration or oscillation
- Scroll-linked motion
- Autoplay and infinite loops
- Flashing, contrast alternation, and repeated patterns
- Background motion behind reading

Provide pause/stop/hide controls where required and avoid unsafe flashing. Do not rely on user discomfort reports as the only prevention method.

## Sensory alternatives

- Sound-off must preserve meaning.
- Haptic-off must preserve confirmation.
- Motion-off must preserve causality and hierarchy.
- Canvas/video must provide semantic or textual access to necessary information.
- Captions, transcripts, and descriptions must match the content purpose.

## Performance budget

Define:

- Target devices and browsers
- Frame-rate or frame-time objective
- Interaction latency objective
- JavaScript/runtime budget
- CPU/GPU and memory risk
- Asset weight and network strategy
- Battery/thermal constraints
- Long-task, layout, paint, overdraw, and compositing limits
- Measurement method and representative scenario

Do not invent universal budgets. Agree on budgets relative to product context and measure on representative hardware.

## Performance design

- Give immediate acknowledgment even when completion is slow.
- Avoid continuous work when content is offscreen, hidden, backgrounded, or static.
- Cap particles, blur, shadows, filters, and layer count.
- Prefer adaptive quality and graceful fallback over stutter.
- Reserve expensive material effects for moments that carry value.
- Preload only what is likely and valuable; do not transfer delay elsewhere invisibly.
- Preserve text and control responsiveness during motion.

## Motion QA matrix

Test:

| Dimension | Cases |
|---|---|
| Trigger | mouse, keyboard, touch, programmatic, repeated, rapid |
| State | initial, mid-flight, complete, reversed, interrupted, error |
| Content | empty, long, localized, dynamic, media missing |
| Layout | narrow, wide, zoomed, resized, orientation change |
| System | reduced motion, high contrast, low power, background/foreground |
| Performance | representative low device, slow network, CPU/GPU pressure |
| Accessibility | focus, reading order, announcements, alternatives, autoplay control |
| Visual | intermediate frames, clipping, z-order, blur, color, text legibility |
| Audio/haptic | muted, unavailable, delayed, repeated |

## Critique order

1. Does the motion need to exist?
2. Is state and causality understandable?
3. Does it express the chosen thesis?
4. Is attention sequenced correctly?
5. Is the physical/material model coherent?
6. Does it remain useful after repetition?
7. Does meaning survive reduced motion and silent use?
8. Does it meet runtime budgets?
9. Does it use approved tokens and patterns?
10. Are intermediate frames crafted?

## Severity

- **Blocker:** causes harm, loss of control, inaccessible core task, unsafe flashing, severe sickness risk, data/state error, or unusable performance.
- **High:** misleading causality, interaction latency, broken interruption, missing reduced-motion path, major attention or legibility failure.
- **Medium:** inconsistent thesis/token use, repetition fatigue, local jank, weak fallback, or noticeable craft defect.
- **Low:** small polish issue without meaningful outcome impact.

## Acceptance evidence

Require:

- Actual runtime or rendered temporal proof
- Full-speed and slowed inspection
- Repeated and interrupted behavior
- Reduced-motion capture
- Representative device profile
- Token conformance
- Accessibility behavior
- Known limitations and owner
