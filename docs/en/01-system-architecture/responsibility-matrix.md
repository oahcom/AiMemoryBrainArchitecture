---
document_metadata:
  domain: architecture
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      evidence_reference: []
    evidence_verification:
      verification_status: Unverified
      last_verification_note: "Owner-authorized classification direction for AID-2026-11-26-GOV-DOC-01; not a formal approval record. Pre-metadata content blob: 4f6ad30f4005cfd0b7f275d02b22dbc7d7fbdd57. Approval remains Draft; evidence verification remains Unverified."
    usage_status: Active
    modification_status: Modified
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "Subsystem responsibility matrix"
    canonical_scope_id: architecture/subsystem-responsibility-matrix
    canonical_scope_keywords:
      - primary-owner
      - supporting-owner
      - responsibility
      - capability
    canonical_conflict_status: None
    normative_status: Normative
  bilingual_counterpart:
    source: "01-system-architecture/responsibility-matrix.md"
    en: null
    zh-CN: "docs/zh-CN/01-system-architecture/responsibility-matrix.md"
  steward: "user-authorized operator (delegated by account owner)"
---
# Subsystem Responsibility Matrix

- Document ID: SYS-RESP-001
- Version: 1.0
- Source: [Normative source specification](../../../01-system-architecture/responsibility-matrix.md)
- Source revision: 7fc26ca93f4db3b5074156e76bee3555ac744e3a
- Chinese counterpart: [子系统职责矩阵](../../zh-CN/01-system-architecture/responsibility-matrix.md)
- Status: DECIDED ownership baseline; detailed boundary questions remain OPEN where stated

Legend: **P** = primary component; **S** = supporting component; **—** = not responsible. The matrix columns are capability/component labels, not Owner A–I identities.

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

## Capability-to-Owner crosswalk

The capability columns above are a component taxonomy, not Owner identities. The P/S cells describe component participation only. The authoritative Owner mapping is:

| Capability column | Primary Owner(s) | Supporting Owner(s) | Authority boundary |
|---|---|---|---|
| Domain Model | B | D, E, G | B owns domain semantics and identity meaning; persistence/lifecycle execution remains D. |
| Canonical Store | D | B, E, F, G | D owns canonical Memory mechanics; B defines meaning; E proposes writes; F/G consume canonical state. |
| Lifecycle | D | B, I | D owns canonical lifecycle transitions; I owns global policy constraints, authorization and retention/legal-hold policy. |
| Entity/Relation | B | D, E | B owns identity and relation semantics; D persists canonical state; E may propose derived relations. |
| Ingestion | E | D, I, H, C | E owns ingestion workflow; D owns canonical transaction mechanics; I authorization; H protocol; C Agent-side mapping. |
| Extraction | E | B, D | E produces candidates; B defines domain semantics; D controls canonical acceptance. |
| Evidence | E | B, I, D | E manages evidence/provenance production; B defines semantic references; I governs policy/authorization; D owns canonical lifecycle. |
| Consolidation | E | B, D, I | E transforms candidates; B owns semantics; D owns canonical commit/lifecycle; I supplies policy constraints. |
| Retrieval | F | D, B, G | F owns retrieval; D remains canonical authority; B defines semantics; G owns context boundary. |
| Activation | F | G, C, D | F owns activation policy; G owns context version authority; C supplies Agent-boundary integration; D owns canonical state. |
| MCM | G | F, D, C, H | G owns Memory Context semantics/version; F supplies retrieval/activation input; D canonical identity; C/H execute adapter/protocol boundaries. |
| Sync | Joint: G (delivery intent/state), H (wire and acknowledgement semantics), C (Agent-side application) | D, F | No single Owner controls the whole path. G does not own BMCP wire semantics; H does not own context meaning; C does not choose canonical memories. |
| Governance | I | D and every executing Owner | I owns global authorization, retention/legal hold, external-copy policy, target inventory and completion criteria; each Owner performs local enforcement; D owns canonical Forget mechanics. |
| Consistency | Joint / contract-specific; no single primary Owner | A, B, C, D, E, F, G, H, I as applicable | Transaction, replay and recovery authority is allocated per contract. Owner A coordinates cross-owner conflicts; no blanket transfer of domain authority occurs. |

Shared rows are intentionally joint; this crosswalk does not force a sole Owner where the authority is split.

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

## Owner reference namespace and validation boundary

- `P` and `S` identify primary/supporting component participation only; neither is an Owner role.
- Capability-column names are taxonomy labels, not Owner identifiers. A capability reference does not assign accountability.
- Formal accountability must cite `Owner A` through `Owner I` explicitly and use the Owner crosswalk above. Bare A–I letters and unqualified capability labels MUST NOT be used as Owner references.
- Subsystem identifiers use the `SYS-*` namespace defined by the Component Map.
- Automated detection of ambiguous references is tracked in Issue #1237. Until its checker is merged, this is a manual documentation rule, not a claim of automated enforcement.
