---
document_metadata:
  domain: ai-development
  role: work-record
  steward: "user-authorized operator (delegated by account owner)"
  lifecycle:
    approval:
      decision_status: Draft
      approver: "delegated adjudication (Issue #305 / 7042461592)"
      decision_date: "2026-11-27"
      approved_version:
        scheme: content-hash
        value: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-286/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-27"
      last_verification_note: "Supplied measurements are recorded as historical facts; nothing in this record is presented as a fresh CI, merge or acceptance result."
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
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords:
      - "AID-2026-286"
      - "evidence"
      - "§5(3)"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# Evidence — AID-2026-286

## 1. Purpose

This work item converts the remaining AC2 gap into an explicitly named and scoped exception record.

The terminal AC2 adjudication is PARTIAL. Its remaining gap was identified as:

> Owner explicitly names the §5(3) exception record; NOT_STARTED.

The purpose of this carrier is to provide that named record, document its factual basis, explicitly constrain its scope, and preserve the original contemporaneous-signing obligation for future assessments.

This evidence document does not assert that the carrier has been written to the repository, passed CI, or merged.

## 2. Authoritative inputs

### 2.1 AC2 terminal adjudication

- Issue: #262.
- Adjudication comment: `7211718343`.
- Timestamp: `2026-11-27T06:38:55Z`.
- Outcome: `PARTIAL`.
- Contemporaneity: not satisfied.
- Remaining gap: explicit naming of the §5(3) exception record.

### 2.2 Governing requirement

Source: `14-ai-development/PR-GOVERNANCE-001.md`.

- §5(3) English text: L142.
- §5(3) Chinese text: L147.
- Explicit exception instruction: L138.

The requirement calls for `assessor`, `assessed_version`, and `evidence_baseline`, prohibits after-the-fact baseline signing, and requires re-signing or an applicability boundary when the referenced version changes.

The exception instruction requires exceptions to be explicitly recorded.

### 2.3 Four historical assessments

| Assessment | Three-field and attachment range | Lines before | Lines after | Insertion |
|---|---:|---:|---:|---:|
| `reviews/architecture/SYS-RISK-001.en.md` | L12–L15 | 964 | 968 | +4 |
| `reviews/architecture/SYS-RISK-001.zh-CN.md` | L12–L15 | 963 | 967 | +4 |
| `reviews/complexity/architecture-complexity-assessment.en.md` | L10–L13 | 317 | 321 | +4 |
| `reviews/complexity/architecture-complexity-assessment.zh-CN.md` | L10–L13 | 317 | 321 | +4 |

The three required fields were attached by the AID-2026-250 rework on 2026-11-27.

All four documents identify assessed version:

`b372b62c640a2b656e54b6db62a4ee67d7d8c001`

The four `signature_attached` declarations explicitly describe the attachment as retrospective and not contemporaneous. Their exact wording is preserved in the exception record.

### 2.4 Historical carrier and validation evidence

The four assessment changes were carried by PR #1424.

- Merge commit: `101ea55e021d6c3a819f66fc588c76b1e99a77fe`.
- Merge type: true two-parent merge.
- Recorded parent prefixes: `af2660d5` and `e17c0e9a`.
- Baseline checker summary: `SUMMARY files=4 failures=0`.
- Mutation tests: three field-deletion mutations per document, four documents, 12 total.
- All 12 deletion mutations exited with code 1.
- Required contexts: 16/16 success.
- Branch protection behind count: 0.
- Blob comparison: 11/11 files matched.

These are supplied historical measurements, not fresh measurements performed by AID-2026-286.

### 2.5 Historical comment integrity

The supplied evidence identifies the following historical comments as unchanged:

- `7011312621`
- `7014315135`
- `7143927480`
- `7149369280`

Their recorded `updated_at` values remain within:

`2026-11-27T04:54–05:03Z`

The rework trace comment `7211285798` has:

`created == updated == 2026-11-27T06:10:38Z`

The terminal adjudication comment is `7211718343`, dated `2026-11-27T06:38:55Z`.

No historical comment body is modified by this work item.

## 3. Delegated authority

The decision relies on Issue #305, comment `7042461592`, dated 2026-11-20T14:46:28Z.

Its §3 grants a delegate authority to declare an acceptance criterion satisfied, partially satisfied, or not satisfied with evidence, and to open, update, and merge the pull requests needed to carry those acts.

Its §4 requires the delegate not to fabricate independence where the toolchain cannot establish it.

The resulting record is explicitly classified as:

`delegated adjudication, not a natural-person Owner signature`

No natural-person Owner signature is claimed.

## 4. Measurements and limitations

| Measurement | Supplied result | Repeated in AID-2026-286 |
|---|---|---|
| Baseline checker | `SUMMARY files=4 failures=0` | No |
| Signature-field deletion mutations | 12/12 exit code 1 | No |
| Required contexts | 16/16 success | No |
| Behind count | 0 | No |
| Blob comparison | 11/11 matching | No |
| Historical comment timestamp integrity | Supplied values unchanged | No |

The following items are explicitly `NOT_MEASURED` in this work item:

1. Re-execution of the 12 mutation tests.
2. Independent re-opening and verification of all 16 required-context run URLs.
3. Re-execution of the 11-file blob comparison.
4. The final merge commit and per-file blob identity of AID-2026-286.
5. Natural-person Owner signature or subsequent ratification.

No CI success, merge, or Owner acceptance is claimed by this evidence document.

## 5. Evidentiary conclusion

The supplied evidence supports creation of a narrow retrospective exception for the four named historical assessment documents.

It does not support a claim that their contemporaneity requirement was satisfied.

The exception record must preserve the following distinction:

- Historical signature-field attachment occurred retrospectively.
- The contemporaneity requirement was not met.
- The explicit exception addresses that historical failure only.
- Future assessments remain subject to contemporaneous signing under §5(3).

**This work item does not claim that §5(3) has been satisfied.**
