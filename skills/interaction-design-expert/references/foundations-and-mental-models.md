# Foundations and Mental Models

Use this module when the problem is ambiguous, the navigation or object model is unstable, or users repeatedly misunderstand what the product does.

## First-principles decomposition

Separate:

- **Outcome:** the change the actor is trying to create.
- **Actor:** person, role, group, or system with a distinct authority and perspective.
- **Object:** thing the actor believes exists and can inspect or change.
- **Action:** transformation the actor intends.
- **Rule:** condition that permits, blocks, modifies, or explains the action.
- **Evidence:** signal that the action happened and had the intended effect.
- **Constraint:** limit imposed by safety, law, business, platform, technology, or environment.

Do not begin with UI nouns such as modal, tab, wizard, card, or dashboard. Derive controls after the outcome, objects, actions, rules, and consequences are known.

## Mental-model interview

Prefer observed or recalled behavior over preference speculation:

1. Ask the user to describe the last real attempt.
2. Ask what they believed would happen before each consequential step.
3. Ask what terms they used and where those terms came from.
4. Ask how they knew the task was complete or safe.
5. Ask what they did when uncertain, interrupted, or wrong.
6. Ask what they expected to remain unchanged.

Record:

| Element | User belief | Product reality | Cost of mismatch | Design response |
|---|---|---|---|---|
| Object | | | | |
| Action | | | | |
| State | | | | |
| Ownership | | | | |
| Time | | | | |

## Object-oriented interaction model

For each primary object define:

- User-facing name and disallowed synonyms
- Identity and recognisable attributes
- Relationships and containment
- Lifecycle states and permitted transitions
- Ownership, visibility, permission, and sharing
- Primary actions and consequences
- History, versioning, reversibility, and deletion

Use the object model to align navigation, URLs, headings, actions, permissions, and persistence. Do not let each screen invent a different model of the same object.

## Task analysis

For a recurring task capture:

- Trigger and motivation
- Preconditions and needed information
- Decisions and uncertainty
- Physical or cognitive effort
- Dependencies on people or systems
- Frequency, duration, interruptions, and batching
- Error likelihood and consequence
- Completion evidence and follow-up

Distinguish:

- **Goal:** desired state in the world.
- **Task:** meaningful unit of work toward the goal.
- **Action:** atomic user or system operation.
- **Control:** interface mechanism used to invoke an action.

## Information architecture

Organize around user-recognized objects, tasks, and decisions rather than departments or database tables.

Choose and test:

- Organization scheme: object, task, lifecycle, topic, audience, time, geography, or hybrid
- Navigation model: global, local, contextual, utility, history, search, or command
- Label system: familiar, specific, mutually distinguishable, and translation-ready
- Orientation cues: current place, available moves, path back, scope, and state

Validate findability with tree tests, first-click tests, search logs, support questions, or task observation. A tidy sitemap is not evidence that people can find anything.

## Decision rules

- Prefer the user’s stable conceptual model when it does not create falsehood or unsafe behavior.
- Teach a necessary new model through visible objects, consistent language, progressive learning, and feedback.
- Do not expose internal architecture merely because it is easier to implement.
- When expert and novice models differ, preserve a simple default path and provide accelerators without duplicating the underlying truth.
