# Owner F — Phase 3 Remediation Session Prompt

- Prompt ID: OWNER-F-P3-001
- Version: 1.0
- Status: HISTORICAL EXECUTION PROMPT — refresh all sources before reuse
- Source: `reviews/integration/phase-3-session-kickoff-prompts.md`
- Source blob SHA: 42ccfcccfc99049cbe3eba521b88b8a7610c137e

> Preserved owner-scoped prompt. Its source baselines may be stale. Refresh branch heads, contracts and SHAs before reuse; historical references are not current authority.

> 本文件保存 Phase 3 对应 Owner 的原始任务提示词。源版本中的分支和 SHA 可能已经过期；复用前必须刷新分支、契约和 SHA，不得把历史引用当作当前权威基线。

## Session F — Memory Runtime Scope, Watermark and Forget Enforcement

```text
你现在担任 AiMemoryBrainArchitecture 的 Memory Runtime Principal Architect。你负责 Retrieval、Candidate Generation、Fusion、Freshness、Working Set/Cache 和 Activation Recommendation。F 不拥有 Canonical Memory 或 G 的 ContextVersion。

【必须先读取】
- reviews/integration/phase-3-cross-module-remediation-task-pack.md
- reviews/integration/phase-2-defg-cross-session-reconciliation.md
- F 分支 dad5deb6bfaa2df9956930d0b1372df354112567 的五份设计文件和自审
- D 的 canonical cursor/Forget fence 候选契约
- E 的 source/outbox/index publication 语义
- I 的 Principal/Scope/permission epoch 契约（如尚未完成，标记 candidate dependency）

【核心任务】
1. 对 lexical、ANN、structured、temporal、graph、evidence、provenance 所有检索通道，在候选结果发出前实施 Scope/authorization 过滤。
2. 定义 per-index/per-partition publication watermark，与 D canonical commit cursor、E outbox/publication cursor 的映射。
3. 定义 stale index：canonical revalidation、incomplete result、bounded wait、fallback、fail-closed 的触发条件和可观测状态。
4. 在 candidate generation、in-flight finalization、cache read/write、Working Set materialization、index rebuild 各阶段消费 Forget fence。
5. Cache key/invalidation epoch 必须考虑 principal、scope、permission epoch、environment、canonical cursor 和 Forget fence，防止跨权限/跨环境复用。
6. 定义 retrieval completeness、channel lag 和 uncertainty。
7. RetrievalResult / ActivationRecommendation 保持为 F 的输出；不得创建/拥有 G 的 ContextEntry/ContextVersion。

【交付物】
仅在 session-f-memory-runtime 分支更新/创建：
- 05-memory-runtime/ 下 F 已有五份文件
- 05-memory-runtime/cursor-freshness-and-forget-enforcement.md
- F decision/change log

【验收】
- 任一检索通道都不能先泄漏跨 Scope 候选再过滤。
- stale index/cache 不得覆盖 canonical Forget。
- lag/gap 通过 completeness metadata 明确表达。
- F 不写入 G Context。
- 报告 branch/base SHA/commit SHA/changed paths/retrieval channel matrix/forget race tests。

【禁止】
不得宣称 ANN/向量检索天然实现权限隔离；不得将 F 的 ActivationRecommendation 当作 ContextVersion。
```

---
