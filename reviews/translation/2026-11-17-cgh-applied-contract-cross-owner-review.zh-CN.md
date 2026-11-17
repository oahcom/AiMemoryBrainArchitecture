# C/G/H Phase 3.6 Applied 合同跨 Owner 复审

- 复审日期：2026-11-17
- 复审范围：C Final Request Evidence、G Applied/Forget/Reconciliation、H Adapter Capability/Applied Attestation
- 复审方式：基于 Owner 源文件的独立语义与字段级交叉复核
- 非目标：本报告不构成 Owner 批准、Wire 冻结、实现验证、一致性测试执行或生产验收。

## 1. 精确源文件基线

| Owner | 源路径 | 分支 | 精确源 Blob SHA | 源状态 |
|---|---|---|---|---|
| C | `07-agent-integration/phase-3.6-final-request-evidence-contract.md` | `session-c-agent-integration-2026-11-16` | `fd2f47ba6c89bb270e9f2bec956873cb7ae3592b` | C 语义决策已记录；C/G/H 冻结阻塞；实现/执行未验证 |
| G | `06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md` | `session-g-memory-context` | `aa3afa73d8a76cc6f025839c52bfbff6a983046a` | G 语义决策已记录；C/G/H 冻结阻塞；实现/执行未验证 |
| H | `08-bmcp-protocol/adapter-capability-and-applied-attestation.md` | `session-h-bmcp-protocol` | `ed6b43a29aa368d772c701ffc83309a5aadf3c00` | CANDIDATE；final-request 证明配置与 C 的对齐仍 OPEN；授权绑定与 I 的对齐仍 OPEN |

Blob SHA 只标识精确文件内容，不代表分支 HEAD、批准或实现证据。

## 2. 跨 Owner 语义一致性

### 2.1 六阶段生命周期 — 一致

三个合同均保留严格区分的生命周期：

`Prepared → Delivered → Materialized → Final Request Submitted → Applied → Execution Started`

- C 仅在精确的、完成全部转换后的请求跨过可观测且成功的 Runtime/Provider Submit 边界后，产生不可变的逐请求 Final Request Submitted 证据。
- H 的能力等级决定 Adapter 能观测什么。Tier 2/3、绕过路径或未知覆盖不得声称 Full。
- 只有 G 可以验证完整谓词并提交权威的逐请求 Applied 记录。
- Execution Started 必须由 Runtime/Provider 单独提供，并关联同一个 InferenceRequestId。

没有任何合同允许合并传输接收、物化、提交、Applied 和执行开始。Applied 不证明模型注意、理解、回忆、行为使用、正确性或执行成功。

### 2.2 历史事实与当前使用资格 — 一致

C 与 G 均规定：历史上有效的提交/Applied 事实是追加式证据。后续 Forget、撤销、Scope/Session/Capability 变化会使当前使用资格失效，但不改写历史事实。若 Forget/撤销先于提交线性化，则拒绝 Full Applied；若顺序无法证明，则为 Unknown，并持续抑制相关内容。

H 的 CapabilityEpoch 规则与此兼容：历史 attestation 绑定产生它的 epoch；降级不会改写历史，但会阻止未来 Full 声明。

### 2.3 重复与迟到证据 — 语义一致，H Wire 映射仍开放

C 与 G 要求相同身份和摘要的精确重放必须幂等；相同身份但摘要不同必须冲突/隔离。迟到 ACK/证据不能回滚更新的 ContextVersion/Delivery attempt，也不能跨 Adapter 实例、Runtime Session 或 CapabilityEpoch 重新绑定。H 要求 attestation 不可变并绑定能力 epoch，但当前候选字段模型尚未定义完整公共身份元组及重放日志 Wire 映射。

### 2.4 Forget 边界 — 权责一致，H 字段映射不完整

G 拥有 Applied 与当前使用资格失效状态；D 拥有 ForgetFence；I 拥有授权/PermissionEpoch；H 拥有协议/ACK/Capability；C 拥有 Final Request 证据。Forget ACK 与 Applied Attestation 是不同证据族。Context Remove 不是 Canonical Forget。G 的 reconnect 流程要求在恢复任何旧 Snapshot/Delta 前，重新认证并重新验证 I/D/G/H 权威状态。

## 3. H 候选字段相对 C/G 的缺口

H 源文件明确为 CANDIDATE，并注明 final-request proof profile 与 C 的对齐仍 OPEN。以下是字段映射缺口，不允许在翻译中自行发明 Wire 字段：

| 发现 | H 候选现状 | C/G 所需绑定 | 必须处理的状态 |
|---|---|---|---|
| H36-AP-01 — 边界身份 | H 有 `inference_request_id` 和泛化的 `final_request_evidence`；候选表没有明确的 `FinalRequestBoundaryId` 或边界类型 | C 要求 Runtime 实际分配的 InferenceRequestId 及精确 FinalRequestBoundaryId/边界类型；G 同时要求请求和边界身份 | H 必须发布或接受精确映射；OPEN |
| H36-AP-02 — 目标身份 | H 使用 `context_ref / target_context_version`、`delivery_id / attempt_id`、`applied_context_version` | C/G 要求 ContextId、精确 ContextVersion、DeliveryId、DeliveryAttemptId，且 attempt 未被 supersede | 定义规范字段映射，并区分目标版本与实际物化版本；OPEN |
| H36-AP-03 — Managed Region 完整性 | H 要求 `managed_region_digest` 和 `digest_profile` | C/G 要求精确 Region 身份、inventory/revision、完整覆盖，以及最终提交请求中实际嵌入 Region 的摘要 | 增加或规范引用 inventory/revision/coverage 证据；只有摘要不充分；OPEN |
| H36-AP-04 — 权威向量 | H 表中 `permission_epoch` 由 I 定义，`forget_fence` 由 D/I 定义 | C/G 要求最终提交时当前的 PermissionEpoch + 授权决策，以及 D ForgetFenceGeneration/Cursor + lineage 验证 | 保留 Owner 签发的强类型引用，并定义 H 的精确传输绑定；H 不得签发权威；OPEN |
| H36-AP-05 — 认证身份 | H 列出 `authenticated_transport_principal_ref`，并明确它不是 payload-authenticated；Agent/session 引用为条件字段、由 C 定义 | C/G 要求由 verifier 解析的 Agent/Adapter/Runtime/Session 身份和受保护绑定，不接受 payload 声明 | 明确受保护 verifier context，以及 issuer/instance/session 精确绑定；OPEN |
| H36-AP-06 — 证据来源信息 | H 有 `created_at`、`integrity` 和候选 submission evidence | C 还要求 evidence issuer、可用时的边界时间戳/单调序号、schema version、correlation/causation 与 audit reference | H/C 必须定义哪些来源字段必需、哪些有条件，并确定完整性配置；OPEN |
| H36-AP-07 — Tier 语义 | H Tier 1/2/3 大体匹配 C 的能力上限 | C 还将逐请求 bypass/unknown 路径以及精确省略/不可观测覆盖视为非 Full | 确保逐请求 coverage 与 bypass 枚举属于被接受的证据，而不只是 Adapter 能力声明；OPEN |

这些是 C/H/G 精确字段级绑定的实质性阻塞项。不得通过中英文翻译把 H 候选文件悄悄升级为已批准合同。

## 4. Owner 权威边界 — 保持不变

- C：Final Request 提交证据的唯一生产者；不修改 Applied。
- G：Context Applied 状态及当前使用资格投影的唯一权威。
- H：协议 Schema、ACK/Capability 协商、证据编码与验证；不裁决 Applied，也不签发 I/D 权威。
- I：Principal/Actor 授权、PermissionEpoch、撤销及安全/完整性策略。
- D：ForgetOperation、ForgetFence、lineage 覆盖及顺序。
- B：Actor/Scope/Environment 强类型引用。
- Runtime/Provider：真实请求身份、成功 Submit 边界及独立 Execution Started 回执。

不得从某个 Owner 的决议推断其他 Owner 已接受。

## 5. 发现与结论

- **PASS — 生命周期语义：** 六阶段分离及非声明边界一致。
- **PASS — 历史/当前使用语义：** 后续失效保留历史并阻止复用。
- **PASS — 重复/迟到证据语义：** C/G 语义规则一致；H Wire 重放身份仍 OPEN。
- **BLOCKED — H/C 精确 Wire 映射：** H36-AP-01..07 需要 H/C 明确解决并对精确版本作出批准。
- **BLOCKED — 权威集成：** I/D/B 权威确认仍是独立前置条件。
- **NOT RUN — 一致性测试：** 本次复审未取得 C-FR-01..12、G-36-01..15 或 H Adapter 测试的可执行运行证据。
- **NOT VERIFIED — 实现：** 本报告不接受任何 Runtime/Adapter/Provider 实现或生产证据作为已验证。

## 6. 必须执行的后续动作

1. H Owner 发布修订版 Adapter Capability/Applied Attestation 候选合同（或精确版本映射补充），逐项解决 H36-AP-01..07，并对齐 C 的 Final Request 证据和 G 的 Applied 谓词。
2. C 确认修订后的 final-boundary/evidence 映射；G 确认 Applied 消费映射。双方决议必须固定到同一个精确 package/source Blob，不能只引用文件名或分支。
3. I 与 D 分别确认其权威字段及顺序/当前性语义；B 确认强类型引用。
4. 只有源合同对齐后，才基于精确 Owner Blob SHA 生成完整 EN/zh-CN 对照文件并进行语义一致性复审。
5. 在各自证据门禁通过前，保持 C/G/H freeze 为 BLOCKED，所有实现/一致性状态维持 NOT VERIFIED / NOT RUN。

**结论：** 六阶段架构语义一致，但 H 当前 Adapter Capability/Applied Attestation 候选文件尚不是覆盖 C 最终请求证明和 G Applied 接受的完整字段级合同。翻译不得掩盖这一缺口。
