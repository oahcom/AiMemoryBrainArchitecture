# 权威记忆大脑架构指南

- 文档 ID：DOC-BRAIN-001
- 版本：1.0
- Owner：D — Memory Brain
- 源文件版本：a157b0ed6fc8e45e66fe01a99e6b895f995fd20c
- 对应英文：[Canonical Memory Brain Architecture Guide](../../en/03-memory-brain/memory-brain-guide.md)
- 状态：解释性指南；跨模块执行和实现证据仍受集成门禁约束

## 1. Memory Brain 是什么

Memory Brain 是持久化、可寻址 Canonical Memory 资产的权威。它拥有稳定的 Memory 身份、不可变版本、Claim/Entity/Relation 的规范引用、生命周期历史，以及执行受治理 Forget 所需的权威领域记录。

它不是事件接收流水线、检索引擎、Agent 上下文规划器、协议网关、全局授权服务，也不是物理删除执行器。这些职责分别由 E/F/G/H/I 和共享基础设施按照明确契约承担。

## 2. D 负责什么，不负责什么

| D 负责 | D 不负责 |
|---|---|
| Canonical Memory 身份和不可变版本 | Event 接收和完整编译流水线（E） |
| 权威 current-version pointer 和历史读取 | 检索排序、Runtime 缓存、索引维护（F） |
| Canonical 生命周期记录和转换历史 | Context 规划、ContextVersion、Delivery 状态（G） |
| Entity/Relation 规范身份和引用 | BMCP wire 协议和 Adapter 本地行为（H） |
| ForgetOperation、Canonical Forget Fence、依赖清单权威 | 全局授权、保留/备份策略、物理擦除（I） |
| Canonical Commit Cursor 语义 | 存储引擎实现和事务证明 |

这一区分非常重要：D 可以定义权威记忆域中的 Forget 屏障，并提供 Canonical Target 的证据；但 D 不能宣称所有索引、缓存、Adapter、备份和外部副本都已擦除。

## 3. Canonical Memory 与不可变版本

一个 Memory 是稳定身份及其不可变版本序列。更新 Memory 时必须创建后继版本，禁止原地修改历史版本。

Canonical Commit 必须：
- 校验对象身份、引用、Scope 兼容性、Schema 版本以及必需的 Evidence/Provenance。
- 使用 expected-version/CAS 或等价并发控制。
- 保留历史版本和明确的变更原因。
- 使 current-version pointer 与已提交版本保持一致。
- 发布可恢复的变更意图，以便索引和下游消费者协调。

Schema 合法不代表内容真实。D 保存规范命题及其证据/认知限定，但不独立裁定客观真相。

## 4. Lifecycle 不等于真实性

Lifecycle 描述管理状态，不代表 Confidence、Relevance、Trust 或 Claim 的认知状态。D 的 Canonical Lifecycle 状态包括 Candidate、Consolidated、Active、Superseded、Archived 和 Forgotten。Claim 可以处于 Disputed，而其所属 Memory 仍处于 Active。

Forget 由受治理的 ForgetOperation 及其持久化记录表示。临时抑制和工作流状态不能与普通 Memory Lifecycle 转换混淆。只有满足 I 规定的完成条件后，Memory 才能标记为 Forgotten；D 无权单方面宣布全局 Forget 完成。

## 5. Entity 和 Relation 身份

Entity 身份不是展示名称、文本提及或相似度匹配。D 保留稳定不透明 Entity ID、带版本的属性/别名、解析证据，以及明确的 Merge/Split 历史。

Relation 是带类型的关联，必须验证端点、方向性、Scope、时间有效性、认知限定和 Evidence 引用。文本共现或 Embedding 相似度不足以创建规范 Relation。身份解析存在歧义时必须返回歧义，不得猜测。

## 6. Canonical Cursor 模型

D 为每个 Canonical Memory Authority 定义一个全局有序 CanonicalCommitCursor。其他游标属于独立的类型化命名空间：

| Cursor | 作用范围 | 排序对象 |
|---|---|---|
| CanonicalCommitCursor | 一个 Brain Authority | 成功的 Canonical Transaction |
| AggregateRevision | 一个 Aggregate | 该 Aggregate 的不可变修订 |
| LifecycleEventCursor | 一个 Memory | 追加式 Lifecycle Event |
| IndexWatermark | 一个 Index Partition | 该分区已连续处理的 Canonical Commit 前缀 |
| ForgetFenceCursor | 一个 Forget Operation | Fence Generation 和目标集合身份 |

这些 Token 不可互换。Canonical Commit Cursor 不证明索引已应用、Context 已投递、Forget 已抑制或数据已物理删除。IndexWatermark 也不证明全局 Forget 已完成。

## 7. Forget Fence 与完成边界

Forget Fence 是持久化抑制屏障，目的是在 Forget 生效后，阻止过期或迟到任务再次发布或暴露相关内容。

D 的权威领域契约覆盖：
1. 持久化 ForgetOperation 身份和单调递增 Fence Generation。
2. 受影响的 Canonical Target 集合及依赖清单。
3. Producer Registration 和 Barrier 任务核算。
4. Canonical Domain 的抑制决策和逐目标进度证据。
5. 按照 I 的全局完成条件，有控制地转换为 Forgotten。

跨模块执行职责如下：

| Owner | Forget 职责 |
|---|---|
| D | Canonical ForgetOperation、Fence、依赖清单、Canonical Target 证明 |
| E | 队列、Lease、重试、DLQ、Replay、派生物登记和 Publish Gate |
| F | 在途检索、候选抑制、缓存/工作集、索引重建和水位 |
| G | Context Snapshot、Delta、ChangeSet、Delivery Intent 和协调 |
| H | Adapter 本地状态、离线重连、清理/抑制 ACK |
| I | Principal/授权、保留、备份/外部副本、残留例外和全局完成策略 |

**关键实现缺口：** Producer Admission、Fence 安装、Dependency Registration 和派生物 Publication 必须共享经过证明的原子/线性化边界。先单独“读取 Fence”，再发布的流程是不安全的。D 和 E 已描述所需语义，但仍需要 D/E/Storage 集成和故障注入证据。不得仅凭 D 的局部记录宣称全局 Forget 闭环完成。

## 8. 故障与恢复要求

- Canonical Version 不可变；恢复时应协调或推进指针，不得改写历史。
- 过期写入必须被拒绝，并基于最新 Canonical Version 进行协调。
- Outbox/Replay 必须幂等，并重新检查当前 Fence 和授权。
- 缺失的 Evidence/来源材料必须标记为不可用；Replay 时不得伪造。
- Index 和 Projection 可以重建，但重建必须遵守 Forget Fence 和当前策略。
- Cursor 缺口和消费者延迟必须显式表达；Cursor 不能代替消费者 Receipt。
- 在持久化状态与发布之间发生崩溃时，恢复不得产生重复逻辑效果或旧内容复活。

## 9. 未决和待验证事项

- Fact/Claim 身份及修订语义仍受阻塞 ADR 约束；正式解决前禁止冻结下游 Schema。
- Storage 必须证明 Producer Admission/Fence/Publication 原子操作。
- E/F/G 消费者必须符合类型化 Cursor 命名空间。
- I 必须定义全局 Forget 完成和残留例外策略。
- H/C 必须证明 Adapter 清理/重连和 Applied 证据。
- 仍需进行崩溃、竞态、Replay、索引重建、缓存失效和备份恢复测试。

## 10. D 的详细源规范

- [Memory Brain 总览](https://github.com/oahcom/AiMemoryBrainArchitecture/blob/session-d-memory-brain-2026-11-16/03-memory-brain/memory-brain-overview.md)
- [Canonical Memory Store](https://github.com/oahcom/AiMemoryBrainArchitecture/blob/session-d-memory-brain-2026-11-16/03-memory-brain/canonical-memory-store.md)
- [Memory Lifecycle Manager](https://github.com/oahcom/AiMemoryBrainArchitecture/blob/session-d-memory-brain-2026-11-16/03-memory-brain/memory-lifecycle-manager.md)
- [Entity and Relationship Manager](https://github.com/oahcom/AiMemoryBrainArchitecture/blob/session-d-memory-brain-2026-11-16/03-memory-brain/entity-and-relationship-manager.md)
- [Memory Versioning](https://github.com/oahcom/AiMemoryBrainArchitecture/blob/session-d-memory-brain-2026-11-16/03-memory-brain/memory-versioning.md)
- [Forget Fence and Completion Contract](https://github.com/oahcom/AiMemoryBrainArchitecture/blob/session-d-memory-brain-2026-11-16/03-memory-brain/forget-fence-and-completion-contract.md)
- [Canonical Commit Cursor Semantics](https://github.com/oahcom/AiMemoryBrainArchitecture/blob/session-d-memory-brain-2026-11-16/03-memory-brain/commit-cursor-semantics.md)

本指南让职责边界和关键不变量更易理解；它不声称 Storage 原子操作或端到端 Forget 已经实现或验证。
