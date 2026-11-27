---
document_metadata:
  domain: ai-development
  role: work-record

  lifecycle:
    approval:
      decision_status: Draft
      approver: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-24"
      last_verification_note: "Both missing paths were measured with git cat-file -e origin/main:<path> at 1259f1af. The degraded output was produced by copying the merged script into an empty directory and running it there, with no registry and no git repository; the exact strings and the exit code 2 are that run's output. The four-error result was measured on a clean tree at the same commit. The #926 diff was read from git diff 882ed439..2914c32f, and its commit message was compared against the measured behaviour rather than accepted as a description of it. No figure is inferred."
    usage_status: Active
    modification_status: Unchanged

  authority:
    canonical_status: Non-Canonical
    canonical_conflict_status: None
    normative_status: Informative

  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# AID-2026-058 — the traceability checker is in the repository and its inputs are not

**Work item:** `AID-2026-058`
**Class / risk:** `GATE/CODE/TEST` / `R1`
**Status:** `DISPATCHED`
**Measured at:** `main = 1259f1af`

---

## 1. Why this exists

`#899` was merged as `a23e6cc0`, which put `scripts/check_traceability.py` and its test suite into the repository. The script reads two paths that were never committed:

```
00-governance/requirements-registry.yaml      git cat-file -e origin/main:... -> NOT FOUND
scripts/ci/baselines/traceability.txt         git cat-file -e origin/main:... -> NOT FOUND
```

Measured at `1259f1af`, in a directory containing only the current script:

```
$ python t.py
WARN cannot complete traceability check: cannot read registry: [Errno 2] No such file or directory: '.../00-governance/requirements-registry.yaml'
INCOMPLETE TRACEABILITY: 0 requirements / 0 work items / 0 errors / 1 warnings
$ echo $?
2
```

`#926` (merged as `1259f1af`) already changed part of this: a missing registry now counts as a warning plus `indeterminate`, so the summary says `INCOMPLETE` rather than `FAIL`, and the exit code is 2 rather than 1. That is an improvement — the word and the code agree. It is not what OD-23 asked for.

OD-23 ruled:

> 脚本在必需注册表缺失或不可读取时必须返回非零状态（当前约定的 `exit 2`），并且**不得输出看似完整判决的 `PASS`、`FAIL` 或 `INCOMPLETE TRACEABILITY: 0 requirements / 0 work items / 0 errors` 一类摘要**。可以输出明确标识为诊断的错误信息，但不能让空输入伪装成一次有效检查。

The measured output still prints `INCOMPLETE TRACEABILITY: 0 requirements / 0 work items / 0 errors / 1 warnings` — the exact string the ruling names as forbidden. `0 requirements / 0 work items` describes inputs that were never read.

## 2. Why this is worse than when #899 was open

While `#899` was open, the script was not in the repository. Nobody could mistake its absence for a passing run, because there was nothing to run.

Now the script is on `main`. `git ls-files` finds it. A CI job wired to it would produce a verdict-shaped line on every commit — currently `INCOMPLETE`, which a reader can at least tell apart from `PASS`, but which still reads as a statement about the tree rather than about the tool's own input.

## 3. What to change

Two independent changes. Either alone is insufficient.

**(A) Commit the two input files.** `00-governance/requirements-registry.yaml` and `scripts/ci/baselines/traceability.txt`, as they exist in the working tree and as the merged script reads them (`REGISTRY_PATH` at line 26, `json.loads` at line 108 — the file is named `.yaml` and contains JSON, pre-existing, see §5).

**(B) Stop printing a verdict over unread inputs.** When `REGISTRY_PATH` is absent or unreadable, the process must exit non-zero **and** the summary line must not contain the count of requirements or work items, because those counts were not measured. A diagnostic naming the missing path and stating that no check was performed is the correct output. `#926` established the distinction between "error" and "indeterminate"; this change establishes the distinction between "indeterminate verdict" and "no verdict".

Order matters. (B) first, then (A): if (A) lands first and the registry is later deleted or a path changes, the same misleading line returns. (B) is what makes (A) durable.

## 4. Acceptance criteria

- **AC1** — On a clean checkout of the merged result, `python scripts/check_traceability.py` exits 1 with `4 errors` and the four errors are exactly `AID-2026-023`, `AID-2026-024`, `AID-2026-025`, `AID-2026-026` not appearing in `INDEX.md`. Asserted by path, not by count alone.
- **AC2** — With `REGISTRY_PATH` temporarily renamed, the process exits non-zero and its combined output contains **no** occurrence of any of: `PASS`, `FAIL`, `INCOMPLETE`, `0 requirements`, `0 work items`, `0 errors`. Asserted by grepping the captured output for the literal list, not by reading it.
- **AC3** — `gate_ratchet.py --baseline scripts/ci/baselines/traceability.txt --format paths --command "python scripts/check_traceability.py"` exits 0 with `regressions=0 fixed=0` on the merged result.
- **AC4** — The four baseline entries are the four AC1 paths, byte-identical. `fixed=0` means the baseline was not refreshed to match a changed result.
- **AC5** — The existing suite in `scripts/test_check_traceability.py` passes unmodified except where AC2 requires a new case. `#926` added tests for the error/indeterminate split; those must keep passing, since (B) is a further step in the same direction, not a reversal of it.
- **AC6** — The exit code is in `{1, 2}`, not `0`, in the AC2 condition. Either is acceptable; `0` is not, and the choice must be stated in the PR body rather than left to be inferred.

## 5. What not to change

- **Do not refresh the baseline to hide the four errors.** They are the check working: four work items are registered and not indexed. Fixing those is a different change with a different owner.
- **Do not rename the registry to `.json`.** The path is referenced in `REGISTRY_PATH` and in the file's own header comments; renaming touches more than it fixes. Record the mismatch as a finding.
- **Do not reverse `#926`.** Its change (a missing registry is a repository defect, reported as such) stands. This work item removes the verdict line, not the classification.
- **Do not add the inputs without (B).** See §3's ordering paragraph.

## 6. Authorisation

This work item is registered only. No file has been committed by the session that wrote this manifest.

- `implementation_write`: `NOT_GRANTED` — the two files to be committed and the one script to be edited are named above, but committing them requires an implementing session.
- `gate_behaviour_change`: `DECIDED by OD-23, PARTIALLY IMPLEMENTED by #926` — (B) is the remaining part, and it alters what the script prints.
- `baseline_content_change`: `NOT_GRANTED` — AC4 asserts the baseline is unchanged.
- `root_membership_change`: `NOT_APPLICABLE`.

## 7. Why the ruling did not just fix it

OD-23 chose "(c) both" and added the boundary: *"OD-23 的两个缺失文件和脚本缺失输入时的行为，也必须有正式工作项承接，不能仅凭本轮裁定直接修改仓库。"*

So the decision exists and the implementation does not. That is the state this manifest records.

## 8. Provenance

Both paths were measured absent with `git cat-file -e origin/main:<path>` at `1259f1af`. The degraded output was produced by copying the merged script into an empty directory and running it there — no registry, no git repository. The four-error result was measured on a clean tree at the same commit. The `#926` diff was read from `git diff 882ed439..2914c32f`. No figure is inferred.

**Note on numbering.** This work item was first written as `AID-2026-057`, which a concurrent session claimed for an unrelated work item (classifying paths the admission gate refuses) between the write and the merge. Renumbered rather than contested: the issuing session had no claim on the number, and two manifests under one ID is the hazard, not the fix.
