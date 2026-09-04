# Data and Architecture

Use this module when product behavior must become an implementable domain, schema, API, event, or analytics design.

## Start with the domain

Derive, do not invent:

1. Actors and permissions
2. Entities and their identity
3. Value objects and controlled vocabularies
4. Relationships and cardinality
5. Lifecycle/state transitions
6. Invariants and business rules
7. Commands and domain events
8. Ownership and system boundaries

Name concepts in business language. Distinguish a lifecycle state from a display status, an entity from an event, and source-of-truth data from derived projections.

## Domain model table

| Concept | Kind | Identity/keys | Owner | Lifecycle | Invariants | Sensitive? |
|---|---|---|---|---|---|---|

Add a state-transition table for consequential workflows:

| From | Command/trigger | Preconditions | To | Event | Failure behavior |
|---|---|---|---|---|---|

## Schema design sequence

1. Declare database engine, scale, tenancy, consistency, and retention constraints.
2. List read/write access patterns with expected frequency, selectivity, latency, and ordering.
3. Model normalized truth; denormalize only for a measured or credible access need.
4. Define tables/collections, keys, types, null meaning, constraints, timestamps, and deletion policy.
5. Resolve many-to-many relationships with associative entities when the relation has identity or metadata.
6. Design indexes for named access patterns. Every index has a served query and write/storage cost.
7. Address concurrency, idempotency, uniqueness, optimistic locking, and transaction boundaries.
8. Document partitioning, archival, retention, audit, encryption, and residency where relevant.
9. Plan additive migration, dual-read/write if necessary, backfill, validation, cutover, rollback, and cleanup.

Do not mechanically require the same conventions everywhere. For example, soft delete, UUIDs, and timestamps are context decisions, not universal laws.

## Schema deliverable

- Scope and assumptions
- Mermaid ER diagram with cardinality
- Table/collection definitions and constraints
- Access-pattern-to-index matrix
- Normalization/denormalization decisions
- Data lifecycle, privacy, and audit policy
- Migration/backfill/rollback plan
- Open risks and load-test needs

## API and event contracts

For each operation define:

- Consumer and user intent
- Authorization and tenant boundary
- Request/command schema and validation
- Response/result schema
- Idempotency and concurrency semantics
- Error taxonomy and recovery
- Pagination/filter/sort semantics
- Rate/size/latency expectations
- Versioning and compatibility
- Observability and audit

For events define:

- Past-tense event name and business meaning
- Producer and consumers
- Aggregate/entity identity and correlation/causation IDs
- Event time and processing time
- Required/optional fields with semantics
- Ordering, duplication, late arrival, retry, dead-letter handling
- Schema version and deprecation policy
- PII classification and retention

## Analytics instrumentation

Instrumentation is a decision system, not a click inventory.

Use a naming convention such as `object_action` and define:

| Event | Trigger | Actor | Required properties | Source | Metric/decision | Privacy |
|---|---|---|---|---|---|---|

Include exposure events for experiments, server-side outcome events when truth lives on the server, and identity rules across anonymous/authenticated sessions. Define metric formulas, denominators, windows, exclusions, late data, and data-quality tests.

Avoid sensitive free-text properties, duplicated client/server events without deduplication, and events that cannot be tied to a decision.

## Data contract

Treat a shared dataset or event stream as a provider-consumer agreement, not merely a schema. Specify:

- Contract ID, version, status, effective date, owner, producers, consumers, and support channels
- Business purpose, permitted uses, limitations, service scope, and accountable teams/roles
- Grain, keys, schema, references, field semantics, examples, classifications, null meaning, timezone, units, and currency
- Infrastructure/server/environment, location, format, access method, and authentication boundary
- Freshness, completeness, validity, uniqueness, consistency, availability, and latency expectations with measurement rules
- PII/security classification, purpose limitation, retention, masking, access policy, usage terms, and audit requirements
- Field and dataset lineage, transformations, source-of-truth status, and downstream criticality
- Breaking versus non-breaking changes, compatibility, notice period, consumer impact review, deprecation, migration, and rollback
- Monitoring, validation, enforcement point, alert owner, incident path, and behavior when the contract is breached
- Commercial or chargeback terms when they materially affect product behavior or consumer adoption

Make the contract machine-validatable when the ecosystem can support it, but do not confuse a YAML or JSON schema with the full agreement. Review the currently adopted standard before generating files; avoid anchoring new work to a deprecated contract format.

## Security, privacy, and integrity scan

- Least privilege and permission matrix
- Tenant isolation and object-level authorization
- Authentication/session assumptions
- PII/sensitive classification, minimization, consent, purpose limitation
- Encryption, secrets, audit logs, retention, deletion/export
- Abuse, fraud, moderation, threat boundaries
- Regulatory or contractual requirements
- Failure blast radius and incident response

Flag these for specialist review when stakes exceed product-design competence.

## Research lineage

The data-contract fields were cross-checked against [Open Data Contract Standard v3.1.0](https://github.com/bitol-io/open-data-contract-standard), an Apache-2.0 standard. Its predecessor at `datacontract/datacontract-specification` is deprecated, so this module routes new work to the current standard while remaining implementation-neutral.
