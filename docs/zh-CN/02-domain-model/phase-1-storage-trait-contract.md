# Phase 1 Storage Trait 契约

状态：CANDIDATE 实现边界；本文件不选择具体后端。

## 目的

定义纯 memory-domain 与未来持久化实现之间与后端无关的 Application Port。

## 操作

- create_memory (with resolved scope)
- read_current
- read_version
- commit_version
- list_changes
- resolve_idempotency (with resolved scope)

## 提交边界

后端实现 MUST 将不可变 Version、Current-Version CAS、Idempotency Record 与 Canonical Commit Sequence 视为一个可恢复提交边界。本 Trait 不规定 SQLite DDL 或分布式事务协议。

## 安全

每次读写都接收已解析 Scope，包括 create_memory 与幂等查询。后端 MUST 拒绝 memory_id 与 new_version.memory_id 不一致的 CommitRequest。后端 MUST NOT 将陈旧 Projection 当作 Canonical State。expected_current_version 是乐观并发保护。

## 幂等

相同 Idempotency Key + Request Digest 可以返回原 Receipt；相同 Key + 不同 Digest MUST 返回 IdempotencyConflict。

## 明确不包含

不包含 SQLite Adapter、Event Store、Memory Store facade、网络传输、Vector/Graph Index、物理 Forget 或生产持久化能力声明。

## 验证边界

本 Crate 只包含纯 Rust 契约形态测试，不证明后端原子性、崩溃恢复、跨进程并发、序列化或持久化能力。


> 双语同步说明：本文件与 `docs/en/02-domain-model/phase-1-storage-trait-contract.md` 同一提交更新，语义保持一致。