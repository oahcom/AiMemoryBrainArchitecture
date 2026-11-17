# Architecture Breakthrough — 总协调记录

**状态：** 四条隔离研究分支已建立；本文件是协调入口，不是架构决策。  
**共同基线：** `main@b3c666e67982cb3d3374e759cfb6552c7765aacb`（2026-11-18）  
**总跟踪：** [Issue #43](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/43)

## 工作流

| ID | 研究方向 | 分支 | 当前状态 |
|---|---|---|---|
| A | Forget Protocol Formal Verification | `research/breakthrough-a-forget-model-checking-2026-11-18` | 已建立隔离分支；模型/来源核验待执行 |
| B | Memory Operating System | `research/breakthrough-b-memory-operating-system-2026-11-18` | 已建立隔离分支；基线分析/原型待执行 |
| C | Memory IR / Compiler | `research/breakthrough-c-memory-ir-compiler-2026-11-18` | 已建立隔离分支；基线分析/原型待执行 |
| 0 | Principal Coordination | `research/breakthrough-0-coordination-2026-11-18` | 本协调记录 |

## 共同规则

- 每个方向独立读取精确当前来源，记录 branch HEAD、path、Blob SHA。
- 只在各自 research branch 新增报告、模型、合成数据和原型。
- 不改 main、Owner 分支、现有 PR、Issue #43 正文或权威契约。
- 不合并、不部署、不启动生产 Runtime 实现。
- 中英文件同一变更集，保持语义一致。
- 分类：DECIDED / CANDIDATE / TO_VALIDATE / UNRESOLVED / REJECTED。
- 模拟其他 Owner 角色不等于独立 Owner 批准；模型通过不等于物理生产验证。

## 初始系统问题映射

1. Forget 安全：跨 Owner Admission、Dependency Registration、Publication、Visibility、Restore 的组合证明不足。
2. Runtime 复杂度：Retrieval、Activation、Context Budget、Eviction 可能存在重复决策与状态同步。
3. Formation 复杂度：Raw Experience 到 Canonical Memory 的中间表示、类型边界、Provenance 和增量演化需要验证。

以上是研究假设/已知问题映射，不是对当前规范的完整审查结论。

## 汇总门禁

任何方向提交结论前必须附：
- 精确来源账本与证据等级；
- 可复现的模型/实验/命令；
- 反例或负面结果；
- 与现有架构的逐项对照；
- 安全、复杂度、性能、迁移和运维影响；
- 未决问题及其正确权威归属；
- 中英双语语义对等检查。

## 总协调最终问题

最终比较应回答：哪些机制应复用成熟产品、哪些领域不变量必须自研、哪些模块可合并/下沉、哪些候选不值得引入，以及最小安全可行架构是否因此更容易实现。除非得到正式批准，所有建议保持候选状态。
