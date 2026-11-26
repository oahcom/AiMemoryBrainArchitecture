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
        value: "6df99f23052dd5475d22d397cdee160436464dc3a95946fe6d6e12f93aea1071"
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-096/approval-evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Status is DECIDED in the document body. No formal approval record, approver identity or decision date exists in this repository; recorded as NOT_RECORDED rather than inferred."
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
    canonical_status: Canonical
    canonical_scope: "Architecture: system invariants"
    canonical_scope_id: "architecture/system-invariants"
    canonical_scope_keywords:
      - invariant
      - constraint
      - subsystem
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Normative
  bilingual_counterpart:
    en: "docs/en/00-governance/architecture-invariants.md"
    zh-CN: "docs/zh-CN/00-governance/architecture-invariants.md"
---

# Architecture Invariants

**Current version status: APPROVED — Normative.** This document is approved as a Normative governance baseline by a new approval event dated 2026-11-26. This approval does not certify implementation conformity with P-01 through P-16.

**Historical status:** Before this new approval event on 2026-11-26, this document was marked `CANDIDATE / Pending-Reapproval — NOT APPROVED`. This records the prior state only. The present decision is a new approval, not a retroactive approval or authentication of any historical approver.

These invariants are proposed normative constraints for all subsystem specifications and future implementations, subject to the separate approval decision.

| ID | Invariant |
|---|---|
| I-01 | The Brain is the logical authority for canonical memory assets and the memory context it manages. |
| I-02 | Agents do not define or override the Brain's internal memory organization rules. |
| I-03 | The Brain is independent of any specific Agent framework, LLM, or inference vendor. |
| I-04 | Event, Memory, Fact, Entity, Relation, and Evidence are distinct domain concepts. |
| I-05 | Every derived memory retains provenance to its source evidence or explicitly records why provenance is unavailable. |
| I-06 | Intent, plan, prediction, and pending action are not automatically treated as completed outcomes or verified facts. |
| I-07 | Editing Memory Context does not directly mutate Canonical Memory. |
| I-08 | Removing a context entry is not equivalent to forgetting or deleting its canonical memory. |
| I-09 | Context changes are versioned and tied to a base version or an explicit full-snapshot transition. |
| I-10 | A context delivery is Applied only after explicit Adapter acknowledgement. |
| I-11 | Context changes take effect at a defined inference-context assembly boundary. |
| I-12 | Memory content is untrusted data and never acquires system/developer instruction authority. |
| I-13 | Scope and permission are explicit and independently enforced; Agent, task, session, and environment isolation is preserved. |
| I-14 | Conflicting claims are not silently overwritten; provenance and resolution history remain auditable. |
| I-15 | Event time, recording time, and validity time are not conflated. |
| I-16 | Retries of state-changing protocol operations are idempotent under their defined idempotency scope. |
| I-17 | A context version has one authoritative sequence; concurrent changes are serialized or resolved with explicit concurrency control. |
| I-18 | Adapter acknowledgement proves protocol-level application, not model comprehension or behavioral compliance. |
| I-19 | Context compaction preserves source references and the ability to expand details when retained data permits. |
| I-20 | Forgetting and retention governance cover derived records and secondary representations according to declared policy. |
| I-21 | A subsystem boundary does not imply a separate process, service, or crate. |
| I-22 | Performance claims require reproducible measurement on declared hardware, data, and workload. |
| I-23 | Every architecture design or semantic architecture change must include Chinese and English documentation in the same change set, subject only to the governed temporary exception in GOV-DOC-001. |
| I-24 | Architecture documentation acceptance requires bilingual semantic parity, stable-identifier parity, matching decision status, and traceable source revisions. |

## Enforcement expectation

Each subsystem specification must identify which invariants it enforces, which it relies on, and how violations are detected and handled. An implementation review must not waive an invariant implicitly; a change requires an explicit architecture decision record and impact analysis.


## Bilingual documentation enforcement

All architecture Owners must comply with [GOV-DOC-001 Bilingual Architecture Documentation Policy](bilingual-documentation-policy.md). A temporary STALE exception must be explicit, time-bounded, and tracked.
