# Open Questions and Blockers / 未决问题与阻塞项

- Task: TECH-REALITY-001-A | Owner A | Date: 2026-11-17
- Status: **OPEN / BLOCKED ITEMS PRESERVED**

## 1. Critical architecture blockers / 关键架构阻塞

| ID | Question | Current evidence | Required owner | Blocks |
|---|---|---|---|---|
| OQ-01 | Which physical storage topology can prove canonical commit, cursor and Forget admission/publication semantics? | TAB-001 TEC-003 candidate; Issue #43/PR #44 says D/Storage serialization topology ADR-BLOCKED; Issue #25 open | Storage + D/E; A integrates | DB selection and implementation |
| OQ-02 | How are COC recovery-cutoff and JF-10 prepared-participant protocols bridged? | Issue #43/PR #44 explicitly says separate protocols; automatic composition not approved; JF-10 Gate B/C blocked | Storage/Consistency + A/I | Distributed transaction/recovery claims |
| OQ-03 | What is the exact linearization point for producer admission vs Forget fence installation? | TAB-001 §9 OPEN critical; Issue #25 | D/E/Storage | Forget safety |
| OQ-04 | What is the exact atomic/linearizable dependency-registration and final publication gate? | TAB-001 §9 OPEN critical; Issue #25 | D/E/Storage | Anti-resurrection |
| OQ-05 | What is the full Applied proof chain at final inference request? | Issue #3 says Applied Contract Frozen = NO; PR #44 says chain not frozen | C/G/H (+ I/D) | Context sync and acceptance |
| OQ-06 | Which Fact/Claim representation is normative? | Issue #43/PR #44 preserves B Fact/Claim ADR-BLOCKED | B | Schema, serialization, indexes |
| OQ-07 | What is the sealed Global Forget target inventory and cross-owner evidence vector? | Issues #4/#5; PR #44 says governance approvals remain blocked | I + D/E/F/G/H | Global Forget completion |
| OQ-08 | What identity and trust binding applies to producer/adapter/provider? | I-owned Principal/Actor/Scope and C/H contract dependencies remain open | I/B/C/H | Auth, audit, external egress |
| OQ-09 | What does Storage mean by transaction participant identity and physical participant topology? | Issue #10 JF-10 probe; Issue #43 says topology ADR blocked | Storage/Consistency | COC/JF-10 and recovery |
| OQ-10 | Which OS, hardware, corpus, concurrency and RPO/RTO are actual product requirements? | TAB-001 §11/§12 lists unknowns; no workload data | Product/Owner A/Release | Performance and topology selection |

## 2. Technology-specific open questions / 技术选型未决

1. SQLx or rusqlite for SQLite adapter? Which connection/worker model owns writes and transactions?
2. SQLite or PostgreSQL for the first executable prototype after Storage's physical topology decision?
3. Is a content-addressed filesystem adequate for the first target OS and backup threat model?
4. Does FTS5 meet Chinese/mixed-language recall quality, or is Tantivy required?
5. Is vector retrieval needed in the first vertical slice? If yes, which single candidate wins on filtered recall, updates/deletes and rebuild?
6. Does the compiler require a workflow engine beyond DB-backed leases/outbox? Which task durations and retry patterns prove that?
7. Is Cedar's entity/action/resource model compatible with I's policy semantics? Is an external relationship graph service needed?
8. Which BMCP transport/encoding is required by C's real Agent integration targets?
9. Which inference backend has compatible operators, GPU execution provider and packaging for the target device?
10. Which observability signals are stable and necessary in local deployment, given OTel Rust signal maturity differences?

## 3. Currentness and repository governance / 当前性与仓库治理

### PR #44 / Issue #43

At capture time PR #44 is open and draft. Its body states:
- NOT READY FOR ARCHITECTURE FREEZE.
- D/Storage serialization topology ADR-BLOCKED.
- C/H/D/I exact-version migration incomplete.
- Integrated publication and Forget/restore reference-model evidence incomplete.
- Full Applied chain not frozen.
- B Fact/Claim ADR blocked.
- COC and JF-10 are separate protocols; automatic composition is not approved; JF-10 Gate B/C remain blocked.

This research must remain complementary to PR #44 and must not be used to imply that its architecture freeze gates passed.

### PR #28

PR #28 is open and draft. Its current body explicitly says:
- The bilingual manifest scope is only the files included in that PR; it is not repository-wide completion.
- Detailed Owner source specifications and several C/G/H Applied and Storage/Consistency contract pairs remain incomplete.
- Structural CI is not semantic parity or architecture approval.
- H36 suites remain NOT RUN; Applied freeze remains BLOCKED; Storage topology remains ADR-BLOCKED; JF-10 remains P0 OPEN / NOT IMPLEMENTED / NOT RUN.

The new research files in this task are bilingual in a single paired artifact (Chinese and English sections). They do not translate or alter other Owners' contracts.

### PRs #31–#35

AI-RUN-003 runtime architecture and ADR chain is stacked, open and proposed. PR #35 says its logical data model is storage-neutral and no SQLite/PostgreSQL choice or production migration is claimed. Do not use this Owner Worker runtime as evidence that the product Memory Brain runtime has been implemented.

## 4. Evidence needed to close / 关闭所需证据

- Approved physical storage topology ADR with exact participant and recovery semantics.
- D/E/Storage operation contract and executable race tests in both serial orders.
- C/G/H final-request Applied conformance tests with lost ACK, stale delivery and reconnect.
- I approved identity/revocation/Forget target model and restore semantics.
- B approved Fact/Claim and typed-reference semantics.
- Reproducible storage, workflow, search and inference prototypes on declared hardware.
- Full DB + blob + index backup/restore with current Forget/revocation replay before serving.
- Independent review by the responsible Owners and a separate independent technology reviewer.


## 5. Current Owner branch drift and Storage ADR update / 当前 Owner 分支漂移与 Storage ADR 更新

The current Owner branch HEADs read directly on 2026-11-17 are newer than the exact branch pins recorded in PR #44's Phase 2 evidence ledger. The current heads are:
- B `8f83e4b172bc6bb41df60de58c1884886b22e617`
- C `667bbf84b89dc1a54ddc02852477a74083d2d89b`
- D `97e68fbd225bdf0ac71860c01077481afc162d50`
- E `fdb4f67a83083d995930b88f93975b5ee36080f3`
- F `8d5ef89ce9b1ff1471ffd1a03fe4f289addb0af3`
- G `f9ca0ddc36e17f74041506f17039f0202d13042e`
- H `f809be092a6c04db7982cc1bdbdd9c88787a4286`
- I `28df608b075e619563c6367a8a1c171185c1faaf`
- Storage `17be31915b06d98d7f822e6e5270b8cde39eb0bb`

PR #44's evidence ledger records earlier branch heads (B `0df144...`, C `fecd925...`, D `73bcfa...`, E `df3f56...`, F `348b5e...`, G `69ba55...`, H `c50809...`, I `80ecf0...`, Storage `ce07f5...`). Its Phase 2 report therefore requires a fresh exact-version/currentness refresh before it can be treated as a current cross-owner bundle.

A further important update: current Storage ADR Blob `1ef47d4e5711c7db73a24d249adf1992be1f6aa4` has a 2026-11-17 addendum selecting Storage-ADR Option A as the normative v1 **logical serialization profile**. This supersedes the older ADR text's "NO TOPOLOGY SELECTED" only at the abstract architecture level. Physical DB/deployment selection and Gate A–C remain open as specified in the dossier.

本次直接读取的 Owner 分支 HEAD 均比 PR #44 Phase 2 Evidence Ledger 记录的精确分支 Pin 更新。当前 HEAD 列表见上。PR #44 的 Evidence Ledger 仍记录较旧分支 HEAD，因此必须先刷新精确版本/当前性，才能将其视为当前跨 Owner 绑定清单。

另一个重要更新：当前 Storage ADR Blob `1ef47d4e5711c7db73a24d249adf1992be1f6aa4` 的 2026-11-17 补充条款选择 Storage-ADR Option A 作为 v1 规范**逻辑序列化档案**。该补充条款仅在抽象架构层面取代旧正文的“NO TOPOLOGY SELECTED”；物理数据库/部署选型以及 Gate A–C 仍按能力档案保持 OPEN。

## 6. 完整中文版本 / Chinese Version

### 6.1 关键架构阻塞

| ID | 问题 | 当前证据 | 责任 Owner | 阻塞 |
|---|---|---|---|---|
| OQ-01 | 哪种物理 Storage 拓扑能证明 Canonical Commit、Cursor、Forget Admission/Publication？ | TAB-001 候选；Storage 逻辑 v1 档案已选，但物理部署仍开放 | Storage+D/E | DB 选型/实现 |
| OQ-02 | COC Recovery Cutoff 与 JF-10 Prepared Participant 如何桥接？ | 两协议分离，自动组合未批准；Gate B/C 未关闭 | Storage/Consistency+A/I | 分布式事务/恢复 |
| OQ-03 | Producer Admission 与 Forget Fence 的精确线性化点？ | Issue #25 仍开放 | D/E/Storage | Forget 安全 |
| OQ-04 | Dependency Registration 与 Final Publication 的原子边界？ | Issue #25 仍开放 | D/E/Storage | 防复活 |
| OQ-05 | Final Inference Request 的 Applied 证明链是什么？ | Issue #3 Applied Contract Frozen = NO | C/G/H/I/D | Context Sync |
| OQ-06 | Fact/Claim 的规范表示是什么？ | B ADR-001 仍阻塞 | B | Schema/Protocol |
| OQ-07 | Global Forget Target Inventory 和证据向量如何封闭？ | Issues #4/#5；治理审批未通过 | I+D/E/F/G/H | Global Forget |
| OQ-08 | Producer/Adapter/Provider 的身份和信任绑定是什么？ | I/C/H 依赖仍开放 | I/B/C/H | Auth/Egress |
| OQ-09 | Storage 的 Participant Identity 和物理 Participant Topology 是什么？ | Issue #10 JF-10；拓扑 ADR 仍有物理 Gate | Storage | COC/JF-10 |
| OQ-10 | 真实 OS、硬件、语料、并发、RPO/RTO 是什么？ | TAB-001 未知 | Product/A/Release | 性能/拓扑 |

### 6.2 技术选型未决

1. SQLite Adapter 选 SQLx 还是 rusqlite？谁拥有写入和事务？
2. 在 Storage 物理拓扑要求下，首个原型用 SQLite 还是 PostgreSQL？
3. 内容寻址文件系统是否满足目标 OS 和备份威胁模型？
4. FTS5 是否满足中文/混合语言检索，还是需要 Tantivy？
5. 首个纵向切片是否真的需要向量检索？若需要，哪个单一候选在过滤 Recall、更新删除和重建上胜出？
6. Compiler 是否需要 DB Lease/Outbox 之外的 Workflow Engine？
7. Cedar 是否与 I Policy 语义一致？是否需要 OpenFGA/SpiceDB？
8. BMCP 对真实 Agent 的 Transport/Encoding 需求是什么？
9. 哪个推理后端在目标 GPU/算子/打包环境兼容？
10. OTel 哪些 Signal 稳定且本地部署确有必要？

### 6.3 PR 与当前性

PR #44 / Issue #43 当前集成结论为 NOT READY FOR ARCHITECTURE FREEZE。它指出 D/Storage 物理部署、C/H/D/I 精确版本、Publication/Forget/Recovery 参考模型、Fact/Claim、Applied/Provider Outcome 仍未闭合。当前 Owner 分支 HEAD 已比 PR #44 Phase 2 Evidence Ledger 中的 Pins 更新，必须刷新精确版本登记。

Storage ADR 最新补充条款选择一个逻辑 Serializable Transaction Domain/Canonical Authority 作为 v1 序列化架构，但不选择物理数据库或生产部署。PostgreSQL 18.7 CI 能力证据不能替代 D/I/COC 应用集成。

### 6.4 关闭所需证据

必须有批准的物理 Storage ADR、D/E/Storage 可执行竞争测试、C/G/H Final Applied Conformance、I 身份/撤销/Forget 清单、B Fact/Claim 决策、目标硬件原型、完整 DB+Blob+Index Backup/Restore、Owner 独立审查和独立技术审查。


## 7. Late status correction — 2026-11-17 / 最新状态校正

The earlier sections describe the initial PR #44 / Issue #43 and initial JF-10 evidence snapshot. The following exact current Storage artifacts were fetched after those snapshots and control the technical evidence described here:

- Storage v3.2.6 successor manifest Blob `dbfa37617d109d5891a067769e858085e2ce547a`.
- Normative Storage v3.2.3 body Blob `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792`.
- PostgreSQL 18.7 dossier Blob `0aabf66848dc97deee028c571183c0d7204008c0`.
- Deployment readiness Blob `ef4eff1708e4bd6072b86cc234340dd848bb5fbc`.

### 7.1 Corrected status vector / 校正后的状态向量

| Concern | Current evidence | Status |
|---|---|---|
| Logical serialization profile | Storage readiness selects one authority-local serializable transaction/lock domain; does not select production DB topology | Logical profile selected; production binding deferred |
| PostgreSQL 18.7 engine capability | Seven pinned isolated CI subtests pass, including prepared-XID recovery, standby promotion, restore fixture, ACK-loss and PITR cases | PARTIAL PASS / OPEN |
| Storage/JF-10 exact successor | v3.2.6 manifest binds H 1.2.13/C 1.0.1 successor sources | Bound; not jointly frozen |
| C candidate | CSubmitOutcome 1.0.1 candidate CI 19 tests success | Candidate evidence only |
| H exact version | H 1.2.13 has 15-test source; exact-head CI not run | OPEN |
| D lineage / release | Exact structural carrier review exists; lineage completeness, late-discovery and release CAS not proven | OPEN |
| I authorization / trust | I P0 structural candidate accepted; L3 vectors, trust/key lifecycle and anti-rollback remain open | OPEN |
| JF-10 Gate A | Isolated PostgreSQL capability evidence exists; application/deployment binding deferred | PARTIAL PASS / OPEN |
| JF-10 Gate B | Design protocol acceptance with enumerated exceptions; v3.2.6 not jointly frozen | Design-level only |
| JF-10 Gate C | End-to-end distributed fault campaign deferred to engineering | NOT RUN |
| Runtime P0 / production | No live Brain runtime integration or production activation | OPEN / NOT AUTHORIZED |

### 7.2 Questions that remain blocking / 仍然阻塞的问题

1. Complete exact Owner review and freeze of Storage v3.2.6 successor bundle, including H 1.2.13 exact CI and any amendments; changed Blob requires new review.
2. Complete I L3 family vectors, production trust/key registration, signer/audience/revocation/anti-rollback and policy-domain controls.
3. Complete D lineage enumeration, late-discovery handling and final barrier-release CAS evidence.
4. Complete C provider-specific idempotency, same-key outcome lookup, UNKNOWN/IN_DOUBT recovery and final side-effect boundary.
5. Implement bidirectional COC participant ↔ I/D/C admission join and same-GID RecoveryJoin in the designated runtime during engineering phase.
6. Run deterministic end-to-end race/crash/restart/partition/restore/failover tests with exact schema, database, COC and adapter binaries/configuration.
7. Designate production host/failure domains, durable media, KMS/HSM custody, backup retention, human operator/on-call, runbook, monitoring, RPO/RTO and restore rehearsal before production activation.
8. Keep multi-PolicyDomain atomicity BLOCKED until a separate approved protocol and proof exist.

### 7.3 What this research does not authorize / 本研究不授权事项

- No production implementation or deployment is authorized by this research PR.
- No technology recommendation is promoted to DECIDED.
- No JF-10 P0 closure, Gate B/C implementation PASS, Global Forget completion, production activation or architecture freeze is claimed.
- The independent technology review must be performed by a different session and must independently re-fetch the exact source bundle.

前文记录了 PR #44 / Issue #43 的初始状态和初始 JF-10 证据快照。以上四个精确 Storage 工件是之后直接读回的当前证据，应用于校正旧快照。当前逻辑序列化档案已选择，但生产 DB 拓扑未选；PostgreSQL 18.7 七项隔离 CI 子测试 PASS，Gate A 仍 PARTIAL PASS / OPEN；v3.2.6 Bundle 已绑定但未联合冻结；C 候选 19 项测试成功，H 1.2.13 精确 CI 未运行；D Lineage/Release 和 I L3/信任仍 OPEN；Gate B 仅设计级接受，Gate C NOT RUN；JF-10 Runtime P0 OPEN，生产激活未授权，多 PolicyDomain BLOCKED。

## 6. Updated owner closure questions / 更新后的 Owner 关闭问题

1. D: What are the exact callable APIs and durable linearization points for ProducerWork admission, ForgetFence, complete dependency registration and PublicationParticipant admission? Where are both serial-order race tests?
2. E: What executable evidence proves durable ingress-before-execution, immutable run/attempt identity, lease fencing, private staging and retry/lost-ACK recovery?
3. I: Who approves the crypto profile, production trust/key custody, issuer/key status, revocation ordering, historical verification and anti-rollback/restore model?
4. Storage: Which physical engine/deployment realizes L1 Option A? Where is the L4/JF-10 physical proof, HA/failover/restore and UNKNOWN barrier evidence?
5. C/G/H: Where is the frozen final-request Applied contract and end-to-end evidence for lost ACK, stale delivery, reconnect, provider side effects, Forget and revocation races?
6. B: When is Fact/Claim ADR no longer ADR-BLOCKED, and which canonical type/identity constraints can be frozen?
7. License: What is the intended Restate Server distribution/use model, and has BSL 1.1 Additional Use Grant been reviewed for it?
8. Parity: Where is the line-by-line English/Chinese semantic parity checklist and independent review?

Until evidence is attached, these remain OPEN. See [OWNER-REMEDIATION-001](owner-remediation/OWNER-REMEDIATION-001.md).

**中文：** 以上问题分别要求 D/E/I/Storage/C/G/H/B 提供精确 API、可执行竞争/恢复测试、生产密钥与撤销证据、L4/JF-10 物理证明、Final-request Applied 端到端证明、Fact/Claim 决策、BSL 使用模式法律审查和逐行双语语义一致性审计。在证据提交前均保持 OPEN。
