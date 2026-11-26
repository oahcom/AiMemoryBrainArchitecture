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
        - "14-ai-development/work-items/AID-2026-170/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-26"
      last_verification_note: "Scope snapshot of the delegated dispatch, not a raw session transcript; the platform session identifier is not available, so no live capture is claimed."
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
---
# AID-2026-170 — Executed prompt snapshot (v1)

Provenance: user-authorised delegated dispatch to a worker subagent, 2026-11-26. The text below is the instruction the worker executed, copied from the dispatch brief `.superpowers/sdd/2026-11-26-chatgpt-session-ops-skill/u170.md` together with the worker contract that governs it. It is a scope snapshot, not a full raw session transcript.

## 1. Contract reference

Read `D:\code\.superpowers\sdd\2026-11-26-chatgpt-session-ops-skill\worker-contract.md` and work strictly by it (ID range, Work Item structure, PR creation, 16 required contexts, atomic merge, blob verification).

## 2. Task: AID-2026-170 — align SYS-RISK-001's P0 allowlist pointer

### Facts

- `08-bmcp-protocol/SYS-RISK-001.en.md` on main, line 297, pins the I P0 allowlist at blob `5c0e2049` (which corresponds to `phase-3.8.9`).
- `FINAL-A-002.en.md` on main, lines 102 and 126, pin the same allowlist at `44986f5f` (which corresponds to `phase-3.8.10`).
- The two allowlists have zero substantive difference: `git diff --text` reports only 18+/11-, all of it the `1.2.13 -> 1.2.14` version string and the header schema blob `8e7f6a6c -> 09fcd1fa` (one place each), plus a new §14 at the end. The §2-12 field lists are identical line for line.
- Owner final ruling: **current = `phase-3.8.10` (`44986f5f`)**, and `phase-3.8.9` is judged `SUPERSEDED_BY`.

### Required work

1. Change `5c0e2049` in `SYS-RISK-001.en.md` to `44986f5f`, changing **only this one pointer**, and add `reconciled_by: AID-2026-170` at the same location.
2. If `SYS-RISK-001` exists as root/EN/ZH, change all three and keep their structure consistent.
3. Sweep main for any **other file** that also pins `5c0e2049` (`git grep -n 5c0e2049 origin/main`). List each one but do not change it; record it in the evidence for a later ruling.
4. The evidence must give: the text before and after the change, the full blob SHA of both pins, and one sentence on why this is not a semantic change but a registration alignment.
5. Three documents plus one INDEX row, open a PR, wait for the 16 contexts, merge atomically, verify blobs.

### Prohibited

Do not change the body of either allowlist, do not change any other pin, do not restore `phase-3.8.9`.

Report in the worker-contract §7 format.
