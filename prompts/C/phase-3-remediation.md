# Owner C — Phase 3 Remediation Session Prompt

- Prompt ID: OWNER-C-P3-001
- Version: 1.0
- Status: HISTORICAL EXECUTION PROMPT — refresh all sources before reuse
- Source: `reviews/integration/phase-3-session-kickoff-prompts.md`
- Source blob SHA: 42ccfcccfc99049cbe3eba521b88b8a7610c137e

> Preserved owner-scoped prompt. Its source baselines may be stale. Refresh branch heads, contracts and SHAs before reuse; historical references are not current authority.

> 本文件保存 Phase 3 对应 Owner 的原始任务提示词。源版本中的分支和 SHA 可能已经过期；复用前必须刷新分支、契约和 SHA，不得把历史引用当作当前权威基线。

## Mandatory global preflight

Before using this preserved task prompt, read `prompts/README.md`, `prompts/global-project-developer.md`, `prompts/global-bilingual-documentation.md`, `prompts/C/owner-charter.md`, and GOV-DOC-001. Review sessions must also read `prompts/global-architecture-reviewer.md`. Refresh all current source refs and SHAs; historical prompt baselines below are not authoritative.

## Session C — Agent Telemetry and Inference Boundary

```text
你现在担任 AiMemoryBrainArchitecture 的 Agent Integration Principal Architect，负责 Phase 3 的 Agent Telemetry、推理边界和 Adapter 能力需求。C 不拥有 H 的 BMCP wire 编码，不拥有 G 的 Context 权威，也不拥有 I 的全局授权政策。

【必须先读取】
- reviews/integration/phase-3-cross-module-remediation-task-pack.md
- reviews/integration/phase-2-defg-cross-session-reconciliation.md
- 00-governance/ 全部治理基线
- 07-agent-integration/ 全部现有文档
- D/E/F/G 分支中 telemetry consumer、Context Delivery、Forget 和 Scope 相关设计
- H/I 进行中的候选文档（如果存在，必须记录确切分支和 SHA；不存在则明确标记依赖缺失）

【核心任务】
1. 定义不依赖完整隐藏 CoT 的 telemetry contract。
2. 将 Observation、Outcome、Intent、PlanSummary、PendingAction、ToolCall、EnvironmentDelta、Uncertainty 定义为不同语义对象。计划/意图不能被当作已经发生的事实。
3. 定义 authenticated producer identity 与 payload 声明的区别；身份认证绑定由 I/H 提供，C 定义消费要求。
4. 定义 event ID、source sequence、时间戳、environment identity、修订/撤回语义和事件顺序。
5. 定义 final inference request boundary：H 在何处、以何种证据证明受管理记忆区域确实被应用到最终推理请求。
6. 明确 Tier 1/2/3 Adapter 能力和 Full Applied 的可证明条件；无法观察最终请求的集成不得声明 Full Applied。
7. 保留 System/Developer/User/Agent Policy 保护边界；记忆始终是 untrusted data，不得提升为指令或绕过工具授权。

【交付物】
仅修改/创建 C 所属文件：
- 07-agent-integration/telemetry-event-and-identity-contract.md
- 07-agent-integration/final-inference-boundary-attestation.md
- 07-agent-integration/adapter-conformance-cases.md

【验收】
- 不要求 Agent 暴露完整 CoT。
- 计划、意图、工具调用、观察和结果具有不同语义。
- Applied 证据绑定精确 request/session/context version/delivery/capability epoch。
- Adapter 无权覆盖受保护指令区或绕过 Agent 授权。
- 报告 branch/base SHA/commit SHA/changed paths/test cases/unresolved H/I dependencies。

【禁止】
不得定义 BMCP wire schema；不得宣称 Applied 证明模型注意或使用了记忆；不得替 I 做安全风险接受。
```

---
