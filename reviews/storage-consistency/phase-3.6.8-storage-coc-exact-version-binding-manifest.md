# Phase 3.6.8 — Storage / COC Exact-Version Binding Manifest

- Owner: Storage — consistency and Forget atomicity
- Status: **PROPOSED PINNED CROSS-OWNER REVIEW BUNDLE — NOT JOINTLY FROZEN**
- Date: 2026-11-17
- Purpose: pin the exact Storage, COC, I and D artifacts used for the next cross-owner integration review; eliminate floating "current/latest" companion references.

## 1. Normative candidate bundle

| Role | Artifact | Exact Blob | Status / authority |
|---|---|---|---|
| Storage | `reviews/storage-consistency/phase-3.6-coc-durable-log-and-recovery-protocol-storage-design-v3.md` — Storage Design v3.1 | `d5bdc72f193fcdaa654e4f07f865b77c578673ca` | Storage owner candidate; §5.2–5.6 defines manifest-first/two-record sequence |
| COC | `reviews/storage-consistency/phase-3.6.3-coc-durable-log-and-recovery-protocol.md` — Phase 3.6.3 plus §15 ordering supersession | `345cb915dc9d64306c639718af70864a4569203d` | Revised COC candidate; §15 supersedes old §6.2 ordering |
| Storage identity/version correction | `reviews/storage-consistency/phase-3.6.7-storage-canonical-version-and-prepared-participant-identity-amendment.md` | `dd1b30eca08cea16f2d3ef1556ffb1a61d0f181f` | Required companion provenance and exact participant identity correction |
| I | `09-security-governance/phase-3.6.8-i-global-inventory-receipt-restore-currentness-amendment.md` | `cf4b76f151204fa47b156b5d807e7378c28fd268` | I R1–R4 revised source |
| I decision | `09-security-governance/phase-3.6.8-i-exact-version-r1-r4-rereview-decision.md` | `f865ec592491cb251f35c07b562a2ca57db9bad8` | I exact-Blob ACCEPT for I36.8-R1..R4 |
| D | `03-memory-brain/phase-3.6.8-d-cross-boundary-fencing-terminalization-amendment.md` | `2d95099a2e19a8cbec325925b70da576f73d9899` | D R1–R4 revised source |
| D decision | `03-memory-brain/phase-3.6.8-d-exact-version-r1-r4-rereview-decision.md` | `5aafe8a977ec0cfa1287e7af8c47c8f67ee3a501` | D exact-Blob ACCEPT for D36.8-R1..R4 |

## 2. Superseded COC version

The prior COC Blob `8ac17816476f280ab6fb3afca0688aa03e37de1d` is retained as immutable historical evidence only. It MUST NOT be used as the normative COC companion for the bundle above because its §6.2 order was: commit Recovery Cutoff Batch, then enumerate participants.

The revised COC Blob `345cb915dc9d64306c639718af70864a4569203d` adds §15, which normatively requires:
1. close and freeze owner snapshots;
2. establish exact committed prefix P;
3. enumerate and precompute the complete participant manifest;
4. commit the batch binding manifest ID/digest/count/high-water;
5. commit the separate Participant Set Reconciliation manifest record;
6. read back and verify both records before participant reconciliation.

This matches Storage v3.1 §§5.2–5.6. The old §6.2 step order is expressly superseded by COC §15.4.

## 3. Exact-version integrity rules

- Every downstream review MUST cite the exact Blob SHA in this manifest, not a branch name, moving path or "latest" label.
- Any change to a pinned artifact creates a new Blob and requires a new manifest revision; do not silently update a pin.
- I/D decisions apply only to their exact reviewed source Blobs and their stated owner-local findings.
- Storage v3.1 and revised COC §15 remain proposals pending exact cross-owner re-review; this manifest does not itself approve them.
- COC batch membership is not I authorization, D clearance, Storage commit or C Provider Outcome.
- Owner-local counters/positions remain typed and incomparable; no timestamp-derived cross-owner ordering is introduced.

## 4. Outstanding acceptance dependencies

The bundle is not jointly frozen until all applicable items below are completed:

1. **Storage exact-owner re-review:** Storage must confirm the revised COC §15 and the complete pinned bundle, including the v3.1 manifest-first sequence and exact participant identity binding.
2. **C Provider Outcome:** C must publish/confirm the exact C-owned provider outcome contract and evidence references for success, rejection, non-invocation, ambiguous handoff and lookup-unavailable cases. D's requirement to consume CSubmitOutcomeRef is not evidence that C has supplied it.
3. **H wire/schema:** H must pin exact field names, types, requiredness, nullability, canonical serialization, schema evolution and interoperability vectors for the shared reconciliation envelope, batch/manifest records, owner pending/release attestations and I/Storage final-gate proof.
4. **I cryptographic profile:** I must separately version the issuer/subject/audience/purpose, signed canonical bytes, algorithms, key custody/rotation/revocation/compromise, historical verification and anti-rollback profile; H must map the wire schema to that approved profile.
5. **A final integration review:** A must review the exact revised I, D, Storage, COC and H Blobs and issue a new integration ruling after the above owner artifacts exist.

## 5. Non-claims

This manifest is a version-pinning and review-coordination artifact only. It does not claim:
- joint semantic or wire freeze;
- implementation or conformance PASS;
- production deployment or activation;
- completed JF-10 same-XID runtime bridge;
- physical erasure, Forget completion or Global Forget Completion;
- Multi-PolicyDomain atomicity.

The Storage/COC ordering correction is specified in text; its crash/retry conformance obligations remain **specified, not executed**.

## 6. Provenance

Assistant-authored Storage role artifact committed at the user's direction. It is not an independent human Storage Owner signature or approval.
