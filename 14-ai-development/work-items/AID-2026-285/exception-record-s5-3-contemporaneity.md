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
        - "14-ai-development/work-items/AID-2026-285/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-27"
      last_verification_note: "Exception record text is authoritative as authored; the four assessment documents, the checker and the Issue body are unchanged by this work item."
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
      - "§5(3)"
      - "retrospective exception"
      - "assessment contemporaneity"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# §5(3) Retrospective Exception Record — Contemporaneity

## 1. Decision record

| Field | Value |
|---|---|
| Exception ID | EX-AID-2026-285-S5-3-CONTEMPORANEITY |
| Work Item / carrier | AID-2026-285; single carrier PR, number to be recorded after creation |
| Rule | `14-ai-development/PR-GOVERNANCE-001.md` §5(3) |
| Exception type | Retrospective exception to contemporaneity |
| Decision status | Accepted — delegated adjudication |
| Decision date | 2026-11-27 |
| Decision-maker | user-authorized operator (delegated by account owner) |
| Decision classification | delegated adjudication, not a natural-person Owner signature |
| Review date | 2026-11-27 |
| Unclosed evidence | Natural-person Owner signature is not supplied by this record; historical contemporaneity remains factually unmet |

## 2. Governing rule

The governing English text in `14-ai-development/PR-GOVERNANCE-001.md` §5(3) states:

> (3) **Signature**: the output must carry `assessor`, `assessed_version` (full 40-character commit) and `evidence_baseline`; a baseline may not be signed after the fact, and an assessment that cannot name one is unsigned. Once a later commit changes the version a signature points at, the assessment must be re-signed or marked with its applicability boundary.

The corresponding Chinese text states:

> (3) **署名** —— 产出须带 `assessor`、`assessed_version`（完整 40 位 commit）与 `evidence_baseline`；基线不得事后补签，签不到即视为未署名。署名指向的版本一旦被后续提交改变，评估须重签或标注适用边界。

The governing exception instruction immediately preceding the numbered requirements states:

> Record exceptions explicitly; do not silently waive the requirement.

This record explicitly invokes the exception mechanism for §5(3). It does not silently waive the rule, reinterpret retrospective attachment as contemporaneous signing, or change the underlying factual assessment.

## 3. Exception objects and factual basis

This exception applies exclusively to the following four historical assessment documents:

1. `reviews/architecture/SYS-RISK-001.en.md`
2. `reviews/architecture/SYS-RISK-001.zh-CN.md`
3. `reviews/complexity/architecture-complexity-assessment.en.md`
4. `reviews/complexity/architecture-complexity-assessment.zh-CN.md`

All four documents identify the same historical assessed version:

`b372b62c640a2b656e54b6db62a4ee67d7d8c001`

Their evidence baselines identify `main@b372b62c...` and the corresponding document path.

The three required signature fields were attached on 2026-11-27 by the AID-2026-250 rework. The attachment is explicitly identified in each document as retrospective.

The exact `signature_attached` declarations are:

**SYS-RISK-001.en.md**

> - signature_attached: 2026-11-27 by the AID-2026-250 rework — retrospective attachment, not a contemporaneous signature

**SYS-RISK-001.zh-CN.md**

> - signature_attached: 2026-11-27，AID-2026-250 返工补录——事后附加，不冒充同期签署

**architecture-complexity-assessment.en.md**

> - signature_attached: 2026-11-27 by the AID-2026-250 rework — retrospective attachment, not a contemporaneous signature

**architecture-complexity-assessment.zh-CN.md**

> - signature_attached: 2026-11-27，AID-2026-250 返工补录——事后附加，不冒充同期签署

The four documents were carried by PR #1424, merged at:

`101ea55e021d6c3a819f66fc588c76b1e99a77fe`

The merge was a true two-parent merge, with parents identified by the supplied evidence as `af2660d5` and `e17c0e9a`.

The following distinction is mandatory:

- The four documents describe their signature-field attachment as retrospective.
- This record grants a retrospective exception to the contemporaneity requirement for those same four documents.

These statements describe the same historical situation from two different perspectives. Neither statement establishes that contemporaneous signing occurred.

## 4. Decision and precise scope

**Decision:**

An explicit retrospective exception to §5(3) contemporaneity is granted for the four historical assessment documents listed in Section 3.

The exception covers only the following circumstance:

The three signature-related fields (`assessor`, `assessed_version`, and `evidence_baseline`) were attached on 2026-11-27 by the AID-2026-250 rework to assessments whose identified historical baseline is the 2026-11-27 pre-existing baseline represented by commit `b372b62c640a2b656e54b6db62a4ee67d7d8c001`.

For these four documents only, the absence of contemporaneous attachment is explicitly excepted.

The exception does not:

1. Establish that contemporaneity was satisfied.
2. Convert retrospective field attachment into contemporaneous signing.
3. Waive the requirement that the three signature fields exist and be complete.
4. Waive the requirement to identify the full 40-character assessed version.
5. Waive the requirement to identify the evidence baseline.
6. Apply to any future assessment document.
7. Apply to any newly created or re-signed assessment.
8. Authorize retrospective signing of future assessments.
9. Change the semantics of §5(3).
10. Change the behavior or interpretation of `scripts/ci/check_req_assessment_signatures.py`.

**Explicit applicability boundary:**

This exception covers only the four named documents and only their historical assessment baselines formed before the 2026-11-27 retrospective attachment.

No other document, version, assessment, or future baseline is covered.

## 5. Decision-maker and delegated authority

This is a delegated adjudication.

It is not a natural-person Owner signature.

The authority relied upon is Issue #305, comment `7042461592`, dated 2026-11-20T14:46:28Z.

The relevant delegated-authority language in §3 expressly authorizes a delegate acting alone, without further Owner confirmation, to:

> Declare an acceptance criterion satisfied, partially satisfied, or not satisfied, with evidence.

It also expressly authorizes a delegate to:

> Open, update and merge pull requests needed to carry these acts.

The relevant §4 independence boundary states that where independence cannot be established by the toolchain, the delegate records `INDEPENDENCE_UNVERIFIABLE` and proceeds; it does not fabricate an independent reviewer.

The delegated-authority boundary also prohibits:

> State that an unimplemented capability is implemented.

This record exercises the specifically delegated authority to make an evidence-based adjudication and record an explicit exception.

It does not claim that the delegate is a natural-person Owner, does not fabricate an Owner signature, and does not claim that §5(3) contemporaneity has been satisfied.

Attribution:

`user-authorized operator (delegated by account owner)`

Decision classification:

`delegated adjudication, not a natural-person Owner signature`

## 6. Non-waivable residual obligation

**Future assessments remain subject to the original contemporaneity requirement.**

Future new or re-signed assessments must carry their required signature fields contemporaneously with the applicable assessment baseline.

§5(3) is not waived for new documents.

In particular:

- New assessments must not rely on this exception.
- Newly signed assessments must not use retrospective attachment as a substitute for contemporaneous signing.
- Any later change to an assessed version must be handled under the original §5(3) re-signing or applicability-boundary requirement.
- The existence of this exception must not be interpreted as a standing or general-purpose waiver.

This residual obligation is permanent with respect to the scope of this exception: the exception cannot be extended to future assessments by implication.

## 7. Closure and independent verification

The exception is closed as an explicit, named exception only when this record is present in the repository as a merged and independently readable work-item artifact.

The following verification rules apply:

1. Any newly added assessment must still be checked against the original §5(3) wording.
2. The three required signature fields must remain subject to the existing signature checks.
3. `scripts/ci/check_req_assessment_signatures.py` retains its existing semantics.
4. This record must not be used as a mechanism to bypass future signature validation.
5. The four named documents must continue to identify their retrospective attachment honestly.
6. Any proposed expansion of the exception requires a separate, explicitly scoped adjudication; this record cannot be silently extended.

**Review date:** 2026-11-27.

The review is a scope and rule-consistency review. It does not claim that contemporaneity has become satisfied.

## 8. Unclosed evidence and limitations

The following distinctions remain explicit:

| Evidence item | Recorded state |
|---|---|
| Four documents and their retrospective declarations | Supplied factual evidence |
| Three signature fields in the four documents | Supplied factual evidence |
| Historical baseline | `b372b62c640a2b656e54b6db62a4ee67d7d8c001` |
| Retrospective attachment carrier | PR #1424 |
| Retrospective attachment merge | `101ea55e021d6c3a819f66fc588c76b1e99a77fe` |
| AC2 terminal adjudication | PARTIAL |
| Contemporaneity | NOT SATISFIED |
| This record's natural-person Owner signature | NOT PROVIDED |
| Future assessments | Original §5(3) applies without exception |

The original contemporaneity requirement remains factually unmet for the four historical assessments. This exception records an authorized retrospective disposition; it does not rewrite that fact.

## 9. Provenance and authorship

Work item: `AID-2026-285`

Attribution: `user-authorized operator (delegated by account owner)`

Decision classification: `delegated adjudication, not a natural-person Owner signature`

Decision date: `2026-11-27`

Related adjudication authority: Issue #305, comment `7042461592`.

Related acceptance criterion: Issue #262, AC2.

This document is an explicit exception record. It is not a modification of the four assessment documents, the governing signature requirement, the validation checker, or the Issue #262 body.
