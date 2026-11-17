# 架构决策冲突登记册 — CONFLICT-002

- 版本：1.0.0；基线 `b372b62c640a2b656e54b6db62a4ee67d7d8c001`。
- 状态：A 集成裁决；不替代 Owner 领域规范决策。

| ID | 表面冲突/歧义 | A 裁决 | 权威/所需行动 | Gate |
|---|---|---|---|---|
| AC-01 | Modular Monolith 建议与 Storage 物理拓扑未决 | 不构成矛盾。Modular Monolith 是部署形态；Storage §8 已选择 L1 Option A（每个 Canonical Memory Authority 一个 Serializable Transaction Domain）。L4 Engine/Deployment 符合性仍由 Storage/D/I 负责且开放 | Storage + D + I 选定并证明拓扑；A 集成 | G3/G5；JF-10 |
| AC-02 | P0 Durable Vertical Slice 与 P0 语义/原子性前置条件未解决 | P0-07 必须位于 P0-02..05 之后；此前仅能开展 Harness/Fixture 工作 | A 修正 F/D/P 路线；D/E/Storage 负责前置条件 | 实现准入 |
| AC-03 | Delivery/Transport ACK 与 Applied | 必须保留为不同事实；ACK 不能证明跨越 Final Request 或 Provider Outcome | C/G/H 负责 Final Request/Applied 合同；I/D 提供授权/Fence 输入 | G2/G4；Issue #3 |
| AC-04 | COC 顺序、I Commit 决策和 Storage Visibility | 保留不同权威：COC 排序/记录；I PolicyDomain Sequencer 决定 JF-10 COMMIT/ABORT；Storage 解决同 XID 并拥有 Visibility；D 拥有 ForgetFence | A 只协调，不合成权威 | JF-10 A/B/C |
| AC-05 | Storage-first Participant 与 D Admission/Lineage Registration | Issue #25 当前 Crash-safe 提案顺序仅作为候选：先隐藏持久 Storage Participant，再 D Participant Registration，再 I Authorization，最后 Storage Visibility。未获精确 Owner 接受前不冻结 | D/E/I/Storage 必须独立接受当前精确 Bundle | G2/G3/G4 |
| AC-06 | Gate A 部分通过与旧 Issue 文本中的阻塞状态 | 以 Issue #10 最新修订为准：Gate A PARTIAL PASS / OPEN；Gate B 等待 A 全部条件而 BLOCKED；Gate C 等待 B 而 BLOCKED。另 Storage §8 已关闭 L1 Option A，不代表 L4 关闭。 | Storage 提供 A 剩余证据；A 跟踪 | JF-10 A/B/C |
| AC-07 | R Critical/High 风险等级与 X 序数复杂度分数 | 属于不同模型；不可相加或互相替代。R 衡量风险；X 衡量复杂度维度 | A 保留两个独立登记册 | G7 |
| AC-08 | F/D/P 模拟角色与独立 Owner 批准 | F/D/P 是同一会话中的分析角色，不是三个独立 Owner 批准 | 仍须 B/C/D/E/F/G/H/I/Storage 实际权威决策 | G2 |
| AC-09 | 架构仓库与实现责任归属 | README 确认架构定义用途；Issue #7 仍待指定运行时仓库/工程负责人 | 项目权威答复 Issue #7；本仓库不添加伪实现 | G5/G7 |
| AC-10 | Candidate Schema/Technology 工件与 Freeze 声明 | Candidate 和有限 CI 状态不等于规范冻结或生产符合性 | 对应 Owner/ADR 权威决定；A 要求精确 HEAD 证据 | G1/G2/G5 |

## A 的明确边界

A 决定全局顺序、范围、跨 Owner 兼容性和 Gate 证据充分性。A 不批准 B 领域语义、I 治理策略、D Canonical Lifecycle/Fence 语义、C Provider Outcome、G Applied 语义、H Wire Schema/Cryptography 或 Storage 物理拓扑。凡 Owner 决策或物理证明缺失，不得标记冲突已关闭。
