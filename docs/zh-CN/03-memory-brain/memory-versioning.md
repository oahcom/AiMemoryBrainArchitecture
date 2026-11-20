# Memory Versioning 与历史语义

- 文档 ID：D-VERSIONING-001
- 版本：1.0
- 源分支：session-d-memory-brain-2026-11-16
- 源文件版本：DEREFERENCED — 保留历史源 Blob `af747f339d03bdd4684b6ed60fca05957dc8e1fb`；原规范源路径在当前 main tree 中不存在。
- 审查时源分支 HEAD：6b654d5cffaeb71b01f2b0750daa0abc14eb64b3
- 源规范：DEREFERENCED — 原规范源路径 `03-memory-brain/memory-versioning.md` 在当前 main tree 中不存在；替代物：[现存英文对照文本](../../en/03-memory-brain/memory-versioning.md)（仅供阅读，不是规范性替代源）。
- 对应英文：[Memory Versioning and Historical Semantics](../../en/03-memory-brain/memory-versioning.md)
- 状态：Claim identity 与不可变 ClaimRevision 语义已 DECIDED FOR CONVERGENCE（Option A）；具体 Schema 表示与精确事务/时间表示仍为 CANDIDATE/OPEN
- 相关问题：INT-P0-01/03、INT-P1-01/02/06；DM-002/003/006/008/009/013

## 1. 目的

定义 Canonical Memory、Claim、Entity 和 Relation 的变更如何表示，以避免破坏性覆盖；提供确定性的历史查询、并发控制、幂等性、协调和感知 Forget 的历史语义。

## 2. 范围与所有权

覆盖 MemoryVersion、候选 ClaimRevision、EntityVersion、RelationRevision、LifecycleEvent Sequence、Canonical Commit Receipt、时间语义、历史引用解析和迁移记录。ContextVersion 和 ChangeSet 明确由 G 拥有。

D 定义不可变修订语义和 Parent 关系；Canonical Store 持久化 Revision/Commit Record；Lifecycle Manager 拥有 Lifecycle Event；B 拥有领域/认知/时间语义；I 拥有授权和 Forget Policy。

## 3. 职责与非职责

职责：定义不可变 Revision Identity/Parent；定义 CAS 和 Stale-write 行为；分别保留 Valid Time 与 Record/Transaction Time 历史；提供精确历史/As-of 读取；使 Retry 幂等并显式暴露 Conflict；保留 Entity Merge/Split 和 Relation Migration 历史；协调 Version/Dependency 枚举与 Forget。

不负责 ContextVersion 状态机、Delivery/Applied、Event Ingestion Sequence、BMCP Version 协商、全局 Permission Policy、Storage Engine 选型或物理擦除策略。

## 4. 领域对象

- **MemoryVersion：** 单个 Memory 的不可变 Snapshot；Per-Memory 单调 Sequence、Parent Version、Canonical Commit Sequence、Digest、Actor、Reason、Schema Version、Recorded Time、引用和内容快照。
- **ClaimRevision（身份/修订语义：DECIDED FOR CONVERGENCE — Option A；具体 Schema 表示：CANDIDATE）：** 稳定 Claim Identity 的不可变修订语义；以下字段仅为候选表示：Revision ID、Claim ID、Sequence、Parent Revision、命题、Epistemic Status、Valid Time、来源/Evidence 引用、Provenance 引用、ScopeRefs、Actor、Recorded Time、Method 和 Digest。Fact 专属建模和 Fact 批准继续保持 OPEN。
- **EntityVersion：** 稳定 Entity ID 的不可变属性/别名档案修订。
- **RelationRevision：** 稳定 Relation ID 的不可变 Predicate/Endpoint/Validity/Evidence/Lifecycle 修订。
- **LifecycleEvent：** 权威的追加式状态转换记录，具有 Per-Aggregate Sequence；当前状态通过 Fold/Projection 得出。
- **CanonicalCommitReceipt：** Idempotency Key、Request Digest、Expected Base、Committed Version、Commit Sequence、Outcome 和 Timestamp。
- **MigrationRecord：** 明确的旧/新类型化引用、操作类型、映射/分区、Actor、Evidence、Scope、Sequence 和 Reason。

## 5. 数据模型与时间语义

所有 Revision 都不可变、使用不透明 ID 寻址、带 Schema Version 且绑定 Scope。除 Genesis 外，每个 Revision 都有一个 Parent。分支/Fork 不得静默合并：Canonical Aggregate Head 通过 CAS 推进；竞争 Revision 成为被拒提案或明确的协调候选。

时间轴：
- Event Time：被描述事件实际发生的时间。
- Recorded At：Brain 接受/记录信息的时间。
- Valid Time：命题/关系声称成立的区间。
- Commit/Transaction Time：Canonical Version 成为权威的时间。

候选 TimeValue 字段：lower_bound、upper_bound、precision、timezone、certainty、original_phrase、source_ref。TimeInterval 包含 start/end TimeValue、左闭右开边界约定，以及显式 Unknown/Unbounded 标记。Unknown 不等于 Infinity；缺失不代表永远有效。

历史查询契约：“在 T 时有效”按 Valid Time 过滤；“在 T2 时已知”按 Canonical Transaction/Record Time 过滤。结果标识准确 Revision/Version，以及它是 Current、Superseded、Retracted、Archived 还是因 Forget 不可用。

## 6. Claim Identity 备选方案（INT-P1-02）

| 维度 | Option A：稳定 Claim ID + 不可变 ClaimRevision | Option B：每次修正/后继都创建新 Claim ID |
|---|---|---|
| 身份 | 命题线程跨 Revision 持续；Revision 标识准确声明 | 每次声明/修正都是新身份，通过 Successor 关联 |
| Evidence | 链接到准确 Revision；共享 Evidence 显式关联 | 自然绑定 Claim，但重复链接会增多 |
| Lifecycle | 追加 Epistemic Status Revision；Retraction 是 Revision/Event | 旧 Claim Retract，再创建 Successor/新 Claim |
| Versioning | MemoryVersion 固定 ClaimRevision ID | MemoryVersion 固定 Claim ID；修正会导致身份变化 |
| Conflict | ConflictSet 引用准确 Revision | ConflictSet 引用不同 Claim Identity |
| Query | “当时已知的 Claim”需要选择 Revision | 不可变声明查询更简单；演进命题的聚合更困难 |
| Permissions | Scope 作用于 Claim Identity 和每个 Revision | 每个新 Claim 分别评估 Scope；Successor Link 另行授权 |
| Storage | Revision Table + Identity Index | 更多 Identity 和 Successor Graph |

**DECIDED FOR CONVERGENCE — Option A：** 稳定 Claim 身份加不可变 ClaimRevision。它在保持每条历史声明不可变的同时，提供持久引用身份。Correction 创建新 Revision 和明确的 Correction/Supersession Relation；Retraction 创建新的 Epistemic Revision/Event，不删除先前声明。Option B 继续作为身份模型备选方案保留，但不属于本次选定的收敛方向。如果 ADR 批准独立 Fact 对象，FactRecord 具有自己的不可变 Revision Stream，并链接到其 Attest 的准确 ClaimRevision。

本决策仅确定身份语义，不批准 Claim/Fact Schema、DDL、公共 API 或 Wire Contract。

## 7. 状态机

Revision：Draft → Validated → Committed。Committed Revision 不可变；后继 Revision 指向之前已提交 Revision。Retraction 是新的 Revision/Status Event，不是修改旧 Revision。Lifecycle 独立，由 Lifecycle Manager 管理。

Entity/Relation Version 使用相同的追加式 Parent/CAS 模式。Merge/Split 创建 Migration Record，不改写旧引用。ContextVersion/ChangeSet 是 G 拥有的独立对象，并固定 MemoryVersion ID。

## 8. 操作与并发

操作：ReadHead；ReadRevision；ReadAsOf(valid_at, known_by)；CommitRevision(expected_parent)；RetractClaim(expected_revision)；SupersedeRelation；MergeEntity；SplitEntity；ReconcileConflict；ResolveHistoricalRef；EnumerateVersionDependenciesForForget。

并发更新：
1. 客户端读取 Head Revision/Version。
2. 使用 Expected Parent 和 Idempotency Key 提交修改。
3. Brain 校验 Schema、Scope、Permission 结果、引用和 Evidence。
4. CAS 只推进一次 Head。
5. 失败方收到 STALE_VERSION；若授权允许，附带当前可见 Head 引用。
6. 调用方重新读取并提交协调后的新操作；不得自动 Last-write-wins。

Idempotency Key 的范围由 ActorRef + Operation + Resource + 相关 ScopeRef 确定；Request Digest 绑定 Canonical Payload。相同 Key/相同 Digest 返回原 Receipt；相同 Key/不同 Digest 产生 Conflict。Receipt 保留必须与 Forget/Retention 协调，不能保留已遗忘内容。

## 9. 不变量

- 已提交 Revision 不得原地更新。
- 每个 Revision 都有稳定身份和 Parent Lineage。
- 每个 Aggregate 同时只有一个权威 Head；并发 Fork 必须显式协调。
- 历史查询返回准确 Revision Identity 和时间依据。
- Event、Valid、Recorded 和 Transaction Time 不得混淆。
- Correction 不得静默改写过去有效性或 Epistemic Status。
- Merge/Split 和 Relation Migration 保留历史引用。
- Context 引用固定准确 MemoryVersion，而不是会变化的 Current Pointer。
- Forget 可以使内容不可用，但不得伪造历史 Sequence 元数据。

## 10. 接口

E 提交带 Expected Base、Source Event/Evidence Ref、Provenance、Actor/Scope/Time 和 Idempotency 的 Candidate Revision。Brain 返回已接受的 Canonical Revision/MemoryVersion 引用，或结构化 Conflict/Defer。F 读取准确 Revision/As-of State，并暴露陈旧/部分 Projection。G 在 Context Entry 中保存 Memory ID + MemoryVersion ID，并独立管理 Context/ChangeSet Version（INT-P1-01）。H 序列化不透明 Version 引用。I 授权 Revision/Forget，并定义哪些历史元数据可保留。跨模块操作按需携带 Schema Version、ActorRef、ScopeRefs、Correlation/Causation 和 Idempotency。

## 11. 错误处理

STALE_VERSION；REVISION_PARENT_MISMATCH；IDEMPOTENCY_CONFLICT；INVALID_TIME_INTERVAL；TIME_PRECISION_LOSS；SCOPE_MISMATCH；PERMISSION_DENIED；REVISION_NOT_FOUND_OR_NOT_VISIBLE；HISTORY_UNAVAILABLE_DUE_TO_FORGET；MIGRATION_MAPPING_INCOMPLETE；SCHEMA_VERSION_UNSUPPORTED。

## 12. 一致性

Aggregate Head 更新和不可变 Revision 追加，必须与 Receipt/Outbox 原子提交。历史读取使用已提交 Transaction Sequence，而不是 Projection 到达顺序。LifecycleEvent Sequence 在每个 Memory Aggregate 内唯一，并确定性折叠。Projection Rebuild 记录 Watermark 和 Schema 兼容性。Entity/Relation Migration 和 Successor Ref 与 Canonical Version/Outbox Intent 一起提交。

## Claim/Fact 端到端受保护发布协议

### 1. 逻辑事务边界

端到端协议 MUST 在以下环节之间保持统一、可审计的逻辑顺序：

- Authorization 与 Scope 解析。
- 在串行化、可恢复的 Admission 边界内检查 Forget Fence 并执行 Producer Admission。
- 在同一受保护 Admission 边界内持久化登记完整的直接及传递依赖集合。
- E 创建私有不可变 Staging 产物，不产生公开可见性。
- D 规范 ClaimRevision/FactRevision 提交，包括精确 Parent 链接、授权证据和必需 Provenance 引用。
- 以原子或可恢复方式，将已提交 Revision 与依赖登记及 Publication Intent 关联。
- 通过幂等、可恢复的协议完成 E Publication。
- 只有在必需规范记录和依赖登记得到确认后，才能推进 Storage Visibility。
- G 在同一受保护可见性边界内提交 ContextVersion，并引用精确的规范 Revision。
- 只有全部必需可见性条件满足后，才能标记逻辑操作完成。

协议 MUST NOT 将任何中间状态暴露为完整发布状态。

G ContextVersion 提交及参与方协调 MUST 遵循适用的权威 Visibility Outcome。

### 2. 必需顺序

规定的逻辑顺序如下：

A. 解析授权与 Scope。

B. 在同一个串行化、可恢复的 Admission 边界内检查当前 Forget Fence，并执行 Producer Admission。

C. 在同一受保护 Admission 边界下，持久化登记完整的直接及传递依赖集合。

D. 创建 E 私有不可变 Staging 产物。Staging MUST NOT 产生公开可见性。

E. 在 D 的规范提交边界内提交 ClaimRevision 和 FactRevision、精确 Parent 链接、授权证据及必需 Provenance 引用。

F. 以原子或可恢复方式，将已提交 Revision 与依赖登记及 Publication Intent 关联。

G. 通过幂等、可恢复的发布协议完成 E Publication。

H. 只有在必需规范记录和依赖登记得到确认后，才能推进 Storage Visibility。

I. G 必须在同一受保护可见性边界内提交 ContextVersion，并引用精确的规范 Revision。

J. 只有全部必需可见性条件满足后，才能将逻辑操作标记为完成。

#### 端到端事务顺序图

以下图是上述规范 A-J 顺序的独立执行视图。
箭头表示必需的推进顺序，不表示各步骤可以独立提交事务。

```
[1] Authorization / Scope（授权与 Scope）
      |
      v
[2] D Fence
      |
      v
    Admission（Producer Admission）
      |
      v
[3] Dependency Registration（依赖登记）
      |
      v
[4] E Staging（私有、不可变）
      |
      v
[5] D Canonical Commit（D 规范提交）
      |
      v
[6] Association（关联）
    （规范 Revision + 依赖 Receipt
     + Publication Intent）
      |
      v
[7] E Publication（E 发布）
      |
      v
[8] Storage Visibility（Storage 可见性）
      |
      v
[9] G Context Commit（G Context 提交）
      |
      v
[10] Logical Completion（逻辑完成）
```

Fence-first 分支（T17）：

```
D Fence 先于 Admission 线性化
      |
      +--> Admission MUST 拒绝
      +--> 步骤 3-10 MUST NOT 执行
```

Participant-first 分支（T18）：

```
+------------------------------------------------------+
| 权威串行化 Fence / Admission 边界                    |
|                                                      |
| Producer Admission + 精确 Participant 记录           |
| 作为一个不可分割操作完成持久化                        |
| (Participant 持久化失败 => Admission                 |
|  MUST NOT 报告成功)                                  |
+------------------------------------------------------+
                    |
                    v
      Admission 成功结果变为可观察
                    |
                    v
      后续 Fence MUST 等待该精确 Participant 记录
      对其 Participant Barrier 持久可见
```

组件职责边界：

- D Fence：权威 Forget Fence 顺序及线性化。
- Admission：串行化 Producer Admission，并原子持久化
  准确 Participant 记录。
- D Canonical Commit：不可变规范 Revision 提交、
  准确 Parent/Reference 绑定和持久 Receipt。
- E Publication：对已准入、已提交的规范对象进行幂等发布。
- Storage Visibility：所有必需规范记录及依赖记录确认后，
  才能推进 Storage 可见性。
- G Context Commit：使用准确规范 Revision 引用，
  提交不可变 ContextVersion。

恢复边界（规范故障矩阵：§16.1）：

- UNKNOWN：保持非最终状态，不得推断成功。
- Crash：使用原始逻辑 Operation Identity 恢复。
- Lost ACK：查询原始操作和 Receipt，不得创建第二次逻辑提交。
- Retry：复用原始 Idempotency Identity，
  协调已有 Participant/Publication 状态。

任何恢复路径都不得绕过必需顺序、T17、T18
或权威六组件故障矩阵。


### 2.1 T17 — Fence-first（Fence 优先）

如果 Forget Fence 先于 Producer Admission 线性化，则该 Fence MUST 阻止相关操作获得准入并进入发布流程。

不得通过任何 Staging、规范提交、Publication Intent 或 Visibility 转换绕过这一决定。

### 2.2 T18 — Participant-first（参与者优先）

Producer Admission 一旦成功线性化，该精确操作 MUST 被持久化登记为 Participant。

Producer Admission 成功与精确已准入 Participant 的
持久化记录 MUST 在权威串行化 Fence/Admission 边界内
构成一个不可分割的操作。

后续 Forget Fence MUST NOT 在其 Participant Barrier
评估线性化或完成之前，越过尚未对该 Barrier 持久可见的
已准入 Participant 记录。

后续 Forget Fence MUST NOT 静默跳过、删除或错误分类该已准入参与者。

必须依据串行化的 Fence/Admission 顺序协调该操作。

其完成或抑制结果 MUST 遵循声明的 Forget Policy，并保留精确参与者身份、依赖闭包和可审计结果。

在权威操作结果得到解决之前，UNKNOWN MUST 保持非最终状态。

恢复 MUST 使用原始操作身份，并协调 Fence、Admission、依赖登记、规范提交、E Publication、Storage Visibility 和 G ContextVersion 状态。

恢复 MUST NOT 根据缺失证据制造成功的最终状态。
### 3. Staging 与依赖不变量

Staging 是私有状态，不等于 Publication。

依赖枚举 MUST 先于持久化依赖登记。

依赖登记必须在规范发布获得可见资格之前完整完成。

依赖状态 UNKNOWN 或不完整时，必须保持私有，不得准入为完整准备状态的发布。

### 4. 规范提交不变量

ClaimRevision 和 FactRevision 是不可变规范修订。

D 的规范提交 MUST 绑定：

- 精确修订身份和 Parent 链接。
- Aggregate Head CAS 更新。
- 精确 Claim/Fact 交叉引用。
- Evidence 和 Provenance 依赖引用。
- Scope 和时间元数据。
- Fact Attestation 所需的有效 I AuthorizationDecisionRef。
- 必需 Forget 依赖登记。
- CanonicalCommitCursor 分配。
- 持久提交 Receipt 和可恢复 Outbox Intent。

必需授权证据或依赖登记缺失时，不得报告 Revision 已提交。

Lost ACK 必须使用原始幂等身份和精确请求 Digest 查回，不得创建第二个 Revision。

### 5. PREPARED_HIDDEN 与 Admission 不变量

Producer Admission MUST 在串行化、可恢复的 Admission 边界内线性化，并且必须先于依赖登记和 E Staging。

Admission 只有在精确 Participant 记录已持久化提交后，
才能报告成功。

Participant 记录持久化失败 MUST 导致 Admission 失败，
或保持非成功状态。

Forget Fence MUST 等待权威 Fence/Admission 边界确定
Admission 是否已成功提交，不得忽略 Participant 记录
尚未完成或结果尚未解决的已准入操作。

精确的已准入操作 MUST 被持久化登记为 Participant。

如果 Forget Fence 先于 Producer Admission 线性化，则该 Fence MUST 阻止相关操作进入依赖登记、E Staging、规范提交或 Publication。

后续 Forget Fence MUST 按照权威 Fence/Admission 顺序处理所有此前已经准入的 Participant，不得静默跳过或错误分类已准入参与者。

PREPARED_HIDDEN 仍然是持久化但非公开的 Publication 状态。

Prepared Publication Tuple MUST 绑定到精确的既有准入操作及其依赖登记证据。

不得仅凭 PREPARED_HIDDEN 的存在推断 Producer Admission 已经发生。

Storage 只有在精确准入参与者、依赖登记、Prepared Tuple 和适用 Forget Fence 条件全部得到验证后，才能推进最终 Visibility。

### 6. I Commit Authorization

I MUST 授权精确操作及适用 Publication Tuple。

授权决定 MUST 绑定其身份、有效期、撤销状态、Scope 和适用 Policy Version。

授权缺失、歧义、过期、撤销或无法验证时，必须阻止最终 Visibility。

### 7. Storage Visibility

只有在此前规范提交、PREPARED_HIDDEN 和 Admission 要求全部满足后，Storage 才能执行最终 Visibility。

Visibility 转换 MUST 保持适用的 per-BrainAuthorityRef Serialization Anchor。

不得使用进程内事务、异步消息、重试或参与方独立成功替代受保护排序。

### 8. G Context 可见性

引用 ClaimRevision、FactRevision 或派生资产的 ContextVersion MUST 绑定精确不可变 Revision 引用和适用 ForgetFenceCursor。

G MUST：

- 重新验证当前 I 授权。
- 重新验证适用 D Forget Fence。
- 验证所有被引用的 Claim/Fact Revision。
- 验证完整 Dependency Registration Receipt。
- Context 包含已发布 Artifact 时，验证精确 Storage Visibility Outcome。
- 通过受保护可见性协议提交不可变 ContextVersion。
- 只有权威提交结果得到确认后才允许发布。

后续 Forget 不会因为 ContextVersion 曾经提交就赋予永久访问权。历史 Context 读取和 Replay 仍必须重新执行当前授权和 Forget 抑制检查。

### 9. UNKNOWN、Lost ACK 与恢复

如果参与方返回 UNKNOWN 或丢失 ACK：

- 操作 MUST 保持可恢复的非最终状态。
- Retry MUST 使用相同操作身份和幂等范围。
- 参与方 MUST 先解析先前操作结果，再创建第二次逻辑提交。
- 不得出现重复可见的 ClaimRevision、FactRevision、Publication 或 ContextVersion。
- 不得根据超时推断操作完成。

崩溃后，恢复过程 MUST 检查权威操作记录并协调：

- ForgetFence 状态。
- 依赖登记。
- Claim/Fact 规范提交。
- PREPARED_HIDDEN Publication Tuple。
- PublicationParticipant Admission。
- I Commit Authorization。
- Storage Visibility。
- D/E 参与方终结。
- G ContextVersion 状态。

恢复 MUST 完成同一个逻辑操作，或者将其保留为未完成/未知状态。

恢复 MUST NOT 根据缺失证据制造成功的最终状态。

### 10. Storage 边界

既有 Storage L1 决策保持不变。

本协议定义逻辑顺序、受保护发布及外部可观察的一致性要求。

它不选择或批准物理数据库、部署拓扑、HA/PITR 策略或 Storage L4 设计。

Storage L4 继续保持 OPEN / NOT APPROVED。

## 13. 安全 / Scope

每个 Revision 都携带或继承明确解析的 Ownership/Applicability ScopeRef，并遵循文档化继承规则；不得扩大 Scope。授权必须同时检查 Identity 和准确 Revision。Evidence Ref 独立授权。历史查询不能绕过当前 Policy 或 Forget Suppression。不得从 Revision Snapshot、Log、可逆辅助数据、Cache 或 Provenance 摘录中重建已遗忘 Payload。

## 14. 性能

候选优化：不可变 Snapshot + 紧凑 Current Projection + 周期性派生 Snapshot。限制历史扫描、Parent Chain 深度、Relation Migration 扇出和 Conflict 查询窗口。基准测试 Snapshot 频率、写放大、Temporal Index 选择性、CAS 竞争和历史读取延迟。压缩必须保留所需 Lineage/Retention 义务。

## 15. 可观测性

记录 Aggregate ID、Version/Revision ID、Parent ID、Commit Sequence、Actor/Scope ID、Request Digest、Idempotency Outcome、CAS Conflict、Schema Version、Transaction/Recorded/Valid Time 和 Projection Watermark。指标包括历史深度、Conflict Rate、Stale-write Rate、Reconciliation Latency 和历史查询 Partial Rate。

## 16. 故障场景

- 并发更新：一个 CAS 获胜；失败方协调。
- 响应丢失后的重复 Retry：返回原 Receipt。
- 相同 Idempotency Key 搭配修改后的 Payload：拒绝。
- Projection 滞后：准确 Canonical Read 仍可用，或明确返回降级结果。
- 未知 Schema：安全失败；绝不静默重新解释字段。
- Merge/Split Projection 失败：重放 Migration Record。
- Forget 删除 Payload：只保留 I 批准的不可反向重建审计状态；历史内容读取返回 Unavailable。
- Clock Skew：保留来源时间/精度并独立记录 Commit Time；不得仅按客户端时间戳排序。

### 16.1 受保护发布与 Forget Barrier 故障矩阵

以下矩阵对逻辑 Claim/Fact 发布操作具有规范效力。

六个组件顺序如下：

1. D Fence
2. Admission
3. D 规范提交
4. E Publication
5. Storage Visibility
6. G Context Commit

Producer Admission 成功与精确已准入 Participant 的
持久化记录 MUST 在权威串行化 Fence/Admission 边界内
构成一个不可分割的操作。

后续 Forget Fence MUST NOT 在已准入 Participant
记录对该 Barrier 持久可见之前，线性化或完成
Participant Barrier 评估。

| 场景 | D Fence | Admission | D 规范提交 | E Publication | Storage Visibility | G Context Commit | 禁止的半发布或重复可见效果 |
|---|---|---|---|---|---|---|---|
| Fence before Admission（T17） | Fence 先线性化 | MUST 拒绝准入 | MUST NOT 提交 | MUST NOT 发布 | MUST NOT 推进 | MUST NOT 提交 | 不得出现任何规范 Revision、Artifact、Serving Reference 或 ContextVersion |
| Fence after Admission（T18） | Fence 发现持久 Participant | 原已准入操作保持可识别 | 按声明的完成/抑制策略处置 | 仅授权终态结果可发布 | 仅授权终态结果可推进 | 仅精确授权结果可提交 | Fence MUST NOT 在遗漏已准入 Participant 的情况下完成屏障 |
| Crash after Admission | 保留持久 Fence/Admission 结果 | 以原始 Operation identity 恢复 Participant 记录 | 不得推定提交 | 不得推定发布 | 不得推定可见 | 不得推定 Context 提交 | 不得出现无持久 Participant 记录却成功的 Admission；不得重复 Participant |
| Crash after Canonical Commit | 保留 Participant 与 Fence 状态 | 解析原 Admission | 恢复精确规范 Receipt | Publication 保持可恢复且幂等 | MUST NOT 暴露缺少发布前置条件的可见性 | MUST NOT 早于必要可见性提交 | 不得出现半发布规范状态；不得重复 Revision 或 Receipt |
| Lost ACK | 保留权威操作状态 | 查询原始 Operation identity | 返回原提交 Receipt | 解析原 Publication identity | 返回原可见性结果 | 解析原 ContextVersion identity | ACK 丢失 MUST NOT 产生第二个逻辑操作或重复可见效果 |
| Retry | 复用原始 Operation identity 与请求摘要 | 返回原准入结果 | 幂等 Receipt 查询 | 幂等发布 | 幂等可见性解析 | 幂等 Context 提交 | 不得重复 Participant、Publication、Visibility 转换或 ContextVersion |
| Crash after Storage Visibility | 保留精确 Participant 与 Fence 处置 | 解析原 Admission | 验证原规范提交 | 验证原 Publication | 恢复精确已提交可见性结果 | 提交或恢复精确 ContextVersion | 不得第二次推进可见性；不得重复 ContextVersion |

在权威结果得到解析之前，UNKNOWN MUST 保持非最终状态。

恢复 MUST 使用原始 Operation identity，不得生成新身份。

Fence MUST 对每个已准入 Participant 记录可审计的
完成或抑制处置结果。

该矩阵 MUST 保持 §2 的逻辑顺序，
MUST NOT 改变 B 的顺序契约。

Storage L1 保持不变。
Storage L4 保持 OPEN / NOT APPROVED。

## 17. 依赖与开放问题

依赖：Domain Model 时间/认知语义；Canonical Store；Lifecycle Manager；E Proposal/Replay；F Historical Retrieval；G ContextVersion 引用；H ActorRef/Wire 兼容性；I Retention/Forget Policy；Consistency/Recovery。

- DECIDED FOR CONVERGENCE：INT-P0-01 的 Claim 身份语义，选择稳定 Claim identity + 不可变 ClaimRevision（Option A）。该身份决策不批准 Schema、DDL、公共 API 或 Wire Contract。
- OPEN：INT-P0-01 中尚未由 Claim 身份决策解决的 Fact 专属建模及批准事项。
- OPEN：ContextVersion/ChangeSet Schema 由 G 拥有；Brain 只提供固定引用。
- OPEN：不确定 TimeValue 规范化和时区策略（DM-006）。
- OPEN：Sequence 范围（Per-Aggregate 还是 Global Commit Stream）。
- OPEN：Schema/Vocabulary Registry 和 Migration 兼容性（DM-013）。
- TO_VALIDATE：不可变 Snapshot 与 Delta Storage、历史查询和迁移性能。

## Phase 3 整改 — 规范 Cursor 边界

以下是不同类型，**MUST NOT** 将它们比较、相加、替代或序列化为一个通用整数：

| 类型 | 权威/范围 | 含义 |
|---|---|---|
| CanonicalCommitCursor | D；单个 Brain Authority | 全局有序的已提交事务位置，仅在成功原子提交时分配 |
| AggregateRevision | D；单个 Aggregate | Aggregate 内单调 Revision，不可全局比较；已提交 Revision 同时携带 CanonicalCommitCursor |
| LifecycleEventCursor | D；单个 Memory Lifecycle Stream | (memory_id, lifecycle_event_sequence, event_id)；按 Memory 连续，同时记录所属 CanonicalCommitCursor |
| IndexWatermark | F；单个 Index/Channel/Partition | (index_id, partition_id, applied_through: CanonicalCommitCursor, coverage/schema metadata)；仅表示覆盖进度，绝不是 Forget Proof |
| ForgetFenceCursor | D；Operation + Target Set | (forget_operation_id, fence_generation, target_set_digest)；单调抑制 Epoch，不是 Commit Position 或 Index Watermark |

ContextVersion 仍由 G 拥有；BMCP Delivery/Request ID 仍由 H 拥有；I Permission/Revocation Epoch 仍由 I 拥有。D 不定义其 Wire Encoding。

### Canonical Transaction 可见性与 Replay

成功的 Canonical Transaction 原子暴露对象/Revision 写入、Aggregate Head CAS 更新、LifecycleEvent 追加、CanonicalCommit Record 和可恢复 Outbox Intent。它在 Commit Serialization 时获得一个全局有序 CanonicalCommitCursor。中止/拒绝事务不获得 Cursor；回滚分配不会在已提交 Stream 中造成空洞。As-of Reader 看到整个事务或完全看不到。Cursor 只有在持久化提交后才可见。

Consumer 从最后一个持久化应用 Cursor 之后恢复。允许重新投递，但必须幂等。任何 Consumer 都不得越过缺失 Commit、应用失败或未知 Schema 推进。乱序工作可以暂存，但 Watermark 必须停留在最后连续前缀。历史过期时，使用带 Base Cursor 的一致 Snapshot Bootstrap，再继续；不得跳到 Latest。Outbox 延迟/重试不能改变 Canonical 顺序。Projection Watermark 只报告覆盖进度。

### Lifecycle Event Cursor

LifecycleEvent Sequence 属于单个 Memory Stream，只有 Event 和所属 Transaction 提交时才分配。Consumer 观察到 Gap 时必须 Replay/Reconciliation。Commit Cursor 排序跨 Aggregate 事务；Lifecycle Cursor 排序单个 Memory 的事件。二者不能互相替代。

## Phase 3 整改 — Version 与 Cursor 语义

**DECIDED：** MemoryVersion Sequence 是 Per-Memory AggregateRevision，不是全局 CanonicalCommitCursor。每个已提交 MemoryVersion 都记录两者。EntityVersion 和 RelationRevision 同样携带各自 Revision 和 Commit Cursor。只有成功提交才推进 Aggregate Revision；被拒提案/CAS 失败不消耗 Revision。

**DECIDED：** LifecycleEventCursor 属于单个 Memory Lifecycle Stream，独立于 MemoryVersion AggregateRevision 和 CanonicalCommitCursor。Lifecycle Event 可以与 MemoryVersion 在同一事务提交，但三种值必须保留独立名称和含义。Lifecycle Event 记录所属 Canonical Commit Cursor。

**DECIDED：** IndexWatermark 由 F 拥有，并限定于 Index/Channel Partition。它描述已应用的连续前缀以及 Coverage/Schema 元数据。Rebuild 从一致 Canonical Snapshot Cursor 开始并 Replay；候选可见前检查最新 ForgetFence。Rebuild 进度不得使用 MemoryVersion Sequence 或 LifecycleEventCursor 表示。

### 历史读取与 Replay

历史读取使用已提交 CanonicalCommitCursor/As-of Snapshot 和准确 Aggregate Revision 引用，绝不依赖 Projection 到达顺序。Replay Cursor 是 Exclusive：从最后一个已提交且已应用 Cursor 之后恢复。重复 Replay 必须幂等；缺失 Cursor 阻止连续推进。Replay Window 过期时，使用带 Base Cursor 的一致 Snapshot。由于其他 Aggregate 可能在两个 Revision 之间提交，一个 Aggregate 的历史在全局 Commit Stream 中可以是稀疏的；这不代表该 Aggregate 自己的 Revision Sequence 有缺口。

### Claim / ConflictSet 冻结门禁

Claim identity 语义与不可变 ClaimRevision 语义已 **DECIDED FOR CONVERGENCE（Option A）**。具体 ClaimRevision Schema、ConflictSet Schema 和字段级引用，在 Architecture Governance + B 批准 INT-P0-01 之前仍保持 **ADR-BLOCKED**。Fact-specific modeling 与 Fact approval 继续保持 **OPEN**。本文现有 ClaimRevision 表只是字段表示的备选草图，不是 D 决议；它不会重新开启或削弱已决定的 Claim identity 语义。D 会在批准后将 ADR 映射到不可变 Revision 机制；此前不得冻结 Schema、DDL、公共 API 或 Wire Contract。
