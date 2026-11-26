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
      last_verification_note: "All four gap counts in §9 (77 / 77 / 11 / 11) were measured on 2026-11-23 in a throwaway worktree at 880e6a78, calling current_bilingual_gaps() after each variant. The dual-heading counts in §9.1 come from reading all 58 files, not a sample."
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
    source: "14-ai-development/governance-register/GOV-NC-2026-11-21-EMBEDDED-ROOT-015.md"
    en: null
    zh-CN: "docs/zh-CN/14-ai-development/governance-register/GOV-NC-2026-11-21-EMBEDDED-ROOT-015.md"
---

# GOV-NC-2026-11-21-EMBEDDED-ROOT-015

**Status:** `RULED` — §6 branch 3 is true (see §9); dispatched as `AID-2026-054`. Independent review remains `NOT_ASSIGNED`.
**Nature:** `REGISTER_ONLY / NO_IMPLEMENTATION / NO_GATE_CHANGE / REQUIRES_INDEPENDENT_REVIEW`
**Measured at:** `main = 67074d2ff7`; re-verified at `8a2ce1b` with identical counts
**Extends:** `GOV-NC-2026-11-21-SPLIT-DOMAIN-011.md`, `...-PAIRING-RESIDUAL-013.md`, `...-CWD-SPLIT-014.md`
**Register author:** strategic requirement orchestrator session. **Not** an independent reviewer, **not** the accountable owner.

---

## 0.1 Revision history

| Version | Date | Change |
|---|---|---|
| v1 | 2026-11-21 | Initial. Claimed the 58 gaps are caused by Shape 3 being gated on `root_name == "14-ai-development"` |
| **v2** | 2026-11-21 | **Attribution corrected**: Shape 3 requires a `docs/en` mirror, and none of these 58 has one, so Shape 3 was never the cause. The real mechanism is that the gate has **no shape at all** for single-file embedded bilingual, only a per-file allowlist. See §3.1, §3.2 |

**The v2 correction matters**: v1 pointed at a fix that does nothing. Measured, removing the root-name guard leaves the gap count at 77 — unchanged. Following v1 would have produced a large diff with no effect.

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

This is not a documentation backlog. Those files are bilingual — they carry both languages inside one file. **The gate has no shape that recognises this** (§3.2), so the only way such a file can pass is a per-file entry in `EMBEDDED_BILINGUAL_SOURCES`. That list has 21 entries; none is in this root.

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
| >= 5% (clearly embedded bilingual) | **52** |
| >= 15% | 3 |
| exactly 0% | 1 |

So **57 of 58** carry substantial Chinese text. The one at 0% is `13-engineering-decisions/technology-architecture-blueprint.md`, which is a genuine single-language file and a genuine gap.

## 2. The root's own audit says so

`13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/bilingual-parity-audit.md` is the root's self-audit. Its acceptance rule:

> A file is bilingual-complete only when the full normative content is present in both languages **in the same file/change set**, with semantic parity, stable-ID parity, matching decision status, matching examples/constraints and traceable source revisions.

And its per-file table records, file after file:

```
| canonical-domain-entity-inventory.md | ... | REMEDIATED - MANUAL PARITY REVIEW PENDING |
| canonical-identity-semantics.md      | ... | REMEDIATED - MANUAL REVIEW PENDING |
| canonical-state-semantics.md         | ... | REMEDIATED - MANUAL REVIEW PENDING |
| canonical-temporal-evidence-semantics.md | ... | REMEDIATED - MANUAL PARITY REVIEW PENDING |
```

Every row is `REMEDIATED`. The remediation was performed **inside the file**, which is exactly the shape `_carries_chinese()` was written to detect.

## 3. Why the gate still reports all 58

`current_bilingual_gaps()` accepts exactly three shapes:

| Shape | Condition | Applies to `13-...`? |
|---|---|---|
| 1. mirror | `docs/en/X` **and** `docs/zh-CN/X` both exist | only 3 files have this |
| 2. side-by-side | `X.zh-CN.md` / `X.en.md` sibling | 0 files have this |
| 3. embedded | `docs/en/X` exists **and** `_carries_chinese(X)` | **0 files qualify — see §3.1** |

### 3.1 Correction: Shape 3 was never the cause

**v1 of this register claimed "Shape 3 is the shape that matches these files, and it is hard-coded to a single root". That attribution was wrong.**

Shape 3 requires `docs/en/X` to exist. Measured:

```
of the 77 gaps, how many have a docs/en mirror:      0
of the 13 root's 58 gaps, how many have docs/en:     0
```

So removing the root-name guard entirely rescues **nothing**. Confirmed by running it:

```
M5 (delete the root_name == "14-ai-development" guard)
BEFORE  gaps=77 baseline=77 new=0 resolved=0
AFTER   gaps=77 baseline=77 new=0 resolved=0
```

Not one gap moves. That is also why mutant M5 can survive unnoticed: **the branch it guards never fires on any of the 77 baseline entries.**

Shape 3's actual scope, measured, is exactly three files, all inside the 14 root:

```
14-ai-development/AI-EXEC-001.md
14-ai-development/AI-EXEC-002.md
14-ai-development/AI-EXEC-ROLLOUT-001.md
```

They satisfy all four conditions at once: no `docs/zh-CN`, no side-by-side partner, a `docs/en` mirror, and Chinese content. With the guard removed, the number of files in the other eight roots meeting those four conditions is **0**. So removing it changes nothing today — which does not prove it is harmless, only that it currently carries no load.

### 3.2 The real mechanism for the 58: no counterpart file of any kind

Classifying all 77 gaps by what counterpart exists:

| Mechanism | Count |
|---|---|
| has a side-by-side partner | 0 |
| has both `docs/en` and `docs/zh-CN` | 0 |
| `docs/en` only | 0 |
| `docs/zh-CN` only | 0 |
| **no counterpart at all** | **77** |

The 13 root's 58 are the same: `docs/en` = 0, `docs/zh-CN` = 0, side-by-side = 0, and 57 of the 58 carry Chinese.

**The correct statement is therefore**: these 58 files are single-file embedded bilingual, and all three gate shapes **require a second file to exist** (a mirror or a sibling). The gate has no shape that accepts "one file carrying both languages". The 21 entries in `EMBEDDED_BILINGUAL_SOURCES` exist precisely because of this — they are a **per-file allowlist**, not a shape recogniser.

The policy/gate contradiction is therefore more fundamental than v1 stated: not "the shape exists but is gated to one root", but "**the shape does not exist in the gate at all**; it can only be registered file by file". `00-governance` registered 12, the 14 root registered 9, and the 13 root registered 0 — in the root where embedded bilingual is most concentrated (57 of 58).

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
| 014 | `ROOT = cwd` inflates the baseline 77 -> 117 | **worse than reported**: the 41 added entries land on top of an already-75%-wrong baseline |

And a correction to my own framing in 013: I described the baseline as "77 frozen gaps" without asking what they were. **Three quarters of them are one root's embedded-bilingual documentation.** A number that large deserved a breakdown before I used it as a denominator.

## 6. What would have to be true for this to be a non-issue

Any one of these would close it:

1. `13-engineering-decisions` was deliberately excluded from embedded-bilingual recognition, and that decision is recorded. -> then the 58 entries are correct and the root should arguably leave `NORMATIVE_ROOTS`.
2. The 58 files are not actually embedded bilingual despite the audit table. -> then the audit table is wrong, which is a larger problem.
3. Shape 3 is meant to be root-agnostic and the `root_name ==` guard is a leftover. -> then 58 entries are a gate bug, not a documentation debt.

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

find 13-engineering-decisions -name '*.md' | wc -l              -> 58
find docs/en/13-engineering-decisions -name '*.md' | wc -l      -> 3
find docs/zh-CN/13-engineering-decisions -name '*.md' | wc -l   -> 3
```

CJK ratio per file requires only reading the file; no gate involvement.

## 8. What this register does not claim

- It does not claim the 58 files should be exempted. That is a policy decision.
- It does not claim the gate is wrong to require mirrors; shape 3's root guard may be intentional.
- It does not propose adding 58 entries to `EMBEDDED_BILINGUAL_SOURCES`. That would be a 58-entry exemption list nobody reviewed.
- It does not claim the parity audit is accurate. I verified CJK presence, not semantic parity — the audit itself says every row is still `MANUAL REVIEW PENDING`.
- It does not assign an independent review seat. That seat remains `NOT_ASSIGNED`.

**Blocking chain unchanged:** independent review `NOT_ASSIGNED`, implementation authorisation `NOT_AUTHORISED`, sponsor / accountable owner `NOT_ASSIGNED`.

---

## 9. Ruling: §6 branch 3 is the true one (2026-11-23)

The body of this register and its three-way §6 question are **not changed**. §6 says "I cannot distinguish these three from the repository. **That is the finding.**" This section decides that finding and supplies the measurement §6 could not get.

Ruling: `OWNER-DECISION-EMBEDDED-BILINGUAL-001` (`14-ai-development/adr/`). Work order: `AID-2026-054`.

| §6 branch | Verdict |
|---|---|
| 1. `13-engineering-decisions` was deliberately excluded, and the decision is recorded | **False.** No such decision exists. Checked `00-governance/bilingual-documentation-policy.md`, the root's own parity audit, `EMBEDDED_BILINGUAL_SOURCES` and its history, and the root's git history. |
| 2. The 58 files are not actually embedded bilingual; the audit table is wrong | **False for 57 of 58.** See §9.1. |
| 3. Shape 3 should be root-agnostic and `source.startswith("14-ai-development/")` is a leftover | **True.** |

### 9.1 The 58 files are embedded bilingual, on stronger evidence than §1 used

§1 used CJK ratio (≥5% → 52 files). A ratio is weak evidence: an appendix of Chinese notes lifts it. This section uses whether **headings place both languages on one line** (`# Agent Integration Boundary / Agent 集成边界`), because that is the parity shape policy §3 describes.

| Measure | Files |
|---|---|
| Both languages in ≥50% of headings | **42** |
| Both languages in at least one heading | **57** |
| Zero dual-language headings | **1** |

The exception is `13-engineering-decisions/technology-architecture-blueprint.md`: 56 headings, **0 CJK characters in 49,666 bytes**. It is genuinely single-language and is the one entry that must survive as a gap — it is the control that proves the new predicate is not simply accepting everything.

### 9.2 Correction to §3.1 and §6: the guard measured zero because it never ran

§3.1 recorded mutation M5: delete the root-name guard, measure `77 → 77`, conclude the guard "has no payload today".

That inference is wrong, and wrong somewhere reproducible. Shape 3's condition is **two** clauses: `source.startswith("14-ai-development/")` **and** `english.is_file()`. The 58 files fail the **second** — they have no `docs/en` mirror. The guarded branch was never reached, so deleting the guard measured zero change regardless of the guard.

Three variants were measured on a throwaway worktree at `880e6a78`, each calling `current_bilingual_gaps()`:

| Variant | Change | Gaps |
|---|---|---|
| — | `main` as-is | **77** |
| A | remove the root guard only; keep `english.is_file()` | **77** |
| B | remove both; predicate stays `_carries_chinese()` | **11** |
| C (ruled) | remove both; predicate requires `cjk >= 100` **and** `latin >= 1000` in the same file | **11** |

Variant A reproduces M5's `77 → 77` exactly. M5's number was right; its conclusion was not. **A branch that never executes measures zero either way.** That is also why the M5 mutant survived unnoticed.

**B and C measure the same 11 today and are not equivalent.** B accepts a file with 100 CJK characters and no English — the same one-sided-predicate defect as 013 §3.1, moved to the embedded shape. Only C survives a Chinese-only document committed tomorrow. The identical measurement is recorded as identical, not as agreement.

### 9.3 Gaps 77 → 11, resolved 66, new 0

| | |
|---|---|
| gaps after | **11** |
| resolved from the baseline | **66** |
| new gaps | **0** |
| by root | `06-memory-context` 7, `08-bmcp-protocol` 2, `00-governance` 1, `13-engineering-decisions` 1 |

The one remaining `13-engineering-decisions` entry is `technology-architecture-blueprint.md`, as expected. The 9 resolutions outside that root were verified individually: every one places both languages in one file (lowest 105 CJK / 2,107 Latin letters). They had been failing the mirror precondition, not a language requirement.

**A wrong prediction is recorded, not quietly replaced.** This section's first draft computed "77 → 20, delta −57" from the file count. The measurement is 11, because removing the mirror precondition also resolves 9 entries outside the 13 root. The prediction counted one root; the measurement counts the tree.

### 9.4 Status and residue

`OPEN` → `RULED — branch 3; dispatched as AID-2026-054; independent review still NOT_ASSIGNED`.

Not `CLOSED`: the ruling changes a gate predicate, and a session that writes the predicate cannot supply independence for it; and the baseline shrink in §9.3 is practically irreversible — once 66 entries leave the baseline, nothing records that they were ever considered gaps, and re-adding any of them is a ratchet error. So this change carries more verification weight than usual and cannot be self-certified by the side that dispatched it.

Out of scope here: whether `technology-architecture-blueprint.md` should be translated, mirrored, or moved out of `NORMATIVE_ROOTS`. All three leave it a gap; choosing is the document owner's call.
