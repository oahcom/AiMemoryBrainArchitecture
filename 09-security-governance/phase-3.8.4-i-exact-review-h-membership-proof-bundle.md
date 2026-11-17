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
| H I crypto wire mapping 3.8.4 | `a692a790a4c7abef94dba6da9c22b5e06417879a` |
| H unified Manifest contract 3.8.4 | `e0f561df814c1539ee3b1e72ce7cfc2fd15dd175` |
| H semantic reference validator | `e26379d38825ee13d15f652d3bd019c4091da37d` |
| H Unified Schema 1.2.11 tests | `3e993400cba7a0e744e865434fb1bb90c48fd525` |
| H RecoveryJoin 1.0.2 schema tests | `3c61cc8c9d973a27f890e1452305e3fb0ad09f1a` |
| I Python/Node P0 vectors | `9210219a85afe1f48da0ea253a073aba8b2e138c` |
| I Python/Node crypto tests | `01239e06e8f4464f49acd34241dc00899befe424` |
| D owner proof contract candidate | `d80dabe7210e681bc4e2290355a38f8b67be9ddd` |
| C owner proof contract candidate | `5e37185610869951c3b392c9ad143a72b4c702ac` |
| H CI candidate run | `44051676055` (H test commit `16c0e63458a3e3773cd38ef86bfb4f7fe44dd0b4`; 288 tests total, 266 passed, 22 skipped, 0 failed) |

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


## 5. Exact H bundle refresh

The exact H review and wire mapping were refreshed after adding RecoveryJoin 1.0.2 and the owner-verifier callback:
- H exact review Blob: `b91c645d54ddbcc16aba84fbd83436bcb106bd98`.
- H wire mapping Blob: `a692a790a4c7abef94dba6da9c22b5e06417879a`.
- H union contract Blob: `e0f561df814c1539ee3b1e72ce7cfc2fd15dd175`.
- RecoveryJoin 1.0.2 test Blob: `3c61cc8c9d973a27f890e1452305e3fb0ad09f1a`.
- Unified 1.2.11 test Blob: `3e993400cba7a0e744e865434fb1bb90c48fd525`.
- Unified 1.2.12 test Blob: `91f7cc668d55ce3cfa4d4b9af079dfb118c320d7`.
- H semantic reference module Blob: `e26379d38825ee13d15f652d3bd019c4091da37d`.

The reference validator now requires an explicit owner-proof verifier callback for any non-empty admission set. The test adapter is marked TEST-ONLY. It is not a production I/D/C signature verification implementation.


## 6. Final exact CI result

H candidate CI run `44050250038` completed successfully against commit `34fb4ccf8b1580321d38eda1340cf53f73b83f24`: 281 tests total, 259 passed, 22 skipped, 0 failed. The 22 skipped tests are the superseded historical Unified Schema 1.2.10 semantic fixture class. Current 1.2.11, 1.2.12 and RecoveryJoin 1.0.2 suites ran.

This result supports candidate schema/reference-validator behavior only. The proof verifier used by tests is TEST-ONLY; no production I/D/C signer, key registry or ledger adapter is connected.


## 7. Sixth I P0 vector — membership proof

The exact I membership-proof P0 projection is now represented as the sixth cross-language vector family. It binds the exact owner ledger/version/entry/admission, owner-local namespace/sequence/high-water, ledger root, immutable snapshot/attestation, gate/scope, operation/request, anti-rollback and key-status fields. `proof_digest` is derived; `signature_ref` is external to P0.

- I proof contract exact blob: `88209bbea0ab600880c5c630cfe83af31ee16dd7`.
- H vector exact blob: `9210219a85afe1f48da0ea253a073aba8b2e138c`.
- Python/Node test exact blob: `01239e06e8f4464f49acd34241dc00899befe424`.
- H CI run `44051045877`: 282 tests total, 260 passed, 22 skipped, 0 failed.

The vector is TEST-ONLY and does not approve production I signing, key trust, ledger completeness or anti-rollback. D/C continue to own their own proof profiles and signatures.


## 9. Exact proof payload validation

H's RecoveryJoin proof validator now validates actual proof payload fields against the exact owner row and frozen snapshot and requires the owner-authoritative verifier callback. The exact H semantic module is `e26379d38825ee13d15f652d3bd019c4091da37d`; RecoveryJoin tests are `3c61cc8c9d973a27f890e1452305e3fb0ad09f1a`. CI Run `44051676055` passed 288 tests (266 passed, 22 skipped, 0 failed). This is a reference/test seam only; production I trust/key/ledger verification remains open.
