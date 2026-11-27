---
document_metadata:
  steward: "Architecture Governance"
  domain: ai-development
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Applicable-To-Current-Version
      evidence_reference:
        - "Live GET /repos/oahcom/AiMemoryBrainArchitecture/branches/main/protection payload, HTTP 200, 7813 bytes, 2026-11-27"
        - "Schema v3 implementation and offline test suite"
        - "Initial baseline experiment: PR #1038, head b5cf4f2578de0e9aa2ba3e7e86a110ce1d8f69d9, run 138943464904"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-27"
      last_verification_note: "Schema v3 is based on the complete branch protection endpoint payload. The recorded fingerprint includes all 12 required fingerprint fields. The observed required_pull_request_reviews key is absent and is represented explicitly as null. The live required-status-check context set contains 16 entries."
    usage_status: Active
    modification_status: Modified
  authority:
    canonical_status: Non-Canonical
    canonical_conflict_status: None
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# Protection Fingerprint Ratchet

## 1. Purpose

This document specifies a fail-closed fingerprint check for the repository's GitHub branch-protection configuration.

The check reads the complete branch-protection endpoint, extracts a defined set of protection properties, and compares them with a repository-controlled baseline. It detects weakening, reports tightening, and rejects incomplete evidence rather than treating missing data as unchanged.

The fingerprint is deliberately limited to the fields defined in schema version 3. A passing result establishes equality or tightening only for those fingerprinted fields; it is not a general certification of every GitHub security setting.

## 2. API boundary and payload shape

The source of truth is:

`GET /repos/{owner}/{repo}/branches/{branch}/protection`

The endpoint response is the protection object itself. It is not wrapped in a `protection` property, and it does not contain the summary endpoint's `protection.enabled` property.

The implementation must therefore read fields directly from the response root. It must not require or synthesize either of these structures:

- `payload.protection`
- `payload.protection.enabled`

The live response calibrated on 2026-11-27 returned HTTP 200 and contained:

- `required_status_checks`
- `required_signatures`
- `enforce_admins`
- `required_linear_history`
- `allow_force_pushes`
- `allow_deletions`
- `block_creations`
- `required_conversation_resolution`
- `lock_branch`
- `allow_fork_syncing`

The `required_pull_request_reviews` key was absent from that response.

A request without `GITHUB_TOKEN` is incomplete. HTTP 403 and HTTP 404—including insufficient permission and non-administrator-token cases—are also incomplete outcomes. The checker must report the HTTP status and return exit code `2`. It must never turn an authorization or not-found response into a passing result.

## 3. Schema version 3 fingerprint

The schema version is `3`. The fingerprint has exactly 12 top-level fields:

| Field | Source in endpoint payload | Type |
|---|---|---|
| `strict` | `required_status_checks.strict` | Boolean |
| `contexts` | `required_status_checks.contexts` | List of unique non-empty strings |
| `required_signatures` | `required_signatures.enabled` | Boolean |
| `enforce_admins` | `enforce_admins.enabled` | Boolean |
| `required_linear_history` | `required_linear_history.enabled` | Boolean |
| `allow_force_pushes` | `allow_force_pushes.enabled` | Boolean |
| `allow_deletions` | `allow_deletions.enabled` | Boolean |
| `block_creations` | `block_creations.enabled` | Boolean |
| `required_conversation_resolution` | `required_conversation_resolution.enabled` | Boolean |
| `lock_branch` | `lock_branch.enabled` | Boolean |
| `allow_fork_syncing` | `allow_fork_syncing.enabled` | Boolean |
| `required_pull_request_reviews` | Root property, when present | Object or explicit `null` for absence |

The `contexts` value is normalized as a sorted set for comparison. API response ordering does not affect the fingerprint. Duplicate or empty context names make the payload incomplete.

For the ten boolean values, the relevant source object and its `enabled` property must both exist and have the expected type. `strict` must exist as a boolean under `required_status_checks`.

### 3.1 Required pull-request reviews: presence is data

`required_pull_request_reviews` has a three-part contract:

1. If the key is absent from the endpoint response, the fingerprint value is `null`.
2. If the key is present, its value must be an object and the object is recorded.
3. If the key is present with `null` or a non-object value, the live payload is incomplete.

Absence is not treated as a missing required field. It is an explicit state of the endpoint and must be stored in the baseline as JSON `null`.

When present, the object is retained as a JSON-compatible object and serialized with stable key ordering. This records `required_approving_review_count` and other returned review-policy properties rather than reducing the object to a single boolean.

### 3.2 Fail-closed completeness

If a field represented in the baseline is missing from the live payload, has an invalid type, or cannot be normalized, the result is `INCOMPLETE` with exit code `2`.

A baseline that does not contain all 12 fields, contains invalid field types, or has invalid experiment metadata is also incomplete.

The checker must not:

- infer a missing value from the baseline;
- substitute a default boolean;
- treat a missing object as `false`;
- treat a present `null` review object as equivalent to an absent key;
- interpret a failed API request as an unchanged configuration.

## 4. Direction rules

Each field has an explicit direction rule. No field may fall through to an implicit default classification.

### 4.1 Boolean fields

The protective polarity is fixed as follows:

| Field | TIGHTENED value | LOOSENED value |
|---|---:|---:|
| `strict` | `true` | `false` |
| `required_signatures` | `true` | `false` |
| `enforce_admins` | `true` | `false` |
| `required_linear_history` | `true` | `false` |
| `allow_force_pushes` | `false` | `true` |
| `allow_deletions` | `false` | `true` |
| `block_creations` | `true` | `false` |
| `required_conversation_resolution` | `true` | `false` |
| `lock_branch` | `true` | `false` |
| `allow_fork_syncing` | `false` | `true` |

A value change toward the protective value is `TIGHTENED`; a value change away from it is `LOOSENED`. Equal values are `UNCHANGED`.

This polarity is applied symmetrically. For example, changing `allow_deletions` from `true` to `false` is tightening, while changing it from `false` to `true` is loosening. Likewise, changing `required_signatures` from `true` to `false` is loosening.

### 4.2 Required contexts

Let \(B\) be the baseline set and \(C\) the current set.

| Condition | Direction |
|---|---|
| \(B = C\) | `UNCHANGED` |
| \(B \subset C\) | `TIGHTENED` |
| \(C \subset B\) | `LOOSENED` |
| Neither set contains the other | `LOOSENED` |

Adding contexts without removing existing contexts is tightening. Removing any baseline context is loosening. A mixed change containing both additions and removals is loosening.

### 4.3 Required pull-request reviews

| Baseline | Current | Direction |
|---|---|---|
| Absent (`null`) | Absent (`null`) | `UNCHANGED` |
| Absent (`null`) | Present object | `TIGHTENED` |
| Present object | Absent (`null`) | `LOOSENED` |
| Same present object | Same present object | `UNCHANGED` |
| Present object with lower approving-review count | Higher count | `TIGHTENED` |
| Present object with higher approving-review count | Lower count | `LOOSENED` |

For changes to a present review object other than a comparable integer `required_approving_review_count` change, the checker conservatively reports `LOOSENED`. This prevents an unrecognized or ambiguous object mutation from being silently accepted as safe. The complete object is still printed and retained in the fingerprint, so the change remains visible for review.

### 4.4 Overall result

The overall classification follows these rules:

- If any field is `LOOSENED`, the overall result is loosening and exit code is `1`.
- If no field is loosened and at least one field is `TIGHTENED`, the overall result is tightening and exit code is `0`.
- If every field is `UNCHANGED`, the overall result is unchanged and exit code is `0`.

Tightening never cancels loosening in another field.

Every tightening must produce a visible notice that the fingerprint baseline should be reviewed and synchronized. The checker does not silently rewrite the baseline during an ordinary comparison.

## 5. CLI and exit-code contract

Implementation:

`scripts/ci/check_protection_fingerprint.py`

Supported arguments:

- `--repo`: repository in `owner/name` form; defaults to `oahcom/AiMemoryBrainArchitecture`.
- `--branch`: branch name; defaults to `main`.
- `--fingerprint`: baseline path; defaults to `scripts/ci/baselines/protection-fingerprint.json`.
- `--write`: explicitly write a new baseline from the live payload.
- `--experiment-pr`
- `--experiment-head`
- `--experiment-run`
- `--experiment-date`

`--write` requires all four experiment arguments. If any is absent or empty, the checker returns exit code `2` without writing a baseline.

Exit codes:

| Exit code | Meaning |
|---|---|
| `0` | All fields unchanged or at least one field tightened, with no loosening |
| `1` | One or more fields loosened |
| `2` | Missing token, HTTP/API error, incomplete live payload, invalid baseline, missing write metadata, or unexpected checker error |

The checker prints one line for each fingerprint field:

`FIELD <name>: recorded=<x> live=<y> DIRECTION=<UNCHANGED|LOOSENED|TIGHTENED>`

The final comparison summary is:

`PROTECTION FINGERPRINT: <n> field(s) changed, <m> loosened, <k> tightened`

Each `TIGHTENED` field also produces a baseline synchronization notice.

HTTP 403 and HTTP 404 must remain distinguishable in the error message and must both return exit code `2`. Neither status may be interpreted as an empty configuration or a pass.

## 6. Baseline and experiment provenance

The baseline is stored at:

`scripts/ci/baselines/protection-fingerprint.json`

It uses schema version `3` and records all 12 fields.

The initial experiment provenance is retained from the earlier baseline experiment:

| Item | Value |
|---|---|
| Pull request | #1038 |
| Head SHA | `b5cf4f2578de0e9aa2ba3e7e86a110ce1d8f69d9` |
| Workflow run | `138943464904` |
| Date | `2026-11-25` |
| Experiment observation | HTTP 405 for required status check `rust-workspace-test` |
| PR disposition | Closed, unmerged |

The schema-v3 fingerprint values are calibrated from the complete endpoint payload observed on 2026-11-27. The absent `required_pull_request_reviews` key is stored explicitly as `null`.

Baseline writes are explicit operations. The writer uses deterministic JSON serialization, sorted object keys, normalized context ordering, a trailing newline, and an atomic replacement. Repeating a write with the same live payload and the same experiment metadata must produce byte-identical output.

A baseline update must be reviewable as a repository change. Normal comparison must never update the baseline.

## 7. CI execution and tests

The offline test suite is:

`scripts/ci/test_check_protection_fingerprint.py`

It must run without network access:

```powershell
cd scripts/ci
python -m unittest -v test_check_protection_fingerprint
```

Tests inject a `payload_fetcher` and cover field-level direction rules, absent/present review-object semantics, incomplete data, HTTP failures, CLI write requirements, and deterministic baseline writing.

The workflow is:

`.github/workflows/protection-fingerprint.yml`

It performs recurring checks using the repository's configured token permissions. A missing or insufficient credential must result in a failing incomplete outcome, not a pass.

## 8. Declared check context versus platform-required contexts

The repository's declared check-context inventory is maintained in:

`14-ai-development/PR-GOVERNANCE-001.md`

Its `declared-check-contexts` list contains 17 entries, including:

`Protection fingerprint`

The live platform `required_status_checks.contexts` set currently contains 16 entries. `Protection fingerprint` is not yet configured as a required platform status check.

These counts describe different contracts:

- The 17-entry declaration is the repository's declared check-context inventory.
- The 16-entry live set is the platform's currently required status-check context set.

`check_declared_check_contexts.py` enforces inclusion: every declared context must be produced by a workflow job. It does not require the declaration to equal the platform-required set.

Therefore, the declaration may contain 17 entries while platform branch protection currently requires 16. The presence of `Protection fingerprint` in the declaration does not mean GitHub already enforces it as a required status check.

The checker must not claim that it is self-enforced by branch protection until a live read confirms that `Protection fingerprint` appears in the platform's required contexts.

## 9. Boundary with Repository hygiene

The protection fingerprint and Repository hygiene checks have separate responsibilities.

The fingerprint check compares selected live branch-protection settings with a repository-controlled baseline.

Repository hygiene checks repository content and governance requirements, including document metadata and manifest consistency.

Neither check substitutes for the other:

- A passing fingerprint check does not establish repository document or manifest compliance.
- A passing Repository hygiene check does not establish that live branch protection has not been weakened.
- A declared workflow context does not establish that GitHub requires that context.

The fingerprint check must not weaken or bypass Repository hygiene requirements.

## 10. Known blind spots and residual risks

### 10.1 Endpoint scope

The fingerprint covers the 12 schema-v3 fields defined in section 3. It does not claim to cover every setting that GitHub may expose through other endpoints or administrative interfaces.

A passing result is evidence only about the recorded fields in the complete branch-protection endpoint response.

### 10.2 Review-object direction

The complete `required_pull_request_reviews` object is retained and compared. The implementation recognizes the monotonic direction of `required_approving_review_count`. Other object mutations are conservatively classified as loosening because their direction cannot safely be inferred from an unreviewed generic JSON difference.

This may produce a conservative loosening classification for a review-object change that is in fact more restrictive. Such a result requires human review; it must not be silently downgraded to unchanged.

### 10.3 Required-context producer identity

The fingerprint compares required context names as a set. The endpoint's `checks` entries also include app IDs, but schema version 3 does not include those app IDs in its 12-field fingerprint.

A context name that remains unchanged while its producing GitHub App identity changes is outside the current fingerprint's detection scope.

### 10.4 Self-enforcement gap

A repository-controlled workflow cannot guarantee that GitHub continues requiring its own check.

At the calibrated state, the declared inventory contains 17 contexts, while the platform requires 16. `Protection fingerprint` is not yet platform-required. This is an explicit enforcement gap.

The scheduled workflow provides recurring observation while it remains enabled and executable. It does not eliminate the risk that the workflow, schedule, permissions, or platform requirement is disabled or removed.

### 10.5 API and credential availability

API outages, rate limits, permission changes, token scope changes, HTTP 403, HTTP 404, transport errors, and response-shape changes can prevent a complete comparison.

All such conditions must fail closed with exit code `2`. In particular, an authorization failure must never be interpreted as proof that the configuration is unchanged.

### 10.6 Baseline governance

A baseline is only as trustworthy as the process that admits changes to it. An unauthorized or inadequately reviewed baseline replacement can make a weakened configuration appear unchanged.

Baseline changes must remain explicit, reviewable, deterministic, and tied to recorded experiment provenance.

## 11. Acceptance criteria

The implementation is acceptable when:

1. It reads the complete `/branches/{branch}/protection` endpoint and treats the response root as the protection object.
2. It fingerprints all 12 schema-v3 fields.
3. It records an absent `required_pull_request_reviews` property as explicit JSON `null`.
4. It rejects a present review property with a non-object value.
5. It rejects any missing or mistyped baseline-recorded live field with exit code `2`.
6. It rejects an incomplete baseline with exit code `2`.
7. It returns exit code `2` for missing credentials and HTTP 403/404, preserving the HTTP status in the diagnostic.
8. It applies explicit protective polarity to every boolean field.
9. It classifies context removal and mixed context changes as loosening, and pure additions as tightening.
10. It classifies review-object absence/presence and approving-review-count changes as specified.
11. It prints a field-level direction line for each of the 12 fields and a final summary.
12. It emits a baseline synchronization notice for every tightened field.
13. It requires all four experiment arguments for `--write`.
14. It writes deterministic, byte-identical baseline output for repeated writes of the same payload and metadata.
15. Its offline tests use an injected payload fetcher and perform no network requests.
16. Its tests detect mutations that remove loosening detection, remove the tightening notice, or allow HTTP 403 to pass.
17. Documentation distinguishes the 17 declared contexts from the 16 currently platform-required contexts and does not claim that `Protection fingerprint` is already required by branch protection.
