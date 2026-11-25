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
      verification_status: Verified
      last_verified_date: "2026-11-25"
      last_verification_note: "Every count, path and comment id below was produced by reading the repository and the Issue on 2026-11-25, not recalled. Where a number is quoted from a session that is not this one, the source is named."
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

# Session role / use case

REGISTRATION for AID-2026-075. The work item itself is `NOT_STARTED`: no checker,
no test, no workflow invocation exists. What this session did was authorise stage
one and record the boundary that keeps stage three from being inferred from it.

The distinction matters because a work item that grants an observation mode is
easy to read later as having granted the enforcement that follows from it. Ten
acceptance criteria are recorded, and one of them (C10) exists only to make the
refusal checkable.

# Actual AI input

**Committed, pinned.** `prompt-v1.md` in this directory is the instruction this
registration was carried out against, and its digest is recorded in the manifest.

`executed_prompt_provenance` is `NOT_VERIFIED`: the digest proves the committed
file has not changed since it was pinned, not that it is byte-for-byte what the
session read. The prompt was assembled in-session from the sources below, so the
weaker claim is the true one.

**Read before writing:**

| input | what it settled |
|---|---|
| Issue #262 comment `7153428650` | the five requirements gaps the Owner accepted, and specifically the fifth: a named gate that cannot pass in the absence of a signed assessment; accountability written as a disclosure duty rather than a veto |
| `PR-GOVERNANCE-001.md` §5 at `edbc3632` | the four normative parts (role, isolation, signature, accountability) and the non-exemption sentence that closes the paragraph |
| `AID-2026-071/session-evidence-r45.md` | the clause's own statement that no check enforces it — the gap this work item exists to close |
| every `14-ai-development/work-items/*/manifest.yaml` (48 at `edbc3632`) | the counts the staging argument rests on: 41 carry all three fields, 14 carry `implementing_ai_session` only nested, 41 of 41 distinguish owner from implementer once `sponsor == accountable_owner` is permitted |
| the four assessment records on `#262` | that none of them carries `assessor`, `assessed_version` or `evidence_baseline`, which is why remediation has to precede enforcement |
| `AID-2026-073/manifest.yaml` and its evidence record | the shape of a `GATE/*` registration in this registry: five `authorization` keys, `scope.files_out_of_scope` naming what is not granted, and acceptance criteria that are falsifiable one at a time |

**Judgment that is recorded rather than assumed:** the observation-first order was
chosen over enforcement-first for one measurable reason and not for caution. With
the counts above, a blocking check added today would report against most of the
registry and would mark every existing assessment unsigned in its first run — the
shape `rust-workspace-test` had before PR #1027 removed the path filter, where the
only available response to a gate failing on its own introducing commit is a
revert.

# AI-visible output

Five files, and the acceptance text in the manifest is the substantive one. The
rest is bookkeeping.

1. `manifest.yaml` — `class: GATE/CI/TEST`, `risk: R2`, five `authorization` keys
   with `gate_behaviour_change: NOT_GRANTED`, `implementation.status: NOT_STARTED`,
   and C1–C10.
2. `prompt-v1.md` — the scope, the staging, and the measured basis for the staging.
3. `INDEX.md` — one row, `DISPATCHED`, pointing at the manifest and stating that
   nothing is implemented.
4. This record.

**What the acceptance criteria constrain, stated so a reviewer can check the shape
and not just the prose:**

- C2 makes the top-level requirement testable, because a nested-only field is the
  exact shape 14 of 48 manifests already have.
- C3 makes principal identity the judged quantity, which is the correction
  AID-2026-071 landed: equal strings are not evidence of distinct principals, and
  distinct strings are not evidence either.
- C8 keeps previously accepted assessments out of the observer's blast radius,
  which is what makes stage one safe to run against the existing registry.
- C10 restates `gate_behaviour_change` as something a reviewer can observe in the
  workflow file rather than trust from the manifest.

**Not claimed:** that the checker exists, that any record has been remediated, that
any enforcement is authorised, or that Issue #262 AC2 is met. It remains PARTIAL
until stage one runs and reports.
