---
document_metadata:
  domain: ai-development
  steward: "Architecture Governance"
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
      last_verification_note: "Every line number quoted below was read from the immutable snapshot of main at a1533c67 on 2026-11-25, including the disposition the gate actually returns for the two hardcoded-false flags, which is Suppressed and not Blocked."
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

# WO-05 / F6-A — executed instruction

Scope: make a refused publication actually refuse. A disposition other than
`Published` must stop the write and the delivery that currently happen anyway,
and the authority's refusal must be produced by an executable path rather than
by two literal `false` values. Touch the three named files and nothing else.

The defect, read at `a1533c67`:

- `crates/brain-cli/src/main.rs:694-705` writes `create_memory` and
  `write_revision` before the gate runs. The gate runs at `:766`
  (`run_compiler_stage`), and delivery runs at `:795` (`deliver_snapshot`).
- `crates/brain-cli/src/main.rs:377` copies `outcome.disposition` into the stage
  outcome. Nothing branches on it. The only consumer is the notice formatter at
  `:135`, so `Blocked` is printed and then ignored.
- `crates/memory-compiler/src/publication_authority.rs:138-139` sets
  `publication_participant_admitted: false` and
  `protected_visibility_authorized: false` with a comment at `:133-137` that says
  these "let the gate return `Blocked`". At `a1533c67` they do not: the branch at
  `crates/memory-compiler/src/lib.rs:653-658` returns `Suppressed` for exactly
  those two flags. The comment and the code disagree; that disagreement is part
  of what this work item has to resolve, because a refusal nobody can name is a
  refusal nobody can test.

Acceptance asked for, with the observable that settles each:

1. A refused publication blocks the upstream write. Observable: a test whose
   authority refuses, then a query on the same SQLite file showing
   `SELECT COUNT(*) FROM memories` is `0`. Asserting the returned disposition is
   not this criterion; the database is.
2. A refused publication blocks delivery. Observable: the same test shows no
   delivery record and no snapshot output file for that run, or the delivery log
   has no `delivery applied` line. Asserting an `eprintln` is not this criterion.
3. The refusal path is executable. Observable: no production `false` literal
   remains for those two flags — `grep -n 'publication_participant_admitted: false'
   crates/memory-compiler/src/publication_authority.rs` returns nothing in
   production code — and a test constructs a refusing authority explicitly.
4. A legal publication still succeeds. Observable: the same suite has a case
   where the authority admits, `run` returns `Published`, the row exists and
   delivery happened. A change that blocks everything fails this criterion, which
   is why it is stated.
5. `Blocked`, `Suppressed` and `Failed` stay distinguishable. Observable: three
   inputs produce the three dispositions, and the existing assertions at
   `crates/memory-compiler/src/lib.rs:1189`, `:1202` and `:1215` still pass.
6. `cargo test -p memory-compiler` and `cargo test -p brain-cli` pass at the
   acceptance head, and moving the write back before the gate makes the new test
   fail — the mutation is performed and recorded, not asserted in prose.

Excluded, and stated as excluded: the derivative lifecycle (that is WO-06 /
F6-B), any change to the storage error taxonomy (WO-02 / F8), and any new
`REQ01-F10`/`F11`. F6 is not green until WO-05 and WO-06 are both green.

Order constraint, from R26 §六 and R29 §7: F6-A must land before F6-B. If F6-B
lands first, the two hardcoded `false` values make every legal publication
refuse, and F6-B cannot be accepted.

Context that produced the numbers above:

- `git show a1533c67:crates/brain-cli/src/main.rs | sed -n '690,800p'` — the
  order is create (`:694`), write (`:698`), gate (`:766`), deliver (`:795`).
- `git show a1533c67:crates/memory-compiler/src/lib.rs | sed -n '609,661p'` —
  the gate's four `Blocked` returns and one `Suppressed` return for the two
  hardcoded flags.
- `git show a1533c67:crates/memory-compiler/src/publication_authority.rs |
  sed -n '128,142p'`.
