# Gate 准入与退出标准 — GATE-002

- 版本：1.0.0；基线 `b372b62c640a2b656e54b6db62a4ee67d7d8c001`。
- 本文件保留两层独立门禁：Issue #43 集成 Gate G1–G8 与 JF-10 物理 Gate A/B/C。两者不可互换。

## Issue #43 集成 Gate

| Gate | 准入/退出证据 | 当前 A 裁决 |
|---|---|---|
| G1 精确源版本/时效 | 每项关键源均有当前分支 HEAD、Commit、Path、Blob SHA、废止关系和回读 | PARTIAL；报告绑定来源，但尚未完成全量 Owner 刷新和 A 回读 |
| G2 权威/消费者接受 | 完整 A–I + Storage 权威/消费者矩阵；精确版本 Owner 决策；不得推定批准 | BLOCKED |
| G3 端到端状态/因果一致性 | 无矛盾模型，或每个未决冲突均分配责任并保持阻塞；不得比较不同类型的本地位置 | BLOCKED |
| G4 P0/P1 Race/Crash/Recovery/Identity/Trust | 每项关键案例均有直接证明或明确阻塞状态 | BLOCKED |
| G5 技术/拓扑可行性 | 有责任人的拓扑/技术决策及可复现证据；不允许无依据的部署假设 | BLOCKED |
| G6 双语语义一致性 | 中英文配对，并独立检查语义/状态一致性 | PARTIAL；配对报告存在，全跨文档一致性仍需复审 |
| G7 A 集成裁决 | A 决策记录及 Owner 专属未决行动 | 本 PR 提供候选 A 裁决；仍需独立最终审查 |
| G8 冻结建议 | 基于 G1–G7 明确 READY / READY WITH ENUMERATED BLOCKERS / NOT READY | NOT READY |

不能仅凭文档存在、角色模拟、Schema-only 测试或候选参考模型测试判定 G1–G8 通过。

## JF-10 物理 Gate（保持原定义并独立）

**Gate A — 真实数据库能力。** 必须指定所选产品/版本/Build/配置及实际 Canonical Authority DB Adapter/Path；证明事务隔离、Prepared-XID（或明确获批的等效机制）、锁保留、重启后同 XID Commit/Rollback、VisibilityPointer + PublicationReceipt + Owner Outcome + Receipt-consumption Evidence + Outbox 原子性、权威读一致性、故障切换 Fencing、WAL Archive PITR/Restore、陈旧快照隔离和部署持久性。Issue #10 最新状态：**PARTIAL PASS / OPEN**。有限 PostgreSQL 18.7 能力探测不能关闭实际运行时、同步备库/提升、旧主 Fencing、PITR、Control Ledger 和操作员/Runbook 证据要求。

**Gate B — 持久化 COC Coordinator。** 必须选择 Durable Log/Consensus 实现，提供 Quorum 确认的 Digest-chained Prefix、单调 Term/Index、持久 Participant Intent Registry 与预分配 XID 绑定、故障期间 Recovery-cutoff Batch、未决 Participant 枚举/协调、带回滚保护的 Snapshot/Restore，以及 Prefix 缺失时 Fail-closed。当前：**等待 Gate A 全部通过，故 BLOCKED**。

**Gate C — 确定性故障注入套件。** 必须可复现测试所有崩溃、ACK Loss、Race、Provider UNKNOWN、COC Quorum 故障、陈旧副本、Prefix 丢失、Restore Rollback、IN_DOUBT 保留、无效 Receipt/Signature 和 Inventory/Lineage 不匹配；证据绑定精确 Binary/Schema/DB/Config，并经独立 Owner 复核。当前：**等待 Gate B 通过，故 BLOCKED**。

Gate A 部分通过不意味着 B 或 C 通过。Gate B/C 通过也不授权生产激活。JF-10 P0 仍 OPEN；Multi-PolicyDomain Atomicity 仍 BLOCKED。

## 生产授权

要求所有适用 Owner 批准、已选定并部署的拓扑、安全/身份治理、物理符合性、经过测试的 Backup/Restore 和 DR、具名负责操作员/On-call、批准的 Runbook、Monitoring、RPO/RTO 及明确生产授权。当前没有证据满足这些条件。

参见 SYS-RISK-002、READINESS-002 和 FINAL-A-002。
