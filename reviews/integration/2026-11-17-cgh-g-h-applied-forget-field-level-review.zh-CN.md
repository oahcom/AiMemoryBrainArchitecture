# C/G/H Applied、Forget 与 Reconciliation 字段级跨 Owner 一致性审查

- 日期：2026-11-17
- 范围：针对 C 最终请求证据文件组、G Applied/Forget/Reconciliation 契约、H Adapter Capability/Applied Attestation 契约，以及精确的 CGH-APPLIED-1.1 recovery-batch 决议记录开展独立复核。
- 审查性质：基于仓库工件的委派角色模拟审查；不构成独立人类 Owner 签署。
- 结论：**语义对齐部分通过；ACK 身份字段仍需统一；Wire 冻结受阻。**

## 1. 精确源文件与决议版本

| 项目 | 分支 / 工件 | Blob SHA 或精确引用 |
|---|---|---|
| C Final Request Evidence | `session-c-agent-integration-2026-11-16` / `07-agent-integration/phase-3.6-final-request-evidence-contract.md` | `fd2f47ba6c89bb270e9f2bec956873cb7ae3592b` |
| C 因果顺序 / recovery-batch 补充契约 | `session-c-agent-integration-2026-11-16` / `07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md` | `45a48249717c8cddb07ab96197730ef93d406c22` |
| G Applied / Forget / Reconciliation | `session-g-memory-context` / `06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md` | `aa3afa73d8a76cc6f025839c52bfbff6a983046a` |
| H Adapter Capability / Applied Attestation | `session-h-bmcp-protocol` / `08-bmcp-protocol/adapter-capability-and-applied-attestation.md` | `74be8374a67da385a5f0f8e34c7aef2b38b72bcf` |
| A 共同 recovery-batch package | `CGH-APPLIED-1.1` | `4961ffefc0f9920efb8425a9b2a7af42d8f64819` |
| 配套 COC 架构 | `CausalOrderProfile/1.0` | `fc3bac39ec64fda68b8cba5e1aada4e719e5acea` |
| C 精确版本决议工件 | Issue #3 精确决议对账 | `a72a3eb1e5207f67c01f804508311f42db9a6e0a` |
| H 精确版本决议工件 | Issue #3 精确决议对账 | `22853b21d583d2cae75eb3ef1c580c68b4cf4c70` |
| G 精确版本决议工件 | G 源决议 / Issue #3 对账 | `aa3afa73d8a76cc6f025839c52bfbff6a983046a` |

Issue #3 的精确决议记录表明：C、G、H 均针对同一个 A package Blob `4961ffefc0f9920efb8425a9b2a7af42d8f64819` 和 COC companion Blob `fc3bac39ec64fda68b8cba5e1aada4e719e5acea` 作出了附带列明例外的接受决议。这修正了此前“H 尚未接受同一精确语义 package”的说法。

**关键范围区分：** H 对 A/COC 语义 package 的精确接受，不会自动把 H Adapter Capability §11.8–11.9 从 CANDIDATE 升格为已冻结 Wire Schema。H 源文件仍明确将 §11.8–11.9 标为候选映射，并要求补充精确 Schema/SDK 映射及相关消费者确认。精确 package 语义接受与精确 Wire 字段/Schema 接受是两个独立决议。

## 2. 六阶段生命周期

三个契约均保留相同的六项事实及权威边界：

1. **Prepared（已准备）**——G 提交不可变 ContextVersion 和 Delivery intent。
2. **Delivered（已送达）**——H 对精确 DeliveryId/attempt 的传输接收进行认证。
3. **Materialized（已物化）**——Adapter 证据标识精确 Managed Region、revision/inventory 和 digest。
4. **Final Request Submitted（最终请求已提交）**——C 证明经过全部转换的不可变请求，已跨越声明的成功提交边界。
5. **Applied（已应用）**——只有 G 可以验证完整谓词并提交逐请求 Applied 记录。
6. **Execution Started（执行已开始）**——由与同一 InferenceRequestId 关联的独立 Runtime/Provider 启动回执证明。

**结果：语义层面 PASS。** 不得从前一阶段推断后一阶段。特别是：传输 ACK 不等于物化；物化不等于最终请求提交；C 的提交证据不等于 G 的 Applied；Applied 不等于执行开始，更不证明模型关注、理解、回忆或行为正确。

## 3. C → H → G 字段映射

| 证据概念 | C 生产者契约 | H 承载 / Attestation | G 消费谓词 | 审查结果 |
|---|---|---|---|---|
| 请求身份 | Runtime/Provider 实际分配的 InferenceRequestId + FinalRequestBoundaryId 和边界类型 | `inference_request_id`、`final_request_boundary_id`、边界类型 | 同一精确 request/boundary 身份 | 对齐 |
| G 目标 | ContextId/ContextVersion + DeliveryId/DeliveryAttemptId | `context_id`、`context_version`、`delivery_id`、`delivery_attempt_id` | 精确的当前且未 supersede 的 G 目标/attempt | 对齐 |
| 物化状态 | Managed Region identity/inventory 和实际完整 digest | `materialized_context_version`、region ID/revision/inventory digest/coverage/content digest/profile | 完整目标与 region digest 匹配 | 对齐；Full 必须 COMPLETE |
| 身份 | 受保护认证绑定中的 Agent/Adapter/Runtime/Session | verifier-resolved principal/actor/instance/session refs；transport principal 不能替代 | 当前且相互绑定的身份；G 消费 B/I 语义 | 权责对齐；精确 Wire 编码仍开放 |
| Scope / Environment | 精确 ScopeRef 和适用的 EnvironmentRef | `scope_ref`、`environment_ref` | 精确保留角色的 scope/environment 绑定 | 对齐；禁止 payload fallback |
| 授权 | 最终提交时的 I PermissionEpoch 和 decision | I 签发的 `permission_epoch_ref`、`permission_decision_ref`，以及 §11.8 的 I terminal/revocation 证据 | 当前 I decision/epoch 与因果 terminal 证据 | 语义对齐；Wire requiredness/profile 未冻结 |
| Forget | D ForgetFence generation/cursor 和 lineage validation | D fence generation/cursor/validation ref；§11.8 D lineage、request cutoff 和 effective position | 当前 D fence 和完整 lineage；未知时抑制 | 语义对齐；必须区分 cutoff 与 effective position |
| Capability | H CapabilityEpoch/profile | `adapter_capability_epoch`、capability profile 和逐请求 coverage | 精确 Adapter/session 当前 capability epoch；只有 Tier 1 可申请 Full | 对齐 |
| Provider outcome | C 因果顺序补充契约要求真实 provider receipt 和不可变 CSubmitOutcome | §11.9 的 `c_provider_receipt_ref`、`c_submit_outcome_ref` | G 要求确定且成功的 C outcome，不能只凭 reservation/ACK | 语义对齐；H 字段映射仍是候选 |
| 因果 terminal | CausalOrderTransaction/Intent/Reservation/TerminalProof 和精确 digest | §11.8 COC refs、terminal proof/digest、recovery batch、完整 participant/high-water 证据 | G 仅在完整且确定的因果证明后接受 Full | 语义对齐；精确 message-family Schema 未冻结 |
| Owner gate release | I/D 仍是唯一权威 | `owner_gate_release_attestation_ref` 必须由对应 Owner 签发 | G 不把 COC/H observation 当作 I/D release | 对齐 |

C Final Request Evidence 基础文件与 C 因果顺序补充文件必须作为组合后的 producer contract 阅读。仅凭基础文件并不包含完整 recovery-batch/provider-outcome 证据集；独立的 C 补充契约才提供精确 CGH-APPLIED-1.1 接受决议，以及 C 所有的 CSubmitOutcome/provider receipt 要求。

## 4. P1 — ACK/evidence 身份元组尚未规范性统一

C §6 将 evidence identity 描述为 Adapter instance + Runtime Session + DeliveryId + attempt + evidence kind + digest。H §11.6 提出的元组是：

`(adapter_instance_ref, runtime_session_ref, delivery_id, delivery_attempt_id, inference_request_id, final_request_boundary_id, evidence_kind, adapter_capability_epoch)`

H 随后将 canonical payload digest 作为独立内容进行比较：相同元组 + 相同 digest 是幂等；相同元组 + 不同 digest 是 CONFLICT。

这两种定义并非逐字段等价。更重要的是，如果 C 将 digest 本身纳入 identity key，那么 digest 改变后可能被视为另一个 identity，而不是同一 identity 的冲突 payload。

**必须进行的规范性修正：**
- 定义不包含 payload digest 的稳定 evidence identity 元组。
- 在稳定元组中纳入精确 request/boundary 和 capability epoch，或者明确证明更窄身份范围的安全性。
- 将 canonical payload digest 视为绑定到该 identity 的不可变内容，而不是 key 的组成部分。
- 相同 identity + 相同 digest → 返回原持久化 disposition。
- 相同 identity + 不同 digest → CONFLICT/quarantine；禁止 last-write-wins。
- G 的持久化 Applied 幂等键必须明确映射到该 evidence identity，以及 1.1 profile 的精确 CausalOrderTransaction/ParticipantIntent/Reservation identity。

在 C、G、H 对同一个精确元组作出记录前，ACK 幂等性只能判定为**语义意图一致，但字段级尚未完全冻结**。

## 5. 迟到证据与 Supersession

C、H、G 的语义方向一致：
- 旧 attempt 或已 supersede attempt 的迟到证据，只能保留为历史证据。
- 不得回滚较新的 ContextVersion 或 Delivery attempt。
- 旧 Adapter/Runtime Session 证据不得重新绑定到替换后的 session 或 CapabilityEpoch。
- 没有满足全部当前权威和因果谓词的迟到 ACK，不得提升为 Full Applied。
- 同一稳定 identity 下 digest 改变是冲突，不是第二个有效 ACK。

**结果：语义方向 PASS；精确共享 identity 元组仍是 P1。**

## 6. Forget / 撤销 / Provider 副作用的竞争顺序

组合后的 1.1 profile 不是单一时钟。以下权威及顺序域必须保持区分：

- COC causal-order epoch/position/entry digest；
- I policy-domain sequencer epoch/position/decision digest；
- D fence request cutoff 和后续 effective position；
- Storage transaction/resolution position；
- C 实际 provider receipt 和 CSubmitOutcome。

规范性竞争结果：

1. I receipt consumption 之前发生的 revocation 可以胜出并阻止准入。
2. I 已将精确 receipt terminalize 为 COMMIT_WON 后，后续 revocation 必须等待该未决 participant；不得按 H 到达时间或 wall clock 静默重排。
3. ParticipantIntent cutoff 之前的 D fence request 会拒绝该 intent。
4. Intent 之后提出的 D fence 必须纳入较早的未决 participant；在安全 terminal resolution 前不得越过它生效。
5. 在持久化 intent、兼容的 I/D 证明及 coordinator reservation 之前，C 不得调用 provider。
6. Provider timeout/crash/结果不明确时，必须保持 UNKNOWN/IN_DOUBT；不得作为新 transaction 重试，不得生成新的幂等身份，I/D barrier 必须保持。
7. Recovery batch 必须枚举全部 pre-batch participant，证明枚举完整性和 Owner high-water，并协调 I/D/C/Storage outcome。缺少列表不等于空列表。
8. COC recovery observation 本身不是 I/D Owner gate release。只有对应 Owner 签署的 disposition 才能重新开放其 gate。
9. 如果成功提交被证明早于后续生效的 Forget/revocation，保留历史 Applied，但立即使当前使用资格失效。如果 Forget/revocation 先于 submit 胜出，则拒绝 Full。顺序未知时，必须抑制并保持 UNKNOWN/IN_DOUBT。

**结果：针对精确 1.1 recovery-batch package 的语义决议层面 PASS，但受列明例外约束。** H §11.8–11.9 仍需精确 Schema/SDK 表达；生产 coordinator、provider 幂等性和 Storage/JF-10 仍未验证。

## 7. Forget 行为与 Reconciliation 义务

G 契约正确地区分了以下事项：
- Context Remove 只是成员关系移除，不是 Canonical Forget。
- D 拥有 canonical ForgetOperation/Fence/lineage；G 消费 D 的证据。
- G 建立持久化 deny tombstone，并抑制受影响的 Entry、ContextVersion、ChangeSet、Snapshot、Delta、Pending Delivery、缓存/队列及 reconnect 状态。
- G 保留有效历史 Applied 事实，但在后续 Forget/revocation 后标记为 InvalidatedForCurrentUse。
- H Forget ACK 与 Applied Attestation 是不同证据族，不能证明 global Forget 或 provider 删除。
- Reconnect 是新的信任边界：重新认证、重新协商 capability、刷新 I/D 权威状态、协调 tombstone 和 delivery ledger、拒绝陈旧 Snapshot/Delta/ACK，然后在 apply 和 final submit 前重新验证。
- 权威证据缺失或未知时 fail closed；不得重放旧 payload 或旧 ACK。

这些契约均不能证明 global Forget completion、物理擦除、F index/cache purge、H 本地 cache purge 或 provider 侧删除。

## 8. 发现与关闭要求

| ID | 严重度 | 发现 | 关闭证据 |
|---|---|---|---|
| CGH-FLD-01 | P1 | C 与 H evidence identity 元组不同；C 将 digest 放入 identity，H 将稳定 identity 与 digest 分开 | C/G/H 精确共享 identity 元组及 changed-digest 负向测试 |
| CGH-FLD-02 | P1 | H §11.8–11.9 是候选映射，尚不能证明所有 recovery/provider 字段已进入冻结的生成版 Applied ACK Schema/SDK | 精确 H Schema/IDL/SDK 版本、requiredness/canonicalization、生成工件和读回 |
| CGH-FLD-03 | P1 | G 持久化 Applied 幂等键尚未明确绑定到 H 精确 evidence identity 和 COC participant identity | G Owner 规范性映射及 crash/replay/conflict 测试 |
| CGH-FLD-04 | P2 | C Final Request 基础契约与 causal-order addendum 必须作为一个组合 evidence producer profile 登记 | Manifest 同时绑定两个精确 C Blob SHA 和 schema version |
| CGH-FLD-05 | P2 | COC/I/D/Storage 顺序域必须保持强类型区分；禁止 wall-clock 或 receiver-sequence fallback | 针对逆序、cutoff 缺失、recovery batch 不完整的跨 Owner 负向测试 |
| CGH-FLD-06 | P2 | 必须验证迟到 ACK + Forget/revocation 竞争下历史 Applied 与 current-use invalidation 的区分 | G 持久化/恢复测试及确定性竞争顺序 |

## 9. 最终结论

- 六阶段生命周期与权威分工：**语义 PASS**。
- C/G/H 对精确 CGH-APPLIED-1.1 recovery-batch 的语义决议：**已记录，均附带明确例外**，共同针对 A Blob `4961ffefc0f9920efb8425a9b2a7af42d8f64819` 和 COC Blob `fc3bac39ec64fda68b8cba5e1aada4e719e5acea`。
- C/G/H 字段级契约：**部分一致；P1 identity 元组和精确 Wire Schema 仍未关闭**。
- H Adapter Capability §11.8–11.9：**候选映射；Wire 未冻结**。
- G Applied persistence：**未验证**。
- C provider-specific same-key idempotency/recovery：**未验证**。
- COC 部署/operator 及 Storage/JF-10 生产实现：**未验证 / BLOCKED**。
- C/G/H 一致性测试：剩余跨 Owner race/recovery suite **SPECIFIED / NOT RUN**。
- Global Applied Contract Frozen：**NO**。生产激活/provider egress：**NOT AUTHORIZED**。

本审查不是 Owner 签署，不授权分支合并、架构冻结或生产激活。
