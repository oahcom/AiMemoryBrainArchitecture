# GOV-NC-2026-11-21-EMBEDDED-ROOT-015

**Status:** OPEN — MEASUREMENT ONLY
**Nature:** `REGISTER_ONLY / NO_IMPLEMENTATION / NO_GATE_CHANGE / REQUIRES_INDEPENDENT_REVIEW`
**Measured at:** `main = 67074d2ff7`
**Extends:** `GOV-NC-2026-11-21-SPLIT-DOMAIN-011.md`, `...-PAIRING-RESIDUAL-013.md`, `...-CWD-SPLIT-014.md`
**Register author:** strategic requirement orchestrator session. **Not** an independent reviewer, **not** the accountable owner.

---

## 0. The finding

The frozen baseline has 77 entries. **58 of them — 75% — are the entire `13-engineering-decisions` root.**

```
13-engineering-decisions  58
06-memory-context         10
14-ai-development          4
08-bmcp-protocol           4
00-governance              1
---
total                     77
```

`13-engineering-decisions` contains exactly **58** `.md` files. **All 58 are gaps. Zero pass.**

This is not a documentation backlog. Those files are bilingual — they carry both languages inside one file, which is the third legitimate shape the policy describes. The gate cannot see that shape for this root, because the exemption list does not include it.

---

## 1. The files really are bilingual

Sampled directly, without any gate involvement:

```
13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/canonical-domain-model.md
  bytes: 16152   CJK chars: 1574   ratio: 12.7%
  first headings:
    # Canonical Domain Model
    # 规范领域模型
    ## 1. Design principles / 设计原则
```

Distribution over all 58 files in the root:

| CJK ratio | files |
|---|---|
| ≥ 5% (clearly embedded bilingual) | **52** |
| ≥ 15% | 3 |
| exactly 0% | 1 |

So **57 of 58** carry substantial Chinese text. The one at 0% is `13-engineering-decisions/technology-architecture-blueprint.md`, which is a genuine single-language file and a genuine gap.

## 2. The root's own audit says so

`13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/bilingual-parity-audit.md` is the root's self-audit. Its acceptance rule:

> A file is bilingual-complete only when the full normative content is present in both languages **in the same file/change set**, with semantic parity, stable-ID parity, matching decision status, matching examples/constraints and traceable source revisions.

And its per-file table records, file after file:

```
| canonical-domain-entity-inventory.md | ... | REMEDIATED — MANUAL PARITY REVIEW PENDING |
| canonical-identity-semantics.md      | ... | REMEDIATED — MANUAL REVIEW PENDING |
| canonical-state-semantics.md         | ... | REMEDIATED — MANUAL REVIEW PENDING |
| canonical-temporal-evidence-semantics.md | ... | REMEDIATED — MANUAL PARITY REVIEW PENDING |
```

Every row is `REMEDIATED`. The remediation was performed **inside the file**, which is exactly the shape `_carries_chinese()` was written to detect.

## 3. Why the gate still reports all 58

`current_bilingual_gaps()` accepts exactly three shapes:

| Shape | Condition | Applies to `13-...`? |
|---|---|---|
| 1. mirror | `docs/en/X` **and** `docs/zh-CN/X` both exist | only 3 files have this |
| 2. side-by-side | `X.zh-CN.md` / `X.en.md` sibling | 0 files have this |
| 3. embedded | `docs/en/X` exists **and** `_carries_chinese(X)` | **gated on `root_name == "14-ai-development"`** |

Shape 3 is the one that matches these files. It is hard-coded to a single root:

```python
paired = mirrored or _side_by_side_bilingual(source)
if not paired and root_name == "14-ai-development":
    # Shape 3: the root file IS the Chinese source and docs/en holds the English side.
    paired = english.is_file() and _carries_chinese(source)
```

Shape 3 also requires a `docs/en/X` mirror to exist. The 13 root has only 3 such mirrors (`req02-fts5-vs-like-benchmark.md`, `req02-fts5-vs-like-decision.md`, `technology-architecture-overview.md`), and those 3 happen to be the only files in the root that are *not* embedded bilingual.

**The two mechanisms are mutually exclusive in practice:** the files that are embedded bilingual have no `docs/en` mirror, and the files that have a `docs/en` mirror are not embedded bilingual.

## 4. The exemption list makes the asymmetry explicit

`EMBEDDED_BILINGUAL_SOURCES` has 21 entries, described in the source as "reviewed single-file bilingual sources":

| Root | exemptions |
|---|---|
| `00-governance` | **12** |
| `14-ai-development` | **9** |
| `13-engineering-decisions` | **0** |

Two roots got a per-file exemption review. The third root, whose 58 files were remediated to embedded bilingual by their own audit, got none. Whether that is an oversight or a deliberate decision is not recorded anywhere I could find — and I looked in `00-governance/bilingual-documentation-policy.md`, the parity audit, and the git history for the 13 root.

**The consequence is structural:** 75% of the frozen baseline is one root's documentation that the policy considers complete and the gate considers missing. The ratchet then freezes it forever, because removing an entry is an error (`resolved must be empty`) and adding is an error (`new_gaps must be empty`). The baseline can only shrink by editing the gate — which requires authorisation nobody has.

## 5. What this changes about the other registers

| Register | Claim | Effect of this finding |
|---|---|---|
| 011 | diff domain blocks 5 real side-by-side pairs | unchanged; those 5 are all outside the 13 root |
| 013 | 5 live pairs outside the 14 root, 0 of 5 editable | unchanged |
| 014 | `ROOT = cwd` inflates the baseline 77 → 117 | **worse than reported**: 41 of the 40 added entries would be added on top of an already-75%-wrong baseline |

And a correction to my own framing in 013: I described the baseline as "77 frozen gaps" without asking what they were. **Three quarters of them are one root's embedded-bilingual documentation.** A number that large deserved a breakdown before I used it as a denominator.

## 6. What would have to be true for this to be a non-issue

Any one of these would close it:

1. `13-engineering-decisions` was deliberately excluded from embedded-bilingual recognition, and that decision is recorded. → then the 58 entries are correct and the root should arguably leave `NORMATIVE_ROOTS`.
2. The 58 files are not actually embedded bilingual despite the audit table. → then the audit table is wrong, which is a larger problem.
3. Shape 3 is meant to be root-agnostic and the `root_name ==` guard is a leftover. → then 58 entries are a gate bug, not a documentation debt.

I cannot distinguish these three from the repository. **That is the finding.** A 75% concentration in one root, produced by a hard-coded root name, with a self-audit that says the opposite, is not a state anyone can act on without a decision from the accountable owner.

## 7. Reproduction

```
repo:   oahcom/AiMemoryBrainArchitecture
commit: 67074d2ff7
cwd:    repo root   (register 014: a foreign cwd invalidates this measurement)

python -c "import sys,os;sys.path.insert(0,os.path.join(os.getcwd(),'scripts'));sys.argv=['x'];
import check_bilingual_docs as g, collections;
gp=g.current_bilingual_gaps();
print(collections.Counter(x.split('/')[0] for x in gp))"

-> {'13-engineering-decisions': 58, '06-memory-context': 10,
    '14-ai-development': 4, '08-bmcp-protocol': 4, '00-governance': 1}

find 13-engineering-decisions -name '*.md' | wc -l    -> 58
find docs/en/13-engineering-decisions -name '*.md' | wc -l   -> 3
find docs/zh-CN/13-engineering-decisions -name '*.md' | wc -l -> 3
```

CJK ratio per file requires only reading the file; no gate involvement.

## 8. What this register does not claim

- It does not claim the 58 files should be exempted. That is a policy decision.
- It does not claim the gate is wrong to require mirrors; shape 3's root guard may be intentional.
- It does not propose adding 58 entries to `EMBEDDED_BILINGUAL_SOURCES`. That would be a 58-entry exemption list nobody reviewed.
- It does not claim the parity audit is accurate. I verified CJK presence, not semantic parity — the audit itself says every row is still `MANUAL REVIEW PENDING`.
- It does not assign an independent review seat. That seat remains `NOT_ASSIGNED`.

**Blocking chain unchanged:** independent review `NOT_ASSIGNED`, implementation authorisation `NOT_AUTHORISED`, sponsor / accountable owner `NOT_ASSIGNED`.
