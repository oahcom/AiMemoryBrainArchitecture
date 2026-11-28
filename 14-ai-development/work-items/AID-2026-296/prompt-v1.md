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
      last_verification_note: "Prompt snapshot recorded; CI verification and independent review are pending."
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
      - "prompt-snapshot"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---
# AID-2026-296 — Task input (v1, structured snapshot)

Prompt ID: AID-2026-296-PROMPT v1. This is the task input as dispatched to the
implementing session, condensed to the operative requirements. It is a
structured snapshot, not a raw transcript.

## Authority for the ruling

Carrier conflict adjudication, `chatgpt-session-ops` reply
`reply-6b07c97e-081917.md` §5:

> `blob_sha256` or `*_blob_sha256` declarations that have no bindable path are
> `VIOLATION`, and must not be excluded from the check scope.

Basis: PR #1417 comment 7212343821 —

> Please close this draft as superseded by #1426. Port malformed-array
> fail-closed handling only; the proposal to classify unbound blob_sha256 as
> out of scope is rejected.

That comment supersedes the p71 §6 exclusion ("fields without a path are out of
scope").

## What #1426 must absorb

1. One independent finding per unbound `blob_sha256` / `*_blob_sha256`.
2. Finding type fixed to `UNBOUND_BLOB_SHA256`.
3. Record manifest path, YAML/JSON pointer, field name and digest value.
4. Classify as `VIOLATION`; the checker returns a non-zero violation exit code.
5. Four positive/negative tests: bound + matching digest passes; bound +
   mismatched digest is `MISMATCH`; bound + absent target is `PATH_MISSING`;
   digest with no path is `UNBOUND_BLOB_SHA256` and must fail.
6. The unbound fields must not be absorbed into the existing ratchet baseline.

## Preconditions checked before implementation

`scripts/ci/check_manifest_blob_pins.py` is already on `main` and is already
wired into `.github/workflows/repository-hygiene.yml` (the "Measure manifest
blob-pin baseline and negative sample" and "Ratchet manifest blob pins" steps).
#1426 is an improvement PR owned by another session and is not a prerequisite:
the work is implemented on the checker that exists on `main`.

## Task list as dispatched

1. Fetch `origin`, record the full `origin/main` SHA.
2. Create an isolated worktree; do not touch the primary worktree.
3. Measure and record the current behaviour on `main` for a pathless
   `blob_sha256` (before evidence).
4. Implement the `UNBOUND_BLOB_SHA256` finding with a non-zero exit code and the
   fields listed above.
5. Add the four tests, run the whole existing suite, paste real output.
6. Run the checker over the whole of `main`, count new violations and their
   distribution per manifest, paste real output.
7. Push without force and open a PR; the PR body carries the ruling citation.
8. Comment on #1426 stating that the fail-closed behaviour now exists on `main`
   and must be absorbed as the baseline, not excluded or baselined away.
9. Poll check-runs for the 16 declared contexts; keep a red
   `Repository hygiene (hard gate)` red and report it as a newly discovered real
   violation instead of masking it.
10. Deliver the round report.

## Explicit constraints

- No force push, no rebase, no merge, no edits to another PR's branch, no edits
  to the primary worktree.
- Do not change the ratchet baseline to make the gate green.
