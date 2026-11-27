---
document_metadata:
  steward: "user-authorized operator (delegated by account owner)"
  domain: ai-development
  role: reference
  lifecycle:
    approval:
      decision_status: Draft
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-27"
      last_verification_note: "The payload digest and byte count were recomputed from the payload after the copy; the front matter is excluded from the digest scope."
    usage_status: Active
    modification_status: Unchanged
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "Executed prompt snapshot for AID-2026-302"
    canonical_scope_id: "ai-development/aid-2026-302-prompt-v1"
    canonical_scope_keywords:
      - "prompt-snapshot"
      - "body-digest"
    canonical_conflict_status: None
    normative_status: Informative
# prompt_id: AID-2026-302-PROMPT
# version: 1
# payload_encoding: UTF-8
# digest_algorithm: SHA-256
# digest_scope: "Exact bytes after the closing front-matter delimiter and its immediately following LF; the front matter is excluded."
# executed_prompt_sha256: 6907cc7a0e5ad4c1f43e4978be3589673a61f46654ec3101172b0589df884575
# executed_prompt_bytes: 4817
---
# 任务：为 issue #1246 产出实现（协调会话不写代码，只逐字落盘你的输出）

## 背景（实测事实，勿再质疑，基线 origin/main = a588cd99）

仓库 `oahcom/AiMemoryBrainArchitecture`。缺陷：PR body 摘要只写不读。

- 唯一写入点：`.github/workflows/session-evidence.yml:119-142`，步骤名 `Bind the verdict to the body it judged`，`if: always()`，用 `curl` 取 PR body 后 `python3 -c` 算 `sha256(body.encode('utf-8'))`，校验 `^[0-9a-f]{64}$`，写 `AI-SESSION-EVIDENCE-BODY-SHA256: $digest >> $GITHUB_STEP_SUMMARY`。
- 全树仅 2 处命中该 key：上述写入点 + `AID-2026-059/session-evidence-1029-1076.md:115` 的散文说明。
- 唯一读 `$GITHUB_STEP_SUMMARY` 的地方是 `session-evidence.yml:149` 的 `grep -q '^AI-SESSION-EVIDENCE: '`，按构造不匹配该 key。
- `scripts/governance/session_evidence/validate.py` 只校验 prompt 摘要（`:1817` 的 `hashlib.sha256`），不碰 body 摘要。
- 既有 shape guard：`scripts/check_session_evidence_workflow_shape.py`（351 行，位于 required context `Repository hygiene (hard gate)` 内，由 `.github/workflows/repository-hygiene.yml:181-182` 调用；自测在 `:186-191`）。它已断言 4 条性质：三个 job id 齐全、head job 无 `ref:`、verdict job 无 `needs:`、`pull_request` 声明 `edited`。文件内 `digest|BODY-SHA256|always()` 命中数为 0。
- 该 guard 的测试：`scripts/test_check_session_evidence_workflow_shape.py`（17 个 test）。
- issue 给出的关闭条件 A：**某个 gate 必须对下列三种 mutation 返回非零**：
  1. 删除整个 `Bind the verdict to the body it judged` 步骤
  2. 把该步骤的 `if: always()` 改成 `if: success()`
  3. 把 `echo "AI-SESSION-EVIDENCE-BODY-SHA256: $digest"` 换成裸 `echo "AI-SESSION-EVIDENCE: PRESENT"`
- 关闭条件 B（不采用）：若维持"report 而非 gate"，须在 `PR-GOVERNANCE-001 §7` 写明，且 `grep -n "BODY-SHA256\|body digest" 14-ai-development/PR-GOVERNANCE-001.md` 当前为 0。**本任务选择 A，不走 B。**

## 硬约束

- **不得新增 workflow，不得新增 required context**。实现必须是既有 guard 的扩展，从而自动落在 `Repository hygiene (hard gate)` 里。
- 只用 Python 标准库。不引入依赖。
- 不得改动 `session-evidence.yml` 本身（那是被检查对象；改它等于让被测方改判据）。
- 不得改动既有 4 条断言的语义与消息；新断言必须独立可诊断（失败消息要能指出是三种 mutation 中的哪一种，并给出行号）。
- 检查器对**当前 main** 必须 exit 0；对三种 mutation 各 exit 1。
- 代码注释英文，与仓库风格一致（docstring 首段说明"钉住哪个缺陷"，测试 docstring 写 `python3 scripts/test_...py`）。

## 交付物（严格格式，禁止"略"）

### 1. 决策记录（≤25 行）
- 断言粒度：为什么用"步骤名 + 该步骤内三要素（`if: always()` / 正则命中写入行 / 64-hex 校验存在）"而不是解析 YAML 语义。
- 为什么不在 `validate.py` 里读 summary 回比（给出你判断的 1 条硬理由）。
- 被否决的替代方案 2 条，各 1 句理由。

### 2. 文件全文（fenced code block，第一行 `# path: <相对路径>`）
- `scripts/check_session_evidence_workflow_shape.py`（**完整文件**，不是 diff）
- `scripts/test_check_session_evidence_workflow_shape.py`（**完整文件**）
- `14-ai-development/work-items/AID_PLACEHOLDER/manifest.yaml`
- `14-ai-development/work-items/AID_PLACEHOLDER/evidence.md`

manifest 必须含且仅需含下列 20 个顶层键（`scripts/ci/check_work_item_manifest_schema.py` 的 REQUIRED）：
`work_item_id, title, class, risk, risk_rationale, status, id_status, sponsor, accountable_owner, acceptance_authority, attribution, date, repository, base_branch, base_commit_sha, scope, evidence, documentation, session_evidence, implementation`
其中 `work_item_id: AID_PLACEHOLDER`、`status: DISPATCHED`、`id_status: PROVISIONAL`、`base_branch: main`、`base_commit_sha` 留 `PLACEHOLDER_BASE_SHA`、`carrier` 信息留 `PLACEHOLDER_PR`。`scope.files_to_create` / `files_to_modify` 必须与上面文件清单一致。

### 3. 三种 mutation 的自证命令序列
对每种 mutation 给出：`git apply` 可用的 patch 文本 + 期望的检查器退出码 + 期望失败消息的关键子串。要求 patch 能在干净树上直接应用。

### 4. 回归声明
明确写出：本扩展不改变既有 4 条断言的任何行为，并给出为什么（1–2 句）。

## 输出纪律
- 中文说明，英文代码。
- 不给"示意""伪代码""其余同上"。文件必须是可保存即用的全文。
- 若你认为契约有歧义，按最严格读法实现，并在决策记录里写明你选了哪个读法。
