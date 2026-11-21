<!-- 目标：docs/zh-CN/04-memory-compiler/compiler-stage-contract.md | 插入：新增独立 Compiler Stage 契约，不修改现有契约。 -->

# Memory Compiler Stage 契约

**Work Item：** GAP-01-COMPILER-CORE-001  
**Owner：** E — Memory Compiler Architect  
**基线：** `360d88c99a47018ce78b870379be3ee43841a837`  
**状态：** CANDIDATE 实现契约；必须通过实现一致性检查。

## 1. 权威范围与边界

Memory Compiler MUST 将持久化 Accepted 的 Event 转换为具有显式 Provenance 的暂存派生。

Compiler MUST NOT 宣告 Canonical Truth、授权 Forget、批准 Schema、批准 Public API，或独立推进 Storage 可见性。

以下区分具有强制性：

- Accepted MUST NOT 等于 Compiled。
- Compiled MUST NOT 等于 Canonical。
- Staged MUST NOT 等于 Published。
- PublicationParticipant Admission MUST NOT 等于 Producer Admission 成功。
- Producer Admission MUST NOT 替代 PublicationParticipant Admission。
- `DECIDED FOR CONVERGENCE` MUST NOT 被解释为 `ACCEPTED`。

现有 Event Store Contract 继续作为 Accepted Receipt、幂等身份和 Compile Intent 持久化的权威依据。

现有 Extraction and Normalization 契约 §19.1 和 §19.2 继续作为发布顺序的权威依据。

## 2. Stage 清单

| 顺序 | Stage | 输入 | 输出 |
|---|---|---|---|
| 1 | Ingestion | Accepted Event、Receipt、持久化 Intent | Ingested Event |
| 2 | Extraction | Ingested Event、不可变 Payload | Extraction IR |
| 3 | Normalization | Extraction IR | Normalized IR |
| 4 | Staging | Normalized IR、Lineage、Dependency Registration | `PREPARED_HIDDEN` 派生物 |
| 5 | Publication Gate | Staged Derivative、权威准入证据 | Publication Disposition |

每个 Stage MUST 具有：

1. 不可变逻辑身份。
2. 显式类型化输入和输出。
3. 确定性的参数摘要。
4. 结构化 Provenance。
5. 显式失败分类。
6. 幂等 Retry 身份。
7. 可恢复执行状态。

## 3. 共享 Provenance 契约

每个 Stage 输出 MUST 携带：

| 字段 | 要求 |
|---|---|
| `source_event_id` | 精确且不可变的来源 Event Identity |
| `source_payload_digest` | 精确的 Accepted Source Digest |
| `stage_output_id` | 不可变 Stage Output Identity |
| `upstream_outputs` | 精确的上游输出身份 |
| `compiler_version` | 固定的 Compiler 实现版本 |
| `parameter_digest` | 精确 Stage 参数摘要 |
| `stage_name` | 精确的产出 Stage |
| `attempt_generation` | Worker Attempt Generation |

Provenance MUST 使用结构化数据。

Stage MUST NOT 使用展示字符串、推断身份或可变引用替换上游身份。

改变 Source Digest、Compiler Version 或有效 Stage Parameters MUST 创建不同的逻辑输出身份。

使用相同输入和参数的 Retry MUST 保持相同的逻辑 Stage Identity。

## 4. Stage 契约

### 4.1 Ingestion

**输入**

- 持久化 Accepted Event。
- 原始 Accepted Receipt。
- 精确 Source Payload Reference 和 Digest。
- 持久化 Compile Intent Record。

**输出**

- 不可变 `IngestedEvent`。
- Source Lineage。
- 原始 Receipt Identity。

**前置条件**

- Event Acceptance MUST 已经持久提交。
- Compile Intent MUST 已经持久记录。
- Scope Authorization MUST 在 Receipt Replay 之前执行。
- Payload Dereference 之前 MUST 检查 Source Authorization。

**失败语义**

- Receipt 缺失：`REJECTED`。
- Compile Intent 缺失：`BLOCKED`。
- Payload Digest 不匹配：`FAILED`。
- Authorization 未知：失效关闭（fail closed）。
- 重复 Accepted Event：返回现有逻辑 Ingestion 结果。

**幂等性**

Ingestion Identity MUST 根据 Accepted Event Identity 和 Source Digest 确定。

**可重入性**

Ingestion MAY 在 Crash Recovery 后重新进入。重新进入 MUST NOT 创建第二个 Accepted Receipt 或 Compile Intent。

### 4.2 Extraction

**输入**

- `IngestedEvent`。
- 不可变 Payload。
- Extraction Parameter Set。
- 当前 Authorization Evidence。

**输出**

- `ExtractionIR`。
- Source Spans 和 Source Locators。
- Extraction Method Receipt。
- Provenance。

**前置条件**

- Ingestion MUST 完成。
- Payload Integrity MUST 根据 Accepted Digest 验证。
- Source Authorization MUST 处于当前有效状态。
- Scope MUST 保留。
- MUST 评估当前 Forget Fence。

**失败语义**

- Source Span 无效：`FAILED`。
- 不支持的 Modality：`REJECTED`。
- 内容存在歧义：在 IR 中保留歧义。
- Model 不可用：`RETRYABLE`。
- Policy 或 Fence 状态未知：失效关闭（fail closed）。

**幂等性**

Extraction Identity MUST 根据 Event Identity、Source Version、Digest、Scope、Parser Version、Model Version 和 Policy Version 确定。

**可重入性**

相同 Extraction Identity MUST 返回相同持久化结果，或者恢复同一个未完成 Attempt。

Parser 部分失败 MUST NOT 将不完整内容静默提升为完整 Extraction。

### 4.3 Normalization

**输入**

- `ExtractionIR`。
- 显式 Normalization Parameters。
- 上游 Provenance。

**输出**

- `NormalizedIR`。
- 标准化时间与文本表示。
- 未解决歧义记录。
- Provenance。

**前置条件**

- Extraction MUST 完成。
- 每个标准化元素 MUST 保留 Source Lineage。
- Scope 和 Epistemic Distinctions MUST 保留。
- Normalization MUST NOT 发明 Canonical Identity。

**失败语义**

- 转换无效：`FAILED`。
- 时间值无法解析：保留 `UNKNOWN`。
- Entity 存在歧义：保留歧义。
- 不支持的语义转换：`REJECTED`。

**幂等性**

相同 IR 和 Parameter Digest MUST 产生相同逻辑 Normalized Output。

**可重入性**

Normalization MUST 能够重新启动，且 MUST NOT 改变上游 Extraction IR。

### 4.4 Staging

**输入**

- `NormalizedIR`。
- 完整的直接与传递 Dependency Set。
- Provenance。
- 成功的 Producer Admission Evidence。
- 可用时的权威 Canonical Commit References。

**输出**

- 不可变 Staged Derivative。
- 完整 Lineage Registration。
- Dependency Registration Identity。
- Publication Tuple Identity。
- `PREPARED_HIDDEN` 状态。

**前置条件**

- Producer Admission MUST 成功。
- 精确 Producer Participant MUST 已持久记录。
- `DependencyClosurePersisted(P)` MUST 等于 TRUE。
- 精确 Dependency Closure MUST NOT 缩小。
- D Canonical Commit MUST 满足 §19.1 顺序。
- Storage MUST 将精确 Publication Tuple 持久化为 `PREPARED_HIDDEN`。

**失败语义**

- Dependency Closure 不完整：`BLOCKED`。
- Producer Admission 缺失：`REJECTED`。
- Canonical Commit 缺失：`BLOCKED`。
- Storage Preparation 失败：`FAILED`。
- Dependency Persistence 未知：失效关闭（fail closed）。

**幂等性**

Staging MUST 使用精确 Operation Identity 和不可变上游 Lineage。

对于已经终态拒绝的 Operation，Retry MUST NOT 创建替代 Publication Identity。

**可重入性**

Staging MUST 在 Crash Recovery 后恢复原始 Staged Identity。

**可见性**

暂存派生 MUST 在以下条件全部满足前保持不可见：

1. 完整 Lineage 已持久登记。
2. 完整 Dependency Closure 已持久登记。
3. 必需 Canonical Commits 已确认。
4. 精确 Storage Tuple 已持久化为 `PREPARED_HIDDEN`。
5. PublicationParticipant Admission 成功。
6. 受保护的可见性处理授权推进。

`PREPARED_HIDDEN` MUST 使用现有 §19.2 的语义。MUST NOT 引入独立的暂存可见性状态。

### 4.5 Publication Gate

**输入**

- 精确 Staged Derivative。
- 精确 Publication Tuple。
- PublicationParticipant Identity。
- 当前 Forget Fence Evidence。
- 权威 Storage Preparation Evidence。
- Canonical Commit Evidence。

**输出**

以下之一：

- `PUBLISHED`
- `SUPPRESSED`
- `BLOCKED`
- `FAILED`

**前置条件**

- 精确 Staged Identity MUST 验证。
- Successful Producer Admission MUST 独立验证。
- Successful PublicationParticipant Admission MUST 独立验证。
- Storage MUST 确认精确的 `PREPARED_HIDDEN` Tuple。
- Dependency Closure MUST 保持完整。
- 当前受保护的可见性授权 MUST 已经建立。

**失败语义**

- 第二阶段准入被拒绝：`SUPPRESSED`。
- Evidence 缺失：`BLOCKED`。
- Evidence 冲突：失效关闭（fail closed）。
- Fence 未知：`BLOCKED`。
- Worker Generation 过期：`SUPPRESSED`。
- Storage 可见性推进失败：保留隐藏状态，或者恢复权威终态处置。

**幂等性**

Publication MUST 对精确 Publication Identity 保持幂等。

Retry MUST NOT 将已拒绝的 PublicationParticipant Admission 转换为成功准入。

**可重入性**

Publication Recovery MUST 查询权威终态证据。MUST NOT 从 Worker Local State 重建授权。

## 5. Publication 顺序

以下顺序 MUST 保持：

1. 解析 I Authorization 和 Scope。
2. D Forget Fence 评估及 Producer Admission。
3. 完整 Dependency Registration 持久化。
4. E 私有不可变 Staging。
5. D ClaimRevision/FactRevision Canonical Commit。
6. Canonical Revisions、Dependency Registration 和 Publication Intent 的可恢复关联。
7. E Publication Preparation。
8. 确认所有必需记录后进行 Storage 受保护的可见性推进。
9. G 使用精确不可变 Canonical Revision References 提交 ContextVersion。
10. Logical Completion。

§19.2 中额外的 PublicationParticipant Admission 顺序 MUST 保持：

1. Producer Admission 和 Participant 持久记录。
2. Dependency Closure Registration。
3. D Canonical Commit。
4. Storage 持久化 `PREPARED_HIDDEN` Tuple。
5. PublicationParticipant Admission。
6. 受保护的可见性处理。

两个准入操作 MUST 保持独立。

ForgetFence/Admission Ordering Anchor 与 per-BrainAuthorityRef Serialization Anchor MUST 指向同一个权威 Ordering Anchor。

## 6. 执行与恢复状态机

Compiler Execution State MUST 使用以下生命周期：

```text
PENDING
   |
   v
LEASED
   |
   v
RUNNING
   |
   v
STAGED
   |
   v
PREPARED_HIDDEN
   |
   v
PUBLICATION_ADMISSION
   |
   +------> PUBLISHED
   |
   +------> SUPPRESSED
   |
   +------> BLOCKED
   |
   +------> FAILED
```

终态：

- `PUBLISHED`
- `SUPPRESSED`
- `FAILED`

`BLOCKED` MUST 保持可恢复，MUST NOT 被视为成功终态。

### 6.1 Retry

- 可重试失败 MUST 返回 `PENDING`。
- Retry MUST 保留逻辑 Stage Identity。
- Retry MUST 增加 Attempt Generation。
- 已终态 Suppressed 的 Publication MUST NOT 在同一 Identity 下重试为发布成功。
- 独立授权的 Operation MUST 使用新的 Operation Identity。

### 6.2 Lease

- Worker MUST 在执行 Stage 前持有有效 Lease。
- Lease Ownership MUST 标识 Worker、Operation 和 Generation。
- Lease 过期 MUST 使旧 Generation 失去 Publication 资格。
- Lease Renewal MUST NOT 改变逻辑 Output Identity。
- 并发 Lease Acquisition MUST 由权威 Lease Provider 串行化。

### 6.3 Crash Recovery

- 已完成 Stage MUST 具有持久化结果和可恢复的下一阶段 Intent。
- Recovery MUST 识别最后一个持久化 Stage Result。
- Recovery MUST 从该结果恢复，MUST NOT 重复已经产生的外部可见效果。
- 未知 Commit Outcome MUST 保持未解决。
- Recovery MUST 使用原始 Operation Identity。
- 敏感处理之前 MUST 重新检查 Authorization 和 Forget Fence。

### 6.4 Late-worker Suppression

Lease Generation 已过期的 Worker MUST NOT 发布。

Late Worker MUST NOT：

- 覆盖更新的 Stage Result。
- 替换终态处置。
- 恢复已经 Suppressed 的派生物。
- 推进 Storage Tuple。
- 将 `PREPARED_HIDDEN` 转换为可见状态。
- 重用被拒绝的 PublicationParticipant Identity。

权威 Publication Boundary MUST 拒绝过期 Generation。

精确 Publication Identity 的终态处置 MUST 不可变。

## 7. Evidence 与 Provenance

每个输出 MUST 保留：

- 精确来源 Event Identity。
- Source Digest。
- 精确上游 Output Identities。
- Compiler Version。
- Parameter Digest。
- Stage Identity。
- Attempt Generation。
- 持久化 Dependency Registration Identity。
- 适用时的 Publication Identity。

Evidence MUST 区分直接来源证据和派生解释。

Extraction MUST NOT 伪造 Source Span。

Normalization MUST NOT 删除未解决歧义。

Staging MUST NOT 宣告 CandidateProposition 为 Canonical。

Compiler MUST 保留 D 已有的 Claim Identity 决策，MUST NOT 将其扩展为未经批准的 Fact-specific Modeling。

## 8. 跨 Owner 权威边界

| 操作 | 必需权威 | E 的权限 |
|---|---|---|
| Accepted Receipt | Event Store | 仅消费 |
| Producer Admission | D 权威 Fence/Admission | 调用并保留精确证据 |
| Dependency Closure | 权威 Dependency Registrar | 提交精确 Dependency Set |
| ClaimRevision Commit | D | 提交候选材料 |
| FactRevision Commit | D | 记录未解决依赖 |
| `PREPARED_HIDDEN` 持久化 | Storage | 提交精确 Publication Tuple |
| PublicationParticipant Admission | D 权威 Fence/Admission | 调用并保留精确证据 |
| 受保护的可见性推进 | Storage 及适用的 D/I Authorization | 不具有独立授权权 |
| ContextVersion Commit | G | 提供精确不可变引用 |
| Forget Authorization | I/D 权威策略边界 | 重新检查并遵守 |

E MUST NOT 实现替代授权决策。

E MUST NOT 引入第二个 Forget Fence、独立 Ordering Anchor 或独立 Publication Transaction Domain。

## 9. 实现一致性

参考 Crate MUST 实现确定性的进程内 Stage 执行和类型安全的 Stage 边界。

参考 Crate MUST NOT 声称具有生产级持久化、分布式原子性、Canonical Commit Authority 或生产 Publication Authorization。

每项未实现的权威集成都 MUST 使用 `NOT IMPLEMENTED` 显式标注，并给出具名依赖。

Schema、DDL、Public API、H Wire Format、Production Keys、Trust Root、Crypto Profile 和 Storage L4 Approval 均保持 `NOT APPROVED`。

---

## 9. 已执行的验证

| 检查 | 命令 | 结果 |
|---|---|---|
| 构建 | `cargo build --offline -p memory-compiler` | PASS，0 警告 |
| 测试 | `cargo test --offline -p memory-compiler` | PASS，11 通过 / 0 失败 |
| 依赖 | `Cargo.toml` 的 `[dependencies]` | 为空——纯 Rust，无 SQLite、无网络、无模型提供方 |

实际使用的工具链：`cargo 1.100.0` / `rustc 1.100.0`。

本 crate 刻意不依赖任何东西。任何依赖 `libsqlite3-sys` 的 crate 在当前环境无法构建，因为本机
`gcc` 缺少 `cc1`；这是环境缺陷，不是本 crate 的缺陷，也正是本 crate 不携带存储依赖的原因。

这 11 个测试证明了什么：stage 管线独立执行两次准入，在六个条件全部成立之前拒绝暂存可见性，
抑制过期的 worker generation，并要求完整依赖闭包。它们没有证明什么：任何真实 Event Store、
Storage 适配器、Fence 或授权服务的性质——这些在此均未实现。

