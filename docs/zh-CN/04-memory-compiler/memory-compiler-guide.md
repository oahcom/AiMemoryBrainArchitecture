# 记忆编译器架构指南

- 文档 ID：DOC-COMP-001
- 版本：1.0
- Owner：E — Memory Compiler
- 源规范：E Owner 分支中的 Compiler 总览及 Phase 3 Accepted Receipt/Forget 契约
- 对应英文：[Memory Compiler Architecture Guide](../../en/04-memory-compiler/memory-compiler-guide.md)
- 状态：解释性指南；编排拓扑仍为 CANDIDATE，资源/性能声明仍为 TO_VALIDATE

## 1. 目的

Memory Compiler 将可靠接收的 Event 和已登记来源材料，转换为可追溯的候选 Memory、Claim、Entity 和 Relation。它只通过 D 所有的契约协调 Canonical Commit，之后再请求下游 Projection/Index 发布。

它是一条可恢复的语义转换流水线，不是把文本交给 LLM、再写入向量数据库的捷径。

## 2. E 负责什么

- 编译任务编排和持久化 Work Item 状态。
- 确定性校验、规范化、分类和来源处理。
- 在有界、版本化策略下执行可选的模型辅助提取。
- 创建 Evidence 和 Provenance，保留精确来源引用及派生链路。
- 提出候选 Entity/Relation 和冲突提案。
- 处理编译任务重试、Lease、Replay 和最终处置。
- 在不接管 D 权威的前提下协调 Canonical Write 和发布通知。

E 不拥有 Canonical Schema/Lifecycle 权威（D）、Runtime 检索和缓存（F）、ContextVersion（G）、BMCP Wire/Adapter 行为（H/C）、全局身份/权限/保留策略（I），也不负责物理索引实现。

## 3. Accepted 不等于 Compiled

必须区分以下里程碑：

| 里程碑 | 含义 |
|---|---|
| Accepted | 来源 Event 及必需的 Receipt/Idempotency 状态已可靠持久化 |
| Compiled | Compiler Work Item 已形成有记录的处理结果 |
| Candidate Produced | 已创建结构化候选对象及其来源链路 |
| Canonical Committed | D 已接受并提交权威 Memory Version |
| Indexed | 某个 Index Partition 已处理对应 Canonical Commit |
| Context Applied | 后续 Adapter 推理边界确认；不属于 E 的职责 |

Accepted Event 最终没有候选结果也可能完全合理，例如 NO_CANDIDATE、PENDING_EVIDENCE、REVIEW_REQUIRED、DEFERRED 或 REJECTED。可靠接收不得依赖同步 LLM 推理。

## 4. 编译流水线

~~~text
可靠 Event + Idempotency + Accepted Receipt
        ↓
可恢复 Compile Intent / Work Item
        ↓
Scope 与授权检查
        ↓
确定性规范化和分类
        ↓
可选模型辅助提取
        ↓
Evidence / Provenance / 候选 Memory 与 Claim
        ↓
Entity 和 Relation 解析提案
        ↓
冲突提案和 Canonical Write Request
        ↓
D Canonical Commit
        ↓
Index / Projection 发布请求
~~~

必须在来源解引用、提取、实体匹配、合并或写入之前完成 Scope 过滤。即使推理服务不可用，确定性处理阶段也必须能够继续工作。

## 5. 模型辅助处理

LLM 可以提出提取或规范化结果，但不能确立事实、批准 Canonical Lifecycle 转换、解决授权问题，也不能决定 Fact 是否是独立领域对象。每个模型辅助转换都必须按详细契约记录足以识别模型、Prompt/Policy 版本、输入链路、输出和校验结果的信息。

流水线必须有明确边界：超时、重试、并发、Token Budget 和资源配额都必须定义。模型故障应使相关任务延迟或重试，而不是丢失已经可靠接收的来源。

## 6. 持久化任务、幂等和 Replay

每个 Work Item 都需要稳定身份、来源和 Scope 引用、Schema/Policy 版本、幂等范围、Lease/Retry 状态以及持久化阶段结果。重放同一逻辑任务不得产生重复 Canonical 效果。

相同 Idempotency Key 对应不同 Payload Digest 时，应判定为冲突，而不是成功去重。Accepted Receipt 不等于 Canonical Commit Receipt。

Retry 和 Replay 必须重新检查当前授权与 Forget Fence。某项旧任务不能仅因为在 Fence 之前被接收，就绕过后续 Forget 操作。

## 7. Forget 与派生物发布

E 是派生资产生产者，必须参与 D 的 Forget 契约：
- 在输出可见前登记 Producer Class 和具体 Work Item。
- 为每个派生物保留持久化来源链路和依赖登记。
- 在通过发布门之前，暂存输出必须保持不可见。
- 最终发布时重新检查当前 Forget Fence 和授权。
- 在 Retry、Lease 恢复、DLQ Replay 或 Recompile 时，不得使已抑制内容复活。

Producer Admission、Fence 安装、Dependency Registration 和 Publication 的精确原子边界，是 D/E/Storage/Consistency 的跨 Owner 要求。E 的本地检查本身不能关闭竞态。在事务设计和故障注入测试证明之前，这仍是实现/一致性验收阻塞项。

## 8. 故障处理

| 故障 | 必须行为 |
|---|---|
| LLM 不可用 | 继续确定性阶段；模型依赖阶段延迟或重试 |
| Worker 崩溃 | 根据 Lease/Intent 状态恢复持久化任务 |
| 重复投递 | 幂等空操作或返回之前的 Receipt |
| 相同 Key、不同 Digest | 作为冲突拒绝 |
| 来源缺失 | 保留引用并标记不可用，不得伪造 |
| Permission 被撤销 | 在受保护处理/发布前重新检查并 Fail Closed |
| Forget Fence 前进 | 抑制旧输出并记录最终处置 |
| Canonical Commit 冲突 | 重新读取 D 状态并协调，不得静默覆盖 |
| Index 发布延迟 | 保持 Canonical Commit 与 Index 可见性分离 |

## 9. 接口和不保证事项

输入包括 Accepted Event 引用、Source/Content 引用、认证 Actor/Scope 上下文、权限决策上下文、Schema 版本、时间戳、幂等身份、Retention Class、信任元数据和关联/因果 ID。

输出包括阶段 Receipt、候选 Envelope、Evidence/Provenance 引用、Entity/Relation 与 ConflictSet 提案、CanonicalWriteRequest/Result、发布请求，以及结构化可重试/永久错误。

Compiler 输出不证明真实性、用户意图、外部行动授权、模型正确性、索引可见性、Context 已应用或物理擦除已完成。

## 10. 仍需验证

- Accepted Receipt 和 Idempotency 的崩溃一致性。
- Worker 崩溃、Lease 过期、Retry、DLQ、Replay 和 Recompile。
- D/E/Storage 原子 Producer Admission 与 Publication Gate。
- Forget 竞态和迟到派生物抑制。
- Provenance 完整性和未经授权的来源解引用拒绝。
- 模型离线时的降级运行及资源边界。
- 代表性吞吐量和延迟基准。

## 11. 详细源规范

详细 Compiler 契约见 [E Owner 分支](https://github.com/oahcom/AiMemoryBrainArchitecture/tree/session-e-memory-compiler-2026-11-16/04-memory-compiler)。本指南不替代字段级 Schema，也不表示实现已通过验收。
