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
        - "14-ai-development/work-items/AID-2026-296/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-28"
      last_verification_note: "Local execution recorded; CI verification and independent review are pending."
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
    canonical_scope_keywords:
      - "manifest-blob-pins"
      - "unbound-blob-sha256"
      - "fail-closed"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---
# Session Evidence — AID-2026-296

## Session role / use case

Implementation session for Issue #1350, dispatched by an owner-proxy session to
close the exclusion that PR #1417 comment 7212343821 rejected: a
`blob_sha256` declaration with no bindable path is a violation, not an
out-of-scope field.

## Actual AI input

The dispatched task supplied the adjudication text and the six absorption rules
for #1426, plus the preconditions to verify rather than assume: the checker and
its workflow wiring already exist on `main`, and #1426 is an open improvement PR
owned by another session that must not be touched or waited on.

The task also fixed the evidence requirements: before/after output for a
path-less `blob_sha256` on the unmodified checker, the four positive/negative
tests, the whole-suite result, a full run over main with the new violation count
and its distribution, and an explicit prohibition on baselining the new findings
to keep the gate green.

## AI-visible output

Origin was fetched and `origin/main` resolved to
`a0500d5196dc990d899d8ccaca2e270faaf29efc`. An isolated worktree was created at
`D:\code\_aimb\wt-unbound` on `fix/2026-11-28-unbound-blob-pin`; the primary
worktree was not modified.

The checker gained a document-wide walk for `blob_sha256` / `*_blob_sha256`
keys. A path is bound from the same mapping only (`<base>_path`, `<base>_file`,
a bare `<base>` value that reads as a path, then `path`/`file`). Bound digests
are verified as SHA-256 over committed bytes and report `MISMATCH` or
`PATH_MISSING`; an unbound digest reports `UNBOUND_BLOB_SHA256` with the manifest
path, JSON pointer, field name and digest value, and forces exit 1. The summary
line gained `unbound=N` at the end, so every pre-existing assertion on the
earlier prefix still holds.

Local execution (Windows PowerShell, `python`, no WSL):

```
python test_check_manifest_blob_pins.py
Ran 17 tests in 23.525s
OK
```

The whole of main at a0500d519:

```
pins=238 -> 242   unbound=0 -> 4   ok=223   mismatch=13   path_missing=2   incomplete=0
```

All four new findings are `AID-2026-001/dev_baseline_integration/measurement_basis`:
`model_blob_sha256_lf`, `model_blob_sha256_crlf`, `tests_blob_sha256_lf`,
`tests_blob_sha256_crlf`.

The ratchet, with `UNBOUND_BLOB_SHA256` added to the existing sed filter and the
baseline left byte-unchanged:

```
ratchet: baseline=15 current=19 regressions=4 fixed=0
ratchet: FAIL - 4 new failure(s) above baseline.
```

Main later advanced to `b333ad1c`, which added
`scripts/ci/assert_manifest_blob_pin_negative.py` — an exact-equality assertion
over the immutable negative sample `9a2063ae`. That sample carries the same four
unbound declarations, so its pinned summary was moved to `pins=172 … unbound=4`
with `EXPECTED_UNBOUND = 4`, tightening the count instead of relaxing it. On the
merged head the ratchet reads `baseline=4 current=8 regressions=4`.

## Boundary

No force push, no rebase, no merge, no edit to the primary worktree, no edit to
PR #1426 or its branch, and no change to
`scripts/ci/baselines/manifest-blob-pins.txt`. The red hard gate is reported as
a newly discovered real violation. No Owner acceptance, CI success or merge is
asserted by this document.
