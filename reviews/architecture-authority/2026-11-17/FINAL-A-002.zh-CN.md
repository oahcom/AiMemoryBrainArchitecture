# 最终架构工程评估 — FINAL-A-002

- 权威角色：A — 首席系统架构权威
- 版本：1.0.0
- 日期：2026-11-17
- 精确 Main 基线：`6470f25ca23b8d35c06f60be2326867066418d18`
- 审查分支：`review/session-4-a-final-architecture-authority-2026-11-17`
- 统一跟踪入口：Issue #43
- 整体决策结果：**DEFERRED**
- 架构状态：**ARCHITECTURE_NOT_READY**

## 执行决策

架构**原则上合理，但尚未证明完整系统在语义、物理实现、验证和维护层面成立**。本项目并未被判定为不可行。由于不可豁免的语义、权威、原子性、安全和恢复前置条件仍未关闭，架构冻结和全面实现准入暂缓。

A 仅允许有界准备工作。范围限定的 `APPROVED_WITH_CONDITIONS` 仅适用于：（1）有条件接受 Option A 作为 v1 逻辑方向，仍须关闭 A-01..A-05 并取得 D 精确采纳；（2）有条件接受 H 1.2.14/CSubmitOutcome 1.0.1 作为 L1/L2 协议候选，仍须关闭 B-01..B-04。两项均不代表 L1/L2 关闭、Gate 通过、受保护路径实现授权、Schema/Technology Freeze、部署批准或生产授权。

## 五项根本风险

1. Option A 仅作为 v1 逻辑方向获得有条件接受；A-01..A-05 和 D 精确采纳仍开放，L2/L3/L4 证明也未完成。
2. B 的 Fact/Claim/Identity/Temporal 语义仍 ADR-BLOCKED。
3. Forget/Revocation/Restore 缺少端到端防复活证明和完整 Inventory。
4. I36 Governance、Trust 和 Authorization 批准仍开放。
5. D/E/I/Storage Publication、JF-10 Recovery 和 C/G/H Applied/Provider Outcome 尚无端到端验证。

## 五项复杂度瓶颈

1. Forget Fence × Producer Admission × Dependency Registration × Publication。
2. Global Forget 跨 Canonical、衍生物、索引、缓存、Context、Adapter、副本和备份。
3. Storage/COC/JF-10 事务、同 XID 恢复、Quorum、Failover 和 Restore，并叠加共享 Transaction Executor、EffectPermit 生命周期覆盖和 Anchor Anti-rollback 义务。
4. D/E Durable Ingress、Outbox、Lease、Retry、Replay 和 Cursor 组合。
5. C/G/H Final Request、Provider Side-effect、Applied 与 I/D 权威耦合。

## 工程前置条件与关键路径

P0-01 实现仓库/责任人 → P0-02 B 领域语义及 P0-03 I 治理/Inventory → B-01..B-04 H/C/D/I/Storage 精确 Manifest 关闭 → A-01..A-05 Option A L1/L2 澄清及 D 精确采纳 → P0-04 D/E/I/Storage 原子 Publication/Forget 合同 → P0-05 Storage/COC/JF-10 L3/L4 物理证明 → P0-06 C/G/H Applied 合同 → P0-07 有界 Durable Canonical 切片 → P0-08 安全 Retrieval/Rebuild → P1 Context/Adapter/Applied → 集成 Recovery 和 Conformance。该顺序并非完全串行：Synthetic Benchmark、Harness 脚手架、源刷新、双语自动化和候选 DB 实验可以并行。

## 决策记录

**整体结果：DEFERRED。** 范围：架构冻结、全面实现准入、P0 正确性声明和生产激活。允许的下一步：READINESS-002 和 PRIORITY-002 列出的有界准备工作。

决策结果严格限定为：
- APPROVED — 指定范围证据完整，所有强制条件满足。
- APPROVED_WITH_CONDITIONS — 仅适用于有界范围；每项接受的残余条件均有完整 Owner/证据/期限/Gate 记录。
- DEFERRED — 证据或前置条件不足；禁止范围继续关闭。
- REJECTED — 提议设计违反不可豁免不变量或无法协调。

### 已批准条件

仅 COND-NB-01：延后 Vector/ANN 生产能力；允许 F 负责 Synthetic Benchmark。完整记录见 DEFERRED-002。没有任何 Critical 条件被豁免。

### 被拒绝条件

不整体拒绝五份独立评估。任何要求豁免领域真值、Canonical Authority、原子性、安全/Forget、强制 Owner 合同或明确 Gate 准入条件的提议，均作为不可豁免事项拒绝。

### 延后事项与责任人

| ID | Owner | 关闭期限 | 风险接受 |
|---|---|---|---|
| AR-01 已选 Option A 的 L4 物理实现 | Storage + D + I | 最终 Visibility 实现/JF-10 Gate A 完成前 | 不接受；阻塞 |
| AR-02 领域语义 | B | 依赖 Schema Freeze 前 | 不接受；阻塞 |
| AR-03 Forget/Inventory | I + D + Storage；所有消费者 | Forget/Restore 安全 Gate 前 | 不接受；阻塞 |
| AR-04 Applied/Provider | C/G/H + I/D | Applied 实现/验收前 | 不接受；阻塞 |
| AR-05 治理 | I + 外部权威 | 受保护生产使用前 | 不接受；阻塞 |
| AR-06 JF-10/COC | Storage + A/COC + I/D/C | Gate A→B→C 顺序退出 | 不接受；阻塞 |
| AR-07 源版本时效 | 各 Owner；A 跟踪 | G1/G2 和每次冻结复审前 | 不接受；阻塞 |
| AR-08 Cursor/Replay | D/E/Storage | Canonical 端到端符合性前 | 不接受；阻塞 |
| AR-09 生产 DR | Storage + I + 运维权威 | 生产授权前 | 不接受；阻塞 |
| AR-10 治理经济性 | A + 全体 Owner + 工程负责人 | 规模化/运维模式承诺前 | 残余风险开放；不得豁免核心语义 |\n| AR-11 B 协议精确当前性 | H + C + D + I + Storage；A 集成 | G1/G2 和协议关闭前 | 不接受；阻塞 |

## 强制未决条件记录——不得作为残余风险接受

以下均为阻塞条件。它们**尚未被接受或豁免**；记录仅用于明确责任人与关闭证据。

### A-01 — 跨 Owner 事务执行器与写入权威边界
- 问题：一个共享事务需要同时写入 D 自有行和 Storage 自有行，但事务执行权威、Mutation Capability 和 DB Role 隔离尚未规范化。
- 证据：PR #54 审查 Blob `ff782d7ab32bdbe66f01a2057c516c5a855abdd3`；修订提案 Blob `f5ad30c8570d480f60bc9b02ee53c06317b41525`（NOT ADOPTED）；Storage ADR Blob `bb544ba2f346bdc130d524bd5c7310d86f367988`。
- 风险：High；阻塞：是，阻塞 L1/L2 关闭。
- 允许：Owner 合同编写和事务 Harness。禁止：共享通用写权限、跨 Owner 行变更或关闭 L1。
- Owner：Storage + D。关闭标准：定义每 BrainAuthority 的 Transaction Executor/UoW、不可变 D/Storage Mutation Command、DB Role 隔离、Anchor CAS 和相同 Transition Ref/Digest 幂等性；取得 D/Storage 精确接受。
- 截止：L1/L2 关闭前。验证：后继 ADR/API Blob、Owner 决策记录、双语一致性和错误 Owner/过期 Command 负向测试。
- 风险接受依据/权威：无；A 不代表 D/Storage 接受该未决风险。升级：保持 L1/L2 阻塞；停止任何假设共享写权限的实现。Gate：G2/G3、Option A L1/L2。

### A-02 — D Fence-sensitive 生命周期与 EffectPermit 覆盖
- 问题：当前 Anchor Transition 集可能遗漏 Attempt/Lease、Retry/Replay、受保护 Source Read/Execution、迟到 Dependency 和 Terminalization 竞态。
- 证据：PR #54 审查 Blob `ff782d7ab32bdbe66f01a2057c516c5a855abdd3`；提案 Blob `f5ad30c8570d480f60bc9b02ee53c06317b41525`；D Publication Proposal Blob `17e53890dd6cce9bea9eacc1be2e64b0ef55ac78`。
- 风险：Critical；阻塞：是，阻塞 Forget/Publication 正确性。
- 允许：状态机和竞态 Harness 设计。禁止：基于不完整 Fence 覆盖执行受保护 Source Read/Execution 或最终 Publication。
- Owner：D，E/Storage 为消费者。关闭标准：映射每个 Fence-sensitive Transition；签发 Typed Single-use/Non-replayable EffectPermit，绑定 BrainAuthority、WorkItem、Attempt、Lease、Source/Lineage/Scope Digest、ForgetFenceGeneration 和 Anchor Revision；定义 Late Dependency 的 Barrier Reopen 语义。
- 截止：L1/L2 关闭和任何受保护路径启用前。验证：精确 D 合同、消费者接受、两种串行顺序、Stale Permit、Late Dependency、Crash/ACK-loss、Retry/Replay 轨迹。
- 风险接受依据/权威：无；A 无权接受 D 生命周期正确性风险。升级：保持 Forget/Publication Gate 阻塞。Gate：G3/G4。

### A-03 — v1 每个原子操作仅限一个 BrainAuthority
- 问题：每 Authority Anchor 尚未明确一个 Publication/Forget Operation 是否可能跨越多个 BrainAuthorityRef。
- 证据：PR #54 审查 Blob `ff782d7ab32bdbe66f01a2057c516c5a855abdd3`；提案 Blob `f5ad30c8570d480f60bc9b02ee53c06317b41525`。
- 风险：High；阻塞：是，阻塞 v1 范围关闭。
- 允许：单 Authority 操作配置和 Fan-out 设计。禁止：跨 BrainAuthority 原子性声明或跨 Authority 单事务。
- Owner：D + Storage + I；A 集成。关闭标准：明确每个 v1 原子 PublicationOperation/ProducerWork Admission/Fence/Visibility Outcome 只绑定一个 BrainAuthorityRef 和 SerializationDomainRef；Global Forget 必须按 Authority Fan-out，并收齐终态 Proof。
- 截止：L1 关闭和任何多 Authority 功能前。验证：规范范围声明、跨 Authority 负向测试、Global Inventory/Completion Proof。
- 风险接受依据/权威：A 仅有条件接受单 Authority v1 范围；不接受跨 Authority 风险。升级：阻止多 Authority 功能。Gate：G2/G3/G4。

### A-04 — I COMMIT_WON Receipt 崩溃/撤销/重放语义
- 问题：单次 I Authorization 消费必须定义不可变 Tuple、后续 Revocation、相同 Receipt 重放及 Storage Commit 前崩溃行为。
- 证据：PR #54 审查 Blob `ff782d7ab32bdbe66f01a2057c516c5a855abdd3`；提案 Blob `f5ad30c8570d480f60bc9b02ee53c06317b41525`；I P0 Blob `44986f5f864bcdc1a79d34978273644d381a68c0`。
- 风险：Critical；阻塞：是，阻塞 L2/授权正确性。
- 允许：I 自有 Policy/Receipt 合同和 Synthetic Replay 测试。禁止：Storage 独立解释 COMMIT_WON，或在不明确崩溃后用新 Tuple 重新授权。
- Owner：I + Storage，D/H 为消费者。关闭标准：精确 Tuple 绑定；已获胜 Tuple 不被后续 Revocation 追溯改变，但后续 Tuple 被阻止；相同 Tuple 重放返回相同不可变结果；崩溃保持未决，直到同一 Storage Operation 达到 COMMITTED_VISIBLE 或权威 NO_PUBLICATION。
- 截止：L2 关闭和受保护 Visibility 前。验证：I 签署后继合同、D/H/Storage 精确复审、Crash/Revocation/Replay 负向向量。
- 风险接受依据/权威：无；A 无权接受 I Policy 风险。升级：UNKNOWN 保持阻塞并升级 I/A。Gate：G2/G3/G4。

### A-05 — 独立 Anchor Checkpoint 与 Restore Anti-rollback Witness
- 问题：Anchor Row 和 Transition Log 同在一个 DB，陈旧 PITR/Restore 可能同时回滚二者且表面自洽。
- 证据：PR #54 审查 Blob `ff782d7ab32bdbe66f01a2057c516c5a855abdd3`；提案 Blob `f5ad30c8570d480f60bc9b02ee53c06317b41525`；Storage ADR Blob `bb544ba2f346bdc130d524bd5c7310d86f367988`。
- 风险：Critical；阻塞：是，阻塞 Recovery/L2/L3/L4。
- 允许：Witness 设计和一次性 Restore 实验。禁止：没有独立连续性证明就恢复写入。
- Owner：Storage + I；D 参与。关闭标准：DB 故障域之外的独立不可回滚 Checkpoint/Root，精确 DatabaseIncarnation 和连续 Transition Prefix 证明；不可用/不匹配/Fork/Prefix 缺失必须 RESTORE_FENCED/UNKNOWN。
- 截止：L2/L3 关闭及任何生产 Restore 声明前。验证：Witness 合同、故障模式矩阵、陈旧 PITR/Rollback/Fork/Record 缺失测试及 Owner 批准。
- 风险接受依据/权威：无；A 无权接受 Storage/I Recovery 风险。升级：保持 RESTORE_FENCED 并停止受影响写入。Gate：G3/G4；JF-10 A/B/C。

### B-01 — H Mapping 必须绑定当前 D Crosswalk，C 必须复审后继版本
- 问题：H Mapping Blob `c196fdc7a9d88e344d37ba2810a9bce1803f8b96` 仍绑定前一版 D Crosswalk；当前 D Crosswalk 为 `c4adf827dd62d44c43b8e871dec4835581508adf`。
- 证据：PR #51 Ledger Blob `247b6644a3f1c61078e19befc7428be78d789d5c`；C 接受 Blob `f2d33a8998f8a6906c9bef8be6f9e880c61a0c8c`。
- 风险：High；阻塞：是，阻塞协议 Bundle 关闭。
- 允许：H 后继 Mapping 与 C 复审。禁止：协议冻结，或将 C 对旧 H Blob 的接受自动转移到新 Blob。
- Owner：H + C。关闭标准：H 发布绑定当前 D Crosswalk 的 Mapping；C 接受该精确后继 Blob。
- 截止：B 协议关闭前。验证：精确 H/C Blob 和当前分支/Commit Pin。风险接受：无。权威：H/C；A 仅集成。升级：保持 B 阻塞。Gate：G1/G2/G6。

### B-02 — H/I 精确 P0 与 Anchor Review Pin 必须收敛
- 问题：当前 I P0 Blob `44986f5f864bcdc1a79d34978273644d381a68c0` 和 H 1.2.14 Schema `09fcd1fa29fe24255fbd87cae79dafb406594a59` 尚未反映在同一组当前 H Review + I Anchor Review 中。
- 证据：PR #52 报告 Blob `b59b2ef745330f901027f59b69c68b99097c604b`；PR #51 Ledger Blob `247b6644a3f1c61078e19befc7428be78d789d5c`。
- 风险：High；阻塞：是，阻塞协议/安全闭环。
- 允许：H 复审和 I Pin 刷新。禁止：声称 I P0 与 H Review 已联合当前化。
- Owner：H + I。关闭标准：H 复审精确当前 I P0/H Schema；I 将 Anchor Review 刷新到精确当前 I P0/H 工件。
- 截止：B 协议关闭前。验证：精确 Review Blob 和消费者矩阵。风险接受：无。权威：H/I。升级：保持 G2 阻塞。Gate：G1/G2/G6。

### B-03 — H Mapping 状态/CI 记录过期
- 问题：H Mapping 仍标记需要 C Review，尽管 C 已接受；当前 H CI 绑定为 Run `44069941327` / Commit `ba2c9341fee4eb9ca9e665c74bdd37b4675dd251` / Job `133993324484`。
- 证据：H Mapping Blob `c196fdc7a9d88e344d37ba2810a9bce1803f8b96`；C Review Blob `f2d33a8998f8a6906c9bef8be6f9e880c61a0c8c`；PR #51 Ledger Blob `247b6644a3f1c61078e19befc7428be78d789d5c`。
- 风险：Medium；阻塞：是，阻塞精确 Bundle 当前性。
- 允许：H 当前性补充。禁止：将旧状态或 CI 当作最新证明。
- Owner：H。关闭标准：发布精确状态更新，绑定 C Review 和当前 H CI Run/Commit/Job。截止：v3.3.0 Manifest 冻结前。验证：H Blob 回读及 Run/Job 链接。风险接受：无。权威：H。升级：保持 G1/G2 部分阻塞。Gate：G1/G2。

### B-04 — Storage v3.2.9 Manifest 已过期
- 问题：Manifest Blob `bf323a1682f2bfadc3ff41ea4f86883d678a77e3` 绑定较早 C/D/I Review 和 H CI Run 44069777296，而非当前修正后的 Pin。
- 证据：PR #51 Ledger Blob `247b6644a3f1c61078e19befc7428be78d789d5c`；当前 H Run `44069941327` / Commit `ba2c9341fee4eb9ca9e665c74bdd37b4675dd251` / Job `133993324484`。
- 风险：High；阻塞：是，阻塞协议 Bundle 关闭。
- 允许：Storage 发布 v3.3.0 或等效版本。禁止：A/C/H/D/I 手工修改 Storage Manifest，或将 v3.2.9 视为当前版本。
- Owner：Storage；C/H/D/I 复审；A 集成。关闭标准：后继 Manifest 绑定当前 H Schema/Mapping/CI、C Schema/Review、D Crosswalk/Review、I P0/Anchor Review 和精确 Run/Commit/Job；C/H/D/I 复审同一 Blob；A 独立回读。
- 截止：G1/G2 和协议关闭前。验证：精确 Manifest Path/Branch HEAD/Blob、四个 Owner 决议、A 回读和双语一致性。风险接受：无。权威：Storage 发布；各 Owner 批准自己的领域；A 只接受集成。升级：协议 Bundle 保持阻塞。Gate：G1/G2/G6。

## 允许开展的工作

- 隔离 Synthetic Data 可行性 Spike 和基准测试。
- Rust Workspace/Toolchain 与不冻结合同的 Ports 探索。
- DB/COC 候选比较和一次性能力实验。
- 确定性 Reference Model/Fault Harness 脚手架。
- Synthetic Fixtures 上的 Retrieval 质量实验。
- 精确源版本、双语一致性和 Conformance 自动化。
- 硬件/工作负载盘点及运维/Runbook 草案。

## 禁止开展的工作

- 本决策不允许修改或合并 Main/Owner 分支。
- 不得将 Candidate Schema/ADR 视为冻结。
- 不得 Canonical 生产写入或检索受保护生产数据。
- 不得执行 Provider Side-effect 或声称 Applied。
- 未经 I 权威不得自行定义安全策略或声称 Global Forget 完成。
- 不得声称支持跨 PolicyDomain 原子性。
- 不得解除 Gate、部署或生产激活。

## Gate 限制

- Issue #43 G1–G8：G1/G6 部分完成；G2–G5 阻塞；G7 为候选 A 裁决；G8 NOT READY。
- JF-10 Gate A：PARTIAL PASS / OPEN。Gate B：等待 Gate A 完成而 BLOCKED。Gate C：等待 Gate B 完成而 BLOCKED。JF-10 P0 仍 OPEN。
- 生产授权仍为 NOT AUTHORIZED。

## 残余风险与可逆性

所有 Critical 风险仍开放。若已接受条件违反 Owner、证据、范围、期限或 Gate 边界，或非阻塞事项升级为 P0/P1 正确性依赖，该条件自动暂停。升级至 A 和相关 Owner；停止受影响工作；刷新精确源版本并记录新决策。A 的决策可逆，不会默默覆盖 Owner 权威。

## 证据与交叉引用

R PR #50；X PR #49；F/D/P PR #46；B 协议 PR #51；B→A 审查 PR #52；Option A 拓扑审查 PR #54；当前 Main `6470f25ca23b8d35c06f60be2326867066418d18`；Issues #3、#5、#7、#10、#25、#29、#43；精确来源见 SYS-RISK-002。配套文件：ARCH-CX-002、DEV-FEAS-002、DEP-DAG-002、PRIORITY-002、READINESS-002、CONFLICT-002、GATE-002、DEFERRED-002。本评估不合并 PR、不关闭 Issue #43，也不授权生产。
