# FIX-2026-P1-T4-FU1 audit record — documented shape vs shipped checker

- **Work Item:** FIX-2026-P1-T4-FU1
- **Baseline:** `8a1f7e98457873587a564ed49942fa0c39c807ad`
- **Decision:** `DEC-FIX-2026-P1-T4-FU1-GO-001` (coordinator, self-issued — see manifest `authority_note`)
- **Scope:** documentation only; the checker and its 67 tests are unchanged

## 1. How the defects were found

The shipped policy requires every work item to declare evidence depth and to validate the declaration with `scripts/governance/evidence/check-evidence-tiering.py`. The policy also says the checker's per-scenario records — not its exit code — are the acceptance evidence.

So the natural test of the policy is: **take the template's own example declaration, change nothing but the two SHA placeholders, and run the checker.** If the documented shape does not work, the documentation is defective regardless of how the prose reads.

## 2. Defect F-FU1-01 — evidence paths are root-relative, the example is not

The template example wrote evidence paths as bundle-relative names:

```yaml
evidence:
  design_doc: "design.md"
  impact_analysis: "impact.md"
  test_log: "test-report.md"
  review_record: "review-report.md"
  rollback_plan: "rollback.md"
  review_note: "reviewer acknowledgement"
classification_record: "classification.md"
```

With the declaration at `wi/evidence-declaration.yaml` and the files present at `wi/design.md` … the checker returned:

```
VERDICT	BLOCKED
LEVEL	2
REASON	CE_EVIDENCE_NOT_IN_SUBJECT	evidence.design_doc=design.md is not in the subject tree of c9a11d6bce06
REASON	CE_EVIDENCE_NOT_IN_SUBJECT	evidence.impact_analysis=impact.md is not in the subject tree of c9a11d6bce06
REASON	CE_EVIDENCE_NOT_IN_SUBJECT	evidence.review_note=reviewer acknowledgement is not in the subject tree of c9a11d6bce06
REASON	CE_EVIDENCE_NOT_IN_SUBJECT	evidence.review_record=review-report.md is not in the subject tree of c9a11d6bce06
REASON	CE_EVIDENCE_NOT_IN_SUBJECT	evidence.rollback_plan=rollback.md is not in the subject tree of c9a11d6bce06
REASON	CE_EVIDENCE_NOT_IN_SUBJECT	evidence.test_log=test-report.md is not in the subject tree of c9a11d6bce06
REASON	CE_CLASS_RECORD_NOT_IN_SUBJECT	classification_record=classification.md is not in the subject tree of c9a11d6bce06
SUMMARY	change_class=FEATURE	review_level=R2	evidence_level=2	subject_head=c9a11d6bce06	reasons=7
```

The files existed. The reason they were "not in the subject tree" is that `verify_path()` resolves every declared value against the **repository root** (`git cat-file -e <subject>:<path>` and `os.path.join(repo, path)`), while the example implied the declaration's own directory. Adding the `wi/` prefix cleared six of the seven:

```
VERDICT	BLOCKED
REASON	CE_EVIDENCE_NOT_IN_SUBJECT	evidence.review_note=reviewer acknowledgement is not in the subject tree of c9a11d6bce06
SUMMARY	... reasons=1
```

## 3. Defect F-FU1-02 — `review_note` is normative as a path, the example used free text

The seventh reason is the second defect. `LEVEL3_FIELDS = ("review_note",)` is fed through the same `verify_path()` as every other evidence key, so `review_note` is a **path**. The policy listed it as required Level 3 evidence without saying what kind of value it takes, and the template showed a sentence ("reviewer acknowledgement"). A work item copying the example is blocked on a field the prose calls satisfied.

Judgement recorded here: the **checker is right and the prose was wrong**. Accepting free text for one evidence field would create an unbound evidence slot — exactly what the policy's binding-integrity rule forbids. So the fix is documentation, not code.

## 4. What this work item changes

| File | Change |
|---|---|
| `evidence-tiering-policy.md` / `.en.md` | §2 closes the Level 3 row: `evidence.review_note` is a path, not free text; §5 gains item 8: **all evidence paths resolve against the repository root of `subject_head`**, never the declaration directory, and `review_note` must point at an existing acknowledgement record |
| `ai-development-standard.md` | §4.2.1 MUST rule 9, both languages: the same path-base and `review_note` requirement |
| `prompt-and-evidence-template.md` | example now uses root-relative bundle paths and `review_note: ".../review-ack.md"`; the manifest `evidence_tiering` block gains `repository` (policy §4 marks it machine-enforced); both rule lists state the path base |
| `work-items/INDEX.md` | two rows: `FIX-2026-P1-T4` (the #289 registration #289 itself deferred) and this work item |

## 5. Verification (exact commands and outputs)

Positive — corrected example, verbatim, only SHA placeholders replaced, declaration at `14-ai-development/work-items/AID-YYYY-NNN/evidence-declaration.yaml`:

```
$ python scripts/governance/evidence/check-evidence-tiering.py 14-ai-development/work-items/AID-YYYY-NNN/evidence-declaration.yaml
VERDICT	PASS
LEVEL	2
SUMMARY	change_class=FEATURE	review_level=R2	evidence_level=2	subject_head=fe6dd131250f	reasons=0
exit=0
```

Negative — same declaration, `review_note` reverted to free text, to prove the gate did not get weaker:

```
$ python scripts/governance/evidence/check-evidence-tiering.py .....yaml
VERDICT	BLOCKED
LEVEL	2
REASON	CE_EVIDENCE_NOT_IN_SUBJECT	evidence.review_note=reviewer acknowledgement is not in the subject tree of fe6dd131250f
SUMMARY	change_class=FEATURE	review_level=R2	evidence_level=2	subject_head=fe6dd131250f	reasons=1
exit=1
```

Regression — the shipped suite, unchanged, on this head: `Ran 67 tests, OK`.

## 6. Not closed by this work item

- The checker is still not wired into any workflow (`.github/workflows/**` is outside every current allowlist) — the policy therefore has **no automated enforcement**; a manual run is all there is.
- No regression test asserts that the template example passes. Adding one makes the parity self-holding; it needs a `scripts/**` authorization, which this work item deliberately excludes.
- Policy status stays **PROPOSED**; adoption needs a formal adoption record naming the approver, effective date and checker commit SHA.
