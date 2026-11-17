# 全系统架构风险登记册 — SYS-RISK-002

- 权威角色：A — 首席系统架构权威
- 版本：1.0.0（候选集成基线）
- 日期：2026-11-17
- 历史来源快照（非当前 Main）：`b372b62c640a2b656e54b6db62a4ee67d7d8c001`
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
| AR-01 | Option A 仅有条件接受为 L1 方向；L1 澄清及 L2/L3/L4 仍开放 | Critical | 是 | Storage + D + I + A；适用时包括 COC Owner | 关闭 A-01..A-05：事务执行器/写权威；D EffectPermit/生命周期覆盖；单 BrainAuthority 原子操作范围；I COMMIT_WON 崩溃/撤销/重放；独立 Anchor/DB-Incarnation Anti-rollback Witness；随后证明 L2/L3/L4 | G1–G5；JF-10 A/B/C |
| AR-02 | Fact/Claim/Evidence/时间语义未规范性闭环 | Critical | 是 | B | B 权威 ADR、类型定义、修正/冲突案例、下游精确版本采用 | G2/G3 |
| AR-03 | Forget/撤销/Restore 缺少端到端防复活证明 | Critical | 是 | I + D + Storage；E/F/G/C/H 消费者 | 闭世界 Inventory、Owner 证明、两种竞态顺序、Replay/索引/缓存/备份/还原测试 | G4；Forget Gate |
| AR-04 | Publication、Provider Outcome 与 Applied 尚无完整证明链 | High | Applied 工作流阻塞 | C/G/H，依赖 I/D/Storage | 精确 Owner 合同、最终请求边界、同 Key 的 UNKNOWN 恢复、符合性测试 | G2/G4 |
| AR-05 | Identity、Scope、Delegation 与授权治理不完整 | 受保护生产使用为 Critical | 是 | I + 外部治理权威；B/C/H 消费者 | I36-GOV-01..10 签署决策、时效/撤销证据、消费者接受 | G2/G4 |
| AR-06 | JF-10/COC 持久恢复与物理拓扑不完整 | Critical | 是 | Storage + A/COC + I/D/C | Gate A/B/C 证据、同 XID 恢复、Quorum/Restore/故障轨迹 | JF-10 A/B/C |
| AR-07 | 精确版本漂移与候选 Schema 不匹配 | High | 冻结时阻塞 | 各源 Owner；A 跟踪 | 当前分支 HEAD、路径、Blob、精确消费者绑定、双语与时效检查 | G1/G2/G6 |
| AR-08 | Canonical Cursor、Replay 和 Lineage 恢复不完整 | High | 端到端 Canonical 声明阻塞 | D/E/Storage | Cursor/Outbox 持久原子性；Replay/Gap/Duplicate/Crash 测试 | G3/G4 |
| AR-09 | 生产 DR、密钥托管、操作员及 RPO/RTO 未明确 | High | 生产阻塞 | Storage + I + 项目运维权威 | 部署 ADR、具名操作员、密钥生命周期、备份/PITR/Restore 演练、RPO/RTO | 生产验收 |
| AR-10 | 治理/合同负担可能超过可维护预算 | High | 有界准备不阻塞；规模化承诺阻塞 | A + 全体 Owner + 工程负责人 | 度量审查成本、自动符合性收益；在不损失不变量前提下减少重复状态机 | G5/G7 后续 |

| AR-11 | B/H/C/D/I/Storage 精确协议 Bundle 过期或未完整联结 | High | 协议冻结阻塞 | H + C + D + I + Storage；A 集成 | H 更新当前 D Crosswalk Mapping 并由 C 复审；H 复审当前 I P0、I 刷新 Anchor Review；H 更新 Mapping 状态/CI 当前性；Storage 发布 v3.3.0 或等效 Manifest 并由 C/H/D/I 与 A 复审 | G1/G2/G6 |

## 五项根本风险

1. Option A 仅作为 v1 逻辑方向获得有条件接受；L1 A-01..A-05 澄清、L2 合同组合、L3 并发证明和 L4 物理部署仍开放。
2. Canonical 领域真值（尤其 Fact/Claim、时间和证据语义）尚未由 B 关闭。
3. Forget/撤销尚未以证明覆盖所有衍生物、缓存、重放、备份及还原路径。
4. Identity/Security Governance 和全局 Inventory 缺少必要外部批准。
5. 跨 Owner Publication、JF-10 恢复、Applied/Provider Outcome 缺少完整物理及端到端符合性证据。

## 风险处理

任何 Critical 风险均不接受、不豁免。AR-04、AR-07、AR-08、AR-10 在涉及强制正确性或冻结准入时仍然阻塞。只有 Deferred Capabilities Register 明确列出的能力延期，才可作为有界非阻塞工作开展。

A 可以接受全局范围和顺序风险，但不能代替 B、D、I、C、G、H 或 Storage 接受其领域风险。每项风险必须由对应权威提供上述证据，并由相关 Gate Owner 单独记录裁决后才能关闭。

## 基于 main@6470f25 的当前源刷新（2026-11-17）

- Main 新增 `canonical-identity-semantics.md` Blob `403105e130353884a6369b3d091e2284ee9f1c2c`（CANDIDATE；跨 Owner 绑定 OPEN）和 `canonical-domain-entity-inventory.md` Blob `2e0d45dfef9db2ddee19493cd274194312ad6332`（CANDIDATE INVENTORY；B1 IN PROGRESS）。B Fact/Claim ADR Blob `a1024938ff5baba069cf128c69496a44e143330c` 仍 ADR-BLOCKED。
- B→A 审查 PR #52：分支 HEAD `2727bd8544f812d796186769f86cf92aba244dee`，报告 Blob `b59b2ef745330f901027f59b69c68b99097c604b`。
- Option A 审查 PR #54：分支 HEAD `208c5e84f64ec68338045b963407bcb6d2463faf`，报告 Blob `ff782d7ab32bdbe66f01a2057c516c5a855abdd3`；提案修订 Blob `f5ad30c8570d480f60bc9b02ee53c06317b41525` 尚 NOT ADOPTED。
- B 协议对齐 PR #51：分支 HEAD `042f60217903215b75251bc36a650d7a4c994704`，证据 Ledger Blob `247b6644a3f1c61078e19befc7428be78d789d5c`。H 1.2.14 / wire 1.3.0 + CSubmitOutcome 1.0.1 是候选；v3.2.9 Manifest Blob `bf323a1682f2bfadc3ff41ea4f86883d678a77e3` 相对后续 C/D/I Review 与 H CI Pin 已过期。
- 精确候选源 Blob：H Schema `09fcd1fa29fe24255fbd87cae79dafb406594a59`；C Schema `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda`；H Mapping `c196fdc7a9d88e344d37ba2810a9bce1803f8b96`；C Re-review `f2d33a8998f8a6906c9bef8be6f9e880c61a0c8c`；D Review `55ae7bc33b37f0e729949fdd2a694eb6211bbc55`；I P0 `44986f5f864bcdc1a79d34978273644d381a68c0`；I Anchor Review 当前 Blob `f22d31dec3a95f094c2942ab816c830f007e830e`；Storage 拓扑 ADR `bb544ba2f346bdc130d524bd5c7310d86f367988`。
- H CI 当前性修正：Run `44069941327`，Commit `ba2c9341fee4eb9ca9e665c74bdd37b4675dd251`，Job `133993324484`；PR #51 Ledger 引用 H 分支 HEAD `362cc113cfb5b595a4002a6f6e980d19ae2d2d15`。同一 Ledger 引用 Storage 分支 HEAD `39a1e0429f6b4b08c6c437c8e3f5ace582a7315f`。
- PR #51 判定 v3.2.9 已过期；Storage 必须发布 v3.3.0 或等效版本，随后 C/H/D/I 对同一 Manifest 复审，A 再复审。Manifest 分支路径/Commit 必须由 Storage 精确绑定；A 不得手工修改 Owner 分支。

## 交叉引用

参见 ARCH-CX-002、DEV-FEAS-002、DEP-DAG-002、PRIORITY-002、READINESS-002、CONFLICT-002、GATE-002、DEFERRED-002、FINAL-A-002。全部绑定同一 Main 基线 SHA。


## 源版本时效与评估基线

本评估的来源证据基线固定为 main Commit `b372b62c640a2b656e54b6db62a4ee67d7d8c001`。发布时观察到的 main HEAD 为 `8c0c5b11abf56a6f580fcf2a99c8043d3057da4f`（后续 Revert Commit）；本评估不会将该 HEAD 偷换为已完成审查的基线。在任何 Gate 关闭或架构冻结决策前，必须针对该 HEAD 刷新所有引用的 Owner 工件并重新执行差异审查。Storage L1 拓扑另行固定为分支 `session-storage-consistency-forget-atomicity-2026-11-16`、Blob `bb544ba2f346bdc130d524bd5c7310d86f367988`；§8 已为 L1 选择 Option A，L4 物理符合性仍为 OPEN。


## 当前 Main HEAD

本次发布观察到的当前 Main HEAD：`8c0c5b11abf56a6f580fcf2a99c8043d3057da4f`。此前 `6470f25...` / `b372b62...` 均为历史快照，并非当前 Main。尚未完成针对当前 Main 的逐来源完整差异审计；G1 仍为 PARTIAL，Gate/冻结限制继续有效。
