# Phase 3.6.8 — I Exact-Blob Owner Re-Review Decision

- Decision authority represented: I — Security & Governance
- Review date: 2026-11-17
- Decision: **ACCEPT WITH ENUMERATED MANDATORY AMENDMENTS**
- Reviewed I source path: 09-security-governance/phase-3.6.8-i-global-inventory-receipt-restore-currentness-amendment.md
- Exact reviewed I Blob: 929b30ba10ac627927d3959e0777b467846b268d
- Companion D source path: 03-memory-brain/phase-3.6.8-d-cross-boundary-fencing-terminalization-amendment.md
- Exact companion D Blob: 0668667daeb936bf223ab049277ea2a4117c3b09
- Normative Storage companion: Storage Design v3.1 Blob d5bdc72f193fcdaa654e4f07f865b77c578673ca
- Normative COC companion: Phase 3.6.3 COC protocol Blob 8ac17816476f280ab6fb3afca0688aa03e37de1d
- Prior I Phase 3.6.7 decision Blob: 325cd63164c217f8712964da58509f867d105740
- Scope: I authority, inventory currentness, receipt issue/consume, I Gate and restore release. Architecture semantics only.

## 1. Decision summary

I accepts the Phase 3.6.8 amendment as a substantial and materially correct response to the Phase 3.6.7 I-M1..I-M5 findings. It correctly separates:
- I request Gate generation/high-water from ProducerDomainInventoryEpoch and global registry state;
- I policy/revocation authority from D ForgetFence authority;
- owner-local signed evidence from COC ordering and observation;
- Storage participant identity/attempt/ledger/DB identity from I receipt identity;
- I outage-Gate release from authorization, PermissionEpoch advancement, D Fence clearance, Storage visibility and Global Forget Completion.

The amendment's strongest improvement is I-M2: proof currentness is validated at the final I sequencer/CAS transaction, not by a stale read-then-sign workflow. I-M3 correctly makes receipt consumption single-use and atomic with the I terminal decision, and supports append-only late discovery of PostgreSQLNativeXID without replacing participant identity. I-M4 and I-M5 establish generation fencing and a two-owner restore currentness handshake.

## 2. Mandatory amendments before I semantic freeze

### I36.8-R1 — Restate the I Gate-close linearization transaction (BLOCKING)

The 3.6.8 amendment defines the reconciliation tuple, currentness, issue/consume fencing and release, but it does not restate the exact atomic close operation required by the accepted 3.6.7 decision and Storage v3.1 §5.2.

It MUST explicitly require one serializable I PolicyDomain sequencer transaction to:
1. append the stable IRevocationRequestRef/RequestDigest;
2. set the affected I Gate to PENDING_COC_CUTOFF;
3. increment IGateGeneration;
4. capture the exact request-set count/digest/high-water and owner cursor;
5. persist the anti-rollback anchor;
6. only then acknowledge the request as pending.

Every affected receipt issue/consume transaction MUST serialize through this same sequencer and compare the current Gate state/generation in-transaction. No admitted operation may exist outside the I request ledger and the COC/recovery inventory accounting.

### I36.8-R2 — Complete the exact Storage owner-final-gate participant proof (BLOCKING)

I-M3 lists the Storage tuple, but the exact proof contract must explicitly repeat:
- stable StorageFinalGateParticipantRef / exact owner-final visibility-gate participant identity;
- owner_boundary;
- ISequencerPosition and terminal decision enum (COMMIT_WON, REVOCATION_WON, INDETERMINATE_ABORTED; UNKNOWN/IN_DOUBT remains nonterminal);
- exact CommitAuthorizationReceiptRef/digest and single-use consumption identity;
- PreparedParticipantRef, GID, DatabaseIncarnationRef, native XID when known, PrepareAttemptRef/Generation, ParticipantLedgerRef/Version, PreparedParticipantReceiptRef/digest and complete ParticipantTupleDigest;
- PolicyDomainRef, PermissionEpoch, COC PrepareIntentRef/typed position/digest.

The final I coordinator transaction MUST atomically validate/consume this exact tuple and issue the terminal proof. A detached I terminal token cannot authorize a later unrelated Storage commit. This is required by Storage v3.1 §§7.2 and 15.7; I must explicitly accept the same boundary.

### I36.8-R3 — Make the cross-owner reconciliation attempt identity interoperable (BLOCKING FOR JOINT FREEZE)

IReconciliationTuple currently has rich fields but does not define a stable shared ReconciliationAttemptRef, tuple schema/version, canonical digest and owner-subrecord references that D can bind byte-for-byte by reference. It also omits D's exact fence-installation cursor from its D subrecord.

Add:
- ReconciliationAttemptRef and monotonically increasing attempt generation;
- tuple schema/version and canonicalization profile reference;
- I-signed subrecord digest and D-signed subrecord digest;
- D FenceInstallationCursor in addition to FenceGeneration and D work/barrier high-waters;
- exact COC RecoveryEpoch/prefix/batch/manifest references;
- explicit invalidation/restart rule if any owner subrecord advances.

This is a reconciliation envelope, not a global atomic snapshot. No owner may sign another owner's fields.

### I36.8-R4 — Preserve cryptographic-policy separation and explicit non-terminal behavior

The amendment correctly binds signer/key-status generation, but does not itself select a complete I cryptographic/key lifecycle profile. I does not approve a cryptographic freeze through this decision. The exact issuer/subject/audience/purpose, key custody/rotation/revocation/compromise, historical verification, algorithm agility and anti-rollback policy must be separately versioned and jointly mapped by H.

For any stale key status, unavailable registry/sequencer, unknown terminal outcome, missing owner proof, changed digest or uncertain restore, result is UNKNOWN/CONFLICT and I Gate remains closed. Timeout, missing COC row, expired lease or lost ACK is never terminal evidence.

## 3. Clause-by-clause disposition

| Clause | I disposition |
|---|---|
| §1 authority and typed vocabulary | ACCEPT |
| §2 IReconciliationTuple | ACCEPT WITH R3 |
| §3 I-M2 currentness/CAS | ACCEPT |
| §4 I-M3 participant receipt consumption | ACCEPT WITH R2 |
| §5 I-M4 generation fencing | ACCEPT |
| §6 I-M5 restore handshake | ACCEPT |
| §7 release algorithm | ACCEPT WITH R1/R3 |
| §8 in-flight classes | ACCEPT |
| §9 conformance cases | ACCEPT AS SPECIFIED; NOT EXECUTED |

## 4. I invariants reaffirmed

1. Only I changes PermissionEpoch, decides revocation victory, issues/consumes I receipts and closes/releases I Gate.
2. IRequestHighWater is not ProducerDomainInventoryEpoch.
3. Inventory completeness and TargetInventorySeal are stale after any relevant registry/entry/scope/key generation change until revalidated.
4. A proof is issued only by a currentness-checked authoritative I transaction.
5. Receipt issue/consume races serialize with Gate close through the I sequencer.
6. I terminality is not Storage visibility; Storage resolves the same participant/XID and supplies PublicationReceipt/VisibilityPointer or non-publication proof.
7. COC batch membership is not I authorization or I Gate release.
8. I release never clears D Fence, D barrier, Storage visibility gate or global Forget obligations.
9. No UNKNOWN/IN_DOUBT, lost ACK, stale restore or missing evidence is terminal.

## 5. Final I decision

**ACCEPT WITH ENUMERATED MANDATORY AMENDMENTS I36.8-R1..R4.**

The exact I Phase 3.6.8 Blob is accepted as the correct owner-local semantic direction, but is **not semantically frozen** until a new immutable I amendment addresses R1–R4 and is re-reviewed by exact Blob. This decision does not approve Storage v3.1/COC 8ac178 as a jointly frozen bundle, does not approve H wire/crypto profiles, and does not claim implementation, conformance, deployment or production readiness.

## 6. Provenance

This is a delegated role-based architectural review and decision record prepared in this ChatGPT session at the user's direction. It is not a cryptographic signature and does not prove independent human I Owner authorship or approval.
