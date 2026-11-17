# Owner G — Phase 3 Remediation Session Prompt

- Prompt ID: OWNER-G-P3-001
- Version: 1.0
- Status: HISTORICAL EXECUTION PROMPT — refresh all sources before reuse
- Source: `reviews/integration/phase-3-session-kickoff-prompts.md`
- Source blob SHA: 42ccfcccfc99049cbe3eba521b88b8a7610c137e

> Preserved owner-scoped prompt. Its source baselines may be stale. Refresh branch heads, contracts and SHAs before reuse; historical references are not current authority.

> 本文件保存 Phase 3 对应 Owner 的原始任务提示词。源版本中的分支和 SHA 可能已经过期；复用前必须刷新分支、契约和 SHA，不得把历史引用当作当前权威基线。

## Session G — Context Reconciliation, Delivery and Applied Semantics

```text
你现在担任 AiMemoryBrainArchitecture 的 Memory Context Manager Principal Architect。G 拥有 Context membership/order/budget、ContextVersion、ContextChangeSet、reconciliation 和 Delivery intent。G 不拥有 Canonical Memory、Runtime retrieval 或 Adapter wire execution。

【必须先读取】
- reviews/integration/phase-3-cross-module-remediation-task-pack.md
- reviews/integration/phase-2-defg-cross-session-reconciliation.md
- G 分支 3d2c065be863bc1d349faaeece6f6eaa0047abae 的六份设计文件和 G 自审
- D 的 MemoryVersion/Forget fence
- F 的 RetrievalResult/ActivationRecommendation
- C 的 final inference boundary 和 H 的 Applied attestation 候选契约
- I 的 revocation/Forget governance（如缺失，标记 OPEN）

【核心任务】
1. 只引用 D 提供的 immutable Memory ID + MemoryVersion；不得修改 Canonical Memory。
2. 只消费 F RetrievalResult/ActivationRecommendation；F 不创建 ContextEntry/ContextVersion。
3. 定义 ContextChangeSet CAS、base/target version、幂等、重复/replay、partial failure 和 snapshot fallback。
4. Forget 时 tombstone/remove Context entries、invalidate snapshots/deltas、取消 Prepared/Delivered delivery（能力允许时），阻止 stale delivery 被标记 Applied。
5. Offline Adapter 状态必须保持 Pending/Unknown，直到收到可信 reconnect/reconciliation attestation。
6. 与 C/H 定义 Applied：Full Applied 要求受管理区域完整物化到实际提交给 inference runtime 的最终请求；Partial/Bypassed/Unknown 分别处理。
7. Applied 不证明模型关注或使用了记忆。预算/充分性也不能做此类推断。

【交付物】
仅在 session-g-memory-context 分支更新/创建：
- 06-memory-context/ 下 G 已有六份文件
- 06-memory-context/forget-reconciliation-and-offline-adapter.md
- 06-memory-context/applied-attestation-consumer-contract.md
- G decision/change log

【验收】
- ContextVersion 与 Delivery 是独立状态机。
- ChangeSet 原子、幂等、base-version safe。
- late delivery 不会复活已 Forget entry。
- Applied 绑定 exact ContextVersion、Delivery、session、capability epoch、inference request。
- 报告 branch/base SHA/commit SHA/changed paths/offline & stale-delivery tests。

【禁止】
不得把 Context Remove 当作 Canonical Forget；不得把 Adapter 内存缓冲写入当作 Full Applied；不得把 Applied 描述为模型使用证明。
```

---
