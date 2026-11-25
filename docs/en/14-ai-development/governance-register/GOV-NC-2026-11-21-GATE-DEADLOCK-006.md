---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-21"
      last_verification_note: "All figures come from the GitHub REST API and from local gate runs on 2026-11-21; the 2026-11-25 annotations added in 12.3, 14.1 and 14.2 record no new measurement and change no number."
    usage_status: Active
    modification_status: Modified
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
    source: "14-ai-development/governance-register/GOV-NC-2026-11-21-GATE-DEADLOCK-006.md"
    en: null
    zh-CN: "docs/zh-CN/14-ai-development/governance-register/GOV-NC-2026-11-21-GATE-DEADLOCK-006.md"
---

# GOV-NC-2026-11-21-GATE-DEADLOCK-006 — The gate deadlocks itself on main: no PR can pass

- Register ID: GOV-NC-2026-11-21-GATE-DEADLOCK-006
- Status: `ACCEPTED` / `F-2_APPROVED; F-1_EQUIVALENT_FOR_TEMPLATE_ONLY` (Owner ruling 2026-11-21, section 14) / the empty diff returned `EXIT=2` from `ae37a419` until `81dd9a72d2` (section 12)
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

This is not "some PR is written wrong". It is **the gate itself sitting in an unsatisfiable state on the trunk**. An empty diff cannot pass, so no PR that omits the two-sided mirrors can pass either — the dividing line is "did it supply `docs/en` + `docs/zh-CN` mirrors", not "which file did it touch". See the six isolation trials in section 2.1.

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

### 2.1 Correction of scope: it is not "no PR can pass"

The first draft of this register said "any PR based on the current `main` gets the same `EXIT=2`". Measured, that is **too broad** and must be narrowed.

Six isolation trials on `14-ai-development/governance-register/`, all on the same clean `main` tree:

| Trial | What was done | gaps | baseline | NEW | EXIT |
|---|---|---|---|---|---|
| A | three register pairs, each given real `docs/en` + `docs/zh-CN` mirrors | 207 | 207 | **0** | **0** |
| B | three register pairs written into `EMBEDDED_BILINGUAL_SOURCES` | 207 | 207 | **0** | **0** |
| C | three register pairs appended to the baseline | 213 | 213 | **0** | **0** |
| D | three register pairs all deleted | 207 | 207 | **0** | **0** |
| E | a brand-new side-by-side `.md` + `.en.md` pair, no mirrors | 215 | 207 | **8** | **2** |
| F | a brand-new file elsewhere, **with** real mirrors | 213 | 207 | 6 (all of them 005/006/007) | **2** |

A, B, C and D are all `EXIT=0`. So **the directory is not closed**. What is closed is "adding a file to it without mirrors".

The mechanism, more precisely: `current_bilingual_gaps()` requires `docs/en/<path>` and `docs/zh-CN/<path>` to **both** exist for every `.md` under `NORMATIVE_ROOTS`. `14-ai-development/` routes through `counterpart_14()`, but that only affects the `resolved_14` test — it does **not** affect the `english.is_file()` / `chinese.is_file()` tests. A side-by-side `.en.md` pair therefore does not by itself move a file out of the gap set. That is exactly why all 18 existing files in `governance-register/` (including `README.md`) sit in the baseline — both language sides are there.

Re-checked on a real PR (`main` → the three register pairs + all mirrors): `207 frozen, 0 new gaps`; adding `BILINGUAL-MANIFEST: COMPLETE` to the body gives `PASS (18 changed paths inspected)`, `EXIT=0`.

**So the correct conclusion is**: the unpaired template on `main` makes the **empty diff** permanently `EXIT=2`; any PR that **adds normative documents without two-sided mirrors** is likewise permanently `EXIT=2`; and a PR that supplies the mirrors passes. The first draft generalised "PRs without mirrors" into "any PR". Corrected here.

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

| # | Approach | Cost | Risk | Measured |
|---|---|---|---|---|
| F-1 | Add the template to `EMBEDDED_BILINGUAL_SOURCES` (it genuinely is a single-file bilingual template, which is what that list means) | 1 line + 1 reason comment | lowest; same pattern #404 used to add reasons elsewhere | trial B: `NEW=0` |
| F-2 | Give the template `docs/en` + `docs/zh-CN` counterparts | 2 new files | low; the mirrors are **not** new prose, they are copies of the same source | trial A: `NEW=0`, and **requires no normative change at all** |
| F-3 | Add the template to `bilingual-baseline.txt` | 1 line | **highest**: directly violates "the baseline may only shrink, never grow", turning the ratchet into a freely extensible list | trial C: `NEW=0`, but it destroys the ratchet's meaning |

**F-2 has to be stated precisely, or it reads as "split one template into three":**

a mirror means a **verbatim copy of the same source file**, not three documents that each evolve on their own. `00-governance/templates/document-metadata-template.md` stays where it is and remains the single authoritative source; `docs/en/...` and `docs/zh-CN/...` merely satisfy the existence check. Any change to the template's content still edits the source only, and the mirrors follow.

This is not this register's inference. The Owner's ruling of 2026-11-21 states the boundary:

> **On `document-metadata-template.md`: splitting it into three is not approved.**
> The template should remain in its existing location under `00-governance/templates/` as the single template source. If the file falls within the scope the gate requires mirrors for, supply both sides as mirrors of the same source; do not produce three independently evolving copies of the template body in order to satisfy a scanner.

So the correct execution of F-2 is "one source plus two copies", not "three bodies".

**F-2 is the recommendation** (approved by the Owner; F-1 is not this round's preferred fix and F-3 is not approved). F-2 changes no normative text and no script — pure documentation. F-1 works equally well (trial B: `NEW=0`) but is a normative change: it decides whether a single-file bilingual template belongs in the exemption class, which section 5 requires independent review for, and the author cannot supply it. The Owner also limits it: **`EMBEDDED_BILINGUAL_SOURCES` must not become the default channel for new registers**.

F-3 works mechanically (trial C: `NEW=0`) but **must not be used**: it converts a shrink-only ratchet into an appendable list, which abolishes the mechanism itself.

## 9. Relation to the rest of this round

- **005 (zero execution)**: this register is 005's first concrete consequence. 005 says "no verdict exists"; this says "even if one existed, it is 2".
- **#409**: merged at 04:20:40Z (head `ccd19ecd`, base `423fb4b7`). At merge time the baseline did not yet contain 005's two files, so it is unrelated to this deadlock; but main advanced 26 commits after it to reach `ae37a419`. **005's two files are still not on main** (`GET /contents/...CI-NOT-EXECUTED-005.md` → 404).
- **#407**: the Owner's comment there reports 83 (full scanner) vs 88 (gate basis). This register is two faces of the same mechanism: `current_bilingual_gaps()` requires both `docs/en` and `docs/zh-CN`, so **a side-by-side `.en.md` pair does not count as paired** — all 18 existing files in `governance-register/` (including `README.md`) sitting in the baseline is the direct consequence of that rule.
- **#414**: `ddd4150bf4` fixed "a paired-file move misread as a deletion" (`scripts/check_bilingual_docs.py` +36/−8). That is a **real improvement** to the gate's implementation, but it does not touch this deadlock — this deadlock is not a misjudgement, it is a correct rejection by design.
- **DIRECT-MAIN-001**: the introducing commit is direct push #63, and continues the escalation that register already recorded (the gate implementation rewritten by direct push) — this time the *content the gate governs* was also written by direct push.

## 10. Boundary between fact and inference

Facts:
- Every command, input, output and exit code in §1, §2.1, §3, §4.
- §5's commit metadata, the PR-association query result, the line counts.
- §7's identity census over 300 commits.

Inferences (**not** made):
- This register does not rule that `ae37a419`'s author "deliberately" bypassed the gate. The evidence shows only that no PR was used and the bilingual gate was not run.
- It does not rule whether F-1 or F-3 should be adopted. §8 gives cost, risk and measured exit codes, not a verdict.
- It does not read this deadlock as "#401/#408's ratchet design is defective". The ratchet works as designed; the defect is that adding an unpaired normative document and adding the baseline happened in one direct push, with no channel ever running the gate once.
- It does not read §2.1's four `EXIT=0` trials as "the deadlock does not exist". They read as: **the dividing line is the mirrors, not the file's content**. The empty diff is still `EXIT=2`, and that has not changed.

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

# 5) section 2.1's boundary: give a new file real mirrors and see it leave the gap set
#    call the gate's own functions directly, so the diff basis cannot interfere:
python - <<'PY'
import importlib.util, os, sys
os.chdir(".")
spec = importlib.util.spec_from_file_location("g", "scripts/check_bilingual_docs.py")
g = importlib.util.module_from_spec(spec); sys.argv = ["x"]; spec.loader.exec_module(g)
gaps, base = g.current_bilingual_gaps(), g.read_baseline()
print("gaps", len(gaps), "baseline", len(base), "NEW", len(sorted(gaps - base)))
PY
# after adding docs/en/<path> + docs/zh-CN/<path>, NEW goes to zero
```

**Register status**: `ACCEPTED` / `F-2_APPROVED` / empty diff on main is permanently `EXIT=2` / the dividing line is "did the PR supply two-sided mirrors", not "which file did it touch" (§2.1) / introduced by direct push with no PR / recommended fix F-2 approved by the Owner, not executed

Owner ruling (2026-11-21), summarised:

- Section 2.1's boundary correction is adopted; the first draft's "any PR gets `EXIT=2`" is withdrawn as too broad.
- **F-2 is approved** (supply the two-sided mirrors); F-1 is not this round's preferred fix; F-3 is not approved.
- F-2's constraints: mirrors must correspond to the correct source path and must not be satisfied by unrelated or placeholder files; `NORMATIVE_ROOTS`, the gate script, the exemption list and the baseline must not be modified; `EMBEDDED_BILINGUAL_SOURCES` must not become the default channel for new registers.
- **Splitting `document-metadata-template.md` into three is not approved**: the template stays under `00-governance/templates/` as the single source, and the mirrors are copies of that one source.
- Mirror copying under F-2 may be treated as a mechanical documentation operation and does not require separate word-by-word authorisation; but if a PR also carries a governance judgement, a normative content change, a template-semantics change or an exemption grant, the corresponding review requirements still apply.

---

## 12. The deadlock is resolved on main — via F-1, and via a self-reviewed merge

### 12.1 Facts

Roughly twelve minutes after this register was written, the deadlock was lifted:

| Item | Value |
|---|---|
| Issue | #416 `[P0] main is red: ae37a419 added a normative source with no bilingual mirror and...`, opened 2026-11-21T05:13:04Z, closed 05:52:03Z |
| PR | #418 `fix(bilingual): register metadata template exemption (#416)` |
| Change | `scripts/check_bilingual_docs.py` only, **+5 −0** |
| Substance | adds `00-governance/templates/document-metadata-template.md` to `EMBEDDED_BILINGUAL_SOURCES` with a reason string |
| author | `oahcom` |
| sole reviewer | `oahcom`, `COMMENTED`, 05:51:33Z |
| merger | `oahcom`, 05:51:45Z |
| review → merge | **12 seconds** |
| merge commit | `fce408340c3f` |

The entry added:

```python
"00-governance/templates/document-metadata-template.md": (
    "Provides one copy-paste metadata block whose field names, closed enums, "
    "and REQUIRED markers are consumed verbatim by check_document_management.py; "
    "split mirrors would let the two languages document different enum values."
),
```

### 12.2 Re-measured: the empty diff on main is now EXIT=0

On a clean tree at `main` `81dd9a72d2`:

```
$ BASE_SHA=$SHA HEAD_SHA=$SHA PR_BODY="BILINGUAL-MANIFEST: COMPLETE" python scripts/check_bilingual_docs.py
bilingual baseline: 207 frozen, 0 new gaps
exemptions: 21
Bilingual documentation and prompt-library gate: PASS (0 changed paths inspected).
EXIT=0
```

and:

```
exemptions 21
template exempt: True
gaps 207  baseline 207  NEW 0
```

**Section 1's central claim — the empty diff is permanently `EXIT=2` — no longer holds on `main`.** That is measured, not inferred.

### 12.3 Three things that must be recorded together, none cancelling another

**First, the fix applied was F-1, not the F-2 the Owner approved.**

The ruling said "F-2 is approved; F-1 is not this round's preferred fix; F-3 is not approved", and explicitly that "`EMBEDDED_BILINGUAL_SOURCES` must not become the default channel for new registers". What was actually executed is F-1.

That is not necessarily a violation: F-1 also measured `NEW=0` in trial B of section 2.1, and section 8 concedes it works technically. But **it is a normative change, which section 5 requires independent review for**, and section 12.1 shows the reviewer was the author.

> **〔Added 2026-11-25〕** This sentence uses the account-layer fact "the section 12.1 table shows `author` and the sole `reviewer` are both `oahcom`" as the reason for the review-layer conclusion "this normative change had no independent review". Section 5 was amended on 2026-11-24 by `2eb4e352` (PR #935) to a session-level test (see `GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036`): a separate session under the same GitHub identity can constitute independent review. `/pulls/{n}/reviews` returns only `user.login`, not the session, so the step "same identity implies same session" cannot be verified from that payload, and the table carries no session identifier either. Read this as "account layer not independent; session layer not verified".
> **What survives:** the section 12.1 table records exactly one review on that PR, with state `COMMENTED`. Section 5 states that a `COMMENT` review is technical commentary, not an `APPROVE`, and that holds under any version of section 5; so the conclusion "no independent approval was obtained" stands, but on that ground rather than on the account comparison. Only the account-comparison step is withdrawn.

**Second, the merge that lifted the deadlock is itself the failure mode register 007 records.**

`author == sole reviewer == merger`, 12-second interval, `COMMENTED` state. Identical in shape to all six rows in 007 section 1.

> **〔Added 2026-11-25〕** This sentence uses the account triple `author == sole reviewer == merger` as the reason for "identical in shape to all six rows in 007 section 1", that is, the same self-review failure mode. Section 5 was amended on 2026-11-24 by `2eb4e352` (PR #935) to a session-level test (see `GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036`): a separate session under the same identity can be independent. `/pulls/{n}/reviews` returns only `user.login`, not the session, so "same identity implies same session" cannot be verified from that payload. Read this as "account layer not independent; session layer not verified".
> **What survives:** the 12-second interval and the `COMMENTED` state are fields recorded in the section 12.1 table and do not depend on how identity is defined; and a `COMMENT` is not an `APPROVE` under any version of section 5, so "this merge carried no `APPROVE`" holds. What does not survive is "same shape implies same self-review": equal accounts do not entail equal sessions.

So there is a loop that has to be stated plainly:

> 006 records "the gate is unsatisfiable on the trunk".
> 007 records "merges rest on self-review".
> And 006's resolution was carried out by exactly the method 007 describes.

**Third, the resolution is technically valid and its reason holds up.**

The reason string for `document-metadata-template.md` is specific: its field names, closed enums and `REQUIRED` markers are **consumed verbatim** by `check_document_management.py`, so split mirrors could let the two languages document different enum values. That matches F-1's semantics (a single-file bilingual source) and matches the Owner's own ruling against splitting the template into three.

So the accurate record is: **the outcome is right, the process did not satisfy section 5.** Both, not one.

> **〔Added 2026-11-25〕** The second half of this sentence, "the process did not satisfy section 5", rested on the account equation `author == sole reviewer == merger`. Section 5 was amended on 2026-11-24 by `2eb4e352` (PR #935) to a session-level test (see `GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036`): a separate session under the same identity can be independent; `/pulls/{n}/reviews` returns only `user.login`, not the session, so "same identity implies same session" cannot be verified. The account comparison should be read as "account layer not independent; session layer not verified".
> **What survives:** "the outcome is right" is untouched. The second half also stands, but on a different ground: the section 12.1 table records exactly one review — `COMMENTED`, by `oahcom`, 12 seconds before the merge. Section 5 states that a `COMMENT` review is technical commentary, not an `APPROVE`, and that is version-independent; "the only review was not an `APPROVE`" therefore holds under any version of section 5, so "the process did not satisfy section 5" still holds. What does not hold is "same account implies same session".

### 12.4 Effect on this register's conclusions

| Claim | Status |
|---|---|
| §1: the empty diff on `main` is permanently `EXIT=2` | **lapsed** (`EXIT=0` from `81dd9a72d2`) |
| §1: the deadlock persisted across 7 commits | holds (`ae37a419` → `7d2233a5`) |
| §2.1: the dividing line is "did the PR supply two-sided mirrors" | **still holds**, and #418 confirms it from the other side — without mirrors, the only exit is the exemption list |
| §8: F-2 is the preferred fix | approved by the Owner, not executed; F-1 was executed |
| §7: three failures stack | still holds; #418 does not touch 005's zero execution |

### 12.5 A more precise mechanism

Combining section 2.1's six trials with section 12.1, a new file under `NORMATIVE_ROOTS` has **three** ways to pass, not two:

1. supply `docs/en` + `docs/zh-CN` mirrors (trial A);
2. enter `EMBEDDED_BILINGUAL_SOURCES` (trial B — the path #418 took);
3. append to the frozen baseline (trial C — breaks the ratchet's meaning, must not be used).

Path 1 needs no normative change. Path 2 needs one, plus independent review. Path 3 is unavailable.

The first draft of this register treated "no mirrors means permanently rejected" as the only dividing line, which missed path 2. That is the second over-generalisation, corrected here.

---

## 13. What this register's own PR has to look like — the structural gate and semantic correctness are not connected

### 13.1 What the gate actually requires of a file in the root of `14-ai-development/`

`current_bilingual_gaps()` applies a **hard two-sided check** to every `*.md` under `NORMATIVE_ROOTS`:

```python
english = REPO_ROOT / "docs" / "en" / source
chinese = REPO_ROOT / "docs" / "zh-CN" / source
if not english.is_file() or not chinese.is_file() or resolved_14 is None:
    gaps.add(source)
```

`resolved_14` calls `counterpart_14()`, which does accept side-by-side naming (`X.md` ↔ `X.en.md`). The two `is_file()` calls above do **not**. Side-by-side naming makes `resolved_14` non-null; it does not make `docs/en/` or `docs/zh-CN/` exist.

Measured on this register's own three files at `main` `ad4d7221f9`:

| Trial | Shape | Files | Result |
|---|---|---|---|
| S1 | root `X.md` + `X.en.md` only (side-by-side) | 6 | `::error::New bilingual gap outside frozen baseline` × 6, `EXIT=2` |
| S2 | S1 plus `X.md` and `X.en.md` in both `docs/en` and `docs/zh-CN` | 12 | still `EXIT=2` (`.en.md` missing from both mirrors; 3 errors) |
| S3 | root `X.md`(zh) + `docs/en/X.md`(en) + `docs/zh-CN/X.md`(zh) | 9 | **`EXIT=0`**, `207 frozen, 0 new gaps` |
| T-a | no root file; `docs/en`(en) + `docs/zh-CN`(zh) only | 6 | **`EXIT=0`** |

Conclusion: a new register under `14-ai-development/` **cannot pass on side-by-side `.en.md` alone**; it must supply real mirrors in both `docs/en/` and `docs/zh-CN/`.

### 13.2 "Just add it to the baseline" is not an exit

Trial C in section 2.1 only exercised `current_bilingual_gaps()`. After writing the file into `scripts/bilingual-baseline.txt`, **a second check rejects it**:

```
$ # add 14-ai-development/probe-single.md and list it in the baseline
bilingual baseline: 208 frozen, 0 new gaps
::error::14-ai-development/probe-single.md has no resolvable bilingual counterpart
         (side-by-side .en.md/.zh-CN.md or docs/en mirror); pair it, register it in
         EMBEDDED_BILINGUAL_SOURCES, or use a documented BILINGUAL-EXCEPTION
Bilingual documentation gate: FAIL
EXIT=1
```

So "trial C: `NEW=0`" in section 2.1 holds only at the first check. Extending the baseline both violates the ratchet's meaning and **fails mechanically** — the two checks run in series, so extending the baseline merely converts `EXIT=2` into `EXIT=1`.

### 13.3 A defect that must be stated: the gate cannot tell a mirror from a copy of the other language

The first version of this register's PR #419 had 18 files:

```
14-ai-development/governance-register/X.md           (Chinese)
14-ai-development/governance-register/X.en.md        (English)
docs/en/14-ai-development/governance-register/X.md   (Chinese <- same blob as root)
docs/zh-CN/14-ai-development/governance-register/X.md (Chinese <- same blob)
```

`docs/en/` contained **Chinese prose**. Measured hashes:

```
97c43724309d 14895  14-ai-development/governance-register/GOV-NC-2026-11-21-SELF-REVIEW-007.md
a2ab8d078533 16635  14-ai-development/governance-register/GOV-NC-2026-11-21-SELF-REVIEW-007.en.md
97c43724309d 14895  docs/en/14-ai-development/governance-register/GOV-NC-2026-11-21-SELF-REVIEW-007.md
97c43724309d 14895  docs/zh-CN/14-ai-development/governance-register/GOV-NC-2026-11-21-SELF-REVIEW-007.md
```

`docs/en` and the root are **the same blob** — the English directory held Chinese. The gate judged that shape `EXIT=0`.

This is not a bug in the gate; it is its declared boundary. On success the script prints:

```
This is a structural gate only; semantic parity requires independent review.
```

But one consequence has to be recorded: **"supply the two-sided mirrors" can be satisfied mechanically while being semantically wrong.** An executor watching only for `EXIT=0` will ship a file whose English directory contains Chinese, and the gate will endorse it. The first version of this register did exactly that. I wrote it; nobody else did.

### 13.4 Disposition

This PR is reshaped to S3 (9 files): Chinese prose in the root, **genuine English** in `docs/en/` (the former `X.en.md` content), Chinese in `docs/zh-CN/`. The side-by-side `.en.md` files are deleted, and the Chinese copies under `docs/en` are deleted.

Two independent reasons:

1. **The gate requires it.** S3 is the smallest `EXIT=0` shape and matches the repository's existing convention — established normative documents such as `00-governance/design-principles.md` are exactly this three-part layout.
2. **The Owner's ruling requires it.** Do not duplicate prose to satisfy a scanner. The 18-file version put Chinese under `docs/en`, which is precisely that duplication.

### 13.5 Effect on this register's conclusions

| Claim | Status |
|---|---|
| §2.1: the dividing line is "did the PR supply two-sided mirrors" | **holds, but must be made precise**: the mirrors are real files under the `docs/en` and `docs/zh-CN` *directories*, not side-by-side `.en.md` |
| §2.1 trial C: "baseline gives `NEW=0`" | **narrowed**: passes the first check only, fails the second with `EXIT=1` (§13.2) |
| §12.5: three passing paths | **narrowed to two and a half**: mirrors (both directories), the exemption list, baseline (mechanically unavailable and against the ratchet) |
| The gate guarantees semantic correctness | **it does not**, and there is now a counter-example (§13.3) |

---

## 14. Owner ruling (2026-11-21): F-1 as a restricted equivalent for this template, and non-retroactivity for #418's process

### 14.1 What the ruling says

| Dimension | Ruling |
|---|---|
| F-1 technical path (for `document-metadata-template.md`) | **accepted** |
| Current governance basis for the template exemption | **this ruling** (there was none before) |
| Did #418 have prior authorisation | **no** |
| Did #418 satisfy the independent-review requirement | **no**〔Added 2026-11-25: this "no" rests on the section 12.1 account triple; section 5 became a session-level test on 2026-11-24, and account layer not independent, session layer not verified. The "no" itself still holds, on the ground that the only review was a `COMMENTED`, not an `APPROVE`, which is version-independent. Original text preserved〕 |
| Was #418's merge process compliant | **no**〔Added 2026-11-25: this "no" rests on the section 12.1 account triple; section 5 became a session-level test on 2026-11-24, and account layer not independent, session layer not verified. The "no" itself still holds, on the ground that the only review was a `COMMENTED`, not an `APPROVE`, which is version-independent. Original text preserved〕 |
| Does F-1 become a general channel for new registers | **no**, this template only |

The technical reason given matches section 12.3's third point: the template's field names and closed enums are consumed verbatim by `check_document_management.py`, so split mirrors could let the two languages record different enum values.

The ruling also draws five boundaries, all of which must be recorded:

1. it applies to this template only and **does not authorise F-1 as a general channel for other new register files**;
2. machine-consumed field names and enum values must keep a single, stable authoritative form;
3. reader-facing prose may be bilingual, but **machine-consumed identifiers must not be translated or rewritten**;
4. the exemption must record its reason, scope and authority, and **must not expand into a directory-level exemption**;
5. **F-1 passing must not be read as proof that the Chinese and English are semantically equivalent.**

### 14.2 Retroactive approval is not prior authorisation

The ruling states plainly: "this round's approval does not retroactively change the procedural state of #418 at merge time. Post-hoc approval must not be written up as prior authorisation, and `SELF-REVIEW-007` must not be closed or weakened on its account."

That is the criterion this register has to fix in place. The facts of #418 are unchanged:

```
author = oahcom
sole reviewer = oahcom   (COMMENTED, 05:51:33Z)
merger = oahcom          (05:51:45Z)
review → merge = 12 seconds
```

F-1's technical result being accepted and that merge failing section 5 are **two independent facts**. Section 12.3's three-part structure therefore stands unchanged; only the first part is restated: F-2 was approved in advance, F-1 was what actually ran, and the Owner has now approved F-1 after the fact as a restricted equivalent for this template.

> **〔Added 2026-11-25〕** The preceding paragraph grounds "that merge failing section 5" in the three-line account record in the block above — an account-layer fact used as the reason for a review-layer conclusion. Section 5 was amended on 2026-11-24 by `2eb4e352` (PR #935) to a session-level test (see `GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036`); `/pulls/{n}/reviews` returns only `user.login`, not the session, so "same identity implies same session" cannot be verified. The block itself is a factual record and is left as written; the account comparison should be read as "account layer not independent; session layer not verified".
> **What survives:** "the only review was a `COMMENTED`" is not an `APPROVE` under any version of section 5, so "failing section 5" still holds — on that ground, not on account equality.

### 14.3 Effect on this register's conclusions

| Claim | Status after the ruling |
|---|---|
| §8 recommends F-2 | approved in advance, **not executed**; F-1 approved after the fact, restricted |
| §12.1 the fix used F-1, not F-2 | facts unchanged; the procedural deviation **stands** and is not erased by retroactive approval |
| §12.5 three passing paths | keeps section 13.5's narrowing: mirrors (both directories) / exemption list (case-by-case approval) / baseline (mechanically unavailable and against the ratchet) |
| §13.3 the gate cannot tell a mirror from a copy | unchanged, and indirectly confirmed by boundary 5 (`EXIT=0` does not imply semantic equivalence) |
| This register's own status | `ACCEPTED`, but the actual fix path on main differs from the path this register recommended, and that difference is recorded permanently |
