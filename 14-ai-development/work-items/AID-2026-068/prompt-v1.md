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
      last_verification_note: "Every count and line number quoted below was measured on 2026-11-25 against the immutable snapshot of main at a1533c67, including the zero production call sites of publish_prepared and the zero .rs occurrences of publish in bmcp-server."
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

# WO-06 / F6-B — executed instruction

Scope: make the derivative lifecycle reachable in production. Preparations
currently stop at `PreparedHidden` and nothing publishes them, so `Published`,
`Blocked` and `Failed` are statements no production run can falsify. Touch the
three named files and nothing else.

The defect, read at `a1533c67`:

- `crates/memory-storage-sqlite/src/lib.rs:822` defines `publish_prepared`, and
  `:1017` is the only statement that sets `state = 'Published'`. Neither has a
  production caller. The facade method exists at `crates/memory-store/src/lib.rs:135`
  and is called only from `crates/memory-store/src/lib.rs` tests and
  `crates/memory-store/tests/publication_lifecycle_through_facade.rs`.
- The only production caller of `prepare_version` is
  `crates/brain-cli/src/main.rs:227`.
- `crates/bmcp-server/`: `grep -rc 'publish' crates/bmcp-server --include=*.rs`
  returns `0` for every file. The single occurrence in the crate is in
  `Cargo.toml`. There is no read path and no publish path in the server that
  would make a derivative observable to a consumer.
- `crates/memory-compiler/src/admission.rs:1109` issues a canonical commit,
  `:1116` rejects any issuer other than `DEV_BASELINE_ISSUER`, `:1139-1140`
  inserts the `signature` column as the literal empty string, and `:1183`
  validates. Issuer and validator sit on the same production path, so the
  admission "authority" currently certifies itself.
- `crates/memory-compiler/src/admission.rs:1708-1720` is a doc comment block for
  one record kind stacked directly above `struct StoredCanonicalCommit` at
  `:1721`, which is a different record kind. The documentation currently
  describes the wrong struct.

Acceptance asked for, with the observable that settles each:

1. The derivative lifecycle is reachable. Observable: after the change,
   `grep -rn 'publish_prepared' crates/bmcp-server crates/brain-cli --include=*.rs`
   returns at least one production call site, where it returns `0` today.
2. Publication is what makes a version readable. Observable: a test prepares a
   version, asserts `read_version` does not return it, calls the production
   publish path, and then asserts the stored state reads back as `Published`.
   The assertion is on the state read from the database, not on the return value.
3. `Published` cannot be reached by writing the flag. Observable: a test attempts
   publish without a prepared row and fails on the guard at
   `crates/memory-storage-sqlite/src/lib.rs:912` (`state != "PreparedHidden"`).
4. `Blocked` and `Failed` are defined in production terms. Observable: this work
   item names, for each of the three states, the production condition that
   produces it and the command that observes it. If a state remains unreachable,
   that is stated and the criterion is not claimed — the three are not to be
   declared green by definition.
5. The server exposes the entry point. Observable: the `.rs` occurrence count of
   `publish` in `crates/bmcp-server` goes from `0` to at least `1`, and a
   server-level test exercises it end to end.
6. The issuer/validator path is not test-only. Observable:
   `grep -n 'issue_canonical_commit' crates/memory-compiler/src/admission.rs` and
   the call site in `crates/brain-cli/src/main.rs:291` both exist outside
   `#[cfg(test)]`, and `cargo test -p memory-compiler` passes.
7. The misplaced doc block is resolved. Observable: the four-paragraph block at
   `:1708-1720` either documents the function it describes or is moved; the
   struct at `:1721` carries documentation that describes `StoredCanonicalCommit`.

Excluded, and stated as excluded: F6-A (that is WO-05 / AID-2026-067, and it must
land first), the context/tombstone surface (WO-04 / F7), and any change to the
storage error taxonomy (WO-02 / F8).

Honesty constraint that this work item does not discharge: reaching `Published`
in production does not by itself show that publication is *authorised*, because
`signature` is still inserted as `''` at `:1139-1140` and the issuer constant is
still shared. A criterion that observes `Published` without saying which
authority produced it is not acceptance for a trust-boundary claim.

Context that produced the numbers above:

- `grep -rn 'publish' crates/bmcp-server --include=*.rs | wc -l` → `0`.
- `grep -rn 'publish' crates/bmcp-server/Cargo.toml | wc -l` → `1`.
- `grep -rn '\.publish_prepared(' crates --include=*.rs` → no production caller
  outside `crates/memory-store/src/lib.rs` tests.
- `git show a1533c67:crates/memory-compiler/src/admission.rs | sed -n '1109,1145p'`,
  `'1700,1725p'`.
