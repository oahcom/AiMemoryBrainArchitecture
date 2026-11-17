# 根本性优先级与开发路线图 — PRIORITY-002

- 版本：1.0.0；基线 `8c0c5b11abf56a6f580fcf2a99c8043d3057da4f`。
- 状态：仅为规划建议；不构成实现或 Gate 授权。

## 统一优先级

| 优先级 | 工作 | Owner | 准入/退出证据 | Gate |
|---|---|---|---|---|
| P0-01 | 指定运行时仓库、工程负责人、维护者、Build/CI 和合同到代码追溯 | 项目权威/A 协调 | Canonical Repo/Branch、具名 RACI、可复现 Build/CI、责任人接受 | G5/G7；Issue #7 |
| P0-02 | 关闭 Domain Identity、Fact/Claim、Evidence 和 Temporal 语义 | B；消费者采用 | 已批准 B ADR、精确 Blob、类型案例、消费者采用 | G2/G3 |
| P0-03 | 关闭 I 安全治理、Trust、Revocation 和闭世界 Inventory | I + 外部权威 | 签署 I36-GOV-01..10 决策、InventorySealReceipt、Target/Backup/Recipient 枚举 | G2/G4 |
| P0-04 | 关闭 D/E/I/Storage Admission、Lineage、Forget Fence 和 Visibility 组合 | D/E/I/Storage | 精确 Owner 决策、两种竞态顺序、Crash/ACK-loss/Stale Lease、UNKNOWN 时保持隐藏 | G3/G4 |
| P0-05 | 完成已选定 L1 Option A 的 L4 物理 DB/COC/JF-10 证明 | Storage + A/COC + I/D | Gate A 完整；Gate B 持久 COC；Gate C 故障活动；同 XID 证明 | JF-10 A/B/C |
| P0-06 | 关闭 C/G/H Final Request、Provider Outcome 和 Applied 合同 | C/G/H + I/D 消费者 | 精确合同批准、Provider Close-vs-Send、相同 Idempotency Key、负向符合性 | G2/G4 |
| P0-07 | 有界 Durable Ingress → Canonical Commit/Cursor 纵向切片 | E/D/Storage；工程负责人 | Durable ACK、Outbox、幂等 Replay、Canonical Cursor 原子性、恢复证明；仅在 P0-02..05 后 | 实现准入 |
| P0-08 | 安全 Structured/Lexical Retrieval 与 Forget-safe Index/Cache Rebuild | F + D/I/Storage | Ranking 前 Permission/Fence、陈旧投影抑制、Rebuild/Restore 证明 | 实现验证 |
| P1 | Context Delivery、Adapter 集成、历史/当前 Applied 处理 | G/C/H + I/D | 精确 Applied Predicate 和 Provider Outcome；Version/Reconnect/Late Evidence 测试 | Applied 工作流 |
| P2 | Vector/ANN、Reranking、Entity Resolution、Consolidation 和 Conflict Resolution 智能能力 | F/D/E/B | 标注评估集、可量化收益、资源边界、Owner ADR | 延后能力准入 |
| P3 | 高并发、分布式扩展、高级自动扩缩容、多地域运维 | Engineering/Storage/I | 实测负载和已证明需求；部署/DR ADR 与故障证据 | 生产规模化 Gate |

P0 并非一个不可拆分的大阶段。P0-01..06 是权威与证明前置条件；P0-07..08 只有在指定依赖满足后才可开展有界实现。

## 新增根本性阻塞

- B 协议 Bundle 当前性是 P0/P1 冻结前置条件：v3.2.9 已过期；Storage v3.3.0 或等效版本必须绑定当前精确 Owner/CI 工件，并由 C/H/D/I 和 A 复审。
- A-01..A-05 被采纳且 D 对 Storage ADR 作出精确决议前，不得称 Option A 的 L1 已关闭。L3/L4 仍是独立证明。

## 首期形态

优先考虑 Local-first Rust Modular Monolith，保留逻辑 Owner 边界；限制为一个 I PolicyDomain；若 Storage/D/I 批准，可采用一个 Canonical Authority/事务域；先使用 Structured + Lexical Retrieval、可重建投影和窄 Adapter。该形态是候选配置，不是技术冻结。

## 明确顺序约束

- Permission 和 Forget 抑制未成立前，不得使用生产数据检索。
- D/E/I/Storage 原子性未明确并证明前，不得 Canonical Publication。
- C/G/H Final Request 与 Provider Side-effect 语义未接受并测试前，不得标记 Applied。
- 首期不支持 Multi-PolicyDomain Atomicity。
- Vector/Reranker/Graph 功能不得挤占未解决的 P0 正确性工作。

参见 DEP-DAG-002、DEFERRED-002、READINESS-002 和 GATE-002。
