# Phase 3.6 — 最终请求证据契约

- **Owner：** Session C — Agent Integration、Telemetry 与 Final Request Boundary
- **源状态：** **C 语义决策已记录；C/G/H 跨 Owner 冻结 BLOCKED；实现和执行 NOT VERIFIED**
- **源分支：** `session-c-agent-integration-2026-11-16`
- **精确源 Blob SHA：** `fd2f47ba6c89bb270e9f2bec956873cb7ae3592b`
- **权威边界：** C 负责生成 Agent 侧最终请求提交证据；H 负责 Wire/ACK/capability 协议；G 负责 Context Applied 状态；I 负责授权；D 负责 Forget fence。
- **对应文件状态：** 双语阅读对应文件；不改变源决策状态。
- **English companion:** [English](../../en/07-agent-integration/phase-3.6-final-request-evidence-contract.md)

## 1. 证据阶段词汇

以下阶段彼此不同，MUST NOT 合并：

| 阶段 | 含义 | 权威证据 | 不证明 |
|---|---|---|---|
| Context Prepared | G 创建不可变授权目标版本及 delivery intent | ContextVersion、ChangeSet、DeliveryId/attempt intent | 已发送、已接收、已物化或已应用 |
| Context Delivered | H transport endpoint 接受精确 delivery attempt | 已认证 H delivery receipt | Managed Region 已安装 |
| Context Materialized | Adapter 将精确内容放入其声明的 Brain-managed region | Adapter 本地 materialization evidence、region identity 和 digest | 最终请求包含该内容或已提交 |
| Final Request Submitted | 精确不可变、完成转换后的 inference request 跨过可观测 submit boundary | C 生成、受完整性保护且绑定实际 request/boundary 的提交证据 | 模型关注、理解或执行开始 |
| Applied | G 根据 Applied predicate 接受完整 C/H 证据 | G 权威 Applied record | 模型关注、理解、记忆使用或行为正确 |
| Execution Started | Runtime/provider 报告该 request 已开始执行 | 与 InferenceRequestId 关联的 runtime/provider execution-start receipt | 执行完成、响应正确性或记忆使用 |

Delivered ACK 不等于 Materialized。Materialized 不等于 Final Request Submitted。提交只有在 G 校验后才是 Applied。Applied 不等于 Execution Started。

## 2. C Final Request Submission Evidence

只有当 C 集成能够观察所有转换后的实际最终不可变请求，以及该请求成功交接给 inference runtime/provider 时，C 才为每个请求生成不可变证据记录。

必需字段：

- `InferenceRequestId`：由 runtime/provider boundary 实际分配的请求标识，不是本地自行创建的 correlation token。
- `FinalRequestBoundaryId` 和 boundary type：精确 hook/submit boundary 及 evidence profile。
- `ContextId`、`ContextVersion`、`DeliveryId`、`DeliveryAttemptId`：精确 G target 和 attempt。
- 已认证的 `AgentPrincipal/AgentRef`、Agent instance、`AdapterPrincipal/AdapterRef`、Adapter instance、Runtime instance 和 Runtime Session；全部从受保护的已认证绑定解析，不得来自 payload claims。
- 精确 `ScopeRef`、必要时的 `EnvironmentRef`，以及 Managed Region identifier/inventory。
- 规范化的 Managed Region 内容 digest 及 digest algorithm/version；digest 覆盖实际嵌入最终请求的完整 region 内容。
- `PermissionEpoch` 和 authorization decision reference，并针对本请求 boundary 校验。
- `ForgetFenceGeneration/Cursor`，以及针对 region 所表示全部 source lineage 的 D validation reference。
- `AdapterCapabilityEpoch`、协商后的 capability profile 和 conformance profile version。
- Submission outcome、可用时的 boundary timestamp/monotonic sequence、evidence issuer、integrity/signature/key reference、schema version、correlation/causation 和 audit reference。
- Coverage declaration：complete、partial、bypassed 或 unknown；精确列出遗漏/不可观测的 request path 和 region coverage。

C MUST NOT 从 DeliveryId 合成 InferenceRequestId，不得根据本地 render 声称 submit 成功，也不得从 submission 推断 execution start。

## 3. 证据完整性、不可变性与失效

1. 证据签发后 append-only 且不可变。更正必须创建链接到原记录的新 superseding record；不得原地改写。
2. 证据完整性必须依据已认证 Adapter/runtime issuer 和双方约定的 H wire integrity profile 验证。Payload 身份字符串本身不是凭据。
3. Digest canonicalization、签名密钥、replay protection、schema ID 和 Wire encoding 仍需 H/C 最终一致；在此之前它们只是候选集成细节。
4. 若任一身份绑定、request ID、region digest、delivery attempt、ContextVersion、Scope/Environment、PermissionEpoch、ForgetFence 或 CapabilityEpoch 缺失、陈旧、不可验证或不匹配，该记录不具备 Full Applied 资格。
5. Permission revocation、fence advancement、scope/environment 变化、capability epoch 变化、session 替换、delivery supersession、过期或更新的 Context head，都会使当前使用资格失效；但不会抹除历史上有效的 submission fact。
6. 历史 Applied record 在 Forget/revocation 后仍是审计事实；必须标记为后续使用不再 current，且未经新授权和 reconciliation 绝不能作为后续 request 的种子。
7. 证据保留不得仅为保存证明而保留已忘记的明文。只保留 I policy 允许的最少不可重构 digest、类型化引用和审计元数据。

## 4. Capability 上限

| 集成层级 | 可观测证据 | 允许声明 |
|---|---|---|
| Tier 1 — Full inference boundary | 精确最终不可变 request、实际 submit、request ID、完整 Managed Region digest 和当前 authority bindings | 可生成候选 Full Applied evidence，交由 G 校验 |
| Tier 2 — Middleware | 受控 middleware materialization/insertion；无法完整观察最终转换或实际 submit | 仅 Partial/Unknown；MUST NOT 声称 Full Applied |
| Tier 3 — Events/Recall | 仅 Event 和 Recall receipts；没有主动 final-request boundary | 不得声称 Applied |
| Unsupported/Limited | 无法证明 boundary、identity、digest 或 authority checks | 明确报告 Unsupported/Limited；不得 Full Applied |

Tier 是已证明的证据上限，不是产品标签或自我声明。每个 request 都必须枚举 bypass path。本地渲染的 prompt、middleware callback 或 transport ACK 均不足以达到 Tier 1。

## 5. G Applied Acceptance Predicate（C producer 侧）

C 提供证据；只有 G 可以接受 Applied。候选 Full Applied 必须同时满足：

1. 精确 ContextVersion 与 G 的不可变 target 匹配。
2. DeliveryId 和 DeliveryAttempt 匹配 active、未 supersede 的 G attempt。
3. InferenceRequestId 是实际 ID，在其 runtime domain 内唯一，并绑定可观测 final boundary。
4. Agent、Adapter、runtime 和 session 身份已认证、已注册、当前有效且相互绑定。
5. Managed Region identity 和精确完整内容 digest 与 delivered target 匹配。
6. ScopeRef 及必需的 EnvironmentRef 与授权 Context 精确匹配。
7. PermissionEpoch 和 authorization decision 在 submission boundary 仍然 current。
8. ForgetFenceGeneration 在 submission boundary 对全部 source lineage 仍然 current。
9. CapabilityEpoch 当前有效，并支持完整 final-boundary observation。
10. Final Request Submitted evidence 完整、integrity-valid、不可重放、不可变，且因果顺序晚于 delivery/materialization。
11. 在 submission boundary 前没有 supersession、revocation、fence、scope、session 或 capability invalidation 先行线性化。
12. 用于认证 delivery/Adapter identity 和 evidence transport 的 H protocol evidence 有效。

字段缺失或存在歧义时，必须 fail closed 为 Partial/Unknown/Rejected。G MUST NOT 从多个较弱 receipt 的组合推断 Full Applied。

## 6. 排序、迟到证据与幂等

- ACK/evidence identity 由 Adapter instance + Runtime Session + DeliveryId + attempt + evidence kind + digest 共同限定。
- 完全相同的重复证据必须幂等，并返回原始 disposition。
- 相同 identity 但 digest 不同属于 conflict；必须 quarantine 并发出 security/consistency event。
- 已 supersede attempt 的迟到证据只能建立历史事实，不能将 G 当前 Applied pointer 向后移动。
- 来自旧 Runtime Session 或 Adapter instance 的证据不得重新绑定到新 session/capability epoch。
- 迟到 ACK 不得回滚更新的 ContextVersion 或 delivery。
- 若 submission 先于后续 Forget/revocation，保留历史事实并标记 current-use invalid；若 fence/revocation 先于 submission 线性化，则拒绝 Full Applied。
- 若无法证明先后顺序，状态为 Unknown，受保护内容继续 suppressed。

## 7. Prompt injection 与记忆信任边界

所有 Memory、Evidence、summary、compacted text、retrieval snippet、observation 和 tool output 都是不可信数据。它们 MUST 在结构上与 system/developer instructions、user input、tool definitions、tool authorization 和 Agent policy 分离。Context 内容可以描述动作，但不能授权或执行动作。

Provenance、source identity、Scope、trust/epistemic status、lifecycle 和 transformation lineage 必须在 summary/compaction 后保留。Summary 是派生的不可信工件，不是信任升级。跨 Scope 材料必须在 candidate admission 前以及 final request submission 前再次拒绝。Tool-call declaration 是意图/声明；只有独立认证的 tool result/side-effect receipt 才能证明执行。

## 8. C 一致性矩阵

除非未来执行附带 executable fixture、environment、expected/actual output 和可复现工件，否则以下全部为 **SPECIFIED / NOT RUN**。

| ID | Fixture 与操作顺序 | 预期 | 禁止行为 | 证据 |
|---|---|---|---|---|
| C-FR-01 | Tier 1；prepare、deliver、materialize、提交精确 request | 为 G 生成候选 Full evidence | G 接受前标记 Applied | Request ID、region digest、boundary proof |
| C-FR-02 | Materialize region；无 submit event | 仅 Materialized | Final Request Submitted / Applied | Materialization receipt；缺少 submit proof |
| C-FR-03 | Middleware 看不到最终转换/submit | Partial/Unknown | Full Applied | Tier profile、bypass coverage |
| C-FR-04 | Final request digest 与 delivered region 不同 | 拒绝 Full Applied | 忽略 digest mismatch | 两个 digest 和 canonicalization profile |
| C-FR-05 | Final assembly 期间、submit 前 Permission 被撤销 | Block/omit region；不产生 Full Applied | 将陈旧 ALLOW 提升为有效 | Epoch/decision 和 boundary ordering |
| C-FR-06 | Final submit 前 fence 前进 | Suppress region；不产生 Full Applied | 提交 fence 前的 materialization | Fence proof 和 submit attempt |
| C-FR-07 | 有效 submit 后发生 revocation | 保留历史证据；current-use invalid | 删除历史或复用旧 permission | Submission ordering 和新 epoch |
| C-FR-08 | 重复证据且 digest 相同 | 幂等返回原结果 | 重复提升状态 | Evidence ID/digest |
| C-FR-09 | 相同 evidence identity、digest 被修改 | Conflict/quarantine | Last-write-wins | 两个 digest、security event |
| C-FR-10 | Reconnect 后旧 session ACK 到达 | 仅历史记录或拒绝 | 重新绑定新 session | Old/new session 和 capability epoch |
| C-FR-11 | Summary 含恶意指令 | 作为不可信数据处理 | 指令权限升级 | Provenance/trust labels 和 region boundary |
| C-FR-12 | Tool call declaration 没有 tool receipt | 仅是意图 | 声称 tool 已执行/产生副作用 | Call declaration 和缺失的 result receipt |

## 9. 未决发现与决策记录

- **C-36-01（BLOCKED）：** H wire schema、signature/integrity、ACK 和 capability epoch 的精确映射需要 H 批准。
- **C-36-02（BLOCKED）：** G Applied 状态转换及 historical/current-use projection 需要 G 验收。
- **C-36-03（BLOCKED）：** I PermissionEpoch decision freshness/revocation 语义及 B typed Scope/Actor 绑定需要 Owner 批准。
- **C-36-04（BLOCKED）：** D ForgetFence currentness 和 E/Storage durable publication/lineage evidence 仍是上游依赖。
- **C-36-05（NOT RUN）：** 本设计阶段没有提供可执行 Agent/Adapter final-boundary 测试证据。

**C 决策：** 阶段分离；C 是 final-request evidence producer；候选 Full evidence 必须对应精确最终不可变 request 和实际 submit；Tier 2/3 不得声称 Full Applied；Memory 始终是不可信数据；历史 Applied 保留，但失效后不得复用。

**跨模块状态：** C/G/H Applied contract 尚未 Frozen。本文仅规定 C 的 producer contract，不改变 H Wire 或 G 状态权威。

## Phase 3.6 CFG 联合架构闭环补充 — C Owner 决策

- **决策包：** A 所有的 `reviews/integration/phase-3.6-cgh-applied-contract-decision-package.md`
- **审查的精确 package Blob SHA：** `61d961c32138fd875069e8cbac4696bb031447c0`
- **C 决策：** 对 C 所有的 final-request 语义及共享六阶段生命周期 **APPROVE WITH ENUMERATED EXCEPTIONS**。这不是全局冻结，也不是 H 批准。

### C 接受的条款

1. 生命周期严格为 `Prepared → Delivered → Materialized → Final Request Submitted → Applied → Execution Started`；每阶段是由不同权威负责的独立事实。
2. 只有在精确转换后的 request 跨过声明的、成功的 runtime/provider submit boundary 后，C 才单独生成不可变、逐 request 的 Final Request Submitted evidence。本地 buffer、middleware render、transport ACK 或 Delivery receipt 均不足。
3. C 将证据绑定到 runtime 实际分配的 `InferenceRequestId`、`FinalRequestBoundaryId`、G `ContextId/ContextVersion`、`DeliveryId/DeliveryAttempt`、已认证 Agent/Adapter/Runtime/Session、精确 Scope/Environment、ManagedRegion identity/revision、完整 region digest/profile、I `PermissionEpoch`、D `ForgetFenceGeneration`、H `CapabilityEpoch` 及 integrity/correlation evidence。
4. 只有在精确 final-request 和 submit 可观测性、region 完整性、身份绑定和 integrity 均得到证明时，Tier 1 才可发出候选 Full evidence。Tier 2/3 以及任何 bypass/unknown coverage 都不能声称 Full。
5. C evidence 是 append-only。完全相同 identity+digest 的重复是幂等；相同 identity 但 digest 改变则 conflict/quarantine。迟到证据不能回滚更新的 Context，也不能跨 Adapter/Session/CapabilityEpoch 重新绑定。
6. C 不修改 G Applied state。Applied 不证明模型关注、理解、回忆、行为使用或正确性。Execution Started 需要独立 runtime/provider receipt。
7. 如果无法证明 D/I transition 相对于 submit 的排序，C 报告 Unknown，且 managed region 在未来使用中继续 suppressed。

### 枚举例外与外部权威保留项

- **H Wire 例外：** 此批准不冻结 H message schema、field encoding、ACK taxonomy、signature/MAC、key rotation、canonicalization、replay journal、receiver ordering、capability negotiation 或 reconnect Wire 行为。H 必须批准同一 package Blob SHA，或发布列明例外的替代版本及新的 common package version。
- **I authorization 例外：** C 消费但不定义 PermissionEpoch domain/issuer/freshness、Principal/delegation trust 或 revocation policy。仍需 I 批准和权威 current-decision evidence。
- **D Forget 例外：** C 消费但不定义 ForgetOperation/Fence generation、lineage coverage 或 canonical linearization proof。仍需 D 确认。
- **B typed-reference 例外：** C 不定义 ActorRef/ScopeRef/EnvironmentRef 类型或 Scope hierarchy。仍需 B 批准。
- **Execution evidence 例外：** 此语义决定不批准任何实现、live Adapter/provider boundary、测试执行或生产证据。

### C 决策后果

C 认为 A package 中属于 C 的语义部分已在上述例外范围内接受。C/G/H Applied Contract 仍为 **NOT FROZEN**，直到 H 明确接受同一版本（并且 I/D/B 提供各自权威确认）。C conformance 和 PI suites 仍为 **SPECIFIED / NOT RUN**；实现仍为 **NOT VERIFIED**。

## Phase 3.6.3 — Issue #3 C 精确版本 Owner 决策

- **Owner：** C — Final Request Boundary 和不可变 submission evidence。
- **精确共享 package：** `reviews/integration/phase-3.6-cgh-applied-contract-decision-package.md`，Blob SHA `122b164bcc0760b83bf555072a36fc55631623e1`。
- **决策：** 对 C 所有的 final-request evidence 和 lifecycle 条款 **APPROVE WITH ENUMERATED EXCEPTIONS**。这是 C 对 Issue #3 的明确决定，不是全局冻结。
- **共同契约版本：** **CGH-APPLIED-1.0**，锚定上述精确 package Blob。
- C 要求实际转换后的 request 跨过成功的 provider/runtime submit boundary；runtime 分配的 InferenceRequestId 和 FinalRequestBoundaryId；精确 ContextId/ContextVersion 与 DeliveryId/attempt；已认证 Agent/Adapter/RuntimeSession 和 verifier-resolved ActorRef；精确 role-tagged ScopeBindingSet 与适用 EnvironmentRef；完整 ManagedRegion identity/revision/inventory/digest/profile；当前 I PermissionDecision/PermissionEpoch；D ForgetFenceGeneration/lineage；H CapabilityEpoch 和 authenticated ACK binding。本地 render、materialization、transport ACK 或 caller claim 都不是 submission evidence。
- **时间规则：** 已证明的 submit 先于后续 fence/revocation 时，可保留为历史证据，但 current-use 失效；fence/revocation 先于 submit 时不能 Full；顺序不确定时为 Unknown 并 suppressed。C 从不修改 G Applied state。
- **例外：** H 负责 Wire serialization 和 cryptographic profile；I 负责 policy/PermissionEpoch 和 governance；D 负责 fence/lineage；B 负责 typed references；此决策不提供 runtime/test evidence。
- **负向案例：** no submit、partial/bypassed boundary、digest mismatch/truncation、stale epoch/fence、伪造 ActorRef/Scope/Environment、迟到的旧 session ACK、相同 identity 下 digest 改变、顺序歧义，都必须拒绝 Full 或保持 Unknown/suppressed。
- C-FR-01..12 仍为 **SPECIFIED / NOT RUN**。

## Phase 3.6.3 — Issue #6 C BIH 消费者验收

- **精确 BIH package：** `reviews/integration/phase-3.6-identity-trust-joint-architecture.md`，Blob SHA `a45ae90b318a79bf009d14f4d917611881e9e214`。
- **处置：** 作为 BIH36-JD-01..17 的下游消费者，**ACCEPT WITH ENUMERATED EXCEPTIONS**。
- **映射：** PrincipalRef/IssuerRef 和 workload/Adapter identity 只能来自受保护 verifier context；ActorRef 是 verifier 逐操作生成的归因；payload identity values 仍只是 claims。C 将显式 ScopeRef roles 和适用 EnvironmentRef 绑定到 final-request evidence。PermissionDecision/PermissionEpoch 是 opaque 且限定 policy domain；C 在 final submit 重新校验 currentness，不签发 epoch，也不推断 grants。
- **执行约束：** final submission 前，C 校验已认证 Principal/Actor/workload/session、精确 operation/resource/purpose/audience、Scope/Environment applicability、delegation result、当前 I decision/epoch、D fence 和 H capability/session evidence。输入缺失、不匹配、陈旧、有 gap、已撤销或不确定时，阻止 submission 并禁止 Full evidence。
- **Fail closed：** 伪造/无法解析的身份、未知 issuer、格式错误 Ref、缺少必需 Scope/Environment、无效 delegation、未授权跨 Scope/Environment、陈旧/不可比较 epoch、未知 requiredness profile、不支持的 capability、陈旧 fence 或顺序不确定，均导向 DENY/PAUSE/UNKNOWN；不回退信任 payload，也不产生 Full Applied。
- **例外：** C 不负责 issuer admission、Principal registry、delegation policy、PermissionEpoch issuance、跨域 grants、cryptographic suite、BMCP serialization、ForgetFence issuance 或 G Applied state。I36-GOV approvals 和 I36/H36 runtime tests 是独立门禁。
- C-FR-05..10 和 BIH negative cases 仍为 **SPECIFIED / NOT RUN**。
