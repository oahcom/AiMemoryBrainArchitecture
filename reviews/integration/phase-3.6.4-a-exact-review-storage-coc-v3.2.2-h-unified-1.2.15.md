# Phase 3.6.4 — A Exact Review of Storage COC v3.2.2 / §14–17 and H Unified 1.2.15
# Phase 3.6.4 — A 对 Storage COC v3.2.2 / §14–17 与 H Unified 1.2.15 的精确审查

- Review date: 2026-11-18
- Reviewing role: A / COC integration — delegated role simulation under project-owner instruction, **not an independent human Owner signature**
- Storage COC protocol Blob: `5b950a3a29bd7a5276b92a49a9114d700718b987`
- H Unified 1.2.15 schema Blob: `860fc4cec658db7d2703cd6adf72aa31a2723f6d`
- H 1.2.15 dedicated structural tests Blob: `d8d09ec54a2cc95761c3670fb2a69e325caed5e9`
- H exact branch Head tested: `5c1e492825910370c5fe6afd7e239d94a01559ec`
- H Recovery Cutoff CI: [#44190526491](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44190526491) — SUCCESS, 306 tests

## 1. A review disposition

**ACCEPT AS ARCHITECTURE PROTOCOL WITH ENUMERATED OWNER / ENGINEERING CONDITIONS.**

The Storage COC v3.2.2 protocol §§14–17 is internally coherent as the architecture-level durable participant/recovery contract and aligns with the current H Unified 1.2.15 structural surface for the union manifest and dual-ledger snapshots. This is a design-level acceptance only. Gate B is not an implementation PASS, COC runtime conformance, production deployment or authorization to activate.

## 2. Exact cross-owner findings

### 2.1 Prepared-participant identity — §14

The protocol correctly keeps the following types distinct:
- stable engine-neutral `PreparedParticipantRef`;
- client-chosen PostgreSQL `PreparedTransactionGID`;
- engine-assigned `PostgreSQLNativeXID` observed only after PREPARE;
- canonical authority/database incarnation identity;
- attempt/generation and append-only participant ledger/version;
- complete immutable participant tuple digest.

The required order is sound: Storage durably allocates/binds the immutable tuple; COC quorum-commits and reads back exact prepare intent; only then may Storage issue PREPARE; Storage reads authoritative `pg_prepared_xacts`, observes native XID and persists the signed PreparedParticipantReceipt. Absence from `pg_prepared_xacts` alone is not terminal proof. UNKNOWN retains the participant and locks.

### 2.2 Recovery Cutoff ordering — §§15–17

The two-record order is preserved and explicit:
1. close affected I/D/C gates and freeze owner snapshots;
2. establish exact quorum-confirmed prefix P;
3. enumerate and precompute the complete manifest before batch append;
4. quorum-commit the Recovery Cutoff Batch binding the manifest content digest/count/high-water;
5. commit a separate Participant Manifest Record;
6. linearly read back and verify both exact records;
7. reconcile participants and obtain owner-local releases;
8. append RecoveryEpochCompleted only after all required releases and reconciliation root.

§17 correctly expands membership to the canonical union of (A) COC participants at/before P and (B) applicable owner-local I/D/C admissions through frozen admission high-water, including work not yet registered in COC. Request and admission ledgers are distinct; absence of a COC ref cannot erase an owner-local admission. The two member variants and typed membership proofs are explicit.

### 2.3 H schema mapping — current source pin

The current H schema artifact is revision **1.2.15**, wire version **1.3.0**. Its structural surface includes:
- COC_PARTICIPANT and OWNER_LOCAL_ADMISSION typed union;
- distinct request/admission high-waters, counts, digests and roots;
- I/D/C owner-specific high-water shapes;
- owner snapshot membership-proof fields;
- Batch/Manifest/RecoveryEpochCompleted cross-references and positions;
- C Provider Outcome final request boundary;
- typed JF-10 PreparedParticipant/GID/database-incarnation fields.

The dedicated test file adds 18 exact structural checks; the full H Recovery Cutoff suite passed 306 tests on the exact H branch code Head. This is structural/reference candidate evidence, not production semantic or crypto proof.

**Documentation drift:** Storage §17.5 still names H unified schema 1.2.5, while the exact current H artifact is 1.2.15 / wire 1.3.0. Storage Owner should append a superseding pin and explicitly state that 1.2.5 is historical. Do not treat the stale §17.5 pin as the current H wire artifact.

### 2.4 Authority and failure boundaries

- COC orders and accounts for participants; it does not issue I authorization, D fence clearance, Storage visibility, C provider outcome or G Applied.
- C alone proves provider handoff/side-effect outcome. COC membership, Storage COMMITTED, I terminality, D clearance or H ACK cannot synthesize C success.
- I owns PolicyDomain sequencing, COMMIT_WON/REVOCATION_WON and receipt/key/revocation/anti-rollback semantics.
- D owns producer eligibility, dependency/lineage, ForgetFence ordering and PublicationParticipant terminality.
- Storage alone owns database GID/XID, prepared participant, physical visibility and durable outcome.
- One I PolicyDomain only. Multi-PolicyDomain atomicity remains BLOCKED.
- Three-voter/two-quorum is a target topology. RPO 0 is bounded to quorum-acknowledged entries in the stated one-voter crash-fault model; correlated majority loss requires external checkpoint recovery or RESTORE_FENCED.

## 3. Remaining gates

- Gate A remains PARTIAL PASS / OPEN: five PostgreSQL 18.7 CI evidence classes exist, but the project-designated canonical authority runtime/database adapter, WAL-archive PITR, old-primary fencing/rejoin, sync-standby-unavailable fail-closed behavior, real host/zone/storage placement and human on-call remain unverified.
- Gate B remains BLOCKED: no selected/deployed persistent COC consensus runtime, voter topology, durable participant registry, production prefix/checkpoint custody, live owner-ledger adapters or production quorum restart/restore evidence.
- Gate C remains BLOCKED: no end-to-end fault-injection suite on the selected deployed Storage+COC stack.
- H 1.2.15 structural tests do not replace semantic cross-owner validators, canonical bytes, signature/key lifecycle or real quorum/owner snapshot proof verification.
- D/E/I/Storage independent human Owner acceptance and production engineering ownership remain outstanding.

## 4. Final A status

- Storage COC §§14–17 architecture: **ACCEPT WITH ENUMERATED CONDITIONS**.
- H Unified 1.2.15 structural schema surface: **PASS 18/18 dedicated checks**.
- H Recovery Cutoff candidate suite: **PASS 306 tests**.
- Gate A: **PARTIAL PASS / OPEN**.
- Gate B persistent COC: **BLOCKED**.
- Gate C physical fault injection: **BLOCKED**.
- Production JF-10 / Global Forget / multi-domain atomicity: **NOT AUTHORIZED**.

---

## 中文完整审查结论

本审查由协调会话按项目 Owner 指示模拟 A/COC Integration 角色完成，**不是独立人类 Owner 签名**。

### 1. A 审查处置

**作为带明确 Owner/Engineering 条件的架构协议予以接受。**

Storage COC v3.2.2 §§14–17 作为架构层持久 Participant/Recovery Contract 内部一致，并与当前 H Unified 1.2.15 的 Union Manifest 和双账本 Snapshot 结构表面对齐。这只是设计层接受，不是 Gate B 实现 PASS、COC Runtime Conformance、生产部署或激活授权。

### 2. 精确跨 Owner 结论

**§14 Prepared Participant Identity：** 正确区分稳定的 `PreparedParticipantRef`、客户端选择的 PostgreSQL `PreparedTransactionGID`、仅在 PREPARE 后由引擎观察的 `PostgreSQLNativeXID`、Canonical Authority/Database Incarnation、Attempt/Generation、Append-only Participant Ledger/Version 和完整 Tuple Digest。顺序正确：Storage 先持久化绑定；COC Quorum Commit 并 Read Back 精确 Prepare Intent；之后才允许 PREPARE；Storage 再从权威 `pg_prepared_xacts` 观察 Native XID 并持久化签名 Receipt。仅凭 `pg_prepared_xacts` 中不存在不能证明终态；UNKNOWN 必须保留 Participant 和 Locks。

**§§15–17 Recovery Cutoff 顺序：** 明确保留两条记录顺序：关闭 I/D/C Gate 并冻结 Snapshot；建立精确 Quorum Prefix P；Batch Append 前完成 Manifest 枚举/预计算；提交绑定 Manifest Digest/Count/High-water 的 Recovery Cutoff Batch；单独提交 Participant Manifest Record；线性 Read Back 并验证两条记录；执行 Participant Reconciliation 和 Owner-local Release；全部 Release 与 Reconciliation Root 完成后才追加 RecoveryEpochCompleted。

§17 正确将成员扩展为两类规范 Union：(A) P 之前 COC Participant；(B) 冻结 Admission High-water 内适用的 I/D/C Owner-local Admission，包括尚未注册进 COC 的工作。Request Ledger 与 Admission Ledger 分离；缺少 COC Ref 不得抹掉 Owner-local Admission；两种 Member Variant 和 Typed Membership Proof 均已明确。

**H Schema Mapping：** 当前 H Schema Artifact 为 Revision **1.2.15**，Wire Version **1.3.0**。结构包含 COC_PARTICIPANT/OWNER_LOCAL_ADMISSION Typed Union、独立 Request/Admission High-water/Count/Digest/Root、I/D/C Owner-specific High-water、Owner Snapshot Membership Proof、Batch/Manifest/RecoveryEpochCompleted 交叉引用与位置、C Provider Outcome Final Request Boundary，以及类型化 JF-10 PreparedParticipant/GID/Database Incarnation 字段。

新增的专用测试文件包含 18 项精确结构检查；完整 H Recovery Cutoff 套件在精确 H 分支代码 Head 上 306 项通过。这仍是结构/参考候选证据，不是生产 Semantic 或 Crypto Proof。

**文档漂移：** Storage §17.5 仍引用 H Unified Schema 1.2.5，而当前精确 H Artifact 已为 1.2.15 / Wire 1.3.0。Storage Owner 应追加 Superseding Pin，并明确 1.2.5 仅为历史版本。不得把旧 §17.5 Pin 当作当前 H Wire Artifact。

**Authority 边界：** COC 只负责排序和 Participant Accounting，不签发 I Authorization、D Fence Clearance、Storage Visibility、C Provider Outcome 或 G Applied。C 独占 Provider Handoff/Side-effect Outcome；COC Membership、Storage COMMITTED、I Terminality、D Clearance 或 H ACK 均不能伪造 C Success。I/D/Storage 各自保留其授权、Fence、数据库 GID/XID 和 Visibility 权威。只允许一个 I PolicyDomain；多域原子性仍 BLOCKED。三投票节点/两票 Quorum 是目标拓扑；RPO 0 仅适用于所述单节点崩溃模型下已确认的 Quorum Entry，相关多数派同时丢失时必须外部 Checkpoint Recovery 或 RESTORE_FENCED。

### 3. 剩余 Gate

- Gate A：PARTIAL PASS / OPEN。已有五类 PostgreSQL 18.7 CI 证据，但项目指定的 Canonical Authority Runtime/DB Adapter、WAL-archive PITR、旧 Primary Fencing/Rejoin、同步 Standby 不可用时 Fail-closed、真实 Host/Zone/Storage Placement 和人类 On-call 仍未验证。
- Gate B：BLOCKED。尚无选定/部署的持久 COC Consensus Runtime、Voter Topology、Durable Participant Registry、生产 Prefix/Checkpoint Custody、实时 Owner Ledger Adapter 或生产 Quorum Restart/Restore 证据。
- Gate C：BLOCKED。尚无在选定部署 Storage+COC Stack 上运行的端到端 Fault Injection Suite。
- H 1.2.15 结构测试不能替代 Semantic Cross-owner Validator、Canonical Bytes、Signature/Key Lifecycle 或真实 Quorum/Owner Snapshot Proof 验证。
- D/E/I/Storage 独立人类 Owner 验收和生产工程责任人仍待落实。

### 4. A 最终状态

- Storage COC §§14–17 架构：**带明确条件接受**。
- H Unified 1.2.15 结构表面：**专用检查 18/18 PASS**。
- H Recovery Cutoff 候选套件：**306 项 PASS**。
- Gate A：**PARTIAL PASS / OPEN**。
- Gate B Persistent COC：**BLOCKED**。
- Gate C 物理 Fault Injection：**BLOCKED**。
- 生产 JF-10 / Global Forget / 多域原子性：**NOT AUTHORIZED**。


## 5. Append-only currentness correction — H Unified 1.2.16

The later H exact-source reconciliation found that 1.2.15 did not explicitly carry four categories required by Storage §17.1: owner scope generation, I PermissionEpoch distinct from ProducerDomainInventoryEpoch, D dependency-closure cursor/root, and C provider idempotency namespace/final-request-boundary generation.

H has published schema artifact revision **1.2.16** (wire version 1.3.0), Blob `3ed43c4d0d067d4db98a2fa94f4d232280b4bbf5`, with dedicated test Blob `70e1169cc05295f18cde95ce8e66a0498bc74902`. Exact H Head `5545f45fb78af385c72269a0cb850980b7570cd7` passed run [#44191375797](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44191375797): **317 tests**, including 11 dedicated 1.2.16 checks.

Storage Owner appended §19 (Storage protocol Blob `1f8fac86886dc28f2d7727de430ee8a24473e1d0`) to supersede §18's 1.2.15 pin. The earlier 1.2.15 finding above is historical; current A review should use 1.2.16. This improves structural completeness only; live I/D/C ledger issuance/signing, H semantic validation, COC quorum and physical JF-10 remain open.

### 中文补充

后续 H 精确源码对照发现 1.2.15 未显式携带 Storage §17.1 要求的四类字段：Owner Scope Generation、独立于 ProducerDomainInventoryEpoch 的 I PermissionEpoch、D Dependency-closure Cursor/Root，以及 C Provider Idempotency Namespace/Final-request-boundary Generation。

H 已发布 Schema Artifact Revision **1.2.16**（Wire Version 1.3.0），Blob `3ed43c4d0d067d4db98a2fa94f4d232280b4bbf5`，专用测试 Blob `70e1169cc05295f18cde95ce8e66a0498bc74902`。H 精确 Head `5545f45fb78af385c72269a0cb850980b7570cd7` 在 Run [#44191375797](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44191375797) 中 **317 项通过**，其中包括 11 项 1.2.16 专用检查。

Storage Owner 已追加 §19（Storage Protocol Blob `1f8fac86886dc28f2d7727de430ee8a24473e1d0`），取代 §18 的 1.2.15 Pin。上文关于 1.2.15 的发现现为历史记录；当前 A 审查应使用 1.2.16。这只提高结构完整性，不关闭实时 I/D/C Ledger 签发/签名、H Semantic Validation、COC Quorum 或物理 JF-10。
