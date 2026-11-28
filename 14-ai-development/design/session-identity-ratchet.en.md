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
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Implementation and repository enforcement have not yet been independently verified."
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
    canonical_scope: "English-language counterpart of the Session Identity Ratchet design specification."
    canonical_scope_id: ai-development/session-identity-ratchet-en
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# Session Identity Ratchet

- Document ID: SESSION-IDENTITY-RATCHET
- Version: 1.0
- Status: DRAFT
- Scope: Governance infrastructure
- Implementation: `scripts/ci/check_session_identity.py`
- Required context: `Session identity ratchet`

## 1. Problem statement

The existing Session Evidence validator establishes structural validity.
It does not establish that a claimed session identifier represents a
syntactically identifiable session.

The measured repository inventory establishes the need for an incremental
control:

- 132 manifests exist.
- 93 manifests contain session_evidence.
- There are 104 session evidence entries.
- Only 5 entries contain parseable UUID session identifiers.
- 39 entries contain sentinel values.
- 60 entries contain human-readable labels.
- 64 entries claim RECORDED, but only 5 contain UUIDs.
- 11 entries claim RECORDED while containing sentinels.
- 12 entries claim NOT_RECORDED while containing human-readable labels.

A hard replacement of the existing validator would turn historical
inconsistency into a repository-wide blocking failure.

That is not an acceptable migration strategy.

## 2. Why a ratchet instead of a one-time repair

The session identity ratchet introduces a new independently enforced
check without changing the existing Session Evidence validator.

The existing violations are frozen into a generated baseline.

The baseline is an explicit inventory of historical exceptions, not an
approval of those exceptions.

The enforcement rule is:

1. A violation present in the baseline is reported but does not block.
2. A violation absent from the baseline blocks.
3. Fixing a violation removes it from the current violation set.
4. The corresponding baseline entry must then be removed.
5. A baseline entry that no longer corresponds to an actual violation
   is stale and blocks until the baseline is reduced.
6. Baseline expansion is forbidden.
7. Invalid YAML is never suppressible.

This allows existing work items to remain usable while ensuring that
newly introduced identity defects cannot silently accumulate.

The migration therefore moves monotonically toward zero violations.

## 3. Parseable session identity

The checker accepts three identifier representations: UUID v4, UUID v8,
and platform conversation identifiers.

### 3.1 UUID v4 and UUID v8

A canonical 36-character UUID is accepted when its version and variant
bits satisfy one of the following formats:

- UUID v4: version nibble is `4`.
- UUID v8: version nibble is `8`.

Both versions must satisfy the RFC 4122 variant requirement:

- The variant nibble must be `8`, `9`, `A` or `B`.

The complete UUID layout is:

- 8 hexadecimal characters
- hyphen
- 4 hexadecimal characters
- hyphen
- version nibble `4` or `8`, followed by 3 hexadecimal characters
- hyphen
- RFC variant nibble `8`, `9`, `A` or `B`, followed by 3 hexadecimal characters
- hyphen
- 12 hexadecimal characters

Examples:

UUID v4:

`550e8400-e29b-41d4-a716-446655440000`

UUID v8:

`6b09360b-13cc-83ec-abfd-aa0e6362566c`

Existing repository session identifiers, including:

- `6b092534-81b4-83ec-a4de-49c5c6ecaa8b`
- `6b090a00-c1b0-83ec-ad26-9668c882a144`
- `6b0926ee-d24c-83ec-9ce4-69e18656db14`
- `6b092946-cf54-83ec-81bc-cb7e7993ed28`

are valid UUID v8 identifiers.

UUID versions other than 4 and 8 are rejected.

UUIDs with variant nibbles outside `8`, `9`, `A` and `B` are rejected.

The checker validates the complete format, including version and variant
bits, rather than merely checking the UUID length or hexadecimal layout.

### 3.2 Conversation identifier

A conversation identifier in this form:

`conv_<32-or-more-hexadecimal-characters>`

Example:

`conv_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`

The prefix is case-insensitive. The hexadecimal suffix must contain
at least 32 characters.

### 3.3 Explicit exclusions

The following are not parseable session identifiers:

- `S6-B`
- `ChatGPT-GPT-6`
- `opencode-go/deepseek-v4.1-flash`
- UUID v3 identifiers
- UUIDs with non-RFC variant bits
- `NOT_RECORDED`
- `NOT_AVAILABLE`
- `NOT_EXPOSED_BY_PLATFORM`
- arbitrary labels and arbitrary non-empty strings

Parseability proves only conformity to an accepted identifier format.
It does not prove that the session actually existed or that its evidence
is authentic.

## 4. Status consistency

Two status values are accepted:

- `RECORDED`
- `NOT_RECORDED`

The following invariants apply.

| Status | implementing_ai_session | Result |
|---|---|---|
| RECORDED | UUID v4 | Valid |
| RECORDED | conv_ identifier | Valid |
| RECORDED | Sentinel | Invalid |
| RECORDED | Human label | Invalid |
| NOT_RECORDED | Sentinel | Valid |
| NOT_RECORDED | Human label | Invalid |
| NOT_RECORDED | UUID or conv_ identifier | Invalid |

A missing required field is independently invalid.

Sentinel values are compared case-insensitively after trimming
surrounding whitespace.

## 5. Violation codes

### SESSION_UNPARSEABLE

The status is RECORDED, but the supplied value is neither an accepted
UUID v4 nor an accepted conversation identifier.

Examples:

- RECORDED + S6-B
- RECORDED + ChatGPT-GPT-6

### SESSION_SENTINEL_MISMATCH

The status is NOT_RECORDED, but the value is not a recognized sentinel.

This prevents human-readable labels from being represented as an
unrecorded session.

### SESSION_RECORDED_SENTINEL

The status is RECORDED, but the value is a recognized sentinel.

This is reported separately from SESSION_UNPARSEABLE because it is
a direct contradiction between the declaration and the value.

### Additional structural violations

- SESSION_FIELD_MISSING: a required field is absent, null, empty,
  or has an invalid entry structure.
- SESSION_STATUS_INVALID: an unsupported status is declared.
- SESSION_YAML_INVALID: the manifest cannot be parsed or its
  top-level structure is invalid.

YAML errors always count as new violations.

## 6. Baseline format and ownership

Canonical location:

`scripts/ci/baselines/session-identity.txt`

Initial creation requires an explicit bootstrap against the target branch:

`python3 scripts/ci/check_session_identity.py --bootstrap-baseline --base-ref origin/main`

Bootstrap baseline contents are derived only from the work-items tree
referenced by `--base-ref`, not from the current working tree. Bootstrap
freezes violations already present in that target branch tree and refuses
when the current tree contains violations absent from the target branch tree.

Each baseline entry consists of:

`CODE manifest-path#entry-index`

Entry indexes are one-based.

The path and entry index distinguish individual findings. The violation
code distinguishes the type of finding.

The baseline is gate input. It is not manually editable.

After initial bootstrap, subsequent baseline generations may only remove
entries. The ordinary `--write-baseline` command requires an existing
baseline and cannot create or expand one.

If the current tree introduces a finding not already in the baseline,
baseline generation refuses to proceed.

If a finding has disappeared, generation removes it.

Deleting the baseline file does not reset the ratchet: ordinary checking
and ordinary `--write-baseline` both exit with code `2` when the baseline
is missing.

The checker also rejects stale baseline entries during normal execution.

This prevents the baseline from becoming a permanent exemption list.

## 7. Relationship with Session Evidence

The existing `Session Evidence` required context remains unchanged.

Its existing implementation is:

`scripts/governance/session_evidence/validate.py`

That validator remains responsible for its existing decisions, including
structural fields, evidence paths, hashes and byte counts.

The new checker does not modify or replace those decisions.

The division of responsibility is:

| Control | Responsibility |
|---|---|
| Session Evidence | Existing evidence structure and integrity |
| Session identity ratchet | Semantic identity format and status consistency |

The two checks are independent required contexts.

This separation is intentional. Changing the existing validator would
change historical outcomes across the 132 manifests and violate the
non-blocking migration requirement.

## 8. Workflow enforcement

Workflow:

`.github/workflows/session-identity-ratchet.yml`

Required job context:

`Session identity ratchet`

Triggers:

- pull_request: opened
- pull_request: synchronize
- pull_request: reopened
- pull_request: ready_for_review
- push to main

The job runs the isolated checker tests before scanning the repository.

The job uses checkout-local files only. It does not access GitHub APIs,
network services, external session platforms or remote evidence stores.

The required context must be added to the repository's required
status-check declarations and protection configuration.

The workflow's existence alone does not establish platform enforcement.

## 9. Future tightening

The first implementation deliberately limits enforcement to session
identity and status consistency.

It does not include independent reviewer completeness.

The measured repository has 47 manifests containing independent_reviewer,
with NOT_ASSIGNED and NOT_APPOINTED accounting for 77.1%.

The most recent 20 work items contain zero actual independent reviews.

This is a separate governance defect and must not be silently mixed
into the initial identity baseline.

A future ratchet extension should introduce:

1. A defined parseable reviewer-session identity.
2. A distinction between an actual independent reviewer and a placeholder.
3. A verifiable relationship between reviewer and implementing session.
4. A separate violation inventory and baseline.
5. Tests for same-session self-review and delegated role simulation.
6. A shrink-only migration that preserves historical records.

The eventual target is to prohibit new NOT_ASSIGNED and NOT_APPOINTED
reviewer declarations while allowing historical entries to be
remediated incrementally.

The future extension must not weaken or replace the session identity
invariants established here.

## 10. Acceptance boundary

The checker passing means:

- No new session identity violations exist outside the frozen baseline.
- The baseline contains no stale entries.
- All manifests containing session_evidence have been examined.
- Invalid YAML has not been suppressed.

Bootstrap freezes violations already present in the target branch tree. It
refuses only when the current tree contains violations absent from that target
branch tree. The negative case was verified with
`--bootstrap-baseline --base-ref cb5b3dcd`, which exited `1` because the
current tree contained two violations absent from that base tree.

The current baseline was regenerated by the checker from the target
branch tree at `3da2e32cf0475a5d7645862a4a288988f69f09cc` after the target tree
advanced and the previous baseline no longer matched it. The checker refused
to proceed with the mismatch, so the baseline was regenerated from the
updated target tree. This was not a manual edit or an expansion of the ratchet's
allowance.

The baseline includes the existing violations in `AID-2026-265` and
`AID-2026-291` because both are present in the target branch tree. Their repair
belongs to separate work items; this PR does not modify either work item's
files.
It does not mean:

- Every historical session has been recovered.
- A UUID proves an actual platform session.
- Prompt provenance has been verified.
- Independent review has occurred.
- Every historical session-evidence record is authentic.

Those claims require separate evidence and separate controls.
