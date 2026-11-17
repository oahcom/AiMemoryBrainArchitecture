# ABR-INTEGRATION-006 — Forget 模型审查整改与双操作扩展

- Review ID: ABR-INTEGRATION-006
- 关联模型审查：ABR-INTEGRATION-005（PR #93 分支内的后续模型复核）
- 当前范围：单操作跨 Owner 模型 M-01/M-02 修订；M-03 双操作有限扩展；M-04/M-05 保留。
- CI：run [44141001299](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44141001299)，SUCCESS，测试提交 `33db9554bb2b9a6aecdfabf16250c98dc88e272b`。

## 1. 结果摘要

| 项目 | 当前结果 | 判定 |
|---|---|---|
| 单操作模型 | 28,383 state/depth pairs，最大深度 14，13 个 weakened-guard mutants，15 项 unittest | BOUNDED PASS |
| 双操作模型 | 2,425 state/depth pairs，最大深度 12，5 个 mutants，7 项 unittest | BOUNDED PASS |
| 合并 CI | 两个模型脚本 + 两套 unittest 全部通过 | <badge>SUCCESS</badge> |
| M-01 | `global_complete` 改为 `core_barrier_ready`，明确不是 I GlobalForget Completed | 模型范围内 CLOSED |
| M-02 | 加入外部 durable no-publication proof 输入；无证明不能 terminalize；旧 Worker 不能复活 | 模型范围内 CLOSED；Owner 合同 OPEN |
| M-03 | 新增两个重叠操作、共享 target、独立 generation/barrier/receipt、late target reopen | 部分覆盖；只证明双操作有限模型 |
| M-04 | 真实 durable participant / prepared transaction / crash cut points | OPEN |
| M-05 | Safety 与 liveness/fairness 分离、progress assumptions | OPEN |

## 2. M-01 — 防止模型越权声称 Global Forget Completed

单操作模型将状态和动作改为 `core_barrier_ready` / `mark_core_barrier_ready`，只表示该有限模型中的 D/I core barrier 条件已满足。它不表示：
- I ProducerDomainInventoryEpoch 已封存；
- E/F/G/H 全部强制目标已确认；
- External recipient / Backup / Restore / Physical Erasure 已完成；
- I typed evidence vector 已满足；
- I `Completed` / `CompletedWithPolicyException` 已形成。

因此 M-01 的命名和范围误导在当前模型内关闭；I Global Forget Completed 仍未建模、未证明。

## 3. M-02 — Registered but never started 的外部终态证明

新增 `record_no_publication_proof` 抽象输入。只有在 Fence 已安装、WorkItem 已登记但未执行、无 lease、无 I participant、无可见 Artifact 时，模型才接受该外部 D/E/Storage durable proof。之后才允许 terminalize 和 barrier closure。

模型同时加入：
- `cancel_without_proof` mutant：无证明直接 terminalize，产生反例；
- `stale_worker_after_cancel` mutant：取消证明后旧 Worker 仍启动，产生反例；
- 对应不变量与回归测试。

**重要：** 这是外部权威证据输入的抽象，不是本会话发明或批准新的 Cancel API。E Cancelled/Rejected 仍是 CANDIDATE；E→D terminal acknowledgement schema/reconciliation、D barrier receipt、Storage no-publish participant 和 late-worker fencing 的精确 Owner 合同仍 OPEN。D/E/Storage 必须先给出精确合同，模型通过不等于 Owner 接受。

## 4. M-03 — 双操作重叠模型

新增独立模型 `overlapping_forget_model.py`，以两个有交集的 Forget 操作为最小模型：
- Operation 1 targets：`{a, shared}`
- Operation 2 targets：`{shared, b}`
- 两者从同一 D-local durable generation counter 分配不同 operation generation；
- 各自拥有独立 terminal evidence namespace、barrier 和 receipt generation；
- 共享 target 必须分别在各自 operation identity 下取得 terminal evidence；
- late target discovery 生成受影响 operation 的 successor generation，只 reopen 该 operation，并使旧 receipt 不再代表当前 generation。

2,425 state/depth pairs 内未发现不变量违反。5 个削弱约束变体产生最短反例：
1. 重用 generation；
2. 一个操作关闭另一个操作的 barrier；
3. 共享 target evidence 跨 operation 复用；
4. late target 不 reopen 原 barrier；
5. 一个操作的 receipt 错误关闭另一个操作的 barrier。

这部分只把 M-03 从“完全未覆盖”推进到“两个操作的有限组合性质有证据”。它不证明任意数量的重叠 Forget、任意 target DAG、多个并发 Producer/Worker、跨 Scope 或物理恢复。

## 5. 当前可复现 CI

[GitHub Actions run 44141001299](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44141001299) 在提交 `33db9554...` 执行：
- 单操作模型：28,383 state/depth pairs，13 mutants；
- 单操作 unittest：15 tests，PASS；
- 双操作模型：2,425 state/depth pairs，5 mutants；
- 双操作 unittest：7 tests，PASS。

历史失败 run `44139591931` 是模型新增转移后旧 expected count 未更新导致；后续 `44140051181` 和当前合并 run `44141001299` 均成功。历史失败不删除、不隐藏。

## 6. 仍然禁止的推断

- 双操作有限模型不是无界并发证明。
- Model generation counter 不是对所有 Owner namespace 的统一数字；本模型只表达 D-local generation 的单调性。
- 双操作 barrier closure 不等于 I Global Forget Completed。
- Abstract no-publication proof 不等于真实 D terminal receipt、Storage durable participant 或 late-worker fencing 已实现。
- CI PASS 不等于真实 DB/WAL/MVCC/2PC、HA/PITR、split-brain、crash/restart 或物理擦除已通过。
- M-04/M-05、JF-10、Global Forget typed completion 仍 OPEN / NOT PROVEN。

## 7. 下一步

1. D/E/Storage：定义 pre-execution Cancelled/Rejected → durable D terminal receipt 的 exact schema、authority、same-WorkItemId idempotency、participant closure 和 stale-worker rejection。
2. I：定义多个重叠 Forget 的 inventory epoch、target set、reopen 与 Global completion evidence join。
3. Storage/D/I：将真实 prepare/commit/visibility/receipt/authority closure 的每个 durable boundary 纳入 crash-cut matrix。
4. A：在 Owner 合同落地后扩展多操作模型至更多 target、late lineage 和并发事件；M-05 单独建模。

本报告为有限模型研究交付，不是 Owner 签字，不关闭 Issue #43 Gate，不授权生产实现或部署。
