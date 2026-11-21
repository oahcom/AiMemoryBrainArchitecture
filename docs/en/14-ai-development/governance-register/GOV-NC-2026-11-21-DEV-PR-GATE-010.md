# GOV-NC-2026-11-21-DEV-PR-GATE-010 — Four of nine development PRs cannot pass the gate, all for the same reason

## 0. Summary

Following Owner ruling D (development continues; first make one compliant path actually work), I applied each of the nine development PRs' exact heads onto current main (`c138654c94`) and ran the bilingual gate on **real git history**.

Result:

**4 fail / 5 pass. All four failures share one cause, and none of them is "the PR content is wrong".**

More important: the five that pass fall into four different shapes, and the four that fail are all one shape. **The gate is effectively judging "which directory did you put the file in", not "is the bilingual pairing complete".**

| PR | Workstream | Shape | Gate | Cause |
|---|---|---|---|---|
| #430 | Agent Integration | root + `docs/en` + `docs/zh-CN` | **PASS** | both `docs/` sides exist |
| #428 | BMCP | `reviews/…/X.en.md` + `.zh-CN.md` | **PASS** | `reviews/` is **not** under `NORMATIVE_ROOTS` |
| #429 | Memory Compiler arch | edits **existing** `docs/en` + `docs/zh-CN` pairs | **PASS** | both sides changed together |
| #434 | Memory Context tests | `crates/` only | **PASS** | gate scans `*.md` under `NORMATIVE_ROOTS` only |
| #444 | Memory Context e2e | `crates/` only | **PASS** | same |
| #425 | Memory Compiler | root `X.md` + `X.zh-CN.md` | **FAIL** | no `docs/` mirror |
| #433 | Memory Context | root `X.md` + `X.zh-CN.md` | **FAIL** | same |
| #435 | Phase 2 domain model | root `X.md` + `X.zh-CN.md` | **FAIL** | same |
| #436 | BMCP | root `X.md` + `X.zh-CN.md` | **FAIL** | same |

Correction record: #429 first measured `EXIT=1` because my harness silently skipped one file on `URLError`, producing a phantom missing counterpart. With the file fetched it is `EXIT=0`. That was my harness defect, not a PR defect.

## 1. This is not "some PRs are written badly"

### 1.1 Four positions, four different constraints

1. write under `crates/` -> unconstrained (code and tests)
2. write under `reviews/` -> unconstrained (not in the root list)
3. write into existing `docs/` pairs -> constrained but satisfied
4. write into a `NORMATIVE_ROOTS` root with side-by-side bilingual -> **constrained and unsatisfied**

All four failures are case 4.

### 1.2 The mechanism

```python
english = REPO_ROOT / "docs" / "en" / source
chinese = REPO_ROOT / "docs" / "zh-CN" / source
if not english.is_file() or not chinese.is_file() or resolved_14 is None:
    gaps.add(source)
```

and

```python
resolved_14 = counterpart_14(source) if root_name == "14-ai-development" else True
```

**`counterpart_14` only applies to `14-ai-development`.** For the other eight roots — `00-governance`, `01-system-architecture`, `02-domain-model`, `04-memory-compiler`, `06-memory-context`, `07-agent-integration`, `08-bmcp-protocol`, `13-engineering-decisions` — `resolved_14` is always `True` and side-by-side naming plays no part at all. Only the two `docs/` directories count.

| Shape | the other eight roots | 14-ai-development |
|---|---|---|
| `X.md` + `X.zh-CN.md` side by side | **gap** | needs `docs/` mirror too |
| `X.md` + `X.en.md` side by side | **gap** | `resolved_14` passes, still needs `docs/` mirror |
| root + `docs/en` + `docs/zh-CN` | pass | pass |
| only `docs/en` + `docs/zh-CN` (no root) | pass | pass |

**Side-by-side bilingual works only for `14-ai-development`. For the other eight roots it does nothing.**

### 1.3 So the four failing PRs face one choice

**(a) add `docs/en` + `docs/zh-CN` mirrors** — the same prose then exists three times (root / `docs/en` / `docs/zh-CN`), which is exactly the duplication the Owner's #318 boundary forbids;

**(b) delete the root file, keep only `docs/en` + `docs/zh-CN`** — but that breaks the repository's existing convention and leaves `04-memory-compiler/` with a shape no other root uses;

**(c) enter `EMBEDDED_BILINGUAL_SOURCES`** — needs case-by-case governance approval, and the Owner has said explicitly it must not become the default channel.

**All three cost something. None is "just tweak the PR".**

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

**First, code and tests are entirely outside the bilingual gate.** It scans only `*.md` under `NORMATIVE_ROOTS`. So continued progress produces more implementation while the specs that explain it wait outside the door. #433 versus #434/#444 is that bias in a single sample.

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
```

## 5. What this register does not claim

- It does not claim the four PRs should be closed. Their content is fine; their **shape** is not accepted.
- It does not claim the gate should be relaxed. The rule in §1.2 is reasonable in principle (a spec must be findable in both languages); the problem is that it recognises one shape only for eight of nine roots.
- It does not claim I have solved this. I only measured it.
- It does not count #444's local failure as a PR defect (§3).

## 6. One decision is needed

Four of nine PRs are stuck on the same shape question. This is not nine independent judgements, it is **one judgement**:

> For the eight `NORMATIVE_ROOTS` other than `14-ai-development`, should side-by-side `.zh-CN.md` count as a valid counterpart?

- **If yes**: widen `resolved_14`'s scope. One-line change, all four PRs unblocked. But that is a normative change and needs independent review.
- **If no**: then every existing side-by-side file in the repository is legacy, all new files must use `docs/` mirrors, and the root-prose convention is being phased out. That has to be stated, otherwise every new PR hits this once.

**Both options need an Owner ruling. I do not choose on its behalf.**
