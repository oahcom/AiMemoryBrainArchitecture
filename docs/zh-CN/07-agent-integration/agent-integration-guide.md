---
document_metadata:
  domain: agent-integration
  role: guide
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
        - "07-agent-integration/agent-integration-overview.md"
        - "PR #430 comments 7061007191, 7061333647 and 7061563540"
        - "Issue #449 comment 7061011800"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "与当前 C 规范源配对的解释性指南；精确 Operation Registry 仍未冻结。"
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
    canonical_scope: "Agent Integration 解释性架构指南"
    canonical_scope_id: null
    canonical_scope_keywords:
      - agent-integration
      - MCP
      - BMCP
      - Agent Adapter
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "07-agent-integration/agent-integration-guide.md"
---

# Agent 集成——架构指南

- 文档 ID：DOC-AGENT-001 | 版本：1.1
- Owner：C — Agent Integration
- 规范源：[C 架构总览](../../../07-agent-integration/agent-integration-overview.md)
- 对应英文：[Agent Integration Architecture Guide](../../en/07-agent-integration/agent-integration-guide.md)
- 状态：解释性指南；家族级路由已 DECIDED；精确 C-H Operation Mapping 仍为 OPEN / DEPENDENCY_NOT_FROZEN

## 1. 目的

本文解释 Agent 接入边界，仅作说明。C 的规范源是 Agent Integration Architecture Overview。本文不定义 BMCP Wire 字段、Transport、ACK Encoding，也不授权 Runtime 实现。

## 2. 参与者与权威

- **Agent Host / Agent：** 拥有推理、规划、工具执行、Agent 原生状态和 Agent 安全策略。
- **C Agent Integration：** 拥有面向 Agent 的语义、MCP Dispatch Mapping、C 侧 Agent Request/Attempt/Turn/Session 身份、参数校验和响应映射。
- **H Protocol Gateway / BMCP：** 拥有 BMCP Wire/Envelope、Transport、Message/Correlation/Causation 身份、ACK、Validator 和 Capability Negotiation。
- **B/D/E/F/G/I：** 保留各自领域权威：B 负责词汇；D 负责 Canonical Identity/Lifecycle/ForgetFence；E 负责 Event Durable Acceptance；F 负责 Retrieval；G 负责 ContextVersion/ChangeSet/Applied；I 负责 Principal Authorization/PermissionEpoch/Global Forget。

## 3. MCP 与 BMCP 是不同接口

- MCP 是 Agent Host ↔ C 的北向 Tool/Resource 接口。
- BMCP（Brain Memory Context Protocol）是 C Agent Adapter ↔ Brain 的协议边界，经 H 接入。
- MCP Method 或 Tool Call 不是 BMCP Message。MCP Server 是接入 Adapter，不是 BMCP，也不是并行的 Canonical Brain API。
- MCP 成功、HTTP 2xx、Queue Acceptance 或 H Transport ACK 均不能被报告为 E Accepted 或 G Applied。
- Tool/Resource 名称及精确 Schema 仍为 OPEN，须等待后端 Owner Contract 和 H Operation Registry 固定并获得接受；本文不暗示任何占位操作。

## 4. C 对 BMCP 家族的路由决定

| 家族 | 相对 C 的方向 | C 的处理方式 |
|---|---|---|
| Telemetry | Agent/Adapter → Brain | 仅在 H 注册精确操作且 I/C 身份与授权绑定被接受后，才可暴露 C 自有的 Agent-facing Tool |
| Event Ingress | Producer/Agent → Brain | 必须使用 H 注册的 Ingress 和 E Durable Receipt/Idempotency；MCP Result 本身不是 E Receipt |
| Context Snapshot | Brain → Adapter | G 所有的 ContextVersion Snapshot 入站交付；不是通用 MCP Request/Response |
| Context Delta | Brain → Adapter | G 所有、具有精确 Base/Target 的 ChangeSet 入站交付；不是通用 MCP Request/Response |
| Delivery | Brain → Adapter | H/G Delivery Lifecycle；C 只在声明的 Inference Boundary 应用受管区域 |
| Acknowledgement | Adapter → Brain | 只能发送 H 定义的 Evidence；不是 MCP Success，也不是 G Applied |
| Capability Negotiation | 双向 | 归 H 所有；C 不得发明 MCP Tool 或本地替代协商 |
| Forget / Revocation | Brain/I → Adapter | C 消费并执行 D/I 控制；不得实现 C-local Forget |
| Administrative Governance | I/Control Plane → Adapter/Gateway | 仅 Control Plane；没有明确 I Policy/H Registration 时，不暴露为普通 Agent Tool |

Recall/Search 归 F 所有，不是 BMCP 家族。不得发明 BMCP Search Operation。未来若提供 MCP Search Tool，必须有固定的 F-owned Query API 和 I/D Authorization Path。

## 5. Agent 身份与 H 协议身份

C 保留 `AgentRequestId`、`AgentAttemptId`、`AgentTurnId` 和 `AgentSessionId`。H 拥有 `message_id`、`correlation_id` 和 `causation_id`。不得发明核心 `request_id`；`AgentAttemptId` 既不是 Transport Attempt，也不是 Idempotency Key。字段级交叉映射仍为 OPEN / DEPENDENCY_NOT_FROZEN。

Authenticated Principal 来自 I Trust Integration。Payload 中的 Principal、Producer、Agent、Actor 和 Scope 声明不能自我认证。H 的 Transport Sender/Audience Binding 不能替代 I Authorization。

## 6. 幂等与重试

状态变更重放使用由操作 Owner 管理、绑定 Canonical Payload Digest 的 Owner-scoped Idempotency Identity：

- 相同 Identity + 相同 Digest：返回原始结果/Receipt。
- 相同 Identity + 不同 Digest：Conflict。
- H Message Identity、Correlation、Causation 和 C AgentAttemptId 均不能替代 Operation Idempotency。
- H 已在逻辑层选择 RFC 8785 JCS 作为 JSON Canonicalization 基础；精确逐操作 Schema、Integrity/Signature Profile 仍为 OPEN。

## 7. 不可混淆的结果

MCP Tool Result、BMCP Business Response、H Transport ACK、E Accepted Receipt、G Applied Evidence、Forget ACK 和 I Global Forget Completion 各自独立。任何层都不得将其中一种升级为另一种。Delivered 不等于 Applied；Applied 也不证明模型注意或理解。

## 8. Active Recall 与 Context Delivery

Recall/Search 属于 F 的 Retrieval/Query Interface，并且需要 I Authorization 与 D Lifecycle/ForgetFence 检查。它不是 BMCP Message Family。Context Snapshot/Delta/Delivery 属于 Brain→Adapter 路径：G 拥有 ContextRef/ContextVersion/ChangeSet 和 Applied Acceptance；H 负责 Transport；C 仅校验并在 Inference Boundary 应用受管区域。

## 9. Capability Tier 与有限 Reference Model

Tier 1 要求可观察最终请求的 Inference Boundary Evidence。Tier 2 仅覆盖 Middleware-Controlled Path。Tier 3 支持 Telemetry/Recall，不得声称 Full Applied。Tier 不授予 Permission。

PR #452 已合并，在 `48a03f694684f7a62bc5b337dc758c98e3cc0e5b` 提供有限的 Rust Tier Enforcement Reference Model，检查 Tier-to-Operation Authorization 和 Protected-Region/Frozen-Request Rejection。它不是生产 Adapter、MCP Server、BMCP Negotiation/Transport、Telemetry Pipeline、Provider Integration，也不是实际 Inference Application 的证明。

PR #487 已于 `18b1c574433a6f3f600a9d2947b690084727aa75` 合并，增加确定性的内存 `ContextDeliveryAdapter`：精确后继 Snapshot Apply、Clear/Reset，以及断连/重连状态报告。crate 共报告 8 个 Unit Test。这不是真实 Transport、持久化 Delivery/Session State、自动 Retry、Snapshot/Delta Reconciliation、生产 Attestation 或 Runtime 集成。

## 10. 安全与故障处理

I 拥有 Authenticated Principal、Authorization 和当前 PermissionEpoch；D 拥有 Canonical Identity/Lifecycle 和 ForgetFence。受保护操作及重放结果披露前都必须重新校验。权限过期或状态未知时 Fail Closed。Memory 和 Telemetry 是不可信数据，不是指令；不要求私有 Chain-of-Thought。

明确发生在 Dispatch 前且无副作用的失败可以按策略重试。Dispatch 后 Timeout/响应丢失必须标记 UNKNOWN 并等待 Reconciliation；Cancellation 不等于 Rollback。必须保留 Authentication、Authorization、Validation、Integrity、Conflict、Unknown/Transient 和 Owner-Domain Error 的区别，并对错误详情脱敏。

## 11. Offline 与 Reconnect

Reconnect 时，必须先处理当前 I Authorization/PermissionEpoch 和 D ForgetFence/Revocation 控制，再重放缓存 Context。随后重新验证 Adapter/Session 身份、Capability 和 ContextVersion。只有 Base 精确匹配时才应用 Delta，否则请求 Full Snapshot。部分 Delivery/Application 绝不能报告为 Full Applied。

## 12. 当前决议状态

- MCP/BMCP 家族级路由：Issue #449 comment 7060351480 已 DECIDED。
- H Logical Identity/JCS/ACK/Validator 原则：PR #428 comments 7060190878、7060264372 在逻辑层 DECIDED。
- 精确 H Operation ID、字段名称/类型/必填性、逐家族 Schema、MCP Tool/Resource 名称：OPEN / DEPENDENCY_NOT_FROZEN。
- D/I 权威边界：语义层 DECIDED；没有 API/Schema 冻结。
- E/G Consumer Acceptance 和 C-H Operation Mapping：OPEN。
- Issue #7：`IMPLEMENTATION_BINDING=DEFERRED_TO_ENGINEERING_PHASE`；未授权 Runtime 实现。所有 Runtime 验收仍为 PLANNED_NOT_RUN / NOT AUTHORIZED。

## 13. 源文件版本锚点

本次读取的 current main：`5a1964fa77f6dff024c8cef9e4e6a43f3bd051af`。

- C 规范源 `07-agent-integration/agent-integration-overview.md`：本 FollowUp 前 Blob `073ff4ddf71fbcaf959107bb06ab724bfa48e63b`。
- C Capability Tiers：Blob `60bce314c36313a14dffe476a6f2a5cf7aa03b37`。
- C Capability Tiers 中文翻译（Non-Canonical）：`07-agent-integration/adapter-capability-tiers.zh-CN.md`，Blob `85a77163d1761a38074678983ad8d89ccf25d040`。
- C Inference Boundary：Blob `e2d5cb6abd9ec40da6e3680531de5944fc8b14df`。
- C Telemetry：Blob `9bb4a77e4bd79caaf3e1faeaf77c6b42858998f0`。
- PR #487 内存 Reference Model README/Source：Blob `ee68705248f80972232ebf28a4713554f377908e` / `125ebfb382a43c8e7ea79b547f86eaa7b611e202`；8 个测试，不证明生产 Transport 或 Runtime。
- H 当前 Protocol Index：Blob `a5b64941cdc783b385348de1b22e0eaace2c003d`；H Applied Evidence Addenda：`afa294bc42a8488e4569e6a8bdf5437c7a90e247`、`7b73491c765091728af6f5306b9efd502cf7f30a`。
- H RecoveryJoin 1.0.2 Schema：Blob `bbac8742401249230c629e858d033a09cd8f3acb`；仅证明工件存在，不代表 D Proof Adoption、生产 Conformance 或 C-H Operation Registry 冻结。
- G ContextVersion：Blob `1bfe7f1891e1f9da1ff7508f4e25a11bbf7f649b`；G Applied/Forget Reconciliation：`aa3afa73d8a76cc6f025839c52bfbff6a983046a`。
- E Event Store Contract：Blob `17b14591d76160a7c125903b41e7dae014c3c5df`。
- D/I 语义决议：Issue #429 comments `7060243632` / `7060259541`；H Logical Decision：PR #428 comments `7060190878` / `7060264372`。

四份 C 根目录文档仍是规范源基线。本 Guide Pair 仅作解释，不替代规范源。
