# AI-EXEC-UNIFICATION-RULING-001
# Owner Ruling on Three Inter-Standard Conflicts / 三处上位规范冲突的 Owner 统一裁定

- **Document ID:** AI-EXEC-UNIFICATION-RULING-001
- **Version:** 1.0
- **Status:** ADOPTED — binding Owner policy ruling
- **Ruling authority:** Project Owner, exercising the owner-directed authority expressly delegated for Issue #218
- **Ruling date:** 2026-11-18
- **Tracking:** Issue #218 · AID-2026-003 · AID-2026-002
- **Implementation:** This ruling and the corresponding execution-rule amendments land together on `main`; the effective commit is recorded in the AID-2026-003 manifest, INDEX and Issue #218 closeout.
- **Language authority:** The English and Chinese texts below are equally authoritative. Neither is a summary or translation-only aid.

## 1. Authority, scope and inter-document relationship / 权限、范围与文档关系

### English

This is a binding owner-directed policy ruling resolving exactly three inter-standard conflicts previously deferred by Issue #218 comment #6971736655. It applies to the interpretation and execution of the identified provisions in AI-STD-001 §5 and §10, AI-PROMPT-STD-001 §4 and §5, and CHATGPT-GLOBAL-001 session-flow item 7.

**Relationship: SUPERSEDE (narrow and explicit).** Under AI-EXEC-001 v1.1 §10, this ruling supersedes the prior deferred-conflict wording and interim execution interpretations in AI-EXEC-001/002, and supersedes the conflicting operational readings of the enumerated upstream clauses only to the extent necessary to implement RULING-01 through RULING-03. The corresponding AI-EXEC-001/002 text is rewritten in this same change set. The source standards' unrelated clauses and literal historical text are not edited. For these three subjects, apply this ruling as the Owner's controlling interpretation; all other upstream requirements remain in force.

This ruling does not create a new PR or Issue, does not amend the broad body of any upstream standard, and does not retroactively invalidate completed and accepted work. Where a historical record honestly states NOT_VERIFIED, TESTED, or a 12-item prompt structure, preserve that historical fact; apply the new mapping prospectively.

### 中文

本文件是具有约束力的 Owner 定向政策裁定，专门解决此前由 Issue #218 评论 #6971736655 延期保留的三处上位规范冲突。适用范围严格限定为 AI-STD-001 §5、§10，AI-PROMPT-STD-001 §4、§5，以及 CHATGPT-GLOBAL-001 会话流程第 7 条的解释和执行。

**文档关系：SUPERSEDE（范围狭窄且明确）。** 依照 AI-EXEC-001 v1.1 §10，本裁定取代 AI-EXEC-001/002 中此前的冲突延期文字和临时执行解释，并仅在落实 RULING-01 至 RULING-03 所必需的范围内，取代所列上位条款之间相互冲突的执行解释。本次变更集同步回改 AI-EXEC-001/002 对应文字。上位规范的其他条款及其历史原文不作修改。涉及这三个主题时，以本裁定作为 Owner 的控制性解释；其他上位要求继续有效。

本裁定不创建新 PR 或 Issue，不大范围修改任何上位规范正文，也不追溯否定已经完成并验收的工作。历史记录中如实写明的 NOT_VERIFIED、TESTED 或 12 项提示词结构必须保留为历史事实；新映射向前适用。

## 2. RULING-01 — Mandatory prompt structure: unify to 15 / 裁定一——提示词强制结构统一为 15 项

### English

**Ruling — UNIFY-TO-15.** AI-STD-001 §5's 15-item list is the sole complete mandatory structure for every substantive execution prompt. AI-PROMPT-STD-001 §4's 12 items remain fully mandatory as the core items 1–12. AI-STD-001's items 13, 14 and 15 are separately represented as mandatory supplemental sections: (13) commit, read-back, branch-head and evidence requirements; (14) stop conditions and escalation for ambiguity/conflicting contracts; and (15) the bilingual documentation manifest. All 15 must be present; the 12-item structure is not an alternative or a waiver.

The six-item R0/R1 documentation focus subset and seven-item code-session focus subset in AI-EXEC-002 are emphasis/checking aids only. They never remove any of the 15 required sections. Applicable scheduled-prompt additions remain additional requirements.

**Reason.** The 15-item upper-standard list includes explicit bilingual semantic-parity and evidence/branch-readback controls. The 12-item prompt-authoring structure is a useful core skeleton, but treating it as exhaustive silently drops mandatory upper-standard controls. The adopted v1.1 execution rules already treat the six/seven-item subsets as focus subsets; making the 15-item structure canonical resolves the ambiguity without rewriting the upper-standard documents.

**Boundary.** Applies to prompts newly drafted or materially revised after this ruling takes effect. It does not retrospectively classify already completed and accepted prompts as non-compliant. Existing executed prompt bytes remain immutable.

**Review deadline.** 2026-12-02.

### 中文

**裁定——UNIFY-TO-15。** AI-STD-001 §5 的 15 项清单是所有实质执行提示词唯一完整的强制结构。AI-PROMPT-STD-001 §4 的 12 项全部保留为第 1–12 项核心内容。AI-STD-001 的第 13、14、15 项必须分别作为强制补充章节列出：（13）提交、回读、分支 Head 和证据要求；（14）歧义及契约冲突的停止条件和升级路径；（15）双语文档清单。15 项必须全部存在；12 项结构不是另一种可选模板，也不构成豁免。

AI-EXEC-002 中 R0/R1 文档会话的六项重点子集和代码会话的七项重点子集，仅用于强调和检查，不得删除任何 15 项必需章节。适用的定时提示词附加要求继续叠加执行。

**理由。** 上位规范 15 项清单明确包含双语语义对等、证据和分支回读控制。12 项提示词结构适合作为核心骨架，但将其视为完整清单会悄然遗漏上位规范的强制控制。已采纳的 v1.1 执行细则本来就将六项/七项集合定义为重点子集；将 15 项确定为唯一主结构即可消除歧义，无需重写上位规范。

**边界。** 适用于本裁定生效后新起草或实质修订的提示词。不追溯将已经完成并验收的历史提示词判定为不合规。已执行提示词字节保持不可变。

**复核期限。** 2026-12-02。

## 3. RULING-02 — Verification vocabulary: unify to VERIFIED / 裁定二——验证状态词表统一为 VERIFIED

### English

**Ruling — UNIFY-TO-VERIFIED.** The eight-state vocabulary in CHATGPT-GLOBAL-001 session-flow item 7 is the sole canonical session/work-item lifecycle vocabulary: `PROPOSED / IMPLEMENTED / VERIFIED / REVIEWED / ACCEPTED / MERGED / BLOCKED / NOT RUN`. `VERIFIED` is the only lifecycle state for the verification stage. `TESTED` is not a lifecycle state; it may appear only as descriptive wording for test evidence that was executed.

Mapping: a historical `TESTED` entry means checks were executed, not that the verification gate necessarily passed. It maps to `VERIFIED` only when all applicable verification requirements have evidence tied to the exact relevant commit and the required outcome is satisfied. Otherwise retain the historical `TESTED` wording as evidence metadata and report the actual lifecycle state. `NOT RUN` remains explicit and can never be treated as PASS or VERIFIED.

**Reason.** The eight-state session contract distinguishes implementation, verification, review, acceptance and merge, and preserves the non-execution state `NOT RUN`. Treating `TESTED` as a parallel lifecycle state would create two names for one stage and lose the explicit non-run state. The execution rules already use VERIFIED in their Stage 5 table and session workflow; this ruling aligns the vocabulary.

**Boundary.** Applies to new status reporting and new lifecycle transitions after the effective date. Existing records are not rewritten; historical TESTED is interpreted using the mapping above. Test-result labels such as PASS/FAIL/NOT RUN remain evidence outcomes, not lifecycle states.

**Review deadline.** 2026-12-02.

### 中文

**裁定——UNIFY-TO-VERIFIED。** CHATGPT-GLOBAL-001 会话流程第 7 条的八态词表是唯一规范化的会话/工作项生命周期词表：`PROPOSED / IMPLEMENTED / VERIFIED / REVIEWED / ACCEPTED / MERGED / BLOCKED / NOT RUN`。验证阶段唯一生命周期状态为 `VERIFIED`。`TESTED` 不再是生命周期状态，只能作为已执行测试证据的描述文字。

映射规则：历史 `TESTED` 表示曾执行检查，不代表验证门禁必然通过。只有所有适用验证要求均有绑定准确提交的证据且满足要求结果时，才可映射为 `VERIFIED`。否则保留历史 `TESTED` 作为证据元数据，并报告实际生命周期状态。`NOT RUN` 必须明确保留，永远不得视为 PASS 或 VERIFIED。

**理由。** 八态会话契约区分实现、验证、审查、验收和合并，并保留明确的未执行状态 `NOT RUN`。将 `TESTED` 作为并行生命周期状态会为同一阶段制造两个名称，并丢失未运行状态。执行细则的 Stage 5 表和会话流程已经使用 VERIFIED；本裁定使词表统一。

**边界。** 适用于生效日期之后的新状态报告和生命周期转换。不重写历史记录；历史 TESTED 按上述映射解释。PASS/FAIL/NOT RUN 等测试结果标签仍属于证据结果，不属于生命周期状态。

**复核期限。** 2026-12-02。

## 4. RULING-03 — Prompt SHA-256: mandatory; NOT_VERIFIED is not a waiver / 裁定三——提示词 SHA-256 必录；NOT_VERIFIED 不构成豁免

### English

**Ruling — UNIFY-TO-MANDATORY-SHA256.** SHA-256 of the exact prompt bytes is mandatory provenance evidence. `NOT_VERIFIED` is permitted only as an honest evidence status when the digest could not be computed or independently checked; it is not a substitute for the required digest, an integrity assertion, or a waiver of the readiness gate.

- **T1 (repository file):** calculate SHA-256 over the exact committed prompt bytes (UTF-8; no newline, whitespace, Unicode or line-ending normalization) and record path, byte length, digest, blob SHA, introducing commit SHA and execution reference.
- **T2 (chat instruction):** archive the complete executed instruction snapshot as immutable UTF-8 bytes and calculate its SHA-256; record the conversation/session source anchor and timestamp/permalink when exposed by the platform. Do not invent unavailable identifiers.
- **T3 (mixed):** record the T1 file provenance and the complete T2 supplement snapshot/digest separately; both are required.
- If the digest cannot be computed or verified, record `NOT_VERIFIED`, state the precise capability/source limitation, and do not claim prompt integrity. The prompt MUST NOT enter `PROMPT_READY` or `READY` until the required digest and provenance are verified. An unavailable tool is a blocker to evidence completion, not an exception from the rule.

**Reason.** AI-STD-001 §5 requires the exact executed prompt and its SHA-256 in the Work Item evidence bundle. AI-PROMPT-STD-001 §5's NOT_VERIFIED provision correctly prevents fabricated integrity claims; it does not cancel the mandatory evidence requirement. A truthful failure state and a waiver are categorically different.

**Boundary.** Applies to prompts and execution starts after this ruling takes effect. It does not rewrite historical manifests or retroactively fail accepted work. Existing NOT_VERIFIED values remain unchanged unless the original exact bytes are independently available and a new verified digest is produced; no digest may be reconstructed or guessed.

**Review deadline.** 2026-12-02.

### 中文

**裁定——UNIFY-TO-MANDATORY-SHA256。** 对准确提示词字节计算的 SHA-256 是强制出处证据。只有在无法计算或独立核验摘要时，才允许将 `NOT_VERIFIED` 作为诚实的证据状态；它不是必需摘要的替代品，不是完整性声明，也不是就绪门禁的豁免。

- **T1（仓库文件）：** 对准确提交的提示词字节计算 SHA-256（UTF-8；不做换行、空白、Unicode 或行尾归一化），记录路径、字节数、摘要、Blob SHA、引入提交 SHA 和执行引用。
- **T2（会话指令）：** 将实际执行的完整指令快照归档为不可变 UTF-8 字节并计算 SHA-256；平台提供时记录会话来源锚点、时间戳/永久链接。不得编造不可获得的标识。
- **T3（混合）：** 分别记录 T1 文件出处和完整 T2 增补快照/摘要；两部分均为必需。
- 如果无法计算或核验摘要，记录 `NOT_VERIFIED`，说明具体能力/来源限制，不得声称提示词完整性已验证。在必需摘要及出处完成核验之前，提示词不得进入 `PROMPT_READY` 或 `READY`。工具不可用意味着证据未完成的阻塞，不是规则例外。

**理由。** AI-STD-001 §5 要求将准确执行提示词及其 SHA-256 纳入 Work Item 证据包。AI-PROMPT-STD-001 §5 的 NOT_VERIFIED 规定正确地防止虚构完整性声明，但不取消强制证据要求。诚实报告失败状态与豁免规则是截然不同的两件事。

**边界。** 适用于本裁定生效后的提示词及执行启动。不重写历史 manifest，也不追溯判定已验收工作失败。既有 NOT_VERIFIED 值保持不变，除非原始准确字节可被独立取得并重新计算出经核验摘要；不得重建或猜测摘要。

**复核期限。** 2026-12-02。

## 5. Effective date, review and provenance / 生效日期、复核与出处

### English

This ruling is effective when the ruling file and the matching AI-EXEC-001/002 amendments are committed to the repository's `main` branch. The exact landing commit is recorded in AID-2026-003's manifest and session-level INDEX row, and in the Owner's Issue #218 ruling comment.

The ruling is reviewed on **2026-12-02**, together with the existing time-bounded bilingual STALE exception. Review may confirm, amend or replace the ruling; until a later written Owner decision is recorded, this ruling remains in force.

Source instruction: the Owner's user-provided dispatch in this ChatGPT conversation. This interface does not expose a stable conversation ID/permalink or the raw message byte stream for independent hashing. No synthetic ID or digest is created; those unavailable provenance fields remain explicitly NOT_VERIFIED.

### 中文

本裁定在裁定文件及对应 AI-EXEC-001/002 修订提交至仓库 `main` 分支时生效。准确落地主提交记录在 AID-2026-003 manifest、会话级 INDEX 行及 Owner 在 Issue #218 发布的裁定评论中。

本裁定于 **2026-12-02** 复核，与现有有期限双语 STALE 例外同窗。复核可以确认、修订或替代本裁定；在后续书面 Owner 决议记录之前，本裁定持续有效。

指令出处：本 ChatGPT 会话中用户提供的 Owner 定向任务指令。当前接口不暴露稳定会话 ID/永久链接，也不提供可供独立哈希的原始消息字节流。不创建虚构标识或摘要；不可获得的出处字段明确标记为 NOT_VERIFIED。
