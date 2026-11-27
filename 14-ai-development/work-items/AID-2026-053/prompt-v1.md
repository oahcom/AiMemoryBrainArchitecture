---
document_metadata:
  domain: ai-development
  steward: "Architecture Governance"
  role: work-record

  lifecycle:
    approval:
      decision_status: Draft
      approver: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-23"
      last_verification_note: "Every figure in §2 was measured at main 86c66ec4 in this session: the two enum declarations and the EvidenceExtension fixture were read from crates/memory-domain/src/lib.rs; the four non-contract EvidenceKind construction sites were enumerated repo-wide with git grep and returned none; the four-arm availability match and the one Unavailable test were read from crates/memory-compiler; and the absence of any persisted Evidence was established by searching for EvidenceExtension in the storage crates, which returns nothing."
    usage_status: Active
    modification_status: Unchanged

  authority:
    canonical_status: Non-Canonical
    canonical_conflict_status: None
    normative_status: Informative

  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# TASK — make the two Evidence enums match §8, and delete the four values nothing constructs

`main` is at `86c66ec4`.

`OWNER-DECISION-EVIDENCE-CONTRACT-001` split register 026: WP-A is blocked on three
undefined contract types, WP-B is not blocked at all. This is WP-B.

WP-B is small, and it is small for a measured reason: the four non-contract
`EvidenceKind` values have **zero construction sites** in the entire repository. They exist
only as variants. So this is not a migration — it is deleting unused variants and adding
the values the contract requires.

---

## 1. Hard constraints

**#0 — Do not touch `crates/memory-domain/src/lib.rs` outside the two enum declarations.**
`Evidence` and `EvidenceExtension` keep every field they have. Field conformance is WP-A,
and WP-A is blocked. A change to `Evidence`'s fields in this PR is out of scope and will be
treated as a scope violation however small it looks.

**#1 — Do not touch `crates/bmcp-protocol/`.** Its `EvidenceKind` is an unrelated enum:
four delivery classes (`FINAL_REQUEST_SUBMITTED`, `APPLIED_CONTEXT_OBSERVED`,
`EXECUTION_STARTED`, `RECONCILIATION_OBSERVED`), in `pub mod evidence`. That crate does not
depend on `memory-domain`, nothing outside it references `evidence::EvidenceKind`, and no
conversion exists anywhere. The two enums share a name and nothing else. Register 026 §7
item 4 asks you to "verify the BMCP protocol mapping"; **there is no mapping to verify**, and
the correct response is to report that, not to create one.

**#2 — Removal is deletion, not renaming.** `Message`, `Record`, `Dataset` and `Other(String)`
are removed. Do not map `Message` to `SourceSpan` on name similarity — §7 explicitly forbids
it, and §5.4 says so twice. If any of these four turns out to have a construction site you
find that the measurement in §2 missed, **stop and report**, do not invent a mapping.

**#3 — `Unavailable` is removed, not split.** See §3. This is the one place a decision was
owed and it has been made for you.

**#4 — Serde must reject, not coerce.** A payload carrying a removed value must fail
deserialization with a clear error. Silently mapping old wire values onto new ones is the
thing §7 item 7 prohibits.

**#5 — Report only commands you actually ran, with real output and real exit codes.**
`NOT RUN` is a valid answer. Do not report a green suite you did not observe.

**#6 — `cargo test -p memory-domain` and `cargo test -p memory-compiler` are your evidence.**
Not the workspace. A local multi-gigabyte `target/` is not a contribution, and CI runs the
workspace.

---

## 2. Measured state at `86c66ec4`

`crates/memory-domain/src/lib.rs`:

```rust
pub enum EvidenceKind {
    Document,
    Message,
    Observation,
    Record,
    Dataset,
    Other(String),
}

pub enum EvidenceAvailability {
    Available,
    Restricted,
    Unavailable,
    Forgotten,
}
```

Neither enum carries a `serde(rename)`. Serde therefore writes `"Document"`, `"Message"`,
and so on.

Construction sites, measured repo-wide:

| value | construction sites |
|---|---|
| `EvidenceKind::Document` | 3 — `memory-domain/src/lib.rs:1700`, `memory-compiler/tests/evidence.rs:48`, `phase2_acceptance.rs:894` |
| `EvidenceKind::Message` | **0** |
| `EvidenceKind::Record` | **0** |
| `EvidenceKind::Dataset` | **0** |
| `EvidenceKind::Other(..)` | **0** |
| `EvidenceAvailability::Available` | 4 |
| `EvidenceAvailability::Restricted` | 3 |
| `EvidenceAvailability::Forgotten` | 3 |
| `EvidenceAvailability::Unavailable` | **1** — `memory-compiler/tests/evidence.rs:243` |

The one non-test match over `availability`, `crates/memory-compiler/src/evidence.rs:142-155`:

```rust
match &entry.extension.availability {
    EvidenceAvailability::Available => AttachmentDecision::Attach,
    EvidenceAvailability::Unavailable => AttachmentDecision::Defer {
        reason: "unavailable: source payload is not retained".into(),
    },
    EvidenceAvailability::Restricted => AttachmentDecision::Defer {
        reason: "restricted: evidence is not currently attachable".into(),
    },
    EvidenceAvailability::Forgotten => AttachmentDecision::Defer {
        reason: "forgotten: source was erased under a forget fence".into(),
    },
}
```

No persisted Evidence anywhere: `EvidenceExtension` appears in no storage crate, there are no
tracked `.db`/`.sqlite` files, and there are no `*.sql` migrations. Nothing is stored that
would need migrating.

---

## 3. The `Unavailable` decision, already made

`Unavailable` is a catch-all. The contract has two states where it has one: `expired` and
`external_unavailable`. Its only interpretation, above, says *"source payload is not
retained"* — which is consistent with **both** and distinguishes neither.

So it cannot be split mechanically, and a split that picked one would be inventing the
distinction it claims to discover.

The ruling, from `OWNER-DECISION-EVIDENCE-CONTRACT-001` §4, is:

1. `Expired` and `ExternalUnavailable` are **added**, because the contract requires both.
2. `Unavailable` is **removed**, not renamed to either.
3. The single construction site — the test at `memory-compiler/tests/evidence.rs:236` named
   `unavailable_evidence_defers_attachment_with_its_reason` — is rewritten to name the state
   it actually means. **You choose which, and you say which and why in the commit message.**
   Either is defensible; picking silently is not.
4. Both new values get a `Defer` arm in `attachment_decision`, with a reason string that
   names the state. `Expired` and `ExternalUnavailable` are not interchangeable reasons: one
   says the source aged out, the other says it was never reachable. Keep them distinct.
5. Serde rejects `"Unavailable"`.

Note the existing test asserts `reason.contains("unavailable")`. That assertion and the
reason string both have to change; a reason that keeps the word "unavailable" in order to
keep the test passing is the wrong direction.

---

## 4. Target state

`EvidenceKind` — exactly the seven contract values, from §8:

```text
source_span, user_statement, document, observation, tool_result, attestation, derived_excerpt
```

`EvidenceAvailability` — exactly the five contract values:

```text
available, restricted, expired, forgotten, external_unavailable
```

Serde representation: §7 item 6 asks for a stable, contract-conforming string form. The
contract writes these values in lowercase snake_case. Use `#[serde(rename_all = "snake_case")]`
on both enums, which produces exactly `"source_span"`, `"external_unavailable"` and so on.
This is a wire-format change; it is safe here **only** because nothing is persisted — if you
find a persisted store you were not told about, stop and report rather than proceeding.

`Other(String)` disappears with the rest. A catch-all that admits arbitrary future values is
precisely what §7 item 7 forbids, and §8's enum is closed.

---

## 5. Acceptance criteria

1. `EvidenceKind` has exactly 7 variants, named for the contract values.
2. `EvidenceAvailability` has exactly 5 variants, and `Unavailable` is gone.
3. `git grep EvidenceKind::Message`, `::Record`, `::Dataset`, `::Other` return nothing.
4. Deserializing a payload with `"Unavailable"`, `"Message"`, `"Record"`, `"Dataset"` or an
   `Other` value **fails**, and a test asserts the failure rather than the absence of a panic.
5. Round-trip test: each of the 7 `EvidenceKind` values and each of the 5
   `EvidenceAvailability` values serializes to its exact contract string and deserializes back.
6. `attachment_decision` covers all five availability values with distinct reasons; the
   compiler proves it is exhaustive.
7. `cargo test -p memory-domain` and `cargo test -p memory-compiler` pass; state the counts.
8. `cargo fmt --check` and `cargo clippy` clean for both crates.
9. `git diff` touches no field of `Evidence` or `EvidenceExtension`, and nothing under
   `crates/bmcp-protocol/`.

---

## 6. What this does not close

`GOV-NC-2026-11-22-EVIDENCE-CONTRACT-026` stays **OPEN**. Its §2 says neither work package
closes it alone, and WP-A is blocked on `Instant`, `Locator` and `ContentRef` having no
definition anywhere. Closing condition 10 also requires formal implementation authorization,
which a dispatch is not.

Register 027 is unaffected: it is about `Provenance`'s reference fields and is dispatched
separately as `AID-2026-052`. If you find yourself editing `Provenance`, you are in the wrong
file.

---

## 7. Provenance

Dispatched by the owner-proxy session that measured the four non-contract `EvidenceKind`
values at zero construction sites, found `bmcp-protocol`'s same-named enum to be unrelated,
and ruled the `Unavailable` split in `OWNER-DECISION-EVIDENCE-CONTRACT-001`. The measurements
are in §2 so you do not have to re-derive them, and §1 tells you which of them to distrust if
the tree has moved.
