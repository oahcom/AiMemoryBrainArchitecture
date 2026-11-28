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
      last_verification_note: "Session evidence recorded for traceability; this metadata does not assert approval or independent verification."
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
    canonical_scope: "Session evidence for AID-2026-313, the IPv6 transition-form SSRF guard repair in oahcom/chatgpt-session-ops."
    canonical_scope_id: "ai-development/aid-2026-313-session-evidence"
    canonical_scope_keywords:
      - "AID-2026-313"
      - "session evidence"
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

# Session role / use case

Role: IMPLEMENTATION_SESSION.

Work item: AID-2026-313 — close the IPv6 transition-form SSRF bypass in
`oahcom/chatgpt-session-ops` `scripts/mcp_connector.py::assert_safe_url`.

Authorization: the Owner ruling on `64-wb-decisions.md` item C, reproduced
verbatim in `prompt-v1.md` §2: the `2002::1` 6to4 bypass is a reproducible
security defect, authorize a new independent work item covering 6to4 / Teredo /
IPv4-mapped unwrapping and rejection, with positive and negative tests, as its
own Draft PR, without changing any other SSRF policy.

Boundaries honoured: one Draft PR, no merge, no Issue state change, no
renumbering, no correction of existing `aid-ledger` rows, no other SSRF policy
change.

# Actual AI input

Executed order: the Owner ruling above plus the task framing transcribed in
`prompt-v1.md` §3. The snapshot is committed as `prompt-v1.md`
(sha256 `7fb1d53aaf31c80a95222872f9b8608fd5208953c79ee2560051ead6b7b74679`,
3821 bytes). `executed_prompt_provenance: NOT_VERIFIED`: the delivered prompt was
the ruling text, not this file byte for byte.

Identifier: AID-2026-313 was reserved on `AiMemoryBrainArchitecture` branch
`aid-ledger` at commit `c36794d0` (push `5592658f..c36794d0`, fast-forward),
after a scan that put main's work-items tree at `AID-2026-290`, the ledger at
`285`, and every origin branch head and all 19 open PR heads at `AID-2026-311`.
This registration lives in `AiMemoryBrainArchitecture` because that is where the
AID registry and the document/bilingual/traceability/hygiene gates live; the code
under change lives in `oahcom/chatgpt-session-ops`, which has no such registry.
That split is a deviation from "one PR", recorded rather than hidden.

# AI-visible output

Code change, branch `fix/ssrf-6to4-unwrap` in `oahcom/chatgpt-session-ops`,
Draft PR #161 <https://github.com/oahcom/chatgpt-session-ops/pull/161>:

| Item | Value |
|---|---|
| base | `ea7bdd36607bcf99d8b68ccd647f4ee2ea7639e5` |
| head | `0e11c33ce8a074c381119709994eb885e4fe9e3f` |
| `scripts/mcp_connector.py` | `_embedded_ipv4`, `_is_public_destination`; +34 / −4 |
| `tests/test_mcp_connector_url_guard.py` | `TestTransitionFormRejections`; +59 / −0 |

Reproduction at the base commit, unmodified module:

```
OLD CODE ACCEPTS: https://[2002::1]/
OLD CODE ACCEPTS: https://[2002:c0a8:101::1]/   (6to4 carrying 192.168.1.1)
old code rejects: https://[::ffff:127.0.0.1]/ UNSAFE_ENDPOINT
```

Test runs (Windows, Python 3.12.3):

| Command | base `ea7bdd3` | head `0e11c33` |
|---|---|---|
| `python -m unittest tests.test_mcp_connector_url_guard` (3.12.3) | 16 tests, 1 failure (`2002::1` not rejected) | 21 tests, OK |
| `python -m unittest tests.test_mcp_connector_url_guard` (3.11.15) | — | 21 tests, OK |
| `python -m unittest discover -s tests` (3.12.3) | 1251 tests, 3 failures | 1256 tests, 2 failures |
| GitHub Actions on `0e11c33` | — | `unit tests` success, `tools/tests guards` success, `real MCP SDK integration` success, `e2e against real memory-stdio` success |

The first CI run failed, and the failure was this work item's own positive control:
CI runs Python 3.11, where `2002::/16` is still listed as private, so
`2002:808:808::1` is rejected by the envelope alone and cannot serve as a positive
control. 3.12 removed that entry — which is exactly why the bypass exists on 3.12 and
not on 3.11. `0e11c33` moves the control to `2001:4860:4860::8888` and pins the decode
`2002:808:808::1 -> 8.8.8.8` directly, so the property under test no longer depends on
which release's `is_global` table is installed.

The two remaining failures are `tests/test_cdp_import_order.py` CJK-console cases
that fail identically at the base commit; they are not caused by this change and
are not repaired by it.

Known limits, stated rather than hidden:

- On the Linux CI runner the pre-existing `2002::1` expectation passes for the
  wrong reason (numeric IPv6 `getaddrinfo` fails there, so the guard rejects
  before judging the address). The new cases patch `getaddrinfo` so they test the
  guard rather than the host resolver.
- NAT64 `64:ff9b::/96` is not unwrapped; the ruling did not authorize it.
- `implementing_ai_session` is a label, not a platform session id; no such id was
  recorded, so none is claimed.
