# AI-REQTRACE-001 — GitHub 需求可追溯性标准

- **文档 ID：** AI-REQTRACE-001
- **版本：** 1.1
- **状态：** PROPOSED（提议）
- **生效日期：** NOT_EFFECTIVE
- **Owner：** 项目 Owner（待确认）
- **维护者：** Integration Owner（拟任）
- **范围：** 全仓库
- **语言：** 中文语义等效版本；英文版为规范主文本
- **配套文件：** AI-REQTRACE-001.md

## 1. 目的

本标准建立基于 GitHub 的长期项目需求记录、识别、管理和追溯机制，确保需求不只存在于 ChatGPT 对话中；每项获批准的伞形需求具有稳定 GitHub 身份；原始意图得到保留；需求执行可通过 Work Item、子 Issue、Pull Request、commit 和验证证据追溯；需求满足与实现活动明确区分；并防止重复需求载体及不必要的 Issue/PR 膨胀。

本标准不引入独立数据库、自定义编排器或脚本硬阻断系统。GitHub Issues、Pull Requests、仓库文档、现有 Work Item 记录和既有工作流仍是权威运行基础设施。

## 2. 规范用语与已裁定决策

MUST、MUST NOT、SHOULD、SHOULD NOT、MAY 分别表达规范强度。AI 生成的提案不构成 Owner 批准。登记、接受、执行和满足是不同状态。

REQ-TRACE Phase 0 L4 裁定具有约束力且已定案。本标准只落实、不重新开启以下七项决策：(1) 五个需求维度；(2) 五个固定主标签；(3) 需求生命周期；(4) 原始证据保全；(5) PR 引用语义；(6) 有界的初始登记例外；(7) 需求身份与执行身份分离。

## 3. 权威与上位标准

本标准受项目既有治理体系和 Owner 权威约束。相关标准包括 AI-STD-001、AI-PROC-001、AI-EXEC-001、AI-EXEC-002、PR-GOVERNANCE-001、AI-ARCH-002、GOV-DOC-001，以及适用时的 AI-PROMPT-STD-001。

发现冲突时，必须保留既有权威层级、明确记录冲突、不得默默取代其他规范文件、提交 Owner 或获授权治理方裁定，并通过可审计 PR 更新受影响标准。本标准不自行修改任何上位标准的权威。

## 4. 需求身份与维度

### 4.1 伞形需求

伞形需求是持久的长期项目需求，表达连贯方向、目标或用户期望，可能需要多个执行单元和交付物。它不是单个实现任务、单个 PR、单个 AI 会话、临时缺陷报告，也不等同于单项技术决策。

### 4.2 规范身份

每项获批准的伞形需求 MUST 拥有唯一规范 GitHub Issue。Requirement ID 与 Issue 编号共同标识该需求。即使 Issue 标题或相关实现发生变化，Requirement ID 仍 MUST 保持稳定。Requirement ID 标识长期需求；AID 标识执行单元；会话和提示词标识执行来源。这些身份 MUST NOT 相互替代。

AID MUST 在适用时引用对应 Requirement ID 和 Issue 编号。一项需求 MAY 对应多个 AID、子 Issue 和 PR；一个 AID 或子 Issue MAY 对多项需求作出贡献。每项关联 MUST 说明实际贡献，不要求人为建立一对一关系。

### 4.3 五个已裁定需求维度

初始五个维度固定如下：
- REQ-01 — 风险评估（Risk Assessment）
- REQ-02 — 技术选型（Technology Selection）
- REQ-03 — PR 治理（PR Governance）
- REQ-04 — 架构突破（Architecture Breakthrough）
- REQ-05 — 文档管理（Documentation Management）

这些是需求维度，不是生命周期状态或执行任务。不得通过重新标记这组已裁定初始集合来创建未来维度；扩展维度必须取得明确 Owner/治理授权，并通过可审计变更修订本标准。

## 5. 固定主标签

五个固定主标签必须逐字精确使用：
- `requirement/risk`
- `requirement/tech-selection`
- `requirement/pr-governance`
- `requirement/architecture-breakthrough`
- `requirement/documentation`

每个伞形需求 Issue MUST 且只能有一个上述需求维度主标签。映射顺序分别对应 REQ-01 至 REQ-05。标签用于分类，不授予权威、不代表接受，也不替代生命周期状态。仓库政策允许时可以使用其他非维度标签，但不得把它们视为额外的需求维度主标签。

## 6. 原始意图与证据保全

每个需求 Issue MUST 包含 **Original Requirement Evidence（原始需求证据）** 章节。该章节 MUST 原样保留所提供的用户原始措辞；标明来源会话 ID；仅在核实后记录原始日期；日期或完整来源措辞不可得时使用 NOT_RECORDED；区分直接引文与历史摘要；并在需求契约后续修订时保留先前措辞。

AI 生成的摘要 MUST NOT 被表述为用户原始引文。修正或扩展后的契约 MUST 保留旧措辞并记录变更历史。缺失证据必须如实披露，不得重构或伪造引文。

## 7. 需求 Issue 结构

每个伞形需求 Issue MUST 包含：(1) Metadata；(2) Original Requirement Evidence；(3) Requirement Contract；(4) Intent and Expected Outcomes；(5) Scope and Exclusions；(6) Acceptance Criteria；(7) Current Requirement Status；(8) Related AID Work Items；(9) Related Child Issues；(10) Related Pull Requests；(11) Decisions and Evidence；(12) Change History；(13) Governance Notes。

未知值 MUST 明确标记为 NOT_RECORDED、NOT_CONFIRMED 或 NOT_ASSIGNED。不得编造未知信息。

## 8. 需求生命周期

支持的需求状态严格为：RECORDED、PROPOSED、ACCEPTED、ACTIVE、SATISFIED、DEFERRED、REJECTED、SUPERSEDED。登记不代表接受。接受必须有明确 Owner 授权。激活必须存在可识别的执行路径。满足必须有证据和明确 Owner 接受。延期需求必须保持可追溯，并记录原因和恢复条件。被取代需求必须链接替代项。被拒绝需求必须保留其历史意图和拒绝理由。

### 8.1 明确状态转换规则（v1.1 澄清）

正常转换如下：
- 尚未登记 → RECORDED：建立规范 Issue 和最低元数据/证据章节；这仅代表登记。
- RECORDED → PROPOSED：起草需求契约和验收标准。
- PROPOSED → ACCEPTED：记录明确 Owner 授权；或 PROPOSED → REJECTED，并记录 Owner 理由。
- ACCEPTED → ACTIVE：记录责任 Owner 和可识别执行路径；或 ACCEPTED → DEFERRED，并记录原因及恢复条件。
- ACTIVE → SATISFIED：关联证据并记录 Owner 明确接受；或 ACTIVE → DEFERRED，并记录原因及恢复条件。
- DEFERRED → ACCEPTED 或 ACTIVE：复核恢复条件，并记录 Owner/授权方决定。
- RECORDED、PROPOSED、ACCEPTED、ACTIVE 或 DEFERRED → SUPERSEDED：记录替代 Requirement ID/Issue 和 Owner 理由。
- DEFERRED → REJECTED：记录 Owner 拒绝理由。

不得推定存在其他状态转换。REJECTED 和 SUPERSEDED 为终态；若需纠正，必须记录新的可审计决定；若出现实质新意图，应建立新需求，不得默默重开历史。SATISFIED 状态的重开必须有明确 Owner 更正记录、解释先前满足为何不再成立的证据，并记录转为 ACTIVE 或 DEFERRED。

GitHub Issue 的 open/closed 状态是独立的载体生命周期，MUST NOT 替代需求状态。关闭 Issue 本身不代表 SATISFIED；已关闭载体仍可继续承载历史追溯。

## 9. Work Item 与子 Issue

需求层记录长期意图、范围、权威和满足状态。Work Item 层记录可独立识别的执行单元、责任、提示词、证据和结项。现有 AID 约定及规范 `work-items/INDEX.md` 继续具有权威。AID MUST 引用适用的 Requirement ID 和 Issue 编号。

子 Issue 用于记录有界决策、调查、缺陷和交付物。子 Issue SHOULD 标明父需求 Issue、相关 AID、责任角色、预期输出、验收标准、依赖和证据要求。

关系在适当情况下为多对多。一项需求 MAY 有多个 AID 和子 Issue；一个 AID 或子 Issue MAY 对多项需求作出贡献。每项关系都应说明实际贡献。

## 10. PR 可追溯性

### 10.1 必需引用

每个实质 PR MUST 标明：主需求 Issue；其他相关需求 Issue；关联 AID Work Item；适用时的子 Issue；AI-EXEC-002 规定的会话和提示词身份；准确 PR Head SHA；以及验证和审查证据。

### 10.2 引用语义

伞形需求 Issue 使用 `Refs #N`；尚未完成的子 Issue 也使用 `Refs #N`。仅对已完成的子 Issue 使用 `Closes #N`。PR MUST NOT 对伞形需求 Issue 使用自动关闭关键词（包括 `Closes`、`Fixes` 或 `Resolves`）。引用是追溯链接，不是生命周期决定。

### 10.3 贡献与关闭

PR MUST 说明其贡献的需求、具体变更、对应验收标准、支持证据和剩余工作。PR 合并 MUST NOT 自动将伞形需求标记为 SATISFIED，也不得自动关闭其规范 Issue。需求满足必须按 §8 单独取得证据和 Owner 接受。

## 11. 反膨胀规则与初始登记例外

创建需求 Issue 前，创建者 MUST 搜索是否已有规范需求。新 AI 会话、新提示词版本、新 PR、新 commit、常规子任务、讨论更新或状态转换均 MUST NOT 创建新的伞形需求。应复用已有 Issue 和 AID 记录。

新需求必须具备可证明的不同长期意图、重复检查、明确范围、明确 Owner 授权和记录在案的理由。

初始五个历史 Issue 登记集合（REQ-01 至 REQ-05）是一次性、有界例外，仅用于登记五个已裁定的历史维度并保留其来源；它只例外于常规前瞻性登记/授权顺序。该例外不豁免规范身份、证据、精确主标签或生命周期记录；不授权新增其他伞形需求，也不授权无关 Issue/PR 膨胀。任何未来需求均须遵循常规授权和重复检查流程。

## 12. 与既有治理集成

### 12.1 AI-EXEC-001

实质工作开始前，执行规划 MUST 识别所服务的需求。需求身份补充但不替代 Work Item 身份。

### 12.2 AI-EXEC-002

会话身份 MUST 保留既有 Work Item ID、Prompt ID、Prompt Version 和提示词文件 commit SHA 约定。Requirement ID 是额外追溯维度，MUST NOT 替代任何现有身份字段。

### 12.3 PR-GOVERNANCE-001

PR-GOVERNANCE-001 管辖 PR 创建、审查、集成和合并证据。本标准管辖需求身份以及需求到交付物的关系。两者互补。精确 Head 检查、审查独立性、五种处置和目标分支规则仍由 PR-GOVERNANCE-001 管辖。

### 12.4 AI-ARCH-002、AI-PROC-001 与 GOV-DOC-001

架构需求与架构决策 MUST 保持区分；需求不会自动授权某项架构决策。需求识别、登记、细化、执行、审查和满足 SHOULD 遵循既有项目流程。本标准及配套文件 MUST 遵循既有文档结构、manifest 和双语语义一致性要求。

若集成条款与已采用的上位标准冲突，在授权裁定解决前以上位权威层级为准。

## 13. Owner 权威与决策记录

只有指定权威方可以接受、拒绝或宣布需求满足。AI 会话 MAY 提议范围、验收标准、技术方案、执行计划和满足证据。AI 会话 MUST NOT 默默将提案转为已接受决定。

每项重大 Owner 决策 MUST 记录决定、权威方、日期、理由、证据，以及受影响的需求和文档。

## 14. 人工运行合规

本标准通过派发头要求、PR 模板、GitHub Issue 模板、AID 登记约定、Work Item 索引更新、人工审查和结项实施。本标准不假设存在脚本硬阻断机制。MAY 使用 GitHub 原生引用和标签。若已采用，MAY 使用 GitHub Projects，但不得使其成为需求事实的唯一来源。

必须准确披露平台强制控制的缺失。除非实时仓库配置证明确实强制执行，否则不得将模板、标签、评论或 AI 自审表述为硬合并门禁。

## 15. 本标准的接受

本文件保持 PROPOSED，直到记录以下事项：Owner 审查、冲突解决、必需模板和索引变更审查、按既有治理创建 PR、适用的精确 Head 检查、必需的独立审查，以及明确 Owner 采用决定。若无适用权威和证据，不得将已合并文件表述为已获 Owner 采用。

## 16. 初始 rollout

初始 rollout 包括：登记五项历史伞形需求；保留提供的原始措辞和来源；建立规范 Requirement ID；添加主标签；链接现有 AID、Issue 和相关 PR；在另行授权时更新派发和 PR 模板；更新 Work Item 索引约定；执行追溯审计；记录尚未映射的历史工作。

本标准的采用 PR 本身不授权无关实现 PR，也不会自动满足任何伞形需求。

## 17. 变更历史

| 版本 | 状态 | 变更 |
|---|---|---|
| 1.0 | PROPOSED | 初始 GitHub 需求可追溯性设计（本次提供的基线）。 |
| 1.1 | PROPOSED | 澄清精确主标签映射；明确生命周期转换，包括终态/重开处理；限定五项历史登记例外；明确 PR 引用不会关闭伞形需求；说明 Requirement ID、AID 和会话/提示词身份不可相互替代。七项 Phase 0 裁定未改变。 |

## 18. 采用记录

- Owner Decision：PENDING
- Decision Date：NOT_RECORDED
- Adoption Evidence：NOT_RECORDED
- Effective Date：NOT_EFFECTIVE
- Related PR：PENDING
- Bilingual Manifest：COMPLETE（本次变更提供配套版本；语义审查仍须经过独立审查）
