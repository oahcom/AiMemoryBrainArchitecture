# Phase 3.6.8 D — Exact-Blob Re-Review of R1–R4 Revision

- Reviewer role: D — Memory Brain / Forget Authority (delegated role simulation)
- Decision date: 2026-11-17
- Reviewed source path: 03-memory-brain/phase-3.6.8-d-cross-boundary-fencing-terminalization-amendment.md
- Exact reviewed source Blob: 2d95099a2e19a8cbec325925b70da576f73d9899
- Prior D decision Blob: 35fa09e9bd5d15e6ad092c0c0ace52ca02a48692
- Companion I exact source Blob: cf4b76f151204fa47b156b5d807e7378c28fd268
- Storage Design v3.1 Blob reviewed for boundary consistency: d5bdc72f193fcdaa654e4f07f865b77c578673ca
- COC Phase 3.6.3 Blob reviewed for boundary consistency: 8ac17816476f280ab6fb3afca0688aa03e37de1d
- Scope: D36.8-R1..R4 only; owner-local architecture semantics, not implementation.

## 1. Decision

**ACCEPT — D36.8-R1..R4 SATISFIED IN THE EXACT REVIEWED BLOB.**

The new D Blob materially closes all four mandatory findings from the prior D decision. No additional D-owner-local semantic amendment is required for these four findings.

This is a D-local exact-version decision only. It does not approve a joint I/D/Storage/COC/H freeze, C Provider Outcome implementation, physical erasure, Forget completion or production activation.

## 2. Exact finding verification

| Finding | Exact source evidence | Result |
|---|---|---|
| D36.8-R1 — shared reconciliation tuple | §11.1 binds the common attempt/generation/schema/canonicalization identity, I and D signed subrecord digests, PermissionEpoch, I sequencer position, target seal, completeness proof, signer/key generation, scope mapping, D fence cursor, COC batch/manifest and applicable Storage/Restore refs. | SATISFIED |
| D36.8-R2 — publication-before-fence | §11.2 requires exact FenceGeneration/FenceInstallationCursor, ValidatedFenceGeneration read by the final effect transaction, publication commit and visibility evidence, WorkItem/Attempt/Lease/scope/lineage identity, and proof the check and visibility mutation share one atomic/linearizable boundary. Unknown ordering remains private/quarantined. | SATISFIED |
| D36.8-R3 — C Provider Outcome | §11.3 requires C-owned CSubmitOutcomeRef/digest, provider idempotency namespace, exact request digest and provider receipt/lookup evidence; it rejects Storage, I, COC and transport ACK as substitutes. Unknown provider outcome blocks D terminalization/release/completion. | SATISFIED |
| D36.8-R4 — fresh I currentness | §11.4 requires authoritative I currentness immediately before D outage-Gate release and D Forget terminalization, including inventory epoch, registry, entry generations, target seal, completeness proof, key status and scope mapping. Stale evidence reopens the barrier. | SATISFIED |

## 3. Cross-owner consistency observations

- D's shared tuple is structurally aligned with I Blob cf4b76f151204fa47b156b5d807e7378c28fd268 on attempt identity, schema/version, canonicalization profile and signed subrecords.
- D correctly consumes, but does not mint, I-owned inventory and permission evidence.
- D's publication-before-fence classification now has a mechanically decidable final-effect witness rather than wall-clock ordering.
- D's C provider subrecord remains C-owned. This review confirms the required contract, not that C has supplied or verified actual provider outcome artifacts.
- D's COC batch/manifest references remain exact, but the separate COC-vs-Storage ordering conflict remains unresolved.

## 4. Remaining boundaries

1. The reviewed conformance cases are specified, not executed.
2. Provider outcome evidence must still be supplied/verified by C for applicable barrier members.
3. No independent cryptographic signature or human Owner approval is represented by this delegated role review.
4. Joint freeze remains blocked pending Storage/COC ordering reconciliation and C/H schema/provider evidence alignment.

## 5. Final disposition

**D Phase 3.6.8 exact Blob 2d95099a2e19a8cbec325925b70da576f73d9899: ACCEPT for D36.8-R1..R4.**

No further D-local amendment is required for these four findings.