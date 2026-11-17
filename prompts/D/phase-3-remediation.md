# Owner D — Phase 3 Remediation Session Prompt

- Prompt ID: OWNER-D-P3-001
- Version: 1.0
- Status: HISTORICAL EXECUTION PROMPT — refresh all sources before reuse
- Source: `reviews/integration/phase-3-session-kickoff-prompts.md`
- Source blob SHA: 42ccfcccfc99049cbe3eba521b88b8a7610c137e

> Preserved owner-scoped prompt. Its source baselines may be stale. Refresh branch heads, contracts and SHAs before reuse; historical references are not current authority.

> 本文件保存 Phase 3 对应 Owner 的原始任务提示词。源版本中的分支和 SHA 可能已经过期；复用前必须刷新分支、契约和 SHA，不得把历史引用当作当前权威基线。

## Session D — Memory Brain Corrections and Canonical Authority

```text
你现在担任 AiMemoryBrainArchitecture 的 Memory Brain Principal Architect。你的任务是执行 Phase 3 task pack 中 D 的整改，只修改 D 所有的设计文件。D 是 Canonical Memory、MemoryVersion、Lifecycle、Entity/Relation 和 canonical ForgetOperation 的权威；D 不拥有 G 的 ContextVersion、H 的 wire/Adapter 或 I 的全局授权政策。

【必须先读取】
- reviews/integration/phase-3-cross-module-remediation-task-pack.md
- reviews/integration/phase-2-defg-cross-session-reconciliation.md
- reviews/03-memory-brain/review-scope-correction-and-design-reassessment.md
- D 分支 9dc08c63f6912320e290a963c634748ec44a81c8 的五份设计文件及 D 自审
- B 的 Fact/Claim ADR（如果尚未批准，保持 ADR-BLOCKED）
- E/F/G/H/I 对应候选契约（缺失时明确记录）

【必须关闭或明确阻塞】
1. D-REV-P1-001：统一 Forgetting 语义。明确 Memory Lifecycle 的持久状态与临时 ForgetOperation/fence/suppression 的区别。不要让同一概念同时成为 Memory 生命周期状态和操作状态。
2. D-REV-P1-002：明确 canonical commit sequence、per-aggregate revision、LifecycleEvent cursor 的边界；定义事务可见性、gap、replay/resume 及其与 Outbox/Index Watermark 的关系。
3. D-REV-P1-003：定义 durable ForgetOperation ID + monotonic fence/generation、dependency inventory、producer registration、barrier/watermark、late derivative suppression、target acknowledgement 和 completion proof。
4. Forget fence 必须能覆盖 Compiler queued/leased/retry/DLQ/replay、Runtime in-flight retrieval/cache/index rebuild、Context snapshots/deltas/delivery 和 Adapter offline reconnect。各模块执行细节归各模块所有，但 D 必须给出 canonical authority。
5. B 的 Fact/Claim ADR 未批准前，不得冻结 Claim/ClaimRevision/ConflictSet schema。
6. 定义 Entity Merge/Split 和 Relation 迁移，保持历史引用可审计。

【交付物】
仅在 session-d-memory-brain-2026-11-16 分支更新/创建：
- 03-memory-brain/ 下 D 已有五份文件
- 可新增 03-memory-brain/forget-fence-and-completion-contract.md
- 可新增 03-memory-brain/commit-cursor-semantics.md
- D decision/change log

【验收】
- D-REV-P1-001/002 语义闭合。
- D-REV-P1-003 有完整 race/barrier 语义，能防止晚到派生物复活。
- Canonical Commit、LifecycleEvent、Index Watermark、Forget Fence 均为不同 typed cursor。
- 不越权定义 H/I/G 的职责。
- 提交后重新读取验证，报告 branch/base SHA/commit SHA/changed paths/三项状态。

【禁止】
不得修改 main 或其他会话分支；不得把局部 D 设计宣称为全系统 Forget 完成；不得把 Forget suppression 当作物理删除证明。
```

---
