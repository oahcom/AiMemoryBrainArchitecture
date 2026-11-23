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
      last_verified_date: "2026-11-23"
      last_verification_note: "Both §7 figures (77 and 120) were measured on 2026-11-23 in a clean worktree at origin/main: the baseline writes 77 as-is, and 120 when only line 170 is reverted to `ROOT = Path.cwd()`. The claim that both suites fail identically in the fixed and broken states was established by `diff`, not by inspection. The body of this file was byte-identical to the Chinese canonical before this change (md5 a0de7b67913b48f4ed5409804d50771e for all three carriers), so it is a copy of the Chinese text, not an English translation; §7 is the first English prose in it. That pre-existing condition is declared here rather than hidden, and it is not repaired by this change."
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
    source: "14-ai-development/governance-register/GOV-NC-2026-11-21-CWD-SPLIT-014.md"
    en: null
    zh-CN: "docs/zh-CN/14-ai-development/governance-register/GOV-NC-2026-11-21-CWD-SPLIT-014.md"
---

# GOV-NC-2026-11-21-CWD-SPLIT-014

**Status:** `FIXED-UNGUARDED` — the defect is fixed on main (see §7); it has no regression test. Independent review remains `NOT_ASSIGNED`.
**Nature:** `REGISTER_ONLY / NO_IMPLEMENTATION / NO_GATE_CHANGE / REQUIRES_INDEPENDENT_REVIEW`
**Measured at:** `main = 67074d2ff7`
**Extends:** `GOV-NC-2026-11-21-SPLIT-DOMAIN-011.md`, `GOV-NC-2026-11-21-PAIRING-RESIDUAL-013.md`
**Register author:** strategic requirement orchestrator session. **Not** an independent reviewer, **not** the accountable owner.

---

## 0. Summary

`scripts/check_bilingual_docs.py` resolves its two roots from **two different anchors**:

```python
REPO_ROOT = Path(__file__).resolve().parents[1]   # line 23 — anchored to the script
ROOT      = Path.cwd()                            # line 157 — anchored to the process
```

The gap scan walks `REPO_ROOT`. Every pairing decision (`side_by_side_partner`, `mirror_partner`, `_carries_chinese`, `_has_any_chinese`) reads `ROOT`.

When `cwd != repo root`, the two disagree. The consequences are measurable and, in one direction, severe:

| `cwd` | pairing works? | `--write-baseline` result |
|---|---|---|
| repo root (CI condition) | yes | **77** entries (correct) |
| any other directory | **no — every pair fails** | **117** entries (+41, all real pairs frozen as gaps) |

**In CI this never fires.** `.github/workflows/bilingual-docs.yml` runs `python3 scripts/check_bilingual_docs.py` with the default working directory, which is the checkout root. The defect is a *local measurement* hazard and a *baseline-regeneration* hazard, not a CI-runtime hazard.

**Correction to this register's first version:** I originally claimed this split explains the wrong measurements in commit `67074d2`. §3 now shows that the real cause there was that the probe file was English, not that `cwd` was wrong. The split is real and the hazard is real; the attribution was not.

---

## 1. The mechanism

```python
REPO_ROOT = Path(__file__).resolve().parents[1]     # always the repo, wherever you are
...
ROOT = Path.cwd()                                   # wherever you happen to be
```

`current_bilingual_gaps()` iterates `REPO_ROOT / root_name`, so it always finds the files. It then calls `_side_by_side_bilingual(source)`, which calls `side_by_side_partner(source)`, which tests `(ROOT / cand).is_file()`.

If `ROOT` is not the repo, `(ROOT / cand).is_file()` is always `False`. Therefore:

- `side_by_side_partner()` returns `None` for everything
- `_side_by_side_bilingual()` returns `False` for everything
- every side-by-side pair is reported as an unpaired gap

Measured directly, same script, same tree, same probe file `02-domain-model/sb.md` + `sb.zh-CN.md`:

```
cwd = repo root
  {'REPO_ROOT': '...\amb_now', 'ROOT': '...\amb_now',
   'sbs': True, 'partner': '02-domain-model/sb.zh-CN.md', 'in_gaps': False}

cwd = parent directory
  {'REPO_ROOT': '...\amb_now', 'ROOT': '...\opencode',
   'sbs': False, 'partner': None, 'in_gaps': True}
```

One `cd` flips a correct pair into a gap.

---

## 2. The severe direction: baseline regeneration

`--write-baseline` writes `sorted(current_bilingual_gaps())` to `scripts/bilingual-baseline.txt`. Run from a foreign `cwd`, it writes the *unpaired* view of the whole tree.

Reproduced on a clean clone at `67074d2`:

```
A) python scripts/check_bilingual_docs.py --write-baseline     (cwd = repo root)
   -> baseline written: 77 entries
   -> file unchanged (77)

B) cd /tmp/opencode && python <clone>/scripts/check_bilingual_docs.py --write-baseline
   -> baseline written: 117 entries
   -> git diff --stat: 41 insertions(+), 1 deletion(-)
```

The 41 added lines are not junk. They are **every real bilingual pair in the repository**:

```
02-domain-model/phase-2-domain-extension.md
02-domain-model/phase-2-domain-extension.zh-CN.md
06-memory-context/context-implementation-coverage.md
06-memory-context/context-implementation-coverage.zh-CN.md
07-agent-integration/adapter-capability-tiers.md
07-agent-integration/adapter-capability-tiers.zh-CN.md
08-bmcp-protocol/protocol-index.md
08-bmcp-protocol/protocol-index.zh-CN.md
14-ai-development/AI-EXEC-001.md
14-ai-development/governance-register/README.md
... (41 total)
```

### 2.1 Why the ratchet does not stop it

The gate enforces a two-way ratchet:

```python
new_gaps = sorted(gap_now - baseline)
resolved = sorted(baseline - gap_now)
if new_gaps: return 2
if resolved: return 2          # "Resolved bilingual gap must be removed from ..."
```

Freezing 41 pairs into the baseline means:

- `new_gaps` is empty (the pairs are now expected to be gaps)
- `resolved` is empty (they are still gaps under the same foreign-`cwd` view)

**Both directions are silent.** The ratchet is designed to detect *documentation* drift; it cannot detect a baseline regenerated under a *different measurement anchor*, because under that anchor the numbers are self-consistent.

### 2.2 What a frozen-at-117 baseline would actually permit

With the inflated baseline committed, the 41 pairs would no longer be *required* to have counterparts — they would be permanently grandfathered as known-defective. A later PR could then delete `docs/en/...` or the `.zh-CN.md` side of any of them and the gate would report `resolved`, which *also* passes only if someone removes the entry. In practice the effect is: the 5 live non-14 pairs from register 013 stop being enforced at all.

This is not a hypothetical escalation of a cosmetic bug. It is a path from "a correct pair is blocked" to "a correct pair is not checked."

### 2.3 Not exploited

I found no commit in main that contains a 117-entry baseline. The current file is 77. This register records a reachable hazard, not a realised incident.

---

## 3. The public claim this explains — corrected

Commit `67074d2` ("withdraw the zero-byte gate exploit — it is closed on main") added a section to `14-ai-development/work-items/GAP-BASELINE-001.md` asserting, at `f687346c`:

```
=== zero-byte .zh-CN.md ===
  zz-empty-probe.md          exists=True  size=805  in_gaps=True
  zz-empty-probe.zh-CN.md    exists=True  size=0    in_gaps=True
=== all-English .zh-CN.md (byte-identical copy of the .md) ===
  zz-eng-probe.md            exists=True  size=805  in_gaps=True
  zz-eng-probe.zh-CN.md      exists=True  size=805  in_gaps=True
```

and concluding "The exploit does not reproduce."

**I first attributed this to the `cwd` split. That was the wrong cause, and the discriminating experiment below settles it.**

### 3.1 The discriminating experiment

Two probes, identical in byte size (805), identical in shape (`.zh-CN.md` is a byte-for-byte copy of `.md`), identical `cwd` (repo root). **The only variable is whether the bytes are CJK:**

```
zz-pure-en   size=805  CJK=False
   .md       in_gaps=True   sbs=False
   .zh-CN.md in_gaps=True   sbs=False

zz-has-cjk   size=805  CJK=True
   .md       in_gaps=False  sbs=True
   .zh-CN.md in_gaps=False  sbs=True
```

The English probe is reported as a gap. The Chinese probe is accepted. `cwd` never changed. **CJK presence is the discriminator, not `cwd`.**

### 3.2 So the two variants must be separated

| Probe | Source language | Result | Meaning |
|---|---|---|---|
| zero-byte `.zh-CN.md` + **Chinese** `.md` | Chinese | **accepted** | **exploit is OPEN** |
| all-English `.md` + all-English `.zh-CN.md` | English | **both gaps** | correct behaviour, not the exploit |

`67074d2` printed `in_gaps=True` for **both** pairs. The second pair being a gap is correct. The first pair being a gap is what its probe reported — and with a Chinese source it does not reproduce.

The printed output is therefore consistent with the probe having used an **English** `zz-empty-probe.md`. `_has_any_chinese(source)` returns `False`, `_has_any_chinese(partner)` returns `False`, `_side_by_side_bilingual()` returns `False`, and the pair is a gap — for the correct reason, having nothing to do with zero bytes.

**I cannot prove the source was English** — I have the output, not the command. But I can state that the output is fully explained by that hypothesis, and that the same probe with a Chinese source produces the opposite result.

### 3.3 Verdict

- The **zero-byte exploit is open** on `f687346` and on current main: a Chinese `X.md` with a 0-byte `X.zh-CN.md` is accepted as a bilingual pair.
- The **`cwd` split is real** (§1, §2) and is a genuine hazard for baseline regeneration, but it is **not** what produced `67074d2`'s numbers.
- The withdrawal section in `GAP-BASELINE-001.md` should be withdrawn: it withdrew a true finding on the strength of a probe that measured a different case.

---

## 4. Three defects, three different scopes

Registers 011, 013 and this one describe problems that look similar and are not:

| # | Defect | Where it fires | Fix scope |
|---|---|---|---|
| 011 | diff domain demands `docs/en` + `docs/zh-CN` for non-14 roots | **CI** — blocks 5 real pairs on every PR | policy decision required |
| 013 | content predicate accepts 1 CJK char or a 0-byte partner | **CI** — accepts near-empty "translations" | predicate calibration |
| 014 | `ROOT = Path.cwd()` vs `REPO_ROOT = Path(__file__)` | **local only**; baseline regeneration | one-line anchor unification |

Only 014 is a one-line class of fix, and only 014 is currently *not* affecting CI. Ordering the work by severity would put 011 first, 013 second, 014 third — but 014 first by ease, and 014 is the one that corrupts other people's measurements, which is why it is worth recording before the other two are fixed.

---

## 5. Reproduction

```
repo:    oahcom/AiMemoryBrainArchitecture
commit:  67074d2ff7
clone:   git clone <repo> /tmp/x && cd /tmp/x && git reset --hard 67074d2ff7

# A — correct anchor
cd /tmp/x
python scripts/check_bilingual_docs.py --write-baseline
grep -vc '^#' scripts/bilingual-baseline.txt      # 77

# B — foreign anchor
git checkout -- scripts/bilingual-baseline.txt
cd /tmp
python /tmp/x/scripts/check_bilingual_docs.py --write-baseline
grep -vc '^#' /tmp/x/scripts/bilingual-baseline.txt   # 117
```

No network access, no CI, no API quota required.

---

## 6. What this register does not claim

- It does not claim CI is broken. CI sets `cwd` to the checkout root and is unaffected.
- It does not claim the 117-entry baseline was ever committed. It was not.
- It does not claim to know the author's command in `67074d2`. It claims their printed output is the signature of this defect and that the correct measurement contradicts it.
- It proposes no patch. Unifying the anchor is a policy-neutral one-line change, but it is still a gate change and requires authorisation.
- It does not assign an independent review seat. That seat remains `NOT_ASSIGNED`.

**Blocking chain unchanged:** independent review `NOT_ASSIGNED`, implementation authorisation `NOT_AUTHORISED`, sponsor / accountable owner `NOT_ASSIGNED`.

---

## 7. Measured: the defect is fixed, and there is no regression test (2026-11-23)

The body of this register and its §5 reproduction steps are **not changed**. The mechanism in §1 and §2 was real at `67074d2` and the record stands. What follows is measured on current `main`.

### 7.1 The fix has landed

| Item | Value |
|---|---|
| Fix commit | `8ab40fb4`, 2026-11-22 10:37:32 +0800, `fix(gate): enumerate tracked files and refuse baseline writes on a dirty tree` |
| Current `main` | `8365716a`; `8ab40fb4` is an ancestor |
| Change | `ROOT = Path.cwd()` → `ROOT = REPO_ROOT` (line 170), and every `subprocess` call switched from `cwd=ROOT` to `cwd=REPO_ROOT` |
| Residue | `grep -c 'Path.cwd()' scripts/check_bilingual_docs.py` → **0** |

The two anchors §1 describes are now one. `current_bilingual_gaps()`, `side_by_side_partner()` and `_has_any_chinese()` read the same root.

### 7.2 Behavioural verification, not just reading the code

On a clean worktree at `origin/main`, running `--write-baseline` from outside the repository:

| Tree state | Result |
|---|---|
| `main` as-is (`ROOT = REPO_ROOT`) | **77** entries |
| The same tree with line 170 reverted to `ROOT = Path.cwd()` | **120** entries |

The 43-entry difference is exactly what §2 describes: every real pair frozen as a gap. §2 measured 117 at `67074d2`; the figure here is 120. That difference is two days of new pairs, not a change in mechanism.

`8ab40fb4` also added a dirty-tree write refusal, and it holds:

```
$ echo x > 02-domain-model/untracked-probe.md
$ python scripts/check_bilingual_docs.py --write-baseline
baseline write refused: working tree is not clean; git status --porcelain --untracked-files=all:
?? 02-domain-model/untracked-probe.md
```

So §2.1's "both ratchet directions are silent" path now has a precondition in front of it: a dirty tree cannot write a baseline at all.

### 7.3 The fix has no regression test — this is the section's main finding

With line 170 reverted to `ROOT = Path.cwd()`, the failure sets of both suites are **identical, line for line**:

| Suite | Fixed | Broken |
|---|---|---|
| `scripts/test_check_bilingual_docs.py` | `Ran 3 tests` / `OK` | `Ran 3 tests` / `OK` |
| `scripts/governance/evidence/test_gate_normative_roots.py` | `Ran 52 tests` / `FAILED (failures=3, errors=21)` | the same 24 failures, `diff` empty |

Those 24 failures are identical in both states — that part holds. But attributing them to "a pre-existing Windows temp-path problem, unrelated to this defect" is **wrong**; see §8: this fix introduced them. Before `8ab40fb4` the suite was `Ran 52 tests` / `OK`; after it, `FAILED (failures=3, errors=21)`; and between the two, only `8ab40fb4` touched the gate or that test file. Of the 24, only 1 is a `WindowsPath` assertion; 10 are `current_bilingual_gaps()`'s `git ls-files` exiting 128, 11 are other, and 2 are file-creation identity unavailable.

Consequence: **this defect can return exactly as it was, and neither suite will make a sound.** The only way to observe the difference is to run the gate from outside the repository and write a baseline — and no test does that. The six `os.chdir()` calls in `test_gate_normative_roots.py` all set the cwd **into** the repository, the opposite direction.

That gap between "fixed" and "cannot regress" is what this section records, not something it papers over.

### 7.4 The fix does not point back at this register

`8ab40fb4`'s commit message does not mention `014`; it registers the boundary in `GOV-NC-2026-11-22-ENUM-BOUNDARY-021`, created by that same commit, whose §4 and T07 cover this defect. A repo-wide `grep CWD-SPLIT-014` hits only the `Extends:` lines of 015 and 017.

So this register's status line, `OPEN — MEASUREMENT ONLY`, is still literally accurate — nobody has declared it closed — while reading as though the defect is live. §7 is for that reader.

### 7.5 Status

`OPEN` → `FIXED-UNGUARDED — defect fixed on main, no regression test; independent review still NOT_ASSIGNED`.

Not `CLOSED`, for two reasons: §6's blocking chain includes independent review, and a session that writes this measurement cannot supply independence for it; and §7.3 shows the fix has no guard, and an unguarded fix should not be booked as resolved. §3's zero-byte question belongs to register 013; it was re-measured on 2026-11-23 and is still open (a zero-byte partner is accepted by `_side_by_side_bilingual()`), and it is out of scope here.

---

## 8. Correcting §7.3's attribution (2026-11-23)

§7.3's **main conclusion is unchanged**: this register's defect can return with neither suite making a sound, because `scripts/test_check_bilingual_docs.py` — the only one CI runs, 3 tests — is `OK` in both the fixed and the broken state.

But §7.3's causal explanation of those 24 failures is wrong. Corrected:

| | §7.3 as written | Measured |
|---|---|---|
| Pre-existing? | "pre-existing" | **No.** `9944d07e` → `Ran 52 tests` / `OK`; `8ab40fb4` → `FAILED (failures=3, errors=21)` |
| Related to this defect? | "unrelated" | **Directly.** The `cwd=ROOT` → `cwd=REPO_ROOT` step — this register's fix itself — is what broke the test helper |
| Attribution | "a Windows temp-path problem" | **1 of 24.** 10 are `current_bilingual_gaps()`'s `git ls-files` exiting 128, 11 other, 2 file-creation identity unavailable |

The mechanism: `load_gate()` points `mod.ROOT` at a temp repo but leaves `mod.REPO_ROOT` alone; after `8ab40fb4` made `changed_status()` read `REPO_ROOT`, the helper's temp repo is never consulted, so `git diff A...B` runs in the real repository against two SHAs that exist only in the temp one, and exits 128.

The full measurement, timeline and reproduction steps are in `GOV-NC-2026-11-23-UNREACHABLE-GUARD-030`.

**This correction does not change this register's `FIXED-UNGUARDED` status.** It changes what a reader takes "those 24 are historical noise" to mean — they are not noise; they are this fix's own product.
