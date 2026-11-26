---
document_metadata:
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
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-096/approval-evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-26"
      last_verification_note: "Evidence artifact; does not independently attest authority or session identity."
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
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# AID-2026-096 — NEW normative approval evidence

- work_item_id: AID-2026-096
- id_status: FINAL
- merge_queue_action: ASSIGNED_AT_MERGE; MAIN_INDEX_MAX=AID-2026-095; CURRENT_ID=AID-2026-096; NO_RENUMBER
- approval_event_date: 2026-11-26

## Approval identity
- approver: user-authorized operator (delegated by account owner)
- designation_source: account owner statement, 2026-11-26
- approval_event_date: 2026-11-26
- approval_type: NEW_APPROVAL
- decision: APPROVED_NORMATIVE
- repository enum mapping: `decision_status: Approved` + `normative_status: Normative`; APPROVED_NORMATIVE is represented by this permitted metadata pair.

## Decision and rationale
The canonical root Design Principles and Architecture Invariants are approved as Normative governance baselines. Their EN and ZH-CN documents are translation/mirror artifacts; the root remains the canonical normative source. The documents are frozen as a governance baseline and are cited by downstream governance work.

The AID-2026-014 supplemental sections remain in their existing EN/ZH mirror locations and are explicitly marked `mirror-only supplemental, not part of canonical root`. They remain non-normative and are not merged into root. Any promotion of a statement is pending Owner adjudication.

This is a new approval event on 2026-11-26. It is not a retroactive approval and does not authenticate any historical approver.

## Exact approved scope — six path/blob pairs
| Path | Git blob SHA | Approved body content SHA-256 |
|---|---|---|
| `00-governance/design-principles.md` | `352b969fa8c07ad1f2848797f06404293242db13` | `273f048d8dd3401ec62e2c177fa00787ab6f6cb855e190b471b3a0c7f3b81523` |
| `00-governance/architecture-invariants.md` | `3c64217fde34fe67f463856b648a3e8a935a1654` | `6df99f23052dd5475d22d397cdee160436464dc3a95946fe6d6e12f93aea1071` |
| `docs/en/00-governance/design-principles.md` | `50d1d1d0907f25e2104414ba9bb48a31fb470b1d` | `e467d7cf3e8feb0457843b5f4f0fd038b01608c32a9fbe35e585cc41e49c665a` |
| `docs/en/00-governance/architecture-invariants.md` | `ca7052afa486ce124e180c63812e082a6def5ebc` | `6b818d9b1884530bdf208507d6a7913699c8598d4c0f351f238cfaff449c0a3a` |
| `docs/zh-CN/00-governance/design-principles.md` | `cf6ce6c08970dea58e3a93514cea1f801e55a666` | `7cd923872a16ec0b01174798614d6ccf867b20fa18edfe9c3c08b4f3e31e3e00` |
| `docs/zh-CN/00-governance/architecture-invariants.md` | `de534192ce8c343318d7da4add21daf0bbf1e04b` | `88bbebd033e0b5669bafc83c71afa2831cebb4a2e3a6cfa47573cf6b3259b293` |

The approval is bound only to these six exact path/blob pairs. Any content or metadata change creates a new blob and requires a new approval event and a new exact scope list.

## Metadata
All six documents carry `decision_status: Approved`, the designated approver, `decision_date: 2026-11-26`, `normative_status: Normative`, and an exact `content-hash` of the approved body. The former `CANDIDATE / Pending-Reapproval — NOT APPROVED` state is preserved as historical context.

## Limits
- This approval does not cover implementation conformity with P-01–P-16.
- It does not assert runtime, validator, test, deployment or production conformance.
- No runtime code or validator semantics are modified.
- Mirror-only supplemental content is not promoted into the canonical root.

## DEC-13 and evidence references
- DEC-13 status: RECORDED (new approval event).
- approver: user-authorized operator (delegated by account owner)
- decision_date: 2026-11-26
- Register: main decision-acceptance register and EN/ZH-CN mirrors.
- Matrix: main A–I/Storage matrix and EN/ZH-CN mirrors.
- Issue #1189 evidence comment: https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1189#issuecomment-7185429832
- Issue state was observed OPEN before the comment; this Work Item does not change it.

## Carrier
- Carrier PR: https://github.com/oahcom/AiMemoryBrainArchitecture/pull/1256
- Original approval baseline: `81906cfc8d3cd477d26657520aa04d81466e7ce2` (the six exact approved blobs are pinned to this baseline).
- Current merge-queue base: `31385bc1aabc1599be2c8320be408c0d170057a8`.
- Merge-time ID allocation: main INDEX max was `AID-2026-095`; final ID is `AID-2026-096`; no renumbering was required.
- Issue #1189 remains OPEN; DEC-13 Owner/joint acceptance and remaining acceptance conditions remain pending.
