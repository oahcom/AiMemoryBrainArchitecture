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
      last_verification_note: "Review case record; the verdict belongs to the reviewed declaration."
    usage_status: Active
    modification_status: Unchanged
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "First executed review case for AID-2026-269 (#1278 / AID-2026-092)"
    canonical_scope_id: "ai-development/aid-2026-269-review-case"
    canonical_scope_keywords:
      - "exact-head-review"
      - "review-case"
      - "declaration-mismatch"
      - "dual-head"
    canonical_conflict_status: None
    normative_status: Informative
---

# Review case #1278 — AID-2026-092 prompt digest

Protocol: Exact-Head Independent Review Protocol v1
Work item: AID-2026-269
Reviewer: L2-B (real case review)
Adjudicated by: Owner ruling 2026-11-27 (`reply-6b08fa9b-124545.md`, applied by L2-B2); dual-head restructure applied by L2-B4 under `reply-6b08fa9b-145049.md`
Issue under review: #1278 (`AID-2026-092` prompt digest)
Head bindings: Head A `987d2602` (historical defect), Head B `a7cf5256` (post-#1321), review submission head `c7d56bbe` (§1)

All numbers below were produced by the commands recorded in
[evidence.md](evidence.md). No value was copied from the issue text. Where the
issue's own numbers disagree with the measurement, the measurement is reported
and the disagreement is stated explicitly (see §2.7).

### Record revisions (2026-11-27)

Three corrections are applied to this record, each at the section it changes:

- **F4 enumeration** (§2.3.4, §6, §7.2, §7.7): the distinct-version count is
  restated per scope — 2 versions at the literal 092 path and 6 at the 092+083
  pair the manifest itself cites, measured at `c7d56bbe`; 3 and 7 across all refs
  at the independent re-measurement (8 if the 0-byte row is counted as a
  version). The earlier five-version statement came from a path listing without
  `--full-history` and from reading zero-length output as absence.
- **F9, new finding** (§6, §7.2, §7.7): the attribution sentence at
  `manifest.yaml:36-37` is true of the content and false of the declared path —
  `E3 ATTRIBUTION_MISMATCH`.
- **INDEX line numbers** (§2.5, §5, §6): every row locator is stated with the
  head it belongs to; a line number is a locator inside a named head, never a
  stable identity.

The independent re-measurement behind the first two was taken at `main`
`cb5b3dcd23ff86e10a354bb27b668dce19e95f62` — envelope 9871 commits / 2780 refs /
14845 blobs. The 2275-byte version it found is carried by `c6f2128d`, which is an
ancestor of `c7d56bbe`, so the corrected count is a property of this head as
well: the earlier five was a method error, not a difference of envelope.

The Owner supplied an English block for `## Dual-Head Review and Historical
Measurements`. The ruling's section list is authoritative, so that prose is
embedded under the headings it matches: its `### Head A` text in §2, `### Head B`
in §3, `## Review Submission Head` in §4, `### Interpretation and Evidence
Boundary` in §8. Its two bucket lists are stated once in §7.3 and its
remaining-findings list once in §6, so that no measurement appears twice.

---

## Review Scope and Head Binding

This record covers **three named heads** — a historical defect head, the
post-remediation merge head that follows it, and the head at which this case was
submitted — each identified by its own commit SHA. Each object carries its own
locked SHA, tree SHA, review/measurement time and INDEX row, and is reported under
that SHA, never under a branch name.

**Measurements from different heads are never mixed.** A number quoted below is
valid only at the commit it is bound to; no grade, line number or bucket count may
be carried from one head to another, and the historical counts are never presented
as the counts of any later head.

**Operative rule — named heads only.** A new head is a new observation appended to
this record, not a revision of the existing ones. No head's findings, line numbers,
bucket counts or verdict may be overwritten by a later head. PR heads, `main` and
branch names are locators, never substitutes for a commit identity: a statement is
true of a commit SHA, and of a branch only through the SHA that branch pointed to at
a recorded time.

| role | commit (locked) | tree SHA | review / measurement time (UTC) | INDEX row |
|---|---|---|---|---|
| `historical_defect` — Head A | `987d26021affbb5ba6d651e0fb5985d6bd4026a5` | `2a73559ebf1406ef3892c4c71dce33c20731e446` | 2026-11-27T04:09:16Z – 04:22:51Z (recorded review window) | 65 |
| `post_remediation` — Head B | `a7cf5256e975ff25fd2f75b3b5051b16d8d77d36` | `a9b018e7449f4be2e375d082235e2d892c5a40b1` | 2026-11-27T06:55:36Z (post-#1321 re-measurement) | 67 |
| `review_submission` — submission head | `c7d56bbee7a404c575c60f78055e366faed85f0a` | `94580c56c2827e5584d8cd59fcaaad22934cede2` | 2026-11-27T06:55:36Z (same re-measurement run) | 67 |

Head A is the object of the original #1278 review. Head B is `origin/main` after
PR #1321 merged; it is a post-remediation measurement, not a second defect. The
review submission head is the head of branch
`review/2026-11-27-aid269-exact-head-review` at the moment this case was submitted:
`c7d56bbe`, one commit beyond the merge base
`af2660d55a93278157fa6668aba338daf81e127c`; at that SHA its manifest is
byte-identical to Head B's (§4). A later push to the same branch does not revise
this entry — it creates a new one, appended under its own SHA.

Binding environment:

| Field | Value |
|---|---|
| repository | `oahcom/AiMemoryBrainArchitecture` |
| worktree | `D:\code\wt-aid268` (linked worktree; common git dir `D:/code/AiMemoryBrainArchitecture/.git`) |
| branch | `review/2026-11-27-aid269-exact-head-review` |
| Git | `git version 2.56.1.windows.1` |
| Python | `Python 3.12.3` |
| `origin/main` at Head A first lock (2026-11-27T04:09:16Z) | `10d33b3f6c012e1c0d5649a5279cadb6d27b1a2f` |
| `origin/main` at Head A second lock (2026-11-27T04:22:34Z) | `386d8f57b02d8e3c511ff0e3980b9ce0af8b3028` |
| history envelope at end of the Head A review | 2454 refs, 9211 commits reachable from `--all` |
| history envelope at the review submission head (`c7d56bbe`) re-measurement | 2708 refs, 9753 commits reachable from `--all` |

The three head bindings were re-read with `git rev-parse "<sha>^{tree}"`,
`git ls-tree <sha> -- <path>` and `git show <sha>:<path>`; the re-measurement at
2026-11-27T06:55:36Z, bound to `c7d56bbe`, re-ran the path enumeration and the
2455-byte object scan at the wider envelope (2708 refs / 9753 commits) and
reproduced every per-path table unchanged, so the widened envelope alters no
conclusion.

## Head A — Historical Defect at 987d2602

At candidate head `987d2602`, the AID-2026-092 manifest declared
`prompt_sha256: a459d7e523fbba4ffb8c0f6ade8d3d8c1ec6ce45b95c3f48f65b192c0413edb3`
and `prompt_bytes: 3772` (`manifest.yaml:29` and `:30`; the manifest blob identity
at this head is in §2.1). The
historical review found that these declarations did not match the prompt bytes
measured for that reviewed state. **F1 (`prompt_sha256`) and F2 (`prompt_bytes`)
are therefore graded E1 — DECLARATION_MISMATCH for this historical head.**

The per-declaration grades for this head are §7.1; its bucket counts and
`overall_result` are §7.3. They apply only to the review bound to `987d2602`.

### 2.1 Declared values at this head

Source: `14-ai-development/work-items/AID-2026-092/manifest.yaml` at the
candidate SHA (blob `227c761d82984fb671ab3fa53f57b41c10bdd04c`, 7680 bytes,
sha256 `a91b25f165766b7d7ee15f1a25269f98a4564dceeb4e6acf4e5db6b405a1f5ca`).

| # | file:line | field | declared value |
|---|---|---|---|
| D1 | `AID-2026-092/manifest.yaml:27` | `prompt_file` | `14-ai-development/work-items/AID-2026-092/prompt-v1.md` |
| D2 | `AID-2026-092/manifest.yaml:29` | `prompt_sha256` | `a459d7e523fbba4ffb8c0f6ade8d3d8c1ec6ce45b95c3f48f65b192c0413edb3` |
| D3 | `AID-2026-092/manifest.yaml:30` | `prompt_bytes` | `3772` |
| D4 | `AID-2026-092/manifest.yaml:31-41` | `prompt_digest_correction` (historical claim) | registration value was `9be8aebf7d595f81cc062e5c03a67fd8317aeefaf69dd635fd9031f112dc25d1` at 2455 bytes; "matched no version … at any commit reachable from any ref"; enumeration "exactly four (7689, 3772, 2915 and 4137 bytes)" |
| D5 | `AID-2026-092/manifest.yaml:25` | `prompt_id` | `AID-2026-083-PROMPT` (explained by `RENUMBERED_FROM: AID-2026-083`, line 2) |
| D6 | `work-items/INDEX.md:65` | INDEX repeat of D2/D3 | `3772 bytes, SHA-256 a459d7e5…`, plus the same `9be8aebf…` / 2455 historical claim |

No `prompt_file_blob_sha` key exists in the manifest; `git ls-tree` gives the
blob identity directly (§2.2).

### 2.2 Recomputation from the committed blob

The prompt file was read as a Git object, never from the working tree, and hashed
as bytes (`sys.stdin.buffer.read()`), with no text decode.

| field | value |
|---|---|
| declared path | `14-ai-development/work-items/AID-2026-092/prompt-v1.md` |
| `git rev-parse HEAD:<path>` | `7adf342a51f924cb732129ba3052ca65a832ea75` |
| `git cat-file -s 7adf…` | `3714` |
| recomputed sha256 (stdin pipe) | `9de0895124032230b3418ff062ef2d590d27f37582d2847032a46b7116a53724` |
| recomputed sha256 (redirected file, second method) | `9de0895124032230b3418ff062ef2d590d27f37582d2847032a46b7116a53724` |
| byte count (second method) | `3714` |
| line count / endings | 67 LF, 0 CRLF, no BOM (`b'---'` head) |
| working tree copy | 3714 bytes, `9de08951…` (identical to blob; `core.autocrlf=false`) |

Declared vs actual:

| field | declared | actual | result |
|---|---|---|---|
| `prompt_sha256` | `a459d7e523fbba4ffb8c0f6ade8d3d8c1ec6ce45b95c3f48f65b192c0413edb3` | `9de0895124032230b3418ff062ef2d590d27f37582d2847032a46b7116a53724` | MISMATCH |
| `prompt_bytes` | `3772` | `3714` | MISMATCH (−58) |
| `prompt_file` | path above | path exists, resolves to blob `7adf342a51f924cb732129ba3052ca65a832ea75` | MATCH |

The declared pair `a459d7e5… / 3772` is not fabricated: it is the *previous*
revision of the same file, still reachable at `f61dc15a…` (§2.3). The declaration
was correct when written and became stale at `44b57170…`, which edited the prompt
without updating the manifest.

### 2.3 History table

Search envelope: every ref present after `git fetch origin --prune` at
2026-11-27T04:22:34Z — 2454 refs, 9211 commits reachable from `git rev-list
--all`. Unreachable/dangling objects are outside the envelope. Paths were
enumerated separately; `git show <commit>:<path>` was read as binary and hashed
as bytes. Re-run at the review-submission-head envelope (`c7d56bbe`; 2708 refs /
9753 commits) reproduced the same two-commit listing for the 092 path. The 083
path listing is **not** identical once `--full-history` is used: the default
listing drops the commits that carry the path across the 083→090 renumber and one
2275-byte version. That is the method error corrected in §2.3.4, and it changes no
grade.

#### 2.3.1 `14-ai-development/work-items/AID-2026-092/prompt-v1.md` (2 commits)

| commit_sha | byte_count | sha256 |
|---|---|---|
| `f61dc15a7701702a57a7c0edcfc9d61591986bca` | 3772 | `a459d7e523fbba4ffb8c0f6ade8d3d8c1ec6ce45b95c3f48f65b192c0413edb3` |
| `44b57170b86c7f3e56744da756ed24744b1c659c` | 3714 | `9de0895124032230b3418ff062ef2d590d27f37582d2847032a46b7116a53724` |

#### 2.3.2 `14-ai-development/work-items/AID-2026-083/prompt-v1.md` (4 commits under default history simplification)

| commit_sha | byte_count | sha256 |
|---|---|---|
| `e5068b65c5f06857c4d21ba66b171b5e222f7cfc` | 4137 | `7ce260dfb8f1a959bce48ac3abcbfa2d53bbd0c984663013136fbcd3152b67ec` |
| `ecbb9bc743586edb3a116049c51ede9ddb324492` | 2915 | `9614ddf7013eaaa6f740842163f5f2f53d9475103d602fc0858bc62b3608166f` |
| `45045ed319caa7049deacfc98de75f698db7a3d0` | — (file deleted by this commit, `D`) | — |
| `44c530a02e1c7f34f742f619449f13efd60ed4e0` | 7689 | `0c0ce002db720c6a46186a94a591bc13939768627910b447960cbbd4f5cfe640` |

This table is the default-simplification listing and is kept as recorded. The
full-history enumeration adds the commits that carry the path across the 083→090
renumber and one further version, **2275 B / `f7c1aacc…`**; both scopes and the
0-byte row are in §2.3.4.

#### 2.3.3 `14-ai-development/work-items/AID-2026-092/manifest.yaml` (4 commits)

| commit_sha | byte_count | sha256 |
|---|---|---|
| `f61dc15a7701702a57a7c0edcfc9d61591986bca` | 6677 | `64af89558212bce7b85e39b9af4c5bbea35429807f56b5cc66fee2fca8aaf326` |
| `3619502712b422f1149c5c37ab6e97679f8130ce` | 6691 | `daec20c56161a691667f2d4ba453eef45fac1b784159971615c4e5dcd5b00c48` |
| `e0d6a9920cee5fe0629af7daef2656d0bfb26acd` | 7680 | `a91b25f165766b7d7ee15f1a25269f98a4564dceeb4e6acf4e5db6b405a1f5ca` |
| `27bfa597764281b3abdbe939843b45c14f25b388` | 7680 | `11759f4c586af7654fb0c96d3d8b1783e59a293cc3a1dc7f0ea6eae70722c6c6` |

`27bfa597…` is reachable from `pr1321` / `pr1336` / `origin/gov/aid-116-pin-and-attribution`
but is **not** an ancestor of the candidate; it is included because the envelope
is "all refs", not "ancestors of HEAD".

#### 2.3.4 Distinct prompt versions, by scope

The correction at `manifest.yaml:31-41` counts versions inside the scope its own
text declares: line 34 reads "enumerating every distinct blob at this path and at
`AID-2026-083/prompt-v1.md`". Enumerated per path with `git rev-list --all
--full-history -- <path>`, then per commit `git rev-parse <commit>:<path>` +
`git cat-file blob` + SHA-256 of the raw bytes, absent paths skipped — 26 commits
touch the two paths, 0 missing at the independent re-measurement.

| scope | at `c7d56bbe` | across all refs (independent re-measurement) |
|---|---|---|
| literal 092 path only | **2**: 3772 `a459d7e5…`, 3714 `9de08951…` | **3**: those two plus 3751 `7d8dbc1c…`, reachable only from `c7db0ef0`, which is not an ancestor of `c7d56bbe` |
| 092 + 083 — the pair line 34 cites | **6**: adds 2275 `f7c1aacc…`, 2915 `9614ddf7…`, 4137 `7ce260df…`, 7689 `0c0ce002…` | **7**: the six plus 3751 `7d8dbc1c…` |

**The 0-byte row.** The full-history enumeration also yields a 0-byte row
(`e3b0c442…`) on three commits of the 083 path. It is not a committed empty
prompt: those are the three commits where the 083 path is absent — the deletion
`45045ed3`, the 083→090 renumber `c6f2128d` and `143d093f` — and a zero-length
read of an absent path hashes to the empty-string digest. They are recorded here
as absence, not as a version; counted as a version, the 092+083 scope would read
8. Either reading makes the assertion's number wrong, and the count used below is
the non-empty one (7).

The version the earlier statement missed is **2275 B / `f7c1aacc…`**, at the 083
path from commit `c6f2128d` (2026-11-26 14:48) — the commit that renumbers the 083
directory to `AID-2026-090`, and the last commit whose parent tree still carries
2275 bytes at the 083 path. No commit at either declared path has 2455 bytes.

**"Exactly four" is false in both scopes, at both envelopes.** At the literal 092
path there are two versions at `c7d56bbe` and three across all refs, so four
overstates. At the 092+083 pair the manifest itself cites there are six at
`c7d56bbe` and seven across all refs — eight if the 0-byte row is counted — so
four understates and omits 2275, 3714 and 3751. No reading of the sentence
produces four: the enumerated four (7689, 3772, 2915, 4137) is a proper subset of
the six, and the sizes it leaves out are the ones that make the assertion
testable — 2275, the version the enumeration missed; 3714, the version the pin was
later corrected to; and 3751 on a side branch. The grade remains E4 (the count is
incomplete) and the bucket membership is unchanged.

### 2.4 First introduction and historical existence

Method: for each path, `git rev-list --all -- <path>` (default history
simplification), then the oldest entry is confirmed with
`git diff-tree -r --name-status <parent> <commit> -- <path>`.

| path | first introduction commit | evidence |
|---|---|---|
| `AID-2026-092/prompt-v1.md` | `f61dc15a7701702a57a7c0edcfc9d61591986bca` (2026-11-26 15:04:18 +0800, "docs(work-items): reallocate acceptance evidence as AID-2026-092 after main collision") | diff vs first parent `1e7f4d0a7baf06103dc3bd504293e25e53bd24c2` = `A` |
| `AID-2026-092/manifest.yaml` | `f61dc15a7701702a57a7c0edcfc9d61591986bca` (same commit) | diff vs first parent = `A` |
| pre-rename `AID-2026-083/manifest.yaml` that carried the original declaration | `cac933cb9eb3e51b725dfaca0af47d5c05f8ad80` (2026-11-26 14:37:01 +0800, "docs: add delegated evidence package for #1189 #1197 #1037", parent `515b7144320fd9fcc1e1a2c3d2d2744d979b4ca8` = the manifest's `base_commit_sha`) | manifest there declares `9be8aebf…` / 2455 at lines 25-26 |

Manifest and prompt both first appear at `f61dc15a…`, in the same commit.

At that commit the prompt file was already **3772 bytes / `a459d7e5…`**, and the
manifest declared **2455 bytes / `9be8aebf…`**. At the earlier commit that
created the declaration, `cac933cb…`, the pinned file
(`AID-2026-083/prompt-v1.md`, blob `ecdb9285c2c2c9975de35a002a7efbc47915346d`)
was likewise already 3772 bytes / `a459d7e5…`.

That 3772-byte content sits at the **083** path at `cac933cb…`. The path the
manifest actually pins is the **092** path (`prompt_file`, `manifest.yaml:27`),
and at `cac933cb…` that path does not exist: `git cat-file -e
cac933cb9eb3e51b725dfaca0af47d5c05f8ad80:14-ai-development/work-items/AID-2026-092/prompt-v1.md`
exits 128. The correction's attribution sentence (`manifest.yaml:36-37`, "the
file it pins is already 3772 bytes") is therefore true of the content and false
of the declared path; it is graded as F9 (§6).

**Did the declared 2455-byte / `9be8aebf…` version ever exist at any reachable
commit? No.** Zero of the 9211 reachable commits contain a blob of 2455 bytes or
of sha256 `9be8aebf7d595f81cc062e5c03a67fd8317aeefaf69dd635fd9031f112dc25d1` at
either prompt path; the sha256 target search returned 0 hits, and 2455 is absent
from the seven non-empty distinct sizes of the manifest's declared scope (§2.3.4). At the review-submission-head envelope (`c7d56bbe`;
2708 refs / 9753 commits) the scan returns one 2455-byte blob in the whole object
store —
`72993b655aa5e72edab78055415fbacf43fc66a3`, sha256
`9f21343969ef0299ff43490de777ae3fa4c596139f0426492a37fd7f294d409f`, the
unrelated file `14-ai-development/work-items/AID-2026-082/session-evidence.md` —
and 0 hits for the declared digest. This confirms E2 for the registration
declaration.

### 2.5 INDEX cross-check at line 65 of `987d2602`

`14-ai-development/work-items/INDEX.md` at the candidate (blob
`3e652348dc7df5286d4ba0408091a1f052968c07`, 308 lines) repeats the same pair.
Line 65 **at `987d2602`**, digest-relevant segment:

> `AID-2026-083-PROMPT` v1 — `14-ai-development/work-items/AID-2026-092/prompt-v1.md`, 3772 bytes, SHA-256 `a459d7e523fbba4ffb8c0f6ade8d3d8c1ec6ce45b95c3f48f65b192c0413edb3`. The digest recorded at registration was `9be8aebf…` at 2455 bytes, which matched no version of the file at any ref — not the AID-2026-047 shape, where the stale value described a real earlier revision; corrected by AID-2026-102, `prompt_status: RECORDED_NOT_FROZEN`.

The INDEX row is byte-consistent with the manifest (same wrong pair) and therefore
propagates the same E1. Only line 65 of this head carries the digest; line 146
(the AID-2026-102 correction row) carries no `AID-2026-092` digest. Line 146's
clause "`AID-2026-092`'s `prompt_sha256` and `prompt_bytes` now equal the
committed bytes" is false at the candidate; it is recorded here as a note and is
not graded, because it is a superseded correction record rather than a live pin.

Line numbers are locators inside a named head, never a stable identity: the same
row is line 65 at `987d2602`, line 67 at `c7d56bbe`, line 71 at `f155122c` and
line 72 at `cb5b3dcd` (§5).

### 2.6 Drift log (shared git dir)

| observation | time (UTC) | origin/main | refs | commits (`rev-list --count --all`) |
|---|---|---|---|---|
| first lock, after fetch | 04:09:16Z | `10d33b3f6c012e1c0d5649a5279cadb6d27b1a2f` | 2452 | 9204 |
| second lock, after re-fetch | 04:22:34Z | `386d8f57b02d8e3c511ff0e3980b9ce0af8b3028` | 2454 | 9211 |
| review-submission-head re-measurement | 06:55:36Z | — | 2708 | 9753 |

Candidate `987d2602…` unchanged throughout. The history enumeration was re-run at
the wider envelope (2454 refs / 9211 commits) and produced identical per-path
tables under the same enumeration method; the method itself was the limitation
corrected in §2.3.4, so the widening changed no conclusion while the version count
does change. No E5 is assigned
to the candidate; the drift is in `origin/main` and the ref set, caused by other
sessions sharing `D:/code/AiMemoryBrainArchitecture/.git`.

### 2.7 Relationship to the numbers stated in issue #1278

The issue states declared `2455` / `9be8aebf…` and actual `3772` /
`a459d7e5…`. My measurement **contradicts the "actual" pair**: at candidate
`987d26021affbb5ba6d651e0fb5985d6bd4026a5` the committed prompt is **3714 bytes /
`9de0895124032230b3418ff062ef2d590d27f37582d2847032a46b7116a53724`** (§2.2).

Reason: the issue's "actual" pair was correct at `e0d6a9920cee5fe0629af7daef2656d0bfb26acd`
(the AID-2026-102 correction, merged 2026-11-26T09:36:13Z) but the prompt was
edited afterwards by `44b57170b86c7f3e56744da756ed24744b1c659c`
(2026-11-26 18:06:14 +0800), which removed two YAML keys
(`included_sections: []`, `included_assets: []`, −2 lines / −58 bytes) from the
prompt's frontmatter and did not update the manifest or INDEX. So:

- the original defect (E1 + E2) is confirmed;
- the correction is itself stale (new E1), with a *different* actual pair than the
  issue reports;
- a sibling branch already carries the correct pin: `27bfa597…` declares
  `3714` / `9de08951…`, matching my measurement.

## Head B — Post-#1321 State at a7cf5256

PR #1321, titled “repin 33 prompt digests”, corrected the AID-2026-092 manifest
declaration. At merge head `a7cf5256` (tree `a9b018e7…`) the manifest blob is
`50e41dfa0c6f68ee1342fb7b107de286ff0b30b6` and it declares
`prompt_sha256: 9de0895124032230b3418ff062ef2d590d27f37582d2847032a46b7116a53724`
and `prompt_bytes: 3714` (lines 29 and 30). The prompt blob is unchanged from
Head A — `7adf342a…`, whose 3714-byte / `9de08951…` identity was measured in §2.2 —
so the declaration and the committed prompt agree. **F1 and F2 are graded E0 —
VERIFIED at this head.**

This is a post-remediation measurement, not evidence that the historical mismatch
at `987d2602` never existed.

The INDEX row at this head is line 67 at `a7cf5256`, and its cell text is
byte-identical to the row read at Head A (line 65 at `987d2602`). That residual
finding is graded in §6; the per-declaration grades for this head are §7.1 and its
bucket counts §7.3.

## Review Submission Head — c7d56bbe

This section is an observation bound to commit
`c7d56bbee7a404c575c60f78055e366faed85f0a`, tree
`94580c56c2827e5584d8cd59fcaaad22934cede2`: **the head at which this case was
submitted**, not the current state of the branch. A later push produces a new head
and therefore a new observation appended to this record; it does not rewrite what
was measured here.

At `c7d56bbe` the branch carries one commit beyond the merge base
`af2660d55a93278157fa6668aba338daf81e127c`.

At `c7d56bbe` the manifest is identical to Head B's: same blob `50e41dfa…`,
therefore the same declared pair at the same lines (§3). **F1 and F2 are E0 —
VERIFIED at `c7d56bbe`.** The INDEX row at this head is line 67 at `c7d56bbe`.

The findings open at `c7d56bbe` are listed once in §6. This head's
per-declaration grades are §7.2, its bucket counts and `overall_result` §7.3.

## Head D — Post-#1452 Remediation at 5e30d497

This section is an observation bound to commit
`5e30d49776a2ce75069227a41470fa7e4ae00b2e`, tree
`808f30b1b1c0ebe2624467a7768834d6c482c80d`: merge of PR #1452
(`fix/2026-11-27-aid116-index-cells`), merged 2026-11-27T07:55:28Z. It is a
**fourth named entry**, appended after the submission head because #1452 landed
after that head was measured; it does not revise §3, §4 or their counts.

At `5e30d497` the manifest blob is `987f1efe409709165af80940e3a56062ced49a75`,
declaring `prompt_sha256: 9de08951…` and `prompt_bytes: 3714` at lines 29 and 30 —
the same pair as Head B and the submission head. The prompt blob is unchanged,
`7adf342a…`, 3714 bytes / `9de08951…` (§2.2).

The `AID-2026-092` INDEX row is **line 72 at `5e30d497`**, and its cell now reads
`3714 bytes, SHA-256 9de08951…`, with the registration clause restated at 3714
bytes. The row therefore matches the manifest and the committed prompt: **F3 moves
from E1 to E0 — VERIFIED at this head.** F1 and F2 remain E0 (§3).

F4 and F5 are unchanged (the correction block at lines 31-41 and the absence of a
blob-pin field are the same text), F6, F7 and F8 are unchanged (they are
historical assertions bounded by their own envelopes), and F9 is unchanged: the
attribution sentence at lines 36-37 is still present in this head's manifest blob,
so the declared path still does not exist at `cac933cb` and the E3 stands.

**Head D is the last head this record covers.** Any later head is a fifth named
entry, appended with its own commit SHA, tables and bucket counts; it is never
substituted for Head D or for any earlier head.

## Historical Measurements and Head-Specific Differences

| session | locked candidate | tree SHA | INDEX row for the AID-2026-092 digest |
|---|---|---|---|
| L2-B (this record, Head A) | `987d26021affbb5ba6d651e0fb5985d6bd4026a5` | `2a73559ebf1406ef3892c4c71dce33c20731e446` | 65 |
| L3-1 (independent review) | `10d33b3f6c012e1c0d5649a5279cadb6d27b1a2f`, re-read at `386d8f57b02d8e3c511ff0e3980b9ce0af8b3028` | `4b5c1a06ce1a08682cc892beb4f83e96a854377e` / `8d3caf7f30c8687e0da1bb4bd2d9268eb8182350` | 66 |
| L2-C / review submission head (and Head B) | `c7d56bbee7a404c575c60f78055e366faed85f0a` / `a7cf5256e975ff25fd2f75b3b5051b16d8d77d36` | `94580c56c2827e5584d8cd59fcaaad22934cede2` / `a9b018e7449f4be2e375d082235e2d892c5a40b1` | 67 |
| Head D (post-#1452 remediation) | `5e30d49776a2ce75069227a41470fa7e4ae00b2e` | `808f30b1b1c0ebe2624467a7768834d6c482c80d` | 72 |

All three rows quote the **same** AID-2026-092 digest cell text — compared byte
for byte, the cell is identical at `987d2602`, `10d33b3f`, `a7cf5256` and
`c7d56bbe`. Only the line number differs, because the rows above it differ between
the heads (line 65 at `987d2602`, 66 at `10d33b3f`, 67 at `a7cf5256` and
`c7d56bbe`). The 65 / 66 / 67 difference is therefore **head-specific, not
contradictory**: none of the three readings is wrong at its own commit, and none
may be transplanted to another head.

Two later heads were measured for the same row: **line 71 at `f155122c`** and
**line 72 at `cb5b3dcd`**, both still carrying the stale cell. At **line 72 at
`5e30d497`** the line number is the same as at `cb5b3dcd` while the cell text
changed (3714 bytes / `9de08951…`) — the clearest illustration that a line number
is not an identity. The rule is stated once and binds every locator in this
record: a line number is a locator inside a named head, never a stable identity.
The row is cited as "line N at `<commit>`" or not at all; a bare "INDEX line 67"
is not a fact about the INDEX file, it is a fact about `c7d56bbe`.

The same rule governs the manifest and prompt blobs: `227c761d…` at Head A and
`50e41dfa…` at Head B and at `c7d56bbe` are two different manifest blobs, so a
declared pair read at one head says nothing about the other.

## Remaining Findings, by Head

The graded set is nine declarations. Only their grades move, and every move is
bound to the head where it was measured — no head's cell is carried into another
head's row.

| # | checked item | A `987d2602` | B `a7cf5256` | submission `c7d56bbe` | D `5e30d497` |
|---|---|---|---|---|---|
| F1 | `prompt_sha256` (`manifest.yaml:29`) | E1 | E0 | E0 | E0 |
| F2 | `prompt_bytes` (`manifest.yaml:30`) | E1 | E0 | E0 | E0 |
| F3 | INDEX row (line 65 / 67 / 67 / 72, one per head) | E1 | E1 | E1 | **E0** |
| F4 | "exactly four blob versions" (`manifest.yaml:35`) | E4 | E4 | E4 | E4 |
| F5 | no fixed blob field, only the SHA-256 + bytes pair | E4 | E4 | E4 | E4 |
| F6 | "2455 / `9be8aebf…` never existed" | E0 | E0 | E0 | E0 |
| F7 | "3772 / `a459d7e5…` at first introduction" | E0 | E0 | E0 | E0 |
| F8 | registration value `9be8aebf…` / 2455 | E2 | E2 | E2 | E2 |
| F9 | attribution of the 3772-byte pair to `cac933cb` (`manifest.yaml:36-37`) | — | — | E3 | E3 |

The Head A column is the adjudicated set (§7.1), reproduced and not re-graded. F9
is added to the graded set at `c7d56bbe` and carried forward to Head D; the Head A
and Head B entries are closed at their own eight rows and are not extended
retroactively. The sentence F9 grades is present in all four manifest blobs, so
the dash in those two columns is a record boundary, not a finding of accuracy.

Open at `c7d56bbe` — five findings, nothing else in the set:

| # | result | grade | evidence at `c7d56bbe` |
|---|---|---|---|
| F3 | FAIL | **E1 DECLARATION_MISMATCH** | the row still declares the pre-#1321 pair (cell text identical to Head A's, §2.5), while the committed prompt hashes to the §2.2 pair; the locator is head-scoped — line 65 at `987d2602`, line 71 at `f155122c`, line 72 at `cb5b3dcd` (§5) |
| F4 | INCOMPLETE | **E4 INCOMPLETE_EVIDENCE** | 7 non-empty versions in the pair line 34 cites (8 if the 0-byte row counts) and 3 at the literal 092 path across all refs; 6 and 2 at this head's envelope. Four is wrong in both scopes (§2.3.4) |
| F5 | INCOMPLETE | **E4 INCOMPLETE_EVIDENCE** | no `*_blob_sha` key at this head; the identity is available only via `git ls-tree` (`7adf342a…`) |
| F8 | FAIL | **E2 HISTORICAL_NONEXISTENCE** | 0 hits for the digest at either path; the only 2455-byte blob in the object store is `72993b65…` = `AID-2026-082/session-evidence.md` (§2.4) |
| F9 | FAIL | **E3 ATTRIBUTION_MISMATCH** | at `cac933cb` the declared path `AID-2026-092/prompt-v1.md` does not exist — `git cat-file` exits 128; the 3772-byte blob is at the 083 path (§2.4) |

Open at Head D `5e30d497` — four findings: F4 and F5 at E4, F8 at E2, F9 at E3.
F3 is closed there: the row at line 72 reads `3714 bytes, SHA-256 9de08951…` and
matches the manifest and the prompt.

F1 and F2 are on no open list after Head A: #1321 corrected them (§3), and the case
does not re-count that historical fix as a defect at `c7d56bbe` or at Head D (§8).

## Results and Bucket Counts by Head

### 7.1 Head A (`987d2602`) — adjudicated grade table

Source: Owner ruling 2026-11-27, §1 (`reply-6b08fa9b-124545.md`). This table is
the single final grade set for the historical head and governs the Head A record.

| # | checked declaration | result | final grade | basis |
|---|---|---|---|---|
| F1 | manifest `prompt_sha256` declaration (`AID-2026-092/manifest.yaml:29`) | FAIL | **E1 DECLARATION_MISMATCH** | declared value ≠ actual SHA-256 at the candidate head |
| F2 | manifest `prompt_bytes` declaration (`AID-2026-092/manifest.yaml:30`) | FAIL | **E1 DECLARATION_MISMATCH** | declares 3772 bytes, measured 3714 |
| F3 | INDEX same-row repeat (`INDEX.md:65`) | FAIL | **E1 DECLARATION_MISMATCH** | the INDEX declaration does not match the reviewed content |
| F4 | "exactly four blob versions" (`manifest.yaml:31-41`) | INCOMPLETE | **E4 INCOMPLETE_EVIDENCE** | the ruling recorded five versions; the count is corrected to seven non-empty versions in §2.3.4, and the two reviewers locked different candidate SHAs, which is not sufficient to call a single-review E5 drift. Grade and bucket unchanged |
| F5 | no fixed blob field, only the SHA-256 + bytes pair | INCOMPLETE | **E4 INCOMPLETE_EVIDENCE** | no field binds the declaration to a specific blob; evidence structure incomplete |
| F6 | the correction claim "2455 bytes / `9be8aebf…` never existed" | PASS | **E0 VERIFIED** | not found in the stated refs/commits/reachable-blob scope; the only 2455-byte object belongs to an unrelated file |
| F7 | "3772 bytes / `a459d7e5…` at first introduction" | PASS | **E0 VERIFIED** | manifest and prompt both first introduced with that byte count and digest |
| F8 | original manifest pin on `9be8aebf…` / 2455 (registration value) | FAIL | **E2 HISTORICAL_NONEXISTENCE** | ruled separately from F6: the pin asserts a value that has no historical existence |

`result` is the per-declaration outcome (`PASS` / `FAIL` / `INCOMPLETE` /
`UNVERIFIABLE`) and `grade` is the protocol severity code (`E0`–`E6`); the two are
not interchangeable — F1, F2, F3 and F8 all read `FAIL` while carrying two
different grades (E1 ×3, E2 ×1), and F4 and F5 read `INCOMPLETE` at E4.

Row-to-row mapping to the pre-adjudication IDs: F1 = D2, F2 = D3, F3 = D6,
F4 = D4b, F5 = new (no pre-adjudication row), F6 = D4a, F7 = the
"3772 / `a459d7e5…` at first introduction" finding, F8 = H1. `prompt_file` (D1)
and `prompt_id` (D5) were not part of the adjudicated table and are not graded
here; their pre-adjudication grades (E0, E0) appear only in §7.4.

### 7.2 Review submission head (`c7d56bbe`) — final grades

The same nine declarations, re-graded at `c7d56bbe`. The only movement from Head A
is the #1321 correction; F9 enters the set at this head.

| # | checked declaration | grade at `c7d56bbe` | movement from Head A |
|---|---|---|---|
| F1 | `prompt_sha256` (`manifest.yaml:29`) | **E0 VERIFIED** | E1 → E0, fixed by #1321 (§3) |
| F2 | `prompt_bytes` (`manifest.yaml:30`) | **E0 VERIFIED** | E1 → E0, fixed by #1321 (§3) |
| F3 | INDEX row (line 67 at `c7d56bbe`) | **E1 DECLARATION_MISMATCH** | unchanged |
| F4 | "exactly four blob versions" (`manifest.yaml:35`) | **E4 INCOMPLETE_EVIDENCE** | unchanged |
| F5 | no fixed blob field | **E4 INCOMPLETE_EVIDENCE** | unchanged |
| F6 | "2455 / `9be8aebf…` never existed" | **E0 VERIFIED** | unchanged |
| F7 | "3772 / `a459d7e5…` at first introduction" | **E0 VERIFIED** | unchanged |
| F8 | registration value `9be8aebf…` / 2455 | **E2 HISTORICAL_NONEXISTENCE** | unchanged |
| F9 | attribution of the 3772-byte pair to `cac933cb` (`manifest.yaml:36-37`) | **E3 ATTRIBUTION_MISMATCH** | new declaration, not in the Head A set |

### 7.2.1 Head D (`5e30d497`) — final grades

| # | checked declaration | grade at `5e30d497` | movement from `c7d56bbe` |
|---|---|---|---|
| F1 | `prompt_sha256` | **E0 VERIFIED** | unchanged |
| F2 | `prompt_bytes` | **E0 VERIFIED** | unchanged |
| F3 | INDEX row (line 72 at `5e30d497`) | **E0 VERIFIED** | E1 → E0, fixed by #1452 |
| F4 | "exactly four blob versions" | **E4 INCOMPLETE_EVIDENCE** | unchanged |
| F5 | no fixed blob field | **E4 INCOMPLETE_EVIDENCE** | unchanged |
| F6 | "2455 / `9be8aebf…` never existed" | **E0 VERIFIED** | unchanged |
| F7 | "3772 / `a459d7e5…` at first introduction" | **E0 VERIFIED** | unchanged |
| F8 | registration value `9be8aebf…` / 2455 | **E2 HISTORICAL_NONEXISTENCE** | unchanged |
| F9 | attribution of the 3772-byte pair to `cac933cb` | **E3 ATTRIBUTION_MISMATCH** | unchanged |

### 7.3 Bucket counts and `overall_result`, per commit SHA

| bucket | Head A `987d2602` | Head B `a7cf5256` | submission `c7d56bbe` | Head D `5e30d497` |
|---|---:|---:|---:|---:|
| `verified` (E0) | 2 (F6, F7) | 4 (F1, F2, F6, F7) | 4 (F1, F2, F6, F7) | 5 (F1, F2, F3, F6, F7) |
| `failed` (E1/E2/E3) | 4 (F1, F2, F3, F8) | 2 (F3, F8) | 3 (F3, F8, F9) | 2 (F8, F9) |
| `unverifiable` (E6) | 0 | 0 | 0 | 0 |
| `incomplete` (E4/E5) | 2 (F4, F5) | 2 (F4, F5) | 2 (F4, F5) | 2 (F4, F5) |
| **total** | **2 + 4 + 0 + 2 = 8** | **4 + 2 + 0 + 2 = 8** | **4 + 3 + 0 + 2 = 9** | **5 + 2 + 0 + 2 = 9** |
| `overall_result` | **FAIL** | **FAIL** | **FAIL** | **FAIL** |

Arithmetic, per head, from the declaration list in §6:

- Head A `987d2602`, its own eight declarations: verified 2 (F6, F7) + failed 4
  (F1, F2, F3, F8) + unverifiable 0 + incomplete 2 (F4, F5) = 8.
- Head B `a7cf5256`, its own eight: verified 4 (F1, F2, F6, F7) + failed 2 (F3,
  F8) + 0 + 2 (F4, F5) = 8.
- Submission `c7d56bbe`, nine: verified 4 (F1, F2, F6, F7) + failed 3 (F3, F8,
  F9) + 0 + 2 (F4, F5) = 9.
- Head D `5e30d497`, nine: verified 5 (F1, F2, **F3**, F6, F7) + failed 2 (F8, F9)
  + 0 + 2 (F4, F5) = 9. #1452 closes F3 and touches nothing else, so `verified`
  rises by one and `failed` falls by one; F6 and F7 stay verified because they are
  content and historical assertions that #1452 did not reach, and F9 stays E3
  because the attribution sentence is still in Head D's manifest blob. Reading the
  set as "F3 plus one other verified item" would undercount: the verified bucket at
  this head holds five findings, not four.

The historical row `2 / 4 / 0 / 2` applies only to the review bound to `987d2602`
and is not the count of any later head; the `a7cf5256`, `c7d56bbe` and `5e30d497`
rows are not a correction of the historical one.

Head B (`a7cf5256`) shares its finding set and its `4 / 2 / 0 / 2 = 8` counts with
`c7d56bbe` as it stood before F9 was added, because its manifest blob and INDEX
row are identical (`50e41dfa…`, line 67 at both heads); it is nevertheless a
separate named entry, not a restatement of the submission head, and it is not
extended with F9 retroactively.

Head D is the last head this record covers. Any later head is a **fifth named
entry**: it is appended with its own commit SHA, its own tables and its own bucket
counts, and is never merged into these four. No entry's findings, line numbers,
bucket counts or verdict may be overwritten by the entry appended after it.

### 7.4 Adjudication record at `987d2602` / `10d33b3f` (raw grades, retained as audit history)

Both reviewers' grades, exactly as they were reported before the ruling, each set
bound to the head that reviewer locked: L2-B at `987d2602`, L3-1 at `10d33b3f`
(re-read at `386d8f57`). They are reproduced unchanged; the divergence is the reason
the ruling exists.

**L2-B (implementing review, `987d2602`):**

| id | declaration | raw grade |
|---|---|---|
| D1 | `prompt_file` | E0 |
| D2 | `prompt_sha256` | E1 |
| D3 | `prompt_bytes` | E1 |
| D4a | correction: "`9be8aebf…`/2455 matched no version at any ref" | E0 |
| D4b | correction: "exactly four versions" | E4 |
| D5 | `prompt_id` | E0 |
| D6 | INDEX repeat | E1 |
| H1 | registration pin `9be8aebf…`/2455 | E2 |

L2-B totals: E0 ×3, E1 ×3, E2 ×1, E4 ×1 — 8 declarations. (The pre-adjudication
grade table additionally carried H2 E0 for the attribution of the stale pair to
`cac933cb…`; that item was not part of the ruling table and is retained here only
for completeness: **H2 E0**.)

**L3-1 (independent review, `10d33b3f` / re-read `386d8f57`):** E0 ×3, E1 ×3, E4 ×1, E5 ×1 — 8 declarations.

The two reviewers therefore agreed on the three E1s and on the E0/E1 mix, and
diverged on the two items the ruling settles: L2-B graded the version enumeration
E4 where L3-1 graded it E5, and L3-1 carried an E5 that the ruling rejects as
single-review candidate drift. Neither reviewer had a row for F5; the ruling adds
it, and the ruling also separates F6 (E0) from F8 (E2) where the earlier tables
had folded them into one item.

### 7.5 Ruling reasoning

1. **Count-assertion classification.** The protocol classes "exactly four
   versions" as a `COUNT_ASSERTION`, not as a historical or free-text claim: it
   must be bound to a candidate SHA, carry an explicit scan envelope, and
   enumerate the counted items individually. E5 is available only when the locked
   candidate itself changes during one review.
2. **Why "four versions" is E4 and not E5.** Seven non-empty distinct blob versions
   exist in the scope the manifest itself cites — eight if the 0-byte row is
   counted (§2.3.4) — so the enumerated count is incomplete, which is the E4
   condition. The two reviewers locked different candidate SHAs (`987d2602…` for
   L2-B, `10d33b3f…` for L3-1); each review held its own candidate stable, so the
   disagreement between reviewers is not candidate drift inside a single review and
   cannot produce E5.
3. **Why "2455 never existed" is E0 while the original pin is E2.** These are two
   different assertions. F6 is a negative claim — that the value is absent from a
   stated envelope — and it holds: zero hits across the declared refs/commits, and
   the only 2455-byte object in scope belongs to an unrelated file. F8 is the
   positive claim that the manifest pinned a value that existed, and it has no
   historical existence at all, which is E2. Verifying the negative claim does not
   rehabilitate the positive pin; both grades stand side by side, as the protocol
   permits.

### 7.6 Protocol classification

Classes assigned in this record: `BLOB_IDENTITY` (F1, F2, F3 — recomputed from the
committed blob), `HISTORICAL_ASSERTION` (F6, F7, F8 — bounded by the stated ref
and commit envelope), `ATTRIBUTION` (F9 — compared against the commit and the path
the declaration pins), and `COUNT_ASSERTION` (F4 — the distinct-version
enumeration, judged by re-running the path enumeration and counting results). F5
is an evidence-structure defect rather than a content class and is graded E4
under the "declaration that cannot be bound to a specific object blocks
completion" rule. The "four versions" assertion is now classed `COUNT_ASSERTION`
per the ruling.

E1, E2 and E3 coexist, as the spec allows: F3 carries E1, F8 E2, F9 E3. No E5
(candidate SHA stable within each review), no E6 among the machine-checkable set.

### 7.7 Machine-readable result

Bucket arithmetic at `c7d56bbe`, applied to the nine rows of §7.2: `verified` (E0)
= 4 (F1, F2, F6, F7); `failed` (E1/E2/E3) = 3 (F3, F8, F9); `unverifiable` (E6) =
0; `incomplete` (E4/E5) = 2 (F4, F5). Therefore 4 + 3 + 0 + 2 = 9 =
`declarations_checked`, with `overall_result: FAIL`. The JSON below is bound to
`c7d56bbe`, the submission head; it is not the Head D total. Head A's counts are
carried in `historical_head`, labelled as its own eight-declaration set; Head D's
counts are carried in its `head_bindings` entry (5 + 2 + 0 + 2 = 9). The four SHAs
are carried in `head_bindings`.

```json
{
  "protocol": "Exact-Head Independent Review Protocol v1",
  "work_item": "AID-2026-269",
  "issue": 1278,
  "candidate_sha": "c7d56bbee7a404c575c60f78055e366faed85f0a",
  "candidate_tree_sha": "94580c56c2827e5584d8cd59fcaaad22934cede2",
  "review_complete": true,
  "adjudicated_by": "Owner ruling 2026-11-27",
  "declarations_checked": 9,
  "verified": 4,
  "failed": 3,
  "unverifiable": 0,
  "incomplete": 2,
  "head_bindings": [
    {
      "role": "historical_defect",
      "label": "Head A",
      "candidate_sha": "987d26021affbb5ba6d651e0fb5985d6bd4026a5",
      "candidate_tree_sha": "2a73559ebf1406ef3892c4c71dce33c20731e446",
      "review_window_utc": "2026-11-27T04:09:16Z/2026-11-27T04:22:51Z",
      "index_row": 65,
      "manifest_blob_sha": "227c761d82984fb671ab3fa53f57b41c10bdd04c",
      "declared_sha256": "a459d7e523fbba4ffb8c0f6ade8d3d8c1ec6ce45b95c3f48f65b192c0413edb3",
      "declared_bytes": 3772
    },
    {
      "role": "post_remediation",
      "label": "Head B",
      "candidate_sha": "a7cf5256e975ff25fd2f75b3b5051b16d8d77d36",
      "candidate_tree_sha": "a9b018e7449f4be2e375d082235e2d892c5a40b1",
      "measured_at_utc": "2026-11-27T06:55:36Z",
      "index_row": 67,
      "manifest_blob_sha": "50e41dfa0c6f68ee1342fb7b107de286ff0b30b6",
      "declared_sha256": "9de0895124032230b3418ff062ef2d590d27f37582d2847032a46b7116a53724",
      "declared_bytes": 3714
    },
    {
      "role": "review_submission_head",
      "label": "head at submission",
      "candidate_sha": "c7d56bbee7a404c575c60f78055e366faed85f0a",
      "candidate_tree_sha": "94580c56c2827e5584d8cd59fcaaad22934cede2",
      "measured_at_utc": "2026-11-27T06:55:36Z",
      "index_row": 67,
      "manifest_blob_sha": "50e41dfa0c6f68ee1342fb7b107de286ff0b30b6",
      "declared_sha256": "9de0895124032230b3418ff062ef2d590d27f37582d2847032a46b7116a53724",
      "declared_bytes": 3714
    },
    {
      "role": "post_1452_remediation",
      "label": "Head D",
      "candidate_sha": "5e30d49776a2ce75069227a41470fa7e4ae00b2e",
      "candidate_tree_sha": "808f30b1b1c0ebe2624467a7768834d6c482c80d",
      "merged_at_utc": "2026-11-27T07:55:28Z",
      "index_row": 72,
      "manifest_blob_sha": "987f1efe409709165af80940e3a56062ced49a75",
      "declared_sha256": "9de0895124032230b3418ff062ef2d590d27f37582d2847032a46b7116a53724",
      "declared_bytes": 3714,
      "declarations_checked": 9,
      "verified": 5,
      "failed": 2,
      "unverifiable": 0,
      "incomplete": 2,
      "overall_result": "FAIL"
    }
  ],
  "historical_head": {
    "label": "Head A historical head, its own eight-declaration set (unaffected by F9 and by Head D)",
    "candidate_sha": "987d26021affbb5ba6d651e0fb5985d6bd4026a5",
    "candidate_tree_sha": "2a73559ebf1406ef3892c4c71dce33c20731e446",
    "index_row": 65,
    "declarations_checked": 8,
    "verified": 2,
    "failed": 4,
    "unverifiable": 0,
    "incomplete": 2,
    "overall_result": "FAIL"
  },
  "findings": [
    {
      "id": "D2",
      "category": "BLOB_IDENTITY",
      "declaration_file": "14-ai-development/work-items/AID-2026-092/manifest.yaml",
      "declaration_line": 29,
      "declaration_field": "prompt_sha256",
      "declared_path": "14-ai-development/work-items/AID-2026-092/prompt-v1.md",
      "declared_sha256": "9de0895124032230b3418ff062ef2d590d27f37582d2847032a46b7116a53724",
      "actual_blob_object_sha": "7adf342a51f924cb732129ba3052ca65a832ea75",
      "actual_sha256": "9de0895124032230b3418ff062ef2d590d27f37582d2847032a46b7116a53724",
      "actual_bytes": 3714,
      "candidate_sha": "c7d56bbee7a404c575c60f78055e366faed85f0a",
      "declared": "9de0895124032230b3418ff062ef2d590d27f37582d2847032a46b7116a53724",
      "actual": "9de0895124032230b3418ff062ef2d590d27f37582d2847032a46b7116a53724",
      "result": "PASS",
      "grade": "E0",
      "historical_grade": "E1",
      "historical_candidate_sha": "987d26021affbb5ba6d651e0fb5985d6bd4026a5",
      "note": "final grade F1 at c7d56bbe: the declaration equals the SHA-256 of the blob at this head, fixed by #1321 (Head B a7cf5256, same manifest blob 50e41dfa…). The E1 for this declaration survives only in the Head A record, where the manifest declared a459d7e5… and measured 9de08951… (§2.2, §7.1)."
    },
    {
      "id": "D3",
      "category": "BLOB_IDENTITY",
      "declaration_file": "14-ai-development/work-items/AID-2026-092/manifest.yaml",
      "declaration_line": 30,
      "declaration_field": "prompt_bytes",
      "declared_path": "14-ai-development/work-items/AID-2026-092/prompt-v1.md",
      "declared_sha256": null,
      "actual_blob_object_sha": "7adf342a51f924cb732129ba3052ca65a832ea75",
      "actual_sha256": "9de0895124032230b3418ff062ef2d590d27f37582d2847032a46b7116a53724",
      "actual_bytes": 3714,
      "candidate_sha": "c7d56bbee7a404c575c60f78055e366faed85f0a",
      "declared": "3714",
      "actual": "3714",
      "result": "PASS",
      "grade": "E0",
      "historical_grade": "E1",
      "historical_candidate_sha": "987d26021affbb5ba6d651e0fb5985d6bd4026a5",
      "note": "final grade F2 at c7d56bbe: declares 3714 bytes, measured 3714. The Head A E1 (declared 3772, measured 3714) survives only in the historical record. declared_sha256 is null because this declaration is a byte count and asserts no digest."
    },
    {
      "id": "D4b",
      "category": "COUNT_ASSERTION",
      "declaration_file": "14-ai-development/work-items/AID-2026-092/manifest.yaml",
      "declaration_line": 35,
      "declaration_field": "prompt_digest_correction (distinct version enumeration)",
      "declared_path": "14-ai-development/work-items/AID-2026-092/prompt-v1.md, 14-ai-development/work-items/AID-2026-083/prompt-v1.md",
      "declared_sha256": null,
      "actual_blob_object_sha": null,
      "actual_sha256": null,
      "actual_bytes": null,
      "candidate_sha": "c7d56bbee7a404c575c60f78055e366faed85f0a",
      "declared": "exactly four (7689, 3772, 2915, 4137 bytes)",
      "actual": "seven non-empty distinct versions in the scope the declaration itself cites (7689, 2275, 4137, 2915, 3772, 3714, plus 3751 across all refs); eight if the 0-byte row is counted; three at the literal 092 path across all refs (two at c7d56bbe)",
      "result": "INCOMPLETE",
      "grade": "E4",
      "note": "final grade F4: the enumerated count is incomplete under both scopes, so E4 stands. The four digest/byte/object fields are null because the assertion counts distinct versions across commits at two paths, so no single digest, byte count or blob object applies. Counts: at c7d56bbe, 2 at the literal 092 path and 6 at the 092+083 pair; across all refs at the independent re-measurement (main cb5b3dcd, 9871 commits / 2780 refs / 14845 blobs), 3 and 7, or 8 if the 0-byte row counts. The 0-byte row (e3b0c442…) is the zero-length read of the three commits where the 083 path is absent, not a committed empty prompt (§2.3.4)."
    },
    {
      "id": "D7",
      "category": "BLOB_IDENTITY",
      "declaration_file": "14-ai-development/work-items/AID-2026-092/manifest.yaml",
      "declaration_line": 27,
      "declaration_field": "prompt_file_blob_sha (absent; only the prompt_sha256 + prompt_bytes pair is declared)",
      "declared_path": "14-ai-development/work-items/AID-2026-092/prompt-v1.md",
      "declared_sha256": null,
      "actual_blob_object_sha": "7adf342a51f924cb732129ba3052ca65a832ea75",
      "actual_sha256": "9de0895124032230b3418ff062ef2d590d27f37582d2847032a46b7116a53724",
      "actual_bytes": 3714,
      "candidate_sha": "c7d56bbee7a404c575c60f78055e366faed85f0a",
      "declared": "no fixed blob field",
      "actual": "blob identity available only via git ls-tree: 7adf342a51f924cb732129ba3052ca65a832ea75",
      "result": "INCOMPLETE",
      "grade": "E4",
      "note": "final grade F5: no field binds the declaration to a specific blob, so the evidence structure is incomplete. declared_sha256 is null because the missing binding is exactly the blob identity; the manifest declares only prompt_sha256 and prompt_bytes."
    },
    {
      "id": "D6",
      "category": "BLOB_IDENTITY",
      "declaration_file": "14-ai-development/work-items/INDEX.md",
      "declaration_line": 67,
      "declaration_field": "AID-2026-092 prompt digest cell",
      "declared_path": "14-ai-development/work-items/AID-2026-092/prompt-v1.md",
      "declared_sha256": "a459d7e523fbba4ffb8c0f6ade8d3d8c1ec6ce45b95c3f48f65b192c0413edb3",
      "actual_blob_object_sha": "7adf342a51f924cb732129ba3052ca65a832ea75",
      "actual_sha256": "9de0895124032230b3418ff062ef2d590d27f37582d2847032a46b7116a53724",
      "actual_bytes": 3714,
      "candidate_sha": "c7d56bbee7a404c575c60f78055e366faed85f0a",
      "declared": "3772 bytes, a459d7e523fbba4ffb8c0f6ade8d3d8c1ec6ce45b95c3f48f65b192c0413edb3",
      "actual": "3714 bytes, 9de0895124032230b3418ff062ef2d590d27f37582d2847032a46b7116a53724",
      "result": "FAIL",
      "grade": "E1",
      "historical_declaration_line": 65,
      "note": "final grade F3: the INDEX declaration does not match the reviewed content. The row is line 67 at c7d56bbe, line 65 at 987d2602, line 71 at f155122c and line 72 at cb5b3dcd; the cell text is byte-identical at those four heads, so the finding is unchanged by the move. At 5e30d497 (Head D) line 72 carries the corrected cell — 3714 bytes, 9de08951… — and F3 is E0 there; this entry records the c7d56bbe grade."
    },
    {
      "id": "H1",
      "category": "HISTORICAL_ASSERTION",
      "declaration_file": "14-ai-development/work-items/AID-2026-092/manifest.yaml",
      "declaration_line": 32,
      "declaration_field": "registration value 9be8aebf7d595f81cc062e5c03a67fd8317aeefaf69dd635fd9031f112dc25d1 / 2455",
      "declared_path": "14-ai-development/work-items/AID-2026-083/prompt-v1.md",
      "declared_sha256": "9be8aebf7d595f81cc062e5c03a67fd8317aeefaf69dd635fd9031f112dc25d1",
      "actual_blob_object_sha": "ecdb9285c2c2c9975de35a002a7efbc47915346d",
      "actual_sha256": "a459d7e523fbba4ffb8c0f6ade8d3d8c1ec6ce45b95c3f48f65b192c0413edb3",
      "actual_bytes": 3772,
      "candidate_sha": "c7d56bbee7a404c575c60f78055e366faed85f0a",
      "declared": "existed at registration",
      "actual": "0 occurrences at either prompt path across 2708 refs / 9753 commits (and across the 2454 refs / 9211 commits envelope of the Head A review); file was 3772 bytes at the declaring commit f61dc15a7701702a57a7c0edcfc9d61591986bca and at cac933cb9eb3e51b725dfaca0af47d5c05f8ad80",
      "result": "FAIL",
      "grade": "E2",
      "note": "final grade F8: the pin asserts historical existence of a value absent from the whole stated envelope; the correction's negative claim (F6) is E0 and does not rehabilitate the pin. The actual fields are the pinned pre-rename file as it stood at the declaring commit cac933cb… (§2.4): blob ecdb9285…, 3772 bytes, a459d7e5… — not the declared digest."
    },
    {
      "id": "D4a",
      "category": "HISTORICAL_ASSERTION",
      "declaration_file": "14-ai-development/work-items/AID-2026-092/manifest.yaml",
      "declaration_line": 31,
      "declaration_field": "prompt_digest_correction (historical nonexistence claim)",
      "declared_path": "14-ai-development/work-items/AID-2026-092/prompt-v1.md, 14-ai-development/work-items/AID-2026-083/prompt-v1.md",
      "declared_sha256": "9be8aebf7d595f81cc062e5c03a67fd8317aeefaf69dd635fd9031f112dc25d1",
      "actual_blob_object_sha": null,
      "actual_sha256": null,
      "actual_bytes": null,
      "candidate_sha": "c7d56bbee7a404c575c60f78055e366faed85f0a",
      "declared": "9be8aebf… / 2455 matched no version of the file at any commit reachable from any ref",
      "actual": "0 hits for the digest and no 2455-byte blob at either path across 2708 refs / 9753 commits; the five sizes present are 7689, 3772, 2915, 4137 and 3714; the single 2455-byte blob in the object store is 72993b65… (AID-2026-082/session-evidence.md)",
      "result": "PASS",
      "grade": "E0",
      "note": "final grade F6: the negative claim holds in the stated envelope. actual_blob_object_sha, actual_sha256 and actual_bytes are null because the claim is one of absence — no object carries the declared digest or the declared byte count at either prompt path, so there is no actual object to name."
    },
    {
      "id": "F7",
      "category": "HISTORICAL_ASSERTION",
      "declaration_file": "14-ai-development/work-items/AID-2026-092/manifest.yaml",
      "declaration_line": 30,
      "declaration_field": "prompt_bytes / prompt_sha256 (the declared pair as of first introduction)",
      "declared_path": "14-ai-development/work-items/AID-2026-092/prompt-v1.md",
      "declared_sha256": "a459d7e523fbba4ffb8c0f6ade8d3d8c1ec6ce45b95c3f48f65b192c0413edb3",
      "actual_blob_object_sha": null,
      "actual_sha256": "a459d7e523fbba4ffb8c0f6ade8d3d8c1ec6ce45b95c3f48f65b192c0413edb3",
      "actual_bytes": 3772,
      "candidate_sha": "c7d56bbee7a404c575c60f78055e366faed85f0a",
      "declared": "3772 bytes, a459d7e5… at first introduction",
      "actual": "3772 bytes, a459d7e523fbba4ffb8c0f6ade8d3d8c1ec6ce45b95c3f48f65b192c0413edb3 at f61dc15a7701702a57a7c0edcfc9d61591986bca (the introduction commit)",
      "result": "PASS",
      "grade": "E0",
      "note": "final grade F7: manifest and prompt were both first introduced at f61dc15a… with this byte count and digest (§2.3.1, §2.4). actual_blob_object_sha is null because §2.3.1 records the commit SHA and the content, not the blob object SHA at that commit, and no value is inferred here. No pre-adjudication row id exists for this finding (§7.1 mapping)."
    },
    {
      "id": "F9",
      "category": "ATTRIBUTION",
      "declaration_file": "14-ai-development/work-items/AID-2026-092/manifest.yaml",
      "declaration_line": 36,
      "declaration_field": "prompt_digest_correction (attribution of the 3772-byte pair to cac933cb)",
      "declared_path": "14-ai-development/work-items/AID-2026-092/prompt-v1.md",
      "declared_sha256": null,
      "actual_blob_object_sha": null,
      "actual_sha256": null,
      "actual_bytes": null,
      "candidate_sha": "c7d56bbee7a404c575c60f78055e366faed85f0a",
      "declared": "the pair was present from cac933cb, the commit that created this manifest, in which the file it pins is already 3772 bytes",
      "actual": "at cac933cb the declared path AID-2026-092/prompt-v1.md does not exist (git cat-file -e exits 128); the 3772-byte / a459d7e5… content sits at AID-2026-083/prompt-v1.md, blob ecdb9285…, which is the path the manifest pinned before the 092 renumber",
      "result": "FAIL",
      "grade": "E3",
      "note": "final grade F9: the sentence is true of the content and false of the declared path. declared_sha256 is null because the sentence asserts a byte count and a provenance commit, not a digest; the three actual_* fields are null because the declared path has no object at cac933cb, and the 083-path measurement is carried in actual and §2.4 rather than written into a field that would then read as if it described the declared path. The raw H2 E0 row in §7.4 is retained unchanged: it grades the content half of the attribution, which holds; F9 grades the path half, which does not."
    }
  ],
  "overall_result": "FAIL"
}
```

## Remediation and Scope Boundary

#1321 fixed F1 and F2: at `a7cf5256`, at `c7d56bbe` and at `5e30d497` the manifest
declares the measured pair, so **the case does not re-count a historical fix as a
defect at any of those heads**. The E1 for F1/F2 survives only in the Head A record
(§2, §7.1) and is not overwritten by the later E0.

The case equally does not treat the remaining findings as fixed. At `c7d56bbe`
the INDEX row (line 67 at `c7d56bbe`), the four-version enumeration, the missing
blob field, the registration value and the attribution sentence are the same
content Head A's manifest and INDEX carried, and they are graded open in §6 / §7.2.
At Head D `5e30d497`, #1452 closes the INDEX row (line 72, F3 → E0) and leaves F4,
F5, F8 and F9 open (§7.2.1, §7.3).

Scope: AID-2026-092's files were not modified by this review, and this restructure
changed only this record.

- **Review execution: PASS** — every declaration was recomputed from committed
  objects with recorded commands and exit codes.
- **Reviewed declaration: FAIL at all four heads** — Head A `987d2602` fails on E1
  (F1, F2, F3) and E2 (F8) with two E4s; Head B `a7cf5256` and the submission head
  `c7d56bbe` fail on E1 (F3), E2 (F8) with two E4s (F4, F5), and `c7d56bbe`
  additionally carries E3 (F9); Head D `5e30d497` fails on E2 (F8), E3 (F9) and two
  E4s (F4, F5), with F3 closed there. The per-head grades are §7.1, §7.2, §7.2.1 and
  the counts §7.3.
- **Remediation: NOT IN SCOPE** — AID-2026-092's files were not modified.

### Interpretation and Evidence Boundary

Each measurement is bound to its own exact candidate commit. Findings, line
numbers, bucket counts, and overall results must always be reported with that
candidate identity. Historical findings remain in the historical-head record;
post-remediation measurements establish the state at `a7cf5256`, `c7d56bbe` and
`5e30d497`. No head's record may overwrite or silently substitute for another's:
each new head is appended, never merged. Head D `5e30d497` is the last head this
record covers; a later head is appended as a fifth entry.

The review execution result and the reviewed declaration result are separate: a
completed review can correctly return `overall_result: FAIL` when the reviewed
head contains declarations or evidence defects. Recording the post-remediation E0
results for F1 and F2, and for F3 at Head D, does not imply that the remaining
findings at `c7d56bbe` or at `5e30d497` have been remediated.

## Prompt-to-Commit Trace Gate Disposition

The Prompt-to-commit trace (ratchet) check reports:

`NEW_NON_TRACEABLE AID-2026-269 NO_TRACE`

This is an expected fail-closed policy outcome, not a checker defect.

The ratchet compares newly introduced manifest identifiers against the manifest inventory in the base snapshot. Seeding an identifier into `--baseline` does not exempt it from the base-snapshot addition check. The checker explicitly requires a genuinely new non-traceable manifest to fail.

No implementation commit reachable from the PR base has been established as the implementation commit for AID-2026-269. The PR head commit is not base-reachable, and the base commit itself has not been established as implementing this work item. Assigning either commit as an implementation reference would create unsupported provenance.

Disposition:

- Work-item trace status: `NO_TRACE`
- Gate result: `FAIL`
- Governance disposition: `BLOCKED — PROMPT_TO_COMMIT_TRACE`
- Checker or workflow modification: `NOT AUTHORIZED`
- Fabricated implementation commit reference: `PROHIBITED`

This disposition does not invalidate the independently verified review findings recorded in this case. It records that the review artifact itself does not yet satisfy the repository's prompt-to-commit trace policy.
