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
      last_verification_note: "The md5 identity and the CJK count are reproduced locally from main @ 1a7e3cddae: three files, one md5 f14149cf7a, zero CJK in each. The five IN_DM01 lines are greps against the gate's own --strict output, not against a summary."
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

# GAP-24 — A zh-CN mirror that is the English file, byte for byte

**Status:** Open · **Area:** `check_bilingual_docs.py`, `governance-register/`
**Measured at:** `main` @ `1a7e3cddae`
**Author:** owner delegate under standing instruction (Issue #564, comment 7074302216)

---

## 1. The finding

`GAP-EXEC-2026-11-22-MEASUREMENT-REPRODUCIBILITY-023.md` exists in three places:

```
14-ai-development/governance-register/GAP-EXEC-...-023.md           md5 f14149cf7a  CJK 0
docs/en/14-ai-development/governance-register/GAP-EXEC-...-023.md   md5 f14149cf7a  CJK 0
docs/zh-CN/14-ai-development/governance-register/GAP-EXEC-...-023.md md5 f14149cf7a  CJK 0
```

Identical md5. Zero CJK characters in the file labelled `zh-CN`.

This is not a translation that is incomplete. It is not a translation at all. The `docs/zh-CN/` copy is the English document, and the bilingual gate passes it because the gate checks that the file **exists**, not that it is in a different language.

## 2. Why the gate passes it

`check_bilingual_docs.py` enforces pairing by path:

```python
:35   PAIR_EXEMPT_PREFIXES = (
:36       "14-ai-development/work-items/",
:37       "14-ai-development/prompts/",
:38       "14-ai-development/adr/",
:39   )
```

`14-ai-development/governance-register/` is **not** in that tuple, so the three-file pair is enforced rather than exempted. The enforcement is:

```
:1028  if source.startswith(PAIR_EXEMPT_PREFIXES): continue
:1030  if source.startswith("14-ai-development/"):
:1031      if Path(source).suffix.lower() not in PAIR_ENFORCED_SUFFIXES: continue
:1033      partner = counterpart_14(source)
:1034      if partner is None:
:1035          errors.append(f"{source} has no resolvable bilingual counterpart ...")
```

`counterpart_14(source)` resolves a path. When it resolves, the check passes. Nothing reads the file.

The gate's own module docstring is honest about this being a coverage gate rather than a quality gate, and `GAP-20` §6 makes the general point: a gate silent about a state is not a gate approving of it. This is the specific instance — a file that satisfies every structural condition of being a translation while containing none of one.

## 3. What the gate cannot check, and what it can

It cannot decide whether prose is a good translation. That is a reviewer's judgment and no script replaces it.

It **can** check two things it currently does not:

**(a) That the pair is not byte-identical.** A translation of a non-trivial document is never byte-identical to its source. If `md5(zh-CN) == md5(source)`, the `zh-CN` file is a copy. This is a one-line check with no false positives worth worrying about: a document short enough to translate to identical bytes is short enough that the check does not matter.

```python
if (REPO_ROOT / chinese).is_file() and (REPO_ROOT / source).is_file():
    if (REPO_ROOT / chinese).read_bytes() == (REPO_ROOT / source).read_bytes():
        errors.append(
            f"GOV-DOC-001 {source}: zh-CN mirror is byte-identical to the source; "
            "a copy is not a translation"
        )
```

**(b) That the `zh-CN` file contains CJK.** Weaker than (a) in one way — a translation can legitimately contain no CJK if it is a table of identifiers — and stronger in another: it catches the case where the mirror is *nearly* the English file with a translated title. The right threshold is not zero but "fewer than the source's code-block content", which is fragile. A simpler rule that holds for this repository: a `zh-CN` file must contain at least one CJK character, and a file that cannot is exempted explicitly with a reason, the same way `PAIR_EXEMPT_PREFIXES` exempts whole directories.

I would apply (a) first. It is unambiguous, it catches this exact defect, and it needs no exemption list.

## 4. The second defect in the same file, which is separate

`GAP-EXEC-...-023.md` also has **no `document_metadata` block** — not the root file, not the `docs/en/` copy, not the `docs/zh-CN/` copy. All three open directly with `# GAP-EXEC-...` and a `**Status:**` line.

That is a plain `DM-01` violation and it is already counted: all three are among the 566 `DM-01` errors at `1a7e3cddae`. Nothing needs to be added for this; it needs the backlog worked.

I separate the two because they are different problems with different fixes and one of them is mine to specify while the other is the backlog's:

| defect | rule | fix |
|---|---|---|
| zh-CN mirror is the English file | none exists — `GOV-DOC-001` passes it | add the byte-identity check (§3a) |
| no metadata on any of the three | `DM-01` | work the 566 backlog |

## 5. A correction to the audit that found this

The audit that surfaced this file reported that the nine files it examined are "**not** in the 566 DM-01 errors — they are unlisted."

That is wrong, and it is wrong in a way worth recording because the audit itself warned against it. All nine are in the 566. Verified:

```
IN_DM01  14-ai-development/work-items/GAP-10-IMPLEMENTATION-FRONTIER.md
IN_DM01  14-ai-development/work-items/GAP-10-IMPLEMENTATION-FRONTIER.zh-CN.md
IN_DM01  14-ai-development/work-items/GAP-12-CANONICAL-COMMIT-UNDEFINED.md
IN_DM01  14-ai-development/work-items/D-OWNER-DECISION-PARTICIPANT-ADMISSION-001.md
IN_DM01  14-ai-development/governance-register/GAP-EXEC-2026-11-22-MEASUREMENT-REPRODUCIBILITY-023.md
```

`grep -c` over the gate's own output finds each path. The audit's `not listed` conclusion came from checking a sample of the output rather than the whole of it, and "not in the part I read" became "not in the list."

This matters beyond the audit: if the nine were genuinely unlisted, the gate would have a hole in its enumeration, which would be a far more serious finding than nine missing blocks. They are listed. The enumeration is complete. The backlog is just large.

## 6. Why this is worth a document

Three lines of Python and one duplicated file. Ordinarily that does not need a write-up.

It needs one because the defect is **invisible to every gate in the repository and was found by a human reading two md5 sums**, and because the natural conclusion — "the zh-CN file is missing" — is the wrong one. The file is present, paired, and passing. A future reader who greps for missing mirrors will not find this, and a future reader who trusts `GOV-DOC-001` green will conclude the translation exists.

The check in §3a is the cheapest possible way to make the next one visible at the moment it is introduced rather than at the moment someone thinks to hash two files.
