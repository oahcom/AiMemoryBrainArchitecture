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
      last_verification_note: "Both findings were measured in this session against the committed tree and the live API, and both measurements are quoted below so they can be repeated without trusting this document."
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

# Session evidence — AID-2026-187

## Session role / use case

Role: IMPLEMENTER, acting also as the registering session. The account Owner is delegated by
standing instruction: no Owner opinion is supplied, so the session that measures a defect is the
session that registers the correction and merges it. This is recorded rather than glossed, because
it means no independent party reviewed the change before it landed; the mitigation is that both
findings rest on commands quoted in full below, not on judgement.

Use case: correct two records that credit work to a work item which did not perform it, and
register the correction as a work item so the change is attributable rather than an unattributed
edit to somebody else's manifest.

## Actual AI input

The prompt executed is `AID-2026-187/prompt-v1.md`, 7476 bytes, SHA-256
`0102ca64769d623c8987f51648d668a1f05cfd2f4d8524f64ac1451ad91a4c97`. It is the snapshot, not a
summary of it, and it is committed beside this file.

The dispatch that produced it, verbatim, was the standing instruction repeated across the preceding
sessions:

> 你不应该停下，因为我不输出观点，所有owner都可以是一个会话，你持续到收敛即可，若因需人类干预才可继续你可以当作为人类去收敛，但不能自己动手写代码。以最高效率去执行，动用所有能动用的资源，使用最多的子线程子代理

Two constraints in that instruction bind this work item and are worth naming: the session may act
as Owner where a decision is needed, and the session may not write code. This change is
documentation only for that reason, not because a checker would have been harder.

## AI-visible output

The measurements, in the order they were taken, each with the command that produced it.

**One: the three attributions.** A sweep for attribution phrasing over every manifest returns five
references, of which two resolve. The three that do not:

```
$ grep -rn "Corrected by AID-2026-090\|Refreshed by AID-2026-090" --include=*.md --include=*.yaml .
./14-ai-development/work-items/AID-2026-047/manifest.yaml:31:  ... Corrected by AID-2026-090."
./14-ai-development/work-items/AID-2026-072/manifest.yaml:67:  counter. Refreshed by AID-2026-090, which records the prior value.
./14-ai-development/work-items/AID-2026-076/manifest.yaml:72:  merged; it was not refreshed when it did. Refreshed by AID-2026-090, which records the
```

**Two: the target knows nothing about them.**

```
$ grep -c "AID-2026-047\|AID-2026-072\|AID-2026-075\|AID-2026-076\|AID-2026-080\|AID-2026-101" \
    14-ai-development/work-items/AID-2026-090/manifest.yaml
0
$ grep -in "correct\|refresh\|stale\|prior_value" 14-ai-development/work-items/AID-2026-090/manifest.yaml
43:  - {id: CVI-04, criterion: "Correction/removal/Forget creates successor, never edits predecessor."}
```

The single hit is an acceptance criterion about ContextVersion mutation. `AID-2026-090` is the
ContextVersion immutability work item; it is not a correction record and never was.

**Three: the record that does hold the prior values.** `AID-2026-101`'s `corrections:` block lists
six targets, the first three of which are exactly the three manifests above:

```
14-ai-development/work-items/AID-2026-047/manifest.yaml
14-ai-development/work-items/AID-2026-076/manifest.yaml
14-ai-development/work-items/AID-2026-072/manifest.yaml
14-ai-development/work-items/INDEX.md   (three separate cells)
```

**Four: the identifier the branch abandoned.** From `AID-2026-101`'s own `identifier_history`:

> This correction was prepared four times under identifiers that main assigned to other work items
> while it was in review: AID-2026-080 (taken by PR #1215), AID-2026-081 (taken by the GOV-DOC-001
> ratchet work item), AID-2026-090 (taken by the ContextVersion immutability work item, PR #1255)
> and AID-2026-101 is the fourth and current number.

That paragraph is what makes the three references self-contradicting. The record that performed the
correction declares the number abandoned in the same file whose neighbours still credit it.

**Five: the second defect, found while checking the first.** The pull request named in that
quotation does not exist as described:

```
$ GET /pulls/1255
 title: docs(context): correct merged ContextVersion Work Item to pending AID
 state: closed   merged: false   merge_commit_sha: null
$ GET /pulls/1241
 title: docs(context): define immutable ContextVersion boundary (AID-2026-090)
 state: closed   merged: true    merge_commit_sha: 72c9e68a158a5a0a00936fc7fc0adfc1fa024b5c
 merged_at: 2026-11-26T06:57:20Z
```

Every other file in the tree already cites #1241 — `AID-2026-090/manifest.yaml:51`,
`AID-2026-085:176`, `AID-2026-091:100`, `AID-2026-093:227` — so `AID-2026-101` is the single
outlier, and it is the file whose subject is the obligation to record prior values accurately.

**Six: the ordering, which rules out the alternative reading.** #1241 merged at 06:57:20Z and the
correction merged as #1248 at 08:18:17Z, eighty minutes later, so `AID-2026-090` could not have
performed the correction even if it had wanted to: at the time the three sentences were written,
the number had not yet been taken.

```
$ GET /pulls/1248
 merged: true   merge_commit_sha: 6c4956688cd4bf45f08266ae54840100faccefa5
 merged_at: 2026-11-26T08:18:17Z
$ git merge-base --is-ancestor 51d925bf origin/main   # the commit that wrote the three sentences
exit 0
```

## What this session did not do, and why

It did not amend the three commits that introduced the wrong identifier. They are ancestors of
`main`, their messages are part of the history the SHAs point at, and rewriting them would make
every recorded SHA disagree with the tree. The correction is a forward commit that names the
abandoned number, which is the same treatment `AID-2026-101` gave the stale cells it corrected.

It did not add a checker for attribution references. The user instruction forbids writing code, and
the honest assessment is that a checker here would be a small grep with a large false-positive rate:
the broad sweep that found these three returned 66 candidates of which 63 were ordinary
ownership references ("owned by AID-2026-014", "recorded in AID-2026-051-F3"). Narrowing it to
attribution verbs is what made the three visible, and that narrowing is a judgement about English
phrasing, not a rule a script can enforce without an allowlist that would rot.

## The 32 repins, old and new side by side

Every manifest below declared a digest that described no committed byte after PR #1281. The
declared column is read from `main a7e7c64b`, the base this pull request was opened against, and
the committed column is the SHA-256 of the prompt file at that same commit. Each file is exactly
58 bytes shorter than the byte count its manifest declared -- the two removed lines plus their
newlines -- and that uniformity is what identifies the cause as one mechanical edit.

| Work item | declared at `a7e7c64b` | declared bytes | committed bytes | committed digest |
|---|---|---|---|---|
| `AID-2026-059` | `65474e7f0927…ab7317` | 3866 | 3808 | `4881d6292e96…e34a8c` |
| `AID-2026-060` | `f9a01079c017…1ec5e9` | 7797 | 7739 | `7a9793427868…5ad605` |
| `AID-2026-061` | `7ea255ab98c0…6f0b81` | 18776 | 18718 | `6c0a9cc7e47f…f6e3cd` |
| `AID-2026-062` | `3f57662579cf…9766de` | 2927 | 2869 | `96358a3a9af4…1c6c42` |
| `AID-2026-063` | `4cf341c81da4…29efd8` | 2691 | 2633 | `411a0be8d6e7…81b4b5` |
| `AID-2026-066` | `1ae516e747ae…91c6ae` | 5921 | 5863 | `d6afe924427a…619c6c` |
| `AID-2026-067` | `07b49d7fa41e…5ac0da` | 5261 | 5203 | `c73aa6e35fdd…906ab5` |
| `AID-2026-068` | `7d55d2011f93…ab5a31` | 6031 | 5973 | `9a1e0e823d20…eb71f5` |
| `AID-2026-069` | `360c3273a8e6…816db6` | 6062 | 6004 | `12a7ebc07e9d…1e4c7e` |
| `AID-2026-070` | `b0013ed25ebd…da024a` | 6371 | 6313 | `6df00b015153…030d31` |
| `AID-2026-071` | `4c735edd42b8…8609c7` | 4303 | 4245 | `8080149aa3a0…631af5` |
| `AID-2026-072` | `1c8f58cff7d2…b67ea7` | 8623 | 8565 | `5e29f0695537…c67a8f` |
| `AID-2026-073` | `08eb2369f7f6…145c1a` | 5089 | 5031 | `278e8a975be3…b3a7cd` |
| `AID-2026-074` | `78044dfbc688…91a915` | 3967 | 3909 | `b5c8c5470850…f802fe` |
| `AID-2026-075` | `e85f9ae06779…ee4d83` | 4961 | 4903 | `0a1b6f824842…a2d0df` |
| `AID-2026-076` | `06ee5615ab9f…24f6b2` | 5525 | 5467 | `697484699587…a424c0` |
| `AID-2026-077` | `0339f07cd6bd…68a931` | 5621 | 5563 | `9de48039bb47…134aee` |
| `AID-2026-078` | `c2ae6f744dbf…d4b1a2` | 7533 | 7475 | `cb9890fc1c4e…1eb5d6` |
| `AID-2026-079` | `a2d216ee6479…afc81f` | 5790 | 5732 | `af8ad57de5ed…5e03a8` |
| `AID-2026-080` | `08f5e42efdef…4df19a` | 9932 | 9874 | `c071d0ee5978…96c2b8` |
| `AID-2026-081` | `7b761550e7cf…1eb3de` | 4428 | 4370 | `a02724519122…c44f0c` |
| `AID-2026-082` | `79bcd0738f9c…31b7cb` | 5831 | 5773 | `ff3eccdc7154…e7c5cd` |
| `AID-2026-084` | `acdd40d2b2b2…c86b55` | 4775 | 4717 | `3e02da52ac45…5d6745` |
| `AID-2026-085` | `17a8cd7583b8…b3f35e` | 7689 | 7631 | `80a1ecb80d09…5447f9` |
| `AID-2026-089` | `7682d9287605…92a903` | 4258 | 4200 | `e75f603f054d…409064` |
| `AID-2026-090` | `32e5a263ab34…3fe3a3` | 2034 | 1976 | `79288220c219…808d6c` |
| `AID-2026-091` | `11b2d92aa94d…1ac5d8` | 2058 | 2000 | `a531954b26c8…9e88ac` |
| `AID-2026-092` | `a459d7e523fb…13edb3` | 3772 | 3714 | `9de089512403…a53724` |
| `AID-2026-094` | `81644f71a94a…6ba2c5` | 6972 | 6914 | `766d5bd3f8ed…5b6d4e` |
| `AID-2026-097` | `4e3dbbd35d00…0fed56` | 4283 | 4225 | `70f4eb79f8c4…554d91` |
| `AID-2026-101` | `89ac65f2d58e…7e94c1` | 4470 | 4412 | `de3b9b80c952…22fc94` |
| `AID-2026-102` | `df3c53282d85…4e4e7a` | 4470 | 4412 | `468a1d4fd8f4…16072d` |

`AID-2026-106` is absent from that table because its byte count did not change. The same two keys
were removed and the replacement text happened to be the same length: declared
`0ef830572575708a3fd2c253d507b9ce97e8c39eff4fff04a7784e6a1daffd36` at 2998 bytes, actual
`ed3345b0f9c71b3cd7d8822bc4e42424000f17d4317bc03db5edc47486fa2ba0` at 2998 bytes. A repin that
guarded only size would have passed it.

## Why the prompt files were not restored

The two removed keys are `approval_scope.included_sections` and `approval_scope.included_assets`.
Ruling 76 (#833, comment 7120131295) ordered both removed, and `check_document_management.py` now
rejects them as DM-02 unknown keys. Restoring them to make the old digests true would put the
corpus back into the state that gate refuses, so the digests move to the files rather than the
files moving to the digests. That is the direction AID-2026-101 and AID-2026-102 took, and for the
same reason: the snapshot is the executed input, and a pin describes it rather than governing it.

This work item's own prompt and evidence file were first written with the two keys, copied from a
template that predates the ruling, and both were stripped before the first push. The DM-02 check
caught them -- the gate working as intended on a new file. What F4 records is that nothing
comparable runs over the digests of files that already exist, which is why 32 stale pins sat in
`main` for eight hours with every required context green.
