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
        - "Live GET /repos/{owner}/{repo}/branches/{branch} payload calibration on 2026-11-27"
        - "Protection fingerprint baseline experiment: PR #1038, head b5cf4f2578de0e9aa2ba3e7e86a110ce1d8f69d9, run 138943464904"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-27"
      last_verification_note: "The checker was validated against the live branch endpoint payload. enabled, enforcement_level, and all 16 required contexts matched the recorded baseline. The documented declared-check-contexts list contains 17 entries, including Protection fingerprint; that context is not yet enabled as a required platform status check."
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

The check detects changes to the branch-protection properties that are observable through the repository branch endpoint and compares them with a repository-controlled baseline. Its purpose is to detect protection weakening without treating every configuration change as equivalent.

The check is deliberately limited to fields that the selected API endpoint actually returns. It does not claim to fingerprint every setting visible in GitHub's branch-protection UI or every setting available through other administrative endpoints.

## 2. API boundary and observed payload

The source of truth used by this implementation is:

`GET /repos/{owner}/{repo}/branches/{branch}`

The live response used for calibration returned HTTP 200 and exposed the following protection fields:

- `protection.enabled`
- `protection.required_status_checks.enforcement_level`
- `protection.required_status_checks.contexts`

The fingerprint consists of exactly those three values:

| Fingerprint field | Meaning |
|---|---|
| `enabled` | Whether branch protection is enabled |
| `enforcement_level` | Required-status-check enforcement level |
| `contexts` | Required status-check context names |

The calibrated live values on 2026-11-27 were:

- `enabled`: `true`
- `enforcement_level`: `everyone`
- `contexts`: 16 entries

The 16 live required contexts matched the recorded baseline as a set. The calibrated comparison result was `MATCH` for all three fingerprint fields.

The observed endpoint response did **not** include the following settings:

- `strict`
- `enforce_admins`
- `allow_force_pushes`
- `allow_deletions`
- `required_linear_history`
- `required_conversation_resolution`
- `required_pull_request_reviews`

These fields must not be fabricated, inferred, or treated as part of this fingerprint. Their absence from this endpoint is an API visibility limitation, not evidence that the corresponding settings are disabled.

If the API response is incomplete or does not contain the required fingerprint fields, the checker must fail closed with an incomplete/error result. Missing data must never be converted into a passing default.

## 3. Fingerprint representation

The baseline is stored at:

`scripts/ci/baselines/protection-fingerprint.json`

The baseline schema version is `2`.

The fingerprint payload contains:

- `enabled`: boolean
- `enforcement_level`: string
- `contexts`: list of required context names

Context names are normalized into a deterministic sorted representation before comparison. This makes the fingerprint independent of the order in which GitHub returns the context list.

The comparison is set-based for `contexts`; duplicate or ordering differences must not create a false configuration change.

The baseline also carries experiment metadata. That metadata records the provenance of the initial baseline and is not itself part of the branch-protection fingerprint.

## 4. Change classification

The checker classifies each comparable field as unchanged, tightened, or loosened. The overall result is derived from the field-level classifications.

### 4.1 Required contexts

Let:

- \(B\) be the recorded baseline context set
- \(C\) be the current live context set

Classification:

| Condition | Classification |
|---|---|
| \(B = C\) | Unchanged |
| \(B \subset C\) | Tightened |
| \(C \subset B\) | Loosened |
| Neither set contains the other | Loosened |

Adding required contexts without removing any existing required context is tightening.

Removing one or more baseline contexts is loosening. A mixed replacement—one or more additions combined with one or more removals—is also classified as loosening. This conservative rule prevents a replacement from being treated as safe merely because the total number of required contexts did not decrease.

### 4.2 Enforcement level

The recognized enforcement ordering is:

`off < non_admins < everyone`

A move upward in this ordering is tightening. A move downward is loosening. An unchanged value is unchanged.

An unrecognized or missing value is not assigned an invented ordering. It makes the fingerprint incomplete and must not produce a passing result.

### 4.3 Protection enabled state

For the boolean `enabled` field:

| Baseline | Current | Classification |
|---|---|---|
| `true` | `true` | Unchanged |
| `false` | `true` | Tightened |
| `true` | `false` | Loosened |
| `false` | `false` | Unchanged |

### 4.4 Overall result

The overall result is:

- `LOOSENED` if any field is classified as loosened
- `TIGHTENED` if no field is loosened and at least one field is tightened
- `UNCHANGED` if all fields match

A simultaneous tightening and loosening is therefore classified as `LOOSENED`. Improvements in one field cannot cancel a regression in another.

## 5. Exit-code contract

The checker exposes three outcomes:

| Exit code | Meaning | CI interpretation |
|---|---|---|
| `0` | Unchanged or tightened | Pass |
| `1` | At least one loosened field | Fail |
| `2` | Incomplete data, invalid baseline, API failure, or other checker error | Fail closed |

Exit code `2` is not a warning and must not be treated as success.

In particular:

- An HTTP error must not be converted into an empty protection object.
- A missing `protection` object must not be interpreted as a disabled-but-valid configuration.
- Missing required fields must not be filled with baseline values.
- Invalid JSON or an invalid baseline must not be accepted as unchanged.
- A failed API request must not silently reuse a cached live value.

The checker reports the number of changed, loosened, and tightened fields so that the result can be audited from CI output.

## 6. Baseline creation and experiment provenance

The baseline is repository-controlled. A candidate must not be able to redefine the baseline as an incidental side effect of an ordinary check.

Baseline writing is an explicit experiment operation. The checker requires the experiment metadata arguments when invoked with `--write`; normal checking does not rewrite the baseline.

The initial baseline experiment is recorded as:

| Item | Value |
|---|---|
| Pull request | #1038 |
| Head SHA | `b5cf4f2578de0e9aa2ba3e7e86a110ce1d8f69d9` |
| Workflow run | `138943464904` |
| Date | `2026-11-25` |
| Experiment observation | HTTP 405 for the required status check `rust-workspace-test` |
| PR disposition | Closed, unmerged |

The experiment metadata records provenance; it does not change the classification rules or make a failing required check acceptable.

Any future baseline update must be an explicit, reviewable repository change with the experiment provenance recorded. A live value must not automatically become the new baseline merely because it differs from the current one.

## 7. CI execution

The protection fingerprint check is implemented by:

`scripts/ci/check_protection_fingerprint.py`

Its offline tests are implemented by:

`scripts/ci/test_check_protection_fingerprint.py`

The workflow is:

`.github/workflows/protection-fingerprint.yml`

The workflow has a daily scheduled execution at:

`0 3 * * *`

It also supports explicit workflow dispatch. The scheduled check provides recurring detection of out-of-band branch-protection changes that do not necessarily arrive through a repository commit.

The workflow obtains its API credential from `GITHUB_TOKEN`. The token must have sufficient permission to read repository branch-protection data. API permission failures are incomplete/error outcomes, not successful checks.

The offline test suite exercises the classification and fail-closed behavior without requiring a live GitHub API call. The live endpoint check is a separate validation of the actual repository payload.

## 8. Declared check context versus platform-required contexts

The repository's declared check-context inventory is maintained in:

`14-ai-development/PR-GOVERNANCE-001.md`

Its `declared-check-contexts` list currently contains 17 entries. The additional entry is:

`Protection fingerprint`

The platform's live `required_status_checks.contexts` currently contains 16 entries. `Protection fingerprint` is **not yet enabled as a required platform status check**.

These two counts describe different things and must not be conflated:

- The 17-entry governance declaration records the intended/declared check-context inventory.
- The 16-entry live API value records the contexts currently configured as required by platform branch protection.

The `check_declared_check_contexts.py` contract is inclusion-based: each declared context must be produced by a workflow job. It does not require the declaration list to equal the live branch-protection context list.

Consequently, the 17-entry declaration can be valid while the platform still requires only 16 contexts. The existence of `Protection fingerprint` in the declaration does not establish that GitHub currently enforces it as a required status check.

This document therefore makes no claim that the protection fingerprint check is already a required platform status check. Any future change to make it required must be separately applied and verified against the live branch endpoint.

## 9. Boundary with Repository hygiene

The protection fingerprint check and Repository hygiene serve different purposes.

The fingerprint check observes a limited set of live branch-protection settings and compares them against a recorded baseline.

Repository hygiene governs repository content and repository-level policy requirements. It remains responsible for its own checks, including document and manifest validation.

Neither check substitutes for the other:

- A passing fingerprint check does not establish that repository files comply with governance requirements.
- A passing Repository hygiene check does not establish that live branch protection has not been weakened.
- A declaration that a check context exists does not establish that the platform requires that context.

The fingerprint check must not modify Repository hygiene policy or weaken its admission rules.

## 10. Known blind spots and residual risks

### 10.1 Endpoint visibility

The fingerprint covers only `enabled`, `enforcement_level`, and `contexts` as returned by the selected branch endpoint.

It does not verify settings omitted from that response, including administrator enforcement, force-push restrictions, deletion restrictions, linear-history requirements, conversation resolution, strict status checks, or pull-request review requirements.

A passing result must not be described as proof that all branch-protection settings are secure.

### 10.2 Required-context identity

The `contexts` field is compared by context name. The selected endpoint also returned a `checks` representation containing context/app-id pairs, but that representation is not part of schema version 2's fingerprint.

Therefore this fingerprint does not establish the identity of the GitHub App that produces a required context. A context name that remains unchanged while its producer identity changes is outside this check's detection scope.

### 10.3 Self-removal and enforcement gap

A repository-controlled workflow cannot, by itself, guarantee that GitHub will continue requiring that workflow's check.

If the `Protection fingerprint` context is removed from platform branch protection, or if the workflow is otherwise prevented from running, the check may no longer be an effective enforcement barrier.

At the current calibrated state, the declared context list has 17 entries but the platform requires 16; `Protection fingerprint` is not among those 16 required contexts. This is an explicit enforcement gap, not a successful proof of self-protection.

The daily schedule provides recurring observation while the workflow remains enabled and executable. It does not eliminate the risk that the workflow or its schedule is disabled, that permissions are removed, or that the check is no longer required by the platform.

### 10.4 Baseline governance

A baseline is only as trustworthy as the process that admits changes to it. If an unauthorized or inadequately reviewed change replaces the baseline, the checker may faithfully compare against an untrustworthy reference.

Baseline changes must therefore remain explicit, reviewable, and tied to recorded experiment evidence. The checker must not self-approve or silently absorb regressions into the baseline.

### 10.5 API and credential availability

GitHub API outages, rate limits, permission changes, response-shape changes, and credential failures can prevent a complete comparison.

These conditions must produce an error/incomplete result. They must not be interpreted as evidence that protection is unchanged.

## 11. Acceptance criteria

The implementation is acceptable when all of the following hold:

1. The checker reads the live branch endpoint and fingerprints only `enabled`, `enforcement_level`, and `contexts`.
2. The baseline is schema version 2 and is normalized consistently with the live payload.
3. Context additions without removals are classified as tightening.
4. Context removals and mixed additions/removals are classified as loosening.
5. Enforcement-level changes follow the documented ordering.
6. Disabling protection is classified as loosening; enabling it is classified as tightening.
7. Any loosening produces exit code `1`.
8. Unchanged or tightened configurations produce exit code `0`.
9. Missing or invalid data, API failures, and invalid baselines produce exit code `2`.
10. The checker does not silently rewrite the baseline during normal execution.
11. Offline tests cover the classification rules and prove that incomplete data cannot become a pass.
12. Documentation distinguishes the 17 declared check contexts from the 16 currently required platform contexts and does not claim that `Protection fingerprint` is already platform-required.

The calibrated live comparison on 2026-11-27 produced:

`PROTECTION FINGERPRINT: 0 field(s) changed, 0 loosened, 0 tightened`

with exit code `0`. This confirms that the three currently fingerprinted fields matched the recorded baseline at the time of that observation. It does not verify the settings outside the fingerprint's scope or close the required-context enforcement gap described above.
