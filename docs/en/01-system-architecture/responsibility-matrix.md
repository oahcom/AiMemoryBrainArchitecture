# Subsystem Responsibility Matrix

- Document ID: SYS-RESP-001
- Version: 1.0
- Source: [Normative source specification](../../../01-system-architecture/responsibility-matrix.md)
- Source revision: 85548fcee05b28f8c2d54d4c0a8bf77840c8cdf3
- Chinese counterpart: [子系统职责矩阵](../../zh-CN/01-system-architecture/responsibility-matrix.md)
- Status: DECIDED ownership baseline; detailed boundary questions remain OPEN where stated

Legend: **P** = primary owner; **S** = supporting participant; **—** = not responsible.

| Capability / concern | Domain Model | Canonical Store | Lifecycle | Entity/Relation | Ingestion | Extraction | Evidence | Consolidation | Retrieval | Activation | MCM | Sync | Governance | Consistency |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Canonical object semantics | P | S | S | S | — | S | S | S | S | — | S | — | S | — |
| Durable event acceptance | S | S | — | — | P | — | — | — | — | — | — | — | S | S |
| Candidate extraction | S | — | S | S | S | P | S | S | — | — | — | — | — | — |
| Provenance/evidence linkage | S | S | — | S | S | S | P | S | S | — | S | — | S | — |
| Entity identity and typed relations | S | S | — | P | — | S | S | S | S | S | S | — | S | — |
| Consolidation/conflict handling | S | S | S | S | — | S | S | P | — | — | S | — | S | S |
| Canonical lifecycle transitions | S | S | P | S | — | S | S | S | S | — | S | — | S | S |
| Candidate retrieval | S | S | — | S | — | — | S | — | P | S | S | — | S | S |
| Activation decision | S | — | S | S | — | — | S | S | S | P | S | — | S | — |
| Context planning/editing/versioning | S | S | — | S | — | — | S | S | S | S | P | S | S | S |
| Context delivery/acknowledgement | — | — | — | — | — | — | — | — | — | S | S | P | S | S |
| Scope/permission enforcement | S | S | S | S | S | S | S | S | S | S | S | S | P | S |
| Forgetting/retention governance | S | S | S | S | S | S | S | S | S | — | S | S | P | S |
| Ingress idempotency and receipt replay | — | S | — | — | P | S | — | — | — | — | — | — | S | S |
| Cross-component replay, reconciliation and recovery coordination | — | S | S | S | S | S | S | S | S | S | S | S | S | P |
| Metrics/tracing/audit correlation | — | S | S | S | S | S | S | S | S | S | S | S | S | P |

## Ownership rules

1. A primary owner defines the contract and state transitions for its capability.
2. Supporting components may provide data or execute a sub-step but must not create a competing source of truth.
3. Governance is a cross-cutting enforcement responsibility; each subsystem must still perform local checks at its boundary.
4. The Context Manager owns context version authority. The Synchronization Engine owns delivery tracking, not context semantics.
5. The Canonical Store owns durable storage mechanics; the Domain Model owns meaning and validity rules.
6. The Compiler proposes and transforms memories; canonical lifecycle policy decides whether and how candidates become durable canonical assets.
7. Retrieval returns candidates and evidence; Activation Policy decides whether candidates belong in a context.
8. Agent Adapter applies context at the boundary; it does not become the authority for memory selection or canonical memory.
9. Idempotency ownership is layered: Event Ingestion owns ingress deduplication and original-receipt semantics; the Event Store owns atomic persistence of Event plus compile intent; Consistency/Recovery owns cross-component replay, reconciliation and recovery coordination. Exact idempotency identity fields remain governed by the dedicated idempotency contract, not redefined here.

## Boundary questions to resolve in detailed design

- Whether lifecycle policy is a distinct module or part of canonical domain services.
- Whether entity resolution is synchronous, asynchronous, or hybrid by event class.
- Which consistency operations belong in a shared coordinator versus subsystem-local transactional outboxes.
- Whether Protocol Gateway is a distinct logical subsystem or a façade over BMCP services.

These questions remain design questions; this matrix does not silently decide them.
