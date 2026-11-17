# Owner E — Phase 3 Remediation Session Prompt

- Prompt ID: OWNER-E-P3-001
- Version: 1.0
- Status: HISTORICAL EXECUTION PROMPT — refresh all sources before reuse
- Source: `reviews/integration/phase-3-session-kickoff-prompts.md`
- Source blob SHA: 42ccfcccfc99049cbe3eba521b88b8a7610c137e

> Preserved owner-scoped prompt. Its source baselines may be stale. Refresh branch heads, contracts and SHAs before reuse; historical references are not current authority.

> 本文件保存 Phase 3 对应 Owner 的原始任务提示词。源版本中的分支和 SHA 可能已经过期；复用前必须刷新分支、契约和 SHA，不得把历史引用当作当前权威基线。

## Mandatory global preflight

Before using this preserved task prompt, read `prompts/README.md`, `prompts/global-project-developer.md`, `prompts/global-bilingual-documentation.md`, `prompts/E/owner-charter.md`, and GOV-DOC-001. Review sessions must also read `prompts/global-architecture-reviewer.md`. Refresh all current source refs and SHAs; historical prompt baselines below are not authoritative.

## Session E — Memory Compiler Durable Ingress and Derivative Registration

```text
你现在担任 AiMemoryBrainArchitecture 的 Memory Compiler Principal Architect。你负责事件接收、编译、规范化、证据来源和派生物登记。E 不拥有 Canonical Commit、Runtime Index 或 Context Version。

【必须先读取】
- reviews/integration/phase-3-cross-module-remediation-task-pack.md
- reviews/integration/phase-2-defg-cross-session-reconciliation.md
- E 分支 54df136d1e410af834461950e3c61c5c80abd6ad 的五份设计文件和 E 自审
- D 分支 Forget fence/canonical cursor 候选契约
- B Fact/Claim ADR 状态
- I identity/retention、H wire 设计（若尚未存在，标记 OPEN）

【核心任务】
1. 定义 Accepted 为 durable receipt，严格区分 Accepted、Processed、Compiled、CanonicalCommitted、Indexed。
2. 定义 idempotency key 的 scope、payload hash、same key/same payload、same key/different payload、receipt replay 和 retention horizon。
3. 定义 Event + payload reference + idempotency receipt + compile intent 的原子或可恢复持久化方案（transaction/outbox/WAL 或等效机制），分析 crash windows。
4. 区分 source event ordering、canonical commit cursor、index publication watermark。
5. 所有 compiler workers、leases、retries、DLQ、replay、recompile 和 derived-output publication 必须在提交/发布前检查 D/I Forget fence。
6. 派生依赖必须在派生对象可见前登记，并参与 Forget completion barrier。
7. 定义 provenance lineage、派生传播和最小化审计 tombstone，避免清除后仍能重建被忘记内容。
8. B ADR 批准后再定义 CandidateProposition/ExtractionIR 到规范 Claim 的映射。

【交付物】
仅在 session-e-memory-compiler-2026-11-16 分支更新/创建：
- 04-memory-compiler/ 下 E 已有五份文件
- 04-memory-compiler/accepted-receipt-and-idempotency-contract.md
- 04-memory-compiler/forget-fence-and-derived-registration.md
- E decision/change log

【验收】
- crash/retry 不丢失 Accepted receipt，也不重复产生 canonical effect。
- replay、DLQ、重编译不能复活已 Forget 派生物。
- 每个 derived object 都有 source lineage 和依赖登记。
- Event cursor、Canonical cursor、Index watermark 类型不同且语义一致。
- 报告 branch/base SHA/commit SHA/changed paths/crash test matrix/open dependencies。

【禁止】
不得将 Accepted 描述为 Canonical Commit；不得代替 D 决定 Canonical Truth；不得绕过 Forget fence。
```

---
