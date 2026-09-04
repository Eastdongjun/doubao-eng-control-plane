# Delivery and Governance

Use this module to turn a product definition into coordinated delivery, safe launch, and reliable learning.

## Handoff package

Provide one traceable package rather than disconnected tickets:

- Outcome, segment, evidence, principles, and non-goals
- Requirements and acceptance examples with stable IDs
- Flow and state coverage
- Content and business rules
- Domain/data/API/event/analytics implications
- Design links or prototype behavior
- Dependencies, decisions, assumptions, and open questions
- Test strategy and rollout/rollback plan

Map each delivery item to the requirement and outcome it serves. Record design or engineering deviations as decisions, not silent drift.

## Readiness review

Review these dimensions:

| Dimension | Ready when |
|---|---|
| Product | scope, acceptance, non-goals, pricing/policy decisions are final enough |
| Experience | flows, states, accessibility, content, support paths are covered |
| Engineering | reliability, performance, security, migration, rollback are verified |
| Data | instrumentation, dashboards, quality checks, ownership are live |
| Operations | support, sales/CS, moderation, finance, legal, and training are prepared |
| Launch | cohort, communication, feature control, thresholds, incident ownership are explicit |

Use `Ready`, `Ready with conditions`, or `Not ready`; name blockers, owners, and dates.

## Rollout design

Prefer staged exposure:

1. Internal or synthetic validation
2. Trusted pilot with direct support
3. Small production cohort
4. Progressive expansion by explicit criteria
5. General availability only after stability and value thresholds

Define:

- Eligibility and exclusion
- Feature flag/configuration owner
- Exposure logging
- Performance, quality, business, and harm guardrails
- Stop/rollback authority
- Data review cadence
- Support/escalation path
- Migration and backward compatibility

Deployment is not release. Code can be deployed while user exposure, policy activation, billing, or model authority remains controlled separately.

## Release control contract

For each material feature flag, configuration switch, entitlement, or staged policy define:

| Field | Required content |
|---|---|
| Control ID and purpose | Stable name and the decision/risk it controls |
| Type and scope | Release, experiment, entitlement, operational kill switch, or permission; environments and services affected |
| Default/failure state | Behavior when the provider, rule, or dependency is unavailable |
| Eligibility and targeting | Population, exclusions, precedence, and evaluation context |
| Exposure record | When evaluation becomes exposure and how it is logged |
| Owner and authority | Who may create, change, expand, pause, or delete it |
| Guardrails | Product, reliability, data, financial, safety, and support signals |
| Observability/audit | Evaluation reason, configuration version, change log, alerts, and incident linkage |
| Lifecycle | Created, review, expiry, cleanup, and permanent-state decision |

Prefer vendor-neutral product semantics even when the implementation uses a specific flag provider. Temporary controls require an expiry and removal owner; stale flags create hidden states and operational risk.

## Decision dashboard

Separate:

- **Adoption:** exposure, activation, repeat use, coverage by segment
- **User value:** task success, time/effort, quality, confidence, retention behavior
- **Business value:** revenue, cost, risk, retention/expansion, strategic effect
- **Quality:** errors, latency, reliability, support burden, data correctness
- **Guardrails:** harm, privacy/security, accessibility, fairness, cannibalization

For every chart state the decision it informs. Include cohort/segment breakdowns where averages can hide failure.

## Post-launch learning loop

At the declared cadence:

1. Validate exposure and data quality before interpreting outcomes.
2. Compare results with baseline, target, guardrails, and confidence.
3. Combine behavior data with support/research evidence.
4. Explain likely mechanisms and alternative explanations.
5. Decide expand, hold, repair, reposition, or retire.
6. Update assumptions, requirements, roadmap, and decision log.

## Decision log

| Date | Decision | Context/evidence | Options | Trade-off | Owner | Revisit trigger |
|---|---|---|---|---|---|---|

Capture material scope, policy, architecture, metric, and launch decisions. A future teammate should be able to understand why the current product behaves as it does.

## Product governance

- Assign a single accountable decider for each consequential decision.
- Give data, design, engineering, legal/safety, operations, and affected customer-facing teams explicit review roles.
- Establish change control for requirements, schemas, policies, and external contracts.
- Set expiry or review dates for assumptions, exceptions, experiments, and temporary flags.
- Preserve an auditable link among evidence, decision, implementation, and outcome.

## Partner, vendor, and continuity readiness

When delivery depends on an external vendor, public-sector acquisition, implementation partner, or another team, define:

- Outcome and acceptance evidence, not only activities or staffing
- Product owner, contract owner, technical owner, and operational owner
- Required access, data rights, portability, security, support, and service levels
- Change-control, incident, escalation, and dispute paths
- Knowledge-transfer artifacts and paired ownership before handover
- Dependency exit plan, data/model export, replacement path, and continuity window
- Procurement, legal, policy, accessibility, and audit constraints that can change sequencing

Treat transfer readiness as a release gate when the original team will not operate the product. A shipped capability without maintainable ownership is unfinished.

Do not let governance become ceremony. The smallest useful governance records irreversible choices, protects users and the business, and accelerates future decisions.

## Research lineage

Release-control concepts are informed by the vendor-neutral principles in the [OpenFeature specification](https://github.com/open-feature/spec). Partner, de-risking, and continuity concepts are informed by the public-domain [18F Guides](https://github.com/18F/guides). The guidance above is product-level synthesis, not an SDK or procurement-specification copy.
