# Phase 3.6.8 I — Exact-Blob Re-Review of R1–R4 Revision

- Reviewer role: I — Security & Governance (delegated role simulation)
- Decision date: 2026-11-17
- Reviewed source path: 09-security-governance/phase-3.6.8-i-global-inventory-receipt-restore-currentness-amendment.md
- Exact reviewed source Blob: cf4b76f151204fa47b156b5d807e7378c28fd268
- Prior I decision Blob: 0b9954d137a966c062a32424c69936a78ecc470c
- Companion D exact source Blob: 2d95099a2e19a8cbec325925b70da576f73d9899
- Storage Design v3.1 Blob reviewed for boundary consistency: d5bdc72f193fcdaa654e4f07f865b77c578673ca
- COC Phase 3.6.3 Blob reviewed for boundary consistency: 8ac17816476f280ab6fb3afca0688aa03e37de1d
- Scope: I36.8-R1..R4 only; owner-local architecture semantics, not implementation.

## 1. Decision

**ACCEPT — I36.8-R1..R4 SATISFIED IN THE EXACT REVIEWED BLOB.**

The new I Blob materially closes all four mandatory findings from the prior I decision. No additional I-owner-local semantic amendment is required for these four findings.

This is an I-local exact-version decision only. It does not approve a joint I/D/Storage/COC/H freeze, a cryptographic profile, implementation, deployment or production activation.

## 2. Exact finding verification

| Finding | Exact source evidence | Result |
|---|---|---|
| I36.8-R1 — atomic Gate close | §11.1 requires one serializable PolicyDomain sequencer transaction to append request+digest, set PENDING_COC_CUTOFF, increment IGateGeneration, capture count/digest/high-water/cursor, persist anti-rollback anchor, commit atomically, then acknowledge pending. Receipt issue/consume serialize through the same sequencer. | SATISFIED |
| I36.8-R2 — exact Storage final-gate participant | §11.2 binds StorageFinalGateParticipantRef, owner_boundary, PolicyDomainRef, ISequencerPosition, explicit terminal enum, single-use CommitAuthorizationReceipt, complete PreparedParticipant/GID/DB incarnation/native XID/attempt/ledger/receipt tuple and COC PrepareIntent position/digest. UNKNOWN/IN_DOUBT remain nonterminal. | SATISFIED |
| I36.8-R3 — shared reconciliation attempt | §11.3 defines ReconciliationAttemptRef, AttemptGeneration, schema/version, canonicalization profile/digest, I/D signed subrecord refs/digests, D FenceInstallationCursor and exact COC prefix/batch/manifest refs. It explicitly disclaims a global atomic snapshot and requires append-only restart on evidence change. | SATISFIED |
| I36.8-R4 — crypto separation and fail-closed | §11.4 requires a separately versioned key/crypto lifecycle profile and makes stale key status, missing proof, changed digest, uncertain restore and unknown terminal outcomes blocking. | SATISFIED |

## 3. Cross-owner consistency observations

- I's shared reconciliation envelope now contains the D FenceInstallationCursor required by D.
- I's envelope explicitly binds the same ReconciliationAttemptRef/AttemptGeneration/schema/canonicalization identity and both signed owner subrecords.
- I's Storage final-gate proof is consistent in direction with Storage v3.1 §7.2 and §15.7: the exact participant/authorization tuple is validated and consumed in the authoritative I transaction.
- I's exact COC batch and manifest references remain required; this decision does not resolve the separate COC-vs-Storage record-order conflict.
- The I cryptographic/key lifecycle profile remains a separate freeze dependency, as intended.

## 4. Remaining boundaries

1. The reviewed conformance cases are specified, not executed.
2. No independent cryptographic signature or human Owner approval is represented by this delegated role review.
3. The source header remains a proposal; this decision accepts the I-local semantics only.
4. Joint freeze remains blocked pending Storage/COC ordering reconciliation and C/H schema/provider evidence alignment.

## 5. Final disposition

**I Phase 3.6.8 exact Blob cf4b76f151204fa47b156b5d807e7378c28fd268: ACCEPT for I36.8-R1..R4.**

No further I-local amendment is required for these four findings.