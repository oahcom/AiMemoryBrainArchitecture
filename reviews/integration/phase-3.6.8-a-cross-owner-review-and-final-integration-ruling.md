# Phase 3.6.8 — A Cross-Owner Review & Final Integration Ruling

- Authority represented: A — Principal Integration Architect
- Review date: 2026-11-17
- Decision class: exact-blob cross-owner review and integration disposition
- Overall decision: **NOT ACCEPTED FOR JOINT FREEZE — INTEGRATION AMENDMENTS REQUIRED**
- I source Blob: 929b30ba10ac627927d3959e0777b467846b268d
- D source Blob: 0668667daeb936bf223ab049277ea2a4117c3b09
- I exact-version decision Blob: 0b9954d137a966c062a32424c69936a78ecc470c
- D exact-version decision Blob: 35fa09e9bd5d15e6ad092c0c0ace52ca02a48692
- Storage Design v3.1 Blob: d5bdc72f193fcdaa654e4f07f865b77c578673ca
- COC Phase 3.6.3 protocol Blob: 8ac17816476f280ab6fb3afca0688aa03e37de1d
- Storage canonical-version/participant-identity amendment Blob: dd1b30eca08cea16f2d3ef1556ffb1a61d0f181f
- Scope: integration semantics only. No implementation, deployment, production readiness or production activation approval.

## 1. Executive ruling

A has completed the cross-owner review after the exact-version I and D re-reviews.

The two owner amendments are directionally compatible and materially strengthen the Phase 3.6.7 baseline:
- I correctly owns global inventory membership/currentness, permission/revocation, receipt issue/consume and I Gate release.
- D correctly owns ForgetFence, affected work admission, lineage/barrier membership, terminalization and D outage-Gate release.
- Storage owns prepared participant identity, durability and visibility resolution.
- C owns actual provider/runtime side-effect outcome.
- COC orders and persists evidence but cannot mint any Owner's authority.
- A integrates the contracts but cannot replace an I or D owner proof.

However, the exact bundle is not yet coherent enough to freeze. The I and D decisions themselves accept their owner-local direction with enumerated amendments; they do not constitute unconditional acceptance of the integrated contract.

## 2. Owner decision reconciliation

| Owner | Exact source reviewed | Owner decision | A reconciliation |
|---|---|---|---|
| I | 929b30... | ACCEPT WITH ENUMERATED MANDATORY AMENDMENTS I36.8-R1..R4 | Accepted as owner-local direction; exact I Gate-close and final-gate proof still need explicit restatement |
| D | 066866... | ACCEPT WITH ENUMERATED MANDATORY AMENDMENTS D36.8-R1..R4 | Accepted as owner-local direction; tuple parity, publication ordering and C evidence need completion |

No I/D authority collision remains in the stated ownership model. D consumes I's signed global inventory projection; I consumes D's operation-specific barrier/closure evidence. Neither side may create the other's membership or terminal proof.

## 3. Blocking integration findings

### A36.8-01 — The pinned COC protocol and Storage v3.1 disagree on Recovery Cutoff Batch ordering (BLOCKING)

The exact COC Blob 8ac178 §6.2 specifies:
1. append RECOVERY_CUTOFF_BATCH;
2. then enumerate every affected pre-batch ParticipantIntentRef and bind the participant-set digest.

The exact Storage Design v3.1 Blob d5bdc72 §5.3–5.4 specifies the opposite safe construction:
1. freeze P and owner high-water attestations;
2. enumerate and compute the complete immutable participant manifest before batch commit;
3. commit the batch binding manifest_id/digest/count/high-water;
4. commit a separate immutable PARTICIPANT_SET_RECONCILIATION record bound to the batch;
5. read back both before leaving the fenced state.

These are not equivalent wordings. The exact normative companion pair currently cited by I/D has a direct sequence conflict. A requires a new COC protocol revision or an explicit versioned supersession addendum that makes the two-record manifest-first sequence normative. Until the exact COC source is corrected and pinned, Recovery Cutoff Batch is not accepted for joint freeze.

### A36.8-02 — I Gate close transaction is not restated in the Phase 3.6.8 I Blob (BLOCKING)

I's Phase 3.6.8 amendment covers currentness, issue/consume generation fencing and release, but does not explicitly restate the one-transaction close rule carried by the accepted Phase 3.6.7 decision and Storage v3.1 §5.2.

I36.8-R1 is mandatory: the I sequencer transaction must atomically append the request, close the affected gate, increment IGateGeneration, capture request-set count/digest/high-water and anti-rollback anchor, then acknowledge pending. Receipt issue/consume must serialize through the same sequencer.

### A36.8-03 — I terminal proof does not explicitly bind the exact Storage final-gate participant in its Phase 3.6.8 field list (BLOCKING)

Storage v3.1 §§7.2 and 15.7 require I's sequenced operation to be the exact Storage owner-final visibility-gate participant, bound to the exact owner boundary, participant, XID/DB incarnation, operation tuple, one-time receipt consumption and I sequence.

I36.8-R2 must explicitly add StorageFinalGateParticipantRef, ISequencerPosition and the accepted terminal vocabulary to the I proof tuple. A generic COMMIT_WON token followed by a detached Storage commit is prohibited.

### A36.8-04 — I/D reconciliation tuples are semantically similar but not yet the same interoperable attempt (BLOCKING)

IReconciliationTuple includes I global inventory state, D barrier state, COC batch/manifest and Storage participant joins. DReconciliationTuple includes D work/barrier state and I inventory/request state. But the two definitions do not share one stable ReconciliationAttemptRef, tuple schema/version, canonical digest and owner-signed subrecord references.

The cross-field mismatch is material:
- I's D subrecord does not bind D FenceInstallationCursor.
- D's I subrecord does not bind PermissionEpoch, TargetInventorySealRef/digest, GlobalInventoryCompletenessProof generation/status and signer/key-status generation.
- Neither exact Phase 3.6.8 source defines the same stable reconciliation attempt identity and digest contract.

I36.8-R3 and D36.8-R1 must be resolved as one common, versioned join envelope. The envelope is not a globally atomic snapshot: each owner signs only its own subrecord, and every owner validates the other owner's authoritative reference.

### A36.8-05 — D publication terminalization needs an exact linearization witness (BLOCKING)

D-M4 requires PUBLISHED_BEFORE_FENCE evidence ordered before D's fence linearization, but the exact proof fields do not yet name the generation checked by the final publication transaction and the publication transaction's atomic compare-and-publish reference.

D36.8-R2 is mandatory. If the publication system cannot prove that the exact current D FenceGeneration was checked atomically with the visibility mutation, the member is UNKNOWN and remains private/quarantined. Wall-clock time and an earlier worker read are not ordering proof.

### A36.8-06 — D barrier members that crossed C's provider boundary need C-owned outcome evidence (BLOCKING)

The D Phase 3.6.8 terminalization contract includes COC and Storage references, but does not explicitly require CSubmitOutcomeRef/provider idempotency evidence for provider-bound work. A Storage XID resolution or COC state cannot prove provider handoff.

D36.8-R3 is mandatory. C remains the sole authority for actual provider outcome. Unknown provider outcome keeps the affected D barrier member unresolved.

### A36.8-07 — Exact bundle manifest must include the version-binding correction (BLOCKING FOR TRACEABILITY)

Storage v3.1's header still carries an older companion-clarification provenance reference, while the Phase 3.6.7 Storage canonical-version amendment dd1b30... explicitly binds the current pair as Storage v3.1 d5bdc72... + COC 8ac178.... The I/D Phase 3.6.8 amendments cite that pair but do not include the version-binding amendment in their explicit source lineage.

A requires the next bundle manifest to pin all three immutable artifacts: Storage v3.1, the exact COC protocol revision that is actually normative, and the canonical-version correction that establishes their relationship. No floating "current/latest companion" references.

## 4. Accepted cross-owner invariants

A accepts these invariants as consistent and mandatory:
1. I, D, C, Storage and COC positions/counters are typed and incomparable; no timestamp or cross-owner high-water ordering.
2. COC RecoveryEpoch completion, I outage-Gate release, D outage-Gate release, D Forget effectiveness/completion, Storage visibility and C provider outcome are separate events.
3. I and D outage gates close before acknowledging pending and reopen only through their own signed, monotonic, batch/manifest-bound release.
4. Recovery Cutoff Batch membership is not an I authorization, D clearance, Storage commit or provider outcome.
5. Every pre-P participant is accounted for, including lost ACK, pre-COC registration work, in-flight provider invocation, prepared XID, late discovery and restore replay.
6. UNKNOWN/IN_DOUBT is durable and blocking. No timeout, lease expiry, absent worker, missing queue row, missing COC projection or operator override may synthesize terminality.
7. JF-10 uses the same immutable PreparedParticipant/GID/DB incarnation/native XID/attempt/ledger tuple from intent through PREPARE, I terminal decision and Storage same-XID resolution.
8. COMMITTED requires Storage PublicationReceipt + VisibilityPointer from the same atomic publication transaction; ROLLED_BACK requires authoritative non-publication proof.
9. C provider outcome is separate from Storage visibility; D barrier completion is separate from both.
10. No Multi-PolicyDomain atomicity is implied or approved.

## 5. Required revision and re-review sequence

1. **I** publishes a new append-only Phase 3.6.8 revision addressing I36.8-R1..R4, then exact-blob I re-review.
2. **D** publishes a new append-only Phase 3.6.8 revision addressing D36.8-R1..R4, then exact-blob D re-review.
3. **Storage** aligns the exact COC source with the Storage v3.1 manifest-first/two-record protocol and publishes a versioned bundle manifest pinning the canonical pair.
4. **C** confirms the provider-outcome evidence required by D barrier members and the shared participant reconciliation envelope.
5. **H** publishes the exact wire/schema representation for the shared reconciliation envelope, batch/manifest records, owner pending/release attestations and the exact I/Storage final-gate proof fields.
6. **A** re-runs cross-owner review against the new exact I, D, Storage, COC and H blobs. Only then can joint freeze be reconsidered.

## 6. Final A integration decision

**NOT ACCEPTED FOR JOINT FREEZE — INTEGRATION AMENDMENTS REQUIRED.**

The Phase 3.6.8 I and D owner-local designs are accepted as sound directions with mandatory amendments. Their current exact blobs are not jointly accepted as a complete cross-owner contract because A36.8-01..07 remain open.

This ruling does not close Gate A, authorize Gate B/C, approve implementation or conformance, establish production readiness, authorize production activation, prove physical erasure or close JF-10 P0. Multi-PolicyDomain remains BLOCKED.

## 7. Provenance

This is a delegated role-based A integration review prepared in this ChatGPT session at the user's direction. It is not a cryptographic signature or proof of independent human A Owner authorship or approval.
