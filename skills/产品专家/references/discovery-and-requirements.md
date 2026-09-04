# Discovery and Requirements

Use this module to turn uncertainty into an evidence-backed problem definition and traceable requirements.

## Research starts with a decision

Write: `We need to decide [decision]. We currently believe [hypothesis]. The study must reveal [evidence] by [date]. If [threshold], we will [action]; otherwise [different action].`

Do not conduct generic research. Choose methods by claim:

| Claim | Better evidence |
|---|---|
| Problem exists and matters | Past-behavior interviews, observation, support evidence |
| Behavior frequency/scale | Product analytics, logs, survey with behavioral anchors |
| Users can complete a flow | Task-based usability testing |
| Demand is strong enough | Concierge test, commitment, preorder, workflow adoption |
| Technical feasibility | Spike, benchmark, architecture review |
| Business viability | Price/packaging test, unit-economics model, sales evidence |
| Causal impact | Controlled experiment or credible quasi-experiment |

Triangulate consequential decisions with behavioral, qualitative, and quantitative evidence.

## Segment and JTBD frame

Define one primary segment by:

- Situation and trigger
- Desired functional, emotional, and social progress
- Current workflow and alternatives
- Constraints and switching forces
- Frequency, severity, and cost
- Buyer, user, administrator, and affected parties

JTBD statement: `When [situation], I want to [motivation/action], so I can [desired progress], despite [constraint].`

Avoid future-tense “Would you use…?” questions. Ask for the last occurrence, sequence of actions, tools, people, trade-offs, failures, and consequences.

## Opportunity map

Construct:

1. Outcome
2. User opportunities/problems
3. Evidence and affected segment for each
4. Severity, frequency, reach, and strategic relevance
5. Solution mechanisms under the chosen opportunity
6. Assumptions and tests under each solution

Do not compare solutions attached to different outcomes with one score.

## Journey and service blueprint

For the selected persona and scope, map:

| Stage | Trigger | User goal/action | Touchpoint | Emotion/confidence | Friction | Evidence | Opportunity |
|---|---|---|---|---|---|---|---|

For operational products add backstage process, responsible team/system, policy, data exchange, support path, and failure recovery. Distinguish current state from desired future state.

## Assumption map

Cover:

- Desirability
- Viability
- Feasibility
- Usability
- Integrity: safety, privacy, fairness, compliance, trust

Rank by `consequence if wrong x uncertainty x time-to-learn`. Give each critical assumption a test, evidence threshold, owner, and resulting decision.

## Requirement decomposition

Use this hierarchy:

`Outcome -> Opportunity -> Capability -> User flow -> Requirement -> Acceptance example -> Data/event -> Metric`

Give durable items stable IDs, for example `OUT-01`, `OPP-02`, `CAP-01`, `REQ-07`, `EVT-03`.

### Requirement form

For each requirement capture:

- ID and short title
- Actor and permission
- Trigger/precondition
- Observable behavior or business rule
- Success outcome
- Alternate and failure behavior
- Acceptance examples using Given / When / Then where useful
- Source or rationale
- Dependencies
- Data created/read/changed
- Analytics evidence
- Status: confirmed / inferred / assumed

Keep implementation detail out unless it is a constraint or decision already made.

## Flow completeness

Map:

- Entry points and prerequisites
- Primary path
- Decision branches
- Cancel/back/undo
- Loading and progress
- Empty and first-use
- Validation and recoverable error
- System/permission/network failure
- Success and confirmation
- Timeout, concurrency, duplicate submission, boundary values
- Admin/support/audit path where relevant

## PRD structure

1. Decision summary and status
2. Problem, segment, evidence, and cost of inaction
3. Outcome, metric, baseline, target, and guardrails
4. In scope, non-goals, and principles
5. User journeys and flows
6. Requirements with IDs and acceptance examples
7. Content, states, permissions, and business rules
8. Data, analytics, privacy, security, and compliance
9. Dependencies and operational changes
10. Validation and rollout
11. Risks, assumptions, open questions, and owners
12. Decision log and change history when needed

## Requirement quality gate

- Each requirement traces to an outcome/opportunity.
- Rules are deterministic enough to test.
- All affected actors and permissions are covered.
- Edge and failure states are explicit.
- Non-goals prevent scope ambiguity.
- Data and measurement are designed alongside behavior.
- Open questions have owners and decision dates.
