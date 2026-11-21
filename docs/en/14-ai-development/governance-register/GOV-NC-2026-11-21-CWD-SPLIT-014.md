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
