---
document_metadata:
  domain: memory-compiler
  role: design-specification
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
      last_verification_note: "从 Owner 源分支逐字节恢复；Owner 接受仍待定。"
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
    canonical_status: Canonical
    canonical_scope: "E 域 Memory Compiler 记录 decision-change-log.md；规范归属位置待 Owner 接受后确定。"
    canonical_scope_id: "memory-compiler/e-decision-change-log"
    canonical_scope_keywords:
      - memory-compiler
      - e-domain
      - decision-change-log
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---



# Session E —— 决策 / 变更日志

**分支：** `session-e-memory-compiler-2026-11-16`  
**基线：** `54df136d1e410af834461950e3c61c5c80abd6ad`  
**日期：** 2026-11-16  
**状态：** 候选整改交付；不构成跨模块契约冻结、实现签核或安全批准。

## 1. 已审阅输入与证据边界

| 输入 | 结果 | 说明 |
|---|---|---|
| `reviews/integration/phase-3-cross-module-remediation-task-pack.md` | 已读（READ） | E 的所有权、WS-6、WS-3 执行约束与验收标准 |
| `reviews/integration/phase-2-defg-cross-session-reconciliation.md` | 已读（READ） | INT-P0-03、INT-P1-04/06、INT-X-01/02/06 及门禁依赖 |
| `04-memory-compiler/extraction-and-normalization.md` | 已读（READ） | CandidateProposition 仍为前规范化状态；源模态与 IR 血缘 |
| `04-memory-compiler/evidence-and-provenance.md` | 已读（READ） | Evidence/Provenance 血缘与依赖义务 |
| `04-memory-compiler/consolidation-and-conflict-resolution.md` | 已读（READ） | D 的规范权威；既有跨模块接口附录 |
| E 分支五文件清单与 E 自审 | **未完全核实（NOT FULLY VERIFIED）** | 连接器暴露了上述三个具名 E 设计路径，但未暴露目录树，也未解析其余两个设计文件路径/自审。此处不声称五份文件均已读。该审阅局限必须在签核前关闭。 |
| D 的 Forget 栅栏/规范游标候选 | **OPEN —— 未核实（NOT VERIFIED）** | 本轮未从 D 分支确认候选文件名/契约引用。因此 E 契约将 D 的 schema、epoch 命名空间与屏障视为依赖，而非本地决策。 |
| B 的 Fact/Claim ADR | **ADR-BLOCKED / 未核实已批准** | 第 2 阶段与任务包将 INT-P0-01 标记为 OPEN / ADR-BLOCKED。E 不映射到规范 Claim。 |
| I 的身份/保留策略 | **OPEN** | 任务包将 I 列为新工作流；未假定任何已批准的 I 契约。 |
| H 的线上协议/Adapter | **OPEN** | 任务包将 H 列为新工作流；未假定任何已批准的 H 契约。 |

## 2. 决策与提案

| ID | 决策 / 变更 | 状态 | 所有者 / 依赖 |
|---|---|---|---|
| E-DEC-001 | Accepted 仅指持久回执；与 Processed、Compiled、CanonicalCommitted、Indexed 均不同 | 候选（CANDIDATE） | E；H/I/Storage 审阅 |
| E-DEC-002 | 幂等键按已认证签发方、生产者、安全域与事件族命名空间化 | 候选（CANDIDATE） | H/I/B 批准身份类型 |
| E-DEC-003 | 同键/同语义摘要返回原始回执；同键/不同摘要构成冲突 | 候选（CANDIDATE） | E/H/Storage |
| E-DEC-004 | 接受的线性化点是事务提交：绑定 Event、载荷引用/摘要、幂等回执与编译意图 outbox | 候选（CANDIDATE） | Storage/Consistency 验证实现 |
| E-DEC-005 | 源 Event 游标、D 的规范提交游标与 F 的索引水位是三种不同的类型化命名空间 | 候选（CANDIDATE） | D/F/A/Storage 对齐精确游标定义 |
| E-DEC-006 | 每个 worker/重试/租约/DLQ/重放/重编译/发布都检查当前授权与 D 的 Forget 栅栏；栅栏未知时失败关闭 | 候选（CANDIDATE） | D/I 提供权威栅栏/策略 API |
| E-DEC-007 | 派生依赖登记必须在派生品可见之前持久完成；生产者运行参与 D 屏障 | 候选（CANDIDATE）/ 阻塞性 D 依赖 | 需要 D 的原子登记/发布门 |
| E-DEC-008 | 审计墓碑不含内容、不可重构，且不足以作为物理擦除证明 | 候选（CANDIDATE） | I 批准字段与保留期 |
| E-DEC-009 | 在 B/治理层 ADR 批准之前，CandidateProposition/ExtractionIR 映射保持阻塞 | ADR-BLOCKED | B/治理层；D 消费该决策 |

## 3. 变更路径

- `04-memory-compiler/accepted-receipt-and-idempotency-contract.md` —— 新增。
- `04-memory-compiler/forget-fence-and-derived-registration.md` —— 新增。
- `04-memory-compiler/decision-change-log.md` —— 新增。
- 本候选补丁未重写既有 E 设计文档；其当前契约由两份新的边界契约交叉引用。后续编辑需要已核实的清单与按路径限定的审阅。

## 4. 接口影响

| 模块 | 对 E 的影响 | 需要的所有者决策 |
|---|---|---|
| D | 消费 Forget 栅栏、生产者屏障、依赖登记与规范提交结果/游标；E 只提交提案 | D 拥有精确的规范契约与 Forget 契约 |
| B | 中立 IR 到 Fact/Claim 的映射 | 先批准 ADR-001 |
| F | E 发出规范后发布请求；从不拥有索引水位 | F 定义索引 ACK/水位 |
| G | E 只发出规范影响事件 | G 拥有 ContextVersion 与对账 |
| H | E 消费已认证信封并返回持久回执/状态 | H 定义 BMCP 与 Adapter 线上语义 |
| I | E 消费身份、权限 epoch、保留与 Forget 策略 | I 拥有全局治理/完成判定 |
| Storage/Consistency | Event + 载荷引用 + 回执 + 编译意图的持久性 | 选定/验证事务/outbox/WAL 实现 |

## 5. 验收与一致性矩阵

| 验收项 | 设计覆盖 | 状态 |
|---|---|---|
| 崩溃/重试保留 Accepted 回执 | 事务性 inbox/outbox 与崩溃矩阵 | 候选；需要存储故障注入 |
| 无重复规范副作用 | 稳定操作键；结果未知时查询 D | 候选；需要 D 一致性验证 |
| 重放/DLQ/重编译不得复活已遗忘的派生品 | 每个阶段与发布门处检查栅栏 | 阻塞于 D/I 原子屏障与一致性验证 |
| 每个派生对象都有源血缘与已登记依赖 | 可见性前的依赖登记 | 候选；需要 Storage/D 门 |
| Event、规范与索引游标彼此不同 | 类型化命名空间契约 | 候选；精确 D/F 定义未定 |
| B 的 Fact/Claim 映射仅在批准后 | 显式 ADR 门 | ADR-BLOCKED |
| 五文件 E 审阅与自审完成 | 并非所有路径均已核实 | OPEN |

## 6. 变更控制

本分支变更不合并 D/F/G/H/I 的工作，不冻结线上协议/schema 契约，不选定具体数据库产品，不定义 I 的保留时长，不声明物理擦除，也不声称生产测试已通过。任何 D/I/H 的 schema 不一致，都必须在契约冻结前由所属模块对账。


## 7. 追加的分支感知源审阅（对 §1 的更正）

已读取 D 分支 `session-d-memory-brain-2026-11-16` 的：
- `03-memory-brain/canonical-memory-store.md`；
- `03-memory-brain/memory-versioning.md`；
- `03-memory-brain/memory-lifecycle-manager.md`；
- `03-memory-brain/memory-brain-overview.md`；
- `reviews/03-memory-brain/three-party-six-dimension-review.md`。

E 消费的 D 候选发现：
- CanonicalCommit 携带操作/幂等/请求摘要、期望/结果版本与 commit_sequence；D 提议单调规范序列，但序列范围仍为 OPEN。
- LifecycleEvent 序列按 Memory 聚合划分，不是全局规范提交游标。
- ForgetOperation 包含目标清单、策略/授权引用、抑制时间、依赖快照/水位、按目标进度、例外与完成证明引用。
- D 要求异步清理之前先做抑制，并要求把迟到到达的派生品记录以便后续清理；生产者登记屏障与原子预发布门在所检查的 D 候选中尚未闭合。D-REV-P1-003 仍为 OPEN。
- E 的契约有意要求 D/I/Storage 闭合该竞争，并在权威门存在之前失败关闭。

H 与 I 的分支检索未返回匹配分支。如第 3 阶段任务包基线所述，它们的契约仍为 **OPEN**。B 的 Fact/Claim ADR 仍未核实为已批准；第 2 阶段与 D 的审阅继续将 INT-P0-01 标记为 ADR-BLOCKED。未新增任何 E 映射。

E 的五文件清单与 E 自审仍仅部分核实：定位并读取了三个 E 设计文件；GitHub 连接器本轮未暴露目录列表，也未解析其余两个设计路径/自审。三个已定位文件已按新的入站/Forget 约束更新。该局限使"五文件/自审已完成"的声明无法成立，并作为显式 OPEN 审阅项记录。


## 8. 已完成的分支感知源审阅（取代 §1 与 §7 中较早的局限说明）

### E 源包

全部五个 E 设计文件均已在 `session-e-memory-compiler-2026-11-16` 上定位并读取：
- `04-memory-compiler/compiler-overview.md`
- `04-memory-compiler/event-ingestion-engine.md`
- `04-memory-compiler/extraction-and-normalization.md`
- `04-memory-compiler/evidence-and-provenance.md`
- `04-memory-compiler/consolidation-and-conflict-resolution.md`

E 自审已读：
- `reviews/04-memory-compiler/three-party-six-dimension-review.md`

五个设计文件已按第 3 阶段的回执、游标、身份/保留与 Forget 登记约束更新。E 自审仍是一份审阅记录，未被修改。

### D 源包

D 候选设计与审阅已在 `session-d-memory-brain-2026-11-16` 读取（基线提交 `9dc08c63f6912320e290a963c634748ec44a81c8`）：
- `03-memory-brain/canonical-memory-store.md`
- `03-memory-brain/memory-versioning.md`
- `03-memory-brain/memory-lifecycle-manager.md`
- `03-memory-brain/memory-brain-overview.md`
- `reviews/03-memory-brain/three-party-six-dimension-review.md`

D 的关键状态：CanonicalCommit 具备操作/幂等/请求摘要、期望/结果版本与 commit_sequence；序列范围仍为 OPEN。LifecycleEvent 序列按 Memory 聚合划分。ForgetOperation 携带目标清单、抑制时间、依赖快照/水位、按目标进度与完成证明。D 的候选提到迟到派生品的发现/后续清理，但未闭合生产者登记 epoch 加原子发布门；D-REV-P1-003 仍为 OPEN。

### H 源包

H 候选设计已在 `session-h-bmcp-protocol` 读取，基线 `8e57f38e1f81a26280f0d56d6a40d6b98c5c6ac2`，候选提交 `fcc5103399b4c322e52d642cae5a2414969399a7`：
- `08-bmcp-protocol/protocol-overview.md`
- `08-bmcp-protocol/message-envelope-and-versioning.md`
- `08-bmcp-protocol/context-delivery-and-acknowledgement.md`
- `08-bmcp-protocol/adapter-capability-and-applied-attestation.md`
- `08-bmcp-protocol/forget-revocation-and-reconnect.md`
- `08-bmcp-protocol/protocol-conformance-matrix.md`

H 已存在但为 CANDIDATE，尚未批准。其信封携带所有者定义的幂等命名空间/键/摘要；H 传输 E 的回执语义。它要求 I 提供已认证的传输主体绑定，把载荷中的 ActorRef/producer 视为声明，区分 E 源游标、D 规范游标、生命周期游标与 F 索引水位，并把 Forget 栅栏/权限 epoch 视为不透明值。H 明确不得声明全局 Forget 完成或提供方物理擦除。

### I 源包

I 候选设计已在 `session-i-security-governance-2026-11-16` 读取，基线 `8e57f38e1f81a26280f0d56d6a40d6b98c5c6ac2`，候选提交 `8c91d99e450ab5e8862bd6a3301fa193e28e6cbb`：
- `09-security-governance/security-and-identity-overview.md`
- `09-security-governance/principal-actor-and-authorization-contract.md`
- `09-security-governance/scope-and-revocation-policy.md`
- `09-security-governance/forget-retention-backup-and-erasure-policy.md`
- `09-security-governance/threat-model-and-adversarial-test-plan.md`
- `09-security-governance/audit-and-exception-governance.md`

I 已存在但为 CANDIDATE，尚未批准。它提议幂等命名空间 = 已认证生产者 + 租户/安全域 + 操作族 + 调用方键；要求在入站与每次重试/重放时校验当前授权；要求回执元数据覆盖声明的重试/重放视野，而具体时长数值仍为 OPEN。其 Forget 证明要求密封的目标清单、生产者登记 epoch/在途屏障、全部屏障前生产者的终态、消费者水位，以及显式的 Confirmed 或 PolicyException 目标。未知/离线不等于成功。其墓碑必须不可重构且有界；禁止原始内容、低熵哈希、嵌入向量、摘要与溯源边。

### B ADR 状态

在所审阅的输入中未核实到已批准的 B Fact/Claim ADR。第 2 阶段与 D 的审阅仍将 INT-P0-01 记为 OPEN / ADR-BLOCKED。CandidateProposition/ExtractionIR 映射保持阻塞；未新增规范映射。

### 更新后的依赖处置

- **H 存在 / CANDIDATE：** 线上信封与序列化可影响字段映射，但不构成最终线上协议冻结。
- **I 存在 / CANDIDATE：** 身份、授权、保留与全局 Forget 策略可影响执行约束，但不构成最终策略冻结。
- **D 存在 / CANDIDATE：** 规范游标与 Forget 栅栏形态仍由所有者控制；D-REV-P1-003 的屏障缺口仍构成阻塞。
- **B ADR 缺失/未批准：** 映射仍为 ADR-BLOCKED。


## 9. 第 3 阶段定向整改 —— 当前分支 HEAD 对账

本节作为对上述历史记录的更正追加。更早的表述作为历史审计记录保留；若与本节冲突，以本节记录的较新检查与取代状态为准。

### 9.1 本次整改读取的精确当前源引用

| 所有者 | 分支 | 已检查的当前 HEAD | 结果 |
|---|---|---|---|
| E | `session-e-memory-compiler-2026-11-16` | `3dea6096eefa6779eb12e4e788bcf9429d2a3f83` | 已枚举当前 E 包目录树；识别出全部八个 E 设计路径，已读取核心入站/Forget/溯源/总览文件 |
| D | `session-d-memory-brain-2026-11-16` | `30dbffdc7d47af0888ecf7b42cfa686d2ec0c9d6` | 已读取当前 ForgetFence、CanonicalCommitCursor 与 MemoryVersioning |
| H | `session-h-bmcp-protocol` | `fcc5103399b4c322e52d642cae5a2414969399a7` | 已检查当前信封与 Forget/Revocation 包；仅 CANDIDATE |
| I | `session-i-security-governance-2026-11-16` | `8c91d99e450ab5e8862bd6a3301fa193e28e6cbb` | 已检查当前 Principal/ActorRef/ProducerIdentity 与 Forget/Retention 包；仅 CANDIDATE |
| B | `session-b-domain-model-phase3` | `ab19afbf92f67fe0a7679e9aa3a35b015fed89f4` | 已检查当前 ADR-001 与类型化 ScopeRef 语义；ADR 仍为 ADR-BLOCKED |

所请求的 `reviews/integration/phase-3-defghi-cross-module-contract-review.md` 在当前 A 分支树中不存在，抓取时返回 NOT_FOUND。它不被表示为已读。第 3 阶段任务包从 A 的当前分支读取；A 的 Contract Registry 与 Typed Cursor 提案也已读取。该具名审阅报告缺失仍是源证据局限。

### 9.2 现被消费的 D 决策 —— 取代 §§1、2、7、8 中的较早条目

- **DECIDED —— CanonicalCommitCursor：** 每个 Canonical Memory 权威一个全局有序序列，仅在持久规范事务成功提交时分配。
- **DECIDED —— AggregateRevision：** 按聚合独立的修订序列；每个已提交修订都携带其 CanonicalCommitCursor。
- **DECIDED —— LifecycleEventCursor：** 按 Memory 独立的连续生命周期流；每个事件同时记录其所属的 CanonicalCommitCursor。
- **DECIDED —— ForgetFenceCursor：** D 拥有的元组 `(forget_operation_id, fence_generation, target_set_digest)`；独立于规范提交、生命周期、权限与索引位置。
- **DECIDED —— 生产者屏障语义：** D 的生产者登记处在栅栏安装时捕获登记高水位；每个栅栏前登记都必须达到持久终态处置。队列删除、租约过期、超时或 worker 丢失都不是终态。
- **DECIDED —— 先登记后可见原则：** 派生品登记先于可见性，最终门重新检查最新栅栏；这是语义要求，不是已发布的可调用 API。
- **OPEN / BLOCKING —— D/E/Storage 原子性：** D 尚未规定可调用的登记/依赖/发布操作、完整回执字段、事务所有者，或把最终门与 Storage 可见性耦合起来的已验证线性化协议。D-REV-P1-003 的实现级竞争仍为 OPEN。

### 9.3 H/I/B 对齐与状态

- **H 存在 / CANDIDATE：** 已认证传输主体绑定具有权威性；载荷中的 ProducerId/ActorRef/ScopeRef 仅为声明/选择器。权限 epoch 与 Forget 栅栏是彼此独立的类型化字段；重放会重新检查两者。线上协议未冻结。
- **I 存在 / CANDIDATE：** ProducerIdentity 绑定已认证 Principal/签发方、已登记生产者/应用、工作负载/实例、凭据有效期/epoch、允许的事件族、安全域与撤销状态。PermissionEpoch 归 I 所有。授权必须在操作的提交/披露线性化点重新检查。策略未冻结。
- **B 存在 / ADR-BLOCKED：** ScopeRef 是类型化领域引用，不是权限。ClaimRef/ClaimRevisionRef 与 Fact/Claim 规范映射仍被 ADR-001 阻塞。CandidateProposition/ExtractionIR 不得自动升级。
- **H/I 状态更正：** "H/I 分支缺失"的历史表述已被取代；正式的候选包现已存在。

### 9.4 E 决策与取代台账

| 历史条目 | 先前状态 | 当前处置 |
|---|---|---|
| E-DEC-001 Accepted 与处理里程碑 | CANDIDATE | **CANDIDATE，已细化**：AcceptedReceipt、CompilerCompletionReceipt、CanonicalCommitReceipt、DerivedRegistrationReceipt、PublicationReceipt 与 F Index ACK 是彼此不同的证据 |
| E-DEC-002 幂等命名空间 | CANDIDATE | **CANDIDATE，已细化**：绑定已认证 Principal + ProducerIdentity + 已校验 Scope 绑定 + 安全域 + 操作族 + 调用方键；精确规范化待 H/I/B |
| E-DEC-003 同键摘要行为 | CANDIDATE | **CANDIDATE**：同键/同摘要返回原始结果；不同摘要构成冲突 |
| E-DEC-004 接受的线性化 | CANDIDATE | **CANDIDATE**：持久 Event + 载荷引用/摘要 + 幂等 + 回执 + 编译意图，处于同一事务或已验证的 WAL |
| E-DEC-005 游标分离 | CANDIDATE | **已消费 D 的语义决策**：CanonicalCommitCursor 按 Brain 权威全局；AggregateRevision 与 LifecycleEventCursor 独立；IndexWatermark 归 F；ForgetFenceCursor 归 D；PermissionEpoch 归 I；ContextVersion 归 G |
| E-DEC-006 异步工作上的栅栏检查 | CANDIDATE | **CANDIDATE E 执行约束**；最终门仍为 OPEN/BLOCKING |
| E-DEC-007 可见性前的依赖登记 | CANDIDATE / 阻塞 | **D 语义规则已 DECIDED；D/E/Storage 原子操作 OPEN/BLOCKING** |
| E-DEC-008 不可重构墓碑 | CANDIDATE | **CANDIDATE**，取决于 I 的保留/审计批准 |
| E-DEC-009 Fact/Claim 映射 | ADR-BLOCKED | **ADR-BLOCKED —— 未变** |

### 9.5 本次整改的变更路径

- `04-memory-compiler/forget-fence-and-derived-registration.md` —— 重写以消费当前 D 的栅栏、生产者屏障与游标决策；记录缺失的精确 D/E/Storage 操作。
- `04-memory-compiler/accepted-receipt-and-idempotency-contract.md` —— 重写以拆分 Accepted、Compiler Completion、Canonical Commit、Derived Registration、Publication 与 F Index 证据。
- `04-memory-compiler/compiler-state-and-producer-admission.md` —— 新增 E 拥有的生命周期与 D 准入映射。
- `04-memory-compiler/evidence-and-provenance.md` —— 追加类型化游标与可见性前血缘登记要求。
- `04-memory-compiler/decision-change-log.md` —— 追加本源/决策更正，同时保留全部更早的审计历史。

### 9.6 测试与验证状态

更新后的 E 文档中的所有一致性场景均为 **NOT RUN**。本次交付仅限设计与文档。未执行任何 Storage 事务、D 端点、worker、队列、DLQ、栅栏服务、权限服务、发布门或运行时测试。E 分支提交与写入后的文件回读，记录在提交创建后的最终交付报告中。


## 10. 交付前最终并发分支刷新

本 E 整改撰写期间 H 与 I 有推进。最终交付前重新读取了它们的最新分支引用；上文所用语义已对照这些当前 HEAD 校验，取代 §9.1 记录的较早 H/I SHA。

| 所有者 | 分支 | 重新读取的最新 HEAD | 相关当前文件 |
|---|---|---|---|
| H | `session-h-bmcp-protocol` | `3c4c03c28c4e50cc6eed89d505725b873241bad7` | `message-envelope-and-versioning.md` blob `5547ecd78d118bd63e571e5daad87194d9b694e4`；`forget-revocation-and-reconnect.md` blob `695909360782987781e259187041618f495f1c8c` |
| I | `session-i-security-governance-2026-11-16` | `135afd3d8333256ee2efcca9525a39a9d06739fc` | `principal-actor-and-authorization-contract.md` blob `4f6f5691a599a0566b036f4240003152d64e2242`；`forget-retention-backup-and-erasure-policy.md` blob `db602095f1b9760798ea423b09887ae8b9b4821c` |

刷新后的 H/I 文档继续要求已认证传输绑定，拒绝把载荷自述的生产者/参与者/范围身份当作认证，在重放以及提交/披露边界处重新检查当前 PermissionEpoch 与 ForgetFence，并把本地 Adapter 确认与全局 Forget 完成区分开。H/I 仍为 CANDIDATE，未冻结。

当前 A 分支树与仓库代码检索均未定位到 `reviews/integration/phase-3-defghi-cross-module-contract-review.md`；该具名审阅仍不可用，且不声称已读。



---
## 9. 第 3.5 阶段 —— 权威取代与当前处置

本节是当前 E 侧的源对齐记录。更早的表述作为历史审计记录保留，但若与本节冲突，则**已被取代（SUPERSEDED）**，不得用作当前状态。

### 9.1 被取代的历史表述

| 历史表述 / 章节 | 状态 | 取代者 |
|---|---|---|
| §1 称 D 的 Forget 栅栏/规范游标候选未核实、D 序列范围仍为 OPEN | **SUPERSEDED** | 第 3 阶段跨模块审阅以及 D 当前 Forget 栅栏与提交游标语义；D 的 CanonicalCommitCursor 按权威全局 |
| §7 称 D 屏障/原子预发布门未闭合、D-REV-P1-003 仍广泛未定义 | **部分取代（PARTIALLY SUPERSEDED）** | D 现已规定 Producer Registration Barrier、先登记后可见与最新栅栏发布门语义；更窄的 D/E/Storage 原子操作/线性化仍为 OPEN |
| §7 称 H 与 I 分支缺失 | **SUPERSEDED** | H 与 I 的候选包存在于第 3 阶段跨模块审阅记录的各个分支 HEAD；其契约未冻结/未批准 |
| §1/§7 称 I 身份/保留与 H 线上协议/Adapter 契约不可用 | **仅就"存在性"而言被取代** | 已读取 I/H 候选契约；身份、保留、ACK 映射与线上 schema 仍为候选/未决依赖 |
| §1/§7 关于 E 五文件清单与自审的局限 | **仅在 §8 已核实范围内被取代** | §8 记录了已完成的源清单；本次更新不声称运行时测试或实现证据 |
| 任何把 E 本地栅栏预检查视为发布充分条件的措辞 | **SUPERSEDED** | PublishDerivedIfFenceCurrent 必须由 D 权威，并与栅栏安装串行化；E 的本地检查仅为纵深防御 |
| 任何暗示 Accepted 即已编译/已提交/已发布的措辞 | **SUPERSEDED** | AcceptedReceipt 证据矩阵：Accepted 仅为持久入站 |

### 9.2 当前分支/源基线

第 3 阶段跨模块审阅记录了下列已审阅分支 HEAD（完整 SHA）：

| 会话 | 分支 | 已审阅 HEAD | 当前包状态 |
|---|---|---|---|
| A | session-a-integration-2026-11-16 | f76cc558273fbc1a27bb930a2f1e8d940b717c80 | 协调产物；登记册更正仍归 A 所有 |
| B | session-b-domain-model-phase3 | ab19afbf92f67fe0a7679e9aa3a35b015fed89f4 | Fact/Claim ADR 仍为 ADR-BLOCKED；类型化引用未冻结 |
| D | session-d-memory-brain-2026-11-16 | 30dbffdc7d47af0888ecf7b42cfa686d2ec0c9d6 | Forget 与游标语义已具备；D/E/Storage 原子实现 OPEN |
| E | session-e-memory-compiler-2026-11-16 | 3dea6096eefa6779eb12e4e788bcf9429d2a3f83 | E 设计包；第 3.5 阶段更新在该已审阅基线之后单独提交 |
| H | session-h-bmcp-protocol | fcc5103399b4c322e52d642cae5a2414969399a7 | 候选 Forget ACK/重连包已存在；未冻结 |
| I | session-i-security-governance-2026-11-16 | 8c91d99e450ab5e8862bd6a3301fa193e28e6cbb | 候选全局 Forget/身份策略已存在；未冻结 |

F 与 G 不属于第 3 阶段 D/E/H/I 审阅所记录的分支 HEAD 集合。此处不推断任何 F/G HEAD。E 分支的审阅后 HEAD 是第 3.5 阶段交付所报告的提交 SHA，而非上述历史已审阅基线。

### 9.3 当前权威依赖决策

- **D 生产者屏障 —— 已 DECIDED 的语义要求：** D 当前 Forget 契约要求封闭世界的 ProducerClass/ProducerWork 登记、执行/租约/重试/DLQ 重放/发布之前的持久登记、捕获生产者登记高水位的栅栏安装、全部栅栏前工作的终态处置、可见性之前的持久依赖登记，以及紧邻发布之前的最新栅栏复检。
- **D/E/Storage 操作契约 —— OPEN / BLOCKING：** RegisterProducerWork、InstallForgetFence、RegisterDerivedDependency、PublishDerivedIfFenceCurrent 与 CompleteProducerWork 的精确输入/输出/错误与线性化，必须可共同实现并经测试。D 的语义要求不构成可调用 API 或事务实现的证明。
- **H/I —— 候选已存在：** H 有 Adapter 本地 ACK 与重连候选契约；I 有全局 Forget 清单/完成、身份/授权与保留/备份候选契约。H ACK 仅为本地证据；全局完成策略仅归 I。
- **B Fact/Claim —— ADR-BLOCKED：** E 继续把 CandidateProposition/ExtractionIR 视为前规范化编译器制品。本次更新未批准任何规范 Fact/Claim 映射、schema 冻结或线上字段。
- **CanonicalCommitCursor —— D 已 DECIDED：** 每个权威一个全局序列。AggregateRevision、LifecycleEventCursor、F IndexWatermark、D ForgetFenceGeneration、I PermissionEpoch 与 G ContextVersion 是彼此独立的类型化命名空间。
- **未核实的实现 —— 未通过（NOT PASSED）：** 设计文档与静态审阅不是运行时一致性。没有可执行夹具、环境、期望/实际输出与留存证据，任何测试都不得标记 PASS。

### 9.4 第 3.5 阶段变更清单

| E 文件 | 变更 |
|---|---|
| compiler-state-and-producer-admission.md | ProducerClass 与 WorkItem 登记；租约/尝试/重试/DLQ/重放/重编译与终态证据；崩溃恢复 |
| forget-fence-and-derived-registration.md | 五项 D 操作映射；暂存/可见性边界；发布证据；显式 OPEN 契约；16 个竞争/故障用例 |
| accepted-receipt-and-idempotency-contract.md | Accepted 到发布的状态矩阵；重复提交；ACK 丢失恢复；游标命名空间 |
| decision-change-log.md | 显式取代标记与当前跨模块状态 |

### 9.5 门禁处置

- CR-P1-01：**OPEN / BLOCKING** —— D/E/Storage 原子登记、依赖可见性与最终发布线性化仍未解决且未实现。
- INT-P0-03：**OPEN** —— 端到端 Forget 需要 D/E/F/G/H/I 与 Storage 的证据；本次 E 文档变更无法闭合它。
- CR-P1-02 / INT-X-01：E 的语义游标描述已对齐 D 的按权威全局决策；A/F/G/Storage 集成与可执行的持久性/恢复验证仍不在本次纯 E 变更范围内。
- INT-P0-01：**ADR-BLOCKED** —— B 的 Fact/Claim 批准仍缺失/未核实。
- H/I：确认候选包存在；不暗示任何跨模块契约冻结或安全批准。



---
## 9.6 D 第 3.5 阶段操作级细化 —— 当前

当前 D 的规范源是 03-memory-brain/forget-fence-operation-and-publication-gate.md（D 分支 session-d-memory-brain-2026-11-16；blob 2c5b1358ff58f99af838b741a75966ccd07ad088）以及 D 的 decision-change-log §7（blob 1deecb7e97a35782aa48f9053398d8b3ff9b0932）。本细化取代 §9.3 中"仅定义五项 D 操作"的任何暗示。

D 的完整语义操作集合为：
1. RegisterProducerClass
2. RegisterProducerWork
3. InstallForgetFence
4. CaptureProducerRegistrationHighWater
5. RegisterDerivedDependency
6. PublishDerivedIfFenceCurrent
7. CompleteProducerWork
8. ResolveProducerWork
9. ReconcileForgetBarrier

D35-01 至 D35-07 是已 DECIDED 的语义契约；D35-08 的 Storage/Consistency 所有权与实现为 OPEN / 所有者未指派；D35-09 的 E/I/H/B 集成仍为 OPEN；D35-10 的运行时故障测试为 NOT RUN。D 的操作契约明确不主张 API 或 Storage 事务已经存在。

ProducerRegistrationSequence / ProducerRegistrationHighWater 与 ProducerRegistryVersion 是彼此独立的 D 账本类型。它们不是 CanonicalCommitCursor 或 ForgetFenceGeneration。E 原样存储每一个，且不跨命名空间比较。

Session E 任务中明确要求的五项操作在 §1 中映射；本附录补齐 D 当前规范契约所需的四项支撑操作。CR-P1-01 与 INT-P0-03 仍为 OPEN。



---
## 9.7 OPEN 项精确化 —— D 语义契约现已规定

本节取代较早的 §5/§9.3/§9.5 措辞，只要其暗示 D 的操作级语义输入、输出、幂等、错误结果或线性化点仍未规定。

D 当前规范文件 03-memory-brain/forget-fence-operation-and-publication-gate.md 规定了全部九项语义操作及其类型化输入/输出、幂等、错误词汇与线性化点。D 决策日志 §7 将 D35-01 至 D35-07 记录为已 DECIDED 的语义契约。特别是，RegisterProducerWork 与 InstallForgetFence 共享同一个可线性化顺序；栅栏安装捕获 ProducerRegistryVersion 与 ProducerRegistrationHighWater；CaptureProducerRegistrationHighWater 校验不可变截止点；PublishDerivedIfFenceCurrent 与可见性一同线性化；ResolveProducerWork 与 ReconcileForgetBarrier 定义恢复/对账。

因此：
- 任何把 E 的 OPEN 项表述为"D 尚未定义操作输入/输出/错误/高水位/竞争顺序"的早期说法，均**已被取代**。
- 仍为 OPEN 的是：可调用 API/传输 schema 与线上错误映射；I/H/B 的已认证身份与 PermissionEpoch 绑定；I/A 对全局生产者/接收方清单与 D 本地登记册的对账；E 重编译子项/再准入身份的精确语义；具名的 Storage/Consistency 所有者与经测试的事务/CAS/隐藏准备实现；可执行一致性验证。
- D35-08 为 OPEN，因为 Storage/Consistency 所有权未指派且实现未验证。
- D35-09 就 E/I/H/B 集成与全局清单协调而言为 OPEN。
- D35-10 为 NOT RUN；设计表格不是测试结果。

本次 E 更新不改变任何 D 语义决策。CR-P1-01 与 INT-P0-03 仍为 OPEN。


---

## 10. 第 3.5 阶段再处理 —— 取代、源证据与当前 OPEN 登记

本节是当前 E 侧状态记录。上文历史条目保留以供审计；冲突表述在此被取代。

### 10.1 被取代的历史表述

| 历史表述 | 状态 | 替代 |
|---|---|---|
| D 的 Forget 屏障/生产者语义缺失 | **SUPERSEDED** | D 操作契约定义了九项语义操作、类型化回执、幂等、错误与线性化 |
| D 操作输入/输出/错误/高水位/竞争顺序未规定 | **SUPERSEDED** | D35-01..07 语义决策；仅可调用传输/API 与经测试的 Storage 实现仍为 OPEN |
| H/I 分支缺失 | **SUPERSEDED** | 已在下列 HEAD 读取当前 H/I 候选包；存在不等于批准 |
| D 的 CanonicalCommitCursor 范围未决或分区 | **SUPERSEDED** | D 决定每个 Canonical Memory 权威一个全局序列 |
| E 本地栅栏预检查/缓存令牌足以发布 | **SUPERSEDED** | D 的 PublishDerivedIfFenceCurrent 与可见性一同线性化，并与 Fence 安装串行化 |
| 租约过期、队列删除、worker 丢失或 DLQ 停泊使工作终结 | **SUPERSEDED** | 在取得持久终态回执并完成对账之前，D 屏障保持开启 |
| Accepted 意味着已编译、规范提交或已发布 | **SUPERSEDED** | AcceptedReceipt 仅为持久入站/编译意图证据 |
| E 分配 CanonicalCommitCursor 或 IndexWatermark | **SUPERSEDED** | D 拥有 CanonicalCommitCursor；F 拥有 IndexWatermark；E 原样存储所有者签发的值 |
| E 可冻结 Fact/Claim 映射 | **SUPERSEDED / ADR-BLOCKED** | B 的 Fact/Claim ADR 仍为 ADR-BLOCKED；CandidateProposition/ExtractionIR 保持前规范化 |

### 10.2 本次 E 提交前读取的精确分支 HEAD 清单

| 所有者 | 分支 | 完整 HEAD SHA | 读取/状态 |
|---|---|---|---|
| Main | `main` | `8a6414158c9c056c1638222534e1993d1bbc99d2` | 已读必需的 D/E/H/I 审阅 |
| A | `session-a-integration-2026-11-16` | `f18c64950a84385bd407752c7188e1bd52029a7b` | 只读协调输入 |
| B | `session-b-domain-model-phase3` | `66adf6bdcf5ec69a146fe75afe20ce3b85af8448` | Fact/Claim ADR 仍为 ADR-BLOCKED |
| C | `session-c-agent-integration-2026-11-16` | `35de58ddc93c5f1e554596cdfc430cd6c392d355` | 未修改；未推断任何 C 决策 |
| D | `session-d-memory-brain-2026-11-16` | `da8e5882d0b238d765d00b2225b79eea45a483b1` | 已读当前 Forget 操作、游标与决策日志 |
| E 父 | `session-e-memory-compiler-2026-11-16` | `13a720724fcfae84f4c4abe36fbc44dd2820445d` | 本次纯 E 更新的父 HEAD |
| F | `session-f-memory-runtime` | `8b16a3621cbe2be4badac1799822b64824532b25` | 未修改；无 F 实现主张 |
| G | `session-g-memory-context` | `3d2c065be863bc1d349faaeece6f6eaa0047abae` | 未修改；无 G 实现主张 |
| H | `session-h-bmcp-protocol` | `a830628ec0f15a960277412c67c2197565ca1dc4` | 已读 Forget/Revocation/离线重连；CANDIDATE |
| I | `session-i-security-governance-2026-11-16` | `5591ad3620ec3f5d74194bd79556dcf3e25bea07` | 已读全局清单/身份/Forget 策略；CANDIDATE |
| Storage | `session-storage-consistency-forget-atomicity-2026-11-16` | `ec0e29d9b6e6e32728116514376214503aeb2434` | 已审阅拟议实现；实现 OPEN |

### 10.3 已读的必需源文件

- 跨模块审阅：main 上的 `reviews/integration/phase-3-defghi-cross-module-contract-review.md`。
- D：`03-memory-brain/forget-fence-operation-and-publication-gate.md`、`commit-cursor-semantics.md`、`decision-change-log.md`。
- E：全部五个编译器设计文件，以及 compiler-state、Forget/派生登记、Accepted 回执/幂等与本变更日志。
- H：`08-bmcp-protocol/forget-revocation-and-reconnect.md`（CANDIDATE）。
- I：`09-security-governance/phase-3.5-global-identity-forget-governance.md`、`forget-retention-backup-and-erasure-policy.md`、`principal-actor-and-authorization-contract.md`（CANDIDATE）。

### 10.4 OPEN 登记

| OPEN ID | 精确的未解决问题 | 所有者 |
|---|---|---|
| OPEN-API-01 | 可调用的 D API/传输 schema、已认证绑定、序列化/版本化与语义错误到线上错误的映射 | D/H/B/I |
| OPEN-STORAGE-01 | 具名的 Storage 所有者与已验证的事务/CAS/可串行化/隐藏准备实现；栅栏到可见性的共享线性化、持久性、故障切换、副本/读取与恢复保证 | Storage + D/E |
| OPEN-I-AUTH-01 | 在最终发布边界处，当前 I PermissionEpoch 与授权决策的新鲜度/撤销证明 | I + D/E |
| OPEN-REGISTRY-GLOBAL-01 | 将 I 的 ProducerDomainInventoryEpoch 与 A/模块清单同 D 的 ProducerRegistryVersion/ProducerRegistrationHighWater 对账；证明全局封闭世界完整性 | I/A + D/E/H |
| OPEN-RECOMPILE-01 | 重编译与屏障结算所需的显式关联子项/再准入身份 | D/E |
| OPEN-REC-01 | AcceptedReceipt + 载荷引用 + 幂等 + CompileIntent/outbox 事务/WAL 的持久性与崩溃恢复画像 | E + Storage |
| OPEN-REC-02 | 规范语义摘要/规范化画像，以及 B/H 类型化身份/Scope 序列化 | E + B/H/I |
| OPEN-REC-03 | 幂等/墓碑保留视野，以及 Forget 之后披露安全的回执查询 | I + E/Storage |
| OPEN-TEST-01 | 可执行的竞争/故障夹具、崩溃/故障切换注入、实际输出与所有者审阅的证据 | D/E/Storage + 消费者 |

D 的操作级语义字段、结果回执、幂等、错误结果与线性化均为 DECIDED；本 OPEN 登记不得被解读为重新打开这些决策。D35-08 的 Storage 所有权/实现、D35-09 的跨所有者集成与 D35-10 的运行时故障测试仍为 OPEN/NOT RUN。

### 10.5 跨所有者处置与不作声明

- D 的生产者屏障与操作语义为 DECIDED；D/E/Storage 实现与可执行一致性仍为 OPEN。
- CanonicalCommitCursor 是每个 Canonical Memory 权威一个全局序列。AggregateRevision 按聚合；LifecycleEventCursor 按 Memory；IndexWatermark 按 F 索引/通道分区；ForgetFenceGeneration 是 D 独立的栅栏命名空间；PermissionEpoch 归 I；ContextVersion 归 G。禁止跨命名空间比较或替换。
- H/I 包已存在但仍为 CANDIDATE。H ACK 受目标/动作/能力/会话限定；I 拥有全局清单、目标聚合与完成判定。
- B 的 Fact/Claim 仍为 ADR-BLOCKED；本次 E 更新未批准任何规范 schema/API/线上字段。
- CR-P1-01 与 INT-P0-03 仍为 OPEN/BLOCKING。文档不能证明 D/E/Storage 的原子执行约束或全局 Forget 完成。
- 全部故障/竞争用例均为 NOT RUN。不声称任何实现、运行时、存储、安全或性能测试 PASS。
- 仅修改 `04-memory-compiler/` 下 E 拥有的文件；所有其他模块文件均为只读输入。

### 10.6 本次再处理变更的文件

- `04-memory-compiler/compiler-state-and-producer-admission.md` —— 生命周期、稳定身份、租约/重试/DLQ/重放/重编译/终态语义，以及更正后的 D 决策状态。
- `04-memory-compiler/forget-fence-and-derived-registration.md` —— 五项被要求的 D 操作 + 四项支撑操作、可见性边界、精确 OPEN 项与扩展故障矩阵。
- `04-memory-compiler/accepted-receipt-and-idempotency-contract.md` —— 独立的回执状态矩阵、重复提交与恢复/重放语义。
- `04-memory-compiler/decision-change-log.md` —— 取代台账、分支 HEAD 清单、源读取证据与 OPEN 登记。


### 10.7 本次再处理的提交与回读证据

纯 E 文件提交（每个提交恰好变更所述路径）：

| 文件 | 提交 SHA |
|---|---|
| `compiler-state-and-producer-admission.md` | `2c11cca8ca2b68da53f8ede9e85acd56d8b34a96` |
| `forget-fence-and-derived-registration.md` | `262d36d2cc551192d75cf510eb44e4ae1795c1a8` |
| `accepted-receipt-and-idempotency-contract.md` | `07833bc582d63ba68000291fbf840cb97b42b575` |
| `decision-change-log.md` —— 取代/源/HEAD 记录 | `09f5892d0999f0933a73ccc6ac784ce4dd54e8a0` |
| `accepted-receipt-and-idempotency-contract.md` —— 显式 ForgetFenceGeneration 命名空间更正 | `488621d0d2d8493bee2c098a791c96bbf3e3c954` |

回读确认了 E 分支上的更新文件，包括重校验章节、D 到 E 的映射、故障矩阵、回执状态矩阵，以及类型化游标/栅栏代号表。最终决策日志自更新提交与由此产生的分支 HEAD，将在重新抓取后的交付记录中报告。这些提交未变更任何其他路径。

回读仅为文档/提交证据。它不确立可执行的 D 端点、Storage 事务、运行时发布安全或测试 PASS。

 
---

## 第 3.6 阶段 —— 栅栏强制的编译器发布与持久依赖原子性

**状态：** 设计契约完成 / 实现未核实（IMPLEMENTATION NOT VERIFIED）。本条目仅在下方第 3.6 阶段 E 拥有的协议更具体之处取代第 3.5 阶段的候选措辞。它不主张 D/Storage/F/I 的批准或实现。

### 1. 本次读取的源基线

| 所有者 | 分支 | 已读 HEAD | 证据 / 处置 |
|---|---|---|---|
| 集成审阅 | main | `8a6414158c9c056c1638222534e1993d1bbc99d2` | `reviews/integration/phase-3-defghi-cross-module-contract-review.md`；有条件通过，CR-P1-01 OPEN/BLOCKING |
| D | `session-d-memory-brain-2026-11-16` | `da8e5882d0b238d765d00b2225b79eea45a483b1` | D 操作级语义；本次未取得第 3.6 阶段更新后的 HEAD |
| E | `session-e-memory-compiler-2026-11-16` | `c2f14408ba62447c11172d65b93a279fef96d175` | 本次第 3.6 阶段变更集之前的 E 源基线 |
| Storage | `session-storage-consistency-forget-atomicity-2026-11-16` | `3a14550648f21c0bc2725dac38b29e099c2f3196` | 仅为拟议的共享串行化设计；不是已批准实现 |
| F | `session-f-memory-runtime` | `f86f9b536ea69d8e0fbb4bf290c7023ef0eada76` | 重建/回填/重放消费者契约与类型化证据矩阵 |
| I | `session-i-security-governance-2026-11-16` | `5591ad3620ec3f5d74194bd79556dcf3e25bea07` | 全局清单分支 HEAD；清单制品 blob `9100061fa986fb6676656169de3fcf9fc1c72664` |

当前 D 分支包含第 3.5 阶段的操作级契约，而非单独核实的第 3.6 阶段操作修订。Storage 的分支报告是拟议实现，不是已批准的 Storage 权威。集成审阅属历史记录且仍为有条件通过；它不是对本次 E 更新的批准。

### 2. 已消费的 D 操作映射

E 消费 D 的语义操作，不发明传输 schema：RegisterProducerClass、RegisterProducerWork、InstallForgetFence、CaptureProducerRegistrationHighWater、RegisterDerivedDependency、PublishDerivedIfFenceCurrent、CompleteProducerWork、ResolveProducerWork 与 ReconcileForgetBarrier。E 的最终门要求是：当前栅栏校验、活动工作/尝试/租约校验、完整依赖回执、当前 I 授权与可见性切换，共享同一个串行化决策。

### 3. 请求的联合决策

- **D 请求：** 确认根 WorkItemId 在重试、DLQ 重放、重编译与 worker 恢复之间的稳定性；确认重编译使用新的 DerivationRunId 而不改变根屏障身份；确认精确的当前栅栏/源祖先检查与发布对栅栏的竞争结果。
- **Storage 请求：** 确认跨 D 的栅栏/生产者账本、完整依赖登记与制品可见性标记的共享事务/串行化权威与精确线性化点；或提供已批准的持久准备/提交协调器、隐藏准备不变量、最终可见性 CAS 处的栅栏/权限重校验、参与者恢复与恢复协议。
- **I 请求：** 确认当前 PermissionEpoch 与撤销决策如何在最终可见性提交处取得权威性；E 无法独立断言其新鲜度。
- **F 请求：** 确认索引器/重建/回填/重放只消费已提交的 PUBLISHED 制品，并在索引与服务之前重校验当前栅栏/权限。

不从文档存在推断任何响应或批准。在记录显式的所有者决策之前，确认状态仍为 OPEN。

### 4. 变更的 E 拥有路径

- `04-memory-compiler/compiler-state-and-producer-admission.md`
- `04-memory-compiler/forget-fence-and-derived-registration.md`
- `04-memory-compiler/accepted-receipt-and-idempotency-contract.md`
- `04-memory-compiler/phase-3.6-producer-publication-conformance.md`
- `04-memory-compiler/decision-change-log.md`

本次变更集未修改任何 D、Storage、F、I 或 A 路径。

### 5. 验证边界

文档定义了 E 的生产者协议、私有暂存、最终发布门、回执语义、重试/恢复规则与 F 交接。它不确立可执行 API、事务隔离、原子依赖登记、租约栅栏、可见性执行约束、恢复安全或运行时行为。E36-01..20 为 NOT RUN。最终提交/回读证据将在 E 分支重新抓取后的交付响应中记录。
