# L2-05-A-GOVERNANCE-PORTFOLIO：独立核验报告

<badge color="success">只读核验模式</badge> <badge color="warning">尚未形成 Owner 批准</badge>

**核验对象：** `oahcom/AiMemoryBrainArchitecture`

**本轮权限边界：**
- 不创建 PR、Issue 或 Git 对象。
- 不修改分支、文件、assignee、标签或 PR 状态。
- 不替 B–I 作领域决策。
- 不将提交、文件存在或协调方意见视为 Owner 批准。
- 不把 REQ-01 至 REQ-05 的登记状态升级为批准状态。

## 1. 启动记录与规范加载

已通过 GitHub 连接器读取私有仓库。仓库默认分支为 `main`，当前连接具有读取和写入权限，但本任务只使用读取操作。

| 项目 | 本轮核验结果 |
|---|---|
| AI-EXEC-001 | v1.1，已读取 |
| AI-EXEC-002 | 按 v1.1 执行，已读取 |
| AI-EXEC-002 v1.2 | PENDING ADOPTION，不作为本轮执行依据 |
| main 目标 SHA | `d61f813cac6780b6bcc5c09536a8e9bee96cc362`，待逐项确认 |
| remediation 分支 SHA | `745c768deca0a5826d436744213bed3beb65cd85`，待核验 |
| Git 写入 | 未执行 |
| PR/Issue 操作 | 未执行 |

实际加载声明：

`LOADED: AI-EXEC-001 v1.1 + AI-EXEC-002 v1.1`

这里有一个重要区分：规范加载版本已经明确，但尚不能据此证明本轮的 T2 Prompt 快照、SHA-256 和永久登记记录已经满足完整的项目追溯要求。

另外，AI-EXEC 文档明确区分 `ADOPTED`、`LOADED`、`VERIFIED`、`ACCEPTED` 和 `MERGED`，本报告沿用这些区分，不相互替代。

## 2. A–I Owner Baseline：实际分支核验

<badge color="warning">9/9 均未达到 APPROVED</badge>

这是本次最重要的治理发现之一。

Issue #11 的最新协调记录再次确认：九个模块都存在第一轮 Baseline & Redlines 提案，但没有找到九位 Owner 对精确版本作出的正式采纳或拒绝决定。

我进一步读取了九个 Owner 分支的实时分支 API、提案文件和 Blob SHA。结果如下：

| Owner | 当前分支 HEAD（缩写） | 提案 Blob（缩写） | 当前提案状态 |
|---|---|---|---|
| A | `8d2d59ff` | `a43a8f2f` | PROPOSED |
| B | `4ba22c89` | `410d6cc6` | PROPOSED |
| C | `3e7640cb` | `c79da952` | PROPOSED |
| D | `b525e1f8` | `84e402f4` | PROPOSED |
| E | `ee098e14` | `7f037a76` | PROPOSED |
| F | `1908ce4d` | `d4756cab` | PROPOSED |
| G | `0f77ffbe` | `fb2eb805` | PROPOSED |
| H | `36703686` | `a4d961ac` | PROPOSED |
| I | `8abddf81` | `b0493cf0` | PROPOSED |

以上均为实时读取到的分支及文件对象，不是根据 P 分支的历史登记推算。

### 2.1 当前状态的关键解释

1. 九份提案确实已经存在于各自 Owner 分支。
2. 文件头明确使用 `PROPOSED`、`Owner review required` 或 `NOT APPROVED`。
3. P 分支准备的九份协调材料不是九位 Owner 的正式决定。
4. P 分支的统一跟踪文件仍是 2026-11-17 的历史快照，不能作为今天的当前状态清单。
5. 九个 Owner 分支的当前 HEAD 均未开启 GitHub Branch Protection。

特别注意：九个分支的当前 HEAD 与提案中记录的部分准备时 HEAD 不一致。分支从原始提案快照之后已经继续演进，不能直接把旧快照中的源证据当成当前版本证据。

**结论：**

- Baseline 文件存在：9/9。
- Owner 明确批准：0/9 有可确认的证据。
- Owner 明确拒绝：0/9 有可确认的证据。
- 当前正式采纳矩阵：尚未完成。
- 项目级 PGA/G0：仍未授权。

因此，不能将这项 rollout 描述为已经完成，只能描述为第一轮提案已经形成、正式采纳和跨域验收仍开放。

## 3. A 的责任边界和治理 Issue 总表

首先纠正一个容易产生误判的地方：A 是 Integration Owner，不等于 Project Governance Authority，也不等于所有跨模块需求的最终 Accountable Owner。

根据 AI-STD-001 §3.1，A 的职责是 Principal Integration、跨模块契约登记和集成决策；B–I 各自保留领域权威。

### 3.1 Issue 责任矩阵

| Issue | 事项 | A 的责任 | 其他责任方 | 当前判断 |
|---|---|---|---|---|
| #11 | A–I Baseline rollout | 统筹和核验 | A–I 各 Owner | OPEN |
| #24 | Owner Workflow / Scheduled Tasks | 统筹执行模型 | A、工程、治理 | OPEN |
| #30 | Event-driven Worker Runtime | 架构集成协调 | 工程、I、安全审查 | OPEN |
| #41 | ChatGPT Native Execution | 统筹执行模型 | A、治理 | PROPOSED |
| #43 | 全系统架构收敛 | 集成审查 | A–I、Storage、R | OPEN |
| #254 | 外部架构审查 | 逐项分流、保持证据链 | 各领域 Owner、R | OPEN |
| #262 | REQ-01 风险评估 | 组织和集成 | R、相关领域 Owner | RECORDED |
| #263 | REQ-02 技术选型 | 组织跨模块评估 | 对应模块 Owner、Storage | RECORDED |
| #264 | REQ-03 PR 治理 | 流程和集成协调 | A、I、治理管理员 | RECORDED |
| #265 | REQ-04 架构突破 | 系统集成与收敛 | A–I、R、工程 | RECORDED |
| #266 | REQ-05 文档驱动 | 文档协调和追溯 | A–I、I、治理 | RECORDED |
| #130 | Session Delivery Traceability | Integration Owner 统筹 | 每个 Session 作者 | ADOPTED；审计 OPEN |

这里的责任是工作分配建议，不是对 Issue 中尚未指定的 Accountable Owner 作正式任命。

### 3.2 五项 Umbrella Requirement 的责任建议

| 需求 | 建议的责任结构 | 当前状态 |
|---|---|---|
| REQ-01 系统风险 | R 主责独立评估；A 提供架构依赖与证据 | 未任命 |
| REQ-02 技术选型 | 各模块 Owner 对本领域选型负责；A 组织比较；Storage 参与物理技术评估 | 未任命 |
| REQ-03 PR 治理 | A 负责集成流程；I 负责安全治理边界；管理员负责平台设置 | 未完成运营审计 |
| REQ-04 架构突破 | A 负责系统收敛；各模块 Owner 对自身架构决策负责；R 独立评估风险 | 未任命 |
| REQ-05 文档治理 | A 负责工作流和追溯；各 Owner 维护自身规范；I 负责治理政策边界 | 未任命 |

重要区分：

- #130 的 PR-GOVERNANCE-001 已经 ADOPTED。
- #130 仍 OPEN，是因为运营审计尚未完成。
- #134 的平台强制门禁仍然是独立问题。
- REQ-03 不能重新打开已经采纳的 PR-GOVERNANCE-001，也不能以其已经采纳为理由声称平台强制门禁已经完成。

---

### 3.3 发现：REQ-01 至 REQ-05 已有新的角色指派裁决

补充核验了 #262–#266 的最新评论，发现存在一个比原始 Issue 正文更新的事实：

**RULING-05 已经对五项需求作出 Governance 角色层面的责任指派。**

权威登记位于 #265 comment `7009148932`。

| Issue | 最新角色指派 | 权限边界 |
|---|---|---|
| #262 REQ-01 | Governance + A | Governance 负责风险识别、分级、优先级；A 负责跨域风险集成 |
| #263 REQ-02 | A + B/C/E/F/H/Storage | A 统筹选型流程；领域 Owner 只负责各自领域 |
| #264 REQ-03 | A + Governance | A 负责集成；Governance 负责流程、证据和授权门禁 |
| #265 REQ-04 | A + B/C/D/E/F/G/H/I/Storage | A 负责收敛；领域 Owner 分别负责自己的契约、实现和验证 |
| #266 REQ-05 | Governance + A | Governance 负责规范权威；A 负责文档流程、Work Item 和集成追溯 |

因此，修正前述责任建议：

- REQ-01 的 Accountable 角色不是由 R 单独担任，而是 Governance + A。
- R 的独立风险审查职责仍然成立，但属于独立评估职责，不自动获得需求批准权。
- 上述裁决是 ChatGPT Owner 角色指派，不是真人任命，也不是验收批准。

**尤其重要：** 五个 Issue 的正文仍然显示 `Accountable Owner: NOT_ASSIGNED`，assignee 仍为空，状态仍为 `RECORDED`。RULING-05 明确没有授权自动修改这些状态。

正式进入 `OWNER_ASSIGNED`，还需要责任会话实例、提案/审查/验收责任、交付物、退出条件和证据链接齐备。

这意味着：责任角色已有裁决，实际责任链尚未完成登记。不能把两者混为一谈。

---

## 4. #254 外部架构审查：Finding → Owner 分流

<badge color="warning">领域分流尚未等于 Owner 接受</badge>

Issue #254 的外部审查报告应作为只读证据来源，而不是新的规范或决策来源。

我核对了 #254 的讨论和 #43 的现有集成范围。#254 已被明确作为独立证据载体保留，处置为 HOLD；不得为每条建议重新创建 Issue。

以下是建议分流矩阵。

| #254 审查问题 | 首要领域 Owner | 相关协同方 | A 的工作 |
|---|---|---|---|
| ForgetFence 顺序、活性恢复 | D | I、E、F、G、Storage | 对齐全链路顺序和依赖 |
| Validator/Test Blob 声明不一致 | 对应工件 Owner | Verification、A | 建立自动证据清单 |
| BMCP Tier 与证据状态矛盾 | H | C、G、I | 协调协议与消费端契约 |
| JCS 与 Python JSON 规范化不一致 | H | C | 核对序列化和摘要契约 |
| 幂等、冲突、重放仍为测试桩 | 对应生产语义 Owner | D、E、F、G、Storage、H | 区分参考模型和真实实现 |
| CI 触发路径缺失 | 相应工作流 Owner | A、I、Verification | 检查触发条件和合并门禁 |
| Fact/Claim 语义矛盾 | B | I、A | 保留 ADR 阻塞并协调消费者 |
| Lifecycle / Forget 权威矛盾 | D | I、E、Storage | 统一依赖问题，不代替 D 决定 |
| Context 必需字段矛盾 | G | C、H | 组织消费者兼容性审查 |
| Delivery 状态机及 Tier 2/3 冲突 | G、H | C、I | 对齐 Applied 证据链 |
| 检索读放大、延迟和可用性预算 | F | D、I、G、Storage、R | 组织性能和风险评估 |
| README、目录、链接及双语门禁缺陷 | A | 各文档 Owner、I | 修正治理目录和文档追溯 |
| SQLite 参考 Ledger 跨平台问题 | G | Storage、Verification | 区分参考模型与物理能力 |
| 缺少产品价值对照基线 | A（统筹） | C、F、G、R、工程 | 建立可衡量的实验计划 |
| G/H Join Key 不完整 | G、H | C、I、D | 形成跨模块身份映射矩阵 |

### 4.1 必须保留的领域决定

**B：Fact/Claim**

- Fact/Claim 的独立对象语义仍由 B 的 ADR-001 决定。
- 当前证据保持 ADR-BLOCKED。
- 外部审查建议不能直接把 ClaimRevision 方案升级为已批准模型。

**D：Forget 与 Lifecycle**

- ForgetFence 的权威及生命周期语义由 D 负责。
- I 保留授权、撤销及安全治理职责。
- Storage 负责物理事务、恢复和持久化能力证据。
- E、F、G 必须分别接受相关生产者/消费者边界。

**G/H/C：Applied**

必须继续区分：

1. Prepared
2. Delivered
3. Materialized
4. Final Request Submitted
5. Applied
6. Execution Started

不得把 Adapter 的应用证据扩大解释为模型真正注意、理解或使用了记忆。

**F：Retrieval**

检索结果不能越过 Canonical Authority、Permission 和 Forget 状态检查。候选上限、Canonical 读放大、延迟预算和缓存恢复仍需要量化。

### 4.2 #254 的特殊处置

当前 #254 是跨目录外审证据载体，不是某一个模块的普通实现任务。

现有评论已明确：

- 不转移至单个领域 Issue。
- 不合并至 REQ-05。
- 不因报告历史较久而直接关闭。
- 优先把实际问题映射至 #43 和已经存在的领域工作项。

<text color="secondary" size="xs">分流状态：CANDIDATE。上述矩阵不是新建的 Finding 登记，也不代表对应 Owner 已接受。</text>

---

## 5. PR #271 与 PR #275：OPEN Findings 和实际阻塞

### 5.1 PR #271 — GOV-DOC-001 v1.2

<badge color="warning">HOLD — 不具备合并授权</badge>

<row align="center" gap={2}>
  <box flex="1">
    **PR #271**

    <text color="secondary" size="xs">GOV-DOC-001 v1.2 bilingual remediation</text>
  </box>
  <badge color="warning">DRAFT 以外的开放 PR</badge>
</row>

| 项目 | 实测 |
|---|---|
| 状态 | OPEN |
| Draft | false |
| 当前 Head | `e6ff27468bfa215f603d39524e9ff198d6d04f11` |
| Base | `c5a995d9a2808112b007a9108e085048cbed5cc9` |
| 文件数 | 11 |
| 最新结构性 CI | SUCCESS |
| 正式 GitHub Reviews | 0 |
| 合并授权 | NO |

PR 的目标是扩展 GOV-DOC-001 v1.1，不创建新的 Policy ID，并为 Umbrella Requirement、Issue、Commit Message、PR 提供双语治理规则。

**原始 R1 审查：FAIL。**

原审查针对 Head：

`a77219fa2834af0c4535e6692029adaec2e62638`

登记结果：

| Finding | 级别 | 当前证据状态 |
|---|---|---|
| F-01 规范完整性和 §7.1 兼容性 | P1 | CLOSED |
| F-02 仓库继承强制机制 | P1 | PARTIAL，1/3 退出条件完成 |
| F-03 历史迁移字段与枚举 | P2 | 尚待当前 Head 独立复核 |
| F-04 历史证据可复算性 | P2 | 部分补充，完整验收未完成 |
| F-05 双语语义质量 | P2 | 尚待当前 Head 独立复核 |
| F-06 历史 Issue/Commit 清点 | P1/P2 追踪项 | 未全部闭合 |
| F-07 历史 Blob SHA 转录修正 | 证据修正项 | 已有更正记录，最终复算未完成 |

这里有两项特别重要。

**第一，F-01 已经关闭，但不能据此认定整个 PR 合格。**

后续补充了 GOV-DOC-001 v1.1 完整原文和 AI-STD-001 §7.1，逐项对照后确认旧版 MUST、MUST NOT、SHOULD 的实质要求得到保留，双语门禁不存在已经证明的规范冲突。

**第二，F-02 仍然没有闭合。**

最新证据：

- 独立复算权威 Policy Blob SHA：PASS。
- GitHub required check 配置：OPEN。
- 权威版本漂移自动检测：OPEN。

PR 中已经增加 `scripts/check_policy_inheritance.py`，但当前 `.github/workflows/bilingual-docs.yml` 没有调用它。

这意味着：

- 校验代码存在；
- 测试代码存在；
- 局部 CI 可以成功；
- 但权威版本变化不能因此保证触发失败；
- GitHub 也没有通过 Branch Protection 强制执行这一门禁。

当前精确工件：

| Artifact | Commit | Blob SHA |
|---|---|---|
| `scripts/check_policy_inheritance.py` | `e6ff27468bfa215f603d39524e9ff198d6d04f11` | `3c1df44ac282f670d3a5508d810ba39c382c3a98` |
| `tests/test_policy_inheritance.py` | 同上 | `4ca1f8a2a5eeba329d2039ff7682a74effaf779f` |
| `.governance/GOV-DOC-001-inheritance.json` | 同上 | `56d2e2c5e8febe03d39da9bb99204adda54ef445` |

另外，F-07 更正记录指出历史审查报告中有一个 41 字符的错误 SHA 转录。正确值是：

`66517d39dfeae459fef5cedf9d5a79de08faf08d`

这不是 Git 对象损坏，但最终七文件清单仍须从当前精确 Head 独立重新读取。

**合并前剩余条件：**

1. 完成 v1.1 → v1.2 的逐项规范保留对照。
2. 对当前 `e6ff2746...` 进行独立语义复审。
3. 取得明确的授权治理关系裁定：`SUPERSEDE / COMPLEMENT / PARALLEL`。
4. 当前 Head 的全部适用 CI 通过。
5. 补齐 F-06、F-07 的历史证据核验。

这些要求也与 #264 comment `7009210471` 的治理登记一致。

当前 Head 的结构性 CI 虽然成功，但 Branch Protection 仍关闭，正式 Reviews API 为空。因此不能把 CI SUCCESS 等同于合并批准。

### 5.2 PR #275 — README 定位变化与残余风险

<badge color="warning">HOLD — 存在配额冻结期创建问题</badge>

<row align="center" gap={2}>
  <box flex="1">
    **PR #275**

    <text color="secondary" size="xs">Project positioning and strategic direction</text>
  </box>
  <badge color="warning">Draft</badge>
</row>

| 项目 | 实测 |
|---|---|
| 状态 | OPEN |
| Draft | true |
| 当前 Head | `b686b46fda6e34439d3826c32c16e41ba74d2440` |
| Base | `f16d04de67b8955b77e7f25d4685ef5e500a471d` |
| 变更 | README.md 一个文件 |
| 当前 Head CI | SUCCESS |
| 正式 Reviews | 0 |
| Inline Review Threads | 0 |

当前 README Blob：

`de6b0cf7203e23b2fd953b90053c5f7bd523521a`

**定位变化**

旧 README 主要表达：

- Architecture specifications；
- System architecture baseline；
- Implementation not started by design；
- 记忆生命周期和上下文管理的逻辑设计。

新 README 将项目定位进一步明确为：

**正在设计中的独立 Memory Authority and Governance Layer。**

同时增加：

- 模型、Agent 和运行环境独立性；
- Canonical Memory / Memory Context / Applied Context 三层区分；
- 项目问题定义和差异化价值；
- 产品状态和路线图；
- 不属于 Agent Framework、RAG 或单纯向量数据库的边界；
- 生产实现尚未开始的声明。

我认为这次定位调整方向合理，尤其是以下几个修正很重要：

1. 不再把参考模型说成产品运行时。
2. 不再把 BMCP 的候选协议说成已经证明互操作。
3. Applied 证据只限定在 Adapter 声明的请求边界。
4. 不把 Provenance 解释为真实性、准确性或独立性的证明。
5. 不声称 Forget 已经获得生产正确性证明。

**残余风险**

| 风险 | 判断 |
|---|---|
| 与成熟记忆产品的实际差异 | 尚未经过系统对照 |
| 模型无关性 | 目前主要是架构目标，缺少真实多 Agent 互操作证据 |
| 记忆效果 | 缺少任务成功率和召回质量对照 |
| 性能 | 没有代表性负载下的运行数据 |
| Forget 正确性 | 缺少真实运行及故障注入证据 |
| 外部定位 | 尚需核对既有治理文件和对外承诺 |

因此，README 不能被当作项目价值已获市场验证的证明。

**还有一个更直接的治理问题：PR #275 的创建发生在配额冻结期间。**

#264 comment `7009210471` 已经登记：

- 冻结开始：2026-11-18 19:45 +08；
- PR 创建：2026-11-19 11:17:06Z；
- 创建时没有已确认的事前授权；
- 处理结果：`FREEZE_BREACH_CONFIRMED / HOLD`；
- 新增 Finding：`F-PR-FREEZE-275-01 [P2]`。

这不是 README 内容质量问题，而是载体创建权限问题。

PR #271 也有类似的冻结期创建记录，当前仍 HOLD，不能用开放 PR 数量低于阈值作为追溯授权。

**我的建议：** 保留 #275，不关闭、不合并。先完成冻结期创建授权的治理处置，再对当前 Head 做独立语义复审。原有基于旧 Head `10e5dc...` 的 HOLD 评论不能替代当前 Head 的复审。

---

## 6. AI-STD-001 / AI-PROC-001 的规范关系

<badge color="danger">存在未解决的规范层级冲突</badge>

这是本轮必须明确停止自行裁决的地方。

### 6.1 当前规范状态

| 文件 | 版本 | main 当前状态 |
|---|---:|---|
| AI-STD-001 | 1.0 | PROPOSED |
| AI-PROC-001 | 1.0 | PROPOSED |
| AI-EXEC-001 | 1.1 | ADOPTED |
| AI-EXEC-002 | 1.1 | ADOPTED（本轮执行版本） |
| AI-EXEC-002 | 1.2 | PENDING ADOPTION |
| PR-GOVERNANCE-001 | 1.0 | ADOPTED |
| GOV-DOC-001 | 1.1 | NORMATIVE |

### 6.2 启动记录的版本纠正

本轮第一次读取当前 main 上的 AI-EXEC-002 时，读到的是 v1.2，而不是指定执行的 v1.1。

随后我重新读取了已经采纳的 v1.1 精确版本：

- AI-EXEC-002 v1.1 源文件 Commit：`1f97c3fae65828266a0c3cb1d1e8d4e6cb330856`
- 源 Blob：`ebb7f1ee9a084864c454711d271499cfbf8d386f`
- 英文译文 Commit：`08b07d228dbe78a209a5af68c4988b292e65e9c8`
- 英文译文 Blob：`96aab56ce856484e24ad99ec6944a4c45ceb763b`

AI-EXEC-001 v1.1 当前 main 源文件：

- Commit：`d61f813cac6780b6bcc5c09536a8e9bee96cc362`
- Blob：`58af59af266b81109269156ea667df1a15edfb7b`

因此，**本报告的实际执行口径是 v1.1，不采用 v1.2 的待采纳修订。**

启动记录的首次声明早于这次精确版本复核，不能倒签为已经在首次启动时完成了历史版本读取。后续分析使用的是上述已核实的 v1.1。

### 6.3 必须解决的结构冲突

AI-EXEC-002 v1.1 的规则和其对应的统一裁决要求：

- 12 项核心义务；
- AI-STD-001 原有 13–15 项附加义务；
- 完整的 15 项强制结构；
- 6/7 项只是关注重点，不是豁免。

但当前 main 的 AI-STD-001 §5.1 已经出现：

- Seven core sections；
- 12 项内容义务映射到七个结构章节；
- 不允许额外强制顶层章节。

AI-EXEC-002 v1.2 正是针对这一结构锚点变化提出修订，将 15/12 项重分类为内容义务，而不是新增顶层章节。

然而 v1.2 仍为 PENDING ADOPTION。

这形成了明确的状态冲突：

| 事项 | 已有事实 |
|---|---|
| AI-EXEC-002 v1.1 | ADOPTED，15 项结构口径 |
| AI-STD-001 §5.1 | 当前文本是七章节口径 |
| AI-EXEC-002 v1.2 | 已存在，但 PENDING ADOPTION |
| 最终规范解释 | 本轮不自行选择 |

这不能由 A 的集成报告直接解决。

**停止条件：** 涉及 Prompt 模板强制结构、上位规范修订和执行规则生效边界的工作，必须由有权治理主体解决版本和规范层级冲突。

### 6.4 AI-PROC-001 与 AI-EXEC 的关系

AI-PROC-001 定义 Stage 0–8 生命周期：

1. Intake；
2. Impact & Dependency；
3. Prompt Drafting；
4. Readiness；
5. Implementation；
6. Verification；
7. Independent Review；
8. Cross-owner Integration；
9. Acceptance / Merge / Closeout。

AI-EXEC-001 将这些阶段落实为操作证据、跟踪载体和关闭条件。

AI-EXEC-002 管理实际执行 Prompt 的版本、来源、哈希、审查和 Closeout。

PR-GOVERNANCE-001 则要求实质工作进入 GitHub Issue/PR，而不是只存在于 ChatGPT 对话中。

三者应当分工：

- AI-STD-001：定义工程治理要求；
- AI-PROC-001：定义生命周期；
- AI-EXEC-001/002：定义执行纪律；
- PR-GOVERNANCE-001：定义 GitHub 交付和集成记录。

但前两项目前仍是 PROPOSED，不能仅凭执行细则 ADOPTED 就把它们整体提升为正式采纳规范。

---

## 7. A 负责的跨域决策与集成事项

这里的“负责”是 A 的职责范围，不代表 A 可以替其他 Owner 批准语义。

| 编号 | A 应负责的工作 | 交付证据 |
|---|---|---|
| A-01 | A–I + Storage 权威边界整合 | Authority Matrix |
| A-02 | 跨模块依赖和执行顺序 | Dependency DAG |
| A-03 | 精确版本和证据当前性 | Source Pin Registry |
| A-04 | 生产者/消费者接口兼容性协调 | Contract Acceptance Matrix |
| A-05 | 跨域矛盾和阻塞登记 | Contradiction Register |
| A-06 | 架构收敛与最小闭环集成评估 | Architecture Consolidation Report |
| A-07 | 跨 Owner Prompt 起草及责任边界 | Prompt Version / Approval Record |
| A-08 | GitHub Issue/PR 交付追溯 | Session Delivery Index |
| A-09 | 双语规范和治理文件之间的关系协调 | Normative Relationship Registry |
| A-10 | 架构冻结就绪建议 | READY / READY WITH BLOCKERS / NOT READY |

### 7.1 A 已经可以给出的集成判断

REQ-04 的 A 角色会话已经给出了 `NOT_READY` 集成处置，登记在 #265 comment `7008783906`。

该处置指出：

- 四份研究材料已经形成；
- 成熟生态借鉴有了初步边界；
- 仍有 Canonical Transaction、Producer Admission、Forget、Full Applied、物理恢复等 P0 根因；
- 研究交付不等于架构决策；
- 研究交付不等于领域 Owner 接受；
- 参考模型通过不等于实现验收。

这属于 A 对系统集成状态的判断，不是项目架构批准。

### 7.2 A 需要形成的跨域工作顺序

我建议 A 不再以“文档数量”作为进展指标，而改为维护以下四张核心表：

1. **Authority Matrix**：谁能决定什么。
2. **Contract Matrix**：谁生产、谁消费、谁接受。
3. **Evidence Matrix**：每个结论依赖哪个精确版本和哪项验证。
4. **Critical Dependency Matrix**：不解决什么就不能继续推进。

这四张表应该成为 #43 的主要交付物，而不是再产生一套与现有规范并行的治理制度。

---

## 8. 不能由 A 决定的事项

<badge color="danger">权限边界</badge>

| 事项 | 决策权威 | A 可以做什么 |
|---|---|---|
| Fact/Claim 本体语义 | B | 整合消费者影响 |
| Canonical Memory 身份和生命周期 | D | 审查全链路依赖 |
| ForgetFence 语义 | D | 协调 I/E/F/G/Storage |
| Principal / Permission / Revocation | I | 核对安全边界 |
| Compiler Admission / Publication | E | 核对上下游合同 |
| Retrieval / Cache / Suppression | F | 核对跨模块一致性 |
| ContextVersion / Applied | G | 核对 C/H/I 消费条件 |
| BMCP Schema / ACK / Reconnect | H | 协调消费者接受 |
| 物理事务域和数据库部署 | Storage + 授权决策方 | 组织技术评估 |
| 独立风险结论 | Governance / R | 提供系统架构证据 |
| 产品实现责任人 | 项目治理授权主体 | 提交责任和依赖建议 |
| PGA 任命与 G0 批准 | Project Governance Authority | 准备精确版本材料 |

另外有三个特殊禁止：

**第一，不得将角色指派等同于真人授权。**

RULING-05 已经建立角色责任链，但没有创造第二个 GitHub 操作者，也没有创造独立真人签署。

**第二，不得将研究建议等同于技术选型。**

REQ-02 的 AID-2026-008 明确禁止在当前证据整理阶段进行候选排名、评分、最终推荐或技术选型。

**第三，不得将 A 的 NOT_READY/READY 等集成结论升级为项目 G0 批准。**

A 可以报告系统是否具备集成条件，但不能替代 PGA。

---

## 9. 现有载体复用方案

本轮没有必要新建 Issue 或 PR。

建议按以下方式继续使用既有载体：

| 工作 | 主载体 | 处理方式 |
|---|---|---|
| A–I Baseline | #11 | 只补当前 Owner 决策和精确版本 |
| 系统架构收敛 | #43 | 统一矩阵、矛盾和依赖 |
| 外部审查 | #254 | 保留原始证据，逐项回链 |
| 风险评估 | #262 | Governance + A |
| 技术选型 | #263 | A + 领域 Owner |
| PR 治理 | #264 | A + Governance |
| 架构突破 | #265 | A + B–I + Storage |
| 文档治理 | #266 | Governance + A |
| ChatGPT 原生执行 | #41 | 保留交互执行约束 |
| Owner Workflow | #24 | 与 #41 对齐 |
| Worker Runtime | #30 | 保留为有条件的候选架构 |
| Session Traceability | #130 | 继续运营审计 |
| 平台合并门禁 | #134 | 独立 P0 治理问题 |
| 双语规范修复 | PR #271 | 保持 HOLD |
| README 定位 | PR #275 | 保持 HOLD |

### 9.1 需要特别核对的历史载体

- PR #23：已关闭，但没有合并。不能作为已经交付的 Owner 自动化系统。
- PR #27：当前 GitHub API 显示已经合并，Merge SHA 为 `19ae5ed2b7a0ab613f188a4dc8e75e4f5bc81320`。
- PR #27 的 Read-only Diagnostics 仍然是 `NOT_RUN`，重启恢复和不可信 PR 隔离仍是 `NOT_VERIFIED`。
- PR #144/#145：已经完成 PR-GOVERNANCE-001 的规范采纳和状态修正。
- #130：仍然 OPEN，原因是全仓 Session Delivery Traceability 审计没有全部完成。

这里发现一个需要修正的事实差异：

#30 正文仍然把 PR #27 描述为 Open、未合并，但 GitHub 当前 API 已显示其 Closed/Merged。

这属于工作载体的状态同步问题，不能继续引用旧正文作为当前事实。

### 9.2 A–I Template 的实际位置问题

本次直接读取发现：

- `main` 上 `00-governance/module-baseline-and-redlines-template.md`：404。
- `main` 上 `00-governance/module-baseline-and-redlines-rollout.md`：404。
- 两份文件实际存在于 P 协调分支。

<text color="secondary" size="xs">P 分支 HEAD：`0559a03ccd4f9640ddb7d4af8e37a059930b55af`</text>

| 文件 | P 分支 Blob |
|---|---|
| `00-governance/module-baseline-and-redlines-template.md` | `408979f2125b67e7599118038b9a415a213399ee` |
| `00-governance/registries/module-baseline-rollout-tracking.md` | `0fd50c4ef51ea77bff55b3d2f08d1674c03b855d` |

这意味着：

- P 已经准备了规范化模板；
- 但该模板没有进入 main；
- 也没有获得正式采纳；
- 不能要求 Owner 以它作为已经生效的规范强制验收；
- 现有九份提案应保留自己的结构，不应静默重写。

建议 A 把这个问题纳入 #11 和 #43 的治理依赖登记，而不是自行把 P 模板升级为规范。

---

## 10. 依赖顺序与开发优先级

这里采用根因优先，而不是按模块目录顺序推进。

<title size="lg">根因优先级</title>

<box border radius="lg" gap={3} padding={3}>
  <box gap={1}>
    <row align="center" justify="between">
      **P0 — 权限、规范和证据根基**
      <badge color="danger">最高优先级</badge>
    </row>
    - 解决 AI-STD-001 / AI-EXEC-002 v1.1 / v1.2 的结构冲突。
    - 明确 Governance、A–I、Storage、R、P 的权限边界。
    - 修复 #134 的 main 合并门禁。
    - 修复规范目录识别和双语校验盲区。
    - 维持配额冻结，禁止未经授权扩张载体。
  </box>
  <divider color="subtle"/>
  <box gap={1}>
    <row align="center" justify="between">
      **P1 — 核心正确性和跨模块一致性**
      <badge color="warning">基础架构</badge>
    </row>
    - B：Fact/Claim ADR-001。
    - D/I/Storage：Forget、Permission、事务和恢复。
    - D/E：Producer Admission 与 Canonical Publication。
    - F/G：检索、Context、Suppression。
    - C/G/H：Applied 完整证据链。
    - H：JCS、错误码、Schema 演进和 Join Key。
    - 真实并发、崩溃、重放和恢复测试。
  </box>
  <divider color="subtle"/>
  <box gap={1}>
    <row align="center" justify="between">
      **P2 — 技术选型和最小可运行闭环**
      <badge color="info">验证可行性</badge>
    </row>
    - 逐模块完成成熟技术 Build-vs-Adopt 研究。
    - 明确实际运行时仓库和工程责任人。
    - 选择一个最小端到端纵向闭环。
    - 用真实实现和可重复测试验证架构假设。
  </box>
  <divider color="subtle"/>
  <box gap={1}>
    <row align="center" justify="between">
      **P3 — 性能、产品价值和生态扩展**
      <badge>后续增强</badge>
    </row>
    - 无记忆 / 简单检索 / Brain 全链路对照。
    - Precision / Recall、错误激活率、Token 成本。
    - Recall 延迟和恢复成本。
    - ANN、向量库、Reranker 等按实际收益扩展。
    - 多 Agent、多模型和多运行环境互操作验证。
  </box>
</box>

### 10.1 我建议的实际依赖图

<CodeBlock language="mermaid" editable>
flowchart TD
    A["P0: 权限与规范层级明确"] --> B["P1: Owner 权威决策"]
    B --> C["P1: 跨域契约和状态机一致"]
    C --> D["P1: 物理事务及故障证明"]
    D --> E["P2: 成熟技术 Build-vs-Adopt"]
    E --> F["P2: 最小纵向实现"]
    F --> G["P2: 独立审查和精确版本验收"]
    G --> H["P3: 产品价值与性能验证"]
    H --> I["P3: 生态扩展"]
</CodeBlock>

有一点需要单独强调：#24/#30 的连续事件驱动目标，与 #41 的 ChatGPT 原生执行限制存在实际冲突。

#41 规定：

- 普通 ChatGPT 对话是唯一 AI 执行通道；
- Ubuntu 只负责确定性构建、测试和 CI；
- 不使用 API Worker、Codex 或本地 AI 中转。

而 #24/#30 原先要求不依赖会话打开状态的持续 Owner Worker。

在这些约束同时有效时，不能声称 Ubuntu 上的事件驱动 Worker 可以自行调用 ChatGPT 完成无人值守的 AI 开发。

因此：

- #24/#30 可以继续研究事件接收、队列、状态同步和确定性任务；
- 不能据此启动自主 AI 写入；
- 不得把每日 Scheduled Task 伪装成真正的连续事件驱动执行；
- 需要由有权主体明确解决执行模型冲突。

这属于架构决策，不由 A 自行选择。

### 10.2 五项需求的状态补充核验

| 需求 | 当前 GitHub 状态 | 新发现 | 不能宣称 |
|---|---|---|---|
| REQ-01 | OPEN / RECORDED | 已有风险评估工作单，但目前仅形成治理、交付、追溯风险条目 | 不能声称系统架构风险评估已完成 |
| REQ-02 | OPEN / RECORDED | AID-2026-008 已在 main 出现 manifest 和 INDEX 记录 | 不能声称完成技术调研或选型 |
| REQ-03 | OPEN / RECORDED | PR-GOVERNANCE-001 已采纳 | 不能声称平台门禁已生效 |
| REQ-04 | OPEN / RECORDED | A 已给出 NOT_READY 集成处置，研究材料已有交付 | 不能声称架构突破或实现验收完成 |
| REQ-05 | OPEN / RECORDED | 已有双语扫描和分类研究 | 不能声称全仓双语语义一致性完成 |

补充几个重要事实：

**REQ-01：** #262 的最新工作单说明，首轮风险条目只足以支持治理、交付和追溯风险分析，尚不足以完整评价内部技术设计、Forget 正确性和生产安全性。

**REQ-02：** `AID-2026-008` 已有文件，但 manifest 仍写：

- `status: PROPOSED`
- `accountable_owner: NOT_ASSIGNED`
- `registration.status: BLOCKED_PENDING_REGISTRATION`

它的工作范围明确禁止在当前阶段做最终技术排名或选型。

**REQ-04：** A 的 `NOT_READY` 是目前应该保留的集成结论，不应因研究材料增加而自动升级。

**REQ-05：** #266 有一份历史扫描快照：

<text color="secondary" size="xs">基线 main@`2d2d577e856f4b9812f694b8a4d0f008dac110d7`，2026-11-19 扫描</text>

| 分类 | 数量 |
|---|---:|
| Markdown 总数 | 591 |
| 成对文件 | 120（60 组） |
| ZH_ONLY | 133 |
| EN_ONLY | 215 |
| Embedded bilingual candidates | 123 |

这些数字不是当前 main 的最新全量扫描结果，也不是语义对等的证明。

尤其是 `14-ai-development/` 与 `docs/en/14-ai-development/` 存在跨目录映射关系，不能仅根据扫描器的 ZH_ONLY 分类就重复创建英文译文。#266 已将这个问题登记为 `F-REQ05-PAIR-01 [P1]`。

---

## 11. 证据登记与本轮 Closeout

以下是本轮已经实际读取的关键工件。Commit 和 Blob 分开列出，不能将两者混为一谈。

### 11.1 main 与治理规范

| 路径 | Commit SHA | Blob SHA |
|---|---|---|
| `14-ai-development/AI-EXEC-001.md` | `d61f813cac6780b6bcc5c09536a8e9bee96cc362` | `58af59af266b81109269156ea667df1a15edfb7b` |
| `14-ai-development/AI-EXEC-002.md`（v1.2） | `d61f813cac6780b6bcc5c09536a8e9bee96cc362` | `7f5928a5d16eb12da7621cfb8bd99ca463afd859` |
| `docs/en/14-ai-development/AI-EXEC-002.md`（v1.2） | `d61f813cac6780b6bcc5c09536a8e9bee96cc362` | `772cee6b9a9a9c510c79adfd85eefd96397573c2` |
| `14-ai-development/ai-development-standard.md` | `d61f813cac6780b6bcc5c09536a8e9bee96cc362` | `d9624a6397df9ae8b6589cdd9f3124093c6fc082` |
| `14-ai-development/iteration-lifecycle.md` | `d61f813cac6780b6bcc5c09536a8e9bee96cc362` | `f87e8eaec1a3ea889c089aec8c0ed727d9710111` |
| `14-ai-development/PR-GOVERNANCE-001.md` | `d61f813cac6780b6bcc5c09536a8e9bee96cc362` | `4a28fa8181af0da06f52d31a6dca5d30fbf6458a` |
| `scripts/check_bilingual_docs.py` | `d61f813cac6780b6bcc5c09536a8e9bee96cc362` | `25205bbd9ecaf626422db23b46cbae46806cefd6` |
| `00-governance/bilingual-documentation-policy.md` | `d61f813cac6780b6bcc5c09536a8e9bee96cc362` | `0e170479e1a71e8f4c124c6f1dc170241652f42b` |

### 11.2 本轮实际采用的 AI-EXEC-002 v1.1

| 项目 | 精确版本 |
|---|---|
| 源路径 | `14-ai-development/AI-EXEC-002.md` |
| Source Commit | `1f97c3fae65828266a0c3cb1d1e8d4e6cb330856` |
| Source Blob | `ebb7f1ee9a084864c454711d271499cfbf8d386f` |
| 英文路径 | `docs/en/14-ai-development/AI-EXEC-002.md` |
| Translation Commit | `08b07d228dbe78a209a5af68c4988b292e65e9c8` |
| Translation Blob | `96aab56ce856484e24ad99ec6944a4c45ceb763b` |

这组精确版本是本报告使用的 v1.1 依据。

### 11.3 A–I Owner 分支与提案

以下 HEAD 来自本轮直接读取的 GitHub Branch API；Blob 来自各 Owner 分支当前提案文件。

| Owner | Branch HEAD SHA | Proposal Blob SHA |
|---|---|---|
| A | `8d2d59fff5ebc6077adc470e91d5d8b9684b3b0e` | `a43a8f2fa3d31681d64b79d584364fdae80f8866` |
| B | `4ba22c899469ab0f5df9e6f965a1ba1253625733` | `410d6cc62294e1a7ee5efa0cfe4ef496a8179326` |
| C | `3e7640cbe8a3d5c1dc95b6a0b887a1c41f62916c` | `c79da952efaa490083c88ccb4608d62f526fcbae` |
| D | `b525e1f8fee2471a131e4a38efda99804045e424` | `84e402f471d452c7dab63a7db344f86b5b57bd7c` |
| E | `ee098e14747d9915de5b3efb63b3a8dd77f670ed` | `7f037a7684723fdbddd593b3d131c7c348e2ccbe` |
| F | `1908ce4d233b20f7cafd00cb679affd01bd15174` | `d4756cabda3151999cbe1ddde0adb554458004a1` |
| G | `0f77ffbe956c5f93df295c436fcb0a750629d595` | `fb2eb805be385469b5ab5f25c4ef76f234feb4c2` |
| H | `36703686e3b40a07322a4d7855554b18b60237aa` | `a4d961ac7b7e1a5fdf59422a4ebe21a6db95ace1` |
| I | `8abddf814467b271344a9814613a6b7ca6a446c6` | `b0493cf0366159c99536ee8847996916bc21c606` |

以上九个 Owner 分支的 GitHub API 均返回：

`protected: false`

### 11.4 其他关键工件

| 工件 | Commit / Branch HEAD | Blob |
|---|---|---|
| AID-2026-008 manifest | `d61f813cac6780b6bcc5c09536a8e9bee96cc362` | `211ace92841478a37fed14623ebe2afee99a11a2` |
| Work Items INDEX | 同上 | `d9f004b26b3b6cbac2f0d59291b33f2b1ad90e3d` |
| PR #271 inheritance checker | `e6ff27468bfa215f603d39524e9ff198d6d04f11` | `3c1df44ac282f670d3a5508d810ba39c382c3a98` |
| PR #271 inheritance tests | 同上 | `4ca1f8a2a5eeba329d2039ff7682a74effaf779f` |
| PR #271 inheritance JSON | 同上 | `56d2e2c5e8febe03d39da9bb99204adda54ef445` |
| PR #275 README | `b686b46fda6e34439d3826c32c16e41ba74d2440` | `de6b0cf7203e23b2fd953b90053c5f7bd523521a` |
| D Erratum-004 | `745c768deca0a5826d436744213bed3beb65cd85` | `a00a8648350f58647b911af17ace07ce6c104b62` |

D 的 Erratum-004 是对历史执行记录中三项错误描述的更正，不代表 Forget 契约整体已经关闭。其当前工件只证明相应历史记录被更正和重新标注。

---

### 11.5 本轮正式登记字段

<box border radius="lg" padding={3} gap={2}>
  **Decision_ID**

  <badge color="warning">NOT_CREATED</badge>

  **Delta_Scope**

  `READ_ONLY / L2-A-GOVERNANCE-PORTFOLIO`

  - 只核验现有 Issue、PR、分支、规范及证据。
  - 不创建新载体。
  - 不改变 Owner、Issue、PR 或 Git 状态。
  - 不产生任何新的规范批准。

  **Relevant_Artifacts**

  已列于 §11.1–11.4，包含完整路径、Commit SHA、Blob SHA。

  **Evidence**

  - GitHub API 实时读取。
  - Branch HEAD 实际核验。
  - Issue/PR 正文和评论读取。
  - 正式 Reviews 和 Review Threads 查询。
  - Branch Protection 状态读取。
  - Exact-Head CI 记录读取。

  **Verification**

  <badge color="success">GitHub 只读取证完成</badge>

  <badge color="warning">本会话未运行测试</badge>

  **Unresolved_Findings**

  1. 九个 Owner Baseline 尚未批准。
  2. 模板和 Rollout 文件尚未进入 main。
  3. 五项 REQ 的角色指派尚未完成实际责任链登记。
  4. #43 G1–G8 尚无已确认 PASS。
  5. #254 尚未完成逐项正式 Finding 归属。
  6. #271 尚未取得当前 Head 的合格独立审查。
  7. #275 存在冻结期创建违规，保持 HOLD。
  8. #134 平台合并门禁仍未解决。
  9. #24/#30/#41 执行模型存在未解决冲突。
  10. AI-EXEC-002 v1.1/v1.2 与 AI-STD-001 §5.1 的规范层级冲突仍然存在。
  11. 产品级运行时及工程责任主体尚未得到完整确认。
  12. 配额冻结尚未正式解除。
</box>

### 11.6 最终结论

<box border radius="lg" padding={3} gap={2}>
  <title size="xl" color="danger">NOT READY</title>
  **L2 治理 Portfolio 对齐尚未完成。**

  已经具备：
  - 九份模块提案；
  - 五项需求角色指派裁决；
  - PR-GOVERNANCE-001 正式采纳；
  - 多项跨域技术研究；
  - 一定数量的精确版本和测试证据。

  但尚不具备：
  - 九位 Owner 的正式 Baseline 决定；
  - 完整跨域接受矩阵；
  - 无冲突的规范层级；
  - 完整的独立审查和 Exact-Head 证据；
  - 系统级实现和运行验收；
  - Project Governance Authority 的正式 G0 批准。
</box>

**我认为 A 当前最应该做的不是继续扩大规范和研究范围，而是收敛三个事情：**

1. 把 A–I 的真实权威、责任和接受关系固定下来。
2. 把 #43 中所有根本性跨域冲突转给正确的领域 Owner，并要求精确版本决定。
3. 将技术研究转化为有实际实现证据的最小纵向闭环，而不是继续累积架构文档。

本报告仅在当前对话中交付。由于本单元明确为只读，没有向 #11、#43 或其他既有 Issue 发布 Closeout 评论，因此不能声称已经完成 GitHub 持久登记。

**提交给 Owner A：** 请将本报告作为 L2 独立核验输入；保留所有 OPEN、HOLD、NOT_ASSIGNED 和 ADR-BLOCKED 状态，不要将本报告解释为 A–I 的批准或项目 G0 决议。

