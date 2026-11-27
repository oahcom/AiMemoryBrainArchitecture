---
document_metadata:
  steward: "user-authorized operator (delegated by account owner)"
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
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-27"
      last_verification_note: "The prompt snapshot was hashed from its committed bytes after adding the required DM-15 steward field; the digest and byte count below are reproducible with sha256sum and wc -c."
    usage_status: Active
    modification_status: Modified
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

# Evidence — AID-2026-116 prompt digest recalculation

The prompt snapshot `prompt-v1.md` received the required DM-15 steward metadata:

`steward: \"user-authorized operator (delegated by account owner)\"`

**因 DM-15 补 steward 重算。** The top-level manifest `prompt_sha256` / `prompt_bytes` and `session_evidence[0].executed_prompt_sha256` / `executed_prompt_bytes` were recomputed from the resulting file bytes, without changing any of the 33 digest correction records or their target/attribution conclusions.

- Previous prompt SHA-256: `3b8f72e2e124b24625035c42398c0529655be4d8e8e48ddfc4b7369b89ce1c94`
- Previous prompt bytes: `8274`
- Recomputed prompt SHA-256: `6fd626bfd4674e3e98f107baa93b4f2ef1061eac36c80c66a7778714ab5b725e`
- Recomputed prompt bytes: `8341`
- Reproduction: `sha256sum 14-ai-development/work-items/AID-2026-116/prompt-v1.md` and `wc -c < 14-ai-development/work-items/AID-2026-116/prompt-v1.md`
