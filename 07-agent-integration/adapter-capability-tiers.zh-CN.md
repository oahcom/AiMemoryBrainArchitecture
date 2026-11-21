# Agent Adapter 能力等级

**状态：** 等级意图与保证边界已决定；操作级绑定作为参考模型的可执行解释  
**Owner：** Session C — Agent Integration  
**对应英文规范：** [adapter-capability-tiers.md](adapter-capability-tiers.md)

## 14. 可执行操作绑定（参考模型契约）

下表将已决定的等级保证绑定为可执行操作。该映射是确定性参考模型契约，不是 BMCP 线上协商协议，也不是生产级 Adapter 实现。

| 操作枚举 | 最低等级 | Tier 1 | Tier 2 | Tier 3 |
|---|---:|---:|---:|---:|
| `SubmitScopedTelemetry`（提交有作用域的遥测） | 3 | 允许 | 允许 | 允许 |
| `RequestActiveRecall`（主动回忆请求） | 3 | 允许 | 允许 | 允许 |
| `InsertMiddlewareMemorySlot`（写入中间件记忆槽） | 2 | 允许 | 允许 | 拒绝 |
| `AttestMiddlewareApplication`（证明中间件应用） | 2 | 允许 | 允许 | 拒绝 |
| `ObserveFullInferenceBoundary`（观察完整推理边界） | 1 | 允许 | 拒绝 | 拒绝 |
| `ApplyFullBoundaryMemory`（在完整边界应用记忆） | 1 | 允许 | 拒绝 | 拒绝 |
| `AttestFullBoundaryApplication`（证明完整边界应用） | 1 | 允许 | 拒绝 | 拒绝 |
| `ReconcileSnapshotAndDelta`（快照与增量协调） | 1 | 允许 | 拒绝 | 拒绝 |

较低等级不得仅因能够表达某项请求，就执行该操作。参考模型返回类型化错误 `AdapterError::TierInsufficient { required, actual }`；调用方必须匹配枚举，不能解析显示文本。Tier 1 包含 Tier 2 和 Tier 3 的操作能力；Tier 2 包含 Tier 3 的操作能力。

## 15. 推理边界拒绝码

参考模型提供以下可断言的边界拒绝原因：

- `ProtectedRegionMutation(region)`：尝试写入 System 指令、Developer 指令、用户输入、Agent 安全策略、工具 Schema/授权或 Agent 工作状态。
- `RequestAlreadyFrozen`：请求组装器冻结推理请求后，仍尝试修改 Brain 管理区域。

这两条规则直接落实 `inference-boundary-model.md` 中已决定的原则：受保护区域不可由 Brain 写入；已冻结/执行中的请求不可变。本参考模型实现这两类边界情形；版本缺口协调仍由源规范定义，但不在此最小模型中实现。

## 16. 范围与状态

该映射是对本文已标记为 DECIDED 的等级保证所作的可执行解释。线上协商、已认证的能力声明、传输、Provider 集成、真实推理和生产级遥测均不在范围内。本模型不声称实现上述能力。


## 17. 内存上下文交付生命周期（已实现的参考行为）

crate 现在提供 `ContextDeliveryAdapter` trait 和 `InMemoryContextDeliveryAdapter`。内存实现按 session 保存已应用的 `ContextSnapshot` 与连接标志。

| 生命周期动作/状态 | 已实现行为 |
|---|---|
| 已连接 / apply | 仅接受精确的后继版本（新 session 或清空后的 session 从版本 1 开始）；只有接受后才记录快照 |
| 版本拒绝 | 返回类型化错误 `AdapterError::VersionMismatch { expected, received }`；已应用快照保持不变 |
| Clear | 移除已应用快照；下一次 apply 从版本 1 开始 |
| 已断连 | 使用 `SessionDisconnected` 拒绝 apply；保留最后一次成功应用的快照 |
| Reconnected | 恢复内存连接标志，并报告最后一次成功应用的版本（或 `None`） |

**NOT IMPLEMENTED（未实现）：** 真实传输；逐运行时 Agent 集成；持久化交付账本；持久化 session 状态；自动重试/重新交付；生产级协调或应用证明。Reconnect 只是确定性的内存状态转换，并不能证明远端 Agent 的真实状态。本实现不转换 Provider 特定运行时对象，也不声称交付状态超出当前进程内存的范围。

## 18. 规范快照类型接入（round 6）

内存交付适配器现在直接接收并保留规范类型
`memory_context::ContextSnapshot`。`agent-integration` 依赖
`memory-context`；依赖方向仍为单向，因为 `memory-context` 不依赖
`agent-integration`。不再定义适配器本地的第二种快照结构，也不需要
调用方手工进行序列化转换。

适配器只使用 `ContextSnapshot.context_version` 作为版本值。接受 apply
之前，必须调用 `memory_context::validate_snapshot`。验证失败通过类型化
错误 `AdapterError::InvalidSnapshot(ContextError)` 返回；版本不连续返回
`VersionMismatch { expected, received }`；断连 session 返回
`SessionDisconnected`。这三种拒绝路径都必须保持最后一次成功应用的快照
不变。`applied_snapshot` 返回适配器实际接受的同一个规范快照值。

这仍然是内存中的参考适配器，不是传输层或生产运行时集成。采用规范类型
消除了调用方手工序列化的边界，但本身并不能证明远端 Agent 运行时已经应用
该上下文。
