# 全系统架构风险登记册 — SYS-RISK-002

- 权威角色：A — 首席系统架构权威
- 版本：1.0.0（候选集成基线）
- 日期：2026-11-17
- Main 基线：`8c0c5b11abf56a6f580fcf2a99c8043d3057da4f`
- A 审查分支：`review/session-4-a-final-architecture-authority-current-2026-11-17`
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

| AR-11 | B/H/C/D/I/Storage 精确协议 Bundle 过期或未完整联结 | High | 协议冻结阻塞 | H + C + D + I + Storage；A 集成 | H 更新当前 D Crosswalk Mapping 并由 C 复审；H 复审当前 I P0、I 刷新 Anchor Review；H 更新 Mapping 状态/CI 当前性；Storage 发布 v3.3.0 后继版本并由 C/H/D/I 与 A 复审 | G1/G2/G6 |

## 五项根本风险

1. L1 逻辑序列化已选择（Storage Option A）；实际 L4 Engine/Deployment、权威 Adapter、HA/Fencing 和 Restore 符合性仍未证明。
2. Canonical 领域真值（尤其 Fact/Claim、时间和证据语义）尚未由 B 关闭。
3. Forget/撤销尚未以证明覆盖所有衍生物、缓存、重放、备份及还原路径。
4. Identity/Security Governance 和全局 Inventory 缺少必要外部批准。
5. 跨 Owner Publication、JF-10 恢复、Applied/Provider Outcome 缺少完整物理及端到端符合性证据。

## 风险处理

任何 Critical 风险均不接受、不豁免。AR-04、AR-07、AR-08、AR-10 在涉及强制正确性或冻结准入时仍然阻塞。只有 Deferred Capabilities Register 明确列出的能力延期，才可作为有界非阻塞工作开展。

A 可以接受全局范围和顺序风险，但不能代替 B、D、I、C、G、H 或 Storage 接受其领域风险。每项风险必须由对应权威提供上述证据，并由相关 Gate Owner 单独记录裁决后才能关闭。

## 基于 main@8c0c5b 的当前源刷新（2026-11-17）

- R PR #50、X PR #49 和 F/D/P PR #46 报告绑定的是较早 Main 基线 `b372b62c640a2b656e54b6db62a4ee67d7d8c001`；它们仍是分析输入，并非对当前 Main 的刷新评估。A 已集成 PR #51/#52/#54 后续证据，但在精确当前源/消费者 Pin 和必要角色刷新完成独立回读前，G1/G7 仍为部分完成。
- 当前 Main HEAD `8c0c5b11abf56a6f580fcf2a99c8043d3057da4f` 撤销了 Commit `6470f25...`、`67f1122...` 和 `e723222...` 短暂引入的三份 B 研究工件。这些工件不属于当前 Main 基线，也不是规范证据。B Fact/Claim ADR 仍 ADR-BLOCKED。
- B→A 审查 PR #52：分支 HEAD `2727bd8544f812d796186769f86cf92aba244dee`，报告 Blob `b59b2ef745330f901027f59b69c68b99097c604b`。
- Option A 审查 PR #54：分支 HEAD `208c5e84f64ec68338045b963407bcb6d2463faf`，报告 Blob `ff782d7ab32bdbe66f01a2057c516c5a855abdd3`；提案修订 Blob `f5ad30c8570d480f60bc9b02ee53c06317b41525` 尚 NOT ADOPTED。
- B 协议 PR #51：分支 HEAD `042f60217903215b75251bc36a650d7a4c994704`，证据 Ledger Blob `247b6644a3f1c61078e19befc7428be78d789d5c`。H 1.2.14 / wire 1.3.0 + CSubmitOutcome 1.0.1 是 L1/L2 候选；Storage v3.2.9 Manifest Blob `bf323a1682f2bfadc3ff41ea4f86883d678a77e3` 已过期。
- 精确候选 Blob：H Schema `09fcd1fa29fe24255fbd87cae79dafb406594a59`；C Schema `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda`；H Mapping `c196fdc7a9d88e344d37ba2810a9bce1803f8b96`；C Re-review `f2d33a8998f8a6906c9bef8be6f9e880c61a0c8c`；D Review `55ae7bc33b37f0e729949fdd2a694eb6211bbc55`；I P0 `44986f5f864bcdc1a79d34978273644d381a68c0`；I Anchor Review `f22d31dec3a95f094c2942ab816c830f007e830e`；Storage 拓扑 ADR `bb544ba2f346bdc130d524bd5c7310d86f367988`。
- H CI 当前 Pin：Run `44069941327`，Commit `ba2c9341fee4eb9ca9e665c74bdd37b4675dd251`，Job `133993324484`；H HEAD `362cc113cfb5b595a4002a6f6e980d19ae2d2d15`；Storage HEAD `39a1e0429f6b4b08c6c437c8e3f5ace582a7315f`（均按 PR #51 Ledger）。
- Storage v3.2.9 相对修正后的 C/D/I Review Pin 和 H CI 已过期。Storage 必须发布 v3.3.0 或等效版本；C/H/D/I 对同一 Manifest 复审，A 再回读。精确 Path/Commit 必须由 Storage 发布。

## 交叉引用

参见 ARCH-CX-002、DEV-FEAS-002、DEP-DAG-002、PRIORITY-002、READINESS-002、CONFLICT-002、GATE-002、DEFERRED-002、FINAL-A-002。全部绑定同一 Main 基线 SHA。



### AR-12 — 双语研究证据被误认为已独立验证的领域闭环
- 等级：**High**。阻塞：B5，以及任何依赖受影响 B 研究工件的规范性决策；其本身不是独立的运行时故障模式。
- 根因：作者侧翻译和成对文件可能被误认为独立语义对等，即使仍存在未翻译表格/条款、待人工复审项、过期来源 Pin 或状态漂移。
- 触发/后果：下游 Owner 使用尚未独立核验完整规范内容和决策状态的研究证据，冻结领域合同或 Schema。
- Owner：B 负责源文件整改；独立审查者负责逐条/逐行语义对等；各下游 Owner 负责精确版本采用；A 负责 G1/G6 集成跟踪。
- 关闭证据：整改所有 PARTIAL/PROVISIONAL 行；独立对照每条规范条款、表格行、稳定 ID、字段、枚举、状态、示例和来源 Pin；重新读取精确当前 Blob；记录 B Owner 决议及消费者采用。来源审计 Blob `a877ceff906da01e70e277a81b95978982af3ede` 只能证明审计存在，不能证明翻译通过。
- 风险接受：**不接受**。不虚构截止日期；必须在任何依赖该证据的规范决策/Schema Freeze 前关闭。B5 继续 BLOCKED；Issue #43 G6 在全系统复审完成前继续 PARTIAL / NOT PASSED。
- 残余风险：所有受影响 B 研究工件在独立接受前仅可作为研究材料。
- Gate：B5/B6；Issue #43 G1/G2/G6。
