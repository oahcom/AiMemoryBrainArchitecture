# Session 4 — G1 当前来源与证据时效审计
# G1-003 — Main 精确差异、Owner Pin、R/X/F/D/P 与治理对账

- 审查 ID：G1-CURRENTNESS-003
- 审查角色：A — 首席系统架构权威（委托集成审查角色）
- 日期：2026-11-17
- 用户指定不可变基线：`8c0c5b11abf56a6f580fcf2a99c8043d3057da4f`
- 最终审计时观察到的 main HEAD：`901e38ba7b45ed1822eaefddc2da8d765cf8985c`
- 审查分支：`review/session-4-a-g1-currentness-audit-2026-11-17`
- 状态：**G1 PARTIAL — main 差异已完整枚举；已刷新部分 Owner 来源 Pin；Owner 全量逐源语义审查与同 Bundle 采纳审查仍未完成。**
- 本文件是证据审计，不是 Owner 批准、架构冻结、实现授权或生产验收。

## 1. 执行结论

用户指定的 SHA `8c0c5b1...` 是真实 main 提交。最终审计快照中的 main 为 `901e38ba...`，提交历史领先两个提交。中间提交 `ca69d50...` 曾短暂新增一个仅属研究用途的双语对等审计文件；随后 `901e38ba...` 将其撤回。因此 `901e38ba...` 的最终文件树与 `8c0c5b1...` 完全相同（Tree SHA `7096e0bc3fdc9a390fccff388f9261522fa424f2`）。指定基线到当前 main 的最终净文件差异为零。

**G1 仍为 PARTIAL，不能 PASS。** Main 差异已完整识别并读取，但：
1. R、X、F/D/P 正式评估稿仍声明历史 main 基线 `b372b62...`。
2. 当前 Owner 分支已推进，超出这些评估和旧证据登记册使用的 Owner 精确 Pin。
3. H Unified 1.2.15 已成为新的结构候选；C、I 仅有条件接受其 Schema Shape。C 明确尚未审查 Validator/CI；Storage 最新 v3.3.2 清单仍绑定 H 1.2.14。
4. B Fact/Claim 仍为 ADR-BLOCKED；I36-GOV-01..10 仍为治理阻塞。
5. 多个当前 A 复审 PR（#57–#61）仍以 `8c0c5b1...` 为 base，比审计时 main 落后一个提交。

没有证据支持将 G1 升级为 PASS，也没有依据改变 A 的总体裁决 **DEFERRED / ARCHITECTURE_NOT_READY**。

## 2. Main 提交与逐文件差异

### 2.1 用户指定的基线提交

提交 `8c0c5b11abf56a6f580fcf2a99c8043d3057da4f`：
- 提交说明：`revert(domain): remove research artifact mistakenly written to main`
- 父提交：`67f1122e2ecad3bacd013871dde9a165f0730292`
- 影响：删除 `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/domain-model-decision-record.md`（154 行）。

被删除文件是研究工件，不是 B Owner 的正式 ADR 批准。删除它并没有解决 Fact/Claim 决策；当前 B Owner 分支仍保留两份明确标记 ADR-BLOCKED 的记录（见 §4）。

### 2.2 指定 SHA 到最终审计时当前 main 的精确差异

| 路径 | 两提交之间的历史变化 | 精确 Blob | 审计结论 |
|---|---|---|---|
| `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/bilingual-parity-audit.md` | 由 `ca69d50...` 新增（+131 行），随后由 `901e38b...` 删除 | `a877ceff906da01e70e277a81b95978982af3ede`（中间版本） | 已从中间提交读取。其结论为 B5 **NOT PASSED / BLOCKED**；多数研究文件仍需双语对等复审。这是研究审计，不是 Owner 决策或架构规范修订，且最终 main 中已不存在。 |

文件树计数：`8c0c5b1...` 为 82 个 Blob；中间版本 `ca69d50...` 为 83 个 Blob；最终版本 `901e38b...` 为 82 个 Blob。最终 Tree SHA 与用户指定基线完全相同：`7096e0bc3fdc9a390fccff388f9261522fa424f2`；净文件差异为零。

该短暂双语审计仍是研究分支证据：中文标题或部分翻译不能证明双语对等。其 B5 结论在研究分支上仍为 BLOCKED。不能推断 G6 PASS，也不能声称该文件属于当前 main。

## 3. R / X / F-D-P 评估审计

### 3.1 R — 全系统风险评估

- PR #48：OPEN / DRAFT / 未合并；base `b372b62...`；head `cfcc8f20e2bd6323798864875735db4c57038479`；报告 Blob `799bed6453eb654e52b97d05e3e281efd2139a7c`。
- PR #50：OPEN / DRAFT / 未合并；base `b372b62...`；head `8542d608ccfe6747c5f6171a2a38d325f10a628c`；英文报告 Blob `4067005a65fe528aa7d5fc43ff5be79eb0adaa53`。
- 最新观察到的 R 分支：`review/r-principal-system-wide-risk-2026-11-17` @ `7d5d98bdf0ad68f9382485d97d2d1de4381f1409`；报告 Blob 仍为 `799bed...`。

**时效发现：** R 报告仍绑定 main `b372b62...`。R-01 仍称拓扑未选定，并将 Storage ADR 描述为 ADR-BLOCKED / NO TOPOLOGY SELECTED。对于 L1，这一说法已经过时：精确 Storage ADR Blob `bb544ba...` 的 §8.1 和 §8.6 已选择 Option A 作为 v1 规范逻辑拓扑。§7 明确将早期“未选择方案”标记为历史状态，并声明该状态已在 L1 被后续内容取代。剩余阻塞不是“没有 L1 拓扑”，而是 A-01..A-05 规范澄清尚未采纳、L3 集成证明未完成、L4 物理部署/符合性仍开放。R 必须修正风险措辞与来源 Pin。其总体 NOT READY 结论仍有依据。

### 3.2 X — 架构复杂度评估

- PR #49：OPEN / DRAFT / 未合并；base `b372b62...`；head `131f91743bd506517ee354d58c277501ca447929`；英文报告 Blob `c509120644d6f7c7223decf3f9f0ee33b0548bb7`。
- 最新观察到的 X 分支：`review/architecture-complexity-assessment-2026-11-17` @ `d556c127ebe872f42f18edb2923e9a0438d50f5b`；报告 Blob `f562ad0c9932ec7190701f399dc5ed7081226840`。

**时效发现：** X 同样绑定 `b372b62...`，并将 Storage 拓扑 ADR 描述为阻塞/未选定。必须更新为 L1 Option A 已选定、L4 仍开放。复杂度结论（**NOT PROVEN**）仍然合理，因为跨 Owner 证明负担、Restore、Forget、Applied 和物理实现仍未闭环。不得把 L1 选择误当成 L3/L4 可行性证明。

### 3.3 F / D / P — 工程可行性、依赖 DAG 与优先级

- PR #46：OPEN / DRAFT / 未合并；base `b372b62...`；head `8b9ff8efa92a88dacc8f97b5faba5918fe5d2edc`。
- 英文报告 Blob：`081610b1734ec08dc7c35c75fae1cae3ca713be4`。
- 报告明确说明其基线仅在 PR 创建时得到核实，不代表 main 此后没有变化。

**时效发现：** F/D/P 对旧基线和证据限制的披露是诚实的，但它不是当前 main 评估。Storage “生产拓扑 BLOCKED” 在 L4 层面仍成立；不得解读为 L1 逻辑拓扑尚未选择。其根本优先级顺序仍可作为候选计划参考，但不构成实现授权。必须用当前 Owner 分支刷新 F/D/P Pin，并重新运行依赖/优先级分析，之后才能将 DAG 视为当前版本。

### 3.4 评估裁决

R/X/F/D/P 是可供审查的分析证据，不是已合并的规范基线，也不是独立人类 Owner 批准。相关 PR 均仍是 OPEN Draft，均未合并。历史评估基线不能替代当前 main 或当前 Owner 分支 HEAD。

## 4. 当前 Owner 分支快照与选定规范源读回

以下为本轮观察到的实时分支 HEAD。它们仅是本报告的不可变快照；后续任何 Push 都会使当前性声明失效。

| Owner | 分支 HEAD | 已读取的选定精确源 Blob | 当前解释 |
|---|---|---|---|
| A 集成 | `review/a-b-to-a-currentness-reconciliation-2026-11-17` @ `26fd171f558540cb762f9dcad948db54db866fe3` | Phase 4 报告 `049807f4f03a536eb714481362b1ada3637456c4` | 有用但以 main `8c0c5b1...` 为基线；必须刷新至 `ca69d50...` 并纳入 H 1.2.15 当前证据。 |
| B | `session-b-domain-model-phase3` @ `2faf8ec38f14dba49e7263d7a60804dae1a74ee2` | ADR `a1024938ff5baba069cf128c69496a44e143330c`；规范模型 ADR `df77e4a93cb8fef689ae7c828888d960cbf381d6` | 两份文件均明确 ADR-BLOCKED。B 仅能提出候选建议，无权代表 Architecture Governance 作出决策。 |
| C | `session-c-agent-integration-2026-11-16` @ `78fd99c0ea4c90dc989eef19f079c8d18e2e1468` | H 1.2.15 精确复审 `c5ff68814be49ec5e6e2c081004e7fa058d276fa`；CSubmitOutcome 1.0.1 `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda`；Storage Anchor 复审 `9e280ff6b3850871de118186b03d4831a5c259e9` | 有条件接受 1.2.15 Schema Shape 候选；尚未审查 Validator/CI。 |
| D | `session-d-memory-brain-2026-11-16` @ `194c4c8d64972547cdbcf3fe64bd806c4d1d6a2f` | Publication Participant/Terminal 合同 `17e53890dd6cce9bea9eacc1be2e64b0ef55ac78`；Storage Anchor 复审 `cb1e71730c6fd1fe5eed5c643d2fd59eceba008a` | D 合同仍为角色提案；D 接受精确基线 Anchor 作为排序基底，但 Row Schema、完整依赖分页、迟到发现证明和独立人类批准仍 OPEN。 |
| E | `session-e-memory-compiler-2026-11-16` @ `ee098e14747d9915de5b3efb63b3a8dd77f670ed` | Publication Orchestration/Retry/Recovery `475fee41e5eea527af4edefbfe88c58c86967d0a` | E 角色提案；D/I/Storage 精确 API 和独立 Owner 批准仍 OPEN。 |
| F | `session-f-memory-runtime` @ `1908ce4d233b20f7cafd00cb679affd01bd15174` | Local Lifecycle `29e9504c75d737c2dd200ebc3306eda555f0b0ac`；Forget Suppression `ce59252dbbdc5d10d016704797e9ba12d5a941bd` | F 是投影/消费者，不是 Canonical Authority；本地提案明确跨 Owner 接口和实现仍 OPEN / NOT VERIFIED。 |
| G | `session-g-memory-context` @ `3367438f7b6ba5fa1b7d7540a0fd03a72bbebdbe` | Applied/Forget Reconciliation `aa3afa73d8a76cc6f025839c52bfbff6a983046a`；Local Lifecycle `c1de241ec69834377d9b0e24aa4770a809796d4b` | G 拥有 Context 侧 Applied，不拥有 Provider Truth 或 Canonical Memory；C/G/H 跨 Owner 接口仍 OPEN / NOT VERIFIED。 |
| H | `session-h-bmcp-protocol` @ `cba9e5ccf9ea4d116d5868369595cd014b18b26a` | Unified 1.2.15 Schema `860fc4cec658db7d2703cd6adf72aa31a2723f6d`；Mapping `2dc30f193d9c4f4bdc05ca4c137103687db28924` | 1.2.15 是 Schema/Mapping 候选；无 Validator/CI 声明，也未冻结。 |
| I | `session-i-security-governance-2026-11-16` @ `d3d680dee795c0adf8af306ac549e4c3a21438ba` | I36-GOV 提案 `33cc37eb19c1ce1e1125b7db68ad6c41f3200abf`；1.2.15 精确复审 `6ba4ce3a93f2adf6f8961d4927d9b87deb9696bf`；Storage Anchor 复审 `f22d31dec3a95f094c2942ab816c830f007e830e` | 仅接受 Schema Shape 作为 Trust-Carrier 候选；I 注册、Trust Root、Key Status、Custody、Anti-Rollback 与治理仍 OPEN。I36-GOV-01..10 仅是提案，未批准、未生效。 |
| Storage | `session-storage-consistency-forget-atomicity-2026-11-16` @ `830a559bd2f4ec72608f5a51e1a0b43779f2b989` | v3.3.2 Manifest `5c614375e10698e4931d83deb57d20321445e068`；Topology ADR `bb544ba2f346bdc130d524bd5c7310d86f367988` | v3.3.2 绑定 H 1.2.14，而非 1.2.15；要求 A 精确复审；未联合接受、未冻结。 |

### 4.1 Option A 修正——不得继续沿用过时的“拓扑未选择”措辞

Storage ADR Blob `bb544ba...`：
- §7 将早期“未选择方案”标为历史状态，并明确其在 L1 已被后续内容取代。
- §8.1 选择 Option A 作为 v1 规范逻辑拓扑。
- §8.6 声明 L1 已由 ADR 关闭。
- §8.6/§8.7 保留 L4 OPEN：实际 DB 引擎/配置、部署、Operator、HA/PITR、旧主隔离、权威读路径、Restore 连续性和物理故障演练。

D、I、C 均读取了同一个精确 ADR Blob，并在各自权威边界内接受：
- D Blob `cb1e717...`：接受其作为 D Fence/Participant 排序基底。
- I Blob `f22d31d...`：接受，但严格保持 PolicyDomain 分离。
- C Blob `9e280ff...`：接受，同时保持 C Sequencer/Outcome 分离。

这些均是委托 Owner 角色复审，不是独立人类 Owner 签名。A-01..A-05 修订提案仍 NOT ADOPTED。因此正确状态是：**L1 Option A 已选；A-01..A-05 与集成证明仍 OPEN；L4 物理实现仍 OPEN**，而不是“拓扑未选择”。

### 4.2 H 1.2.15 / C / I / Storage 精确版本不一致

- H 1.2.15 Schema Blob `860fc4...` 与 Mapping Blob `2dc30f...` 是新的不可变候选工件。
- C 复审 Blob `c5ff688...` 有条件接受 Schema Shape，并明确尚未审查 Validator/CI。
- I 复审 Blob `6ba4ce...` 仅接受结构 Carrier；I 注册、Trust Root/Key、Sequence Registry 和生产验证仍 OPEN。
- Storage v3.3.2 Blob `5c6143...` 仍绑定 H Unified 1.2.14 / wire 1.3.0 和旧 Mapping `1cbe74...`，没有绑定 H 1.2.15。
- 因此 v3.3.2 不能作为 H 1.2.15 的当前同 Bundle Manifest。H 必须先稳定 Provider Outcome 与 Integrated Authority-Join 两种不同 Mapping/Validator；C 必须审查精确 Integrated Mapping 和 Validator/CI；I/D 必须复审各自精确接口；Storage 再发布后继 Manifest；A 最后读回同一个 Bundle。不得从 Schema Shape 接受推断整体采纳。

## 5. PR 审计与基线时效

以下状态来自实时 PR 元数据。本次审计时均未合并。

| PR | 用途 | Base SHA / Ref | Head SHA | 状态 |
|---|---|---|---|---|
| #46 | F/D/P 工程规划 | `b372b62...` | `8b9ff8e...` | OPEN / DRAFT |
| #48 | R 全系统风险 | `b372b62...` | `cfcc8f2...` | OPEN / DRAFT |
| #49 | X 复杂度 | `b372b62...` | `131f917...` | OPEN / DRAFT |
| #50 | R SYS-RISK-001 | `b372b62...` | `8542d60...` | OPEN / DRAFT |
| #51 | Phase B 协议对齐 | Phase 2 分支 @ `4f3181f...` | `e1f0263...` | OPEN / DRAFT |
| #52 | B→A 协议/拓扑复审 | `b372b62...` | `2727bd8...` | OPEN / DRAFT |
| #54 | Storage Option A 复审 | Phase 2 协议分支 @ `2119748...` | `208c5e8...` | OPEN / DRAFT |
| #57 | A 最终评估 v3 | `8c0c5b1...` | `d354ec4...` | OPEN / DRAFT |
| #58 | A Clean-base 评估 v2 | `8c0c5b1...` | `dbec207...` | OPEN / DRAFT |
| #59 | A Phase 4 当前性复审 | `8c0c5b1...` | `26fd171...` | OPEN / DRAFT |
| #60 | A current-main 最终评估 | `8c0c5b1...` | `d476db8...` | OPEN / DRAFT |
| #61 | A B-02 / H 1.2.15 差异复审 | `8c0c5b1...` | `4726d93...` | OPEN / DRAFT |

PR #57–#61 均以 `8c0c5b1...` 为 main base；最终 main 已为 `901e38b...`，提交历史领先两个提交，但文件树与旧 base 完全相同。它们的 Base Commit 在历史上较旧，尽管当前文件树没有净内容差异。PR #63 创建时的 Base SHA 为 `901e38b...`，仅包含两份 G1 审计文件。PR #51/#54 以审查分支为 base，是堆叠 PR，不是直接以当前 main 为基线。本审计未重定向、合并或关闭任何现有 PR。

## 6. Issue 审计

| Issue | 状态 | 当前证据解释 |
|---|---|---|
| #3 C/G/H Applied | OPEN | 存在带例外的候选决策；H 1.2.15 Schema Shape 不会冻结 Validator/Applied Transport 或 Provider Side-effect Truth。 |
| #4 Global Inventory / 外部依赖 | OPEN | Inventory、Backup/Export/Restore 覆盖和 Global Forget Completion 仍未解决。 |
| #5 I36-GOV-01..10 | OPEN | 十项治理决策仍全部阻塞；提案不等于批准。 |
| #7 Runtime Repo / 责任工程 Owner | OPEN | Issue 中仍未指定 Canonical Runtime Repository 和 Accountable Engineering Owner。 |
| #10 JF-10 | OPEN | Gate A 仍 PARTIAL PASS / OPEN；Gate B 持久化 COC 与 Gate C 确定性物理故障活动仍阻塞。 |
| #25 D/E/I/Storage Publication Atomicity | OPEN | Owner 合同与候选测试存在；完整集成 Race/Crash/Restore 证明及物理符合性仍开放。 |
| #29 HRC / RecoveryJoin / Topology | OPEN | 候选/参考模型证据有明确边界，不能证明生产 COC Quorum、实时 Owner Ledger、物理拓扑或完整故障恢复。 |
| #43 全系统收敛 | OPEN | 最新 A 评论记录 G1/G6 PARTIAL、G2–G5 BLOCKED、G8 NOT READY。Issue 正文仍保留较早的“Storage topology ADR-BLOCKED”措辞；应更新为区分 L1 已选与 L4 未完成。 |

## 7. G1 裁决与关闭标准

**G1 = PARTIAL。** 本次已完成：
- 核实用户指定 SHA，并审计至当前 main 的单提交差异；
- 枚举并读取唯一新增文件；
- 重新读取选定 R/X/F/D/P 报告，识别其 main/Owner 快照过时问题；
- 重新 Pin 高风险 Owner 工件，发现 H 1.2.15 与 Storage v3.3.2 不匹配；
- 读取相关 PR 与 Issue 元数据/状态。

G1 要通过，仍需：
1. 将 R/X/F/D/P 刷新到实际 main HEAD 和当前 Owner HEAD；修正 R/X 对 Option A L1 已选、L4 未完成的描述。
2. 对每个关键 Owner 工件记录 branch HEAD + path + Blob，并读取规范正文；消费者复审必须对照同一精确版本。
3. 稳定 H 1.2.15 Provider Outcome 与 Integrated Authority-Join Mapping/Validator/Test 源，并取得精确 C/H/I/D 复审。
4. Storage 发布绑定上述精确工件的后继 Manifest；所有必要 Owner 审查同一个 Bundle；A 重新读回。
5. B Fact/Claim 由指定权威作出正式决策；否则继续显式阻塞，不得冻结下游 Schema。
6. 由授权治理机构提供 I36 治理和封闭世界 Inventory 批准。
7. 独立核验 B5/G6 双语对等，不能从翻译完成或审计文件存在推断通过。
8. 将 Issue #43 和 A 当前基线报告更新到最新 main SHA。

## 8. 最终治理裁决

- 总体：**DEFERRED**。
- 架构状态：**ARCHITECTURE_NOT_READY**。
- G1：PARTIAL。
- G2–G5：BLOCKED。
- G6：PARTIAL。
- G7：仅有 A 候选集成裁决；Owner 批准仍须独立取得。
- G8：NOT READY。
- 不进行架构/Schema/技术冻结。
- 未建立实现就绪或验证就绪。
- 未获生产授权。
- 不合并 PR、不关闭 Issue、不解除 Gate、不部署、不激活生产。

本审计只更新证据记录，不修改 main 或任何 Owner 分支，不采纳未批准的 Storage 修订，也不把委托角色复审转换成独立 Owner 批准。
