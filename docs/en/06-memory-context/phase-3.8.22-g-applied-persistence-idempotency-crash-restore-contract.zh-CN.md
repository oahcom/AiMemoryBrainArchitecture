---
document_metadata:
  domain: memory-context
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
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-200/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "GOV-DOC-002 classification of a mirror that carried no front-matter: records domain, role, status and the canonical source path only (basis, the document's own statement: Status: G-owned normative design draft; implementation NOT VERIFIED; cross-owner acceptance required). Claims no canonical authority and does not verify semantic parity with the source. Pre-metadata content blob: abace324c42e18736b1cd273a9aea7f0c29177f8."
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
    canonical_conflict_status: None
    normative_status: Informative
  bilingual_counterpart:
    source: "06-memory-context/phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.zh-CN.md"
    en: null
    zh-CN: "docs/zh-CN/06-memory-context/phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.zh-CN.md"
---
# Reader mirror for the Chinese G Applied persistence contract

This English reader mirror corresponds to the canonical Chinese normative source:
`06-memory-context/phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.zh-CN.md`.

The contract assigns the durable Full Applied decision exclusively to G. C `HANDOFF_ACCEPTED` is necessary but insufficient; G must join C Provider Outcome, authenticated H evidence, COC participant/terminal proof, I authorization, D ForgetFence, applicable Storage same-GID resolution, and G Context/Delivery predicates.

Merged PR [#139](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/139) adds a bounded single-node SQLite reference model. Exact PR-head run [#44187485388](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44187485388) and post-merge main run [#44187595305](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44187595305) passed; the latter is pinned to main `af3b0380e35a5834f8b5cdca92dfa0f8fcd8e1bf` and reports 8 tests OK.

This is a reference/conformance prototype, not production G runtime or Owner acceptance. It does not prove multi-replica linearization, distributed restore fencing, current-use revalidation, live authority resolution, cryptographic authentication or production durability. Production G Applied and cross-owner Full Applied remain **NOT VERIFIED / NOT FROZEN**.
