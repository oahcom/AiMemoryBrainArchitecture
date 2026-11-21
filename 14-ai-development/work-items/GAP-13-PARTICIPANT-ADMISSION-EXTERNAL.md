# GAP-13 — participant admission is blocked behind Storage signing and COC quorum

**Status:** open · **Severity:** Tier 1 (one of three blockers on `Published`) · **Owner:** Storage, COC, I — not E
**Measured at:** `444deef1` · **Related:** ADR `OWNER-DECISION-PUBLICATION-RECORD-001` (D3, D7), GAP-07, GAP-12

## 1. What is missing

`PublicationProof::publication_participant_admitted` has no issuer. The production
adapter reports it `false` (`publication_authority.rs:104`), and
`PublicationGate::run` then returns `Suppressed` if the other four flags pass
(`lib.rs:540`).

## 2. The issuer is specified

`docs/en/07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md:137`:

> C MUST NOT invoke a protected provider side effect until the exact participant has a
> quorum-committed `JF10_PREPARE_INTENT_REGISTERED`, a Storage-signed
> `PreparedParticipantReceipt` is durably registered as
> `JF10_PREPARED_PARTICIPANT_REGISTERED`, and the I owner-final gate has produced an
> authoritative terminal decision for the exact immutable tuple.

So admission is a three-issuer fact, not a local lookup.

## 3. Measured absence

| element | state | how measured |
|---|---|---|
| `JF10_*` in Rust | absent | `grep -rn "JF10" --include=*.rs crates/` → 0 |
| receipt shape | candidate | schema title says "candidate"; description disclaims crypto suite, canonicalization, key policy and cross-message owner authority |
| validator | none | `protocol-index.md:55` → "no dedicated validator or production conformance claim" |
| C conditions | specified, not run | "C-CO-01..10 and H-JF10-01..10 remain SPECIFIED / NOT RUN" |
| Storage signing key policy | absent | no key custody, rotation or verification code in tree |

## 4. Why E must not build a registry

A registry that stores a `PreparedParticipantReceipt` and reports admission would:

- accept an unverifiable signature as proof of signature;
- accept a claim of quorum as proof of quorum;
- accept a tuple binding as proof of the I decision.

That is a substitute authorization decision (`compiler-stage-contract.md` §8). It is
worse than `false` because it produces a witness-shaped value from a caller
assertion — the same defect class GAP-12 removes from the canonical-commit path.

## 5. What E can and cannot do

- **Cannot:** issue the flag, verify the signature, establish quorum, or bind the
  I decision.
- **Can:** keep the flag `false`; keep the disposition honest (`Suppressed` once the
  other four flags pass); and make the dependency legible so it is not mistaken for
  an E-side implementation gap.

## 6. Closure criteria

1. Storage publishes a signing profile for `PreparedParticipantReceipt`, with key
   custody and rotation, and a verifier E can call.
2. COC exposes a durable `JF10_PREPARE_INTENT_REGISTERED` quorum record for an exact
   participant/operation digest.
3. I exposes an owner-final terminal decision for the exact immutable tuple.
4. Only then: E sources the flag from a verifier, with a test that fails if an
   unsigned or unbound receipt yields `true`.
5. The protocol index row for `Storage.PreparedParticipantReceipt` cites the C
   contract as its normative source (D7.3).

## 7. Note on honesty of the current index

`protocol-index.md:68` says "no separate normative source mapped in this scoped
audit". That hedge is accurate — the audit was scoped — but a reader looking for the
issuer will not find it there. D7.3 asks for the citation, not for a re-audit.
