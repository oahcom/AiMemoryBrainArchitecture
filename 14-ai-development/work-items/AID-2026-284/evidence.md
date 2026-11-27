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
        - "14-ai-development/work-items/AID-2026-284/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Local unit suites and offline proofs passed; the full required gate and GitHub Actions execution remain pending."
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
      - "negative-fixture-assertion"
      - "event-aware-base-resolution"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# AID-2026-284 — Evidence

Date: 2026-11-27

## 1. Contract and scope

This work addresses issues #1349 and #1350 in `oahcom/AiMemoryBrainArchitecture`.

The fix commit is `ccb22465`:

`fix(ci): make the blob-pin negative sample and base binding able to fail (AID-2026-284)`

The branch is `fix/aid268-negative-assertion`, based on:

`7fc4ddabe1ea3b216b4536c0f5cb0a0c84306f19`

The implementation changes exactly five paths:

- `.github/workflows/repository-hygiene.yml`
- `scripts/ci/resolve_manifest_blob_pin_base.py`
- `scripts/ci/assert_manifest_blob_pin_negative.py`
- `scripts/ci/test_resolve_manifest_blob_pin_base.py`
- `scripts/ci/test_assert_manifest_blob_pin_negative.py`

The workflow modification replaces the measurement step, changes the ratchet's `--commit` target from `HEAD` to `$GITHUB_SHA`, and adds one self-check step. The existing job ID `repository-hygiene` and job name `Repository hygiene (hard gate)` are unchanged. No new job, required context, dependency, or branch-protection change is introduced.

## 2. Defect 1 — the negative sample did not prove rejection

A successful checker exit alone is not sufficient evidence that the immutable negative fixture is being rejected. The new assertion checks the fixture against its expected rejection evidence and fails when the checker accepts it or produces different evidence.

The assertion is restricted to the immutable fixture commit:

`9a2063ae1fa5d905b3817cd4eddba065a06daa73`

The expected checker result is:

- Exit status 1.
- Exact summary:

  `main=9a2063ae1fa5d905b3817cd4eddba065a06daa73 manifests=108 pins=168 ok=82 mismatch=86 path_missing=0 incomplete=0`

- Exactly 86 `MISMATCH` lines.
- Zero `PATH_MISSING` lines.
- Zero `INCOMPLETE` lines.

An incomplete checker execution is not treated as a successful rejection. A false acceptance or mismatched evidence is a violation.

### Offline step-level proof

The proof used an offline clone, replaced the checker with a test double that prints nothing and exits 0, extracted the pre-fix `run:` step from base `7fc4ddab` and the delivered `run:` step from the working tree using PyYAML and the step name, and executed both extracted steps.

Measured output:
