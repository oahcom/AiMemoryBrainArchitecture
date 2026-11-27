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
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-23"
      last_verification_note: "§8's conclusions were measured on 2026-11-23 at main f39dfb7b: 0 of 384 normative_changes candidates are non-.md; reverting the one line from 717dfbf0 reproduces §0's error on a clean worktree; the suite is 52 green at 9944d07e and 24 problems at 8ab40fb4. All run in this session, not quoted."
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
    source: "14-ai-development/governance-register/GOV-NC-2026-11-21-SUFFIX-SCOPE-017.md"
    en: null
    zh-CN: "docs/zh-CN/14-ai-development/governance-register/GOV-NC-2026-11-21-SUFFIX-SCOPE-017.md"
---

# GOV-NC-2026-11-21-SUFFIX-SCOPE-017

**Status:** `FIXED-CLOSED-BY-OTHER` — fixed in `717dfbf0` (#527) by a different route than §5 branch 3, behaviourally verified (see §8). Its three shipped tests are broken and no workflow runs them. Independent review remains `NOT_ASSIGNED`.
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
| #507 | `c8f496ae` | FAIL | 1 -> **1** after manifest | manifest, then **author omission** | yes |
| #505 | `75e3b9e2` | FAIL | 1 -> **2** after manifest | manifest, then **017 x2** | no |
| #504 | `a608df27` | **PASS** | 0 | — | yes |
| #500 | `6a7cafdb` | **FAIL** | **41** | **PAIR x41, all `.json` (017)** | no |
| #496 | `4495b314` | **PASS** | 0 | — | no |
| #494 | `c572c946` | **PASS** | 0 | — | no |
| #471 | `d33ee2bb` | FAIL | 1 -> **0** after manifest | manifest only | yes |
| #433 | `81558c89` | **PASS** | 0 | — | yes |

5 pass, 4 fail. After supplying the missing manifest: **6 pass, 3 fail** — of which **2 are gate defects** (`#500`, `#505`, both 017) and **1 is a legitimate author omission** (`#507`, mirrors not updated).

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

### 2.2 Three PRs are structurally blocked, and only two are the gate's fault

| PR | blocking file | verdict |
|---|---|---|
| `#500` | 41 x `08-bmcp-protocol/schemas/*.schema.json` | **017** — `.json` subject to pairing |
| `#505` | 2 x `08-bmcp-protocol/schemas/*.schema.json` | **017** — same |
| `#507` | `02-domain-model/domain-model-overview.md` | **NOT a defect** — see §2.2a |

### 2.2a #507's error is legitimate, and I got it wrong first

`#507` fails after the manifest with:

```
02-domain-model/domain-model-overview.md requires all counterparts changed in this PR
```

I first attributed this to register 011. **That was wrong.** On main, `domain-model-overview.md` **already has both mirrors**:

```
02-domain-model/domain-model-overview.md            27542 bytes
docs/en/02-domain-model/domain-model-overview.md    29109 bytes
docs/zh-CN/02-domain-model/domain-model-overview.md 26231 bytes
```

So the file is a full mirror triple, the diff domain's requirement is satisfiable, and `#507` simply edited the source without updating the two mirrors. **That is a real pairing omission by the author, and the gate is right to reject it.**

The distinction matters: register 011's claim is that a correct side-by-side pair is rejected. `#507` is the opposite case — a file that has mirrors, edited without them. Conflating the two would have inflated 011's evidence with a case that does not support it.

`#507`'s other file, `phase-2-domain-extension.md`, genuinely has no mirrors and is a genuine 011 case. But the PR fails on `domain-model-overview.md` regardless, so `#507` cannot serve as 011's witness. Register 011's witness remains the five pairs measured directly in 013 §2.1.

### 2.3 #505 shows the author doing it right and still failing

`#505`'s file list:

```
added    08-bmcp-protocol/schema-nonempty-audit.md        <- correct .md + .zh-CN.md pair
added    08-bmcp-protocol/schema-nonempty-audit.zh-CN.md
modified 08-bmcp-protocol/schemas/bmcp.applied-delivery-evidence-1.0.0.schema.json
modified 08-bmcp-protocol/schemas/bmcp.recovery-join-1.0.2.schema.json
added    08-bmcp-protocol/schemas/test_nonempty_audit.py
```

The `.md` pair is satisfied. The two `.json` edits are not, and cannot be. That is 017 in one file list.

### 2.4 #494 passes

`#494` — the register branch carrying 011/012/013/014/015/016 — passes at its own exact head with 41 changed paths inspected, baseline 77 frozen. The governance documents it adds are all `.md` and all mirrored, so they do not hit the suffix problem.

---

## 3. Why `PAIR_ENFORCED_SUFFIXES` is unreachable, not wrong

The constant is correct and was presumably added when someone hit exactly this problem inside `14-ai-development`. The 14 root contains `.png`, `.drawio`, `.yaml`, `.json` and the filter skips them.

The other eight roots never got the filter, because they were never given a `counterpart_14()`-style resolution path at all — they got the blanket two-mirror rule. So the suffix policy was written once, for one root, and the blanket branch was written without it.

This is the same structural pattern as register 015: a rule that exists, is correct, and is scoped to one root by a hard-coded prefix.

**Measured exposure:** non-`.md` files inside normative roots, which would all be blocked if touched:

```
00-governance              2
06-memory-context          2
08-bmcp-protocol          14
13-engineering-decisions   2
14-ai-development         47   (these are protected by the suffix filter)
```

`docs/zh-CN/` contains **zero** `.json` files. `docs/en/` contains **zero** `.json` files. `docs/zh-CN/08-bmcp-protocol/schemas/` does not exist. So for the 20 non-`.md` files outside the 14 root, the required counterparts have never existed and are not being created.

---

## 4. Relationship to the other four registers

| # | Defect | Root scope | File-type scope | CI impact |
|---|---|---|---|---|
| 011 | side-by-side rejected in diff domain | 8 of 9 roots | `.md` only (in practice) | blocks 5 real pairs |
| 013 | 1-CJK / 0-byte partner accepted | 9 of 9 | `.md` only | accepts empty translations |
| 014 | `ROOT = cwd` vs `REPO_ROOT` | global | all | local only |
| 015 | embedded bilingual only in 14 root | 8 of 9 roots | `.md` only | 58 of 77 baseline entries |
| **017** | **suffix filter only in 14 root** | **8 of 9 roots** | **all types** | **blocks #500 and #505** |

Five defects, all produced by the same design decision: one root (`14-ai-development`) got a bespoke resolution path, and the other eight got a blanket rule that ignores every refinement the bespoke path accumulated — suffix filtering (017), embedded-bilingual recognition (015), and side-by-side acceptance (011).

**That is the single sentence this whole series reduces to.** It is not five unrelated bugs. It is one root being special-cased, and every special case being withheld from the other eight.

---

## 5. What would have to be true for this to be a non-issue

1. JSON schemas are meant to have `docs/zh-CN/` Markdown translations of their field descriptions. -> then `docs/zh-CN/08-bmcp-protocol/schemas/` should exist for the current schemas and does not.
2. `08-bmcp-protocol/schemas/` is meant to be outside the normative scan entirely. -> then `NORMATIVE_ROOTS` or a new exempt prefix should say so.
3. The suffix filter is meant to be root-agnostic. -> then the errors on #500 and #505 are a gate bug.

I cannot distinguish these from the repository. What I can state: `docs/zh-CN/` has zero `.json` files today, so option 1 describes a state that has never existed.

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

# the manifest-vs-structural split
for body in "<real body>" "<real body>\n\nBILINGUAL-MANIFEST: COMPLETE"; do
  BASE_SHA=<main> HEAD_SHA=<overlay> PR_BODY="$body" python scripts/check_bilingual_docs.py
done
```

No CI, no API quota beyond reading the PR.

---

## 7. What this register does not claim

- It does not claim #500 should be merged. Its 41 errors are structural, not its only problem.
- It does not claim JSON schemas need no bilingual treatment. It claims they cannot get the treatment the gate demands.
- It does not claim #507 is gate-blocked. §2.2a corrects my own earlier claim on that PR.
- It does not propose moving the suffix check. That is a gate change requiring authorisation.
- It does not verify whether `docs/zh-CN/08-bmcp-protocol/schemas/` has ever existed in git history.
- It does not assign an independent review seat. That seat remains `NOT_ASSIGNED`.

**Blocking chain unchanged:** independent review `NOT_ASSIGNED`, implementation authorisation `NOT_AUTHORISED`, sponsor / accountable owner `NOT_ASSIGNED`.

---

## 8. Measured: the defect is fixed, by a different route than §5 branch 3 (2026-11-23)

The body of this register and its §2 PR matrix are **not changed**. Those figures were measured at `d647e7d5` and the record stands. What follows is measured on current `main`.

### 8.1 The fix landed 80 minutes before this register was measured

| Item | Value |
|---|---|
| Fix commit | `717dfbf0`, 2026-11-21 22:09:16 +0800, `fix(bilingual): stop treating data files as documents requiring counterparts` (PR #527) |
| This register's measurement point | `d647e7d5`, 2026-11-21 20:48:30 +0800 |
| This register committed | `d9c29a1c`, 2026-11-21 23:21:05 +0800 (PR #494) |
| Change | one line: `suffix in {".md",".yaml",".yml",".json",".toml",".proto"}` → `suffix == ".md"`, `+1 −1` |
| Shipped in the same commit | `scripts/governance/evidence/test_gate_normative_roots.py` `+71`, three tests |

The fix predates this register's commit by 72 minutes and its measurement point by 80. **The commit message does not mention 017**, and a repo-wide `grep SUFFIX-SCOPE-017` hits nothing outside this register — structurally the same as §2.2a's finding about #507: the evidence was all present, just never connected.

### 8.2 The fix is not §5 branch 3, and the difference is substantive

§5 branch 3 was "the suffix filter should be root-agnostic". **That diagnosis is correct** — §3's reasoning holds — but the fix does not move the filter. It narrows the **upstream** set to `.md` only:

```python
normative_changes = []
for path in sorted(changed):
    parts = Path(path).parts
    if len(parts) >= 2 and parts[0] in NORMATIVE_ROOTS:
        if Path(path).suffix.lower() in EXEMPT_SUFFIXES:
            continue
        if Path(path).suffix.lower() == ".md":      # <-- here, not line 1031
            normative_changes.append(path)
```

Consequence: `check_normative_pairing()` can never receive a non-`.md` file, so the `PAIR_ENFORCED_SUFFIXES` guard at line 1031 can never fire. Replaying `main`'s construction over all 552 tracked normative paths gives **384 candidates, 0 non-`.md`**.

`PAIR_ENFORCED_SUFFIXES = {".md"}` is still declared at line 41 and still read at line 1031, and is now a tautology. The code reads as "pairing is required only for Markdown"; what executes is "only Markdown gets here".

### 8.3 Behavioural verification: the broken state reproduces, so this is not a reading of the code

On a clean worktree at `origin/main`, changing one character in a `.json` schema:

| Tree state | Result |
|---|---|
| `main` as-is | `PASS (1 changed paths inspected)` |
| the one line from `717dfbf0` reverted | `FAIL` — `::error::08-bmcp-protocol/schemas/bmcp.applied-delivery-evidence-1.0.0.schema.json requires all counterparts changed in this PR: ..., docs/en/..., docs/zh-CN/...` |

That is exactly the error shape §0 records. The defect was real and the fix is real.

### 8.4 Cost: 167 files leave pairing, and 0 of them ever had a mirror

`.json` 59, `.py` 54, `.yaml` 47, `.mjs` 4, other 4. Non-`.md` files under `docs/en/` and `docs/zh-CN/`: **0**.

§5's judgement — that demanding a Markdown translation of a JSON schema is **unsatisfiable** — still holds after the fix; the fix changed "unsatisfiable" into "not checked". That is the right outcome. This section does not argue for reverting it.

What is not recorded is that `.py` (54) and `.json` (59) now share one exemption: a schema and a validator are not the same question when it comes to "does this need Chinese prose".

### 8.5 All three tests the fix shipped with are broken on `main`

The three tests added in `717dfbf0` (`test_schema_json_change_does_not_require_counterpart`, `test_markdown_still_requires_counterpart`, `test_governance_markdown_still_requires_counterpart`) all run through `_run_real_git_gate_for_change()`. They were green at `9944d07e` (#534, `sys.argv` patched) and broke at `8ab40fb4` — register 014's fix, which changed `changed_status()` from `cwd=ROOT` to `cwd=REPO_ROOT` while `load_gate()` still patches only `mod.ROOT`, never `mod.REPO_ROOT`.

And **no workflow runs this suite**: `grep -rn 'test_gate_normative_roots' .github/` returns nothing. So those three tests neither pass nor turn anything red.

The full measurement and timeline are in `GOV-NC-2026-11-23-UNREACHABLE-GUARD-030`.

### 8.6 Status

`OPEN` → `FIXED-CLOSED-BY-OTHER` — the defect was fixed by `717dfbf0` and behaviourally verified; the route differs from §5 branch 3 (§8.2); the three tests it shipped with are broken and unrun by CI (§8.5). Independent review remains `NOT_ASSIGNED`.

Not `CLOSED`: §6's blocking chain includes independent review, and a session that writes this measurement cannot supply independence for it; and §8.2 and §8.5 each leave an open item, both taken up by 030.
