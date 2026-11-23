---
document_metadata:
  domain: domain-model
  role: decision-record

  lifecycle:
    approval:
      decision_status: Approved
      approver: "Project Owner (repository owner), converging under standing instruction"
      decision_date: "2026-11-23"
      approved_version:
        scheme: content-hash
        value: "fd0375e5ace208a2e86ad7096b0d222c2228b309d9829bd84802daa9790e4433"
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "Issue #723 (one issuer string mints both attestations and decisions)"
        - "Issue #724 (main violates GAP-18 §5)"
        - "PR #717 / commit 3d1bd80d (the change that removed the separation)"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-23"
      last_verification_note: "Measured on main @ f82b6367 and on 3d1bd80d via git: attestor.rs absent, I_DEV_BASELINE_ATTESTOR 0 occurrences, I_DEV_BASELINE_ISSUER 22, attestation_authority.rs absent. Contract re-read in GAP-18-AUTHORIZATION-VALIDATOR-REMAINDER §5 and §8, which do state the answer; #723 concluded they did not because it searched only the WORK-ORDER."
    usage_status: Active
    modification_status: Unchanged
    supersession:
      supersedes: []
      supersession_reason: null

  authority:
    canonical_status: Canonical
    canonical_scope: "Owner ruling: attestation and authorization-decision issuer allowlists must stay separate, per GAP-18 §5 and §8. The separation removed by 3d1bd80d is to be restored, not re-decided."
    canonical_scope_id: domain-model/attestor-issuer-separation-ruling
    canonical_scope_keywords:
      - attestor-issuer
      - i-attestations
      - gap-18
      - separation
      - i-dev-baseline-attestor
    canonical_conflict_status: None
    normative_status: Normative
---

# RULING-031 — Attestation and decision issuers stay separate; restore what #717 removed

**Status:** Decided
**Decided at:** `main` @ `f82b6367`
**Raised by:** #723, #724
**Effect:** restores a contract requirement that `3d1bd80d` (#717) removed

---

## 1. The question, and why it looked open

#723 asked whether a single issuer string may mint both `i_attestations` and
`authorization_decisions`, and concluded the contract did not say:

> The separation the contract requires is **the table and its primary key**. It
> introduces exactly one issuer constant, `I_DEV_BASELINE_ISSUER`... So `3d1bd80d`
> is **not violating the contract**... Both are contract-permitted.

That conclusion came from searching `GAP-18-AUTHORIZATION-VALIDATOR-WORK-ORDER.md`,
which is indeed silent. The answer is in the other half of the pair, which #723
did not open.

`GAP-18-AUTHORIZATION-VALIDATOR-REMAINDER.md` §8, line 157, names the deliverable:

> `crates/memory-domain/src/attestor.rs` — `AttestorData`, a three-state
> `IssuedAttestorRef` (`Absent | PendingI | Issued`, the same shape as
> `AuthorizationDecisionRef`), and **`I_DEV_BASELINE_ATTESTOR`, a constant
> separate from `I_DEV_BASELINE_ISSUER` for the §5 reason.**

§5, the "what not to do" list:

> **Do not reuse `DEV_BASELINE_ISSUER` for decisions.** `#662` introduced a
> separate issuer and a separate primary-key namespace (`i_attestations`). That
> separation is the point.

So the contract is not silent. It specifies two constants, names the file they
live in, and states the reason. The question #723 opened is closed by a document
that was already in the tree.

## 2. What main actually does

Measured at `f82b6367`, not from a PR description:

```
$ ls crates/memory-domain/src/attestor.rs
No such file or directory
$ ls crates/memory-compiler/tests/attestation_authority.rs
No such file or directory
$ grep -rn I_DEV_BASELINE_ATTESTOR crates/ | wc -l
0
$ grep -rn I_DEV_BASELINE_ISSUER crates/ | wc -l
22
```

`3d1bd80d` deleted 203 lines of `attestor.rs` and 285 lines of
`attestation_authority.rs`. What replaced them: `authorization.rs` validates
attestations at line 287 against `data.issuer.as_str() != I_DEV_BASELINE_ISSUER`
— the same comparison the decision path uses at line 121.

One string now mints both kinds of record. That is the state §5 forbids, reached
by deleting the file rather than by deciding against it.

## 3. The ruling

**Attestation and authorization-decision issuers stay separate.**
`I_DEV_BASELINE_ATTESTOR` is restored, with a value distinct from
`I_DEV_BASELINE_ISSUER`, and attestation validation compares against it.

The reasoning, stated so the next reader does not have to reconstruct it:

- The primary-key namespaces (`i_attestations` vs `canonical_commits`) stop an
  attestation id being mistaken for a decision id. They cannot stop a record
  being *minted* by the wrong authority — the namespace is a property of the
  table, and both tables accept a write from whichever validator admits it.
- A shared issuer string therefore makes "who issued this" unanswerable from the
  issuer field alone for the two record kinds. With separate strings, an
  attestation carrying the decision issuer is refusable on inspection, which is
  what `the_decision_issuer_is_refused` asserted before it was deleted.
- This is defence in depth over a boundary that already has one layer. The cost
  is one constant and one comparison. The cost of not having it is that the
  second layer must be argued for again by whoever notices its absence — which
  is what #723 and #724 are.

## 4. What #723 got right, and the one place it withdrew too much

Right, and accepted:

- The contract's namespace requirement is the two tables, and that part is met.
- `3d1bd80d` is not a cut corner: 19 attestor/attestation test functions exist
  and the workspace is green. The change implemented real behaviour.
- No exploitable path is claimed, and none is assumed here. `admission.rs` still
  restricts issuance to the dev-baseline literal.

Where the withdrawal went too far: #723 first said deleting
`attestation_authority.rs` removed coverage, then retracted that on #717 after
counting 19 tests in `admission.rs`. The count is right; the inference from it
is not.

```
crates/memory-compiler/src/admission.rs
  issuance_refuses_an_issuer_outside_the_allowlist   -> canonical_commits (decisions)
  validator_rejects_a_record_that_disagrees_with_the_reference -> canonical_commits
```

Every issuer test in that file exercises the **decision** path. The 19 attestor
tests in `agent-integration/tests/delivery_lifecycle.rs` exercise the delivery
lifecycle — `legal_accepted_to_applied_with_matching_attestation`,
`applied_requires_attestation`, and so on — and none of them asserts which
issuer an attestation must carry. So the coverage for *this* property did go
with the file, and the retraction should not have been made.

That distinction is the reason this ruling is a document rather than a comment:
the count 19 is true, "coverage was preserved" is not, and the two were merged
into one sentence.

## 5. What this ruling does not decide

- It does not decide the attestor's *admission* rules, only its issuer identity.
- It does not ask for `3d1bd80d` to be reverted. The behaviour it added is kept;
  one constant and one comparison are restored on top.
- It does not settle the symmetric case of a third record kind later. If one
  arrives, this ruling's reasoning applies: separate table, separate issuer, or
  a written decision that says why not.

## 6. Acceptance

1. `I_DEV_BASELINE_ATTESTOR` exists, distinct from `I_DEV_BASELINE_ISSUER`.
2. Attestation validation compares against `I_DEV_BASELINE_ATTESTOR`.
3. A test asserts an attestation carrying `I_DEV_BASELINE_ISSUER` is refused —
   the assertion `the_decision_issuer_is_refused` made before deletion.
4. `cargo test --workspace --all-targets --no-fail-fast` stays green.
5. #723 and #724 close against this ruling rather than against a PR comment.
