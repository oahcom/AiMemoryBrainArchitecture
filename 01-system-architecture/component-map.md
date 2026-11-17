# Logical System Component Map

This map describes responsibility boundaries. It does not prescribe process, service, or crate boundaries.

## Level 0 — System

**AI Memory Brain** — model- and Agent-independent memory infrastructure.

## Level 1 — Subsystems

### A. Memory Brain — canonical memory authority

| ID | Logical subsystem | Primary responsibility |
|---|---|---|
| MB-01 | Memory Domain Model | Canonical object semantics, identifiers, typed relations, temporal and epistemic metadata |
| MB-02 | Canonical Memory Store | Durable persistence, version history, canonical reads/writes |
| MB-03 | Memory Lifecycle Manager | Candidate/active/superseded/archive/retract transitions and lifecycle policy |
| MB-04 | Entity & Relationship Manager | Entity identity, resolution, typed relations, graph consistency |

### B. Memory Compiler — experience-to-memory transformation

| ID | Logical subsystem | Primary responsibility |
|---|---|---|
| MC-01 | Event Ingestion Engine | Validate, scope, deduplicate, and durably accept events |
| MC-02 | Extraction & Normalization Engine | Extract candidate memories/claims and normalize structure |
| MC-03 | Evidence & Provenance Manager | Attach source spans, evidence, derivation lineage, and trust metadata |
| MC-04 | Consolidation & Conflict Resolver | Deduplicate, merge, version, qualify, and preserve conflicting claims |

### C. Memory Runtime — memory serving and context control

| ID | Logical subsystem | Primary responsibility |
|---|---|---|
| MR-01 | Memory Retrieval Engine | Route queries and retrieve candidates across structured, lexical, semantic, temporal, and relational indexes |
| MR-02 | Memory Activation Policy Engine | Decide what memory should be activated, when, and why |
| MR-03 | Memory Context Manager (MCM) | Plan, edit, version, budget, and reconcile scoped memory contexts |
| MR-04 | Context Synchronization Engine | Deliver snapshots/deltas and track adapter acknowledgements and applied versions |

### D. Cross-cutting infrastructure

| ID | Logical subsystem | Primary responsibility |
|---|---|---|
| XF-01 | Storage, Index & Cache Infrastructure | Persistence primitives, index maintenance, cache and runtime working-set support |
| XF-02 | Scope, Permission & Governance Engine | Authorization, isolation, retention, forgetting, audit policy |
| XF-03 | Protocol Gateway & Adapter Contracts | BMCP validation, capability negotiation, telemetry and context message boundaries |
| XF-04 | Consistency, Recovery & Observability | Idempotency, replay, reconciliation support, health, tracing, metrics, audit correlation |

## External participants

| Participant | Owns | Does not delegate to Brain |
|---|---|---|
| Agent | Reasoning, planning, action selection, tool execution | Brain does not become its planner or executor |
| LLM / Inference Runtime | Model inference and token processing | Brain does not own model internals |
| Agent Adapter | Mapping telemetry and applying context at inference boundaries | Adapter does not redefine Brain memory policy |
| Environment Adapter | Environment events and state observations | Brain does not actuate the environment |
| Skill Library | Executable skills and procedures | Memory records experience; it is not automatically executable code |

## Primary relationships

- Event Ingestion writes durable events and emits accepted-event references to the Compiler.
- Compiler creates candidate memory assets through Brain-owned domain and lifecycle contracts.
- Evidence/Provenance links every derived asset to its origins.
- Consolidation updates canonical assets and publishes change events for indexes and runtime reconciliation.
- Retrieval supplies candidates to Activation and Context Planning.
- Activation Policy evaluates task/telemetry signals and requests context changes.
- MCM is authoritative for each managed context's version sequence.
- Context Synchronization transports snapshots/deltas and records Adapter acknowledgement.
- Governance applies across ingestion, reads, mutations, synchronization, retention, and forgetting.
- Consistency/Recovery coordinates replay, idempotency, repair, and observability across subsystem boundaries.

## Architectural caution

The 16 logical components above are a map of responsibilities, not a mandate to create 16 deployable units. Detailed design may merge or split implementation modules while preserving the ownership boundaries and invariants.
