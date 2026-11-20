# Memory Compiler — 阅读指南

- 文档 ID：E-READING-GUIDE-001
- 版本：1.0
- 英文对应：[Memory Compiler Reading Guide](../../en/04-memory-compiler/README.md)

## 已完成双语配对的源规范

1. [Compiler 总览](compiler-overview.md) — Pipeline、职责边界、确定性/模型辅助阶段和安全不变量。
2. [Accepted Receipt 与幂等契约](accepted-receipt-and-idempotency-contract.md) — 可靠接收、独立 Receipt、Retry/Replay 和 Evidence 边界。
3. [Compiler 状态机与 D Producer Admission](compiler-state-and-producer-admission.md) — WorkItem/Attempt/Lease 身份、D Registration、Barrier 和 Terminal Disposition。

## 尚待双语化的核心源规范

E 分支清单还包含 Event Ingestion、Extraction/Normalization、Consolidation/Conflict Resolution、Evidence/Provenance，以及 Forget Fence/Derived Registration 规范。它们的完整双语伴随文档仍待完成，进度见[双语迁移状态](../../governance/translation-status.md)。

## 权威与状态

E 拥有来源接收/编译编排、Candidate 生成、Stage Lineage、Retry/Replay 和 Producer-side Derivative Evidence。D 拥有 Canonical Identity/Version/Lifecycle 和 Forget Fence 语义。I 拥有授权/PermissionEpoch 和 Global Forget Policy。Storage/Consistency 默认不拥有领域语义；必须明确指定其实现责任 Owner。

CANDIDATE 描述不是已批准 Schema。Fact/Claim 仍为 ADR-BLOCKED 时，不得冻结映射。D/E/Storage 的原子 Admission/Dependency/Publication 实现仍为 OPEN，直到联合证据通过审查。
