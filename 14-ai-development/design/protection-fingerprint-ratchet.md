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
        - "Live GET /repos/oahcom/AiMemoryBrainArchitecture/branches/main summary payload, observed 2026-11-27"
        - "Schema v4 implementation and offline test suite"
        - "Initial baseline experiment: PR #1038, head b5cf4f2578de0e9aa2ba3e7e86a110ce1d8f69d9, run 138943464904"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-27"
      last_verification_note: "Schema v4 records the complete 12-field /protection fingerprint and the three-field branch-summary fingerprint separately. The full endpoint's required_pull_request_reviews key is absent and is represented explicitly as null. Both endpoint context sets contain the same 16 entries."
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

This document specifies a two-endpoint fingerprint check for the repository's GitHub branch-protection configuration.

The checker prefers the complete branch-protection endpoint. If the caller cannot read that endpoint because of an authorization or visibility response, `--endpoint auto` visibly degrades to the branch summary endpoint. The summary endpoint has a smaller evidence surface; the checker compares only its three independently baselined fields and explicitly reports the eleven full-endpoint fields it could not verify.

The two endpoint fingerprints are separate evidence contracts. A summary value must never be substituted for, inferred as, or written into a full-endpoint field.

The check detects weakening, reports tightening, and rejects incomplete evidence rather than treating missing data as unchanged.

## 2. API boundary and endpoint selection

### 2.1 Full endpoint

The complete source is:

`GET /repos/{owner}/{repo}/branches/{branch}/protection`

The response is the protection object itself. It is not wrapped in a `protection` property, and it does not contain the summary endpoint's `protection.enabled` property.

The implementation reads fields directly from the response root. It must not require or synthesize:

- `payload.protection`
- `payload.protection.enabled`

### 2.2 Summary endpoint

The summary source is:

`GET /repos/{owner}/{repo}/branches/{branch}`

The summary response exposes the branch's protection summary under `protection`. The checker reads only:

- `protection.enabled`
- `protection.required_status_checks.contexts`
- `protection.required_status_checks.enforcement_level`

The summary endpoint's contexts are normalized as a sorted set. It does not provide the other eleven fields in the full fingerprint.

### 2.3 Endpoint modes

The CLI accepts:

| Mode | Behavior |
|---|---|
| `--endpoint auto` | Default. Try `/protection` first; on HTTP 401, 403, or 404, use the branch summary endpoint. |
| `--endpoint full` | Require the complete `/protection` endpoint. Any HTTP 401, 403, or 404 is incomplete evidence and returns exit code `2`. |
| `--endpoint summary` | Force the branch summary endpoint; do not request `/protection`. |

In `auto` mode, HTTP 401, 403, and 404 are the only statuses that trigger summary fallback. Other HTTP statuses, transport failures, invalid JSON, and incomplete payloads return exit code `2`.

A missing `GITHUB_TOKEN` is not rejected before making the full request in `auto` mode. The request is made without an Authorization header. GitHub may return HTTP 401; that status triggers the same visible summary fallback as 403 or 404. In `full` mode, a missing token returns exit code `2`.

Fallback does not mean the full check passed. It means the run obtained a smaller but useful evidence set and explicitly reports that reduced coverage.

## 3. Schema version 4

The baseline uses schema version `4` and contains two separate fingerprint objects.

### 3.1 Full fingerprint

`fingerprint` contains exactly the twelve schema-v3 fields. Their meanings and direction rules are unchanged.

| Field | Source in `/protection` response | Type |
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

The `contexts` value is normalized as a sorted set. Duplicate or empty context names make the payload incomplete.

For boolean values, the source object and its `enabled` property must exist and have the expected type. `strict` must exist as a boolean under `required_status_checks`.

### 3.2 Summary fingerprint

`summary_fingerprint` contains exactly three fields:

| Field | Source in branch summary response | Type |
|---|---|---|
| `enabled` | `protection.enabled` | Boolean |
| `contexts` | `protection.required_status_checks.contexts` | List of unique non-empty strings |
| `enforcement_level` | `protection.required_status_checks.enforcement_level` | One of `off`, `non_admins`, `everyone` |

The calibrated summary baseline is:

- `enabled`: `true`
- `contexts`: the same normalized 16-entry context set recorded in `fingerprint.contexts`
- `enforcement_level`: `everyone`

The two `contexts` values are stored separately because they come from different endpoint responses. They must not be merged or treated as a single shared field.

`enforcement_level` uses this explicit ordering:

| Value | Rank |
|---|---:|
| `off` | 0 |
| `non_admins` | 1 |
| `everyone` | 2 |

An unknown or missing enforcement level is incomplete evidence and returns exit code `2`. The checker must not guess a rank for an unrecognized value.

### 3.3 Baseline completeness

Both `fingerprint` and `summary_fingerprint` must exist in every schema-v4 baseline and must contain exactly their defined fields.

A missing section, missing field, extra field, invalid type, duplicate context, invalid enforcement level, or incomplete experiment metadata makes the baseline incomplete and returns exit code `2`.

This requirement applies even when a particular run selects only one endpoint. A full-only run does not excuse a missing summary baseline, and a summary-only run does not excuse a missing full baseline.

The checker must not:

- infer a missing value from the other endpoint;
- substitute a default boolean;
- treat a missing object as `false`;
- treat a present `null` review object as equivalent to an absent key;
- interpret a failed API request as an unchanged configuration;
- use `strict` as a substitute for `enforcement_level`;
- use `protection.enabled` as a substitute for any full fingerprint field.

## 4. Direction rules

### 4.1 Full fingerprint boolean fields

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

### 4.2 Full fingerprint contexts

Let \(B\) be the baseline set and \(C\) the current set.

| Condition | Direction |
|---|---|
| \(B = C\) | `UNCHANGED` |
| \(B \subset C\) | `TIGHTENED` |
| \(C \subset B\) | `LOOSENED` |
| Neither set contains the other | `LOOSENED` |

Adding contexts without removing existing contexts is tightening. Removing any baseline context is loosening. A mixed change containing both additions and removals is loosening.

### 4.3 Required pull-request reviews

`required_pull_request_reviews` has a three-part contract:

1. If the key is absent from the full endpoint response, the fingerprint value is `null`.
2. If the key is present, its value must be an object and the object is recorded.
3. If the key is present with `null` or a non-object value, the live payload is incomplete.

Absence is an explicit state and is stored in the baseline as JSON `null`.

When present, the object is retained as a JSON-compatible object and serialized with stable key ordering. The checker recognizes the monotonic direction of an integer `required_approving_review_count` change. An increase is tightening and a decrease is loosening. Other mutations to a present review object are conservatively classified as loosening.

### 4.4 Summary `enabled`

For `summary_fingerprint.enabled`:

- `true` to `false` is `LOOSENED`.
- `false` to `true` is `TIGHTENED`.
- Equal values are `UNCHANGED`.

### 4.5 Summary contexts

Summary contexts use the same set-direction rule as full contexts:

- no change is `UNCHANGED`;
- pure additions are `TIGHTENED`;
- any removal, including a mixed addition/removal, is `LOOSENED`.

### 4.6 Summary enforcement level

The summary enforcement direction follows the rank table in section 3.2:

- a rank increase is `TIGHTENED`;
- a rank decrease is `LOOSENED`;
- equal ranks are `UNCHANGED`;
- an unknown value is incomplete and returns exit code `2`.

### 4.7 Overall result

For either endpoint comparison:

- If any comparable field is `LOOSENED`, the run returns exit code `1`.
- If no field is loosened and at least one field is `TIGHTENED`, the run returns exit code `0`.
- If every comparable field is `UNCHANGED`, the run returns exit code `0`.

Tightening never cancels loosening in another field.

Every tightening must produce a visible notice that the corresponding baseline should be reviewed and synchronized. The checker does not silently rewrite the baseline during an ordinary comparison.

## 5. Visible degraded-mode contract

When `auto` receives HTTP 401, 403, or 404 from `/protection`, it must:

1. Print an explicit degraded-mode diagnostic identifying the full-endpoint HTTP status.
2. Request the branch summary endpoint.
3. Validate and compare all three summary fields against `summary_fingerprint`.
4. Print one `FIELD` direction line for each of `enabled`, `contexts`, and `enforcement_level`.
5. Print exactly eleven `UNVERIFIABLE` lines in this fixed order:

   1. `strict`
   2. `required_signatures`
   3. `enforce_admins`
   4. `required_linear_history`
   5. `allow_force_pushes`
   6. `allow_deletions`
   7. `block_creations`
   8. `required_conversation_resolution`
   9. `lock_branch`
   10. `allow_fork_syncing`
   11. `required_pull_request_reviews`

Each line has this form:

`UNVERIFIABLE <field> (requires Administration read on /protection)`

The run also prints a note naming the full-baseline fields not re-verified in this run:

`NOTE: baseline fields not re-verified this run: ...`

The final line is exactly:

`PROTECTION FINGERPRINT: DEGRADED MODE — 3 field(s) verifiable, 11 unverifiable`

A degraded run is not automatically a failure. If the three summary fields are unchanged or tightened, exit code is `0`. If any summary field is loosened, exit code is `1`. If the summary request or summary payload is incomplete, exit code is `2`.

The degraded result must never be described as a successful verification of the twelve full-endpoint fields.

## 6. CLI and exit-code contract

Implementation:

`scripts/ci/check_protection_fingerprint.py`

Supported arguments:

- `--repo`: repository in `owner/name` form; defaults to `oahcom/AiMemoryBrainArchitecture`.
- `--branch`: branch name; defaults to `main`.
- `--fingerprint`: baseline path; defaults to `scripts/ci/baselines/protection-fingerprint.json`.
- `--endpoint`: one of `auto`, `full`, or `summary`; defaults to `auto`.
- `--write`: explicitly update the selected endpoint's baseline section.
- `--experiment-pr`
- `--experiment-head`
- `--experiment-run`
- `--experiment-date`

`--write` requires all four experiment arguments. If any is absent or empty, the checker returns exit code `2` without writing a baseline.

Exit codes:

| Exit code | Meaning |
|---|---|
| `0` | Comparable fields are unchanged or tightened, with no loosening |
| `1` | One or more comparable fields are loosened |
| `2` | Missing required evidence, non-fallback API error, invalid baseline, incomplete payload, missing write metadata, or unexpected checker error |

`--endpoint full` never falls back. HTTP 401, 403, or 404 returns exit code `2`.

`--endpoint summary` requests only the summary endpoint.

`--endpoint auto` first requests the full endpoint and falls back only for HTTP 401, 403, or 404. A transport error or another HTTP status is not a fallback condition.

## 7. Baseline writes and provenance

The baseline is stored at:

`scripts/ci/baselines/protection-fingerprint.json`

Schema version `4` records:

- `fingerprint`: the complete twelve-field `/protection` baseline;
- `summary_fingerprint`: the independent three-field branch-summary baseline;
- `experiment`: provenance metadata.

Both sections are mandatory.

`--write` updates only the section corresponding to the endpoint used:

| Effective endpoint | Section updated | Section preserved |
|---|---|---|
| Full success | `fingerprint` | `summary_fingerprint` |
| Forced summary | `summary_fingerprint` | `fingerprint` |
| Auto fallback | `summary_fingerprint` | `fingerprint` |

The unselected section's JSON value must remain unchanged. In particular, a degraded write must not clear, replace, synthesize, or otherwise modify any of the twelve full-fingerprint values.

A write requires the complete existing schema-v4 baseline. It must not bootstrap a missing section from the live endpoint or from the other section.

The writer uses deterministic JSON serialization, sorted object keys, normalized context ordering, a trailing newline, and atomic replacement. Repeating a write with the same selected live payload and experiment metadata must produce byte-identical output.

The initial experiment provenance is retained from the earlier baseline experiment:

| Item | Value |
|---|---|
| Pull request | #1038 |
| Head SHA | `b5cf4f2578de0e9aa2ba3e7e86a110ce1d8f69d9` |
| Workflow run | `138943464904` |
| Date | `2026-11-25` |
| Experiment observation | HTTP 405 for required status check `rust-workspace-test` |
| PR disposition | Closed, unmerged |

Baseline changes must remain explicit, reviewable, deterministic, and tied to recorded experiment provenance.

## 8. CI execution and tests

The offline test suite is:

`scripts/ci/test_check_protection_fingerprint.py`

It must run without network access:

```powershell
cd scripts/ci
python -m unittest -v test_check_protection_fingerprint
```

Tests inject both endpoint fetchers. They cover the full-field direction rules, summary-field direction rules, endpoint selection, fallback HTTP statuses, unknown enforcement values, baseline completeness, preservation of the unselected baseline section, write requirements, and deterministic output.

The scheduled workflow is:

`.github/workflows/protection-fingerprint.yml`

It runs on pushes to `main`, on its daily schedule, and through manual dispatch. It does not run on `pull_request` events and is not a required status check.

The workflow uses `secrets.GITHUB_TOKEN`. Its normal permission set does not grant Administration read access to `/protection`, so the expected run may be degraded. The checker output's final `PROTECTION FINGERPRINT:` line is copied into `$GITHUB_STEP_SUMMARY`. The workflow preserves the checker exit status: a detected loosening remains a failing run, while an unchanged degraded comparison can pass with its coverage gap explicitly visible.

## 9. Why degrade instead of fail

The default workflow credential is `GITHUB_TOKEN`. Under the current permission model, it cannot obtain Administration read access to the complete `/protection` endpoint. The following eleven fields are therefore permanently unverifiable through that credential:

- `strict`
- `required_signatures`
- `enforce_admins`
- `required_linear_history`
- `allow_force_pushes`
- `allow_deletions`
- `block_creations`
- `required_conversation_resolution`
- `lock_branch`
- `allow_fork_syncing`
- `required_pull_request_reviews`

The summary endpoint still exposes three useful fields: `protection.enabled`, `required_status_checks.contexts`, and `required_status_checks.enforcement_level`. Failing every scheduled run solely because the workflow credential cannot read the full endpoint would discard this available evidence. Silently treating the summary as the full fingerprint would overstate what was verified.

The selected behavior is visible degradation:

1. Try the full endpoint first.
2. On HTTP 401, 403, or 404, query the summary endpoint.
3. Compare its three fields with the independent `summary_fingerprint` baseline.
4. Print the eleven `UNVERIFIABLE` lines and the note naming the unverified full-baseline fields.
5. End with the explicit degraded-mode summary showing three verifiable and eleven unverifiable fields.

This makes the coverage gap part of the run's ordinary output and GitHub Actions summary. A green degraded run means only that the three summary fields were not loosened. It does not mean that the eleven full-endpoint fields were checked or unchanged.

If an Administration-read PAT is provisioned for this workflow, the operator must deliberately switch the invocation to:

```bash
python3 scripts/ci/check_protection_fingerprint.py \
  --repo "${GITHUB_REPOSITORY}" \
  --branch main \
  --endpoint full
```

The switch must be recorded as evidence in the same reviewed change that provisions or references the credential. That evidence must identify the credential's intended permission scope without disclosing its value, the workflow/configuration change selecting `--endpoint full`, the approving change or PR, and a successful full-endpoint run showing all twelve field comparisons. This is necessary because changing the endpoint mode changes the evidence contract and removes the explicit degraded-mode warning; an unrecorded switch could make a workflow appear to have complete coverage without demonstrating that the credential can actually read the endpoint.

The workflow remains non-required and has no `pull_request` trigger. Degraded operation is an observability policy, not a PR merge gate.

## 10. Declared check context versus platform-required contexts

The repository's declared check-context inventory is maintained in:

`14-ai-development/PR-GOVERNANCE-001.md`

Its `declared-check-contexts` list contains 17 entries, including:

`Protection fingerprint`

The live platform `required_status_checks.contexts` set currently contains 16 entries. `Protection fingerprint` is not configured as a required platform status check and is intentionally not being made required.

These counts describe different contracts:

- The 17-entry declaration is the repository's declared check-context inventory.
- The 16-entry live set is the platform's currently required status-check context set.

`check_declared_check_contexts.py` enforces inclusion: every declared context must be produced by a workflow job. It does not require the declaration to equal the platform-required set.

Therefore, the declaration may contain 17 entries while platform branch protection currently requires 16. The presence of `Protection fingerprint` in the declaration does not mean GitHub enforces it as a required status check. Its declaration records the workflow's check context and producer contract; it does not opt the check into PR merge enforcement.

## 11. Boundary with Repository hygiene

The protection fingerprint and Repository hygiene checks have separate responsibilities.

The fingerprint check compares selected live branch-protection settings with repository-controlled full and summary baselines.

Repository hygiene checks repository content and governance requirements, including document metadata and manifest consistency.

Neither check substitutes for the other:

- A passing full fingerprint check does not establish repository document or manifest compliance.
- A passing degraded summary check establishes only the three summary fields and does not establish that the eleven full-endpoint fields are unchanged.
- A passing Repository hygiene check does not establish that live branch protection has not been weakened.
- A declared workflow context does not establish that GitHub requires that context.

The fingerprint check must not weaken or bypass Repository hygiene requirements.

## 12. Known blind spots and residual risks

### 12.1 Endpoint scope

The full fingerprint covers the twelve schema-v4 full-endpoint fields. The summary fingerprint covers only the three summary fields. Neither claims to cover every setting that GitHub may expose through other endpoints or administrative interfaces.

A full-mode passing result is evidence about the twelve recorded full fields. A degraded-mode passing result is evidence only about the three recorded summary fields.

### 12.2 Review-object direction

The complete `required_pull_request_reviews` object is retained and compared in full mode. The implementation recognizes the monotonic direction of `required_approving_review_count`. Other object mutations are conservatively classified as loosening because their direction cannot safely be inferred from an unreviewed generic JSON difference.

### 12.3 Required-context producer identity

Both fingerprints compare required context names as sets. The full endpoint's `checks` entries also include app IDs, but schema version 4 does not include those app IDs in either fingerprint.

A context name that remains unchanged while its producing GitHub App identity changes is outside the current fingerprint's detection scope.

### 12.4 Self-enforcement gap

The protection fingerprint workflow is intentionally not a required PR check. Its declaration in the 17-entry context inventory does not make it platform-required.

The scheduled workflow provides recurring observation while it remains enabled and executable. It does not eliminate the risk that the workflow, schedule, permissions, or platform access is disabled or removed.

The daily schedule also creates a detection interval: a protection change may not be observed until the next successful scheduled run. Degraded runs further leave the eleven full-endpoint fields unverified.

### 12.5 API and credential availability

API outages, rate limits, permission changes, token scope changes, transport errors, and response-shape changes can prevent a comparison.

Only HTTP 401, 403, and 404 from the full endpoint trigger automatic summary fallback. Other HTTP statuses and transport errors return exit code `2`. A failure of the summary request or an incomplete summary payload also returns exit code `2`.

The degraded-mode output must not be suppressed or summarized as a full success. The eleven `UNVERIFIABLE` lines and final degraded-mode line are mandatory evidence of reduced coverage.

### 12.6 Baseline governance

A baseline is only as trustworthy as the process that admits changes to it. An unauthorized or inadequately reviewed baseline replacement can make a weakened configuration appear unchanged.

The two baseline sections must remain endpoint-specific. Updating one section must preserve the other section's values. A partial write must never convert unverified data into a new baseline.

## 13. Acceptance criteria

The implementation is acceptable when:

1. It supports `--endpoint auto`, `--endpoint full`, and `--endpoint summary`, with `auto` as the default.
2. `auto` tries `/branches/{branch}/protection` first and falls back only for HTTP 401, 403, or 404.
3. `full` never falls back and returns exit code `2` for HTTP 401, 403, or 404.
4. `summary` calls only `/branches/{branch}`.
5. The schema-v4 baseline requires both endpoint-specific sections and all fields in each section.
6. The full fingerprint retains the twelve schema-v3 fields and their existing direction rules.
7. The summary fingerprint contains `enabled`, `contexts`, and `enforcement_level`.
8. Summary enforcement uses the ordered values `off`, `non_admins`, and `everyone`; unknown values return exit code `2`.
9. Degraded mode compares all three summary fields and returns exit code `1` for any loosening.
10. Degraded mode prints the eleven `UNVERIFIABLE` lines in the specified order and the baseline non-verification note.
11. Degraded mode ends with `PROTECTION FINGERPRINT: DEGRADED MODE — 3 field(s) verifiable, 11 unverifiable`.
12. A missing token in auto mode can trigger HTTP 401 fallback; a missing token in full mode returns exit code `2`.
13. Full writes update only `fingerprint`; summary and degraded writes update only `summary_fingerprint`.
14. A write preserves the unselected fingerprint section's JSON value.
15. The baseline writer is deterministic and atomic.
16. The offline tests inject fetchers and perform no network requests.
17. The workflow has no `pull_request` trigger and is not a required status check.
18. The workflow copies the checker's final `PROTECTION FINGERPRINT:` line into `$GITHUB_STEP_SUMMARY` and preserves the checker exit status.
19. The documentation distinguishes the 17 declared contexts from the 16 currently platform-required contexts.
20. A future switch to an Administration-read PAT and `--endpoint full` is recorded in a reviewed change and supported by a successful full-endpoint run.
