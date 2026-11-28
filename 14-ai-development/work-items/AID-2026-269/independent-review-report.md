---
document_metadata:
  steward: "user-authorized operator (delegated by account owner)"
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Independent L3-2 re-execution; every number below was computed by this reviewer from Git objects."
    usage_status: Active
    modification_status: Unchanged
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "Independent review of review case #1278 (AID-2026-269 / AID-2026-092)"
    canonical_scope_id: "ai-development/aid-2026-269-independent-review"
    canonical_scope_keywords:
      - "exact-head-review"
      - "independent-review"
      - "l3-2"
      - "declaration-mismatch"
    canonical_conflict_status: None
    normative_status: Informative
---

# Independent review — review case #1278 / AID-2026-092 prompt digest

Reviewer: **L3-2** (independent; authored no file in this change set).
Method: every value was recomputed from Git objects by this reviewer. No value was
taken from `review-case-1278.md`, `evidence.md`, the issue text, or any other
agent's report. No other reviewer's report was read.

Scope of this document: the **accuracy of the review case**, not the truth of the
issue it reviews. Both verdicts are stated separately in §V.

---

## 0. Candidate binding

| Field | Value |
|---|---|
| repository | `oahcom/AiMemoryBrainArchitecture` |
| worktree | `D:\code\wt-aid268` |
| branch | `review/2026-11-27-aid269-exact-head-review` |
| **PR head (findings bind here)** | **`c7d56bbee7a404c575c60f78055e366faed85f0a`** |
| **PR head tree** | **`94580c56c2827e5584d8cd59fcaaad22934cede2`** |
| merge base with `origin/main` | `af2660d55a93278157fa6668aba338daf81e127c` |
| `origin/main` at fetch | `7ecf2a8e7d1e40a13f6af6d4335a6766a222194f` |
| `origin/main` at end of measurement | `5670357db7a836d4f26838dbaf99494af41e2b65` |
| commits on branch beyond merge base | 1 (`c7d56bbe`) |
| refs at first enumeration | 2654 |
| commits reachable from `--all` at first enumeration | 9660 |
| refs / commits at end of run | 2668 / 9708 |
| Git / Python | `git version 2.56.1.windows.1` / `Python 3.12.3` |

`origin/main` and the ref set moved during this review because the worktree shares
its common git dir with other sessions that fetch concurrently. The candidate is
pinned, so nothing below depends on the moving refs except the history envelope,
which only widened.

**All findings in this document bind to `c7d56bbe`, tree `94580c56`.** Where the
review case binds to a different SHA, both measurements are reported side by side
and the difference is the finding.

Every value below was read from Git objects (`git show <sha>:<path>`), never from
the working tree, so working-tree state cannot affect any number here.

**Concurrent-writer note.** The worktree was clean when this review started
(`git status --short` empty). During the run, two files this reviewer did not
touch became modified in the working tree:

```
 M 14-ai-development/work-items/AID-2026-269/exact-head-review-protocol-v1.md
 M 14-ai-development/work-items/AID-2026-269/review-case-1278.md
?? 14-ai-development/work-items/AID-2026-269/independent-review-report.md   <- this file
```

The uncommitted edit to `review-case-1278.md` adds a `result` column to the §9.1
grade table. It is **not** part of `c7d56bbe` and is not reviewed here; the
committed blob (`52c4da52…`, 23675 B) is what §9 and §10 grade. Recorded so that a
later reader does not attribute the dirty tree to this review.

---

## 1. Locking the candidate

Command:

```
git -C D:\code\AiMemoryBrainArchitecture fetch origin --prune
git -C D:\code\wt-aid268 rev-parse HEAD
git -C D:\code\wt-aid268 rev-parse "HEAD^{tree}"
git -C D:\code\wt-aid268 merge-base HEAD origin/main
git -C D:\code\wt-aid268 log --oneline origin/main..HEAD
```

Exit code: 0. Output excerpt:

```
HEAD=c7d56bbee7a404c575c60f78055e366faed85f0a
TREE=94580c56c2827e5584d8cd59fcaaad22934cede2
ORIGIN_MAIN=7ecf2a8e7d1e40a13f6af6d4335a6766a222194f
--- merge-base with origin/main ---
af2660d55a93278157fa6668aba338daf81e127c
--- commits on branch not in origin/main ---
c7d56bbe docs(aid-2026-269): add the exact-head review protocol and the #1278 review case
```

**Discrepancy against the review case, item 1.** `review-case-1278.md` §1 states
`candidate SHA (git rev-parse HEAD) = 987d26021affbb5ba6d651e0fb5985d6bd4026a5`
and `candidate tree SHA = 2a73559ebf1406ef3892c4c71dce33c20731e446`.

Command:

```
git -C D:\code\wt-aid268 log -1 --format="%H|%cd|%s" --date=iso-strict 987d2602
git -C D:\code\wt-aid268 rev-parse "987d2602^{tree}"
git -C D:\code\wt-aid268 merge-base --is-ancestor 987d2602 HEAD
git -C D:\code\wt-aid268 ls-tree -r --name-only 987d2602 -- "14-ai-development/work-items/AID-2026-269/"
```

Exit code: 0. Output excerpt:

```
987d2602|2026-11-27T12:55:00+08:00|Merge pull request #1365 from oahcom/w9/aid-2026-252-steward
tree_987d2602=2a73559ebf1406ef3892c4c71dce33c20731e446
tree_HEAD=94580c56c2827e5584d8cd59fcaaad22934cede2
ancestor_exit=0        (987d2602 IS an ancestor of HEAD)
--- ls-tree of the 269 directory at 987d2602 ---
(empty)
```

`987d2602` is a **main-branch merge commit** (`Merge pull request #1365`), it is an
*ancestor* of the head, and it does not contain the work item under review at all.
It cannot be `git rev-parse HEAD` of this branch, and it is not.

Timeline check (`%cd`, ISO strict):

| commit | committer date | UTC |
|---|---|---|
| `10d33b3f` (case's "origin/main at first lock") | 2026-11-27T12:08:06+08:00 | 04:08:06Z |
| **case's claimed review window** | — | **04:09:16Z – 04:22:51Z** |
| `987d2602` (case's claimed candidate) | 2026-11-27T12:55:00+08:00 | **04:55:00Z** |
| `c7d56bbe` (actual head, author date) | 2026-11-27T13:17:34+08:00 | 05:17:34Z |

The claimed candidate was created **32 minutes after the claimed review ended**,
and the document that reports that review window is committed at 05:17Z. The
§1/§7 metadata is therefore not a reproducible record of a review performed on
`987d2602` inside that window.

---

## 2. Declared values, read from Git objects only

Command:

```
git -C D:\code\wt-aid268 show HEAD:14-ai-development/work-items/AID-2026-092/manifest.yaml
git -C D:\code\wt-aid268 ls-tree -r HEAD -- "14-ai-development/work-items/AID-2026-092/"
```

Exit code: 0. Output excerpt (blob identity at head):

```
100644 blob 50e41dfa0c6f68ee1342fb7b107de286ff0b30b6	14-ai-development/work-items/AID-2026-092/manifest.yaml
100644 blob 7adf342a51f924cb732129ba3052ca65a832ea75	14-ai-development/work-items/AID-2026-092/prompt-v1.md
```

Declaring lines **at the head `c7d56bbe`**:

```
25 | prompt_id: AID-2026-083-PROMPT
27 | prompt_file: 14-ai-development/work-items/AID-2026-092/prompt-v1.md
28 | prompt_status: RECORDED_NOT_FROZEN
29 | prompt_sha256: 9de0895124032230b3418ff062ef2d590d27f37582d2847032a46b7116a53724
30 | prompt_bytes: 3714
31 | prompt_digest_correction: >-
32 |   The digest recorded at registration was 9be8aebf7d595f81cc062e5c03a67fd8317aeefaf69dd635fd9031f112dc25d1
33 |   at 2455 bytes. It matched no version of prompt-v1.md at any commit reachable from any ref:
34 |   enumerating every distinct blob at this path and at AID-2026-083/prompt-v1.md across
35 |   `git rev-list --all` returns exactly four (7689, 3772, 2915 and 4137 bytes), none of them 2455.
```

Declaring lines at the review case's claimed candidate `987d2602` (blob
`227c761d82984fb671ab3fa53f57b41c10bdd04c`, 7680 B, sha256 `a91b25f1…`):

```
27 | prompt_file: 14-ai-development/work-items/AID-2026-092/prompt-v1.md
29 | prompt_sha256: a459d7e523fbba4ffb8c0f6ade8d3d8c1ec6ce45b95c3f48f65b192c0413edb3
30 | prompt_bytes: 3772
35 |   `git rev-list --all` returns exactly four (7689, 3772, 2915 and 4137 bytes), none of them 2455.
```

**Finding.** The review case's §2 quotes `prompt_sha256: a459d7e5… / prompt_bytes: 3772`
as the *current* declaration. That is true of `987d2602`. It is **false of the
head**: at `c7d56bbe` the manifest declares `9de08951… / 3714`, i.e. the value the
case calls "actual". The manifest blob the case identifies
(`227c761d…`, sha256 `a91b25f1…`) is the `e0d6a992` version, not the head's
`50e41dfa…` / sha256 `11759f4c…`.

---

## 3. Recomputation of the prompt blob

Command (binary pipe, no text decode):

```
git cat-file blob 7adf342a51f924cb732129ba3052ca65a832ea75 | python -c "import sys,hashlib;b=sys.stdin.buffer.read();print('prompt_bytes',len(b));print('prompt_sha256',hashlib.sha256(b).hexdigest())"
```

Exit code: 0. Output:

```
prompt_bytes 3714
prompt_sha256 9de0895124032230b3418ff062ef2d590d27f37582d2847032a46b7116a53724
```

Manifest blob, same method:

```
manifest_bytes 7680
manifest_sha256 11759f4c586af7654fb0c96d3d8b1783e59a293cc3a1dc7f0ea6eae70722c6c6
```

**Confirmed:** the committed prompt at `c7d56bbe` is 3714 bytes /
`9de0895124032230b3418ff062ef2d590d27f37582d2847032a46b7116a53724`. The case's
"actual" pair is correct.

---

## 4. History enumeration

Envelope at enumeration: **2654 refs**, **9660 commits** reachable from
`git rev-list --all`. Paths enumerated separately; each commit's blob read with
`git show <c>:<path>` and hashed as bytes.

```
git rev-list --all -- <path>            # per path
git show <commit>:<path> | sha256        # per commit
```

Exit codes: 0 for all three paths. Output:

### 4.1 `14-ai-development/work-items/AID-2026-092/prompt-v1.md` — 2 commits

| commit | bytes | sha256 |
|---|---|---|
| `44b57170b86c` | 3714 | `9de0895124032230b3418ff062ef2d590d27f37582d2847032a46b7116a53724` |
| `f61dc15a7701` | 3772 | `a459d7e523fbba4ffb8c0f6ade8d3d8c1ec6ce45b95c3f48f65b192c0413edb3` |

### 4.2 `14-ai-development/work-items/AID-2026-083/prompt-v1.md` — 4 commits

| commit | bytes | sha256 |
|---|---|---|
| `44c530a02e1c` | 7689 | `0c0ce002db720c6a46186a94a591bc13939768627910b447960cbbd4f5cfe640` |
| `45045ed319ca` | ABSENT (`git show` rc=128) | — |
| `ecbb9bc74358` | 2915 | `9614ddf7013eaaa6f740842163f5f2f53d9475103d602fc0858bc62b3608166f` |
| `e5068b65c5f0` | 4137 | `7ce260dfb8f1a959bce48ac3abcbfa2d53bbd0c984663013136fbcd3152b67ec` |

### 4.3 `14-ai-development/work-items/AID-2026-092/manifest.yaml` — 5 commits

| commit | bytes | sha256 |
|---|---|---|
| `e7f8a28780d1` | 8232 | `7ab84099592e142e05c4a73d8f02a104040d66c4f80ba7cd8f725639775791b2` |
| `27bfa5977642` | 7680 | `11759f4c586af7654fb0c96d3d8b1783e59a293cc3a1dc7f0ea6eae70722c6c6` |
| `e0d6a9920cee` | 7680 | `a91b25f165766b7d7ee15f1a25269f98a4564dceeb4e6acf4e5db6b405a1f5ca` |
| `3619502712b4` | 6691 | `daec20c56161a691667f2d4ba453eef45fac1b784159971615c4e5dcd5b00c48` |
| `f61dc15a7701` | 6677 | `64af89558212bce7b85e39b9af4c5bbea35429807f56b5cc66fee2fca8aaf326` |

**Findings against the case.** The per-path prompt tables reproduce exactly. The
manifest table does not: the case lists 4 commits; the current envelope contains
**5**, the extra one being `e7f8a287` (8232 B, 2026-11-27T13:32:19+08:00,
"docs(aid-2026-251): migrate AC4 references cohort batch 3/4 (61-66)"), which is
not an ancestor of the head. That is envelope drift, not a defect in the case.

The material defect is different: the case's §4.3 states that `27bfa597` "is
**not** an ancestor of the candidate". At the head that is false —

```
git merge-base --is-ancestor 27bfa597764281b3abdbe939843b45c14f25b388 HEAD  ->  exit 0
```

`27bfa597` **is** an ancestor of `c7d56bbe`, and it is the commit that changed the
manifest to `3714` / `9de08951`. This is the mechanism by which the case's E1
evaporates at the head.

### 4.4 Distinct prompt versions across both paths

`7689`, `3772`, `2915`, `4137`, `3714` — **five**, each at exactly one commit. No
commit at either path has 2455 bytes.

---

## 5. Did 2455 / `9be8aebf…` ever exist?

### 5.1 At the two prompt paths, across all refs

```
9be8aebf7d59... (declared 2455 bytes) -> 0 hits []
a459d7e523fb... (declared 3772 bytes) -> 1 hits [('f61dc15a7701', '.../AID-2026-092/prompt-v1.md', 3772)]
9de089512403... (declared 3714 bytes) -> 1 hits [('44b57170b86c', '.../AID-2026-092/prompt-v1.md', 3714)]
```

### 5.2 Across the entire object database (stronger than the case's envelope)

Every object in the ODB, reachable and unreachable:

```
git cat-file --batch-all-objects --batch-check=%(objectname) %(objecttype) %(objectsize)
git cat-file --batch   # then sha256 each blob's content
```

Exit code: 0. Output:

```
ODB_objects_total 63300
ODB_blobs 14103
ODB_commits 10748
blobs_size_2455: 1
   72993b655aa5e72edab78055415fbacf43fc66a3 2455 9f21343969ef0299ff43490de777ae3fa4c596139f0426492a37fd7f294d409f no owners= ['14-ai-development/work-items/AID-2026-082/session-evidence.md']
sizes_within_25_of_2455: [2433, 2438, 2439, 2440, 2443, 2444, 2449, 2450, 2451, 2452, 2453, 2455, 2458, 2462, 2463, 2464, 2465, 2471, 2472, 2473, 2476, 2480]
blobs_hashed 14104
sha256_equals_9be8aebf: []
target_absent_from_entire_ODB: True
```

Corroborated by a second, independently implemented full scan (per-object
`git cat-file blob`, not the `--batch` stream), taken earlier in the same run at an
envelope of 63,050 objects / 14,053 blobs:

```
ODB_objects_total 63050
ODB_blobs 14053
blobs_with_size_2455: 1
    72993b655aa5e72edab78055415fbacf43fc66a3 2455 9f21343969ef0299ff43490de777ae3fa4c596139f0426492a37fd7f294d409f no-match owners= ['... AID-2026-082/session-evidence.md']
blob_object_named_target_sha: []
blobs_whose_sha256_equals_target: []
sizes_within_40_of_2455: [2418, 2419, 2420, 2425, 2433, 2438, 2439, 2440, 2443, 2444, 2449, 2450, 2451, 2452, 2453, 2455, 2458, 2462, 2463, 2464, 2465, 2471, 2472, 2473, 2476, 2480, 2490, 2494, 2495]
```

This second scan does not assume the declared 2455-byte size: it hashes **every**
blob, so the absence of `9be8aebf…` is established unconditionally, not only among
2455-byte candidates. Both scans agree.

**Answer to both questions: no.** No reachable commit contains a 2455-byte version
of either prompt path, and sha256
`9be8aebf7d595f81cc062e5c03a67fd8317aeefaf69dd635fd9031f112dc25d1` does not exist
as the content of **any** blob in the object database (14,104 blobs hashed), so it
cannot have existed at any path in any commit, reachable or not.

Closest matches:

| match | value | delta |
|---|---|---|
| only 2455-byte object in the ODB | `AID-2026-082/session-evidence.md` (`72993b65…`, sha256 `9f213439…`) | size exact, digest unrelated |
| nearest prompt version by size | 2915 bytes (`ecbb9bc7`, `9614ddf7…`) | −460 |
| next nearest | 3714 bytes (`44b57170`, `9de08951…`) | +1259 |

This reproduces the case's F6 basis, including its statement that "the only
2455-byte object belongs to an unrelated file".

---

## 6. Did `44b57170` remove `included_sections` / `included_assets`, net −58?

```
git diff --numstat f61dc15a 44b57170 -- 14-ai-development/work-items/AID-2026-092/prompt-v1.md
```

Exit code: 0. Output:

```
0	2	14-ai-development/work-items/AID-2026-092/prompt-v1.md
```

Byte measurement and hunk:

```
before 3772 after 3714 delta -58
@@ -12,8 +12,6 @@
         value: null
       approval_scope:
         type: Full-document
-        included_sections: []
-        included_assets: []
       approval_applicability: Not-Applicable-To-Current-Version
```

**CONFIRMED.** `44b57170` deletes exactly `included_sections: []` and
`included_assets: []`; 0 insertions, 2 deletions; 3772 − 3714 = **−58 bytes**.

---

## 7. Were manifest and prompt both first introduced in `f61dc15a`?

```
git diff-tree -r --name-status --no-commit-id 1e7f4d0a f61dc15a -- 14-ai-development/work-items/AID-2026-092/
git log -1 --format="parents=%P" f61dc15a
git rev-list --all -- <each path>
```

Exit code: 0. Output:

```
A	14-ai-development/work-items/AID-2026-092/ISSUE-1037-validator-and-metadata-verification.md
A	14-ai-development/work-items/AID-2026-092/ISSUE-1189-approval-provenance.md
A	14-ai-development/work-items/AID-2026-092/ISSUE-1197-phase-freeze-audit.md
A	14-ai-development/work-items/AID-2026-092/manifest.yaml
A	14-ai-development/work-items/AID-2026-092/prompt-v1.md

parents=1e7f4d0a7baf06103dc3bd504293e25e53bd24c2 c92953fd6e6465a2dbbaaa2f1ca038061c219093
```

`f61dc15a` is the oldest entry in `git rev-list --all` for both paths.

**CONFIRMED.** Both files are added (`A`) in `f61dc15a` against its first parent.

---

## 8. INDEX cross-check

```
git rev-parse HEAD:14-ai-development/work-items/INDEX.md
git cat-file -s <blob>
# then scan every line for a459d7e5 / 9be8aebf / 9de08951
```

Exit code: 0. Output at the head `c7d56bbe`:

```
79f065c67068e002ebb61e085d4e953ae8fbd86c
212188
lines 320
---LINE 67 ---
| [AID-2026-092](AID-2026-092/manifest.yaml) | ... `AID-2026-083-PROMPT` v1 — `14-ai-development/work-items/AID-2026-092/prompt-v1.md`, 3772 bytes, SHA-256 `a459d7e523fbba4ffb8c0f6ade8d3d8c1ec6ce45b95c3f48f65b192c0413edb3`. The digest recorded at registration was `9be8aebf…` at 2455 bytes, ...
```

At the review case's candidate `987d2602`:

```
blob 3e652348dc7df5286d4ba0408091a1f052968c07
lines 308
line 65 len 1344
```

**CONFIRMED WITH CORRECTION.** The INDEX does repeat the same wrong pair — but at
the head the row is **line 67**, not line 65, and the blob is `79f065c6`
(212188 B, 320 lines), not `3e652348` (308 lines). Line 65 and blob `3e652348` are
correct for `987d2602` only. Only one line carries the digest, as the case says.

---

## 9. Grade audit against my own measurements

Rule as stated in the case (§9.1 + §9.3): E1 = declared ≠ actual at the candidate
head; E2 = asserted historical existence with no historical existence; E4 =
incomplete evidence (including an incomplete count); E0 = verified.

| # | checked declaration | case grade | my measurement at `c7d56bbe` | verdict |
|---|---|---|---|---|
| F1 | `manifest.yaml:29` `prompt_sha256` | E1 | declared `9de08951…` = actual `9de08951…` | **CONTRADICTED — should be E0** |
| F2 | `manifest.yaml:30` `prompt_bytes` | E1 | declared `3714` = actual `3714` | **CONTRADICTED — should be E0** |
| F3 | `INDEX.md` same-row repeat | E1 | INDEX says `3772` / `a459d7e5…`, prompt is `3714` / `9de08951…` | holds (line is 67, not 65) |
| F4 | "exactly four blob versions" | E4 | five exist: 7689, 3772, 2915, 4137, 3714 | holds |
| F5 | no fixed blob field | E4 | no `*_blob_sha` key at head; identity only via `ls-tree` (`7adf342a…`) | holds |
| F6 | "2455 / `9be8aebf…` never existed" | E0 | 0 hits at both paths; absent from all 14,104 ODB blobs | holds |
| F7 | "3772 / `a459d7e5…` at first introduction" | E0 | `f61dc15a` has 3772 / `a459d7e5…` for both files | holds |
| F8 | registration pin `9be8aebf…` / 2455 | E2 | value has no historical existence anywhere | holds |

**Six of eight grades reproduce at the head. Two are contradicted (F1, F2.)**

The two contradicted grades are not measurement noise: they are the consequence of
the wrong candidate binding in §1. At the case's own candidate `987d2602` both E1s
reproduce exactly (manifest declares `3772` / `a459d7e5…`, prompt is `3714` /
`9de08951…`). The case is internally consistent; it is bound to the wrong commit.

Recomputed totals at the head: E0 ×4 (F1, F2, F6, F7), E1 ×1 (F3), E2 ×1 (F8),
E4 ×2 (F4, F5) — **verified 4 / failed 2 / unverifiable 2**, `overall_result` still
**FAIL**, but for a narrower reason than the case gives.

---

## 10. JSON block arithmetic

```
declarations_checked 8
verified 2 failed 4 unverifiable 2 sum 8
findings_len 6
grades {'E1': 3, 'E4': 2, 'E2': 1}
ids ['D2', 'D3', 'D4b', 'D7', 'D6', 'H1']
overall FAIL
candidate_sha 987d26021affbb5ba6d651e0fb5985d6bd4026a5
candidate_tree_sha 2a73559ebf1406ef3892c4c71dce33c20731e446
grade_table_rows 8 ['F1','F2','F3','F4','F5','F6','F7','F8']
```

- The §9.1 table has **8** graded rows (F1–F8) and `declarations_checked` = 8. ✔
- The buckets sum to 8 (`2 + 4 + 2`). ✔
- `overall_result: "FAIL"` follows from `failed: 4 > 0`. ✔
- **`findings` has only 6 entries.** The two E0 declarations (F6, F7) are counted
  in `verified` but are not enumerated anywhere in `findings`. The JSON therefore
  claims 8 declarations checked while enumerating 6. ✘

Also: `candidate_sha` / `candidate_tree_sha` in the JSON are `987d2602` /
`2a73559e` — a main merge commit that is not the head of this change and does not
contain the work item. The machine-readable result is bound to the wrong object.

---

## 11. `session-evidence.md` deliverable digests

All four recomputed from committed blobs at `c7d56bbe`:

| deliverable | quoted bytes / sha256 | recomputed | result |
|---|---|---|---|
| `exact-head-review-protocol-v1.md` | 17014 / `211bd96bb61a307f93795942c463af53225c4522c5f4618fb8a4009bae71512f` | 17014 / `211bd96b…` | **MATCH** |
| `review-case-1278.md` | 23675 / `1369678c6f9c43a4734713f8dd9c04b4bb28b2e3b5c925c45aa65e6a3f3c8726` | 23675 / `1369678c…` | **MATCH** |
| `evidence.md` | 31175 / `09cffdb163a6aeb84f0a004c042be33e374ab51ec1e06bee721d87b46b2a537e` | 31175 / `09cffdb1…` | **MATCH** |
| `prompt-v1.md` (AID-2026-269) | 16877 / `b2ddd33dee27df4d4c88e01c796f4d70d7a4e663d4504441615f1099e7162170` | 16877 / `b2ddd33d…` | **MATCH** |

**All four digests are correct as committed.** ✔

Related defect found while checking this: `evidence.md` §E17 records a self-check
output that no longer matches the committed artifacts —

```
recorded in §E17 : evidence.md 24995, review-case-1278.md 16288,
                   "checked 6 verified 2 failed 4 unverifiable 0 findings 5"
committed now    : evidence.md 31175, review-case-1278.md 23675,
                   declarations_checked 8, unverifiable 2, findings 6
```

§E17's assertion that "the JSON block parses and its counts agree" describes an
earlier revision of the review case, not the one committed. The raw-log appendix
was not re-run after the adjudication append.

---

## 12. Was any `AID-2026-092/` file modified by this branch?

```
git diff --name-only af2660d5...HEAD -- 14-ai-development/work-items/AID-2026-092/
git diff --stat  af2660d5  HEAD -- 14-ai-development/work-items/AID-2026-092/
git ls-tree -r af2660d5 -- .../AID-2026-092/
git ls-tree -r HEAD      -- .../AID-2026-092/
```

Exit code: 0. Output: **empty** for both diffs; both `ls-tree` listings are
blob-identical:

```
BASE 50e41dfa0c6f68ee1342fb7b107de286ff0b30b6  .../AID-2026-092/manifest.yaml
HEAD 50e41dfa0c6f68ee1342fb7b107de286ff0b30b6  .../AID-2026-092/manifest.yaml
BASE 7adf342a51f924cb732129ba3052ca65a832ea75  .../AID-2026-092/prompt-v1.md
HEAD 7adf342a51f924cb732129ba3052ca65a832ea75  .../AID-2026-092/prompt-v1.md
```

**CONFIRMED.** The branch does not touch `AID-2026-092/`. Its manifest at the head
is already the `27bfa597` repin, inherited from `origin/main`, not authored here.

---

## 13. Does the branch touch only declared paths?

```
git diff --name-only af2660d5...HEAD
git show --name-status --format="%H" c7d56bbe
```

Exit code: 0. Output:

```
A  14-ai-development/work-items/AID-2026-269/evidence.md
A  14-ai-development/work-items/AID-2026-269/exact-head-review-protocol-v1.md
A  14-ai-development/work-items/AID-2026-269/manifest.yaml
A  14-ai-development/work-items/AID-2026-269/prompt-v1.md
A  14-ai-development/work-items/AID-2026-269/review-case-1278.md
A  14-ai-development/work-items/AID-2026-269/session-evidence.md
M  14-ai-development/work-items/INDEX.md
```

7 paths. The AID-2026-269 manifest declares exactly these 7 at lines 116–128
(`manifest.yaml`, `prompt-v1.md`, `exact-head-review-protocol-v1.md`,
`review-case-1278.md`, `evidence.md`, `session-evidence.md`, `INDEX.md`).

**CONFIRMED.** No undeclared path is touched.

---

## 14. Independent numbers table

| quantity | review case | measured @ `987d2602` (case's SHA) | measured @ `c7d56bbe` (real head) |
|---|---|---|---|
| manifest declares `prompt_sha256` | `a459d7e5…` | `a459d7e5…` ✔ | **`9de08951…`** ✘ |
| manifest declares `prompt_bytes` | `3772` | `3772` ✔ | **`3714`** ✘ |
| manifest blob | `227c761d…` / `a91b25f1…` | `227c761d…` / `a91b25f1…` ✔ | **`50e41dfa…` / `11759f4c…`** ✘ |
| prompt bytes | 3714 | 3714 ✔ | 3714 ✔ |
| prompt sha256 | `9de08951…` | `9de08951…` ✔ | `9de08951…` ✔ |
| declared vs actual | MISMATCH | MISMATCH ✔ | **MATCH** ✘ |
| INDEX digest line | 65 | 65 ✔ | **67** ✘ |
| INDEX blob / lines | `3e652348…` / 308 | `3e652348…` / 308 ✔ | `79f065c6…` / 320 ✘ |
| distinct prompt versions | "four" (claim), five (measured) | five | five |
| 2455-byte version at either path | none | none ✔ | none ✔ |
| `9be8aebf…` in the whole ODB | not checked by the case | absent | absent |
| `44b57170` delta | −58, 2 keys removed | −58, 2 keys removed ✔ | same ✔ |
| both files introduced in `f61dc15a` | yes | yes ✔ | yes ✔ |
| `27bfa597` ancestor of candidate | no | no ✔ | **yes** ✘ |
| refs / commits scanned | 2454 / 9211 | — | 2654 / 9660 (→2668 / 9708) |

---

## V. Verdicts

These are two different questions and are answered separately.

### V.1 Accuracy of review case #1278 — **REQUEST CHANGES**

The case's *measurements* are reproducible and almost all correct. Its *binding*
is not, and two of its eight grades do not survive at the head it is supposed to
describe.

Blocking defects:

1. **Wrong candidate.** §1 and the JSON bind to `987d2602`, a main-branch merge
   commit (`Merge pull request #1365`) that is an ancestor of the head, contains
   none of the work item's files, and was created 32 minutes *after* the review
   window the same document claims. `git rev-parse HEAD` at this branch is
   `c7d56bbe`. Baseline and candidate are conflated into one SHA, which makes the
   reviewed diff empty by construction.
2. **F1 and F2 are contradicted.** At `c7d56bbe` the manifest declares
   `9de08951… / 3714`, exactly the committed prompt. Both E1s must become E0. The
   headline claim of the case ("the manifest declares a digest the prompt does not
   have") is false at the head.
3. **F3 line reference is wrong at the head.** The INDEX repeat is real, but at
   line 67 (`79f065c6`, 320 lines), not line 65 (`3e652348`, 308 lines).
4. **JSON `findings` (6) ≠ `declarations_checked` (8).** The two E0 declarations
   are counted in `verified` but never enumerated.
5. **`evidence.md` §E17 is stale.** Its recorded self-check (sizes 24995 / 16288,
   `checked 6 … findings 5`) describes a pre-adjudication revision and contradicts
   the committed 31175 / 23675 / 8 / 6.

Non-blocking notes:

- §4.3's manifest table has 4 commits; the current envelope has 5 (`e7f8a287`).
  Envelope drift, immaterial.
- §4.3's claim that `27bfa597` is not an ancestor of the candidate is true only
  for `987d2602`; it is an ancestor of `c7d56bbe` and is the commit that repaired
  the pin.
- Everything else checks out: the 3714 / `9de08951…` measurement, the −58 drift at
  `44b57170` with the two named keys, first introduction in `f61dc15a`, the five
  distinct versions, the total absence of 2455 / `9be8aebf…`, and all four
  session-evidence digests.

### V.2 The reviewed declaration (AID-2026-092 prompt pin) — **DOES NOT STAND**

At `c7d56bbe`:

- the manifest's own `prompt_sha256` / `prompt_bytes` pair is **correct**
  (`9de08951…` / 3714) — this part of the declaration now stands;
- `INDEX.md:67` still publishes `3772` / `a459d7e5…` for the same file — **E1
  stands**;
- `prompt_digest_correction` still asserts "exactly four (7689, 3772, 2915 and
  4137 bytes)" when five exist — **E4 stands**;
- no manifest field binds the pair to a specific blob — **E4 stands**;
- the registration value `9be8aebf… / 2455` has no existence anywhere in the
  object database — **E2 stands**.

The declaration is therefore still defective and `overall_result: FAIL` is still
correct, but the defect is now: a stale INDEX row, an incomplete count assertion,
a missing blob pin, and a fabricated historical pin. The manifest's live digest
mismatch that the case reports no longer exists.

---

## 15. Machine-readable result

```json
{
  "reviewer": "L3-2",
  "protocol": "Exact-Head Independent Review Protocol v1",
  "work_item": "AID-2026-269",
  "reviewed_case": "14-ai-development/work-items/AID-2026-269/review-case-1278.md",
  "candidate_sha": "c7d56bbee7a404c575c60f78055e366faed85f0a",
  "candidate_tree_sha": "94580c56c2827e5584d8cd59fcaaad22934cede2",
  "merge_base_with_origin_main": "af2660d55a93278157fa6668aba338daf81e127c",
  "case_declared_candidate_sha": "987d26021affbb5ba6d651e0fb5985d6bd4026a5",
  "case_candidate_is_ancestor_of_head": true,
  "case_candidate_contains_work_item": false,
  "case_candidate_created_after_claimed_review_window": true,
  "items_checked": 13,
  "items_failed": 5,
  "failed_items": [
    "1 candidate binding is not the branch head and did not exist during the claimed review window",
    "2 declared-value section quotes a superseded manifest blob; head declares 9de08951.../3714",
    "8 INDEX digest row is line 67 at the head, not line 65",
    "9 grades F1 and F2 contradicted at the head (manifest matches the prompt)",
    "10 findings array has 6 entries for declarations_checked 8"
  ],
  "items_passed": [
    "3 prompt blob 3714 bytes / 9de0895124032230b3418ff062ef2d590d27f37582d2847032a46b7116a53724",
    "4 history enumeration reproduced per path (prompt 2 commits, 083 prompt 4, manifest 5)",
    "5 2455-byte version and sha256 9be8aebf7d595f81cc062e5c03a67fd8317aeefaf69dd635fd9031f112dc25d1 absent from all 14104 ODB blobs",
    "6 44b57170 removes included_sections/included_assets, 0+/2-, delta -58",
    "7 manifest and prompt both introduced in f61dc15a7701702a57a7c0edcfc9d61591986bca",
    "11 all four session-evidence digests match the committed blobs",
    "12 no AID-2026-092 file modified by the branch",
    "13 branch touches exactly the 7 declared paths"
  ],
  "envelope": {
    "refs_first": 2654,
    "commits_all_first": 9660,
    "refs_last": 2668,
    "commits_all_last": 9708,
    "odb_blobs_hashed": 14104,
    "odb_objects_total": 63300
  },
  "measured_at_head": {
    "manifest_declared_prompt_sha256": "9de0895124032230b3418ff062ef2d590d27f37582d2847032a46b7116a53724",
    "manifest_declared_prompt_bytes": 3714,
    "prompt_actual_sha256": "9de0895124032230b3418ff062ef2d590d27f37582d2847032a46b7116a53724",
    "prompt_actual_bytes": 3714,
    "manifest_matches_prompt": true,
    "index_digest_line": 67,
    "index_declared_prompt_bytes": 3772,
    "index_declared_prompt_sha256": "a459d7e523fbba4ffb8c0f6ade8d3d8c1ec6ce45b95c3f48f65b192c0413edb3",
    "index_matches_prompt": false,
    "distinct_prompt_versions": [7689, 3772, 2915, 4137, 3714],
    "distinct_version_count": 5,
    "correction_claims_four": true,
    "value_2455_exists_anywhere": false,
    "sha256_9be8aebf_exists_anywhere": false
  },
  "regrade_at_head": {
    "F1_prompt_sha256": {"case": "E1", "measured": "E0", "agrees": false},
    "F2_prompt_bytes": {"case": "E1", "measured": "E0", "agrees": false},
    "F3_index_repeat": {"case": "E1", "measured": "E1", "agrees": true},
    "F4_four_versions": {"case": "E4", "measured": "E4", "agrees": true},
    "F5_no_blob_field": {"case": "E4", "measured": "E4", "agrees": true},
    "F6_2455_never_existed": {"case": "E0", "measured": "E0", "agrees": true},
    "F7_first_introduction_3772": {"case": "E0", "measured": "E0", "agrees": true},
    "F8_registration_pin": {"case": "E2", "measured": "E2", "agrees": true}
  },
  "recomputed_totals_at_head": {
    "declarations_checked": 8,
    "verified": 4,
    "failed": 2,
    "unverifiable": 2,
    "overall_result": "FAIL"
  },
  "case_verdict": "REQUEST_CHANGES",
  "reviewed_declaration_verdict": "DOES_NOT_STAND",
  "reviewed_declaration_note": "manifest pin is now correct at the head; INDEX:67 E1, count E4, missing blob pin E4 and registration-pin E2 remain, so overall FAIL still holds for narrower reasons",
  "findings": [
    {
      "id": "L3-2-01",
      "severity": "blocking",
      "item": 1,
      "statement": "candidate_sha 987d2602 is a main-branch merge commit (PR #1365), an ancestor of the head, containing none of the AID-2026-269 files, and created 2026-11-27T12:55+08:00 (04:55Z) which is 32 minutes after the claimed review end 04:22:51Z; the real head is c7d56bbe"
    },
    {
      "id": "L3-2-02",
      "severity": "blocking",
      "item": 9,
      "statement": "F1 and F2 graded E1 do not reproduce at the head: manifest.yaml:29-30 declare 9de0895124032230b3418ff062ef2d590d27f37582d2847032a46b7116a53724 and 3714, identical to the committed prompt"
    },
    {
      "id": "L3-2-03",
      "severity": "blocking",
      "item": 8,
      "statement": "the INDEX digest row is line 67 at the head (blob 79f065c6, 320 lines), not line 65 (blob 3e652348, 308 lines); the repeat itself is real"
    },
    {
      "id": "L3-2-04",
      "severity": "blocking",
      "item": 10,
      "statement": "JSON declarations_checked is 8 and the buckets sum to 8, but findings enumerates only 6; the two E0 declarations (F6, F7) appear in no finding object"
    },
    {
      "id": "L3-2-05",
      "severity": "blocking",
      "item": 11,
      "statement": "evidence.md E17 records a stale self-check (evidence 24995 / review-case 16288 / checked 6 / findings 5) that contradicts the committed artifacts (31175 / 23675 / 8 / 6)"
    },
    {
      "id": "L3-2-06",
      "severity": "note",
      "item": 4,
      "statement": "manifest path now has 5 commits including e7f8a287 (8232 B), absent from the case's table; envelope drift, immaterial"
    },
    {
      "id": "L3-2-07",
      "severity": "note",
      "item": 4,
      "statement": "27bfa597 is an ancestor of c7d56bbe, contrary to the case's statement; it is the commit that repinned the manifest to 3714/9de08951 and therefore the cause of the E1 evaporation"
    }
  ]
}
```
