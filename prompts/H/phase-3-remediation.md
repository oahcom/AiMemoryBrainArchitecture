# Owner H — Phase 3 Remediation Session Prompt

- Prompt ID: OWNER-H-P3-001
- Version: 1.0
- Status: HISTORICAL EXECUTION PROMPT — refresh all sources before reuse
- Source: `reviews/integration/phase-3-session-kickoff-prompts.md`
- Source blob SHA: 42ccfcccfc99049cbe3eba521b88b8a7610c137e

> Preserved owner-scoped prompt. Its source baselines may be stale. Refresh branch heads, contracts and SHAs before reuse; historical references are not current authority.

> 本文件保存 Phase 3 对应 Owner 的原始任务提示词。源版本中的分支和 SHA 可能已经过期；复用前必须刷新分支、契约和 SHA，不得把历史引用当作当前权威基线。

## Mandatory global preflight

Before using this preserved task prompt, read `prompts/README.md`, `prompts/global-project-developer.md`, `prompts/global-bilingual-documentation.md`, `prompts/H/owner-charter.md`, and GOV-DOC-001. Review sessions must also read `prompts/global-architecture-reviewer.md`. Refresh all current source refs and SHAs; historical prompt baselines below are not authoritative.

## Session H — BMCP Protocol and Agent Context Adapter

```text
你现在担任 AiMemoryBrainArchitecture 的 BMCP Protocol & Agent Context Adapter Principal Architect。H 是新建工作流；当前仓库此前没有 H 的正式设计包。BMCP 暂定为 Brain Memory Context Protocol。H 拥有 wire envelope、协议版本、序列化、传输交互、Adapter SDK 和 application acknowledgement；H 不拥有 Brain 记忆语义、G Context membership 或 I 全局安全政策。

【必须先读取】
- reviews/integration/phase-3-cross-module-remediation-task-pack.md
- reviews/integration/phase-2-defg-cross-session-reconciliation.md
- 00-governance/ 全部治理基线
- 07-agent-integration/ C 现有文档
- D/E/F/G 的确切分支和基线 commit，重点读取其接口输出
- I 正在设计的 Principal/ActorRef/permission epoch/Forget governance 契约（如未存在，先标记依赖，不要自创最终安全政策）

【核心任务】
1. 设计 BMCP message families：Telemetry、Event Ingress、Context Snapshot/Delta、Delivery、Acknowledgement、Capability Negotiation、Forget/Revocation notification、Administrative governance envelope。
2. 定义协议版本协商、required/optional fields、unknown enum handling、canonical serialization、integrity metadata、correlation/causation IDs、错误分类。
3. 消费 I 提供的 authenticated transport principal binding；payload 自称的 ActorRef 不构成认证。
4. 定义 Adapter capabilities 与 Tier 1/2/3 conformance。
5. 定义 Prepared、Delivered、Applied、Rejected、Expired、Superseded、Unknown 状态，及重试/幂等语义。
6. 定义 Full/Partial/Bypassed/Unknown application attestation。Full Applied 必须绑定实际提交给 inference runtime 的 final request，不能只证明 Adapter 内部 buffer 更新。
7. 定义 Forget/revocation notification、managed-region clearing、offline reconnect、stale snapshot rejection 和 ACK。不得声称可控制模型服务商保留的隐藏 prompt 或模型内部状态。
8. 记忆 payload 始终作为数据，不得修改受保护指令区域或 Agent 工具授权。

【交付物】
在独立新建的 H 分支工作，先核实分支是否已存在；如不存在，从当前约定 baseline 创建新分支。仅创建：
- 08-bmcp-protocol/protocol-overview.md
- 08-bmcp-protocol/message-envelope-and-versioning.md
- 08-bmcp-protocol/context-delivery-and-acknowledgement.md
- 08-bmcp-protocol/adapter-capability-and-applied-attestation.md
- 08-bmcp-protocol/forget-revocation-and-reconnect.md
- 08-bmcp-protocol/protocol-conformance-matrix.md

【验收】
- 与 C telemetry、D canonical refs、E receipt、F retrieval、G Context delivery 一致。
- Full Applied 有 final-request 可验证证据；无法观察 final request 的 Adapter 不得声称 Tier 1 Full Applied。
- duplicate/stale/superseded/expired/offline/late ACK 行为确定。
- H 不代替 I 决定 authorization policy，不代替 G 管理 Context。
- 提交后验证文件，报告 branch/base SHA/commit SHA/changed paths/interface matrix/open dependencies。

【禁止】
不得冻结仍依赖 I/C/G 的字段；不得把 Delivered 当作 Applied；不得把 Applied 当作模型注意/使用证明；不得承诺物理删除。
```

---
