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
        - "14-ai-development/work-items/AID-2026-330/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-28"
      last_verification_note: "Inventory compiled from the pinned base commit and recorded command outputs; it states its own discovery limits."
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
    canonical_scope: "Blob declaration inventory for Issue #1350"
    canonical_scope_id: "ai-development/aid-2026-330-blob-declaration-inventory"
    canonical_scope_keywords:
      - "blob-pin"
      - "manifest"
      - "inventory"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---

# Blob Declaration Inventory

## 1. Basis

- Repository: `oahcom/AiMemoryBrainArchitecture`
- Base commit: `f77b1e63f0aca6b93f14fee5bd5c04510053ee23`
- Blob-pin checker: `scripts/ci/check_manifest_blob_pins.py`
- Manifest schema checker: `scripts/ci/check_work_item_manifest_schema.py`
- Session Evidence validator: `scripts/governance/session_evidence/validate.py`

This document inventories the declaration families identified in the supplied checker and repository searches. It records the definition locations, checker coverage, overlapping enforcement, and limits of the available discovery evidence.

It does not claim that the checker discovers every declaration, that current declaration data is correct, or that any issue or work item has been accepted or closed.

## 2. Definition-location findings

### 2.1 No independent normative definition for root/mirror/evidence families

Command:

```powershell
git grep -l -E "root_blob|en_mirror_blob|related_evidence|authored_indexes" f77b1e63 -- "*.md" "*.yaml" "*.yml" "*.json" "*.py"
```

Output: seven paths.

```text
14-ai-development/work-items/AID-2026-100/manifest.yaml
14-ai-development/work-items/AID-2026-255/independent-review.md
14-ai-development/work-items/AID-2026-255/prompt-v1.md
14-ai-development/work-items/AID-2026-255/session-evidence.md
14-ai-development/work-items/AID-2026-268/evidence.md
scripts/ci/check_manifest_blob_pins.py
scripts/ci/test_check_manifest_blob_pins.py
```

The earlier description of this output as six paths was a counting error. The seven displayed paths are the correct count.

The supplied search and source inspection found no normative schema, specification, template, or governance document defining:

- `root`, `root_blob`;
- `en_mirror`, `en_mirror_blob`;
- `zh_cn_mirror`, `zh_cn_mirror_blob`;
- `related_evidence`, `authored_indexes`;
- `evidence_file`, `evidence_blob`;
- `gate_a_reconstruction`, `reconstructed_root_blob`;
- `d_source_commit`, `d_source_blobs`.

For these families, the definition of record is:

**NONE - defined only by `scripts/ci/check_manifest_blob_pins.py`.**

This is a discovery gap, not merely a missing citation. The checker is the consumer and the only located definition of the declaration shapes it consumes. Its own implementation cannot independently establish that it has discovered all declarations that should exist.

### 2.2 Manifest schema checker confirms the gap

`scripts/ci/check_work_item_manifest_schema.py` is the manifest schema checker of record.

Its supplied required top-level keys are:

```python
REQUIRED = (
    "work_item_id", "title", "class", "risk", "risk_rationale", "status",
    "id_status", "sponsor", "accountable_owner", "acceptance_authority",
    "attribution", "date", "repository", "base_branch", "base_commit_sha",
    "scope", "evidence", "documentation", "session_evidence", "implementation",
)
```

Its supplied documentation relationship set is:

```python
DOC_RELATIONSHIPS = {
    "normative", "design", "implementation", "evidence",
    "reference", "code", "schema"
}
```

The supplied structural rules require:

- `documentation` to be a non-empty sequence of `{path, relationship}` entries;
- every documentation path to exist in the Git tree;
- every relationship to belong to `DOC_RELATIONSHIPS`;
- `session_evidence` to be a non-empty sequence with `role`, `issue_refs`, `implementing_ai_session`, and `session_evidence_ref`;
- the session evidence reference basename to match `session-evidence*.md`;
- `implementation` to carry `status`, `summary`, `files_changed`, and `tests`;
- implementation status to belong to `NOT_STARTED`, `IN_PROGRESS`, `IMPLEMENTED`, `BLOCKED`, or `NOT_APPLICABLE`;
- `files_changed` and `tests` to be sequences;
- duplicate YAML keys to be rejected.

No blob-declaration field appears in the supplied schema. In particular, `root_blob`, `en_mirror_blob`, `related_evidence`, `authored_indexes`, `evidence_blob`, and `d_source_blobs` are not part of the manifest schema.

The schema checker therefore confirms that the listed blob declaration families are outside the repository's general manifest schema. It does not define or validate those field families.

### 2.3 The AID-2026-001 manifest workflow is not a general manifest schema

The supplied inspection of `.github/workflows/aid-2026-001-manifest-validation.yml` establishes that its manifest structure gate validates only the required keys of `AID-2026-001/manifest.yaml`.

It is not a schema for other work-item manifests or for blob declaration fields.

`14-ai-development/work-items/INDEX.md` defines registration membership and index conventions, not manifest field semantics.

## 3. Prompt and session-evidence contract

The normative template is:

`14-ai-development/prompt-and-evidence-template.md`

The supplied excerpts establish:

- Lines 45–46: the normative prompt digest is `executed_prompt_sha256` in a `session_evidence` entry.
- Lines 49–51: top-level `prompt_sha256` is non-normative and human-readable.
- Lines 53–55: the legacy top-level executed-prompt snapshot fields.
- Lines 222–228: `session_evidence` is the canonical repeatable representation; the legacy top-level representation applies only when `session_evidence` is absent; the two representations are mutually exclusive and fail-closed.
- Line 246: enforcement lives in `scripts/governance/session_evidence/validate.py`.
- Line 248: the top-level `prompt_id` / `prompt_sha256` pair is non-normative; the authoritative value is `executed_prompt_sha256` inside a `session_evidence` entry.

### 3.1 Top-level prompt digest

The top-level `prompt_sha256` is explicitly non-normative. It is not the authoritative digest of the executed prompt.

The authoritative digest is `executed_prompt_sha256` in the canonical `session_evidence` entry, or the specified legacy top-level representation when no `session_evidence` block exists.

### 3.2 Nested `prompt:` mapping conflict

Checker branch F reads:

- `prompt.prompt_file`;
- `prompt.prompt_sha256`;
- `prompt.prompt_bytes`.

The supplied normative template does not define this nested `prompt:` mapping. It defines the relevant prompt fields at top level and defines `session_evidence` as the canonical repeatable representation.

The nested mapping is present in nine manifests:

- `AID-2026-005`;
- `AID-2026-006`;
- `AID-2026-008`;
- `AID-2026-009`;
- `AID-2026-024`;
- `AID-2026-025`;
- `AID-2026-029`;
- `AID-2026-100`;
- `FIX-2026-P1-T1`.

Presence in manifests does not establish that this shape is normative. The nested mapping is an undefined checker-consumed representation and must not be silently equated with either the canonical session list or the specified legacy top-level representation.

## 4. Session Evidence check 11: overlapping enforcement

The supplied source inspection identifies check 11 in:

`scripts/governance/session_evidence/validate.py`

Its stated responsibility is to verify that `executed_prompt_sha256` and `executed_prompt_bytes` match the executed prompt snapshot blob.

The supplied implementation excerpts establish:

```python
# Hash the original blob bytes, not decoded/re-encoded text.
actual_hash = hashlib.sha256(raw).hexdigest()
expected_hash = entry["executed_prompt_sha256"].lower()
```

The validator also compares:

```python
len(raw) != entry["executed_prompt_bytes"]
```

The supplied line references are 1811–1828.

The supplied retrieval helper at lines 286–330 uses `gh_blob_bytes(repo, sha, path)` to resolve the blob from the PR-head tree.

`.github/workflows/session-evidence.yml` is supplied as running on:

- `pull_request` opened;
- `pull_request` synchronize;
- `pull_request` reopened;
- `pull_request` edited;
- `merge_group`.

Its `validate` job is a required context.

### 4.1 Coverage collision and different bases

The blob-pin checker branch F and Session Evidence check 11 overlap on executed-prompt snapshot fields:

| Field | Blob-pin checker basis | Session Evidence validator basis |
|---|---|---|
| `executed_prompt_sha256` | Candidate commit | PR-head tree blob |
| `executed_prompt_bytes` | Candidate commit | PR-head tree blob |

The bases can disagree when the candidate commit and PR-head tree differ. Therefore, the two gates can produce different results without either calculation necessarily being internally incorrect.

The Session Evidence gate being green on `main` does not prove that a candidate-commit lookup returns the same blob bytes as the PR-head-tree lookup.

### 4.2 AID-2026-101 and AID-2026-102

The supplied current checker results show two snapshots, AID-2026-101 and AID-2026-102, each with:

- an `executed_prompt_sha256` mismatch;
- an `executed_prompt_bytes` mismatch.

These are two snapshot records with two observed properties each. They are not four independent snapshot defects.

The byte-count checks are not unenforced metadata. Session Evidence check 11 already enforces `executed_prompt_bytes`. Removing the duplicate byte-count assertion from the blob-pin checker would remove duplicate enforcement from that checker only; it would not remove enforcement from the required Session Evidence gate.

## 5. Field-family inventory

| Family | Definition location | Shape / resolution | Blob-pin checker coverage | Session Evidence overlap | Disposition |
|---|---|---|---|---|---|
| Top-level root/mirror triple | NONE - defined only by `scripts/ci/check_manifest_blob_pins.py` | Root plus optional EN/ZH mirror paths and Git blob SHA-1 declarations; candidate commit | Family A | None established | Checker-defined contract; no independent normative schema located |
| Gate-A reconstructed root | NONE - defined only by `scripts/ci/check_manifest_blob_pins.py` | `gate_a_reconstruction[]`; root and reconstructed-root blob; source commit selected from `source_commit`, `commit`, or note | Family B | None established | Checker-defined contract; no independent normative schema located |
| Authored indexes | NONE - defined only by `scripts/ci/check_manifest_blob_pins.py` | `baseline_and_source_evidence.authored_indexes[]`, falling back to top-level `authored_indexes[]`; root/EN/ZH triple | Family B2 | None established | Checker-defined contract; no independent normative schema located |
| Related evidence and mirrors | NONE - defined only by `scripts/ci/check_manifest_blob_pins.py` | Evidence path and optional EN/ZH mirror paths with blob declarations; candidate commit | Family C | None established | Checker-defined contract; no independent normative schema located |
| Evidence file | NONE - defined only by `scripts/ci/check_manifest_blob_pins.py` | `evidence_file` / `evidence_blob`; candidate commit | Family D | None established | Checker-defined contract; no independent normative schema located |
| D-source blobs | NONE - defined only by `scripts/ci/check_manifest_blob_pins.py` | `d_source_blobs[]`; `name: Git blob SHA`; resolves against `d_source_commit` | Family E | None established | Separate semantic decision needed: historical provenance object or candidate-tree declaration |
| Top-level `prompt_sha256` | `14-ai-development/prompt-and-evidence-template.md`, lines 45–51 and 248 | Non-normative, human-readable/historical pair | Checker branch F reads a nested `prompt.prompt_sha256`, not this top-level field | Template says top-level pair is non-normative | Not authoritative executed-prompt digest |
| Legacy top-level executed-prompt fields | `14-ai-development/prompt-and-evidence-template.md`, lines 53–55 and 222–228 | Legacy representation only when `session_evidence` is absent; all seven legacy fields required | Branch F does not establish correct handling of this shape | Session Evidence validator enforces the template-defined representation | Preserve template semantics; no silent mixing |
| `session_evidence[]` snapshot fields | `14-ai-development/prompt-and-evidence-template.md`, lines 222–228 and 248 | Canonical repeatable list; one entry per session | Branch F reads snapshot path, SHA-256, and byte count | Check 11 asserts SHA-256 and bytes from PR-head tree | Resolve duplicate assertions and resolution-base contract |
| Nested `prompt:` mapping | No definition in the normative template | Present in nine manifests; checker expects nested prompt fields | Branch F | Not the template-defined canonical or legacy shape | Explicit contract conflict; do not silently treat as normative |
| Generic digest/blob names | No independent definition established by the supplied inventory | Meaning cannot be inferred from key name or digest length alone | Only the exact branches above are established | No overlap established | Further targeted definition search required |
| Commit-like names | No common family definition established by the supplied inventory | Object type and resolution semantics need declaration-context evidence | Some are branch-specific selectors | No overlap established | Further targeted definition search required |
| `tree_sha` | No independent definition established by the supplied inventory | Tree object identity, not blob identity | No general coverage established | No overlap established | Keep separate from blob fields |

## 6. Generic field-name enumeration

The supplied literal-key counts across YAML/YML files are:

```text
89 base_commit_sha
67 prompt_sha256
66 blob_sha
66 executed_prompt_sha256
54 merge_commit_sha
24 observed_main
9 merge_commit
9 prompt_file_commit_sha
9 prompt_file_blob_sha
9 source_blob_sha
9 sha
9 implementation_commit_sha
7 merged_head_sha
6 head_sha
6 exact_head_reviewed
6 commit
5 base_sha
5 restored_blob_sha
5 frontmatter_blob_sha
5 reviewed_head
4 tree_sha
3 reviewed_head_sha
3 git_blob_sha
3 source_commit_sha
3 translation_commit_sha
3 translation_blob_sha
3 reverified_source_blob_sha
3 reverified_translation_blob_sha
3 registration_merge_commit_sha
3 head
2 commit_before_manifest_update
2 exact_head
2 prompt_original_payload_sha256
2 baseline_merge_commit_sha
2 prior_value
2 new_value
2 stdout_sha256
2 before_blob
2 after_blob
```

These are literal key-name counts. They do not prove semantic type, nesting completeness, normative status, or checker coverage. `blob_sha256` was mentioned in the issue context, but no occurrence count for it was supplied by this enumeration.

## 7. Identifier availability evidence

Command:

```powershell
git grep -n -E "AID-2026-3[3-9][0-9]" f77b1e63 -- 14-ai-development
```

Output:

```text
```

The supplied result is zero hits in tracked files under `14-ai-development` for IDs AID-2026-330 through AID-2026-339. This does not establish availability in an external registry or untracked files. AID-2026-330 remains marked `PROVISIONAL` in this record.

## 8. DISCOVERY_LIMITS

This inventory cannot prove:

1. That every declaration-bearing field in every manifest has been found. Literal-key searches can miss aliases, indirect declarations, dynamically generated fields, and unsearched file types.
2. That the blob-pin checker covers every declaration that ought to be covered. Its demonstrated coverage is limited to the branches identified in its source.
3. That a field is a Git blob identity merely because its key contains `blob`, `sha`, or `digest`.
4. That the checker-defined root/mirror/evidence families have an independent normative schema. The supplied searches found none.
5. That the manifest schema checker validates blob declarations. Its supplied required-key list and structural rules contain no such fields.
6. That the nested `prompt:` mapping is a normative manifest representation. The supplied template does not define it.
7. That candidate-commit and PR-head tree blob resolutions are equivalent for all pull requests or merge-group events.
8. That a green Session Evidence check proves the blob-pin check's candidate-commit lookup resolves to the same bytes.
9. That the seven displayed paths establish a complete inventory of all declaration-bearing files. They are the output of one literal search.
10. That AID-2026-330 is registered or accepted merely because the supplied tracked-file identifier search returned zero hits.
11. That current declarations are correct, that discrepancies are accepted, or that any work item has owner acceptance.

## 9. Reproduction commands

Run against the pinned commit.

### Root/mirror/related-evidence family search

```powershell
git grep -l -E "root_blob|en_mirror_blob|related_evidence|authored_indexes" f77b1e63 -- "*.md" "*.yaml" "*.yml" "*.json" "*.py"
```

### Manifest schema checker

```powershell
git show f77b1e63:scripts/ci/check_work_item_manifest_schema.py
```

### Prompt template

```powershell
git show f77b1e63:14-ai-development/prompt-and-evidence-template.md
```

### Session Evidence validator

```powershell
git show f77b1e63:scripts/governance/session_evidence/validate.py
```

### Session Evidence workflow

```powershell
git show f77b1e63:.github/workflows/session-evidence.yml
```

### AID-2026-001 manifest workflow

```powershell
git show f77b1e63:.github/workflows/aid-2026-001-manifest-validation.yml
```

### Work-item INDEX

```powershell
git show f77b1e63:14-ai-development/work-items/INDEX.md
```

### Identifier availability

```powershell
git grep -n -E "AID-2026-3[3-9][0-9]" f77b1e63 -- 14-ai-development
```

Results must be interpreted at the pinned base. A later `main` result is not evidence about this inventory basis.
