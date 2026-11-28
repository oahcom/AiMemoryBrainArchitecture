---
document_metadata:
  steward: "Architecture Governance"
  domain: ai-development
  role: normative-standard
  lifecycle:
    approval:
      decision_status: Under-Review
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Applicable-To-Current-Version
      evidence_reference:
        - "00-governance/schemas/work-item-registry.source-rules.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "本文件是非规范权威的简体中文镜像；尚无独立治理批准和验证记录。"
    usage_status: Active
    modification_status: Unchanged
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "AI 开发：工作项注册表源规则"
    canonical_scope_id: "ai-development/work-item-registry/source-rules"
    canonical_scope_keywords:
      - work-item-registry
      - source-rules
      - manifest
      - field-state
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Normative
  bilingual_counterpart:
    source: "00-governance/schemas/work-item-registry.source-rules.md"
    en: "docs/en/00-governance/schemas/work-item-registry.source-rules.md"
---

# 规范性工作项注册表——源规则

## 1. 权威模型

规范性注册表是工作项字段规范化取值的唯一权威来源。本文件定义一个值如何进入注册表，以及如何在注册表中变更。

以下内容属于投影或证据载体，不构成独立权威：

- `14-ai-development/work-items/INDEX.md`
- 各工作项自己的 `manifest.yaml`
- PR 描述和 Issue 描述
- 评论、审查、会话证据和 CI 输出

不得仅仅因为投影中的文本与注册表不同，就用投影覆盖规范值。

每个规范字段值 MUST 至少有一个来源引用。没有可验证来源的值 MUST 记录为 `UNCONFIRMED`，不得推断。

## 2. 证据优先级

针对正在解析的具体字段应用以下优先级。某个来源对一个字段具有权威性，并不意味着它对其他字段也具有权威性。

1. 明确且可归属的 Owner 决策或授权；该字段必须属于此人的权限范围，并且决策必须标明工作项及其范围。
2. 精确 Git 对象证据：固定提交中的文件字节、树成员关系、提交元数据或精确差异。
3. 已合并治理制品中的明确结构化记录，前提是其 schema 和适用范围授权该字段。
4. 由问责权威发布且可归属、无歧义的 Issue/PR 正文或评论。
5. 可佐证的审查、CI 或实现证据。
6. INDEX 展示文本或派生说明文字。

较晚出现的来源不会自动优先于较早来源。它必须获得授权以取代原来源，并且必须明确指出被变更的值。

同等优先级的来源发生冲突时，记录 `UNCONFIRMED` 并保留两个来源。不得依据时间戳、少数服从多数、PR 合并顺序，或哪份副本更容易解析来解决冲突。

## 3. `work_item_id`

权威来源：
- 规范注册表命名空间中的精确目录/manifest 身份。
- 在仓库适用 ID 认领注册机制时，使用预留 ID 认领记录。

规则：
- 格式 MUST 为 `AID-YYYY-NNN`。
- 目录名称本身不能证明其中的 manifest 声明了相同 ID。
- manifest 中的 `work_item_id` 与目录名不一致时，构成冲突。
- 两个不同的规范记录路径声明同一个 ID，构成硬性唯一性违规。
- 除非获得授权的记录明确变更 ID，否则目录重命名不构成 ID 变更。
- 不得从 PR 编号、Issue 编号、标题、分支名或相邻目录推断缺失的 ID。

未知/不匹配：
- ID 缺失：`UNKNOWN`。
- 目录 ID 与 manifest ID 冲突：`UNCONFIRMED`。
- 不同规范注册记录之间出现重复 ID：拒绝此次注册表更新。

## 4. `title`

权威来源：
- 明确指定的标题来源的精确 UTF-8 字节，必须在解析或规范化之前保留。
- 如果标题定义在 manifest 中，原始 manifest scalar 是证据；当 YAML parser 改变了原值时，parser 的解析结果不具权威性。

YAML 截断规则：
- 未加引号的 ` #` 在 YAML plain scalar 中表示注释开始。
- 因此，当原始字节中的标题 scalar 包含未加引号的 ` #` 时，MUST NOT 将解析后的 YAML 值视为完整标题。
- MUST 使用能够理解引号、转义、块标量和行边界的 YAML 感知型源码跨度解析器，或精确的字节级提取方法恢复原始 scalar。
- 简单地在 ` #` 处分割是不充分的，因为带引号的 scalar 和块标量具有不同语义。
- 如果原始提取无法在没有歧义的情况下确定预期完整 scalar，标题 MUST 为 `UNCONFIRMED`。

对于已知的五个被截断标题：
- 不得将解析后的 YAML 值复制到注册表。
- 未经佐证，不得复制 INDEX 文本。
- 比较原始 manifest 字节、精确的历史 Git 版本，以及来源 Issue/PR 中任何明确的标题声明。
- 如果这些来源共同确定了唯一且完全相同的标题，则记录为 `KNOWN`。
- 如果这些来源相互矛盾，或无法确定原始预期标题，则记录为 `UNCONFIRMED`，并在 provenance 证据中保留所有候选值。

除非 PR 明确声明其标题就是规范工作项标题，否则 MUST NOT 从 PR 标题重建工作项标题。

## 5. `owner`

Owner 是由多个角色组成的结构化集合。MUST NOT 将其压平为单个账户名称字符串。

字段：
- `owner.accountable_owner`：对工作项承担问责责任的主体。
- `owner.attribution`：被记载为发起或参与该工作项的主体。
- `owner.authority`：允许对工作项范围或验收作出决策的权威或授权依据。
- `owner.resolution`：现有来源之间的关系及其处理结果。

来源处理：
- 顶层 `accountable_owner` 是问责责任角色的证据。
- 只有当包含它的 authority 对象明确定义了该含义时，`authority.accountable_owner` 才是问责责任角色的证据。
- `attribution` 是归属证据，不能自动替代问责责任。
- INDEX 复合文本属于展示投影。只有在每个组成部分都能追溯到来源时，才 MUST 对其进行拆分。
- MUST NOT 将 GitHub 登录名、提交作者、PR 作者、实现会话或代理发布者推断为自然人问责责任人。

优先级：
1. 针对该工作项的明确、可归属 Owner 任命或决策。
2. 明确的结构化 `authority.accountable_owner`，前提是 authority 记录有效且适用于该工作项。
3. 明确的结构化顶层 `accountable_owner`。
4. 其他结构化 Owner 字段，但仅用于其声明的角色。
5. INDEX 复合文本，仅作为佐证。

冲突规则：
- 如果 `accountable_owner` 与 `authority.accountable_owner` 一致，记录规范化后的问责责任人，并保留两个来源引用。
- 如果二者不一致，且没有获得授权的后续决策解决冲突，则 `accountable_owner.state` MUST 为 `UNCONFIRMED`。
- 即使 `attribution` 与问责责任人取值相同，也 MUST 保留为独立字段。
- 如果 INDEX 单元格组合了多个角色，只有来源文本明确识别这些角色时才可拆分；否则受影响角色为 `UNCONFIRMED`。
- 代理行为 MUST 记录为代理归属/权威证据；MUST NOT 将其表示为自然人 Owner 的签名。

已知来源形态：
- 六条 INDEX Owner 与 `attribution` 相同的记录，仍然只是归属证据，除非另有来源确立问责责任。
- 六份没有 Owner 字段的 manifest MUST NOT 从 INDEX 继承 Owner。
- 十二条 `authority.accountable_owner` 记录是问责责任证据候选项，但仍须验证其范围和权威性。
- 十八个 INDEX 复合 Owner 单元格 MUST NOT 被视为单一规范 Owner 值。

## 6. `class`

权威来源：
- 获得授权的工作项记录中的明确结构化分类，或获得授权的分类决策。
- 旧版 manifest 或 INDEX 标签仅属于迁移证据。

规则：
- 只有当旧值到规范枚举的映射明确且有文档记录时，才可进行映射。
- 不得根据标题关键词、文件路径、PR 标签或实现语言推断 class。
- 如果存在两个合理的规范类别，使用 `UNCONFIRMED`。
- 如果字段已知是有意留空，使用 `KNOWN_EMPTY`。
- 如果尚未作出分类，使用 `UNDECIDED`，而不是 `UNKNOWN`。

## 7. `risk`

权威来源：
- 由获授权的审查者或风险责任人作出的明确风险分类，并具有范围和证据。
- 现有的 `risk`、`risk_level` 或 INDEX 风险标签，在其含义被映射到规范枚举之前，都仅属于证据。

规则：
- 不得根据标题或 Issue 描述中的严重程度词语推断风险。
- 不得将实现优先级等同于风险。
- 不得将“未记录风险”等同于 `LOW`。
- `UNKNOWN` 表示不存在可靠的风险证据。
- `UNDECIDED` 表示需要进行评估，但尚未作出决定。
- `NOT_APPLICABLE` 必须有明确理由说明风险分类为何不适用。
- 风险来源之间存在冲突时，使用 `UNCONFIRMED`。

## 8. `status`

权威来源：
- 工作项实际生命周期记录，并由精确的已合并 PR、仓库和验收证据支持。
- INDEX 中的 status token 是投影，不是生命周期权威来源。
- 自由格式的状态说明文字不是机器生命周期 token。

规范状态 token：
- `PROPOSED`
- `DISPATCHED`
- `IN_PROGRESS`
- `BLOCKED`
- `IN_REVIEW`
- `MERGED`
- `VERIFIED`
- `ACCEPTED`
- `REJECTED`
- `CANCELLED`
- `SUPERSEDED`

INDEX 解析：
- 仅从注册表导入器维护的明确 allowlist 中，解析整个单元格开头的已识别 token。
- token 必须通过已识别分隔符与后续说明文字分开。
- 分隔符和剩余说明 MUST 分别保留为 `status_note` 证据；MUST NOT 将说明文字附加到 token。
- `—` 后跟说明文字、`-` 后跟说明文字以及其他分隔形式，都是格式模式，不是状态值。
- 一个单元格包含多个互斥生命周期 token 时，使用 `UNCONFIRMED`。
- 如果单元格没有可识别 token，不得从说明文字分配生命周期状态。如果其中包含有歧义的状态声明，则为 `UNCONFIRMED`；否则为 `UNKNOWN`。
- 导入器 MUST NOT 仅因为 PR 已关闭就推断 `MERGED`。
- `MERGED` 需要已合并 PR 或等效的精确合并证据。
- `VERIFIED` 需要针对精确相关制品/head 的验证证据。
- `ACCEPTED` 需要由获授权的验收权威作出的明确验收决定。
- `SUPERSEDED` 需要有效的后继关系。

已知 INDEX 分布：
- 66 个 `—` 加说明文字的单元格、8 个 `-` 加说明文字的单元格，以及 8 个使用其他分隔符的单元格，MUST 作为 token 加说明的候选项处理，不得复制成合并后的状态字符串。
- 26 个包含互斥 token 的单元格，在生命周期含义得到解决之前 MUST 为 `UNCONFIRMED`。
- 这些数量是迁移诊断数据，不是永久 schema 常量。

## 9. `prompt`

Prompt 身份是一个多字段记录。单独的 prompt ID 不是内容固定标识；单独的摘要也不是定位符。

字段：
- `prompt_id`：prompt 的身份标识。
- `prompt_sha256`：按照声明的规范字节约定，对精确 prompt 字节计算的摘要。
- `prompt_path`：仓库路径或其他精确定位符。
- `prompt_version`：明确的版本标识。
- `prompt_commit_sha`：包含 prompt 字节的 Git commit。
- `provenance_note`：历史说明或旧版证据。

足以证明 `PINNED` 的证据：
- 已验证的 prompt 定位符。
- 该定位符处的精确字节。
- 根据这些精确字节计算的 SHA-256 摘要。
- 一致的 prompt 身份/版本关系。
- 能够识别 commit 或不可变制品的来源引用。

`IDENTIFIED_UNPINNED`：
- 已确定 prompt ID 和/或精确路径，但没有经过验证的摘要。

`LEGACY_PROVENANCE_ONLY`：
- 唯一可用的 prompt 身份证据是历史自由文本 provenance 说明。
- MUST NOT 将此状态视为完整 prompt 固定标识。

`NOT_PRESENT`：
- 权威来源明确声明没有适用或使用 prompt，且符合该工作项声明的流程。
- 仅仅缺少 `prompt_id` 不能证明 `NOT_PRESENT`。

已知来源形态：
- 56 条没有 `prompt_id` 的记录 MUST NOT 获得虚构的 ID。
- 6 条有 `prompt_id` 但没有 `prompt_sha256` 的记录 MUST NOT 标记为 `PINNED`；它们最多只能是 `IDENTIFIED_UNPINNED`。
- 对于 AID-2026-064，`prompt_provenance_note` 仅是历史证据。不得通过提取或猜测将其转化为 prompt ID 或摘要。
- 没有经过验证的字节定位符的摘要不是固定标识。
- ID 加空摘要不是完整的 prompt 记录。
- 猜测的 prompt 路径、分支名称或最新 prompt 文件不是证据。

## 10. `provenance`

权威来源：
- 附着在每个字段上的证据，而不是笼统声称 manifest 可信。

等级：
- `PRIMARY`：针对该字段具有精确范围的直接权威来源。
- `CORROBORATED`：两个或更多独立来源一致，但没有任何单一来源能够独立构成直接权威。
- `DERIVED`：根据已识别的 primary 证据进行确定性计算所得。
- `CONFLICTED`：primary 来源或同等优先级来源相互矛盾。
- `UNCONFIRMED`：证据不足以确立该字段。

规则：
- provenance 等级 MUST NOT 高于确立该字段所需的最弱实质性来源。
- 派生值 MUST 记录推导过程以及所有输入来源引用。
- CI 成功只能证明实际执行过的检查；除非检查明确验证了相关命题，否则不能证明作者身份、Owner 身份或验收。
- 已合并 PR 证明合并状态和合并 commit，不证明验收。
- commit 作者字段证明 Git 元数据，不证明自然人身份。
- 代理发布证明代理行为及其声明的授权，不证明委托 Owner 亲自发布。

## 11. `supersedes` 和 `superseded_by`

权威来源：
- 明确的工作项替代决策，或无歧义且获得授权的后继声明。

规则：
- 两个方向 MUST 保持一致。
- MUST NOT 仅仅因为两个 PR 标题相似或修改了相同文件，就推断存在 supersession 边。
- 重复载体不自动构成后继工作项。
- 使用相同工作项 ID 的载体 PR 替换，不会在工作项之间创建 supersession 边。
- 环路无效。
- 除非迁移期间明确标记为 `UNCONFIRMED`，否则目标记录缺失属于验证失败。

## 12. `source_refs`

权威来源：
- 精确 Git 路径和 commit、GitHub Issue/PR/评论/审查标识符、CI run 标识符，或不可变的外部文档定位符。

规则：
- 每个定位符 MUST 解析到预期对象。
- 用作证据的 Git 引用 MUST 包含不可变 commit SHA。
- 没有 commit SHA 的分支名称或 `main` 不是不可变证据。
- source reference MUST 声明其角色：`PRIMARY`、`CORROBORATING`、`HISTORICAL` 或 `CONTRADICTING`。
- 不得引用 PR head SHA 作为合并证据；应使用实际 merge commit。
- 不得引用已合并 PR 来证明其正文中的每项陈述都已获接受。
- 选择规范来源后仍须保留矛盾来源，不得删除。

## 13. 迁移和写入规则

- 解析或重写之前，必须保留原始 manifest 字节。
- 在所有有损 scalar 情况得到解决之前，绝不得通过 parser 和 serializer 往返处理 manifest，并将其称为“规范化”。
- 不得从未确认的注册表字段生成 INDEX 值。
- 注册表更新 MUST 只修改正在变更的工作项记录，除非存在明确的跨记录关系更新。
- 注册表验证器 MUST 拒绝重复工作项 ID、无效 supersession 图、无效来源引用和非法状态转换。
- 注册表写入器 MUST 针对预期的当前 blob SHA 使用 compare-and-swap 语义。过期写入器 MUST 失败，而不是覆盖。
- 合并冲突 MUST 通过比较来源证据解决，而不是选择第一行、最后一行或最短的一行。
- 未知的旧版数据 MUST 继续明确标记为未知。MUST NOT 通过编造值来实现迁移完整性。