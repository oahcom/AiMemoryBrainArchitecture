# Session 4 — R/X/F/D/P 当前源证据对账与刷新
# Session 4 — R/X/F/D/P Current-Source Reconciliation and Refresh

- 报告 ID：A-RX-FDP-REFRESH-003
- 审查日期：2026-11-17
- 仓库：`oahcom/AiMemoryBrainArchitecture`
- 用户指定基线：`8c0c5b11abf56a6f580fcf2a99c8043d3057da4f`
- 最终观察到的 main HEAD：`b3c666e67982cb3d3374e759cfb6552c7765aacb`
- 两个提交的 main Tree SHA：`7096e0bc3fdc9a390fccff388f9261522fa424f2`
- 审查分支：`review/session-4-a-rx-fdp-currentness-refresh-2026-11-17`
- 状态：**以下精确绑定工件的当前源对账已完成；系统级批准与 G1 完成尚未成立**
- 权限：仅 A 集成审查。R/X/F/D/P 是分析角色，不是独立人类 Owner 签署。

## 0. 执行裁决

**R/X/F/D/P 仍可作为分析输入，但原始报告不是当前 main 基线，不能被引用为已重新基于当前 main 审查。** R 已在 §14 加入针对 R-01 的定向修正，承认 Storage Option A 在 L1 已选定；X 与 F/D/P 仍将 `b372b62...` 作为 main 基线。PR #50、#49、#46 仍为基于该历史 SHA 的 OPEN Draft PR。

刷新后的系统图景：

1. 当前 Storage ADR 已选择 Option A 作为 **L1 逻辑拓扑**：每个 Canonical Memory authority 一个可串行化事务域。该选择不是 D/Storage 联合批准，也不证明 L3 竞态行为或 L4 物理引擎/部署符合性。
2. B Fact/Claim 仍为 **ADR-BLOCKED**。D/E/I/Storage Phase 3.7/3.8 工件仍是提案或候选合同，不是精确版本的联合批准和实现合同。
3. I36-GOV-01..10 仍为治理阻塞；当前治理登记表明确说明，未取得必要外部批准前，任何政策决议均不生效。
4. H Unified 1.2.15 已存在于 H 当前分支；C 已在附带 C 自有语义条件的情况下接受其 Schema Shape。C 明确指出 Validator/CI 尚未复审。Storage v3.3.2 中绑定的 H 60 项测试证据属于 H 1.2.14，而非 1.2.15。
5. Storage v3.3.2 仍是绑定 H 1.2.14 / C 1.0.1 的精确版本 Manifest，并明确要求 A 对 v3.3.2 重新审查；它没有绑定 H 1.2.15。统一 Bundle 进入可接受状态前，必须发布后继 Manifest 并由 Owner 精确复审。

**整体架构裁决仍为 DEFERRED / ARCHITECTURE_NOT_READY。G1 为 PARTIAL，不是 PASS。**

## 1. Main 基线与差异

用户指定 SHA `8c0c5b11abf56a6f580fcf2a99c8043d3057da4f` 与最终观察到的 main HEAD `b3c666e67982cb3d3374e759cfb6552c7765aacb` 具有相同的 Git Tree SHA：`7096e0bc3fdc9a390fccff388f9261522fa424f2`。在 `901e38b...` 之后，main 又推进了四个提交；最新提交 `b3c666e...` 撤回了一份误加入的 R/X/F/D/P 说明。更早的 `ca69d50...` / `901e38b...` 也曾新增并撤回一份仅供研究使用的 B 双语对等审计。这些中间新增均已检查，但最终都不在当前 main 中。因此，用户指定基线到当前 main 的最终净文件差异仍为零。

这不意味着 Owner 分支已经当前化或获批。Main 文件树相同只是源基线事实，不是 Owner 采纳证明。

## 2. 分析报告精确版本与局限

| 角色 | 现有 PR | 分支 HEAD | 报告路径 | Blob | Main Base | 当前性 |
|---|---:|---|---|---|---|---|
| R | #50 | `8542d608ccfe6747c5f6171a2a38d325f10a628c` | `reviews/architecture/SYS-RISK-001.en.md` | `4067005a65fe528aa7d5fc43ff5be79eb0adaa53` | `b372b62...` | 含 §14 R-01 修正；不是完整当前 main 重基 |
| X | #49 | `131f91743bd506517ee354d58c277501ca447929` | `reviews/complexity/architecture-complexity-assessment.en.md` | `c509120644d6f7c7223decf3f9f0ee33b0548bb7` | `b372b62...` | 历史源基线；需要定向刷新 |
| F/D/P | #46 | `8b9ff8efa92a88dacc8f97b5faba5918fe5d2edc` | `reviews/engineering-planning/2026-11-17-session-3-engineering-planning-en.md` | `081610b1734ec08dc7c35c75fae1cae3ca713be4` | `b372b62...` | 历史源基线；源登记表明确说明未穷尽重绑 Owner 分支 |

中文对应文件也已读取：R Blob `5fcc55636619d1df373f4caa0afa7db869e4fb70`；X Blob `981a376ddf283ace1e891795c813b17ac4aa3d8b`；F/D/P Blob `834dc39998342dc2f292fe1dfed411768b3ed156`。

三个 PR 均为 OPEN / DRAFT / 未合并。旧 Base 不会自动使其分析结论全部失效，但在采纳前必须针对当前精确源重新验证。本报告不改写或重定向这些 PR。

## 3. 当前 Owner 源精确快照

本次刷新从 GitHub 分支元数据读取以下 HEAD：

| Owner | 分支 | 精确 HEAD | 相关精确源 / Blob |
|---|---|---|---|
| B | `session-b-domain-model-phase3` | `2faf8ec38f14dba49e7263d7a60804dae1a74ee2` | `02-domain-model/ADR-001-fact-claim-semantics.md` — `a1024938ff5baba069cf128c69496a44e143330c` |
| C | `session-c-agent-integration-2026-11-16` | `71047cdb51139ca4080ac67f451e38a48698859d` | Phase 3.8.26 H 1.2.15 Schema 复审 — `c5ff68814be49ec5e6e2c081004e7fa058d276fa` |
| D | `session-d-memory-brain-2026-11-16` | `194c4c8d64972547cdbcf3fe64bd806c4d1d6a2f` | Phase 3.8 Publication Participant/Terminal 合同 — `17e53890dd6cce9bea9eacc1be2e64b0ef55ac78` |
| E | `session-e-memory-compiler-2026-11-16` | `ee098e14747d9915de5b3efb63b3a8dd77f670ed` | Phase 3.7 生命周期提案 — `4fb9e58511941f59b4d777336f8f85ad88ecccf1` |
| F | `session-f-memory-runtime` | `1908ce4d233b20f7cafd00cb679affd01bd15174` | 已读取分支 HEAD；不推断新的 F Owner 批准 |
| G | `session-g-memory-context` | `3367438f7b6ba5fa1b7d7540a0fd03a72bbebdbe` | Applied/Forget 合同 — `aa3afa73d8a76cc6f025839c52bfbff6a983046a` |
| H | `session-h-bmcp-protocol` | `0d36324457e39bd50ad56ae902d477c4ea765b61` | Unified 1.2.15 Schema — `860fc4cec658db7d2703cd6adf72aa31a2723f6d`；Mapping — `2dc30f193d9c4f4bdc05ca4c137103687db28924`；本地 Validator — `90a2d4b6f5b05590e3e0a7daecb5a01d9bf525c0` |
| I | `session-i-security-governance-2026-11-16` | `0d071bf1ee7cc71912398c6ae57e4496e08f44ab` | Phase 3.7 Enforcement 提案 — `e3b1b5d99eb36ac0b395854d8c19287d2b64b752`；治理登记表 — `f5fd2558c657f4ef49396a7a00cdbcd0f226f853` |
| Storage | `session-storage-consistency-forget-atomicity-2026-11-16` | `830a559bd2f4ec72608f5a51e1a0b43779f2b989` | Option A ADR — `bb544ba2f346bdc130d524bd5c7310d86f367988`；v3.3.2 Manifest — `5c614375e10698e4931d83deb57d20321445e068`；Phase 3.7 实现提案 — `2ab899ee37a18ae6c8f2f64dbb82ad6499842060` |

分支 HEAD 只标识当前候选源快照，不构成 Owner 批准、分支集成或运行时实现证明。本次未读取所有 Owner 分支的每一个文件；此处绑定的是与下述结论直接相关的精确工件。

## 4. R — 全系统风险刷新

R 现有 §14 已修正“尚未选择 Storage 拓扑”的过时说法。针对当前精确 Storage ADR Blob，该修正仍然有效：

- **L1：** Storage ADR §§8–8.7 选择 Option A：每个 `BrainAuthorityRef` 对应一个逻辑可串行化事务域和持久化 `CanonicalAuthoritySerializationAnchor`。
- **跨 Owner D 采纳：** 未证明。当前 D Phase 3.8 工件明确标记为 D-role proposal；精确 Owner 批准、可调用 API 和符合性仍 OPEN。
- **L3：** 尚未证明 ProducerWork/Fence、依赖登记、PublicationParticipant 和最终 Visibility 的双向串行顺序，也未证明 I 撤权、重试、ACK 丢失和恢复场景。
- **L4：** 实际数据库/构建/配置、权威读取路径、HA/PITR、旧主隔离、运维责任人以及物理崩溃/故障切换/恢复符合性仍 OPEN。

因此，基础风险仍为 Critical / OPEN，但原因必须准确：不是“没有 L1 选择”，而是**已有 L1 选择，但缺少联合采纳、可执行逻辑证明和物理符合性**。

其他关键风险仍存在：
- B Fact/Claim 权威与 Canonical 语义仍 ADR-BLOCKED。
- 跨衍生物、索引、缓存、Adapter、副本、备份与 Restore 的 Forget/不复活尚未证明。
- I 治理决议和封闭世界 Producer/Recipient/Backup Inventory 尚未解决。
- C/G/H Applied 必须保留最终不可变请求身份、实际 Provider Submit 证据、逐请求 G Applied Predicate、迟到证据及撤权/Fence 当前性。
- Issue #7 尚未指定运行时仓库和负责工程 Owner。

## 5. X — 复杂度刷新

X 原有评级仍为 **High complexity; controllability not proven（高复杂度；可控性未证明）**。其基线已过时，但当前 Owner 工件继续印证了原有状态空间驱动因素。

最高复杂度集中于：

1. D/E/Storage Admission、Fence、完整依赖登记、私有暂存与最终 Visibility 排序。
2. Canonical、Index、Context、Adapter、副本、备份与 Restore 之间的 Global Forget 扇出和不复活。
3. Storage/COC/JF-10 持久化 Participant、Quorum、Same-GID Recovery、Failover 与 Anti-Rollback。
4. C/G/H Final Request、Provider Side-Effect 证据、Gateway Attestation、Applied 幂等及历史有效性与当前有效性的区分。
5. I Authorization Epoch、撤权线性化、Issuer Trust、跨 Scope/Environment 治理与 Global Completion。
6. B Typed Domain Reference 和 Fact/Claim 语义权威。

对简化预算作必要修正：**不能再把 Option A 的 L1 拓扑决策算作缺失项**。剩余复杂度在于 D/Storage 采纳、精确 Row/Transition 所有权、同一 Anchor 的事务实现、L3 确定性交错证明和 L4 物理证明。反过来，H 1.2.15 Schema 与本地 Validator 代码的存在只增加了候选工件；在 Validator/CI、I Trust 注册和 C/G/H 精确接受闭环前，不会减少证明负担。

复杂度控制：
- 保留 Accepted、Compiler Completion、Canonical Commit、Index Applied、Context Applied、Provider Outcome 和 Forget Completion 的不同语义。
- 不要为每个概念状态都新增独立服务、队列、数据库或版本命名空间。
- 首个可执行切片保持狭窄和本地化；生产 Vector/ANN、Reranking、高级 Consolidation 和分布式扩展继续延期。
- 每个 Authority Boundary 都必须有可追溯证明对象，并明确幂等与终态语义。

## 6. F — 工程可行性刷新

F 的总体结论仍为 **FEASIBLE_WITH_CONDITIONS / PARTIALLY VERIFIED（有条件可行 / 部分验证）**，不是已具备实现条件。

当前正向证据：
- Rust 模块化单体/架构定义路径原则上仍合理。
- H 1.2.15 Schema 和本地 Validator 实现已作为候选工件存在。
- H 1.2.14 Reference Ingress Bundle 在 Storage v3.3.2 中有受限的 60 项 CI 记录。
- 候选/参考模型测试和合成 Harness 可支持有限准备工作。

硬性可行性阻塞：
- Issue #7 仍 OPEN：未指定正式运行时仓库、负责工程负责人、可复现构建/CI 和部署/运维映射。
- B Fact/Claim ADR 仍 ADR-BLOCKED。
- D/E/I/Storage 原子 Producer Admission、完整依赖登记、Visibility 线性化及精确跨 Owner 采纳仍 OPEN。
- Storage L1 Option A 已选择，但 L4 物理数据库和部署证明仍 OPEN。
- C/G/H Final Request Applied 合同及 I Trust 注册尚未闭合。
- I36-GOV-01..10 仍 GOVERNANCE-BLOCKED。

只允许有限准备工作：合成基准、Rust Workspace/Toolchain 探索、候选数据库能力探测、参考模型/故障 Harness、符合性测试脚手架、双语与源版本 Pin 自动化。不得将这些工作描述为受保护路径实现、生产符合性或 Gate 通过。

## 7. D — 依赖与关键路径刷新

依赖顺序得到确认：

`B 领域语义 + I 治理/身份 + D/E Producer/Fence/Lineage`
→ `Storage L1/L3/L4 序列化与 Visibility 证明`
→ `C/G/H Final Request 与 Applied 证据闭环`
→ `最小 Durable Canonical 垂直切片`
→ `授权 Retrieval/Context/Adapter`
→ `Recovery、Restore、运维与生产符合性`。

这是偏序关系，不要求所有准备任务严格串行。合成 Benchmark、工具链探索、候选数据库探测和双语自动化可在明确非生产约束下并行。

不得颠倒依赖关系，在 Canonical Truth、Forget、Authorization 和 Durable Visibility 之前先建设 Vector/Reranking 功能。

## 8. P — 根因优先级刷新

| 优先级 | 工作项 | Gate 条件 |
|---|---|---|
| P0-01 | 指定正式运行时仓库和负责工程 Owner（Issue #7） | 记录仓库、负责人、维护者、构建/CI 和部署边界 |
| P0-02 | 关闭 B Fact/Claim 语义权威 | 具有精确批准 Hash 和 Typed Consumer Mapping 的正式 ADR 决议 |
| P0-03 | 关闭 I36 治理与封闭世界 Inventory | I36-GOV-01..10 批准及签名 Inventory/Exception 证据 |
| P0-04 | 关闭 D/E/I/Storage 原子 Admission、Fence、Dependency 和 Visibility 合同 | 同版本 Owner 决议、Row/API 所有权和竞态/故障符合性 |
| P0-05 | 证明 Storage/COC/JF-10 物理能力 | 实际引擎/配置、持久化 Prepared-XID/等价能力、Same-XID Recovery、HA/Failover、权威读取和 Restore 证据 |
| P0-06 | 关闭 C/G/H Final Request Applied 证据 | 精确 C/G/H Schema、Validator/CI、Signer/Profile Trust、幂等、迟到证据和撤权行为 |
| P0-07 | 构建最小 Durable Canonical 垂直切片 | 仅在 P0-02 至 P0-05 之后，且保留受限授权和 Forget 语义 |
| P0-08 | 安全 Retrieval/Rebuild | 当前 I Authorization + D Fence/Lineage + Index/Context 新鲜度证明 |

P1：Event/Ingress、Compiler、Canonical Memory、Retrieval、Context、Adapter 和 Applied 集成，须满足其 P0 依赖后推进。

P2：Hybrid/Vector Retrieval、Reranking、Entity Resolution、Consolidation 和 Conflict Resolution。

P3：高并发、分布式扩展、性能优化和规模化运维。

## 9. C/G/H 与 Storage 精确版本对账

### 9.1 H 1.2.15 候选

当前 H Schema Blob `860fc4...` 和 Mapping Blob `2dc30f...` 存在于 H HEAD `0d363244...`。H 本地 Validator Blob `90a2d4...` 明确说明：它不认证外层 BMCP Envelope、Transport Principal、Channel Binding 或 Replay；它只是通过注入 Authority Callback 的集成接口，缺少 Callback 时返回 UNKNOWN。

C 精确复审 Blob `c5ff688...` 在附带 C 自有语义条件的情况下接受 1.2.15 **Schema Shape**，但明确标记 **VALIDATOR/CI NOT YET REVIEWED**。这是委托角色的 C 复审，不是独立人类 C Owner 签名。

### 9.2 Storage v3.3.2 版本不匹配

当前 Storage v3.3.2 Manifest Blob `5c6143...` 明确绑定：
- H Unified Schema **1.2.14** Blob `09fcd1...`；
- CSubmitOutcome 1.0.1；
- 60 项 H Reference Ingress 测试证据及相关 C/I 复审 Pin；
- Option A ADR Blob `bb544b...`。

它**没有**绑定 H 1.2.15。Manifest 中的 60 项 CI 结果是针对 1.2.14 精确 Bundle 的证据，不是 H 1.2.15 的证据。Manifest 本身要求 A 对 v3.3.2 精确复审，并明确它尚未联合接受/冻结。

下一步必须是：H 发布精确 1.2.15 Validator、Test 和 Workflow 证据；C/I 完成精确语义/Trust 复审；Storage 发布绑定这些精确 Blob 的后继 Manifest；D 和其他受影响 Owner 只复审该精确后继 Bundle；随后 A 对同一个 Bundle 复审。任何前序复审都不会自动转移。

## 10. Issue 与 Gate 证据

本次直接刷新 Issue 元数据：
- #43 全系统收敛 — OPEN。
- #7 运行时仓库/负责工程 Owner — OPEN。
- #25 D/E/I/Storage 原子 Producer Admission 与衍生物 Visibility — OPEN。
- #29 HRC/RecoveryJoin 与物理拓扑证明 — OPEN。
- #3 C/G/H Applied 合同 Owner 决策 — OPEN。
- #4 I 外部治理/Inventory 决策 — OPEN。
- #5 I36-GOV-01..10 正式治理批准 — OPEN。
- #10 JF-10 物理 Prepared-XID/COC/Recovery 证明 — OPEN。

当前控制状态仍为：
- G1 PARTIAL，不是 PASS。
- Gate A PARTIAL PASS / OPEN。
- Gate B BLOCKED。
- Gate C BLOCKED。
- 未授权生产。

## 11. 更新后的发现与关闭条件

| ID | 发现 | 严重性 | 是否阻塞 | Owner | 关闭证据 |
|---|---|---|---|---|---|
| RXFDP-01 | R/X/FDP 旧 Main 基线尚未完整刷新；不能作为当前 Main 批准引用 | High | 是，阻塞 G1 完成 | A/R/X/F/D/P | 精确源登记、双语对等和当前 Main 复审 |
| RXFDP-02 | Option A 仅在 Storage L1 已选择；D 采纳/L3/L4 仍开放 | Critical | 是 | D/Storage/I | 联合精确合同、竞态/故障套件和物理证明 |
| RXFDP-03 | B Fact/Claim ADR 仍阻塞 | Critical | 是 | B / Architecture Governance | 带精确 Hash 的正式权威决议 |
| RXFDP-04 | I36 治理/Inventory 未解决 | Critical | 是 | I / 外部治理机构 | 签署的 I36-01..10 与封闭世界 Inventory 证据 |
| RXFDP-05 | H 1.2.15 Schema Shape 有条件接受，但 Validator/CI/Trust 未闭环 | High | 是，阻塞 Applied 闭环 | H/C/I | 精确 Validator 测试、可信签名 Profile 和 C/I 接受 |
| RXFDP-06 | Storage v3.3.2 绑定 H 1.2.14，而非 1.2.15 | High | 是，阻塞精确 Bundle | Storage/H/C/I/D/A | 后继 Manifest 精确 Blob Pin 与 Owner 复审 |
| RXFDP-07 | 运行时仓库和负责工程 Owner 未指定 | Critical | 是，阻塞实现准入 | 项目权威方 | Issue #7 正式答复和实现追溯映射 |

任何涉及领域真值、Canonical Authority、Authorization、Forget、Atomicity、Durable Visibility 或强制 Gate 证明的问题，都不能作为非阻塞条件接受。

## 12. 明确边界

本报告：
- 不批准任何 Owner 提案；
- 不把委托角色模拟转换为独立 Owner 批准；
- 不冻结架构、Schema、技术或协议；
- 不授权受保护路径实现、部署或生产；
- 不合并 PR、不关闭 Issue、不解除 Gate。

**A 最终集成裁决：DEFERRED / ARCHITECTURE_NOT_READY。G1 仍为 PARTIAL。**
