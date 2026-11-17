# 开发可行性矩阵 — DEV-FEAS-002

- 版本：1.0.0；基线：`main@8c0c5b11abf56a6f580fcf2a99c8043d3057da4f`
- 来源：F/D/P PR #46，分支 `review/session-3-engineering-planning-2026-11-17`，Commit `8b9ff8efa92a88dacc8f97b5faba5918fe5d2edc`，英文 Blob `081610b1734ec08dc7c35c75fae1cae3ca713be4`，中文 Blob `834dc39998342dc2f292fe1dfed411768b3ed156`。
- A 裁决：原则上 **FEASIBLE_WITH_CONDITIONS**；当前实现准入 **BLOCKED**。

## 可行性矩阵

| 领域 | 裁决 | 复杂度 | 责任 Owner | 关键前置条件 |
|---|---|---:|---|---|
| B Domain | FEASIBLE_WITH_CONDITIONS | L | B | Fact/Claim、Identity、时间 ADR；下游采用 |
| D Canonical Brain | FEASIBLE_WITH_CONDITIONS | XL | D | Canonical Authority、Cursor、Producer Barrier、Forget Fence、Visibility 合同 |
| E Compiler | FEASIBLE_WITH_CONDITIONS | L–XL | E | Durable Admission、Register-before-Queue、Lineage、Replay/Recovery |
| F Runtime/Retrieval | FEASIBLE_WITH_CONDITIONS | M–L | F | 权威 Permission/Fence 前置过滤；陈旧投影抑制 |
| G Context | FEASIBLE_WITH_CONDITIONS | L–XL | G | Context Version、Delivery、Applied 边界 |
| C Agent Integration | FEASIBLE_WITH_CONDITIONS | L–XL | C | Final Request 边界、Provider Side-effect 幂等与 UNKNOWN 恢复 |
| H BMCP | FEASIBLE_WITH_CONDITIONS | L | H | 精确 Schema、Canonicalization、Signature、Crypto、互操作决策 |
| I Security/Governance | 策略闭环 BLOCKED；机制有条件可行 | XL | I + 外部治理权威 | I36-GOV-01..10、InventorySeal、Revocation、Trust 批准 |
| Storage/Consistency | 生产拓扑 BLOCKED；原型可行 | XL | Storage | Option A 仅有条件接受为 L1 逻辑方向；A-01..A-05 和 D 精确采纳仍开放；实际 DB Engine/Adapter、持久 COC、同 XID 恢复、故障切换/还原证明仍开放 |
| Index/Cache | FEASIBLE_WITH_CONDITIONS | M–L | F + D + Storage | Derived-only Authority、Rebuild、Stale Suppression、Forget 安全 |
| 端到端系统 | NOT PROVEN | XL | 全体 Owner；A 集成 | 精确 Owner 合同 + 物理 P0 证明 + 符合性 |

## 工作量与置信度

F/D/P 使用相对规模 S/M/L/XL，而非人日。由于工程人数、可用时间、目标硬件、运行时仓库和交付责任尚未指定，无法可靠估算日历周期或人员投入。将相对规模转换为日期属于虚假精确。

## 关键技术结论

- Rust Local-first Modular Monolith 合理，适合作为候选起点；但它不是已批准的技术/拓扑 ADR。
- 在授权和 Forget 抑制成立后，Structured SQL + Lexical Retrieval 可作为首期读取路径。
- PostgreSQL 18.7 证据只是受限引擎能力探测，不证明已选生产拓扑或 D/I/COC 集成。
- Durable Ingress/Outbox、Canonical Cursor、Forget/Publication、JF-10 Recovery 和 Applied 必须分别提供证据。
- Vector/ANN、Reranking、Graph Backend 扩张不是安全首期纵向切片的前置条件。

## 当前 B→A 可行性更新

B Fact/Claim 仍 ADR-BLOCKED。中间 B Identity/Entity 研究工件已从 Main 撤销，不属于当前基线证据。H Unified 1.2.14 / wire 1.3.0 + CSubmitOutcome 1.0.1 是 L1/L2 候选；C 接受精确 H Mapping，D 接受 H Carrier/Crosswalk，I 有 Option A Anchor Review。但 H Mapping 状态过期，H/I/D 精确 Review Pin 未在同一当前 Bundle 中收敛，Storage v3.2.9 已过期。Storage v3.3.0 或等效版本由 C/H/D/I 和 A 共同复审前不得协议冻结。Option A 仅有条件接受为逻辑方向；A-01..A-05、D 精确采纳及 L2/L3/L4 仍开放。

## 五项工程前置条件

1. 项目权威指定运行时仓库、工程负责人、维护者、Build/CI 和合同到代码追溯机制（Issue #7）。
2. B 关闭规范性 Identity/Fact-Claim/Temporal 语义；消费者绑定精确版本。
3. I 与外部权威关闭安全治理决策及签署的闭世界 Producer/Recipient/Backup Inventory。
4. D/E/I/Storage 对 Admission → Dependency Registration → Fence → Final Visibility 达成精确一致，并证明两种竞态顺序和崩溃窗口。
5. Storage 完成 L4 物理实现并证明已选定的 L1 Option A 配置（实际 DB/Adapter、COC、同 XID 恢复、故障切换/还原）；C/G/H 关闭 Final Request 和 Applied/Provider Outcome 合同。

## 有界工程工作

仅允许在隔离、非生产的 Spike 范围内开展：Synthetic Fixtures、Rust Workspace/Toolchain 探索、不冻结领域语义的 Typed Ports、存储引擎比较、一次性 PostgreSQL 能力测试、确定性模型/故障测试框架脚手架、Synthetic Data 上的 FTS/Vector 质量基准、资源盘点和文档自动化。每个 Spike 必须有 Owner、精确输入版本、可复现命令、证据工件及明确非声明。

本评估不授权使用生产数据、Canonical Visibility、安全策略实现、Provider Side-effect、Schema Freeze 或生产部署。

参见 DEP-DAG-002、PRIORITY-002、READINESS-002 和 GATE-002。
