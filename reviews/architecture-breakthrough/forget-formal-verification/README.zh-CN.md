# Forget 协议形式化验证工作流（独立研究）

**状态：** 启动基线已固定；研究尚未完成。  
**基线：** `main@b3c666e67982cb3d3374e759cfb6552c7765aacb`（2026-11-18）  
**跟踪：** [Issue #43](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/43)

## 目标

验证 Forget、Producer Admission、Derived Registration、Canonical Publication、Retrieval/Delivery、Index/Cache、Restore/Recovery 在并发、崩溃、重试、旧 Worker 和恢复场景下是否满足防复活安全要求。研究必须以反例和可执行模型为中心，不以增加规范文档代替证明。

## 初始证据边界

- Issue #43 将 D ForgetFence / Storage visibility 的物理线性化组合、跨 Owner publication、Global Forget inventory 与 Restore anti-resurrection 保留为开放阻塞。
- PR #71 是针对 D/I Phase 3.9 的 Storage 角色模拟审查提案，不是独立 Storage Owner 签署，也不是物理验证。
- 以上仅作为定位线索；本分支必须重新读取精确当前来源并记录 branch HEAD、路径、Blob SHA。不得把 Issue 正文或 PR 摘要当作当前规范。

## 建模范围

参与者：Forget coordinator、Producer、Admission authority、Worker、Queue、Derived registrar、Canonical store、Index、Cache、Retrieval/Delivery、Backup/Restore。

至少定义：
1. Forget 的权威状态与线性化点；
2. Admission 与 Forget 的竞争顺序；
3. 派生依赖注册与发布的原子性边界；
4. fencing epoch / generation 的产生、传播、校验；
5. ACK 丢失、重复请求、重试与未知结果；
6. 索引/缓存重建、备份恢复及旧任务重放；
7. 可见性检查与最终交付边界。

## 候选不变量（待从权威规范精确定义）

- F1 No resurrection：完成权威撤销后，旧任务、重放、投影重建或 Restore 不得使目标重新可见。
- F2 Stale publisher rejection：过期 epoch/generation 的 Worker 不得发布。
- F3 Admission ordering：Forget 与新 Producer Admission 必须存在无歧义的序列化关系。
- F4 Dependency completeness：可能产生目标派生物的执行者必须在发布前受可验证的依赖/撤销约束。
- F5 Read/delivery suppression：检索、缓存、上下文和 Adapter 交付均不得绕过撤销状态。
- F6 Idempotent retry：重复 Forget、ACK 丢失及重试不得回退安全状态。
- F7 Restore fencing：恢复旧数据后必须重新施加当前撤销世代。
- F8 Crash safety：所有声明支持的崩溃点均保持上述安全属性。

## 执行计划

1. 读取 main 和 D/E/I/Storage/F/G/H 的当前相关规范、模型、测试与 PR 变更。
2. 建立 source ledger：branch、HEAD、path、Blob SHA、证据等级、读取时间。
3. 用 TLA+/TLC 优先建模；如不可用，采用可执行有限状态枚举并披露局限。
4. 对每条 race 执行双序列检查；在每个 durable boundary 前后注入 crash、lost ACK、duplicate/replay、stale worker、restore rollback。
5. 保存最短反例、模型配置、运行命令、输出摘要。
6. 提出最小修复建议并标注正确的权威 Owner；不修改其契约。

## 证据分级

规范声明、静态模型、模型检查、CI 测试、物理数据库故障注入、部署/运维验证必须分别标注。有限状态空间未发现反例，不等于生产安全证明。

## 禁止事项

只读现有 Owner 权威文件；只在本研究分支增加模型、测试夹具和报告。不得改写 D/E/I/Storage 权威契约、不得合并、不得部署、不得启动生产 Runtime 实现。所有结论分类为 DECIDED / CANDIDATE / TO_VALIDATE / UNRESOLVED / REJECTED。

## 验收

交付状态机、不变量、可执行模型、可重现命令、反例目录、来源账本、修复提案和中英双语结论。任何未覆盖项必须明确列为 UNRESOLVED。
