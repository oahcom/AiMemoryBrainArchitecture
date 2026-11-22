---
document_metadata:
  domain: ai-development
  role: review-report

  lifecycle:
    approval:
      decision_status: Draft
      approver: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-22"
      last_verification_note: "The fifteen roots are quoted from check_bilingual_docs_full.py:14 at main @ 1a7e3cddae and compared against the same tree's top-level directories. The sixteen unscanned files are counted with find under 08-bmcp-protocol and the two docs mirrors."
    usage_status: Active
    modification_status: Unchanged
    supersession:
      supersedes: []
      supersession_reason: null

  authority:
    canonical_status: Non-Canonical
    canonical_conflict_status: None
    normative_status: Informative
---

# GAP-26 — Seven of fifteen normative roots do not exist, so a whole domain was never scanned

**Status:** Open · **Area:** `scripts/check_bilingual_docs_full.py`
**Measured at:** `main` @ `1a7e3cddae`
**Author:** owner delegate under standing instruction (Issue #564, comment 7074302216)

---

## 1. The finding

`check_bilingual_docs_full.py:14` declares fifteen normative roots:

```python
NORMATIVE_ROOTS = {
    "00-governance", "01-system-architecture", "02-domain-model",
    "03-memory-brain", "04-memory-compiler", "05-memory-runtime",
    "06-memory-context", "07-agent-integration", "08-protocols",
    "09-storage-and-index", "10-security-and-governance",
    "11-consistency-and-recovery", "12-testing-and-acceptance",
    "13-engineering-decisions", "14-ai-development",
}
```

The repository has nine of them:

| declared | exists |
|---|---|
| `00-governance` | yes |
| `01-system-architecture` | yes |
| `02-domain-model` | yes |
| `03-memory-brain` | **no** |
| `04-memory-compiler` | yes |
| `05-memory-runtime` | **no** |
| `06-memory-context` | yes |
| `07-agent-integration` | yes |
| `08-protocols` | **no** — the directory is `08-bmcp-protocol` |
| `09-storage-and-index` | **no** |
| `10-security-and-governance` | **no** |
| `11-consistency-and-recovery` | **no** |
| `12-testing-and-acceptance` | **no** |
| `13-engineering-decisions` | yes |
| `14-ai-development` | yes |

Six roots are gone entirely. One is a rename that was never propagated: `08-protocols` became `08-bmcp-protocol`, and the constant still says the old name.

## 2. What that costs

The check is a prefix match:

```python
:65    any(path.startswith(root + "/") for root in NORMATIVE_ROOTS)
:111   if any(path.startswith(root + "/") for root in NORMATIVE_ROOTS):
```

A path under a root that is not in the set is not scanned. So:

```
08-bmcp-protocol/*.md            8 files   never scanned
docs/en/08-bmcp-protocol/*.md    4 files   never scanned by the full check
docs/zh-CN/08-bmcp-protocol/*.md 4 files   never scanned by the full check
```

Sixteen files in a domain the repository treats as normative — `protocol-index.md` is cited by `GAP-22` as the authority for 22 message types — and the full bilingual check has never looked at any of them.

The other five missing roots are names that never existed under those spellings (`03-memory-brain`, `05-memory-runtime`, `09-storage-and-index`, `10-security-and-governance`, `11-consistency-and-recovery`, `12-testing-and-acceptance`). They cost nothing directly because no files sit under them. They cost something else: a reader of the constant concludes the repository has fifteen normative domains, and the number is wrong by seven. That is the same defect as a stale count in a report, in the place reports are generated from.

## 3. Why the gate reports success

The check iterates `NORMATIVE_ROOTS` and filters the file list by prefix. A root with no files contributes zero files, zero pairs, zero errors. It is not distinguished from a root that was scanned and found clean.

This is the third instance this session of one shape, and it is worth naming precisely:

| instance | the gate was | produced |
|---|---|---|
| `GAP-20` §6 | silent about a state | no error line |
| `GAP-25` §3 | degraded about a state | a `note:` line, no `FAIL` |
| **here** | **scoped to a root that does not exist** | **no output at all** |

In all three the absence of an error line meant "not checked", and in all three it was read as "checked and passed". The first two at least emitted a line. This one emits nothing, which is the hardest to notice and the easiest to fix.

## 4. The fix

Two changes, and the second is the one that prevents recurrence.

**(a) Correct the roots.** `08-protocols` → `08-bmcp-protocol`; delete the six that do not exist. Deleting them is not cosmetic — leaving a root in the constant that has no directory makes the constant a wish list rather than an inventory, and the next reader will add files to a directory named in it.

**(b) Fail when a declared root does not exist.** A normative root with no directory is either a typo or a deletion that was not followed through, and both need attention:

```python
missing = sorted(r for r in NORMATIVE_ROOTS if not (REPO_ROOT / r).is_dir())
if missing:
    errors.append(
        "GOV-DOC-001 declared normative root(s) with no directory: "
        + ", ".join(missing)
        + " — a root that does not exist scans nothing and reports clean"
    )
```

Without (b), the same drift happens again the next time a directory is renamed, and it is invisible for exactly as long as nobody greps the constant against `ls`.

## 5. What to expect when (a) is applied

Sixteen files become newly scannable. Some will fail. That is the point, and it means this fix cannot be applied alone as a green-PR change — it needs the same ratchet treatment `gates.yml` already uses for the bilingual scan, or it will turn a passing gate red for reasons that predate it.

The honest sequence is:

1. Add (b) first. It fails immediately on the six dead roots, which is a small, real, fixable failure.
2. Fix the roots and accept that the scan now covers `08-bmcp-protocol`.
3. Measure what the wider scan reports, and ratchet that number rather than expecting zero.

Applying (a) alone produces a red gate with no baseline, which is how a real finding gets reverted.

## 6. What this does not claim

- **Not that the 16 files are untranslated.** They may all be correctly paired. The claim is that nothing checked, not that something is wrong.
- **Not that the six dead roots ever had directories.** `03-memory-brain` and the rest may be names from a planned layout that was never built. Either way the constant should not claim them.
- **Not that `08-protocols` was ever correct.** It may have been renamed before the constant was written. The cost is the same.

## 7. Why this is worth a document

Because it was found by reading a constant against `ls`, and the gate that contains it has been reporting clean. A stale list of roots is the cheapest possible way for a coverage gate to silently stop covering something, and it leaves no trace in the output — no `note:`, no `NOT VERIFIED`, nothing to grep for.

`GAP-25` §4 says a baseline cannot be quoted while `grep -c 'NOT VERIFIED'` is non-zero. This adds the companion rule: **a coverage gate's scope must be checked against the tree it claims to cover, because a root that does not exist produces the same output as a root that is clean.**
