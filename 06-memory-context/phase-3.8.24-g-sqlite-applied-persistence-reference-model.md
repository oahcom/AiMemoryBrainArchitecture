# Phase 3.8.24 — G SQLite Applied Persistence Reference Model
# Phase 3.8.24 — G SQLite Applied Persistence 参考模型

- Owner domain: G — ContextVersion, Delivery, Applied State and Reconciliation.
- Mode: delegated G-role reference implementation; **not a production implementation or independent human G Owner signature**.
- Normative contract: Phase 3.8.22 Blob \`bd297873bc1e593280484a43cb44b56058d9c4ff\`.
- Source file: \`06-memory-context/reference_model/test_g_applied_persistence.py\`.
- Test Blob: \`84b54693311d2d09430bba731bcc0a702abf17cd\`.
- Workflow Blob: \`045f7b76783d0aa5d6b7cd0dc9bec42a5f6140be\`.
- Exact commit: \`a244cb5e7d80e000300150345b1417e9edc57cf6\`.
- CI: [G Applied Persistence Reference Model run 44182845249](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44182845249) — **SUCCESS, 14/14 tests**.
- Status: **BOUNDED SQLITE REFERENCE MODEL PASS; PRODUCTION G APPLIED PERSISTENCE NOT IMPLEMENTED / NOT VERIFIED**.

## 1. Purpose and evidence ceiling

G Phase 3.8.22 specifies durable Applied identity, immutable evidence revisions, idempotency, atomic local commit, current-use invalidation and restore fencing. Its G-AP-P01..P18 conformance obligations remain SPECIFIED / NOT RUN at the production-system level.

This addendum supplies a bounded SQLite-backed reference model to make part of the contract executable. It is not a Brain runtime, production G repository, PostgreSQL implementation, distributed transaction, multi-replica linearizability proof, backup/restore implementation or Owner approval.

## 2. Modeled persistence shape

The reference model uses:
- a unique primary key on \`g_applied_identity_key\`;
- immutable \`evidence_revision\` and \`evidence_set_digest\`;
- a unique G Applied receipt and ledger sequence;
- one local transaction to commit the Applied ledger row, outbox event and ledger high-water;
- a unique outbox event per Applied identity;
- append-only current-use invalidation events while preserving the historical Applied row;
- a restore fence that keeps serving disabled when the snapshot epoch/high-water is stale or any required owner-currentness input is absent.

The test model requires C, H, COC, I, D and Storage proof statuses to be exactly VALID before writing a Full Applied row. It additionally requires C Outcome=HANDOFF_ACCEPTED and SideEffectStatus=PROVEN_OCCURRED. UNKNOWN, IN_DOUBT, HANDOFF_REJECTED, NOT_INVOKED, missing or non-VALID proof rejects the write.

## 3. Executed bounded cases

The exact workflow ran 12 tests:
1. Same identity + same revision/digest returns the original receipt.
2. Same identity + changed EvidenceSetDigest conflicts.
3. Same identity + changed evidence revision conflicts.
4. Missing or UNKNOWN C/H/COC/I/D/Storage proof blocks Full Applied.
5. Crash before transaction commit leaves no ledger, outbox or high-water partial write.
6. Lost ACK after commit; same identity retry returns the original receipt.
7. Ledger row, receipt, outbox and high-water commit atomically in the modeled transaction.
8. Six concurrent duplicate submissions serialize to one Applied fact and one outbox event.
9. Later Forget invalidates current-use while preserving historical Applied.
10. Stale restore epoch/high-water keeps serving fenced.
11. Missing owner-currentness proof keeps restore fenced.
12. Exact restore epoch/high-water and all owner-currentness inputs permit the modeled serving flag to be re-enabled.

13. C Outcome UNKNOWN/IN_DOUBT with POSSIBLE_OR_UNKNOWN side effect blocks Full Applied.
14. C Outcome HANDOFF_REJECTED or NOT_INVOKED blocks Full Applied.

Result: **14/14 PASS** on the exact commit above.

## 4. Limitations — what this does not prove

- SQLite WAL/FULL in a single local file is not the selected production Storage topology and does not prove PostgreSQL Serializable transaction behavior.
- The model does not implement a generated G Applied schema/SDK or production canonicalization profile.
- Proof statuses are supplied as test values; there are no live C/H/COC/I/D/Storage authority resolvers or signatures.
- The restore high-water inputs are test arguments, not signed external checkpoints or actual owner-ledger continuity proofs.
- The concurrent test exercises six local SQLite connections in one process; it is not a multi-process, multi-host or multi-replica linearizability test.
- No power-loss, filesystem corruption, backup snapshot, point-in-time restore, failover or production operator runbook was exercised.
- It does not close the complete G-AP-P01..P18 matrix; several cases remain unmodeled or only partially represented.
- It does not prove C provider exactly-once side effects, H durable replay, COC quorum, I sequencer, D barrier release or Storage same-GID/Prepared-XID integration.

## 5. Required next production work

1. G Owner must approve the stable Applied identity and generated machine-readable schema/SDK.
2. Select/confirm the actual persistence engine under the approved Storage L4 profile and implement unique constraints and transaction semantics there.
3. Bind the G transaction to exact authenticated C/H/COC/I/D/Storage records; no caller-supplied VALID booleans.
4. Add production-engine crash/restart and multi-replica duplicate tests, stale backup restore, external high-water continuity, failover and current-use revalidation.
5. Complete G-AP-P01..P18 with exact fixtures, expected/actual outputs and reproducible artifacts.
6. Obtain independent G/Storage/COC/C/H/I/D review against exact final commits.

## 6. Final disposition

- SQLite bounded reference model: **PASS 14/14**.
- G durable Applied algorithm: **REFERENCE MODEL ONLY**.
- Production G schema/SDK/unique index/database adapter: **NOT IMPLEMENTED / NOT VERIFIED**.
- Production crash/restart/restore/multi-replica proof: **OPEN**.
- Full Applied / global C/G/H freeze / production activation: **NOT PROVEN / NOT AUTHORIZED**.

---

## 7. 中文完整结论

G Phase 3.8.22 已规定 Durable Applied Identity、不可变 Evidence Revision、幂等、原子本地提交、Current-use Invalidation 和 Restore Fencing，但生产级 G-AP-P01..P18 仍为 SPECIFIED / NOT RUN。

本补充增加 SQLite-backed bounded reference model，使部分契约可执行。它不是 Brain Runtime、生产 G Repository、PostgreSQL 实现、分布式事务、多副本 Linearizability Proof、Backup/Restore 实现或 Owner 批准。

模型包含 Applied Identity 唯一主键、不可变 Evidence Revision/Digest、唯一 Receipt/Ledger Sequence、同一事务内 Ledger/Outbox/High-water 原子提交、历史 Applied 保留与 Current-use Invalidation、Stale Restore Fence。C/H/COC/I/D/Storage 六类证明必须全部为 VALID 才允许写入 Full Applied；缺失或 UNKNOWN 必须拒绝。

精确 CI 执行 12 项：
- 同身份同 Digest 幂等返回原 Receipt；
- 同身份不同 Digest/Revision 冲突；
- 缺失/UNKNOWN Owner Proof 拒绝；
- Commit 前 Crash 无部分 Ledger/Outbox/High-water；
- Commit 后 Lost ACK 重试返回同 Receipt；
- Ledger/Receipt/Outbox/High-water 原子；
- 六个本地 SQLite Connection 并发重复只形成一条事实；
- Forget 后保留历史 Applied、失效 Current-use；
- Stale Restore Epoch/High-water 阻止 Serving；
- 缺失 Owner Currentness Proof 阻止 Restore；
- 完整 Currentness 可恢复模型 Serving Flag。

结果：**14/14 PASS**。

但 SQLite 单文件不是生产 Storage 拓扑，也不证明 PostgreSQL Serializable；Proof 是测试输入而非真实权威签名；Restore High-water 是测试参数而非外部签名 Checkpoint；并发仅为单进程六个 SQLite Connection，不是多进程/多主机/多副本；未测试断电、文件系统损坏、备份快照、PITR、Failover 或生产运维。该模型也没有关闭完整 G-AP-P01..P18。

最终状态：SQLite 参考模型 **PASS 14/14**；G Durable Applied 仍是 **REFERENCE MODEL ONLY**；生产 Schema/SDK/Unique Index/DB Adapter **NOT IMPLEMENTED / NOT VERIFIED**；生产 Crash/Restore/Multi-replica 证明 **OPEN**；Full Applied/全局冻结/生产激活 **NOT PROVEN / NOT AUTHORIZED**。


## 8. Current test-head reconciliation — 2026-11-18

The original §3 test count and Blob are historical. The G Owner branch subsequently expanded the model from 14 to 17 tests.

- Current G Owner branch HEAD observed: `2c53a9d872ad4d57d99bd24a860ca695b9e3a661`.
- Exact code/test commit: `470d4c1934999263bfb8a4822b13c2ff854c3dfd`.
- Current test file Blob: `e77d2375506e423bf53d8341fe9aecf2719d0609`.
- Workflow Blob: `045f7b76783d0aa5d6b7cd0dc9bec42a5f6140be`.
- Exact CI run [#44188852578](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44188852578): SUCCESS; job log explicitly reports `Ran 17 tests`, `OK`.
- The two additional cases beyond the earlier 14-test snapshot reject restore snapshots whose epoch or high-water is ahead of the trusted external anchor.
- A further case proves that while the restore fence is active, a new Full Applied write is rejected and the pre-existing ledger/outbox remain unchanged.

This is a bounded local SQLite reference-model result only. It does not prove PostgreSQL/Serializable behavior, multi-process or multi-host linearizability, signed external anchor authenticity, real C/H/COC/I/D/Storage proof resolution, power-loss recovery, production backup/PITR/failover or G Owner acceptance. G-AP-P01..P18 remain SPECIFIED / NOT RUN for production.

### Updated disposition

- SQLite reference model: **PASS 17/17** on exact code commit `470d4c1...`.
- Production G schema/SDK/unique index/database adapter: **NOT IMPLEMENTED / NOT VERIFIED**.
- Production crash/restart/restore/multi-replica proof: **OPEN**.
- Full Applied / global C/G/H freeze / production activation: **NOT PROVEN / NOT AUTHORIZED**.

---

## 9. 中文：当前测试 Head 对账 — 2026-11-18

原 §3 的测试数量和 Blob 已是历史快照。G Owner 分支随后将模型从 14 项扩展至 17 项。

- 当前 G Owner 分支 HEAD：`2c53a9d872ad4d57d99bd24a860ca695b9e3a661`。
- 精确代码/测试提交：`470d4c1934999263bfb8a4822b13c2ff854c3dfd`。
- 当前测试文件 Blob：`e77d2375506e423bf53d8341fe9aecf2719d0609`。
- Workflow Blob：`045f7b76783d0aa5d6b7cd0dc9bec42a5f6140be`。
- 精确 CI Run [#44188852578](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44188852578)：SUCCESS；Job 日志明确为 `Ran 17 tests`、`OK`。
- 相较早期 14 项快照，新增两项测试：当 Restore Snapshot 的 Epoch 或 High-water 超前于 Trusted External Anchor 时必须保持 Fenced。
- 另新增一项测试：Restore Fence 激活期间必须拒绝新的 Full Applied 写入，并保持既有 Ledger/Outbox 不变。

该结果仍仅是本地 SQLite 有界参考模型。它不证明 PostgreSQL/Serializable 行为、多进程/多主机 Linearizability、签名外部 Anchor 真实性、真实 C/H/COC/I/D/Storage 证明解析、断电恢复、生产 Backup/PITR/Failover 或 G Owner 验收。生产级 G-AP-P01..P18 仍为 SPECIFIED / NOT RUN。

### 更新后的结论

- SQLite 参考模型：精确代码提交 `470d4c1...` 上 **PASS 17/17**。
- 生产 G Schema/SDK/Unique Index/Database Adapter：**NOT IMPLEMENTED / NOT VERIFIED**。
- 生产 Crash/Restart/Restore/Multi-replica 证明：**OPEN**。
- Full Applied/全局 C/G/H Freeze/生产激活：**NOT PROVEN / NOT AUTHORIZED**。
