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
      last_verification_note: "The exception instrument was read from main at 1ae2d07; the quoted table rows are from EX-20261123-01.md at that ref, and the insertion point was taken from PR-GOVERNANCE-001.md section 5 as it stands at the same ref."
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

IMPLEMENTER for the wording, and the session that answers the deferred boundary
question. Issue #262 AC2 asks that the risk assessment name a session
responsible for it; the standard said nothing about assessment signature, so the
requirement could not be met by any record.

This session did not write production code. It added one clause to a normative
document and one work item that makes the addition accountable.

# Actual AI input

**Committed, byte-exact.** `prompt-v1.md` in this directory is the instruction the
change was carried out against, pinned at
`4c735edd42b80f43d04c26fdbbcc8e29662d96456394fbf5417a8386d88609c7`, 4303 bytes.

`executed_prompt_provenance` is `NOT_VERIFIED`: the digest proves the committed
file has not changed since it was pinned, not that it is byte-for-byte what the
session read.

The clause text is not this session's composition. It is reproduced from Issue
#262 comment `7153428650`, where Owner accepted it as the landing target. One
sentence is added to it, and that sentence is the answer below.

# Boundary question 5 — answered, not deferred

The owner recorded this as the only deferred item that blocks the merge:

> 5. 与 `EX-20261123-01` 例外机制的关系——DEFERRED，且合并前必须回答：例外若可覆盖本要求，条款即可被静默豁免。

**Answer: the exception instrument can reach a §5 obligation, so the clause
carries an explicit non-exemption sentence.** The evidence, from
`14-ai-development/governance-register/EX-20261123-01.md`:

| what was read | what it settles |
|---|---|
| the record's own header | "**这是本仓库第一条例外记录。**" … "本条记录即该句要求的产物。它不豁免任何东西，不改变任何 PR 的处置" |
| the `规则 / 缺失控制` row | the instrument names its target precisely: `PR-GOVERNANCE-001` §5「reviewer independent of the author」 |
| §2 of the record | "RULING-05 的边界原句：「例外本身绝不能将 HOLD 变为 MERGE」" |
| the closing sentence of §5 | "任何例外都必须显式记录，不得默默豁免。" — an exception is a disclosure channel, not a waiver |

Two things follow, and they are different. First, an exception record is not a
waiver: it cannot make an unmet control count as met, and it cannot turn a HOLD
into a merge. Second, an exception record *does* reach a §5 obligation when it
names that obligation — `EX-20261123-01` names the reviewer-independence duty by
name, which is how it is able to register anything at all.

So a general §5 exception would silently cover a new paragraph that said nothing
about its own reach. The clause therefore ends with: "本段只能由明确指名本段的例外记录豁免，泛指 §5 或审查独立性的例外不覆盖本段。" and the English side says the same thing. This narrows the reach; it does not pretend exceptions are impossible.

# AI-visible output

```
14-ai-development/PR-GOVERNANCE-001.md          section 5, one addition, both languages
14-ai-development/work-items/AID-2026-071/      manifest, prompt, this record
14-ai-development/work-items/INDEX.md           one row
```

# Limitations

1. **This does not re-approve the standard.** `decision_status: Approved` and its
   `approved_version` content hash are unchanged. The document already reads
   `modification_status: Pending-Reapproval`; it still does, and it is accurate.
2. **No check enforces the clause.** It states an obligation for the record that
   assesses a REQ; no validator reads it. C6 of the work item asks for a review at
   the session level, and `EX-20261123-01` records that this repository has zero
   APPROVED reviews, so the review is not claimed here.
3. **Four boundary questions remain deferred** — assessor qualification, whether
   a human must sign, what happens after a conclusion is overturned, and whether
   the requirement reaches single-PR risk. The clause is written so that none of
   the four is silently decided by it.
4. **The enforcement addendum is untouched.** `docs/en` and `docs/zh-CN`
   PR-GOVERNANCE-001-ENFORCEMENT.md summarise §5 in one line each; editing them to
   echo the new paragraph would claim a parity that does not exist today, so they
   are left as they are and the pull request says so.
