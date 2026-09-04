# AI Context, Retrieval, and Agents

Load this module when the product requires prompt operations, context management, retrieval-augmented generation, memory, tools, workflow agents, multi-agent coordination, or organizational AI-readiness assessment. Use it together with [ai-product-extension.md](ai-product-extension.md), which governs user value, evaluation, uncertainty, safety, cost, and release.

## Choose the least complex effective architecture

Evaluate in order:

1. Deterministic rules, search, workflow, or conventional software
2. A bounded model call with explicit input/output contract
3. Retrieval or tool use for current, private, or verifiable information
4. A stateful workflow with deterministic orchestration
5. A single agent for variable planning within bounded authority
6. Multiple agents only when specialization, isolation, independent verification, or parallel work creates measured value
7. Fine-tuning or custom models when data, differentiation, quality, latency, or cost justify lifecycle ownership

Complexity is a cost in latency, observability, security, reproducibility, and failure recovery. Multi-agent systems do not inherently have a higher quality ceiling.

## Context contract

Define:

- Task, user, environment, and decision being supported
- Instruction hierarchy and conflict resolution
- Required facts, optional context, and prohibited data
- Source authority, provenance, timestamp, freshness, and expiry
- Token/latency/cost budgets and reserved output space
- Personalization and memory scope, consent, retention, correction, deletion, and portability
- Tool results and external content as untrusted inputs
- Compression, summarization, truncation, and what must never be dropped
- Citation and uncertainty behavior
- Version exposure for model, prompt, retrieval, tools, and policy

Context selection is a relevance and authority problem, not a maximum-token problem.

## Retrieval system design

### Ingestion and knowledge lifecycle

- Inventory sources, owners, authority, sensitivity, update cadence, and deletion obligations.
- Parse structure and preserve headings, tables, relationships, provenance, access control, and effective dates.
- Chunk by semantic and task boundaries; measure retrieval quality before fixing chunk size or overlap.
- Define indexing, re-indexing, tombstones, source deletion, permission change, and stale-content handling.

### Retrieval pipeline

1. Classify the request and determine whether retrieval is required.
2. Apply identity, tenancy, authorization, jurisdiction, and policy filters before content reaches the model.
3. Transform or decompose queries only when evaluation shows value.
4. Use keyword, vector, structured, graph, or hybrid retrieval according to the information shape.
5. Retrieve candidates, deduplicate, rerank, diversify, and enforce authority/freshness rules.
6. Assemble context with provenance and explicit separation between instructions and retrieved content.
7. Generate with citations, coverage checks, contradiction handling, and abstention/fallback.
8. Log privacy-safe traces for evaluation and incident analysis.

Do not choose a universal `top-k`, chunk size, similarity threshold, or reranker. Optimize them against representative questions, answerability, recall, precision, latency, cost, and harm.

### Retrieval evaluation

Measure layers separately:

- Corpus coverage and source freshness
- Permission correctness and leakage rate
- Candidate recall and precision at relevant cutoffs
- Ranking quality and citation support
- Answer faithfulness, completeness, usefulness, and calibrated abstention
- Latency, cost, failure rate, and subgroup or domain performance

A correct final answer can hide a broken retrieval system; a good retrieval result can still produce an unsupported answer.

## Prompt operations

Treat prompts, policies, examples, tool schemas, and output validators as versioned product artifacts.

For every material prompt change:

1. State the intended behavior and affected tasks.
2. Maintain representative fixtures, adversarial cases, and prior bad cases.
3. Test output contract, factuality, instruction following, safety, refusal, injection resistance, latency, and cost.
4. Compare against the current version with predeclared release thresholds.
5. Roll out by cohort or shadow mode where risk warrants it.
6. Record version, model, retrieval, tools, policy, results, and rollback path.

Avoid endlessly appending rules after each failure. Diagnose whether the cause is task design, missing context, retrieval, model capability, tool contract, orchestration, or policy.

## Agent and workflow design

### Define the work contract

- Goal, completion evidence, allowed and denied outcomes
- Inputs, outputs, schemas, state, and lifecycle
- Task decomposition and plan revision rules
- Tool catalog with least privilege, scopes, rate limits, and side-effect class
- Per-action authorization, confirmation, and human approval gates
- Time, token, monetary, retry, recursion, and concurrency budgets
- Checkpointing, idempotency, compensation, cancellation, timeout, and recovery
- Audit trail, provenance, versioning, and user-visible progress

### Select orchestration deliberately

| Pattern | Use when |
|---|---|
| Deterministic workflow | Steps, transitions, and failure behavior are known |
| Router + specialists | Requests vary but each path has bounded responsibilities |
| Planner + executor | Plans must adapt, while execution remains constrained and observable |
| Generator + verifier | Independent critique catches material errors and incentives are separated |
| Parallel workers | Tasks are independent and latency or perspective benefits outweigh cost |
| Multi-agent negotiation | Distinct goals or authorities genuinely need reconciliation; use rarely |

Define message schemas, ownership of shared state, precedence, conflict resolution, stopping conditions, and final accountability. A coordinator must verify and reconcile outputs, not merely concatenate them.

### Memory

Separate:

- Working state required to finish the current task
- Session history needed for continuity
- User preferences with consent and correction
- Domain knowledge with provenance and freshness
- Audit records required for accountability

Never use conversation history as an unbounded database. Define write criteria, retrieval criteria, conflicts, expiry, deletion, and sensitive-data exclusions.

## AI-readiness assessment

Assess evidence across:

- Business strategy and use-case value
- Data authority, quality, rights, governance, and feedback loops
- Model, retrieval, evaluation, deployment, and observability capability
- Product interaction, uncertainty, human control, and support readiness
- Team roles, ownership, incident response, and change capacity
- Security, privacy, compliance, intellectual property, abuse, and ethics
- Economics: build/run cost, latency, human review, support, and downside exposure

Do not produce a universal maturity score from arbitrary weights. If scoring aids comparison, define evidence anchors, weights from decision risk, uncertainty, and the actions associated with each level.

## Minimum AI-system deliverable

1. Architecture decision and simpler alternatives rejected
2. Context/retrieval/tool/agent contracts
3. Permission and human-control model
4. Evaluation set, layer metrics, release thresholds, and bad-case taxonomy
5. Cost, latency, availability, and capacity budgets
6. Failure, abstention, recovery, rollback, and incident paths
7. Versioning, monitoring, audit, and improvement governance

## Anti-patterns

- Do not add agents because a task sounds complex; first test a bounded workflow or single agent.
- Do not let retrieved content override system policy or grant permissions.
- Do not expose tools with broader scopes than the current task requires.
- Do not treat model confidence language as calibrated probability.
- Do not evaluate only happy-path prompts or average scores.
- Do not store user context indefinitely by default.
- Do not optimize prompt, retrieval, and model simultaneously without attribution.
- Do not allow autonomous external side effects without explicit authority, safeguards, and auditability.
