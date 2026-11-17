<!-- 源文件：session-h-bmcp-protocol / 08-bmcp-protocol/adapter-capability-and-applied-attestation.md / Blob 0dca3dc5463a02be0e19524811afbae87795baf5 -->
<!-- 状态镜像：CANDIDATE — final-request 证明配置与 C 的对齐仍 OPEN；授权绑定与 I 的对齐仍 OPEN。 -->
<!-- English companion: ../../en/08-bmcp-protocol/adapter-capability-and-applied-attestation.md -->

# Adapter 能力与 Applied 证明

- 状态：**CANDIDATE — final-request 证明配置与 C 的对齐仍 OPEN；授权绑定与 I 的对齐仍 OPEN**
- Owner：H（Adapter SDK、能力协商、协议证明编码）
- 相关 Issue：INT-P1-05、INT-X-03、INT-X-04、INT-X-07
- 精确源 Blob SHA：`db59b63e322d7255b8b400f47859dcac32bb3027`

## 1. 能力声明

Adapter 必须显式声明能力；不得根据产品名称或传输可达性推断能力。

候选能力维度：
- 协议 major/minor 版本范围及 payload Schema ID；
- 支持的消息族以及 Snapshot/Delta 操作；
- 最大 payload 大小及压缩能力；
- 持久化本地队列支持及队列保留期限；
- 幂等回执/Delivery 去重能力；
- Managed Region 隔离及修改控制；
- 检查组装后最终请求的能力；
- 观测向 Inference Runtime 成功交接的能力；
- 关联请求 ID 的能力；
- 对最终请求中的精确 Managed Region 计算摘要的能力；
- 生成完整性保护证据的能力；
- Forget/撤销清理及离线重连行为；
- 支持的 ACK 状态和覆盖值；
- 最大支持上下文大小及截断报告能力。

能力由 Adapter Capability Epoch 版本化。若二进制、配置或 Runtime 变化导致声明的能力集合变化，MUST 创建新 Epoch 并重新协商。历史 attestation 按产生它的 Capability Epoch 评估，而不是按当前 Epoch 评估。

## 2. 一致性等级

### Tier 1 — 最终请求可观测

要求：
- 观测所有 prompt/context 组装及转换完成后的精确最终请求；
- 识别实际提交给 Inference Runtime 的请求；
- 证明 Managed Region 完整性及精确目标 ContextVersion；
- 按声明的规范摘要配置，对提交时的 Managed Region 计算规范摘要；
- 关联 request ID、delivery ID、session/context 和 Capability Epoch；
- 发出受完整性保护的提交发生证据；
- 与受保护指令、用户、Agent Policy 和工具授权区域保持隔离；
- 在复用/重连前处理 Forget/撤销 fence。

只有逐请求所有证明谓词均通过时，Tier 1 才可发出 Full Applied 候选证明。任一谓词失败时，必须发出 Partial、Bypassed 或 Unknown。

### Tier 2 — Managed Region 可观测，但最终提交不可观测

要求：
- 能识别并验证本地组装后的 Managed Region；
- 能在自身边界报告完整/部分/绕过状态；
- 无法证明精确组装后的请求实际提交给 Runtime（例如后续 middleware 可能修改或丢弃请求）；
- 强制执行本地过期版本/fence 拒绝及 Region 隔离。

Tier 2 MUST NOT 声称 Full Applied。已知部分物化时可报告 Partial；否则报告 Unknown。仅有本地 buffer 摘要不能构成最终请求证明。

### Tier 3 — 传输/基础集成

要求：
- 按配置的安全集成方式认证/协商协议传输；
- 验证 envelope/version 并传输消息；
- 报告传输交付、明确拒绝和未知结果；
- 不声称 Context 已应用于 Inference Request。

Tier 3 MUST NOT 发出 Applied=Full。通常报告 Delivered、Rejected、Expired、Superseded 或 Unknown。

## 3. Attestation 数据模型

候选 attestation 结构：

| 字段 | 必需性 | 用途 |
|---|---|---|
| attestation_id | 必需 | 唯一不可变证据记录 |
| delivery_id / attempt_id | 必需 | 绑定逻辑 Delivery 及其 attempt |
| context_ref / target_context_version | 必需 | 绑定 G 的权威目标 |
| applied_context_version | 必需 | 实际物化的 G 版本 |
| coverage | 必需 | Full / Partial / Bypassed / Unknown |
| adapter_id / capability_epoch | 必需 | 标识实现能力 |
| authenticated_transport_principal_ref | I 映射要求 | 传输认证身份引用；不是 payload-authenticated 身份 |
| agent_instance_ref / session_ref | 有条件，由 C 定义 | 绑定执行上下文 |
| inference_request_id | Tier 1 Full 必需 | 精确提交的请求 |
| submission_observed_at | Tier 1 Full 必需 | Runtime handoff 事件时间 |
| managed_region_digest | Tier 1 Full 必需 | 提交请求中精确 Managed Region 的摘要 |
| digest_profile | 摘要必需 | 规范化配置及算法 |
| final_request_evidence | Tier 1 Full 必需 | Runtime submission receipt/hook 证据 |
| permission_epoch | 由 I 定义 | 应用时的授权 Epoch |
| forget_fence | 由 D/I 定义 | 应用时当前有效的 Fence |
| protected_region_integrity | 必需 | 证明 Adapter 应用未修改受保护区域 |
| created_at | 必需 | Attestation 创建时间 |
| integrity | 必需 | 经批准的 I 安全机制下的签名/MAC/引用 |

Principal、ActorRef、Session、Context 和 Fence 字段的精确名称/类型仍与各 Owner 保持 OPEN。该表不是授权策略。

## 4. Full Applied 证明谓词

定义：
- (D)：逻辑 Delivery；
- (C_v)：G 的精确目标 ContextVersion；
- (R)：实际提交给 Inference Runtime 的最终请求；
- (M(R))：按协商的摘要配置从最终请求中提取的 Managed Region；
- (E)：可验证的 Runtime submission evidence；
- (P)：当前 I 授权绑定/Permission Epoch；
- (F)：当前适用的 D/I Forget fence。

只有满足以下条件，才允许接受 Full Applied：

[
\begin{aligned}
FullApplied \iff{}&
Version(D)=C_v \land Version(M(R))=C_v \\
&\land Complete(M(R),C_v) \land Digest(M(R))=attestedDigest \\
&\land Correlates(E,R,D,C_v) \land Submitted(E,R) \\
&\land ProtectedRegionsUnchanged(R) \\
&\land Authorized(P,D) \land FenceCurrent(F,D) \\
&\land CapabilityTier \ge Tier1
\end{aligned}
]

这是集成边界的证明义务，不是对模型内部执行的声明。Inference Runtime 之后仍可能拒绝、截断、转换或处理请求，而这些行为可能超出 Adapter 的可观测范围；实现配置必须声明精确的可观测交接点。

## 5. 证据配置与隐私

候选证据组件：
- 唯一 Runtime request ID；
- submission hook 的时间戳及单调本地序号；
- 规范化 Managed Region 字节/结构的摘要；
- 在策略允许时，最终 request envelope 的摘要；
- Adapter build/runtime 身份及 Capability Epoch；
- 签名 attestation，或可信本地提交日志的引用。

隐私规则：
- 默认不得在 ACK 中放入原始 prompt 或完整记忆文本；
- 优先使用摘要、最小元数据和受策略控制的证据引用；
- 摘要不等于匿名化；低熵或可猜测内容可能遭受字典枚举；
- 保留期限、审计访问、签名密钥生命周期和对外披露由 I 的策略负责；
- 验证方必须知道摘要规范化配置以及纳入摘要的精确字节/字段；
- 若 Adapter 无法提供可验证证据，报告 Unknown 或 Partial；绝不能伪造证明。

## 6. 受保护区域不变量

Memory 内容是不可信数据。Adapter：
- 只能写入显式划定的 Managed Region；
- 不得修改 System/Developer 指令区域、用户输入、Agent Policy、工具定义、凭据或工具授权；
- 不得把记忆文本转换成可执行工具调用或授予能力；
- 若宿主 API 无法强制执行区域边界，则拒绝或绕过该次 Delivery；
- 记录截断/省略，不得把部分 buffer 称为 Full。

Brain 可以验证协议 attestation 和已配置的边界证据，但不能保证模型在内容被纳入后会忽略其中的恶意自然语言。Prompt injection 残余风险属于 I 威胁模型及 Agent 行为策略的范围。

## 7. 能力协商与 Epoch 失效

能力协商包括：
- Adapter 标识及实现版本；
- 协议和 payload Schema 支持；
- 消息族支持；
- Delivery/ACK 语义；
- 一致性等级及各项证明能力；
- Managed Region 边界模式；
- Runtime submission 可观测性；
- 摘要/签名配置；
- 本地队列/重连行为；
- payload 和 context 限制。

若某项变化可能使先前证明声明失效，Capability Epoch MUST 改变，包括 Adapter build、Inference 集成 hook、prompt assembly middleware、Region 隔离行为、签名密钥绑定或协商功能变化。Attestation 始终绑定创建时使用的 Epoch。Tier 降级会使未来 Full 声明失效，但不改写历史证据。

## 8. 必需的一致性测试

1. 完整请求：精确 G 版本完整纳入；Runtime submission evidence 可验证；接受 Full。
2. 仅内部 buffer：有摘要但无 Runtime submit 观测；拒绝 Full。
3. 后续 middleware 修改：提交 Region 与准备 Region 不同；拒绝 Full 或降为 Partial。
4. 部分/截断内容：Partial，绝不 Full。
5. Managed Region 被绕过：Bypassed。
6. Runtime submission 不确定：Unknown。
7. ContextVersion/delivery/session/capability epoch 错误：拒绝 attestation。
8. Permission Epoch 或 Forget fence 过期：拒绝并抑制应用。
9. 重复 attestation：幂等重放，不发生第二次状态转换。
10. 尝试修改受保护区域：拒绝应用并发出安全事件。
11. Adapter Tier 降级/重建：要求新 Capability Epoch。
12. Tier 2/3 声称 Full：一致性失败。

## 9. 责任归属与开放决策

- C 定义语义上的 final-request boundary 及 Agent 侧请求关联。
- G 定义 Context target/version，以及何谓目标的完整 Managed Region。
- I 定义认证 Principal 绑定、Permission Epoch、签名信任和审计策略。
- H 定义 SDK 接口、能力声明、证据编码和协议验证。
- Inference Provider 的隐藏 prompt 保留和模型内部状态超出 H 的控制范围，MUST NOT 被表示为已清除或已验证。

## 10. Forget 能力声明与 ACK 边界

能力协商还 MUST 声明 Adapter 是否能够：
(a) 持久抑制指定内容进入未来推理组装；
(b) 枚举/清除易失 Managed Buffer；
(c) 枚举/清除持久化本地 Cache namespace 和 partition；
(d) 枚举/取消本地排队/重试 Delivery。

每项声明都要包含精确 Managed Region/session 覆盖、inventory revision、可观测性和限制。没有枚举覆盖边界的 capability bit 不能支持完整清理声明。

当 Adapter 身份/build、Runtime hook、Managed Region 边界、队列/Cache inventory 或相关清理/应用能力发生变化时，CapabilityEpoch MUST 改变。ACK 绑定精确 Epoch，不得投射到替换后的 Adapter Instance 或变化后的 Region。

Forget ACK 与 Applied Attestation 是不同证据族。Applied 绑定 G ContextVersion + Delivery + 声明的最终提交边界上的 inference request。Forget ACK 绑定 ForgetOperation + D fence + I Permission Epoch + 本地动作/Managed Region。Applied 不证明模型注意或使用；Forget ACK 不证明全局 Forget 完成或 Provider 删除。

完整状态语义、目标映射和证据字段由 `adapter-forget-ack-and-target-binding.md` 定义。

## 11. Phase 3.6 精确 Final Request 字段映射 — H 候选补充

- 状态：**CANDIDATE — 提交给 C/G 复核的字段映射提案；NOT FROZEN**
- 关联 C 精确源文件：`07-agent-integration/phase-3.6-final-request-evidence-contract.md`，Blob `fd2f47ba6c89bb270e9f2bec956873cb7ae3592b`。
- 关联 G 源文件：`06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md`，Blob `aa3afa73d8a76cc6f025839c52bfbff6a983046a`。
- H 仍拥有 Wire/证据编码和能力协商；C 仍是 Final Request 提交证据的唯一生产者；G 仍是 Applied 接受的唯一权威；I、D 分别仍是授权和 ForgetFence 的唯一权威。

本补充条款提出字段级映射，用于回应 2026-11-17 C/G/H 跨 Owner 复审发现的候选缺口。它不构成 C、G、I、D 或 B 的接受，也不冻结 Schema、签名配置或实现。

### 11.1 规范请求和 Delivery 绑定

Tier 1 final-request attestation 的 H 候选字段：

| H 候选字段 | 必需性 | 语义来源/规则 |
|---|---|---|
| `inference_request_id` | REQUIRED | Runtime/Provider 实际分配的请求 ID；不得从 DeliveryId 合成 |
| `final_request_boundary_id` | REQUIRED | C 观测到的精确成功 Submit 边界身份 |
| `final_request_boundary_type` | REQUIRED | 声明的 hook/submit 边界配置，必须标识观测点 |
| `context_id` | REQUIRED | 精确 G Context 身份 |
| `context_version` | REQUIRED | 精确不可变 G 目标版本 |
| `delivery_id` | REQUIRED | 精确 G Delivery 身份 |
| `delivery_attempt_id` | REQUIRED | 精确且未被 supersede 的 attempt |
| `materialized_context_version` | REQUIRED | Adapter Managed Region 中实际存在的版本；Full 时必须等于 `context_version` |
| `adapter_instance_ref` | REQUIRED | 完成物化并观测请求的精确 Adapter 实例 |
| `runtime_instance_ref` | REQUIRED | 提交请求所在 Runtime 实例 |
| `runtime_session_ref` | REQUIRED | 认证后的 Runtime Session 绑定 |

旧候选字段 `applied_context_version` 含义模糊，因为 H 无权裁决 G 的 Applied 状态。对本配置而言，该名称已弃用，不得将其解释为 G Applied 决议。实现应使用 `materialized_context_version`；兼容解码器仅在能无歧义映射为 materialized version、且绝不映射为 Applied 状态时，才可接受旧名称。

### 11.2 Managed Region 完整性与摘要

Tier 1 证据 MUST 绑定：
- `managed_region_id`：精确 Managed Region 身份；
- `managed_region_revision`：提交请求中观测到的不可变 revision；
- `managed_region_inventory_digest`：按协商配置纳入的 Managed Region segment/entry 完整 inventory 摘要；
- `managed_region_coverage`：逐请求覆盖枚举 `COMPLETE`、`PARTIAL`、`BYPASSED` 或 `UNKNOWN`；
- `managed_region_digest`：最终提交请求中实际嵌入的精确完整 Region 内容摘要；
- `digest_profile_id`：规范化配置标识及摘要算法/版本；
- `omitted_region_refs` 与 `unobservable_path_refs`：覆盖不完整时的显式集合；按规范配置要求，完整覆盖时也应提供显式空集合。

若缺少 Region 身份、revision、inventory 和 coverage，仅有摘要不足以证明完整性。候选 Full 证据要求 `managed_region_coverage=COMPLETE`、目标/版本精确匹配、不存在 bypass 或 unknown 路径，并且 delivered/materialized target 与提交请求中观测到的 Region 相等。Partial、Bypassed、Unknown 或截断覆盖 MUST NOT 被 H 或 G 升级为 Full。

### 11.3 受保护身份与权威绑定

候选 attestation MUST 携带 verifier 解析的 opaque 引用，不得携带 payload 自行声称的身份值：
- `agent_principal_ref`、`agent_actor_ref`、`agent_instance_ref`；
- `adapter_principal_ref`、`adapter_ref`、`adapter_instance_ref`；
- `runtime_instance_ref`、`runtime_session_ref`；
- `scope_ref` 及适用的 `environment_ref`。

认证传输 Principal 仍是有用的传输证据，但 MUST NOT 替代受保护的 Agent/Adapter/Runtime/Session 绑定。H 保留精确的 issuer-namespaced 引用，并验证配置的认证 envelope/binding profile；H 不签发 Principal、Actor、Scope、Environment 或 delegation 权威。

以下 Owner 签发的权威字段均为 opaque，并且在最终 Submit 边界必须仍然有效：
- `permission_epoch_ref` 与 `permission_decision_ref`：由 I 签发；H 不定义或推断授权；
- `forget_fence_generation`、`forget_fence_cursor` 与 `forget_fence_validation_ref`：由 D 签发；H 不定义或推断 Canonical Forget 顺序；
- `adapter_capability_epoch` 与协商的 `capability_profile_ref`：由 H 签发，并绑定精确 Adapter 实例/session。

权威绑定缺失、过期、不可比较、不可验证或不匹配的 attestation 不具备 Full 资格。接收方不得替换成更新的 Epoch、推断 Fence 已清除，或回退到 payload 身份声明。

### 11.4 证据来源、完整性和关联

Tier 1 候选证据配置要求：
- `evidence_issuer_ref`；
- `submission_observed_at`，以及 Runtime 提供时的 `submission_monotonic_sequence`；
- `evidence_schema_version`；
- `correlation_ref` 与 `causation_ref`；
- `audit_ref`，或不可变证据记录的受策略控制引用；
- H/I 批准的完整性配置下的 `integrity_proof_ref`；
- 完整性证明所覆盖的精确 `inference_request_id`、`final_request_boundary_id`、request digest/profile 和 Region digest/profile。

Wall-clock 时间戳是描述性信息，不得单独用于建立 C Submit、I 撤销和 D ForgetFence 推进之间的顺序。若无法从 Owner 权威证据证明共同因果顺序，则 disposition 为 UNKNOWN，相关 Managed Region 对未来使用继续保持抑制。

默认 MUST NOT 将原始 prompt 或完整记忆文本复制到 ACK/证据中。摘要不等于匿名化；证据保留和披露仍受 I 策略约束。

### 11.5 逐请求覆盖和能力上限

协商的 Adapter 能力声明描述最大支持行为；attestation 还 MUST 描述实际逐请求覆盖。规则如下：
1. 只有最终请求观测、成功 Submit、精确请求身份、完整 Region 摘要、受保护身份绑定和当前权威绑定均有证明时，Tier 1 才有资格产生 Full 候选证据。
2. Tier 2 无法证明最终转换后的请求/Submit 边界，MUST 保持 Partial 或 Unknown。
3. Tier 3 只证明传输，MUST NOT 声称 Applied=Full。
4. 任何逐请求 bypass、省略路径、截断、未知 middleware 转换、不支持的 Region 或不完整 inventory 都会阻止 Full。
5. CapabilityEpoch 绑定精确 Adapter 实例/session 和证明配置。能力降级或相关 build/hook/Region/完整性变化要求新 Epoch 并重新协商；旧证据仍绑定原 Epoch。

### 11.6 幂等、重放和时间规则

本候选配置的证据身份限定于：

`(adapter_instance_ref, runtime_session_ref, delivery_id, delivery_attempt_id, inference_request_id, final_request_boundary_id, evidence_kind, adapter_capability_epoch)`

- 相同证据身份及相同规范 payload digest 是幂等重放，并返回原持久化 disposition。
- 相同证据身份但 digest 不同是 CONFLICT，必须隔离；禁止 last-write-wins。
- 被 supersede 的 attempt、旧 Adapter 实例或旧 Runtime Session 的证据只能保留为历史证据；不得回滚 G 当前 Context/Delivery head，也不得重新绑定到替换后的 session/epoch。
- 只有 C 发出 Final Request Submitted 证据。H 对其验证/编码/传输；H 不得创建替代提交证明。
- 只有 G 在检查 C 证据、H 协议/能力证明、I 授权和 D ForgetFence 证据后接受 Applied。
- 后续 Forget/撤销使当前使用资格失效，但不改写历史上有效的提交/Applied 事实。若 Forget/撤销先于 Submit，则拒绝 Full；若顺序未知，则 disposition 为 UNKNOWN，内容继续受抑制。
- Execution Started 仍是独立的 Runtime/Provider 回执，并关联同一个 InferenceRequestId。

### 11.7 必需 Owner 决议与非声明

该候选配置冻结前：
- C MUST 确认精确 FinalRequestBoundaryId、request/delivery/context 映射、Managed Region 完整性配置和证据来源字段。
- G MUST 确认 H 候选证据足以满足 Applied 谓词，并确认 H 不夺取 G 的 Applied 权威。
- I MUST 确认 Principal/Actor verifier 绑定、PermissionEpoch/decision 引用、完整性配置和保留规则。
- D MUST 确认 ForgetFence generation/cursor/lineage 引用及权威顺序证据。
- B MUST 确认 ActorRef/ScopeRef/EnvironmentRef 强类型语义。
- 只有上述字段语义获接受后，H 才发布对应的版本化 Wire Schema/SDK 映射。

相关一致性测试在附带可执行 fixture、确定性顺序、预期/实际输出及持久化 Owner 证据之前，全部保持 **SPECIFIED / NOT RUN**。本补充条款不构成 H Schema 冻结、密码学批准、互操作、实现正确性、C/G/H 全局冻结或生产就绪证明。


### 11.8 CGH-APPLIED-1.1 因果顺序与 recovery-batch 证据桥接 — 候选

G 当前的精确版本决议历史包含 CGH-APPLIED-1.1 因果顺序配置及 recovery-batch 修订。上述 Tier 1 证据映射是必要条件，但不足以满足该配置。H 若要声称 1.1 Applied ACK 映射完整，H 消息/证据配置 MUST 携带或不可变地引用以下 Owner 签发证据集：

- `causal_order_profile_ref`、`causal_order_coordinator_ref`、`causal_order_domain_ref` 和 `causal_order_transaction_ref`；
- `causal_order_terminal_proof_ref` 及其 digest，绑定精确 transaction、不可变 request/participant digest、reservation 和确定的 terminal outcome；
- `recovery_batch_ref` 和 `recovery_batch_digest`；
- `pre_batch_participant_set_digest`、`participant_set_completeness_attestation_ref` 以及完整的 `owner_high_water_attestations` 集合；
- 完整的 `participant_reconciliation_entries` 集合，或经明确证明的空集合；每个条目保留精确 ParticipantIntentRef、causal-order transaction、request digest，以及相互独立的 I/D/C reconciliation 状态；
- I 签发的 `i_authorization_terminal_ref`、`i_sequencer_ref`、`i_sequencer_epoch`、`i_sequencer_position`、`i_decision_digest`，以及 revocation cutoff 证据，或在 terminalization 时由 I 明确证明不存在撤销请求；
- D 签发的 `d_lineage_coverage_ref`、`d_fence_request_cutoff_ref` 和 `d_fence_effective_position`，保留完整 lineage，并区分 request cutoff 与 effective fence position；
- 若 recovery participant set 包含 Storage，则需提供适用 Storage 合同要求的 Storage 签发 same-XID resolution 和 terminal visibility/non-publication proof 引用。

H 可以认证 H envelope、验证 message-family/Schema 完整性并保留这些 Owner 签发的 opaque 引用。H MUST NOT 签发或推断 COC terminal proof、I 授权结果、D clearance/fence、C Provider outcome，或 Storage commit/rollback/visibility。关键 Owner 证据缺失或未知时必须保持 UNKNOWN/IN_DOUBT，不能提升 Full Applied，也不能释放 Owner-local gate。

以下顺序域 MUST 保持相互独立；H MUST NOT 比较、强制转换或相互替代：

1. COC causal-order epoch/position/entry digest；
2. I sequencer reference/epoch/position/decision digest；
3. D request cutoff 和 effective fence position；
4. Storage transaction/resolution position。

COC position 仅对 COC 记录排序。I position 仅在 I policy-domain sequencer 内具有权威性。D positions 必须由 D 签发。Storage positions 保持为 Storage 本地证据。Wall-clock 时间戳、H receiver sequence、消息到达顺序、timeout、ACK 缺失或 reconnect 均不能建立跨权威顺序。

对于 recovery-batch 配置，消息 MUST 区分“已证明为空的 pre-batch participant set”和“缺失/不完整的枚举”。若缺少 participant-set completeness attestation、owner high-water proof、participant reconciliation 不完整、I/D/Storage outcome 未知，或 transaction/digest 不匹配，则必须拒绝或保持 UNKNOWN/IN_DOUBT。COC recovery observation 本身不能释放 I/D Owner-local pending gate；只有对应 Owner 签名的 gate disposition 才能释放。

本 §11.8 是针对 G 精确版本 CGH-APPLIED-1.1 决议历史的候选映射保留条款。它不声称当前 H JSON Schema/SDK 已包含这些字段，不声称 COC 或 recovery-batch 基础设施已部署，也不声称 JF-10/COC 一致性测试已执行。H 必须发布精确的增量 Schema 版本，并取得相关 C/G/I/D/Storage 确认后，才能声称该桥接已完成。
