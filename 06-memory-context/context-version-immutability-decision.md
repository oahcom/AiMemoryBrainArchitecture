---
document_metadata:
  domain: memory-context
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
        - "Owner-delegated direction decision, 2026-11-26"
        - "Work Item AID-2026-090"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Direction decision recorded; exact-version Owner acceptance and normative approval pending."
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
    canonical_status: Canonical
    canonical_scope: "memory-context decision contract"
    canonical_scope_id: "memory-context/decision-084"
    canonical_scope_keywords:
      - architecture-decision
      - memory-context
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    en: "docs/en/06-memory-context/context-version-immutability-decision.md"
    zh-CN: "docs/zh-CN/06-memory-context/context-version-immutability-decision.md"
---
# ContextVersion Immutability Decision
Decision ID: CV-IMM-01
Authority: user-authorized operator (delegated by account owner)
Date: 2026-11-26
Owner: G; dependent boundaries B, D, I, C/H and Storage/Consistency
Issues: #1144, #1151
Status: Direction decided; exact-version Owner acceptance and normative approval pending.

## Decision and immutable boundary
A committed ContextVersion is an immutable, content-addressed snapshot of one complete desired managed Context state. No field that identifies, describes or changes the meaning of that committed snapshot may be edited in place.

Immutable fields comprise Context ID, Context Session ID, immutable Version ID, monotonically increasing sequence, parent/base Version reference, the complete ordered ContextEntryVersion set, each entry's identity/revision/content digest/qualifiers/state/delivery-relevant metadata, canonical serialization profile/version, snapshot reference and digest, commit identity/time, source revision references and applicable ForgetFence cursor references.

Mutable state must live outside the version object: current-head pointer; delivery attempts, receipts, retries, Applied evidence and operational health; rebuildable indexes, caches and projections. None may rewrite or reinterpret a committed version.

## Legal mutation paths
1. Any content or membership change creates a new ChangeSet and successor ContextVersion.
2. The ChangeSet names the exact expected base. Commit atomically checks that base is still current, persists the new immutable snapshot and advances the head; stale base conflicts.
3. Correction, replacement, removal, policy change or Forget invalidation creates a successor with explicit provenance/reason; it never edits the predecessor.
4. Same idempotency key and same request digest replays the original receipt/version. Same key with different digest conflicts.
5. Delivery, Applied, expiry, rejection, supersession and retry are append-only external evidence records.
6. The trusted commit boundary computes the snapshot digest over exact canonical ordered committed entries. Caller-supplied digest is advisory and must be recomputed/compared. Read/replay verifies that snapshot reference and digest identify the same immutable bytes.

## Violations
In-place change to committed fields/entry order/content/source refs; reuse of Version ID/sequence for different content; head movement without a committed successor and expected-base check; acceptance of a mismatched caller digest; mutation of a Version to record delivery/Applied/Forget status; replay of the same Version identity with different bytes.

## Reviewer PASS/FAIL
- CVI-01 PASS iff committed ContextVersion and its entry snapshot are immutable; else FAIL.
- CVI-02 PASS iff Context/session/version/sequence/parent/ordered entries/delivery-relevant metadata are inside the immutable boundary; else FAIL.
- CVI-03 PASS iff head advances only by append-only successor ChangeSet with exact expected-base/CAS; else FAIL.
- CVI-04 PASS iff corrections/removals/Forget create successors and never edit predecessors; else FAIL.
- CVI-05 PASS iff delivery attempts/receipts/Applied/projections are outside ContextVersion; else FAIL.
- CVI-06 PASS iff digest binds exact ordered entries and is verified on read/replay; else FAIL.
- CVI-07 PASS iff same-key/same-digest retries replay and same-key/different-digest conflicts; else FAIL.
- CVI-08 PASS iff EN and ZH-CN express the same boundary and legal paths; else FAIL.

## Authority boundary
G owns ContextVersion semantics and exact-version acceptance. B owns referenced domain-object identity/revision; D/I own Forget authority/policy; C/H own delivery and inference-boundary evidence; Storage owns physical atomicity/durability/recovery. This decision does not select storage topology, digest algorithm, wire encoding or implementation details beyond these semantic invariants. #1144 and #1151 remain OPEN until their own evidence and Owner acceptance criteria are met. No product/runtime code, tests, schemas, validators, workflows, deployment or production state is changed.
