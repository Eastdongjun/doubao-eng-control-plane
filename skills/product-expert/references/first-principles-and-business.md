# First Principles and Business Reasoning

Use this module for ambiguous strategy, business analysis, root-cause diagnosis, and consequential product decisions.

## First-principles decomposition

Build the model in this order:

1. **Outcome:** What observable change is valuable? For whom? Over what time horizon?
2. **Actors:** Who experiences, decides, pays, administers, supports, regulates, or bears risk?
3. **Current mechanism:** How does the result happen today, including workarounds and informal labor?
4. **Constraints:** Separate physical, economic, legal, technical, organizational, and contractual limits from preferences or precedent.
5. **Causal mechanism:** What must become easier, faster, safer, cheaper, more trustworthy, or more capable for the outcome to improve?
6. **Evidence:** What has been observed? What is inferred? What is merely assumed?
7. **Alternatives:** Consider process, policy, education, service, integration, pricing, and subtraction before adding software.
8. **Disproof:** What observation would show the model is wrong?

Use “five whys” only while each answer remains causal and evidence-seeking. Stop when another “why” becomes speculation. Use counterfactuals:

- If the requested feature vanished, what outcome would still be needed?
- If this constraint disappeared, what would change?
- If nothing is built, what happens?
- If adoption is high but the business result is flat, what mechanism failed?
- What is the simplest explanation consistent with the evidence?

## Evidence ledger

| Label | Meaning | Appropriate use |
|---|---|---|
| Fact | Verified from a reliable current source | Use directly with provenance |
| Observed | Seen in behavior, data, or research sample | State context and sample limits |
| Inference | Reasoned conclusion from facts/observations | Show the reasoning |
| Assumption | Unverified belief needed by the plan | Add a test or risk treatment |

For important claims, record `claim -> label -> source -> confidence -> consequence if wrong -> next check`.

## Validation effort by risk

Use two dimensions:

- **Consequence:** cost, harm, lock-in, regulatory exposure, migration burden, reputation
- **Reversibility:** how cheaply and quickly the decision can be undone

Low consequence + reversible: use expert judgment, smoke tests, or instrumented rollout.  
High consequence or irreversible: require triangulated research, technical/operational spikes, formal review, staged rollout, and explicit stop rules.

## Business system scan

Analyze the following as a connected system, not separate slides:

### Customer and demand

- Segment by situation, behavior, constraint, and willingness to switch, not demographics alone.
- Identify trigger, job, current alternative, switching cost, urgency, buyer/user/admin differences, and evidence of active demand.
- Distinguish “interesting” from “important enough to change behavior or pay.”

### Value creation and capture

- User value: time, money, risk, capability, confidence, status, or reduced effort.
- Business value: revenue, margin, retention, acquisition efficiency, expansion, cost-to-serve, risk reduction, strategic option value.
- Capture mechanism: price, packaging, usage, cross-sell, retention, reduced operating cost, or ecosystem leverage.
- Identify who receives value, who pays, who approves, and who bears implementation cost.

### Market and alternatives

- Compare direct competitors, substitutes, internal/manual workflows, and “do nothing.”
- Analyze segment-specific strengths, distribution, trust, workflow fit, switching cost, data advantage, ecosystem, and business model.
- Treat feature matrices as evidence only when quality and workflow depth are described, not presence/absence alone.

### Economic engine

When data exists, model ranges for:

- Revenue driver and price/volume relationship
- Acquisition cost and payback
- Gross margin and variable cost-to-serve
- Activation, retention, expansion, churn, and lifetime value
- Capacity constraints and operational load
- Cannibalization, subsidy, or cross-product effects

Run sensitivity on the two or three assumptions that most change the conclusion. Do not hide uncertainty behind a single forecast.

### Strategy and execution

- Strategic fit: mission, positioning, moat, platform/ecosystem, capability building, opportunity cost
- Distribution: how the intended segment learns, evaluates, buys, adopts, and renews
- Operations: onboarding, support, sales, compliance, moderation, content, partner dependencies
- Timing: why now, window duration, prerequisites, and sequencing
- Integrity: privacy, security, fairness, safety, manipulation, environmental or social cost

## Metric tree

Build metrics causally:

`business outcome <- product outcome <- user behavior/value event <- leading signals <- operational inputs`

For every metric specify:

- Definition and formula
- Population, window, and exclusions
- Baseline and source
- Target as a range when uncertain
- Expected causal link
- Guardrails and failure modes
- Owner and decision cadence

Avoid vanity metrics that can rise while the intended outcome falls.

## Decision memo skeleton

1. Decision required
2. Context and non-negotiable constraints
3. First-principles model
4. Evidence ledger
5. Options, including do-nothing
6. Business and user effects
7. Risks and sensitivity
8. Recommendation and trade-offs
9. Revisit/kill triggers
10. Owner, date, and next evidence
