# Phase 3.6.8 — Storage / COC / I / D / C / H Exact-Version Binding Manifest v2

- Owner: Storage / Consistency
- Status: **PINNED REVIEW BUNDLE — OWNER-LOCAL ACCEPTANCES RECORDED; A FINAL INTEGRATION DECISION REQUIRED**
- Date: 2026-11-17
- Supersedes manifest v1 for subsequent review coordination; v1 remains immutable history.
- This is an exact-version pinning artifact, not a joint freeze.

## 1. Exact pinned bundle

| Owner | Artifact | Exact Blob | Disposition |
|---|---|---|---|
| Storage | Storage Design v3.1 | `d5bdc72f193fcdaa654e4f07f865b77c578673ca` | Normative candidate; exact owner review below |
| Storage | Storage ordering amendment, Phase 3.6.4 | `9704d110a06d0c2ee98be960054e0396d0b68546` | Defines two-phase Batch/Manifest and three digest types |
| Storage | Canonical-version / PreparedParticipant identity correction | `dd1b30eca08cea16f2d3ef1556ffb1a61d0f181f` | Required companion provenance |
| Storage / COC | COC protocol with §15–16 supersession | `a07a8d352f31d5406786e1cd8ecddd4065ec384a` | Revised COC candidate; old §6.2 order superseded |
| Storage | Storage exact-version review decision | `d2e804da153ae30e9c2862bf524bc89c42a5dad3` | ACCEPT: Storage v3.1 and revised COC order aligned |
| I | Phase 3.6.8 revised source | `cf4b76f151204fa47b156b5d807e7378c28fd268` | R1–R4 addressed |
| I | I exact-version re-review decision | `f865ec592491cb251f35c07b562a2ca57db9bad8` | ACCEPT I36.8-R1..R4 |
| D | Phase 3.6.8 revised source | `2d95099a2e19a8cbec325925b70da576f73d9899` | R1–R4 addressed |
| D | D exact-version re-review decision | `5aafe8a977ec0cfa1287e7af8c47c8f67ee3a501` | ACCEPT D36.8-R1..R4 |
| C | Provider Outcome contract | `f538d921d06c92dfaba13fbe326a80d6550fe1b7` | C-owned provider outcome semantics |
| C | Revised-bundle exact-version review | `9b6239b8429bd10bab06af3cb8f32b88bda33207` | ACCEPT WITH C-owned provider-specific exceptions |
| H | Two-phase Batch/Manifest wire-validator addendum | `c216853412f654d92e2890ddcc2dffc12406cbe6` | Current semantic/wire candidate |
| H | Recovery Cutoff schema 1.0.5 | `3d451778b9867c3b54779c5cd478522993719025` | Structural schema candidate |
| H | H exact-version re-review decision | `bf7964267e77ad024009026ee6a332fe2baa48bb` | ACCEPT as semantic/wire candidate with blockers |

## 2. Normative Recovery Cutoff sequence

The pinned Storage, COC and H artifacts agree on the following order:

1. Close affected I/D/C owner gates and freeze owner-local snapshots/high-waters.
2. Establish exact quorum-confirmed prefix P.
3. Enumerate every participant through P; stage immutable manifest content and compute ParticipantManifestContentDigest.
4. Commit RecoveryCutoffBatch binding ManifestId + ParticipantManifestContentDigest + owner snapshots + exact P/count/high-water.
5. Commit the separate Participant Manifest Record after Batch, with exact BatchId/BatchDigest back-reference.
6. Compute/verify ParticipantManifestRecordDigest.
7. Linearly read back both records and verify all cross-bindings and BatchPosition < ManifestRecordPosition.
8. Only then begin participant reconciliation; provider lookup/retry additionally requires C's own gate and I/D/Storage predicates.
9. Owner-local releases remain exclusively I/D/C-owned; COC completion is an observation only.

Digest dependency:
`ParticipantManifestContentDigest → RecoveryBatchDigest → ParticipantManifestRecordDigest`.

The staged manifest content is prepared before Batch. The quorum-committed Manifest Record is committed after Batch. These are different phases and MUST NOT be conflated.

## 3. Superseded artifacts and exact-version rules

- COC base Blob `8ac17816476f280ab6fb3afca0688aa03e37de1d` is historical only; it is not the current normative COC companion because §6.2 placed Batch before participant enumeration.
- COC current candidate is Blob `a07a8d352f31d5406786e1cd8ecddd4065ec384a`, whose §§15–16 supersede that order and distinguish all three digests.
- Every downstream review must pin exact Blob SHAs. Branch names and moving paths are not version identities.
- Any subsequent change creates a new Blob and requires a new manifest revision; no pin may float to "latest".
- I/D acceptances apply only to their exact source Blobs and owner-local R1–R4 findings.

## 4. Remaining blockers before joint freeze

1. **A final integration ruling:** A must review the exact bundle above and explicitly accept/reject joint semantic integration.
2. **I cryptographic profile:** separate versioned issuer/subject/audience/purpose, canonical signed bytes, algorithms, key custody, rotation/revocation/compromise, historical verification and anti-rollback approval remains open.
3. **H executable validation/interoperability:** schema and semantic validator vectors are specified, not demonstrated as passing; canonical-byte fixtures across independent implementations remain required.
4. **C provider-specific behavior:** same-key lookup/idempotency, durable outcome persistence, crash/failover recovery and definitive no-handoff evidence must be proven per production provider.
5. **Conformance and runtime:** Batch/Manifest crash/retry, owner snapshot completeness, I/D/Storage JF-10 joins and provider-side-effect vectors remain specified/not executed unless separate evidence is attached.

## 5. Non-claims

This manifest does not claim joint protocol freeze, implementation/conformance PASS, production deployment or activation, JF-10 runtime P0 closure, physical erasure, Forget completion, Global Forget Completion or Multi-PolicyDomain atomicity.

## 6. Provenance

Assistant-authored Storage version-binding artifact committed at the user's direction. It is not an independent human Owner signature.