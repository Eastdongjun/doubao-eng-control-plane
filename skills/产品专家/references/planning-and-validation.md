# Planning and Validation

Use this module to prioritize, slice, prototype, experiment, and build a learning-oriented roadmap.

## Choose the decision tool

Frameworks organize judgment; they do not create evidence.

| Situation | Useful approach |
|---|---|
| One objective, comparable initiatives, usable estimates | RICE or weighted score |
| Early uncertainty and fast learning | Impact / confidence / ease plus risk retirement |
| Release scope alignment | MoSCoW with a precise definition of “must” |
| Basic vs performance vs delight | Kano, validated by research |
| Portfolio and sequencing | Value, risk, strategic leverage, dependency, capacity |
| User needs | Opportunity importance vs satisfaction |

Always publish raw inputs, confidence, overrides, and rejected items. Scores within different objectives or frameworks are not comparable.

## A better minimum product

Define the minimum as the smallest coherent release that:

- Solves one meaningful end-to-end job for one segment
- Retires the most consequential uncertainty
- Has safe failure and recovery
- Produces decision-quality evidence
- Can be supported and operated

Distinguish:

- **Prototype:** tests comprehension or usability; may be fake
- **Concierge/pilot:** delivers value manually to test demand/workflow
- **Technical spike:** tests feasibility or performance
- **Minimum marketable slice:** real end-to-end value for a narrow segment
- **Operational release:** includes support, analytics, security, migration, and rollback

## Slice vertically

Prefer slices that include interface, rules, data, and feedback for one job. Avoid roadmaps of horizontal layers such as “database first, UI later” unless the layer is a deliberate enabling investment with a named consumer and exit criterion.

For each slice state:

- User/business outcome
- Included flow and states
- Dependencies and enabling work
- Assumption retired
- Acceptance and telemetry
- Rollout cohort
- Exit/expansion threshold

## Roadmap by outcomes and bets

Use time horizons only when evidence supports dates.

| Horizon | Outcome/bet | Evidence | Slice | Dependency | Success/guardrail | Revisit trigger |
|---|---|---|---|---|---|---|

Separate committed work from options. Add capacity for discovery, quality, migration, operational load, and unplanned work. Do not present a long-range feature calendar as certainty.

## Prototype fidelity

Match fidelity to uncertainty:

- Concept/value uncertainty: storyboards, landing tests, concierge
- Information architecture: tree tests, content models, low-fidelity flows
- Interaction/usability: clickable mid-fidelity prototype with realistic content
- Visual trust/brand: high-fidelity key moments
- Technical performance: coded prototype or spike
- Operational viability: service rehearsal or pilot

Prototype only the paths needed to answer the research question. Specify clickable versus static areas and a reset process.

## Usability test design

For each task:

- Scenario gives context without naming the target control.
- Success is observable and time-bounded.
- Record completion, critical error, assistance, path, time, confidence, and qualitative evidence.
- Test recovery and alternate paths, not only success.

Synthesize patterns with participant context; do not turn two anecdotes into prevalence claims.

## Experiment design

Pre-register:

1. Hypothesis: `If [change], then [primary metric] will [direction/magnitude] for [population] because [mechanism].`
2. Unit of assignment and analysis
3. One primary metric and limited guardrails
4. Baseline, minimum worthwhile effect, sample, duration
5. Exclusions and data-quality checks
6. Decision thresholds and practical significance
7. Risks: novelty, seasonality, network effects, spillover, peeking, multiple tests, sample-ratio mismatch
8. Ship / iterate / stop / follow-up rules

Do not use an A/B test when traffic is inadequate, harm is unacceptable, network effects dominate, or qualitative/operational evidence answers the question more directly.

## Validation plan table

| Assumption | Consequence | Evidence now | Method | Sample/window | Pass threshold | Decision if pass/fail | Owner |
|---|---|---|---|---|---|---|---|

Every test must be able to change scope, sequence, design, or the go/no-go decision.
