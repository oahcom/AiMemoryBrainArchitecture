# Architecture Roadmap

## Objective

Complete the system architecture and subsystem specifications before implementation. Progress is measured by architectural clarity and verifiable acceptance criteria, not by code volume.

## Design workflow

### Phase 1 — System architecture baseline

- Define product scope, non-goals, system boundaries, and design principles.
- Establish the system component map and responsibility matrix.
- Define primary data flows and trust boundaries.
- Establish architecture invariants and terminology.
- Identify unresolved architecture questions.

**Exit criteria:** every top-level component has a bounded purpose, explicit ownership, inputs/outputs, dependencies, and known open questions.

### Phase 2 — Domain and subsystem architecture

Specify each subsystem using a common template:

1. Purpose and responsibility
2. Non-responsibilities
3. Core capabilities
4. Internal component structure
5. Data model
6. Input contract
7. Output contract
8. Main workflows
9. State machines
10. Collaboration and dependencies
11. Consistency and transaction semantics
12. Failure and recovery behavior
13. Security and isolation
14. Performance budgets and measurement plan
15. Acceptance criteria
16. Open questions and decision status

Recommended dependency order:

1. Domain Model → Scope & Permission → Lifecycle
2. Event Ingestion → Extraction & Normalization → Evidence & Provenance → Consolidation & Conflict Resolution
3. Retrieval → Activation → Context Management → Context Synchronization
4. Storage & Index → Consistency & Recovery → Governance → Observability

### Phase 3 — System contracts and acceptance

- Define BMCP messages, version negotiation, errors, and compatibility.
- Define Adapter capability tiers and inference-boundary semantics.
- Define consistency, idempotency, replay, and recovery guarantees.
- Define security, retention, deletion, and audit requirements.
- Define measurable system-level acceptance tests.

### Phase 4 — Technology and engineering architecture

Only after the logical architecture is stable:

- Evaluate Rust module/crate boundaries.
- Benchmark storage and index candidates on representative workloads.
- Specify process boundaries and deployment modes.
- Specify resource budgets for the target local hardware.
- Record decisions and trade-offs in ADRs.

### Phase 5 — Prototype and implementation

- Build narrow vertical slices against frozen contracts.
- Validate assumptions with reproducible benchmarks and agent tasks.
- Revise architecture through explicit decision records.
- Do not silently turn experimental behavior into normative guarantees.

## Status vocabulary

| Status | Meaning |
|---|---|
| DECIDED | Normative baseline; changes require an explicit decision record |
| CANDIDATE | Preferred proposal, not yet binding |
| TO_VALIDATE | Requires measurement, experiment, or prototype |
| OPEN | Unresolved question |

## Initial deliverables

1. System Architecture Specification
2. Memory Domain Model Specification
3. Memory Brain Subsystem Specification
4. Memory Compiler Subsystem Specification
5. Memory Runtime Subsystem Specification
6. Memory Context Manager Specification
7. Memory Activation Policy Specification
8. BMCP Protocol Specification
9. Agent Adapter Integration Specification
10. Storage and Index Specification
11. Consistency and Recovery Specification
12. Security and Governance Specification
13. System Test and Acceptance Specification
14. Rust Engineering Architecture and Technology Evaluation

## Working rule

No implementation task is considered ready until its architecture contract and acceptance criteria are sufficiently precise to test independently.
