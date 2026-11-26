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
        - "14-ai-development/work-items/AID-2026-198/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Session role, the dispatched input and the produced output for AID-2026-198; no independent review and no CI result are claimed."
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
# Session Evidence — AID-2026-198

## Session role / use case

Dispatched implementation session for AID-2026-198: make every gate that reads Git output decode that output as UTF-8 instead of with the console's locale codec, and make an undecodable read fail closed as INCOMPLETE instead of turning into a content assertion such as "the file did not exist at approved_version" (DM-10) or a crash (`check_bilingual_docs.py`, hit by the AID-173 worker).

## Actual AI input

The dispatched task text, captured verbatim as `14-ai-development/work-items/AID-2026-198/prompt-v1.md`: read the unit brief, work only inside the assigned worktree `D:\code\wt-locale` on branch `fix/2026-11-27-git-decode-locale`, grep the whole repository for `text=True` / `subprocess.run` / `subprocess.check_output`, give every read of Git output an explicit UTF-8 encoding, make a decode failure report "decode" and exit 2 rather than asserting absence, add a test built from non-UTF-8 bytes, and record the before/after exit codes measured on a GBK console without `PYTHONUTF8`.

The operator also supplied the two reproducing call sites (`check_document_management.py:1189-1206` and `:1290-1296`), the AID-173 `git show` crash, the measured fact that the nine DM-10 "did not exist" claims correspond to nine files that `git cat-file -e` says exist, and the prohibition on changing any gate's pass condition.

## AI-visible output

- `scripts/check_bilingual_docs.py`: added `GIT_TEXT_ENCODING`, `GitOutputDecodeError` and `decode_git_output()`; `_git_log_output()` now decodes strictly; the six remaining Git reads take `encoding="utf-8", errors="replace"`; `main()` turns a decode failure from registration-history verification into `::error::` plus exit 2.
- `scripts/check_document_management.py`: `git()` captures bytes and decodes strictly, so a decode failure raises instead of returning `None`; DM-10 reports it through the existing `unanswerable` channel (exit 2), and when `git show` yields `None`/empty output it asks `git cat-file -s` whether the object exists, so a genuine absence keeps its message and an unreadable blob does not borrow it.
- `scripts/check_bilingual_docs_full.py`: an undecodable `git ls-files -z` stream prints `git output decode failed` and exits 2.
- Seven further gate scripts that read Git output (fmt, policy inheritance, source-revision pointers, traceability, branch freshness, evidence tiering, the bilingual tiering shell gate) now pass `encoding="utf-8", errors="replace"`.
- `scripts/governance/status_migration/check_status_gates.py` is a sidecar-anchored protected file; its Git reads were re-encoded and the sidecar was regenerated through the anchor mechanism that file documents, with the new sidecar SHA-256 in the commit message.
- Tests: `T95a`/`T95b` in `test_check_document_management.py` (undecodable pin → exit 2 naming "decode", and the counterfactual real absence → exit 1 naming "did not exist"), two cases in `test_check_bilingual_docs.py` (undecodable blob names the decode failure; `main()` reports it as INCOMPLETE), plus UTF-8 decoding in the fixture Git helpers of the affected self-checks.
- `14-ai-development/work-items/AID-2026-198/`: manifest, this session record, the captured task text, and `evidence.md` (Canonical), plus the EN and ZH-CN mirrors and the INDEX row.

The pull request itself is the CI record: this session does not restate CI results it did not observe.
