# Phase 3.8.4 — A Cross-Owner Integration Review: Snapshot Membership Proof × RecoveryJoin 1.0.2
# Phase 3.8.4 — A 跨 Owner 集成审查：Snapshot Membership Proof × RecoveryJoin 1.0.2

- Reviewer perspective: A — Principal Integration Architect
- Review mode: delegated A-role simulation in the coordinating session at the user's direction; **not an independent human A Owner or governance signature**
- Decision: **ACCEPT AS CANDIDATE COMPOSITION WITH BLOCKING CONDITIONS**
- Joint contract freeze: **NOT APPROVED**
- Production activation: **NOT AUTHORIZED**

## 1. Exact reviewed bundle

| Owner | Artifact | Exact Blob / Evidence |
|---|---|---|
| H | Unified Schema 1.2.11 / wire 1.3.0 | `4f1e103ab4b2ac961d77179dba0b65093532ea40` |
| H | RecoveryJoin 1.0.2 | `4b664e3bce465499bcdfd93796349a4ba7074002` |
| H | I crypto wire mapping 3.8.4 | `a692a790a4c7abef94dba6da9c22b5e06417879a` |
| H | Unified Manifest union contract 3.8.4 | `e0f561df814c1539ee3b1e72ce7cfc2fd15dd175` |
| H | H exact review | `f5ab9a9232b04720faf552a70d5d2962343f843f` |
| H | Semantic reference validator | `6710bd7876be5f2c60640f21090729b8859a7a3e` |
| H | RecoveryJoin 1.0.2 tests | `6afa788da2a899f03de8207cb700c40e0533aba1` |
| H | Unified 1.2.11 tests | `7582091c22ad7f75ed51dba7fbbd02d43af06933` |
| H | Unified 1.2.12 tests | `5b444aa11ffb86c145ec745752204e623c1c2b41` |
| H | Candidate CI | Run `44050250038`, commit `34fb4ccf8b1580321d38eda1340cf53f73b83f24`, 281 total / 259 passed / 22 skipped / 0 failed |
| I | Crypto profile proposal | `5eeb011032c53c2f7897d699d6f512b26f07d0a2` |
| I | Artifact revision / manifest digest amendment | `35c47cc56c9d5e7ab72fdddb7ef9032aa3661ff9` |
| I | Owner membership proof contract | `b1e39c92252eadf8ca592f9a8dc6879cf44fd593` |
| I | Exact H membership proof review | `909165ca0866bb231470a6efc51c9e811e578816` |
| D | Owner membership proof contract | `d80dabe7210e681bc4e2290355a38f8b67be9ddd` |
| D | Exact H membership proof review | `fe4ba71dd3a07d0775e17dbb90e8aeccc3bc71c0` |
| D | Gate/currentness/producer contract | `7f2861d9441b9be6c8e69f41fd0276636be483a8` |
| C | Owner membership proof contract | `5e37185610869951c3b392c9ad143a72b4c702ac` |
| C | Exact H membership proof review | `c6b317f5050bca745bb6308ad6f77ba7d8284f77` |
| C | Provider Outcome binding decision | `1353572f7d5655e3007b2fb5b3f10066f483e6bb` |
| C | Provider Egress Gate Adapter | `a8d1cfc4d2171c9b0a0ced10e53fc6b110479aca` |
| Storage | COC protocol v3.2.3 | `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792` |
| Storage | Batch/Manifest order amendment | `1c8c0bc11798293293bcf47fa560f1699a5bcfe0` |
| Storage | Updated exact binding manifest | `e5f283a0aa88f2f78bbdd3ab85fac011178887f5` |

## 2. Integration findings

### A-1 — Authority separation: ACCEPT

I, D and C each author and verify only their own snapshot membership proofs. H owns the wire schema, typed proof payload and reference joins. Storage owns COC durable ordering and quorum evidence. A integrates but does not replace owner authority.

### A-2 — Canonical union: ACCEPT AS CANDIDATE

The Manifest union is the disjoint typed union of:
1. every quorum-committed COC ParticipantIntent at/before frozen prefix P; and
2. every applicable I/D/C owner-local admission at/below that owner's independently frozen admission high-water that is not already joined to a COC participant.

A COC participant may contain zero or more exact owner admission bindings. An unregistered owner-local admission is a separate union member with explicit null ParticipantIntentRef and non-empty absence reason. No fabricated COC identity is permitted. Every owner row and every applicable COC participant must be represented exactly once or have a valid owner-signed scope exclusion proof.

### A-3 — Membership vs completeness: ACCEPT WITH BLOCKING CONDITIONS

RecoveryJoin 1.0.2 provides a typed owner-signed membership proof payload. This addresses row identity/inclusion but does not establish complete enumeration. Each owner must separately prove query identity, pagination completion, count, ordered set root, owner-local high-water vector and anti-rollback state. Empty sets require an owner-signed COMPLETE_EMPTY proof.

The H semantic reference validator now requires an injected owner-proof verifier callback and fails closed when the verifier is missing or rejects. The callback in current CI is TEST-ONLY; actual I/D/C key registries and ledger adapters are not connected.

### A-4 — No cross-owner sequence synthesis: ACCEPT

I PermissionEpoch/InventoryEpoch, D FenceGeneration/producer high-waters, C admission/provider high-waters, Storage XID/commit cursor and COC term/index remain distinct typed namespaces. They are joined by exact references/digests, never numeric comparison or wall-clock ordering.

### A-5 — Provider truth remains C-owned: ACCEPT

Membership proof and COC Batch/Manifest prove admission inventory and ordering, not provider send or result. Only C's immutable CSubmitOutcome derived from actual provider receipt or authoritative same-key lookup can establish provider boundary outcome. UNKNOWN/IN_DOUBT remains blocking. H ACK, I COMMIT_WON, D clearance or Storage receipt cannot synthesize provider truth.

### A-6 — Digest separation and Batch/Manifest order: ACCEPT AS CANDIDATE

The protocol distinguishes:
- `member_set_root`;
- `manifest_content_digest`;
- final `manifest_record_entry_digest`;
- `batch_digest`;
- final `batch_entry_digest`.

RecoveryCutoffBatch is quorum-committed before ParticipantSetReconciliation, which binds the exact Batch record ref/position/entry digest. Crash after Batch but before Manifest leaves the epoch fenced; no empty Manifest or owner release may be synthesized.

### A-7 — CI evidence: LIMITED PASS

Run 44050250038 executed 281 candidate tests: 259 passed, 22 skipped, 0 failed. The 22 skipped tests are the superseded legacy Unified Schema 1.2.10 semantic fixture class. Current 1.2.11, 1.2.12 and RecoveryJoin 1.0.2 suites ran. This is candidate schema/reference-validator evidence only; it is not production owner-signature, COC quorum, database, provider or distributed crash/failover conformance.

## 3. Blocking conditions

1. I/D/C must implement actual immutable snapshot attestations and owner-signed membership proofs from authoritative ledgers.
2. Each owner must demonstrate complete query/pagination/count/root/high-water coverage and independent anti-rollback, including signed COMPLETE_EMPTY semantics.
3. H must connect its verifier callback to owner-specific trust adapters; TEST-ONLY callback is not production verification.
4. Storage must implement and prove real quorum-committed prefix enumeration, Batch-before-Manifest append, linearizable S4 readback and crash/recovery behavior.
5. C must prove final provider send-vs-Gate-close linearization, same-key provider lookup, durable CSubmitOutcome and multi-replica recovery.
6. D/Storage must prove producer admission/Fence and final visibility ordering, late-discovery barrier reopening, crash/failover/restore and read-path invisibility.
7. I must approve production cryptographic suite, key lifecycle, trust-root ceremony, HSM/KMS, revocation, nonce consumption and external anti-rollback.
8. A fresh independent human Owner/governance review is required; coordinator role simulations do not satisfy sign-off.

## 4. Gate disposition

| Gate | Decision |
|---|---|
| H protocol/schema candidate | ACCEPT WITH ENUMERATED AMENDMENTS |
| I/D/C membership-proof wire composition | ACCEPT AS CANDIDATE WITH OWNER CONDITIONS |
| R1 Recovery Cutoff Batch completeness | OPEN — owner ledger completeness/quorum proof not implemented |
| R2 Owner-local Gate linearization | OPEN — real I/D/C CAS and race/fault proof absent |
| Storage Gate A | PARTIAL PASS / OPEN |
| COC persistence Gate B | BLOCKED pending Gate A acceptance and deployment binding |
| Executable end-to-end Gate C | BLOCKED / deferred to engineering phase |
| JF-10 P0 | OPEN |
| Multi-PolicyDomain atomicity | BLOCKED |
| Production activation | NOT AUTHORIZED |

## 5. Final A ruling

**ACCEPT AS CANDIDATE COMPOSITION WITH BLOCKING CONDITIONS.**

The new membership-proof contract closes an important protocol ambiguity: a row locator is no longer mistaken for proof of inclusion in an owner-frozen snapshot. The distinction between row membership and full-set completeness is explicit. Owner authority and C provider truth remain separated.

It does not close R1/R2, Storage Gate A/B/C, JF-10 P0, multi-domain atomicity or production activation. No schema/protocol freeze or production conformance PASS is declared.

**候选组合有条件接受；R1/R2、Storage Gate、JF-10 P0 与生产激活仍保持开放/阻断。**
