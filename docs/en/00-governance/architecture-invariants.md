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
        value: "6b818d9b1884530bdf208507d6a7913699c8598d4c0f351f238cfaff449c0a3a"
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
      last_verification_note: "Usual role: constraints every subsystem specification must obey"
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
    source: "00-governance/architecture-invariants.md"
    zh-CN: "docs/zh-CN/00-governance/architecture-invariants.md"
---

# Architecture Invariants

- Document ID: GOV-INV-001
- Version: 1.1
- Source: [Normative source specification](../../../00-governance/architecture-invariants.md)
- Chinese counterpart: [架构不变量](../../zh-CN/00-governance/architecture-invariants.md)
- Status: APPROVED / Normative — new approval event dated 2026-11-26. This does not certify implementation conformity with P-01 through P-16.

**Historical status:** Before this new approval event on 2026-11-26, this document was marked `CANDIDATE / Pending-Reapproval — NOT APPROVED`. This records the prior state only. The present decision is a new approval, not a retroactive approval or authentication of any historical approver.

These invariants are proposed constraints for all subsystem specifications and future implementations, subject to separate formal approval.

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

## Supplemental mirror-only section — AID-2026-014 Claim/Fact semantic invariants

> mirror-only supplemental, not part of canonical root. Retained in this EN mirror only; non-normative and not promoted. Whether any statement should be elevated is pending Owner adjudication.

This section is retained as existing supplemental content in this language mirror. It has no corresponding section in the current canonical source `00-governance/architecture-invariants.md`, and therefore is not part of the canonical invariant set by virtue of appearing here. It does not amend or replace the source. Whether to promote these statements into the canonical source is a decision reserved for the relevant content Owner.

- Claim and Fact are independent canonical objects.
- Claim identity is stable across proposition-preserving revisions.
- ClaimRevision is immutable and must be addressed by exact ClaimRevisionRef.
- FactRevision must bind exact ClaimRevisionRef, Evidence, Provenance, Scope, Attestor and Method/Version.
- FactRevision must retain the exact I authorization decision reference.
- F and G must not substitute current-head or semantic-similarity resolution for exact historical revision references.
- Forget enforcement must cover shared Fact dependencies and every declared alternate read path.
- These are semantic invariants, not Schema, DDL, public API or implementation-acceptance approvals.

## Enforcement expectation

Each subsystem specification must identify which invariants it enforces, which it relies on, and how violations are detected and handled. An implementation review must not waive an invariant implicitly; a change requires an explicit architecture decision record and impact analysis.

## Bilingual documentation enforcement

All architecture Owners must comply with [GOV-DOC-001 Bilingual Architecture Documentation Policy](../../../00-governance/bilingual-documentation-policy.md). A temporary STALE exception must be explicit, time-bounded, and tracked.
