# A Review — Prepared GID, Participant Identity & JF-10 Bridge

- Reviewer role: A — Principal Integration Architect (role-simulated in the coordinating ChatGPT session; not an independently authenticated A-session signature)
- Decision: **ACCEPT WITH ENUMERATED AMENDMENTS**
- Review class: architecture-only; not implementation or production approval
- Target 1: `reviews/storage-consistency/phase-3.6-coc-durable-log-and-recovery-protocol-storage-design-v2.md`
  - Commit: `337fe8bffa178e64ad8e4750f1ede1d561424edc`
  - Blob: `4ed4234ce548a814a9496adf7a14c4459ea9f7ce`
  - Relevant: §§2–8, 10–11, 13.1
- Target 2: `reviews/storage-consistency/phase-3.6.3-coc-durable-log-and-recovery-protocol.md`
  - Commit: `71f0c745961cff7f75ef0ba2ac7bfd6f8aeccb66`
  - Blob: `86ff3b247d7565a0dcd1f2e4ed21b5ba70a6b0d7`
  - Relevant: §14 and §§1, 3.2–3.3, 4, 5, 7–9, 13

## Executive decision

The architecture has the correct identity hierarchy and the correct fail-closed recovery principle:

1. `PreparedParticipantRef` is the stable cross-service identity.
2. `PreparedTransactionGID` is a PostgreSQL-specific, client-chosen prepared-transaction locator.
3. PostgreSQL native numeric XID is engine-assigned evidence only.
4. COC records ordering and observations; I owns authorization terminality; Storage owns exact-XID resolution and visibility; D owns Forget/lineage; C owns provider outcome.
5. An unresolved or contradictory participant remains UNKNOWN/IN_DOUBT and cannot be replaced by a fresh participant/GID.

The v2 design also materially closes the earlier recovery ordering gap by binding the immutable participant manifest to the cutoff batch and requiring a separate committed manifest record before recovery completion. This review does not reopen or re-decide the earlier five-Owner baseline; it evaluates only the two pinned targets above.

## Blocking amendments before joint contract freeze

### A-1 — Bind a governed database-incarnation identity

Target 2 §14.4 and Target 1 §7.5 currently bind CanonicalAuthorityDBRef, cluster system_identifier and target database identity/OID. These are necessary but are not a complete non-reusable incarnation contract across clone, restore, reprovisioning and authority migration.

Normative amendment:
- Add `DatabaseIncarnationRef`, minted and governed by the canonical Storage authority registry, globally unique and never reused.
- Bind it into the pre-PREPARE immutable tuple, COC prepare intent, PreparedParticipantReceipt, I terminal proof, StorageResolutionProof and outcome-ledger key.
- Physical clone, logical restore, cluster replacement or authority migration MUST create or explicitly preserve an incarnation only through a separately authorized migration procedure with old/new incarnation cross-reference and anti-rollback evidence. A copied GID in another incarnation MUST NOT resolve the original participant.
- A lookup MUST require exact `CanonicalAuthorityDBRef + DatabaseIncarnationRef + PreparedTransactionGID + PreparedParticipantRef`; no GID-only or system_identifier-only resolution.

### A-2 — Make prepare attempts immutable and replay-safe

Target 2 §14 does not define attempt identity or the durable participant-ledger version. A stale receipt could otherwise be replayed after an aborted PREPARE attempt or participant recreation.

Normative amendment:
- Add monotonic `PrepareAttemptRef` and `PrepareAttemptGeneration` allocated before PREPARE and bound to the COC prepare-intent record.
- Bind `ParticipantLedgerRef` and `ParticipantLedgerVersion` into the receipt.
- One `PreparedParticipantRef` has exactly one immutable operation tuple. A failed/aborted attempt is represented by an append-only terminal attempt record; a retry is either an exact replay of that attempt or a new explicitly authorized generation that cannot inherit the previous receipt.
- Same identity + same canonical tuple is lookup/replay; same identity + changed tuple/generation is CONFLICT. Never silently overwrite.

### A-3 — Define what PREPARED evidence means

Target 2 §14.4 says “prepared state” but does not specify the authoritative observation point.

Normative amendment:
- Receipt issuance is permitted only after successful PREPARE followed by authoritative readback from the writable primary's `pg_prepared_xacts`, matching exact GID, database and observed native XID.
- A command ACK, client-side success, standby-only observation or COC record is insufficient.
- Bind `PreparedObservedAt` for audit only, observation source/role, database incarnation, native XID and COC prepare-intent position/digest.
- If readback is unavailable or disagrees, no PREPARED receipt is issued; state remains UNKNOWN/IN_DOUBT and locks/private data remain retained.

### A-4 — Separate original prepare coordinates from recovery observations

Target 2 §7.5 correctly says recovery timeline/LSN must not replace original prepare identity, but the exact typed fields are not specified.

Normative amendment:
- Preserve `OriginalPrepareTimeline` and `OriginalPrepareLSN` as immutable receipt fields.
- Add append-only `RecoveryObservation[]` entries, each with recovery epoch, observed cluster/database incarnation, timeline, LSN, source role and authoritative evidence reference.
- A timeline change creates a new recovery observation; it never mutates the original prepare coordinates.

### A-5 — Close exact I terminal-to-Storage participant join

Target 1 §7.2 and §7.4 require I to bind the exact Storage final-gate participant and require same-XID resolution. This is the correct boundary, but joint closure depends on I's normative proof showing atomic single-use receipt consumption and final-gate participant binding in one I-authoritative transaction.

Normative condition:
- I terminal proof MUST bind the exact `CommitAuthorizationReceiptRef + digest`, one-time consumption record, `PreparedParticipantRef`, `PreparedTransactionGID`, `DatabaseIncarnationRef`, participant tuple digest, owner boundary, PolicyDomainRef/PermissionEpoch and I sequencer position.
- If I cannot prove that these fields are consumed/recorded atomically in I's own transaction, Storage MUST NOT commit.
- COC may record the proof but cannot create or repair it.

## Non-blocking clarifications

- State names in COC projections must remain observation labels, not owner decisions. Prefer explicit `I_TERMINAL_DECISION_OBSERVED` and `STORAGE_RESOLUTION_OBSERVED`; never treat COC's copy as authority.
- PostgreSQL GID length/character constraints and uniqueness retention period should be captured in the PostgreSQL adapter profile, not generalized to other engines.
- The existing rule that absence from `pg_prepared_xacts` is not proof of COMMIT/ROLLBACK is correct and must remain.

## Positive integration checks

- No generic `xid` field or coercion between GID and native XID.
- Same-GID/same-tuple retry is lookup/replay; same-GID/different-tuple is immutable conflict.
- COMMITTED requires same participant plus exact VisibilityPointer/PublicationReceipt transaction identity and digest.
- ROLLED_BACK requires authoritative non-publication evidence.
- UNKNOWN retains the same prepared participant and blocks protected reads.
- COC, I, D, Storage and C positions remain separate typed namespaces.
- No Storage receipt implies I authorization, COC commit, D clearance, provider success or G Applied.

## Disposition

**ACCEPT WITH ENUMERATED AMENDMENTS** for the integration architecture shape only. **Not accepted for joint contract freeze** until A-1 through A-5 are incorporated or explicitly dispositioned by the accountable owners, and I/H publish their own normative decisions. No implementation, conformance, deployment or production activation approval is granted.

## Review provenance

This is an A-role technical assessment authored by the coordinating session at the user's direction. It is not evidence that the separate A owner session independently reviewed or signed these targets.
