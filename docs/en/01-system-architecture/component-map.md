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
      last_verification_note: "Owner-authorized classification direction for AID-2026-11-26-GOV-DOC-01; not a formal approval record. Pre-metadata content blob: 062e1a2f74690b24ff56365e964c31a4c506d929. Approval remains Draft; evidence verification remains Unverified."
    usage_status: Active
    modification_status: Modified
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "Logical system component map"
    canonical_scope_id: architecture/logical-system-component-map
    canonical_scope_keywords:
      - subsystem
      - owner
      - capability
      - component-boundary
    canonical_conflict_status: None
    normative_status: Normative
  bilingual_counterpart:
    source: "01-system-architecture/component-map.md"
    en: null
    zh-CN: "docs/zh-CN/01-system-architecture/component-map.md"
---
# Logical System Component Map

- Document ID: SYS-COMP-001
- Version: 1.0
- Source: [Normative source specification](../../../01-system-architecture/component-map.md)
- Chinese counterpart: [逻辑系统组件图](../../zh-CN/01-system-architecture/component-map.md)
- Status: DECIDED logical responsibility baseline; implementation boundaries remain design-dependent

This map describes responsibility boundaries. It does not prescribe process, service, or crate boundaries.

## Level 0 — System

**AI Memory Brain** — model- and Agent-independent memory infrastructure.

## Level 1 — Subsystems

### SYS-MEMORY-BRAIN — canonical memory authority

| ID | Logical subsystem | Primary responsibility |
|---|---|---|
| MB-01 | Memory Domain Model | Canonical object semantics, identifiers, typed relations, temporal and epistemic metadata |
| MB-02 | Canonical Memory Store | Durable persistence, version history, canonical reads/writes |
| MB-03 | Memory Lifecycle Manager | Candidate/active/superseded/archive/retract transitions and lifecycle policy |
| MB-04 | Entity & Relationship Manager | Entity identity, resolution, typed relations, graph consistency |

### SYS-MEMORY-COMPILER — experience-to-memory transformation

| ID | Logical subsystem | Primary responsibility |
|---|---|---|
| MC-01 | Event Ingestion Engine | Validate, scope, deduplicate, and durably accept events |
| MC-02 | Extraction & Normalization Engine | Extract candidate memories/claims and normalize structure |
| MC-03 | Evidence & Provenance Manager | Attach source spans, evidence, derivation lineage, and trust metadata |
| MC-04 | Consolidation & Conflict Resolver | Deduplicate, merge, version, qualify, and preserve conflicting claims |

### SYS-MEMORY-RUNTIME — memory serving and context control

| ID | Logical subsystem | Primary responsibility |
|---|---|---|
| MR-01 | Memory Retrieval Engine | Route queries and retrieve candidates across structured, lexical, semantic, temporal, and relational indexes |
| MR-02 | Memory Activation Policy Engine | Decide what memory should be activated, when, and why |
| MR-03 | Memory Context Manager (MCM) | Plan, edit, version, budget, and reconcile scoped memory contexts |
| MR-04 | Context Synchronization Engine | Deliver snapshots/deltas and track adapter acknowledgements and applied versions |

### SYS-CROSS-CUTTING — cross-cutting infrastructure

| ID | Logical subsystem | Primary responsibility |
|---|---|---|
| XF-01 | Storage, Index & Cache Infrastructure | Persistence primitives, index maintenance, cache and runtime working-set support |
| XF-02 | Scope, Permission & Governance Engine | Authorization, isolation, retention, forgetting, audit policy |
| XF-03 | Protocol Gateway & Adapter Contracts | BMCP validation, capability negotiation, telemetry and context message boundaries |
| XF-04 | Consistency, Recovery & Observability | Idempotency, replay, reconciliation support, health, tracing, metrics, audit correlation |

## Owner A–I authority crosswalk

The Level-1 groups below are logical aggregations, not Owner identities and not one-to-one ownership assignments. The Owner namespace is exclusively A–I:

| Logical group | Primary Owner authority | Supporting Owners | Authority boundary |
|---|---|---|---|
| SYS-MEMORY-BRAIN | B for domain semantics; D for canonical Memory identity, persistence/lifecycle and Forget Fence; I for global policy | E, F, G as their workflows require | Aggregate group has no single Owner. B defines domain meaning; D owns canonical mechanics; I owns authorization, retention/legal-hold, external-copy policy and global completion criteria. |
| SYS-MEMORY-COMPILER | E | B, D, I | E owns ingestion/compilation and derivative production; B owns semantic definitions; D controls canonical acceptance/lifecycle; I controls authorization and policy. |
| SYS-MEMORY-RUNTIME | F for retrieval/activation; G for Memory Context authority | B, D, C, H | F owns retrieval/activation; G owns context semantics/version; D remains canonical source; C applies at Agent inference boundary; H owns BMCP wire/protocol semantics. |
| SYS-CROSS-CUTTING | I for global security/governance policy; H for BMCP protocol; C for Agent-side integration | A, B, C, D, E, F, G, H, I according to the specific contract | Storage/consistency execution is shared and contract-specific; no aggregate Owner is invented. Owner A retains cross-system integration/conflict-resolution authority. |

Subsystem IDs (for example, MB-01, MC-01, MR-01, XF-01) identify logical components only. They are not Owner IDs.

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

## Owner reference namespace and citation rule

- Formal accountability references use the exact form `Owner A` through `Owner I`. A bare letter (A–I) is not an Owner citation.
- Logical subsystem references use their `SYS-*` identifier (for example, `SYS-MEMORY-COMPILER`); do not cite a subsystem by a bare letter.
- Responsibility Matrix capability/component labels and P/S participation markers are a separate taxonomy. They do not identify an accountable Owner.
- When a sentence needs both a subsystem and an Owner, name both explicitly (for example, “SYS-MEMORY-COMPILER; accountable Owner E”). Do not infer one from the other.
- Automated enforcement is tracked separately by Issue #1237. Until that check is merged, this section is the manual reference rule, not evidence that a lint gate exists.
