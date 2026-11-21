# OWNER-DECISION-PUBLICATION-RECORD-001 — What the durable publication record is

**Status:** DECIDED (owner-proxy decision, 2026-11-22)
**Decided by:** Verifier acting as owner proxy, per the standing instruction that a
blocking decision with no human available is to be taken and recorded rather than
left open.
**Effect:** unblocks GAP-07 Tier-1 item 1. Does not by itself grant publication.
**Supersedes:** nothing. Neither the compiler stage contract nor any prior ADR
names this record, which is why the item was blocked.

## The question that was blocking

GAP-07 and GAP-10 both end at the same sentence: the compiler stage is unreachable
because `PublicationAuthority` has no production implementation, and implementing
it requires first answering *what is the durable publication record*. Nobody had
answered it, so three separate domains (compiler, context, agent-integration) sat
behind one unnamed decision.

That framing was wrong in one respect, and correcting it is most of the decision.

## Finding 1 — the record already exists, in production code

`crates/memory-compiler/src/admission.rs` is **not** a test module. It is declared
`pub mod admission;` at `lib.rs:6`, it is 1388 lines, its only `#[cfg(test)]` is
at line 977, and it is backed by SQLite with five tables:

```
admission_meta(  singleton, fence_generation, protocol_sequence )
producer_registry( producer_id, registered_at, registry_digest )
producer_work(  work_item_id, ... )
dependency_edges( artifact_ref, artifact_version, receipt_json, ... )
publication_receipts( publication_id, artifact_ref, artifact_version,
                      request_digest, receipt_json )
```

`admission.rs:261-292`.

`AdmissionStore::final_publication_gate` (`admission.rs:738`) already does, inside
one `IMMEDIATE` transaction:

1. idempotency by `publication_operation_id` + `request_digest`, returning the
   stored receipt on replay and `IdempotencyConflict` on digest mismatch;
2. `StaleFence` / `StaleProtocol` compare-and-swap against `admission_meta`;
3. producer-work existence check;
4. dependency-closure completeness (`dependency_receipt_ids` must equal the stored
   set exactly, sorted-compared, else `ReceiptMismatch`);
5. a durable `PublicationReceipt` bound to artifact ref, artifact version,
   `fence_generation`, `permission_epoch`, `protocol_sequence` and `visible`;
6. monotonic `protocol_sequence` advancement.

That is a durable publication record. It is not an authority, but the record is
not missing.

**So the decision is not "invent a record". It is "designate this one".**

## Finding 2 — six of the eight proof flags have a source; two have none

`PublicationProof` (`lib.rs:285-294`) carries eight fields. Tracing each one to a
producer outside `memory-compiler/src/lib.rs`:

| proof field | production source | where |
|---|---|---|
| `producer_admitted` | **YES** | `AdmissionStore::is_producer_registered` / `producer_work` row, `admission.rs:449,461` |
| `dependency_closure_complete` | **YES** | `AdmissionStore::dependencies_complete`, `admission.rs:655` |
| `canonical_commit_confirmed` | **NO** | no producer anywhere; `admission_canonical_commit_cursor: Option<OpaqueId>` exists as a request field and is `None` in every construction |
| `storage_prepared_hidden` | **PARTIAL** | the state exists (`publication_preparations.state='PreparedHidden'`, `memory-storage-sqlite/src/lib.rs:111,699`) but no `MemoryStorage` trait method exposes it; `prepare_version` returns `PreparedCommitReceipt` which does not carry state |
| `publication_participant_admitted` | **NO** | zero occurrences outside `lib.rs`; no registry table, no request type |
| `protected_visibility_authorized` | **NO** | zero occurrences outside `lib.rs`; no policy input, no table |

Measured by:

```sh
for f in producer_admitted dependency_closure_complete canonical_commit_confirmed \
         storage_prepared_hidden publication_participant_admitted \
         protected_visibility_authorized; do
  grep -rln "$f" crates/ --include=*.rs | grep -v "memory-compiler/src/lib.rs"
done
```

Four of the six return nothing. Two of those four (`canonical_commit_confirmed`,
`protected_visibility_authorized`) also have no table, no request type and no
spec-doc sentence that defines who issues them.

## Finding 3 — the spec forbids the compiler from inventing the missing ones

`docs/en/04-memory-compiler/compiler-stage-contract.md` §8 lists the required
authority per operation. For the two unsourced flags it says:

| Operation | Required authority | E authority |
|---|---|---|
| PublicationParticipant Admission | D authoritative Fence/Admission | Invoke and preserve exact evidence |
| Protected visibility advancement | Storage and applicable D/I authorization | **No independent authority** |

and then, directly:

> E MUST NOT implement substitute authorization decisions.

So the tempting implementation — an `AdmissionAuthority` that reads
`final_publication_gate`, sets the six available flags from it and hardcodes the
other two to `true` — is **non-conformant**, and it is exactly what the three
test-only authorities already do (`lib.rs:926,945,1335`; each hardcodes
`dependency_closure_complete: true, canonical_commit_confirmed: true` and similar).
Copying that shape into production would convert a visible gap into an invisible
false authorization, which is strictly worse than the current skip notice.

## The decision

**D1. The durable publication record is the `publication_receipts` row written by
`AdmissionStore::final_publication_gate`, joined with the storage
`publication_preparations` row in state `PreparedHidden` for the same publication
identity.** Both already exist. Neither is to be duplicated or re-implemented.

**D2. A production `PublicationAuthority` MUST be an adapter, not a decider.** It
may only report what those two records say. It MUST NOT compute, infer, default or
hardcode any of the eight flags.

**D3. The two unsourced flags (`publication_participant_admitted`,
`protected_visibility_authorized`) and the one partial flag
(`canonical_commit_confirmed`) MUST be reported `false` by the production adapter
until their authoritative issuers exist.** Because `PublicationGate::run`
(`lib.rs:544-562`) maps `false` to `Blocked`, the immediate consequence is:

```
compile() becomes reachable, and returns Ok(Blocked) with disposition preserved.
It does not return Published, and must not pretend to.
```

**D4. `storage_prepared_hidden` MUST be sourced** by adding one read to the
storage port (`MemoryStorage::publication_state(publication_id) -> Option<
PublicationState>` or equivalent), because the state is already durable and
withholding it would force a `false` that is factually wrong. This is the only new
production API the decision authorizes.

**D5. GAP-07 recommendation (b) stays as implemented in #538.** The skip notice
remains printed until D3's blocked path replaces it, and the two must not both be
silent.

## Why this is better than the alternatives

- **Versus leaving it open:** three domains stay blocked behind an unnamed
  question. The question is now named and answered, and the answer was already in
  the tree — it had just never been pointed at.
- **Versus an authority that hardcodes the two flags to `true`:** that is a spec
  violation (§8) and it launders missing authorization into a `Published`
  disposition. A `Blocked` disposition with a named cause is honest and testable.
- **Versus refusing to implement anything until D and I ship the missing
  issuers:** that keeps the compiler unreachable indefinitely, and it also
  prevents the adapter from ever being tested against the two records that *do*
  exist.

## Consequences, stated plainly

- After this decision, `brain compile` will report a **blocked publication**
  rather than a skipped stage. That is progress and it will look like a
  regression to anyone reading only the notice text. The notice text must be
  changed to say which flag blocked it.
- Six of eight flags will be `true` on any realistic input, so the pipeline's
  observable behaviour barely moves. The value is that the gate is now executed
  for real instead of bypassed.
- Two new work items exist as a direct result: implement D4's storage read, and
  implement the D-side publication-participant registry that would let
  `publication_participant_admitted` be sourced.
- Nothing here authorizes `Published`. The first `Published` in production
  requires all eight flags from real issuers.

## What would reopen this decision

- If D's fence/admission authority turns out to be a different component than
  `AdmissionStore` — i.e. if `AdmissionStore` is meant to be a local test double
  rather than the D-side ledger. Evidence to check: whether any other crate is
  designated as the producer registry in `07-agent-integration` or `01-system-architecture`.
  Nothing in the tree currently contradicts treating it as authoritative; nothing
  explicitly confirms it either, which is itself recorded here as a residual risk.
- If `canonical_commit_confirmed` gains a producer (the `admission_canonical_commit_cursor`
  field suggests one was intended).
- If a later spec revision assigns E an independent visibility authority, which
  §8 currently forbids.

## Amendment — D6, taken 2026-11-22 02:35 +08:00, after #552 and #545 landed

D3 treated `canonical_commit_confirmed` as a flag with "no producer". That reason
was wrong, and the error matters: it invites the next person to "just add the
producer the field suggests". There is no producer to add, because the fact it
would produce is undefined by its own owner.

### The contradiction, measured

All four readings are from `444deef1`.

| location | what it says |
|---|---|
| `memory-compiler/src/lib.rs:633-635` | `if producer_request.admission_canonical_commit_cursor.is_none() { return Err(MissingCanonicalCommit) }` |
| `memory-compiler/src/lib.rs:641` | `staging.canonical_commit_confirmed = true;` |
| `memory-compiler/src/publication_authority.rs:103` | `canonical_commit_confirmed: false,` |
| `memory-compiler/src/lib.rs:531` | `if !proof.canonical_commit_confirmed { return Blocked }` |

In one call to `compile()`, the compiler first asserts the commit is confirmed —
it will not proceed otherwise — and then hands the gate a proof that says the
commit is not confirmed. The gate blocks. This is not a conservative default; it
is the same boolean holding opposite values inside a single run.

Because staging *hard-errors* on a missing cursor, the only way to reach the gate
at all is to supply one. So the gate's reachability depends on asserting the fact.

### Where the asserted fact comes from

`admission_canonical_commit_cursor` is a field of `ProducerRegistrationRequest`
(`admission.rs:127-137`), which is caller-supplied and merely persisted by the
ledger. Nothing validates it, and nothing can: there is no canonical-commit record
type to validate against.

The domain says so itself, in its own words (`memory-domain/src/lib.rs:489-500`):

```rust
/// NOT DEFINED: awaiting D. Required placeholder with no invented commit semantics.
/// `pending_d()` is public and any caller can create this placeholder.
pub struct CanonicalCommitRef(());
impl CanonicalCommitRef { pub const fn pending_d() -> Self { Self(()) } }
```

`CanonicalCommitRef` carries no data and `pending_d()` lets any caller mint one.
It is a declared placeholder for a contract its owner has not frozen.

So the honest chain is: caller asserts an opaque cursor → the ledger stores it →
the compiler reads it back and calls it a confirmed canonical commit → the domain
elsewhere says no such contract exists. That is a substitute authorization
decision of exactly the shape `compiler-stage-contract.md` §8 forbids, and it is
the *only* route by which the publication gate is reachable today.

### Decision

**D6.1. `canonical_commit_confirmed` stays `false` in the production adapter until
owner D freezes a canonical-commit contract that provides a constructible,
content-bearing reference and a validator for it.** Not "until a producer exists" —
the apparent producer is a caller assertion, and promoting it would launder an
unvalidated claim into a `Published` disposition.

**D6.2. Staging must stop naming a caller-supplied cursor a confirmed commit.**
Its precondition is renamed to what it actually verifies:
`canonical_commit_cursor_recorded`. The check, the error and every disposition stay
byte-for-byte identical; only the claim shrinks to the evidence.

**D6.3. `ProducerRegistrationRequest::admission_canonical_commit_cursor` must not
be treated as evidence of commit confirmation anywhere in E**, including comments
and doc strings. If it survives as a request field it is documented as unvalidated.

**D6.4. `CanonicalCommitRef::pending_d()` must not appear on any path that feeds
publication authorization.** It is a placeholder affordance, not evidence.

### What D6 does not decide

Whether D delivers the contract, or when. That is D's own frontier, and §8 keeps E
from inventing it. D6 only stops E from pretending the contract already exists.

### Consequence

Behaviour does not change: `compile()` still returns `Ok(Blocked)` naming
`canonical_commit_confirmed`, and `brain-cli` still exits 0. What changes is that
the tree no longer contains a line asserting a fact its own domain refuses to
define. `Published` remains reachable only through a real canonical-commit
contract plus the two participants D3 already names.
