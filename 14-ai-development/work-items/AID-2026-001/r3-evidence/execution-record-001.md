# R3 执行记录 001（协调方本地执行）

## 1. 执行基线

- 执行 commit：`ea467e4e82931bde587dfee04c733871d851c31a`
- 分支：`remediation/aid-2026-001-forget-contract-closure-2026-11-18`
- 执行者：协调方本地环境
- OS / Shell：Windows 11 / Git Bash
- Python：Python 3.13.14（CPython，标准库）
- 工作目录：仓库根目录
- 运行命令：`python -m unittest discover -s 14-ai-development/work-items/AID-2026-001/reference-model -p 'test_*.py' -v`
- 执行时间：协调方未提供时间戳，本记录不推定。
- 以下 stdout 和 EXIT 行按协调方回传材料原样收录。

## 2. 原始完整执行输出（原样）

```text
test_ack_is_not_erase_evidence (test_forget_model.ForgetReferenceModelTests.test_ack_is_not_erase_evidence) ... ok
test_backup_restore_must_apply_latest_fence_before_serving (test_forget_model.ForgetReferenceModelTests.test_backup_restore_must_apply_latest_fence_before_serving) ... ok
test_bounded_approved_exception_is_derived_projection_only (test_forget_model.ForgetReferenceModelTests.test_bounded_approved_exception_is_derived_projection_only) ... ok
test_cancel_after_suppression_cannot_restore_access (test_forget_model.ForgetReferenceModelTests.test_cancel_after_suppression_cannot_restore_access) ... ok
test_context_remove_does_not_change_canonical_lifecycle (test_forget_model.ForgetReferenceModelTests.test_context_remove_does_not_change_canonical_lifecycle) ... ok
test_denied_authorization_never_suppresses (test_forget_model.ForgetReferenceModelTests.test_denied_authorization_never_suppresses) ... ok
test_domain_completion_is_separate_from_governance (test_forget_model.ForgetReferenceModelTests.test_domain_completion_is_separate_from_governance) ... ok
test_idempotency_key_binds_canonical_request (test_forget_model.ForgetReferenceModelTests.test_idempotency_key_binds_canonical_request) ... ok
test_inventory_expansion_invalidates_prior_evaluation (test_forget_model.ForgetReferenceModelTests.test_inventory_expansion_invalidates_prior_evaluation) ... ok
test_notify_ack_can_only_satisfy_notify_action (test_forget_model.ForgetReferenceModelTests.test_notify_ack_can_only_satisfy_notify_action) ... ok
test_stale_lease_cannot_commit_checkpoint (test_forget_model.ForgetReferenceModelTests.test_stale_lease_cannot_commit_checkpoint) ... ok
test_suppression_linearizes_memory_and_fence_together (test_forget_model.ForgetReferenceModelTests.test_suppression_linearizes_memory_and_fence_together) ... ok
test_unknown_or_unsupported_cross_system_target_blocks_compliance (test_forget_model.ForgetReferenceModelTests.test_unknown_or_unsupported_cross_system_target_blocks_compliance) ... ok
test_unsupported_capability_cannot_claim_erasure (test_forget_model.ForgetReferenceModelTests.test_unsupported_capability_cannot_claim_erasure) ... ok
test_DFI_001 (test_r3_contract.DFI.test_DFI_001) ... ok
test_DFI_002 (test_r3_contract.DFI.test_DFI_002) ... ok
test_DFI_003 (test_r3_contract.DFI.test_DFI_003) ... ok
test_DFI_004 (test_r3_contract.DFI.test_DFI_004) ... ok
test_DFI_005 (test_r3_contract.DFI.test_DFI_005) ... ok
test_DFI_006 (test_r3_contract.DFI.test_DFI_006) ... ok
test_DFI_007 (test_r3_contract.DFI.test_DFI_007) ... ok
test_DFI_008 (test_r3_contract.DFI.test_DFI_008) ... ok
test_DFI_009 (test_r3_contract.DFI.test_DFI_009) ... ok
test_DFI_010 (test_r3_contract.DFI.test_DFI_010) ... ok
test_DFI_011 (test_r3_contract.DFI.test_DFI_011) ... ok
test_DFI_012 (test_r3_contract.DFI.test_DFI_012) ... ok
test_DFI_013 (test_r3_contract.DFI.test_DFI_013) ... ok
test_DFI_014 (test_r3_contract.DFI.test_DFI_014) ... ok
test_DFI_015 (test_r3_contract.DFI.test_DFI_015) ... ok
test_DFI_016 (test_r3_contract.DFI.test_DFI_016) ... ok
test_DFI_017 (test_r3_contract.DFI.test_DFI_017) ... ok
test_DFI_018 (test_r3_contract.DFI.test_DFI_018) ... ok
test_DFI_019 (test_r3_contract.DFI.test_DFI_019) ... ok
test_DFI_020 (test_r3_contract.DFI.test_DFI_020) ... ok
test_DFI_021 (test_r3_contract.DFI.test_DFI_021) ... ok
test_DFI_022 (test_r3_contract.DFI.test_DFI_022) ... ok
test_T01 (test_r3_contract.OwnerIU011.test_T01) ... ok
test_T02 (test_r3_contract.OwnerIU011.test_T02) ... ok
test_T03 (test_r3_contract.OwnerIU011.test_T03) ... ok
test_T04 (test_r3_contract.OwnerIU011.test_T04) ... ok
test_T05 (test_r3_contract.OwnerIU011.test_T05) ... ok
test_T06 (test_r3_contract.OwnerIU011.test_T06) ... ok
test_T07 (test_r3_contract.OwnerIU011.test_T07) ... ok
test_T08 (test_r3_contract.OwnerIU011.test_T08) ... ok
test_T09 (test_r3_contract.OwnerIU011.test_T09) ... ok
test_T10 (test_r3_contract.OwnerIU011.test_T10) ... ok
test_T11 (test_r3_contract.OwnerIU011.test_T11) ... ok
test_T12 (test_r3_contract.OwnerIU011.test_T12) ... ok
test_T13 (test_r3_contract.OwnerIU011.test_T13) ... ok
test_T14 (test_r3_contract.OwnerIU011.test_T14) ... ok
test_T15 (test_r3_contract.OwnerIU011.test_T15) ... ok
test_T16 (test_r3_contract.OwnerIU011.test_T16) ... ok
test_STOR_01_concurrent_suppression_race (test_r3_contract.StorageFaults.test_STOR_01_concurrent_suppression_race) ... ok
test_STOR_02_replica_lag_failover (test_r3_contract.StorageFaults.test_STOR_02_replica_lag_failover) ... ok
test_STOR_03_stale_worker_old_lease (test_r3_contract.StorageFaults.test_STOR_03_stale_worker_old_lease) ... ok
test_STOR_04_duplicate_events_outbox_replay (test_r3_contract.StorageFaults.test_STOR_04_duplicate_events_outbox_replay) ... ok
test_STOR_05_timeout_retry_reconciliation (test_r3_contract.StorageFaults.test_STOR_05_timeout_retry_reconciliation) ... ok
test_STOR_06_restore_isolation_reconciliation (test_r3_contract.StorageFaults.test_STOR_06_restore_isolation_reconciliation) ... ok
test_STOR_07_missing_manifest_unknown (test_r3_contract.StorageFaults.test_STOR_07_missing_manifest_unknown) ... ok

----------------------------------------------------------------------
Ran 59 tests in 0.002s

OK
EXIT=0
```

## 3. 汇总

| 项目 | 实际结果 |
|---|---:|
| 发现并执行 | 59 |
| 既有 ForgetReferenceModelTests | 14 |
| DFI-001…022 | 22 |
| I-U011-T01…T16 | 16 |
| STOR-01…07 | 7 |
| PASS / FAIL / ERROR | 59 / 0 / 0 |
| SKIPPED | 0（输出未报告 skip） |
| unittest 摘要 | Ran 59 tests in 0.002s / OK |
| EXIT | 0 |

该次运行由协调方本地执行。本会话未重新运行；归档不将其冒充为本会话执行。

## 4. 逐项结果表

PASS 仅表示相应测试方法在该次本地运行中输出 ok，不表示生产义务已实现或证明。

| Test ID | 预期断言类别 | 实际输出 | 状态 | 输出定位 | 备注 |
|---|---|---|---|---|---|
| BASE-01 | `test_ack_is_not_erase_evidence` | ok | PASS | 原始输出 1 | 既有测试 |
| BASE-02 | `test_backup_restore_must_apply_latest_fence_before_serving` | ok | PASS | 原始输出 2 | 既有测试 |
| BASE-03 | `test_bounded_approved_exception_is_derived_projection_only` | ok | PASS | 原始输出 3 | 既有测试 |
| BASE-04 | `test_cancel_after_suppression_cannot_restore_access` | ok | PASS | 原始输出 4 | 既有测试 |
| BASE-05 | `test_context_remove_does_not_change_canonical_lifecycle` | ok | PASS | 原始输出 5 | 既有测试 |
| BASE-06 | `test_denied_authorization_never_suppresses` | ok | PASS | 原始输出 6 | 既有测试 |
| BASE-07 | `test_domain_completion_is_separate_from_governance` | ok | PASS | 原始输出 7 | 既有测试 |
| BASE-08 | `test_idempotency_key_binds_canonical_request` | ok | PASS | 原始输出 8 | 既有测试 |
| BASE-09 | `test_inventory_expansion_invalidates_prior_evaluation` | ok | PASS | 原始输出 9 | 既有测试 |
| BASE-10 | `test_notify_ack_can_only_satisfy_notify_action` | ok | PASS | 原始输出 10 | 既有测试 |
| BASE-11 | `test_stale_lease_cannot_commit_checkpoint` | ok | PASS | 原始输出 11 | 既有测试 |
| BASE-12 | `test_suppression_linearizes_memory_and_fence_together` | ok | PASS | 原始输出 12 | 既有测试 |
| BASE-13 | `test_unknown_or_unsupported_cross_system_target_blocks_compliance` | ok | PASS | 原始输出 13 | 既有测试 |
| BASE-14 | `test_unsupported_capability_cannot_claim_erasure` | ok | PASS | 原始输出 14 | 既有测试 |
| DFI-001 | 对应 DFI 源场景 | ok | PASS | test_DFI_001 | 参考模型断言 |
| DFI-002 | 对应 DFI 源场景 | ok | PASS | test_DFI_002 | 参考模型断言 |
| DFI-003 | 对应 DFI 源场景 | ok | PASS | test_DFI_003 | 参考模型断言 |
| DFI-004 | 对应 DFI 源场景 | ok | PASS | test_DFI_004 | 参考模型断言 |
| DFI-005 | 对应 DFI 源场景 | ok | PASS | test_DFI_005 | 参考模型断言 |
| DFI-006 | 对应 DFI 源场景 | ok | PASS | test_DFI_006 | 参考模型断言 |
| DFI-007 | 对应 DFI 源场景 | ok | PASS | test_DFI_007 | 参考模型断言 |
| DFI-008 | 对应 DFI 源场景 | ok | PASS | test_DFI_008 | 参考模型断言 |
| DFI-009 | 对应 DFI 源场景 | ok | PASS | test_DFI_009 | 参考模型断言 |
| DFI-010 | 对应 DFI 源场景 | ok | PASS | test_DFI_010 | 参考模型断言 |
| DFI-011 | 对应 DFI 源场景 | ok | PASS | test_DFI_011 | 参考模型断言 |
| DFI-012 | 对应 DFI 源场景 | ok | PASS | test_DFI_012 | 参考模型断言 |
| DFI-013 | 对应 DFI 源场景 | ok | PASS | test_DFI_013 | 参考模型断言 |
| DFI-014 | 对应 DFI 源场景 | ok | PASS | test_DFI_014 | 参考模型断言 |
| DFI-015 | 对应 DFI 源场景 | ok | PASS | test_DFI_015 | 参考模型断言 |
| DFI-016 | 对应 DFI 源场景 | ok | PASS | test_DFI_016 | 参考模型断言 |
| DFI-017 | 对应 DFI 源场景 | ok | PASS | test_DFI_017 | 参考模型断言 |
| DFI-018 | 对应 DFI 源场景 | ok | PASS | test_DFI_018 | 参考模型断言 |
| DFI-019 | 对应 DFI 源场景 | ok | PASS | test_DFI_019 | 参考模型断言 |
| DFI-020 | 对应 DFI 源场景 | ok | PASS | test_DFI_020 | 参考模型断言 |
| DFI-021 | 对应 DFI 源场景 | ok | PASS | test_DFI_021 | 参考模型断言 |
| DFI-022 | 对应 DFI 源场景 | ok | PASS | test_DFI_022 | 参考模型断言 |
| I-U011-T01 | 对应 U-011 源场景 | ok | PASS | test_T01 | T15 断言仅检查 required_targets 为空；PASS 不证明完整 D-completion 语义 |
| I-U011-T02 | 对应 U-011 源场景 | ok | PASS | test_T02 | T15 断言仅检查 required_targets 为空；PASS 不证明完整 D-completion 语义 |
| I-U011-T03 | 对应 U-011 源场景 | ok | PASS | test_T03 | T15 断言仅检查 required_targets 为空；PASS 不证明完整 D-completion 语义 |
| I-U011-T04 | 对应 U-011 源场景 | ok | PASS | test_T04 | T15 断言仅检查 required_targets 为空；PASS 不证明完整 D-completion 语义 |
| I-U011-T05 | 对应 U-011 源场景 | ok | PASS | test_T05 | T15 断言仅检查 required_targets 为空；PASS 不证明完整 D-completion 语义 |
| I-U011-T06 | 对应 U-011 源场景 | ok | PASS | test_T06 | T15 断言仅检查 required_targets 为空；PASS 不证明完整 D-completion 语义 |
| I-U011-T07 | 对应 U-011 源场景 | ok | PASS | test_T07 | T15 断言仅检查 required_targets 为空；PASS 不证明完整 D-completion 语义 |
| I-U011-T08 | 对应 U-011 源场景 | ok | PASS | test_T08 | T15 断言仅检查 required_targets 为空；PASS 不证明完整 D-completion 语义 |
| I-U011-T09 | 对应 U-011 源场景 | ok | PASS | test_T09 | T15 断言仅检查 required_targets 为空；PASS 不证明完整 D-completion 语义 |
| I-U011-T10 | 对应 U-011 源场景 | ok | PASS | test_T10 | T15 断言仅检查 required_targets 为空；PASS 不证明完整 D-completion 语义 |
| I-U011-T11 | 对应 U-011 源场景 | ok | PASS | test_T11 | T15 断言仅检查 required_targets 为空；PASS 不证明完整 D-completion 语义 |
| I-U011-T12 | 对应 U-011 源场景 | ok | PASS | test_T12 | T15 断言仅检查 required_targets 为空；PASS 不证明完整 D-completion 语义 |
| I-U011-T13 | 对应 U-011 源场景 | ok | PASS | test_T13 | T15 断言仅检查 required_targets 为空；PASS 不证明完整 D-completion 语义 |
| I-U011-T14 | 对应 U-011 源场景 | ok | PASS | test_T14 | T15 断言仅检查 required_targets 为空；PASS 不证明完整 D-completion 语义 |
| I-U011-T15 | 对应 U-011 源场景 | ok | PASS | test_T15 | T15 断言仅检查 required_targets 为空；PASS 不证明完整 D-completion 语义 |
| I-U011-T16 | 对应 U-011 源场景 | ok | PASS | test_T16 | T15 断言仅检查 required_targets 为空；PASS 不证明完整 D-completion 语义 |
| STOR-01 | 对应存储故障模型场景 | ok | PASS | test_STOR_01 | 内存模型，不是真实存储故障 |
| STOR-02 | 对应存储故障模型场景 | ok | PASS | test_STOR_02 | 内存模型，不是真实存储故障 |
| STOR-03 | 对应存储故障模型场景 | ok | PASS | test_STOR_03 | 内存模型，不是真实存储故障 |
| STOR-04 | 对应存储故障模型场景 | ok | PASS | test_STOR_04 | 内存模型，不是真实存储故障 |
| STOR-05 | 对应存储故障模型场景 | ok | PASS | test_STOR_05 | 内存模型，不是真实存储故障 |
| STOR-06 | 对应存储故障模型场景 | ok | PASS | test_STOR_06 | 内存模型，不是真实存储故障 |
| STOR-07 | 对应存储故障模型场景 | ok | PASS | test_STOR_07 | 内存模型，不是真实存储故障 |

## 5. 证据层级声明

**本证据是契约级参考模型一致性证据（in-memory reference model conformance），不是生产运行时持久化证明。**

59/59 PASS 仅说明本次 Python 3.13.14 执行中的内存参考模型断言通过。不得推断 v2.1/v2.2 生产实现完成、生产激活、Owner 批准或合规闭环成立。

下列生产级项目均为 **NOT IMPLEMENTED / NOT RUN**，除非未来提供真实实现载体及独立回执：

1. 真实数据库 Transaction/WAL 落盘、提交回执、崩溃恢复与事务原子性。
2. 六项原子提交元组在真实进程/主机崩溃注入下的全有或全无验证。
3. 多进程/多节点真实并发抑制竞态与线性化测试（STOR-01 仅顺序内存模型调用）。
4. 权威副本/分片完整清单及逐副本擦除、去标识化回执。
5. 真实副本复制滞后测量、故障切换、旧副本隔离与恢复高水位验证。
6. 跨进程、节点、重启、灾难恢复后的 Fence 持久单调性证据。
7. 分布式租约服务与真实陈旧 Worker 写入拦截，包括网络分区/时钟边界。
8. 数据库 Outbox 与消息 Broker 的事务联动、投递、重复消费及重放回执。
9. 外部副作用超时后的真实查询、ReconciliationCompleted 持久化及安全重试。
10. 经认证的完整备份/快照/归档副本清单及覆盖证明。
11. 备份介质擦除、密钥销毁、到期策略及可验证回执。
12. 真实 Restore 演练、隔离环境、最新 Fence 与后续 Forget 事件完整重放/对账回执。
13. 生产服务层在 Restore reconciliation 完成前拒绝流量的端到端证明。
14. 生产连接器/数据目录中的 required-target 发现、清单封存、修订和 UNKNOWN 传播证据。
15. 各目标系统真实删除/擦除执行、独立验证、失败重试与审计回执。
16. 授权基础设施端到端验证：Issuer 信任根、签名密钥管理、Audience/请求绑定、撤权传播、PermissionEpoch 权威源、Nonce 防重放、委托撤销。
17. 不可抵赖审计、可信时间戳、证据完整性保护与保留策略。
18. 多区域切换、网络分区、灾难恢复及 Forget 状态不复活验证。

## 6. 复现指引

在仓库根目录检出 `ea467e4e82931bde587dfee04c733871d851c31a`，使用 CPython 3.13.14（Runbook 要求 3.10+），执行：

```sh
python --version
python -m unittest discover -s 14-ai-development/work-items/AID-2026-001/reference-model -p 'test_*.py' -v
```

协调方回传的本次结果为 59 tests / 0.002s / OK / EXIT=0。复现如有不同，必须按新实际输出记录，不得以本记录覆盖。

## 7. 治理状态

- 仅归档协调方提供的执行材料；未修改测试代码或契约文档。
- v2.2 仍为 **PROPOSED**。
- 测试 PASS ≠ 实现完成 ≠ 生产激活 ≠ Owner 批准。
- 本记录不替代 U-044 非实现者独立复核。
- `AID-2026-001` 仍为 **BLOCKED_PENDING_R3_EVIDENCE**，直至证据审查及后续治理门槛完成。
