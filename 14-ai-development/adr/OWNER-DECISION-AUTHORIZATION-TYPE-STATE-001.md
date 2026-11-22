---
document_metadata:
  domain: domain-model
  role: decision-record

  lifecycle:
    approval:
      decision_status: Draft
      approver: null
    evidence_verification:
      verification_status: Unverified
    usage_status: Active
    modification_status: Unchanged
    supersession:
      supersedes: []
      supersession_reason: null

  authority:
    canonical_status: Canonical
    canonical_scope: "Owner ruling: absence of an authorization decision must be representable as a distinct state before presence can be validated. Resolves the type-level blocker on dm2_06."
    canonical_scope_id: domain-model/authorization-decision-ref-type-state
    canonical_scope_keywords:
      - authorization-decision-ref
      - type-state
      - absent-placeholder-issued
      - dm2-06
    canonical_conflict_status: None
    normative_status: Normative
---

# OWNER-DECISION-AUTHORIZATION-TYPE-STATE-001 — Absence must be representable before presence means anything

**Status:** DECIDED (owner-proxy decision, 2026-11-22T05:10Z)
**Decided by:** Verifier acting as owner proxy, exercising Owner I, B and D in one session, per the standing instruction that a blocking decision with no human available is to be taken and recorded rather than left open.
**Effect:** unblocks `dm2_06`, the last `#[ignore]` in the workspace. Does not by itself make any publication flag sourceable.
**Supersedes:** nothing. **Amends:** the scope of `B-P2-XO-01`, the framing of `GAP-14-B`, and closure criterion 4 of `GAP-13`.

---

## 1. The question that was actually being asked

`dm2_06` is the last `#[ignore]` in the workspace. Its stated reason:

> `FactRevision::initial` 强制要求 `AuthorizationDecisionRef`，但当前唯一公开构造是 `AuthorizationDecisionRef::pending_i()`；类型没有 absent/validated-I-issued 状态，无法证明缺失授权被拒绝。

`B-P2-XO-01` was filed against a different question:

> What exact domain-side Attestor reference may B store, and what I-issued `AuthorizationDecisionRef` **proves the Attestor is authorized** for this Fact/Scope/Method?

These are not the same question, and conflating them is why `dm2_06` has been blocked for four rounds.

- `B-P2-XO-01` asks: *is this authorization genuine?* That needs I's cryptographic contract, key custody, quorum, and a validator. It is genuinely blocked, and it should stay blocked.
- `dm2_06` asks: *is an authorization present at all?* That needs a type that can represent absence. It needs nothing from I.

The DM2-06 acceptance sentence is exact about which one it is:

> missing or invalid I authorization reference **prevents Fact publication**

"Prevents" is a property of the gate. "Missing" is a property of the value. Neither requires knowing whether a present reference is authentic.

## 2. The measurement that makes this decidable

`crates/memory-domain/src/lib.rs:831` — the `initial` constructor takes authorization as a **required, non-`Option`** parameter:

```rust
pub fn initial(
    ...
    attestor_ref: AttestorRef,
    authorization_decision_ref: AuthorizationDecisionRef,   // not Option<..>
    ...
) -> Result<Self, DomainError>
```

and `AuthorizationDecisionRef` is a unit struct with exactly one public constructor:

```rust
pub struct AuthorizationDecisionRef(());
impl AuthorizationDecisionRef {
    pub const fn pending_i() -> Self { Self(()) }
}
```

`Self(())` carries no state. There is therefore **no value of this type that means "absent"**, and no way for a caller to express one. `FactRevision::initial` cannot be called without producing a value that claims an authorization decision was made.

`validate()` does not compensate: `fact_with_placeholder_attestor_validates_today` (`lib.rs:2196`) pins that the placeholder passes structural validation, with the comment *"Known temporary compromise: structural validation currently accepts the placeholders."*

So the current state is: **every `FactRevision` in existence asserts an I authorization that nobody issued, and the type system prevents anyone from saying otherwise.** That is a stronger defect than the missing test. The missing test is a symptom.

## 3. Decision

**D1. `dm2_06` is not blocked by `B-P2-XO-01`, and must stop being filed under it.** The two questions are separable and were separated incorrectly. `B-P2-XO-01` stays open on its own terms (attestor authenticity). `dm2_06` is unblocked by this decision.

**D2. Absence must be representable before presence can be meaningful.** `FactRevision` gains a three-state authorization field. The states are structural, not cryptographic:

| state | meaning | constructible by |
|---|---|---|
| `Absent` | no authorization decision was recorded | any caller, via a constructor that takes no authorization argument |
| `Placeholder` | a value exists but is known unvalidated (`pending_i()`) | any caller |
| `Issued(AuthorizationDecisionRef)` | a reference claimed to be I-issued | any caller; authenticity is **not** asserted |

**D3. Only `Absent` blocks publication.** `Placeholder` and `Issued` both pass the presence gate, because presence is all this gate can check. This is deliberate: the gate's job is "did someone record an authorization", not "was it real". Asserting the second is `B-P2-XO-01`'s job and I's contract.

**D4. The type must not be nameable as proof.** `Issued` is a *claim* of issuance, and the name must not invite the opposite reading. Acceptable: `Issued`, `ClaimedIssued`, `Referenced`. Not acceptable: `Valid`, `Verified`, `Authorized`. The distinction is the whole point — a name that reads as proof converts an open question into a false answer, which is the defect class `compiler-stage-contract.md` §8 forbids.

**D5. `FactRevision::initial` must keep a constructor that requires authorization**, and gain one that does not. Removing the required-argument constructor would let every existing call site silently become `Absent`, converting a compile-time guarantee into a runtime surprise. The existing 11 call sites keep compiling unchanged; the new constructor is opt-in.

**D6. The presence gate is a domain invariant, not a compiler concern.** `validate()` must reject `Absent` when `outcome == FactOutcome::Attested`. An attested fact with no authorization is the exact thing DM2-06 says must not publish, and it must be rejected where the fact is constructed, not three crates later.

## 4. What `dm2_06` becomes

It stops being `unimplemented!()` and becomes two assertions:

1. `FactRevision` constructed with `Absent` authorization and `FactOutcome::Attested` fails `validate()` with a named error.
2. The same revision with `Placeholder` authorization validates — pinning that presence, not authenticity, is what this gate checks.

The second assertion is the one that keeps the decision honest. Without it, a future reader sees only "absent is rejected" and assumes "present is verified", which is the error this decision exists to prevent.

## 5. What this does not decide

- **Not** whether `pending_i()` should be deprecated. That happens when I ships a real contract, and it is I's call.
- **Not** whether `Placeholder` should be rejected at publication time in some later, stricter gate. It may need to be, once `B-P2-XO-01` closes. This decision deliberately leaves that door open by keeping the states distinct.
- **Not** the authenticity of any `Issued` value. `B-P2-XO-01` owns that, and remains `PENDING CROSS-OWNER DECISION`.

## 6. Consequence for the three publication flags

This decision does not unblock `GAP-14-B`, but it corrects how that item is described. `GAP-14-B` currently reads as *"three flags lack an authoritative issuer, blocked on the D3 decision"*, which implies all three need I's contract. Reading the actual normative sources:

| flag | normative source | what it needs |
|---|---|---|
| `canonical_commit_confirmed` | `OWNER-DECISION-PUBLICATION-RECORD-001` D6.1 | a content-bearing `CanonicalCommitRef` from D — **decision** |
| `publication_participant_admitted` | `07-agent-integration/phase-3.6-c-...md:137` | three-issuer fact: COC quorum + Storage signature + I terminal — **components** |
| `protected_visibility_authorized` | `06-memory-context/context-versioning.md` §13.3 `CV-34` | *"Revalidate current I authorization"* — **decision** |

`GAP-14-B` and ADR-001's table both record `protected_visibility_authorized` as having *"zero occurrences outside `lib.rs`; no policy input, no table"*. That measurement is incomplete, and the reason is instructive. `06-memory-context/context-versioning.md:188` says, in its own words:

> This section is the canonical root-level normative source for G Claim/Fact protected visibility.

and `CV-34` names the requirement: *"Revalidate current I authorization."*

But that file **has no `document_metadata` frontmatter at all** — it is one of the 551 unclassified documents the gate reports. So it *claims* canonical status in prose while being invisible to `resolve_canonical()`, which only reads frontmatter. The measurement in ADR-001 was not careless; it searched for a declared authority and correctly found none. What it missed is that the prose claim exists and disagrees with the machine-readable state.

The correct statement is therefore narrower than "a normative source exists":

- A **prose** normative claim exists (`context-versioning.md` §13.3, `CV-34`).
- No **declared** authority exists for `protected_visibility_authorized`.
- The two disagree, and the disagreement is invisible to the gate because the document is unclassified.

This does not unblock `GAP-14-B`, and it does not change the decision above. It changes what the blocker *is*: not "nobody wrote a spec", but "a spec claims authority the governance layer cannot see". That is a `DM-01` backlog problem colliding with a publication-authority problem, and it should be recorded as such rather than as a missing decision.

## 7. Why this is a decision and not an implementation

The change is small — one enum, one constructor, one validation branch, one test. It is recorded as a decision because the small change settles a question four rounds of work treated as open, and because the *shape* of the change (three states, presence-not-authenticity) is what future work must respect. An implementation note would not bind the next person; a decision does.

The code is not written here. Per the operating constraint, this document authorizes the change and specifies it exactly; writing it is a separate act with its own review.
