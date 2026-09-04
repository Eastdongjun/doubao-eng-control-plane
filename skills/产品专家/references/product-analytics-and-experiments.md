# Product Analytics and Experiments

Load this module for metric systems, north-star decisions, funnel or cohort analysis, retention, SaaS economics, experiment design, experiment readout, or product-health diagnosis.

## Start with the decision and causal model

State:

- The decision the analysis will change
- The target population and behavioral context
- The intervention or product mechanism
- The expected causal path from exposure to behavior, user value, and business value
- Alternative explanations and guardrails
- The analysis window and decision deadline

Do not start with available dashboard charts. Start with the decision and derive the required evidence.

## Metric contract

For every decision-critical metric define:

| Field | Required content |
|---|---|
| Name | Stable, unambiguous name |
| Decision use | What decision changes when it moves? |
| Population | Inclusion, exclusion, eligibility, and exposure |
| Numerator/denominator | Exact calculation and deduplication |
| Time | Event time, processing time, timezone, window, and late-arrival rule |
| Segmentation | Required dimensions and privacy constraints |
| Source | Event/table, owner, lineage, and freshness |
| Quality | Completeness, validity, uniqueness, consistency, and acceptable delay |
| Baseline/threshold | Source, uncertainty, minimum worthwhile change, and guardrail |
| Failure behavior | What happens if the metric or pipeline is unreliable? |

Use a metric tree to connect business outcomes, user value, product behavior, input/quality metrics, and harm or integrity guardrails. A single north-star metric is optional; use one only when it does not hide materially different value modes or actors.

## Select the evaluation design

| Question or constraint | Preferred method |
|---|---|
| Randomization is feasible and interference is low | User/account/session A/B test |
| Treatment spills across users or time | Cluster, geo, network, or switchback design |
| Rollout must be staged for operational reasons | Stepped-wedge or cohort rollout with predeclared analysis |
| Randomization is infeasible | Matched comparison, difference-in-differences, interrupted time series, or regression discontinuity when assumptions hold |
| Product behavior is not yet built | Prototype, fake door, concierge, simulation, or shadow evaluation |
| Main uncertainty is usability or comprehension | Task-based qualitative test, not an A/B test |
| Main uncertainty is model quality | Representative offline evaluation plus controlled online validation |

Name the assumptions required by the selected design. Do not imply causality when those assumptions are not defensible.

## Pre-register an experiment

Define before exposure:

1. Decision, hypothesis, mechanism, and minimum worthwhile effect
2. Eligibility, exposure event, unit of assignment, unit of analysis, and identity stability
3. Control, treatments, allocation, stratification, clustering, and contamination risks
4. Primary metric, secondary diagnostics, guardrails, and metric contracts
5. Baseline, variance, minimum detectable effect, significance or posterior rule, statistical power, and sample plan
6. Required duration based on business cycles, novelty, seasonality, carryover, and delayed outcomes
7. Data-quality checks, sample-ratio-mismatch rule, implementation validation, and exclusions
8. Sequential monitoring or fixed-horizon stopping policy
9. Multiple-testing policy and pre-specified subgroup analyses
10. Ship, iterate, extend, stop, and rollback rules

Conventional values such as `alpha = 0.05` or `power = 80%` are choices, not natural laws. Tie error tolerance to decision cost.

## Choose advanced methods deliberately

Use additional methods only when their assumptions and decision value are explicit:

- **CUPED or covariate adjustment:** reduce variance with pre-treatment variables that are predictive and not affected by treatment; lock the specification before reading outcomes.
- **Post-stratification or regression adjustment:** improve balance or transport estimates across declared strata; preserve the original assignment and report both adjusted and unadjusted results.
- **Sequential inference:** permit planned interim decisions with valid error or posterior control; do not disguise repeated fixed-horizon peeking as sequential analysis.
- **Bayesian analysis:** use when priors, posterior decision loss, and uncertainty communication are appropriate; expose sensitivity to the prior and loss rule.
- **Multi-armed bandits:** optimize allocation during learning when immediate reward, fast feedback, low interference, and stable outcomes justify it; do not use them when unbiased long-term causal estimates are the primary need.

Distinguish **inference** from **allocation**. A method that sends more traffic to a current winner may be operationally useful while making treatment-effect estimation, delayed outcomes, or subgroup learning harder.

## Analyze in this order

1. **Integrity:** assignment, exposure, instrumentation, identity, duplication, missingness, latency, sample ratio, and invariant metrics.
2. **Implementation:** confirm the variants actually differed and the intended population experienced the mechanism.
3. **Estimation:** report point estimates, absolute and relative effects, uncertainty intervals, and sample sizes.
4. **Decision relevance:** compare with the minimum worthwhile effect, costs, guardrails, and reversibility.
5. **Heterogeneity:** inspect pre-specified segments and credible interactions; label exploratory slices and correct for multiplicity.
6. **Robustness:** assess novelty, seasonality, attrition, crossover, interference, outliers, and alternative specifications.
7. **Decision:** ship, iterate, continue, stop, or collect different evidence, with owner and revisit trigger.

Never equate `p > threshold` with proof of no effect, or statistical significance with customer or business significance.

## Retention and cohort analysis

1. Define the value-bearing return behavior, not merely login.
2. Choose retention windows from the natural usage cadence; daily, weekly, monthly, contract-period, or event-based retention may be appropriate.
3. Define acquisition, activation, renewal, resurrection, and churn events explicitly.
4. Compare acquisition or activation cohorts using consistent maturity windows.
5. Segment by use case, customer type, plan, channel, tenure, implementation path, and other causal candidates.
6. Inspect survival curves, return intervals, frequency, breadth, depth, and value completion.
7. Treat an “Aha behavior” as a hypothesis: correlation with retention may reflect selection, ability, or prior intent.
8. Combine behavioral evidence with interviews or support evidence before assigning causes to churn.

Do not force D1/D7/D30 onto products whose value cadence is weekly, quarterly, episodic, or contract-driven.

## SaaS and recurring-revenue analysis

At minimum distinguish:

- New, expansion, contraction, reactivation, and churned recurring revenue
- Logo retention, gross revenue retention, and net revenue retention
- Committed, contracted, billed, recognized, collected, and recurring revenue
- Gross margin and marginal cost-to-serve
- Acquisition cost by channel and fully loaded sales motion
- Payback period, cohort contribution, and cash timing
- Customer health signals with evidence of predictive value

Document the exact revenue and cohort policies. Never put one-time services, pass-through fees, or non-recurring usage into recurring revenue without an explicit accounting rationale.

Treat common health thresholds as comparables to investigate, not automatic verdicts. Compare against the company stage, segment, contract length, gross margin, capital constraints, and strategic objective.

## Analysis readout

```markdown
# Analysis: [decision]

## Recommendation
Decision, confidence, owner, and deadline

## Population and metric contracts
Eligibility, exposure, definitions, sources, and quality status

## Method and assumptions
Design, estimand, error tolerance, exclusions, and threats

## Results
Absolute/relative effects, intervals, sample, segments, and guardrails

## Interpretation
Mechanism, alternatives, practical significance, and limitations

## Decision and follow-up
Ship/iterate/stop, rollout, next evidence, and revisit trigger
```

## Anti-patterns

- Do not analyze only users who successfully completed the flow.
- Do not change metrics, exclusions, duration, or segments after seeing results without labeling the analysis exploratory.
- Do not repeatedly peek at fixed-horizon tests and stop at the first favorable result.
- Do not report percentages without denominators, uncertainty, and population definitions.
- Do not attribute a time-series movement to a release without a defensible counterfactual.
- Do not let averages hide failures in high-risk, high-value, or protected subgroups.
- Do not build dashboards whose charts have no owner or decision use.

## Research lineage

The release-to-experiment operating pattern and optional statistical methods were cross-checked against [GrowthBook](https://github.com/growthbook/growthbook). GrowthBook is open core; this module absorbs general product-analysis concepts only and does not reproduce licensed implementation material.
