# Organization and Product Operations

Load this module for stakeholder alignment, decision rights, cross-functional delivery, product intake, roadmap governance, sprint or flow planning, release communication, feedback operations, or organizational adoption.

## Treat organization as part of the product system

A correct product decision can still fail when authority, incentives, capacity, policy, adoption, or operational ownership are missing. Map the organization with the same rigor as the user journey.

## Stakeholder and decision map

Identify people by role in the decision, not only title:

| Field | Questions |
|---|---|
| Role | Decider, recommender, executor, operator, user, approver, blocker, expert, or informed party? |
| Stakes | What outcome, risk, budget, status, workload, or obligation changes for them? |
| Authority | What can they approve, veto, fund, stop, or escalate? |
| Evidence | What do they know, and what evidence will change their view? |
| Position | Supportive, conditional, neutral, opposed, or unknown? |
| Incentive/conflict | Where do local incentives diverge from the product outcome? |
| Engagement | What decision, message, format, timing, owner, and feedback channel are needed? |

Use power-interest or influence-impact maps as views, not as substitutes for understanding incentives and decision rights.

## Define decision rights

Choose one lightweight model appropriate to the organization:

- **DACI:** Driver, Approver, Contributors, Informed
- **RAPID:** Recommend, Agree, Perform, Input, Decide
- **RACI:** Responsible, Accountable, Consulted, Informed, primarily for execution ownership

For each material decision define the single final decider, decision deadline, required inputs, escalation path, and how the decision will be recorded. Do not use multiple responsibility matrices for the same decision unless they resolve different layers.

## Alignment workflow

1. Frame the decision, non-decision, deadline, and consequences of delay.
2. Pre-wire high-impact stakeholders with the evidence and trade-offs they need.
3. Surface conflicts in outcomes, incentives, risk tolerance, definitions, or resource commitments.
4. Separate consultation from approval; listening does not imply veto power.
5. Run the decision meeting around options, evidence, risks, and a named decision owner.
6. Record the decision, rationale, dissent, assumptions, commitments, and revisit trigger.
7. Confirm operational ownership after launch; delivery ownership is not automatically business ownership.

## Product intake and feedback operations

For every request or signal capture:

- Source, actor, segment, situation, current workaround, and frequency
- Problem evidence and consequence, not only requested solution
- Revenue, risk, support, strategic, and contractual context
- Related requests, opportunities, requirements, and decisions
- Status, owner, response, and closure reason

Cluster requests by underlying job or failure mode. Volume is not importance: one high-risk compliance failure may outweigh hundreds of preferences, while repeated low-context requests may share no root cause.

Close the loop with the source when appropriate. Explain what was decided, why, what changed, and when evidence could reopen the decision.

## Roadmap and portfolio governance

- Express roadmap items as outcomes, bets, enabling capabilities, or obligations rather than feature promises when uncertainty remains.
- Maintain capacity for committed operations, quality, security, regulatory work, discovery, and incidents.
- Make dependencies, decision dates, evidence gaps, and confidence visible.
- Define who can add, remove, accelerate, or stop work and what trade-off is required.
- Review the portfolio when strategy, evidence, capacity, risk, or dependency changes; do not wait for a calendar ceremony.

Do not impose a universal buffer percentage or priority quota. Size contingency from uncertainty, interruption history, and consequence.

## Delivery planning

Use the team's actual delivery model: continuous flow, Scrum, Kanban, milestones, dual-track discovery, or another explicit system.

For a delivery slice define:

- Outcome or risk retired
- Requirements and acceptance evidence
- Owner and collaborators
- Dependencies and external commitments
- Readiness criteria and unresolved decisions
- Observability, rollout, support, migration, and rollback
- Definition of done that includes quality, data, security, documentation, and operational handoff as applicable

Capacity plans must distinguish planned work, operational load, leave, support, interrupts, and specialist constraints. Historical velocity is evidence about a specific team and work system, not a productivity target.

## Release communication

Tailor communication by audience:

| Audience | Required content |
|---|---|
| Users | Value, who is affected, what changed, how to use it, limits, support, feedback |
| Operators/support | Eligibility, workflow, failure modes, escalation, known issues, rollback status |
| Sales/success | Positioning, qualification, availability, pricing/policy, objections, customer migration |
| Executives | Outcome, evidence, risk, investment, decision required, next review |
| Engineering/data | Version, dependencies, migration, instrumentation, observability, incident ownership |

State known limitations plainly. Release notes are not marketing copy when users need to change behavior or understand risk.

## Organizational readiness gate

Before rollout verify:

- Decider and operational owner are named
- Resource and policy commitments are real
- Incentive conflicts and unresolved objections are visible
- Training, support, sales, success, data, security, and legal responsibilities are assigned where relevant
- Affected teams know the timing, scope, eligibility, failure path, and feedback channel
- Decision and escalation records are accessible

## Knowledge ownership and freshness

Treat product knowledge as an operated asset. For decision briefs, research syntheses, metric definitions, playbooks, product principles, schemas, and support procedures, record:

- Accountable content owner and required reviewers
- Active, provisional, sleeping, superseded, or retired status
- Last verified date, next review date, and event-based freshness triggers
- Scope, audience, evidence lineage, exceptions, and dependencies
- Successor or transfer owner and a recoverable archive path

Use review ownership similar to code ownership for high-impact product guidance. When teams change, transfer the decision context, failure modes, and operating knowledge—not only the latest artifact. Stale documentation should be visibly marked or retired instead of silently trusted.

## Anti-patterns

- Do not interpret seniority as complete knowledge or automatic approval.
- Do not use “leadership asked for it” as the problem statement.
- Do not promise every stakeholder request to avoid conflict.
- Do not turn stakeholder communication into status broadcasting with no decision use.
- Do not use velocity, story points, or utilization as individual performance metrics.
- Do not launch without a named operator, support path, and authority to stop rollout.
- Do not collect feedback without ownership, response, and closure.

## Research lineage

Knowledge ownership, review responsibility, and reusable playbook concepts were informed by the public-domain [18F Guides](https://github.com/18F/guides). They are adapted here for general product organizations rather than copied as a government delivery process.
