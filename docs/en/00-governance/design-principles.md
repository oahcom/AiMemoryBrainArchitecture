---
document_metadata:
  domain: architecture
  role: normative-standard
  lifecycle:
    approval:
      decision_status: Approved
      approver: "user-authorized operator (delegated by account owner)"
      decision_date: "2026-11-26"
      approved_version:
        scheme: content-hash
        value: "e467d7cf3e8feb0457843b5f4f0fd038b01608c32a9fbe35e585cc41e49c665a"
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-096/approval-evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Usual role: principles constraining subsystem design"
    usage_status: Active
    modification_status: Pending-Reapproval
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
    canonical_scope: "Architecture: design principles"
    canonical_scope_id: "architecture/design-principles"
    canonical_scope_keywords:
      - principle
      - design-rule
      - boundary
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Normative
  bilingual_counterpart:
    source: "00-governance/design-principles.md"
    zh-CN: "docs/zh-CN/00-governance/design-principles.md"
  steward: "user-authorized operator (delegated by account owner)"
---

# Design Principles

- Document ID: GOV-PRINCIPLES-001
- Version: 1.0
- Source: [Normative source specification](../../../00-governance/design-principles.md)
- Source revision: 9fb729a4bd6ebcfa9576e5318804a65e2a95abe2
- Chinese counterpart: [设计原则](../../zh-CN/00-governance/design-principles.md)
- Status: APPROVED / Normative — new approval event dated 2026-11-26. This does not certify implementation conformity with P-01 through P-16.

**Historical status:** Before this new approval event on 2026-11-26, this document was marked `CANDIDATE / Pending-Reapproval — NOT APPROVED`. This records the prior state only. The present decision is a new approval, not a retroactive approval or authentication of any historical approver.

This document defines the principles that constrain all subsystem designs.

## P-01 — Brain authority over memory

**DECIDED.** The Brain is the logical authority for canonical memory assets, their lifecycle, provenance, relationships, and the memory context it manages. An Agent may provide telemetry and events but does not define the Brain's internal memory organization rules.

## P-02 — Agent and model independence

**DECIDED.** The Brain must not depend on a particular Agent framework, model family, model vendor, prompt format, or inference API. Integration differences belong in Adapters and protocol capability negotiation.

## P-03 — Stable Brain-defined contracts

**DECIDED.** The Brain publishes canonical schemas, semantics, lifecycle rules, and synchronization contracts. An Agent Adapter maps native Agent state into those contracts. The Brain does not fork its internal architecture to imitate each Agent's private implementation.

## P-04 — Explicit domain semantics

**DECIDED.** Event, Memory, Fact, Entity, Relation, and Evidence are different objects. A source event may support a memory claim, but it is not itself the claim. A memory may be uncertain, reported, inferred, disputed, or retracted.

## P-05 — Provenance by construction

**DECIDED.** Derived memory must retain traceable source references and derivation metadata. Summarization or compaction must not sever the ability to inspect supporting evidence, subject to retention and privacy policy.

## P-06 — Temporal correctness

**DECIDED.** The system distinguishes at least event time, ingestion/recording time, and validity time. A new claim does not silently erase the historical validity of an older claim.

## P-07 — Intent is not outcome

**DECIDED.** Plans, goals, predictions, and pending actions are represented as such. They must not be promoted to completed events or verified facts without outcome evidence.

## P-08 — Canonical memory versus context

**DECIDED.** Canonical Memory is the durable authority. Memory Context is a task- and scope-specific view assembled from canonical assets. Context edits do not mutate canonical memory.

## P-09 — Context synchronization at inference boundaries

**DECIDED.** Brain-generated context changes become effective through an Adapter at a defined inference-context assembly boundary. The architecture does not assume that an in-flight model inference can be safely rewritten.

## P-10 — Explicit application acknowledgement

**DECIDED.** Delivery, receipt, and application are distinct states. An Applied status requires explicit Adapter acknowledgement for the specified context version. It does not prove that a model attended to or correctly used the content.

## P-11 — Memory is data, not authority-bearing instruction

**DECIDED.** Retrieved or injected memory cannot gain system/developer instruction authority. The Brain must not overwrite system/developer instructions, user-originated input, or Agent security policy.

## P-12 — Scope isolation

**DECIDED.** User, project, Agent, Agent instance, session, and environment scopes are explicit. Environment-specific state (for example, separate game worlds or save files) must not be accidentally mixed.

## P-13 — Explicit governance for forgetting

**DECIDED.** Removing an entry from a working context is not deletion of its canonical memory. Forgetting/retention operations are separate governed workflows that account for derived data, indexes, caches, and backups.

## P-14 — Preserve conflict; do not silently overwrite

**DECIDED.** Conflicting claims retain their sources, temporal scope, epistemic status, and resolution history. Resolution may select a current view, but must not erase the conflict record without an explicit governed operation.

## P-15 — Measured performance

**DECIDED.** Latency, recall quality, resource consumption, and agent-level benefit are measured under reproducible conditions. No performance multiplier is an architectural fact until validated.

## P-16 — Logical architecture before deployment topology

**DECIDED.** A subsystem is a responsibility boundary, not automatically a process, service, or Rust crate. Deployment and code boundaries follow from contracts and measured operational needs.
