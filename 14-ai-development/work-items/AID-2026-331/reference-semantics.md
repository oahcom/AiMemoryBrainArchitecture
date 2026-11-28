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

## AID-2026-336 implementation semantics

### Related-evidence reference mode and policy classification

Every non-empty `related_evidence[]` blob declaration MUST have an explicit
`reference_mode` in its own declaration record.

The only accepted values are:

- `historical`
- `current`

The checker MUST NOT infer a missing mode, silently default it to `current`,
or silently default it to `historical`.

A missing or invalid mode is a deterministic declaration-policy violation.
The checker MUST emit:

`REFERENCE_MODE_MISSING_OR_INVALID`

The finding MUST use:

- `classification="policy"`
- `scope=related_evidence`
- `locator=reference_mode`
- `reason="reference_mode must be historical or current"`

This condition is a violation, not an incomplete scan. It MUST contribute to
the violation result and produce exit status `1`, not exit status `2`.

A missing or invalid mode does not authorize the checker to evaluate the
declaration under either reference mode. The declaration remains unevaluated
and the finding records why it could not be accepted.

### Historical and current resolution

`authored_indexes[]` declarations are historical authorship references. Each
non-empty declaration MUST be checked against reachable Git blob history at
the exact declared path.

A historical `related_evidence[]` declaration MUST be checked using the same
exact-path reachable-history rule.

A current `related_evidence[]` declaration MUST be checked against the
candidate commit tree. A current reference is not satisfied merely because
the declared blob appears somewhere else in repository history.

The checker MUST preserve the distinction between:

- `HISTORICAL_REFERENCE_NOT_FOUND`: the declared blob is not recorded at the
  exact path in reachable history;
- `CURRENT_REFERENCE_MISMATCH`: the declared blob does not match the
  candidate-tree reference;
- `REFERENCE_MODE_MISSING_OR_INVALID`: the declaration does not provide a
  valid mode and therefore cannot be assigned historical or current
  resolution semantics.

The first two findings use their respective `historical` and `current`
classifications. The missing/invalid mode finding uses
`classification="policy"`.

### Exit-status contract

The checker uses the following exit-status contract:

| Exit status | Meaning |
|---:|---|
| `0` | No in-scope violation or incomplete scan was found |
| `1` | A deterministic declaration or reference violation was found |
| `2` | The checker could not establish a trustworthy scan result because of genuinely incomplete input or unavailable/unreadable Git data |

A missing or invalid `related_evidence[].reference_mode` is status `1`.
Historical reference misses, current reference mismatches, missing required
paths, and unbound blob SHA-256 declarations are also violations and use
status `1`.

Malformed or unreadable manifest data, an unavailable source commit, or
unreadable Git history/object data that prevents a trustworthy evaluation
remains status `2`.

This distinction allows base and negative-fixture scans of commits predating
the mode migration to complete and report the deterministic policy violation
without misclassifying the scan itself as incomplete.

### `blob_sha256` declarations are in scope

A non-empty manifest key matching the `blob_sha256` declaration family,
including qualified names such as `model_blob_sha256_lf`, is an in-scope
content-integrity declaration.

These declarations are SHA-256 claims over committed file bytes. They are
distinct from Git blob object IDs and MUST be verified using SHA-256 over the
bytes at the bound path in the candidate commit.

The checker MUST discover matching declarations at arbitrary nesting depth.
Each finding MUST preserve its manifest path, JSON Pointer, field name, and
declared digest where applicable.

The declaration MUST bind to a path in its own containing mapping. The
checker may use the corresponding `<base>_path` or `<base>_file` field, or the
supported generic `path` or `file` field. A bare base field is accepted only
when its value is path-like under the checker contract.

A non-empty `blob_sha256` declaration counts as an in-scope pin, including
when it cannot be bound to a path.

A declaration with no bindable path MUST emit `UNBOUND_BLOB_SHA256`, increment
the `unbound` summary counter, and produce exit status `1`. It MUST NOT be
silently excluded.

A bound declaration whose path is absent from the candidate commit tree is a
path violation. A bound declaration whose SHA-256 differs from the committed
file bytes is a mismatch. Invalid declarations or unreadable Git data that
prevent evaluation remain incomplete conditions.

The summary MUST expose the `unbound=` count so that an unbound declaration
cannot disappear from the result merely because it has no path to compare.

### Pin counting and exclusions

The `pins=` summary counts non-empty declarations handled by the in-scope
checker contract, including non-empty `blob_sha256` declarations.

The documented out-of-scope families `gate_a_reconstruction` and
`d_source_blobs` are not promoted into the AID-336 historical/current pin
inventory.

The documented prompt metadata exclusions are not ordinary AID-336
candidate-tree blob pins. Session Evidence check 11 remains authoritative for
the prompt snapshot digest and byte-count enforcement assigned to it.

The runtime `excluded=` summary is an implementation counter. It MUST NOT be
treated as interchangeable with a separately inventoried prompt-metadata
count or a manually assessed declaration-family count.

### Commit selection and `--commit`

The checker accepts an explicit commit-ish revision through `--commit`.
The revision is resolved to a full commit ID before the scan is performed.

Examples include:

```bash
python scripts/ci/check_manifest_blob_pins.py --commit HEAD
python scripts/ci/check_manifest_blob_pins.py --commit origin/main
python scripts/ci/check_manifest_blob_pins.py --commit <commit-sha>
```

`HEAD` selects the commit currently checked out in the invoking worktree.
`origin/main` selects the commit resolved from that local remote-tracking
reference. An explicit commit SHA selects that commit.

The checker MUST report the resolved full commit ID in its summary. It MUST
not silently replace an explicitly requested revision with `HEAD` or another
candidate revision.

An absent, invalid, ambiguous, or unavailable requested commit is an
incomplete scan and returns status `2`. The caller is responsible for
providing a revision that exists in the repository being scanned.

Base, candidate, and fixed negative-fixture scans may therefore use different
explicit commit arguments. A commit predating the related-evidence mode
migration can still be scanned: its missing mode is reported as a policy
violation with status `1`, rather than as an incomplete scan with status `2`.

### Ratchet integration

Any output filter that supplies checker findings to the manifest blob-pin
ratchet MUST retain all violation diagnostic families, including:

- `MISMATCH`
- `PATH_MISSING`
- `INCOMPLETE`
- `UNBOUND_BLOB_SHA256`
- `HISTORICAL_REFERENCE_NOT_FOUND`
- `CURRENT_REFERENCE_MISMATCH`
- `REFERENCE_MODE_MISSING_OR_INVALID`

A ratchet filter MUST NOT omit a newly introduced semantic diagnostic merely
because the current baseline is empty or because the diagnostic did not exist
when the baseline was created.

The baseline remains the ratchet comparison input; the filter is responsible
for ensuring that all relevant checker findings reach it.
