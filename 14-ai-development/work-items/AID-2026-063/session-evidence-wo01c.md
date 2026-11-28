---
document_metadata:
  domain: ai-development
  steward: "Architecture Governance"
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
      last_verified_date: "2026-11-25"
      last_verification_note: "The merge refusal was produced by an actual PUT against the merge endpoint on pull request #1038; the check identifiers, timestamps and conclusions were read from that pull request's check-run list. The result comment on #1038 quotes the same responses."
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

IMPLEMENTER. Implement stage C of WO-01 for REQ-01 / Issue #262: execute the
deliberately-failing-head experiment and replace section 7's "not run, so that
half is unproven" sentence with a dated result.

This work item runs a probe, records what happened, and edits one sentence in each
language of section 7. It does not change branch protection and does not change
any workflow.

# Actual AI input

**Committed, byte-exact.** `prompt-v1.md` in this directory is the protocol this
stage was executed against.

**Recorded, not committed.** The probe itself lives outside this work item, on a
branch that is closed-unmerged on purpose:

| artefact | value |
|---|---|
| probe branch | `governance/wo01c-failing-head` at `b5cf4f25` |
| probe pull request | #1038, closed unmerged |
| failing check | `rust-workspace-test`, run `138943464904` |
| merge attempt | `PUT /pulls/1038/merge` → `405` |

`executed_prompt_provenance` is `NOT_VERIFIED`: the digest pins the committed
protocol, not the bytes a reader would have seen in a terminal.

Two standing directives governed the session and are reproduced verbatim because
the acceptance criteria are stated against them:

> 你不应该停下，因为我不输出观点，所有owner都可以是一个会话，你持续到收敛即可。

> 不能自己动手写代码。

# AI-visible output

Two sentences replaced in `14-ai-development/PR-GOVERNANCE-001.md` section 7, one
per language. Nothing else in the document moved.

Observed, in the order the experiment produced it:

```
cargo fmt --all -- --check                          exit 0
rust-workspace-test                                 failure   run 138943464904
     started 2026-11-25T02:54:38Z  completed 2026-11-25T02:55:15Z
     step outcome: Process completed with exit code 101
mergeable / mergeable_state                         true / blocked
PUT /pulls/1038/merge                               405
     {"message": "Required status check \"rust-workspace-test\" is failing."}
```

The `mergeable: true` line is the reason this experiment was run as an action
rather than a read. A merge gated on that field would have concluded the head was
mergeable while the merge endpoint refused it for a failing required check.

# Limitations

1. **The claim is dated.** It holds for the protection payload and workflows in
   place on `2026-11-25`. A renamed job, a removed context or a changed workflow
   invalidates it, and section 7 now says it must be re-run after such a change.
2. **Only the normal path was exercised.** `enforce_admins` is enabled and force
   pushes are disabled, but administrator bypass, a direct push with a token that
   ignores protection, and rule-set exceptions were not tested. The sentence
   states "cannot merge through the normal path", not "cannot merge".
3. **The probe branch still exists.** That is deliberate: deleting it would delete
   the failing run. The branch must never be merged, and it is the only artefact
   that keeps this claim auditable.
