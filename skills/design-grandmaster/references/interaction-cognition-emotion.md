# Interaction, Cognition, and Emotion

Use this module to design behavior that is understandable, efficient, trustworthy, and emotionally appropriate.

## Interaction contract

For each meaningful action specify:

| Element/action | Affordance | Trigger/input | Immediate feedback | System result | Duration/progress | Error/recovery | Keyboard/AT |
|---|---|---|---|---|---|---|---|

Cover hover only as enhancement; the action must work without hover. Distinguish disabled, unavailable, and permission-restricted states and explain what the user can do next.

## Cognitive principles as tools

- **Recognition over recall:** keep choices, context, examples, and recent state visible.
- **Chunking:** group by meaning and task; do not merely break content into equal cards.
- **Progressive disclosure:** reveal advanced or conditional detail when needed; never hide cost, risk, or irreversible consequences.
- **Hick-Hyman effect:** reduce irrelevant choices, create meaningful categories, and provide sensible defaults; do not remove necessary control.
- **Fitts's law:** make frequent/important targets easy to acquire, adequately sized, and well placed; separate destructive targets.
- **Jakob's law/mental models:** preserve familiar conventions for routine actions; spend novelty where it creates unique value.
- **Gestalt:** use proximity, similarity, continuity, common region, closure, and figure/ground to express structure. Do not use identical styling for unrelated actions.
- **Von Restorff effect:** reserve contrast for the genuinely primary or exceptional item.
- **Cognitive load:** remove redundant decisions, keep context, use defaults, and stage complexity. Do not mistake low information density for low cognitive load.
- **External cognition:** show progress, selected filters, history, summaries, and comparisons so memory is not the interface.

Use principles to explain a specific user effect, not to decorate critique with law names.

## Usability heuristics

Evaluate relevant behavior for:

1. Visibility of system status
2. Match with the real world
3. User control and freedom
4. Consistency and standards
5. Error prevention
6. Recognition rather than recall
7. Flexibility and efficiency
8. Aesthetic and minimalist design
9. Error recognition, diagnosis, and recovery
10. Help and documentation

## Error and recovery design

- Prevent when cost is high; validate at the right moment.
- Preserve entered data and context after failure.
- State what happened, why if known, what was affected, and the next action.
- Put errors near the source and summarize when the user must scan a long form.
- Provide undo for reversible actions; require proportionate confirmation for destructive ones.
- Do not blame users or expose internal codes without a useful explanation.

## Waiting and uncertainty

- Respond immediately to input.
- Use skeletons when structure is known, progress when measurable, and honest indeterminate status otherwise.
- Set expectations for long or asynchronous work.
- Allow cancellation or background continuation when feasible.
- Preserve partial results and offer retry/fallback.
- Avoid fake progress and false certainty.

## Emotional design

Reason across:

- **Visceral:** immediate sensory impression and perceived quality
- **Behavioral:** fluency, control, feedback, competence, and reliability during use
- **Reflective:** meaning, identity, trust, values, and memory after use

For each key moment define:

`current emotion -> desired emotion -> design mechanism -> evidence -> risk of overdoing it`

Useful mechanisms:

- Trust: transparency, provenance, consistency, preview, clear consequences
- Control: undo, cancel, editable defaults, reversible exploration
- Confidence: orientation, examples, validation, status, confirmation
- Momentum: visible progress, reduced re-entry, sensible next action
- Relief: successful recovery, saved work, plain language
- Delight: apt surprise after core utility works, not before
- Pride/identity: meaningful milestones and respectful personalization

Use peak and ending moments deliberately, but do not manipulate memory to conceal a poor journey.

## Ethical behavior design

Prohibit:

- Hidden cost or consequences
- Forced continuity, difficult cancellation, or obstruction
- False scarcity, fake social proof, countdown pressure
- Confirmshaming and guilt
- Preselected consent or privacy-invasive defaults
- Attention traps and infinite engagement without user value
- Visual interference that steers users away from their stated interest

Behavior design should help users achieve their own goals with informed agency.

## Motion principles

Motion must explain one of: state change, spatial relation, causality, hierarchy, progress, or focus. Keep duration and easing consistent by purpose. Preserve input responsiveness. Provide a reduced-motion equivalent that retains meaning.
