---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: content-hash
        value: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-26"
      last_verification_note: "Exact source pins and issue records are listed below. Acceptance is not asserted; unavailable evidence is explicitly marked BLOCKED."
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
    canonical_status: Non-Canonical
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# Issue #1037 — GOV-DOC-002 execution and metadata evidence

**Fix commit:** `cb4b36d055596d4c5c673615aa6e1ecd96436e95`  
**PR #1221 merge commit:** `dc826e4eae381d78a9fc4b1fcbb2cbc783ed2706`  
**Current main at this audit:** `515b7144320fd9fcc1e1a2c3d2d2744d979b4ca8`

## 1. Exact-Head checker execution actually observed

GitHub Actions run: [45765896655 — Architecture document management gate](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/45765896655)  
Job: `GOV-DOC-002 metadata checks`, job ID `139726593864`.  
Run Head: `cb4b36d055596d4c5c673615aa6e1ecd96436e95`.  
Job state: completed / success.

The job log records the invocation:

```sh
python3 scripts/check_document_management.py --require-changed c6b7d987b959c42af5072932963dae9ed55721e4
```

The workflow selected `PR_BASE=c6b7d987b959c42af5072932963dae9ed55721e4`. The command's numeric exit code is not printed separately in the log; the step completed successfully, the job conclusion is `success`, and the checker printed `PASS (incremental)`. Therefore the observed result is **exit 0 by successful-step inference**, not a separately emitted shell `echo $?`.

## 2. Captured checker output summary and hash

The following six selected summary lines are copied verbatim from the job log (they are selected lines, not the complete stdout):

```text
GOV-DOC-002: 762 governed documents, 293 classified, 469 unclassified
DM-10 out-of-scope stale bindings: 0
##[notice]advisory (non-blocking): 117 governed document(s) carry a body '- Status:' line and no front-matter equivalent; DM-02 cannot see them (issue #481)
  02-domain-model: 1/12 classified
  04-memory-compiler: 3/5 classified
PASS (incremental): no GOV-DOC-002 violations; 293 classified, 469 unclassified
```

Selected-output object hash: Git blob SHA-1 `73ebf7144ee7458a08bde5d36a3a9bef42e54324`, calculated over exactly the six UTF-8 lines above including the trailing LF. This is a Git blob SHA-1, not a SHA-256 digest of the entire runner log.

The incremental verdict means files outside the changed set were not required to be classified. It is not a whole-tree classification PASS.

## 3. Validator/source immutability readback

The existing checker and its key inputs were read at pre-fix commit `9e54e6ccec0d07d11fcf36b2a85b888ded747cdc` and fix Head `cb4b36d055596d4c5c673615aa6e1ecd96436e95`:

| Path | Blob SHA-1 at both refs | Result |
|---|---|---|
| `scripts/check_document_management.py` | `5972973829e46297a860b0fecc1324730e5b9505` | identical |
| `scripts/check_bilingual_docs.py` | `cb68c8850459ab8e57758d32e4195cc2bf7e6849` | identical |
| `00-governance/architecture-document-metadata.schema.yaml` | `5f147b0e71bed8f9943a593c75037c80a8c4272b` | identical |
| `00-governance/document-scope-registry.yaml` | `2a570584f3b4810f62f021dc3aed6dadf39c368e` | identical |

This proves those source/input blobs were unchanged. It does **not** prove that the checker stdout was byte-identical.

## 4. Byte-for-byte output comparison

**BLOCKED.**

No raw baseline stdout from the pre-fix commit on an identical repository tree and identical invocation was available in this execution environment. The exact-Head final run above is real, but source-blob identity alone is not an output-equivalence proof. An older run from a different base/tree is not a valid substitute because the governed-tree counts differ.

Minimum completion path:
1. Provide a full-history checkout or authorized ephemeral CI runner that can check out both the pre-fix baseline and exact fix commit.
2. Run the same checker command with the same arguments and environment on both snapshots, save stdout/stderr and numeric exit code separately, and compute SHA-256 for each raw stdout file.
3. Compare raw bytes and attach both files plus the comparison result. Do not normalize timestamps or whitespace before the byte-equality test.

## 5. Fresh metadata recount

**BLOCKED.**

A fresh exact-fix-commit census of `modification_status: Pending-Reapproval` and its `normative_status` split was not executable in the available repository environment. The local container has no repository checkout and cannot resolve GitHub network access; the prior workflow log is an incremental GOV-DOC-002 check and does not emit this census. No remote VM/worktree execution was used.

Historical context only: Issue #1037 comment #7151819257 recorded 11 Pending-Reapproval files, 8 Normative and 3 Informative at `2570ba0c96`; it also corrected that the three Informative files are one underlying governance-register record in root/EN/ZH-CN mirrors. That is not a fresh count at the fix commit and is not reused as one.

Minimum completion path: run a read-only frontmatter census at exact commit `cb4b36d055596d4c5c673615aa6e1ecd96436e95` in a full repository checkout; attach the complete path list, each file's `modification_status` and `normative_status`, totals, command, exit code and SHA-256 of the raw output.

**Result:** the exact-Head incremental GOV-DOC-002 checker run succeeded, and validator/schema blobs are unchanged. Byte-for-byte output equivalence and the fresh metadata recount remain BLOCKED. #1037 remains OPEN.
