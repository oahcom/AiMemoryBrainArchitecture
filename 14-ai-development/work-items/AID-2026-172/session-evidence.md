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
        - "14-ai-development/work-items/AID-2026-172/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-26"
      last_verification_note: "Session role, the dispatched input and the produced output for AID-2026-172; no independent review is claimed."
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
# Session Evidence — AID-2026-172

## Session role / use case

Dispatched implementation session for AID-2026-172: add the missing consistency check between the two frozen bilingual baselines inside the existing GOV-DOC-001 structural gate, and turn the shrink-only header comment in `write_baseline()` into an enforced assertion.

## Actual AI input

The dispatched task text, captured verbatim as `14-ai-development/work-items/AID-2026-172/prompt-v1.md`:

- Read `worker-contract.md` and follow it: work only inside the assigned AID-2026-172 number range, branch from `origin/main`, no squash, no rebase, no force push, do not touch either baseline's contents, do not regenerate a baseline, do not change `current_bilingual_gaps()`.
- Add a minimal check comparing the entry sets of `scripts/bilingual-baseline.txt` and `scripts/ci/baselines/bilingual-docs.txt`, printing both difference directions as `::error::` and exiting non-zero on drift, wired through the existing CI entry point without adding a required context.
- Make `write_baseline()` refuse a product that is not a subset of the previous set, printing the added entries.
- Add unit tests in the existing `test_check_*.py` style, three evidence documents, one INDEX row, then open the pull request, wait for the 16 required contexts, merge atomically and verify blobs.

The operator also supplied the two file paths, the 77-entry count, the comment line in `check_bilingual_docs.py` that the assertion replaces, and the instruction to report in the worker-contract §7 shape.

## AI-visible output

- `scripts/check_bilingual_docs.py`: added `CI_BASELINE_PATH`, `read_baseline_entries()`, `check_baseline_copies_agree()`; `main()` prints both drift directions and returns 2; `write_baseline()` reads the previous set and refuses added entries or a missing previous baseline before creating any temporary file.
- `scripts/test_check_bilingual_docs.py`: `run_gate()` now writes the ratchet copy and can inject drift; eight new tests cover identical copies, both drift directions, comment handling, a missing ratchet copy, refusal on additions, a shrinking rewrite, and a missing previous baseline.
- `14-ai-development/work-items/AID-2026-172/`: manifest, this session record, the captured task text, and `evidence.md` (Canonical), plus the EN and ZH-CN mirrors and the INDEX row.
- Local verification: `test_check_bilingual_docs.py` 15 tests OK; the structural gate reports 77 frozen, 0 new gaps; the ratchet reports baseline=77 current=77; GOV-DOC-002, repository hygiene, traceability, fmt, line endings, test reachability and the session-evidence workflow shape all pass locally.

The pull request itself is the CI record: this session does not restate CI results it did not observe.
