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
