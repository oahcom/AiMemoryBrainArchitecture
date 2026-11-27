---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: content-hash
        value: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-24"
      last_verification_note: "Every measurement in this report was re-taken by the author of the manifest after the review was returned, at main 8e489ec1, not carried over from the reviewing session. The reviewer's own figures were independently reproduced: 77 violations, 9 NORMATIVE_ROOTS with 0 missing, 08-bmcp-protocol present, blueprint 50488 bytes, AID-2026-058's four baseline paths now in INDEX.md. Where the reviewer's number and the re-measured number differed (commit distance behind base), both are stated with the commit they belong to."
    usage_status: Active
    modification_status: Unchanged
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
    source: null
    en: null
    zh-CN: null
---

# AID-2026-056 — Independent review, session-level (OD-25)

**Status:** `COMPLETED` / `REQUEST-CHANGES` / `PRE-DISPATCH`
**Independence basis:** `PR-GOVERNANCE-001` §5 as amended by `2eb4e352` (#935) — independence is a property of the reviewing session, not of the GitHub account.
**Reviewing session:** a newly opened session with no share of the authoring context, no participation in writing this work item or its erratum, and no access to the author's account of it. Conclusions were reached from the repository and from commands it ran itself.
**Authoring session of the reviewed artifacts:** the REQ-05 session (Issue #266).
**Disclosure required by GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036 §3:** the reviewing session and the authoring session carry the **same** GitHub identity (`collaborators = 1`). Independence is asserted at the session level only. This is weaker than human review and weaker than a different model family; the two sessions may share training bias. It is disclosed, not waived.

---

## 1. Verdict

**`REQUEST-CHANGES`.** The work item is not dispatchable as it stands.

The single most consequential finding is not any individual criterion but the state of the package: `manifest.yaml` declares `status: DISPATCHED` while its own `errata[0].status` says `UNAPPLIED — the implementer must read it before starting`. **An implementer who reads only the manifest will implement a defect; an implementer who reads only the erratum will violate the manifest.** Both files are in the same directory and neither says which one wins on a point-by-point basis.

---

## 2. Blocking findings

### B1 — AC6 requires reintroducing a defect that #910 removed

| | |
|---|---|
| Location | `manifest.yaml:92-93` (AC6), `prompt-v1.md` §5 first hard constraint |
| Claim | "`NORMATIVE_ROOTS` is unchanged: same 15 entries, the 7 non-existent roots still listed, `08-bmcp-protocol` still absent." |
| Measured at `8e489ec1` | `NORMATIVE_ROOTS` = **9** entries, **0** missing, `08-bmcp-protocol` **present** |
| Difference | The criterion's pre-state no longer exists. `150fb45e` (#910) removed the seven phantom roots and added the real one. Satisfying AC6 literally means restoring `03-memory-brain`, `05-memory-runtime`, `08-protocols`, `09/10/11/12` — seven directories that do not exist. |

`ERRATUM-01.md` §116-127 already says this and withdraws AC6. The manifest was never updated. **Two mutually exclusive instructions ship in one work item.**

### B2 — AC1 asserts 9 violations; the number is 11, and AC2's arithmetic cannot reach either

| | |
|---|---|
| Location | `manifest.yaml:82-85` |
| Claim | AC1: "exactly 9 violations … set equality". AC2: "72 removals = the 6 side-by-side entries + the 66 embedded-bilingual entries". |
| Measured at `8e489ec1` | baseline **77** entries; embedded-bilingual class **66**; side-by-side entries actually **in the baseline: 0** — all six paths are absent from it; real backlog **11** |
| Difference | 77 − 72 = 5, which is neither AC1's 9 nor the erratum's 11. The six side-by-side paths are not in the baseline, so they cannot be removed from it. AC2's removal set is defined over items that are not there. |

The erratum's AC2′ ("66 removals") is arithmetically consistent; the manifest's "72" is not. The manifest still carries 72.

### B3 — AC5 has a floor on one side only

| | |
|---|---|
| Location | `manifest.yaml:90-91` |
| Claim | "because an inclusive floor fails silently on one side" — and then asserts only the two *negative* cases (`cjk=99/latin=5000`, `cjk=100/latin=999` still violations). |
| Measured | No assertion anywhere that `cjk=100` **and** `latin=1000` must be **resolved**. `grep -rn '1000' scripts/check_bilingual_docs*.py` → **no match**; the predicate does not exist yet. |
| Difference | A predicate that resolves nothing passes AC5 in full. The stated reason ("fails silently on one side") is exactly the failure AC5 fails to cover. A floor written as 101/1001 would resolve none of the intended set and still satisfy every AC5 assertion. |

### B4 — AC8 names a module that does not exist

| | |
|---|---|
| Location | `manifest.yaml:97` |
| Claim | `python3 -m unittest scripts.test_check_bilingual_docs_full` passes. |
| Measured | `ModuleNotFoundError: No module named 'scripts.test_check_bilingual_docs_full'`. The file is `tests/test_check_bilingual_docs_full.py` — a different directory, and not an importable `scripts.` submodule. |
| Difference | The command has never run. Also: prompt §4 says "Three edits, all in `scripts/check_bilingual_docs_full.py`", while the deliverables include tests and a `.github/workflows/gates.yml` comment — the self-description of scope is narrower than the actual scope. |

### B5 — No machine-readable file authorisation

| | |
|---|---|
| Location | `manifest.yaml` — no `authorization` / `scope` / `implementation_write` block |
| Measured | `AID-2026-058/manifest.yaml` has one (six fields, `implementation_write: NOT_GRANTED`). `AID-2026-056` has none; the boundary exists only in prose inside `security_scope`. |
| Difference | The implementer's write boundary is not checkable. Prose is not an authorisation. |

---

## 3. Material findings

### M1 — every premise figure is stale, and the erratum's are right

| figure | manifest | measured `8e489ec1` |
|---|---|---|
| violations | 81 | **77** |
| split | 6 / 66 / 9 | **0 / 66 / 11** |
| `NORMATIVE_ROOTS` | 15 entries, 7 missing | **9 entries, 0 missing** |
| scan totals | 638 in-scope / 199 exempt / 81 | **656 / 205 / 77** |
| blueprint bytes | 49666 | **50488** |
| commits behind base | 13 (per erratum) | **103** at the time of this re-measurement; the reviewer measured 74 earlier the same hour |

The last row is not a discrepancy between two observers — it is the base decaying while the review was in flight. `d40d4e09` is still an ancestor of `main`, so nothing is unbuildable, but the distance is growing and every figure it anchors drifts with it.

### M2 — `ERRATUM-01.md` is 6-for-6 unsynced into the manifest

Each erratum item (A)–(F) checked against manifest fields:

| erratum | what it corrects | present in manifest? |
|---|---|---|
| (A) 77 = 66 + 11 | AC1 "exactly 9" | **no** — AC1 still says 9 |
| (B) two 08-bmcp records added | AC8 test list | **no** |
| (C) three mirrors pair correctly now | AC3 | **no** — AC3 still asserted |
| (D) side-by-side reuse not followed; 932-file agreement is coincidence | deliverable 3 | **no** — the deviation is unrecorded |
| (E) AC6 unsatisfiable | AC6 | **no** — AC6 verbatim |
| (F) control file unchanged | AC4 | partial — byte count 49666 is wrong |

`ERRATUM-01.md` is the more accurate document. The manifest is the one marked `status: DISPATCHED`.

### M3 — `security_scope: None` is being used to answer a different question than the one it answers

`security_scope` describes attack surface. The risk here is **check silence**, not compromise — and the manifest's own `risk_rationale` says so: *"a wrong predicate does not fail loudly."* Those are different axes. `None` correctly says no security review is needed; it does not say no independent review is needed. Conflating them is how a required gate ends up shrinking with nobody assigned to look at the shrinking.

### M4 — the ratchet's documented fail-closed property does not hold at an empty baseline

`scripts/ci/gate_ratchet.py` carries a comment claiming a crash yields zero items and is caught as a stale baseline, "never as a pass". Measured:

```
: > /tmp/empty_base.txt
gate_ratchet.py --baseline /tmp/empty_base.txt --command "python3 -c 'import sys; sys.exit(9)'"
-> baseline=0 current=0 regressions=0 fixed=0 / PASS / exit 0
```

With a non-empty baseline the crash does fail closed (`fixed=77, FAIL`). With an empty one, **a broken gate and a fully passing gate are indistinguishable.** AID-2026-056's entire purpose is to regenerate that baseline. If the regeneration ever emits an empty file — a predicate that resolves everything is precisely the way to get one — the required check goes permanently green and no signal remains.

This is not a defect the implementer introduces; it is a floor that should exist before they start.

### M5 — `OD-22(a)` cannot be verified from the repository

`ERRATUM-01.md:141` quotes it in the grammar of a ruling. `grep -rn 'OD-22'` across the tree returns only the erratum itself. `OD-18` and `OD-23` are likewise present only as quotations inside the manifest. **The rulings this work item implements have no independent recorded original in the repository.** Their content is plausible and consistent across the three quotations, but a reviewer cannot confirm them against a source.

---

## 4. Passed — stated because the negatives matter

- **Authorisation is not borrowed.** `AID-2026-054` `implementation_write` is limited to `scripts/check_bilingual_docs.py` and `scripts/bilingual-baseline.txt`; `AID-2026-051` `gate_behaviour_change: NOT_GRANTED`. AID-2026-056 references neither as a source of write authority, and says so explicitly.
- **The ruling is not treated as a commit.** `OD-18` and `OD-23` are recorded as decisions with constraints, not as permission to edit the tree.
- **Identity and uniqueness hold.** One INDEX row each; `prompt_sha256` and `prompt_bytes` match the actual files byte for byte (`325f567c…`, 10114).
- **`GAP-26` and `GAP-28` are honestly closed.** Both `Resolved by 150fb45e`; the claims were re-measured and hold — 9 roots with 0 missing, and the two baselines byte-identical at 77.
- **AC4's control survives.** `13-engineering-decisions/technology-architecture-blueprint.md` is still a violation at `cjk=0`, so a predicate that resolves everything remains detectable — *provided* AC4 is kept and its byte count fixed.

---

## 5. What this review does not do

- It does not change any file, gate, baseline or predicate. It is a record.
- It does not mark `independent_reviewer` as satisfied in the sense of approving the work. The review is complete and its conclusion is negative; `review.status` becomes `CHANGES_REQUESTED`, not `APPROVED`.
- It does not assert that session-level review is sufficient for this class of change. It asserts that the review was performed under the current rule and that its findings are reproducible.
- It does not resolve the manifest/erratum contradiction by choosing a winner. Choosing is the author's job; the review's job is to say the choice cannot be left implicit in a dispatched work item.
