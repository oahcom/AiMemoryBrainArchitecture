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
      last_verified_date: "2026-11-26"
      last_verification_note: "Every count below was measured in this session at main b978d9bb, not copied from another record."
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

# AID-2026-081 — Make the ratchet comment's count match its baseline, and check it

## The gap, measured

`.github/workflows/gates.yml` said, above the GOV-DOC-001 ratchet step:

```
# GOV-DOC-001 full scan: 81 normative paths lack an en/zh-CN counterpart.
```

The artifacts that comment describes, measured at `origin/main` `1f5ba824`:

```
scripts/ci/baselines/bilingual-docs.txt              77 lines, 77 entries, 77 unique, no comment header
python3 scripts/check_bilingual_docs_full.py         001. ... 077., then "GOV-DOC-001 full scan: FAIL"
python3 scripts/ci/gate_ratchet.py ...                baseline=77 current=77 regressions=0 fixed=0, PASS
```

So the stated number is wrong by four against both the baseline the ratchet is
handed and the live scan, and nothing in CI compares the prose to either. The
number is not carried by the gate's input; it is carried by a comment.

A second, unrelated file, `scripts/bilingual-baseline.txt`, also exists (79
lines, 77 entries, with a comment header). It is not the file this gate
consumes and this work item asserts nothing about it.

Two rows in `14-ai-development/ci-gates-and-ratchets.{en,zh-CN}.md` still show
`baseline=81 current=81` from a 2026-11-22 rebase measurement. They are
historical measurement records, not current claims, and are left as they are.

## What this work item changes

1. The comment states `77` and names its source: the entry count of
   `scripts/ci/baselines/bilingual-docs.txt`, the file handed to the ratchet
   directly below it.
2. `scripts/ci/test_gate_ratchet.py` — already executed by the
   `Self-check the ratchet wrapper` step in the same job — gains one test that
   extracts the number from that comment and asserts it equals the baseline's
   entry count, where entries are counted the way `gate_ratchet.py` counts
   them: non-blank, non-comment, deduplicated.

The check never runs the wrapped gate. The ratchet is red on main by design
("Red on main, so ratchet rather than gate"), so a check that depended on the
ratchet's verdict would be red with it. This one compares two counts and stays
green.

## Why not the general form

"Compare every prose number in every comment to the artifact it describes" has
no computable answer: most comments describe no machine-readable artifact, and
the mapping from a sentence to a file is not derivable. A test that tried would
either assert nothing or assert a hand-written table that rots the same way.
The narrow form covers the one gate whose comment carries a count and whose
count has already rotted.

## Acceptance criteria

- AC1: the comment reads `77` and names `scripts/ci/baselines/bilingual-docs.txt`.
- AC2: with the comment edited to `81`, `python3 scripts/ci/test_gate_ratchet.py`
  exits 1 and prints `gates.yml says 81 normative paths; bilingual-docs.txt has 77 entries`.
- AC3: on the corrected tree the suite exits 0, whether or not the ratchet is red.
- AC4: an unreadable comment or baseline exits 2 with `INCOMPLETE`, never 1 and never 0.
- AC5: no YAML parser is imported; `gates.yml` is read as text, as
  `scripts/check_session_evidence_workflow_shape.py` reads workflows.
