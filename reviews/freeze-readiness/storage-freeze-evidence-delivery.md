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

- Storage controlling bidirectional JoinProof contract: `reviews/storage-consistency/phase-3.6.11-storage-bidirectional-coc-owner-admission-join-proof.md`, Blob `155b0d613dc785f9f5904e4509cfce1ed06a2f0d`.
- Storage COC protocol v3.2.2 companion: `reviews/storage-consistency/phase-3.6-coc-durable-log-and-recovery-protocol-storage-design-v3.2.2.md`, Blob `ce3c41adf826a622a3717eca481b5d53e6549196`.
- Storage exact review / topology disposition: `reviews/storage-consistency/phase-3.8.2-storage-exact-review-and-topology-disposition.md`, Blob `6c0ca46dfdb2d3b142c1796ae44b0cc23f67bf0a`.
- Storage topology ADR: Blob `080433f8e13a500522bc2754da64057edb0ae9d8` — **ADR-BLOCKED / NO TOPOLOGY SELECTED**.
- H RecoveryJoin schema 1.0.0: Blob `dd3234aa1c74caf6d0e335875cd96e0b2b64082f`.
- H semantic validator contract: Blob `e38ab74d29ded66987d3295503b6f717b6cd83e6`.
- HRC/JPF suite: Blob `60a2f4db4bd12f2131ecd147db9bbe328da6db50`.
- H Wire suite: Blob `1a4e754ba9bfa57eb973c6d39731e9f89443b323`.
- H Schema integrity suite: Blob `67aba74c120f2916d768e7b01c45408ee2624f3a`.
- H CI run [44042074640](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44041395001), commit `fb9a2ab8b528c2b7010d935372f76a14d6676755`: **66/66 PASS**, candidate reference suite only.
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


## 10. C Provider Outcome cross-review / C Provider Outcome 交叉审查

C has published a protocol-boundary review of H unified schema 1.2.5 (C review Blob `fd34218202259daa1a66f5ca1746de4e1141bf2f`; H exact schema Blob `164ec3c436558d5d93032edc51e127d15e03db4d`). The wire enum is `HANDOFF_ACCEPTED | HANDOFF_REJECTED | NOT_INVOKED | UNKNOWN | IN_DOUBT`; C alone creates CSubmitOutcome. Storage may persist/validate references but cannot synthesize provider truth. C's own canonical outcome contract was not located/pinned in that review, so Storage does not treat the schema fields as proof that a valid C outcome exists. Provider outcome runtime, same-key recovery and exact C source pin remain OPEN.


## 11. H schema 1.2.7 signature-profile persistence / H Schema 1.2.7 签名配置持久化

Storage exact review now includes the signature-profile boundary (current Storage review Blob `b12d73f0c48aff0b1a339902c29beabcf6aec530`). H schema 1.2.7 Blob `e9748a5b904d2b975e47a32a0cbb31de31636854`; H review Blob `8bed0b05cd631014bf5af7cb5a8dafdd932940e9`. Storage may persist and digest-bind the exact profile reference, but I alone resolves trust/key status; Storage cannot authenticate or choose a profile. Current H 66-case CI does not cover schema 1.2.7. Physical D/Storage topology remains ADR-BLOCKED.


### 7.1 H expanded suite scope refresh

The latest H candidate inventory is 93 methods: HRC-01..25, JPF-01..19, WIRE-01..10, SCHEMA-01..12, TPH-01..26 and XLANG-01. The 26 TPH vectors exercise the reference-model Batch/Manifest two-record digest/order/readback/fenced-restore contract. XLANG-01 compares Python and Node.js outputs over three fixed HRC-TEST-v1 canonical UTF-8/digest vectors. GitHub Actions run 44042074640 reports 93 tests, OK, with Node.js 22 configured.

This is a candidate reference-model/differential test pass only. It does not execute a production COC quorum, authoritative owner ledgers, I signatures/key registry, Storage JoinProof persistence, owner currentness CAS, physical JF-10 or actual D/Storage topology. HRC-TEST-v1 remains non-production. Storage freeze remains BLOCKED.


## 12. H/I Phase 3.8.3 crypto profile and expanded candidate suite / 密码学配置与扩展候选套件

The latest H workflow [44042093922](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44042093922) reports 93/93 candidate tests PASS, including HRC/JPF, two-phase Batch/Manifest, Python/Node fixed-vector differential, wire and RecoveryJoin schema candidates. This remains test-harness evidence and does not validate physical Storage or production signatures.

I candidate crypto profile Blob `5eeb011032c53c2f7897d699d6f512b26f07d0a2`; H wire mapping Blob `c30e8ccbecb75b7e27ddceb0cf088afbbb26f562`; H schema 1.2.7 Blob `e9748a5b904d2b975e47a32a0cbb31de31636854`; I exact review Blob `446109f4867268fe7dca3c7e114346f3c1a74b61`. Storage accepts profile identifiers as immutable references only; it cannot resolve trust or select algorithms. I remains the trust authority. H's two-language fixed-vector test is not proof of two independent production implementations.

The new crypto profile does not resolve the physical D/Storage serialization topology. Storage T1–T8 and JF-10 integrated conformance remain OPEN; topology ADR remains BLOCKED.


## 13. H 95-test latest refresh and Storage JoinProof current pins

- Current Storage JoinProof: Blob `0deffc2dcead5f88264417c2ae0ae231a38cfb6f`.
- Current Storage exact review: Blob `2c9327e89d37e8955d9774a18d2575273000d2a2`.
- H semantic contract: Blob `99ccf2b637b6a87be045ed8342c88b15b8816604`.
- H schema integrity suite: Blob `fa4fc9f7d3bf64a90bc992453b13fc1fb3c11879`.
- H unified schema 1.2.7: Blob `e9748a5b904d2b975e47a32a0cbb31de31636854`.
- Latest H CI [44042568297](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44042568297), commit `b832679d1143e2806cba30e77dd8d0b240334fdc`: **95 tests ran, OK**.

The 95 methods include 25 HRC, 19 JPF, 10 WIRE, 14 SCHEMA, 26 TPH and 1 XLANG. The two added schema checks cover only unified 1.2.7 artifact/wire version separation and signature_profile_id field shape. They do not implement production semantic signature_profile_id requiredness or I trust-registry resolution.

Storage's JoinProof remains a logical proposal accepted with amendments. The 95-test CI result does not prove live COC prefix/quorum completeness, signed I/D/C ledger enumeration, Storage JoinProof durability, owner currentness CAS, JF-10 physical same-GID resolution, or selected D/Storage topology. Storage freeze remains BLOCKED; T1–T8, STORAGE-RJ-01..05 and integrated JF-10 conformance remain OPEN.


## 14. H 97-test / RecoveryJoin 1.0.1 refresh

- Storage JoinProof current Blob: `eaa117aff6635597109c10745f2d70e63e6e0308`.
- Storage exact review current Blob: `6610062306ec28fb6d0e127d3422923835e5faf3`.
- H Recovery Cutoff 1.0.5: `75cd1fedefd50a6ed570b5afaa2d1f9cc4c6a4c7`.
- H RecoveryJoin 1.0.1: `f94e01cf30b4c59fca24cb4ccd8b76a0db8ca95c`.
- H unified COC/JF-10 1.2.8: `70b892797d07489936300a26c0dedfafe1d6e746`.
- H semantic contract: `b32f4a0fe665feefa6eadd3f10c70deb28fe0ba5`.
- H schema test suite: `ff2b735ccdbf5d45f3c6b2ee9a25d14db2e3c7ad`.
- Latest H CI [44043100543](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44043100543): **97 tests ran, OK**.

The 97 methods comprise HRC 25, JPF 19, WIRE 10, SCHEMA 16, TPH 26 and XLANG 1. The newest schema vectors cover owner snapshot attestation content binding and RecoveryJoin 1.0.1 complete-empty/out-of-scope proof shape. They do not prove production signatures or live owner/COC behavior. Storage topology, JF-10 physical same-GID, durable JoinProof, currentness CAS and independent Owner acceptance remain OPEN.
