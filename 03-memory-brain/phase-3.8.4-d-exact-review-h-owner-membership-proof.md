# Phase 3.8.4 — D Exact Review: H Owner Snapshot Membership Proof Contract
# Phase 3.8.4 — D 精确审查：H Owner Snapshot Membership Proof 合同

- Owner perspective: D — Memory Brain / ForgetFence Authority
- Review mode: delegated D-role review in the coordinating session; not an independent human Owner signature
- Decision: **ACCEPT WITH CONDITIONS**
- Exact H Unified Schema: 1.2.11 / wire 1.3.0, Blob `4f1e103ab4b2ac961d77179dba0b65093532ea40`
- Exact H RecoveryJoin: 1.0.2, Blob `4b664e3bce465499bcdfd93796349a4ba7074002`
- D proof contract candidate: Blob `d80dabe7210e681bc4e2290355a38f8b67be9ddd`
- H semantic module candidate: Blob `6710bd7876be5f2c60640f21090729b8859a7a3e`

## 1. Accepted semantics

D accepts the H wire requirement that every D owner-admission row carry an immutable proof ref/digest, and accepts the RecoveryJoin 1.0.2 proof payload as a suitable structural envelope for D-owned membership evidence.

The D proof must bind:
- D BrainAuthorityRef and D owner kind;
- exact producer/work ledger ref/version, row/entry ref and digest;
- ProducerRegistrationRef / WorkItemRef / AttemptRef / DerivativeRef as applicable;
- D-local sequence namespace/value and captured producer-registration/WorkItem/Attempt high-waters;
- immutable D snapshot ref/digest and owner-signed snapshot-attestation ref/digest;
- D ledger root, ForgetOperationRef, target/source/ancestor scope digest;
- D Gate ref/generation, ForgetFenceGeneration, barrier generation/root/member;
- operation/request identity and digest;
- D anti-rollback anchor, key-status generation and D-owned signature profile/key/version.

## 2. D authority and no cross-owner counter comparison

D alone verifies D proofs and D snapshot completeness. I PermissionEpoch/InventoryEpoch, C request/provider counters and COC epoch/index are opaque foreign positions. They may be bound by exact typed references and digests but are never numerically compared or ordered with D counters.

The H membership proof does not replace D's CanonicalProducerAdmissionProof, DGateReleaseReceipt, terminal disposition evidence or D lineage barrier. It proves only exact row membership in a frozen D snapshot.

## 3. Conditions

1. D must implement a signed, immutable snapshot membership proof from its actual authoritative ledger, not a caller-asserted `valid=true`.
2. D completeness requires full query identity, pagination completion, count, ordered set root, producer registry/dependency inventory revision, owner-specific high-waters and anti-rollback checkpoint.
3. Late-discovered pre-fence work invalidates the snapshot and reopens the affected barrier.
4. UNKNOWN/IN_DOUBT, incomplete dependency closure, changed root, stale FenceGeneration or missing proof blocks D release.
5. H semantic validator's verifier callback is only a test seam until wired to the D proof authority and key registry.
6. Storage must prove the real D admission/fence/visibility serialization domain, crash recovery, failover and restore; this schema does not prove it.

## 4. D disposition

**ACCEPT WITH CONDITIONS** for the exact candidate wire contract. The D proof contract is not production-approved, no D signer or ledger adapter is deployed, and no D race/fault conformance PASS is claimed. Forget completion and production activation remain unauthorized.


## 5. H semantic payload validator follow-up

H now has an exact-payload validator that binds the proof to the D owner row and snapshot and requires the D-authoritative signature verifier callback. Exact module Blob: `e26379d38825ee13d15f652d3bd019c4091da37d`; RecoveryJoin tests Blob: `3c61cc8c9d973a27f890e1452305e3fb0ad09f1a`. H CI Run `44051676055` passed 288 tests (266 passed, 22 skipped, 0 failed). The callback remains TEST-ONLY; D's real signer, ledger query and anti-rollback remain unimplemented. D's prior ACCEPT WITH CONDITIONS is unchanged.
