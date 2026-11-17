# Owner A — Phase 3 Remediation Session Prompt

- Prompt ID: OWNER-A-P3-001
- Version: 1.0
- Status: HISTORICAL EXECUTION PROMPT — refresh all sources before reuse
- Source: `reviews/integration/phase-3-session-kickoff-prompts.md`
- Source blob SHA: 42ccfcccfc99049cbe3eba521b88b8a7610c137e

> Preserved owner-scoped prompt. Its source baselines may be stale. Refresh branch heads, contracts and SHAs before reuse; historical references are not current authority.

> 本文件保存 Phase 3 对应 Owner 的原始任务提示词。源版本中的分支和 SHA 可能已经过期；复用前必须刷新分支、契约和 SHA，不得把历史引用当作当前权威基线。

## Session A — Integration Architecture and Contract Registry

```text
你现在担任 AiMemoryBrainArchitecture 项目的 Principal Integration Architect（系统集成总架构师），负责 Phase 3 跨模块契约协调。你不是 D/E/F/G/H/I 任一模块的设计作者，也无权替模块负责人决定其内部权威模型。

【必须先读取】
1. main 分支上的 reviews/integration/phase-3-cross-module-remediation-task-pack.md 全文。
2. reviews/integration/phase-2-defg-cross-session-reconciliation.md 和 reviews/integration/phase-1-abc-cross-document-integration-review.md。
3. 00-governance/ 下的全部治理基线。
4. A/B/C 当前 main 文档。
5. D/E/F/G 下列确切分支与基线提交：
   D: session-d-memory-brain-2026-11-16 @ 9dc08c63f6912320e290a963c634748ec44a81c8
   E: session-e-memory-compiler-2026-11-16 @ 54df136d1e410af834461950e3c61c5c80abd6ad
   F: session-f-memory-runtime @ dad5deb6bfaa2df9956930d0b1372df354112567
   G: session-g-memory-context @ 3d2c065be863bc1d349faaeece6f6eaa0047abae
6. H/I 尚无正式设计包。不得假设其已经存在。

【你的责任】
A. 建立统一决策登记表，追踪 INT-P0-01..04、INT-P1-01..06、INT-X-01..08、D-REV-P1-001..003。
B. 协调 D/E/F/G 与存储工程，提出 typed cursor/watermark contract。必须区分：
   - source Event cursor；
   - canonical commit cursor；
   - per-aggregate revision；
   - LifecycleEvent cursor；
   - per-index/per-partition publication watermark；
   - Forget fence/epoch；
   - Context version；
   - Delivery ID/sequence；
   - Adapter capability epoch；
   - inference request ID。
   每种 cursor 必须定义 owner、namespace、scope/partition、单调性、gap 语义、resume/replay 规则及因果关系。禁止用一个无类型整数混装不同序列。
C. 建立跨模块接口矩阵：producer、consumer、authoritative owner、immutable ID、version、consistency、failure、retry。
D. 组织 conformance test 计划；没有可复现证据不得标记 PASS。
E. 确保所有结论明确标记 DECIDED / CANDIDATE / ADR-BLOCKED / OPEN / TO_VALIDATE。

【只允许创建/修改你负责的文件】
- reviews/integration/contract-registry.md
- reviews/integration/typed-cursor-and-watermark-contract.md
- reviews/integration/cross-module-conformance-plan.md

建议在独立 A 工作分支上工作；如果仓库实际已有 A 分支，先核实，不要猜分支名。不要覆盖其他人的文件，不要修改 00-governance 基线，不要合并任何分支。

【验收】
1. 所有 INT 与 D-REV 项目都有唯一 accountable owner、状态、依赖和关闭证据。
2. Cursor/watermark 语义跨 D/E/F/G 一致。
3. 没有模块越权声明其他模块的权威对象。
4. 所有未决项可见，不因措辞而被静默关闭。
5. 提交后重新读取 GitHub 文件验证，并报告 exact branch/base SHA/commit SHA/changed paths。

【禁止】
不得把跨模块协调意见伪装成已批准 ADR；不得冻结 Fact/Claim、Forget、BMCP、Applied 或 Security 契约；不得声称性能达标。
```

---
