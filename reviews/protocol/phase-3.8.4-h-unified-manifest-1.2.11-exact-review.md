# Phase 3.8.4 — H Exact-Version Review: Unified Manifest Schema 1.2.11
# Phase 3.8.4 — H 精确版本审查：Unified Manifest Schema 1.2.11

- Reviewer perspective: H — BMCP Protocol Architect
- Decision: **ACCEPT WITH ENUMERATED AMENDMENTS**
- Provenance: delegated H-role simulation in the coordinating session at the user's direction; not an independent human H Owner signature.
- Status: **SCHEMA / PROTOCOL CANDIDATE ONLY — NOT FROZEN / NOT DEPLOYED**
- English and Chinese are normative peers.

## 1. Exact reviewed bundle / 精确审查组合

| Artifact | Exact Blob / Evidence |
|---|---|
| H Unified Schema 1.2.11, wire 1.3.0 | `4f1e103ab4b2ac961d77179dba0b65093532ea40` |
| H Unified Manifest contract 3.8.4 | `0b7251d63ba5a585e55e74a10c4c3113d17188bc` |
| H I crypto wire mapping 3.8.4 | `bf160288d7529b37ad1b56924c1583748922aa25` |
| I crypto profile proposal | `5eeb011032c53c2f7897d699d6f512b26f07d0a2` |
| I crypto artifact-revision amendment | `9db3976ed9a891e9395d0e7edf949e75cb4422aa` |
| H RecoveryJoin schema 1.0.2 | `4b664e3bce465499bcdfd93796349a4ba7074002` |
| H semantic reference module | `6710bd7876be5f2c60640f21090729b8859a7a3e` |
| H Unified Schema 1.2.11 tests | `7582091c22ad7f75ed51dba7fbbd02d43af06933` |
| H Unified Schema 1.2.12 tests | `5b444aa11ffb86c145ec745752204e623c1c2b41` |
| H RecoveryJoin 1.0.2 tests | `6afa788da2a899f03de8207cb700c40e0533aba1` |
| I P0 vector set | `4657f0c81e9c8692d29ac183380f3d7e074a4e4c` |
| I Python/Node crypto test | `7658edc6f51dac203742ecc1ecf00d41bd676908` |
| H CI | Run `44050250038`, commit `34fb4ccf8b1580321d38eda1340cf53f73b83f24`, **281 tests: 259 passed, 22 skipped, 0 failed** |

## 2. H findings / H 审查发现

H accepts the following protocol/schema candidate properties:

1. The Manifest now carries a canonical typed union: COC participants plus applicable unregistered I/D/C owner-local admissions.
2. `COC_PARTICIPANT` carries zero or more exact owner admission bindings; where an applicable frozen owner admission exists, semantic validation requires every such binding exactly once.
3. `OWNER_LOCAL_ADMISSION` requires `coc_participant_intent_ref=null` and a non-empty absence reason; fabricated COC participant identities are rejected.
4. Owner snapshots are keyed by I/D/C and bind snapshot digest, attestation digest, Gate generation, request/admission high-waters, ledger roots, owner-specific high-water digest and anti-rollback anchor.
5. Each owner admission binding carries immutable snapshot membership-proof ref and digest.
6. Counts distinguish COC participant count, unregistered owner-local admission count and total Manifest member count.
7. `member_set_root`, `manifest_content_digest` and final `manifest_record_entry_digest` are distinct.
8. RecoveryCutoffBatch precedes ParticipantSetReconciliation; the latter binds the exact Batch record ref/position/entry digest.
9. Owner release uses the common enum `OUTAGE_ADMISSION_RELEASE_ONLY` and binds both Manifest content and final record-entry digests.
10. Exact artifact revision `1.2.11` and wire version `1.3.0` are separate required common-envelope fields; the I mapping includes both in unified-schema P0.
11. Protected I records require an exact `signature_profile_id` semantically even though the common schema keeps the field structurally optional for non-protected compatibility cases.

## 3. Executable evidence / 可执行证据

The exact CI run passed 209 tests, including:
- RecoveryJoin 1.0.2 owner-signed membership-proof payload schema validation;
- Draft 2020-12 meta-schema validation of the full Unified Schema 1.2.11 document;
- structural validation of COC participant, owner-local admission, owner-admission binding and owner snapshot root fixtures;
- union completeness, duplicate/missing/fabricated member and membership-proof vectors;
- Batch-before-Manifest ordering, exact backlink, owner release currentness and RecoveryEpochCompleted joins;
- protected signature-profile semantics and C Provider Outcome status vectors;
- Python RFC 8785/Ed25519 and Node JCS/Ed25519 cross-language P0 vectors for five I proof/message families.

Earlier failed runs were test-harness defects (fixture setup and non-hex test root values); the corrected exact commit above passed. No protocol failure was hidden or reclassified as a pass.

The semantic digest module uses `BMCP-*-TEST-v1` normalized test digests. The 22 skipped tests are the superseded legacy Unified Schema 1.2.10 semantic fixture class; current 1.2.11 and 1.2.12 suites are active. It is not the production canonical digest profile. The tests do not call real COC quorum, I/D/C ledgers, production signature/key registry, provider APIs or Storage database adapters.

## 4. Enumerated amendments / 保留修订

1. **H/I canonical digest freeze:** define production JCS/canonical-byte projections and digest preimages for union member root, Manifest content, final Manifest record and Batch record. TEST-only digest functions are not normative.
2. **I proof authority:** I must define and approve I owner snapshot membership proof schema, signed projection, digest preimage, key status and anti-rollback verification.
3. **D proof authority:** D must define its own WorkItem/Attempt/Lineage membership proof and exact fence-generation binding.
4. **C proof authority:** C must define reservation/provider-attempt membership proof, stable idempotency identity and provider outcome lookup evidence.
5. **Storage COC authority:** real quorum-committed prefix enumeration, Batch/Manifest append ordering, linearizable readback, recovery-round chain and failure-injection evidence remain unimplemented.
6. **C Egress:** the final provider send-vs-Gate-close linearization and same-key recovery must be proven by a concrete adapter; this schema test does not prove it.
7. **I crypto approval:** I's algorithm/regulatory suitability, trust-root ceremony, HSM/KMS, key lifecycle, historical verification and external anti-rollback remain I/governance decisions.
8. **Independent Owner reviews:** I, D, C and Storage must review the exact 1.2.11 Blob in their own Owner branches. The coordinating-session role simulations do not satisfy independent Owner acceptance.
9. **A integration:** A must pin the exact I/D/C/Storage/H bundle and issue a fresh cross-owner integration decision after those reviews.

## 5. Final H disposition / H 最终决议

**ACCEPT WITH ENUMERATED AMENDMENTS** for the exact candidate bundle in §1.

- R1: substantially specified at protocol/schema level; OPEN pending authoritative membership proofs and real COC completeness.
- R2: substantially specified at message/semantic level; OPEN pending real I/D/C currentness CAS and C egress adapter race proof.
- JF-10 P0: OPEN.
- Multi-PolicyDomain atomicity: BLOCKED.
- Production cryptographic freeze: NOT APPROVED.
- Runtime conformance/deployment: NOT ESTABLISHED.
- Production activation: NOT AUTHORIZED.

**对第 1 节精确候选版本作有条件接受。**

- R1：协议/Schema 层面已实质明确；仍开放，等待权威 Membership Proof 与真实 COC 完整性证明。
- R2：消息/语义层面已实质明确；仍开放，等待真实 I/D/C Currentness CAS 与 C Egress Adapter 竞争条件证明。
- JF-10 P0：OPEN。
- Multi-PolicyDomain Atomicity：BLOCKED。
- Production Cryptographic Freeze：NOT APPROVED。
- Runtime Conformance/Deployment：NOT ESTABLISHED。
- Production Activation：NOT AUTHORIZED。


## 6. RecoveryJoin 1.0.2 and owner-verifier seam

H now provides RecoveryJoin 1.0.2 structural proof payloads and requires each join edge to carry exact membership-proof ref/digest. The reference union validator no longer treats a caller-supplied `valid=true` as sufficient: it requires an injected owner-authoritative proof-verifier callback. Missing verifier result returns UNKNOWN; a rejecting verifier returns INVALID. Current unit fixtures use an explicitly TEST-ONLY verifier adapter and do not implement production owner key verification.

The old 1.2.10 semantic fixture is retained as a historical skipped suite because the shared current reference validator now enforces later owner-snapshot/high-water requirements. Current 1.2.11 and 1.2.12 suites exercise the callback seam.

RecoveryJoin 1.0.2 and the new verifier seam remain candidate-level. Actual I/D/C key registries, proof signers, ledger queries, pagination and anti-rollback adapters are not connected.


## 6. Final membership-proof exact bundle addendum

- RecoveryJoin 1.0.2 schema: `4b664e3bce465499bcdfd93796349a4ba7074002`.
- RecoveryJoin 1.0.2 tests: `6afa788da2a899f03de8207cb700c40e0533aba1`.
- Unified Schema 1.2.11 tests: `7582091c22ad7f75ed51dba7fbbd02d43af06933`.
- Unified Schema 1.2.12 tests: `5b444aa11ffb86c145ec745752204e623c1c2b41`.
- Semantic reference module requiring an injected owner proof verifier: `6710bd7876be5f2c60640f21090729b8859a7a3e`.
- Exact CI: [Run 44050250038](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44050250038), H HEAD `34fb4ccf8b1580321d38eda1340cf53f73b83f24`, 281 tests, 259 passed, 22 skipped, 0 failed.

The 22 skipped tests belong to the historical 1.2.10 semantic suite and are superseded by active 1.2.11/1.2.12 suites. No production owner signer/verifier is connected. Candidate CI PASS is not production cryptographic conformance.
