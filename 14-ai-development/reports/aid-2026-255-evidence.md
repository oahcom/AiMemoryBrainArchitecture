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
        - "14-ai-development/work-items/14-ai-development/reports/aid-2026-255-evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Local command output recorded verbatim; no CI run asserted."
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
    canonical_scope: "Delta evidence for AID-2026-255 sibling-key association tests"
    canonical_scope_id: "ai-development/aid-2026-255-evidence"
    canonical_scope_keywords:
      - "manifest"
      - "blob-pin"
      - "sibling-key"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---

# AID-2026-255 evidence — sibling-key association delta

## Carrier

`main` carries the manifest blob-pin checker, its 98-line ratchet baseline and its
Repository hygiene wiring from `AID-2026-268` / PR #1392. This work item is not a
second implementation. Its authorized delta is:

- four sibling-key association mutation tests appended to
  `scripts/ci/test_check_manifest_blob_pins.py`;
- `ratchet-negative.md`, recording the ratchet's negative contract against the
  landed baseline;
- `independent-review.md`, recording the independent review and its dispositions.

Nothing else changes. `scripts/ci/check_manifest_blob_pins.py`,
`scripts/ci/baselines/manifest-blob-pins.txt`,
`.github/workflows/repository-hygiene.yml` and every file under
`AID-2026-268` are byte-identical to `main`.

## What the new tests establish

Each new method is a mutation test: it fails against a resolver that associates a
digest with the wrong sibling path key.

| Test | Wrong implementation it kills |
| --- | --- |
| `test_neighbouring_digest_key_does_not_verify_target_pair` | A resolver that walks the mapping and reuses the last digest seen, or that pairs a digest with the previous path key, reports the neighbour as clean. |
| `test_path_key_identity_uses_en_mirror_path_not_neighbour_file` | A resolver that hashes the file named by the digest's owner rather than the file named by the sibling path key. |
| `test_cross_identity_isolation_reports_only_the_wrong_pin` | A resolver that carries state between identities: one wrong pin must not clear or poison a correct one. |
| `test_every_enumerated_path_digest_pair_is_validated` | A resolver that implements one pair shape and silently skips the others it documents. |

The eight pre-existing methods are byte-identical to `main`.

## Local verification

```
$ python -m unittest discover -s scripts/ci -p "test_check_manifest_blob_pins.py" -v
Ran 12 tests in 22.579s
OK
```

The ratchet is exercised in `ratchet-negative.md`: control, regression and stale
baseline cases, run against the landed checker at the commit that carries this
delta.

## Not claimed

No CI run, no merge, no Owner acceptance, and no reduction of the 89 baseline
entries. Those entries remain known unresolved mismatches recorded by
`AID-2026-268`, not fixes delivered here.
