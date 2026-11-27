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
      last_verification_note: "Every line number in the acceptance text was re-read on 2026-11-25 from the immutable snapshot of main at a1533c67; the byte size and digest of this file were measured from the committed blob after the manifest pinned them."
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

# WO-03 / E2 — executed instruction (not yet executed)

Scope: a second `compile` against a store that already holds the memory must
reach Context construction and Delivery instead of dying at the first write.
Three files. No schema migration. No claim that a version was advanced.

## What is actually there, measured at `a1533c67`

| fact | measurement |
|---|---|
| the unconditional write | `crates/brain-cli/src/main.rs:694-696` calls `store.create_memory(...)` on every run, with no read-back and no conflict branch; the error is flattened into `create_memory failed: {error:?}` at `:696` |
| the pass-through that makes it fatal | `crates/memory-store/src/lib.rs:46-55` forwards to the storage port; there is no "already present" path to take |
| why the second run must collide | `crates/memory-storage-sqlite/src/lib.rs:86` declares `memory_id TEXT PRIMARY KEY` on `memories`, so the second insert of the same `memory_id` is a constraint violation |
| the rest of the run that is never reached | `:698-708` `write_revision`, `:711-713` `read_current`, `:747-755` `build_context` (version argument is the literal `1` at `:749`), `:795` `deliver_snapshot` |
| the test that encodes the defect as expected behaviour | `crates/brain-cli/tests/compile_persists_store.rs:271-334`, `a_failed_compile_leaves_no_readable_store_of_its_own`. `:307` compiles a second time, `:308-311` asserts exit code `Some(1)` with the message `re-compiling the same memory into the same store must fail`, and `:313-317` asserts stderr contains `create_memory failed`. The file is 335 lines and holds three tests, at `:144`, `:212` and `:271` |
| the observables the CLI already prints | `crates/brain-cli/src/main.rs:824` `memory-store: create_memory -> write_revision -> read_current succeeded`; `:825-827` `memory-context: build_context produced {n} entr(y/ies)`; `:830` `output: {path} ({n} bytes)` |

The fifth row is the constraint that decides how this work order can be
accepted. A test currently asserts that the second run fails, so "the second run
succeeds" cannot be demonstrated without editing that test. Editing it is the
work, not a side effect of it.

## Acceptance asked for

1. The second `compile` against the same `--store` exits 0, and the other two
   tests in `compile_persists_store.rs` (`:144`, `:212`) still exit 0.
2. The second run is shown to arrive at Context construction and Delivery, not
   merely to survive the first write: its stderr carries all three stage lines
   named above, and the `--out` file it names exists and is non-empty.
3. The read-back / reuse semantics for an existing memory are written down as one
   named rule and asserted by a test that would fail under a different rule. The
   rule must not be implicit in the code path.
4. The store does not accumulate duplicate memory rows: after two compiles of the
   same event, the set of `memory_id` values in `memories` is exactly the one
   identity named in this manifest, asserted through the test's own `read_memory`
   helper rather than through the implementation's return value.
5. A genuine storage failure still fails. The first half of the existing test —
   an unreadable input exits non-zero and creates no `--store` file
   (`:275-299`) — is unchanged, and the post-condition that the surviving
   revision is the compiled one (`:319-333`) still holds.
6. The existing assertion is inverted, not deleted:
   `re-compiling the same memory into the same store must fail` and the
   `create_memory failed` expectation at `:311-317` are replaced by the asserted
   success, because a passing test that pins the defect is the failure mode the
   Round 25 principle names.
7. No schema migration, and no change to
   `crates/memory-storage-sqlite/src/lib.rs:82-136`.
8. Nothing here claims that a version was advanced. The literal `1` passed to
   `build_context` at `crates/brain-cli/src/main.rs:749` is not changed by this
   work order, and no acceptance criterion above asserts a version number.

## Excluded, and stated as excluded

- Version advancement, snapshot change, tombstone delivery and `Delivery`
  acknowledgement. Those are the F7 work order; reaching `build_context` is the
  whole of this criterion, and reaching it is not the same as producing a
  legitimate new version.
- Any change to `memory-context`, `memory-compiler`, `agent-integration` or
  `bmcp-server`.
- Any decision about which error a duplicate create returns. That is WO-02
  (AID-2026-069), and this work order is written to be accept-able only after it.

## Why this is WO-03 and not part of WO-02

`crates/memory-storage/src/lib.rs` has no variant that can mean "already exists",
so a caller that wanted to read the stored revision back had nothing to branch on
and could only match on a message string. WO-02 supplies the distinction; this
work order spends it. The order is not a preference: without the first, the second
can only be implemented by string-matching an error.
