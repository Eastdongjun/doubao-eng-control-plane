# Product Judgment and Continuity

Load this module when a consequential product decision depends on uncertain forecasts, repeated judgment, institutional knowledge, or a handover between people or teams.

## Treat judgment as a system that can learn

A polished rationale is not evidence that a decision was good. Separate:

- **Decision quality:** whether the choice was reasonable given the information available at the time
- **Outcome quality:** whether the realized result was favorable
- **Process quality:** whether evidence, dissent, uncertainty, ownership, and revisit conditions were handled well
- **Calibration quality:** whether stated confidence matches long-run hit rates

Do not rewrite the original forecast after the result is known. Preserve the evidence available at decision time so luck, hindsight, and skill can be distinguished.

## Run the uncomfortable-question pass

Before committing, ask the smallest set of questions that could overturn the recommendation:

1. What must be true for this mechanism to work?
2. Which actor has a rational reason not to adopt, approve, operate, or renew it?
3. What second-order effect appears if the product succeeds at scale?
4. What evidence would make the preferred option clearly wrong?
5. Which dependency, incentive, policy, or operational burden is being treated as someone else's problem?

Use three to five questions, not a ritual checklist. Stop when the remaining uncertainty no longer changes the decision or risk treatment.

## Create a forecast record

For a decision whose outcome can be resolved later, record:

| Field | Required content |
|---|---|
| Forecast ID | Stable identifier linked to the decision |
| Claim | One falsifiable outcome, not a vague aspiration |
| Probability | Numeric confidence or an explicit range |
| Resolution rule | Observable condition that makes the claim true or false |
| Population/window | Segment, cohort, start date, and resolution date |
| Evidence | Facts, observations, model, base rate, and important assumptions |
| Dependencies | Conditions outside the team's direct control |
| Update policy | What new evidence permits a revision before resolution |
| Owner | Person responsible for resolving and learning from it |

Use probabilities only when the outcome is resolvable. For estimates with a continuous outcome, record an interval and the intended coverage rather than forcing a binary claim.

## Review calibration, not confidence theater

For repeated binary forecasts:

- Resolve forecasts against their predeclared rules.
- Use the Brier score `(probability - outcome)^2` as one diagnostic, not a performance target.
- Group sufficient forecasts into probability buckets and compare stated confidence with observed frequency.
- Review overconfidence, underconfidence, missing base rates, ignored dependencies, and forecast updates.
- Separate calibration by decision class when market, delivery, behavior, safety, and financial forecasts have different evidence systems.

Do not rank individuals from small samples or punish honest uncertainty. Calibration improves only when people can state uncertainty without political penalty.

## Run a decision-outcome review

At the resolution date:

1. Restore the original decision, evidence, forecast, dissent, and constraints.
2. Resolve each forecast without moving its criterion.
3. Compare expected mechanism with observed behavior and operational reality.
4. Identify whether the main error was evidence, model, execution, timing, dependency, or randomness.
5. Record surprises and second-order effects, including positive ones.
6. Decide which principle, assumption, metric, operating rule, or product artifact must change.
7. Name the owner and date for the resulting change.

A retrospective that produces only a narrative is incomplete. It must update a future decision surface.

## Preserve product continuity

For important playbooks, product principles, decision records, metric definitions, schemas, research syntheses, and operating procedures, include:

- Accountable content owner and reviewers
- Status: active, provisional, sleeping, superseded, or retired
- Scope and intended users
- Last verified date, next review date, and freshness trigger
- Evidence and decisions that created the artifact
- Dependencies, exceptions, and known limitations
- Successor or handover owner
- Archive or deprecation rule

Use progressive context: keep active decision material prominent, move dormant context into retrievable references, and retire contradicted guidance. Do not keep every historical detail in the active prompt or briefing.

## Maintain a learning portfolio

Review learning across four levels:

- **Decision:** forecasts, assumptions, dissent, and outcomes
- **Product:** user behavior, value, harm, economics, and quality
- **Operating system:** ownership, support, vendor, policy, and delivery failures
- **Organization:** repeated coordination gaps, lost context, and incentives

Prefer a small learning backlog tied to upcoming decisions. A lesson without an owner, application point, and review date is only documentation.

## Anti-patterns

- Do not confuse a good outcome with a good decision or a bad outcome with negligence.
- Do not backfill probabilities after results are visible.
- Do not create forecasts that cannot be resolved objectively.
- Do not use calibration data as individual surveillance or compensation input.
- Do not let decision logs become append-only archives that never change practice.
- Do not preserve stale guidance merely because it is documented.
- Do not make one universal confidence threshold for decisions with different downside and reversibility.

## Research lineage

This module independently synthesizes product-judgment and continuity principles informed by [PM Brain](https://github.com/andreaskelm/pm-brain) and the public-sector knowledge-sharing practices in [18F Guides](https://github.com/18F/guides). PM Brain uses a non-commercial share-alike license, so no source prose or templates are copied here.
