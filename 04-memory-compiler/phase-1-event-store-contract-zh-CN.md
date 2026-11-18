# Phase 1 Event Store 契约

状态：DECIDED 语义 / CANDIDATE 实现边界。

Event Store 是 Source Event 的持久化 custody 边界。Accepted 表示 Event 元数据、Payload 引用/完整性、幂等身份、Receipt 和可恢复处理意图已经持久提交。Accepted 不等于 Compiled、Verified、Indexed 或 Canonical。

契约要求显式 Scope、Producer Identity、Payload Digest 和 Idempotency Key。SQLite 候选实现将幂等身份定义为 `(producer_actor_ref, idempotency_key)`：同一身份加同一 Digest 返回原 Receipt；同一身份加不同 Digest 必须冲突。重放 Receipt 前先执行 Scope 授权检查。

候选实现通过一个事务持久化完整 Envelope、声明的 Payload 引用/Digest、Acceptance Time、Receipt Identity 和初始 `Pending` 处理状态。它不存储 Payload Bytes，也不独立计算 Payload Hash；Digest 正确性仍是上游断言。`replay` 只返回未改变的原 Receipt，不会入队或执行任务。Queue 投递、处理状态转换、Retention/Forget 授权及 Schema Migration 均不属于本 Adapter。

Replay 重用原 Event Identity 和原 Acceptance Time。Forget/Retention 检查仍由独立策略权威负责。

本单元不包含 SQLite 实现、Queue 拓扑、分布式事务、吞吐目标或生产持久化证明。
