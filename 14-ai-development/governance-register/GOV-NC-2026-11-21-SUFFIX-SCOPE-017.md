# GOV-NC-2026-11-21-SUFFIX-SCOPE-017

**Status:** OPEN — MEASUREMENT ONLY
**Nature:** `REGISTER_ONLY / NO_IMPLEMENTATION / NO_GATE_CHANGE / REQUIRES_INDEPENDENT_REVIEW`
**Measured at:** `main = d647e7d5ef`
**Extends:** `...-SPLIT-DOMAIN-011.md`, `...-PAIRING-RESIDUAL-013.md`, `...-CWD-SPLIT-014.md`, `...-EMBEDDED-ROOT-015.md`
**Register author:** strategic requirement orchestrator session. **Not** an independent reviewer, **not** the accountable owner.

---

## 0. The finding

`PAIR_ENFORCED_SUFFIXES = {".md"}` exists to limit the pairing requirement to Markdown. It is applied **inside the `14-ai-development` branch only**:

```python
for source in normative_changes:
    if source in EMBEDDED_BILINGUAL_SOURCES:      continue
    if source.startswith(PAIR_EXEMPT_PREFIXES):    continue
    if source.startswith("14-ai-development/"):
        if Path(source).suffix.lower() not in PAIR_ENFORCED_SUFFIXES:
            continue                               # <-- suffix filter lives HERE
        partner = counterpart_14(source)
        ...
        continue
    en = f"docs/en/{source}"                       # <-- no suffix filter
    zh = f"docs/zh-CN/{source}"
    errors.extend(check_counterpart_requirement(source, [en, zh], changed, statuses, exception))
```

Every source outside `14-ai-development` reaches the mirror branch with **no suffix check at all**. Any file type in a normative root therefore demands `docs/en/` **and** `docs/zh-CN/` counterparts.

Measured consequence on PR #500 (`6a7cafdb`, 77 files):

```
EXIT=1   errors=41   all 41 classified PAIR
08-bmcp-protocol/schemas/bmcp.applied-ack-1.1.0-jf10-bridge.schema.json requires all counterparts changed
08-bmcp-protocol/schemas/bmcp.applied-ack-1.1.1-jf10-prepared-gid.schema.json requires all counterparts changed
08-bmcp-protocol/schemas/bmcp.coc-jf10-unified-1.2.0.schema.json requires all counterparts changed
...
```

All 41 errors are `.json`:

```
by extension: {'json': 41}
```

A JSON schema cannot carry a Chinese translation of itself as Markdown, and translating a machine-readable schema into `docs/zh-CN/` would break its own consumers. The requirement is not strict — it is unsatisfiable as written.

---

## 1. This is a distinct defect from 011

Register 011 said: the diff domain demands mirrors where the gap scan accepts side-by-side. That was about **which shape** counts.

This is about **which file types** are subject to the rule at all. `PAIR_ENFORCED_SUFFIXES` already encodes the correct policy; it is simply unreachable for eight of the nine roots.

| Register | Question | Answer |
|---|---|---|
| 011 | does a side-by-side pair satisfy the diff domain? | no — mirrors required |
| 017 | does a `.json` file require a bilingual counterpart? | yes, outside the 14 root — and it cannot have one |

## 2. The PR matrix that exposed it

All nine open PRs, each overlaid on `main = d647e7d5ef` at its exact head, `PR_BODY` = the PR's real body:

| PR | head | gate | errors | class | touches `scripts/`/`crates/` |
|---|---|---|---|---|---|
| #509 | `78d61766` | **PASS** | 0 | — | yes |
| #507 | `c8f496ae` | FAIL | 1 -> **1** after manifest | manifest, then **011** | yes |
| #505 | `75e3b9e2` | FAIL | 1 -> **2** after manifest | manifest, then **017 x2** | no |
| #504 | `a608df27` | **PASS** | 0 | — | yes |
| #500 | `6a7cafdb` | **FAIL** | **41** | **PAIR ×41, all `.json`** | no |
| #496 | `4495b314` | **PASS** | 0 | — | no |
| #494 | `c572c946` | **PASS** | 0 | — | no |
| #471 | `d33ee2bb` | FAIL | 1 -> **0** after manifest | manifest only | yes |
| #433 | `81558c89` | **PASS** | 0 | — | yes |

5 pass, 4 fail. After supplying the missing manifest: **6 pass, 3 fail** — and all 3 remaining failures are gate defects (011 or 017), not author defects.

### 2.1 The manifest error is only the first error, not the only error

`#507`, `#505`, `#471` all fail first with:

```
Normative source files changed but PR body lacks 'BILINGUAL-MANIFEST: COMPLETE'
or a fully documented 'BILINGUAL-EXCEPTION: APPROVED' block
```

**I initially recorded this as the whole story and that was wrong.** Re-running each PR twice — once with its real body, once with `BILINGUAL-MANIFEST: COMPLETE` appended — separates manifest failures from structural ones:

| PR | real body | body + `BILINGUAL-MANIFEST: COMPLETE` |
|---|---|---|
| `#471` | `EXIT=1` (manifest) | **`EXIT=0`** — manifest was the only problem |
| `#507` | `EXIT=1` (manifest) | **`EXIT=1`** — `02-domain-model/domain-model-overview.md requires all counterparts changed` |
| `#505` | `EXIT=1` (manifest) | **`EXIT=1`** — `08-bmcp-protocol/schemas/bmcp.applied-delivery-evidence-1.0.0.schema.json requires all counterparts changed` (x2) |

So of the three, **only `#471` is a pure manifest failure.** The other two have a structural error underneath, and the manifest error was masking it because the gate returns early.

### 2.2 Three PRs are structurally blocked, and all three are the same two defects

| PR | blocking file | defect |
|---|---|---|
| `#500` | 41 × `08-bmcp-protocol/schemas/*.schema.json` | **017** — `.json` subject to pairing |
| `#505` | 2 × `08-bmcp-protocol/schemas/*.schema.json` | **017** — same |
| `#507` | `02-domain-model/domain-model-overview.md` | **011** — `.md` without mirrors in a non-14 root |

`#507`'s file list is instructive:

```
modified 02-domain-model/domain-model-overview.md        <- no partner, blocked by 011
modified 02-domain-model/phase-2-domain-extension.md     <- has .zh-CN.md partner, ALSO blocked by 011
modified 02-domain-model/phase-2-domain-extension.zh-CN.md
modified crates/memory-domain/src/lib.rs
```

It **did** pair `phase-2-domain-extension` correctly — both sides in the same PR — and is still rejected, because the diff domain wants `docs/en` + `docs/zh-CN`, not the side-by-side pair. That is register 011's exact claim, now with a live PR as its witness.

`#505`'s file list shows the author doing the right thing twice over:

```
added    08-bmcp-protocol/schema-nonempty-audit.md        <- correct .md + .zh-CN.md pair
added    08-bmcp-protocol/schema-nonempty-audit.zh-CN.md
modified 08-bmcp-protocol/schemas/bmcp.applied-delivery-evidence-1.0.0.schema.json
modified 08-bmcp-protocol/schemas/bmcp.recovery-join-1.0.2.schema.json
added    08-bmcp-protocol/schemas/test_nonempty_audit.py
```

The `.md` pair is satisfied. The two `.json` edits are not, and cannot be.

### 2.3 #494 passes

`#494` — the register branch carrying 011/012/013/014/015/016 — passes at its own exact head with 35 changed paths inspected, baseline 77 frozen. The governance documents it adds are all `.md` and all mirrored, so they do not hit the suffix problem.

---

## 3. Why `PAIR_ENFORCED_SUFFIXES` is unreachable, not wrong

The constant is correct and was presumably added when someone hit exactly this problem inside `14-ai-development`. The 14 root contains `.png`, `.drawio`, `.yaml`, `.json` and the filter skips them.

The other eight roots never got the filter, because they were never given a `counterpart_14()`-style resolution path at all — they got the blanket two-mirror rule. So the suffix policy was written once, for one root, and the blanket branch was written without it.

This is the same structural pattern as register 015: a rule that exists, is correct, and is scoped to one root by a hard-coded prefix.

---

## 4. Relationship to the other four registers

| # | Defect | Root scope | File-type scope | CI impact |
|---|---|---|---|---|
| 011 | side-by-side rejected in diff domain | 8 of 9 roots | `.md` only (in practice) | blocks 5 real pairs |
| 013 | 1-CJK / 0-byte partner accepted | 9 of 9 | `.md` only | accepts empty translations |
| 014 | `ROOT = cwd` vs `REPO_ROOT` | global | all | local only |
| 015 | embedded bilingual only in 14 root | 8 of 9 roots | `.md` only | 58 of 77 baseline entries |
| **017** | **suffix filter only in 14 root** | **8 of 9 roots** | **all types** | **blocks #500, 41 errors** |

Five defects, all produced by the same design decision: one root (`14-ai-development`) got a bespoke resolution path, and the other eight got a blanket rule that ignores every refinement the bespoke path accumulated — suffix filtering (017), embedded-bilingual recognition (015), and side-by-side acceptance (011).

**That is the single sentence this whole series reduces to.** It is not five unrelated bugs. It is one root being special-cased, and every special case being withheld from the other eight.

---

## 5. What would have to be true for this to be a non-issue

1. JSON schemas are meant to have `docs/zh-CN/` Markdown translations of their field descriptions. → then `docs/zh-CN/08-bmcp-protocol/schemas/` should exist for the current 40+ schemas and does not; check whether any exist today.
2. `08-bmcp-protocol/schemas/` is meant to be outside the normative scan entirely. → then `NORMATIVE_ROOTS` or a new exempt prefix should say so.
3. The suffix filter is meant to be root-agnostic. → then 41 errors on #500 are a gate bug.

I checked (1) partially: `docs/zh-CN/08-bmcp-protocol/` exists but I did not find a `schemas/` subtree in it. Whether that is because nobody tried or because the policy forbids it, I cannot tell from the repository.

---

## 6. Reproduction

```
repo:    oahcom/AiMemoryBrainArchitecture
base:    main = d647e7d5ef
PR:      #500 head 6a7cafdb (77 files)

# overlay #500's files on main, commit, then:
BASE_SHA=<main> HEAD_SHA=<overlay> PR_BODY='<#500 body>' \
  python scripts/check_bilingual_docs.py
-> EXIT=1, 41 errors, every one of the form
   "08-bmcp-protocol/schemas/*.json requires all counterparts changed in this PR:
    08-bmcp-protocol/schemas/*.json, docs/en/08-bmcp-protocol/schemas/*.json,
    docs/zh-CN/08-bmcp-protocol/schemas/*.json"

# the constant
grep -n 'PAIR_ENFORCED_SUFFIXES' scripts/check_bilingual_docs.py
-> 40:PAIR_ENFORCED_SUFFIXES = {".md"}
-> 892:            if Path(source).suffix.lower() not in PAIR_ENFORCED_SUFFIXES:   # inside the 14 branch
```

No CI, no API quota beyond reading the PR.

---

## 7. What this register does not claim

- It does not claim #500 should be merged. Its 41 errors are structural, not its only problem.
- It does not claim JSON schemas need no bilingual treatment. It claims they cannot get the treatment the gate demands.
- It does not propose moving the suffix check. That is a gate change requiring authorisation.
- It does not verify whether `docs/zh-CN/08-bmcp-protocol/schemas/` has ever existed in git history.
- It does not assign an independent review seat. That seat remains `NOT_ASSIGNED`.

**Blocking chain unchanged:** independent review `NOT_ASSIGNED`, implementation authorisation `NOT_AUTHORISED`, sponsor / accountable owner `NOT_ASSIGNED`.
