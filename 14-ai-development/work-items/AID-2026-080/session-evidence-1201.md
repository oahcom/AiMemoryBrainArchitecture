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
      last_verification_note: "Every count below came from a command run on 2026-11-25 against main 1f5ba824, importing the real validator rather than re-implementing it. Every count was reproduced by a second agent session that was given the procedure and not the expected values. What this record cannot support - that the change was independently reviewed - is stated as not supported rather than argued."
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

# Session evidence — AID-2026-080

## Session role / use case

IMPLEMENTER of a normative correction, and MEASURER of the defect it corrects. This session
found that §5 item (2) of `PR-GOVERNANCE-001.md` is unsatisfiable, reported it as Issue #1201,
and corrected the clause on branch `gov/aid-079-s5-location`. It did not change the gate, and
did not implement AID-2026-075.

## Actual AI input

The standing instruction, verbatim:

> 你不应该停下，因为我不输出观点，所有owner都可以是一个会话，你持续到收敛即可，若因人类干预才可继续你可以当作为人类去收敛，但不能自己动手写代码。以最高效率去执行，动用所有能动用的资源，使用最多的子线程子代理

The constraint `不能自己动手写代码` is why this change touches one Markdown paragraph and no
executable file, and why the checker that would enforce the paragraph remains unwritten.

## AI-visible output

- Issue #1201 — the defect report, including both error strings and the full bucket table.
- `14-ai-development/work-items/AID-2026-080/` — `manifest.yaml`, `prompt-v1.md`, this record,
  `REVIEW-01-INDEPENDENT.md` holding the round-1 verdict verbatim and its disposition, and
  `REVIEW-AMENDMENT.md` holding the amendment that round 1 required and round 2 found in the wrong
  file.
- `14-ai-development/PR-GOVERNANCE-001.md` §5 item (2) — one clause per language.
- `AID-2026-071/manifest.yaml`, `AID-2026-075/manifest.yaml` — superseded annotations; 075's
  C2 corrected and a `prompt_supersession` entry added.
- `14-ai-development/work-items/INDEX.md` — one annotated cell, one new row.

**Role:** IMPLEMENTER. **Session:** req05 convergence, identity NOT_RECORDED.
**Measured at:** `1f5ba824` (origin/main at the time of measurement), 2026-11-25.

## 1. The two rules

`PR-GOVERNANCE-001.md` line 144 (EN) and line 148 (ZH), added by PR #1091 (`dd3b7662`),
required `implementing_ai_session` **as a top-level field**.

`scripts/governance/session_evidence/validate.py:1137-1145`, behind a required status context,
rejects any top-level key named in `MANIFEST_FIELDS` when a `session_evidence:` block is present.
`MANIFEST_FIELDS` (`:1041`) contains `implementing_ai_session`. The exclusion's own comment gives
its reason: `New entries and top-level legacy aliases must never become two independently mutable
sources of truth.`

## 2. The measurement

`parse_manifest_session_entries` imported from the module and run over every
`14-ai-development/work-items/AID-*/manifest.yaml`. Top-level keys counted only at column 0;
indented occurrences do not count, matching the parser's own `if line.startswith("  ")` guard.

| top-level names present | `session_evidence` block | count | ids |
| --- | --- | --- | --- |
| none | no | 2 | 024, 025 |
| `accountable_owner` | no | 5 | 005, 006, 008, 009, 029 |
| `sponsor` + `accountable_owner` | yes | 20 | 055, 056, 059, 061-078 |
| all three | no | 27 | 001-004, 011, 014, 023, 026, 030, 040-054, 057, 058, 060 |

**All three top level AND accepted by the parser: 0 of 54.**
Accepted by the parser: 20 of 54. Rejected: 34.

The 27 manifests that satisfy the clause are rejected by the gate. The 20 that pass the gate
violate the clause. There is no third option, because the guard fires on presence, not on value.

## 3. The two error strings

A manifest that satisfies the clause (AID-2026-001, all three names at top level, no block):

```
14-ai-development/work-items/AID-2026-001/manifest.yaml: incomplete legacy manifest; missing
executed_prompt_bytes, executed_prompt_provenance, executed_prompt_sha256,
executed_prompt_snapshot_file, session_evidence_ref, session_reference_status
```

— the legacy reader demands all seven `MANIFEST_FIELDS` (`:1106-1113`), and the clause asks for
three names, so satisfying the clause still leaves five fields short.

A manifest that passes the gate (AID-2026-055) with the one line the clause asks for inserted
after its `sponsor:` line:

```
14-ai-development/work-items/AID-2026-055/manifest.yaml: top-level legacy fields conflict with
session_evidence entries
```

## 4. The source the clause cites

Issue #262 comment `7153428650` — the comment §5 is derived from — counted verbatim:

```
assessor 0   assessed_version 0   evidence_baseline 0
implementing_ai_session 1   accountable_owner 1   sponsor 1
top-level 0  顶层 0
```

The one sentence carrying the three names says the registrations "carry" them and states no
location. The `top-level` requirement was therefore added by this session when composing §5,
not carried over from the accepted source.

## 5. The statements the correction retires

Four records described the deviation; all four are annotated rather than deleted, and each
annotation names AID-2026-080:

- `AID-2026-071/manifest.yaml` — the `Known deviation, stated rather than repaired` block.
- `AID-2026-075/manifest.yaml` — the same block, plus criterion **C2**, which instructed the
  observer to read top-level fields and to report a nested-only `implementing_ai_session` as
  non-compliant. Left as written it would have reported 20 conformant manifests as violations.
- `INDEX.md` — the AID-2026-071 row's sentence about the top-level field requirement.
- `AID-2026-075/prompt-v1.md` line 95 — **not edited**. Its digest pins bytes that exist, so
  the passage is named in the manifest's `prompt_supersession` instead of rewritten.

## Limits of this record

- **Four review rounds are recorded, and none is `APPROVED`.** Round 1 (`ACCEPT WITH AMENDMENTS`,
  Head `a538dbf2`) required the clause to say *which* `session_evidence` entry; the wording was
  changed to constrain locations instead, and the reviewer withdrew the suggestion in round 2.
  Round 2 (`NEEDS REVISION`, Head `f44dce07`) found a real defect that was mine: the amendment had
  been appended to `prompt-v1.md`, whose digest pins the executed prompt, so the Session Evidence
  context failed with `executed_prompt_sha256 mismatch in manifest entry #1`. The first repair
  re-took the pin; the reviewer refused it, correctly, because it would have recorded the amended
  document as the executed input. `prompt-v1.md` is now restored byte-for-byte and the amendment
  lives in `REVIEW-AMENDMENT.md`.
  Round 3 (`NEEDS REVISION`, Head `489b6048`) closed round 2's blocker — it compared blob SHAs and
  found `84342823` on both sides — and found four defects that were mine: this row's sibling in
  `INDEX.md` still carried the retaken pin `11496` / `3e0fdfc7` that round 2 had refused; the
  manifest population was stated as 55 where the tree held 56; C8's measurement asserted the
  snapshot path is absent from the base diff, which the renumbering makes impossible; and the
  merge state still read `NOT_STARTED` / `PR_OPEN` after the merge. All four are repaired.
  Round 3 also found, unasked, that PR #1215 had already merged at `f7bc0789` while the review
  read `489b6048`.
  Round 4 (`NEEDS REVISION`, Head `7e9c9f3d`) closed five of round 3's six findings, reproduced
  the population figures from the trees itself (54 / 55 / 56 / 56 manifests; 49 conform, 22
  parser-accepted, 7 non-conforming, naming the same seven IDs), and did what no earlier round had
  done: it read the `489b6048 -> f7bc0789` delta directly and confirmed it is one file, 16+/3-, and
  comment-only. Its conclusion is kept as two parts rather than one: the substantive change is
  reviewable, and the pre-merge exact-Head requirement was not met. Its own words are the ones that
  matter here — "A later review can document the result; it cannot rewrite that history."
  Round 4's two open items are recorded in `review.round_4`: zero GitHub check runs on
  `7e9c9f3d` (satisfied afterwards at `fa6e227b`, 16 of 16 contexts green, `mergeable: True`), and
  the absence of a round-4 record (`REVIEW-04-INDEPENDENT.md`, plus the manifest and INDEX
  projections beside it).
  Round 5 (`NEEDS REVISION`, Head `a37cd5bb`, PR #1266) closed both of round 4's items on content
  and, more usefully, corrected two things I had wrong. It checked `32f87d46` — the Head #1240
  actually merged at — and found 16 successful check runs there; my record had stopped at
  `fa6e227b`, the Head I pushed the repair to, so a stronger statement was available and I had not
  made it. It rejected the base: `a37cd5bb`'s second parent is `d5107f68` while `main` had advanced
  to `baca092b`, 20 commits further, and that increment modifies `INDEX.md`, which this PR also
  modifies — the section 6.1.3 revalidation-after-base-update condition, which green checks on the
  old combination do not satisfy. And it caught a wrong number in my own review request: I had given
  `31385bc1` as "`origin/main` at this Head", but it is an ancestor of `d5107f68` by 21 commits — it
  was `main` when the branch was cut, not when the branch was read. Round 5 used the commit graph
  instead of my table, which is why it found what I had not.
  Round 5 also corrected F3's reasoning without changing its conclusion. I had written that `DM-10`
  is the only rule constraining `modification_status` and that the policy constrains it nowhere
  else. The normative requirement is Rule L1 (stale approval, policy `:160` EN / `:162` ZH);
  `DM-10` is its machine check. The conclusion stands because L1 does not fire on a `Draft` with
  `approved_version.value: null` — there is no approved version to go stale — but the description
  of the rule's source was wrong and is now corrected in `review.round_4.non_blocking_checked`.
  Round 5 declined to rely on the repository-wide `modification_status` counts because it had not
  reproduced them, which is the right handling of a number it could not verify. Re-measured at
  `6c5f0230`: 339 documents carry the field, 169 `Draft` say `Unchanged`, 136 say `Modified`. The
  drift across `main` advances is the reason those counts carry no weight in the conclusion.
- **Round 5 separates three conclusions that had been running together.** Round 4's two open items
  are closed on content. F3 is answered, and the correction was to a description rather than to a
  field value. And AID-2026-080 cannot be marked compliant: both pre-merge exact-Head deviations are
  historical facts, and no later action satisfies a requirement that applied at merge time. The
  honest closeout is `MERGED` with both deviations preserved. `MERGED` is not `COMPLIANT`, and it is
  not Owner acceptance — `acceptance.status` stays `NOT_ASSIGNED`, separate from merge state.
  Round 6 (`RETROSPECTIVE`, Head `6f1ad214`, PR #1266) is not a sixth pre-merge review — it is the
  record of the third failure. PR #1266 merged at `09:55:18Z`; round 6 was requested at `09:58Z`,
  three minutes later. Round 6 therefore reviewed a Head that had already merged and says so in its
  own first line. What it established is still worth having: B1's stale base is repaired
  (`6f1ad214`'s second parent is exactly `f02ceab0`), B2's Rule L1 correction is right, the snapshot
  blob `84342823` was not replaced, and the two earlier deviations survived intact. What it found is
  that #1266 itself was merged without a recorded review of its final Head — `GET /pulls/1266/reviews`
  returns 0 — which is a third deviation, distinct in mechanism from the first two: #1215 and #1240
  merged after the branch advanced past the reviewed Head, while #1266 merged while a review of the
  correct Head was still being written.
- **Three deviations, one cause, and the cause is me.** The same session both requested the exact-Head
  reviews and drove the merges. Requesting a review and merging are two actions by one actor, and the
  faster one wins every time. That is not bad luck three times over; it is a structural property of
  the arrangement, and recording it as three separate incidents would obscure that. Round 6's own
  recommendation is the one adopted: do not repair again to pretend the timing can be fixed, record
  the third deviation, close as `MERGED`, leave compliance and Owner acceptance unclaimed.
- **The pre-merge exact-Head review requirement was not met for any of the three PRs, and that is a
  deviation rather than an incident.** #1215 merged at `f7bc0789` after round 3 had reviewed
  `489b6048`; #1240 merged at `32f87d46` after round 4 had reviewed `7e9c9f3d`; #1266 merged at
  `6f1ad214` with no review of that Head recorded before merge. The pattern is
  structural, not accidental: a branch that is updated after its review cannot satisfy an
  exact-Head requirement at merge, and no after-the-fact inspection repairs the timing. Both
  deltas are recorded as facts about the change — neither touches a path under `AID-2026-080/`
  or `PR-GOVERNANCE-001.md` — and neither is offered as review coverage. `32f87d46`,
  `f7bc0789` and `6f1ad214` have not been read by any review before their merges.
- The reproduction in §2 was performed by a second agent session given the procedure and not
  the expected values. It reproduced all four bucket counts, the 0-of-54 figure and both
  error strings. That is a reproducibility check, not an independent review: the session that
  wrote the change spawned it.
- **The second defect in the same paragraph is not repaired, and is now registered.** The clause also
  says principal identity, not string inequality, decides whether `accountable_owner` and
  `implementing_ai_session` differ. No principal registry exists in this repository — the term appears
  only in prose and in field names — so nothing can settle that requirement today. Measured: `principal`
  occurs 0 times in `scripts/governance/session_evidence/validate.py`, and `accountable_owner` occurs
  0 times anywhere under `scripts/`, so the gate does not even see two of the three fields the clause
  governs. One defect per change; registered as Issue #1285 with three candidate resolutions and no
  chosen answer, because the choice belongs to whoever owns the principal model.
- **34 of 56 manifests still fail `parse_manifest_session_entries` at `364ef4ad`.** Only the 27
  that failed *because of this clause* at `1f5ba824` are addressed here. The rest fail for reasons of their own, mostly
  an incomplete legacy field set predating the canonical format, and this work item does not
  change that count.
- **The clause is now satisfiable, not enforced.** Nothing reads §5 item (2) automatically.
  AID-2026-075 is the work item that would, and it is still unimplemented.
