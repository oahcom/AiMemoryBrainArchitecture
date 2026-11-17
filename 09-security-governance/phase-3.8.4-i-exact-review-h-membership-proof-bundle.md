# Phase 3.8.4 — I Exact Review: H Unified Manifest 1.2.11 / RecoveryJoin 1.0.2 Membership Proof Bundle
# Phase 3.8.4 — I 精确审查：H Unified Manifest 1.2.11 / RecoveryJoin 1.0.2 Membership Proof 组合

- Owner perspective: I — Security, Identity and Governance
- Review mode: delegated I-role review at the user's direction; **not an independent human Owner or governance signature**
- Decision: **ACCEPT AS CANDIDATE SECURITY/WIRE CONTRACT WITH BLOCKING CONDITIONS**
- Freeze: **NOT APPROVED**
- Production activation: **NOT AUTHORIZED**

## 1. Exact reviewed bundle

| Artifact | Exact Blob / Run |
|---|---|
| I cryptographic profile proposal | `5eeb011032c53c2f7897d699d6f512b26f07d0a2` |
| I signed artifact-revision amendment | `9db3976ed9a891e9395d0e7edf949e75cb4422aa` |
| I owner membership-proof contract | `b1e39c92252eadf8ca592f9a8dc6879cf44fd593` |
| H Unified Schema 1.2.11 / wire 1.3.0 | `4f1e103ab4b2ac961d77179dba0b65093532ea40` |
| H RecoveryJoin Schema 1.0.2 | `4b664e3bce465499bcdfd93796349a4ba7074002` |
| H I crypto wire mapping 3.8.4 | `bf160288d7529b37ad1b56924c1583748922aa25` |
| H unified Manifest contract 3.8.4 | `0b7251d63ba5a585e55e74a10c4c3113d17188bc` |
| H semantic reference validator | `4a7c22ed15dff0a688559f79e4facbffca6527cd` |
| H Unified Schema 1.2.11 tests | `c95bea3d7a7bee5f419bfabe914ea56be79fc8ad` |
| H RecoveryJoin 1.0.2 schema tests | `83435af0f75d9e0bea64e2a331571356c3c1c26b` |
| I Python/Node P0 vectors | `4657f0c81e9c8692d29ac183380f3d7e074a4e4c` |
| I Python/Node crypto tests | `7658edc6f51dac203742ecc1ecf00d41bd676908` |
| D owner proof contract candidate | `d80dabe7210e681bc4e2290355a38f8b67be9ddd` |
| C owner proof contract candidate | `5e37185610869951c3b392c9ad143a72b4c702ac` |
| H CI candidate run | `44048969058` (new RecoveryJoin 1.0.2 tests; final status to be verified before freeze) |

## 2. I findings

### I-1 — Artifact/wire version separation

ACCEPT. Unified Schema requires both `schema_artifact_revision=1.2.11` and `schema_version=1.3.0`; both are in I P0 for Unified Schema messages. The receiver must reject registry/artifact mismatch and downgrade. RecoveryJoin is a separate schema artifact and must be pinned independently; it does not inherit the Unified Schema artifact revision.

### I-2 — Distinct digest semantics

ACCEPT. `manifest_content_digest`, `manifest_record_entry_digest`, `batch_digest` and `batch_entry_digest` are distinct, independently verified values. I Gate Release signs the four exact values under its owner P0. A COC coordinator-added record position or backlink may be excluded from owner P0 only where the exact H mapping explicitly enumerates it.

### I-3 — Membership proof requirement

ACCEPT AS WIRE REQUIREMENT. Each owner-admission binding and unregistered owner-local admission carries an immutable membership proof ref/digest. RecoveryJoin 1.0.2 defines the proof payload and binds the owner admission/entry, ledger/version/root, local sequence/high-water, snapshot/attestation, gate/scope, operation/request, anti-rollback and key-status identity.

The proof is owner-authored. I verifies only I-owned proofs; D and C verify their own. H validates structural shape and exact join references, but does not attest owner ledger completeness or sign owner proofs.

### I-4 — I-owned membership proof semantics

ACCEPT AS I CANDIDATE CONTRACT. The I proof must attest exact inclusion in the signed frozen I snapshot and sequence-at-or-below the I admission high-water. Membership does not itself prove query completeness: complete pagination, query identity, count, canonical root/set digest and independent anti-rollback evidence are also required. Empty sets require the separately signed COMPLETE_EMPTY proof.

### I-5 — Crypto and CI evidence boundary

The Python RFC 8785/Ed25519 and Node JCS/Ed25519 implementations are independent test stacks with TEST-ONLY key material. Candidate CI proves the checked-in fixtures and reference tests only. It does not approve production Ed25519/FIPS suitability, trust-root ceremony, HSM/KMS, key rotation, revocation propagation, durable nonce consumption, or external anti-rollback.

## 3. Blocking conditions

1. D and C must independently review and accept their exact owner membership-proof contracts and bind their actual ledger/snapshot/key authority.
2. H must run RecoveryJoin 1.0.2 structural and semantic negative tests; schema validity alone is insufficient.
3. H's proof resolver must fail UNKNOWN on missing/unavailable proof and INVALID on any owner/entry/root/snapshot/high-water/scope/operation mismatch. It must never trust a caller-supplied `valid=true` without owner-authoritative signature verification.
4. I must define the production I proof P0 and proof digest preimage in the frozen cryptographic profile, including proof-ref namespace and uniqueness.
5. Each Owner must prove its snapshot is complete through the captured owner-local high-water; row membership alone is not completeness.
6. A must re-review the exact I/D/C/H/Storage bundle and all current branch heads before any cross-owner freeze.

## 4. I disposition

**ACCEPT AS CANDIDATE SECURITY/WIRE CONTRACT WITH BLOCKING CONDITIONS.**

I accepts the direction of H Unified Schema 1.2.11 and RecoveryJoin 1.0.2 as the correct typed wire shape for owner-signed snapshot membership. I does not attest D/C membership proof semantics, Storage COC persistence, provider egress, JF-10 physical same-XID behavior or production key operations.

- R1 Recovery Cutoff Batch completeness: OPEN pending real owner query completeness and quorum prefix proof.
- R2 Owner-local Gate: OPEN pending I/D/C durable currentness CAS and in-flight admission proofs.
- JF-10 P0: OPEN.
- Multi-PolicyDomain atomicity: BLOCKED.
- Production cryptographic freeze: NOT APPROVED.
- Runtime conformance/deployment: NOT ESTABLISHED.
- Production activation: NOT AUTHORIZED.

**候选 Security/Wire 合同有条件接受；跨 Owner Freeze 与生产密码学启用仍不批准。**
