# Phase 1 SQLite Adapter 契约

状态：CANDIDATE 工程实现；不构成生产就绪证据。

## 范围

将 Phase 1 MemoryStorage Trait 实现到 SQLite，包括：
- 显式 Schema 初始化；
- 不可变 Version Row；
- Current-Version CAS；
- Idempotency Receipt 持久化；
- 单调 Commit Sequence；
- Version/Current Pointer/Commit Log/Idempotency 的原子事务；
- 带 Scope Filter 的读取与变更列表。

## 明确限制

本 Adapter 不实现 Event Store、Lifecycle Manager、Forget 擦除、分布式协调、Backup/PITR、多进程线性一致性证明或生产部署拓扑。

Memory 和 MemoryVersion 的序列化只是工程表示。Claim 跨 MemoryVersion 身份仍保持 OPEN，本 Adapter 不偷偷关闭该决策。

## 事务模型

Writer 使用 SQLite Immediate Transaction。提交边界包括 Version Row、Current Pointer、Commit Log 和 Idempotency Receipt。事务失败必须回滚。

## 验证边界

PR 包含 SQLite 内存数据库 round-trip、幂等和 stale-version 测试。仓库目前尚无 Rust CI，因此在工作流建立前不声称 GitHub Actions 测试通过。
