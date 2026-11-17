# Phase 3.8.2 — Storage Exact Review: RecoveryJoin, Visibility and Serialization Topology

- Reviewer perspective: Storage / Consistency
- Review mode: **role simulation in the integration session; not an independent Storage Owner signature**
- Decision: **ACCEPT WITH ENUMERATED AMENDMENTS; TOPOLOGY ADR-BLOCKED**
- Project phase: architecture proposal only; no implementation/conformance PASS.

## 1. Exact review targets

- D Phase 3.8 contract: Blob 17e53890dd6cce9bea9eacc1be2e64b0ef55ac78.
- E Phase 3.8 contract: Blob 475fee41e5eea527af4edefbfe88c58c86967d0a.
- I Phase 3.8 contract: Blob 54bab0484bd232a5a258e65e34cc7425288b39a6.
- Storage Phase 3.8 visibility contract: Blob 175ee7b1349cfdb79a19898b311a88391ed88010.
- Storage Phase 3.6.11 bidirectional JoinProof: Blob 4520860b28429d35cdb2ca947a56d0ccb64226a3.
- H RecoveryJoin schema 1.0.0: Blob dd3234aa1c74caf6d0e335875cd96e0b2b64082f.
- H semantic validator/test contract: Blob 6f66a72a2d0aa43af338ff9e22d650d47aa2bd80.
- HRC/JPF executable suite: Blob 60a2f4db4bd12f2131ecd147db9bbe328da6db50.
- A race/crash/failover matrix: Blob c0f8ae699a42de46d12d0d311892e5670014e0f1.

## 2. Storage disposition

The bidirectional join design preserves separate authorities and the acyclic digest chain:
ParticipantManifestContentDigest → RecoveryBatchDigest → ParticipantManifestRecordDigest → RecoveryJoinProofDigest → owner release / RecoveryEpochCompleted.

It correctly distinguishes:
- COC ParticipantIntent set through exact prefix P;
- I/D/C request sets;
- I/D/C admission sets;
- OwnerAdmissionRef vs OwnerEntryRef;
- C primary admission anchor vs additional I/D/C/Storage evidence edges;
- NOT_REGISTERED no-effect proof vs unresolved pending obligation;
- D/I/C owner release vs COC recovery completion;
- Storage PreparedParticipantRef/GID/DatabaseIncarnationRef vs COC ParticipantIntentRef.

Storage can persist and quorum-commit JoinProof only after complete authoritative readback of the batch, manifest and owner snapshots. Storage cannot sign or issue I/D/C gate release.

## 3. Blocking amendments

### STORAGE-RJ-01 — JoinProof must include exact request-row disposition

Every I/D/C request member must map to exactly one request disposition by OwnerRequestRef + OwnerEntryRef + OwnerRequestDigest + owner-local sequence namespace/value + Scope. OUT_OF_SCOPE_WITH_PROOF requires an owner-signed proof. A missing request edge blocks JoinProof even if all admission/participant joins match.

### STORAGE-RJ-02 — Manifest enumeration must be independently re-readable

A complete ParticipantManifest must equal the authoritative COC participant set through exact prefix P, including every page/cursor and committed entry digest. Count/root equality without authoritative prefix enumeration is not sufficient. Missing page, stale follower or quorum loss is UNKNOWN.

### STORAGE-RJ-03 — Both digest phases must be crash-safe

Keep the Storage v3.1 digest order: precomputed manifest content → batch → committed manifest record → JoinProof. Crash after batch but before manifest, or after manifest before JoinProof, stays fenced and resumes the same immutable IDs/digests. Never replace a batch or manifest identity to escape an ACK gap.

### STORAGE-RJ-04 — Owner release currentness remains independent

JoinProof is not an aggregate release token. I/D/C each re-read their own authoritative roots/high-waters/generations/anti-rollback anchor and perform a local CAS. Any advance returns STALE and requires a new round. COC cannot release an owner gate.

### STORAGE-RJ-05 — Physical topology remains unselected

The Phase 3.8 Storage visibility contract's one-serializable-DB-per-Canonical-Authority idea is a recommendation, not a deployed topology. The Phase 3.8.2 ADR records Option A as conditional preference, Option B as an alternative and check-then-write as rejected. No actual Canonical Authority runtime/DB adapter or D/Storage shared serialization domain has been designated. JF-10 PostgreSQL 18.7 candidate CI is not proof of production topology.

## 4. Required Storage tests

- Batch/manifest/JoinProof digest order with crash after each commit.
- Missing/duplicate participant, request or admission row.
- OwnerAdmissionRef and OwnerEntryRef independently substituted.
- Same owner row joined to two participants.
- Same participant joined to conflicting operation/scope/digest.
- Empty COC prefix plus empty/non-empty owner request/admission combinations.
- NOT_REGISTERED with no effect vs possible effect.
- JoinProof created then I/D/C high-water advances before release CAS.
- JF-10 same GID/DatabaseIncarnationRef COMMITTED/ROLLED_BACK/UNKNOWN mapping.
- DB failover, old-primary fencing, stale replica, snapshot rollback and restore quarantine.
- Actual visibility pointer, PublicationReceipt, Storage outcome and outbox atomicity.

## 5. Topology ADR disposition

The new Storage topology ADR is **ADR-BLOCKED / NO TOPOLOGY SELECTED**. Option A is preferred only if the real Canonical Authority runtime proves D and Storage can share the approved serializable transaction domain while preserving semantic ownership. Otherwise Option B requires a named durable linearizable coordinator and independent failover proof. The actual runtime, DB adapter, D/Storage row ownership, read path, deployment topology, human operator/on-call and PITR/old-primary fencing remain open.

## 6. Storage conclusion

**ACCEPT WITH ENUMERATED AMENDMENTS** for the logical JoinProof and visibility contract. STORAGE-RJ-01..05 remain explicit blockers. No schema freeze, DB product/topology approval, implementation/conformance PASS, deployment or production activation is claimed.

## 7. 中文结论

Storage 接受双向 Join Proof 的逻辑方向：COC Prefix Participant 集合与 I/D/C Request/Admission 集合分别由各自权威完整枚举，再通过两方向 Typed Edge 建立关系。必须保留 OwnerAdmissionRef 与 OwnerEntryRef 的区分，C Primary Admission Anchor 与 I/D/C/Storage 其他证据分开，NOT_REGISTERED 必须有无副作用证明或保持 Pending。Storage 只持久化/提交 JoinProof，不能签发 Owner Gate Release。

物理拓扑 ADR 仍 ADR-BLOCKED：Option A 是有条件优先候选，Option B 是替代方案，Check-then-write 被拒绝；真实 Canonical Authority Runtime 和 D/Storage 事务域尚未指定。

本文件是本集成会话中的 Storage 角色模拟审查，不是独立 Owner 签名。


## 8. H/Storage schema follow-up

The latest RecoveryJoin schema now binds every owner request row by both logical request digest and owner-row digest, carries distinct OwnerAdmissionRef and OwnerEntryRef, and requires typed D lineage, I authorization, C provider and Storage prepared/resolution evidence. This addresses the schema-shape portion of STORAGE-RJ-01 and makes the bidirectional contract more precise. It does not replace live authoritative enumeration, signed proof dereference, quorum readback or owner-local release CAS. STORAGE-RJ-02..05 remain open, especially physical topology/HA/restore.

Updated Storage JoinProof contract Blob: 4520860b28429d35cdb2ca947a56d0ccb64226a3.
Updated H RecoveryJoin schema Blob: dd3234aa1c74caf6d0e335875cd96e0b2b64082f.
Updated H semantic contract Blob: 6f66a72a2d0aa43af338ff9e22d650d47aa2bd80.
Updated HRC suite Blob: 60a2f4db4bd12f2131ecd147db9bbe328da6db50.


## 6. Exact H candidate and C provider-boundary cross-review / H 候选与 C Provider 边界交叉复核

Current exact references reviewed:
- H RecoveryJoin schema 1.0.0: `dd3234aa1c74caf6d0e335875cd96e0b2b64082f`.
- H semantic contract: `6f66a72a2d0aa43af338ff9e22d650d47aa2bd80`.
- HRC/JPF suite after fixture correction: `60a2f4db4bd12f2131ecd147db9bbe328da6db50`.
- H wire suite: `1a4e754ba9bfa57eb973c6d39731e9f89443b323`.
- H schema suite: `67aba74c120f2916d768e7b01c45408ee2624f3a`.
- H CI run [44039990464](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44039990464): 66/66 candidate tests PASS.
- C Phase 3.8.2 RecoveryJoin/provider-side-effect exact review: commit `d5be3be10f7144476ddc61a94f29faff67424292`.
- Storage bidirectional JoinProof contract: `4520860b28429d35cdb2ca947a56d0ccb64226a3`.

Storage recognizes the H pass as reference-model/schema/wire-candidate evidence only. It does not exercise authoritative COC prefix enumeration, actual owner request/admission ledgers, live quorum readback, Storage durable JoinProof commit, or any owner-local currentness CAS. It does not prove Storage final VisibilityPointer + PublicationReceipt + outcome + outbox atomicity.

C's exact review correctly preserves the C ProviderIdempotencyKey as a C-owned namespace, distinct from Storage PreparedTransactionGID and engine-native XID. Storage must persist/recover the exact provider attempt references supplied by C but must not mint provider keys or infer CSubmitOutcome from Storage commit.

The H test correction addressed a test-fixture issue only. The original JPF-08 fixture returned UNKNOWN because it required unrelated I/D evidence that the test did not supply; the corrected fixture isolates the duplicate C primary-admission invariant. This did not weaken production validator behavior. The CI result remains a test-harness pass, not an implementation proof.

**Storage disposition unchanged:** logical bidirectional JoinProof accepted with enumerated amendments; physical serialization topology remains ADR-BLOCKED. T1–T8 and STORAGE-RJ-01..05 remain OPEN. No production DB/topology, visibility gate, deployment, or TAB-001 freeze is approved.


## 9. Exact-pin refresh after H 66-test execution and Storage JoinProof revision

This addendum supersedes the earlier target pins in §§1 and 8 only for the artifacts explicitly listed below. The review remains a delegated Storage-role simulation, not an independent Owner signature.

### 9.1 Current exact targets

| Artifact | Branch | Current Blob / Run |
|---|---|---|
| D Phase 3.8 publication participant contract | `session-d-memory-brain-2026-11-16` | `17e53890dd6cce9bea9eacc1be2e64b0ef55ac78` |
| E Phase 3.8 orchestration contract | `session-e-memory-compiler-2026-11-16` | `475fee41e5eea527af4edefbfe88c58c86967d0a` |
| I Phase 3.8 authorization proof contract | `session-i-security-governance-2026-11-16` | `54bab0484bd232a5a258e65e34cc7425288b39a6` |
| Storage Phase 3.8 visibility contract | `session-storage-consistency-forget-atomicity-2026-11-16` | `175ee7b1349cfdb79a19898b311a88391ed88010` |
| Storage Phase 3.6.11 bidirectional JoinProof contract | same Storage branch | `364bf7e7833af3d97bc676f7f356e79251ea6cb4` |
| Storage COC protocol v3.2.2 companion | same Storage branch | `ce3c41adf826a622a3717eca481b5d53e6549196` |
| H RecoveryJoin schema 1.0.0 | `session-h-bmcp-protocol` | `dd3234aa1c74caf6d0e335875cd96e0b2b64082f` |
| H semantic validator contract | same H branch | `6f66a72a2d0aa43af338ff9e22d650d47aa2bd80` |
| HRC/JPF suite | same H branch | `60a2f4db4bd12f2131ecd147db9bbe328da6db50` |
| Wire suite | same H branch | `1a4e754ba9bfa57eb973c6d39731e9f89443b323` |
| Schema integrity suite | same H branch | `67aba74c120f2916d768e7b01c45408ee2624f3a` |
| H workflow run | GitHub Actions | [44040502709 — SUCCESS](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44040502709), commit `1c6ddd301d538652ceea22ea665d50c5fad8178e` |

### 9.2 Updated Storage assessment

The current JoinProof artifact now explicitly includes the H schema's separate request/admission source sets, row-level OwnerAdmissionRef vs OwnerEntryRef, owner request dispositions, typed D/I/C/Storage evidence, JF-10 sub-join, currentness checks and both directional relations. The current H test bundle has 66 methods and a successful GitHub Actions run.

This does not close the production/integration gaps:
- HRC/JPF tests run against a normalized reference model and HRC-TEST-v1, not live signed I/D/C owner snapshots or the authoritative COC quorum prefix.
- Schema integrity tests inspect required schema shape; they do not run a production JSON Schema-to-semantic adapter or verify signatures.
- Storage has not executed the live prefix enumeration, complete pagination/readback, durable JoinProof quorum append, or real owner-ledger joins.
- Owner-local I/D/C currentness CAS is not implemented or proven by the H suite.
- JF-10 same-GID/DB-incarnation behavior is not exercised by the 66 H tests.
- Phase 3.8.2 physical D/Storage topology remains ADR-BLOCKED; Option A is conditional, Option B requires a named durable coordinator and proof, Option C remains rejected.

### 9.3 I authority boundary retained

The I review artifact `reviews/security-governance/phase-3.6.9-i-recovery-cutoff-wire-authority-review.md` Blob `5a95e1764c3fb812046c8f725a3dd325d9385b17` records **CANDIDATE / NO I WIRE APPROVAL** for the reviewed Recovery Cutoff 1.0.1 schema because PolicyDomain, typed Scope, global inventory/TargetInventorySeal, restore-attempt and exact Storage tuple fields were underrepresented. That review is not an approval or rejection of the later RecoveryJoin 1.0.0 schema, but it is a binding warning: H/Storage must not claim I wire approval or infer that generic owner snapshot fields prove I global-inventory currentness. I must review the exact integrated schema and its explicit I subrecord before any I acceptance.

C's exact RecoveryJoin/provider-side-effect review remains a delegated role simulation and keeps ProviderIdempotencyKey, ProviderAttemptRef and CSubmitOutcome separate from Storage GID/XID. It does not prove a real provider adapter.

### 9.4 Revised disposition

**ACCEPT WITH ENUMERATED AMENDMENTS** remains the Storage-role disposition for the logical bidirectional JoinProof and Phase 3.8 composition. This exact-pin refresh does not upgrade the status to independent Owner acceptance, wire/schema freeze, physical topology approval, implementation/conformance PASS or production activation.

STORAGE-RJ-01..05, C-RJ-01..08, I authority/currentness proof, H production wire/crypto interoperability, and Storage topology T1–T8 remain OPEN unless separately closed by exact current Owner evidence.


## 10. Current JoinProof artifact exact re-review after H 66/66 run

The Storage JoinProof source has advanced to Blob `364bf7e7833af3d97bc676f7f356e79251ea6cb4` with §16 recording H's current 66/66 candidate CI run. The H source bundle is now H semantic contract `6f66a72a2d0aa43af338ff9e22d650d47aa2bd80`, HRC/JPF `60a2f4db4bd12f2131ecd147db9bbe328da6db50`, Wire `1a4e754ba9bfa57eb973c6d39731e9f89443b323`, Schema Integrity `67aba74c120f2916d768e7b01c45408ee2624f3a`, RecoveryJoin schema `dd3234aa1c74caf6d0e335875cd96e0b2b64082f`; CI run [44040502709](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44040502709) succeeded with 66 tests.

Storage's logical JoinProof disposition remains **ACCEPT WITH ENUMERATED AMENDMENTS**. The latest CI result improves candidate-suite evidence only; it does not close STORAGE-RJ-02 live prefix enumeration, STORAGE-RJ-04 owner currentness CAS, STORAGE-RJ-05 topology, or the real JF-10 physical sub-join. No independent Owner approval or physical conformance is claimed.

This review remains a delegated Storage-role simulation. The latest JoinProof Blob must be re-reviewed by actual H/I/D/C/Storage Owners; previous exact-Blob decisions do not automatically transfer.


## 11. Latest H workflow rerun / current JoinProof pin

The controlling Storage JoinProof artifact is now Blob `d5a84aa22e90d7b8689b23cd8af2fc82125368c4`. It records H's latest rerun [44041395001](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44041395001), job `133896572160`, on H branch commit `b4d7ed2798fcd6514892ac91d8f3ae6c06f0a338`; 66 tests ran and the job ended OK. Test source/schema blobs are unchanged from §10.

The rerun does not add new test vectors. Storage's ACCEPT WITH ENUMERATED AMENDMENTS remains a logical contract disposition only. Actual COC prefix/quorum reads, six live owner-ledger enumerations, signed proof verification, durable JoinProof commit/readback, I/D/C currentness CAS, same-GID JF-10 physical resolution, and topology T1–T8 remain open. This remains a role simulation, not an independent Storage Owner signature.


## 7. Schema 1.2.7 signature profile persistence boundary / Schema 1.2.7 签名配置持久化边界

H schema 1.2.7 exact review Blob `8bed0b05cd631014bf5af7cb5a8dafdd932940e9`; schema Blob `e9748a5b904d2b975e47a32a0cbb31de31636854`. Storage accepts `signature_profile_id` as a signed-envelope reference field only, not as a trust decision. Storage may persist the exact bytes/reference and include it in the immutable proof digest, but must not resolve issuer trust, select algorithms or treat the payload's profile as authenticated. I remains authoritative for trust/key/profile resolution; H owns wire shape; C owns Provider Outcome truth. Because the 66-case candidate suite does not cover schema 1.2.7, no validator or cryptographic conformance PASS is claimed. Storage topology remains ADR-BLOCKED.


## 12. Expanded H 93-test suite and current JoinProof exact pin

The controlling Storage JoinProof contract is now Blob `155b0d613dc785f9f5904e4509cfce1ed06a2f0d`. It records the H 93-method candidate suite and latest CI run [44042074640](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44042074640), commit `fb9a2ab8b528c2b7010d935372f76a14d6676755`, with Node.js 22 explicitly configured; 93 tests completed successfully.

The added TPH-01..26 reference tests improve executable coverage of the two-record Batch/Manifest digest chain and restore-fenced state machine. XLANG-01 compares Python and Node implementations over fixed HRC-TEST-v1 vectors. These are meaningful candidate improvements, but not production conformance.

Updated H exact pins:
- Semantic contract: `e38ab74d29ded66987d3295503b6f717b6cd83e6`.
- Two-phase reference/tests: `4c8dcafdb49db5279a1d1190b832a9c6c05d6b67` / `690ab42b4f8f7e61adf38fd7b6006f20cc71a7f5`.
- Python/Node differential test/reference/vectors: `1b32fdf81530353b8bd4571fe6d4f77119a0458b` / `992585d3bc323dc0224d0075ef14abd992980f65` / `cc7e98c729db8d9f615e17a9542b3cb63f459922`.
- Workflow: `55d877499010f6a776ae432c1fb2a3a31bae5f11`.

The H suite still uses HRC-TEST-v1, not an I-approved production signature/canonicalization profile. TPH uses a deterministic reference model, not a real quorum log or durable COC service. XLANG-01 compares only fixed test vectors; it does not establish full SDK interoperability.

Storage's exact disposition remains **ACCEPT WITH ENUMERATED AMENDMENTS** for the logical JoinProof only. Live COC/owner-ledger enumeration, signatures/key status, durable JoinProof commit/readback, owner-local CAS, JF-10 physical same-GID resolution, and topology T1–T8 remain OPEN. No independent Owner signature or physical conformance PASS is claimed.


## 13. Latest H 95-test exact evidence and Storage JoinProof pin

The controlling Storage JoinProof artifact is now Blob `0deffc2dcead5f88264417c2ae0ae231a38cfb6f`. It records H's latest candidate run [44042568297](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44042568297), commit `b832679d1143e2806cba30e77dd8d0b240334fdc`, job `133900417567`: **95 tests ran, OK**.

The 95 methods are HRC 25, JPF 19, WIRE 10, SCHEMA 14, TPH 26 and XLANG 1. SCHEMA-13/14 add structural checks for unified schema 1.2.7 artifact/wire version distinction and signature_profile_id field shape. They do not prove production semantic requiredness, I trust-registry resolution or cryptographic signature verification.

Storage's logical JoinProof acceptance remains conditional. The run does not execute live COC quorum enumeration, owner-ledger adapters/signatures, Storage durable JoinProof append/readback, I/D/C release CAS, same-GID JF-10 physical resolution, or the D/Storage topology. T1–T8 and STORAGE-RJ-01..05 remain OPEN. No independent Owner signature or physical conformance PASS is claimed.


## 14. H 97-test Recovery Cutoff 1.0.5 / RecoveryJoin 1.0.1 exact refresh

Current controlling Storage JoinProof Blob: `eaa117aff6635597109c10745f2d70e63e6e0308`.

H's current candidate schema/test pins:
- Recovery Cutoff 1.0.5: `75cd1fedefd50a6ed570b5afaa2d1f9cc4c6a4c7`.
- RecoveryJoin 1.0.1: `f94e01cf30b4c59fca24cb4ccd8b76a0db8ca95c`.
- Unified COC/JF-10 1.2.8: `70b892797d07489936300a26c0dedfafe1d6e746`.
- H semantic contract: `b32f4a0fe665feefa6eadd3f10c70deb28fe0ba5`.
- Schema tests: `ff2b735ccdbf5d45f3c6b2ee9a25d14db2e3c7ad`.

Latest run [44043100543](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44043100543), job `133902179251`, reports **97 tests ran, OK**. SCHEMA-15/16 add owner-snapshot attestation and typed empty/out-of-scope proof shape checks; they do not verify signatures, complete live pagination, I key status or actual currentness CAS.

Storage accepts the expanded schema candidate shape as a logical proposal only. It does not change the bidirectional JoinProof authority split or close live COC/owner enumeration, signed proof dereference, durable JoinProof append/readback, I/D/C release CAS, JF-10 same-GID physical resolution or topology. No physical conformance PASS or independent Storage Owner signature is claimed.
