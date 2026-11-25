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
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-25"
      last_verification_note: "The three fold sites, the enum range, the fake-storage implementation and the single-direction assertion were re-read on 2026-11-25 from the immutable snapshot of main at a1533c67; the prompt digest and byte count were computed from the committed file rather than copied from another work item."
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

# Session role / use case

IMPLEMENTER, registration only. Register WO-02 / F8 as an accountable work item
against Issue #262 AC7: a storage contract that reports a duplicate creation and
an invalid reference as one value is a defect with no work item, so AC7 cannot be
evaluated for it.

This session did not write, build or test production code. It wrote three
governance artefacts for this work item and re-measured the code it points at.

# Actual AI input

**Committed, byte-exact.** `prompt-v1.md` in this directory is the instruction
this registration was carried out against. It is the file the manifest pins by
digest (`360c3273a8e6b28cefe583aabe9c5f3d119e94212735c2fae626bbad72816db6`,
6062 bytes).

**Read before writing:**

| input | what it settled |
|---|---|
| the R29 closeout measurement for C3 | `InvalidReference` is declared at `crates/memory-storage/src/lib.rs:11` and `IdempotencyConflict` at `:10`; `AlreadyExists` occurs 0 times under `crates/` |
| the same measurement's line map | the two roles `InvalidReference` already carries, at `crates/memory-storage-sqlite/src/lib.rs:298` (create requires `current_version_id: None`) and `:317` (the `INSERT` collides on the primary key) |
| `facts/r44_ac2_ac4.remeasured.md` | WO-02 is three production files plus one existing test file, and it is ordered before WO-03 |
| `AID-2026-066..068` manifests | the `session_evidence` field set — shape copied, values not |

`executed_prompt_provenance` is `NOT_VERIFIED`: the digest proves the committed
file has not changed since it was pinned, not that it is byte-for-byte what the
executing session read.

Two standing directives governed the session and are reproduced verbatim because
the acceptance text is stated against them:

> 你不应该停下，因为我不输出观点，所有owner都可以是一个会话，你持续到收敛即可。

> 不能自己动手写代码。

# AI-visible output

Three files created, no production file changed:

```
14-ai-development/work-items/AID-2026-069/manifest.yaml
14-ai-development/work-items/AID-2026-069/prompt-v1.md
14-ai-development/work-items/AID-2026-069/session-evidence-r45.md
```

Measurements taken at `a1533c67` and re-read on 2026-11-25:

```
crates/memory-storage/src/lib.rs
    7-21  enum StorageError, 13 variants      no "already exists" value among them
     11   InvalidReference                     the only value a refused write reaches

crates/memory-storage-sqlite/src/lib.rs
  308-309  INSERT INTO memories(...)           where the duplicate row is attempted
    317    .map_err(|_| StorageError::InvalidReference)?   the fold site
    555    the same fold on INSERT INTO versions(...)
    793    the same fold on INSERT INTO publication_preparations(...)
   85-89   memory_id TEXT PRIMARY KEY          why a second insert is a constraint violation

crates/memory-store/src/lib.rs
   46-55   facade pass-through                 no classification of its own
     279   impl MemoryStorage for FakeStorage   the in-memory implementation C3 compares
  419,488  InvalidReference on memory_id mismatch   the genuinely-invalid case

crates/memory-store/tests/cross_crate_contract.rs
    269    Err(...InvalidReference) inside c6   the one direction that is asserted today
```

The last line is what "asserted in one direction only" means concretely: `c6`
pins today's conflation as expected behaviour, which is why C4 requires it to
become two assertions rather than one assertion plus a deletion.

# Limitations

1. **Nothing in this work item is implemented.** `status: DISPATCHED` records
   dispatch, not progress. Every acceptance criterion is a future observable.
2. **C4 is stated as set equality because a count of tests is satisfiable by
   adding an assertion that duplicates an existing one.** The measure is which
   variants the file asserts, in both directions.
3. **`schema_change: NOT_GRANTED` here means no database schema.** A Rust enum
   variant is a source-level contract change and is covered by
   `implementation_write`. Reading the two as the same permission would make the
   manifest claim a grant it does not need and cannot get.
4. **This work item does not make E2 acceptable on its own.** WO-03 (AID-2026-070)
   spends the distinction this one creates; the order is a precondition, not a
   preference.
