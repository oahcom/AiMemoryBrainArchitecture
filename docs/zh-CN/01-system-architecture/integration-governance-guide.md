# 主集成架构与契约治理指南

- 文档 ID：DOC-INTEGRATION-001
- 版本：1.0
- Owner：A — Principal Integration Architect
- 源规范：A Owner 分支中的 Phase 3.5 Contract Registry 和 Typed Cursor/Watermark 协调规范
- 对应英文：[Principal Integration & Contract Governance Guide](../../en/01-system-architecture/integration-governance-guide.md)
- 状态：CANDIDATE 协调指南；不代表契约冻结或实现批准

## 1. 为什么需要 A

A 维护跨模块系统视图。A 协调契约依赖关系，记录每个语义 Token 的权威 Owner，识别规范冲突，并判断跨模块证据是否足以推进集成门禁。

A 不能替代领域 Owner。A 的 Registry 负责记录和协调决议，不负责创建、批准或覆盖 B–I 的领域契约。

## 2. 必须区分的证据维度

| 证据维度 | 能证明什么 | 不能证明什么 |
|---|---|---|
| Artifact Exists | 指定分支/HEAD 上存在且可读取准确文件 | Owner 已批准或已经实现 |
| Owner Decision | 负责 Owner 在其规范中明确将语义决策标记为 DECIDED | 跨模块已接受或运行时行为正确 |
| Cross-module Agreement | 受影响的权威 Owner/消费者接受同一契约和边界 | 持久化正确或测试通过 |
| Implementation Evidence | 可执行行为和可复现测试支持该结论 | 除非治理门禁也通过，否则不代表生产批准 |

文档出现在 Registry 中，不会自动提升其状态。架构审查结论也不等于实现测试结果。

## 3. 契约 Registry 职责

每个跨模块契约都必须记录：
- Contract ID 和精确文档路径。
- Owner 与语义权威。
- 消费模块及预期行为。
- 审查过的准确 Branch、HEAD Commit 和 Artifact Revision。
- 状态：DECIDED、CANDIDATE、ADR-BLOCKED、OPEN、TO_VALIDATE、NOT_RUN。
- 跨 Owner 接受证据。
- 与设计证据分开的实现/测试证据。
- 已知不兼容、依赖和下一步关闭动作。

Registry 必须区分“文件存在”“Owner 已决议”“消费者已接受”和“运行时已证明”，不得从其中一个推断另一个。

## 4. Typed Cursor 和 Epoch 治理

Token 必须保持类型化和命名空间隔离。消费者不得把不同命名空间的值当作一个标量序列进行比较、强转、递增、相减、排序或替代。

主要命名空间包括：
- CanonicalCommitCursor — D；每个 Canonical Memory Authority 一个全局顺序。
- AggregateRevision — D；只在单个 Aggregate 内有序。
- LifecycleEventCursor — D；只在单个 Memory 内有序。
- IndexWatermark — F；每个 Index/Channel Partition 独立，并携带 D 的 applied-through Cursor。
- ForgetFenceGeneration/Cursor — D；每个 Forget Authority/Operation 及目标链路独立。
- Producer Registration/High-water Token — E/D 契约边界。
- PermissionEpoch — I；授权策略代数。
- ContextVersion — G；单个 Context 的权威版本序列。
- AdapterCapabilityEpoch — H/C；单个 Adapter 的能力声明代数。

这些 Token 不可互换。Canonical Commit 进度不等于 Index Application；Index Watermark 不等于 Forget 完成；ContextVersion 不等于 Applied；ForgetFenceGeneration 不等于 PermissionEpoch。

## 5. 集成门禁

A 应按依赖顺序协调关闭：
1. 领域和身份语义：Fact/Claim ADR、类型化 Principal/ActorRef/ScopeRef、Issuer/Delegation 绑定。
2. Forget 和撤销：持久化 Fence、Producer Barrier、派生物清单、本地抑制、备份/外部副本策略、全局完成证据。
3. 跨模块契约：Accepted Receipt、Cursor/Watermark 命名空间、Context Delivery/Applied、恢复桥接。
4. Conformance：共享契约测试、竞态/故障注入、安全测试。
5. 正确性关键契约稳定后，再进行性能/资源验证。

只有当必需 Owner 接受了准确版本的契约，并且相应层级的证据存在时，门禁才能推进。候选提案或文档存在本身不够。

## 6. 当前跨模块阻塞

- Fact/Claim 仍为 ADR-BLOCKED；依赖它的 Schema 不得冻结。
- Principal/ActorRef/ScopeRef/ProducerIdentity 和 PermissionEpoch 绑定需要 B/I/H/C 一致确认。
- D/E/Storage 的 Producer Admission、Forget Fence 安装、Dependency Registration 和最终 Publication 需要一个经过证明的原子/线性化边界。
- I 的 Global Forget Evidence Vector 必须映射 H Adapter ACK Class 和 D/E/F/G 本地目标状态。
- F 必须证明 Scope-first Retrieval、Cache/Index 防复活和 Typed Watermark 消费。
- G/H/C/I 必须证明最终请求 Applied 语义和离线重连行为。
- JF-10/COC 同 XID 恢复及参与者集成需要可执行证据。

## 7. A 不得作出的声明

A 不得：
- 将 CANDIDATE Registry 称为契约冻结。
- 把 Owner 局部决议视为跨模块一致接受。
- 把源文档或设计审查当作实现证据。
- 把 Index Watermark 当作 Forget 完成证明。
- 把 Applied 当作模型理解的证明。
- 把局部清理成功当作全局物理擦除。
- 通过文档措辞批准被阻塞的 ADR。

## 8. 集成验收

只有满足以下条件，集成发现项才算关闭：
1. 负责语义的 Owner 已作出或接受决议。
2. 所有受影响消费者已协调同一准确版本。
3. Registry 记录了准确 Branch/Commit/File 证据。
4. 附上所需的实现、故障、安全或性能证据。
5. 中英文版本符合 GOV-DOC-001 的语义一致性要求。

实时协调资料见 [A Owner 分支](https://github.com/oahcom/AiMemoryBrainArchitecture/tree/session-a-integration-2026-11-16/reviews/integration)。
