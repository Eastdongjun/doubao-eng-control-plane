# Visual Craft Grammar: Color, Composition, Motion, and Interaction

Use this module when visual quality depends specifically on palette relationships, layout tension, spatial rhythm, expressive motion, or interaction character. It turns curated inspiration into transferable mechanisms instead of copying a style.

## 1. Build a reference diet, not an inspiration pile

Separate sources by what they can actually prove:

- **Shipped product/flow evidence:** proves usability patterns, state coverage, copy, interaction sequence, and real constraints
- **Expressive web/portfolio evidence:** reveals emerging layout, material, type, transition, and interaction possibilities
- **Graphic/editorial/image evidence:** expands composition, palette, texture, scale, narrative, and cultural language
- **Motion/creative-development evidence:** exposes timing, continuity, physics, spatial mapping, and implementation technique
- **Adjacent-field evidence:** architecture, film, fashion, publishing, games, industrial design, exhibition, sound
- **Counter-reference:** shows saturation, cliché, usability debt, or identity the work must avoid

Do not infer product usability from an experimental portfolio or aesthetic authorship from a pattern library. Pair expressive references with shipped evidence and implementation reality.

For every saved reference record:

| Field | Question |
|---|---|
| Source/provenance/date | Where did it come from and is it current? |
| Immediate attraction | What catches the eye first? |
| Mechanism | Which relationship creates the effect? |
| Context | Why does it work for this content, audience, and medium? |
| Transfer | What principle can move to this project? |
| Boundary | Where would it become illegible, generic, manipulative, or costly? |
| Test | What proof would show that the transfer works? |

An “eye-catching” reference is only an observation until the mechanism and boundary are explicit.

## 2. Color as topology

Judge palette by spatial and semantic relationships, not swatch beauty.

### Define roles

- **Field:** the dominant canvas or atmosphere
- **Ink:** the structural text, outline, divider, or dark/light anchor
- **Support:** the small recurring family that binds sections and components
- **Signal:** semantic state or action color
- **Surprise:** one controlled hue or temperature shift that creates memory

The roles may share hues only when luminance, placement, or shape prevents ambiguity.

### Saturation strategies

Three useful models:

1. **Quiet field + chromatic anchor:** large neutral/low-chroma field, one visible high-chroma form
2. **Chromatic field + bounded supports:** one dominant vivid field with a few repeated companion hues and strong edge separation
3. **Warm/cool counterpoint:** broad cool atmosphere against a limited warm focal mass, or the inverse

High saturation remains coherent when the palette is limited, proportions are stable, and every edge is legible. Muting everything is not sophistication.

### Similar-value color

When adjacent colors have similar luminance, separate them with at least one intentional device:

- dark/light outline
- neutral buffer or spacing
- hard shape boundary
- texture or pattern contrast
- hue-temperature distance
- local luminance shift

Do not use similar-value chroma for text, focus, state, or critical controls without sufficient contrast.

### Palette tests

- Grayscale hierarchy
- Thumbnail focal anchor
- Color-vision simulation and non-color state cues
- Light/dark and display-condition stress
- Dense-data and mundane-screen behavior
- Brand and semantic token mapping
- One-by-one subtraction: remove each hue and ask what meaning or rhythm is lost

## 3. Composition as attention geometry

Start with masses, voids, and sequence before decoration.

### Active negative space

Every major empty region needs a job:

- isolate the subject
- establish monumental or intimate scale
- slow reading and create calm
- create suspense before reveal
- separate conceptual chapters
- reserve an interaction or motion path
- counterbalance a dense or heavy mass

If the space has no role, it is not restraint; it is unmade composition.

### Focal models

- **Tiny anchor / vast field:** strong for solitude, contemplation, luxury, editorial, and scale; risky for task-dense products
- **Large cropped mass / small witness:** creates immersion and a human scale reference
- **Central specimen / satellite type:** creates archival, catalog, or study behavior
- **Asymmetric counterweight:** balances a heavy image with small distant text or action
- **Continuous strip or surface:** turns navigation into spatial travel; requires orientation and accessible fallback
- **Layered horizon/reflection:** creates depth and continuity with minimal elements

Use one dominant model per moment. Multiple competing models dissolve hierarchy.

### Typographic position

Type can be:

- information hierarchy
- compositional mass
- scale reference
- directional cue
- texture or atmospheric trace
- interaction label

Core content must remain readable. Microtype may create atmosphere only when it is supplementary and does not impersonate meaningful data.

### Distance tests

- **Thumbnail:** one focal path and intended color anchor survive
- **Reading distance:** hierarchy, content, and action are clear
- **Close craft:** type, texture, alignment, and optical detail reward inspection
- **Content stress:** long, short, localized, empty, error, and dense states retain composition

## 4. Motion as continuity

Motion design begins with what persists.

Define:

- Persistent object, surface, horizon, or spatial frame
- Input: time, scroll, drag, pointer, focus, state, or system event
- Mapping between input and visible change
- Entrance, acceleration, transition, rest, interruption, reversal, and exit
- Information revealed or relationship clarified
- Reduced-motion/static equivalent

Prefer:

- transformation that preserves object identity
- spatial continuation between origin and destination
- camera or surface movement that maintains orientation
- stagger derived from hierarchy, not index alone
- loops whose seam is visually and semantically invisible
- secondary motion that follows the primary physical logic

Avoid:

- every section fading independently
- scroll hijacking without control or progress
- infinite loops that duplicate focusable/announced content
- motion that delays routine actions
- ornamental parallax with no depth or hierarchy role
- physics that contradict perceived mass/material

### Motion proof

Review still frame, midpoint, end state, interruption, reverse direction, low-performance case, and reduced motion. A polished hero loop does not prove the rest of the experience.

## 5. Interaction as expressive behavior

Keep the interaction contract conventional enough to discover and recover; place authorship in mapping, transition, feedback, and material response.

For every expressive interaction specify:

- Invitation: how the user knows it can be acted on
- Trigger and input modalities
- Immediate feedback and state persistence
- Spatial/semantic mapping
- Cancellation, interruption, undo, and recovery
- Keyboard, focus, touch, screen-reader, and reduced-motion behavior
- Performance budget and fallback
- What remains stable so the user stays oriented

Use the **expressive shell / conventional core** rule:

- Navigation, forms, permissions, errors, and high-stakes decisions stay familiar and explicit.
- Browsing, storytelling, portfolio exploration, product demonstration, and transitions may carry more expressive spatial behavior.
- The shell must never obscure the core, move controls unpredictably, or make the user wait for spectacle.

## 6. Convert references into a project grammar

Synthesize references into bounded rules:

```text
Intent
-> attention geometry
-> palette topology
-> typography and image roles
-> material/reproduction logic
-> motion continuity
-> interaction contract
-> token/component mapping
-> proof and stress tests
```

Write rules that can generate multiple surfaces, not a screenshot recipe. For example:

- Good: “Use a broad cool field, one warm focal mass, and a small dark human-scale anchor; preserve 80% of the frame as atmospheric depth on editorial moments only.”
- Weak: “Use blue and orange like the reference.”
- Good: “Carry the selected card as the persistent object into detail view, with interruptible transform and focus restoration.”
- Weak: “Add a smooth transition.”

## 7. Quality gates

- **Source gate:** references come from complementary lanes and retain provenance/date.
- **Mechanism gate:** every adopted idea names the relationship that creates the effect.
- **Color gate:** palette roles, proportions, separation, contrast, and semantic mapping are explicit.
- **Composition gate:** void, mass, scale, and reading sequence have defined jobs.
- **Motion gate:** persistent anchors, mapping, rest, interruption, and reduced motion are designed.
- **Interaction gate:** discoverability, control, recovery, accessibility, and performance survive the expressive treatment.
- **Transfer gate:** the result is generated from project intent and constraints, not one recognizable reference.
- **Reality gate:** representative renders and runnable states prove the grammar beyond a moodboard.

Visual culture changes quickly. Date time-sensitive observations and refresh the source field when the project depends on what is currently emerging.
