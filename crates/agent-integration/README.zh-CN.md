# Agent Integration 参考模型

本 crate 是确定性的 Rust 参考模型，覆盖两项契约：

1. 按能力等级授权 Adapter 操作。
2. 拒绝写入受保护请求区域，以及拒绝修改已冻结的推理请求。

在仓库根目录执行：

```sh
cargo test -p agent-integration
```

测试套件包含四个单元测试。本次交付的测试执行状态：**NOT RUN（由派工方执行）**。

这不是生产级 Adapter：不执行真实模型推理、网络传输、持久化、BMCP 协商或生产级遥测。模型只校验操作并返回类型化的 `AdapterError` 枚举值。

选择实现的两类推理边界情形，是因为 `inference-boundary-model.md` 将两者标记为 DECIDED：(a) Brain 不得写入受保护区域；(b) 请求组装快照冻结后，请求不可变。版本缺口协调虽已在源规范中定义，但有意不纳入这个最小模型。
