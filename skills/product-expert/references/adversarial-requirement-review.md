# Adversarial Requirement Review

Use this module to challenge product requirements before commitment. Activate it for consequential, irreversible, cross-role, incentive-sensitive, privacy/security-relevant, operationally complex, or weakly evidenced requirements. The goal is to expose failure conditions and improve the decision, not to reward criticism or delay delivery.

## Contents

1. Match review depth to risk
2. Establish the review contract
3. Challenge through multiple lenses
4. Run the review
5. Classify findings and dispositions
6. Produce the review artifact
7. Apply quality gates

## Match review depth to risk

| Risk profile | Minimum review |
|---|---|
| Low-cost and reversible | One contradiction pass and edge-state check |
| Material workflow or dependency | Structured review across evidence, actors, states, operations, and metrics |
| High-stakes, irreversible, regulated, financial, safety, permission, or platform-wide | Frozen requirement snapshot, independent or role-separated challenge, abuse analysis, pre-mortem, and explicit release verdict |

Do not force a heavy red-team ceremony onto a harmless reversible change. Do not waive review merely because stakeholders already agree.

## Establish the review contract

Freeze the reviewed version and record:

- Decision, requirement IDs, scope, owner, and review date
- Intended user and business outcomes
- Evidence, assumptions, constraints, and unresolved questions
- Review depth and why it matches the risk
- Who argues for the proposal, who challenges it, and who decides
- What finding would block, revise, split, test, defer, or reject the requirement

For material work, separate authorship from challenge. If an independent reviewer is available, give them the requirement, evidence, and constraints without leaking the preferred verdict. If not, run a distinct challenge pass and do not edit the requirement until findings are recorded.

## Challenge through multiple lenses

### 1. Problem and evidence

- Does the evidence prove the problem, affected segment, frequency, severity, and cost?
- Is a requested solution being mistaken for a requirement?
- Which claim is fact, observation, inference, assumption, or stakeholder preference?
- What plausible evidence would falsify the need or selected mechanism?
- Is the requirement solving a root cause, symptom, internal inconvenience, or political demand?

### 2. Actor and incentive conflict

- Who benefits, pays, operates, approves, supports, can be harmed, or can exploit the behavior?
- Which actors can game the rule, metric, permission, workflow, or default?
- Does a local team benefit while users, support, risk, finance, or another product bears the cost?
- Can business emphasis override informed user choice or create coercive behavior?
- What happens for novice, expert, vulnerable, adversarial, and unauthorized actors?

### 3. Scope, rules, and contradictions

- Does every requirement trace to a declared outcome and opportunity?
- Do two requirements, policies, roles, states, or acceptance examples contradict each other?
- Are non-goals precise enough to prevent scope leakage?
- Are boundary values, time windows, precedence, ownership, and source-of-truth rules deterministic?
- Are implementation details being frozen without being genuine constraints?

### 4. State and failure pressure

Attack the requirement with:

- Empty, partial, stale, duplicated, conflicting, malformed, and extreme data
- Loading, timeout, offline, retry, cancellation, interruption, concurrency, and resumed work
- Permission change, role change, account change, expired state, and cross-tenant access
- Dependency degradation, queue delay, partial success, rollback, migration, and version mismatch
- Repeated use, automation, bulk operations, and high-volume behavior

Require observable recovery and completion evidence, not only error copy.

### 5. Abuse, misuse, and integrity

- How could a malicious, careless, rushed, or confused actor misuse the capability?
- Can the feature enable fraud, harassment, manipulation, privacy leakage, unsafe automation, or irreversible loss?
- Can users contest, undo, appeal, inspect history, or reach a human when appropriate?
- Are logging, retention, consent, data minimization, accessibility, fairness, and compliance obligations explicit?
- Does prevention create a new exclusion, surveillance, or operational burden?

### 6. Business and operating reality

- Does the proposal still work under realistic acquisition, conversion, support, service, margin, and retention assumptions?
- Which manual process, policy, training, content, data quality, or support dependency is hidden behind the interface?
- Who owns exceptions, incidents, reconciliation, escalation, and post-launch decisions?
- Can the organization implement and maintain the requirement at the declared quality?
- What opportunity cost or displaced work is omitted?

### 7. Metrics and decision gaming

- Can the primary metric rise while user value, business value, quality, or trust falls?
- Can eligibility, exposure, attribution, timing, or exclusions be manipulated?
- Is the metric measuring an output, proxy, local optimization, or actual outcome?
- Which guardrail catches coercion, low-quality completion, support cost, reversals, harm, or long-term degradation?
- What evidence threshold changes the release decision?

### 8. Reversibility and alternatives

- What is the smallest test or coherent slice that can retire the main risk?
- Can policy, process, content, service, or removal solve the problem better than software?
- What must be true for the rejected alternatives to become preferable?
- What data, contract, migration, or user expectation makes rollback difficult?
- Is there a kill switch, staged rollout, restoration path, and decision owner?

## Run the review

1. Freeze the requirement snapshot and its traceability chain.
2. Restate each material requirement as a falsifiable behavior and acceptance claim.
3. Generate challenges independently from the proposed solution.
4. Record the strongest counterexample, not the largest number of objections.
5. Test contradictions, failure states, abuse paths, incentives, metrics, and rollback.
6. Classify findings by consequence and evidence.
7. Resolve each finding without silently editing the reviewed snapshot.
8. Re-run only the affected lenses after revision.
9. Issue a verdict with residual risk and decision ownership.

## Finding and disposition

| Severity | Meaning | Required response |
|---|---|---|
| Blocker | Likely severe harm, invalid premise, untestable rule, unauthorized access, or unrecoverable failure | Do not approve until resolved or explicitly accepted by the authorized owner |
| High | Material outcome, trust, operational, economic, or compliance risk | Revise, split, test, or add a controlled mitigation before commitment |
| Medium | Significant ambiguity, edge failure, maintenance burden, or metric weakness | Resolve in scope or assign an owner and decision date |
| Low | Limited polish, clarity, or low-consequence case | Fix when efficient or record as accepted |

Disposition options:

- **Survives:** evidence and controls are sufficient
- **Revise:** requirement remains valid but behavior or scope changes
- **Split:** separate value proof, enabling work, or risky capability
- **Test:** evidence is insufficient; run a defined validation
- **Defer:** valid but not justified now
- **Reject:** premise, mechanism, economics, integrity, or opportunity cost fails
- **Accept risk:** authorized owner accepts a named residual risk with review date

## Review artifact

```markdown
# Adversarial Requirement Review: [scope]

Snapshot / requirement IDs / owner / reviewer / date / risk level

## Intended outcome and evidence
## Strongest case for the proposal

## Findings
| ID | Lens | Counterexample or failure | Evidence | Severity | Affected requirement | Resolution |
|---|---|---|---|---|---|---|

## Abuse and failure scenarios
## Metric gaming and guardrails
## Alternatives, rollback, and pre-mortem

## Verdict
Survives / Revise / Split / Test / Defer / Reject / Accept risk

Residual risk / owner / decision date / revisit trigger
```

## Quality gates

- The review attacks claims and mechanisms, not people or job roles.
- The strongest counterargument and counterexample are represented fairly.
- Findings retain evidence, severity, affected requirement, owner, and disposition.
- Agreement, seniority, polish, and prior investment are not treated as proof.
- Review depth remains proportional to consequence, uncertainty, and reversibility.
- The final requirement set preserves traceability and records unresolved residual risk.
