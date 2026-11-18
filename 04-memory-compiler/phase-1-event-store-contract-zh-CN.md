# Phase 1 Event Store 契约

状态：DECIDED 语义 / CANDIDATE 实现边界。

Event Store 是 Source Event 的持久化 custody 边界。Accepted 表示 Event 元数据、Payload 引用/完整性、幂等身份、Receipt 和可恢复处理意图已经持久提交。Accepted 不等于 Compiled、Verified、Indexed 或 Canonical。

契约要求显式 Scope、Producer Identity、Payload Digest 和 Idempotency Key。同一身份加同一 Digest 返回原 Receipt；同一身份加不同 Digest 必须冲突。

Replay 重用原 Event Identity 和原 Acceptance Time。Forget/Retention 检查仍由独立策略权威负责。

本单元不包含 SQLite 实现、Queue 拓扑、分布式事务、吞吐目标或生产持久化证明。
