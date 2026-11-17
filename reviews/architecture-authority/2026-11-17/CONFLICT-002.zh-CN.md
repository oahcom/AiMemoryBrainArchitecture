# 架构决策冲突登记册 — CONFLICT-002

- 版本：1.0.0；基线 `6470f25ca23b8d35c06f60be2326867066418d18`（历史评估快照，非当前 Main）。
- 状态：A 集成裁决；不替代 Owner 领域规范决策。

| ID | 表面冲突/歧义 | A 裁决 | 权威/所需行动 | Gate |
|---|---|---|---|---|
| AC-01 | Modular Monolith 建议与 Storage 已选 L1 逻辑配置及 L4 部署开放 | 不构成矛盾。Modular Monolith 是部署形态；Storage §8 已选择 L1 Option A（每个 Canonical Memory Authority 一个 Serializable Transaction Domain）。L4 Engine/Deployment 符合性仍由 Storage/D/I 负责且开放 | Storage + D + I 证明 Option A 的 L4 实现；A 集成 | G3/G5；JF-10 |
| AC-02 | P0 Durable Vertical Slice 与 P0 语义/原子性前置条件未解决 | P0-07 必须位于 P0-02..05 之后；此前仅能开展 Harness/Fixture 工作 | A 修正 F/D/P 路线；D/E/Storage 负责前置条件 | 实现准入 |
| AC-03 | Delivery/Transport ACK 与 Applied | 必须保留为不同事实；ACK 不能证明跨越 Final Request 或 Provider Outcome | C/G/H 负责 Final Request/Applied 合同；I/D 提供授权/Fence 输入 | G2/G4；Issue #3 |
| AC-04 | COC 顺序、I Commit 决策和 Storage Visibility | 保留不同权威：COC 排序/记录；I PolicyDomain Sequencer 决定 JF-10 COMMIT/ABORT；Storage 解决同 XID 并拥有 Visibility；D 拥有 ForgetFence | A 只协调，不合成权威 | JF-10 A/B/C |
| AC-05 | Storage-first Participant 与 D Admission/Lineage Registration | Issue #25 当前 Crash-safe 提案顺序仅作为候选：先隐藏持久 Storage Participant，再 D Participant Registration，再 I Authorization，最后 Storage Visibility。未获精确 Owner 接受前不冻结 | D/E/I/Storage 必须独立接受当前精确 Bundle | G2/G3/G4 |
| AC-06 | Gate A 部分通过与旧 Issue 文本中的阻塞状态 | 以 Issue #10 最新修订为准：Gate A PARTIAL PASS / OPEN；Gate B 等待 A 全部条件而 BLOCKED；Gate C 等待 B 而 BLOCKED。另 Storage §8 已关闭 L1 Option A，不代表 L4 关闭。 | Storage 提供 A 剩余证据；A 跟踪 | JF-10 A/B/C |
| AC-07 | R Critical/High 风险等级与 X 序数复杂度分数 | 属于不同模型；不可相加或互相替代。R 衡量风险；X 衡量复杂度维度 | A 保留两个独立登记册 | G7 |
| AC-08 | F/D/P 模拟角色与独立 Owner 批准 | F/D/P 是同一会话中的分析角色，不是三个独立 Owner 批准 | 仍须 B/C/D/E/F/G/H/I/Storage 实际权威决策 | G2 |
| AC-09 | 架构仓库与实现责任归属 | README 确认架构定义用途；Issue #7 仍待指定运行时仓库/工程负责人 | 项目权威答复 Issue #7；本仓库不添加伪实现 | G5/G7 |
| AC-10 | Candidate Schema/Technology 工件与 Freeze 声明 | Candidate 和有限 CI 状态不等于规范冻结或生产符合性 | 对应 Owner/ADR 权威决定；A 要求精确 HEAD 证据 | G1/G2/G5 |

| AC-11 | Storage 拓扑 ADR 保留了“尚未选择方案”的前置补充文字，而 §8 已明确在 L1 层覆盖该文字 | 以 §8 为准：L1 已选择 Option A；§3 历史文字不是当前阻塞，但应明确标记/精简以免产生歧义 | Storage | G1/G5 冻结复审前 | G1/G5 |

| AC-12 | Storage v3.2.9 Manifest 被当作当前版本，但后续 C/D/I Review Pin 和 H CI 已更新 | 候选语义仍一致，但 Manifest 已过期；Storage 发布 v3.3.0/等效版本，C/H/D/I 复审同一 Blob，A 再复审 | Storage + C/H/D/I；A 集成 | G1/G2/G6 |
| AC-13 | 新 B Identity/Entity 工件可能被误认为领域语义已关闭 | 这些仍为 CANDIDATE/B1 IN PROGRESS；Fact/Claim 仍 ADR-BLOCKED；不得依此冻结下游 Schema | B；I/C/H 消费者 | G2/G3 |
| AC-14 | Option A 逻辑选择可能被误认为 L1/L2 已完成 | 仅有条件接受 L1 方向；A-01..A-05 和 D 精确采纳仍开放；L2/L3/L4 分离 | Storage/D/I + A | G2/G3/G4/G5 |

## A 的明确边界

A 决定全局顺序、范围、跨 Owner 兼容性和 Gate 证据充分性。A 不批准 B 领域语义、I 治理策略、D Canonical Lifecycle/Fence 语义、C Provider Outcome、G Applied 语义、H Wire Schema/Cryptography 或 Storage 物理拓扑。凡 Owner 决策或物理证明缺失，不得标记冲突已关闭。


## 当前 Main HEAD

本次发布独立观察到的当前 Main HEAD 为 `8c0c5b11abf56a6f580fcf2a99c8043d3057da4f`。此前的 `6470f25...` / `b372b62...` 均为历史评估快照，不是当前 Main。本套文件尚未完成针对当前 Main 的逐来源完整差异审计；G1 仍为 PARTIAL，所有 Gate/冻结限制继续有效。
