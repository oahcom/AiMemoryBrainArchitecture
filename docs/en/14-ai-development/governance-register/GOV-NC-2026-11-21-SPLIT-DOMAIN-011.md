# GOV-NC-2026-11-21-SPLIT-DOMAIN-011 — Side-by-side pairing implemented only in the gap-scan domain: the diff domain still demands a mirror, so five real pairs cannot be edited on main

## 0. Status and conclusion

```
MEASUREMENT_ONLY / NO_IMPLEMENTATION / REQUIRES_INDEPENDENT_REVIEW
```

This document records a set of measurements reproduced on a real clone against real git history. It proposes no implementation and authorises no merge.

**One-sentence conclusion**: on main `cb04524`, `current_bilingual_gaps()` (the gap-scan domain) recognises side-by-side pairing, and `check_normative_pairing()` (the diff domain) **does not**. The two domains return opposite verdicts for the same change. The consequence is that **five real side-by-side pairs in the repository** return `EXIT=1` when edited, and there is **no legal way to pass**.

## 0.1 This document contains a self-correction

In an earlier round I concluded that "PR #470 wrote the GitHub API JSON response body into `scripts/bilingual-baseline.txt`". **That conclusion was wrong and is withdrawn.**

The cause was my measurement harness: `GET /repos/{r}/git/blobs/{sha}` returns a wrapper `{"sha":...,"content":"<base64>","encoding":"base64"}`, and my `fetch_blob()` wrote that wrapper to disk verbatim, so every "downloaded" file was JSON. With correct decoding, #470's baseline is a legitimate 80-entry plain-text file.

**Why this correction matters**: it shows that conclusions in this series must state their decoding method. Every conclusion from §2 onward was re-run with the corrected harness.

## 1. Current state (main `cb04524`, measured)

### 1.1 Code locations of the two domains

| Domain | Function | Recognises side-by-side? |
|---|---|---|
| Gap scan (whole tree) | `current_bilingual_gaps()` | **yes** (merged in #462) |
| Diff judgement (this PR's changes) | `check_normative_pairing()` | **no** |

`check_normative_pairing()` lines 730–732 **unconditionally** require, for every non-`14-ai-development` normative source:

```python
en = f"docs/en/{source}"
zh = f"docs/zh-CN/{source}"
errors.extend(check_counterpart_requirement(source, [en, zh], changed, statuses, exception))
```

It never calls `side_by_side_partner()`. `current_bilingual_gaps()` does.

### 1.2 Consequence: all real pairs cannot be edited

On main, editing **both sides** of a pair that already exists returns:

| Pair | Root | `EXIT` | Error type |
|---|---|---|---|
| `02-domain-model/phase-2-domain-extension` | `02-domain-model` | **1** | `PAIR` ×2 |
| `06-memory-context/context-implementation-coverage` | `06-memory-context` | **1** | `PAIR` ×2 |
| `06-memory-context/phase-3.8.22-...-contract` | `06-memory-context` | **1** | `PAIR` ×2 |
| `07-agent-integration/adapter-capability-tiers` | `07-agent-integration` | **1** | `PAIR` ×2 |
| `08-bmcp-protocol/protocol-index` | `08-bmcp-protocol` | **1** | `PAIR` ×2 |

Typical diagnostic:

```
::error::02-domain-model/phase-2-domain-extension.md requires all counterparts changed in this PR:
  02-domain-model/phase-2-domain-extension.md, docs/en/02-domain-model/phase-2-domain-extension.md,
  docs/zh-CN/02-domain-model/phase-2-domain-extension.md
```

**Both sides changed, still failing** — because what is required is the two `docs/` mirrors, which under policy this pair is not supposed to have.

### 1.3 Adding a new side-by-side pair fails too

| Case | `EXIT` |
|---|---|
| `02-domain-model/p.md` + `p.zh-CN.md` (new) | **1** |
| `02-domain-model/q.en.md` + `q.zh-CN.md` (new) | **1** |
| `13-engineering-decisions/p.md` + `p.zh-CN.md` (new) | **1** |

Controls (showing this is not "all new files fail"):

| Control | `EXIT` |
|---|---|
| `02-domain-model/m.md` + `docs/en/m.md` + `docs/zh-CN/m.md` (mirror triple) | **0** |
| `14-ai-development/s.md` + `s.zh-CN.md` (**14 root** side-by-side) | **0** |
| `02-domain-model/r.md` alone (no partner) | **2** (`GAP`, correct) |

**`14-ai-development` passes, the other eight roots fail** — a direct consequence of the `if source.startswith("14-ai-development/")` branch in `check_normative_pairing()`.

## 2. The deadlock has no legal exit (measured case by case)

The `exception` parameter of `check_counterpart_requirement()` is the only exit, and it is true only when the PR body carries a **complete seven-field** `BILINGUAL-EXCEPTION: APPROVED`:

| Attempt | `EXIT` | Note |
|---|---|---|
| `BILINGUAL-EXCEPTION: APPROVED` plus a self-written reason | **1** | seven fields incomplete |
| All seven fields (`Exception Owner` / `Authoritative language/version` / `Missing counterpart path` / `Exact source revision` / `Due date` / `Tracking Issue/PR` / `Approval evidence`) | **0** | **the only workable path** |

**This means** every edit to a side-by-side pair must fabricate a "missing mirror" exception to pass. Under policy the pair is missing nothing — requiring an exception for a non-existent absence registers the correct practice as a defect.

The gate also prints:

```
Approved bilingual exception declaration detected; human governance approval remains mandatory.
```

So `EXIT=0` means only **syntactically complete**, not that the exception was approved.

## 3. This is not what the spec predicted — it is the spec being bypassed

`SPEC-2026-11-21-PAIRING-001.md` §4.1 explicitly requires **both criteria to change**, and §4.5.2c provides measured evidence: with only the gap scan changed, #433/#435/#436 still return `EXIT=1`.

The #462 that merged into main **changed only the gap scan**. Its own PR body reports N3/N4 as "ACCEPT, rc=0", but that is the **no-op form** (`BASE_SHA == HEAD_SHA`). Re-running the same cases in real PR-diff form (`BASE_SHA = HEAD~1`):

```
PR462 head 7de3111    no-op rc=0 | diff rc=1
main after 462        no-op rc=0 | diff rc=1
origin/main           no-op rc=0 | diff rc=1
```

**N3/N4's ACCEPT holds only on an empty diff.** This does not mean #462's author acted in bad faith — no-op is the repository's established verification form (`NOOP_RC`); it simply cannot cover the diff domain.

## 4. Incidental finding: a mirror-shape regression

The new predicate in `current_bilingual_gaps()`:

```python
paired = mirrored or side_by_side_partner(source) is not None or (english.is_file() and _carries_chinese(source))
```

The third branch, `english.is_file() and _carries_chinese(source)`, **no longer requires `chinese.is_file()`**. It used to apply only to `14-ai-development` (Shape 3); it now applies to all nine roots.

Measured consequence:

| Case | `0ca4d93` (118 baseline) | main `cb04524` (80 baseline) |
|---|---|---|
| `02-domain-model/hm.md` (Chinese) + `docs/en/hm.md` (English), **no `docs/zh-CN`** | **GAP** (correct) | **accepted** (regression) |

That is: **a Chinese source plus an English mirror, missing the Chinese mirror**, is now judged paired. The entire `docs/zh-CN/` side may be absent.

## 5. Attribution of the baseline 118 → 80 (all 38 closed)

| Mechanism | Count | Note |
|---|---|---|
| Side-by-side (`14-ai-development`) | **29** | matches §4.5.2b-2 |
| Side-by-side (non-14 roots) | **1** | `07-agent-integration/adapter-capability-tiers.md` |
| Shape 3 widened from 14 root to all roots | **3** | `AI-EXEC-001.md`, `AI-EXEC-002.md`, `AI-EXEC-ROLLOUT-001.md` |
| Mirror actually added (#470 etc.) | **5** | `06-memory-context/README.md` + four `phase-3.6.x` |
| Unexplained | **0** | — |
| **Total** | **38** | |

Every step's baseline is self-consistent (`baseline == gaps`, `new=0`, `resolved=0`):

| Commit | baseline | gaps | new | resolved |
|---|---|---|---|---|
| `0ca4d93` | 118 | 118 | 0 | 0 |
| `e6db42f` | 86 | 86 | 0 | 0 |
| `7de3111` | 85 | 85 | 0 | 0 |
| `704a712` | 80 | 80 | 0 | 0 |
| `cb04524` | 80 | 80 | 0 | 0 |

**Note**: `29 + 1 + 3 + 5 = 38`, while the spec predicted 29. The 9-entry difference is 1 (non-14 side-by-side) + 3 (Shape 3 widened) + 5 (mirror added). **The spec predicted only the 29 side-by-side entries; the other 9 come from two changes the spec did not recommend.**

## 6. The uniqueness rule was not adopted (counter-example to spec §4.5.2)

main's `side_by_side_partner()` is **return on first match**, with no uniqueness check:

```python
elif source.endswith(".md"):
    stem = source[: -len(".md")]
    for cand in (stem + ".en.md", stem + ".zh-CN.md"):
        if cand != source and (ROOT / cand).is_file():
            return cand
```

Measured with three files present (`X.md` + `X.en.md` + `X.zh-CN.md`):

```
p(u1.md)       = u1.en.md
p(u1.en.md)    = u1.zh-CN.md
p(u1.zh-CN.md) = u1.en.md
```

`partner(partner(x)) != x` — the cycle recorded in spec §4.5.1 **still exists on main**, and all three files are judged paired (`gaps=0`).

English masquerading as Chinese is also accepted:

| Case | Result |
|---|---|
| `fake.md` (English) + `fake.zh-CN.md` (English) | neither is **in** gaps |

So a `.zh-CN.md` suffix plus an English body passes. This is what #468 tries to fix, **not yet merged**.

## 7. #468 does not fix this document's main defect (measured)

`#468` (`fix(bilingual): reject side-by-side pairs without Chinese content`) changes only the gap-scan content validation. Re-run on main + #468 overlay:

| Case | main | main + #468 |
|---|---|---|
| Edit both sides of `02-domain-model/phase-2-domain-extension` | `EXIT=1` `PAIR`×2 | **`EXIT=1` `PAIR`×2** |
| Edit both sides of `08-bmcp-protocol/protocol-index` | `EXIT=1` `PAIR`×2 | **`EXIT=1` `PAIR`×2** |
| Add `02-domain-model/newpair.md` + `.zh-CN.md` | `EXIT=1` `PAIR`×2 | **`EXIT=1` `PAIR`×2** |

**The deadlock persists after #468 merges.** It fixes "fake Chinese", not "the two domains disagree".

## 8. Impact surface

| Item | Status |
|---|---|
| Editable side-by-side pairs (non-14 roots) | **0** (all five return `EXIT=1`) |
| Adding a side-by-side pair (non-14 roots) | **impossible** (`EXIT=1`) |
| Legal bypass | only a seven-field exception declaration (registers correct practice as a defect) |
| Missing `docs/zh-CN` side | silently accepted (§4 regression) |
| Three-file ambiguity | silently accepted (§6) |
| English masquerading as `.zh-CN.md` | silently accepted (§6) |

## 9. What this document does not claim

- It does not claim #462's author had deceptive intent. No-op is the repository's established verification form.
- It does not claim main is currently "red". `baseline == gaps` holds at every step, so **an empty diff is always `EXIT=0`**. The defect appears only **when a side-by-side pair is changed**.
- It proposes no fix. It registers measurements only.
- It does not claim §4's regression is solely caused by #462; it may be a deliberate side effect of widening Shape 3. **The Owner must rule on the policy intent.**

## 10. Matters requiring a ruling

| ID | Matter | Who |
|---|---|---|
| Q-1 | Does the side-by-side policy apply to **non-14 roots** (policy says yes; code implements half) | Owner confirms the code must be completed |
| Q-2 | Is accepting a missing `docs/zh-CN` (§4) a **deliberate relaxation** or a **side effect** | Owner |
| Q-3 | Are three-file ambiguity and English-as-Chinese (§6) resolved once #468 merges | independent reviewer |
| Q-4 | Is the seven-field exception the **intended** pass path for side-by-side pairs | Owner (if not, there is currently no legal path) |

## 11. Reproduction

Environment: real clone, `origin/main` = `cb04524`, Python 3.13, no CI.

```bash
git clone https://github.com/oahcom/AiMemoryBrainArchitecture.git
cd AiMemoryBrainArchitecture
git checkout cb04524

# edit both sides of a real side-by-side pair
printf '\n<!-- t -->\n' >> 02-domain-model/phase-2-domain-extension.md
printf '\n<!-- t -->\n' >> 02-domain-model/phase-2-domain-extension.zh-CN.md
git commit -qam probe

BASE_SHA=HEAD~1 HEAD_SHA=$(git rev-parse HEAD) \
  PR_BODY='BILINGUAL-MANIFEST: COMPLETE' \
  python3 scripts/check_bilingual_docs.py
# -> EXIT=1, 2 x "requires all counterparts changed in this PR"

# control: empty diff
BASE_SHA=$(git rev-parse HEAD) HEAD_SHA=$(git rev-parse HEAD) \
  PR_BODY='BILINGUAL-MANIFEST: COMPLETE' \
  python3 scripts/check_bilingual_docs.py
# -> EXIT=0
```

**The key to reproducing is that `BASE_SHA` must be the real parent commit.** Using `BASE_SHA == HEAD_SHA` yields `EXIT=0` and hides the defect — which is exactly the #462 verification-form problem recorded in §3.

## 12. Status

```
SPLIT_DOMAIN_CONFIRMED / DEADLOCK_NO_LEGAL_EXIT / MIRROR_REGRESSION_OBSERVED
INDEPENDENT_REVIEW: NOT_ASSIGNED
IMPLEMENTATION_AUTHORISATION: NOT_AUTHORISED
```
