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
