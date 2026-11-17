# OWNER-REMEDIATION-001 — Multi-Owner Technical Reality Remediation
# 多 Owner 技术现实性联合整改

- Date: 2026-11-18
- Repository: `oahcom/AiMemoryBrainArchitecture`
- Remediation base: `b3c666e67982cb3d3374e759cfb6552c7765aacb`
- Historical research target: PR #45, base `b372b62c640a2b656e54b6db62a4ee67d7d8c001`, head `6c7c5919c1b50f38c4d24be679a3885ee3c15b97`
- Mode: role simulation, evidence integration and remediation; this document is not a real Owner signature or approval.
- Verdict: **REVISE / NOT YET PROVEN / ARCHITECTURE FREEZE NOT READY**.

## 1. Remediation governance / 整改治理

This work treats the prior research package as a historical snapshot and refreshes its evidence against current Owner proposals. Domain authority remains with the named Owner. The simulated roles may clarify, reconcile and document contracts, but cannot create an Owner approval, freeze an ADR, attest production implementation, or waive a Gate.

本整改将原研究包视为历史快照，并基于当前 Owner 提案刷新证据。领域决策权仍属于对应 Owner。模拟角色可以澄清、对齐和记录契约，但不能制造 Owner 批准、冻结 ADR、证明生产实现或豁免 Gate。

## 2. Owner D — Memory Brain / ForgetFence

**Exact source:** branch `session-d-memory-brain-2026-11-16`; `03-memory-brain/phase-3.8-d-publication-participant-and-terminal-contract.md`; Blob `17e53890dd6cce9bea9eacc1be2e64b0ef55ac78`.

**Status:** D-role proposal; exact Owner approval, callable API and conformance remain OPEN.

D owns ProducerClass eligibility, ProducerWork admission, RegistrationReceipt and ProducerRegistrationSequence, ForgetFence ordering, complete dependency/lineage inventory, PublicationParticipantRef, and producer/publication terminality. D does not own I authorization, Storage persistence/visibility, E queue/lease execution, H wire encoding, or C provider-side intent. A D receipt is not a Storage write capability.

**Required closure work:** define exact callable APIs and durable linearization points; prove both serial orders of RegisterProducerWork vs InstallForgetFence; prove complete direct/transitive dependency registration; bind PublicationParticipant admission to the current fence and exact hidden Storage participant; prove idempotent replay/lost-ACK resolution; prove terminal closeout only after the authoritative Storage outcome; keep UNKNOWN private and barrier-held. No proof is claimed by this role simulation.

**中文：** D 负责 ProducerClass 准入、ProducerWork 注册、RegistrationReceipt/Sequence、ForgetFence 顺序、完整依赖/血缘清单、PublicationParticipantRef，以及生产者/发布终态。D 不负责 I 授权、Storage 持久化/可见性、E 队列/租约执行、H 编码或 C Provider 侧意图。D Receipt 不是 Storage 写入能力。必须补齐精确可调用 API 和持久化线性化点，验证 RegisterProducerWork 与 InstallForgetFence 两种串行顺序、完整传递依赖、当前 Fence 绑定、隐藏 Storage Participant 绑定、丢 ACK 幂等恢复，以及仅在 Storage 权威结果后关闭。UNKNOWN 必须继续私有并持有 Barrier。以上尚无符合性证明。

## 3. Owner E — Memory Compiler

**Exact source:** branch `session-e-memory-compiler-2026-11-16`; `04-memory-compiler/phase-3.8-e-publication-orchestration-retry-recovery-contract.md`; Blob `475fee41e5eea527af4edefbfe88c58c86967d0a`.

**Status:** E-role proposal; exact D/I/Storage APIs and independent Owner approval remain OPEN.

E owns CompileIntent, compiler ingress receipt, immutable compiler input bundle, DerivationRun, Attempt/Lease lifecycle, private staging, complete output/dependency submission and compiler-side recovery orchestration. E does not mint D eligibility/registration/participant, I authorization, Storage visibility outcome or global Forget terminality. Queue ACK, E AcceptedReceipt, local Published/Completed labels and object-store existence are not cross-owner proof.

**Required closure work:** durable ingress before queue/lease/protected dereference/execution; immutable request/run/attempt identities; lease fencing; complete dependency set; private output staging; stable operation identity across retry/lost ACK; crash/recovery and UNKNOWN behavior; prove no compiler side effect can bypass required D admission. No execution proof is claimed.

**中文：** E 负责 CompileIntent、入口 Receipt、不可变编译输入、DerivationRun、Attempt/Lease 生命周期、私有 Stage、完整输出/依赖提交和编译恢复编排。E 不签发 D 准入、I 授权、Storage 可见性或全局 Forget 终态。Queue ACK、AcceptedReceipt、本地 Published/Completed 标签和对象存储存在性都不是跨 Owner 证明。必须验证执行前持久化入口、不可变身份、Lease Fencing、完整依赖、私有 Stage、重试身份稳定、崩溃恢复及 UNKNOWN 行为，并证明不能绕过 D 准入。当前不声称已有运行证据。

## 4. Owner I — Security, Identity and Governance

**Exact source:** branch `session-i-security-governance-2026-11-16`; `09-security-governance/phase-3.8-i-commit-authorization-receipt-and-revocation-sequencer-contract.md`; Blob `54bab0484bd232a5a258e65e34cc7425288b39a6`.

**Status:** I-role proposal; exact Owner approval, crypto profile and conformance remain OPEN.

I owns authenticated principal/workload/delegation trust, PolicyDomain, current authorization, PermissionEpoch, revocation ordering, issuer/key status and authorization terminal proof. I authorization is necessary but never sufficient for visibility. D's current publication participant/fence and Storage's exact durable participant/outcome remain independent conjunctive requirements.

I crypto candidate `AIMBA-I-CRYPTO-1.0`, Blob `5eeb011032c53c2f7897d699d6f512b26f07d0a2`, is candidate evidence only, not production key custody or trust approval. Test-only private seeds are not production keys.

**Required closure work:** approved trust/key lifecycle; issuer/key status and revocation ordering; anti-rollback and restore behavior; exact CommitAuthorizationProof binding; historical verification; production HSM/KMS or an explicitly accepted alternative; negative/race tests. No production cryptographic proof is claimed.

**中文：** I 负责 Principal/Workload/Delegation 信任、PolicyDomain、当前授权、PermissionEpoch、撤销顺序、Issuer/Key 状态和授权终态证明。I 授权不是可见性的充分条件；D 当前 Participant/Fence 与 Storage 精确持久化 Participant/Outcome 仍须同时成立。I Crypto 候选 `AIMBA-I-CRYPTO-1.0` 仅为候选证据，不是生产密钥托管或信任批准；测试私钥不是生产密钥。必须补齐信任/密钥生命周期、Issuer/Key 状态、撤销顺序、Anti-rollback、Restore、CommitAuthorizationProof 绑定、历史验证、生产 HSM/KMS 或明确接受的替代方案及负向/竞争测试。当前不声称生产密码学证明。

## 5. Owner Storage — Consistency and Forget Atomicity

**Exact logical contract:** branch `session-storage-consistency-forget-atomicity-2026-11-16`; `reviews/storage-consistency/phase-3.8-storage-visibility-participant-and-atomic-outcome-contract.md`; Blob `175ee7b1349cfdb79a19898b311a88391ed88010`.

**Exact ADR:** same branch; `reviews/storage-consistency/phase-3.8.2-storage-serialization-topology-adr.md`; Blob `bb544ba2f346bdc130d524bd5c7310d86f367988`.

**Status: L1 logical serialization profile Option A SELECTED; L4 physical engine/deployment OPEN.** This is not the research package's deployment Option A. L1 means one logical Serializable Transaction Domain per Canonical Memory authority. It does not select PostgreSQL/SQLite, physical adapter, HA, deployment or operator. T1–T8 remain OPEN. D and Storage semantic authorities remain distinct; I PolicyDomain sequencer and COC quorum log remain separate; no XA or cross-log atomicity claim is made.

**Required closure work:** final serializable transaction validates exact D proof and pre-commit I COMMIT_WON proof; visibility pointer, outcome, PublicationReceipt and outbox commit atomically; exact hidden Storage participant is durable; transaction/incarnation identity is bound; test both serial orders, crash windows, failover, restore, anti-rollback and JF-10 physical bridge. L4 remains unselected and no physical conformance is claimed.

**中文：** Storage ADR 明确为 **L1 逻辑序列化配置选择 Option A；L4 物理引擎/部署 OPEN**。L1 表示每个 Canonical Memory Authority 一个逻辑 Serializable Transaction Domain；不等于选择 PostgreSQL/SQLite、物理 Adapter、HA、部署或运维负责人。T1–T8 仍 OPEN。D 与 Storage 语义权威分离；I PolicyDomain Sequencer 与 COC Quorum Log 分离；不声称 XA 或跨日志原子性。必须证明最终 Serializable Transaction 验证精确 D Proof 和提交前 I COMMIT_WON Proof，并原子提交 Visibility Pointer/Outcome/PublicationReceipt/Outbox；还须验证隐藏 Participant 持久化、事务/实例身份、两种串行顺序、崩溃窗口、Failover、Restore、Anti-rollback 和 JF-10 物理桥接。L4 未选择，不声称物理符合性。

## 6. Cross-owner publication sequence / 跨 Owner 发布顺序

The current Phase 3.8 proposals describe this logical sequence:

1. E persists ingress and obtains D durable ProducerWork registration before queue/lease/protected dereference/execution.
2. E freezes immutable compiler input and privately stages output.
3. D registers the complete direct/transitive dependency set.
4. Storage durably creates the exact hidden `StorageVisibilityParticipantRef`.
5. D admits `PublicationParticipantRef` bound to that exact Storage participant.
6. I consumes a single-use CommitAuthorization operation in its own PolicyDomain sequencer, bound to both exact participant refs.
7. Storage final serializable transaction validates exact D proof and pre-commit I `COMMIT_WON` proof, then atomically commits visibility pointer, outcome, PublicationReceipt and outbox.
8. D and I independently close only after the same authoritative Storage outcome; UNKNOWN remains private/unresolved.

Pre-commit I `CommitAuthorizationProof` is distinct from post-commit `ITerminalProof`; the latter is for I closeout after Storage's authoritative result and is not a Storage commit precondition. This remains a proposal sequence, not a frozen API or implemented protocol.

**中文：** 当前 Phase 3.8 提案描述的逻辑顺序为：E 先持久化入口并取得 D ProducerWork 注册；E 冻结不可变输入并私有 Stage；D 注册完整依赖；Storage 持久化隐藏 Participant；D 准入绑定该 Participant 的 PublicationParticipant；I 在自己的 PolicyDomain Sequencer 中单次消费并绑定两个 Participant；Storage 最终 Serializable Transaction 验证 D Proof 与提交前 I COMMIT_WON Proof，再原子提交 Visibility/Outcome/Receipt/Outbox；D/I 仅在同一 Storage 权威结果后分别关闭，UNKNOWN 保持私有未解决。提交前 CommitAuthorizationProof 与提交后 ITerminalProof 不同；后者用于 Storage 结果后的 I 关闭，不是 Storage 提交前置条件。此顺序仍为提案，不是冻结 API 或已实现协议。

## 7. Owner C / G / H — Applied and protocol status

- H wire mapping Blob `b132e6a01bcfe13f92020b9778ee3f7ddbf65753` is candidate evidence.
- H Unified COC/JF-10 schema 1.2.8 Blob `70b892797d07489936300a26c0dedfafe1d6e746`; RecoveryJoin schema 1.0.1 Blob `f94e01cf30b4c59fca24cb4ccd8b76a0db8ca95c`.
- H candidate CI run `44043259259`: 97/97 PASS, structural/reference-model scope only. Later run `44044062849`: 101 candidate tests PASS, including four Python/Node JCS/Ed25519 differential tests. Neither is production wire/crypto, real COC/Owner adapter or Brain end-to-end conformance.
- I exact R3 review of H mapping Blob `93afe9c9e06d20de5ce1c2a0f676b4785123fbcf`: ACCEPT WITH ENUMERATED AMENDMENTS; not approval of I crypto profile.
- C provider-side-effect review Blob `a7b57bd5531222559666f0f1d9df59a259cde61a` is review evidence only. Live Owner Ledger adapters, provider fault/race evidence and C/G/H final-request Applied end-to-end proof remain OPEN.
- Issue #3 remains Applied Contract Frozen = NO; Test Executed/Passed = NO/NO; Implementation Verified = NO. H 1.2.13 exact CI remains OPEN.

**中文：** H Wire Mapping、Unified COC/JF-10 1.2.8、RecoveryJoin 1.0.1 和 97/97、101 项 CI 均为有限范围的候选证据，不等于生产 Wire/Crypto、真实 COC/Owner Adapter 或 Brain 端到端符合性。I 对 H Mapping 的 R3 结论是 ACCEPT WITH ENUMERATED AMENDMENTS，不是批准 I Crypto。C Provider Side-effect 复审只是审查证据；真实 Owner Ledger Adapter、Provider Fault/Race 及 C/G/H Final-request Applied 端到端证明仍 OPEN。Issue #3 仍是 Applied Contract Frozen = NO、Test Executed/Passed = NO/NO、Implementation Verified = NO；H 1.2.13 精确 CI 仍 OPEN。

## 8. License remediation — Restate Server / 许可证整改

The canonical Restate Server repository LICENSE is Business Source License 1.1 (BSL 1.1) with an Additional Use Grant; repository API metadata `NOASSERTION` is insufficient. The grant permits internal deployments and own-organization production workflows, while restricting a “Public Restate Platform Service” that exposes Restate APIs to third parties who register their own deployments and invoke through a managed service. Change License is Apache 2.0 on the stated Change Date (four years after release). The separate Restate Rust SDK MIT license does not replace the Server license. Server and SDK must be separate evidence rows. Legal review is required if Brain is offered as a public managed platform to third-party developers. Do not generalize this into a ban on all third-party managed services.

**中文：** Restate Server 规范 LICENSE 是带 Additional Use Grant 的 BSL 1.1；仅记录仓库 API 元数据 NOASSERTION 不充分。Grant 允许内部部署和本组织生产工作流，但限制向第三方提供可注册自有部署并通过托管服务调用 Restate API 的“Public Restate Platform Service”。Change License 在指定 Change Date（发布四年后）为 Apache 2.0。独立 Restate Rust SDK 的 MIT 许可证不能替代 Server 许可证。Server 与 SDK 必须分开登记；若 Brain 面向第三方开发者提供公共托管平台，需要法律审查。不得泛化为禁止所有第三方托管服务。

## 9. Remaining blockers and exact acceptance conditions / 剩余阻塞与验收条件

| ID | Workstream | Current status | Required closure evidence |
|---|---|---|---|
| R-01 | Research currentness | Historical baseline preserved; Phase 3.8 source delta added here | Owner source refresh at each review; exact base/head/Blob pins |
| R-02 | D/E/I/Storage contract | Role proposals only | Explicit Owner approval, stable API/schema, executable cross-owner conformance |
| R-03 | Storage topology | L1 Option A selected; L4 OPEN | Approved physical engine/deployment ADR and JF-10 physical evidence |
| R-04 | H protocol/crypto | Candidate schemas and bounded CI | H 1.2.13 exact CI, production trust/key custody and real adapter conformance |
| R-05 | C/G/H Applied | NOT FROZEN / NOT TESTED / NOT VERIFIED | Final inference-request evidence with lost ACK, stale delivery, reconnect, revocation and Forget races |
| R-06 | Restate license | BSL 1.1 disclosure required | Server/SDK split evidence and legal determination for intended distribution model |
| R-07 | B Fact/Claim | ADR-BLOCKED | B Owner-approved canonical types and persistence constraints |
| R-08 | Bilingual parity | Presence is not semantic parity | Line-by-line paired-section checklist and independent semantic review |
| R-09 | Research package integration | New current-source delta recorded | Matrix, recommendation, synthesis and evidence register updated from this addendum; independent reviewer re-read |
| R-10 | Feasibility | NOT YET PROVEN | Reproducible Brain vertical slice, workload benchmarks, fault injection, backup/restore and no-resurrection proof |

## 10. Explicit non-claims / 明确不作出的声明

No Brain prototype, benchmark, production deployment, production security audit, HSM/KMS integration, live Owner Ledger adapter test, C/G/H Applied end-to-end test, JF-10 physical conformance, or production activation is claimed. Candidate CI is not production proof. Role simulation is not a real Owner signature. No architecture freeze, Gate release, merge approval or deployment authorization is issued.

**中文：** 不声称已有 Brain 原型、Benchmark、生产部署、生产安全审计、HSM/KMS 集成、真实 Owner Ledger Adapter 测试、C/G/H Applied 端到端测试、JF-10 物理符合性或生产激活。候选 CI 不是生产证明。角色模拟不是真实 Owner 签名。不批准架构冻结、Gate 释放、合并或部署。


Canonical license source for independent re-fetch: https://github.com/restatedev/restate/blob/main/LICENSE . The Server license must be read from the Server repository root LICENSE at the reviewed commit; do not substitute repository API license metadata or the separate Rust SDK LICENSE. Legal interpretation for a proposed commercial distribution model remains outside this technical role simulation.


## 11. C/G/H Applied exact consumer review — 2026-11-18 / C/G/H Applied 精确消费者审查

A current-main review has been recorded in \`CGH-APPLIED-REVIEW-001.md\`. It pins C/G/H/I artifacts and identifies five closure items: H duplicate-key rejection (P0), H current-authorization recheck before replay result disclosure (P0), exact CSubmitOutcome 1.0.1 resolver/equality (P0), G's exact consumer decision for the separate H Applied Delivery Evidence 1.0.0 family (P1), and G durable Applied persistence/restore implementation (P0).

The H Applied Delivery Evidence 1.0.0 family is distinct from Unified 1.2.15 C Provider Outcome Gateway Attestation and JF-10 Applied ACK. C's Phase 3.8.27 corrected gateway ordering review does not approve this separate H family. C's Applied Delivery Evidence review accepts identity shape only as a candidate and leaves C outcome mapping NOT ACCEPTED / NOT VERIFIED. A-H-ADE-006 remains DEFERRED with H-ADE-001..003 open. G Phase 3.8.22 remains a normative design draft with conformance SPECIFIED / NOT RUN.

No source-owner contract was modified by this audit. Role simulation is not an Owner signature. Full Applied remains blocked and the overall verdict remains **REVISE / NOT YET PROVEN / ARCHITECTURE FREEZE NOT READY**.

**中文：** 本次 current-main 审查记录于 \`CGH-APPLIED-REVIEW-001.md\`，锁定 C/G/H/I 精确证据，并确定五项关闭条件：H 重复 JSON 键拒绝（P0）、Replay 结果披露前当前授权复核（P0）、CSubmitOutcome 1.0.1 精确 Resolver/Equality（P0）、G 对独立 H Applied Delivery Evidence 1.0.0 消息族的精确消费者决议（P1）、G Applied Durable Persistence/Restore 实现（P0）。

H Applied Delivery Evidence 1.0.0 与 Unified 1.2.15 C Provider Outcome Gateway Attestation、JF-10 Applied ACK 是不同消息族。C Phase 3.8.27 的 Gateway 顺序接受不等于批准该独立 H 消息族。C 对 Applied Delivery Evidence 仅接受身份结构作为候选，C Outcome Mapping 仍 NOT ACCEPTED / NOT VERIFIED。A-H-ADE-006 仍为 DEFERRED，H-ADE-001..003 未关闭。G Phase 3.8.22 仍是规范设计草案，一致性义务 SPECIFIED / NOT RUN。

本次审查没有修改任何 Owner 源契约。角色模拟不是 Owner 签名。Full Applied 仍阻塞，总体结论仍为 **REVISE / NOT YET PROVEN / ARCHITECTURE FREEZE NOT READY**。
