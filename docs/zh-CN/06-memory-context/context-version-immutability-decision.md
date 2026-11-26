# ContextVersion 不可变性决议

- 授权人：user-authorized operator (delegated by account owner)
- 决策日期：2026-11-26
- 决策状态：方向已记录；G 与 A 的精确版本验收待完成
- 规范源：[context-versioning.md](../../../06-memory-context/context-versioning.md)
- 关联 Issue：#1144、#1151

## 决议

已提交的 ContextVersion 是不可变历史聚合。其身份、序号、父版本、Snapshot 引用/哈希/配置、精确提交的 ContextEntryVersion 集合、来源/Provenance 引用、Scope 和提交元数据均不得重写。已提交的 ContextEntryVersion 及其内容在该 Entry Revision 下不可变。当前 Head 指针只能与新 ChangeSet 的接受、不可变回执及幂等结果在同一原子提交中推进。

ContextChangeSet 是不可变变更请求。修改其 Payload 必须创建新的 ChangeSet 身份。常规合法变更路径只有：针对精确 Base Version 构造 ChangeSet；验证 Scope、授权和当前 Head；在可信提交边界计算并验证结果 Snapshot Commitment；原子持久化后继 ContextVersion、Entry Revision、Commit Receipt/Idempotency Result，并推进 Head。过期 Base 必须拒绝；Rebase 必须创建新的 ChangeSet。相同幂等身份和 Digest 的重试返回原结果；相同身份但 Digest 不同属于冲突。

修正、重排、替换、成员移除、失效、Supersession、Rollback 和 Forget 都必须创建后继 ContextVersion，绝不原地编辑已提交版本。Forget/撤销会使受影响历史版本对当前使用不可服务，但不会使其变为可变对象。物理 Payload 擦除是独立的 I 治理 Retention 操作：只有在明确授权并留存证据后才可移除 Payload，同时保留不可重建的 Tombstone/Audit Proof。不可变不意味着必须永久保留依法应擦除的明文。

## 违规定义

观察到以下任一情况即为违规：(a) 相同 ContextVersion ID/Sequence 对应不同的已提交字节或元数据；(b) 同一 ContextEntryVersion Revision 下的内容发生变化；(c) Head 在没有一个已接受 ChangeSet 及对应 Commit/Idempotency Receipt 的情况下推进；(d) 接受了过期 Base；(e) 在没有 I 授权擦除及 Tombstone 证据时原地更新/删除已提交记录；或 (f) 接受了不匹配的 Snapshot Commitment。

## #1144 / #1151 证据处置

#1144 保持 OPEN，因为尚无证据证明 Durable ContextVersion History、Head、ChangeSet 和 Idempotency State 能在进程重启后保留。本决议定义不可变语义，但不实施也不证明持久化。

在已测量的 main 源码中，#1151 所述“缺少重新计算”的缺陷未复现：commit_change_set 会对 staged 调用 snapshot_hash 并拒绝不匹配值；snapshot_hash 按 Entry ID 排序并序列化完整 Entry。当前参考实现使用 FNV-1a 64-bit，不能提供密码学抗碰撞能力。这是独立的 Digest 强度问题，不是缺少重新计算的证据。#1151 保持 OPEN，等待有责任 Owner 作出处理；本文件不关闭该 Issue。

## Reviewer 可核验判据

- CV-I1 PASS 当且仅当已提交版本身份及所有已提交字段/Entry 不可原地更改；否则 FAIL。
- CV-I2 PASS 当且仅当每次语义变更都通过已接受 ChangeSet 创建新的后继版本；否则 FAIL。
- CV-I3 PASS 当且仅当 Head 推进与后继版本及 Durable Commit/Idempotency Receipt 原子完成；否则 FAIL。
- CV-I4 PASS 当且仅当过期 Base 和复用身份但变更 Payload 均被拒绝；否则 FAIL。
- CV-I5 PASS 当且仅当 I 授权擦除是独立留证的 Purge/Tombstone，而不是静默版本变更；否则 FAIL。
- CV-I6 PASS 当且仅当 #1151 的缺少重新计算主张被记录为未复现，且 FNV-1a 强度限制被单独区分；否则 FAIL。

仍未闭合：#1144 的持久化/恢复验收、精确 Canonical Serialization 与 Digest 强度决策、G Owner 和 A 治理验收、Runtime Conformance。
