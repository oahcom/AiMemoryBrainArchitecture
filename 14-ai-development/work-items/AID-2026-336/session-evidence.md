---
document_metadata:
  steward: "user-authorized operator (delegated by account owner)"
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
        - "14-ai-development/work-items/AID-2026-336/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-28"
      last_verification_note: "Records supplied session evidence; executing session identity is not asserted."
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
    canonical_scope: "Session evidence for AID-2026-336"
    canonical_scope_id: "ai-development/aid-2026-336-session-evidence"
    canonical_scope_keywords:
      - "manifest blob pin"
      - "session evidence"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# AID-2026-336 Session Evidence

## Session role

This session produced the AID-2026-336 implementation record set from the
implementation facts and measured command results supplied for branch
`aid-2026-336`.

The implementation work was performed in the user's worktree:

```text
D:\code\_wt-aid336
```

The recorded implementation commit is:

```text
6f75baceae2242e665e62b234d816df8eca86f32
```

Its supplied parent commit is:

```text
c72ba09685eff8f4e00cbf05182dcfdf5d1815a4
```

This evidence document records the role and supplied evidence boundary. It
does not independently attest to the identity of the implementing AI session,
and it does not claim independent review or Owner acceptance.

## Actual AI input

The implementation task was to integrate AID-2026-336 after rebasing onto
`origin/main`, preserving the already-merged `blob_sha256` behavior while
implementing the AID-2026-331 reference semantics.

The required implementation decisions included:

1. `authored_indexes[]` declarations are historical references checked at the
   exact declared path in reachable Git history.
2. Every `related_evidence[]` declaration requires an explicit
   `reference_mode` of `historical` or `current`.
3. A missing or invalid `reference_mode` is a policy violation:
   `REFERENCE_MODE_MISSING_OR_INVALID`, with `classification="policy"` and
   violation exit status 1.
4. Historical and current references retain distinct resolution semantics and
   distinct diagnostic codes.
5. `blob_sha256` and qualified `*_blob_sha256` declarations remain in scope,
   are counted as pins when non-empty, and retain path binding, JSON Pointer
   diagnostics, `UNBOUND_BLOB_SHA256`, and `unbound=` summary accounting.
6. The negative fixture assertion must be updated to the new pin-count and
   diagnostic contract rather than retaining an obsolete count.
7. The repository-hygiene ratchet must include all three new semantic
   diagnostic prefixes.
8. The AID-2026-100 related-evidence migration must add the required mode
   without changing the existing digest.
9. The implementation record must not claim remote CI success, merge, or
   Owner acceptance without evidence.

### Prompt payload reference

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


## AI-visible output
The payload above is preserved verbatim as the executed input. It records the pre-rebase
commit `d8512eee5`, which the rebase onto `c72ba09685eff8f4e00cbf05182dcfdf5d1815a4` rewrote to `6f75baceae2242e665e62b234d816df8eca86f32`. The
measured results below were re-run at the rebased implementation commit.


The implementation evidence supplied for this record reports:

- Branch `aid-2026-336`, rebased onto the supplied `origin/main` state.
- Implementation commit `6f75baceae2242e665e62b234d816df8eca86f32`, parent `c72ba09685eff8f4e00cbf05182dcfdf5d1815a4`.
- Seven changed implementation, test, baseline, workflow, and migration files.
- Checker result at `HEAD`:
  `main=6f75baceae2242e665e62b234d816df8eca86f32 manifests=165 pins=12 ok=12 mismatch=0 path_missing=0 incomplete=0 excluded=166 unbound=0`,
  rc 0.
- Checker test suite: 35 tests passed.
- Negative assertion test suite: 7 tests passed.
- Combined base-resolver and negative-assertion tests: 15 tests passed.
- Fixed negative fixture assertion: `NEGATIVE_ASSERTION_PASS`, with
  `manifests=108 pins=14 ok=7 mismatch=1 path_missing=0 incomplete=0 excluded=146 unbound=4`.
- The negative fixture emitted four `UNBOUND_BLOB_SHA256` findings and one
  `REFERENCE_MODE_MISSING_OR_INVALID` finding, with zero
  `MISMATCH `, `PATH_MISSING `, or `INCOMPLETE ` findings.
- Manifest parse validation: 165/165 passed at the implementation commit.
- Work-item schema validation: rc 0 and zero legacy-ratchet new regressions.
- AID-2026-100 after migration: `pins=10 ok=10`, with its existing digest
  unchanged.

The command results are recorded as local implementation-worktree evidence.
They are not represented as remote CI results.

### Status boundary

| Dimension | Recorded status |
|---|---|
| Implementation | `IMPLEMENTED` |
| Independent review | `NOT_STARTED` |
| Merge | `NOT_MERGED` |
| Owner acceptance | `PENDING` |
