---
document_metadata:
  domain: ai-development
  role: work-record
  steward: "user-authorized operator (delegated by account owner)"
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
        - "14-ai-development/work-items/AID-2026-348/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-28"
      last_verification_note: "Figures in this record were produced by operator-run commands on 2026-11-28 against origin/main f0843a8f; no independent reproduction is claimed."
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
    canonical_scope: "Record for AID-2026-348; this record does not establish normative requirements or acceptance."
    canonical_scope_id: "ai-development/aid-2026-348-record"
    canonical_scope_keywords:
      - "AID-2026-348"
      - "governance register"
      - "status alignment"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# AID-2026-348 — Evidence

Base: `origin/main` `f0843a8f38a420883921cfda96b515204967f885`.

## E1 — the three copies disagreed with each other

`git show origin/main:<path> | Select-String -Pattern '状态|Status'` on the header block:

| file | header line |
|---|---|
| canonical | `- 状态：`RESOLVED_ON_MAIN` / `F-2_APPROVED; F-1_EQUIVALENT_FOR_TEMPLATE_ONLY`（Owner 2026-11-21 裁定，见 §14）/ 解除方式为自我审查合并，见 §12` |
| docs/zh-CN | identical to canonical |
| docs/en | `- Status: `ACCEPTED` / `F-2_APPROVED; F-1_EQUIVALENT_FOR_TEMPLATE_ONLY` (Owner ruling 2026-11-21, section 14) / the empty diff returned `EXIT=2` from `ae37a419` until `81dd9a72d2` (section 12)` |

## E2 — all three copies contradicted themselves in section 11

| file | line | text |
|---|---|---|
| canonical | 281 | `**登记状态**：`ACCEPTED` / ... / main 上空 diff 恒为 `EXIT=2`（`81dd9a72d2` 起解除，见 §12）/ ...` |
| docs/zh-CN | 281 | identical to canonical |
| docs/en | 279 | `**Register status**: `ACCEPTED` / `F-2_APPROVED` / empty diff on main is permanently `EXIT=2` / ...` |

The same document's section 12 is titled "The deadlock is resolved on main — via F-1, and via a
self-reviewed merge", and the section 1 table records `EXIT=0` from `81dd9a72d2`. The section 11
sentence is therefore refuted by the document that contains it.

## E3 — an en-only change is rejected by the pairing gate

```
::error::docs/en/14-ai-development/governance-register/GOV-NC-2026-11-21-GATE-DEADLOCK-006.md requires all counterparts changed in this PR: docs/en/..., 14-ai-development/governance-register/...
Bilingual documentation gate: FAIL
```

This is why the section 11 defect was fixed in the same change: it is the only truthful edit that
makes the canonical and zh-CN copies participate.

## E4 — DM-15 requires the steward field on changed governed documents

```
14-ai-development/governance-register/GOV-NC-2026-11-21-GATE-DEADLOCK-006.md: DM-15 new governed document must declare a non-empty steward
docs/en/...: DM-15 new governed document must declare a non-empty steward
docs/zh-CN/...: DM-15 new governed document must declare a non-empty steward
```

The three files gained `steward: "user-authorized operator (delegated by account owner)"`.

## E5 — gate results after the change

```
check_bilingual_docs.py                                PASS (3 changed paths inspected)
check_document_management.py --require-changed origin/main  PASS (incremental): no GOV-DOC-002 violations; 901 classified, 366 unclassified
```

## E6 — what is not claimed

No CI run, review verdict or acceptance decision is claimed.
