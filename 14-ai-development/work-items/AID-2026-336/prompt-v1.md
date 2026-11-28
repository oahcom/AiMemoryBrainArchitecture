---
document_metadata:
  steward: USER-PRINCIPAL-DELEGATED
  domain: repository-governance
  role: implementation-prompt
  lifecycle: immutable-after-payload-finalization
  authority: task-input-record
---

# AID-2026-336 Implementation Prompt

## Prompt identity

- Work Item: `AID-2026-336`
- Prompt ID: `AID-2026-336-PROMPT`
- Version: `v1`
- Repository: `oahcom/AiMemoryBrainArchitecture`
- Implementation branch: `aid-2026-336`
- Implementation commit: `d8512eee5`
- Parent commit: `daa935f7a`

## Actual prompt payload

# AID-2026-336 实施已完成，请产出最终工作项记录集

## 实测结果（全部由我在 `D:\code\_wt-aid336` 实跑得到，不是推算）

- 分支 `aid-2026-336`，rebase 到 `origin/main` 后实现提交 = **`d8512eee5`**（父提交 `daa935f7a`）。
- 改动 7 个文件：`check_manifest_blob_pins.py`（859 行）、`test_check_manifest_blob_pins.py`、`baselines/manifest-blob-pins.txt`、`assert_manifest_blob_pin_negative.py`、`test_assert_manifest_blob_pin_negative.py`、`.github/workflows/repository-hygiene.yml`（ratchet sed 增加三个新码）、`AID-2026-100/manifest.yaml`（`related_evidence[0]` 加 `reference_mode: historical`，digest 未动）。
- `python scripts/ci/check_manifest_blob_pins.py --commit HEAD` → **rc 0**：
  `main=d8512eee59e8bfdfec5e280e4a3a01fc62c61074 manifests=161 pins=12 ok=12 mismatch=0 path_missing=0 incomplete=0 excluded=163 unbound=0`
  （12 = 10 个 AID-336 in-scope pin + HEAD 上 2 个已绑定的 `blob_sha256`）
- `python scripts/ci/test_check_manifest_blob_pins.py` → **Ran 35 tests … OK**
- `python scripts/ci/test_assert_manifest_blob_pin_negative.py` → 7 tests OK
- `python -m unittest scripts/ci/test_resolve_manifest_blob_pin_base.py scripts/ci/test_assert_manifest_blob_pin_negative.py` → 15 tests OK
- `python scripts/ci/assert_manifest_blob_pin_negative.py --commit 9a2063ae…` → **NEGATIVE_ASSERTION_PASS**，新期望值：
  `main=9a2063ae1fa5d905b3817cd4eddba065a06daa73 manifests=108 pins=14 ok=7 mismatch=1 path_missing=0 incomplete=0 excluded=146 unbound=4`，另有 4 条 `UNBOUND_BLOB_SHA256` + 1 条 `REFERENCE_MODE_MISSING_OR_INVALID`，0 条 `MISMATCH ` / `PATH_MISSING ` / `INCOMPLETE `。
- `check_manifest_parse.py` 161/161 通过；`check_work_item_manifest_schema.py --tree HEAD --baseline 14-ai-development/reports/work-item-manifest-ac4-baseline.json` → rc 0，`Legacy ratchet new regressions: 0`。
- `AID-2026-100` 迁移后的 in-scope 计数：pins=10 ok=10（该 commit 上 `AID-2026-100` 无其它 finding）。

## 要你产出的文件（全部完整正文，不要片段、不要“略”）

1. `14-ai-development/work-items/AID-2026-336/manifest.yaml`
2. `14-ai-development/work-items/AID-2026-336/evidence.md`
3. `14-ai-development/work-items/AID-2026-336/session-evidence.md`
4. `14-ai-development/work-items/AID-2026-336/prompt-v1.md`
5. `14-ai-development/work-items/AID-2026-336/pincount.md`
6. `INDEX.md` 新增的一行（9 列，格式与下表完全一致，插在第 52 行位置之前/之后由你指定）
7. PR 正文（markdown）
8. `14-ai-development/work-items/AID-2026-331/reference-semantics.md` 中需要新增/替换的段落**最终版**（要反映 Q1 的 `classification="policy"`、Q4 的 `blob_sha256` 纳入 in-scope pin、以及 `--commit` 运行说明）

## 硬性约束

- `manifest.yaml` 必须能被 `check_work_item_manifest_schema.py` 与 `check_manifest_parse.py` 通过：`work_item_id`/`title`/`class`/`risk`/`status`/`id_status`/`tracking_issue`/`scope`/`evidence`/`documentation`/`verification`/`implementation`/`acceptance`/`merge`/`review` 等键按 331 的形状给全；**不得**出现 7 个顶层 legacy prompt 字段（`prompt_sha256` 等）与 `session_evidence` 块共存；若用 `session_evidence`，`executed_prompt_bytes` 必须是整数。
- 所有新 `.md` 必须有 `document_metadata`（含 `steward`、`domain`、`role`、`lifecycle`、`authority`）。
- `prompt-v1.md` 里我需要的字节数与 SHA-256 会在落盘后计算并回填，所以请把这两处写成占位符 `__PROMPT_BYTES__` 与 `__PROMPT_SHA256__`，并在需要正文引用的地方用 `__PROMPT_PAYLOAD__` 标记“此处插入实际投递内容摘要”。
- `session-evidence.md` 必须含 `## Session role`、`## Actual AI input`、`## AI-visible output` 三个二级标题（校验器硬性要求）。
- PR 正文必须含：`## Related issue(s)` + `#1350`；`## AI-assisted work` 且值为裸 `YES`；`Session evidence reference(s): 14-ai-development/work-items/AID-2026-336/session-evidence.md`；以及三列 per-Issue 表，表头含 `Related Issue` / `Issue AI-assisted work` / `Evidence refs for this Issue`，历史 Issue 行用 `LEGACY_UNDECLARED` 与 `N/A`。
- 不要声称 CI 通过、不要声称已合并、不要声称 Owner 验收。合并状态写 `NOT_MERGED`，验收写 `PENDING`。
- `pincount.md` 用你上一轮定的口径：manifest 可见声明 15、AID-336 in-scope 10、范围外 5、prompt 元数据 150 条（注意你上一轮更正为 150；本机实测 `excluded=163` 是 checker 的运行时计数，两者不要混用，请明确写清各自的定义）。

## 形状参考：AID-2026-331/manifest.yaml（全文 184 行）

```yaml
work_item_id: AID-2026-331
title: "Define and Migrate Historical Reference Semantics"
class: DOC
risk: R1
risk_rationale: >-
  Documentation-only work item recording two Owner rulings: Option C for
  authored-index and related-evidence references, and
  PROMPT-SNAPSHOT-REFERENCE-SEMANTICS-001 for executed prompt snapshots.
  This work item does not change executable behavior or rewrite digests.
status: PROPOSED
id_status: PROVISIONAL
sponsor: USER-PRINCIPAL-DELEGATED
accountable_owner: USER-PRINCIPAL-DELEGATED
acceptance_authority: NOT_ASSIGNED
attribution: "AI-assisted documentation prepared from two Owner rulings and supplied repository evidence"
date: "2026-11-27"
repository: oahcom/AiMemoryBrainArchitecture
base_branch: main
base_commit_sha: "b333ad1cf0e86992621d41cc1dac87eb3141353c"
tracking_issue: "#1350"

scope:
  summary: >-
    Define and document both Owner rulings. Under Option C, authored_indexes[]
    is a historical authorship reference and related_evidence[] requires an
    explicit per-entry historical/current reference_mode. Under
    PROMPT-SNAPSHOT-REFERENCE-SEMANTICS-001, executed prompt snapshot digest
    and byte count are point-in-time session evidence, not candidate-tree
    blob-pin assertions. Record the migration dispositions without rewriting
    any declared digest or byte count.
  in_scope:
    - "Define authored_indexes[] as historical authorship references verified at the exact declared path in reachable Git history."
    - "Define related_evidence[].reference_mode as required per entry, with only historical and current values."
    - "Define fail-closed behavior for missing, invalid, or unclassifiable related-evidence modes."
    - "Define mode-specific historical and candidate-current resolution."
    - "Define the three Option C diagnostic outcomes and preserve their distinct meanings."
    - "Record preservation of all six existing authored-index digests."
    - "Record preservation of all three existing related-evidence digests and the required historical mode migration."
    - "Define executed_prompt_snapshot_file digest and byte count as point-in-time session evidence under PROMPT-SNAPSHOT-REFERENCE-SEMANTICS-001."
    - "Record that the four AID-2026-101/-102 candidate-tree failures are false positives under the chosen point-in-time semantics."
    - "Record that snapshot verification must use the session's recorded commit or unambiguous entry history."
    - "Record missing execution-commit provenance as a separate defect when historical bytes cannot be resolved unambiguously."
    - "Record that Session Evidence check 11 remains the enforcing PR-head-tree validator for digest and byte count."
    - "Record that AID-2026-336 removes duplicate prompt-snapshot assertions from the blob-pin checker's candidate-tree comparison."
    - "Record the two rulings' non-acceptance and issue-status boundaries."
  files_out_of_scope:
    - "14-ai-development/work-items/AID-2026-100/manifest.yaml"
    - "14-ai-development/work-items/AID-2026-101/manifest.yaml"
    - "14-ai-development/work-items/AID-2026-102/manifest.yaml"
    - "scripts/ci/check_manifest_blob_pins.py"
    - "scripts/ci/test_check_manifest_blob_pins.py"
    - "scripts/governance/session_evidence/validate.py"
    - ".github/workflows/session-evidence.yml"
    - "14-ai-development/prompt-and-evidence-template.md"
  change_boundary: >-
    Documentation-only. This work item defines and records the two Owner
    decisions. It does not rewrite any digest or byte-count declaration,
    apply the manifest migrations, change a checker, validator, workflow,
    or template, or claim implementation, acceptance, or closure. The
    AID-2026-101/-102 execution-commit provenance assessment remains a
    migration/implementation evidence task.

evidence:
  - "Owner A (acct3) Option C ruling for authored_indexes[] and related_evidence[]."
  - "Owner ruling PROMPT-SNAPSHOT-REFERENCE-SEMANTICS-001 for AID-2026-101 and AID-2026-102."
  - "Six authored-index path/blob observations: declared digests, current digests, and same-path historical presence."
  - "Three related-evidence path/blob observations: declared digests, current digests, and same-path historical presence."
  - "The Owner requires preservation of all nine authored-index and related-evidence digests."
  - "AID-2026-101 and AID-2026-102 each have declared prompt snapshot byte count 4470 and current file byte count 4412."
  - "The two prompt snapshot digest and two byte-count candidate-tree findings are the four failures reclassified by the Owner as false positives."
  - "Complete verified SHA-256 values and execution commit identifiers for the two prompt snapshots are not established in the evidence available for this documentation draft."
  - "The Owner requires historical verification at the session-recorded commit or unambiguous entry history, with missing provenance reported separately."
  - "Session Evidence check 11 remains authoritative for PR-head-tree digest and byte-count enforcement."
  - "The Owner expressly requires removal of duplicate prompt-snapshot digest and byte-count assertions from the blob-pin checker's candidate-tree comparison."

documentation:
  - path: "14-ai-development/work-items/AID-2026-331/prompt-v1.md"
    relationship: reference
  - path: "14-ai-development/work-items/AID-2026-331/session-evidence.md"
    relationship: evidence
  - path: "14-ai-development/work-items/AID-2026-331/reference-semantics.md"
    relationship: normative
  - path: "14-ai-development/work-items/AID-2026-331/migration-table.md"
    relationship: evidence
  - path: "14-ai-development/work-items/INDEX.md"
    relationship: reference

dependency_refs:
  - "#1350"
  - "PROMPT-SNAPSHOT-REFERENCE-SEMANTICS-001"

independent_reviewer: NOT_ASSIGNED
integration_reviewer: NOT_ASSIGNED

prompt_id: AID-2026-331-PROMPT
prompt_version: "v1"

created_at: "2026-11-27"
updated_at: "2026-11-27"
implementation_branch: ""
implementation_commits: []
changed_paths:
  - "14-ai-development/work-items/AID-2026-331/manifest.yaml"
  - "14-ai-development/work-items/AID-2026-331/reference-semantics.md"
  - "14-ai-development/work-items/AID-2026-331/migration-table.md"
  - "14-ai-development/work-items/AID-2026-331/session-evidence.md"
  - "14-ai-development/work-items/AID-2026-331/prompt-v1.md"
  - "14-ai-development/work-items/INDEX.md"

verification:
  status: NOT_RUN
  commit_sha: ""
  commands:
    - "python scripts/ci/check_manifest_parse.py"
    - "python scripts/ci/check_work_item_manifest_schema.py"
    - "python scripts/ci/check_document_management.py --require-changed origin/main"
    - "python scripts/ci/check_repository_hygiene.py --base <base> --head <head>"
  evidence_refs: []

evidence_tiering:
  repository: "oahcom/AiMemoryBrainArchitecture"
  change_class: DOC_EDITORIAL
  review_level: R1
  evidence_level: "1"
  assessed_by: NOT_ASSIGNED
  assessed_at: ""
  rationale: >-
    Documentation-only codification of two explicit Owner rulings and the
    supplied declaration observations. No executable behavior or digest
    repair is included in this change boundary.
  base_head: "b333ad1cf0e86992621d41cc1dac87eb3141353c"
  classification_basis: "Documentation-only change boundary"
  classification_confirmed_by: NOT_ASSIGNED
  classification_record: ""
  downgrade_justification: ""
  downgrade_confirmed_by: ""
  downgrade_confirmation_record: ""
  escalation_target: ""
  checker_result: NOT_RUN
  declaration_path: "evidence-declaration.yaml"

review:
  status: NOT_STARTED
  report_ref: ""
  findings: []

implementation:
  status: NOT_STARTED
  summary: >-
    Documentation-only record of Option C and
    PROMPT-SNAPSHOT-REFERENCE-SEMANTICS-001. Preserve all nine authored-index
    and related-evidence digests. Preserve both prompt snapshot digest and
    byte-count declarations; classify their four candidate-tree findings as
    false positives under the point-in-time rule. Record the required
    historical provenance assessment for AID-2026-101/-102. AID-2026-336
    implements the checker changes, including removal of duplicate
    candidate-tree prompt snapshot assertions, while preserving Session
    Evidence check 11. No checker, validator, workflow, or template is
    changed by this work item. Prompt snapshot digest and byte count for
    this work item's own prompt remain substitution placeholders.
  files_changed:
    - "14-ai-development/work-items/AID-2026-331/manifest.yaml"
    - "14-ai-development/work-items/AID-2026-331/reference-semantics.md"
    - "14-ai-development/work-items/AID-2026-331/migration-table.md"
    - "14-ai-development/work-items/AID-2026-331/session-evidence.md"
    - "14-ai-development/work-items/AID-2026-331/prompt-v1.md"
    - "14-ai-development/work-items/INDEX.md"
  tests:
    - "python scripts/ci/check_manifest_parse.py"
    - "python scripts/ci/check_work_item_manifest_schema.py"
    - "python scripts/ci/check_document_management.py --require-changed origin/main"
    - "python scripts/ci/check_repository_hygiene.py --base <base> --head <head>"

session_evidence:
  - role: DOCUMENTATION
    issue_refs:
      - "#1350"
    implementing_ai_session: NOT_VERIFIED
    executed_prompt_snapshot_file: "14-ai-development/work-items/AID-2026-331/prompt-v1.md"
    executed_prompt_sha256: "de27a516afd6194e8fa0a48d2f5dff34768f3f2b379be3f8cb415cc640c08432"
    executed_prompt_bytes: 7747
    executed_prompt_provenance: NOT_VERIFIED
    session_reference_status: RECORDED
    session_evidence_ref: "14-ai-development/work-items/AID-2026-331/session-evidence.md"
```

## 形状参考：INDEX.md 表头与相邻行

表头（第 51 行）：

```markdown
| Work Item ID | Title | Owner | Class/Risk | Status | Prompt | Implementation | Review | Acceptance |
```

331 的行（第 52 行）：

```markdown
| [AID-2026-331](AID-2026-331/manifest.yaml) | Define and Migrate Historical Reference Semantics | USER-PRINCIPAL-DELEGATED | DOC / R1 | PROPOSED — records Option C and PROMPT-SNAPSHOT-REFERENCE-SEMANTICS-001; documentation-only contract and migration record | `AID-2026-331-PROMPT` v1 → `prompt-v1.md`; SHA-256 `de27a516afd6194e8fa0a48d2f5dff34768f3f2b379be3f8cb415cc640c08432`, `7747` bytes; structured snapshot, provenance `NOT_VERIFIED` | Normative reference-semantics contract; eleven-occurrence migration table; session evidence; no digest or byte-count rewrite and no executable files changed | NOT_ASSIGNED — no independent exact-Head review recorded | NOT_RECORDED — no disposition recorded |
```


## Required implementation contract

Implement AID-2026-336 against the rebased `origin/main` baseline.

Preserve the AID-2026-296 `blob_sha256` scan. Do not replace the rebased checker
with a version that drops its G段 behavior, including:

- discovery of `blob_sha256` and qualified `*_blob_sha256` declarations;
- path binding within the containing mapping;
- JSON Pointer reporting;
- `UNBOUND_BLOB_SHA256` findings;
- `unbound=` summary accounting;
- SHA-256 comparison against committed file bytes.

Implement the AID-2026-331 reference semantics:

1. `authored_indexes[]` references are historical references checked at the
   exact declared path in reachable Git history.
2. `related_evidence[]` requires `reference_mode` on each declaration record.
3. The only valid modes are `historical` and `current`.
4. A missing or invalid mode is a policy violation, reported as
   `REFERENCE_MODE_MISSING_OR_INVALID`, with
   `classification="policy"` and exit status 1.
5. Historical references are checked against reachable history at the exact
   path.
6. Current references are checked against the candidate commit tree.
7. Preserve distinct diagnostic outcomes for historical misses, current
   mismatches, and invalid/missing reference modes.
8. Preserve exit status 2 for genuinely incomplete or unreadable scan inputs.

Keep the documented in-scope pin count separate from prompt metadata and
explicitly out-of-scope declaration families. Non-empty `blob_sha256`
declarations are in-scope pins.

Update the fixed negative fixture assertion to the new semantics. Do not
preserve obsolete pin counts by adding fixture-specific compatibility behavior.

Update the repository-hygiene ratchet filter to capture:

- `HISTORICAL_REFERENCE_NOT_FOUND`
- `CURRENT_REFERENCE_MISMATCH`
- `REFERENCE_MODE_MISSING_OR_INVALID`

Migrate `AID-2026-100/manifest.yaml` by adding
`reference_mode: historical` to `related_evidence[0]`. Do not rewrite its
existing digest.

## Verification requirements

Run and record the relevant local commands:

- `python scripts/ci/check_manifest_blob_pins.py --commit HEAD`
- `python scripts/ci/test_check_manifest_blob_pins.py`
- `python scripts/ci/test_assert_manifest_blob_pin_negative.py`
- `python -m unittest scripts/ci/test_resolve_manifest_blob_pin_base.py scripts/ci/test_assert_manifest_blob_pin_negative.py`
- `python scripts/ci/assert_manifest_blob_pin_negative.py --commit 9a2063ae1fa5d905b3817cd4eddba065a06daa73`
- `python scripts/ci/check_manifest_parse.py`
- `python scripts/ci/check_work_item_manifest_schema.py --tree HEAD --baseline 14-ai-development/reports/work-item-manifest-ac4-baseline.json`

Do not claim remote CI success, merge, independent review, or Owner acceptance
unless separately established by evidence.

## Required output boundary

The implementation is not considered merged or accepted merely because local
tests pass.

Record:

- implementation commit;
- changed files;
- local command results;
- negative fixture results;
- remaining review, merge, and acceptance status.

Use:

- Merge: `NOT_MERGED`
- Acceptance: `PENDING`
