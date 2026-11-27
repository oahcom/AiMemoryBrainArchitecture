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
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "wt-aid313/14-ai-development/work-items/AID-2026-313/session-evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Prompt snapshot recorded for traceability; this metadata does not assert approval or independent verification."
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
    canonical_scope: "Executed-prompt snapshot for AID-2026-313, the IPv6 transition-form SSRF guard repair in chatgpt-session-ops."
    canonical_scope_id: "ai-development/aid-2026-313-prompt-snapshot"
    canonical_scope_keywords:
      - "AID-2026-313"
      - "prompt snapshot"
      - "SSRF 6to4 Teredo IPv4-mapped"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# AID-2026-313 — prompt snapshot v1

Role: IMPLEMENTATION_SESSION
Work item: close the IPv6 6to4 / Teredo / IPv4-mapped SSRF bypass in
`chatgpt-session-ops/scripts/mcp_connector.py::assert_safe_url`.
Repository under change: oahcom/chatgpt-session-ops
Registration repository: oahcom/AiMemoryBrainArchitecture

This snapshot is a transcription, not a live capture. The prompt reached the
execution session as the Owner's adjudication on `64-wb-decisions.md` item C plus
the task framing quoted below. Byte-for-byte identity with the delivered prompt
is therefore not claimed (`executed_prompt_provenance: NOT_VERIFIED`).

## 1. Ruling source — 64-wb-decisions.md, item C (verbatim)

**C. `2002::1`（6to4）能绕过 SSRF 守卫**：`is_global=True`，守卫不解包 `sixtofour/teredo/ipv4_mapped`。这是 pre-existing（main 上同样失败）。是否授权开一个新 AID 修守卫并补测试？

## 2. Owner ruling delivered to the executing session (verbatim)

```text
C — the `2002::1` 6to4 SSRF bypass is a reproducible security defect; authorize a
NEW independent work item covering 6to4/Teredo/IPv4-mapped unwrapping and
rejection, with positive and negative tests, as its own Draft PR; do not change
any other SSRF policy.
```

## 3. Task framing (verbatim, executing-session instruction)

```text
Fix the URL guard (`scripts/mcp_connector.py::assert_safe_url`) so that IPv6 6to4
(2002::/16), Teredo (2001::/32) and IPv4-mapped (::ffff:0:0/96) addresses are
unwrapped and their embedded IPv4 checked against the same rejection set; reject
when the embedded address is private/loopback/link-local/reserved/CGNAT/
unspecified, and keep every existing behaviour unchanged. Add positive and
negative tests, including the existing `2002::1` case and a case proving a
genuinely public address still passes.
```

## 4. Boundaries taken from the ruling

- One independent work item, one Draft pull request; no merge.
- Unwrapping and rejection only. Every other SSRF policy decision stays as it is:
  scheme, credentials, fragment, missing host, DNS failure and the outer-address
  rejection set keep their existing codes and their existing order.
- No Issue state change, no renumbering, no correction of existing `aid-ledger`
  rows.
