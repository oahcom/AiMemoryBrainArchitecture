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
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-26"
      last_verification_note: "Every claim in this prompt was measured in the session that wrote it: the three attribution strings were read out of the committed manifests, PR #1241 and PR #1255 were fetched from the API, and the commit ancestry was tested with git merge-base. No figure is copied from a pull request body."
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

# AID-2026-116-PROMPT v1 — Repoint three attributions that name the work item a renumbering abandoned

## User dispatch

Repository: `oahcom/AiMemoryBrainArchitecture`.
Base: `main` at `a7e7c64b` (observed 2026-11-26T11:49Z).
Task: correct two records that credit work to a work item which did not do it, and register
the correction so the change has a record behind it rather than arriving as an unattributed
edit.

## What was measured, and how

A sweep for attribution phrasing — `Corrected by`, `Refreshed by`, `Recorded by` and the like —
over every manifest in `14-ai-development/work-items/` returns five references. Two of them
resolve correctly (`AID-2026-075` cites `AID-2026-080`, which names it eight times; `AID-2026-092`
cites `AID-2026-102`, which carries the correction). Three do not:

| Referrer | Line | Says | What `AID-2026-090` actually is |
|---|---|---|---|
| `AID-2026-047` | 31 | `Corrected by AID-2026-090.` | ContextVersion immutability, PR #1241 |
| `AID-2026-072` | 67 | `Refreshed by AID-2026-090, which records the prior value.` | same |
| `AID-2026-076` | 72 | `Refreshed by AID-2026-090, which records the prior value.` | same |

The three are one mistake made three times, and it is a mistake of timing rather than of
substance. The correction branch carried four identifiers before it merged. It was prepared as
`AID-2026-080`, renumbered to `081`, renumbered to `090`, and renumbered to `101`; each collision
was discovered by rebasing, because the INDEX half merges cleanly under `merge=union` and only
the directory surfaces the clash. The three sentences were written while the branch still held
`090`, and they were not revisited when it lost the number.

`AID-2026-101`'s own `identifier_history` says so in as many words:

> `AID-2026-090` (taken by the ContextVersion immutability work item, PR #1255)

which makes the three references self-contradicting: the record that performed the correction
declares the number abandoned, and three files it corrected still credit it.

## Why this is a defect and not a cosmetic slip

A dangling reference is harmless — the reader sees nothing and looks elsewhere. These are worse.
`AID-2026-090` exists, it is a real manifest, and it is about an unrelated subject. A reader who
follows `Refreshed by AID-2026-090` lands on a plausible document, finds no prior values in it,
and has to decide whether the record is wrong or the manifest is. Both readings are available and
neither is excluded by anything in the tree.

It also breaks the property the INDEX refresh rule exists to guarantee. The rule requires the
refresh to be attributable — the correction is legitimate only because a record itemises what each
cell said before. Three of the four cells this branch corrected point at a record that does not
itemise them.

## The second defect, in the same family

`AID-2026-101`'s `identifier_history` names PR #1255 as the pull request that took `090`.
PR #1255 is `docs(context): correct merged ContextVersion Work Item to pending AID`, and it is
**closed without merging** — `state: closed`, `merged: false`. The pull request that merged the
ContextVersion work item is **#1241**, `docs(context): define immutable ContextVersion boundary
(AID-2026-090)`, merged 2026-11-26T06:57:20Z as `72c9e68a158a5a0a00936fc7fc0adfc1fa024b5c`.

The difference is the same one the INDEX rule insists on elsewhere: *closed unmerged* and
*merged* are not interchangeable, and writing one as the other is exactly the substitution the
rule forbids. Every other file in the tree gets this right — `AID-2026-090`'s own manifest,
`AID-2026-085`, `AID-2026-091` and `AID-2026-093` all cite #1241 — so `101` is the outlier, and it
is the record whose job was to be precise about prior values.

## Authorized scope

- `14-ai-development/work-items/AID-2026-047/manifest.yaml` — the trailing attribution of
  `prompt_digest_correction`.
- `14-ai-development/work-items/AID-2026-072/manifest.yaml` — the trailing attribution of
  `implementation.note`.
- `14-ai-development/work-items/AID-2026-076/manifest.yaml` — the trailing attribution of
  `implementation.note`.
- `14-ai-development/work-items/AID-2026-101/manifest.yaml` — the `PR #1255` clause of
  `identifier_history`.
- `14-ai-development/work-items/INDEX.md` — the `AID-2026-101` row, and the new row for this
  work item.
- `14-ai-development/work-items/AID-2026-116/` — this work item's own files.

## Explicitly out of scope

The measured content of every one of those four sentences. The digest `6d2c4080…0871`, the merge
SHA `2733283bff2b`, the PR numbers, the byte counts — all of it stays exactly as it is. Only the
identifier that says *who did it* changes, and only to the identifier that did. Nothing is
deleted: each sentence keeps its claim and gains the number that supports it, plus the abandoned
number, so a reader who has already followed the wrong pointer learns why it was wrong.

`AID-2026-090`'s manifest is not touched. It is correct, and a work item is not made responsible
for statements other files make about it.

## Acceptance criteria

- **AC1.** The three attributions name `AID-2026-101`, and each keeps the abandoned number visible
  as abandoned. Settled by reading the three fields and by `grep` returning no
  `by AID-2026-090` in the tree outside the historical review documents under `AID-2026-080/`.
- **AC2.** `AID-2026-101`'s `identifier_history` names #1241 as the pull request that merged
  `AID-2026-090`, and says #1255 closed unmerged. Settled against `GET /pulls/1241` and
  `GET /pulls/1255`.
- **AC3.** Every other measured value in the four edited fields is byte-identical to its prior
  value. Settled by a diff that shows only identifier substitutions.
- **AC4.** `python3 scripts/check_traceability.py --index-only` and
  `python3 scripts/ci/check_repository_hygiene.py` both pass on the branch, and the digest audit
  still reports zero mismatches — the prompt pin of this work item included.

## Second defect, measured on the base this pull request opened against

The three attributions above were the whole of this work item until the base moved. Re-running the
digest sweep on `a7e7c64b` before pushing returned 30 matching and 33 mismatching, where the same
sweep on `ba5b26b3` had returned 54 matching and 0. PR #1281 (commit `44b57170`, merged
2026-11-26T11:18:08Z) removed `approval_scope.included_sections` and `approval_scope.included_assets`
from 36 prompt snapshots and repinned only its own manifest, leaving 32 others declaring the digest
of text that no longer exists anywhere.

That is the larger defect and it is fixed here as well: 32 manifests repinned, one more found with
an unchanged byte count (`AID-2026-106`), and 33 INDEX cells that restate those digests repinned to
match. Every superseded value is in the evidence file.
