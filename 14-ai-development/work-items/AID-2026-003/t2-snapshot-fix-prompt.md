# T2 snapshot — remediation round-1 dispatch prompt (verbatim sent payload)

**Archival status: ESTABLISHED — byte-verbatim snapshot of the wire text actually dispatched.**

## Provenance

- **Object (snapshot target):** the *sent payload* of the remediation round-1 dispatch — the exact text transmitted as the first user message by `dispatch_pr256.py` (role `fix`) at 2026-11-18 20:52:09 +08:00 (dispatch log `send-pr256-log.md`: `dispatch fix (修复会话提示词-PR256.md, 9807 chars, new conversation)`) to conversation `6afd9f7f-d544-83ee-98d1-92d7aafb3bcf`.
- **Verbatim body metrics** (coordinator-computed on the exact sent bytes with Python hashlib; cross-checked against the dispatch log char count):
  - characters: 9807
  - UTF-8 bytes: 16735
  - line endings: LF only (158 LF)
  - SHA-256: `bbe275373926603732f0a5ad96d7a7d88f30578cd947327ddc8263148cf797b7`
- **Raw-byte cross-check file:** `t2-snapshot-fix-prompt.source.txt` (this commit) — pure verbatim body, byte-identical to the coordinator wire export of the sent payload.
- **Extraction rule:** the verbatim body of this file is everything after the separator line consisting solely of `---` that follows the "Superseded status note" section below; the body must equal `t2-snapshot-fix-prompt.source.txt` byte-for-byte.
- **Companion authored source:** `t2-snapshot-fix-prompt.authored-prompt.md` (this commit) — the full authored task-book file `修复会话提示词-PR256.md` as maintained in the coordinator workspace (9914 characters / 16916 bytes / SHA-256 `986d52c5c10e17638a96f25482aa2727f0db29aa00e3c27cac9f8ad01996b083`).
- **Known quirk (disclosed; quirks preserved verbatim, not cleaned):** the dispatcher extracted the payload from the *first* textual occurrence of the marker `会话任务：`, which appears inside the usage note (`把从「会话任务：」到文件末尾…`) near the top of the authored file, not at the substantive task header. Consequently the sent text begins mid-sentence with `会话任务：」到文件末尾的整块作为第一条消息发送。…`; the substantive `会话任务：` header and management block follow a few lines later and are complete. The executing session received exactly this text; the snapshot preserves it as-is.
- **Digest provenance:** the SHA-256 / byte / character figures above are **coordinator-computed**, not self-computed by a ChatGPT session. Any session recording them without independent recomputation must label the source `coordinator-supplied` and must not claim a self-measurement.
- **Establishing commit:** this commit (coordinator-executed byte archival; byte-fidelity required exact-byte file I/O). NF-2 registration closeout (manifest / INDEX / PR #256 evidence comment) is executed by the follow-up ChatGPT session and recorded in those places.

## Superseded status note (history preserved)

This file previously held a placeholder written by the remediation round-2 session (commit `24738058a23a2b85b6b66740262aa27fa9ca0afa`), which read in part:

> **Archival status: NOT_VERIFIED — verbatim full snapshot not yet established.**
> **Required completion input:** provide the original `修复会话提示词-PR256.md` as an accessible file or coordinator-exported verbatim snapshot.

That session deliberately refused to commit a reconstruction as if it were the full immutable snapshot. The limitation is resolved by this commit. The placeholder text remains retrievable from git history of this path; it is not erased.

---
会话任务：」到文件末尾的整块作为第一条消息发送。若 GitHub 连接可写，可直接在分支提交修订并发布评论；否则输出文本由操控层落盘与发布。

---

会话任务：

【管理头 · 不可删改】

1. **LOADED 声明**：开工第一行输出 `LOADED: AI-EXEC-001 v1.0 + AI-EXEC-002 v1.0`（先读仓库 `14-ai-development/AI-EXEC-001.md`、`AI-EXEC-002.md` 现行 ADOPTED 版；只读了部分则声明 `LOADED-PARTIAL` 并列出已读章节）。未声明 = 未接入规范，产出须标注 `RULES-NOT-LOADED` 并记一条 finding。

2. **配额预检**：新建 PR/Issue 前先查仓库 open PR 数。**open PR ≥ 10 时禁止新建任何 PR/Issue**，只允许三种动作：①在既有 PR/Issue 上补提交、补评论；②合并/关闭你名下已开的载体；③把工作并入已有 PR 分支（同类项归并）。当前为冻结期（2026-11-18 19:45 起，起点 open=12；派发时刻实测 open=12）——本次任务全部动作落在既有 PR #256 分支与既有 Issue #218 评论内，**禁止新开任何 PR/Issue**。

3. **登记义务**：实质工作建 `AID-YYYY-NNN` + `manifest.yaml` + INDEX 行。提示词出处如实记档：仓库文件记版本 + SHA-256；聊天指令记会话 ID + 指令来源（替代文件哈希）。禁止留空 `NOT RECORDED` 充数，禁止事后补造。本次工作归并入既有 **AID-2026-003**（同类项归并，不开新 AID），其 manifest/INDEX 的更新内容由你在 Closeout 阶段给出。

4. **finding 三要素**：每个发现记 `ID + 严重级(BLOCKER/P0–P3) + 回流去向(Issue #N / RW-YYYYMMDD / Closeout k)`，写入既有 Issue/PR 评论，**不开新 Issue**。

---

（以上管理头结束，以下为任务正文）

## 0. 会话准备 — 自己设计提示词

按仓库 `14-ai-development/AI-EXEC-002.md` §3 的 12 项结构（Identity / Objective / Baseline / Authority / Scope / State of knowledge / Required steps / Acceptance criteria / Verification / Git workflow / Stop-escalation / Evidence）**自行生成你的工作提示词**并在会话开头完整输出（可将本任务书作为输入细化）。随后按你自拟的提示词执行；本任务书的 Baseline、红线、输出契约**优先于**自拟稿，冲突时以本任务书为准并在自拟稿中标注。

## 执行通道与红线

- 仅用 ChatGPT 对话 + 项目 GitHub 连接读写仓库（CHATGPT-GLOBAL-001：禁 API Key / Codex / 第三方模型 / 本地中转；GitHub 工件是持久事实来源）。
- **能力自声明（第一步）**：开工先声明你的工具能力（GitHub 连接有无 / 代码执行有无 / 文件读写有无）。**无代码执行或哈希计算能力时，一切哈希类检查必须记 `NOT_VERIFIED` 并写明能力限制**——严禁把任务书或仓库里的期望哈希抄回来冒充"重算结果"（AI-PROMPT-STD-001 §5 允许的诚实出口）。
- 你不做验收：exact-Head 复验由另一个 owner 会话执行（PR-GOVERNANCE-001 五态处置）；你只做 REMEDIATE 修复、留证据、交出新 Head。
- PR-GOVERNANCE-001 §5 红线：COMMENT ≠ APPROVE；禁止补造 NOT RECORDED；NOT RUN ≠ PASS；例外必须显式记录。
- 版本不可变（AI-EXEC-002 §2）：已执行提示词版本不可变、不可改写历史。凡涉及 `prompt-v1.md` 的修复（F-2/F-3/F-4），自行选择合规处置方式（如不改动已执行正文、另附勘误/派生记录，或按你依据规范得出的其他合规路径）并写明理由与规范依据。

## Identity

- Role: REMEDIATE 修复执行会话（Implementer；用户派发，执行 Integration Owner 的修复交付）
- Work Item: AID-2026-003 · PR #256（Draft，Owner 处置 = REMEDIATE）· Tracking Issue #218
- 你不是审查者、不是 Owner 验收者；你是**修复执行者**。

## Objective

按 Owner 五态处置决议（REMEDIATE）修复独立审查确认的七项 findings，产出可复核的关闭证据与新 Head，供 owner 会话 exact-Head 重新验收。

## Baseline（冻结输入；开工先核对，与 GitHub 实际不符 → 停止并要求刷新任务书）

- 仓库：oahcom/AiMemoryBrainArchitecture
- PR：https://github.com/oahcom/AiMemoryBrainArchitecture/pull/256（Draft）
- 分支：`ai/AID-2026-003/IO-exec-v11`；基线 Head：`ef3aa3e96271ccffe1482931069f30dfa9b1eb2a`；Base：`6b5db2918cffc2281deb22fd9858a37dbaeec726`（注意：manifest.yaml:18 与 prompt-v1.md:19 目前只记了缩写 `6b5db291`——这本身就是 F-3 要修的内容）
- 修复对象（PR 五文件 + F-4 可能涉及的登记文件）：`14-ai-development/AI-EXEC-001.md`、`14-ai-development/AI-EXEC-002.md`、`14-ai-development/work-items/AID-2026-003/manifest.yaml`、`14-ai-development/work-items/AID-2026-003/prompt-v1.md`、`14-ai-development/work-items/INDEX.md`、`docs/translation-status.md`（若 F-4 关闭需要）
- 上位文档只读不改：`ai-development-standard.md`、`iteration-lifecycle.md`、`PR-GOVERNANCE-001.md`、`prompt-authoring-standard.md`、GOV-DOC-001（`00-governance/bilingual-documentation-policy.md`）。

## Authority

- 可以：修改上述修复对象文件、在 PR #256 分支补提交、在 PR #256 / Issue #218 补评论（关闭证据）、更新 AID-2026-003 的 manifest/INDEX 登记内容。
- 不可以：新建 PR/Issue（配额冻结期）；改动上位文档；合并 PR；出具验收结论（那是 owner 复验会话的事）；补造任何证据。

## Scope / Non-goals

- 范围：七项 findings 的条款级修复 + 关闭证据 + 新 Head（修复顺序见下）。
- Non-goals：验收与合并；裁定三处上位冲突（15v12、TESTEDvVERIFIED、SHA-256 逃生门——留 Issue #218）；AI-EXEC-ROLLOUT-001 映射；英译全译。

## State of knowledge

- DECIDED：v1.0 ADOPTED 继续有效；PR #256 五态处置 = REMEDIATE（Owner 会话，PR comment #6977767413）；修复顺序 = ①F-1 → ②F-5/F-6/F-7 → ③F-2/F-3/F-4 → ④关闭证据 → ⑤新 Head（Owner 原文见下）。
- CANDIDATE：你的修复文本与处置方式。
- OPEN：AI-EXEC-002 §2"已执行提示词版本不可变"与 F-2/F-3/F-4 修复 `prompt-v1.md` 之间的张力——如何合规修，由你依规范裁定并记录理由；prompt_file_commit_sha 需两步回填的先例（AID-2026-002：内容提交 53aae842，commit 612c4b2d 补记）。
- TO_VALIDATE：PR 现 Head 与基线一致性；七项关闭条件达成情况（你自证，owner 会话复核）。

## Required steps

1. 输出 LOADED 行 + 能力自声明 + 自拟工作提示词（§0）。
2. 从 GitHub 读取 Baseline 各文件现文，核对 Head 与文件状态。
3. 按 Owner 顺序修复（每步对照关闭条件自查后再进下一步）：
   - **① 先修 F-1（BLOCKER）**：彻底封闭 R3 专家审查豁免路径——这是重新验收的首要条件；
   - **② 修 F-5、F-6、F-7**：解决规则自身的适用范围与门禁漏洞；
   - **③ 修 F-2、F-3、F-4**：补齐提示词、provenance 和双语登记。
4. **④ 更新 PR #256 与 Issue #218 的 finding 关闭证据**（每 finding 一条：ID + 严重级 + 关闭证据 file:line + 回流去向；有 GitHub 评论权限则发布并记录 comment ID，无权限则输出评论文本交操控层发布）。
5. **⑤ 产出新 Head**：把修订落到分支 `ai/AID-2026-003/IO-exec-v11`（有推送能力则直接提交推送并报告 commit SHA 列表与最终 Head；无推送能力则输出每个改动文件的**完整修订后内容**与目标 manifest/INDEX 状态，由操控层落盘提交）。若涉及 prompt_file_commit_sha 回填，按两步提交：先内容提交，再把引入提交 SHA 记入 manifest/INDEX。
6. 输出 Closeout（AI-EXEC-002 §6 九项）+ INDEX 行文本。**不做验收**。

## Findings 事实转达（独立审查会话输出原文引用；严重级以 Owner 处置表为准，括注审查初判）

- F-1 [P1→Owner 升为 BLOCKER] R3 获取桥存在专家审查绕过路径。证据：AI-EXEC-001.md:82-96 允许专家不可用时进入例外，并明确提供“例外降级合并”；但 ai-development-standard.md:92、:53-70（§3.2）要求 R3 在验收前完成独立安全/领域专家审查及可复现测试，AI-EXEC-002.md:90 也重申该要求；PR-GOVERNANCE-001.md:74-87 要求独立审查且 MERGE 必须具备必需审批。当前条款没有明确禁止用时效例外代替 R3 专家审查。— owner Integration Owner — 关闭条件：明文规定 R3 专家审查与可复现测试不可豁免；24h/3 工作日仅用于升级、HOLD、REMEDIATE/REJECT，不得据此降级合并或验收 — 回流 Issue #218。

- F-2 [P2] AID-2026-003 的归档提示词没有满足 12 项结构中的 State of knowledge。证据：prompt-v1.md:5-72 有 Identity、Objective、Baseline、Authority、Scope、Non-goals、Required steps、Acceptance、Verification、Git workflow、Stop、Evidence，但没有 DECIDED/CANDIDATE/OPEN/TO_VALIDATE 状态分列；AI-EXEC-002.md:52-63 与 prompt-authoring-standard.md §4 明确要求该项。PR 声明 12 项结构归档与实际文件不符。— owner Integration Owner — 关闭条件：补充四种知识状态及其事实条目，并复核完整 12 项结构 — 回流 Issue #218。

- F-3 [P2→Owner 升为 P1] T1 provenance 与 Baseline 的完整 SHA 登记未闭合。证据：manifest.yaml:18 和 prompt-v1.md:19 仅记录缩写 base SHA `6b5db291`，未记录完整 `6b5db2918cffc2281deb22fd9858a37dbaeec726`；manifest.yaml:45 的 prompt_file_commit_sha 仍为 PENDING。GitHub PR commits API 已显示引入 prompt-v1.md 的提交为 `bb1ac7a59619e56769ac1e69c272a772f8c96b02`。AI-EXEC-002.md:40 要求 T1 的 Prompt ID + 版本 + 文件 commit SHA 三元组；AI-PROMPT-STD-001 §3 Step 2 / §4 Baseline 要求精确 SHA。— owner Integration Owner — 关闭条件：将完整 base SHA 与实际引入提交 SHA 写入 manifest、prompt/INDEX 对应记录并回读核对 — 回流 PR #256 Closeout + Issue #218。

- F-4 [P1→Owner 降为 P2] v1.1 的双语例外与任务提示词未满足 GOV-DOC-001 的明示条件。证据：prompt-v1.md:28-55 的 Scope/Acceptance 未纳入双语工作及验收；GOV-DOC-001 §2.1（bilingual-documentation-policy.md:58）要求每个 AI 会话将双语工作写入 prompt/scope/acceptance。GOV-DOC-001 §5（:114-123）要求同一 PR 记录临时权威版本、待补路径、精确源版本、Owner、期限和跟踪载体；docs/translation-status.md:79-80 的既有例外仍标记 AID-2026-002，PR #256 又未修改该登记文件，不能仅凭旧例外自动证明其覆盖 v1.1 新源版本。— owner Integration Owner — 关闭条件：在本 PR/登记中明确确认例外覆盖 v1.1 的准确源版本及英文对应路径、权威版本、Owner、期限、跟踪载体；补齐任务提示词中的双语验收要求 — 回流 Issue #218。

- F-5 [P2] 代码会话七项最小集与十二项强制结构的适用关系不清且可能冲突。证据：AI-EXEC-002.md:52-63 规定每份提示词必须包含 12 项；:69 将 IMPL/TEST/SEC/MIG/PERF 的最小集定义为七项，并只明确 R2/R3 代码会话仍走完整 12 项。AI-PROMPT-STD-001 §4 对每份执行提示词规定 12 项 MUST，未提供 R0/R1 代码会话七项豁免。已披露的 15/12 冲突没有解决这一新增 7/12 适用冲突。— owner Integration Owner — 关闭条件：明确七项仅是额外重点子集（其余七项仍需保留），或取得上位规范对 R0/R1 代码会话的明确豁免决议；不得留有两种解释 — 回流 Issue #218。

- F-6 [P2] Grandfather 将“未记录载入”直接分类为 RULES-NOT-LOADED，可能制造历史误报。证据：AI-EXEC-002.md:46 将 v1.1 生效前登记缺失映射为 RULES-NOT-LOADED；AI-EXEC-001.md:24 又规定未声明载入即视为未接入。缺少 LOADED 记录不能证明实际未载入，与“不倒签、不补造、不追罚”的 grandfather 原则不一致。— owner Integration Owner — 关闭条件：区分有证据证明未载入与仅缺少载入记录（例如 RULES-LOAD-NOT-RECORDED）；历史会话只登记证据缺口，不反向认定违规 — 回流 Issue #218。

- F-7 [P2] PARALLEL 挂接关系没有明确的合并前裁定门禁。证据：AI-EXEC-001.md:126-127 允许声明 PARALLEL，并将裁定交给日度治理窗口，但没有规定裁定前必须 HOLD 或禁止 MERGE，也未明确谁批准 PARALLEL 的边界。可能出现治理 PR 先合并、双轨风险后裁定。— owner Integration Owner — 关闭条件：明确所有治理文档 PR 必须在 MERGE 前完成挂接裁定；未裁定时 HOLD；PARALLEL 需记录批准者、边界、理由和复核期限 — 回流 Issue #218。

## Owner 处置事实转达（Owner 会话输出原文引用）

> **最终处置：REMEDIATE。不得合并。决定依据：F-1 [BLOCKER] + F-2 至 F-7。** 不是拒绝整个方案，而是要求修订现有 PR，消除已经确认的语义和治理缺陷。
>
> 建议 Integration Owner 按以下顺序修订：
> 1. **先修 F-1**：彻底封闭 R3 专家审查豁免路径。这是重新验收的首要条件。
> 2. 修复 F-5、F-6、F-7：解决规则自身的适用范围与门禁漏洞。
> 3. 修复 F-2、F-3、F-4：补齐提示词、provenance 和双语登记。
> 4. 更新 PR 和 Issue #218 的 finding 关闭证据。
> 5. 生成新的 Head 后，重新进行 exact-Head 验收。
>
> （Owner 原文另注：PR #256 = REMEDIATE；AI-EXEC-001/002 v1.1 = PROPOSED；v1.0 已采纳版本继续有效；未执行合并、未发布 Issue #218 的 v1.1 采纳评论、未回填 merge SHA、未将文档头改成 ADOPTED、不生成虚假 closeout 完成记录。）

## Acceptance criteria（对你的修复）

1. 七项 findings 各自的关闭条件全部达成，且每项有 file:line 级修复证据；
2. 修复文本与上位文档零冲突；上位文档零改动；
3. finding 关闭证据评论按三要素写明并落在既有 PR #256 / Issue #218（不开新载体）；
4. manifest/INDEX 出处记录补齐（F-3：完整 base SHA + 实际引入提交 SHA 回读核对；prompt 哈希按实际字节重算或诚实 NOT_VERIFIED）；
5. 输出含 Closeout 九项 + INDEX 行 + 新 Head（或待落盘文件清单）。

## Verification（逐项记 `RUN/PASS | RUN/FAIL | NOT VERIFIED | NOT RUN`）

- 逐 finding 关闭条件对照（引用修复后 file:line）；
- 交叉引用一致性抽查（LOADED / T1-T3 / finding 三要素 / 回流术语在两文件口径一致）；
- 上位零改动（diff 范围检查）；
- 哈希类：有能力则对实际提交字节重算（UTF-8 不归一化）；无能力记 NOT_VERIFIED（禁止抄期望值）；
- 测试套件 NOT RUN（纯文档变更）——如实记录，不得混同 PASS。

## Git workflow

- 只在分支 `ai/AID-2026-003/IO-exec-v11` 上补提交；不开新 PR/Issue；不自行合并。
- prompt_file_commit_sha 两步回填：先内容提交，再把引入提交 SHA 记入 manifest/INDEX（先例：AID-2026-002，commit 612c4b2d 补记引入提交 53aae842）。
- 推送后报告最终 Head SHA 供 exact-Head 复验。

## Stop / escalation

- 开工核对基线 Head ≠ `ef3aa3e9…` → **停止**，要求刷新任务书（exact-Head 门禁）；
- 修复中发现与上位文档实质冲突 → 停止写入该处，按 finding 三要素记 Issue #218；
- 无法访问 GitHub 或无写权限 → 输出全部文件内容与评论文本交操控层执行；
- 单 finding 关闭条件无法达成 → 保留 OPEN 并写明阻塞原因与退出条件，**不得谎报关闭**。

## Evidence — 输出格式

```
### [REMEDIATE] PR #256 / AID-2026-003（session-executed, implementer）
LOADED: AI-EXEC-001 v__ + AI-EXEC-002 v__
Capability: <GitHub 连接/代码执行/文件读写 有无——据此解释 NOT_VERIFIED 项>
Working prompt: <你的 12 项自拟提示词>

Fixes:
- F-1 [<严重级>] 关闭证据: <file:line + 修改后条款摘录> — 关闭条件对照 __ — 状态 CLOSED|OPEN — 回流 __ (Issue #N / RW-YYYYMMDD / Closeout k)
- F-2 ... F-7 ...

Deliverables:
- commits: <sha 列表 + 最终 Head> 或 <待落盘文件清单：路径 → 完整修订后内容>
- PR #256 关闭证据评论: <comment ID 或评论文本>
- Issue #218 关闭证据评论: <comment ID 或评论文本>

Closeout（AI-EXEC-002 §6 九项）: ...
INDEX 行: ...
Verification: <逐项 RUN/PASS | RUN/FAIL | NOT VERIFIED | NOT RUN>
Disclosure: 本会话为修复执行会话（implementer），非独立审查、非 Owner 验收；exact-Head 复验与五态处置由 owner 会话执行，合并由 GitHub 账号 oahcom 执行。
```