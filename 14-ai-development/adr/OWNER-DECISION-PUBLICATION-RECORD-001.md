---
document_metadata:
  domain: ai-development
  role: decision-record

  lifecycle:
    approval:
      decision_status: Approved
      approver: "Verifier acting as owner proxy, per the standing instruction that a blocking decision with no human available is to be taken and recorded rather than left open."
      decision_date: "2026-11-22"
      approved_version:
        scheme: git
        value: "ef65cb9682ceee41767c8bc14b0be9082e26fc73"
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/adr/OWNER-DECISION-PUBLICATION-RECORD-001.md — the DECIDED line in this document names the decider and the date"
        - "ef65cb9682ceee41767c8bc14b0be9082e26fc73 — the commit that added D8, the last substantive amendment to this decision"
      revocation: null
    evidence_verification:
      verification_status: Unverified
    usage_status: Active
    modification_status: Pending-Reapproval

  authority:
    canonical_status: Canonical
    canonical_scope: "Owner ruling: what the durable publication record is, that the production PublicationAuthority is an adapter reporting those records rather than a decider, and that no flag may be computed, inferred, defaulted or hardcoded."
    canonical_scope_id: ai-development/publication-record
    canonical_scope_keywords:
      - publication-record
      - publication-authority-adapter
      - canonical-commit
      - publication-flags
      - blocked-not-published
    canonical_conflict_status: None
    normative_status: Normative
---

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

> **Amended — see D8.2 below.** The clause requiring `canonical_commit_confirmed` to be reported `false` is **superseded**: D8.2 replaced that literal with a sourced read (`AdmissionPublicationAuthority::canonical_commit_confirmed`, `publication_authority.rs:56-73`, reported at `:132`), because the authoritative issuer D3 was waiting for now exists. The rule as it applies to the other two flags is unchanged — both are still unsourced, and D7.1 keeps `publication_participant_admitted` `false` and forbids building the registry. Read D3's three flags as **two unsourced flags still reported `false`** plus one now sourced.

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

> **Amended — see D7.1 below.** The third bullet's promise of a D-side publication-participant registry is **withdrawn** by D7.1: no such registry is to be built in E until Storage signing, the COC quorum and the I terminal decision exist. The other three bullets stand.

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

### `AdmissionStore` is not the D ledger — settled, not open

The first bullet that stood here recorded a residual risk: that `AdmissionStore`
might be a local test double rather than the D-side ledger, with nothing in the
tree either confirming or contradicting its authority. That risk does not exist.
The module states its own scope, in its own doc comment
(`crates/memory-compiler/src/admission.rs:3-5`):

```
//! This crate implements the E-side lifecycle and a local SQLite admission
//! ledger. It does not claim to be the D-authoritative producer ledger or to
//! provide a cross-service D/Storage visibility transaction.
```

`AdmissionStore` is an E-side local ledger. It is **not** the D-authoritative
producer ledger, and it is not a test double either — it is the durable record E
keeps for itself. The question the bullet left open was answered by the file it
was asking about.

The consequence for D1: the durable publication record named there is a record of
**E's local view**, not a cross-service D/Storage transaction. A future claim that
`publication_receipts` is D-authoritative would contradict the module's own doc
comment; that is a defect in the module documentation to be fixed, not a reading
of it to be adopted.

### What remains open

- If a later spec revision assigns E an independent visibility authority, which
  §8 currently forbids.

The second original bullet — `canonical_commit_confirmed` gaining a producer — is
resolved. It is deleted here and recorded in Amendment D8 below, which names the
producer.

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

## Amendment — D7, taken 2026-11-22 02:52 +08:00

D3 listed `publication_participant_admitted` as "unsourced", and the Consequences
section promised "a D-side publication-participant registry" as a next work item.
Reading the C contract shows that promise was wrong to make at E's level. The flag
does not need a registry. It needs two components that do not exist here.

### The issuer is specified, and it is not local

`docs/en/07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md:137`
(mirrored at `docs/zh-CN/.../phase-3.6-c-submit-...:137`) binds C as follows:

> C MUST NOT invoke a protected provider side effect until the exact participant has
> a quorum-committed `JF10_PREPARE_INTENT_REGISTERED`, a **Storage-signed**
> `PreparedParticipantReceipt` is durably registered as
> `JF10_PREPARED_PARTICIPANT_REGISTERED`, and the I owner-final gate has produced an
> authoritative terminal decision for the exact immutable tuple.

Three issuers, named: a COC quorum, Storage's signature, and I's terminal decision.

### None of the three exists in this workspace

| element | state | measurement |
|---|---|---|
| `JF10_*` states in Rust | absent | `grep -rn "JF10" --include=*.rs crates/` → 0 matches |
| receipt wire shape | candidate only | schema title: "… — **candidate**"; description: "does not select or verify a cryptographic suite, canonicalization profile, key policy, or cross-message owner authority" |
| conformance | none claimed | `08-bmcp-protocol/protocol-index.md:55` → "no dedicated validator or production conformance claim" |
| C-owned conditions | specified, not run | C contract: "C-CO-01..10 and H-JF10-01..10 remain SPECIFIED / NOT RUN" |

### Why a local registry would be the wrong repair

To record `publication_participant_admitted = true`, the system would have to accept
a `PreparedParticipantReceipt` and treat it as admitted. But:

- no key policy exists to verify the "Storage-signed" requirement, and the schema is
  explicitly not a cryptographic profile;
- no quorum exists to establish `JF10_PREPARE_INTENT_REGISTERED`;
- no I terminal decision exists to bind the exact tuple.

A registry written under those conditions would store an unverifiable claim and
report it as an admission. That is a substitute authorization decision, forbidden by
`compiler-stage-contract.md` §8, and it would be strictly worse than `false`: it
would look like a real witness while being a relay for caller assertions. It is the
same defect class D6 removes from the canonical-commit path, one layer down.

### Decision

**D7.1. `publication_participant_admitted` stays `false`, and no publication-
participant registry is to be built in E until Storage signing, the COC quorum and
the I terminal decision exist.** The Consequences section's promise of a D-side
registry is withdrawn by this amendment.

**D7.2. The blocking dependency is recorded as external, with named owners:** COC
(quorum), Storage (signing + durable `JF10_PREPARED_PARTICIPANT_REGISTERED`
registration), I (terminal decision for the exact tuple). E cannot supply any of them.

**D7.3. The protocol index understates this mapping.** `protocol-index.md:68` records
`Storage.PreparedParticipantReceipt` as "Schema-local definition; no separate
normative source mapped in this scoped audit", while C contract line 137 binds it.
The hedge ("in this scoped audit") is honest, but the index is the repo's authority
for *what implements what*, so the row should cite the C contract.

### Consequence

Two of the three missing proof flags are now explained the same way, and neither can
be closed by E: `canonical_commit_confirmed` (D6: contract undefined by D) and
`publication_participant_admitted` (D7: issuer requires Storage signing + COC quorum
+ I decision). `Published` remains unreachable, and now for three named reasons
rather than one vague one. That is the honest converged statement available to E.

## Post-decision factual correction — 2026-11-22

PR #552 and subsequent production integration have superseded the factual premise
stated in "The question that was blocking", namely that `PublicationAuthority` has
no production implementation.

`AdmissionPublicationAuthority` (`crates/memory-compiler/src/publication_authority.rs:50`)
now exists as a production implementation, and `brain-cli` invokes
`MemoryCompiler::compile()` through a non-test execution path
(`crates/brain-cli/src/main.rs:4`, `:246`, `:285`). GAP-07 was closed on
2026-11-22 for production reachability on that evidence.

This correction does not invalidate the historical decision, and it does not
establish that publication authorization is complete. The decision above — what
the durable publication record is — stands unchanged, as does D3 and the D6/D7
findings in this amendment.

The unresolved concerns remain, and are tracked separately under
`GAP-14-PUBLICATION-AUTHORITY-AND-STORE-LIFECYCLE.md`:

1. `MemoryStore` does not expose the production prepare/publish lifecycle
   (GAP-14-A).
2. The three publication flags lack an authoritative issuer under D3 (GAP-14-B).
3. Durable publication-record recovery has not been independently verified
   (GAP-14-C).

The original wording is preserved above rather than rewritten, because a decision
record whose stated premise is silently edited cannot be audited.

## Amendment — D8, taken 2026-11-22, after GAP-12 step 3 landed

Three corrections, all read off `main` at `4a7624da` (the merge of #622, head
`0b446492`).

### D8.1 — `AdmissionStore` is E's ledger, and D1 is read that way

`crates/memory-compiler/src/admission.rs:3-5`:

```
//! This crate implements the E-side lifecycle and a local SQLite admission
//! ledger. It does not claim to be the D-authoritative producer ledger or to
//! provide a cross-service D/Storage visibility transaction.
```

D1's record is therefore E's local view of what it admitted and published, joined
with the storage `PreparedHidden` row. It is not a cross-service D/Storage
visibility transaction and this ADR does not claim it is. The residual risk under
"What would reopen this decision" is withdrawn: it was not an open question, it
was a settled negative that had not been read.

### D8.2 — `canonical_commit_confirmed` has a producer

`D-OWNER-DECISION-CANONICAL-COMMIT-001` froze the contract; #622 implemented it.
The chain, at `4a7624da`:

| step | location |
|---|---|
| issue the record | `AdmissionStore::issue_canonical_commit`, `admission.rs:996` |
| validate it, three outcomes | `AdmissionStore::validate_canonical_commit`, `admission.rs:1069` |
| read it into the flag | `AdmissionPublicationAuthority::canonical_commit_confirmed`, `publication_authority.rs:56-73` |
| report it | `canonical_commit_confirmed,` at `publication_authority.rs:132`, replacing the literal `false` D3 required |

The second bullet under "What would reopen this decision" is deleted rather than
left stale: its condition occurred, and this subsection is where it went. D6.1's
hold is released by the contract it was waiting for — a constructible,
content-bearing reference and a validator for it.

One scope fact belongs with that, because the record is not a production identity:
the issuer is the dev-baseline issuer (`d-owner-proxy/dev-baseline-v1`), described
by its own decision as "an explicit development trust anchor, not a production
cryptographic identity". The flag confirms a dev-baseline record.

### D8.3 — `Published` is still unreachable

`publication_authority.rs:133-139` still reports, D3's comment intact:

```rust
publication_participant_admitted: false,
protected_visibility_authorized: false,
```

`PublicationGate::run` maps either one to `Suppressed` (`lib.rs:646-650`), so a run
with a valid canonical-commit record reports `Suppressed`, never `Published`. The
reason is D7 and D3, unchanged: no Storage signing, no COC quorum, no I terminal
decision, and no E visibility authority.

That is the converged statement after D8: one of the three unsourced flags is
sourced, two are not, and `Published` still requires all eight.
