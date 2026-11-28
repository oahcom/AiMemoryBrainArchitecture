---
document_metadata:
  steward: "Architecture Governance"
  domain: ai-development
  role: normative-standard
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      approved_version: null
      approval_date: null
      approval_scope: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      verification_reference: null
    usage_status: Active
    modification_status: Unchanged
    supersession: null
    archival: null
  authority:
    canonical_status: Candidate
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Normative
  bilingual_counterpart: "policy.zh-CN.md"
---
```

# Work-item Registry Migration Policy

**Version:** 1.1  
**Policy baseline:** p72 §2 and §3; p74 registry adjudication  
**Source tree for this migration run:** `efbdebfa`  
**Scope:** 140 work-item manifests: 139 AID records and 1 FIX record

## 1. Non-negotiable migration rules

1. Legacy manifests are read only from Git blobs in the specified source tree.
2. No migration operation may modify, normalize, rewrite, or reserialize a legacy manifest.
3. A parsed YAML value is a candidate, not automatically an authoritative value.
4. Every registry field receives an explicit state. Missing evidence is not converted into `NOT_APPLICABLE`, and conflicting evidence is not converted into `UNKNOWN`.
5. A field with ambiguous, malformed, unreadable, or unverifiable source evidence is `UNCONFIRMED`, not `UNKNOWN`.
6. `session_evidence.*.executed_prompt_sha256` and every other executed-prompt digest are distinct from the registered `prompt_sha256`. They must never be candidates for `prompt_sha256`.
7. The migration inventory is a coverage register, not a source of field values.
8. The migration script's dry-run mode is read-only. It must not write to the output directory.

## 2. Work-item identity

### 2.1 Supported identity declarations

Identity extraction supports exactly these three declaration shapes:

| Shape | YAML path | Adoption rule |
|---|---|---|
| Primary | `work_item_id` | Accept a non-empty string matching the AID or FIX identifier grammar |
| Legacy top-level | `aid` | Accept a non-empty string matching the AID or FIX identifier grammar |
| Legacy nested | `work_item.proposed_id` | Accept only when `work_item.identifier_status` is present and equals `coordinator_verified_unique_see_identifier_evidence` |

No other identity field or alias is an identity source.

If multiple supported declarations are populated:

- If all values are identical and valid, identity is `KNOWN`; retain every declaration as a candidate.
- If values differ, identity is `UNCONFIRMED`.
- If any populated declaration is malformed, identity is `UNCONFIRMED`.
- If no supported declaration is populated, identity is `UNKNOWN` only when the manifest was read and parsed successfully. If the manifest cannot be read or parsed, identity is `UNCONFIRMED`.

`work_item.proposed_id` without the exact `identifier_status` value above is not an adoptable identity declaration. Preserve it as a candidate with a rejection reason; do not silently promote it.

### 2.2 Identifier grammar

```regex
^(?:AID-[0-9]{4}-[0-9]{3}|FIX-[0-9]{4}-[A-Z0-9]+(?:-[A-Z0-9]+)*)$
```

The manifest directory name is used only as a consistency check against the resolved content identity. It is never an identity source.

A directory/content mismatch is `UNCONFIRMED`. A duplicate resolved ID across two manifest paths is a duplicate-identity conflict and must be reported independently of directory mismatches.

### 2.3 Record population

The canonical manifest population is direct work-item manifests:

```text
14-ai-development/work-items/<AID-or-FIX-directory>/manifest.yaml
```

Do not discover work items by searching arbitrary YAML files for `work_item_id`. Do not treat `authorization-manifest.yaml` as a work-item manifest.

## 3. Registry field states

Each registry field has exactly one state:

- `KNOWN`: one authoritative, validated value.
- `KNOWN_EMPTY`: evidence proves the field was explicitly judged empty.
- `UNKNOWN`: no candidate value or declaration was found, and the relevant source was completely readable.
- `UNDECIDED`: a decision is known to be required but has not been made by the authorized decision-maker.
- `UNCONFIRMED`: candidate evidence exists but is conflicting, malformed, ambiguous, truncated, or not verifiable.
- `NOT_APPLICABLE`: an explicit applicability decision establishes that the field does not apply.

The migration script must not infer `KNOWN_EMPTY`, `UNDECIDED`, or `NOT_APPLICABLE` from a missing YAML key.

## 4. Field authority and candidate rules

The 12 migrated fields are:

```text
work_item_id
title
owner
class
risk
status
prompt_id
prompt_sha256
prompt_status
implementation
review
acceptance
```

### 4.1 `work_item_id`

Use the identity declarations in §2.1.

A valid, unique, consistent identity is `KNOWN`. Conflicting aliases, malformed declarations, unreadable YAML, duplicate identity, or a directory/content mismatch are `UNCONFIRMED`.

### 4.2 `title`

Authority: the YAML-parsed top-level `title` scalar from the manifest.

- A complete, unambiguous scalar is `KNOWN`.
- A missing title in a successfully parsed manifest is `UNKNOWN`.
- A non-scalar, malformed, or ambiguous title is `UNCONFIRMED`.
- An INDEX title is not an authority and cannot override the manifest.
- Do not append text after an unquoted ` #` to a YAML plain scalar. Under YAML syntax, that sequence begins a comment when it occurs as a comment delimiter. The parser's scalar boundary is not permission to reconstruct text from the comment.
- A title affected by an ambiguous or unrecoverable truncation remains `UNCONFIRMED` until independently verifiable source evidence resolves it.

The migration report must retain the source path, line, Git blob SHA, raw scalar evidence, and parser value when available.

### 4.3 `owner`

Recognized accountable-owner locations, in precedence order:

1. `authority.accountable_owner`
2. `governance.accountable_owner`
3. top-level `accountable_owner`
4. top-level `owner`

`attribution` is not an accountable-owner field and must never be used as an owner fallback.

Rules:

- If all populated accountable-owner locations agree, use the highest-precedence populated location and retain all agreeing candidates.
- If populated accountable-owner locations disagree, `owner` is `UNCONFIRMED`.
- If only a lower-precedence location is populated, it may be `KNOWN` with that exact source path recorded.
- If only `attribution` is populated, `owner` is `UNKNOWN`.
- If no recognized accountable-owner location exists in a completely parsed manifest, `owner` is `UNKNOWN`.
- A malformed or unreadable candidate is `UNCONFIRMED`.

### 4.4 `class`

Authority: top-level manifest `class`.

A class value must be a non-empty string matching:

```regex
^[A-Z][A-Z0-9_-]*(?:/[A-Z][A-Z0-9_-]*)*(?:[ ]*\+[ ]*[A-Z][A-Z0-9_-]*(?:/[A-Z][A-Z0-9_-]*)*)*$
```

This grammar permits observed compound forms such as `GATE/TEST`, `DOC/GOVERNANCE`, `GATE/TEST + DOC/GOVERNANCE`, and `ARCH + DOC`.

The following are not valid confirmed class values:

- `NOT_ASSIGNED`
- free-form prose or provisional adjudication notes
- values containing a risk token as a class component, including `ARCH/R1`, `ARCH/R2`, and `ARCH/R3`

In particular, `ARCH/R3` is `UNCONFIRMED`; do not silently rewrite it to `ARCH` or move `R3` into `risk`. A separate authorized adjudication is required to split or correct a mixed value.

A missing class in a successfully parsed manifest is `UNKNOWN`. A malformed or ambiguous value is `UNCONFIRMED`.

### 4.5 `risk`

Authority: top-level manifest `risk`.

Allowed values:

```text
R1
R2
R3
NOT_ASSIGNED
NOT_ADJUDICATED
```

A value outside this exact set is `UNCONFIRMED`; do not infer risk from class, title, or prose.

A missing risk in a successfully parsed manifest is `UNKNOWN`.

### 4.6 `status`

Authority: top-level manifest `status`.

Allowed values:

```text
DISPATCHED
MERGED
REGISTERED
PROPOSED
IMPLEMENTED
VERIFIED
IMPLEMENTED_ACCEPTANCE_PENDING
REMEDIATION_IN_PROGRESS
CLOSED
ADOPTED
COMPLETE
PENDING_FORMAL_REGISTRATION
DRAFT
IMPLEMENTATION_IN_PROGRESS
IN_PROGRESS
```

Matching is exact and case-sensitive.

A value with an appended explanation or free-form tail is not a valid status. For example:

```text
IN_PROGRESS — remediation after unauthorized integration of original PR
```

is `UNCONFIRMED`, not `IN_PROGRESS`.

Do not strip prose, map one status to another, or infer status from GitHub PR state.

A missing status in a successfully parsed manifest is `UNKNOWN`.

### 4.7 `prompt_id`

Registered prompt ID candidates are:

- top-level `prompt_id`
- nested `prompt.id`

If both are populated and equal, the value may be `KNOWN`. If they disagree, the field is `UNCONFIRMED`.

The value must be a non-empty string matching:

```regex
^[A-Za-z0-9][A-Za-z0-9._:/-]{0,255}$
```

Do not derive a prompt ID from a session ID, PR number, work-item ID, or free-form provenance note.

### 4.8 `prompt_sha256`

Registered prompt digest candidates are limited to:

- top-level `prompt_sha256`
- nested `prompt.sha256`
- nested `prompt.prompt_sha256`

A candidate must be a lowercase or uppercase 64-character hexadecimal SHA-256 digest:

```regex
^[0-9A-Fa-f]{64}$
```

A digest becomes `KNOWN` only when all of the following are true:

1. The registered prompt path is explicitly declared by a supported registered prompt-path field.
2. The registered prompt commit is explicitly declared by a supported registered prompt-commit field.
3. The referenced Git blob can be read from that commit.
4. SHA-256 of the exact blob bytes equals the registered digest.
5. All populated registered digest candidates agree.

If any condition fails, use `UNCONFIRMED`.

The following are never candidates for this field:

- `session_evidence.executed_prompt_sha256`
- `prompt.executed_prompt_sha256`
- any other `executed_prompt_sha256` key, regardless of nesting
- any digest described as an executed, submitted, or session prompt digest

These values describe execution evidence, not the registered prompt pin.

### 4.9 `prompt_status`

Registered prompt-status candidates are:

- top-level `prompt_status`
- nested `prompt.prompt_status`

Allowed values:

```text
PINNED
NOT_PRESENT
```

Only exact matches are accepted as `KNOWN`. Any other populated value is `UNCONFIRMED`; missing values in a successfully parsed manifest are `UNKNOWN`.

A `PINNED` status does not itself prove a valid pin. The `prompt_sha256` validation in §4.8 must independently succeed.

### 4.10 `implementation`, `review`, and `acceptance`

Authority: independently maintained registry-notes records:

```text
00-governance/registry-notes/AID-YYYY-NNN.yaml
00-governance/registry-notes/FIX-YYYY-....yaml
```

Legacy INDEX prose is not authoritative and must not be promoted automatically.

- A traceable, schema-valid notes declaration may be `KNOWN`.
- Explicit evidence of an intentionally empty field may be `KNOWN_EMPTY`.
- No notes declaration in a completely scanned notes population is `UNKNOWN`.
- Conflicting notes declarations, malformed notes, or untraceable candidate text are `UNCONFIRMED`.
- `UNDECIDED` and `NOT_APPLICABLE` require explicit authorized declarations.

The initial migration run has no authority to invent implementation, review, or acceptance facts from PR status, commit messages, session metadata, or INDEX prose.

## 5. YAML truncation and raw evidence

The controlling evidence is the original Git blob, not a reconstructed parser value.

For each affected scalar:

1. Retain the source commit, Git blob SHA, source path, line, and raw bytes.
2. Record the scalar boundary according to YAML syntax:
   - quoted scalars end at their matching quote;
   - block scalars end according to YAML indentation and chomping rules;
   - plain scalars end according to YAML token and comment rules.
3. Record the parser-produced value separately.
4. Do not append a comment tail to a plain scalar.
5. Do not use line length, next-key heuristics, or a presumed intended title as an authority.
6. If the raw scalar boundary or intended value cannot be resolved unambiguously, mark the field `UNCONFIRMED`.

The known 14 top-level plain-scalar ` #` cases are:

```text
AID-2026-002:12
AID-2026-002:45
AID-2026-002:46
AID-2026-002:49
AID-2026-003:12
AID-2026-003:56
AID-2026-003:60
AID-2026-014:16
AID-2026-030:10
AID-2026-059:2
AID-2026-064:2
AID-2026-092:6
AID-2026-106:3
AID-2026-174:2
```

The wider 37-case truncation inventory includes nested and other scalar shapes. The migration must inspect all manifest scalar locations, not only the 14 top-level cases.

## 6. Migration inventory semantics

The inventory records identity coverage and migration state. It is not a field-value source.

Allowed states and exact meanings:

- `NOT_MIGRATED`: discovered in the source tree; no registry record has been created.
- `MIGRATED`: registry record exists and passes schema validation.
- `MIGRATED_WITH_UNCONFIRMED_FIELDS`: registry record exists; one or more fields are explicitly `UNCONFIRMED`.
- `EXCLUDED_BY_AUTHORITY`: an authorized source reference and reason explicitly exclude the item.

The inventory must cover every resolvable identity exactly once. An unreadable manifest or unrecoverable identity is an `INCOMPLETE` condition, not an absent work item.

The migration script must validate inventory identity coverage against the selected source tree. It must not treat the inventory's field values or migration labels as field authority.

## 7. Dry-run output contract

For every inventory item and each of the 12 fields, emit:

```json
{
  "state": "KNOWN",
  "authority": "14-ai-development/work-items/AID-2026-001/manifest.yaml",
  "candidates": [
    {
      "source": "manifest.title",
      "path": "14-ai-development/work-items/AID-2026-001/manifest.yaml",
      "line": 2,
      "blob_sha256": "…",
      "value": "…"
    }
  ],
  "reason": "single valid candidate from the authoritative manifest field"
}
```

`authority` is a source path or `null`. Candidate `blob_sha256` is the SHA-256 of the source Git blob bytes, not the SHA-256 of a parsed value.

A dry run must not write registry files, reports, caches, or temporary artifacts into the repository or output directory.

## 8. Stage boundaries

- Stage A: schema and fixtures.
- Stage B: registry validator and inventory consistency checks.
- Stage C: inventory creation and progressive registry migration.
- Stage D: INDEX projection and notes integrity.

The migration script in Stage C does not generate or modify INDEX. INDEX projection is owned by:

```text
scripts/ci/generate_work_item_index.py
scripts/ci/check_work_item_index.py
