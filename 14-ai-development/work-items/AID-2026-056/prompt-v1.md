---
document_metadata:
  domain: ai-development
  role: work-record

  lifecycle:
    approval:
      decision_status: Draft
      approver: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-24"
      last_verification_note: "Every figure below was measured in this session at main d40d4e09 in the working checkout: the 81 baseline entries were read from scripts/ci/baselines/bilingual-docs.txt and split by calling check_bilingual_docs.side_by_side_partner() and counting CJK/latin characters per file; the 638/199/81 summary line is check_bilingual_docs_full.py's own output; the 3 mirror-of-mirror paths are counterpart() return values; and the predicted 9 was produced by re-running the split with the intended predicate applied to the current violation list. No figure is copied from another document."
    usage_status: Active
    modification_status: Unchanged

  authority:
    canonical_status: Non-Canonical
    canonical_conflict_status: None
    normative_status: Informative

  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# AID-2026-056 — make the full scan agree with the ruling that already governs its contents

**Work item:** `AID-2026-056`
**Register:** `GOV-NC-2026-11-24-GATE-B-AUTHORIZATION-033` (this work item's carrier)
**Base:** `d40d4e09` (main, 2026-11-24)

## 1. Why this exists

`OWNER-DECISION-EMBEDDED-BILINGUAL-001` is `Approved` / `Canonical` / `Normative`. It rules that a document carrying both scripts in quantity is a bilingual document in one file, and that the 66 such files in the frozen baseline are not documentation debt. It also states where those changes live:

> All three changes live in `scripts/check_bilingual_docs.py`

That sentence is why the ruling reached gate A and stopped. Gate B — the required check `Bilingual docs coverage (ratchet)` — runs a different script against a different baseline and still counts all 81 paths as "lack an en/zh-CN counterpart". The ruling has never applied to it.

This was measured, not inferred. Lowering the gate B baseline alone makes the check redder:

```
$ python scripts/ci/gate_ratchet.py --baseline scripts/ci/baselines/bilingual-docs.txt \
    --format paths --command "python3 scripts/check_bilingual_docs_full.py"
ratchet: baseline=15 current=81 regressions=66 fixed=0
ratchet: FAIL - 66 new failure(s) above baseline.
```

The predicate must change before the baseline can. No AID is currently authorized to change either.

## 2. What the 81 are, measured

Split of `scripts/ci/baselines/bilingual-docs.txt` (81 entries, 0 of them pointing at a file that no longer exists), judged by the two criteria the repository itself already implements:

| class | criterion | count |
|---|---|---:|
| A | `check_bilingual_docs.side_by_side_partner()` returns a partner | 6 |
| B | `cjk >= 100` and `latin >= 1000` in the same file | 66 |
| C | neither | 9 |

The six A entries are three pairs:

```
02-domain-model/phase-2-domain-extension.md            + .zh-CN.md
06-memory-context/context-implementation-coverage.md   + .zh-CN.md
07-agent-integration/adapter-capability-tiers.md       + .zh-CN.md
```

The nine C entries, with their measured character counts, are the whole of the real backlog:

```
00-governance/reports/gov-doc-001-full-scan-2026-11-20.md          cjk=35   latin=18497
06-memory-context/context-architecture.md                          cjk=0    latin=13906
06-memory-context/context-budget-and-sufficiency.md                cjk=0    latin=7667
06-memory-context/context-edit-operations.md                       cjk=0    latin=11214
06-memory-context/context-manager.md                               cjk=0    latin=11019
06-memory-context/context-reconciliation.md                        cjk=0    latin=25184
06-memory-context/context-versioning.md                            cjk=0    latin=28669
06-memory-context/phase-3.8.6-g-review-storage-serialization-anchor.md  cjk=21  latin=1135
13-engineering-decisions/technology-architecture-blueprint.md      cjk=0    latin=39156
```

`13-engineering-decisions/technology-architecture-blueprint.md` is 0 CJK / 49666 bytes. It is the control: a predicate that resolves it is a predicate that accepts anything, and the ruling says so explicitly.

## 3. The one thing that is not a predicate question

`counterpart()` reaches the `NORMATIVE_ROOTS` branch without first asking whether the path it was handed is already a language mirror. Four `.zh-CN.md` mirrors live under normative roots outside `14-ai-development/`, and three of them are told to produce a Chinese mirror of themselves:

```
02-domain-model/phase-2-domain-extension.zh-CN.md          -> None
06-memory-context/context-implementation-coverage.zh-CN.md -> None
07-agent-integration/adapter-capability-tiers.zh-CN.md     -> None
```

The fourth resolves only because `docs/en/…` and `docs/zh-CN/…` copies of it happen to exist — i.e. it is satisfied by the very "mirror of a mirror" the other three are being asked for.

For the same three pairs, gate A says "paired" and gate B says "violating". Two required checks, one repository, opposite verdicts on the same two files.

## 4. What to change

Three edits, all in `scripts/check_bilingual_docs_full.py`, plus the baseline that follows and one comment:

1. **`counterpart()` asks what it was given.** A path that is itself a mirror (`.zh-CN.md` / `.en.md`) resolves to its sibling, not to `docs/<lang>/<path>`. Before the `NORMATIVE_ROOTS` branch, not inside it.
2. **Embedded bilingual is recognised.** A path carrying `cjk >= 100` and `latin >= 1000` is a bilingual document in one file and has no counterpart by definition. Same floor as `AID-2026-054`; do not invent a second one.
3. **Side-by-side is recognised.** A path whose sibling pair exists is already paired. Reuse `side_by_side_partner()` rather than writing a second pairing implementation — two implementations of "is this paired" is how gate A and gate B came to disagree in the first place.
4. **Baseline regenerated** from 81 to the number the new predicate actually produces, as removals only and zero additions, in the same commit.
5. **The `gates.yml` comment** saying `81 normative paths lack an en/zh-CN counterpart` is replaced with what the check now measures. It is not accurate for 72 of the 81 and will be less accurate after this change.

## 5. What not to change

- **`NORMATIVE_ROOTS` stays exactly as it is.** It lists 15 roots, 7 of which do not exist on disk, and it omits `08-bmcp-protocol`, which does. That is `GAP-26` and it is a different work item. Adding `08-bmcp-protocol` here would move the violation count by a number this work item has not measured and would make the 81 → 9 prediction untestable. If the implementer believes the roots must be fixed first, stop and say so — do not fix them inside this change.
- **`scripts/check_bilingual_docs.py` and `scripts/bilingual-baseline.txt` are out of scope.** `AID-2026-054` owns them. Touching them here recreates the merge hazard that produced two divergent baselines.
- **No exemptions.** Not for the three mirrors, not for any of the 66. An exemption list makes a wrong predicate permanent.
- **`13-engineering-decisions/technology-architecture-blueprint.md` stays a violation.** If the new predicate resolves it, the floor is wrong.

## 6. Acceptance criteria

Each is checkable by a reader who does not trust this prompt.

- **AC1** — `python3 scripts/check_bilingual_docs_full.py` reports **9** violations, and the nine are exactly the C list in §2. Not "about 9": the set equality is the criterion.
- **AC2** — The baseline diff is **72 removals, 0 additions**, and the 72 are exactly the A and B classes. `git diff --numstat` on the baseline file shows the shape; the removed set is compared against the two lists.
- **AC3** — The three mirror paths in §3 are no longer violations, and a fourth `.zh-CN.md` mirror added in a test fixture is also not asked for a mirror of itself.
- **AC4** — `13-engineering-decisions/technology-architecture-blueprint.md` is still a violation after the change.
- **AC5** — A file with `cjk = 99` and `latin = 5000` is still a violation, and a file with `cjk = 100` and `latin = 999` is still a violation. Both asserted, not sampled — the floor is inclusive on both sides and a one-sided floor is the failure mode the ruling warns about.
- **AC6** — `NORMATIVE_ROOTS` is byte-identical to its pre-change value, verified by `git diff` on that hunk, and the seven non-existent roots are still listed.
- **AC7** — `python3 scripts/ci/gate_ratchet.py --baseline scripts/ci/baselines/bilingual-docs.txt --format paths --command "python3 scripts/check_bilingual_docs_full.py"` exits 0 with `regressions=0 fixed=0`.
- **AC8** — `python3 -m unittest scripts.test_check_bilingual_docs_full` passes, and the suite grows by at least one test per clause of §4. The existing five tests do not mention `NORMATIVE_ROOTS`, do not mention `08-bmcp-protocol`, and do not mention `.zh-CN.md` siblings; that is why the defects above survived.
- **AC9** — `python3 scripts/check_bilingual_docs.py` still reports `77 frozen, 0 new gaps` with `BASE_SHA`/`HEAD_SHA` set, i.e. gate A is unaffected.

## 7. Risk

R2. The baseline is a shrink-only ratchet, so a wrong predicate does not fail loudly: it either freezes entries that should be enforced, or resolves entries that are not actually bilingual and removes them from enforcement permanently. AC5 exists so the floor is asserted from both sides rather than merely not observed. AC2's "0 additions" exists so a predicate that resolves everything cannot pass.

## 8. Provenance

The 81-entry split, the nine C paths with character counts, the three mirror paths, and the predicted 9 were all produced by calling the repository's own functions at `d40d4e09`. The prediction in AC1 is falsifiable: if the implemented predicate produces anything other than exactly those nine, either the predicate or this analysis is wrong, and the implementer should report which rather than adjust the baseline to match.
