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
      last_verified_date: "2026-11-25"
      last_verification_note: "This record re-measures, from scratch, the six closures that round 3 asserted without supporting tables, and checks the two blocking items round 3 raised. It states the state at 21279d3b and not the state after the three non-blocking corrections it produced. Round 4 returned APPROVE with no blocking item."
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

# REVIEW-04 — AID-2026-058 manifest.yaml (independent, round 4)

**Reviewer:** this session (`r4b`), which did **not** author the file.
**Reviewed commit:** `21279d3b` (detached worktree `wt-rv058`).
**Independence:** session-level only, under PR-GOVERNANCE-001 §5 as amended by `2eb4e352` (#935). The reviewer shares the same GitHub identity as preceding sessions. **Disclosed, not claimed as organisational independence.**

## VERDICT: APPROVE

Both round-3 blocking items are repaired. Three non-blocking notes follow.

---

## 1. Parse (duplicate-key-detecting loader)

`yaml.SafeLoader` subclass overriding `construct_mapping` to raise `ConstructorError` on any repeated key at the same mapping node (`scratch-untracked/dupcheck_058b.py`).

- **bytes:** 20495
- **top-level keys:** 37
- **duplicate keys:** none
- **`findings` ids:** F5, F1, F2, F3, F4
- **`acceptance_criteria` ids:** AC1, AC2, AC3, AC4, AC5, AC6, AC7
- **`owner_decisions` ids:** OD-23

Note: `findings` is ordered F5 first, then F1–F4. F5 was appended at the head rather than the tail. Parses identically; purely cosmetic.

## 2. Round-3 blocking items

### R3-3 — base distance: REPAIRED

Measured in the worktree:

```
$ git rev-list --count b3a65e54..2fc4a2ff            -> 125
$ git rev-list --count --first-parent b3a65e54..2fc4a2ff -> 40
```

Current sentence (line 168):

> It is 125 commits behind 2fc4a2ff, the commit this finding is measured at; the distance grows with every merge and is not restated here.

125 matches `git rev-list --count`. The string `70` survives only inside the same sentence's retraction clause:

> Corrected at REVIEW-03: this finding previously read '70 commits behind' and also blamed f640ba50, which is an ancestor of the base rather than a later commit, and therefore cannot have falsified anything the prompt was written against.

No live claim asserts 70. Not blocking.

*Non-blocking note N1:* 125 is the all-commits count; the first-parent distance is 40. "commits behind" conventionally means first-parent. The same sentence then says the distance "is not restated here" while restating it. Harmless but internally loose; either drop the number or label it as `--count`.

### R3-4 — f640ba50 causality: REPAIRED

Measured:

```
$ git merge-base --is-ancestor f640ba50 b3a65e54; echo $?  -> 0   (ancestor: earlier)
$ git merge-base --is-ancestor 35f2b078 b3a65e54; echo $?  -> 1   (not ancestor: later)
```

Every sentence containing either hash, quoted:

- line 42 (`prompt_supersession.reason`): "The prompt was written at b3a65e54, and 35f2b078 — branched from the same parent, merged later — added the four INDEX rows its AC1 required to be missing, so AC1 now orders the opposite of what the repository contains." … "Corrected at REVIEW-03: this sentence also cited f640ba50 as a later commit; it is an ancestor of the base and is not a reason to override anything."
- line 145 (comment): "f640ba50 is an ancestor of the base, so it cannot have falsified anything —"
- line 168 (F5): "The commit that falsifies AC1 is 35f2b078, which branched from the same parent and was merged to main afterwards … introduced by 35f2b078." … "35f2b078 is the only falsifier, and it is sufficient."
- line 46 (`why`): "35f2b078 fixed the four rows after the prompt was written."
- line 55 (`why`): "The four entries stopped failing at 35f2b078."

No sentence asserts f640ba50 came after the base. Every mention either states it is an ancestor or records it as a retracted error. Repaired.

## 3. AC5 exception clause

```
$ grep -n "except where AC2 requires a new case" manifest.yaml -> 56
$ grep -n "except where AC2 requires a new case" prompt-v1.md -> 86
```

Manifest line 56 now quotes the clause:

> prompt-v1.md AC5 (the existing suite in scripts/test_check_traceability.py passes unmodified, except where AC2 requires a new case)

Prompt line 86 confirms the source text is verbatim ("passes unmodified except where AC2 requires a new case"). Minor punctuation drift — the prompt has no comma before "except" — irrelevant to meaning.

The `why` (line 58) explains it correctly: the exception "covers adding a case AC2 requires. It does not cover rewriting the assertion already inside `test_missing_registry_is_fail_not_zero_error_incomplete` at line 513, which requires the output to contain 'FAIL TRACEABILITY: …' and which AC2 forbids. That assertion has to change rather than be supplemented." That is the right distinction — the exception authorises an addition, the conflict is a rewrite of an existing assertion. The closing sentence records the round-3 defect explicitly.

## 4. Id reference resolution

| Reference type | Result |
|---|---|
| `AC[0-9]+` | 15×AC1, 10×AC2, 8×AC3, 13×AC4, 6×AC5, 2×AC6, 2×AC7 — all defined. No AC8+. |
| `findings[F…]` | zero bracket-style references. No dangling. |
| `F[0-9]+` | F1–F5 defined; `F7` at line 169 refers to AID-2026-056's F7 (confirmed present: 056 defines F1–F8). Resolves, but unqualified — see N2. |
| `OD-[0-9]+` | OD-23 defined 6×; OD-26 referenced 3× (lines 148, 153, 166) and **not** defined in this file — see N3. |
| `replaced_by` targets | AC1, AC2, AC3, AC4, AC5 texts and `authorization.baseline_content_change` — all exist. No dangling. |

*N2 (informational):* line 169 reads "056 had an equivalent finding (F7)". The reader is inside 058's `findings` block, where F7 does not exist. Write "056's F7" to keep it unambiguous.

*N3 (informational):* OD-26 is cited three times as the authority for staying `DISPATCHED` and for APPROVED being reachable only by an independent reviewer, but `owner_decisions` rests only OD-23. OD-26 is real — it appears as the governing ruling in AID-2026-056 (`manifest.yaml:206,238`, `REVIEW-02-INDEPENDENT.md:48`) and AID-2026-060 (`manifest.yaml:16`). A local restatement, or a pointer to the rulings register, would let this file be read alone. Not blocking: the requirement to keep status frozen is corroborated elsewhere, and OD-23 is the only ruling this work item implements.

---

## Summary

- R3-3: repaired — 125 matches `rev-list --count`; 70 survives only as declared history. (N1)
- R3-4: repaired — `f640ba50` is an ancestor (exit 0), `35f2b078` is the falsifier (exit 1), and both statements say so.
- AC5 clause: restored verbatim in the quotation; `why` states the addition-versus-rewrite distinction correctly.
- Ids: no dangling references. N2 and N3 are clarity items, not defects.

**VERDICT: APPROVE**
