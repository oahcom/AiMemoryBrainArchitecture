---
document_metadata:
  domain: memory-brain
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-150/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-26"
      last_verification_note: "Metadata and three-way counterpart links added; mirror body is unchanged. Structural correspondence reviewed; this is not a certified line-by-line translation review."
    usage_status: Active
    modification_status: Modified
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "D canonical commit cursor, aggregate revision and lifecycle cursor semantics"
    canonical_scope_id: "memory-brain/commit-cursor-semantics"
    canonical_scope_keywords:
      - "memory-brain"
      - "canonical-commit-cursor"
      - "aggregate-revision"
      - "index-watermark"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "03-memory-brain/commit-cursor-semantics.md"
    en: null
    zh-CN: "docs/zh-CN/03-memory-brain/commit-cursor-semantics.md"
---
# Canonical Commit and Cursor Semantics

- Document ID: D-CURSOR-001
- Version: 1.0
- Source branch: session-d-memory-brain-2026-11-16
- Source revision: DEREFERENCED — historical source blob `4688a0ca487bf4d853c7f0220408abe8d743d159` retained; no current normative source path exists.
- Source branch head audited: 6b654d5cffaeb71b01f2b0750daa0abc14eb64b3
- Source: DEREFERENCED — original normative path `03-memory-brain/commit-cursor-semantics.md` is absent from the current main tree; alternative: [surviving Chinese counterpart](../../zh-CN/03-memory-brain/commit-cursor-semantics.md) (blob `dd3887a46cf34e9958282fb0a495ae79c2f655e7`; translation only, not an authoritative substitute).
- Chinese counterpart: [Canonical Commit 与 Cursor 语义](../../zh-CN/03-memory-brain/commit-cursor-semantics.md)
- Owner: Session D — Memory Brain Principal Architect (canonical cursor authority only)
- Status: D canonical semantics DECIDED; storage-engine implementation and E/F/G consumer conformance OPEN
- Related: D-REV-P1-002, INT-P1-06, INT-P0-03

## 1. Decision

D chooses one globally ordered CanonicalCommitCursor per Canonical Memory authority, plus independent per-aggregate revisions and per-Memory LifecycleEvent cursors. There is no per-aggregate canonical commit sequence. This makes cross-aggregate transaction order explicit while preserving local revision numbering. It does not imply a distributed global clock across multiple Brain authorities.

## 2. Typed cursor registry

| Type | Shape (domain-level, not wire schema) | Owner | What it orders / proves | What it does not prove |
|---|---|---|---|---|
| CanonicalCommitCursor | (brain_authority_id, commit_sequence) | D | Successful canonical transactions in one Brain authority | Index application, Context state, Forget suppression or physical deletion |
| AggregateRevision | (aggregate_type, aggregate_id, revision_sequence) | D | Immutable revisions of one aggregate | Global order across aggregates |
| LifecycleEventCursor | (memory_id, lifecycle_event_sequence, event_id) | D | Append-only lifecycle events for one Memory | Aggregate revision or cross-aggregate order without its commit cursor |
| IndexWatermark | (index_id, partition_id, applied_through: CanonicalCommitCursor, coverage_version, schema_version) | F | Contiguous canonical commit prefix accounted for by one index partition | That every target is deleted/suppressed or that Forget is complete |
| ForgetFenceCursor | (forget_operation_id, fence_generation, target_set_digest) | D | Monotonic suppression fence for exact target set/lineage | A commit position, index progress, G ContextVersion or I policy epoch |
| ContextVersion | G-owned immutable version ref/sequence | G | Desired managed Context state | Canonical Memory revision or Adapter application |
| DeliveryId / AdapterEpoch / InferenceRequestId | H/C-owned identifiers | H/C | Delivery and final inference-boundary correlation | Canonical commit order |

Fields shown are semantic components for agreement, not final serialized schemas. B/H/I must align common typed reference and identity definitions; H alone defines wire encoding.

## 3. Commit and transaction visibility

A canonical transaction validates scope/domain invariants and expected aggregate heads, then commits all canonical writes, new aggregate revisions, aggregate-head updates, LifecycleEvent appends (if any), CanonicalCommit record and outbox intent atomically or through a proven recoverable equivalent. The successful transaction receives one commit sequence in the serialized commit order. Cursor assignment and durable commit are one atomic visibility boundary. Rejected, aborted or rolled-back transactions receive no committed cursor.

A read at cursor N sees all canonical effects of transactions through N and none of later transactions. It never sees only one object from a multi-object transaction. A MemoryVersion has its own per-Memory revision sequence and stores the transaction cursor; an EntityVersion and RelationRevision do likewise.

## 4. Gaps, replay, resume and outbox

The canonical committed sequence is contiguous within its authority. A gap observed by a consumer means it has not accounted for every committed transaction, not that the canonical authority skipped an aborted transaction. Consumers persist the last contiguous applied cursor and resume exclusively after it. Delivery is at-least-once; stable event/operation IDs make replay idempotent. An out-of-order event can be staged, but the contiguous watermark cannot advance over it.

Outbox intent is committed with canonical data. Publication can be delayed, duplicated or retried; publication order is not allowed to redefine canonical order. A consumer's private transport offset is not a CanonicalCommitCursor. If an event is missing, the consumer requests replay/reconciliation; if canonical history retention prevents replay, it loads a consistent snapshot tagged with its base cursor and continues after that cursor. No consumer may silently reset to latest while claiming continuity.

## 5. LifecycleEvent semantics

LifecycleEvent is append-only and authoritative for lifecycle transitions. Its sequence is contiguous per Memory ID, not global. It records its enclosing CanonicalCommitCursor. Multiple lifecycle events for one Memory are ordered by LifecycleEventCursor; events across Memories are ordered by CanonicalCommitCursor. A LifecycleProjection is rebuildable and records the last LifecycleEventCursor folded; that field is not an index watermark.

## 6. IndexWatermark semantics

F owns IndexWatermark. It is scoped to a named index/channel partition and records the highest contiguous CanonicalCommitCursor for which all relevant changes have been accounted for, including explicit no-op/irrelevant coverage. If a relevant commit is delayed, failed or schema-incompatible, the watermark stops before it. Rebuild starts from a consistent snapshot cursor and replays subsequent canonical commits. The index must not emit a candidate from a segment until canonical eligibility and current ForgetFence are rechecked.

A watermark is a freshness/completeness signal only. It is not a proof that a target is absent, that a cache was cleared, that Context was reconciled, or that physical erasure occurred.

## 7. ForgetFence semantics

ForgetFenceCursor is a monotonic generation scoped to a ForgetOperation and its target-set digest. It is checked at admission and immediately before canonical visibility or downstream exposure. It is not derived from CanonicalCommitCursor, although fence installation itself has a commit cursor for audit/replay. A fence generation cannot be used as a LifecycleEvent sequence, aggregate revision or IndexWatermark.

## 8. Contract owner matrix

| Concern | D | E | F | G | H | I |
|---|---|---|---|---|---|---|
| CanonicalCommitCursor | Authority | Consumes D result | Consumes | Consumes | Transports opaque ref | Policy may audit |
| AggregateRevision | Authority | References | Reads exact revisions | Pins exact MemoryVersion | Transports opaque ref | Policy may audit |
| LifecycleEventCursor | Authority | Consumes signal | Consumes freshness/invalidation | Consumes reconciliation trigger | Transports opaque ref | Governance may audit |
| IndexWatermark | No ownership | Supplies source/outbox progress separately | Authority | Consumes | No ownership | No ownership |
| ForgetFenceCursor | Canonical authority | Enforces producer gates | Enforces retrieval/index/cache gates | Enforces Context/delivery gates | Enforces Adapter reconnect gates | Sets global policy/permission epochs separately |
| ContextVersion | No ownership | No ownership | No ownership | Authority | Transports | No ownership |

## 9. Failure and acceptance tests

- Atomic multi-aggregate commit is visible wholly or not at all.
- CAS/validation failure consumes neither commit cursor nor aggregate revision.
- Per-Memory LifecycleEventCursor is contiguous and replays deterministically.
- A consumer gap blocks watermark advancement; duplicate replay is idempotent.
- Snapshot bootstrap + exclusive replay reproduces the same canonical state.
- Two aggregates in one transaction share commit cursor but have independent revisions.
- IndexWatermark is partition-scoped and cannot be passed as ForgetFenceCursor.
- Fence installation has a commit cursor for audit, but its generation is not computed from that cursor.

**Acceptance status:** domain semantics decided; storage/recovery implementation and E/F/G cursor conformance remain OPEN. No SLO or implementation result is asserted.
