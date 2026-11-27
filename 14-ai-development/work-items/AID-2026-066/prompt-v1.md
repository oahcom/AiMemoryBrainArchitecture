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
      last_verification_note: "Every line number quoted below was read from the immutable snapshot of main at a1533c67 on 2026-11-25; none was carried forward from an earlier round without re-reading."
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

# WO-04 / F7 — executed instruction

Scope: make a `ContextSnapshot` a function of authoritative persisted state, so
that a delivery can be certified by the snapshot itself and so that a forget has
somewhere to be expressed. Touch the six named files and nothing else.

The defect, read at `a1533c67`:

- `crates/memory-context/src/lib.rs:118-131` — `ContextEntry` has eleven fields
  and no lifecycle. `build_context` at `:1570-1583` constructs each field by name
  and drops `candidate.memory_lifecycle`, so `Active` and `Consolidated` produce
  byte-identical entries.
- `crates/memory-context/src/lib.rs:169-178` — `ContextSnapshot` carries
  `context_version`, `entries`, `tombstones`, `operation_records`,
  `rendered_bytes`. No field can state what authoritative state the snapshot was
  built from, so the projection cannot certify itself.
- `crates/memory-context/src/lib.rs:1598-1599` — the only production constructor
  sets `tombstones: Vec::new()` and `operation_records: Vec::new()`. The
  tombstone vocabulary at `:134-149` exists and is never used.
- `crates/brain-cli/src/main.rs:749` — `build_context(identity, 1, ...)`. The
  version is a literal.
- `crates/agent-integration/src/lib.rs:767-769` — `if snapshot.version ==
  applied.version && snapshot == *applied { AlreadyApplied }`. Two different
  business states with identical payload are reported as already applied.

Acceptance asked for, with the observable that settles each:

1. `ContextEntry` carries `memory_lifecycle`, populated from the authority, not
   from a default. Observable: a test asserting that two entries built from
   identical content but different authoritative lifecycle differ in that field.
2. `ContextSnapshot` carries a non-empty `authoritative_state_fingerprint`.
   Observable: the same test asserts non-emptiness, and separately asserts that a
   pre-change serialized fixture still deserializes. "An old file still reads" is
   not the same acceptance as "a new file has a fingerprint", and neither
   substitutes for the other.
3. A1: fixed authoritative state rebuilt twice yields an identical fingerprint.
4. A2: changed Claim content yields a different fingerprint.
5. A3: an `Active` memory that is forgotten yields a successor snapshot that
   contains a tombstone, has no entry for that memory, and has a different
   fingerprint — through the real SQLite path exercised by
   `crates/memory-context/tests/forget_excludes_from_context.rs`. The existing
   `read_current returned no revision` failure (`crates/brain-cli/src/main.rs:713`)
   is the bug, not the acceptance.
6. A4: a forget fence recorded directly in storage changes what the successor
   snapshot shows, with no caller input changed.
7. A5: unchanged caller input plus changed persisted state must not reuse the old
   fingerprint.
8. A6 and A7: `Active → Consolidated` and `Consolidated → Active` are both
   observable, in both directions — not one direction with the other implied.
9. Compatibility is enumerated, not assumed. The serialized surface is
   `ContextSnapshot`, `ContextEntry`, `ContextTombstone`, and the `--out` file
   that `crates/brain-cli/src/main.rs` writes. Every field added to any of the
   four is listed, and unknown-field and missing-field behaviour is stated.

Excluded, and stated as excluded: the mutation cluster frozen by D-3, any
in-place modification of a historical snapshot, a global sequence number, and any
new `REQ01-F10`/`F11`.

One design question this instruction does **not** answer and the implementer must:
**B-4, forget during a pending version.** A tombstone must ship inside the
successor snapshot, but D-3 forbids publishing a second unconfirmed version while
the first is pending. So when a forget happens and v1 is still unconfirmed, the
tombstone has nowhere to go. Answer one of two ways and record the consequence:
queue the forget until the pending version is acknowledged, or allow it to
preempt — and if it preempts, record that D-3 was violated and that an Owner
ruling is required. A registration manifest must not decide this.

Context that produced the numbers above:

- `git show a1533c67:crates/memory-context/src/lib.rs | sed -n '118,131p'`,
  `'169,178p'`, `'1570,1600p'`.
- `git show a1533c67:crates/brain-cli/src/main.rs | sed -n '744,760p'` — the
  second argument to `build_context` is the literal `1`.
- `grep -c 'tombstones: Vec::new()' crates/memory-context/src/lib.rs` returns `1`
  in production code; the repository constructs `ContextSnapshot {` in
  production exactly once, at `:1594`.
