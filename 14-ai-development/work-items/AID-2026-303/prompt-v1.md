---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-303/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Prompt snapshot recorded for traceability; its digest and Git blob and commit pins must be measured from the committed prompt file and populated in the work-item manifest."
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
    canonical_scope: "Takeover instructions for the #1267 source-revision pointer implementation lane, including clean cherry-picking of the stalled implementation commits and re-derivation of both English and Chinese mirror section 4.1 text."
    canonical_scope_id: "ai-development/aid-2026-303-source-revision-pointer-takeover-prompt"
    canonical_scope_keywords:
      - "AID-2026-303"
      - "#1267"
      - "source-revision pointers"
      - "stalled lane takeover"
      - "mirror section 4.1 re-derivation"
      - "English and Chinese mirrors"
      - "prompt traceability"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# #1267 接管完成，需要你出：证据补记、PR body、工作项字段处置

## 我做了什么（全部逐字按你上一轮文本）
1. 原分支 `origin/fix/2026-11-27-aid303-source-revision-pointers` 在 `69500815`（15:16:44）之后 **60 分钟无推进、无 PR、无评论回复**，判为停滞车道。我接管。
2. 新分支 `fix/2026-11-27-aid303-mirror-rederive`，从当时的 `origin/main` `460f437e` 起，cherry-pick 两个提交：
   - `fce62cad`（原 `4211b28a`）：8 个 stale 指针 + 4 个 non-blob 修复 + workflow 接线 + 删 `gate-wiring.txt` 条目 + 新 baseline `source-revision-pointers.txt`；
   - `96cf0ba2`（原 `69500815`）：工作项记录对齐 schema。
   两个都**干净应用，无冲突**。
3. 应用了你上一轮给的**两份镜像 §4.1 替换块**（`reply-6b08ffa5-152431.md` 的 B 与 C），逐字。
   - EN 第 50 行现为：`- Canonical Forget identity/lifecycle/Fence mechanics (Owner D); global authorization, retention/legal-hold, external-copy policy, global target inventory and global completion criteria (Owner I).`，第 52 行为 Global Forget Completion 整段。
   - ZH 第 50 行为 `- Canonical Forget 身份／生命周期／Fence 机制（Owner D）；全局授权、保留／法律保全、外部副本策略、全局目标清单及全局完成标准（Owner I）。`，第 52 行为对应整段。
   - 两份镜像的 `Version: 1.0` 与 `Status:` 行按你的裁定保持原值。

## 实测（新分支，`PYTHONUTF8=1`）
```
python scripts/check_source_revision_pointers.py   → exit 1
POINTERS=52  ACCURATE=28  STALE=0  UNRESOLVED=0
DEREFERENCED=24  BAD_DEREFERENCE=0  NON_BLOB_REFERENCE=2  BAD=2
```
两条剩余的失败项与 `scripts/ci/baselines/source-revision-pointers.txt` 中的两行**逐字节相同**（用 Python 模拟 workflow 里那条 `sed -n` 过滤后比较：`identical True`），即 ratchet step 会通过。注意：本地**不能**直接跑 `gate_ratchet.py`——workflow 里那条命令是 `bash -o pipefail -c ...`，本机 `bash` 解析到 WSL 启动器，按硬约束禁止使用；因此我以等价过滤验证，并会在 PR body 里说明"ratchet 本体只在 CI（ubuntu）执行"。

## 其他实测
- 该分支带来的 workflow 改动是在既有 required job `Repository hygiene` 里新增两个 step（self-check + ratchet），**不新增 required context、不改分支保护**。
- `scripts/ci/baselines/gate-wiring.txt` 删掉了 `scripts/check_source_revision_pointers.py` 那一行与 8 行注释块。
- 新文件 `scripts/ci/baselines/source-revision-pointers.txt` 有 7 行注释 + 2 行条目（`memory-brain-guide` EN/ZH）。

## 需要你产出
A. **`14-ai-development/work-items/AID-2026-303/evidence.md` 的追加小节**（Markdown 全文，我将 append 到该文件末尾）。要求：
1. 说明本分支是接管：原分支 `69500815` 停滞、无 PR，接管后 cherry-pick 两个提交并追加镜像正文重派生。
2. 记录上面 scanner 的实测数字与"两条失败项与 baseline 逐字节一致"这一验证方式（含为什么本地不跑 ratchet）。
3. 记录两份镜像 §4.1 的改动前后要点（不复制长篇正文，写清"第 6 个 bullet 替换 + 新增整段"即可），并引用 `c3707831777feb14aedd7aea0eca1c162bf59fc6`。
4. 明确主张边界：**不**声称 #1438/#1439 相关；**不**声称双语门禁已通过（浅克隆限制）；**不**声称 ratchet 已在 CI 通过（尚未跑）。
B. **该分支的 PR body 全文**。要求：
- 标题建议给两条备选，我选一条用；
- 说明 supersedes 停滞分支；
- 列出改动清单（12 个指针行 + 2 份镜像 §4.1 + workflow 2 step + `gate-wiring.txt` 删条目 + 新 baseline + AID-2026-303 四件套）；
- 贴 scanner 实测输出与 ratchet 等价验证；
- 说明两条 `memory-brain-guide` non-blob 基线是**临时例外、另立工作项**（你上一轮的裁定），不得写成已解决；
- 保留 `BILINGUAL-MANIFEST: COMPLETE`，并说明本次确有双语文档正文改动（两份镜像），因此该标记必须有实质对应。
C. **工作项字段处置**：`AID-2026-303/manifest.yaml` 里的 `status`、`pull_request`、`pull_request_url`、`merge_commit_sha`（原提交写的是 `PENDING` 还是别的我不确定，我落盘前会核对）——给出应改成什么值，以及是否需要改 `implementation.summary`。若需要改，给完整的替换行。
D. 一句话：这个 PR 合并后，#1267 能否关闭；若不能，还差什么。

## 约束
- 本机 Windows PowerShell，禁止 WSL；不要给 `bash -lc` 形式的本地执行建议。
- 行尾 LF、无 BOM；中文全角标点；SHA、行号、路径保留原文。
- 不要重发已经给过的两份镜像替换块（我已逐字应用）。
