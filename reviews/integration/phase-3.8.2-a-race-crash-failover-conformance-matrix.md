# Phase 3.8.2 — A Race, Crash, Failover and Restore Conformance Matrix

- Owner perspective: A — Principal Integration Architect (integration-session role simulation)
- Status: **REQUIRED PHYSICAL TEST PLAN — NOT EXECUTED / NO PHYSICAL CONFORMANCE PASS**
- Scope: Phase 3.8 D/E/I/Storage publication gate + COC RecoveryJoin + JF-10 bridge
- Language: English and Chinese are normative peers.

## 1. Exact source bundle

| Role | Artifact | Branch | Blob |
|---|---|---|---|
| D | Phase 3.8 D Publication Participant and Terminal Contract | session-d-memory-brain-2026-11-16 | 17e53890dd6cce9bea9eacc1be2e64b0ef55ac78 |
| E | Phase 3.8 E Publication Orchestration, Retry and Recovery Contract | session-e-memory-compiler-2026-11-16 | 475fee41e5eea527af4edefbfe88c58c86967d0a |
| I | Phase 3.8 I Commit Authorization Receipt and Revocation Sequencer Contract | session-i-security-governance-2026-11-16 | 54bab0484bd232a5a258e65e34cc7425288b39a6 |
| Storage | Phase 3.8 Storage Visibility Participant and Atomic Outcome Contract | session-storage-consistency-forget-atomicity-2026-11-16 | 175ee7b1349cfdb79a19898b311a88391ed88010 |
| Storage | Phase 3.6.11 Bidirectional COC/Owner Admission Join Proof | session-storage-consistency-forget-atomicity-2026-11-16 | 5b3f81ada75994cabc6fdab8537d7f185e6c6287 |
| Storage | Phase 3.8.2 Serialization Topology ADR | session-storage-consistency-forget-atomicity-2026-11-16 | 080433f8e13a500522bc2754da64057edb0ae9d8 |
| H | HRC semantic validator contract | session-h-bmcp-protocol | 6f66a72a2d0aa43af338ff9e22d650d47aa2bd80 |
| H | Recovery-cutoff schema 1.0.4 | session-h-bmcp-protocol | d18b9ae1e2ed5e43ee5a78ac43b873b7d42230f1 |
| H | RecoveryJoin schema candidate 1.0.0 | session-h-bmcp-protocol | dd3234aa1c74caf6d0e335875cd96e0b2b64082f |
| H | HRC semantic suite | session-h-bmcp-protocol | 60a2f4db4bd12f2131ecd147db9bbe328da6db50 |
| H | Wire interop suite | session-h-bmcp-protocol | 1a4e754ba9bfa57eb973c6d39731e9f89443b323 |
| H | Schema integrity suite | session-h-bmcp-protocol | 5292d56661e938c905c61455e9ed53c4ff674c54 |

This matrix is a test plan, not a claim that the referenced proposals are independently approved or implemented.

## 2. Global pass/fail rules

A test PASS requires:
- deterministic seed and immutable source/schema/configuration digests;
- exact OperationId, PublicationOperationId, ParticipantIntentRef, OwnerAdmissionRef, OwnerEntryRef, StorageVisibilityParticipantRef, D PublicationParticipantRef, I receipt, GID and DatabaseIncarnationRef captured;
- authoritative readback from each relevant owner (not only COC observation or local projection);
- owner-local positions preserved as typed values; no cross-authority numeric ordering;
- expected pointer/private visibility and outbox/provider side-effect state checked;
- no timeout, missing row, lease expiry, process death or stale replica treated as terminal proof.

Any unknown authority, incomplete enumeration, signature/key uncertainty, stale high-water, split-brain possibility or contradictory outcome is UNKNOWN/IN_DOUBT and fails closed. A test cannot pass by converting UNKNOWN to abort or empty.

## 3. Race matrix

| ID | Race / both serial orders | Expected invariant | Authorities |
|---|---|---|---|
| RACE-01 | RegisterProducerWork vs D InstallForgetFence | Fence-first rejects; registration-first is counted and fence cannot pass unaccounted work | D |
| RACE-02 | Storage PrepareVisibility vs crash / D Admission | D admission only after durable PREPARED_HIDDEN; orphan prepare stays private | Storage, D |
| RACE-03 | D PublicationParticipant admission vs D ForgetFence | Fence-first rejects; participant-first holds Fence until terminal Storage outcome | D, Storage |
| RACE-04 | I revocation vs single-use CommitAuthorization consumption | REVOCATION_WON blocks; COMMIT_WON creates held participant | I |
| RACE-05 | I COMMIT_WON vs later revocation | revocation cannot release before Storage terminal outcome | I, Storage |
| RACE-06 | D current-fence proof vs Storage visibility linearization | stale/missing D proof blocks; pointer commit validates current participant/fence atomically | D, Storage |
| RACE-07 | C final outbound send vs C gate close | unsent reservation cannot be sent after gate close; sent/ambiguous uses same provider key lookup | C |
| RACE-08 | Owner request vs owner snapshot/high-water capture | each request is captured or remains behind closed gate for later batch; none falls between | I, D, C |
| RACE-09 | COC prefix enumeration vs participant append | exact P includes all committed participants through P; later append is outside P and cannot be silently merged | COC |
| RACE-10 | JoinProof creation vs owner high-water/scope/gate advance | release CAS detects advance and returns STALE; new immutable round required | I, D, C, Storage |
| RACE-11 | owner admission vs COC participant registration | REGISTERED must join exact participant; NOT_REGISTERED has no participant fields and no protected effect | I, D, C, H |
| RACE-12 | I/Storage terminal outcome vs COC recovery observation | COC observes; it never creates or overrides owner terminal decision | I, Storage, COC |

## 4. Crash and ACK-loss matrix

| ID | Crash point / lost response | Required recovery |
|---|---|---|
| CRASH-01 | before Storage prepare commit | no participant, no pointer; retry same immutable operation identity |
| CRASH-02 | after Storage PREPARED_HIDDEN before D admission | orphan participant stays private; resolve same StorageVisibilityParticipantRef |
| CRASH-03 | D admission committed, ACK lost | same PublicationParticipantRef lookup; no duplicate participant |
| CRASH-04 | I COMMIT_WON committed, ACK lost | same receipt/nonce/tuple resolution; I revocation remains held |
| CRASH-05 | I REVOCATION_WON committed, ACK lost | same terminal decision lookup; same prepared participant must roll back |
| CRASH-06 | Storage visibility transaction commits, ACK lost | same PublicationOperationId + tuple digest returns original COMMITTED_VISIBLE outcome |
| CRASH-07 | Storage final commit did not occur but response unknown | UNKNOWN until authoritative ledger proves terminal; never infer NO_PUBLICATION |
| CRASH-08 | after Storage outcome before D/I closeout | D/I independently read same outcome and close their own participant |
| CRASH-09 | after COC RecoveryCutoffBatch before ParticipantManifest record | remain fenced; commit/read back same ManifestId and digest; no replacement |
| CRASH-10 | after manifest record before RecoveryJoinProof | remain fenced; rebuild JoinProof from exact immutable batch/manifest and owner snapshots |
| CRASH-11 | after JoinProof before owner release | each owner rechecks currentness CAS; no release on stale high-water |
| CRASH-12 | after one owner release before other owner releases | only that owner's outage gate is reopened; other gates remain closed; no RecoveryEpochCompleted |

## 5. Failover and restore matrix

| ID | Fault | Required result |
|---|---|---|
| HA-01 | primary DB loss after PREPARE | exact same GID + DatabaseIncarnationRef is resolved on authoritative promoted DB |
| HA-02 | old primary rejoins after promotion | old primary is fenced; no dual writer or second visibility pointer |
| HA-03 | synchronous standby unavailable during protected PREPARE | fail closed; no ACK implying durable prepare |
| HA-04 | stale replica returns old owner/participant state | reject; authoritative linearizable source required |
| HA-05 | DB incarnation, cluster system identifier, database OID or timeline mismatch | quarantine; never resolve same-named GID in another incarnation |
| HA-06 | COC leader restart / quorum loss / lost append ACK | exact same batch/manifest/join identities recovered; no synthetic order |
| HA-07 | COC snapshot rollback or missing committed prefix | RESTORE_FENCED |
| HA-08 | owner snapshot behind independent anti-rollback anchor | owner gate stays closed |
| HA-09 | I ProducerDomainInventoryEpoch advances after JoinProof | I release CAS fails STALE |
| HA-10 | D projection/lineage/fence generation advances after JoinProof | D release CAS fails STALE |
| HA-11 | C provider-attempt high-water advances after JoinProof | C release CAS fails STALE |
| HA-12 | Restore has missing/contradictory D/I/Storage evidence | serving remains disabled; no owner gate or barrier is reopened |

## 6. HRC / JoinProof / wire coverage mapping

- HRC-01..09: explicit empty sets, independent request/admission roots and owner-specific high-waters.
- HRC-10..16: exact prefix enumeration, manifest completeness, bidirectional admission/participant identity and batch/snapshot binding.
- HRC-17..19: owner currentness CAS, owner-only gate release and RecoveryEpochCompleted.
- HRC-20..22: I/Storage terminal pairing and UNKNOWN behavior.
- HRC-23..25: idempotency, digest conflict, strict wire/downgrade/duplicate-key behavior.
- JPF-01..12: participant/admission bidirectional join, NOT_REGISTERED semantics, evidence cardinality, scope/currentness and JF-10 tuple.
- JPF-13..17: request-ledger disposition completeness and OwnerEntryRef / OwnerRequestRef binding.
- JPF-18..19: explicit OwnerAdmissionRef vs OwnerEntryRef substitution rejection.
- WIRE-01..10: deterministic test serialization, duplicate key, absent/null, counter, critical field, GID typing and digest domain separation.
- SCHEMA-01..09: schema-family inventory, strict definitions, independent request/admission statuses, JF-10 typed tuple and row identity fields.

The 66-method HRC/JPF/WIRE/SCHEMA candidate suite passed GitHub Actions run 44039990464 (H commit da94bcc1796cb350eed12845e49cbc3663faab9c). The test code uses a TEST-ONLY canonical digest helper. It does not verify production signatures, final H canonicalization, or cross-language canonical bytes. The physical race/crash/failover/restore matrix in this document remains unexecuted.

## 7. Exit criteria

1. H wire-to-normalized adapters for all six recovery-cutoff message families and RecoveryJoin are implemented.
2. JSON Schema 1.0.4 and RecoveryJoin 1.0.0 structural validators run before semantic validators.
3. HRC/JPF/WIRE/SCHEMA suite runs in CI and all deterministic vectors pass; raw logs and artifact hashes are published.
4. At least two independent language implementations produce identical canonical bytes, digests and signature-input bytes under the approved profile.
5. I approves trust/key/historical verification and currentness semantics; D/I/C approve their own admission evidence and release predicates.
6. Storage selects/proves actual D/Storage serialization topology, DB identity, read path, HA/failover and restore.
7. A re-reads exact final blobs and issues an integration decision. No silent inheritance of older owner decisions.

## 8. 中文规范

本矩阵覆盖 Phase 3.8 发布竞态、COC RecoveryCutoff/ParticipantManifest/RecoveryJoin、Owner Admission、JF-10 同一 Prepared Participant 恢复、Crash/ACK Loss、Failover 和 Restore。每个测试必须记录确定性 Seed、精确 Blob/Schema/DB/Config Hash、Operation/Participant/GID/DB Incarnation、各 Owner 权威回读、Visibility Pointer、Outbox/Provider Side Effect 和不变量检查结果。

任何缺失、未知、签名/Key 状态不明、分页不完整、High-water 变化、陈旧副本或分裂脑可能性都必须返回 UNKNOWN/IN_DOUBT 并 Fail Closed。超时、行缺失、Lease 过期、进程死亡不能作为终态证据。COC 只能记录 Owner 证据，不能创造 I/D/C 决策。

Exit 条件包括：H 六类消息与 RecoveryJoin 的 Wire Adapter；Schema 结构验证；HRC/JPF/WIRE/SCHEMA 全部 CI 执行；至少两种独立语言实现的 Canonical Bytes/Digest/Signature Input 互操作；I/D/C 独立批准；Storage 实际事务拓扑、HA/Restore 证据；最后 A 对精确 Blob 复审。


Current executable candidate inventory: 66 unittest methods (25 HRC + 19 JPF + 10 WIRE + 12 SCHEMA). The H candidate unit suite passed 66/66 in run 44039990464; no physical race/crash/failover conformance PASS is available.


CI evidence boundary: the 66 Python candidate tests passed in run 44039990464. The physical race/crash/failover/restore scenarios in Sections 3–5 remain test plans and have not been executed against a real D/Storage/COC deployment.


## 7. Current exact-pin and H candidate-run refresh

The source pins in §1 are historical where they differ from this refresh. Current H candidate bundle:
- RecoveryJoin schema: `dd3234aa1c74caf6d0e335875cd96e0b2b64082f`.
- H semantic contract: `6f66a72a2d0aa43af338ff9e22d650d47aa2bd80`.
- HRC/JPF: `60a2f4db4bd12f2131ecd147db9bbe328da6db50`.
- Wire: `1a4e754ba9bfa57eb973c6d39731e9f89443b323`.
- Schema integrity: `67aba74c120f2916d768e7b01c45408ee2624f3a`.
- Latest H candidate CI [44042074640](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44040502709): 66/66 PASS, commit `fb9a2ab8b528c2b7010d935372f76a14d6676755`.

Current Storage JoinProof source: `reviews/storage-consistency/phase-3.6.11-storage-bidirectional-coc-owner-admission-join-proof.md`, Blob `155b0d613dc785f9f5904e4509cfce1ed06a2f0d`. Current Storage exact review: Blob `6c0ca46dfdb2d3b142c1796ae44b0cc23f67bf0a`. Current Storage topology ADR: Blob `080433f8e13a500522bc2754da64057edb0ae9d8`, ADR-BLOCKED.

The 66-test H candidate run is not a run of the 36 physical cases in this matrix. All race, crash/ACK-loss, failover/restore and authoritative read-path cases remain **NOT EXECUTED** until a real COC, I/D/C adapters and selected D/Storage transaction topology are available. Do not count the H candidate PASS toward any physical case.


### 7.1 H expanded suite boundary

H now reports 93 candidate methods passing in run [44042074640](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44042074640): 25 HRC + 19 JPF + 10 WIRE + 12 SCHEMA + 26 TPH + 1 XLANG. The TPH and XLANG cases are reference/test-profile only. This does not execute any of the 36 physical race/crash/failover/restore scenarios in this matrix. All physical cases remain NOT EXECUTED.


### 7.3 H 95-test boundary

H's latest run [44042568297](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44042568297) reports 95 candidate methods PASS: 25 HRC + 19 JPF + 10 WIRE + 14 SCHEMA + 26 TPH + 1 XLANG. The additional schema cases are structural-only for unified 1.2.7. None of these runs the 36 physical race/crash/failover/restore scenarios in this matrix. All physical cases remain NOT EXECUTED.
