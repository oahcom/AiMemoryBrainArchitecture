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
        - "14-ai-development/work-items/AID-2026-188/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-26"
      last_verification_note: "Records the request as received, the environment it ran in, and the commands whose output is quoted in evidence.md. No platform session identifier is available, so the session identity is recorded as NOT_RECORDED rather than inferred."
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

# Session Evidence — AID-2026-188

## 1. What was asked

A dispatched worker contract asked for `"03-memory-brain"` to be added to `NORMATIVE_ROOTS`, for a possible second root list to be synchronised, for both frozen baselines to be left untouched, for the bilingual gate and the AID-2026-172 unit tests to stay green, for the three canonical documents to be registered in `00-governance/document-scope-registry.yaml`, and for a work item plus one `INDEX.md` row to be created and shipped as a pull request.

The contract was received as text by this session; the full text is pinned verbatim in `prompt-v1.md` (5934 bytes, SHA-256 `e0741732d3bd920e93729ecbd088cccc9bed2145c0e679891733f0aa804df9d2`). No prompt-library registration exists for it, so `prompt_status` is `NOT_RECORDED`.

## 2. What was actually found before any edit

The first three items of the contract describe a change that was already present at the stated base. Instead of making the edit, the session measured the state and stopped:

- `NORMATIVE_ROOTS` holds 13 entries and contains `03-memory-brain` (`scripts/check_bilingual_docs.py:20`), attributed by `git blame` to `6ab36b3697a0994d8de449d2b9c344f23aac0fda`.
- `current_bilingual_gaps()` = 77, both baselines = 77, `new = 0`, `gone = 0`, `check_baseline_copies_agree()` = `[]`.
- `03-memory-brain/` holds 3 canonical documents; `docs/en/03-memory-brain/` and `docs/zh-CN/03-memory-brain/` hold 13 mirrors each.
- `check_document_management.py` reports `03-memory-brain: 3/3 classified`, so the three documents are governed and metadata-complete.
- `check_bilingual_docs_full.py` imports the constant and asserts equality with a tree-derived set; it holds no second literal.
- `00-governance/document-scope-registry.yaml` declares `03-memory-brain` as a governed root at line 50 and has no `documents:` key at all.

The measurement is recorded in `evidence.md` section 2 as a premise-versus-state table, and section 6 lists the edits refused with the reason for each.

## 3. What this session changed

Six files created, one row appended:

```
14-ai-development/work-items/AID-2026-188/manifest.yaml
14-ai-development/work-items/AID-2026-188/evidence.md
14-ai-development/work-items/AID-2026-188/prompt-v1.md
14-ai-development/work-items/AID-2026-188/session-evidence.md
docs/en/14-ai-development/work-items/AID-2026-188/evidence.md
docs/zh-CN/14-ai-development/work-items/AID-2026-188/evidence.md
14-ai-development/work-items/INDEX.md        (one appended row)
```

No file under `scripts/`, `00-governance/`, `.github/`, `03-memory-brain/` or `docs/*/03-memory-brain/` was modified. `git diff --stat` against `origin/main` is the check that this stayed true.

## 4. Environment

- Host: Windows, PowerShell console codepage GBK.
- `PYTHONUTF8=1` was set for every command. Without it, captured `git` and `python` output fails to decode non-ASCII paths and the gate reports a decoding failure unrelated to the tree. This is a locale artefact of the host, recorded in `evidence.md` section 8 and not fixed here.
- Working tree: `D:\code\wt-norm03`, branch `docs/2026-11-26-normative-root-03`, which was 17 commits behind `origin/main` at the start. `origin/main` was merged with `--no-ff` before any work, so every measurement above is against `1e9341da603dec78377fed240f4d6dbabaa8838e`.
- The branch was clean at the start (`git status --short` empty), so nothing of another session's work was touched.

## 5. Commands whose output is quoted

```
git fetch origin main ; git status --short
git rev-list --left-right --count origin/main...HEAD
git merge --no-ff origin/main
git blame -L 19,24 --porcelain scripts/check_bilingual_docs.py
python -c "<import gate module; print root count, membership, gap count, baseline count, new, gone, copy agreement>"
python scripts/check_bilingual_docs_full.py
python scripts/check_document_management.py
python -m unittest discover -s scripts -p "test_check_bilingual*"
python -m unittest discover -s tests -p "test_check_bilingual*"
```

The one-line `python -c` form is reproduced in `evidence.md` section 9 so the 13 / True / 77 / 77 / 0 / 0 / `[]` tuple can be regenerated rather than trusted.

## 6. What is not evidenced

- No CI context result at any SHA. The pull-request carrier is not yet known when this file is written.
- No merge SHA, no post-merge blob digest, no review approval, no Owner acceptance.
- No platform session identifier: `session_reference_status` is `NOT_RECORDED` and `implementing_ai_session` names the model that executed the contract, not an authenticated account.
- The prompt snapshot is a verbatim capture of received text with provenance `NOT_VERIFIED`; it is not a signed artefact from the dispatching system.
