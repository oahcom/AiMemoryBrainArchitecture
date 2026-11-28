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
# AID-2026-296 — Evidence

**Attribution:** user-authorized operator (delegated by account owner)
**Date:** 2026-11-28
**Issue:** #1350
**Implementation base observed:** a0500d5196dc990d899d8ccaca2e270faaf29efc

## Ruling this change implements

`blob_sha256` or `*_blob_sha256` declarations that have no bindable path are
`VIOLATION`, and must not be excluded from the check scope. The basis is PR
#1417 comment 7212343821, verbatim:

> Please close this draft as superseded by #1426. Port malformed-array
> fail-closed handling only; the proposal to classify unbound blob_sha256 as out
> of scope is rejected.

That comment supersedes the p71 §6 exclusion of path-less fields. The ruling
also forbids absorbing the affected fields into the existing ratchet baseline.

## Before (origin/main a0500d519, unmodified checker)

A fixture manifest whose only pin is a path-less digest:

```
work_item_id: AID-2026-900
artifact_pins:
  model_blob_sha256: 8324ec551749c2d50067967e4a445b26a6683008a4fa52e02da02a9976417a15
```

```
main=a088000ce2489da06a9e09989850836c06e20c06 manifests=1 pins=0 ok=0 mismatch=0 path_missing=0 incomplete=0
EXIT=0
```

`pins=0` and exit 0: the declaration was invisible to the checker. The whole of
main produced the same silence for the four real occurrences:

```
main=a0500d5196dc990d899d8ccaca2e270faaf29efc manifests=140 pins=238 ok=223 mismatch=13 path_missing=2 incomplete=0
```

## After

The same fixture:

```
main=a088000ce2489da06a9e09989850836c06e20c06 manifests=1 pins=1 ok=0 mismatch=0 path_missing=0 incomplete=0 unbound=1
UNBOUND_BLOB_SHA256 manifest=14-ai-development/work-items/AID-2026-900/manifest.yaml pointer=/artifact_pins/model_blob_sha256 field=model_blob_sha256 declared=8324ec551749c2d50067967e4a445b26a6683008a4fa52e02da02a9976417a15
EXIT=1
```

The whole of main:

```
main=a0500d5196dc990d899d8ccaca2e270faaf29efc manifests=140 pins=242 ok=223 mismatch=13 path_missing=2 incomplete=0 unbound=4
UNBOUND_BLOB_SHA256 manifest=14-ai-development/work-items/AID-2026-001/manifest.yaml pointer=/dev_baseline_integration/measurement_basis/model_blob_sha256_lf field=model_blob_sha256_lf declared=8324ec551749c2d50067967e4a445b26a6683008a4fa52e02da02a9976417a15
UNBOUND_BLOB_SHA256 manifest=14-ai-development/work-items/AID-2026-001/manifest.yaml pointer=/dev_baseline_integration/measurement_basis/model_blob_sha256_crlf field=model_blob_sha256_crlf declared=35efab9361f313bb556159818ef2fbb1a6380cbf48d12f8aead273c3c438a946
UNBOUND_BLOB_SHA256 manifest=14-ai-development/work-items/AID-2026-001/manifest.yaml pointer=/dev_baseline_integration/measurement_basis/tests_blob_sha256_lf field=tests_blob_sha256_lf declared=26c72ceaa636606118ef94013b7515842d51b02b521c3cb0e6ef4303c72308af
UNBOUND_BLOB_SHA256 manifest=14-ai-development/work-items/AID-2026-001/manifest.yaml pointer=/dev_baseline_integration/measurement_basis/tests_blob_sha256_crlf field=tests_blob_sha256_crlf declared=f326cafd70c97a7cc0133ad2139d7508d83f493c710d80f534e01c25d68734ce
EXIT=1
```

Four new findings, one manifest. Every other counter is unchanged: the rule adds
only the previously excluded class and does not disturb the 238 pre-existing
pins. Those four fields are exactly the ones #1417 excluded by name.

## Ratchet consequence

The ratchet step of the existing hard gate, with `UNBOUND_BLOB_SHA256` added to
its sed filter:

```
ratchet: scripts/ci/baselines/manifest-blob-pins.txt
ratchet: baseline=15 current=19 regressions=4 fixed=0
ratchet: FAIL - 4 new failure(s) above baseline.
```

The baseline file is byte-unchanged. The red light is a newly discovered real
violation, not a baseline drift and not a test regression.

## Boundary

No baseline entry was added or edited. No other workflow, branch protection,
ruleset or required context was changed. No merge is claimed. PR #1426 and its
branch were not touched.
