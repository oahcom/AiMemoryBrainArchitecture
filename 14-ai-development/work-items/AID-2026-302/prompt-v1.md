---
document_metadata:
  domain: ai-development
  role: reference
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
        - "14-ai-development/work-items/AID-2026-302/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Structured snapshot of the dispatched task payload; prompt provenance is NOT_VERIFIED."
    usage_status: Active
    modification_status: Active-Modified
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  steward: "user-authorized operator (delegated by account owner)"
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "Executed task payload for AID-2026-302"
    canonical_scope_id: "ai-development/aid-2026-302-prompt"
    canonical_scope_keywords:
      - "aid-2026-302"
      - "blob pin"
      - "prompt snapshot"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---

# Executed task payload — AID-2026-302

Snapshot of the task text supplied to the implementing session, in dispatch
order. Turn 2 and Turn 3 are later user clarifications that amend Turn 1; the
effective scope is the three turns together.

## Turn 1 — dispatch

You are a subagent spawned by another session.
实现子代理。仓库 `D:\code\AiMemoryBrainArchitecture`（Windows，PowerShell，用 `;`）。push 权限已配置；API token 在 `D:\code\.tmp\tok.txt`（`Authorization: Bearer <token>`，curl 加 `--noproxy "*"`）。参考数据：`D:\code\.tmp\facts\mismatch-89.md`、`D:\code\.tmp\facts\302-inventory.md`、`D:\code\.tmp\facts\pin-audit-43.md`。

## Owner 已裁决的修复范围：**93 项，只改这些字段，不许扩大**

| 形态 | 对象 | 条数 |
|---|---|---|
| S2 | `session_evidence[].executed_prompt_sha256` | 40 |
| S2 | `session_evidence[].executed_prompt_bytes` | 40（与上面**成对原子修复**） |
| S3 | `authored_indexes[].root / .en_mirror_blob / .zh_cn_mirror_blob` | 6（AID-2026-100） |
| S3 | `related_evidence[].blob / .en_mirror_blob / .zh_cn_mirror_blob` | 3（AID-2026-100） |
| S4 | AID-2026-261 两条全零 sentinel（`prompt_sha256`/`prompt_bytes`） | 2 |
| S4 | AID-2026-100 `gate_a_reconstruction` 悬空 pin | 1 |
| S4 | AID-2026-170 `owner_ruling` 悬空 pin | 1 |

## 硬性规则

1. **只读已提交字节**：`git cat-file blob <commit>:<path>`，禁止读工作树。SHA 用 SHA-256，字节数用真实长度。
2. **S2 是 40 个原子对**：只改 sha 或只改 bytes 都算失败；必须同一 commit 内成对更新。
3. **解析作用域契约**（Owner C 项）：
   - 声明邻域显式给出历史提交（`commit`/`at_commit`/`source_commit`/`note` 里的 40-hex/`retained at commit <sha>`）→ `PINNED_COMMIT`，**在该提交上解析**；
   - 有线索但无法确定归属或唯一提交 → `UNRESOLVED_SCOPE`，标 `BLOCKED`，**不得**按候选树解析、**不得**记 PATH_MISSING、**不得**猜；
   - 只有 `CANDIDATE_TREE` 才允许报 PATH_MISSING；
   - **不得**把 manifest 里某处出现的 commit SHA 当成所有声明共享的锚点。
4. **AID-2026-261 sentinel**：不得当普通过期摘要重算。先查该字段是否仍是 schema 要求的有效声明、是否有明确目标文件。能确认 → 按真实字节成对填写（终态 `RESOLVED_VALID_PIN`）；有正式废弃依据 → 按 schema 允许方式迁移或删除并留记录（终态 `FORMALLY_RETIRED`）；无法确认 → `BLOCKED`，保持原值。
5. 禁止：改 `prompt_sha256` 顶层字段、改 work-item 编号、改未列出的字段、引入任何 baseline/豁免、无依据删除声明。

## 交付

1. 从最新 `origin/main` 建分支 `fix/aid-2026-302-pin-repair-93`，独立 worktree。
2. 新建 `AID-2026-302` work item（`manifest.yaml`/`prompt-v1.md`/`evidence.md`/`session-evidence.md` + `INDEX.md` 一行）。`evidence.md` 必须含**逐条表**：字段路径 / 原声明 / 作用域 / 目标提交 / 目标路径 / 真实 SHA-256 / 真实字节数 / 新声明 / 终态（`FIXED`/`RESOLVED_VALID_PIN`/`FORMALLY_RETIRED`/`BLOCKED`）/ 复核命令。
3. 分批 commit：`fix(aid-2026-302): repair S2 session digest pairs`、`fix(aid-2026-302): repair S3 authored and related declarations`、`fix(aid-2026-302): resolve S4 sentinels and historical pins`。
4. 本地验证并贴原始输出：修复前后 `python scripts/ci/check_manifest_blob_pins.py` 的 pins/mismatch/path_missing 计数对比（期望 mismatch 从 89 降到 0 或只剩已标 BLOCKED 的条数，且必须逐条解释）、`python scripts/check_traceability.py --index-only`、`python scripts/ci/check_repository_hygiene.py --base <main> --head <head>`、`python scripts/check_bilingual_docs.py`。
5. push 并开 PR（base=main），标题 `fix(gov): repair 93 declared pin fields by shape (AID-2026-302)`。body 含：`Work Item ID: AID-2026-302`、`Related issue(s): #1350`、`AI-assisted work: YES`、`Session evidence reference(s): 14-ai-development/work-items/AID-2026-302/session-evidence.md`、修复前后计数、BLOCKED 条数与原因、以及"未改 prompt_sha256、未引入豁免、未扩大范围"的声明。
6. **不合并**、不转 ready。

## 回报

PR 号、head sha、FIXED/RESOLVED_VALID_PIN/FORMALLY_RETIRED/BLOCKED 各多少条、修复前后 mismatch/path_missing 计数、四条命令退出码。

## Turn 2 — environment constraint

环境约束（立即生效，优先级高于你手上的任何命令）：**禁止使用本机 WSL**。不要执行 `wsl`、`wsl.exe`、`bash -lc`、`sh -c`、`/bin/bash`，不要引用 `/home/...`、`/mnt/c/...` 路径，不要用发行版里的 `python3`/`git`。

一律使用本机 Windows 工具链：PowerShell 语法（`;` 分隔）、`python`（而不是 `python3`）、Windows 版 `git`。若某条命令在 Windows 上不能原样运行，改用等价的本机实现并说明等价关系。

## Turn 3 — gate teardown added to scope

**新增硬性要求，立即并入你的实现（这会决定 PR 能否变绿）。**

### 实测事实

main 上的 blob-pin 门禁不是单向棘轮，而是**双向**的。`scripts/ci/gate_ratchet.py` 的 docstring 原文：

> The gate fails when: * a new item appears that is not in the baseline (regression), or * **a baseline item no longer fails (the baseline is stale and must be lowered).** Failing on the second case is deliberate.

基线文件：`scripts/ci/baselines/manifest-blob-pins.txt`。

现场证据：PR #1457（另一个会话做的「repin 40 条 executed-prompt」）CI 红在 `Repository hygiene (hard gate)`，日志原文：

```
##[error]ratchet baseline is stale (no longer failing): MISMATCH session_evidence[0].executed_prompt_snapshot_file path=14-ai-development/work-items/AID-2026-061/prompt-v1.md declared=18776 actual=18718
##[error]ratchet baseline is stale (no longer failing): MISMATCH ... declared=7ea255ab... actual=6c0a9cc7...
```

即：**你每修正一个被基线收录的声明值，基线里那条旧键就"不再失败"，棘轮立刻判红。** 所以"修数据但保留棘轮"在机械上不可能变绿。

### 因此你的交付必须追加两项（与 93 项修复同一个 PR、同一批 commit）

1. **删除 `scripts/ci/baselines/manifest-blob-pins.txt`**（整个文件）。
2. 修改 `.github/workflows/repository-hygiene.yml` 中调用 blob-pin 检查器的步骤：**去掉 `gate_ratchet.py` 包装，改为直接执行检查器并按 `status > 0` 失败**（即 `mismatch > 0` 或 `path_missing > 0` 即红）。**不得**保留 `status > 1` 这种宽松判定，**不得**新建任何替代基线。
3. 在 `AID-2026-302/evidence.md` 里写明：删除基线的前提是 93 项全部有终态且复跑 `mismatch=0 / path_missing=0`；并附上删除前后两次检查器原始输出。
4. 负向验证（必须贴原始输出）：在临时分支上故意把一个已修好的声明改错一位，证明**现在会红**（`status > 0`）；改回后变绿。这是"门禁真的能失败"的唯一证据。

### 不变的边界

- 只改这 93 项声明的声明值 + 上述两项棘轮拆除；**不得**顺手修别的字段、**不得**改 `prompt_sha256` 顶层、**不得**引入任何新豁免或 allowlist。
- S2 仍是 40 个原子对（sha + bytes 同改）。
- 若你发现删掉棘轮后有**基线之外的既有失配**冒出来（即当前 `status>1` 掩盖的错误），停下来把它们逐条列进报告，不要自行扩大修复范围；由我来裁决。

回报里必须包含：棘轮删除后 `python scripts/ci/check_manifest_blob_pins.py` 的 pins/ok/mismatch/path_missing 四个数与退出码、以及上面那条负向验证的原始输出。
