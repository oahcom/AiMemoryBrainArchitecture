---
document_metadata:
  domain: memory-compiler
  role: design-specification
  steward: USER-PRINCIPAL-DELEGATED
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: git
        value: null
      approval_scope:
        type: Full-document
      approval_applicability: Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "从 Owner 源分支恢复；Owner 接受仍待定。"
    usage_status: Active
    modification_status: Unchanged
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
        archived_date: null
        archival_reason: null
        archival_reference: null
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "E 域 Memory Compiler 记录 phase-3.8.2-e-recovery-join-orchestration-exact-review.md；规范归属位置待 Owner 接受后确定。"
    canonical_scope_id: "memory-compiler/e-phase-3-8-2-e-recovery-join-orchestration-exact-review"
    canonical_scope_keywords:
      - memory-compiler
      - e-domain
      - phase-3-8-2-e-recovery-join-orchestration-exact-review
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---




# Phase 3.8.2 — E 精确审查：RecoveryJoin 编排与重试

- 审查视角：E — Memory Compiler
- 审查方式：**集成会话中的角色模拟；不是独立 E Owner 签署**
- 决策：**在列明修订条件下接受**
- 项目阶段：仅架构提案；实现/一致性尚未验证。

## 1. 精确审查目标

- D Phase 3.8 契约：Blob `17e53890dd6cce9bea9eacc1be2e64b0ef55ac78`。
- E Phase 3.8 契约：Blob `475fee41e5eea527af4edefbfe88c58c86967d0a`。
- I Phase 3.8 契约：Blob `54bab0484bd232a5a258e65e34cc7425288b39a6`。
- Storage Phase 3.8 契约：Blob `175ee7b1349cfdb79a19898b311a88391ed88010`。
- Storage RecoveryJoin 契约：Blob `41f80b1aacfebdb1f652b16144afbf83ce950e82`。
- H RecoveryJoin schema 候选：Blob `dd3234aa1c74caf6d0e335875cd96e0b2b64082f`。
- H 语义测试套件：Blob `60a2f4db4bd12f2131ecd147db9bbe328da6db50`。
- A 确定性一致性矩阵：Blob `c0f8ae699a42de46d12d0d311892e5670014e0f1`。

## 2. E 处置

Phase 3.8 编排顺序是连贯的：

Storage 持久化隐藏式 prepare → D 发布准入 → I 单次使用排序器消费 → Storage 最终可见性提交 → D/I 独立 closeout。

E 正确区分：
- 逻辑 ProducerWorkItemId 与 DerivationRunId、AttemptId/LeaseId/LeaseEpoch；
- 同一操作的传输重试/恢复，与权威 NO_PUBLICATION 之后的新发布尝试；
- 私有暂存制品与公开可见制品；
- 编译器本地结果与 D/I/Storage Owner 终态证据。

RecoveryJoin 不会创建新的编译器身份，也不能用于推断缺失的 D/I/Storage 回执。

## 3. 阻断性修订

### E-RJ-01 — Recovery Join 必须门控恢复和受保护派发

E 的 Phase 3.8 可见性流程没有明确规定：恢复后的编译器运行时必须保持不服务状态，直至精确的 RecoveryCutoffBatch、ParticipantManifest、RecoveryJoinProof、当前 I/D/C Owner releases 以及 D/I/Storage restore proofs 全部完成对账。E 必须在恢复后、队列派发、受保护源解引用、租约执行、重试重放或发布之前增加显式恢复门禁。

### E-RJ-02 — 请求行与准入行必须分开

E 不得把 Owner 请求折叠为准入，也不得把 COC ParticipantIntent 当作编译器 D RegistrationReceipt 已存在的证明。JoinProof 的 request-disposition 集合与 admission-to-participant 边是分开的。可能已经产生副作用的 NOT_REGISTERED 请求必须隔离，不能通过重放为其创建新身份。

### E-RJ-03 — JoinProof 之后的重试身份

同一不可变发布恢复必须保留 PublicationOperationId、tuple digest 和全部 Owner participant refs。权威 NO_PUBLICATION 后的新尝试使用新的发布/参与者身份，但保留逻辑 ProducerWorkItemId。编译器输入/源修订/依赖集合变化会创建新的 DerivationRun/输出身份，并要求重新执行 D/I 门禁。

### E-RJ-04 — 编译器本地状态不是 JoinProof 证据

队列 ACK、E AcceptedReceipt、私有对象存在、本地 Published/Completed 标签或过期 Lease，均不能填补 I/D/C Owner 证据边，也不能关闭 D ProducerWork。E 必须为每个 Run、Attempt、stage、dependency、publication 和 replay 路径提供精确的 inventory refs/digests。

## 4. E 必需测试

- JoinProof 缺失或过期时恢复：不得派发队列或解引用受保护源。
- 重复队列投递和过期租约不得改变参与者身份。
- COC participant 存在但缺少 D RegistrationReceipt：阻断。
- 可能产生副作用的 Owner 请求 NOT_REGISTERED：保持隔离。
- 同一发布操作 ACK 丢失：使用相同 ID/摘要解析。
- NO_PUBLICATION 后新尝试：使用新的 PublicationOperationId/participants。
- 编译器输入/依赖/源修订变化：新的 DerivationRun 和新门禁。
- RecoveryJoin 完成但 D/I/Storage terminal UNKNOWN：编译器仍保持不服务/私有。
- Outbox/DLQ/延迟发布器重放不得绕过已关闭的 Owner 门禁。

## 5. E 结论

**在列明修订条件下接受**。E-RJ-01..04 必须反映到 E 恢复/派发生命周期和确定性一致性矩阵中。不声称独立 E Owner 批准、编译器实现 PASS 或生产启用。

## 6. 中文结论

E 接受 Storage→D→I→Storage 的可见性编排，但要求 Restore 后先完成精确 RecoveryJoin 和 I/D/C Owner Release，再允许 Queue Dispatch、Protected Source Dereference、Lease Execution、Retry Replay 或 Publication。Request 与 Admission 必须分离；同一操作恢复沿用原 ID，NO_PUBLICATION 后的新尝试使用新 PublicationOperationId。E 本地状态不能替代 Owner Proof。

本文件是本集成会话中的 E 角色模拟审查，不是独立 Owner 签署。

## 7. H/Storage 后续工作

最新 RecoveryJoin schema 增加了显式 Owner request dispositions、逐行身份/摘要绑定，以及类型化 D/I/C/Storage 证据。这改善了 E 区分待处理请求与已准入工作、并对账精确恢复清单的能力。但它并未实现 E-RJ-01：E 仍需要运行时门禁，在精确 RecoveryJoin、当前 Owner releases 和恢复对账得到证明之前，阻止队列派发、受保护源解引用、租约执行、重试重放和发布。

更新后的 H RecoveryJoin schema Blob：`dd3234aa1c74caf6d0e335875cd96e0b2b64082f`。
更新后的 HRC suite Blob：`60a2f4db4bd12f2131ecd147db9bbe328da6db50`。

## 已验证的 H 候选 CI 结果

GitHub Actions run `44039990464`、job `133891944149` 检出 H commit `da94bcc1796cb350eed12845e49cbc3663faab9c`，并在 Ubuntu 26.04 / CPython 3.12.16 上成功完成 66/66 项候选测试。这仅代表已提交的 Python HRC/JPF/WIRE/SCHEMA 候选测试套件 PASS。它不证明生产签名、跨语言规范字节、真实 Owner/COC 适配器、物理 JF-10 行为或已部署 Storage 拓扑/HA/恢复。
