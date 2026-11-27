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
        - "14-ai-development/work-items/AID-2026-197/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Records the dispatched task scope, not a raw transcript; the session identifier and the verbatim model input stream were not captured."
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
    canonical_scope_keywords:
      - "gate"
      - "ratchet"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# Prompt snapshot — AID-2026-197

**Scope snapshot, not a verbatim raw capture.** This file records the task as it was
dispatched. The dispatching session supplied two files — a common contract and a unit
brief — plus a work-tree assignment. What is reproduced here is the instruction that
selected the work, paraphrased where the original is operational boilerplate and quoted
where it constrains the outcome. The full prompt stream was not captured, which is why the
manifest says `prompt_status: NOT_RECORDED`.

## The assigned unit

> UNIT gates-a · 两个"看起来在查、其实没查"的门禁
>
> worktree: `D:\code\wt-gates-a`, branch `fix/2026-11-27-gates-a`.
>
> 1. `check_source_revision_pointers.py`: `Source revision: main` only counts as
>    `NON_BLOB_REFERENCE`, never as `BAD`, contradicting the docstring "every live pointer
>    resolves"; and a document with several pointers compares all of them against
>    `links[0]`, so b's blob is checked against a.
> 2. `gate_ratchet.py` normalization loses information before the comparison: everything
>    after `-> ` is truncated (a second failure on the same path merges into the first),
>    and real items that begin with `OK`/`PASS`/`FAILED`/`Ran ` are never reported.

## What was asked for

1. Fix `check_source_revision_pointers.py`: a non-blob reference such as `main` must not
   pass silently; multiple pointers must each be compared with their own source.
2. Fix `gate_ratchet.py` normalization: keep what follows `-> ` (or normalize on the whole
   line); lines beginning with `OK`/`PASS`/`FAILED`/`Ran ` must not be discarded.
3. Add, for each fix, a test that can be falsified — construct the counter-example: two
   pointers with different blobs; two lines that differ only after `->`.
4. Run both scripts on `main`, record before/after exit codes and item counts. If the fix
   turns a script red, that is evidence the original under-reported: record the red items
   and the reason, and do not widen a condition to keep it green.

## What was forbidden

- Changing a pass condition, other than the under-reporting named above.
- Changing a baseline.
- Changing branch protection, closing the Issue, deleting a required context, editing files
  outside the unit, or fabricating a SHA, a test output or a gate result.
- Stopping to ask: the brief says execute end to end and report.

## Standing constraints from the common contract

- Work only in the assigned work tree; never in the shared clone.
- Merge `origin/main` first so the pull request is never behind.
- Every work record carries block-style YAML metadata; inline `{}` fails the metadata gate.
- A pull request body needs `Related issue(s)`, `AI-assisted work: YES` and a
  `Session evidence reference(s)` path that resolves in the head tree.
- Merge only when all sixteen required contexts are `completed/success` on the exact head
  SHA, the branch is not behind, and the merge method is `merge`.
- Report the model substitution: the free pool was rate-limited, so this unit ran on
  `opencode-go/deepseek-v4.1-flash`.
