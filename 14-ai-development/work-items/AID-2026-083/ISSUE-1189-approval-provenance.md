---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: content-hash
        value: null
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-26"
      last_verification_note: "Exact source pins and issue records are listed below. Acceptance is not asserted; unavailable evidence is explicitly marked BLOCKED."
    usage_status: Active
    modification_status: Unchanged
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
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# Issue #1189 — approval provenance evidence

**Baseline:** `main` at `515b7144320fd9fcc1e1a2c3d2d2744d979b4ca8` (2026-11-26).  
**Disposition:** **NO APPROVAL EVIDENCE FOUND; delegated non-approval decision recorded.** This report does not approve either document.

## 1. What the existing decision records actually say

- Issue #1189 comment [#7174316473](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1189#issuecomment-7174316473), dated 2026-11-26 (UTC+8), records **Decision C**: the current Design Principles and Architecture Invariants versions are NOT APPROVED and remain candidate / Pending-Reapproval. It expressly says not to retroactively validate unsupported Approved metadata.
- Issue #1189 comment [#7174519803](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1189#issuecomment-7174519803) records D-12: the authorised approving principal for P-01–P-16 cannot be determined from the repository; no decision record names an approver; downstream use is not approval evidence.
- Issue #1189 comment [#7182762040](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1189#issuecomment-7182762040) corrects the date interpretation and pins the earlier comment dates to 2026-11-26 (UTC+8).
- Issue #1189 comment [#7184238858](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1189#issuecomment-7184238858) confirms PR #1221's mirror/scope alignment landed, but does not claim approval or close the Issue.

**Attribution of the recorded direction:** `user-authorized operator (delegated by account owner)`.  
**Date:** 2026-11-26 (UTC+8), as specified in the decision record.  
**Nature:** delegated non-approval/status direction only. **代理登记，非自然人签署。** It is not a formal approval, not a natural-person signature, and not a substitute for the unknown approving principal.

## 2. Required approval fields — honest values

| Field | Design Principles P-01–P-16 | Architecture Invariants I-01–I-24 |
|---|---|---|
| Approver / approving principal | NOT_RECORDED | NOT_RECORDED |
| Formal approval date | NOT_RECORDED | NOT_RECORDED |
| Formal approval event / record | NOT_RECORDED | NOT_RECORDED |
| Current version approved? | NO — delegated Decision C says NOT APPROVED | NO — delegated Decision C says NOT APPROVED |
| Approval scope | Separate scope: P-01 through P-16; no approval granted | Separate scope: I-01 through I-24; no approval granted |
| Delegated decision record | #7174316473 and #7174519803 | #7174316473 and #7174519803 |
| Delegated decision date | 2026-11-26 (UTC+8) | 2026-11-26 (UTC+8) |

The GitHub account that posted a comment is not evidence of a historical approving principal. The delegated operator is recorded as the actor for the non-approval direction only, not as the approver of either source set.

## 3. Exact current version pins

All six files were read from the same current-main commit `515b7144320fd9fcc1e1a2c3d2d2744d979b4ca8`. Blob identifiers below are Git blob SHA-1 values and pin the exact bytes.

| Document set | Current path | Git blob SHA-1 |
|---|---|---|
| Design Principles root | `00-governance/design-principles.md` | `0a67b5b2b4acb22faa0b3dec38d23c771f88b821` |
| Design Principles EN | `docs/en/00-governance/design-principles.md` | `f5370ff4b1cd515e5c77dbbdbb7356cbd2fa4fc2` |
| Design Principles ZH-CN | `docs/zh-CN/00-governance/design-principles.md` | `ce8ef478f06a23d00de11117a8fe47efedf77f6c` |
| Architecture Invariants root | `00-governance/architecture-invariants.md` | `a5a51937133d43585d970cad02dcfd20925078d9` |
| Architecture Invariants EN | `docs/en/00-governance/architecture-invariants.md` | `eb6e84167470830d7a9710c22add92fa2c990a6e` |
| Architecture Invariants ZH-CN | `docs/zh-CN/00-governance/architecture-invariants.md` | `ebfeb9315bd252d708a99e28efab2d344db70daf` |

## 4. Current metadata readback

For both root documents and both language mirrors:

- `decision_status: Under-Review`
- `approver: NOT_RECORDED`
- `decision_date: NOT_RECORDED`
- `evidence_verification.verification_status: Unverified`
- `modification_status: Pending-Reapproval`
- the body says the current version is CANDIDATE / NOT APPROVED.

The recorded `approved_version` git pin `a7d12fe9835d8f53403946ab08c1cae8c3f12fbf` is not an approval event for the current blobs above; metadata says approval applicability is not applicable to the current version. It must not be repurposed as current-version approval evidence.

**Open interpretation gap:** D-12's prose says the default is candidate / non-normative, while current source metadata still has `normative_status: Normative`. The body labels the content CANDIDATE and not approved. The delegated non-approval record does not silently resolve this separate normative-classification question. A competent Owner must explicitly decide whether candidate content remains Normative-but-unapproved or whether the normative classification itself is to be corrected; this report does not change it.

## 5. Minimum path to complete #1189

1. Identify the competent approving principal/body for Design Principles and, separately, Architecture Invariants. If no such authority can be identified, record that fact rather than infer one.
2. For each set, obtain an attributable decision naming the approver, date, exact commit and blob SHA, approval scope (P-01–P-16 or I-01–I-24), and any conditions/exclusions.
3. If approval is not granted, obtain an explicit authorized status/classification decision that resolves the candidate / normative ambiguity; update root and both mirrors consistently.
4. Update evidence references and verification metadata only after the actual decision exists.
5. Separately address the Issue's governance-check criterion; this evidence-only PR does not add a checker.

**Result:** the available evidence supports a version-pinned delegated **non-approval** record, not the requested formal approval. #1189 remains OPEN.
