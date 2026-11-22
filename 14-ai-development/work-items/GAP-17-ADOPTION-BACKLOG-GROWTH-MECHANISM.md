---
document_metadata:
  domain: ai-development
  role: work-record

  lifecycle:
    approval:
      decision_status: Draft
      approver: null
    evidence_verification:
      verification_status: Unverified
    usage_status: Active
    modification_status: Unchanged
    supersession:
      supersedes: []
      supersession_reason: null

  authority:
    canonical_status: Non-Canonical
    canonical_conflict_status: None
    normative_status: Informative
---

# GAP-17 — The adoption backlog grows because the policy's exclusions cannot be expressed at the granularity they occur

**Status:** Open — measured, mechanism identified, one decision needed
**Area:** 00-governance / GOV-DOC-002 / DM-01 / DM-14
**Measured at:** `main @ 46e2d243fc`, `2026-11-22T07:15Z`
**Related:** #564 (closed by #633), #480 (CI billing), GAP-03 (exclusion honesty), GAP-02 (incremental gate cannot prove new files)

## 1. The number, and its direction

```
$ python3 scripts/check_document_management.py
INCOMPLETE: no rule violations in 42 classified documents, but 558 governed documents are still unclassified
```

`--strict`: `FAIL: 558 error(s)`, and all 558 are `DM-01`. There is no other class of error in the tree. The whole of GOV-DOC-002's remaining redness is one rule: 558 documents have no `document_metadata`.

The direction matters more than the number. Two measurements, four commits apart:

| commit | unclassified | classified |
|---|---|---|
| `87f54bb4` | 556 | 42 |
| `46e2d243fc` | **558** | 42 |

The classified count did not move. Two documents were added and neither was classified:

```
+ 14-ai-development/work-items/AID-2026-045/prompt-v1.md
+ 14-ai-development/work-items/AID-2026-046/prompt-v1.md
```

Both are dispatch prompts. Both begin with `# AID-2026-0NN-PROMPT v1 —`. Neither carries metadata.

## 2. The mechanism

Policy §2 says, in both languages:

> Excluded: not scanned, and only when no architecture claim is made — source code, review transcripts, benchmark logs, **prompt text**.

`14-ai-development/work-items/AID-2026-045/prompt-v1.md` is prompt text by that definition. It makes no architecture claim. It dispatches work against an architecture that other documents specify.

But the scope registry expresses exclusion **only at directory granularity**:

```yaml
governed:
  - 14-ai-development        # <- the whole tree
excluded:
  ".github": {...}
  reviews:   {...}
```

`DM-14` rejects a `governed_files` entry whose parent directory is already governed:

```
DM-14 governed file {rel} is already covered by root {top}; drop the individual entry
```

There is no inverse mechanism. A file cannot be declared out of scope while its directory is in scope. `GOVERNED_FILES` exists for the opposite direction only — a file governed *although* its directory is not (`docs/governance/documentation-gaps.md` is the single entry).

So the policy has three states and the registry can express two of them per directory. When a policy category cuts across a directory — prompt text inside `14-ai-development`, review transcripts inside `reviews` (which happens to be wholly excluded, so that one works by luck) — the only expressible answer is "governed", which contradicts §2.

Every dispatch prompt authored into `work-items/` therefore lands as a `DM-01` error. That is not an author's mistake. It is the only outcome the mechanism permits.

## 3. Scale

Current 558, grouped by directory. The groups marked **cross-cutting** are policy-excluded categories living inside governed directories:

| count | path | cross-cutting? |
|---|---|---|
| 116 | `14-ai-development/work-items` | partly — contains prompts and work records |
| 34 | `14-ai-development/governance-register` | no |
| 33 | `13-engineering-decisions/technology-research` | no |
| 27 | `docs/en/14-ai-development` | mirrors of the above |
| 24 | `13-engineering-decisions/domain-model-research` | no |
| 24 | `docs/zh-CN/14-ai-development` | mirrors of the above |
| 16 | `14-ai-development/prompts` | **yes — §2 names "prompt text"** |
| 21 | `14-ai-development/work-items/*/prompt*.md` | **yes** |
| 7 | `14-ai-development/adr` | no |
| rest | mirrors, research, templates | mostly no |

By filename, across all directories:

| pattern | count |
|---|---|
| `prompt*` | 30 |
| `AID-*` | 39 |
| `GAP-*` | 41 |
| `OWNER-DECISION-*` | 6 |
| `r3-*` | 2 |
| README | 17 |
| other | 423 |

`prompt*` at 30 is the clearest instance: §2 excludes it by name, and it is counted anyway. The other 528 are genuine backlog — architecture documents that should be classified and have not been.

## 4. Why this cannot be fixed by classifying faster

Classifying 558 documents is real work, and it is the right work. But it does not converge while the inflow continues: every new dispatch prompt adds one, and dispatch prompts are produced continuously by the automation that drives this repository. Two arrived in the four commits measured here.

`DM-14` guards the `backlog:` count for `docs/` — `documents: 27` is checked against the disk, so that number cannot drift silently. No equivalent guard exists for the governed roots, because there is no declared count to compare against. The 558 is discovered, not declared.

## 5. The decision this needs

Three options. Each is one edit; they differ in what they claim.

**(a) Extend the registry to file-pattern exclusion.** Add a fourth state, `excluded_patterns`, matched against repository-relative paths inside governed roots, with the same bilingual-reason requirement as `excluded`. This makes §2's "prompt text" expressible where it actually occurs.

Cost: a new registry concept, a new `DM-14` check, and a real risk — a pattern exclusion can silently absorb files that do make architecture claims. The `docs/` history is the warning: `not-yet-migrated` was once a fourth state and it let 27 architecture documents sit outside governance while being described as governed-in-spirit. That was removed for good reason.

**(b) Classify the prompts.** Accept that a dispatch prompt inside a governed root is a governed document, and give it `role: work-record`, `normative_status: Informative`, `canonical_status: Non-Canonical`. Amend §2 to drop "prompt text" from the exclusion list, because the registry cannot honour it.

Cost: 30 frontmatter blocks now, and one more per future dispatch. Benefit: no new mechanism, and the classification is arguably correct — a dispatch prompt *does* encode which architecture documents govern which work, which is a claim about the architecture.

**(c) Declare the counts.** Leave the mechanism alone and add a `governed_backlog:` section to the registry with per-root counts, mirroring `backlog:` for `docs/`. The 558 becomes a declared number that `DM-14` checks against the disk, so growth is visible in the diff of the registry rather than discovered in a gate run.

Cost: does not reduce the number, only makes its movement auditable. Benefit: smallest change, no new exclusion semantics, and it makes option (a) or (b) a decision taken with the trend in hand rather than against a moving target.

## 6. Recommendation

**(c) first, then (b) for prompts.**

(c) is one section and one `DM-14` check, and it converts an unbounded discovery into a checked claim. It does not pretend to solve anything, which is the point: the 558 is not a defect to be suppressed, it is a backlog to be measured.

(b) over (a) because the `docs/` precedent shows what a fourth exclusion state costs. A pattern exclusion is a hole in the shape of a filename, and the next author who names a genuine architecture document `prompt-notes.md` inherits an exemption they never asked for. Classifying a dispatch prompt is cheap and honest; exempting a filename pattern is cheap and unverifiable.

(a) should be reconsidered only if the prompt inflow becomes large enough that per-file frontmatter is a real cost. At 30 documents it is not.

## 7. What is not in question

`DM-01` is not wrong. 528 of the 558 are architecture documents that genuinely lack classification, and the gate is correct to say so. The finding here is narrower: the gate's own policy excludes one category that its own registry cannot exclude, so a subset of the 558 is counted by contradiction rather than by oversight. Fixing that subset does not make the tree green and is not offered as if it would.
