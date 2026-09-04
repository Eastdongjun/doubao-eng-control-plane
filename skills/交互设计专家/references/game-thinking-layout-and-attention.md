# Game Thinking, Layout, and Attention Architecture

Use this module when a product needs stronger motivation, progression, mastery, exploration, information hierarchy, layout reasoning, visual guidance, or business emphasis. Apply game thinking as a behavioral model, not as automatic points, badges, streaks, competition, or spectacle.

## Contents

1. Decide whether game thinking belongs
2. Model a meaningful loop
3. Enhance experience without manipulation
4. Treat layout as interaction
5. Model visual habits and reading passes
6. Design explicit and implicit guidance
7. Assign information weight
8. Balance user and business emphasis
9. Prototype and verify

## 1. Decide whether game thinking belongs

Game thinking is useful when users benefit from:

- Learning a system or building skill
- Seeing progress through a long or ambiguous task
- Making meaningful choices under clear rules
- Exploring a space, collection, scenario, or strategy
- Receiving immediate, legible feedback
- Recovering, retrying, comparing approaches, or improving mastery
- Coordinating or collaborating around shared goals

Avoid or severely constrain it when:

- The task is involuntary, urgent, financial, medical, legal, safety-critical, or emotionally vulnerable
- Repetition already creates fatigue
- The business benefits from compulsion more than the user benefits from mastery
- Progress, scarcity, status, reward, or loss can mislead or pressure users
- A straightforward workflow would serve the outcome better

Do not add a “game layer.” Identify which game-design mechanism improves the existing task and what harm it could introduce.

## 2. Model a meaningful loop

Use:

`goal -> choice/action -> immediate feedback -> state change -> understanding/progress -> next meaningful choice`

Specify:

- Goal and why the user values it
- Rules, constraints, and available strategies
- Current state, progress, and completion evidence
- Challenge relative to user knowledge and capability
- Feedback timing, meaning, and persistence
- Opportunity to retry, undo, recover, or choose another path
- Progression in competence, access, complexity, or responsibility
- What remains optional and what is required

Prefer mastery, autonomy, discovery, competence, and meaningful choice over reward accumulation. A loop that only drives repeated clicks is not successful game thinking.

### Mechanics decision

| Mechanic | Valid purpose | Main risk |
|---|---|---|
| Progress | Make long work legible | False completeness or pressure |
| Levels/stages | Sequence capability or complexity | Artificial gating |
| Challenge | Support learning and competence | Frustration or exclusion |
| Choice | Enable strategy and ownership | Illusory options |
| Feedback | Explain causality and improvement | Noise or over-celebration |
| Collection | Support discovery or completion | Compulsive accumulation |
| Social comparison | Enable learning or coordination | Shame, gaming, inequity |
| Streak | Support a user-chosen routine | Loss aversion and coercion |
| Variable reward | Rarely justified | Manipulation and vulnerability exploitation |

Require an explicit user benefit, exit, guardrail, and review owner for any mechanic that creates pressure or repeated engagement.

## 3. Enhance experience without manipulation

Improve experience in this order:

1. **Clarity:** users understand the goal, state, rules, and next action.
2. **Control:** users can choose, pause, cancel, undo, and recover.
3. **Momentum:** feedback and progress reduce uncertainty and wasted effort.
4. **Mastery:** the system helps users learn, compare, and become more capable.
5. **Expression:** delight, personality, and memorable moments reinforce meaning.

Do not use expression to cover weak clarity or control. Keep routine repeated actions quiet; reserve stronger acknowledgment for meaningful progress or rare completion.

## 4. Treat layout as interaction

Layout determines what users notice, understand, compare, and act on. Build it from:

- User goal and current decision
- Objects, relationships, and lifecycle
- Information dependencies
- Primary, secondary, and recovery actions
- Frequency, risk, urgency, and reversibility
- Reading direction, language, input mode, viewport, and environment
- Persistent context and what may change

Place information near the action or decision it affects. Keep objects and controls spatially stable across state changes. Use proximity, alignment, containment, sequence, and whitespace to reveal the product model.

Do not select a card grid, dashboard shell, sidebar, or hero layout before the information and behavioral relationships are known.

### Layout stress

Test:

- First use, repeated expert use, and interrupted return
- Long, short, missing, stale, error, and comparison content
- Narrow, wide, zoomed, touch, keyboard, and screen-reader conditions
- Primary task, secondary task, destructive/recovery state, and business message
- Localization, RTL, mixed scripts, data density, and permission differences

## 5. Model visual habits and reading passes

F-pattern, Z-pattern, top-left entry, center bias, and similar models are hypotheses tied to content, language, device, and task. Do not use them as universal laws.

Map three passes:

### First read

The user should identify:

- Where they are
- What changed or matters now
- The main value, task, or problem
- The safest or most likely next action
- Critical status, risk, cost, or constraint

### Scan

The user should locate:

- Sections and objects
- Comparison points
- Primary and secondary actions
- Evidence, progress, status, and exceptions
- Navigation, recovery, and help

### Close read

The user should understand:

- Rules, details, trade-offs, provenance, and consequences
- Fine-grained controls and expert information
- Terms, permissions, data, and decision evidence

Design the passes intentionally. Do not make close reading necessary to discover a critical consequence, and do not make every detail compete in the first read.

## 6. Design explicit and implicit guidance

### Explicit guidance

Use labels, headings, instructions, numbering, progress, contrast, emphasis, directional cues, state messages, and visible action hierarchy.

Use explicit guidance for:

- Critical choices and consequences
- Unfamiliar interactions
- Permissions, cost, privacy, and destructive actions
- Errors, recovery, irreversible changes, and deadlines

### Implicit guidance

Use proximity, alignment, containment, scale relationship, whitespace, rhythm, repetition, continuity, familiar placement, and persistent object identity.

Implicit guidance should reduce explanation, not hide meaning. It cannot be the only carrier of a critical instruction or state.

Motion and color may reinforce guidance but must not be the sole channel. Visual guidance and focus order must tell the same story.

## 7. Assign information weight

Score each information unit or action on an ordinal `0–3` scale:

- **U — user importance:** effect on the user’s current goal
- **B — business importance:** effect on the declared business outcome
- **D — decision criticality:** whether it changes the current choice
- **R — risk:** consequence if missed or misunderstood
- **T — time relevance:** whether it matters now or later
- **F — frequency:** how often the user needs it

Do not collapse the vector into one average when values conflict. A high business score does not cancel low user value or high user risk.

Assign an attention role:

| Role | Use | Expression |
|---|---|---|
| Critical | High consequence, permission, cost, failure, or irreversible decision | Explicit, adjacent to action, persistent until resolved |
| Primary | Current task, outcome, or decisive information | Dominant focal priority |
| Supporting | Needed to complete or compare | Clear and immediately available without competing |
| Context | Orientation, provenance, status, or secondary evidence | Quiet but findable |
| Deferred | Useful after the current decision | Progressive disclosure with a clear route |
| Remove | No user, business, operational, legal, or learning value | Omit |

Use the simplest expression that preserves the required meaning. Invest fine detail where users compare, diagnose, verify, learn, or make costly decisions. Keep repeated and obvious information concise.

## 8. Balance user and business emphasis

Make the business objective explicit and identify whether it aligns, conflicts, or is neutral relative to the user goal.

- Align business emphasis with genuine user value where possible.
- Label promotions, upgrades, recommendations, sponsored content, and automation honestly.
- Do not visually impersonate business priority as the user’s primary task.
- Do not reduce the visibility of price, cancellation, privacy, risk, or alternatives to improve conversion.
- Place business-critical information at the moment it is relevant without interrupting unrelated work.
- Give the primary focal position to the current legitimate decision, not automatically to the highest-revenue action.

When user and business priorities conflict, record the conflict, user harm risk, guardrail, decision owner, and review condition.

## 9. Prototype and verify

Compare representative layouts using the same content, state, viewport, and task.

Test:

- First-read identification
- Scan path and first meaningful action
- Recall versus recognition
- Missed critical information
- Choice comprehension and confidence
- Time, hesitation, backtracking, recovery, and error
- Business-message recognition without task obstruction
- Game-loop comprehension, agency, fatigue, and repeated-use effects

## Quality gates

- Game mechanics serve a named user benefit and preserve voluntary control.
- Layout follows the object, task, decision, and state model rather than a visual template.
- First-read, scan, and close-read priorities are distinct and testable.
- Critical information has explicit guidance and is not carried by color, motion, or position alone.
- Information weight records user, business, decision, risk, timing, and frequency separately.
- Business emphasis does not hide consequence, impersonate user intent, or obstruct the primary task.
- Real content, repeated use, localization, accessibility, and recovery preserve the intended hierarchy.
