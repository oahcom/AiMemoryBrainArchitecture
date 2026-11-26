work_item_id: AID-2026-083
authorization:
  authorized_by: "user-authorized operator (delegated by account owner)"
  decision_date: "2026-11-26"
external_evidence_reference:
  workflow: "AID-2026-11-26-FORGET-FENCE-01"
  issues: ["#1125", "#1211"]
repository:
  base_branch: main
  base_commit_sha: 9ee89b322a160cc7ea5bcbd44ae2151850e289a0
  branch: docs/forget-fence-authority-2026-11-26
  pull_request: 1232
decision:
  logical_authority: D
  storage_role: "physical durability/recovery and derived rebuildable projections only"
  owner_acceptance: PENDING
  normative_approval: NOT_CLAIMED
  implementation_authorization: NOT_GRANTED
verification:
  criteria:
    FF-01: "D sole logical issuer"
    FF-02: "Storage rows projection-only"
    FF-03: "Typed target + source + Scope + lineage"
    FF-04: "Fail closed on stale/missing/corrupt/underscoped authority"
    FF-05: "D-domain and I-global completion separated"
    FF-06: "EN/ZH-CN semantic parity"
    FF-07: "Issue comments posted; Issues remain OPEN"
  ci_status: PENDING
  owner_review: PENDING
session:
  implementing_ai_session: NOT_RECORDED
  provenance: NOT_VERIFIED
