# A Owner 源刷新 004——Owner 实时引用、合同 Blob、CI 与 Gate 裁定

- 审查编号：**A-OWNER-SOURCE-REFRESH-004**
- 权威角色：A / 首席系统架构权威
- 状态：**只读源审计 / 集成裁定**
- Main 基线：`main@e52594f181d2edb77448adcfed64a0fbdffaf3aa`
- 审查日期：2026-11-18
- 范围：B/C/D/E/F/G/H/I/Storage 实时分支引用、关键规范/候选合同 Blob、相关 PR、有界 CI 证据、H/C 文件树完整性恢复和 Gate 状态。
- 本报告不修改任何 Owner 合同，不批准 ADR，不合并 PR，不释放 Gate，也不授权实现或生产活动。

## 1. 执行裁定

**总体状态：DEFERRED / ARCHITECTURE_NOT_READY。**

实时 main 仍为 `e52594f181d2edb77448adcfed64a0fbdffaf3aa`。本轮通过各分支与自身比较，独立解析了九个 Owner 分支的精确 HEAD。随后从指定分支读取关键合同文件并记录其 Blob SHA。

H/C 文件树完整性事件在**源文件树恢复层面已基本对账**：
- C 的截断事故快照已恢复为 136 个 Blob 的分支，当前 C HEAD 仍为 `88992da...`。
- H 的截断事故快照在 `4e65a2...` 恢复（215 个 Blob），随后推进至当前 HEAD `6608cde...`（216 个 Blob）。
- H 从测试提交 `4e65a2...` 到当前 `6608cde...` 仅变更两个文档文件；Schema、Validator、Tests 和 Workflow 未变。
- 这解决了“缺失的 H/C 文件是否恢复”这一狭义问题，但**没有**解决独立 Owner 批准、C/H Wire Mapping、生产 Trust、Durable Replay 或端到端集成问题。

本轮还发现 Storage 的精确 Option A ADR 存在新的阻塞矛盾：文件头称 L1 已选择 Option A，但第 3 节又称 ADR 未选择任何方案，Option A 只是优先候选。Storage v3.3.2 Manifest 却重复了“已选择”的解释。在 Storage Owner 通过自己的权威源解决矛盾前，L1 必须标记为 **CONFLICTED / NOT SAFE TO FREEZE**，不能视为已无歧义选定。

其他未变化的阻塞项：
- B Fact/Claim 仍为 ADR-BLOCKED。
- I36-GOV-01..10 仍为 GOVERNANCE-BLOCKED；没有记录生效的治理批准。
- D/I/Storage Phase 3.9 终态化文档仍是提案；没有同一精确版本的联合 Owner 接受证据。
- H-ADE-001..003 仍开放，并阻塞受保护的 Applied/Replay 路径。
- Issue #7 仍 OPEN；G3 实现准入仍 BLOCKED。

## 2. 冻结 Main 基线与分支图

| 引用 | 精确 SHA / 比较 | 相对 Main 的 Compare | 含义 |
|---|---|---:|---|
| main | `e52594f181d2edb77448adcfed64a0fbdffaf3aa` | 与自身 identical | 当前审计锚点 |
| B `session-b-domain-model-phase3` | `2faf8ec38f14dba49e7263d7a60804dae1a74ee2` | ahead 42 / behind 58；报告 25 个变更路径 | 已分叉的 Owner 分支 |
| C `session-c-agent-integration-2026-11-16` | `88992da30331121b81cf2773acab11d921daf281` | ahead 169 / behind 58；报告 106 个变更路径 | 已恢复的当前 Owner 分支 |
| D `session-d-memory-brain-2026-11-16` | `194c4c8d64972547cdbcf3fe64bd806c4d1d6a2f` | ahead 109 / behind 66；报告 60 个变更路径 | 当前 D 源快照 |
| E `session-e-memory-compiler-2026-11-16` | `ee098e14747d9915de5b3efb63a3b8dd77f670ed` | ahead 88 / behind 66；报告 28 个变更路径 | 分支引用可解析；提交元数据读取异常见下文 |
| F `session-f-memory-runtime` | `1908ce4d233b20f7cafd00cb679affd01bd15174` | ahead 41 / behind 66；报告 23 个变更路径 | 当前 F 源快照 |
| G `session-g-memory-context` | `763b3d31e910db8fd29c6e4dbaff9273b7fb66b8` | ahead 42 / behind 66；报告 24 个变更路径 | 当前 G 源快照 |
| H `session-h-bmcp-protocol` | `6608cde89d959257db612d8ff8080f631333f3f3` | ahead 490 / behind 58；报告 182 个变更路径 | 已恢复的当前 H 源快照 |
| I `session-i-security-governance-2026-11-16` | `0d071bf1ee7cc71912398c6ae57e4496e08f44ab` | ahead 203 / behind 58；报告 105 个变更路径 | 当前 I 源快照 |
| Storage `session-storage-consistency-forget-atomicity-2026-11-16` | `830a559bd2f4ec72608f5a51e1a0b43779f2b989` | ahead 359 / behind 57；报告 87 个变更路径 | 当前 Storage 源快照 |

Ahead/behind 与变更路径数量是相对 main 的 Git 图比较结果，不是合并这些分支的建议。Owner 分支历史已经显著分叉；不得批量合并，也不得仅凭这些数字推断安全集成基线。

**E 引用异常：** self-compare 将 E 分支 HEAD 解析为 `ee098e...`，按分支引用读取 E 合同也成功。但对该 SHA 直接读取提交元数据时，GitHub 返回 422 “No commit found for SHA”。因此分支引用和 Blob 可作为已观察事实；在将提交祖先关系/提交元数据用于证明前，必须由 E 对账该异常。

## 3. 精确 Owner 源清单

Blob SHA 是从实时分支引用读取的精确内容身份。保留源文件自身的 Candidate/Draft 状态；分支存在不代表批准。

| Owner | 分支 HEAD | 关键精确源（路径 — Blob SHA） | 当前源状态 |
|---|---|---|---|
| B | `2faf8ec38f14dba49e7263d7a60804dae1a74ee2` | `02-domain-model/ADR-001-fact-claim-semantics.md` — `a1024938ff5baba069cf128c69496a44e143330c` | **ADR-BLOCKED**；没有具名治理权威、批准人、选定方案或生效决议 |
| C | `88992da30331121b81cf2773acab11d921daf281` | `07-agent-integration/schemas/c-submit-outcome-1.0.1.schema.json` — `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda`；Workflow `.github/workflows/c-provider-outcome-conformance.yml` — `a1f0b8f884f0f294fb3ec96da7c4f11e294e5142` | C Schema 候选和有界符合性；当前 Workflow push filter 漏掉 1.0.1 Schema 路径 |
| D | `194c4c8d64972547cdbcf3fe64bd806c4d1d6a2f` | `03-memory-brain/forget-fence-and-completion-contract.md` — `1f0391bc49d007c44ec74165bd33d37412cc7990`；`03-memory-brain/canonical-memory-store.md` — `6b37c91033fda21f072e2a3bde6f274663b1e76e` | D 规范 Forget 语义已决定；详细记录布局/事务实现仍为候选；Global Completion 归 I 所有 |
| E | `ee098e14747d9915de5b3efb63a3b8dd77f670ed` | `04-memory-compiler/accepted-receipt-and-idempotency-contract.md` — `5ca77a5b48e69afb3bc81429baf538be7dce4d46` | E 候选合同；Storage 实现、D API、H Envelope、I Policy 批准仍开放 |
| F | `1908ce4d233b20f7cafd00cb679affd01bd15174` | `05-memory-runtime/phase-3.6-runtime-forget-suppression-and-invalidation.md` — `ce59252dbbdc5d10d016704797e9ba12d5a941bd`；模型 `tests/anti_resurrection/f_runtime_model.py` — `33fa2ca2dc29771aca241e194f13e078a4f8d774`；测试 — `c2575327a75577923440ef770d42122218a1e091`；Workflow — `c0fac9eff93ca46e466cda5fe04613bd4565e9b3` | F 逻辑运行时安全语义在补充文件中已决定；跨 Owner 接口仍开放；生产实现未验证 |
| G | `763b3d31e910db8fd29c6e4dbaff9273b7fb66b8` | `06-memory-context/phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.md` — `bd297873bc1e593280484a43cb44b56058d9c4ff` | G 自有规范性设计草案；实现未验证；需要跨 Owner 接受；不是独立人工 Owner 签名 |
| H | `6608cde89d959257db612d8ff8080f631333f3f3` | Unified 1.2.15 Schema — `860fc4cec658db7d2703cd6adf72aa31a2723f6d`；Applied Delivery Evidence 1.0.0 Schema — `2ce8776ca5ee5e014b234dc3eb34a7cb7961e608`；Validator — `2f6de24eea737cf75a16ead7495bea4627bb1bb4`；Tests — `bb2bb6c94cc73293f736c6dcd450ab32bffc6ee5`；Workflow — `7bd9bf3a4141d1e239d0f165e2e98fdd25961254` | 已恢复的 Schema/Validator/Test 候选；有界 CI 通过；H-ADE-001..003 仍 OPEN |
| I | `0d071bf1ee7cc71912398c6ae57e4496e08f44ab` | `09-security-governance/global-forget-target-inventory-and-completion-evidence.md` — `9100061fa986fb6676656169de3fcf9fc1c72664`；治理登记表 — `f5fd2558c657f4ef49396a7a00cdbcd0f226f853` | Global Inventory 合同为候选；I36-GOV-01..10 仍 GOVERNANCE-BLOCKED；没有生效 Policy 批准 |
| Storage | `830a559bd2f4ec72608f5a51e1a0b43779f2b989` | Option A ADR — `bb544ba2f346bdc130d524bd5c7310d86f367988`；v3.3.2 Manifest — `5c614375e10698e4931d83deb57d20321445e068` | **L1 状态内部矛盾**；L4 物理引擎/部署仍 OPEN；v3.3.2 尚未联合接受/冻结 |

### 3.1 B——Fact/Claim 仍阻塞

精确 B ADR 写明：
- 正式决策权威：NOT RECORDED；
- 具名批准人：NOT RECORDED；
- 已批准方案：NONE；
- 批准记录：NONE；
- 状态：ADR-BLOCKED。

B 对 Option A 的推荐只是建议，不是决策。D 的 Canonical Memory Store 也独立写明 Fact/Claim 持久化仍 ADR-BLOCKED，并禁止基于任一备选方案冻结 DDL、公共 Schema、稳定跨模块 Wire 字段或不可变 Fact/Claim Identity。

### 3.2 C——Workflow 触发缺陷

当前 C Workflow Blob `a1f0b8...` 监听 1.0.0 Schema 路径，但未监听 `c-submit-outcome-1.0.1.schema.json`。Draft PR #94 只增加了这一缺失路径；其 Workflow 读回 Blob 为 `75e294ab1552f24fde76c3e881ab2cf5e7b791e2`。PR #94 尚未合并，Schema-only Trigger Execution 明确为 PENDING。下文的 19 项测试确实包含 CSubmitOutcome 1.0.1 测试，但不能证明仅修改该 Schema 文件时原 Workflow 能被触发。

### 3.3 H——Applied Delivery Evidence 阻塞项

A 在 PR #98 的精确审查识别出三个开放阻塞项：
- **H-ADE-001：** Strict Parser 使用标准 JSON 解码，未在对象物化前拒绝重复 JSON Key；存在签名消息歧义/Parser Differential 风险。
- **H-ADE-002：** H Validator 合同未明确 CSubmitOutcome 1.0.1 语义 Join；C 不可变记录、Outcome/SideEffect、Final Boundary/Request Digest 和 Lineage 相等性需要版本固定的 Resolver/Verifier 与 C/G 审查。
- **H-ADE-003：** 在披露 Replay Result Reference 前，当前 I Authorization/PermissionEpoch、Key、Audience/Scope 和适用 D Forget Fence 的复核顺序未明确。

这些问题分别阻塞认证生产使用、Full Applied 和 Replay Acceptance。H 的 11 项测试没有关闭它们。

## 4. H/C 文件树完整性事件——精确对账

| 事件 | 精确引用 | 观察到的证据 |
|---|---|---|
| H 事故快照 | `0277a8b9ee63be850acc0b8b1b08625524aaa33b` | PR #91 报告树仅 7 个路径；相对此前 H 快照删除 205、增加 2、重命名 3 |
| C 事故快照 | `a5dff993e5c2928a28deb777c41023cfe923366f` | PR #91 报告树仅 5 个路径；相对此前 C 快照删除 133、增加 2、重命名 1 |
| H 恢复快照 | `4e65a2ee0c6ac1c52a36f5d830ec7685dc4967e6` | PR #92 记录 215 个 Blob；从 H 事故快照 Compare 为 ahead 5 / behind 0 |
| C 恢复/当前快照 | `88992da30331121b81cf2773acab11d921daf281` | PR #92 记录 136 个 Blob；从 C 事故快照 Compare 为 ahead 1 / behind 0；仍为当前 C 分支 HEAD |
| H 当前快照 | `6608cde89d959257db612d8ff8080f631333f3f3` | A/C 源刷新记录 216 个 Blob；在测试恢复快照之后 1 个提交；Compare 仅显示两个 Phase 3.8.24 文档文件变化 |

就文件树恢复和当前引用身份而言，事故已经完成对账。**但这不证明所有 C/H 合同已被接受或具备生产就绪性。** PR #92 仍为 Draft/Open，目标是 `research/tech-reality-001-c` 而非 main。该 PR 记录 C/H Mapping 为 NOT ACCEPTED / NOT VERIFIED、独立人工审查 PENDING、C Agent/Provider/Tool/Brain 端到端测试 NOT RUN。

## 5. 相关 PR 状态与权威边界

| PR | 审查时状态 | 精确范围/裁定 |
|---|---|---|
| #55 | Open / Draft | B 领域研究提案；不是 Fact/Claim 治理决策 |
| #66 | Open / Draft | D Phase 3.9 终态化提案；基线 D 分支 `194c4c8...`，Head `4d1a044...`；报告 19/19 本地 Python 模型测试，不是 GitHub CI 或生产证明 |
| #68 | Open / Draft | I/D 终态化授权提案；基线 I 分支 `0d071bf...`，Head `a71985e...`；需要精确 D/I 决策及 Storage 边界接受 |
| #71 | Open / Draft | Storage Phase 3.9 审查；基线 Storage 分支 `830a559...`，Head `65c0387...`；明确为角色模拟，不是独立 Storage Owner 签名；仅有条件逻辑接受 |
| #91 | Open / Draft | A H/C 文件树完整性事故报告 |
| #92 | Open / Draft；mergeable=false | C-REVIEW-001 恢复与消费方审查；未合并，不在 main |
| #94 | Open / Draft | C Workflow Path-filter 修复；一行变更；Schema-only Trigger Execution 待完成 |
| #98 | Open / Draft | A 对 H Applied Delivery Evidence 的精确审查；H-ADE-001..003 仍开放 |
| #99 | Open / Draft | ARCH-CONVERGENCE-001 源清单；非规范性，需要本次源刷新增量 |

Open/Draft/mergeable 元数据不等于 Owner 批准。同会话角色模拟审查不等于独立人工 Owner 签名。本次审计没有合并上表任何 PR。

## 6. CI 与可执行证据——严格限定范围

| Owner | Run / Commit | 结果 | 证据上限 |
|---|---|---|---|
| B | 未发现领域 ADR 的 CI 证据 | NOT ESTABLISHED | ADR 决策属于治理行为，不是测试结果 |
| C | Run `44129914790`，Commit `88992da...` | **19/19 PASS** | C Schema/加密候选向量；日志包含 1.0.1 测试；不证明 C/Brain 端到端或生产 Trust |
| D | PR #66 报告 19/19 本地 Python 参考模型测试 | **仅本地** | 非 GitHub Actions；不证明 D/Storage/I 物理符合性 |
| E | 未发现当前 HEAD 的精确 CI 证据 | NOT ESTABLISHED | E 合同仍是候选；不得推断实现就绪 |
| F | Run `43961714501`，测试 Commit `f1ba5c...` | **19/19 PASS** | 内存确定性逻辑模型；对当前 F HEAD `1908ce...` 的 Compare 显示晚 9 个提交且仅文档变更；模型/测试/Workflow Blob 未变 |
| G | 未发现当前 HEAD 的精确 CI 证据 | NOT ESTABLISHED | G Applied 合同明确写明实现未验证 |
| H | Run `44130722532`，测试 Commit `4e65a2...` | **11/11 PASS** | H Applied Delivery Evidence 1.0.0 Schema/Semantic 候选；H Recovery Cutoff Run `44130722851` 在同一提交也 SUCCESS；当前 H HEAD `6608cde...` 仅两个文档文件不同 |
| I | Run `43963450717`，测试 Commit `8a6a6e...` | **30/30 PASS** | 内存 Global Inventory/Completion 逻辑模型；当前 I HEAD `0d071b...` 晚 128 个提交，但 Compare 未发现模型/测试/Workflow 路径变化 |
| Storage | Run `43965501810`，测试 Commit `1979863...` | **25/25 PASS** | 内存 Restore High-water 逻辑模型；当前 Storage HEAD `830a559...` 晚 158 个提交，但 Compare 未发现模型/测试/Workflow 路径变化；不证明真实 DB/HA/Restore |

对于 F/I/Storage，“代码树连续性”仅表示比较的提交之间没有修改相关模型/测试/Workflow 路径，不会把旧 Run 变成当前 HEAD 的精确 CI。H 也同理：测试代码未变化，但当前 HEAD 并非实际测试提交。CI PASS 不等于生产证明。

## 7. Storage Option A——阻塞性源文件矛盾

精确 ADR Blob：`bb544ba2f346bdc130d524bd5c7310d86f367988`。

ADR 文件头写明：

> L1 LOGICAL TOPOLOGY SELECTED — OPTION A; L4 PHYSICAL ENGINE/DEPLOYMENT OPEN

但第 3 节写明：

> Therefore no option is selected by this ADR. Option A is the preferred candidate only if the actual deployment proves it; otherwise Option B requires a separate ADR and proof bundle.

v3.3.2 Manifest Blob `5c614375...` 将 Option A 描述为规范 v1 逻辑架构的已选方案，并称其修正了 ADR 状态。但 Manifest 的表述不能替代对精确 ADR 正文矛盾的解决。同一 ADR 还将 T1–T8 全部保持 OPEN，包括 Runtime Identity、D/Storage Row Boundary、Linearization、I Proof、Atomic Outcome、HA/Restore、Read Path 和 Owner Decisions。

**A 裁定：** 在 Storage 发布 Owner 批准的精确 Blob 修正或后继 ADR，并由 D/Storage 对同一范围确认前，不得宣称 L1 Option A 已被无歧义选定。无论如何，L4 物理引擎/部署仍 OPEN。

PR #71 的 Storage Phase 3.9 审查是有条件的，并明确不是独立 Storage Owner 签名。D/I/Storage Phase 3.9 三份提案尚未成为规范联合协议。

## 8. Gate 状态

| Gate | 当前裁定 | 精确原因 |
|---|---|---|
| G1——源新鲜度/来源证明 | **PARTIAL** | 九个分支 HEAD 和关键 Blob 已固定；H/C 恢复已完成源级对账。完整逐文件 Owner Tree 审计、独立 Owner 批准来源、E 提交对象异常仍开放 |
| G2——规范领域语义 | **BLOCKED** | B Fact/Claim ADR 为 ADR-BLOCKED；Main Invariant/Principle 文案与 Domain Overview 冲突 |
| G3——运行时实现准入 | **BLOCKED** | Issue #7 仍 OPEN；规范运行时仓库、责任工程负责人、可复现 Build/CI 权威及部署/运维拓扑尚未确立 |
| G4——身份、授权与治理 | **BLOCKED** | I36-GOV-01..10 仍 GOVERNANCE-BLOCKED；没有生效批准；Global Inventory 合同仍是候选 |
| G5——规范生命周期/Forget/防复活 | **BLOCKED / NOT PROVEN** | D/I/Storage Phase 3.9 仍为提案；无共同精确版本接受；F 模型仅为逻辑模型；未实际验证生产 Index、Replica、Backup 和外部 Recipient |
| G6——C/H/G Applied 与 Provider Evidence | **PARTIAL / NOT PASSED** | C 19/19、H 11/11 有界候选 CI 通过；C/H 精确映射未接受；PR #94 触发修复待完成；H-ADE-001..003 开放；G 合同仍是 Draft |
| G7——Storage/COC/JF-10 物理一致性 | **BLOCKED / NOT PROVEN** | Option A ADR 自相矛盾；L4 开放；v3.3.2 绑定 H 1.2.14/C 1.0.1，而非 H 1.2.15 加 Applied Delivery Evidence 1.0.0；没有生产 DB/HA/Restore 证明 |
| G8——生产就绪 | **NOT READY** | 缺少完整运行时位置、Owner 批准、精确兼容 Bundle、生产 Trust、物理事务证明和端到端安全证据 |

### A 总体决策

**DEFERRED / ARCHITECTURE_NOT_READY。**

G1 保持 PARTIAL。G2–G5 与 G7 保持 BLOCKED。G6 保持 PARTIAL / NOT PASSED。G8 NOT READY。本报告不释放任何 Gate。

## 9. 必须由 Owner 执行的事项（A 不替代领域语义）

1. **B + Architecture Governance：** 记录具名决策权威、批准人、Fact/Claim Option A/B 决策、理由、时间戳及下游迁移/消费者批准。
2. **C：** 按治理流程合并或正式批准 1.0.1 Workflow Path 修复，然后执行 Schema-only Trigger Run；另行完成 C/H/G 精确字段映射和端到端场景。
3. **D：** 明确 PR #66 Phase 3.9 是否替代任何精确 D 条款；只有在 Storage/I 会签后，才发布精确接受的后继版本。
4. **E：** 对账当前分支提交对象读取异常，并提供可复现的 Compiler/Producer Admission 证据。
5. **F：** 保留逻辑 Anti-resurrection 模型作为回归基线；在提出运行时结论前，提供真实 Index/Cache/Working Set 与 Restore/Rebuild 竞态证据。
6. **G：** 为 Applied 合同取得 C/H/I/D/Storage 精确消费者决议；不得把设计草案表述为实现。
7. **H：** 修复 H-ADE-001 重复键严格解析、H-ADE-002 C Outcome/Final Boundary Join、H-ADE-003 Replay 结果披露前的当前授权/Fence 复核；代码变更后重跑精确 HEAD CI。
8. **I：** 通过必要外部/独立批准解决 I36-GOV-01..10，并将 Global Inventory 绑定到 D 和所有登记的 Producer/Recipient/Backup 表面。
9. **Storage + D：** 解决 Option A ADR 矛盾，发布唯一精确 L1 决议，并提供 L4 Runtime/Engine/Operator 及 T1–T8 物理证明；发布绑定精确 H/C 后继 Bundle 的 successor manifest。
10. **项目权威：** 在 Issue #7 回答规范运行时仓库、分支、Code Owner、Build/CI、Artifact SHA 和部署/运维拓扑。

## 10. 明确不授权事项

本源刷新**不授权**：
- 合并 PR #55/#66/#68/#71/#92/#94/#98/#99 或任何其他 PR；
- 修改 main 或任何 Owner 分支；
- 批准 B Fact/Claim 或任何 Owner ADR；
- 冻结 Storage 拓扑、C/H Wire Mapping、Applied Schema 或生产 Crypto Profile；
- 宣称 GlobalForgetCompleted 或 PhysicalErasureConfirmed；
- 运行时实现、生产数据访问、Provider Side Effect、部署或生产激活。

本报告仅覆盖只读源审查、A 文档报告，以及现有治理边界内有界的合成可行性工作。

## 11. 复核入口

- Main：`https://github.com/oahcom/AiMemoryBrainArchitecture/commit/e52594f181d2edb77448adcfed64a0fbdffaf3aa`
- H/C 完整性审查：PR #91
- C 恢复/消费者审查：PR #92
- C Workflow Path 修复：PR #94
- H Applied Evidence A 精确审查：PR #98
- 初始源清单：PR #99
- D/I/Storage Phase 3.9 提案：PR #66/#68/#71
