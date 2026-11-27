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
        - "14-ai-development/work-items/AID-2026-268/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Implementation evidence only; exact scan counts and CI results are not asserted until observed."
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
    canonical_scope: "Implementation evidence for AID-2026-268 manifest blob-pin verification"
    canonical_scope_id: "ai-development/aid-2026-268-evidence"
    canonical_scope_keywords:
      - "manifest"
      - "blob-pin"
      - "integrity"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---
# AID-2026-268 evidence

**Attribution:** user-authorized operator (delegated by account owner)  
**Date:** 2026-11-27  
**Baseline fetched:** 2026-11-27T03:57:43Z  
**Baseline main:** 40195e8bf96b9cc6aa254066b9b72968f29ac361

## Scope

Implement blob-pin integrity checking in the existing required Repository hygiene job. No branch-protection, new-job, or new-workflow changes are in scope.

## Measurements

Repository hygiene workflow run: `45939439751`; job `140310147849`; exact workflow checkout merge candidate `b2a2b37cbc5bdd74d7fd5511a5e91dd2662f517e`. The base SHA was `386d8f57b02d8e3c511ff0e3980b9ce0af8b3028` and the PR head was scanned separately.

- Main raw summary: `main=386d8f57b02d8e3c511ff0e3980b9ce0af8b3028 manifests=115 pins=178 ok=95 mismatch=83 path_missing=0 incomplete=0`
- #1220 raw summary: `main=9a2063ae1fa5d905b3817cd4eddba065a06daa73 manifests=108 pins=162 ok=79 mismatch=83 path_missing=0 incomplete=0`
- Candidate raw summary: `main=b2a2b37cbc5bdd74d7fd5511a5e91dd2662f517e manifests=116 pins=180 ok=97 mismatch=83 path_missing=0 incomplete=0`

The 83 baseline entries are 40 historical prompt SHA-256 mismatches, 40 prompt byte-count mismatches, and 3 AID-2026-100 related-evidence Git blob mismatches. No missing paths or incomplete commit lookups were observed in these scans. The current-main baseline file contains all 83 raw mismatch lines; the ratchet will reject any new item and any item that stops failing.

### First 10 main mismatch lines (raw)

```text
MISMATCH session_evidence[0].executed_prompt_snapshot_file path=14-ai-development/work-items/AID-2026-059/prompt-v1.md declared=65474e7f0927d2dfeaad33814fdbd7d576635cc8a0e8d2a3a7441e3a65ab7317 actual=4881d6292e96154d5f7364816ae3e9977365e09b88e8475f4dd9d655e3e34a8c
MISMATCH session_evidence[0].executed_prompt_snapshot_file path=14-ai-development/work-items/AID-2026-059/prompt-v1.md declared=3866 actual=3808
MISMATCH session_evidence[1].executed_prompt_snapshot_file path=14-ai-development/work-items/AID-2026-059/prompt-1015.md declared=245dbfc39ca8b20cec30bba392c4b2f5e0db383b404eb4e8e10a8f7cee899f46 actual=2be1e84c9fc262066e687bf21a57d80a090fed73d3c6765f26fc6fc02d3c0b51
MISMATCH session_evidence[1].executed_prompt_snapshot_file path=14-ai-development/work-items/AID-2026-059/prompt-1015.md declared=7986 actual=7928
MISMATCH session_evidence[2].executed_prompt_snapshot_file path=14-ai-development/work-items/AID-2026-059/prompt-1026-v1.md declared=25058389340c796a557746ae5ed90cf73cada98998e62da1692bb5ce4a3e4bd9 actual=8ca8bfc89774fa728e1671808510af4aa9def9b9860a9cc9016c5ca8bba87ea5
MISMATCH session_evidence[2].executed_prompt_snapshot_file path=14-ai-development/work-items/AID-2026-059/prompt-1026-v1.md declared=4811 actual=4753
MISMATCH session_evidence[3].executed_prompt_snapshot_file path=14-ai-development/work-items/AID-2026-059/prompt-1042-1048-v1.md declared=ceae6530d70c60803b58ba91a3f5ed28671a525bcc640c32aa8f020d3defaffd actual=8aa0b29ce5ce620c77ac3621531b4b8df908010675f5486672d056345eb76b11
MISMATCH session_evidence[3].executed_prompt_snapshot_file path=14-ai-development/work-items/AID-2026-059/prompt-1042-1048-v1.md declared=6507 actual=6449
MISMATCH session_evidence[4].executed_prompt_snapshot_file path=14-ai-development/work-items/AID-2026-059/prompt-1029-1076-v1.md declared=f0a315582ba51212758d82c6dfacedaaa676575f2b0ffcec4170fbded05f229e actual=81e070af08045cec4635201b99861bab00a2ffa7e1caafab3342608d0adde22a
MISMATCH session_evidence[4].executed_prompt_snapshot_file path=14-ai-development/work-items/AID-2026-059/prompt-1029-1076-v1.md declared=9166 actual=9108
```

## Field enumeration

The following branches are in `scripts/ci/check_manifest_blob_pins.py` (line numbers are 1-based in the measured source):

| Class | Manifest declaration | Commit used | Code location |
|---|---|---|---|
| Top-level index root | `root` / `root_blob` | Candidate tree | lines 151–160 |
| Top-level language mirrors | `en_mirror` / `en_mirror_blob`; `zh_cn_mirror` / `zh_cn_mirror_blob` | Candidate tree | lines 151–160 |
| Authored index roots/mirrors | `authored_indexes[].root`, `en_mirror`, `zh_cn_mirror` and paired `*_blob` fields | Candidate tree | lines 177–188 |
| Reconstructed root | `gate_a_reconstruction[].root` / `reconstructed_root_blob` | Entry `source_commit`/`commit`, or the commit SHA explicitly named in its note | lines 164–176 |
| Related evidence | `related_evidence[].path` / `blob` | Candidate tree | lines 190–202 |
| Related evidence mirrors | `related_evidence[].en_mirror` / `.en_mirror_blob`; `.zh_cn_mirror` / `.zh_cn_mirror_blob` | Candidate tree | lines 190–202 |
| Execution evidence | `evidence_file` / `evidence_blob` | Candidate tree | lines 203–207 |
| Cross-commit source blobs | `d_source_blobs[]` entries `<path>: <sha1>` | `d_source_commit` | lines 208–225 |
| Top-level prompt snapshot | `prompt.prompt_file` / `prompt_sha256` / `prompt_bytes` | Candidate tree | lines 226–234 |
| Session prompt snapshots | `session_evidence[].executed_prompt_snapshot_file` / `executed_prompt_sha256` / `executed_prompt_bytes` | Candidate tree | lines 235–250 |

Git source-commit resolution and committed blob-byte reads are implemented at lines 45–61. Git blob SHA-1 is recomputed from the Git object header plus committed bytes at lines 64–66. All digest/byte-count comparisons and missing-path handling are centralized in `check()` at lines 91–136. Exit-code selection is at line 253 (0 PASS, 1 VIOLATION, 2 INCOMPLETE).

Non-blob metadata such as timestamps, counts, and status values is deliberately ignored.
