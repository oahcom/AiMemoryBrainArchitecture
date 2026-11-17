# Phase 3.6.8 — A Revised Cross-Owner Integration Ruling After I/D R1–R4

- Role: A — Principal Integration Architect (delegated role simulation)
- Review date: 2026-11-17
- Decision: **ACCEPT AS INTEGRATED DESIGN CANDIDATE — NOT JOINTLY FROZEN**
- Supersedes the earlier open-finding disposition only for the exact findings and exact artifact versions listed here.
- No implementation, deployment, production readiness or activation approval.

## 1. Exact pinned bundle reviewed

| Owner | Artifact | Exact Blob | Decision / status |
|---|---|---|---|
| Storage | Storage Design v3.1 | `d5bdc72f193fcdaa654e4f07f865b77c578673ca` | Design candidate |
| Storage | Recovery Cutoff Batch / Manifest Ordering Amendment | `9704d110a06d0c2ee98be960054e0396d0b68546` | Normative ordering/digest correction |
| Storage | Canonical-version / PreparedParticipant identity correction | `dd1b30eca08cea16f2d3ef1556ffb1a61d0f181f` | Required provenance |
| Storage / COC | COC protocol with §15–16 supersession | `a07a8d352f31d5406786e1cd8ecddd4065ec384a` | Revised COC candidate |
| Storage | Storage exact-version review decision | `d2e804da153ae30e9c2862bf524bc89c42a5dad3` | ACCEPT ordering alignment |
| Storage | Exact-version binding manifest v2 | `8688a03c69227284cd00b4110d87019cd346bfb2` | Pinned bundle |
| I | Phase 3.6.8 revised source | `cf4b76f151204fa47b156b5d807e7378c28fd268` | R1–R4 amended |
| I | I exact-Blob re-review decision | `f865ec592491cb251f35c07b562a2ca57db9bad8` | ACCEPT I36.8-R1..R4 |
| D | Phase 3.6.8 revised source | `2d95099a2e19a8cbec325925b70da576f73d9899` | R1–R4 amended |
| D | D exact-Blob re-review decision | `5aafe8a977ec0cfa1287e7af8c47c8f67ee3a501` | ACCEPT D36.8-R1..R4 |
| C | Provider Outcome contract | `f538d921d06c92dfaba13fbe326a80d6550fe1b7` | C-owned provider outcome semantics |
| C | Revised-bundle exact-version review | `9b6239b8429bd10bab06af3cb8f32b88bda33207` | ACCEPT WITH C-owned exceptions |
| H | Two-phase Batch/Manifest addendum | `c216853412f654d92e2890ddcc2dffc12406cbe6` | Semantic/wire candidate |
| H | Recovery Cutoff schema 1.0.5 | `3d451778b9867c3b54779c5cd478522993719025` | Structural candidate |
| H | H exact-version re-review decision | `bf7964267e77ad024009026ee6a332fe2baa48bb` | ACCEPT as candidate with freeze blockers |

## 2. Executive ruling

A finds that the previous seven Phase 3.6.8 integration blockers have been addressed at the architecture-specification level by the exact revised artifacts above.

**A accepts this pinned bundle as an integrated design candidate. A does not declare it jointly frozen.**

The Owner authority split remains coherent:
- I owns PermissionEpoch, revocation order, global inventory membership/currentness, I receipt issue/consume and I Gate release.
- D owns ForgetFence, affected work admission, lineage/barrier membership, D terminalization and D outage-Gate release.
- C owns provider admission/egress and actual provider outcome.
- Storage owns prepared participant identity, same-XID durability/resolution and visibility evidence.
- COC persists quorum-ordered records and recovery observations; it does not mint Owner decisions.
- H owns wire/schema/canonicalization representation; it does not mint Owner decisions.
- A integrates exact contracts and records the cross-owner decision; A cannot replace any Owner proof.

## 3. Closure of prior A36.8 findings

| Prior finding | New exact evidence | A disposition |
|---|---|---|
| A36.8-01 — COC/Storage Batch ordering conflict | Storage v3.1 §§5.2–5.6; Storage ordering amendment; COC §§15–16; H addendum/schema 1.0.5 | **CLOSED AT SPECIFICATION LEVEL** |
| A36.8-02 — I Gate-close linearization | I revised §11.1: one serializable sequencer transaction, close-before-ACK, issue/consume serialization | **CLOSED AT SPECIFICATION LEVEL** |
| A36.8-03 — exact I Storage final-gate proof | I revised §11.2: StorageFinalGateParticipantRef, owner boundary, I position, terminal enum and single-use exact participant tuple | **CLOSED AT SPECIFICATION LEVEL** |
| A36.8-04 — I/D shared reconciliation tuple | I §11.3 and D §11.1: same attempt/generation/schema/canonicalization, signed subrecords and D FenceInstallationCursor | **CLOSED AT SPECIFICATION LEVEL** |
| A36.8-05 — publication-before-fence witness | D §11.2: final-transaction ValidatedFenceGeneration and atomic/linearizable compare-and-publish proof | **CLOSED AT SPECIFICATION LEVEL** |
| A36.8-06 — C provider outcome in D barrier | D §11.3 plus C Provider Outcome contract and C exact review | **CLOSED AT SPECIFICATION LEVEL; PROVIDER IMPLEMENTATION OPEN** |
| A36.8-07 — exact companion/version manifest | Storage canonical correction plus manifest v2 pins Storage, COC, I, D, C and H exact Blobs | **CLOSED FOR THIS PINNED BUNDLE** |

### 3.1 Batch / Manifest ordering interpretation

A confirms the only valid interpretation:

1. Owner snapshots/gates freeze and exact prefix P is established.
2. Complete immutable manifest content is enumerated/staged and ParticipantManifestContentDigest is computed.
3. RecoveryCutoffBatch is quorum committed and binds ManifestId + ContentDigest.
4. The separate quorum-committed Participant Manifest Record is committed after Batch and binds BatchId + RecoveryBatchDigest.
5. ParticipantManifestRecordDigest is computed/verified for the final record.
6. Both records are linearly read back and cross-validated before participant reconciliation, owner release or provider-side recovery.

The digest dependency is:
`ParticipantManifestContentDigest → RecoveryBatchDigest → ParticipantManifestRecordDigest`.

"Manifest content before Batch" is required. "Manifest record before Batch" is invalid. This distinction resolves the former ordering ambiguity without circular digest references.

## 4. Remaining blockers before joint freeze

The integrated design candidate is not yet jointly frozen because the following normative/evidence dependencies remain open:

1. **I cryptographic/key lifecycle profile:** issuer, subject, audience, purpose, canonical signed bytes, algorithm suite/agility, key custody, rotation, revocation, compromise response, historical verification and anti-rollback must be separately versioned and approved by I; H must map to it.
2. **H executable semantic validators and canonical-byte interoperability:** H schema 1.0.5 and validator rules are specifications. Executable validators, negative/positive vectors and cross-implementation canonical-byte fixtures have not been demonstrated as passing.
3. **C provider-specific behavior:** each production provider requires documented same-key lookup/idempotency, definitive no-handoff semantics and durable outcome recovery across process death/failover. Generic exactly-once is not assumed.
4. **Owner conformance:** I Gate-close/receipt races, D publication/fence races, C egress/gate races, Storage same-XID and COC crash/retry vectors remain specified/not executed unless separately evidenced.
5. **Independent governance:** the records in this coordinating session are delegated role simulations and repository artifacts, not independent human Owner signatures or approvals. Formal project governance must not represent them as independent approvals.

## 5. Phase and production boundary

- Integrated architecture design candidate: **ACCEPTED**
- Joint semantic/wire/cryptographic freeze: **NOT APPROVED**
- Implementation/conformance: **NOT VERIFIED by this ruling**
- JF-10 runtime P0: **OPEN**
- Multi-PolicyDomain atomicity: **BLOCKED / NOT ACCEPTED**
- Gate A production binding: remains subject to its separate deployment/operator evidence boundary
- Gate B persistent COC: remains blocked pending its own prerequisites
- Gate C end-to-end fault campaign: remains blocked pending Gate B
- Production activation: **NOT AUTHORIZED**
- Physical erasure / Forget completion / Global Forget Completion: **NOT CLAIMED**

## 6. Required next sequence

1. I publishes and obtains governance approval for the separate cryptographic/key lifecycle profile.
2. H implements the semantic validators and canonical-byte fixtures against the pinned schema/profile.
3. C qualifies provider-specific same-key lookup and durable outcome recovery for each intended production provider.
4. Storage/COC/H execute the two-record crash/retry and readback conformance campaign.
5. I/D/C/Storage run owner-local race and fail-closed conformance tests against identified builds.
6. A performs a new exact-version review after all revised artifacts and evidence are pinned. Only then may joint freeze be reconsidered.

## 7. Provenance

Assistant-authored delegated A integration ruling prepared at the user's direction. It is not an independent human A Owner signature, cryptographic signature, implementation proof or production approval.