# Storage — Freeze-Readiness Evidence Delivery / 冻结前证据交付

- Role / Owner: Storage & Consistency
- Delivery stage: **DATABASE CAPABILITY + LOGICAL-RESTORE EVIDENCE DELIVERED; CROSS-OWNER JF-10 CONFORMANCE OPEN**
- Freeze disposition: **BLOCKED — GATE A PARTIAL PASS / GATE B NOT ACCEPTED FOR CURRENT REVISION / GATE C DEFERRED**
- Snapshot branch: `session-storage-consistency-forget-atomicity-2026-11-16`
- Snapshot HEAD: `59dcf9529ec67abbc4ca87567e8876a55ea92771`
- Provenance: assistant-authored delegated Storage-role delivery at the user's direction; not an independent human Storage Owner signature.

## 1. Executive disposition / 执行结论

Storage has delivered meaningful physical PostgreSQL 18.7 capability evidence for prepared-XID persistence, synchronous failover, ACK loss, unavailable-standby fail-closed behavior, backup/restore, WAL PITR and old-primary fencing/rejoin. The restore high-water logical reference model also has a recorded 25/25 CI pass.

These results qualify a pinned PostgreSQL 18.7 CI capability profile. They do not prove the application-level I/D/COC/C adapters, the integrated JF-10 state machine, a production Canonical Authority deployment, production routing/fencing/monitoring, or an operational restore drill. The current Storage Phase 3.8 visibility contract remains a logical proposal with physical topology and implementation proof open. JF-10 P0 remains open; production activation is not authorized; Multi-PolicyDomain atomicity remains blocked.

Storage 已交付 PostgreSQL 18.7 的真实 CI 能力证据，覆盖 Prepared-XID 持久性、同步故障切换、ACK 丢失、Standby 不可用时 Fail-closed、备份恢复、WAL PITR，以及旧主隔离/回归。Restore High-water 逻辑参考模型也有 25/25 CI 通过记录。

这些结果只证明固定 PostgreSQL 18.7 CI 能力配置，不证明应用层 I/D/COC/C Adapter、集成 JF-10 状态机、生产 Canonical Authority 部署、生产路由/隔离/监控或运维恢复演练。当前 Storage Phase 3.8 Visibility 合同仍是逻辑提案，物理拓扑与实现证明未闭环。JF-10 P0 仍 OPEN；不授权生产激活；Multi-PolicyDomain 原子性仍 BLOCKED。

## 2. Exact evidence register / 精确证据清单

| Evidence | Exact Blob / Run | Result and scope |
|---|---|---|
| PostgreSQL 18.7 prepared-XID capability dossier | `0aabf66848dc97deee028c571183c0d7204008c0` | Pinned CI capability profile; not production deployment acceptance |
| Prepared-XID capability run | [43959079736](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/43959079736) | SUCCESS; durable prepared-XID probe |
| Synchronous failover/promotion | [43908746695](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/43908746695) | SUCCESS; prepared-XID standby promotion/recovery |
| Standby unavailable fail-closed | [43927416496](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/43927416496) | SUCCESS; UNKNOWN/private/lock-retention boundary |
| Old-primary fencing/rewind/rejoin | [43930047054](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/43930047054) | SUCCESS; old primary stays fenced and rejoins as standby |
| Coordinator ACK-gap recovery | [43912857694](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/43912857694) | SUCCESS; same-XID coordinator ACK-gap recovery |
| TCP CommandComplete ACK loss | [43913477785](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/43913477785) | SUCCESS; same-XID recovery after real TCP response loss |
| Physical backup/restore | [43955195219](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/43955195219) | SUCCESS; physical restore and stale-control gate fixture |
| WAL archive PITR | [43955195388](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/43955195388) | SUCCESS; point-in-time recovery to explicit LSN |
| PITR atomicity / archive negative cases | [43958775001](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/43958775001) | SUCCESS; prepared-XID/VisibilityPointer/PublicationReceipt atomicity and negative cases |
| Restore high-water reference model evidence | `bf991a8a098bfdacc24bace53d452b8ccf2078e6` | 25/25 logical tests PASS; run 43965501810 |
| Restore high-water test implementation | `a9e1a96b449c6bf0e2b52c5fea394a8c32961a24` | Logical reference tests, not production restore |
| Storage Batch/Manifest ordering amendment | `1c8c0bc11798293293bcf47fa560f1699a5bcfe0` | Proposed; exact C/H/A review required |
| Storage exact-version binding manifest v2 | `8688a03c69227284cd00b4110d87019cd346bfb2` | Pins owner-local decisions; A final integration required |
| Storage Phase 3.8 visibility participant/atomic outcome contract | `175ee7b1349cfdb79a19898b311a88391ed88010` | Logical proposal; physical topology and implementation proof OPEN |
| JF-10 executable conformance plan | `49056cd46fd30445c0e564c99e0e234f60f065c4` | TEST DESIGN / NOT EXECUTED |

## 3. Storage invariants / Storage 不变量

1. Storage owns durable participant records, isolation/serialization, idempotency, private staging, authoritative VisibilityPointer, visibility outcome proof, outbox commit and crash/failover/restore mechanics.
2. Storage does not mint D Admission/ForgetFence/PublicationParticipantRef, I authorization/PermissionEpoch/CommitAuthorizationReceipt, C ParticipantIntent/CSubmitOutcome or Global Forget completion.
3. PrepareVisibility creates an immutable PREPARED_HIDDEN participant bound to PublicationOperationId + tuple digest. D admission must bind the exact persisted Storage participant; I consumes a single-use CommitAuthorizationReceipt bound to the exact D and Storage participant refs.
4. The final Visibility transaction is the sole visibility linearization point. It atomically verifies Storage PREPARED_HIDDEN, current D participant/fence proof, consumed I CommitAuthorizationReceipt, exact artifact/version/digest, complete dependencies, Scope and current attempt/lease; then commits VisibilityPointer, PublicationReceipt/Outcome and Outbox.
5. Until that transaction commits, all read paths remain private. Object-store existence, signed URL, cache, index event, queue or outbox delivery is not visibility.
6. UNKNOWN remains private. NO_PUBLICATION requires positive proof that no pointer exists and no delayed writer/retry/outbox can still publish.
7. PostgreSQL engine-native numeric XID is not the cross-service identity. A stable client-chosen PreparedTransactionGID binds the exact operation; native XID is observed evidence only. Same-GID recovery and authoritative outcome readback are mandatory.
8. Restore remains quarantined until database incarnation, prepared participant ledger, I current policy/receipt state, D fence/lineage and COC committed prefix are reconciled.

## 4. What the evidence does not prove / 证据边界

- PostgreSQL 18.7 CI capability success does not prove live I sequencer integration, D fence serialization, C provider egress, COC quorum integration, application VisibilityPointer implementation or independent read-path enforcement.
- The restore high-water 25/25 suite is a logical model, not a production backup restore or real I/D control-ledger replay.
- The JF-10 conformance plan explicitly remains NOT EXECUTED; mocks that return expected values are not acceptable conformance evidence.
- Storage Phase 3.8 is a role-level logical proposal. Actual DB/coordinator topology, isolation profile, read-path enforcement, outbox guarantees, failover/restore topology and cross-service durable prepare/commit remain open.
- Gate B's older revision `4ac63ac79491e79ec0c9114ef73941c73d7bbf25` was design-level accepted with exceptions; the amended revision `86ff3b247d7565a0dcd1f2e4ed21b5ba70a6b0d7` remains published and focused exact-owner re-review required, not yet accepted overall.
- Storage's acceptance of the §14 PreparedParticipantGID mapping with conditions does not imply acceptance of the entire amended COC protocol.
- Production deployment/operations, named operator, runbook, measured RPO/RTO and multi-PolicyDomain atomicity are not approved.

## 5. Phase 3.8.2 serialization topology ADR / 序列化拓扑 ADR

The latest Storage branch adds an explicit topology ADR (Blob `080433f8e13a500522bc2754da64057edb0ae9d8`), status **ADR-BLOCKED — CANDIDATE OPTIONS ONLY; NO DEPLOYED TOPOLOGY SELECTED**.

- Option A: one Serializable transaction domain per Canonical Memory authority, with D retaining semantic authority and Storage owning the physical visibility transaction. Preferred only if the real deployment proves the shared transaction boundary and all protected read paths use it.
- Option B: separate D and Storage services with a durable linearizable coordinator and independently proven prepare/commit, failover and restore.
- Option C (check-then-write / asynchronous event coordination) is explicitly **REJECTED**.
- T1–T8 remain OPEN: runtime/DB identity, D/Storage row ownership, final linearization, I proof verification, atomic outcome, HA/restore, read-path enforcement and D/I/Storage/A owner decisions.

This is a material blocker clarification: PostgreSQL CI capability evidence does not select Option A or prove the actual project Canonical Authority uses PostgreSQL 18.7. Option A remains conditional; Option B needs its own approved ADR and proof bundle.

最新 Storage 分支新增 Phase 3.8.2 拓扑 ADR，明确当前没有选择实际部署拓扑。Option A（单 Serializable 事务域）只是有条件优先候选；Option B（独立服务 + 持久化线性协调器）需要单独决策与证明；Option C（check-then-write/异步事件协调）明确拒绝。T1–T8 全部仍 OPEN。

## 6. Freeze exit criteria / 冻结退出条件

| ID | Required evidence | Current status |
|---|---|---|
| ST-FR-01 | Exact COC amended Blob and bidirectional Batch/Manifest + participant joins accepted by A/I/D/C/H/Storage | OPEN |
| ST-FR-02 | Selected production-equivalent DB/coordinator profile and D/Storage serialization authority | OPEN |
| ST-FR-03 | Real JF-10 H01–H13 / JF10-01…X-17 cases on the integrated coordinator and DB | NOT EXECUTED |
| ST-FR-04 | Exact I receipt and D fence verified at actual Visibility linearization point | OPEN |
| ST-FR-05 | Same-GID recovery, ACK loss, failover, restore and anti-rollback with authoritative reader/bypass probes | PARTIAL — engine capability only |
| ST-FR-06 | Private staging, object-store ACL and every read/cache/index/outbox path proven hidden on UNKNOWN | OPEN |
| ST-FR-07 | Production topology, operator, runbook, monitoring, RPO/RTO and restore drill | DEFERRED TO ENGINEERING / OPEN |
| ST-FR-08 | Multi-PolicyDomain transaction or explicit rejection profile | BLOCKED |

## 7. Storage final delivery statement / Storage 最终交付声明

**Delivered:** pinned PostgreSQL 18.7 capability evidence, logical restore model evidence, exact-version design artifacts and owner-boundary contracts.

**Not delivered:** integrated JF-10 conformance, production Canonical Authority deployment, complete cross-owner COC acceptance, operational restore proof or Multi-PolicyDomain atomicity.

**Decision:** Storage evidence delivery is complete for the database-capability/documentary stage. Storage freeze-readiness remains **BLOCKED** until ST-FR-01 through ST-FR-08 are satisfied.


## 7. Exact RecoveryJoin, bidirectional Owner Admission join and H CI evidence refresh

- Storage controlling bidirectional JoinProof contract: `reviews/storage-consistency/phase-3.6.11-storage-bidirectional-coc-owner-admission-join-proof.md`, Blob `364bf7e7833af3d97bc676f7f356e79251ea6cb4`.
- Storage COC protocol v3.2.2 companion: `reviews/storage-consistency/phase-3.6-coc-durable-log-and-recovery-protocol-storage-design-v3.2.2.md`, Blob `ce3c41adf826a622a3717eca481b5d53e6549196`.
- Storage exact review / topology disposition: `reviews/storage-consistency/phase-3.8.2-storage-exact-review-and-topology-disposition.md`, Blob `0fc74ef747b6e45f8a7d7fcbe8657b88ba67e82d`.
- Storage topology ADR: Blob `080433f8e13a500522bc2754da64057edb0ae9d8` — **ADR-BLOCKED / NO TOPOLOGY SELECTED**.
- H RecoveryJoin schema 1.0.0: Blob `dd3234aa1c74caf6d0e335875cd96e0b2b64082f`.
- H semantic validator contract: Blob `6f66a72a2d0aa43af338ff9e22d650d47aa2bd80`.
- HRC/JPF suite: Blob `60a2f4db4bd12f2131ecd147db9bbe328da6db50`.
- H Wire suite: Blob `1a4e754ba9bfa57eb973c6d39731e9f89443b323`.
- H Schema integrity suite: Blob `67aba74c120f2916d768e7b01c45408ee2624f3a`.
- H CI run [44040502709](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44040502709), commit `1c6ddd301d538652ceea22ea665d50c5fad8178e`: **66/66 PASS**, candidate reference suite only.
- C delegated exact RecoveryJoin/provider-side-effect review: Blob `a7b57bd5531222559666f0f1d9df59a259cde61a`; provider implementation remains unverified.
- I recovery-cutoff wire-authority review: Blob `5a95e1764c3fb812046c8f725a3dd325d9385b17`; that review is **CANDIDATE / NO I WIRE APPROVAL** for its exact 1.0.1 target and does not approve RecoveryJoin 1.0.0.

The Storage JoinProof contract specifies the acyclic ContentDigest → BatchDigest → ManifestRecordDigest → JoinProofDigest chain, exact COC prefix enumeration, six independent I/D/C request/admission sets, both directional typed joins, OwnerAdmissionRef vs OwnerEntryRef row identity, request-row dispositions, explicit difference sets, JF-10 same-GID/DB-incarnation sub-join and independent owner-local currentness CAS.

The H 66/66 CI result proves only that the checked-in Python HRC/JPF/WIRE/SCHEMA candidate suite passed on GitHub Actions. It does not execute live COC quorum prefix enumeration, real owner ledger adapters, owner signatures/key-status verification, Storage durable JoinProof commit, owner-local CAS, JF-10 same-XID physical resolution, or production multi-language interoperability.

C ProviderIdempotencyKey remains a C-owned namespace and cannot be replaced by Storage PreparedTransactionGID or PostgreSQL native XID. C provider outcome remains C-owned. I/D/C each independently own their gate-release decisions. Storage/COC cannot issue them.

**Current disposition:** logical JoinProof accepted with enumerated amendments in delegated role review; physical topology and integrated conformance remain OPEN. No DB topology selection, implementation PASS, production activation or freeze is claimed.


## 8. Current Storage exact review pin / Storage 当前精确审查版本

The latest readback of the Storage Phase 3.8.2 exact review is Blob `2726f0a2a5168f126d25eb48b857d8921a09031e`; the latest bidirectional JoinProof contract is Blob `668faeb20e3e9cb907a8d1061635b12162f3dbe2`. The topology ADR remains `080433f8e13a500522bc2754da64057edb0ae9d8`, ADR-BLOCKED / NO TOPOLOGY SELECTED. H CI [44040312711](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44040312711) is 66/66 candidate PASS, not live Storage/COC integration. T1–T8 and STORAGE-RJ-01..05 remain OPEN.


## 9. Latest H CI and current Storage snapshot / 最新 H CI 与 Storage 快照

Storage has re-read the latest H run [44041110983](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44041110983): 66/66 candidate tests PASS. This is not live Storage/COC/JF-10 conformance. Current Storage branch snapshot for this update: `8540568a469afaf8a7425ace0e8103a407cfd713`. Current Storage exact review Blob: `2726f0a2a5168f126d25eb48b857d8921a09031e`; current JoinProof Blob: `668faeb20e3e9cb907a8d1061635b12162f3dbe2`. Physical topology remains ADR-BLOCKED.
