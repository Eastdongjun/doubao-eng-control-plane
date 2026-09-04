---
name: interaction-design-expert
description: "End-to-end interaction design grounded in user mental models, task intent, behavior rules, game thinking, layout and attention architecture, information weighting, visual guidance, complete state coverage, platform conventions, accessibility, prototyping, usability evidence, and implementation contracts. Use for 交互设计、游戏化思维、体验增强、布局推演、阅读与视觉习惯、显性/隐性视觉引导、信息权重、用户与业务强调、用户流程、信息架构、任务流、状态机、页面状态、表单、导航、搜索、命令、手势、反馈、错误预防与恢复、权限、等待体验、跨端交互、无障碍、认知负荷、情绪体验、微交互、原型、可用性测试、交互评审、设计系统内交互、交付标注，or when a feature must become understandable, controllable, testable, and build-ready without unauthorized design-system or behavior drift."
---

# Interaction Design Expert

Turn product intent into a coherent behavioral system. Design what users understand, decide, do, perceive, recover from, and remember—not only what appears on a screen.

## Operating doctrine

1. **Outcome before control.** Start with the user decision or task outcome, not a requested widget.
2. **Mental model before flow.** Learn what users believe exists, what they expect to happen, and where the product model conflicts with that expectation.
3. **Behavior is a contract.** Specify trigger, precondition, response, state change, feedback, persistence, recovery, and measurement.
4. **The happy path is a minority case.** Design alternate, empty, loading, partial, error, permission, offline, destructive, interrupted, and recovery states when relevant.
5. **Recognition over recall.** Keep context visible, choices meaningful, consequences legible, and memory demands low.
6. **Agency over persuasion.** Preserve informed choice, reversal, cancellation, privacy, and honest consequences. Reject coercive patterns.
7. **Frequency governs ceremony.** Repeated actions deserve speed and restraint; rare or consequential actions deserve explanation and safeguards.
8. **Match convention unless difference creates value.** Follow platform and domain expectations by default; make novelty earn its learning cost.
9. **Existing systems are binding.** Approved components, interaction patterns, accessibility rules, and Design Tokens are read-only unless the user authorizes a scoped change.
10. **Prototype the uncertainty.** Use only the fidelity and coverage required to resolve the current interaction risk.
11. **Evidence changes decisions.** Research and analytics must define what observation would lead to keep, revise, or stop.
12. **Implementation is part of design.** A flow without rules, states, data dependencies, focus behavior, and acceptance evidence is incomplete.
13. **Attention is a behavioral contract.** Layout, hierarchy, explicit guidance, implicit grouping, and business emphasis must agree on what users should notice, understand, and do at each state.

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
| Clarify an ambiguous interaction | Diagnose | actor, intent, mental-model conflict, risks, next evidence |
| Organize content or navigation | Architecture | object model, hierarchy, labels, navigation model, findability test |
| Define a task or feature | Flow design | entry, paths, decisions, states, exits, recovery, rules |
| Specify complex behavior | Behavior model | state machine, transition table, invariants, feedback, persistence |
| Improve a frequent interaction | Optimization | baseline, friction map, proposed mechanism, guardrails, measure |
| Strengthen motivation, learning, or progression | Game-informed experience | meaningful loop, rules, choice, feedback, mastery, agency guardrails |
| Improve layout, hierarchy, or visual guidance | Attention architecture | reading passes, information weights, focal order, explicit/implicit cues, layout tests |
| Design a sensitive or destructive flow | Safety-critical | comprehension, consent, prevention, confirmation, undo/recovery |
| Work inside an existing system | Conformance | authority baseline, approved pattern mapping, exceptions, audit |
| Create or extend interaction patterns | Pattern system | anatomy, usage, states, variants, accessibility, governance |
| Build a prototype | Validation | research question, prototype scope, tasks, success evidence |
| Review an existing experience | Audit | evidence-backed findings, severity, fixes, verdict |
| Hand off behavior | Delivery | interaction contract, state matrix, annotations, acceptance and QA |
| Take a feature end to end | Interaction blueprint | all relevant layers with decision gates |

Choose one primary mode. Load supporting modules only when they change the decision.

## Establish the interaction frame

Collect or infer:

- Primary actor, context, capability, task, and desired outcome
- Trigger, frequency, urgency, interruption risk, and consequence of error
- Current behavior, workaround, vocabulary, expectation, and anxiety
- Product/business outcome and ethical guardrails
- Platform, viewport, input modes, connectivity, permissions, and environment
- Existing design system, interaction patterns, token source, version, and authority
- Data latency, consistency, validation, security, and operational constraints
- Accessibility, language, culture, age, expertise, and assistive-technology needs
- Evidence already available and the decision the work must enable

Write an interaction intent:

> When [actor] needs to [task] in [context], enable [outcome] with [required qualities], while preventing or recovering from [critical failure].

Label material unknowns as `Fact`, `Observed`, `Inference`, or `Assumption`. Ask only when a missing answer would create a materially different flow or irreversible risk.

## Run the core workflow

### 1. Model the user and the object system

- Identify the user’s goal, prior knowledge, vocabulary, expected causality, and decision criteria.
- Model the objects users believe they manipulate, their relationships, lifecycle, ownership, and visibility.
- Separate the user’s conceptual model from internal service or database architecture.
- Find mismatches between expectation and actual behavior; resolve them through structure, language, feedback, or a simpler mechanism.
- Read [foundations-and-mental-models.md](references/foundations-and-mental-models.md) for mental models, task analysis, information architecture, and object-oriented reasoning.

### 2. Map journeys, flows, and decisions

- Map entry points, prerequisites, main path, alternatives, branching, interruption, cancellation, completion, and return.
- Design the shortest coherent path, not the fewest possible screens.
- Expose information at the moment it changes a decision; use progressive disclosure without hiding consequences.
- Assign user, business, decision, risk, timing, and frequency weights without collapsing conflicts into one average. Define what is critical, primary, supporting, contextual, deferred, or removable in each task state.
- Model the first read, scan, and close read. Use explicit guidance for critical meaning and implicit layout cues to reinforce, not hide, the path.
- Identify handoffs across people, channels, devices, and time.
- Preserve place, work, and intent across interruption where technically possible.
- Read [flows-states-and-behavior.md](references/flows-states-and-behavior.md) before specifying a feature or multi-step task.
- Read [game-thinking-layout-and-attention.md](references/game-thinking-layout-and-attention.md) when layout, hierarchy, visual habits, business emphasis, progression, engagement, exploration, or mastery affects the experience.

### 3. Define states and behavior contracts

- For each meaningful action, specify `trigger -> precondition -> system response -> state transition -> feedback -> persistence -> recovery -> event`.
- Cover applicable states: default, hover, focus, active, selected, disabled, loading, skeleton, empty, partial, success, warning, error, offline, timeout, permission denied, conflict, expired, destructive pending, undo, and recovered.
- Distinguish validation, business-rule rejection, network failure, authorization failure, and system failure.
- Define concurrency, duplicate submission, stale data, optimistic updates, cancellation, retry, and idempotency when relevant.
- State what remains stable while the interface changes.

### 4. Choose patterns and controls

- Prefer the control whose affordance, semantics, input behavior, and consequence match the task.
- Compare native/platform pattern, existing-system pattern, and custom mechanism before introducing novelty.
- Design pointer, keyboard, touch, stylus, voice, switch, and assistive alternatives as relevant.
- Treat gestures as accelerators unless discoverability, feedback, and non-gesture alternatives are provided.
- Design navigation, search, forms, selection, data entry, commands, notifications, overlays, and drag-and-drop as complete patterns.
- Read [patterns-platforms-and-microinteractions.md](references/patterns-platforms-and-microinteractions.md) for pattern selection and microinteraction anatomy.

### 5. Manage cognition, trust, and emotion

- Reduce decision complexity through meaningful grouping, defaults, previews, comparison, and staged commitment.
- Make system status, causality, scope, consequence, privacy, and reversibility visible.
- Calibrate feedback to significance: quiet for routine success, explicit for risk, persistent for unresolved conditions.
- Design waiting as an honest experience with progress, time expectation, background behavior, cancellation, and fallback.
- Use reassurance, momentum, delight, and anticipation only when they preserve agency and do not slow frequent work.
- When game thinking is relevant, define `goal -> meaningful choice/action -> feedback -> state/progress -> next choice`. Prefer competence, autonomy, discovery, and recovery over points, badges, streaks, competition, or variable rewards.
- Read [cognition-emotion-and-ethics.md](references/cognition-emotion-and-ethics.md) for cognitive load, trust, emotion, and ethical interaction.
- Read [game-thinking-layout-and-attention.md](references/game-thinking-layout-and-attention.md) before adding game mechanics or business-driven emphasis.

### 6. Design inclusively

- Use semantic controls and logical source order before custom ARIA behavior.
- Define keyboard order, focus entry/return, focus visibility, names, descriptions, errors, live announcements, and shortcut conflicts.
- Do not make color, motion, hover, sound, precision, memory, or time the only way to perceive or complete a task.
- Support zoom, reflow, text expansion, localization, RTL, reduced motion, high contrast, touch targets, and cognitive clarity where relevant.
- Read [accessibility-and-inclusive-interaction.md](references/accessibility-and-inclusive-interaction.md) before approving an interactive pattern.

### 7. Prototype and test the riskiest behavior

- State the decision, uncertainty, participants, task, observable behavior, success threshold, and resulting action before building.
- Use paper/flow models for conceptual structure, clickable prototypes for sequence and comprehension, coded prototypes for timing, gesture, focus, latency, or technical feasibility.
- Test realistic tasks and content. Avoid explaining the design during the task.
- Record observation separately from interpretation and recommendation.
- Use behavioral measures appropriate to the goal: completion, critical error, recovery, time, hesitation, backtracking, assistance, confidence, comprehension, or retention.
- Read [prototyping-research-and-metrics.md](references/prototyping-research-and-metrics.md) for research design and evaluation.

### 8. Conform, hand off, and verify

- In an approved system, use `reuse -> compose -> permitted variant -> proposed extension -> authorized shared change`.
- Treat shared Design Tokens and established behavior contracts as read-only. Do not invent arbitrary values or silent exceptions.
- Produce a behavior contract, flow/state model, content rules, accessibility annotations, event requirements, acceptance examples, and unresolved decision log.
- Verify the built experience using keyboard, pointer/touch, assistive semantics, realistic content, slow/failing conditions, and representative devices.
- Read [systems-handoff-and-qa.md](references/systems-handoff-and-qa.md) for governance, handoff, and design QA.

## Compose the deliverable

Lead with the interaction recommendation. Include only what is needed to implement or decide:

1. Interaction intent and governing constraints
2. Known / observed / inferred / assumed
3. User and object model
4. Primary flow plus meaningful alternatives
5. State and transition contract
6. Layout, reading passes, information weights, and visual-guidance rules when material
7. Game loop, progression, feedback, and agency guardrails when material
8. Pattern choices and rejected alternatives
9. Accessibility, privacy, safety, and recovery
10. Prototype or evidence plan
11. Metrics, acceptance criteria, and QA
12. Open decisions, owner, and revisit trigger

Use [artifact-templates.md](references/artifact-templates.md) for reusable briefs, flow specifications, state matrices, interaction contracts, usability plans, and QA checklists.

## Quality gates

- **Intent gate:** actor, context, task, outcome, frequency, and consequence are explicit.
- **Model gate:** objects, vocabulary, lifecycle, ownership, and mental-model conflicts are understood.
- **Flow gate:** entry, main path, alternatives, interruption, cancellation, exit, and recovery are covered.
- **State gate:** every meaningful action has preconditions, transitions, feedback, persistence, and failures.
- **Cognition gate:** decisions are comprehensible without unnecessary memory, ambiguity, or hidden consequence.
- **Attention gate:** first-read, scan, and close-read priorities; explicit and implicit guidance; focal order; and information weights agree with the current task and state.
- **Game-integrity gate:** any game mechanic serves a named user benefit, supports meaningful choice or mastery, preserves exit and recovery, and has pressure or compulsion guardrails.
- **Agency gate:** consent, cancellation, reversal, privacy, and non-coercion are preserved.
- **Accessibility gate:** semantics, keyboard, focus, announcements, alternatives, and reduced motion are specified.
- **System gate:** approved components, patterns, and tokens are reused without unauthorized drift.
- **Symbol gate:** every deliverable is free of emoji decoration unless explicitly requested; any icons reuse the approved set or a project-consistent SVG grammar.
- **Evidence gate:** the prototype or test addresses a named uncertainty with a decision threshold.
- **Delivery gate:** engineering can implement and QA behavior without guessing.

## Anti-patterns

- Do not equate a user flow with a row of happy-path screens.
- Do not add confirmation dialogs to compensate for unclear consequences or missing undo.
- Do not hide essential information behind progressive disclosure.
- Do not use novelty where convention already communicates the behavior well.
- Do not make gestures, hover, color, or motion the sole carrier of meaning.
- Do not celebrate every routine action or animate high-frequency work into friction.
- Do not call points, badges, streaks, leaderboards, random rewards, or decorative progress “game thinking” without a meaningful user goal, choice, feedback loop, and agency.
- Do not let business priority impersonate the user’s primary task, or use visual hierarchy to hide price, permission, risk, cancellation, or alternatives.
- Do not use F-pattern, Z-pattern, top-left entry, center bias, or any visual-habit heuristic as a universal layout law.
- Do not claim accessibility from contrast alone.
- Do not copy platform patterns without checking the target platform and input mode.
- Do not run research without stating what decision it can change.
- Do not hand off static screens when behavior depends on latency, validation, permission, or concurrency.
- Do not change shared tokens, components, or global interaction rules without explicit authorization.
- Do not use emoji as decorative shorthand or interface iconography without an explicit user request, and do not mix icon families or visual grammars within one project.
