---
document_metadata:
  domain: memory-context
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-200/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "为原本无 front-matter 的镜像补 GOV-DOC-002 分类：仅记录 domain、role、状态与规范源路径（依据正文自述：Status: G semantic decisions recorded; FREEZE BLOCKED; implementation/execution NOT VERIFIED）；不主张规范权威，也不证明与源语义对等。补元数据前正文 blob：f22a7dc6b52325e350f6e36392b9d27f457d1e8c。"
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
    canonical_conflict_status: None
    normative_status: Informative
  bilingual_counterpart:
    source: "06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md"
    en: "docs/en/06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md"
    zh-CN: null
---
<!-- 源文件：session-g-memory-context / 06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md / Blob aa3afa73d8a76cc6f025839c52bfbff6a983046a -->
<!-- English companion: ../../en/06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md -->

# Phase 3.6 — Context Applied 状态、Forget 与 Reconciliation 合同

- Owner：Session G — ContextVersion、Delivery、Applied 状态与 Reconciliation
- 状态：**G 语义决策已记录；C/G/H Applied 合同 FREEZE BLOCKED；实现/执行 NOT VERIFIED**
- 分支：session-g-memory-context
- 权威边界：G 拥有期望 Context 与 Applied 记录；C 产生 final-request 证据；H 拥有 Wire/ACK/Capability；I 拥有授权；D 拥有 ForgetFence。

## 1. Context 证据阶段

G 维护彼此独立的 Context、Delivery 和 Entry 生命周期。以下请求绑定阶段必须严格区分：

Prepared → Delivered → Materialized → Final Request Submitted → Applied → Execution Started

- **Prepared：** G 已提交/识别不可变 ContextVersion 及 Delivery 意图。
- **Delivered：** H 对特定 DeliveryId/attempt 提供经过认证的传输接收回执。
- **Materialized：** Adapter 报告精确内容已位于其声明的 Managed Region。
- **Final Request Submitted：** C 提供可信证据，证明精确不可变请求（包括精确 Region digest）已跨越实际 Submit 边界。
- **Applied：** G 验证全部谓词并提交逐请求 Applied 记录。
- **Execution Started：** 与请求关联的 Runtime/Provider execution-start 证据。

G 的 Applied 记录仅表示：指定 ContextVersion 在有效授权/fence/capability 绑定下，被包含在精确提交的请求中。它不证明模型注意、理解、回忆、行为使用或正确性。

## 2. Applied 状态机

Delivery 与 Applied 证据按 Adapter 实例、Runtime Session、Context、Delivery 和 InferenceRequestId 分别记录；单一标量 applied_version 不足以表达该状态。

| 状态 | 进入条件 | 允许的后续状态 | 说明 |
|---|---|---|---|
| Prepared | G 提交不可变目标和 Delivery 意图 | Delivered、Rejected、Expired、Superseded | 尚未发送 |
| Delivered | H 认证的传输接收回执匹配 DeliveryId/attempt | Materialized、Rejected、Expired、Superseded | 尚未 Applied |
| Materialized | Adapter 证据确认精确 Managed Region 和 digest | FinalRequestSubmitted、Rejected、Expired、Superseded | 尚不是最终请求证明 |
| FinalRequestSubmitted | C 证据证明实际不可变最终请求已提交 | Applied、Rejected、Unknown | G 验证谓词；提交事实可作为历史记录保留 |
| Applied | G 接受完整谓词并写入不可变 Applied 记录 | ExecutionStarted、InvalidatedForCurrentUse | 保留历史事实 |
| ExecutionStarted | 关联的 Runtime/Provider start 证据 | 若单独观测，可进入 Completed/Failed | 不代表成功完成 |
| InvalidatedForCurrentUse | 后续 Forget/撤销/Scope/Session/Capability/supersession 使未来复用失效 | ReconcileRequired | 保留历史 Applied 记录 |

Partial/Unknown/Bypassed/Unsupported 是证据处置状态，不是 Full Applied 的同义词。Tier 2 和 Tier 3 不得转入 Full Applied。无法观测最终边界的 Adapter 始终属于 Limited/Unsupported。

## 3. Applied 接受谓词

只有在最终请求 Submit 边界，且以下**全部**条件均通过权威 Owner 证据验证时，G 才接受 Full Applied：

1. ContextId 和精确不可变 ContextVersion 与当前 G 目标匹配。
2. DeliveryId 和 DeliveryAttemptId 与精确、未被 supersede 的 attempt 匹配。
3. InferenceRequestId 和 FinalRequestBoundaryId 均真实、唯一，并绑定同一个请求。
4. Agent principal/reference/instance、Adapter principal/reference/instance、Runtime instance 和 Runtime Session 均已认证、注册、当前有效且相互绑定。
5. 精确 ScopeRef 及所需 EnvironmentRef 与 Context 和授权决议匹配。
6. Managed Region 身份/inventory 及完整 Region 内容 digest 与实际 delivered/materialized 目标匹配。
7. PermissionEpoch 和 I 授权决议在最终 Submit 边界有效且为当前状态。
8. D ForgetFenceGeneration/Cursor 对 Region 中所有 canonical source 及传递 lineage 均为当前状态。
9. H AdapterCapabilityEpoch 为当前状态，绑定该 Adapter 实例/session，并支持最终不可变请求观测。
10. C Final Request Submitted 证据完整、不可变、完整性有效、未重放，并在因果顺序上晚于匹配的 delivery/materialization。
11. 用于绑定认证 Delivery 和 Adapter 实例的 H transport/ACK 证据有效。
12. 在 Submit 前没有任何 supersession、撤销、fence、Scope/Environment 变化、session 替换或 capability 降级先行线性化。
13. 所有必需 source reference 仍具备资格，且不存在未知 coverage 缺口。

缺失、过期、含糊、不可验证或不匹配的证据均拒绝 Full Applied。G 本地推断不得替代 C final-request 证据、H 协议证明或 I/D 权威检查。

## 4. 历史事实与当前有效性

- Applied 记录是只追加的历史证据。
- Forget 或撤销不得改写实际上有效的历史 Applied 事实。
- 当前使用有效性是独立投影，必须根据当前 D fence、I PermissionEpoch/decision、Scope、Environment、Context head、Adapter capability 和 session 重新计算。
- 若有效 Submit 在线性顺序上早于后续 Forget/撤销，则保留 Applied 历史，并标记为 InvalidatedForCurrentUse。
- 若 Forget/撤销在线性顺序上早于 Submit，则不得接受 Full Applied。
- 若无法证明顺序，则标记 Unknown，并抑制该 Region 的未来使用。
- 迟到 ACK 只能增加历史证据；不得回滚更新的 ContextVersion 或 Delivery attempt。
- 相同 identity/digest 的重复证据是幂等的。相同 identity 但 digest 改变属于冲突，不得提升状态。
- 旧 Session/Adapter ACK 绝不能重新绑定到新 session 或 capability epoch。

## 5. Forget 与撤销处理

D ForgetFence 推进或 I 撤销/PermissionEpoch 变化时，G 必须立即安装持久化 deny tombstone，按 canonical source identity、传递 lineage 和精确 Scope coverage 建立键。物理清理之前，G 必须：

1. 抑制受影响 ContextEntry 的 materialization 和 canonical dereference。
2. 将受影响 ContextVersion 标记为不可服务于新请求；历史不可变版本仅用于审计。
3. 使受影响 ChangeSet 失效，并阻止过期 staged edit 提交。
4. 使包含受影响条目的 Snapshot 和 Delta 失效；过期目标不得发送。
5. 取消/supersede Pending Delivery，以及最终门禁尚未通过的所有活动 attempt。
6. 将历史 Applied 引用标记为 InvalidatedForCurrentUse；不删除历史事实。
7. 使 G cache/queue 和任何 reconnect 恢复状态失效。
8. 发出 G 自有的、按 action 区分的 target evidence；不得声称 F index/cache purge 或 H Adapter 本地 purge 已完成。
9. 只有重新验证 canonical lineage、D fence 和 I permission 后，才将当前 Context head reconciliation 到新的安全版本。

Context Remove 仅表示成员关系移除。它不是 Canonical Forget，也不能满足 Forget target。

## 6. 对象处置矩阵

| 对象 | Forget/撤销动作 | 审计/历史规则 |
|---|---|---|
| ContextEntry | 抑制、标记失效，并从当前期望成员关系中移除 | 按策略允许保留不可重建的身份/provenance 元数据 |
| ContextVersion | 禁止用于服务；创建不含已 Forget/未授权内容的后继版本 | 保留不可变历史版本，绝不重放 |
| ContextChangeSet | Pending 时取消/拒绝；若已提交但未 Delivery，则重新验证 | 保留 digest 和处置结果，不保留已 Forget 明文 |
| Snapshot | 若包含受影响 lineage 或授权过期，则失效并标记为不可发送 | 仅保留历史 digest/target 元数据 |
| Delta | 若 base/target 链包含受影响 lineage 或授权过期，则失效 | 不得跨 tombstone/supersession 重放 |
| Pending Delivery | 取消/supersede；在最终门禁拒绝发送/应用 | 保留 attempt 和取消证据 |
| Applied Context | 保留历史 Applied 事实；使当前使用资格失效 | 未经新的授权/reconciliation 不得复用 |
| Cached Context | 立即抑制并失效；清除能力范围内的本地字节 | 没有证明不得声称物理擦除 |
| Reconnect State | 使旧 session snapshot/delta/ACK 失效；强制重新认证和 reconciliation | 保留最小 replay-deny 标记及审计证据 |

即使 ContextVersion 未变化，PermissionEpoch 变化仍要求重新授权。相同版本的 Context 不能证明当前权限有效。

## 7. Reconciliation 与 reconnect 协议

Reconnect 是新的信任边界，不是旧本地状态的延续。

1. H 认证当前 Adapter/Agent/Runtime 身份并建立新 session。
2. H 协商当前协议/capability profile 和 CapabilityEpoch。
3. I 提供当前 PermissionEpoch 及精确 action/Scope 授权。
4. D 为每个 source/lineage 提供当前 ForgetFence 状态。
5. G 持久化/验证 deny tombstone，并取消过期 Delivery/attempt。
6. Adapter 按其声明能力抑制/清除本地状态；H 发出按 action 区分的证据（SUPPRESSED、LOCAL_BUFFER_CLEARED、LOCAL_CACHE_PURGED、QUEUED_DELIVERY_CANCELLED、FAILED、UNKNOWN、UNSUPPORTED）。
7. G 读取权威的当前 Context head、delivery ledger、期望目标及未解决 attempt。
8. 若旧 Snapshot 已 supersede、被 tombstone、过期、跨 Scope 或未授权，则拒绝。旧 Delta 只有在其精确 base 等于当前已知 Adapter base，且 target 仍为当前且已授权时才可接受。
9. Continuity 未知时，只有在当前身份/permission/fence 检查通过后才允许新的完整 Snapshot；权威状态未知时必须阻断，而不是重放 Snapshot。
10. 在 apply 前以及最终 Submit 前，立即重新验证 PermissionEpoch、D fence、ContextVersion/delivery 状态、expiry/supersession 和 CapabilityEpoch。
11. G 仅通过 §3 的谓词接受 Applied。
12. Reconnect 完成仅表示本 session 已与当前获授权 Context target 对齐；不代表全局 Forget 完成或物理擦除。

在上述流程完成前，不得重放任何旧排队 payload 或旧 Session ACK。离线状态保持 Pending/Unknown，绝不能隐式视为已清除。

## 8. 一致性矩阵

本设计阶段所有案例均为 **SPECIFIED / NOT RUN**。测试 Passed 必须提供可执行 fixture、确定性并发顺序、环境、预期/实际输出、持久化证据和 Owner 签字。

| ID | Fixture / 操作顺序 | 预期 | 禁止行为 | 证据 |
|---|---|---|---|---|
| G-36-01 | 已 Materialized，但无 final submit evidence | 仅 Materialized；无 Applied | Materialized→Applied | Region receipt；缺少 C submit evidence |
| G-36-02 | Final submit evidence 有效，G 接受尚待完成 | 仅 FinalRequestSubmitted | 谓词提交前声称 Applied | C evidence 和 G validation record |
| G-36-03 | 完整谓词通过 | G 提交逐请求 Applied | 推断模型理解 | 所有谓词引用和不可变 Applied 记录 |
| G-36-04 | Applied 决策前 PermissionEpoch 变化 | Reject/Unknown；重新授权 | 接受过期权限 | 新旧 Epoch 和决议 |
| G-36-05 | Delivery 期间 Fence 推进 | Tombstone、取消/supersede，不产生新 Applied | 发送/应用过期 Snapshot | Fence、Delivery attempt、取消证据 |
| G-36-06 | 有效 Applied 后发生 Forget | 保留历史；标记当前使用无效 | 改写历史或复用 | Applied 记录、Fence 和失效证据 |
| G-36-07 | 已 supersede 的 ContextVersion 收到迟到 ACK | 仅历史证据；当前指针不变 | 回滚当前版本 | 新旧版本及 ACK 顺序 |
| G-36-08 | 相同 digest 的重复 ACK | 幂等 | 重复提升状态 | ACK identity/digest 和先前结果 |
| G-36-09 | digest 不同的重复 ACK | Conflict/quarantine | Last-write-wins | 两个 digest 和审计事件 |
| G-36-10 | Reconnect 后收到旧 Session ACK | 拒绝或仅作历史证据 | 重新绑定新 session | 新旧 session 和 capability epoch |
| G-36-11 | 跨 Scope Delivery 尝试 | Materialization 前拒绝 | 跨 Scope 内容 | 强类型 Scope 和 I 决议 |
| G-36-12 | ContextVersion 不变但 PermissionEpoch 变化 | 复用前重新授权 | 把版本当作权限证明 | ContextVersion 及新旧 Epoch |
| G-36-13 | Reconnect 提供旧 Snapshot/Delta | 抑制/清除后 reconciliation；拒绝过期工件 | 先恢复、之后再清理 | 当前权威向量及过期拒绝证据 |
| G-36-14 | 未发生 Canonical Forget 的 Remove 操作 | 仅移除成员关系 | 声称 canonical 删除/全局 Forget | ChangeSet 和 D operation absence |
| G-36-15 | Forget 与最终请求 Submit 竞争 | 由 D/I 边界顺序决定；不明确则阻断 | 在过期 Fence 下 Submit 或虚构顺序 | D fence、I 决议、C boundary proof |

## 9. Prompt injection / 信任边界

Context 是数据区域，不是指令区域。Entry 携带 source refs、provenance、trust/epistemic 和 lifecycle 状态、Scope、classification 与 validity。Summary/compaction 是派生的不可信工件，必须保留 provenance/lineage 和 trust label。任何内容都不得进入 system/developer instructions、tool definitions、tool authorization 或 Agent policy。跨 Scope 条目必须拒绝。Memory 中的 tool-call 声明不是执行证据。

## 10. 开放发现与决议记录

- **G-36-01 BLOCKED：** C evidence schema/integrity 和 final-boundary proof 需要 C/H 达成一致。
- **G-36-02 BLOCKED：** H ACK/capability/reconnect Wire 合同仍由 H 负责，尚未冻结。
- **G-36-03 BLOCKED：** I PermissionEpoch freshness/revocation 及 B typed identity/Scope 语义需要 Owner 批准。
- **G-36-04 BLOCKED：** D/E/Storage 物理 Forget publication atomicity 和 durable gate 尚未经过实现验证。
- **G-36-05 NOT RUN：** 未提供可执行 Applied、race、reconnect、stale replay 或 injection 测试结果。

**G 决议：** G 是 Applied 状态的权威；Applied 必须有完整请求绑定证据；历史 Applied 与当前使用有效性分离；Forget/撤销使所有当前 Delivery/reconnect 表面失效，但不改写历史；Context Remove 不等于 Canonical Forget；Reconnect 在恢复 Context 前必须重新认证并 reconciliation 当前权威状态。

**跨模块状态：** Applied Contract Frozen = NO。Runtime Forget End-to-End Closed = NO。没有声称全局 Forget 完成或物理擦除。

## Phase 3.6 CFG 联合架构闭合补充 — G Owner 决议

- 决议包：A Owner 的 `reviews/integration/phase-3.6-cgh-applied-contract-decision-package.md`
- 已审阅的精确 package Blob SHA：`61d961c32138fd875069e8cbac4696bb031447c0`
- G 决议：对 G 自有 ContextVersion、Delivery 和 Applied 语义 **APPROVE WITH ENUMERATED EXCEPTIONS**。这不是全局冻结，也不是 H 的批准。

### G 接受的条款

1. G 拥有期望 Context 状态、不可变 ContextVersion、ChangeSet commit、Delivery intent/target、reconciliation 和权威的逐请求 Applied 记录。G 不拥有 canonical Memory mutation/Forget、BMCP Wire、Agent reasoning 或 tool execution。
2. 生命周期严格为 `Prepared → Delivered → Materialized → Final Request Submitted → Applied → Execution Started`，每次转换都有独立证据和权威。G 不得从较早的 receipt 推断较后的状态。
3. Full Applied 必须绑定精确 ContextId/ContextVersion + DeliveryId/attempt + InferenceRequestId + FinalRequestBoundaryId + 认证的 Agent/Adapter/Runtime/Session + Scope/Environment + ManagedRegion revision/inventory + 完整 digest/profile + 当前 I PermissionEpoch/decision + 当前 D ForgetFence/lineage + H CapabilityEpoch + 有效 H delivery/identity proof + 不可变 C submission proof。所有谓词均须验证；缺失、过期、不匹配、含糊或不可验证的证据均拒绝 Full。
4. G 按精确 request/attempt/evidence identity 幂等提交 Applied。精确重复 digest 返回原 disposition；相同 identity 但 digest 改变则 conflict/quarantine。迟到证据只能增加历史事实，不能回滚更新的 ContextVersion 或 Delivery attempt。
5. 历史事实与当前使用资格分离。若证明 Submit 先于后续 Forget/撤销，可保留历史 Applied，但当前使用资格失效。若 Forget/撤销先于 Submit，则拒绝 Full。顺序含糊时为 Unknown 并抑制。
6. Execution Started 是绑定同一 InferenceRequestId 的独立 Runtime/Provider 事实；G 不从 Applied 推断。
7. Remove 仅移除 Context 成员关系。它不创建 canonical ForgetOperation、不推进 D fence，也不证明删除。D Forget 按 canonical lineage 和精确 Scope 独立 tombstone 所有匹配的 G entry。
8. 在物理清理前，G deny tombstone 抑制受影响 entry、不可服务的 ContextVersion、ChangeSet、Snapshot、Delta、Pending Delivery attempt、reconnect 状态及当前使用投影。历史审计事实在 I 保留策略允许范围内保持不可变。
9. Reconnect 是新的信任边界：H 认证并协商新 session/capability；I 和 D 提供当前独立 Epoch/Fence；G reconciliation tombstone、delivery ledger 和当前 head；旧 Snapshot 若过期/supersede/tombstone/未授权则拒绝；Delta 要求精确已知 base 和当前 target；continuity 未知时，只有当前检查通过后才允许新完整 Snapshot。apply 前和 final Submit 前再次验证。

### 列明的例外与外部权威保留项

- **H Wire 例外：** G 接受 Delivery receipt、materialization evidence、final-submit evidence、Applied record 和 Execution Started receipt 的语义分离。G 不冻结 H message schema、ACK enums、signature profile、Wire field encoding、replay journal 或 capability negotiation。H 必须明确接受同一个 package Blob SHA，或发布新公共版本。
- **C producer 例外：** G 不能制造 final-request proof；C 仍是精确 Submit 证据的唯一生产者。C 决议必须固定到该 package 和 evidence profile。
- **I authorization 例外：** 只有 I 定义 PermissionEpoch、Principal/Issuer/delegation、revocation 和 policy freshness。G 要求当前决议，但不定义策略。
- **D Forget 例外：** 只有 D 定义 ForgetOperation/Fence/lineage 权威及顺序。G 消费 D 当前 Fence 和 durable target evidence。
- **B type 例外：** B 拥有 ActorRef/ScopeRef/EnvironmentRef 强类型语义；G 不重新定义。
- **D/E/Storage publication 例外：** G ChangeSet 可以私有 staged，但在 dependency registration、当前 D fence、当前 I PermissionEpoch、D final publication gate 和 G BaseVersion CAS 全部得到证明前，不得成为公开 Context head、可发送 Snapshot/Delta 或 Prepared Delivery。可调用 API/物理事务实现仍由 D/E/Storage 处理。

### 再次确认的 Context 操作与版本规则

- Add/Update/Remove/Replace/Reorder/Expire/Compact/Reconcile 都是针对一个 Context 和精确 BaseVersion 的 ChangeSet 操作；必须有确定性操作顺序和幂等 identity。
- 在 staged working copy 上验证；不得让部分 target version 可见。成功的非 no-op ChangeSet 创建一个不可变 ContextVersion；stale base 必须 conflict/reconcile，不得静默 rebase。相同 payload 的重复 operation identity 幂等；payload 改变则 conflict。
- Remove 只写入 G membership tombstone。Replace 在 ContextVersion publication 时原子完成；Reorder 只改变成员顺序；Expire 按权威时间/策略评估且不得在 replay 时复活；Compact 保留 provenance/trust/conflict label 和 lineage；Reconcile 重新验证 canonical refs、permission、temporal validity、retrieval freshness 和 Adapter 状态。
- Context entry 只引用合法的 canonical MemoryVersionRef。过期 canonical ref 只有在 D lifecycle 语义及当前 I 授权允许时，才可 reconciliation 到合格后继版本；不得隐式 float-to-latest。

### G 决议后果

G 认为 A package 中属于自身语义的部分已按上述例外获接受。C/G/H Applied Contract 在 H 明确接受同一版本，且 I/D/B 提供各自权威确认前，仍然 **NOT FROZEN**。G conformance 仍为 **SPECIFIED / NOT RUN**；实现仍为 **NOT VERIFIED**。

## Phase 3.6.3 — Issue #3 G 精确版本 Owner 决议

- Owner：G — ContextVersion、Delivery、reconciliation 与 Applied 状态权威。
- 精确共享 package：`reviews/integration/phase-3.6-cgh-applied-contract-decision-package.md`，Blob SHA `122b164bcc0760b83bf555072a36fc55631623e1`。
- 决议：对 G 自有 Context/Delivery/Applied 条款 **APPROVE WITH ENUMERATED EXCEPTIONS**。这是 G 对 Issue #3 的明确决议，不是全局冻结。
- 公共合同版本：**CGH-APPLIED-1.0**，锚定上述精确 package Blob。
- G 拥有权威的逐请求 Applied 记录。Full Applied 要求精确 ContextId/ContextVersion、DeliveryId/attempt、InferenceRequestId、FinalRequestBoundaryId、认证的 Agent/Adapter/RuntimeSession、verifier-resolved ActorRef、role-tagged ScopeBindingSet、适用 EnvironmentRef、完整 ManagedRegion revision/inventory/digest/profile、当前 I PermissionDecision/PermissionEpoch、当前 D ForgetFence/lineage、H CapabilityEpoch、认证 H ACK，以及不可变 C final-submit proof。
- Commit/幂等：按精确 request/attempt/evidence identity；相同 identity+相同 digest 返回原 disposition；相同 identity+不同 digest 为 conflict/quarantine。迟到证据不得回滚更新的 ContextVersion 或 Delivery attempt。
- 时间规则：证明 Submit 先于后续 Forget/撤销时，可保留历史 Applied，但当前使用无效；Forget/撤销先于 Submit 时拒绝 Full；顺序未知则保持 Unknown 并抑制。发送方 wall clock 不是排序权威；必须使用 Owner 权威 commit cursor 和可信接收方 receipt sequence。
- 例外：G 不拥有 C final-request evidence、H Wire encoding/cryptography、I authorization/PermissionEpoch policy、D ForgetFence/lineage、B typed references 或 Storage publication atomicity。这不证明执行、注意、理解、回忆、全局 Forget 或物理擦除。
- 负面案例（缺少 C proof、H binding 无效、Epoch/Fence 过期、Scope/Environment 不匹配、Tier 不支持、Delivery 过期、重复 digest 改变、顺序含糊）均拒绝 Full 或保持历史/Unknown。
- CGH-01..20 保持 **SPECIFIED / NOT RUN**。

## Phase 3.6.3 — Issue #6 G BIH 消费方接受

- 精确 BIH package：`reviews/integration/phase-3.6-identity-trust-joint-architecture.md`，Blob SHA `a45ae90b318a79bf009d14f4d917611881e9e214`。
- 处置：作为 BIH36-JD-01..17 的下游消费者 **ACCEPT WITH ENUMERATED EXCEPTIONS**。
- 映射：G 将认证 Principal/Issuer 和 Adapter/Agent workload instance 绑定到 RuntimeSession；ActorRef 必须由 verifier 解析并绑定具体操作。G 在 Context、Delivery、Applied 和 reconciliation 记录中保留精确 ScopeRef role set 和适用 EnvironmentRef。PermissionEpoch 是 opaque 且由 I 签发；ForgetFence 是独立的 D 签发 token；CapabilityEpoch 由 H 拥有。
- 强制执行：在 Delivery 授权前、认证 receipt/materialization 时，以及 Applied commit 时，G 验证当前 I decision/epoch、精确 ContextVersion/Delivery attempt、H 认证 Adapter/session/capability 证据、D fence/lineage 和 C 不可变 final-submit 证据。Reconnect 在重新认证和当前权威检查后，reconciliation G 的 durable delivery/ACK journal。
- Fail closed：仅 payload 身份、未知/撤销的 issuer 或 Adapter、伪造 ActorRef、缺失 Scope/Environment、缺少显式跨 Scope/Environment grant、过期/不可比较 Epoch、过期/未知 Fence、capability 不匹配、旧 session ACK、重复 digest 改变或因果顺序未知，均不得修改 Applied 状态；应按情况拒绝/隔离、仅保留历史或标记 Unknown。
- 例外：G 不定义 B identity type、I trust/authorization policy、H Wire cryptography/serialization、D fence 签发、C submit evidence 或 Storage atomicity。外部治理和 Runtime conformance 是独立事项。
- G Applied/reconciliation 矩阵仍为 **SPECIFIED / NOT RUN**。

## G Owner 精确版本决议 — CGH-APPLIED-1.1

- A package：`reviews/integration/phase-3.6-cgh-applied-1.1-causal-order-decision-package.md`
- 精确 A package Blob SHA：`9808b31f840606b329f1a794935dfc9c5084d63b`
- 公共合同：`CGH-APPLIED-1.1`
- 因果配置：`CausalOrderProfile/1.0`
- H Schema 目标：`bmcp.applied-ack/1.1.0`

**决议：ACCEPT WITH ENUMERATED EXCEPTIONS**，仅在 G 对 Full Applied 谓词、durable Applied fact/idempotency 以及 historical/current-use 投影的独占权威范围内有效。

G 接受 1.1 证据集作为 Applied 决策所需的因果顺序输入：精确 G target/context/delivery attempt；C 实际 Provider receipt 和不可变 CSubmitOutcome；I receipt 和 terminal proof（包括 revocation cutoff）；D intent-bound clearance 及 lineage/fence cutoff/effective evidence；H 完整性保护的 transport/schema evidence；B 强类型引用；以及绑定同一 transaction、digest、reservation 和 terminal outcome 的确定性 CausalOrderTerminalProof。G 不会仅凭 I COMMIT_WON、D clearance、reservation、intent 或 transport ACK 推断 Full Applied。

G 对 1.1 的 Applied 规则：只有在验证完整谓词和确定成功的 C Provider handoff 后，才提交历史 Full Applied；历史事实必须与当前使用资格分离，后者要根据当前 Context head、I authorization/PermissionEpoch、D fence/lineage、scope/environment、session 和 capability 重新计算。后续撤销/fence/supersession 不得改写有效历史事实，但会立即使其不再具备受保护使用资格。任何顺序未知、lineage 不完整、Owner 证据缺失/矛盾、Provider outcome 未知或 digest 冲突，都不得提升为 Full，必须保持 suppressed/UNKNOWN。

例外与闭合条件：
1. Coordinator 和 durable participant/order service 尚未指定/部署/验证。G 的接受以持久化、单调 terminal proof 以及不会清除 IN_DOUBT participant 的 recovery 为条件。
2. 尚未证明 G validator 和 Applied persistence 实现消费完整 1.1 证据集。这是合同接受，不是实现验证。
3. 相同 transaction/idempotency key 且 digest 相同必须幂等；相同 identity 但 digest 改变必须 conflict/quarantine，绝不能 last-write-wins。G durable commit 和 recovery 行为仍需测试。
4. 历史 Applied 不授权当前使用；当前使用投影必须在 I/D/current-context 证据过期或缺失时 fail closed。
5. G-CO/Applied race 和 recovery conformance 仍为 SPECIFIED / NOT RUN；不声称 Runtime pass。

本决议仅适用于上述精确 A Blob，不转移先前 1.0 决议，不证明全局 Forget，也不代表实现/部署。

## G Owner 精确版本再次确认 — 当前 CGH-APPLIED-1.1 候选

- A candidate Blob SHA：`d4eef4aecf94f922f7933c1e1fec14a69ad17dec`
- Profile：`CausalOrderProfile/1.0`；H Schema：`bmcp.applied-ack/1.1.0`

**决议：ACCEPT WITH ENUMERATED EXCEPTIONS**，仅在 G 对 Full Applied、durable Applied 幂等性及 historical/current-use 投影的独占权威范围内有效。

G 接受候选版本的完整 1.1 谓词：精确 G ContextVersion/Delivery attempt；C 实际 Provider receipt 和 CSubmitOutcome；I single-use receipt 和 I sequencer terminal evidence（包含 revocation request cutoff 或明确的 none）；D intent-bound participant clearance、完整 lineage、request cutoff 及独立的 effective position；H 完整性保护的 1.1 transport；B 强类型引用语义；以及绑定同一 transaction、digest、reservation 和 terminal result 的确定性 CausalOrderTerminalProof。G 不会仅凭 I COMMIT_WON、D clearance、intent、reservation 或 H ACK 提升 Full Applied。

G 接受 COC outage admission safety 规则作为强制 fail-closed 前置条件：若 coordinator ordering 或 owner cutoff reconciliation 不可用/未知，G 不得提交新的 Full Applied 记录，并必须抑制受保护的当前使用。G 不得从缺失的 coordinator 证据推断不存在 revocation/fence。历史 Applied 一旦有效提交，仍是不可变历史事实；当前使用必须根据当前 Context head、I authorization/PermissionEpoch、D fence/lineage、scope/environment、session 和 capability 单独重新计算。

例外：(1) coordinator/operator 和 durable participant/order service 尚未指定/部署/验证；(2) 尚未证明 G validator 和 Applied persistence 实现消费完整 1.1 证据集；(3) 相同 identity/digest 重放的幂等性及 digest 改变时的冲突行为仍需可执行 recovery 测试；(4) G-CO/Applied race suites 仍为 SPECIFIED / NOT RUN。不声称实现或生产通过。本决议仅适用于上述精确 A Blob，不转移 1.0 决议。

## G 精确版本 Applied 接受 — CGH-APPLIED-1.1 recovery-batch 修订

- A package Blob：`4961ffefc0f9920efb8425a9b2a7af42d8f64819`
- Companion COC Blob：`fc3bac39ec64fda68b8cba5e1aada4e719e5acea`
- Profile：`CausalOrderProfile/1.0`

**决议：ACCEPT WITH ENUMERATED EXCEPTIONS**，仅在 G 对 Full Applied 谓词、durable Applied fact/idempotency 和 current-use projection 的权威范围内有效。

G 接受 recovery-cutoff batch 和 pre-batch participant reconciliation，作为任何新 Full Applied promotion 的强制证据前置条件。若 COC order、owner-local pending gate reconciliation、participant enumeration、I terminal outcome、D complete-lineage barrier 或 owner high-water proof 缺失/未知，G MUST NOT 提交新的 Full Applied 记录，并 MUST 抑制受保护的当前使用。G 不得从 COC outage 或 Owner 消息缺失推断不存在 revocation/fence。Recovery batch 本身不证明 C Provider 成功；仍要求精确 CSubmitOutcome 和确定的 CausalOrderTerminalProof。

历史 Applied 只有在当时依据证据谓词有效提交时才保持不可变；当前使用必须独立根据当前 I/D/Context/session/capability 状态重新计算。

例外：(1) 尚未证明 G validator/Applied persistence 实现消费全部 recovery-batch 证据；(2) 相同 identity/digest 重放、冲突隔离和 restore 行为需要可执行测试；(3) G-CO/Applied race suites 仍为 SPECIFIED / NOT RUN；(4) 不声称实现或生产通过。本决议仅适用于上述精确 A/COC Blob 配对。
