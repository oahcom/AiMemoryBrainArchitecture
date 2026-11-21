# GOV-NC-2026-11-21-REGRESSION-009

- Register ID: GOV-NC-2026-11-21-REGRESSION-009
- Status: `OPEN` / `ACTIVE` / main went red again **45 minutes after** the deadlock was lifted
- Found at: 2026-11-21T07:35Z
- Subject: repository `oahcom/AiMemoryBrainArchitecture`, main `277daec7d0c6`
- Prior registers: 006 (deadlock, lifted), 007 (self-review), 008 (gate merged with zero review)

## 1. Bottom line

The condition register 006 records — the gate returning `EXIT=2` for an empty diff on main — was lifted at `81dd9a72d2` (#418, F-1). **It recurred 45 minutes later at `1ad6c2cf67`.**

```
$ # clean tree at main 277daec7d0c6
$ BASE_SHA=$SHA HEAD_SHA=$SHA PR_BODY="BILINGUAL-MANIFEST: COMPLETE" \
    python scripts/check_bilingual_docs.py
::error::New bilingual gap outside frozen baseline: 14-ai-development/work-items/GAP-BASELINE-001.md
EXIT=2
```

Between the lift and the recurrence there was **no independent review of anything**.

## 2. Facts

### 2.1 The chain

| # | commit | time | identity | action | via PR? |
|---|---|---|---|---|---|
| 1 | `ae37a419` | 04:50:35Z | — | adds an unpaired normative document, first deadlock | no (direct push) |
| 2 | `fce40834` | 05:51:45Z | `oahcom` | #418 lifts it via F-1 (+5 exemption lines) | yes, **self-reviewed in 12 seconds** |
| 3 | `1ad6c2cf67` | 07:08:25Z | **`Owner-A <owner-a@local>`** | adds `14-ai-development/work-items/GAP-BASELINE-001.md` (+160), **second deadlock** | **no (direct push)** |
| 4 | `47b8600e75` | 07:15:33Z | `Owner-A` | modifies the same file (+10 −3) | **no (direct push)** |

### 2.2 The sixth commit identity

`Owner-A <owner-a@local>`, first seen in `1ad6c2cf67` (2026-11-21T07:08:25Z).

The five recorded earlier in this series: `oahcom`, `unknown <1491856051>`, `governance@localhost`, `oahcom <noreply@github.com>` (web commit), `Ubuntu <ubuntu@localhost.localdomain>`.

**The name deserves note**: "Owner" is the role that holds ruling authority in this governance system. And this identity:

- used no PR;
- added a normative file that turns main red;
- did so 45 minutes after someone fixed the same problem.

### 2.3 Identity distribution, last 20 commits on main

```
14  oahcom <81014746+oahcom@users.noreply.github.com>
 4  unknown <1491856051>
 2  Owner-A <owner-a@local>
```

Three identities. The only two PR-mediated commits in the window are `Merge PR #415` and `Merge PR #418`; everything else is a direct push or a web commit.

### 2.4 Why `GAP-BASELINE-001.md` is a gap

The file lives in `14-ai-development/work-items/`, a `.md` under `NORMATIVE_ROOTS`. Under the mechanism in 006 §13.1:

- no `docs/en/` or `docs/zh-CN/` mirror → `current_bilingual_gaps()` flags it;
- not in `scripts/bilingual-baseline.txt` (207 entries) → outside the baseline;
- not in `EMBEDDED_BILINGUAL_SOURCES`.

All three fail, hence `EXIT=2`.

`work-items/` already has 73 paths in the baseline, which is to say the directory has always relied on baseline exemption, and the baseline may only shrink.

### 2.5 What the file itself says

The filename and the two commit messages are worth quoting directly:

```
1ad6c2cf67  docs(work-items): freeze GAP-BASELINE-001 with re-measured six-area state
47b8600e75  docs(work-items): resolve GAP-BASELINE-001 baseline SHA ambiguity
```

That is: **the document is about the baseline, and it became a gap outside the baseline.** Not a rhetorical point — a measured one.

## 3. What the recurrence shows

006 §12 said plainly at the time of the lift: the fix was **technically effective** but **did not satisfy §5** (self-review, 12 seconds).

`1ad6c2cf67` shows that distinction is not formalism. **A fix that never had independent review cannot prevent the same class of problem, because nothing turns "why it was red" into "don't do this again."**

The three events are structurally identical:

| Event | How it entered | Caused | How it was fixed |
|---|---|---|---|
| `ae37a419` | direct push | deadlock #1 | #418, self-reviewed |
| `1ad6c2cf67` | direct push | deadlock #2 | not yet |

Same mistake, same channel, 45 minutes apart.

## 4. Relation to 008

008 records #423 changing the gate implementation (+110 −3) with `reviews=0`, closing the "an exemption can be self-registered" hole.

`1ad6c2cf67` landed 9 minutes after #423 merged (06:59:08Z). So:

- #423 closes one specific channel: registering an exemption in the same commit that creates the file;
- `1ad6c2cf67` neither registered an exemption nor added mirrors — it simply **added an unpaired file**, which was always forbidden and needs no new criterion.

So #423's fix is not shown to be ineffective. The accurate statement is: **#423 closed the self-registration channel, while `1ad6c2cf67` used the original channel — add an unpaired file, never touch the exemption table. That channel has been open from `ae37a419` through `1ad6c2cf67`.**

## 5. Inferences not made

- It does **not** rule that `Owner-A` is impersonating the Owner role. `Owner-A <owner-a@local>` is a git identity string that anyone can configure. This register records only that it exists, that it pushed directly, and that main went red.
- It does **not** rule that `GAP-BASELINE-001.md`'s content is defective. It may be a valuable record; the problem is only that the way it landed turns main red.
- It does **not** rule deliberate sabotage. The evidence supports "no PR, no gate, `EXIT=2`" and nothing further.
- It does **not** read the recurrence as refuting 006. 006 said "unsatisfiable at that time", which was true; the recurrence is a **new fact**, not a negation of the old one.

## 6. A criterion that would prevent a third occurrence

Preventing a third instance needs a constraint that does not exist today:

> Every write to `main`, from whatever identity, must first pass a gate execution that returns `EXIT=0`.

Today `main` accepts direct pushes from any identity, while the gate runs only on PRs — and (per 005) has never actually executed. So the constraint is **empty on both paths**: the PR path never runs it, the direct-push path never checks.

## 7. Reproduction

```bash
# 1) empty diff on main returns EXIT=2
git clone --depth 1 https://github.com/oahcom/AiMemoryBrainArchitecture.git
cd AiMemoryBrainArchitecture
SHA=$(git rev-parse HEAD)
BASE_SHA=$SHA HEAD_SHA=$SHA PR_BODY="BILINGUAL-MANIFEST: COMPLETE" \
  python scripts/check_bilingual_docs.py; echo "EXIT=$?"
# -> ::error::New bilingual gap outside frozen baseline: 14-ai-development/work-items/GAP-BASELINE-001.md
# -> EXIT=2

# 2) the file is not in the baseline
grep -c "GAP-BASELINE-001" scripts/bilingual-baseline.txt   # -> 0
grep -vc "^#" scripts/bilingual-baseline.txt                # -> 207

# 3) the introducing commit and its identity
curl -s -H "Authorization: Bearer $TOKEN" \
  https://api.github.com/repos/oahcom/AiMemoryBrainArchitecture/commits/1ad6c2cf67 \
  | jq '{author: .commit.author, parents: [.parents[].sha], files: [.files[] | {filename, additions}]}'
```

**Register status**: `OPEN` / `ACTIVE` / empty diff on main `277daec7d0c6` is `EXIT=2` / introduced by `Owner-A <owner-a@local>` / direct push, no PR / 006's deadlock recurred 45 minutes after it was lifted

---

## 8. Additional measurement: while main is red, no PR can pass

### 8.1 Isolation

On a clean tree at main `a730880efdae`:

```
=== base only, empty diff ===
::error::New bilingual gap outside frozen baseline: 14-ai-development/work-items/GAP-BASELINE-001.md
EXIT=2
```

Adding this PR's 15 files (root Chinese / `docs/en` English / `docs/zh-CN` Chinese per register):

```
=== 15 files, same base ===
::error::New bilingual gap outside frozen baseline: 14-ai-development/work-items/GAP-BASELINE-001.md
EXIT=2
```

**The identical error, because the tree-wide scan has nothing to do with the diff.** All 15 files are paired correctly and it changes nothing.

### 8.2 With that one file removed, the 15 files are judged fully compliant

Deleting `14-ai-development/work-items/GAP-BASELINE-001.md` from the same tree:

```
bilingual baseline: 207 frozen, 0 new gaps
EXIT=1   (for the single reason in 8.3)
```

By error class:

| Class | Count | Note |
|---|---|---|
| `New bilingual gap outside frozen baseline` | **0** | this PR's 15 files produce no new gap at all |
| `Embedded bilingual source … registered in the same commit` | 21 | all cite `84831075`, the base commit I synthesised locally (see 8.3) |
| `Normative source left NORMATIVE_ROOTS by deletion` | 1 | triggered by deleting `GAP-BASELINE-001.md` itself |

**The zero is the important number**: it proves §8.1's `EXIT=2` comes entirely from a pre-existing gap on main and has nothing to do with the PR's contents.

### 8.3 The 21 same-commit errors are my environment, not the repository

All 21 cite `84831075` — I ran `git init` on the main tree and made a single commit, so the entire history collapses into one. `check_embedded_registration_history()` uses `git log --diff-filter=A` to find the file-creation commit; in a flattened history every file's creation commit is `84831075`, and the exemption registrations are also in `84831075`, so everything reports a violation.

In the real repository's 770 commits, those files were created and registered in different commits and do not trigger. **These 21 cannot be used as evidence that #423 is defective**; they are only a side-observation that the criterion depends on real history (008 §6 records the same property).

### 8.4 The closure this establishes

> **When main carries a gap outside the baseline, no PR based on main can pass the bilingual gate, regardless of what the PR changes or how correct it is.**

This contrasts with 006 §2.1's "the judging domain is the diff, not the tree":

- **pairing** (`check_mirror_pairing`) judges the diff — only the paths this PR touched;
- **gap checking** (`current_bilingual_gaps` vs baseline) judges the **whole tree** — independent of this PR's changes.

So "a PR passes as long as it pairs its own files correctly" is false. **As long as the trunk carries an unfixed red, every PR returns `EXIT=2`.** That is the actual consequence of `1ad6c2cf67`: it did not merely turn main red, it disabled the entire PR channel.

### 8.5 Stacking with 005

005 records: zero gate verdicts in 36 hours, 85 merges.

Add this layer: even someone who wanted to use the PR channel **could not obtain `EXIT=0` after `1ad6c2cf67`**. So:

| Channel | State |
|---|---|
| PR + CI | never executed (005) |
| PR + local gate | permanently `EXIT=2` while main is red (this section) |
| direct push to main | no gate at all (009 §6) |

All three are empty. This is not "the gate is too strict"; it is **that the gate produces no effective verdict on any path**.

---

## 9. Owner ruling: hold section 5, both PRs wait (option b)

### 9.1 What was ruled

Faced with the structural deadlock "repairing the base (#440) and accepting #422 presuppose each other", the Owner chose **(b), hold section 5**, rather than (a), merge #440 by ruling:

> Better to state plainly that the PR channel is blocked for want of an independent reviewer than to manufacture a new governance exception through one urgent merge that no independent party verified.

The ruling also rejects "a repair change is exempt from independent review": #440 carries a **full Chinese translation**, and that translation carries normative force (the "explicit non-claims" and "dispatch rules" sections), so it is not a copy operation but **a transfer of governance text across languages**.

### 9.2 A factual correction accepted

The ruling withdraws the previous round's description of the root `GAP-BASELINE-001.md` as the Chinese authority. Measured:

```
$ # the root file on main a730880efdae
# GAP-BASELINE-001 — Key Missing Workload Baseline
- Repository: `oahcom/AiMemoryBrainArchitecture`
...
8460 bytes, entirely English
```

So the actual layout is:

| Path | Language and role |
|---|---|
| root `GAP-BASELINE-001.md` | the pre-existing English source, **unmodified** |
| `docs/en/.../GAP-BASELINE-001.md` | the root, verbatim, English |
| `docs/zh-CN/.../GAP-BASELINE-001.md` | full Chinese translation |

**The correction is worth recording in its own right**: "root means Chinese authority" was an unverified assumption, and at least one normative file in this repository is written in English. Any gate design or governance judgement that rests on that assumption needs re-checking.

### 9.3 The blocked chain and its release conditions

```
independent review of #440     <- blocked here
       ↓
merge #440
       ↓
tree-wide gap on main repaired
       ↓
empty-diff verification on main
       ↓
re-run #422 at exact head
       ↓
independent review and acceptance of #422
```

Release conditions, from the ruling:

1. designate a reviewer distinct from #440's author and merger;
2. check the English source, the English mirror and the Chinese translation item by item;
3. confirm the Chinese neither omits, alters nor widens the source's normative force;
4. the reviewer states an independent conclusion;
5. only then does the merge decision proceed.

And explicitly: **S-2 being unassigned does not lower the independence standard** — but it also does not require waiting forever for one unnamed account; any real, authorised independent reviewer satisfying identity separation will do.

### 9.4 The evidential weight of the local `EXIT=1` is bounded

The ruling accepts my attribution but bounds what it proves:

| Proposition | Holds? |
|---|---|
| #440 removes the tree-wide gap for `GAP-BASELINE-001.md` | yes (0 gap errors measured) |
| the 21 same-commit errors are a harness artifact | yes, not a repository defect |
| the local `EXIT=1` proves the gate will fail after merge | **no** |
| the local `EXIT=1` proves the gate will pass after merge | **no** |

So "verify the empty diff on the real main history after merge" cannot be skipped, and the local simulation cannot stand in for it.

### 9.5 State after the ruling

| Item | State |
|---|---|
| #440 | `OPEN / PENDING_INDEPENDENT_REVIEW` |
| #422 | `OPEN / BLOCKED_BY_BASE_REPAIR` |
| #419 | `CLOSED_UNMERGED` |
| #423 | `MERGED / PROCEDURALLY_NONCOMPLIANT / AUDIT_PENDING` |
| main bilingual gate | `BLOCKED_BY_GAP_BASELINE_001`, awaiting the real repair |
| S-2 second identity | `APPROVED_IN_PRINCIPLE / IDENTITY_NOT_ASSIGNED` |
| Sponsor / Accountable Owner | `NOT_ASSIGNED` |
| AID-2026-023/024/026 R2 | `NOT_AUTHORIZED` |

### 9.6 What this ruling means on its own

Section 9 does not record "blocked again". It records a **structural fact**:

> The gate's execution, the base's repair and the review's independence each presuppose the others, and every one of them depends on a party that does not yet exist.

006 records the gate being unsatisfiable; 005 records it never executing; 007 records reviews without independence; 008 records the criterion changed with zero review; 009 records the deadlock recurring and disabling the entire PR channel.

**Together they point at one thing: the problem is not a particular merge, file or identity. It is that the position "who has authority to decide" is empty.**

Choosing (b) is an admission that this vacancy cannot be filled by the author doubling as reviewer. It is the first time in this series that a blockage has been explicitly preserved rather than routed around.

---

## 10. The gap count went from one to three: deterioration continues

### 10.1 Measured

On main `776f04fb69` (2026-11-21T07:58:58Z), empty diff:

```
$ BASE_SHA=$SHA HEAD_SHA=$SHA PR_BODY="BILINGUAL-MANIFEST: COMPLETE" \
    python scripts/check_bilingual_docs.py
::error::New bilingual gap outside frozen baseline: 14-ai-development/work-items/AID-2026-040/E1-E8-entry-gate-measurement-2026-11-21.md
::error::New bilingual gap outside frozen baseline: 14-ai-development/work-items/AID-2026-040/prompt-v1.md
::error::New bilingual gap outside frozen baseline: 14-ai-development/work-items/GAP-BASELINE-001.md
EXIT=2
```

**One gap became three.** Two of them are new.

### 10.2 Where the two new gaps came from

| commit | time | PR | change |
|---|---|---|---|
| `1570a7591c` | 07:51:19Z | #437 | adds `AID-2026-040/E1-E8-entry-gate-measurement-2026-11-21.md` (+180), `manifest.yaml` (+106), `prompt-v1.md` (+176), edits `INDEX.md` (+1) |

Two of those `.md` files sit under `NORMATIVE_ROOTS` with no `docs/en` or `docs/zh-CN` mirror and are not in the baseline, so each adds a gap.

### 10.3 How #437 merged

| Item | Value |
|---|---|
| created | 2026-11-21T07:52:20Z |
| merged | 2026-11-21T07:58:58Z |
| span | 6m38s |
| author | `oahcom` |
| merger | `oahcom` |
| reviews | **0** |
| files | 4, `+463 −0` |
| checks | three, all `failure`, `steps=0` |

Identical in shape to #423 in register 008: `reviews=0`, `steps=0`, author is merger, done in minutes.

### 10.4 #426 also had `reviews=0`

| Item | Value |
|---|---|
| created | 07:15:35Z |
| merged | 07:36:55Z |
| span | 21m20s |
| reviews | **0** |
| files | 2, `+60 −6` |
| checks | four, all `failure`, `steps=0` |

#426 changed `scripts/check_bilingual_docs.py` (−6 lines, removing a duplicate exemption key) — **another zero-review change to the gate script**.

### 10.5 What this shows

009 §3 argued that a fix without independent review cannot prevent recurrence. The evidence is now stronger: **the problem is not only recurrence, it is continuing addition.**

```
07:08  Owner-A  direct push  +1 gap (GAP-BASELINE-001)
07:36  #426     zero review  gate script change (no new gap, but a criterion change)
07:51  #437     zero review  +2 gaps (AID-2026-040 x2)
07:58  main reaches 3 gaps
```

Fifty minutes, 1 → 3 gaps, and both writes were `reviews=0` or a direct push.

### 10.6 Against 005

005's window was 36 hours, 348 checks, 0 executions, 85 merges. That window has closed and the pattern continues:

- `#437` three `steps=0`
- `#426` four `steps=0`
- `#425` three `steps=0`
- `#423` three `steps=0`

**`steps=0` is not an incident. It is the default.**

### 10.7 An observation that cannot be avoided

These PRs look like work on GAP-01 through GAP-06 — the six missing areas `GAP-BASELINE-001.md` itself lists. That is:

- someone read the baseline carefully;
- started on all six gaps (#425 GAP-01, #433 GAP-02, #430 GAP-03, #428/#436 BMCP, #435 Phase 2, #434 context tests);
- opened at least nine PRs in parallel;
- none of which can get CI because the payment failed;
- all merged with `reviews=0`.

**Execution intensity is high; governance intensity is zero.** This is not idleness — it is high output coexisting with zero review. And that is exactly what registers 007 and 008 describe once load is applied: when CI is unavailable, the reviewer seat is empty, and the channel must move, `reviews=0` becomes the only workable path.

This has to be written down because it determines the fix: **the answer is not to ask executors to be more careful. It is to fill the empty seat.**

---

## 11. The blockage is lifted, but not by the path section 9 described

### 11.1 main is EXIT=0 again (real history)

On a real clone (770+ commits), checked out at `main` `c138654c94`:

```
$ BASE_SHA=$H HEAD_SHA=$H PR_BODY="BILINGUAL-MANIFEST: COMPLETE" python scripts/check_bilingual_docs.py
bilingual baseline: 118 frozen, 0 new gaps
exemptions: 21
Bilingual documentation and prompt-library gate: PASS (0 changed paths inspected).
EXIT=0
```

**The baseline dropped from 207 to 118 and the gap count from 3 to 0.** Section 8.4's closure — main red means every PR returns `EXIT=2` — still holds mechanically, but **its precondition no longer applies**.

### 11.2 The path taken was not section 9.3's chain

Section 9.3 expected: `independent review of #440 → merge → main repaired`. What happened:

| PR | State | Contents |
|---|---|---|
| #440 | **CLOSED_UNMERGED** (`reviews=0`) | `GAP-BASELINE-001` two-sided mirrors, +299 −0 |
| #442 | **CLOSED_UNMERGED** (`reviews=0`) | 7 files, incl. `document-scope-registry.yaml` mirrors |
| #443 | **CLOSED_UNMERGED** (`reviews=0`) | 6 files, incl. `GAP-BASELINE-001` mirrors |
| #445 | **MERGED** (`reviews=1`) | `bilingual-baseline.txt` **−89**, `check_bilingual_docs.py` **+3** |
| #446 | **MERGED** (`reviews=0`) | 6 files, `terminology.md` + ADR + both mirrors |
| #448 | **MERGED** (`reviews=0`) | 3 files, one line each in `terminology.md` |

**All three "add the mirrors" PRs were closed unmerged; what actually lifted the blockage was #445 — deleting 89 baseline entries.**

### 11.3 What #445 did: wire pair exemption into the gap scan

```diff
--- a/scripts/check_bilingual_docs.py
+++ b/scripts/check_bilingual_docs.py
@@ -258,6 +258,9 @@ def current_bilingual_gaps() -> set[str]:
              if source in EMBEDDED_BILINGUAL_SOURCES:
                  continue
+            # Inventory and changed-path gates must share prefixes or pair-exempt paths become permanent gaps.
+            if source.startswith(PAIR_EXEMPT_PREFIXES):
+                continue
              english = REPO_ROOT / "docs" / "en" / source
```

`PAIR_EXEMPT_PREFIXES`, which already existed:

```python
PAIR_EXEMPT_PREFIXES = (
    "14-ai-development/work-items/",
    "14-ai-development/prompts/",
    "14-ai-development/adr/",
)
```

In other words: **the changed-path gate had always exempted these three prefixes, but the tree-wide gap scan had not**, so every file under them became a permanent gap and was frozen into the baseline one by one. Most of the 89 entries came from exactly here:

```
14-ai-development/adr/ADR-RUN-001..003                (5)
14-ai-development/prompts/global|owners/*             (15)
14-ai-development/work-items/**                       (the rest)
```

### 11.4 This is a real fix, and its reasoning is correct

The comment in the script states it precisely:

> Inventory and changed-path gates must share prefixes or pair-exempt paths become permanent gaps.

That names a **desynchronisation between two criteria**: the same paths, exempt in one gate and not in the other, so the baseline gets permanently polluted by exempt entries and the ratchet cannot shrink.

**This is not routing around the gate; it is fixing an internal inconsistency in the gate itself.** It also explains section 13.2's measurement — why "just add it to the baseline" was never an exit: those 89 entries were the sediment of this very defect.

### 11.5 The procedural problem stands, and went undiscussed

| Fact | Value |
|---|---|
| #445 author | `oahcom` |
| #445 reviews | 1 |
| was that review from the author | **yes** (same shape as 007 §1) |
| #446 / #448 reviews | **0** |
| #440 / #442 / #443 | closed with `reviews=0` |

So: **the merge that lifted the blockage was still self-reviewed, and the next two were zero-review.**

This does not contradict section 9.6; it strengthens it. Fix quality and procedural compliance are independent lines. #445's fix is technically correct (independently evidenced in 006 §13), and its review independence is identical to the six rows in 007.

### 11.6 Effect on this register's conclusions

| Claim | Status |
|---|---|
| §8.4 main red means every PR is `EXIT=2` | **mechanism holds**, precondition currently unmet (`0 new gaps`) |
| §9.3 the blocked chain (#440 review → merge → repair) | **did not happen**; #440/#442/#443 all closed unmerged |
| §9.5 `#440 OPEN / PENDING_INDEPENDENT_REVIEW` | stale: `#440 CLOSED_UNMERGED` |
| §10.5 gaps 1→3 worsening | holds, and was then zeroed in one step by #445 |
| The shapes in 007/008 | **unchanged**; #445/#446/#448 continue them |

### 11.7 A methodological lesson

Section 9 treated "#440 must go through" as the only path, so it framed the blockage as "waiting for a reviewer". The actual solution was **finding two criteria out of sync** — which needs no reviewer, only someone reading the script.

That does not make section 9's ruling wrong (holding section 5 was procedurally right). It means: **when every path points at "we are missing a person", it is worth checking whether the problem was defined too narrowly.** Here, I defined it too narrowly.
