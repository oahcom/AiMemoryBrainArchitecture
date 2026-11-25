---
document_metadata:
  domain: ai-development
  role: normative-standard
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Metadata added on 2026-11-24 so that this file can be edited without tripping DM-01. No content claim in this file is verified by this block."
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
    normative_status: Normative
  bilingual_counterpart:
    source: "14-ai-development/PR-GOVERNANCE-001.md"
    en: "docs/en/14-ai-development/PR-GOVERNANCE-001-ENFORCEMENT.md"
    zh-CN: null
---

# PR-GOVERNANCE-001 — 强制执行与证据补充规范
# PR-GOVERNANCE-001 — Enforcement & Evidence Addendum

- 文档 ID：PR-GOVERNANCE-001-ENFORCEMENT
- 版本：1.2
- 状态：PROPOSED（提议中）——经授权审查并合并后方成为规范性要求
- 上位规范：[PR-GOVERNANCE-001](../../../14-ai-development/PR-GOVERNANCE-001.md)
- 跟踪项：[Issue #130](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/130)、[Issue #134](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/134)
- 英文对应版本：[English](../../en/14-ai-development/PR-GOVERNANCE-001-ENFORCEMENT.md)

## 0. PR 创建与分支合并边界

**只有合并目标为 `main` 时才必须创建 PR。** 该规则适用于所有来源分支，包括 Owner 主分支和子/工作分支：只要目标是 `main`，就必须通过 PR，并满足本补充规范中的准确 Head 检查与独立审查门禁。

合并目标为任何非 `main` 分支时，**不需要 PR**。这包括子/工作分支 → 所属 Owner 主分支、普通工作分支 → Owner 主分支，以及 Owner 主分支 → 其他非 `main` 分支。这些属于 Owner 内部集成操作；责任 Owner 仍须执行必要的范围、测试、证据和安全检查，并将重要决策记录到已有所属工作项。不得仅为表示此类内部合并而创建 PR。

此例外不允许通过先合入其他分支再绕行的方式规避 `main` 的 PR 门禁。创建 PR 前先检索是否已有相同变更和目标分支的 PR，优先更新/复用而不是重复创建。创建 Issue 前先检索已有责任 Issue，优先更新并建立关联。一个会话、子任务或结项记录本身不构成新建 PR/Issue 的理由。只有在确认重复、被取代或已完成，并保留关联链接和原因后，才关闭相应载体。

## 1. 精确 Head 合并门禁

只有当所有适用于变更路径和风险类别的检查，均在 PR 当前准确 Head SHA 上完成并成功，PR 才能标记为 MERGE。结项必须记录 GitHub 实际显示的检查上下文/名称、Workflow Run ID、URL、结论和被测 Head SHA。合并前必须重新读取 PR Head；任何新提交都会使先前的精确 Head 证据失效，必须重新运行受影响的检查。

强制文档门禁：
- 对所有修改受治理文档或 PR manifest 的 PR，必须通过双语文档门禁中的 `GOV-DOC-001 structural checks`。
- 双语清单必须为 `BILINGUAL-MANIFEST: COMPLETE`，或者具有正式批准且有期限的 `BILINGUAL-EXCEPTION: APPROVED`，并记录责任 Owner、缺失的对应文件路径、准确源版本、截止日期和跟踪 Issue。
- 文档 Workflow 变绿本身不证明中英文语义一致；PR 仍必须列出成对文件路径，并披露任何语义差异。

Rust 门禁：
- 修改 `Cargo.toml`、`Cargo.lock`、`crates/**` 或 Rust Workflow 时，必须取得准确 Head 上 Rust Workspace 测试结果，执行命令为 `cargo test --workspace --all-targets`。
- 实测于 2026-11-25：自 #1027 起该 Rust workflow 不再有 `pull_request.paths` 过滤，且 `rust-workspace-test` 是 `main` 上十六个必需上下文之一（分支保护读回于 2026-11-25，`strict: true`，`enforce_admins` 已启用），因此它已在每个 PR 上运行，无需聚合门禁。条件规则：若将来的变更在上下文已属必需的 workflow 上重新引入 `paths` 过滤，该检查会在不匹配的 PR 上被跳过，必须在把该上下文设为必需之前增加始终运行的聚合门禁。

检查缺失、待定、适用时被跳过、失败、Head 过期或无法核验，均不得合并。其他 PR 或后续 main 提交上的运行不能替代本 PR 的精确 Head 证据。

平台检查不可用：
- 检查可能适用，但因已记录的平台故障而无法启动，例如 Actions 计费中断、runner 长期离线、或仓库级 API 拒绝。此时 PR 仍可标记为 MERGE，但验收评论必须完整记录：(a) 存在 run 对象时记录准确 run ID 与 URL，并逐字记录平台消息；(b) 在 PR 准确 Head 上，以完全相同的输入（相同 base SHA、head SHA 与 PR body）本地执行同一仓库内检查脚本的等价执行，其 stdout、stderr、退出码与 SHA-256 归档于 PR 或关联证据文件，并说明该脚本对这些输入为何是确定性的；(c) 按 RULING-06 五字段登记具名例外；(d) 明确声明这是补偿证据，不是检查已通过的证据。
- 该例外仅限当次 PR。平台恢复可运行检查时或到达登记到期日时（以较早者为准）失效；不得复用于后续 PR、不得引为先例跳过检查、不得视为等同于通过检查。

## 2. 审查与批准门禁

- 普通变更至少要求一位与 PR 作者**会话独立**的审查者批准；修改某领域 Owner 规范契约时，必须取得受影响领域 Owner 的批准。独立性是审查会话的属性，不是 GitHub 账号的属性：多个会话可以共用一个身份。
- 新提交推送后必须撤销过期审批。
- 合并前必须解决全部审查讨论。
- COMMENT 不是 APPROVE。独立会话审查自己未撰写、未实现的变更产物，**构成**独立审查，且可以经由作者相同的 GitHub 连接身份提交。撰写会话内部的 AI 角色模拟不构成独立审查：审查者与作者共享同一上下文与同一激励。
- 记录审查者登录名、审查状态、被审查 Head SHA、时间戳/链接、同身份或委派关系披露，以及未解决发现。
- 无法取得独立审批时，处置状态为 HOLD，除非记录了经授权、明确限定范围且有期限的例外。不得自我批准，不得将角色扮演描述为 Owner 批准。

## 2.1 验收评论最小核对表

在 Issue 中发布的验收或合并授权评论——区别于受 PR 模板约束的 PR 正文——必须包含以下四行。本条存在的理由：PR 模板只约束 PR 正文，无法约束自由格式的 Issue 评论；缺少检查结论的验收评论，可能在 exact-Head 检查失败的情况下仍给出 ACCEPT。

必需行：

1. **Exact Head SHA** —— 实际被评估的提交，全写或截断并注明长度。分支名不能替代。
2. **适用检查结论** —— 在该精确 Head 上，每项适用检查的名称、结论与 run URL。若无适用检查，写明「无适用检查」并给出理由。该理由必须能从变更本身客观核验，例如「无任何变更路径匹配任何 workflow 的路径过滤」。仅证明不存在路径过滤匹配的 workflow 不够，还须排除不设路径过滤、始终运行的适用检查。仅由验收方单方断言、无此依据者，不满足本行。
3. **审查状态与审查者身份** —— 审查状态（APPROVED / COMMENTED / REQUESTED_CHANGES / NOT_REVIEWED）、审查者登录名、被审查 Head SHA，以及同身份或委派关系披露。COMMENT 不是 APPROVE。APPROVED 状态仅当批准来自符合 §2 独立性要求的审查者时有效；由与 PR 作者相同 GitHub 身份提交的批准，仅当产出该批准的会话符合 §2 的独立性要求、且评论中披露独立性为会话级时有效；由撰写会话内部 AI 角色模拟产出的批准不构成有效批准，不得记为 APPROVED。凡 §2 对该变更要求批准审查者，状态为 NOT_REVIEWED、COMMENTED 或 REQUESTED_CHANGES 时必须与第 4 行的例外记录配对；未配对者不得承载 ACCEPT。
4. **例外记录** —— 若任一适用检查为失败、缺失、待定、适用时被跳过、Head 过期或无法核验，必须具名登记例外：依据、授权方、范围、到期条件、跟踪 Issue。若无例外，写明「无例外」。

第 4 行例外记录的性质：例外记录是披露与审计机制，不豁免 §1 检查门禁。§2 的例外是对审查与批准门禁的经授权例外，仅限该门禁；检查失败、缺失、待定、适用时被跳过、Head 过期或无法核验等情形，不能仅凭在本核对表登记例外而豁免。只要任一该等检查状态存在，该 PR 即不得合并，该评论亦不得承载 ACCEPT 或合并授权 YES，无论第 4 行登记了何种例外。

无效判定：

缺少上述任一行者，不得视为有效验收，不得承载 ACCEPT 或合并授权 YES。该评论无效，必须撤回并重新发布。撤回必须在同一线程内以追加 VOID 声明的方式留痕，并引用替代评论；禁止删除或编辑该无效评论，因为删除会销毁后续读者据以发现该违规的审计线索。
后续有效验收不能追溯验证已发生的合并；该合并必须登记为门禁违规发现。

已记录实例：

PR #273，exact Head `5e0a919a9253b8747c59062b87d0a580cd204e54`，其上 `GOV-DOC-001 structural checks` = failure（run `44491572672`，完成于 2026-11-19T08:54:26Z）。验收评论 `7005241529`（2026-11-19T09:33:25Z）记录 ACCEPT 与合并授权 YES，其六行对账表不含检查结论行。该 PR 于 2026-11-19T09:33:37Z 合并。跟踪 Issue：#134。

## 3. 评论与会话审计证据

每个产生实质工作的 AI 会话都必须在所属 Issue/PR 留下持久 GitHub 记录。至少记录：
- Session ID、Prompt ID、不可变提示词版本、提示词 SHA-256；可用时记录准确提示词源文件路径/Commit/Blob。
- 如果执行时没有采集提示词哈希，必须写明 `NOT RECORDED`；禁止根据转述或改写内容重建或猜测哈希。
- Work Item 和所属 Issue、相关 PR、责任 Owner 及会话角色。
- Repository、Branch、Base SHA、准确 Head SHA、变更路径和实际完成的工作。
- 重要发现及决策状态（PROPOSED / ACCEPTED / REJECTED / OPEN / BLOCKED）、决策权威和源证据链接。
- 准确命令/环境、已运行和未运行的检查、Run ID/URL、结论和被测 SHA。
- 审查者身份/状态、依赖、阻塞、风险、交接 Owner 和退出条件。
- 合并状态；若已合并，记录目标分支、真实 Merge SHA 和合并后验证。

评论本身是审计记录，不自动构成事实证明。每一项 PASS、合并、批准或 DECIDED 声明都必须链接源证据。保留失败检查和相互矛盾的历史记录；通过追加纠正记录修复，不得改写历史。Integration Owner 维护 Session → Work Item/Issue → PR → Commit → CI 证据追溯索引。每个会话作者仍对自己的结项记录负责。

## 4. CANDIDATE → DECIDED 证据标准

不得仅凭共识措辞、AI 结论、文档检查通过或 PR 合并，将 CANDIDATE 升级为 DECIDED。DECIDED 记录必须具备：
1. 明确的决策权威：具名责任 Owner、批准引用和日期；跨 Owner 决策必须包含所有受影响 Owner，或既定仲裁/ADR 权威。
2. 准确的实现/规范 Commit SHA 和变更路径。
3. 在准确候选 Head SHA 上执行并成功的 CI Run ID 和 URL；列出 Workflow/检查名称及结论。如 CI 不适用，说明原因并提供可复现的替代证据。
4. 必需的领域证据：按情况提供测试、独立审查、兼容性/安全/故障分析、基准或原型结果。
5. 范围、假设、非目标、已知限制，以及证据尚未证明的明确事项。
6. 同步的中英文决策记录，状态、标识和证据引用一致。
7. 同一 PR 中更新决策日志/ADR 或所属规范，并从所属 Issue 和 Work Item 索引建立链接。

任何强制项目缺失时，应保留 CANDIDATE、TO_VALIDATE、OPEN 或 BLOCKED 等适当状态。PR 合并是仓库集成证据，不会自动赋予决策权威。

## 5. GitHub 平台配置操作手册——需管理员人工执行

**当前已观察状态：** Issue #134 记录 `main protected=false` 且 required status checks 未强制。Rulesets 接口返回 HTTP 403，并提示套餐/可见性限制。因此，流程文字、PR 模板和 CI 变绿目前均不构成平台硬合并门禁。本补充规范不声称这些控制已经启用。

**人工操作——Repository Administrator / Owner（建议：仓库所有者 `oahcom`）：**
1. 在保持仓库机密性的前提下决定托管/套餐方案：将私有仓库所有者的 GitHub 套餐升级到支持私有仓库所需分支保护/Rulesets 的等级，或选择具备等效强制控制的其他私有托管配置。未经明确安全/隐私决策，不得仅为解锁功能而将私有仓库公开。
2. 在 GitHub 仓库 Settings → Branches（或支持时使用 Rules → Rulesets）创建规则，目标分支必须精确为 `main`。
3. 启用合并前必须通过 PR；至少要求一项审批；新提交后撤销过期审批；要求解决审查讨论；限制强制推送和分支删除；在平台支持时将管理员纳入规则并禁用绕过。如果无法禁用绕过，必须定义具名紧急操作人、原因、证据和事后审计。
4. 要求 GitHub 在 PR 上实际显示的准确检查上下文。至少对受治理文档要求 `GOV-DOC-001 structural checks`。实测于 2026-11-25：自 #1027 起该 Rust workflow 不再有 `pull_request.paths` 过滤，且 `rust-workspace-test` 已经是十六个必需上下文之一（分支保护读回于 2026-11-25，`strict: true`，`enforce_admins` 已启用），因此该检查已在每个指向 `main` 的 PR 上运行，无需聚合门禁。条件规则：若后续变更在上下文已属必需的 workflow 上重新引入 `paths` 过滤，该检查会在不匹配的 PR 上被跳过，必须在把该上下文设为必需之前增加始终运行的聚合门禁。不得猜测检查上下文名称；必须从真实 PR Head 附带的检查列表中选择。
5. 保存规则后，通过 GitHub UI/API 回读分支/Ruleset 配置。将规则 ID/名称、目标、启用设置、绕过主体和时间戳记录到 Issue #134。读取返回 403/权限拒绝时，状态是 UNKNOWN，不是已强制执行的证明。

**验证操作——Integration Owner（建议由独立于作者的集成负责人执行）：**
1. 创建一个小型测试 PR，在其准确 Head 上故意制造一项必需检查失败；确认 GitHub 阻止正常合并路径。
2. 确认精确 Head 检查通过且具有独立批准的 PR 可以进入可合并状态；再推送新提交，确认旧批准被撤销且检查重新运行。
3. 确认未解决的审查讨论会阻止合并；验证强推/删除限制及管理员绕过行为。
4. 将测试 PR URL、准确 Head SHA、失败/成功 Workflow Run ID、观察到的阻止/可合并状态、规则回读证据和验证者身份记录到 Issue #134。
5. 只有所有验收标准均有证据后才可关闭 Issue #134。仅有设置截图不够；必须提供 UI/API 回读和证明失败必需检查无法合并的负向测试。

**建议职责分配：**
- Repository Owner/Admin（`oahcom`）：套餐/可见性决策、分支/Ruleset 配置、绕过策略。
- Integration Owner：Workflow 检查上下文盘点、政策清单、精确 Head 证据、禁止合并负向测试和 Issue 结项。
- Workflow Maintainer：确保 Workflow 触发条件/检查上下文稳定。实测于 2026-11-25：该 Rust 检查无需聚合门禁，因为自 #1027 起不存在 `pull_request.paths` 过滤，且 `rust-workspace-test` 是十六个必需上下文之一（分支保护读回于 2026-11-25，`strict: true`，`enforce_admins` 已启用）。条件规则：若后续变更在上下文已属必需的 workflow 上重新引入 `paths` 过滤，该检查会在不匹配的 PR 上被跳过，必须在把该上下文设为必需之前增加始终运行的聚合门禁。
- Independent Reviewer / Security Owner：审查平台控制设计和紧急绕过/审计策略。
- 每个 AI 会话作者：提示词哈希、会话结项、准确 Commit 和 Run 证据。
以上为角色建议，不代表相关人员已经接受指派。

## 6. Issue #130 会话覆盖审计

Issue #130 已作为流程规范 ADOPTED，但仍因运营落地审计而保持 OPEN。Integration Owner 应：
1. 从 Work Items 索引和相关 PR/Issue 时间线中枚举所有进行中及已完成的实质性 AI 会话。
2. 将每个会话关联到一个所属 Work Item/Issue 及一个或多个现有 PR/Issue 载体；合并重复载体，不得为同一结果新建重复 PR。
3. 检查每份结项记录是否包含 Session/Prompt 身份、提示词 SHA-256、角色/Owner、Branch 和准确 Head、实际工作、决策状态/权威、含 NOT RUN 项的 CI 证据、审查者身份、阻塞和交接。
4. 执行时未采集的历史提示词哈希标记为 `NOT RECORDED`，不得伪造追溯哈希。为未来提示词建立执行时采集要求。
5. 在现有载体补充缺失的结项记录，尽可能双向关联相关会话，并更新 `14-ai-development/work-items/INDEX.md`。
6. 将覆盖状态报告为 audited/complete、audited/gaps 或 not yet audited。所有发现缺口均明确责任人和关闭条件之前，Issue #130 保持 OPEN。

## 7. 回退与紧急纠正策略

- 如果某次合并在必需检查失败/缺失时仍然通过，立即停止后续正常合并，记录准确 PR/Head/Merge SHA 和运行证据；在授权范围内禁用绕过路径，并创建/更新 P0 治理事件。不得改写失败运行或历史。
- 如果已合并变更不安全或存在实质错误，优先创建针对当前 main Head 的独立 revert PR。回退 PR 本身必须通过适用的精确 Head 检查和独立审查。不得强推或重置共享的 `main`。
- 如果回退不安全或无法恢复服务，使用范围严格限定的前向修复 PR，明确缓解措施、Owner、验证和到期/退出条件，并记录拒绝回退的原因。
- 如果 DECIDED 声明错误，通过追加纠正/取代记录，链接原决策、证据缺口、纠正后的状态和受影响的下游决策。不得静默降级或删除历史决策。
- 紧急绕过只能作为最后手段：必须记录授权操作人、事件/原因、准确 SHA、跳过的测试/检查、风险接受、时间窗口和强制事后独立审查。紧急绕过不会追溯性地把被跳过的检查变成 PASS。

## 8. 当前证据记录——PR #242

- PR #242 已合并，Merge Commit：`aa711289785395d2efa202e34def64c393ee0ac7`。
- 后续验证提交：`4a3e06fd263e9dbd1056179dceb3cb21b17e330f`。
- PR Rust Workflow：[Run 44259233587](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44259233587)，SUCCESS（PR 事件；Head `09ab26963293ee460237c6f27c5b95ed3b401730`）。
- PR 双语文档门禁：[Run 44259233358](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44259233358)，SUCCESS（PR 事件；相同 Head）。
- 后续 main Rust Workflow：[Run 44261208110](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44261208110)，SUCCESS；push 事件；准确 main Head `fcdecf0a4e638c8b3c9ac0e4623f97c98ed21291`；Job `rust-workspace-test`；命令 `cargo test --workspace --all-targets`。
- main 运行验证的是包含 PR #242 的后续 main 快照，与上面 PR 触发的精确 Head 检查是不同证据。

## 9. 采用边界

本补充规范在审查并合并前保持 PROPOSED。既有 PR-GOVERNANCE-001 流程规范仍为 ADOPTED。两份文档均不声称 Issue #134 的平台强制执行已经完成。Issue #130 和 #134 在各自运营验收标准完成前均保持 OPEN。
