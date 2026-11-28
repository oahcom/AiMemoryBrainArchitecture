---
document_metadata:
  steward: "Architecture Governance"
  domain: ai-development
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Implementation and repository enforcement have not yet been independently verified."
    usage_status: Active
    modification_status: Modified
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
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# 会话身份棘轮

- 文档 ID：SESSION-IDENTITY-RATCHET
- 版本：1.0
- 状态：DRAFT
- 范围：治理基础设施
- 实现：`scripts/ci/check_session_identity.py`
- 必需检查上下文：`Session identity ratchet`

## 1. 问题陈述

现有的 Session Evidence 验证器能够确立结构有效性。
但它不能确立所声明的会话标识符是否代表一个在语法上可识别的会话。

仓库实测清单表明，需要引入增量式控制：

- 存在 132 个 manifest。
- 其中 93 个 manifest 包含 session_evidence。
- 共存在 104 条会话证据记录。
- 只有 5 条记录包含可解析的 UUID 会话标识符。
- 39 条记录包含哨兵值。
- 60 条记录包含人类可读标签。
- 64 条记录声明为 RECORDED，但只有 5 条包含 UUID。
- 11 条记录声明为 RECORDED，同时包含哨兵值。
- 12 条记录声明为 NOT_RECORDED，同时包含人类可读标签。

如果直接替换现有验证器，历史不一致将变成整个仓库范围的阻断性失败。

这不是可接受的迁移策略。

## 2. 为什么采用棘轮，而不是一次性修复

会话身份棘轮引入一项新的、独立强制执行的检查，而不改变现有的 Session Evidence 验证器。

现有违规会被冻结到一个生成的基线中。

该基线是历史例外的明确清单，并不表示批准这些例外。

强制执行规则如下：

1. 基线中存在的违规会被报告，但不会阻断。
2. 基线中不存在的违规会阻断。
3. 修复一项违规后，该违规会从当前违规集合中移除。
4. 随后必须移除对应的基线条目。
5. 不再对应实际违规的基线条目属于陈旧条目；在缩减基线之前会造成阻断。
6. 禁止扩充基线。
7. 无效 YAML 永远不能被抑制。

这样既能让现有工作项继续可用，也能确保新引入的身份缺陷不会悄然累积。

因此，迁移过程会单调地朝零违规推进。

## 3. 可解析的会话身份

检查器接受三种标识符表示形式：UUID v4、UUID v8，以及平台会话标识符。

### 3.1 UUID v4 和 UUID v8

当规范的 36 字符 UUID 满足以下任一格式的版本位和变体位要求时，即可接受：

- UUID v4：版本 nibble 为 `4`。
- UUID v8：版本 nibble 为 `8`。

两个版本都必须满足 RFC 4122 变体要求：

- 变体 nibble 必须为 `8`、`9`、`A` 或 `B`。

完整 UUID 布局如下：

- 8 个十六进制字符
- 连字符
- 4 个十六进制字符
- 连字符
- 版本 nibble `4` 或 `8`，后接 3 个十六进制字符
- 连字符
- RFC 变体 nibble `8`、`9`、`A` 或 `B`，后接 3 个十六进制字符
- 连字符
- 12 个十六进制字符

示例：

UUID v4：

`550e8400-e29b-41d4-a716-446655440000`

UUID v8：

`6b09360b-13cc-83ec-abfd-aa0e6362566c`

仓库中现有的会话标识符，包括：

- `6b092534-81b4-83ec-a4de-49c5c6ecaa8b`
- `6b090a00-c1b0-83ec-ad26-9668c882a144`
- `6b0926ee-d24c-83ec-9ce4-69e18656db14`
- `6b092946-cf54-83ec-81bc-cb7e7993ed28`

均为有效的 UUID v8 标识符。

拒绝 UUID v4 和 UUID v8 以外的版本。

拒绝变体 nibble 不属于 `8`、`9`、`A` 和 `B` 的 UUID。

检查器会验证完整格式，包括版本位和变体位，而不只是检查 UUID 长度或十六进制布局。

### 3.2 会话标识符

符合以下形式的会话标识符：

`conv_<32-or-more-hexadecimal-characters>`

示例：

`conv_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`

前缀不区分大小写。十六进制后缀必须至少包含 32 个字符。

### 3.3 明确排除项

以下内容不能作为可解析的会话标识符：

- `S6-B`
- `ChatGPT-GPT-6`
- `opencode-go/deepseek-v4.1-flash`
- UUID v3 标识符
- 具有非 RFC 变体位的 UUID
- `NOT_RECORDED`
- `NOT_AVAILABLE`
- `NOT_EXPOSED_BY_PLATFORM`
- 任意标签和任意非空字符串

可解析性只能证明符合一种已接受的标识符格式。
它不能证明会话确实存在，也不能证明其证据真实可信。

## 4. 状态一致性

接受以下两种状态值：

- `RECORDED`
- `NOT_RECORDED`

适用以下不变量。

| 状态 | implementing_ai_session | 结果 |
|---|---|---|
| RECORDED | UUID v4 | 有效 |
| RECORDED | conv_ 标识符 | 有效 |
| RECORDED | 哨兵值 | 无效 |
| RECORDED | 人类可读标签 | 无效 |
| NOT_RECORDED | 哨兵值 | 有效 |
| NOT_RECORDED | 人类可读标签 | 无效 |
| NOT_RECORDED | UUID 或 conv_ 标识符 | 无效 |

缺少必需字段本身即为无效。

比较哨兵值之前，会先去除其周围的空白字符，再以不区分大小写的方式进行比较。

## 5. 违规代码

### SESSION_UNPARSEABLE

状态为 RECORDED，但提供的值既不是可接受的 UUID v4，也不是可接受的会话标识符。

示例：

- RECORDED + S6-B
- RECORDED + ChatGPT-GPT-6

### SESSION_SENTINEL_MISMATCH

状态为 NOT_RECORDED，但该值不是已识别的哨兵值。

这可以防止将人类可读标签表示为未记录的会话。

### SESSION_RECORDED_SENTINEL

状态为 RECORDED，但该值是已识别的哨兵值。

由于这是声明与值之间的直接矛盾，因此会与 SESSION_UNPARSEABLE 分开报告。

### 其他结构性违规

- SESSION_FIELD_MISSING：必需字段缺失、为 null、为空，或条目结构无效。
- SESSION_STATUS_INVALID：声明了不受支持的状态。
- SESSION_YAML_INVALID：manifest 无法解析，或其顶层结构无效。

YAML 错误始终计为新违规。

## 6. 基线格式与所有权

规范位置：

`scripts/ci/baselines/session-identity.txt`

首次创建时，必须明确针对目标分支执行 bootstrap：

`python3 scripts/ci/check_session_identity.py --bootstrap-baseline --base-ref origin/main`

Bootstrap 基线内容仅从 `--base-ref` 所引用的工作项树生成，而不是从当前工作树生成。Bootstrap 会冻结目标分支树中已经存在的违规；如果当前树包含目标分支树中不存在的违规，则拒绝执行。

每条基线记录由以下内容组成：

`CODE manifest-path#entry-index`

条目索引从 1 开始。

路径和条目索引用于区分各个具体发现。违规代码用于区分发现的类型。

基线是门禁输入，不允许手动编辑。

首次 bootstrap 后，后续基线生成只能移除条目。常规 `--write-baseline` 命令要求基线已经存在，不能创建或扩充基线。

如果当前树引入了基线中尚不存在的发现，基线生成将拒绝继续。

如果某项发现已经消失，生成过程会将其移除。

删除基线文件不会重置棘轮：当基线缺失时，常规检查和常规 `--write-baseline` 都会以代码 `2` 退出。

检查器在正常执行期间也会拒绝陈旧的基线条目。

这可以防止基线演变为永久豁免清单。

## 7. 与 Session Evidence 的关系

现有的 `Session Evidence` 必需检查上下文保持不变。

其现有实现为：

`scripts/governance/session_evidence/validate.py`

该验证器继续负责其现有判定，包括结构字段、证据路径、哈希值和字节数。

新检查器不会修改或替代这些判定。

职责划分如下：

| 控制项 | 职责 |
|---|---|
| Session Evidence | 现有证据的结构与完整性 |
| Session identity ratchet | 语义身份格式与状态一致性 |

这两项检查是相互独立的必需检查上下文。

这种分离是有意为之。修改现有验证器会改变 132 个 manifest 的历史检查结果，并违反非阻断式迁移要求。

## 8. 工作流强制执行

工作流：

`.github/workflows/session-identity-ratchet.yml`

必需作业上下文：

`Session identity ratchet`

触发条件：

- pull_request: opened
- pull_request: synchronize
- pull_request: reopened
- pull_request: ready_for_review
- push to main

该作业会在扫描仓库之前运行隔离的检查器测试。

该作业只使用 checkout 本地文件。它不会访问 GitHub API、网络服务、外部会话平台或远程证据存储。

必须将该必需上下文添加到仓库的必需状态检查声明和保护配置中。

工作流的存在本身并不能证明平台已强制执行该检查。

## 9. 未来收紧

第一版实现有意将强制执行范围限制在会话身份和状态一致性。

它不包括独立审查者完整性。

实测仓库中有 47 个 manifest 包含 independent_reviewer，其中 NOT_ASSIGNED 和 NOT_APPOINTED 合计占 77.1%。

最近的 20 个工作项中，没有任何一次实际独立审查。

这是一个独立的治理缺陷，不得悄然混入初始身份基线。

未来的棘轮扩展应引入：

1. 明确定义可解析的审查者会话身份。
2. 区分实际独立审查者与占位值。
3. 建立可验证的审查者会话与实施会话之间的关系。
4. 独立的违规清单和基线。
5. 针对同一会话自我审查和委派角色模拟的测试。
6. 保留历史记录、只允许缩减的迁移方式。

最终目标是禁止新增 NOT_ASSIGNED 和 NOT_APPOINTED 审查者声明，同时允许历史条目逐步得到修复。

未来扩展不得削弱或替代此处确立的会话身份不变量。

## 10. 验收边界

检查器通过意味着：

- 冻结基线之外不存在新的会话身份违规。
- 基线不包含陈旧条目。
- 所有包含 session_evidence 的 manifest 均已检查。
- 无效 YAML 未被抑制。

Bootstrap 会冻结目标分支树中已经存在的违规。只有当当前树包含目标分支树中不存在的违规时，它才会拒绝执行。使用
`--bootstrap-baseline --base-ref cb5b3dcd`
验证了负向情形：由于当前树包含两个在该基线树中不存在的违规，该命令以 `1` 退出。

当前基线由检查器根据目标分支树
`3da2e32cf0475a5d7645862a4a288988f69f09cc` 重新生成。目标树前进后，原有基线已与更新后的目标树不一致；检查器拒绝在这种不一致状态下继续，因此必须从更新后的目标树重新生成基线。这不是手动编辑，也不是扩大棘轮允许范围。

该基线包括 `AID-2026-265` 和 `AID-2026-291` 中已有的违规，因为这两个工作项都存在于目标分支树中。修复它们属于独立工作项；本 PR 不修改这两个工作项的任何文件。
它不意味着：

- 每个历史会话都已恢复。
- UUID 能证明真实的平台会话存在。
- Prompt 来源已得到验证。
- 已经执行了独立审查。
- 每条历史会话证据记录都是真实可信的。

这些主张需要独立证据和独立控制。


## 12. 为什么采用相对 base 的差分，而不是基线快照

2026-11-28 的迁移依据是 83 次 workflow run 采样：65 次 failure、18 次 success，失败率约 78%；最近 8 次依次为 failure、failure、failure、failure、success、success、failure、failure。main 上的检查器报告 92 项违规，其中 91 项已基线化、1 项新增；唯一新增项为 SESSION_UNPARSEABLE 14-ai-development/work-items/AID-2026-297/manifest.yaml#1，由 PR #1513 引入。库存统计另报告 no_evidence_section=39。这些测量说明，持续失败主要来自快照把 PR base 已存在的债务错误归因给后续 PR，而不是每个 PR 都引入违规。

旧快照机制存在两个恢复死结：--write-baseline 只允许缩小，current - previous 非空便以 exit 1 拒绝；--bootstrap-baseline --base-ref REF 又要求 REF 树不含 baseline 文件，而 baseline 已经存在于 main。基线一旦落入目标分支，常规操作无法重新锚定。共享文件还集中所有权，使并行 PR 更新时产生持续冲突。

差分模式以 violations(current_tree) - violations(base_tree) 作为 PR 增量判据。存量债务自动吸收；PR 无需修改或合并 baseline 文件；不再需要人工记忆基线是否最新；检查可直接挂入既有 required job，而不引入新的 required context。base 中存在、HEAD 中消失的违规是修复，不是新增；base 中没有、HEAD 中出现的违规必须逐条以 NEW: 前缀输出并以 exit 1 阻断。

差分模式不读取、不写入、也不要求 baseline 文件。当前树中的 SESSION_YAML_INVALID 永远失败；base 树中的 YAML 无效项作为已存在债务报告，不计入新增项。无法解析 ref、非 Git 工作树、shallow clone 或缺失 Git 对象均以 exit 2 失败关闭。--diff-base 与旧 baseline 写入/初始化参数互斥。

存量债务不会因差分门禁而自动消失。PR 自己引入的违规仍然失败；但直接 push 到 main 引入的违规会成为下一次 PR 的 base 债务。该缺口必须由 main 上的定期全量扫描和告警暴露，不能声称 PR 差分门禁能够发现它。因此，差分门禁防止 PR 增量，但不证明 main 全量无债务。

本次检查只作为 step 挂入 Repository hygiene (hard gate)，保持 job ID、job name 和既有 required context 不变。Session identity ratchet 不在 PR-GOVERNANCE-001 §7 声明的 16 项 required context 中；真正生效的是 Repository hygiene (hard gate) 内部的 step。新增 required context 会使已打开且未生成该 check run 的 PR 永久处于 required check absent 状态；实测 18 个 open PR 中只有 2 个曾生成旧 ratchet check run。

83-run 样本、65/18 结果、最近 8 次序列、92/91/1 计数、AID-2026-297 具体发现、两个恢复死结，以及 required-job 迁移依据均来自 2026-11-28 协调方提供的实测记录；它们不是本 PR 重新执行的测量结果。
