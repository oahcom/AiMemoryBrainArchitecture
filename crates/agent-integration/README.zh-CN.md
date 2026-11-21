# Agent Integration 参考模型

本 crate 是确定性的 Rust 参考模型，覆盖：
1. 按能力等级授权 Adapter 操作。
2. 推理边界受保护区域写入拒绝。
3. 通过 `ContextDeliveryAdapter` 执行 session 级上下文交付。

在仓库根目录执行：

```sh
cargo test -p agent-integration
```

测试套件包含 **八个单元测试**：原有四个授权/边界测试，以及四个交付生命周期测试（成功后继版本应用、过期/跳号版本拒绝且状态不变、清空/重置、断连/重连版本报告）。

`InMemoryContextDeliveryAdapter` 仅在进程内存中保存快照和连接状态。它强制要求精确的后继版本（新 session 或清空后的 session 从版本 1 开始），只记录成功应用的快照，在 Forget/撤销时清空已应用状态，并在重连后报告最后一次成功应用的版本。

**NOT IMPLEMENTED（未实现）：** 真实传输；逐运行时 Agent 集成；持久化交付账本或持久化 session 状态；自动重试/重新交付；生产级协调或应用证明。Reconnect 不能证明远端 Agent 的真实状态。本 crate 不执行也不声称实现真实模型推理、Provider 集成、BMCP 协商或生产级遥测。

后继版本检查不等于快照/增量协调：生产级版本缺口恢复仍不在范围内。
