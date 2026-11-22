# GAP-12 — the compiler asserts a canonical commit its own domain refuses to define

**Status:** open · **Severity:** Tier 1 (blocks `Published`) · **Owner:** D (contract), E (stop asserting)
**Measured at:** `444deef1` · **Related:** ADR `OWNER-DECISION-PUBLICATION-RECORD-001` (D3, D6), GAP-07, #552

## 1. One sentence

`MemoryCompiler::compile` will not proceed unless a caller-supplied cursor is
present, immediately records that as `canonical_commit_confirmed = true`, and then
asks the publication gate to block because that same flag is `false` — while the
domain declares the underlying contract undefined.

## 2. The four readings

| # | location | text |
|---|---|---|
| 1 | `crates/memory-compiler/src/lib.rs:633` | `if producer_request.admission_canonical_commit_cursor.is_none()` |
| 2 | `crates/memory-compiler/src/lib.rs:634` | `return Err(CompilerError::MissingCanonicalCommit);` |
| 3 | `crates/memory-compiler/src/lib.rs:641` | `staging.canonical_commit_confirmed = true;` |
| 4 | `crates/memory-compiler/src/publication_authority.rs:103` | `canonical_commit_confirmed: false,` |

Line 4 is passed to `PublicationGate::run`, whose check at `lib.rs:531`
(`!proof.canonical_commit_confirmed`) yields `PublicationDisposition::Blocked`.

Observed end to end on `#552`, exit 0:

```
compiler stage blocked: publication not authorized; blocking flag: canonical_commit_confirmed;
false flags: [canonical_commit_confirmed, publication_participant_admitted, protected_visibility_authorized]
```

## 3. Why this is not merely "a flag with no producer"

`admission_canonical_commit_cursor` is a field of `ProducerRegistrationRequest`
(`crates/memory-compiler/src/admission.rs:127-137`). It is caller-supplied. The
ledger persists it and returns it unchanged. Nothing validates it.

Nothing *can* validate it, because the domain states the target contract does not
exist (`crates/memory-domain/src/lib.rs:489-500`):

```rust
/// NOT DEFINED: awaiting D. Required placeholder with no invented commit semantics.
/// `pending_d()` is public and any caller can create this placeholder. It has no
/// canonical-commit meaning until D freezes that contract.
pub struct CanonicalCommitRef(());
impl CanonicalCommitRef { pub const fn pending_d() -> Self { Self(()) } }
```

`CanonicalCommitRef` holds `()`. It has no content and no constructor that
carries evidence; `pending_d()` is a public factory for a meaningless value, and
it is already threaded through `ClaimRevision` fields at `lib.rs:775,793,829,865`.

Therefore:

- the flag cannot be honestly `true` — there is no commit, no record of one, and
  no reference type able to name one;
- the adapter's `false` is not conservatism, it is the only truthful value;
- the staging assignment at line 641 is a substitute authorization decision of the
  shape `compiler-stage-contract.md` §8 forbids.

## 4. The property that makes it Tier 1

Line 2 is a **hard error**, not a disposition. So the publication gate is
reachable only when a caller asserts the cursor. The gate's entire reachability
depends on the assertion it will then refuse.

This is why "just flip the adapter to `true`" is not a fix and must not be
accepted: it would convert an unvalidated caller claim into `Published`, which is
precisely the failure mode D2 exists to prevent.

## 5. Repair, in dependency order

1. **(E, small, behaviour-preserving)** D6.2 — rename staging's precondition to
   `canonical_commit_cursor_recorded`; keep gate flag `false`; keep every
   disposition identical. Removes the contradiction without changing output.
2. **(D, FROZEN — see D-OWNER-DECISION-CANONICAL-COMMIT-001)** Freeze the canonical commit contract: a reference type that
   carries content, a durable record, and a validator. Until then no producer is
   possible and none should be simulated.
3. **(E, NOT AUTHORIZED — superseded by D8)** Keep
   `canonical_commit_confirmed` permanently `false` in the E-side production
   adapter. E MUST NOT source this D-owned `FactRevision` commit flag from a
   cursor, from `StagedDerivative`, or from a validator for a subject absent from
   its production inputs. See `D-OWNER-DECISION-CANONICAL-COMMIT-001.md` D8.
4. **(D, DECIDED — see D-OWNER-DECISION-PARTICIPANT-ADMISSION-001)** Keep
   `publication_participant_admitted` false under the current baseline; §8's D
   authoritative Fence/Admission is not the E-side `AdmissionStore`, and the
   required COC/Storage/I evidence issuers are not implemented.
5. **(I, blocking, independent)** Protected-visibility authority, so
   `protected_visibility_authorized` has an issuer.

Steps 2, 4 and 5 are owned outside E. Step 1 is the only one that can land now.

## 6. Closure criteria

1. No line in `crates/memory-compiler` names a caller-supplied
   `admission_canonical_commit_cursor` as confirmation of anything.
2. `StagingInput` has no field named `canonical_commit_confirmed`; the boolean it
   carries is named for the record it actually checks.
3. A test exists that fails if a caller-supplied cursor alone can produce
   `canonical_commit_confirmed == true` in any `PublicationProof`.
4. `CanonicalCommitRef::pending_d()` appears on no path that feeds
   `PublicationGate`.
5. `compile()` still returns `Ok(Blocked)` naming the flag, and `brain-cli` still
   exits 0 — closure must not change the observable disposition.
6. Steps 2/4/5 are recorded as outstanding with named owners; GAP-12 is not closed
   by step 1 alone.

## 7. What this document does not claim

It does not claim `AdmissionStore` is wrong to store the cursor. Storing an
unvalidated claim is defensible if it is labelled as a claim. The defect is that
the compiler reads it back as a verdict.
