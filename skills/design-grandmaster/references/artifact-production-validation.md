# Artifact Production and Validation

Use this module when the deliverable itself must be rendered, opened, clicked, compared, presented, or exported: HTML prototypes, interactive direction studies, landing pages, decks, data stories, motion pieces, or other executable visual artifacts.

The goal is not to prescribe one technical stack. It is to turn visual intent into reviewable evidence while keeping the process proportional to the decision.

## 1. Activation and authority

Before production, record:

- Deliverable, audience, review context, and decision it must enable
- Target runtime, devices, viewports, input modes, export format, and delivery deadline
- Available research, asset, image, code, browser, rendering, capture, and inspection capabilities
- Governing design specification, tokens, components, brand assets, and content source
- What is real, simulated, generated, placeholder, incomplete, or out of scope
- The cheapest proof that could expose a wrong direction before most of the work is spent

Production never weakens conformance. If a renderer or framework makes approved tokens inconvenient, adapt the implementation or document a blocked constraint; do not replace approved values with convenient approximations.

## 2. The smallest truthful proof

Choose proof by uncertainty, not by habit.

| Decision | Minimum useful proof | Insufficient proof |
|---|---|---|
| Information architecture or flow | graybox of the critical path and recovery | polished hero with no states |
| Visual language for a product | one representative high-fidelity screen plus one ordinary/utility state | mood adjectives or swatches alone |
| Brand/marketing direction | representative hero and one downstream section using real content/assets | three text descriptions |
| Design-system extension | real component composition across relevant states and content extremes | isolated component beauty shot |
| Deck direction | two representative slides with different information structures | cover slide only |
| Motion direction | still frame, storyboard, or rendered key moments with timing logic | motion adjectives or transition list |
| Full application | critical path, mundane state, error/recovery, and representative responsive behavior | every page partially styled |

The proof must use the same content and constraints across competing directions so the reviewer is judging the design mechanism rather than different copy, imagery, or feature scope.

### Adaptive direction count

- **One baseline:** small, reversible, strongly governed conformance work with no material aesthetic ambiguity
- **Two directions:** a bounded product or marketing decision with one meaningful trade-off
- **Three directions:** flagship, identity-defining, premium, editorial, cultural, experimental, or high-cost direction decisions
- **More than three:** only when the decision space genuinely has independent axes and the reviewer can compare without overload

Variation count is not a quality metric. Three nearly identical compositions are one direction disguised as choice.

## 3. Evidence-to-decision gate

Create a persistent `direction-decision.md` when the choice is costly to reverse, has multiple stakeholders, affects several surfaces, or must survive across agents/sessions.

The record includes:

- Decision and owner
- Evidence reviewed and date
- Proof artifacts and runtime
- Chosen thesis and rejected alternatives
- Exact elements approved for reuse or mix-and-match
- Locked system/brand constraints and unresolved conflicts
- Risks, confidence, and revisit trigger
- Explicit authorization for any exception; silence is not approval

Do not require a formal file for a tiny reversible task. A concise decision note in the project record is enough.

## 4. Brand and content truth

Use verified identity, product, UI, packaging, campaign, and content evidence when these determine recognition or meaning. Real assets do not supersede approved governance; they operate inside the source-of-truth order defined by the project.

Rules:

- Prefer user-supplied or official primary assets; verify file type, dimensions, variant, date/version, and rights.
- Use current product/UI evidence for current-product claims. Label archival, concept, mockup, or generated material accurately.
- Never redraw a logo, fabricate a screenshot, or infer a product capability merely to complete the composition.
- Use honest placeholders when evidence is unavailable. A labeled gap is better than false specificity.
- Apply the image necessity test: if removing the image does not change meaning, identity, hierarchy, or emotion, it is decoration and must earn its cost.
- Select a small coherent set of strong assets. More assets do not compensate for weak art direction.

Read [brand-and-visual-language.md](brand-and-visual-language.md) for the asset evidence manifest and conflict protocol.

## 5. Production checkpoints

Use checkpoints only where they can prevent meaningful rework.

### Checkpoint A: frame

Confirm authority, assumptions, proof form, real/placeholder content, and success criteria.

### Checkpoint B: direction proof

Show the smallest representative visual proof. Capture feedback as mechanisms: hierarchy, density, contrast, type voice, material, image treatment, motion character, and restraint—not only “like/dislike.”

### Checkpoint C: representative build

Complete one end-to-end slice before scaling production. For a deck, finish two structurally different slides; for an application, complete the critical path and one ordinary state; for motion, prove transitions between key moments rather than isolated frames.

### Checkpoint D: craft and edge states

Tune typography, rhythm, assets, responsive behavior, interaction, errors, loading, localization, accessibility, and reduced motion after the governing direction is stable.

### Checkpoint E: rendered verification

Open, inspect, exercise, and capture the deliverable in its target runtime. Source code, layer structure, or prose is not execution evidence.

## 6. Runtime-aware execution

Do not assume the same tools exist in Codex/ChatGPT, TRAE Work, Hermes, OpenClaw, Coze, a browser-only canvas, or a local development environment.

At the start of production, classify capabilities:

- **Research:** live web, image search, supplied sources only, or offline
- **Asset handling:** download, inspect, transform, generate, or reference only
- **Rendering:** browser, design tool, slide renderer, video renderer, or none
- **Interaction testing:** automated browser, manual browser, device/simulator, or none
- **Visual inspection:** screenshots/images can be viewed, only files can be written, or neither

For every capability required by the chosen proof, record its runtime and dependency state as `present`, `missing`, or `unknown`. When a read-only check confirms a missing installable or enableable dependency, follow [dependency-authorization.md](dependency-authorization.md): emit `authorization_required`, disclose the narrowest exact change and its consequences, and ask the user before mutating the environment.

After the user authorizes installation, verify the dependency and rerun the blocked proof. If the user declines or defers, record that decision and degrade safely:

1. Reduce the number or fidelity of exploratory proofs before reducing truthfulness.
2. Prefer a static representative proof when interactive rendering is unavailable.
3. Provide an executable specification when no renderer exists, and label the visual finish unproven.
4. Never degrade design-system conformance, accessibility, content honesty, provenance, or critical-state coverage.
5. Do not claim that a page was inspected, an interaction clicked, or a visual direction proven unless that action actually occurred.

## 7. HTML and interactive artifact verification

When the deliverable runs in a browser, verify at minimum:

1. **Open:** load the actual entry file or URL in the intended browser/runtime.
2. **Render:** capture the representative viewport after fonts, assets, data, and intentional entrance motion settle.
3. **Errors:** inspect console, network/asset failures, unhandled exceptions, and blank/blocked states.
4. **Viewports:** test the breakpoints and content pressures material to the brief, not only one desktop screenshot.
5. **Critical path:** exercise primary actions, navigation, toggles, forms, recovery, and reset behavior.
6. **States:** inspect loading, empty, error, success, permissions, disabled, focus, and reduced-motion modes where relevant.
7. **Accessibility:** verify keyboard order, visible focus, semantics/names, zoom/text expansion, contrast, and motion preference with appropriate tools and manual inspection.
8. **Performance:** check layout stability, asset weight, interaction readiness, and animation smoothness in the target context.

For responsive safe areas, non-decorative edge contact, partial clipping, sticky/fixed regions, and horizontal scroll endpoints, use [layout-boundary-safety.md](layout-boundary-safety.md) and run the bundled geometry audit. If its runtime is missing, request installation authorization before selecting a fallback.

Automated browser tools can capture screenshots, console output, and repeatable interaction paths, but they do not replace visual inspection or accessibility judgment. A manual run is an explicitly accepted reduced-proof fallback, not the default response to a missing dependency; state exactly what remains unverified.

## 8. Deck, data, and motion proof

### Decks

- Prove at least two structurally different slide types before producing the full sequence.
- Check every slide at presentation size, not only in the authoring canvas.
- Validate pacing, narrative continuity, type size, overflow, source labels, and contrast.
- Avoid turning every slide into the same card grid.

### Data stories

- Verify data, units, source, time window, filters, uncertainty, and update date before visual polish.
- Test the intended takeaway without animation or color alone.
- Preserve accessible tables or equivalent detail when exact values matter.

### Motion

- Define narrative beats, persistent visual anchors, transition logic, rest points, and reduced-motion/static alternatives.
- For long or flagship motion, keep a concise `motion-director-notes.md` with timing, camera/spatial logic, continuity, audio intent, asset dependencies, and export requirements.
- Prefer continuity, transformation, and motivated transitions over a sequence of unrelated pages fading in and out.
- Audio is deliberate only when the delivery context supports it; never force music or sound effects by default.

## 9. Verification evidence bundle

Keep the evidence proportional to the artifact:

- Build/runtime version and tested entry point
- Representative screenshots or renders
- Viewports, modes, and paths tested
- Console/network/validation result
- Known limitations and untested conditions
- Design-system/token audit status
- Accessibility checks and manual-review status
- Verdict: `Ready`, `Ready with conditions`, or `Not ready`

For critique delivery, use three action bands alongside severity:

- **Keep:** mechanisms already supporting intent and worth protecting
- **Fix:** defects or contradictions that block the intended outcome
- **Quick wins:** bounded improvements with favorable effort-to-impact ratio

Do not let “quick wins” displace a systemic fix. Severity and user effect remain the primary prioritization.

## 10. Boundaries

- Random style selection may provoke exploration but cannot authorize a direction.
- Study multiple works and practitioners by mechanism; do not impersonate a living designer or clone a recognizable work.
- A style library is vocabulary, not a substitute for client discovery, research, or judgment.
- Do not require three complete productions when three small proofs can resolve the direction.
- Do not add technical controls, animation, music, or generated imagery merely because the medium permits them.
- Do not hide unsupported claims behind visual realism.

The production chain is complete only when the artifact is truthful, representative, reviewable, and verified in the runtime actually available.
