# Prototyping, Research, and Metrics

Use this module when behavior is uncertain, implementation is costly, a redesign needs evidence, or a team must decide whether an interaction is ready.

## Contents

- [Start with the decision](#start-with-the-decision)
- [Choose fidelity by uncertainty](#choose-fidelity-by-uncertainty)
- [Usability study](#usability-study)
- [Observation model](#observation-model)
- [Measures](#measures)
- [Sample-size logic](#sample-size-logic)
- [Post-launch learning](#post-launch-learning)

## Start with the decision

Write:

```text
Decision:
Current belief:
Riskiest uncertainty:
Evidence that would support it:
Evidence that would contradict it:
Threshold:
Action if passed:
Action if failed:
```

Do not prototype merely to demonstrate activity. A prototype is an instrument for learning, alignment, feasibility, or specification.

## Choose fidelity by uncertainty

| Uncertainty | Useful method |
|---|---|
| Vocabulary and grouping | card sort, tree test, content comparison |
| Concept and mental model | story, paper prototype, object model, concept test |
| Flow and comprehension | clickable prototype, first-click/task test |
| Dense expert workflow | realistic interactive prototype with representative data |
| Timing, gesture, focus, latency | coded prototype in the target environment |
| Operational handoff | service walkthrough, role-play, backstage simulation |
| Emotional response | high-fidelity representative sequence with realistic content |
| Technical feasibility | spike with production constraints and observability |

Prototype failure, interruption, backtracking, and recovery when they are part of the risk.

## Usability study

Define:

- Research question and decision owner
- Target behavior and participant criteria
- Context, device, accessibility needs, and prior expertise
- Representative tasks and starting state
- Prototype boundaries and known artificiality
- Observation sheet and severity logic
- Privacy, consent, recording, and data retention
- Analysis method and decision threshold

Use task prompts that express intent, not interface instructions. Ask participants to think aloud only when it will not invalidate timing or cognitive measures.

## Observation model

Record each issue as:

```text
Task and participant:
Observed behavior:
User interpretation or quote summary:
Expected behavior:
Impact:
Frequency:
Confidence:
Likely mechanism:
Recommendation:
Evidence still needed:
```

Separate:

- Observation: what happened
- Interpretation: why it may have happened
- Preference: what someone likes
- Recommendation: proposed response

## Measures

Choose measures that match the decision:

- Task completion and quality
- Critical and noncritical error
- Recovery success and recovery time
- Time on task
- Hesitation, backtracking, rework, and assistance
- First-click correctness and findability
- Comprehension and consequence prediction
- Confidence calibrated against actual success
- Accessibility barrier incidence
- Adoption, repeated use, abandonment, support contact
- Business outcome and harm guardrail

Do not optimize a local speed metric when it creates downstream error, regret, support burden, or loss of trust.

## Sample-size logic

Do not use a universal participant count. Select based on:

- Diversity of user segments and contexts
- Complexity and variability of the task
- Severity of missed problems
- Whether the goal is discovery, comparison, or statistical estimation
- Expected effect size and decision cost

Small qualitative rounds can reveal mechanisms; they do not establish population rates.

## Post-launch learning

Connect:

`Interaction hypothesis -> observable behavior -> event definition -> segment -> baseline -> target -> guardrail -> review date -> owner -> decision`

Combine analytics with qualitative evidence. Event counts reveal behavior, not motive.
