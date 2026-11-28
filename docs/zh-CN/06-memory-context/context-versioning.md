---
document_metadata:
  domain: memory-context
  role: normative-standard
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: null
    usage_status: Active
    modification_status: Modified
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
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Normative
  bilingual_counterpart:
    source: "06-memory-context/context-versioning.md"
    en: "docs/en/06-memory-context/context-versioning.md"
    zh-CN: null
  steward: "Architecture Governance"
---

# 上下文版本与变更集

**状态：** 不变量已裁定；对象编码与序列化策略为候选  
**负责人：** Session G  
**相关：** INT-P1-01、INT-P1-05、C review P2-05/P2-06

需求 ID `CV-01`..`CV-48` 是本文档中 48 处 MUST 出现位置的稳定引用。它们仅为标签；规范文本未作更改。其他文档应当引用 `CV-nn`，而不是章节编号，因为章节编号可能发生变化。

## 1. 保证

上下文版本不可变，并标识一个完整的、期望的受管区域状态。每个上下文都有一个权威的、单调递增的序列。每个已提交的变更集都标识基础版本和目标版本。并发变更不能静默覆盖；提交使用 CAS 或等效的逐上下文串行化机制。快照和增量表示相同的目标状态；增量本身不具有独立权威性。适配器已应用状态与上下文头版本相互独立。

## 2. Context Version 对象

| 字段 | 含义 |
|---|---|
| context_version_id | 全局唯一、不透明且不可变的版本 ID |
| context_id | 所属上下文 |
| sequence | 逐上下文单调递增的整数；永不复用 |
| parent_version_id | 直接前一版本；仅创世版本为 null |
| snapshot_ref / snapshot_hash | 不可变的完整条目快照及其规范摘要 |
| schema_version | 上下文领域模式 |
| scope_fingerprint | 与已解析的 Scope/身份/策略 epoch 绑定的不可逆指纹 |
| canonical_watermarks | 每个来源/分区的规范修订水位 |
| policy_epoch | 提交时使用的授权/策略 epoch |
| committed_change_set_id | 创建此版本的变更集 |
| committed_at | Brain 提交时间 |
| actor_ref / reason | 已认证主体/服务及其理由 |
| entry_count / budget_summary | 可复现的聚合元数据 |

快照包含完整且有序的条目状态，以及必需的成员关系墓碑。载荷仍保持为不可变引用或受治理的投影；每次使用时都要重新检查权限。

## 3. ContextEntry 版本

条目在每个不可变的上下文版本内部进行版本化。稳定身份的作用域限定于上下文；每次出现都有一个条目修订版本：
- entry_id, context_id；
- memory_id 和精确的 memory_version（绝不隐式使用最新版本）；
- rendering_ref/projection_schema_version；
- tier, priority, position；
- activation_reason 和 activation_correlation_refs；
- epistemic_status, lifecycle_state, trust 和 classification；
- source_refs/evidence_refs（带类型并经过权限检查）；
- content_hash, token_estimate, byte_size；
- activated_at, expires_at, valid_time；
- entry_revision, created_by_change_set_id, last_changed_by_change_set_id；
- entry_state 和 invalidation_reason。

版本固定可防止内容静默漂移，但不能覆盖撤回、Forget 或权限撤销。

## 4. ContextChangeSet 对象

| 字段 | 含义 |
|---|---|
| change_set_id | 唯一且不可变的变更请求 ID |
| context_id | 目标上下文 |
| base_version | 精确的预期上下文版本 |
| target_version | 仅在成功提交后分配 |
| operations | 带有稳定操作 ID 的有序类型化操作 |
| reason | 触发原因/业务理由，而非任意指令 |
| actor_ref | 已认证的调用方/服务 |
| created_at | 请求创建时间 |
| idempotency_key | 作用域限定的重试身份标识 |
| payload_hash | 规范化请求的哈希 |
| policy_epoch | 已检查的授权 epoch |
| status | Prepared、Committed、Rejected、Conflict 或 Aborted |
| correlation_id / causation_id | 跨系统追踪关联 |
| result_ref | 不可变的操作结果/诊断信息 |

提交前不存在目标版本；调用方不能通过基础版本加一来猜测目标版本。

## 5. MemoryContext 必需对象

必需字段：context_id、scope、agent_instance_id、task_id、environment_id、context_version、applied_version、status、budget、created_at、updated_at、expires_at。

必需的语义扩展：agent_id、session_id、principal_scope_ref、project_scope_ref、purpose/profile、schema_version、policy_epoch、canonical_watermarks、last_reconciled_at。

applied_version 字段仅是一个便利性投影。权威的应用历史按 ContextDelivery/Adapter/Context Session/Inference Request 记录；一个上下文可以有多个处于不同版本的使用者。

## 6. ContextDelivery 必需对象

必需字段：delivery_id、context_id、change_set_id、base_version、target_version、status、timestamps 和 error。

语义扩展：adapter_id、agent_instance_id、agent_context_session_id、inference_request_id、capability_epoch/tier、applied_coverage、managed_region_hash、final_request_hash 或隐私安全的 attestation ref、boundary_id/timestamp、correlation_id、forget_clear_state 和 application authorization epoch。

Applied 要求适配器明确确认：精确的目标版本已完整物化到受控管理区域中，并且该区域属于提交给推理运行时的最终请求。**CV-01、CV-02** 鈥?如果适配器无法观察该最终请求边界，它必须报告 Unknown 或更低能力；不得声称达到 Tier 1。除非 H/C 定义了规范化、捕获和关联方式，否则摘要并不足够。

## 7. 快照与增量

- **快照：** 目标版本的完整期望状态。创世、缺口恢复、基础版本未知、能力变化或不安全的增量协调时必须使用快照。每个规范引用仍要求当前授权。
- **增量：** 从精确基础版本到目标版本的有序操作，包含基础/目标哈希、操作 ID 和模式版本。必须原子应用；重复的 Delivery ID 返回先前结果。基础版本不匹配时拒绝并请求快照。
- 增量不是尽力而为：默认情况下，未知操作、缺失条目、哈希不匹配或授权失败都会拒绝整个更新。
- 将变更集重放到不同的头版本时，必须重新规划并创建新的变更集，不得盲目重放。

## 8. CAS、并发与幂等性

建议的初始策略：按上下文串行化提交，并将基础版本上的 CAS 作为防御性检查。

1. 规范化请求并计算载荷哈希。
2. 在主体 + 上下文 + 操作族/保留窗口范围内解析幂等键。
3. 已存在的键 + 相同哈希：返回原始结果/目标版本。
4. 已存在的键 + 不同哈希：返回 IDEMPOTENCY_KEY_REUSE。
5. 验证当前头版本是否等于基础版本；否则返回 BASE_VERSION_MISMATCH 并重新读取/规划。
6. 针对同一个暂存快照验证所有操作。
7. 原子提交变更集、不可变版本、审计记录和 outbox。
8. 头版本只推进一次；不得部分提交。

不假设存在自动合并。安全的变基是在重新读取规范状态和策略状态后创建一个新的变更集。

## 9. 交付生命周期与迟到确认

Prepared 鈫?Delivered 鈫?Applied；其他状态：Rejected、Expired、Superseded。
- Prepared：数据包已物化/获授权，但尚未确认发送。
- Delivered：仅表示传输/接收方已回执。
- Applied：明确的证明满足第 6 节。
- Rejected：适配器拒绝/验证失败。
- Expired：有效应用前 TTL 已经过期。
- Superseded：在应用之前，有更新的目标取代了该目标。

超时状态是 Unknown，而不是 Rejected 或 Applied。通过 Delivery ID 查询。对于已被取代版本的迟到 Applied，是历史证据，但不能使期望头版本回退；下一次推理之前可能需要最新快照。

## 10. 回滚、取代与重放

已提交的版本永远不会通过修改/删除来回滚。回滚是在重新授权并验证当前规范状态之后创建一个新的补偿性变更集。取代操作会创建一个新版本，并将尚未交付的过期交付标记为 Superseded。重放通过快照/变更集/审计/outbox 重建链；它绝不复用过期授权，也不绕过 Forget 墓碑。

## 11. 已应用覆盖范围

- **Full：** 受管区域中包含完整目标版本；已观察到精确的最终请求边界；请求/会话/能力关联有效。
- **Partial：** 已应用可识别的子集；绝不等同于完整版本已应用。
- **Bypassed：** 推理未使用 Brain 管理的区域，或使用了非受管回退路径。
- **Unknown：** 可见性不足、超时、证据丢失、适配器离线或边界不明确。

在严格语义下，只有 Full 可以将 Delivery 状态设为 Applied。Partial/Bypassed/Unknown 都是非 Applied 的覆盖结果。Applied 并不能证明模型关注或使用了这些内容。

## 12. 决策登记表

- **DECIDED：** 不可变版本、单调递增序列、单一权威头版本、明确的基础/目标版本、CAS/串行化、原子变更集、可重放审计。
- **DECIDED：** Applied 将交付 + 会话 + 请求 + 能力 epoch + 最终边界证明关联起来。
- **CANDIDATE：** 每个上下文使用串行化写入器并结合 CAS。
- **TO_VALIDATE：** 快照/增量大小、哈希规范化、重试保留期限和竞争情况。
- **OPEN：** 证明/摘要字段（C/H）；规范修订水位模式（D/E/F）。
## 13. Phase 3.5 类型化游标、生产者和证明扩展

### 13.1 G 消费的类型化游标注册表

| 字段/引用 | 权威方 | 语义与约束 |
|---|---|---|
| CanonicalCommitCursor | D | Brain 权威方的单一提交排序游标；用于规范协调的来源，不是上下文序列 |
| ForgetFenceCursor | D | 用于标识 ForgetOperation、栅栏代次和目标集摘要的不透明元组 |
| ProducerRegistrationSequence / ProducerRegistrationHighWater | D | D 生产者工作账本的准入顺序，以及每个操作的屏障截止位置 |
| ProducerRegistryVersion | D | 已启用生产者类别的版本 |
| PermissionEpoch | I | 不透明的策略域授权/撤销纪元，并带有当前有效性验证 |
| ProducerDomainInventoryEpoch | I | 全局生产者/接收方清单修订版本 |
| TargetInventorySeal / TargetId | I | 不可变清单封印和稳定目标身份；G 绝不创建其中任何一项 |
| IndexWatermark | F，按索引和分区 | 对该确切分区的连续规范发布覆盖范围 |
| ContextVersion sequence | G，按上下文 | 仅用于期望的上下文状态排序 |
| DeliveryId / DeliveryAttemptId | G | 逻辑投递身份和彼此不同的尝试身份 |
| CapabilityEpoch | H | 适配器实例能力/证明纪元 |
| InferenceRequestId / FinalRequestBoundaryId | C/H | 实际最终请求及边界证据 |

这些值是不透明的、类型化的，并且受权威域约束。跨命名空间进行算术运算、max()、比较或游标替代均无效。特别是，F 的最大分区水位线不能替代按分区划分的水位线向量，D 的 ProducerRegistrationHighWater 不能替代 CanonicalCommitCursor，I 的清单纪元也不能替代 D 针对每次 Forget 的工作屏障。

### 13.2 生产者工作和工件发布字段

对于具备派生能力的 G 工作，保留：
- producer_class_id 和 producer_registry_version；
- producer_work_item_id 和 canonical_request_digest；
- registration_receipt_ref 和 producer_registration_sequence；
- 适用时的 attempt_id / lease_id 和 derivation_run_id；
- source_memory_refs，包含精确的 MemoryVersionRefs 以及传递性血缘摘要/引用；
- scope_refs 和 context_id；
- observed_forget_fence_cursor 和 canonical_commit_cursor；
- permission_epoch 和 authorization_decision_ref；
- derived_artifact_ref/version、dependency_registration_receipt_refs；
- publication_operation_id/receipt_ref 和可见性处置；
- 完整/未知依赖状态以及终态工作处置。

G 的生产者工作注册必须先于排队、租约分配、受保护源数据解引用和执行。重试必须保留 WorkItemId/digest。D 的语义操作回执由其所有者控制；本文档不臆造其线格式或存储模式。

### 13.3 受保护可见性与存储原子性

#### 规范性来源与血缘

本节是 G Claim/Fact 受保护可见性的根级规范性
来源。

双语 EN/ZH Claim/Fact Context Visibility
Addendum 已合并到本节。其规范性要求不是一个
独立且相互竞争的协议。

**CV-03** — 配对的 EN/ZH 文档必须与本节保持同步。
如果发生文本漂移，在配对文档得到
修正之前，以本根级章节为准。

血缘：合并后的要求源自
Phase 3.8.27 G Claim/Fact Context Visibility
Addendum 和 AID-2026-014 R5 修正。

#### 1. 所有权与精确引用

逻辑上下文提交仍由 G 所有，
并创建一个不可变的 ContextVersion。

**CV-04** — 引用 ClaimRevision、
FactRevision 或派生工件的 ContextVersion 必须绑定精确的
不可变修订引用以及适用的 ForgetFenceCursor。

**CV-05** — G 不得以当前 Claim head 替代
已固定的 ClaimRevisionRef。

#### 2. 必需的受保护排序

共享的受保护发布顺序如下：

1. 解析授权和 Scope。
2. 在串行化准入边界下评估 D Forget Fence 并执行 Producer
   Admission。
3. 持久化注册完整依赖集。
4. 将 E 工件暂存为私有状态。
5. 提交规范 ClaimRevision/FactRevision。
6. 将依赖注册和 Publication Intent
   与已提交的修订关联。
7. 以幂等方式完成 E 发布。
8. 只有在确认所需的规范证据和依赖证据之后，
   才推进 Storage 可见性。
9. 使用精确的规范修订引用提交 G ContextVersion。
10. 只有在满足所有
    必需的可见性条件之后，才标记逻辑完成。

#### 3. T17 — 栅栏优先

**CV-06** — 如果 Forget Fence 在线性化顺序上先于 Producer
Admission，则不得准入受影响的工作。

任何暂存、规范提交、发布意图、
E 发布或 Storage 可见性转换
都不得绕过 Fence 决策。

#### 4. T18 — 参与者优先

**CV-07** — 一旦 Producer Admission 成功线性化，
就必须将该确切操作持久记录
为权威参与者。

**CV-08** — 成功的 Producer Admission 与对
该确切已准入参与者的持久记录，必须在权威的串行化
Fence/Admission 边界下构成一个不可分割的
操作。

**CV-09** — 后续 Forget Fence 在该屏障能够持久可见地看到已准入
参与者记录之前，不得线性化或完成
其参与者屏障评估。

**CV-10** — 参与者记录失败必须阻止 Admission
报告成功。

**CV-11** — Fence 不得忽略参与者记录尚未完成或仍未解决的
已准入操作。

**CV-12** — UNKNOWN 必须保持非终态。

**CV-13** — 恢复必须使用原始 Operation 身份。

**CV-14** — Fence 必须为每个已准入参与者
记录可审计的完成或抑制处置。

D memory-versioning.md §16.1 中的六组件受保护发布失败
矩阵，对于源自受保护 Claim/Fact 内容的
G ContextVersion 提交具有规范效力。

**CV-15** — 在相应的参与者屏障
和 Storage 可见性条件得到解决之前，
G 不得提交或暴露 ContextVersion。

**CV-16** — 后续 Forget Fence 不得悄然跳过、
擦除或错误分类该参与者。

**CV-17** — Fence/Admission 屏障必须核算
该参与者，并保留其精确身份、
依赖闭包和可审计处置。

**CV-18** — 最终完成或抑制决策
必须遵循已声明的 Forget 策略。

**CV-19** — 在权威结果得到解决之前，
UNKNOWN 必须保持非终态。

#### 第二阶段 Admission 拒绝与受保护 ContextVersion 可见性

**CV-20** — 当 PublicationParticipant Admission 未能针对权威 ForgetFence/Admission 排序锚点成功线性化时，G 不得将相应 ContextVersion 提交或发布为该次发布的可见结果。

**CV-21** — 不得将成功的 Producer Admission 视为 PublicationParticipant Admission 成功的证据。**CV-22** — 在提交或发布相应的可见 ContextVersion 之前，G 必须独立确立与适用的 StorageVisibilityParticipantRef 和发布元组身份绑定的确切 PublicationParticipant 已成功完成第二阶段 Admission。

**CV-23** — 对于任何已经提交、且引用了一个第二阶段 Admission 未成功发生的发布对象的 ContextVersion，必须应用 D memory-versioning.md §16.1 中 Forget 终态 × 组件处置矩阵所规定的适用终态处置；该矩阵涵盖七个逻辑组件的四种 Forget 终态。**CV-24, CV-25, CV-26** — 相应 G Context Commit 的处置必须与适用的 Forget 终态一致：在 Failed 和 Cancelled 状态下，G 不得提交 ContextVersion；在 CompletedWithPolicyException 状态下，只有当该例外已获得具名批准且满足所有适用前置条件时，G 才可以提交 ContextVersion；在 Completed 状态下，G 必须在提交 ContextVersion 之前满足完整完成要求。**CV-27** — 不得仅仅因为其规范提交此前已成功，就将该 ContextVersion 保留或暴露为成功的可见发布。

**CV-28** — 在每次读取时，恢复和重放都必须重新评估权威的第二阶段 Admission 证据、ForgetFence 处置和 Storage 可见性结果。**CV-29** — 历史 ContextVersion 提交不得赋予永久可见性，不得绕过后续 ForgetFence 处置，也不得替代所要求的第二阶段 Admission 成功。**CV-30** — 缺失、冲突或 UNKNOWN 证据必须以失败关闭方式处理。**CV-31** — 在权威终态结果和经授权的可见性条件得到证明之前，相应 ContextVersion 必须保持不可见。

**CV-32** — 在提交、恢复、重放和读取时的可见性评估全过程中，G 必须保留精确的发布身份，以及该身份与相应 Producer participant、PublicationParticipant、规范依赖闭包和 Forget 终态处置之间的关系。

**CV-33** — 这些要求是 §16.1 下的实现符合性门禁，不得将其解释为改变 §13.3 中定义的准入排序或参与者优先要求。

#### 5. G 受保护提交要求

**CV-34** — G 必须：

- 重新验证当前 I 授权。
- 重新验证适用的 D Forget Fence。
- 验证所有被引用的 Claim/Fact 修订。
- 验证完整的依赖注册回执。
- 当上下文包含已发布工件时，
  验证确切的 Storage 可见性结果。
- 通过受保护可见性协议提交
  不可变的 ContextVersion。
- 只有在权威提交结果得到确认后才发布。

**CV-35** — G 不得仅依据本地预检查，
随后再执行独立且不受保护的 head 更新，
就暴露新的 ContextVersion。

#### 6. 历史可见性

在后续 Forget 发生之前提交的 ContextVersion
并不授予永久访问权限。

**CV-36** — 历史上下文读取和重放必须
重新评估当前授权和 Forget
抑制状态。

**CV-37** — 被遗忘的 ClaimRevision 不得
通过现有 FactRevision 或历史
ContextVersion 泄露。

#### 7. UNKNOWN 与恢复

**CV-38** — UNKNOWN 提交或确认丢失
必须保持非终态。

**CV-39** — 恢复必须解决同一个操作和
确切的 ContextVersion 身份。

任何重试都不得创建重复的可见
ContextVersion 状态。

**CV-40** — 恢复必须协调 Fence、Admission、
依赖注册、规范提交、
E 发布、Storage 可见性和 G 状态。

**CV-41** — 恢复不得根据缺失的证据
臆造成功的终态。

#### 8. 物理实现门禁

**CV-42** — 在启用公共可见性之前，必须由 D 和 Storage/
Consistency 规定并独立证明跨越
G 可见性与 D 最终门禁的物理事务/CAS 或等效的
可恢复 prepare/commit 实现。

**CV-43** — 在该证明存在之前，G 可以私下暂存，
但不得暴露工件、推进
公共 head 或发送投递。

这是一个实现符合性门禁，
而不是尚未解决的规范性排序选择。

本节并不声称某个 API 或
生产实现已经存在。

#### 9. Storage 边界

现有 Storage L1 决策保持不变。

本协议定义逻辑排序、受保护
发布和可观察一致性。

本协议不选择或批准物理数据库、
部署拓扑、HA/PITR 策略或 Storage
L4 设计。

Storage L4 仍为 OPEN / NOT APPROVED。

### 13.4 Applied 证明证据

G Delivery 记录分别消费 H 的证据阶段：DELIVERED（传输端点回执）、MANAGED_REGION_MATERIALIZED（本地区域后置条件）以及 FINAL_REQUEST_SUBMITTED（确切的不可变请求已跨越可信交接边界）。EXECUTION_STARTED 是后续运行时生命周期证据，并非定义 Applied 所必需。

Full Applied 要求满足 C 的最终请求谓词，并且 H 证据记录绑定以下全部内容：
- 确切的 ContextRef 和不可变的目标 ContextVersion；
- 稳定的 DeliveryId 和唯一的 DeliveryAttemptId；
- 经认证的 Adapter Principal/Instance 以及 Agent Principal/Agent/Instance；
- Runtime Instance/Session 和确切的 InferenceRequestId；
- FinalRequestBoundaryId 和可验证的最终提交证据；
- ManagedRegion ID/revision/inventory 以及 FULL 覆盖范围；
- CapabilityEpoch、当前 I PermissionEpoch/授权决策；
- 适用于所有包含的源血缘的 D ForgetFenceCursor；
- 确切的 Managed Region 摘要以及带版本的规范化/摘要配置；
- 受保护区域完整性证据和时间戳/防重放身份。

该摘要的范围限定为从最终不可变请求中提取的声明管理区域；它排除 System/Developer/User 内容、凭据以及不相关的提示词内容。摘要本身不是证明。字段缺失、过期或不可验证时，必须判定为 Partial、Bypassed 或 Unknown，绝不能判定为 Full。Tier 2/3 只有在能够证明满足 C 的相同最终边界符合性谓词时，才可以声明 Full；否则适配器必须报告其较低层级的覆盖范围。

### 13.5 投递身份与状态

一个逻辑投递在重传期间保持稳定的 DeliveryId；每次尝试都具有唯一的 DeliveryAttemptId。每个实际提交的推理调用都具有唯一的 InferenceRequestId；创建了新推理调用的重试必须获得新的请求 ID 和新的最终提交证据。ACK 身份/摘要不可变；相同身份加相同摘要具有幂等性，相同身份加不同摘要则构成冲突。

投递生命周期包括 Prepared、Delivered、Applied、Rejected、Expired、Superseded 和 Unknown。Unknown 表示超时、崩溃、离线或结果不明确；它不代表成功。只有当某个迟到的 Applied ACK 能够证明其排序发生在过期/取代/栅栏/撤销之前时，才可以将其保留为历史证据；它不能恢复当前上下文，也不能使期望的 head 回退。


## 14. Phase 3.5 — 规范性失效与证据对齐

### 14.1 上下文失效矩阵

该矩阵区分逻辑可用性与不可变审计记录的保留。**CV-44** — “Invalidate”（失效）意味着该对象不得用于规划、投递、重放或应用受保护内容；这并不意味着历史记录会被物理删除。

| 触发条件 | ContextEntry | ContextVersion / Snapshot | Delta | Delivery / Pending Delivery | Applied Context Reference |
|---|---|---|---|---|---|
| D ForgetFence 覆盖源数据或传递性血缘 | 立即拒绝/墓碑化匹配条目；不得再次纳入 | 快照包含受影响血缘的任何版本都变为不可服务；仅保留受治理且不可重构的审计元数据 | 任何新增/更新/重排受覆盖条目的 delta 均不得应用；拒绝重放 | Prepared/Delivered 尝试在支持的情况下变为 Superseded 或 Cancelled；不得进一步应用；已经提交的结果仍作为历史记录保留 | 标记为当前用途下的 Invalidated；保留历史证明，绝不作为当前引用 |
| I PermissionEpoch 撤销/拒绝或纪元缺口 | 阻止受影响条目及所有受保护解引用；不得推断为规范 Forget | 版本在结构上可能仍然有效，但在旧纪元下未经授权/不可服务；只有在重新获得授权后才可重建 | 在重新确立当前授权和确切基准之前拒绝 | 待处理尝试被取消/取代；离线/未知状态仍为 Unknown，绝不能是 Applied | 标记为 AuthorizationStale/Unknown；旧 Applied 证据仅保留为历史记录 |
| 来自 D 的规范取代/修订/撤回 | 按权威结果标记为 StaleRevision/Superseded/Retracted；固定精确的旧引用，不得悄然浮动到最新版本 | 受影响快照对当前规划而言变为过期；只有在后继版本得到明确验证时才重建 | 基于旧源/版本的 delta 不得应用；从当前安全基准创建新的 delta | 待处理投递被取代；迟到的 ACK 不能使旧目标变为当前目标 | 标记为当前用途下的 Stale/Invalidated；保留历史证明 |
| Scope 变更、Scope 退役或绑定不匹配 | 在精确所有权/适用性 Scope 重新解析并获得授权之前阻止该条目 | 旧 Scope 指纹不能授权新的 Scope；完整重新授权后创建新版本 | 如果 Scope 指纹/基准/接收方不同，则拒绝 | 待处理投递被取消/取代；不得将旧投递重新定向 | 标记为 ScopeStale/Unknown；新会话/目标需要新的证明 |
| F IndexWatermark 滞后、截断或检索不完整 | 必须针对 D/I 检查现有的精确引用；不得仅仅因为索引中缺失就移除 | 将源覆盖范围标记为 Stale/ReconcileRequired；不得声称完整 | 任何 delta 都不得根据缺失推断删除 | 不得发布其正确性依赖于不完整候选覆盖范围的投递 | Applied 历史保持不变；当前可用性必须独立检查 |
| Adapter 能力/会话/管理区域发生变化 | 如果仍获授权，条目可以继续作为期望内容 | 版本保持不可变；投递包可能需要重新物化 | 根据确切的当前基准和模式重新协商/重建 | 旧尝试不得升级；新尝试使用当前 CapabilityEpoch | 旧证据仍绑定旧会话/区域/CapabilityEpoch；新的应用需要新证据 |
| Context Remove（G 操作） | 在新的 ContextVersion 中设置成员关系墓碑 | 旧版本保持不可变；新版本省略该成员关系 | 重新添加该成员关系的旧 delta/snapshot 被拒绝/取代 | 包含已移除成员关系的待处理投递被取代 | 历史 Applied 引用仍是历史记录；它不会变成 Canonical Forget |

规则：
1. Forget 抑制和权限拒绝在协调工作之前生效；任何读取/规划/编辑/快照/delta/重放/投递/应用路径都不得等待新的 ContextVersion。
2. 规范取代和 Scope 变更需要精确的所有者解析；G 不得臆造后继身份或扩大 Scope。
3. Context Remove 只改变 G 的成员关系。**CV-45** — 它不得创建 D ForgetOperation、推进 D ForgetFence，或被报告为规范删除。
4. 历史 ContextVersion、ChangeSet、Delivery 和 ACK 记录只能按照 I 策略保留，并且不得保留可重构的已遗忘明文。
5. 新的安全 ContextVersion 是一个新的不可变版本，具有新的序列号、提交时观察到的 parent=head、经过重新授权的精确引用、当前类型化权威向量以及新的依赖/发布回执。绝不修改旧版本或重置序列号。

### 14.2 投递状态机与证据

逻辑 DeliveryId 标识一次期望投递。DeliveryAttemptId 标识一次传输/应用尝试。**CV-46** — 重试可以复用 DeliveryId，但每当创建新的尝试时，必须使用不同的尝试身份。每次实际推理调用都需要一个新的 InferenceRequestId。

| 状态 | 进入条件/最低证据 | 允许的后续状态 | 禁止的解释 |
|---|---|---|---|
| Prepared | 不可变目标版本和投递包已私下暂存；已检查当前授权/栅栏；在可见/发送之前，D 依赖注册和最终可见性门禁证据均已具备 | Delivered、Rejected、Expired、Superseded | 尚未发送；不是 Applied |
| Delivered | H/传输接收方回执绑定 DeliveryId + AttemptId + 接收方/会话；传输回执已持久化 | Applied、Rejected、Expired、Superseded、Unknown | 不能证明管理区域已物化或最终推理请求已提交 |
| Applied | C 最终请求谓词以及 H 完整性保护证据将确切的完整目标绑定到最终不可变请求；G 验证所有字段及其当前有效性 | 对该尝试而言为终态；后续失效会创建单独的失效/当前有效性状态，而不是追溯修改 | 绝不能从 Delivered、HTTP 成功、本地缓冲区写入、提交前钩子或单独的摘要推断 |
| Rejected | 带有原因和尝试身份的经认证否定 ACK/验证失败 | 只有在纠正并重新获得当前授权后才允许新尝试；否则该尝试为终态 | 不是可重试的成功；不得推进 Applied 引用 |
| Expired | 在有效 Full Applied 之前截止时间已过；时间来源和过期证据已记录 | 在重建当前目标后，创建新的 DeliveryId 或明确授权的新尝试 | 单纯超时属于 Unknown；过期不能通过迟到 ACK 转换为 Applied |
| Superseded | 更新的 Context 目标、ForgetFence、权限撤销、Scope/能力变更在有效应用之前使该尝试失效 | 该尝试为终态；从当前安全版本创建新的投递 | 不得返回 Prepared/Delivered/Applied-current |
| Unknown | 超时、崩溃、Adapter 离线、ACK 丢失或证据不足；需要查询/协调 | 只有有效证据证明应用发生在失效之前且所有排序均可证明时才可变为 Applied；否则协调后变为 Rejected/Expired/Superseded | 绝不代表成功；不得存在当前 Applied 指针 |

状态转换按每次尝试分别进行，并在审计日志中保持单调。只有当经过认证的事件时间/序列及权威排序证明其发生在 Expired、Superseded、ForgetFence 或撤销之前时，才接受迟到的 ACK 作为历史证据。如果无法证明排序，则保留 Unknown 并阻止当前用途。**CV-47** — 旧目标的迟到 ACK 不得覆盖 Context head、当前 Applied 引用或较新尝试的状态。

### 14.3 Applied 证据映射（G 消费 C/H；不定义其线格式）

只有当以下所有行均存在、完整性有效、彼此一致，并且在最终提交边界仍然有效时，G 才可以将某次尝试设为 Full Applied。

| 证据维度 | 必需绑定/来源 | G 验证 |
|---|---|---|
| Context | 精确的 ContextRef + 不可变的 ContextVersion ID/sequence + 目标快照哈希 | 必须等于投递目标；不得从当前 head 推断目标 |
| Delivery | DeliveryId + 唯一的 DeliveryAttemptId + payload digest + 尝试状态 | 同一次逻辑投递和确切尝试；对重复 ACK 去重 |
| Agent/Adapter 身份 | 经认证的 Agent Principal/instance 和 Adapter Principal/instance；签发方/传输绑定 | 必须匹配已注册接收方，而不是依赖载荷自我声明 |
| Runtime | Runtime instance + 经认证的 Runtime Session | 会话必须确切，并且对该请求有效 |
| Inference request | 确切的 InferenceRequestId + FinalRequestBoundaryId | 必须标识跨越可信交接边界的实际不可变请求 |
| Managed region | ManagedRegion ID/revision/inventory + FULL 覆盖范围 | 必须是声明的 G 管理区域；不得包含不相关的提示词区域 |
| Permission | I PermissionEpoch + 授权决策/引用 | 在最终提交时必须是当前且已授权的；不得存在过期/有缺口的纪元 |
| Forget | 适用于所有源血缘的 D ForgetFenceCursor/Generation | 必须是当前的，且目标中不得包含受覆盖的源；仅由所有者进行不透明验证 |
| Content integrity | 确切的管理区域摘要 + 带版本的规范化/摘要配置 | 摘要必须匹配提取的管理区域；摘要本身不足以构成证明 |
| Capability | H CapabilityEpoch + 协商后的能力配置 | 必须匹配 Adapter 实例/会话和证明层级 |
| Final boundary | C 最终请求证明和 H 传输/完整性证据 | 证明最终不可变请求已提交，而不仅仅是准备好或已缓冲 |
| Anti-replay | ACK/证明身份、单调序列/nonce、时间戳和完整性证明 | 相同身份+摘要的重复项具有幂等性；相同身份+不同摘要则构成冲突 |

覆盖结果：
- **Full：** 每个目标条目和所需的管理区域组件都存在；所有证据行均通过验证。只有此结果映射为 Applied。
- **Partial：** 存在一个已识别的子集；记录精确覆盖范围，但不得设置 Applied。
- **Bypassed：** 推理未使用 Brain 管理区域，或通过非管理回退路径继续执行；不得设置 Applied。
- **Unknown：** 证据缺失、过期、矛盾、不可验证、离线或边界不可观测；不得设置 Applied。

Applied 仅证明在边界处包含了内容。它不证明模型注意到了内容、理解了内容、使用了内容、响应质量或行为遵从性。能力层级本身不能提升证据等级：如果无法证明满足 C 的最终边界谓词，则记录为 Partial/Bypassed/Unknown。

### 14.4 已经 Applied 的引用失效

Applied 是不可变的历史观察结果，而不是永久授权租约。当发生 Forget、Permission Revocation、Canonical Supersession、Scope Change 或能力/会话中断时：
- 将原始证明及其确切目标/请求/会话绑定保留为历史证据；
- 在当前用途投影中将其引用标记为 Invalidated，并记录触发因素、权威令牌和生效观察时间；
- 阻止旧 Applied 引用满足后续推理请求或当前投递要求；
- 对任何替代项，都要求新的 ContextVersion 以及新的 DeliveryAttempt/InferenceRequest/Applied 证据；
- 绝不改写历史，声称旧请求从未提交。

### 14.5 幂等性与提交不变量

- ChangeSet 幂等性以经过认证的 Principal + Context + 操作族 + key/保留窗口为作用域。相同 key/相同规范化载荷哈希返回原始结果和 TargetVersion；相同 key/不同哈希则为 IDEMPOTENCY_KEY_REUSE。
- Delivery ACK 幂等性以经过认证的 Adapter 实例 + DeliveryId + AttemptId + ACK 身份为作用域。相同身份/相同摘要返回先前结果；相同身份/不同摘要则构成冲突/安全信号。
- 重复 ACK 不会创建新的 Applied 记录，也不会改变当前指针。
- 每次成功提交的 ChangeSet 都使 Context head 前进一次。过期的 BaseVersion 返回冲突，并要求重新读取/规划；不执行隐式合并。
- 派生自规范内容的工件，其 G head/version 可见性转换仍受 D 的依赖注册和 PublishDerivedIfFenceCurrent 语义约束。**CV-48** — 物理事务/可恢复实现受 §13.3 作为从属约束进行治理：排序是规范性的且已 DECIDED，而物理实现仍然是一个实现符合性门禁，D 和 Storage/Consistency 必须在启用公共可见性之前予以规定并独立证明。在该证明存在之前，必须私下暂存，不得发布/发送。§13.3 控制这种关系；本小节不将其重新表述为尚未解决的规范性选择。

### 14.6 ChangeSet 准入与事务完整性

准入和提交完整性是两项独立要求。通过入口准入不得被视为事务、版本图或投递状态完整或有效的证明。
- 在 `commit_change_set` 入口处，准入必须在任何提交副作用发生之前，验证经过认证的 Principal 以及适用的 Context/操作权威性。该检查不得替代事务或版本图验证。Enforcement: **not yet enforced**。
- 在事务边界处，提交 ChangeSet 必须以原子方式持久化已提交记录、不可变的 TargetVersion 及其父级关系，以及 Context-head 转换。失败或过期的提交不得留下部分提交状态。Enforcement: **not yet enforced**。
- 在投递状态机中，ACK 必须根据经过认证的 Adapter 实例、DeliveryId、AttemptId 和 ACK 身份进行验证；ACK 处理必须保持幂等性，并且不得自行创建新的 Applied 记录或推进 Context head。Enforcement: §14.5。
