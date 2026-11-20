---
document_metadata:
  domain: architecture
  role: normative-standard
  lifecycle:
    approval:
      decision_status: Approved
      approver: NOT_RECORDED
      decision_date: NOT_RECORDED
      approved_version:
        scheme: git
        value: "a7d12fe9835d8f53403946ab08c1cae8c3f12fbf"
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Applicable-To-Current-Version
      evidence_reference:
        - "00-governance/terminology.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Usual role: terms carrying normative force in this repository"
    usage_status: Active
    modification_status: Unchanged
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    # Translation of the authoritative source. It does not independently
    # claim canonical authority; see bilingual_counterpart below.
    canonical_status: Non-Canonical
    canonical_scope: "Architecture: canonical terminology"
    canonical_scope_id: null
    canonical_scope_keywords:
      - terminology
      - glossary
      - definition
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Normative
  bilingual_counterpart:
    zh-CN: "docs/zh-CN/00-governance/terminology.md"
---

# Canonical Terminology

- Document ID: GOV-TERM-001
- Version: 1.0
- Source: [Normative source specification](../../../00-governance/terminology.md)
- Chinese counterpart: [规范术语表](../../zh-CN/00-governance/terminology.md)
- Status: DECIDED baseline

Terms in this document are normative within this repository. A subsystem specification may refine a term but must not silently redefine it.

| Term | Definition | Not to be confused with |
|---|---|---|
| Brain | The model- and Agent-independent memory authority and its services. | Agent planner or orchestration framework |
| Agent | The system that reasons, plans, chooses actions, and invokes tools or environment controls. | Memory Brain |
| Adapter | Integration component mapping Agent telemetry and applying Brain context changes at an inference boundary. | Policy owner for Brain internals |
| Event | A time-bounded occurrence, observation, report, or state transition captured by the system. | Durable memory or verified fact |
| Memory | A retained, addressable knowledge asset derived from events, documents, user input, or other sources. | Raw event or necessarily true fact |
| Fact / Claim | A proposition about an entity, event, or state, with epistemic and temporal qualifications. | Source evidence itself |
| Entity | An identity-bearing object about which memories and claims can be organized. | A mention/string occurrence |
| Relation | A typed, potentially temporal association among entities, memories, events, or claims. | Unqualified textual co-occurrence |
| Evidence | Source material or observation supporting, refuting, or qualifying a claim. | Confidence score |
| Provenance | Traceable origin and derivation history of a memory or claim. | Similarity score |
| Canonical Memory | The authoritative persisted memory asset and its version/history. | Context-specific rendering |
| Memory Context | A versioned, scoped, task-oriented view of selected memory assets. | Entire memory database or full prompt |
| Context Entry | A reference and presentation of a memory inside a specific Memory Context. | Canonical memory record |
| Applied Context | The context version the Adapter confirms has been applied at the agreed inference boundary. | Proof of model attention |
| Working Set | Runtime-local, bounded set of active memory references/data for low-latency use. | Durable canonical store |
| Telemetry | Structured Agent/task/environment signals used to assess memory needs and outcomes. | Full hidden chain of thought |
| BMCP | Brain Memory Context Protocol: Brain-defined contracts for telemetry, context delivery, acknowledgement, and governance. | Agent-specific private API |
| Scope | Namespace/ownership context for a memory or operation. | Permission |
| Permission | Authorization to perform an operation on a scoped resource. | Scope identity |
| Epistemic Status | How a claim is known or supported (for example, observed, reported, inferred, verified, disputed, retracted). | Lifecycle state |
| Lifecycle State | The management stage of a memory asset (for example, candidate, consolidated, active, superseded, archived). | Truth status |
| Confidence | A calibrated or estimated degree of support, with declared semantics. | Relevance |
| Relevance | Estimated usefulness for a particular task/context at a particular time. | Truth or confidence |
| Event Time | When the represented event occurred. | Ingestion time |
| Recorded At | When the system recorded or ingested the item. | Event time |
| Valid Time | The interval during which a claim is asserted to hold. | Storage retention interval |
| Forget | Governed removal/de-identification workflow for canonical memory and applicable derivatives. | Context Remove |
| Consolidation | Process that evaluates, merges, refines, or relates candidate memories while retaining provenance. | Blind deduplication |

## Required distinctions

- **Epistemic status** answers “what is the basis for knowing this?”
- **Lifecycle state** answers “what management stage is this asset in?”
- **Confidence** answers “how strongly is this claim supported under a declared method?”
- **Relevance** answers “how useful is this memory for this task now?”
- **Scope** answers “where does this asset belong?”
- **Permission** answers “who may perform which operation?”

