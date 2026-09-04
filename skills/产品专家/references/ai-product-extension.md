# AI Product Extension

Load this module for probabilistic, generative, predictive, recommendation, retrieval, or agentic behavior.

## Justify AI

Answer before solution design:

- What user outcome needs probabilistic inference, generation, or adaptation?
- Why are deterministic rules, search, templates, or workflow changes insufficient?
- What is the cost of a wrong, delayed, unsafe, or unavailable result?
- Can the user verify and correct the output?
- Is the expected quality, latency, cost, and privacy profile viable?

If AI adds uncertainty without meaningful user value, recommend the deterministic alternative.

## AI product contract

Define:

1. Task and supported/unsupported scope
2. Input context, data rights, freshness, and privacy boundary
3. Model/system approach and reasons
4. Output format, provenance, citations, and confidence behavior
5. Evaluation dimensions and segment-specific ship thresholds
6. Human control, review, correction, undo, and escalation
7. Fallback for low confidence, unsafe output, latency, quota, outage, and tool failure
8. Cost and p95/p99 latency budgets
9. Security, abuse, prompt injection, data leakage, and harmful action boundaries
10. Rollout, monitoring, drift, regression, and rollback

## Evaluation design

Create a representative, versioned evaluation set covering:

- Common tasks and critical workflows
- Edge cases and adversarial inputs
- User segments, languages, and contexts
- Known failure modes
- Safety and policy cases
- Tool/retrieval failure and stale data

Use task-appropriate metrics. Combine deterministic checks, model-based grading only where calibrated, and human evaluation for subjective/high-stakes dimensions. Report confidence intervals or reviewer agreement where meaningful.

Set an explicit release threshold for each critical dimension; averages must not hide catastrophic subgroup or safety failures.

## UX of uncertainty

- Calibrate claims to evidence; do not present generated output as system truth.
- Reveal source/provenance when it affects trust.
- Make correction and recovery cheaper than starting over.
- Ask for clarification when ambiguity is decision-relevant.
- Use previews/confirmations before consequential actions.
- Show progress and allow cancellation for long tasks.
- Preserve an action/audit trail for agents.
- Provide a non-AI or human path when risk or accessibility requires it.

## Agentic systems

For systems that act, specify:

- Allowed tools/actions and denied actions
- Read vs write boundary
- Approval checkpoints based on consequence
- Spending, rate, scope, and time limits
- Idempotency and duplicate-action prevention
- Sandboxing and secret isolation
- Observation/action logs and user-visible receipts
- Stop, pause, resume, and rollback semantics
- Escalation when confidence or authority is insufficient

## Production monitoring

Track:

- Task success and user correction/override
- Quality regressions by segment and task
- Safety/policy incidents
- Retrieval/tool success and grounding quality
- Latency, availability, timeout, and cost
- Model/prompt/retrieval version exposure
- User trust signals, complaints, and support load
- Data/model drift and evaluation-set freshness

Never improve the model from user data without a declared consent, privacy, retention, and governance boundary.
