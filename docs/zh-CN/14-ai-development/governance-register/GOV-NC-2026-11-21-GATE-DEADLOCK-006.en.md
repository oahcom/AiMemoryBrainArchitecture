# GOV-NC-2026-11-21-GATE-DEADLOCK-006 — The gate deadlocks itself on main: no PR can pass

- Register ID: GOV-NC-2026-11-21-GATE-DEADLOCK-006
- Status: `OPEN` / `ACTIVE` / blocks every PR
- Found at: 2026-11-21T05:05Z (last verified 2026-11-21T05:40Z @ `7d2233a5be`)
- Introducing commit: `ae37a41900f1` (2026-11-21T04:50:35Z, **pushed straight to main, no PR**)
- Prior register: GOV-NC-2026-11-20-CI-NOT-EXECUTED-005 (36 hours of zero gate executions)
- Related: #401 (ratchet/baseline, PR #408), #407 (inventory basis), #414 (pair-move misclassification fix)

## 1. Bottom line

On `main`, the bilingual gate `scripts/check_bilingual_docs.py` **exits 2 for any input**, including an empty diff. Since `ae37a41900f1`, across 7 later commits, up to the current `7d2233a5be`, the verdict is unchanged.

```
$ git reset --hard ae37a41900f1     # clean main
$ BASE_SHA=$HEAD_SHA=$(git rev-parse HEAD) PR_BODY="BILINGUAL-MANIFEST: COMPLETE" \
    python scripts/check_bilingual_docs.py
::error::New bilingual gap outside frozen baseline: 00-governance/templates/document-metadata-template.md
EXIT=2
```

This is not "some PR is written wrong". It is **the gate itself sitting in an unsatisfiable state on the trunk**. Any PR based on the current `main` — whatever it changes, whatever the PR body says, with or without `BILINGUAL-MANIFEST: COMPLETE`, with or without a documented exception — gets the same `EXIT=2`.

**Re-verified at 2026-11-21T05:40Z**: `main` has advanced 7 commits from `ae37a41900f1` to `7d2233a5be`. Re-running the same command on a **clean tree at the newest head**:

```
$ SHA=<clean tree at 7d2233a5be>
$ BASE_SHA=$SHA HEAD_SHA=$SHA PR_BODY="BILINGUAL-MANIFEST: COMPLETE" python scripts/check_bilingual_docs.py
::error::New bilingual gap outside frozen baseline: 00-governance/templates/document-metadata-template.md
EXIT=2
$ # same tree, only that template deleted
$ bilingual baseline: 207 frozen, 0 new gaps / exemptions: 20
$ Bilingual documentation and prompt-library gate: PASS (0 changed paths inspected).
EXIT=0
```

The deadlock **did not self-heal and persists across 7 later commits**.

One correction: the first draft of this register said "`9b6f73385e` grew the baseline from 207 to 208". Measured, that commit changed only three files (`architecture-document-management-policy.md`, `scripts/check_document_management.py`, `scripts/test_check_document_management.py`) and **did not touch `scripts/bilingual-baseline.txt`**. The baseline has been **207** non-comment lines since `180d9ba0ebfc` introduced it, unchanged throughout. The deadlock therefore neither eases nor worsens as the baseline grows; it is determined solely by that one unpaired file.

Because CI has executed zero times since 2026-11-19T16:12:11Z (see 005), **no automated channel can surface this deadlock**. It is visible only when a human runs the script at exact Head.

## 2. Three lines of localisation

| Fact | Value |
|---|---|
| New file | `00-governance/templates/document-metadata-template.md` (101 lines, added by `ae37a419`) |
| Baseline | `scripts/bilingual-baseline.txt`, 207 frozen entries (introduced by `180d9ba0ebfc` at 2026-11-21T03:55:54Z) |
| Rule | the baseline may only shrink; any gap outside it → `::error::` + `EXIT=2` |

The new file lives under `00-governance/` (inside `NORMATIVE_ROOTS`), is `.md`, is neither in `EMBEDDED_BILINGUAL_SOURCES` nor under `PAIR_EXEMPT_PREFIXES`, and has no `docs/en` / `docs/zh-CN` counterpart → it is **a new gap outside the baseline** → the gate rejects it by design.

**Both mechanisms are individually correct; together they deadlock.** The baseline (#401/#408) and "new normative documents must be paired" are each reasonable. `ae37a419` introduced the baseline and an unpaired normative document in the same tree, so its own output cannot pass its own check.

## 3. Stepwise isolation (recomputable)

Same `ae37a419` tree, change one thing, read the exit code:

| # | Action | EXIT | Output |
|---|---|---|---|
| A | as-is, empty diff | **2** | `New bilingual gap outside frozen baseline: 00-governance/templates/document-metadata-template.md` |
| B | delete only that template | **0** | `bilingual baseline: 207 frozen, 0 new gaps` / `PASS (0 changed paths inspected)` |
| C | restore it + add an unrelated file | **2** | same as A |

B and C are inverse operations differing by that one file. **The root cause is isolated to a single path, not inferred.**

## 4. Before/after at the introduction point

| Revision | Template present | Baseline present | EXIT on empty diff |
|---|---|---|---|
| `9eca5eda84ce` (parent of `ae37a419`) | no | yes | **0** (`207 frozen, 0 new gaps`) |
| `ae37a41900f1` (current main) | yes | yes | **2** |

Both runs used a clean tarball, the script from that tree, an empty diff, and `BILINGUAL-MANIFEST: COMPLETE`. **The only variable is the new file.**

## 5. How it got in: direct push, no PR, no review

Commit metadata for `ae37a41900f1`:

```
author:    unknown <1491856051>     2026-11-21T04:50:35Z
committer: unknown <1491856051>     2026-11-21T04:50:49Z
GitHub-linked account: null
parents:   9eca5eda84ce
```

- The commit **has no associated PR** (`GET /commits/ae37a41900f1/pulls` → `[]`).
- The author identity `unknown <1491856051>` maps to no account; it is one of seven identities across 300 main commits (see §7).
- The commit message claims `Self-check: 114/114 passed. Incremental gate: PASS.` — 114 tests of `test_check_document_management.py`, and the *document-management* incremental gate. **That is not the bilingual gate.** The bilingual gate was never run, so it never found that the commit had deadlocked the trunk.

Change surface (5 files, +307/−194):

| File | Change |
|---|---|
| `00-governance/architecture-document-management-policy.md` | +7 −4 |
| `00-governance/architecture-document-metadata.schema.yaml` | +225 −133 |
| `00-governance/templates/document-metadata-template.md` | **+101 −0 (new)** |
| `scripts/check_document_management.py` | +41 −7 |
| `scripts/test_check_document_management.py` | +123 −50 |

## 6. Why 005's 36 hours of zero execution makes this worse

With CI working, `ae37a419` as a PR would have been stopped by its own gate; even as a direct push, the `push`-triggered `bilingual-docs.yml` would have gone red within seconds.

Actual state:

| Layer | State |
|---|---|
| PR gate | zero executions (005) |
| `push`-triggered gate | zero executions (005 §4: of 348 failures after the boundary, 345 have `steps=[]`) |
| Direct-push path | does not require a PR (DIRECT-MAIN-001) |
| Result | the deadlock has existed on the trunk for **> 10 minutes, still undetected**, discoverable only by manual reproduction |

**Three failures stacked**: direct push bypasses PR review → zero-execution CI bypasses automated checks → the baseline ratchet freezes the bypass into an unsatisfiable state. Any one alone is survivable; stacked, the trunk is unusable.

## 7. Commit identities on main (300 commits, 2026-11-19T18:06 → 2026-11-21T04:50)

| Count | Identity |
|---|---|
| 231 | `oahcom <81014746+oahcom@users.noreply.github.com>` |
| 26 | `oahcom <oahcom@users.noreply.github.com>` |
| 20 | `Ubuntu <ubuntu@localhost.localdomain>` |
| 10 | `unknown <1491856051>` |
| 7 | `L0-manager <l0@local>` |
| 4 | `oahcom <1491856051>` |
| 2 | `arch-governance <governance@localhost>` |

23 commits (4 distinct identity strings) **map to no GitHub account**. `unknown <1491856051>` and `oahcom <1491856051>` share the same email string, but one has a name and no account while the other has an account — two different configs on the same machine, and identity cannot be inferred from the shared string.

## 8. Fixes (three options, none executed)

This register **changes no code**. Options, in increasing cost:

| # | Approach | Cost | Risk |
|---|---|---|---|
| F-1 | Add the template to `EMBEDDED_BILINGUAL_SOURCES` (it genuinely is a single-file bilingual template, which is what that list means) | 1 line + 1 reason comment | lowest; same pattern #404 used to add reasons elsewhere |
| F-2 | Give the template `docs/en` + `docs/zh-CN` counterparts | 2 new files | medium; one "template" becomes three files that must stay in sync |
| F-3 | Add the template to `bilingual-baseline.txt` | 1 line | **highest**: directly violates "the baseline may only shrink, never grow", turning the ratchet into a freely extensible list |

F-1 is the recommendation, but it is **a governance judgement, not a mechanical fix**: it decides whether a single-file bilingual template belongs in the exemption class. Under PR-GOVERNANCE-001 §5 that judgement needs independent review, and the author cannot supply it.

## 9. Relation to the rest of this round

- **005 (zero execution)**: this register is 005's first concrete consequence. 005 says "no verdict exists"; this says "even if one existed, it is 2".
- **#409**: merged at 04:20:40Z (head `ccd19ecd`, base `423fb4b7`). At merge time the baseline did not yet contain 005's two files, so it is unrelated to this deadlock; but main advanced 26 commits after it to reach `ae37a419`. **005's two files are still not on main** (`GET /contents/...CI-NOT-EXECUTED-005.md` → 404).
- **#407**: the Owner's comment there reports 83 (full scanner) vs 88 (gate basis). This register is a more severe instance of the same family: not "two scanners disagree" but "the only gate is permanently 2 on the trunk".
- **#414**: `ddd4150bf4` fixed "a paired-file move misread as a deletion" (`scripts/check_bilingual_docs.py` +36/−8). That is a **real improvement** to the gate's implementation, but it does not touch this deadlock — this deadlock is not a misjudgement, it is a correct rejection by design. The two do not cancel out: the gate now judges more accurately, and it still returns 2 for every PR.
- **DIRECT-MAIN-001**: the introducing commit is direct push #63, and continues the escalation that register already recorded (the gate implementation rewritten by direct push) — this time the *content the gate governs* was also written by direct push.

## 10. Boundary between fact and inference

Facts:
- Every command, input, output and exit code in §1, §3, §4.
- §5's commit metadata, the PR-association query result, the line counts.
- §7's identity census over 300 commits.

Inferences (**not** made):
- This register does not rule that `ae37a419`'s author "deliberately" bypassed the gate. The evidence shows only that no PR was used and the bilingual gate was not run.
- It does not rule which of F-1/F-2/F-3 is the correct governance choice. §8 gives cost and risk, not a verdict.
- It does not read this deadlock as "#401/#408's ratchet design is defective". The ratchet works as designed; the defect is that adding an unpaired normative document and adding the baseline happened in one direct push, with no channel ever running the gate once.

## 11. How to recount

```bash
# 1) fetch a clean tree (do not use a working copy; local edits would contaminate)
curl -L -H "Authorization: Bearer $TOK" \
  https://api.github.com/repos/oahcom/AiMemoryBrainArchitecture/tarball/ae37a41900f1 | tar xz

# 2) run the gate on an empty diff
cd oahcom-AiMemoryBrainArchitecture-ae37a41900f1
git init -q . && git add -A && git commit -qm x
SHA=$(git rev-parse HEAD)
BASE_SHA=$SHA HEAD_SHA=$SHA PR_BODY="BILINGUAL-MANIFEST: COMPLETE" \
  python scripts/check_bilingual_docs.py; echo "EXIT=$?"     # -> 2

# 3) delete only that template and rerun
rm 00-governance/templates/document-metadata-template.md
git add -A && git commit -qm y
SHA=$(git rev-parse HEAD)
BASE_SHA=$SHA HEAD_SHA=$SHA PR_BODY="BILINGUAL-MANIFEST: COMPLETE" \
  python scripts/check_bilingual_docs.py; echo "EXIT=$?"     # -> 0

# 4) repeat 1-2 on the parent commit
#    (substitute 9eca5eda84ce for ae37a41900f1)             # -> 0
```

**Register status**: `OPEN` / `ACTIVE` / gate is permanently `EXIT=2` on main `ae37a41900f1` / introduced by direct push with no PR / fix requires a governance judgement, not executed
