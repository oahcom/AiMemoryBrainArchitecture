---
document_metadata:
  domain: ai-development
  role: decision-record

  lifecycle:
    approval:
      decision_status: Approved
      approver: "Owner acting as owner proxy, under the standing instruction that a blocking decision with no human available is to be taken and recorded rather than left open."
      decision_date: "2026-11-23"
      approved_version:
        scheme: content-hash
        value: "b1947c1c6203bd0386c074054c46d612f55ba7c63c3b755d70b607762da159b7"
      approval_scope:
        type: Full-document
      approval_applicability: Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/adr/OWNER-DECISION-EMBEDDED-BILINGUAL-001.md — the DECIDED line in this document names the decider and the date"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-23"
      last_verification_note: "Every figure was measured at main 880e6a78 in this session: §2 by enumerating git ls-files over 13-engineering-decisions/*.md and reading each file in full; §3 by patching a throwaway worktree and calling current_bilingual_gaps() four times (baseline, variant A, B, C); §4 over every accepted side-by-side pair in the tree. The first draft of §3 predicted 20 and was wrong — the measured figure is 11, and the correction is recorded in the body rather than silently replaced."
    usage_status: Active
    modification_status: Unchanged

  authority:
    canonical_status: Canonical
    canonical_scope: "Owner ruling: 13-engineering-decisions is embedded bilingual, gate Shape 3 is root-name-scoped where the policy scopes nothing by root, and honouring the requirement drops the frozen baseline from 77 to 11."
    canonical_scope_id: ai-development/embedded-bilingual-shape
    canonical_scope_keywords:
      - embedded-bilingual
      - bilingual-gate
      - shape-3
      - baseline-delta
      - 13-engineering-decisions
    canonical_conflict_status: None
    normative_status: Normative
---

# OWNER-DECISION-EMBEDDED-BILINGUAL-001 — the 58 entries are gate debt, not documentation debt

**DECIDED — 2026-11-23, Owner acting as owner proxy.**

Answers the three-way question `GOV-NC-2026-11-21-EMBEDDED-ROOT-015` §6 declined to guess at, and pre-specifies the dispatch so a reader can check the ruling against the work order.

## 1. The three branches, and which one is true

Register 015 §6 listed the three states that would make its finding a non-issue. The third is the true one.

| # | Branch from 015 §6 | Verdict |
|---|---|---|
| 1 | `13-engineering-decisions` was deliberately excluded from embedded-bilingual recognition, and that decision is recorded | **False.** No such decision exists. I looked in `00-governance/bilingual-documentation-policy.md`, the root's own parity audit, `EMBEDDED_BILINGUAL_SOURCES` and its history, and the git history of `13-engineering-decisions/`. |
| 2 | The 58 files are not actually embedded bilingual despite the audit table | **False for 57 of 58.** Measured in §2. |
| 3 | Shape 3 is meant to be root-agnostic and `source.startswith("14-ai-development/")` is a leftover | **True.** |

The guard is one line:

```python
if not paired and source.startswith("14-ai-development/"):
    paired = english.is_file() and _carries_chinese(source)
```

Nothing in the policy scopes shape recognition to a root. `00-governance/bilingual-documentation-policy.md` §2 names "technology evaluations, ADRs, engineering decisions" in its scope list — which is `13-engineering-decisions` almost verbatim — and §3 requires parity, never parity-by-root.

## 2. The 58 files are embedded bilingual

Measured over all 58 tracked files, reading each in full. A file counts as embedded bilingual when its headings carry both languages on one line (`# Agent Integration Boundary / Agent 集成边界`) — the shape the policy's §3 parity requirement describes.

| Measure | Files |
|---|---|
| Headings carry both languages in ≥50% of headings | **42** |
| Headings carry both languages in at least one heading | **57** |
| Zero dual-language headings | **1** |

The one exception is `13-engineering-decisions/technology-architecture-blueprint.md`: 56 headings, **0 CJK characters in 49,666 bytes**. It is genuinely single-language and stays a real gap.

Register 015 said "57 of 58 carry substantial Chinese"; the figure holds, and this ruling adds that the 57 carry it *paired by heading*, not merely as a ratio. A ratio can be met by an appendix of Chinese notes; heading pairing cannot.

## 3. What the guard costs, measured — including a wrong prediction

At `main 880e6a78` the frozen baseline is **77** entries:

```
13-engineering-decisions  58
06-memory-context         10
14-ai-development          4
08-bmcp-protocol           4
00-governance              1
```

Two variants were patched into a throwaway worktree and measured separately, because they are not the same change:

| Variant | Change | Gaps |
|---|---|---|
| — | `main` as-is | **77** |
| A | remove the root guard only; keep `english.is_file()` | **77** |
| B | remove the root guard **and** the `english.is_file()` precondition; predicate stays `_carries_chinese()` | **11** |
| C | remove both; predicate becomes "≥100 CJK **and** ≥1,000 Latin letters in the same file" | **11** |

**Variant A measures zero delta.** That reproduces register 015's M5 result exactly, and it is why M5's conclusion — "the guard has no payload" — was reachable and still wrong. The 58 files fail the *mirror* precondition, not the root guard. Deleting a guard changes nothing when the guarded branch is never reached.

**Variant B is the change the policy's wording suggests** — embedded bilingual carries no `docs/en` mirror by definition, so requiring one is the contradiction. But B keeps `_carries_chinese()` as the whole predicate, and that accepts a file with 100 CJK characters and no English at all as "bilingual". Send a Chinese-only document and it passes. That is the same class of defect as register 013 §3.1: a one-sided predicate certifying a two-sided requirement.

**Variant C is the ruling.** It requires both scripts in quantity in the same file, which is what "embedded bilingual" means. It measures the same 11 as B — so no file in today's tree was being carried by the weaker predicate — but the two are not equivalent, and only one of them still works when someone commits a Chinese-only document tomorrow.

Measured result of variant C:

| | |
|---|---|
| gaps after | **11** |
| entries resolved | **66** |
| new gaps | **0** |
| remaining by root | `06-memory-context` 7, `08-bmcp-protocol` 2, `00-governance` 1, `13-engineering-decisions` 1 |

The one remaining `13-engineering-decisions` entry is `technology-architecture-blueprint.md`, which is correct — it carries no Chinese at all.

The 9 resolved entries outside the 13 root were verified individually, not assumed: every one carries both scripts in quantity (lowest 105 CJK / 2,107 Latin, highest 6,387 / 63,727). They were failing the mirror precondition, not a language requirement.

**Correction, recorded rather than quietly replaced:** the first draft of this section predicted "77 → 20, delta −57" from the file count alone. The measured figure is 11, because removing the mirror precondition also resolves 9 entries outside the 13 root that had been failing the same precondition. The prediction was arithmetic on one root; the measurement is over the tree. The measurement is the ruling.

`EMBEDDED_BILINGUAL_SOURCES` stays at 21 entries, all in `00-governance` (12) and `14-ai-development` (9). The point is not to retire it but to stop it being the *only* way to recognise the shape — which is how a root could remain unrepresented for its entire life without anyone deciding that.

## 4. The side-by-side floor is calibration, not preference

Register 013 §3.1 measured that one CJK character anywhere in either file satisfies `_side_by_side_bilingual()`. It has to be fixed. What the fix may cost is measurable, not a matter of taste:

| | |
|---|---|
| Accepted side-by-side pairs in the tree | **86** |
| Shortest side of the smallest pair | **1,364 characters** |
| Pairs with a zero-byte partner | **0** |
| Pairs byte-identical to each other | **0** |
| Sources with both `.en.md` and `.zh-CN.md` present (register 013 §3.3) | **0** |

Every real pair has a shorter side of at least 1,364 characters; the ten shortest run 1,364–2,214. So any floor from 1 to 400 characters rejects **zero** of the 86. A floor of 100 — the same threshold `_carries_chinese()` already uses for the embedded shape — rejects zero and closes §3.1 and §3.2.

§3.3's three-file asymmetry is latent, not live: zero sources have both siblings today. It gets fixed anyway, because an unreachable path becomes reachable the first time someone adds an `.en.md` beside an existing `.zh-CN.md`.

## 5. Dispatch

All three changes live in `scripts/check_bilingual_docs.py` and are authorised together as `AID-2026-054`. This section states the scope; the work order states the constraints.

## 6. Not decided here

- Whether `technology-architecture-blueprint.md` should be translated, mirrored, or moved out of `NORMATIVE_ROOTS`. It stays a gap under all three, and choosing is the document owner's call, not a gate change.
- Whether the remaining 11 baseline entries are correct. This ruling explains 66 of 77; the other 11 belong to registers 011 and 013 and are not touched.
- Whether the gate should recognise embedded bilingual by heading pairing rather than character count. This ruling requires the root-agnostic shape and a non-trivial floor; §4 fixes only what the predicate must not break.
- Whether the baseline file should be regenerated in the same change. It must be, or the ratchet reports 66 `resolved` entries as errors — but that is the work order's acceptance criterion, not this ruling's decision.
