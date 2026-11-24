---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: NOT_RECORDED
      decision_date: NOT_RECORDED
      approved_version: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "No formal approval record, approver identity or decision date exists in this repository; recorded as NOT_RECORDED rather than inferred."
    usage_status: Active
    modification_status: Unchanged
  authority:
    canonical_status: Non-Canonical
    canonical_conflict_status: None
    normative_status: Informative
  bilingual_counterpart:
    source: "14-ai-development/governance-register/GOV-NC-2026-11-21-DEV-PR-GATE-010.md"
    en: null
    zh-CN: "docs/zh-CN/14-ai-development/governance-register/GOV-NC-2026-11-21-DEV-PR-GATE-010.md"
---

# GOV-NC-2026-11-21-DEV-PR-GATE-010 — Four of nine development PRs cannot pass the gate, all for the same reason

## 0. Summary

Following Owner ruling D (development continues; first make one compliant path actually work), I applied each of the nine development PRs' exact heads onto current main (`c138654c94`) and ran the bilingual gate on **real git history**.

Result:

**4 fail / 5 pass. All four failures share one cause, and none of them is "the PR content is wrong".**

More important: the five that pass fall into four different shapes, and the four that fail are all one shape. **The gate is effectively judging "which directory did you put the file in", not "is the bilingual pairing complete".**

**This document contains one self-correction (§1.2).** The first draft said side-by-side bilingual "works only for `14-ai-development`". Measurement shows it works for **none of the nine roots**, `14-ai-development` included. That is exactly the contradiction the Owner flagged, and the measurement is supplied below.

| PR | Workstream | Shape | Gate |
|---|---|---|---|
| #430 | Agent Integration | root + `docs/en` + `docs/zh-CN` | **PASS** |
| #428 | BMCP | `reviews/…/X.en.md` + `.zh-CN.md` | **PASS** |
| #429 | Memory Compiler arch | edits **existing** `docs/` pairs | **PASS** |
| #434 | Memory Context tests | `crates/` only | **PASS** |
| #444 | Memory Context e2e | `crates/` only | **PASS** |
| #425 | Memory Compiler | root `X.md` + `X.zh-CN.md` | **FAIL** |
| #433 | Memory Context | root `X.md` + `X.zh-CN.md` | **FAIL** |
| #435 | Phase 2 domain model | root `X.md` + `X.zh-CN.md` | **FAIL** |
| #436 | BMCP | root `X.md` + `X.zh-CN.md` | **FAIL** |

Correction record: #429 first measured `EXIT=1` because my harness silently skipped one file on `URLError`, producing a phantom missing counterpart. With the file fetched it is `EXIT=0`. That was my harness defect, not a PR defect.

## 1. This is not "some PRs are written badly"

### 1.1 Four positions, four different constraints

1. write under `crates/` -> outside this bilingual gate (code and tests; other governance checks are separate)
2. write under `reviews/` -> unconstrained (not in the root list)
3. write into existing `docs/` pairs -> constrained but satisfied
4. write into a `NORMATIVE_ROOTS` root with side-by-side bilingual -> **constrained and unsatisfied**

All four failures are case 4.

### 1.2 The mechanism (corrected — the first draft was wrong here)

```python
english = REPO_ROOT / "docs" / "en" / source
chinese = REPO_ROOT / "docs" / "zh-CN" / source
resolved_14 = (
    counterpart_14(source) if root_name == "14-ai-development" else True
)
if (
    not english.is_file()
    or not chinese.is_file()
    or resolved_14 is None
):
    gaps.add(source)
```

**The decisive point: `not english.is_file() or not chinese.is_file()` applies unconditionally to all nine roots.** `resolved_14` merely adds one extra condition for `14-ai-development`; **it never substitutes for the existence check on both `docs/` sides.**

So side-by-side bilingual (`.zh-CN.md` or `.en.md`) is **ineffective for all nine roots**, `14-ai-development` included.

#### Measured (real clone, main `c138654c94`, baseline 118)

Adding side-by-side files one group at a time on the real tree and calling `current_bilingual_gaps()` directly:

| Group | Files added | Result |
|---|---|---|
| baseline | — | `118` |
| T1 | `14-ai-development/zzprobe.md` + `.zh-CN.md` | **120** (+2, both gaps) |
| T2 | `04-memory-compiler/zzprobe.md` + `.zh-CN.md` | **122** (+2) |
| T3 | `08-bmcp-protocol/zzprobe.md` + `.zh-CN.md` | **124** (+2) |
| T4 | `02-domain-model/zzprobe.md` + `.en.md` | **126** (+2) |

**All four groups produce two gaps, without exception.** That is:

> **In the gap scan, side-by-side bilingual is never a pairing. It is two independent gaps.**

`counterpart_14`'s real scope is the **changed-path gate** (`check_mirror_pairing`), not the gap scan. In the gap scan it exists only as an extra veto (`resolved_14 is None`) — and even when it resolves, both `docs/` sides must still exist.

### 1.3 The accurate statement

| Shape | Gap scan (whole tree) | Changed-path gate (diff) |
|---|---|---|
| `X.md` + `X.zh-CN.md` side by side | **two gaps** (all nine roots) | resolvable under `14-ai-development`; the other eight do not participate |
| `X.md` + `X.en.md` side by side | **two gaps** | same |
| root + `docs/en` + `docs/zh-CN` | pass | pass |
| only `docs/en` + `docs/zh-CN` (no root) | pass | pass |

**That is the exact reason the four PRs fail: they add root files in side-by-side form, and side-by-side form is not accepted by the gap scan under any root.**

## 2. What this changes

Ruling D says development continues. These nine numbers say:

> **Of the six workstreams, every part that adds a normative document at a `NORMATIVE_ROOTS` root currently cannot pass — not because it is written wrongly, but because the gate recognises one directory shape only, and that shape conflicts with the repository's own convention.**

| Workstream | Related PRs | Gate | Meaning |
|---|---|---|---|
| Memory Compiler core | #425 fail, #429 pass | 1/2 | new contract docs rejected; editing existing docs works |
| Memory Context engine | #433 fail, #434/#444 pass | 2/3 | **tests get in, specs do not** |
| Agent Integration | #430 pass | 1/1 | used the three-part layout |
| BMCP stack | #428 pass (`reviews/`), #436 fail | 1/2 | move the directory and it passes |
| Phase 2/3 domain model | #435 fail | 0/1 | **cannot start** |
| End-to-end tests | #444 pass (not reproducible locally, see §3) | 1/1 | — |

**Two structural biases:**

**First, code and tests sit outside this bilingual gate.** It scans only `*.md` under `NORMATIVE_ROOTS`. So continued progress produces more implementation while the specs that explain it wait outside the door. #433 versus #434/#444 is that bias in a single sample.

**Second, bypassing the gate is easier than satisfying it.** #428 passed by writing into `reviews/`; #430 passed by adding two more copies. Neither is "make side-by-side bilingual legal". That is why nine owners produced nine shapes: **the gate never told anyone what the correct shape is, only what the wrong one is.**

## 3. #444 cannot be reproduced locally (environment, not PR defect)

#444 is the only PR that is genuinely end-to-end testing (Rust integration test, `crates/memory-context/tests/e2e_store_to_context.rs`, 178 lines).

```
$ cargo test --offline -p memory-context --test e2e_store_to_context
error occurred in cc-rs: gcc.exe: fatal error: cannot execute 'cc1'
```

`libsqlite3-sys` compiles sqlite3 from C source and the local gcc is missing `cc1` (incomplete MinGW install). **Environment defect, not a PR defect.** Recorded so it is not misread as "#444's tests fail".

`cargo build -p memory-context` succeeds on main (11.33s), so the crate itself compiles; only the sqlite C dependency cannot be built.

## 4. Reproduction

```bash
# real clone, main c138654c94
for PR in 425 428 429 430 433 434 435 436 444; do
  git reset --hard origin/main && git clean -qfd
  # fetch that PR's changed files, verify each blob SHA-1, write to disk
  git add -A && git commit -m "sim $PR"
  BASE_SHA=$(git rev-parse origin/main) HEAD_SHA=$(git rev-parse HEAD) \
    PR_BODY="BILINGUAL-MANIFEST: COMPLETE" python scripts/check_bilingual_docs.py
done

# pair-probe (§1.2), real clone at main
# add 14-ai-development/zzprobe.md + .zh-CN.md, then call current_bilingual_gaps()
# baseline 118 -> 120; repeat for 04, 08, and .en.md under 02 -> 122, 124, 126
```

## 5. What this register does not claim

- It does not claim the four PRs should be closed. Their content is fine; their **shape** is not accepted.
- It does not claim the gate should be relaxed unconditionally. The rule in §1.2 is reasonable in principle; the problem is that it recognises one shape only, and that was never written down.
- It does not claim I have solved this. I only measured it.
- It does not count #444's local failure as a PR defect (§3).
- It does not read #434/#444 passing as "code is under no governance at all" — it only shows this bilingual Markdown gate does not scan `crates/`; build, tests and other checks are separate.

## 6. Owner ruling (2026-11-21): option A, side-by-side pairing is legitimate

### 6.1 What was ruled

> The eight `NORMATIVE_ROOTS` other than `14-ai-development` shall recognise root-level side-by-side bilingual files as a legitimate pairing.

Policy definition (key points):

- normative Markdown may use either shape: root `X.md` + `X.zh-CN.md`; or root prose + `docs/en`/`docs/zh-CN` mirrors;
- a side-by-side pairing must be an **exact match: same directory, same prose stem**; a file that merely contains `.zh-CN` does not count;
- one-sided language coverage is not allowed;
- existing exemption rules keep applying, but must not be widened;
- **the two shapes are acceptable alternatives, not a double obligation.**

One reason given maps exactly onto §2: the current gate has effectively made "which directory the file is in" a stronger condition than "is the bilingual prose present", **which induces contributors to accommodate the scanner instead of following a clear documentation convention.**

### 6.2 The ruling also flags an error here, and asks for evidence

> Your table says `X.md + X.zh-CN.md` under `14-ai-development` **still needs docs mirrors**, but section 3 says side-by-side works only for `14-ai-development`. Both cannot be accurate descriptions of the mechanism.

**The Owner is right and I was wrong.** §1.2 is corrected with measurement: side-by-side is ineffective for all nine roots (T1–T4, +2 gaps each). `counterpart_14`'s real scope is the **changed-path gate**, not the gap scan; in the gap scan it is only an extra veto and never replaces the existence check on both `docs/` sides.

### 6.3 Policy settled, implementation not authorised

The ruling states plainly: **approving a policy direction is not approving an unreviewed code change.** Adjusting `resolved_14` touches gate decision logic and must go through independent review. Implementation must demonstrate at least six things:

| # | Must demonstrate |
|---|---|
| 1 | side-by-side pairing recognised for all eight roots |
| 2 | a one-sided file missing `.zh-CN.md` is still a gap |
| 3 | near-identical filenames with different stems do not mis-pair |
| 4 | existing `docs/en` + `docs/zh-CN` mirrors still pass |
| 5 | `PAIR_EXEMPT_PREFIXES` behaviour is neither widened nor broken |
| 6 | `14-ai-development` behaviour has no unintended regression |

### 6.4 Disposition of the four failing PRs

The ruling: **the four PRs must not be required to migrate directories or duplicate mirrors to work around this.** Once the gate policy change passes independent review and lands, re-run the gate at each PR's exact head.

**This policy ruling must not be recorded as the four PRs having passed.**

### 6.5 State

| Item | State |
|---|---|
| side-by-side pairing policy | **APPROVED** |
| gate implementation change | `INDEPENDENT_REVIEW_REQUIRED` (not authorised to merge) |
| #425 / #433 / #435 / #436 | `BLOCKED_BY_GATE_POLICY` (not content errors) |
| #428 / #430 / #429 / #434 / #444 | `LOCAL_VERIFIED` (gate shape check, not acceptance) |
| the §1.2 correction | measurement supplied (T1–T4) |

### 6.6 One thing still unresolved

Ruling A recognises side-by-side pairing, but **side-by-side and "root + `docs/` mirror" are not semantically equivalent** in one respect:

- with `docs/` mirrors, `docs/en/` and `docs/zh-CN/` are two independent files that can carry different languages;
- with side-by-side, `X.md` and `X.zh-CN.md` are also two independent files that can;
- but **the gate cannot tell whether the two files are really one Chinese and one English.** 006 §13.3 already has a counter-example: I once shipped an 18-file version whose `docs/en/` held Chinese, and the gate returned `EXIT=0`.

So ruling A fixes "the shape is not recognised". It does **not** fix "the shape is recognised but the content does not correspond". The latter needs independent review, and that seat is still `NOT_ASSIGNED`.
