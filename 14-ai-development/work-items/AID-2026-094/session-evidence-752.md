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
      last_verification_note: "Every command output below was produced in this session against branch req05/752-attestor, measured on origin/main 3a859ac0 and rebased onto ba5b26b3 before the pull request opened. The code under test is byte-identical on both, because neither base commit touches authorization.rs."
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

# Session evidence — AID-2026-094

## Session role / use case

IMPLEMENTER. This session closed the unvalidated `AttestorData` deserialization
boundary reported in issue #752, chose option 1 of the two the issue offered,
verified the guard by two independent mutations, and recorded the result.

## Actual AI input

The assignment that produced this change, abridged only where it repeated
repository context:

> `AttestorData` is a public struct in `crates/memory-domain/src/authorization.rs`
> with a derived `Deserialize`. Deserializing it directly never calls
> `validate_attestor_data`. So a caller can obtain an `AttestorData` with an
> unsupported issuer and treat it as validated data. `AttestorRef` already has a
> hand-written `Deserialize` ... The bare struct is the hole.
>
> The acceptance criteria from the issue — implement one of these, and say
> which: 1. Make `AttestorData` deserialization invoke the domain validator; or
> 2. Make the unvalidated nature of the type explicit and prevent callers from
> treating bare deserialized data as validated/authoritative.
>
> Preserve existing validated `AttestorRef` behaviour exactly. Its wire form is
> per §2.4: `Pending` is JSON `null`, `Issued` is a flat four-field object. Do
> not change that encoding.
>
> Design constraint ... If you make its `Deserialize` validate, you must check
> what breaks — in particular whether the compiler constructs `AttestorData` by
> deserializing data it later validates itself, and whether any test deserializes
> an intentionally-invalid value to reach `validate_attestor_data`.
>
> Pick the option that is smaller and more honest, not the one that sounds
> stronger. If option 1 forces a parallel unvalidated constructor for the
> compiler's internal use, that is a sign option 2 is the better fit.

## AI-visible output

The output visible to the user is: the diff to
`crates/memory-domain/src/authorization.rs`, the three files in this directory,
one row appended to `14-ai-development/work-items/INDEX.md`, and the pull
request that carries them.

## 1. Which option, and the measurement that decided it

Option 1 — the hand-written `Deserialize` that calls `validate_attestor_data`.

The deciding facts, measured at `origin/main` `3a859ac0` (unchanged on the
`ba5b26b3` base this branch was rebased onto; neither commit touches
`authorization.rs`):

```
grep -rn "AttestorData" --include=*.rs crates/
  crates/memory-compiler/src/admission.rs   (import + one struct-literal construction)
  crates/memory-domain/src/authorization.rs (definition, AttestorRefState, data(), validate, tests)

grep -rn "from_str::<AttestorData|from_slice::<AttestorData|from_value::<AttestorData" crates/
  (no matches)
```

The compiler's single construction site is a struct literal followed
immediately by `AttestorRef::from_issued_data`, which validates. So option 1
needs no unvalidated constructor and adds no public API. Option 2 would need a
newtype or a private field, and either a `pub` accessor (reopening the hole) or
a parallel type threaded through `AttestorRefState` and `admission.rs`.

The test the brief warned about — `attestor_data_rejects_empty_attestation_id`
at `authorization.rs:465` — deserializes an `OpaqueId`, not an `AttestorData`:

```rust
data.attestation_id = serde_json::from_str("\"\"").unwrap();
```

That still compiles and still reaches `validate_attestor_data`, so the test is
unchanged and remains meaningful. No test was deleted or made unreachable.

## 2. The diff

`AttestorData`:

```diff
-#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
+///
+/// Construction by struct literal is unvalidated — that is what
+/// [`AttestorRef::from_issued_data`] is for. **Deserialization is validated**:
+/// `Deserialize` routes through [`validate_attestor_data`], so a value decoded
+/// from bytes cannot carry an unsupported issuer, an empty id, a non-hex digest
+/// or a non-RFC-3339 timestamp. There is deliberately no unvalidated decode path.
+#[derive(serde::Serialize, Clone, Debug, Eq, PartialEq)]
 pub struct AttestorData {
```

New impl, placed directly after `validate_attestor_data`:

```rust
impl<'de> serde::Deserialize<'de> for AttestorData {
    fn deserialize<D: serde::Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        use serde::de::Error;

        let wire = AttestorIssuedWire::deserialize(deserializer)?;
        let data = AttestorData {
            attestation_id: wire.attestation_id,
            issuer: IssuerId::new(wire.issuer)
                .map_err(|error| Error::custom(format!("invalid issuer: {error:?}")))?,
            subject_digest: wire.subject_digest,
            issued_at: wire.issued_at,
        };

        validate_attestor_data(&data)
            .map_err(|error| Error::custom(format!("invalid attestor data: {error:?}")))?;
        Ok(data)
    }
}
```

`AttestorIssuedWire` is the existing private wire struct the `AttestorRef`
visitor already decodes through, so both types accept and reject the same
shapes. `Serialize` is untouched, so the emitted object is byte-identical.

## 3. The tests

Four added to `mod tests`:

| Test | Asserts |
| --- | --- |
| `attestor_data_deserialize_rejects_unsupported_issuer` | `from_str::<AttestorData>` with `issuer: "someone-else"` == `Err("invalid attestor data: InvalidCanonicalCommitField(\"issuer\")")` |
| `attestor_data_deserialize_rejects_empty_attestation_id` | `from_str::<AttestorData>` with `attestation_id: ""` == `Err("invalid attestor data: EmptyId")` |
| `attestor_data_valid_value_round_trips_through_json` | exact flat four-field JSON out, equal value back |
| `attestor_ref_keeps_both_wire_forms` | `null` → pending, flat object → issued, bad-issuer object → `Err` |

## 4. The mutation, verbatim

**Mutation A** — the validator call in `Deserialize` replaced with
`let _ = validate_attestor_data(&data);`, so the decode succeeds unvalidated:

```
$ cargo test --offline -p memory-domain --lib
---- authorization::tests::attestor_data_deserialize_rejects_empty_attestation_id stdout ----

thread 'authorization::tests::attestor_data_deserialize_rejects_empty_attestation_id' (23496) panicked at crates\memory-domain\src\authorization.rs:564:9:
assertion `left == right` failed
  left: Ok(AttestorData { attestation_id: OpaqueId(""), issuer: IssuerId(OpaqueId("i-attestor-proxy/dev-baseline-v1")), subject_digest: OpaqueId("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"), issued_at: "2026-11-22T00:00:00Z" })
 right: Err("invalid attestor data: EmptyId")

---- authorization::tests::attestor_data_deserialize_rejects_unsupported_issuer stdout ----

thread 'authorization::tests::attestor_data_deserialize_rejects_unsupported_issuer' (35480) panicked at crates\memory-domain\src\authorization.rs:551:9:
assertion `left == right` failed
  left: Ok(AttestorData { attestation_id: OpaqueId("attestation-domain-test"), issuer: IssuerId(OpaqueId("someone-else")), subject_digest: OpaqueId("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"), issued_at: "2026-11-22T00:00:00Z" })
 right: Err("invalid attestor data: InvalidCanonicalCommitField(\"issuer\")")

failures:
    authorization::tests::attestor_data_deserialize_rejects_empty_attestation_id
    authorization::tests::attestor_data_deserialize_rejects_unsupported_issuer
test result: FAILED. 91 passed; 2 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.01s
```

**Mutation B** — the hand-written `impl Deserialize` deleted and
`serde::Deserialize` restored to the `#[derive(...)]`, i.e. the pre-fix tree:

```
$ cargo test --offline -p memory-domain --lib
---- authorization::tests::attestor_data_deserialize_rejects_empty_attestation_id stdout ----

thread 'authorization::tests::attestor_data_deserialize_rejects_empty_attestation_id' (9260) panicked at crates\memory-domain\src\authorization.rs:546:9:
assertion `left == right` failed
  left: Ok(AttestorData { attestation_id: OpaqueId(""), issuer: IssuerId(OpaqueId("i-attestor-proxy/dev-baseline-v1")), subject_digest: OpaqueId("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"), issued_at: "2026-11-22T00:00:00Z" })
 right: Err("invalid attestor data: EmptyId")
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace

---- authorization::tests::attestor_data_deserialize_rejects_unsupported_issuer stdout ----

thread 'authorization::tests::attestor_data_deserialize_rejects_unsupported_issuer' (62004) panicked at crates\memory-domain\src\authorization.rs:533:9:
assertion `left == right` failed
  left: Ok(AttestorData { attestation_id: OpaqueId("attestation-domain-test"), issuer: IssuerId(OpaqueId("someone-else")), subject_digest: OpaqueId("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"), issued_at: "2026-11-22T00:00:00Z" })
 right: Err("invalid attestor data: InvalidCanonicalCommitField(\"issuer\")")

failures:
    authorization::tests::attestor_data_deserialize_rejects_empty_attestation_id
    authorization::tests::attestor_data_deserialize_rejects_unsupported_issuer
test result: FAILED. 91 passed; 2 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.01s
```

Both mutations fail exactly the two new tests, with `assert_eq!` expected/actual
pairs, and no other test. Both are assertion failures, not compile errors: the
guard is a runtime call, so weakening it is a runtime no-op rather than a type
error. Restored, the suite is green (section 5).

## 5. Cargo results, restored

```
$ cargo test --offline -p memory-domain
running 93 tests ... test result: ok. 93 passed; 0 failed
running 22 tests ... test result: ok. 22 passed; 0 failed
Doc-tests ...       test result: ok. 3 passed; 0 failed

$ cargo test --offline --workspace --all-targets --no-fail-fast
53 suites, all "test result: ok", 0 failed, 0 "test result: FAILED"

$ cargo clippy --offline --workspace --all-targets -- -D warnings
Finished `dev` profile ... (no warnings)

$ cargo fmt --all -- --check
(no output, exit 0)
```

## 6. Host note

The default `gcc` on `PATH` (`~/.local/bin/gcc.exe`) has no `cc1.exe`, so
`libsqlite3-sys`'s build script cannot compile `sqlite3.c` and every crate that
depends on it fails to build. This is a host defect, not a repository one. The
builds above set `CC`/`AR` to the WinLibs MinGW at
`%LOCALAPPDATA%\Microsoft\WinGet\Packages\BrechtSanders.WinLibs.POSIX.UCRT_*\mingw64\bin`,
which has a working `cc1`. The MSVC toolchain is also installed but links
through a broken `link.exe` wrapper on this host.

## 7. What this record does not claim

- It does not claim the struct literal is validated. It is not; the doc comment
  says so, and `from_issued_data` remains the checked constructor. The claim is
  narrower: **bytes cannot produce an unvalidated `AttestorData`.**
- It does not claim the compiler was changed. `admission.rs` is unmodified
  because its construction site was already validated.
- `executed_prompt_provenance` is `NOT_VERIFIED`: the prompt was written from
  the same measurements as this record but was not re-read line by line against
  the final diff.
