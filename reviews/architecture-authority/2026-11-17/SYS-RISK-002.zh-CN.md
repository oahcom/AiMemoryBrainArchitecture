# 全系统架构风险登记册 — SYS-RISK-002

- 权威角色：A — 首席系统架构权威
- 版本：1.0.0（候选集成基线）
- 日期：2026-11-17
- Main 基线：`b372b62c640a2b656e54b6db62a4ee67d7d8c001`
- A 审查分支：`review/session-4-a-final-architecture-authority-2026-11-17`
- 来源评估：R PR #50；X PR #49；F/D/P PR #46
- 决策状态：架构冻结 DEFERRED；仅允许有边界的准备工作。

## 证据精确绑定

| 来源 | 分支 | Commit | 报告 Blob |
|---|---|---|---|
| R 英文 | review/session-1-system-wide-risk-2026-11-17 | 8542d608ccfe6747c5f6171a2a38d325f10a628c | 4067005a65fe528aa7d5fc43ff5be79eb0adaa53 |
| R 中文 | 同上 | 同上 | 5fcc55636619d1df373f4caa0afa7db869e4fb70 |
| X 英文 | assessment/x-architecture-complexity-2026-11-17 | 131f91743bd506517ee354d58c277501ca447929 | c509120644d6f7c7223decf3f9f0ee33b0548bb7 |
| X 中文 | 同上 | 同上 | 981a376ddf283ace1e891795c813b17ac4aa3d8b |
| F/D/P 英文 | review/session-3-engineering-planning-2026-11-17 | 8b9ff8efa92a88dacc8f97b5faba5918fe5d2edc | 081610b1734ec08dc7c35c75fae1cae3ca713be4 |
| F/D/P 中文 | 同上 | 同上 | 834dc39998342dc2f292fe1dfed411768b3ed156 |

## 风险登记册

**Storage 实时源修正（2026-11-17）：** `session-storage-consistency-forget-atomicity-2026-11-16`，`reviews/storage-consistency/phase-3.8.2-storage-serialization-topology-adr.md`，Blob `bb544ba2f346bdc130d524bd5c7310d86f367988`。§8 已为 L1 逻辑架构选择 Option A；L4 物理引擎/部署仍 OPEN。文件读取接口未返回该分支 Commit SHA，仍属于 G1 证据项。

| ID | 风险 | 等级 | 是否阻塞 | 责任权威 | 最低关闭证据 | Gate |
|---|---|---:|---|---|---|---|
| AR-01 | L1 逻辑序列化配置已选定；L4 物理引擎/部署证明不完整 | Critical | 是 | Storage + D + I；A 集成 | Storage §8 已选择 Option A：每个 Canonical Memory Authority 一个 Serializable Transaction Domain；还须证明实际 DB Adapter/产品/配置、Anchor/Transition 持久性、HA/旧主 Fencing、权威读取、PITR/Restore 和物理 Race/Failover | G3/G4；JF-10 A/B/C |
| AR-02 | Fact/Claim/Evidence/时间语义未规范性闭环 | Critical | 是 | B | B 权威 ADR、类型定义、修正/冲突案例、下游精确版本采用 | G2/G3 |
| AR-03 | Forget/撤销/Restore 缺少端到端防复活证明 | Critical | 是 | I + D + Storage；E/F/G/C/H 消费者 | 闭世界 Inventory、Owner 证明、两种竞态顺序、Replay/索引/缓存/备份/还原测试 | G4；Forget Gate |
| AR-04 | Publication、Provider Outcome 与 Applied 尚无完整证明链 | High | Applied 工作流阻塞 | C/G/H，依赖 I/D/Storage | 精确 Owner 合同、最终请求边界、同 Key 的 UNKNOWN 恢复、符合性测试 | G2/G4 |
| AR-05 | Identity、Scope、Delegation 与授权治理不完整 | 受保护生产使用为 Critical | 是 | I + 外部治理权威；B/C/H 消费者 | I36-GOV-01..10 签署决策、时效/撤销证据、消费者接受 | G2/G4 |
| AR-06 | JF-10/COC 持久恢复与物理拓扑不完整 | Critical | 是 | Storage + A/COC + I/D/C | Gate A/B/C 证据、同 XID 恢复、Quorum/Restore/故障轨迹 | JF-10 A/B/C |
| AR-07 | 精确版本漂移与候选 Schema 不匹配 | High | 冻结时阻塞 | 各源 Owner；A 跟踪 | 当前分支 HEAD、路径、Blob、精确消费者绑定、双语与时效检查 | G1/G2/G6 |
| AR-08 | Canonical Cursor、Replay 和 Lineage 恢复不完整 | High | 端到端 Canonical 声明阻塞 | D/E/Storage | Cursor/Outbox 持久原子性；Replay/Gap/Duplicate/Crash 测试 | G3/G4 |
| AR-09 | 生产 DR、密钥托管、操作员及 RPO/RTO 未明确 | High | 生产阻塞 | Storage + I + 项目运维权威 | 部署 ADR、具名操作员、密钥生命周期、备份/PITR/Restore 演练、RPO/RTO | 生产验收 |
| AR-10 | 治理/合同负担可能超过可维护预算 | High | 有界准备不阻塞；规模化承诺阻塞 | A + 全体 Owner + 工程负责人 | 度量审查成本、自动符合性收益；在不损失不变量前提下减少重复状态机 | G5/G7 后续 |

## 五项根本风险

1. L1 逻辑序列化已选择（Storage Option A）；实际 L4 Engine/Deployment、权威 Adapter、HA/Fencing 和 Restore 符合性仍未证明。
2. Canonical 领域真值（尤其 Fact/Claim、时间和证据语义）尚未由 B 关闭。
3. Forget/撤销尚未以证明覆盖所有衍生物、缓存、重放、备份及还原路径。
4. Identity/Security Governance 和全局 Inventory 缺少必要外部批准。
5. 跨 Owner Publication、JF-10 恢复、Applied/Provider Outcome 缺少完整物理及端到端符合性证据。

## 风险处理

任何 Critical 风险均不接受、不豁免。AR-04、AR-07、AR-08、AR-10 在涉及强制正确性或冻结准入时仍然阻塞。只有 Deferred Capabilities Register 明确列出的能力延期，才可作为有界非阻塞工作开展。

A 可以接受全局范围和顺序风险，但不能代替 B、D、I、C、G、H 或 Storage 接受其领域风险。每项风险必须由对应权威提供上述证据，并由相关 Gate Owner 单独记录裁决后才能关闭。

## 交叉引用

参见 ARCH-CX-002、DEV-FEAS-002、DEP-DAG-002、PRIORITY-002、READINESS-002、CONFLICT-002、GATE-002、DEFERRED-002、FINAL-A-002。全部绑定同一 Main 基线 SHA。
