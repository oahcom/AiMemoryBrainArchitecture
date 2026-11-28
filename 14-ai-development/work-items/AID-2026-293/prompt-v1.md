---
document_metadata:
  steward: "user-authorized operator (delegated by account owner)"
  domain: ai-development
  role: reference
  lifecycle:
    approval:
      decision_status: Draft
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "The complete prompt snapshot, including this document metadata block, is recorded and must be verified against its final Git blob using the digest and byte count stored in the work-item manifest."
    usage_status: Active
    modification_status: Unchanged
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "Executed prompt snapshot for AID-2026-293"
    canonical_scope_id: "ai-development/aid-2026-293-prompt-v1"
    canonical_scope_keywords:
      - "prompt-snapshot"
      - "body-digest"
    canonical_conflict_status: None
    normative_status: Informative
# prompt_id: AID-2026-293-PROMPT
# version: 1
# payload_encoding: UTF-8
# digest_algorithm: SHA-256
# digest_scope: "Exact bytes of the entire file, including this front matter and all prompt content; nothing is excluded."
---

# RED-1478 第 1 次投递：PR #1478 五个红项的可执行修复正文

你是仓库 `oahcom/AiMemoryBrainArchitecture` 治理裁决者。我是执行方（RED-1478 子会话），只做机械转录：你给的正文我逐字落盘，不改写、不补全、不翻译。凡需要判断/设计/取舍的地方都由你定。

## 0. 硬约束（执行侧）
- 不 force、不 rebase、不合并、不改其他 PR。
- 已落地且**不得改写正文**：`00-governance/schemas/work-item-registry.schema.json`（722 行 / 16042 B）、`00-governance/schemas/work-item-registry.source-rules.md`（359 行 / 15413 字符）、`00-governance/schemas/fixtures/`（11 例，`PASS=11 FAIL=0`）。**唯一例外**：你明确要求给 `source-rules.md` 加 `document_metadata` 前块。
- 中文正文只能由你产出，执行侧禁止自行翻译。
- 分支 `gov/2026-11-28-registry-schema` 已 merge `origin/main@f77b1e63f0aca6b93f14fee5bd5c04510053ee23`，当前 head `8a69d6dd05679e3d21c31aadb43a0a48188fc0fa`（merge commit，无冲突，`INDEX.md` 手工避开 `merge=union` 后正常合并，无同 AID 双行）。
- 该分支**只新增**了 25 个文件（schema + source-rules + 11 组 fixture + run_fixtures.py），**没有** manifest、没有 INDEX 行、没有前块、没有对文件。

## 1. 五条红项的 CI 原文（逐字，来自 GitHub Actions job log / check-run annotations）

### 1.1 `GOV-DOC-002 metadata checks`（check-run 140801557101，失败步骤 `Enforce work-item uniqueness against the current target base`）
```
DELETION: 14-ai-development/work-items/AID-2026-326 exists_on_base=true absent_on_candidate=true
WORK-ITEM UNIQUENESS: DELETION (base_tree=adafdab4d6de4bec5a0a945b057b25de34ed6406 candidate_tree=0760483e4ac151f333682e6a51ac15e3c67133ba violations=0 deletions=1)
##[error]Process completed with exit code 1.
```
（执行侧判断：这是 candidate 树陈旧造成的——head `ba8b34fa` 里没有 main 后加的 AID-2026-326，GitHub 生成的 merge candidate 因此“删除”了它。本次 merge 已把 AID-2026-326 带入，这条预期自愈。但同一 job 后面的 `Validate document metadata` 步骤一旦执行，本地等价检查报：）
```
FAIL: 1 error(s)
  DM-01 missing document_metadata block: 00-governance/schemas/work-item-registry.source-rules.md
```

### 1.2 `GOV-DOC-001 structural checks`（check-run 140802959278，失败步骤 `Check paired documentation and PR manifest`）
```
##[error]New bilingual gap outside frozen baseline: 00-governance/schemas/work-item-registry.source-rules.md
##[error]Process completed with exit code 2.
```

### 1.3 `Bilingual docs coverage (ratchet)`（check-run 140801558018）
```
ratchet: scripts/ci/baselines/bilingual-docs.txt
ratchet: baseline=77 current=78 regressions=1 fixed=0
##[error]ratchet regression (new failure not in baseline): 00-governance/schemas/work-item-registry.source-rules.md -> docs/en/00-governance/schemas/work-item-registry.source-rules.md AND docs/zh-CN/00-governance/schemas/work-item-registry.source-rules.md
ratchet: FAIL - 1 new failure(s) above baseline.
##[error]Process completed with exit code 1.
```

### 1.4 `Repository hygiene (hard gate)`（check-run 140801557207，失败步骤 `Check committed repository hygiene and new-file admission`）
```
##[error]new-file admission violation: no allowlist rule for '00-governance/schemas/fixtures/invalid_additional_property.expected.json'
##[error]new-file admission violation: no allowlist rule for '00-governance/schemas/fixtures/invalid_additional_property.yaml'
##[error]new-file admission violation: no allowlist rule for '00-governance/schemas/fixtures/invalid_enum.expected.json'
##[error]new-file admission violation: no allowlist rule for '00-governance/schemas/fixtures/invalid_enum.yaml'
##[error]new-file admission violation: no allowlist rule for '00-governance/schemas/fixtures/invalid_known_without_value.expected.json'
##[error]new-file admission violation: no allowlist rule for '00-governance/schemas/fixtures/invalid_known_without_value.yaml'
##[error]new-file admission violation: no allowlist rule for '00-governance/schemas/fixtures/invalid_unknown_with_value.expected.json'
##[error]new-file admission violation: no allowlist rule for '00-governance/schemas/fixtures/invalid_unknown_with_value.yaml'
##[error]new-file admission violation: no allowlist rule for '00-governance/schemas/fixtures/invalid_work_item_id.expected.json'
##[error]new-file admission violation: no allowlist rule for '00-governance/schemas/fixtures/invalid_work_item_id.yaml'
##[error]new-file admission violation: no allowlist rule for '00-governance/schemas/fixtures/known.expected.json'
##[error]new-file admission violation: no allowlist rule for '00-governance/schemas/fixtures/known.yaml'
##[error]new-file admission violation: no allowlist rule for '00-governance/schemas/fixtures/known_empty.expected.json'
##[error]new-file admission violation: no allowlist rule for '00-governance/schemas/fixtures/known_empty.yaml'
##[error]new-file admission violation: no allowlist rule for '00-governance/schemas/fixtures/not_applicable.expected.json'
##[error]new-file admission violation: no allowlist rule for '00-governance/schemas/fixtures/not_applicable.yaml'
##[error]new-file admission violation: no allowlist rule for '00-governance/schemas/fixtures/unconfirmed.expected.json'
##[error]new-file admission violation: no allowlist rule for '00-governance/schemas/fixtures/unconfirmed.yaml'
##[error]new-file admission violation: no allowlist rule for '00-governance/schemas/fixtures/undecided.expected.json'
##[error]new-file admission violation: no allowlist rule for '00-governance/schemas/fixtures/undecided.yaml'
##[error]new-file admission violation: no allowlist rule for '00-governance/schemas/fixtures/unknown.expected.json'
##[error]new-file admission violation: no allowlist rule for '00-governance/schemas/fixtures/unknown.yaml'
##[error]new-file admission violation: no allowlist rule for '00-governance/schemas/work-item-registry.schema.json'
```
（执行侧本地等价复跑在 merge 后 head 上又额外列出 `00-governance/schemas/fixtures/not_applicable.expected.json`、`00-governance/schemas/fixtures/known_empty.expected.json` 等同族路径，以及 `run_fixtures.py` 因 `.py` 后缀本就放行。即：需要放行的是 `00-governance/schemas/**` 下的 `.json` 与 `.yaml`。）

### 1.5 `Session Evidence`（check-run 140802959572，失败步骤 `Validate session evidence`）
```
MISSING: Work Item manifest: path does not exist in PR Head Git tree: 14-ai-development/work-items/AID-2026-293/manifest.yaml
##[error]Process completed with exit code 1.
```
（PR body 缺陷已修；现在只剩这条。校验器读的 manifest 字段集是：`implementing_ai_session`、`executed_prompt_snapshot_file`、`executed_prompt_sha256`、`executed_prompt_bytes`、`executed_prompt_provenance`、`session_reference_status`、`session_evidence_ref`。）

## 2. 仓库现有约定（原文摘录，供你据此产出正文）

### 2.1 `document_metadata` 前块的真实样例 —— `00-governance/architecture-document-management-policy.md` 第 1-40 行
```yaml
---
document_metadata:
  domain: security-governance
  role: normative-standard
  lifecycle:
    approval:
      decision_status: Under-Review
      approver: NOT_RECORDED
      decision_date: NOT_RECORDED
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "00-governance/architecture-document-management-policy.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "No formal approval record, approver identity or decision date exists in this repository; recorded as NOT_RECORDED rather than inferred."
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
    canonical_status: Canonical
    canonical_scope: "Governance: architecture document management"
    canonical_scope_id: "security-governance/document-management-policy"
    canonical_scope_keywords:
      - document-metadata
      - lifecycle
      - canonical-authority
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Normative
---
```

### 2.2 官方模板 `00-governance/templates/document-metadata-template.md` 全文
```markdown
---
document_metadata:
  steward: "Architecture Governance"  # REQUIRED for newly added governed documents
  domain: security-governance
  role: reference
  lifecycle:
    approval:
      decision_status: Draft
    evidence_verification:
      verification_status: Unverified
    usage_status: Active
    modification_status: Unchanged
  authority:
    canonical_status: Non-Canonical
    normative_status: Informative
    canonical_conflict_status: None
---
```

模板内 `## The block / 待复制块` 给出的完整可复制块（含全部 REQUIRED 叶子与注释）：
```yaml
---
document_metadata:
  steward: "Architecture Governance"  # REQUIRED for newly added governed documents
  domain: architecture              # REQUIRED, closed enum (13 values)
  role: design-specification        # REQUIRED, closed enum (9 values)

  lifecycle:
    approval:
      decision_status: Draft        # REQUIRED
      approver: null
      decision_date: null
      approved_version:             # REQUIRED when decision_status: Approved
        scheme: git                 # git | content-hash
        value: null
      approval_scope:
        type: Full-document         # the only value DM-10 honours
      approval_applicability: Applicable-To-Current-Version
      evidence_reference: []
      revocation: null              # REQUIRED and non-null when decision_status: Revoked

    evidence_verification:
      verification_status: Unverified   # REQUIRED
      last_verified_date: null
      last_verification_note: null

    usage_status: Active            # REQUIRED
    modification_status: Unchanged  # REQUIRED

    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null

    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null

  authority:
    canonical_status: Non-Canonical # REQUIRED
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords: []
    canonical_conflict_status: None # REQUIRED
    canonical_conflict_resolution: null
    normative_status: Informative   # REQUIRED
---
```

模板内 `## Rules that are easy to get wrong` 原文要点：
```
- `superseded_by` MUST NOT be written by hand. It is derived (DM-08).
- A document under `docs/en/` or `docs/zh-CN/` MUST declare `bilingual_counterpart.source` (DM-12).
- A mirror group MUST agree on `domain`, `role` and `normative_status`, and at most one member is
  `Canonical` (DM-12).
- `canonical_conflict_status: Under-Review` requires `canonical_status: Candidate`; a document in
  conflict state MUST NOT be `Canonical` (DM-11).
- Every path value is a normalised repository-relative path: no absolute paths, no `..`, no
  backslashes, no repeated `./`. A violation is an error, never silently rewritten.
```

### 2.3 `00-governance/architecture-document-metadata.schema.yaml` 的闭枚举
```
domain enum (13):
  - agent-integration
  - ai-development
  - architecture
  - consistency-recovery
  - domain-model
  - memory-brain
  - memory-compiler
  - memory-context
  - memory-runtime
  - protocol
  - security-governance
  - storage-index
  - testing-acceptance

role enum (9):
  - decision-record
  - design-specification
  - guide
  - index
  - normative-standard
  - reference
  - research
  - review-report
  - work-record

decision_status enum: Approved | Draft | Rejected | Revoked | Under-Review | Withdrawn
verification_status: Unverified | (其它见 schema)
canonical_status: Canonical | Non-Canonical | Candidate
normative_status: Normative | Informative
```

### 2.4 zh-CN / en 对文件的命名与位置
- 源：`00-governance/schemas/work-item-registry.source-rules.md`
- 需要的两个对文件（ratchet 原文）：`docs/en/00-governance/schemas/work-item-registry.source-rules.md` **AND** `docs/zh-CN/00-governance/schemas/work-item-registry.source-rules.md`
- 现有 `00-governance` 对文件实例：`docs/en/00-governance/architecture-invariants.md`、`docs/zh-CN/00-governance/architecture-invariants.md`（同名同相对路径，仅加 `docs/<lang>/` 前缀）。

**源文件** `00-governance/architecture-invariants.md` 的 `bilingual_counterpart` 块（`authority` 之后）：
```yaml
  bilingual_counterpart:
    en: "docs/en/00-governance/architecture-invariants.md"
    zh-CN: "docs/zh-CN/00-governance/architecture-invariants.md"
```

**zh-CN 镜像** `docs/zh-CN/00-governance/architecture-invariants.md` 的对应块（注意有 `source`，且 `canonical_status: Non-Canonical`）：
```yaml
  authority:
    # Translation of the authoritative source. It does not independently
    # claim canonical authority; see bilingual_counterpart below.
    canonical_status: Non-Canonical
    canonical_scope: "Architecture: system invariants"
    canonical_scope_id: "architecture/system-invariants"
    canonical_scope_keywords:
      - invariant
      - constraint
      - subsystem
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Normative
  bilingual_counterpart:
    source: "00-governance/architecture-invariants.md"
    en: "docs/en/00-governance/architecture-invariants.md"
    zh-CN: "docs/zh-CN/00-governance/architecture-invariants.md"
```

### 2.5 `scripts/check_bilingual_docs.py` 的例外机制（原文）
```python
def approved_exception(body: str) -> bool:
    if "BILINGUAL-EXCEPTION: APPROVED" not in body:
        return False
    labels = (
        "Exception Owner:", "Authoritative language/version:",
        "Missing counterpart path:", "Exact source revision:",
        "Due date (YYYY-MM-DD", "Tracking Issue/PR:",
        "Approval evidence",
    )
```
配对要求原文：
```
{source} requires all counterparts changed in this PR: ...
```
ratchet 基线文件：`scripts/ci/baselines/bilingual-docs.txt`（**只可缩小**，`baseline=77`，新增第 78 条即红）。

### 2.6 `scripts/ci/check_repository_hygiene.py` 的准入表实现（原文结构）
```python
CHECK_VERSION = "2026-11-27.2"
...
# A1: protocol schema files live directly under schemas/. One level only;
# schemas/<sub>/x.schema.json is not admitted.
PROTOCOL_SCHEMA_RE = re.compile(r"08-bmcp-protocol/schemas/[^/]+\.schema\.json")
...
# 现有若干同风格锚定规则，例如：
WORK_ITEM_MANIFEST_RE = re.compile(
    r"14-ai-development/work-items/AID-\d{4}-\d{3}/manifest\.yaml"
)
GOVERNANCE_EVIDENCE_RE = ...      # 见文件
ARCHITECTURE_METADATA_SCHEMA_RE = ...
DOCUMENT_SCOPE_REGISTRY_RE = ...
...
def is_allowed_new_path(path):
    """Apply the fixed, positive admission policy to one new tree path."""
    pure = PurePosixPath(path)
    name = pure.name
    suffix = pure.suffix.lower()

    if suffix in ALLOWED_DOCUMENT_SUFFIXES: return True     # .md .rst .adoc
    if suffix in ALLOWED_SOURCE_SUFFIXES: return True       # .py .sh .js .ts ...
    if path in ALLOWED_CONFIG_PATHS: return True
    if path in ALLOWED_DATA_PATHS: return True
    ...
    if WORK_ITEM_MANIFEST_RE.fullmatch(path): return True
    if MANIFEST_SCHEMA_REGISTRY_RE.fullmatch(path): return True
    if WORK_ITEM_MANIFEST_SCHEMA_RE.fullmatch(path): return True
    if PROTOCOL_SCHEMA_RE.fullmatch(path): return True
    if CONFORMANCE_VECTOR_RE.fullmatch(path): return True
    if CRATE_MANIFEST_RE.fullmatch(path): return True
    if GOVERNANCE_EVIDENCE_RE.fullmatch(path): return True
    if CRATE_VERIFICATION_RE.fullmatch(path): return True
    if BASELINE_FILE_RE.fullmatch(path): return True
    if GOV_DOC_001_INHERITANCE_RE.fullmatch(path): return True
    if ARCHITECTURE_METADATA_SCHEMA_RE.fullmatch(path): return True
    if DOCUMENT_SCOPE_REGISTRY_RE.fullmatch(path): return True
    if REMOTE_WORKER_INVENTORY_RE.fullmatch(path): return True
    return False
```
拒绝时的报错正是 `f"no allowlist rule for '{path}'"`。该文件有自己的自检 `scripts/test_check_repository_hygiene.py`（CI 先跑它，107 tests OK 后才跑真实准入），并且 `CHECK_VERSION` 打印在日志里，版本字符串与“规则变化”绑定是仓库明写的纪律（见文件内注释：两个不同策略不得共用同一个版本号）。版本字符串也出现在 `Work-item manifest consistency version=...`、`Work-item index membership version=...` 等行。

### 2.7 `AID-2026-293` 的 manifest 模板 —— `14-ai-development/work-items/AID-2026-326/manifest.yaml` 全文（刚由 main 引入，是当前最新范式）
```yaml
work_item_id: AID-2026-326
title: "Verify actual execution of required PR check contexts on exact Head"
class: CODE/CI
risk: R2
risk_rationale: >-
  Adds a read-only GitHub check-run audit and a manually dispatched workflow.
  Does not modify branch protection or the existing required-context set.
  The implementation distinguishes absent execution, stale heads, failed
  runs, pending runs and incomplete API evidence.
status: DISPATCHED
id_status: PROVISIONAL
sponsor: USER-PRINCIPAL-DELEGATED
accountable_owner: USER-PRINCIPAL-DELEGATED
acceptance_authority: NOT_ASSIGNED
attribution: "user-authorized operator (delegated by account owner)"
date: "2026-11-27"
repository: oahcom/AiMemoryBrainArchitecture
base_branch: main
base_commit_sha: "31c1e5d83e7dad326dbd4b69d4a8e19534718ff1"
tracking_issue: "#1469"

scope:
  summary: >-
    ...
  in_scope:
    - "..."
  files_out_of_scope:
    - "..."
  change_boundary: >-
    ...

evidence:
  - "Issue #1469"
  - "..."

documentation:
  - path: "14-ai-development/work-items/AID-2026-326/prompt-v1.md"
    relationship: reference
  - path: "14-ai-development/work-items/AID-2026-326/evidence.md"
    relationship: evidence
  - path: "14-ai-development/work-items/AID-2026-326/session-evidence.md"
    relationship: evidence

acceptance_criteria:
  - id: AC1
    description: >-
      ...
    measurement: >-
      ...
    expected_result: "..."

review:
  status: NOT_ASSIGNED
  note: >-
    Independent review has not been recorded. The implementing session
    does not review or approve its own work.

acceptance:
  status: NOT_ASSIGNED
  record_ref: ""
  acceptance_authority: NOT_ASSIGNED

implementation:
  status: IMPLEMENTED
  summary: >-
    ...
  pull_request: PENDING
  merge_commit: ""
  implementation_commit: ""
  ci_status: NOT_CLAIMED
  files_changed:
    - scripts/ci/check_required_context_execution.py
    - ...
  tests:
    - "python -m unittest ..."
    - ...

session_evidence:
  - role: IMPLEMENTER
    issue_refs:
      - "#1469"
    implementing_ai_session: GPT6_SESSION_20261127_AID2026326
    executed_prompt_snapshot_file: 14-ai-development/work-items/AID-2026-326/prompt-v1.md
    executed_prompt_sha256: afc8e732df2de2eb29e22b21b05558c395c1b2ee1ee2c4ddeca5e3744ba39e91
    executed_prompt_bytes: 4894
    executed_prompt_provenance: NOT_VERIFIED
    session_reference_status: "RECORDED"
    session_evidence_ref: 14-ai-development/work-items/AID-2026-326/session-evidence.md
```

### 2.8 `14-ai-development/work-items/INDEX.md`
表头（9 列，第 52 行）：
```
| Work Item ID | Title | Owner | Class/Risk | Status | Prompt | Implementation | Review | Acceptance |
```
最新一行的完整形态（第 53 行，供你照抄列语义）：
```
| [AID-2026-326](AID-2026-326/manifest.yaml) | Verify that every required check context executed at the pull request head, not merely that a workflow declares it | USER-PRINCIPAL-DELEGATED | GATE/TEST / R1 | DISPATCHED — read-only merge-time audit reporting EXECUTED / ABSENT / STALE / FAILED / INCOMPLETE, with `mergeable_state=unknown` treated as INCOMPLETE | AID-2026-326-PROMPT v1 — `prompt-v1.md`, 4894 bytes, SHA-256 `afc8e732...`; provenance NOT_VERIFIED | `scripts/ci/check_required_context_execution.py` plus its self-test and a `workflow_dispatch` wiring workflow; no branch protection change and no new required context | NOT_ASSIGNED — independent reviewer not recorded | PENDING — no Owner acceptance asserted; #1469 remains OPEN |
```
该文件自己的前块（第 1-32 行）是 `domain: ai-development` / `steward: "Architecture Governance"` / `role: index` / `canonical_status: Canonical` / `canonical_scope_id: ai-development/work-items-index` / `bilingual_counterpart: {source: null, en: null, zh-CN: null}`。

文件内对 `merge=union` 的规范说明（第 42-49 行）：
```
- It guarantees that two **appends** merge without human intervention.
- It does **not** resolve an edit to a row present on both sides. Union keeps both variants, so one `AID` ends up on two rows with different cells.
- It does **not** preserve a deletion whose neighbouring line was changed on the other side. The deleted row comes back.
- All three silent outcomes end as the same `AID` on two lines, so `scripts/check_traceability.py --index-only` refuses them (`T-04 duplicate INDEX entry`).
```
索引成员检查会核对目录数与链接数一致（本地复跑：`Work-item index membership version=2026-11-27.2 directories=152 linked=152`）。所以新增 `AID-2026-293/` 目录与 INDEX 行必须同时落地。

### 2.9 PR #1478 现有 body 的相关段落（原文）
```
- Work Item ID: AID-2026-293
- Related issue(s): #1464
- AI-assisted work: YES
- Session evidence reference(s):
  00-governance/schemas/work-item-registry.source-rules.md
  00-governance/schemas/fixtures/run_fixtures.py

### Per-Issue AI session evidence / 每个 Issue 的 AI 会话证据

| Related Issue | Issue AI-assisted work | Evidence refs for this Issue |
| --- | --- | --- |
| #1464 | LEGACY_UNDECLARED | N/A |
```
body 的 `## Bilingual documentation` 段现为：
```
- Chinese paths: none added
- English paths: `00-governance/schemas/work-item-registry.source-rules.md`
- Parity evidence: N/A
- GOV-DOC-001 gate result: expected red. ...
- Manifest: BILINGUAL-MANIFEST: PENDING
- Exception Owner / source revision / missing path / due date / tracking Issue / approval evidence: none claimed; ...
```

## 3. 请逐条输出（格式必须照此，便于我机械落盘）

对每个文件用：
```
### FILE: <repo-relative path>
<一句话说明：新建 / 追加 / 替换>
```<language>
<完整文件正文，逐字可落盘；不要省略号，不要 diff 片段>
```
```

需要你给出：

1. **`00-governance/schemas/work-item-registry.source-rules.md` 的 `document_metadata` 前块**：完整 YAML（含 `---` 前后定界行）。请自行选定 `domain` / `role` / `steward` / `lifecycle` / `authority` 的取值，并说明插入方式（在现有第 1 行 `# Canonical Work Item Registry — Source Rules` 之前插入，正文其余字节不变）。若你认为「保持逐字、不加前块」才是正确裁决，请明确写出替代方案（例如用哪个检查的什么机制豁免），并给出该机制要求的正文。

2. **zh-CN / en 对文件**：
   - 是否建立？若建立，给出 `docs/en/...` 与 `docs/zh-CN/...` 两个文件的**完整正文**（zh-CN 必须是你写的中文全文，含它自己的 `document_metadata` 前块与 `bilingual_counterpart` 块）。
   - 源文件是否需要同步补 `bilingual_counterpart` 块？给出该块正文与插入位置。
   - 若你的裁决是不建立对文件、改用 `BILINGUAL-EXCEPTION: APPROVED`，请给出 PR body 中该段的完整正文（7 个标签齐全），并说明为什么这不会同时触发 ratchet 红。

3. **hygiene 准入表的精确 diff**：给出
   - 新增常量的完整代码（常量名、注释、正则；覆盖 `00-governance/schemas/` 下的 `.json` 与 `.yaml`，且必须锚定到该目录、不扩大到全仓库）；
   - `is_allowed_new_path()` 中注册行的插入位置（插在哪一行之后）；
   - `CHECK_VERSION` 是否变更、改成什么值；
   - `scripts/test_check_repository_hygiene.py` 是否需要同步新增用例，若需要给出完整用例函数正文。

4. **`14-ai-development/work-items/AID-2026-293/manifest.yaml`**：完整正文（字段齐全，`session_evidence` 段落必须能通过校验器）。
   - 需要 `prompt-v1.md` / `evidence.md` / `session-evidence.md` 吗？若需要，逐个给出完整正文。
   - 注意：`executed_prompt_sha256` / `executed_prompt_bytes` 必须与真实快照文件一致；请告诉我这些值该怎么取值（我按你的指示计算后回报，或你给出可接受的占位策略）。
5. **`14-ai-development/work-items/INDEX.md` 该行**：完整正文，9 列，以 `|` 收尾，插入位置（第几行之后）。
6. **PR body 需要补/改的段落**：`Related issue(s)` 与三列映射表，以及 `## Bilingual documentation`、`## Merge decision` 中需要改写的整段正文。

最后给一张表：每条修复 → 命中哪个检查 → 执行后预期结论（PASS/仍红及原因）。若你认为某条无法在「不改写已落地正文」的前提下达成 16/16，请直接说明证据不足或需 Owner 决策，不要给出无法落地的正文。
