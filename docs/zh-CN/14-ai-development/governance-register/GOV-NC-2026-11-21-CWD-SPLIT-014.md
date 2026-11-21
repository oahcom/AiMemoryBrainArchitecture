# GOV-NC-2026-11-21-CWD-SPLIT-014

**Status:** OPEN — MEASUREMENT ONLY
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

**In CI this never fires.** `.github/workflows/bilingual-docs.yml` runs `python3 scripts/check_bilingual_docs.py` with the default working directory, which is the checkout root. The defect is a *local measurement* hazard and a *baseline-regeneration* hazard, not a CI-runtime hazard. That distinction is the whole reason this register exists: it explains a wrong public claim without implying the gate is broken in production.

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

## 3. The public claim this explains

Commit `67074d2` ("withdraw the zero-byte gate exploit — it is closed on main") added a section to `14-ai-development/work-items/GAP-BASELINE-001.md` asserting, at `f687346c`:

```
=== zero-byte .zh-CN.md ===
  zz-empty-probe.md          in_gaps=True
  zz-empty-probe.zh-CN.md    in_gaps=True
=== all-English .zh-CN.md ===
  zz-eng-probe.md            in_gaps=True
  zz-eng-probe.zh-CN.md      in_gaps=True
```

and concluding "The exploit does not reproduce."

**Measured at both `f687346` and `67074d2`, in the repo root, the opposite holds:**

```
zero-byte probe
  .md        {'in_gaps': False, 'sbs': True, 'partner': '02-domain-model/zz-empty-probe.zh-CN.md'}
  .zh-CN.md  {'in_gaps': False, 'sbs': True, 'partner': '02-domain-model/zz-empty-probe.md'}

byte-identical probe
  .md        {'in_gaps': False, 'sbs': True}
  .zh-CN.md  {'in_gaps': False, 'sbs': True}
```

Both files of both pairs are **accepted**. The zero-byte exploit is **open**, not closed.

The `cwd` split is the mechanism that produces `in_gaps=True` for every file at once: a probe run from outside the repository reports all four files as gaps, which reads exactly like "the exploit is closed."

I cannot prove that is what the author did — I only have their printed output, not their command. What I can state is that the printed output is the signature of the `cwd` split, and that the same probe run correctly contradicts it. A third party reproducing from the repo root will get my result.

**Therefore the withdrawal section in `GAP-BASELINE-001.md` is itself unreliable and should be withdrawn**, and the zero-byte case should be re-opened until someone reproduces it from a clean clone at the repo root.

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
