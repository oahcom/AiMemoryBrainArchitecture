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
        - "14-ai-development/work-items/AID-2026-331/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Records Option C and PROMPT-SNAPSHOT-REFERENCE-SEMANTICS-001; implementation and snapshot provenance assessment remain outstanding."
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
    canonical_scope: "Reference semantics for authored indexes, related evidence, and executed prompt snapshots under Issue #1350"
    canonical_scope_id: "ai-development/aid-2026-331-reference-semantics"
    canonical_scope_keywords:
      - "authored_indexes"
      - "related_evidence"
      - "reference_mode"
      - "executed_prompt_snapshot_file"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Normative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# Reference Semantics — AID-2026-331

## 1. Status and governing decisions

This document records two Owner decisions:

1. **Option C** — field-family-specific reference semantics for `authored_indexes[]` and `related_evidence[]`.
2. **`PROMPT-SNAPSHOT-REFERENCE-SEMANTICS-001`** — point-in-time semantics for `session_evidence[].executed_prompt_snapshot_file` and its declared digest and byte count.

The contract is field-family-specific. The semantics of one family must not be inferred from another.

AID-2026-331 defines and documents these contracts. AID-2026-336 implements the corresponding checker behavior. This document does not claim that the current checker already implements these rules.

## 2. `authored_indexes[]`: historical authorship reference

Each `authored_indexes[]` declaration is a historical authorship reference.

For every declared path/blob pair:

1. Resolve the candidate commit's reachable Git history.
2. Determine whether the declared blob occurred at the exact declared path in that reachable history.
3. The reference is valid if that blob existed at that exact path in reachable history.
4. A later commit changing the path does not invalidate the historical authorship reference.
5. A blob found elsewhere in the repository, but never at the declared path, does not satisfy the reference.

The declared digest identifies the historical bytes associated with the authorship record. It is not an assertion that the path still contains those bytes at the candidate commit.

## 3. `related_evidence[]`: explicit per-entry reference mode

Every mapping entry in `related_evidence[]` MUST contain a `reference_mode` key at the same object level as that entry's path and blob declarations.

The mode applies to all path/blob pairs declared by that entry, including its primary evidence path and any declared English or Chinese mirror paths.

The only permitted values are the exact lowercase strings:

- `historical`
- `current`

No default exists.

The following are invalid and MUST fail closed:

- the `reference_mode` key is absent;
- the value is null, empty, or not a string;
- the value is not exactly `historical` or `current`;
- the entry cannot be parsed or classified sufficiently to determine its mode.

A checker MUST NOT infer a mode from the field name, digest value, path, neighboring entries, current repository state, or historical presence of the blob.

### 3.1 `reference_mode: historical`

For each declared path/blob pair in the entry, verify that the declared blob existed at that exact path in the candidate commit's reachable Git history.

A later edit to that path does not invalidate the reference. A blob that exists only at another path does not satisfy the reference.

### 3.2 `reference_mode: current`

For each declared path/blob pair in the entry, resolve the path in the exact candidate commit and compare the candidate-tree blob identity with the declared blob.

The reference is valid only when the declared blob matches the bytes at that path in the candidate commit. A missing path or a different candidate-tree blob is a current-reference mismatch.

## 4. `session_evidence[].executed_prompt_snapshot_file`: point-in-time session evidence

The declared `executed_prompt_sha256` and `executed_prompt_bytes` identify the exact prompt snapshot bytes executed for that session. They are historical evidence, not standing assertions about the current candidate-tree contents.

A later edit to a prompt snapshot file does not invalidate an earlier session record, provided the declared snapshot can be verified against:

1. the commit recorded in that session-evidence entry; or
2. that entry's unambiguous history.

Verification must resolve the snapshot bytes at the session's recorded commit. If the entry does not identify a commit sufficiently to resolve those bytes unambiguously, that is a missing historical-provenance defect to report separately. It is not permission to substitute candidate-tree bytes or silently rewrite the declarations.

### 4.1 Blob-pin checker boundary

The blob-pin checker MUST NOT assert `session_evidence[].executed_prompt_snapshot_file` digest or byte-count equality against candidate-tree contents.

AID-2026-336 must remove those duplicate candidate-tree assertions from the blob-pin checker.

The Session Evidence validator remains the authoritative enforcement point for both `executed_prompt_sha256` and `executed_prompt_bytes` against the PR-head tree blob under check 11. This contract does not weaken, remove, bypass, or replace check 11.

Historical verification of what was executed remains a Session Evidence provenance responsibility. The blob-pin checker must not duplicate the validator's current-tree assertion under a different base or report the resulting disagreement as a blob-pin mismatch.

### 4.2 AID-2026-101 and AID-2026-102 disposition

The Owner ruling reclassifies the four current candidate-tree findings for these two sessions — one digest finding and one byte-count finding per session — as false positives from applying candidate-tree equality to a point-in-time evidence family.

Neither session's declared digest nor byte count may be rewritten merely to match the current prompt file. The current `prompt-v1.md` files must not be restored solely to satisfy the blob-pin check.

The historical provenance of each session entry must still be assessed. If its recorded commit or unambiguous entry history cannot resolve the declared snapshot bytes, report that as a separate provenance defect. This does not reopen the chosen point-in-time semantics.

## 5. Required Option C diagnostic outcomes

The checker implementation MUST distinguish these exact diagnostic names:

| Exact diagnostic name | Condition |
|---|---|
| `HISTORICAL_REFERENCE_NOT_FOUND` | A declared historical blob cannot be found at the exact declared path in the candidate commit's reachable Git history. This includes a blob that exists only at a different path. |
| `REFERENCE_MODE_MISSING_OR_INVALID` | A `related_evidence[]` entry has no `reference_mode`, has an unsupported or malformed value, or cannot be classified. |
| `CURRENT_REFERENCE_MISMATCH` | A `related_evidence[]` entry marked `current` has a missing declared path or its candidate-commit bytes do not match the declared blob. |

These diagnostics are not interchangeable:

- A historical reference must not be reported as a current-byte mismatch merely because the candidate tree has since changed.
- A missing or invalid mode must not be silently treated as historical or current.
- A current mismatch must not be reported as a missing historical reference.

The checker must fail closed for each of these outcomes.

The prompt-snapshot provenance assessment is a separate Session Evidence responsibility. The three diagnostics above are the required distinct outcomes for the Option C blob-reference families; they do not authorize treating a prompt-snapshot provenance defect as one of those three blob-pin findings.

## 6. Migration disposition

The six existing `authored_indexes[]` declarations retain their original digests and are classified as historical authorship references.

The three existing `related_evidence[0]` path/blob declarations retain their original digests and are to receive `reference_mode: historical`.

The two prompt-snapshot records retain their declared digest and byte-count values and are classified as point-in-time session evidence. Their historical bytes must be resolved from the recorded session commit or unambiguous entry history. Missing commit provenance must be recorded separately.

The migration table records all eleven occurrences and the required actions. No digest or byte count is rewritten to match current candidate-tree bytes.

## 7. Explicit non-effects and implementation boundary

This document:

- defines the reference contracts; it does not change the checker;
- does not change a validator, workflow, or prompt/evidence template;
- does not rewrite any of the nine authored-index or related-evidence digests;
- does not rewrite either prompt-snapshot digest or byte-count declaration;
- does not apply the `reference_mode: historical` additions to `AID-2026-100/manifest.yaml`;
- does not remove or weaken Session Evidence validator check 11;
- does not claim that AID-2026-101/-102 historical provenance has been resolved;
- does not constitute AID-2026-255 acceptance;
- does not close or accept Issue #1350.

AID-2026-336 implements the checker changes defined here, including removal of the duplicate candidate-tree prompt-snapshot assertions while retaining Session Evidence check 11.
