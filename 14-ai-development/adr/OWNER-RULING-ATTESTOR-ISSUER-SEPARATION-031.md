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
      last_verification_note: "Measured on main @ 82e9da113e on 2026-11-23: I_DEV_BASELINE_ATTESTOR remains present and #747 remains merged. The controlling issuer-policy interpretation is the I Owner-proxy Answer 2 in Issue #763 comment #7097007415: two distinct identifiers under one I-controlled trust-authorization policy. The earlier reliance on GAP-18 §5 as authority for issuer separation is withdrawn; §8 is retained as implementation reasoning, not as the source of the issuer-policy decision. The §2.3 dated clarification remains pending its document PR."
    usage_status: Active
    modification_status: Pending-Reapproval
    supersession:
      supersedes: []
      supersession_reason: null

  authority:
    canonical_status: Candidate
    canonical_scope: "Owner ruling: exactly two distinct I development-baseline issuer identifiers are admitted under one I-controlled trust-authorization policy: i-owner-proxy/dev-baseline-v1 for authorization decisions and i-attestor-proxy/dev-baseline-v1 for attestations. The two record families retain separate encodings, records, and validators, per Issue #763 comment #7097007415."
    canonical_scope_id: domain-model/attestor-issuer-separation-ruling
    canonical_scope_keywords:
      - attestor-issuer
      - i-attestations
      - gap-18
      - separation
      - i-dev-baseline-attestor
    canonical_conflict_status: Under-Review
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

## 7. Canonical conflict, recorded after this ruling was published

Two further metadata values follow from the same fact, both forced by
`scripts/check_document_management.py` rather than chosen:

- `canonical_status: Candidate` — DM-11 forbids a document under canonical
  conflict from being `Canonical`.
- `modification_status: Pending-Reapproval` — DM-10 requires it once content
  changes after `approved_version`.

Neither downgrades the ruling's history. §1-§6 remain the approved text; what
changed is that the document now declares itself awaiting re-approval instead of
presenting as settled.

`canonical_conflict_status` is set to `Under-Review`, which is the schema's term
for "conflict recorded, resolution pending"
(`00-governance/architecture-document-metadata.schema.yaml:227-233`; the enum is
`None | Resolved | Under-Review`, so there is no `Conflict` value to use).

This section was added later. Sections 1-6 stand exactly as approved; nothing
above was rewritten. The body records a conflict that was not known when this
ruling was written.

### 7.1 The two statements

**`I-OWNER-DECISION-AUTHORIZATION-DECISION-001.md:139`** — `Status: DECIDED
(owner-proxy decision, development baseline)`, decision date 2026-11-21:

> Attestor data uses a separately named deterministic `AttestationSubjectV1`
> encoding and its own record/validator. **It uses the same I issuer
> allowlist.** E must not substitute `validate_attestor` for
> `validate_authorization_decision`.

**This ruling, §3:**

> Attestation and authorization-decision issuers stay separate.
> `I_DEV_BASELINE_ATTESTOR` is restored, with a value distinct from
> `I_DEV_BASELINE_ISSUER`, and attestation validation compares against it.

`same I issuer allowlist` and `separate issuers` are not the same statement.

### 7.2 Why this ruling did not notice it

Not a judgement call — a coverage gap, and it is measurable:

```text
F=14-ai-development/adr/OWNER-RULING-ATTESTOR-ISSUER-SEPARATION-031.md
$ git show 021f5a3f:$F | grep -c "I-OWNER-DECISION-AUTHORIZATION-DECISION-001"
0
$ git show 021f5a3f:$F | grep -oE "OWNER-[A-Z0-9-]+\.md|GAP-18[A-Z-]+\.md" | sort -u
GAP-18-AUTHORIZATION-VALIDATOR-REMAINDER.md
GAP-18-AUTHORIZATION-VALIDATOR-WORK-ORDER.md
```

`021f5a3f` is `#731`, the commit that introduced this ruling. The count is taken
there deliberately: run against the file as it stands now, `grep -c` returns 2,
because this section names the contract it is reporting the absence of.

§1 of this ruling criticises `#723` for searching only the WORK-ORDER and
missing the other half of the pair. This ruling then did the same thing against
a different pair: it read the two GAP-18 work items and never opened the owner
contract that governs the same two records.

Both cited sources are implementation records, not owner decisions:

```text
$ git log -1 --format="%h %an %ci" 57c918bf   # introduced §5's "do not reuse"
57c918bf oahcom 2026-11-22 18:26:47 +0800
$ git log -1 --format="%h %an %ci" 5b9ac68d   # introduced §8's separate-constant line
5b9ac68d owner-proxy 2026-11-22 21:35:39 +0800
```

Both postdate `OWNER-DECISION-001` (2026-11-21). An implementation log cannot
overrule an owner decision.

§5's sentence is also narrower than it was read as being: `Do not reuse
DEV_BASELINE_ISSUER for **decisions**` takes *decisions* as its subject. Reading
it as a rule about attestations is the same over-extension this ruling already
withdrew once, on `#717`.

### 7.3 Status of the current implementation

`cf8b88fb` (`#747`) implements §3 of this ruling and is merged. `I_DEV_BASELINE_ATTESTOR`
exists at `crates/memory-domain/src/authorization.rs:11`; the three guards and
`the_decision_issuer_is_refused` (`:421`) are live.

That implementation is **not** being reverted, and it is **not** being declared
normatively confirmed. It stands pending the resolution in §7.4. No code change
is authorised by this section.

### 7.3a The implementation is already coupled, and that is not an approval

Reverting the `:1549` guard from `I_DEV_BASELINE_ATTESTOR` to
`I_DEV_BASELINE_ISSUER` fails nine existing tests. Measured on `5283e98e` with
that one line changed, `cargo test -p memory-compiler --lib`:

```text
test result: FAILED. 110 passed; 9 failed; 0 ignored; 0 measured; 0 filtered out
```

```text
admission::tests::attestor_and_decision_ids_are_separate_namespaces
admission::tests::attestor_issuance_accepts_an_identical_replay
admission::tests::attestor_validator_accepts_issued_attestation
admission::tests::attestor_validator_rejects_expected_subject_digest_mismatch
admission::tests::attestor_validator_rejects_issued_at_reference_mismatch
admission::tests::attestor_validator_rejects_malformed_issued_at
admission::tests::attestor_validator_rejects_malformed_subject_digest
admission::tests::attestor_validator_rejects_nonempty_signature
admission::tests::attestor_validator_rejects_subject_digest_reference_mismatch
```

These failures are valid fixtures being rejected by the changed guard,
demonstrating that the guard's position is indirectly constrained by existing
test coverage. This is evidence of implementation coupling, not evidence of I
Owner approval or resolution of the canonical conflict.

The distinction is worth stating because it is the one this document is most
likely to be misread on:

| | What it shows |
|---|---|
| nine tests fail on the revert | the current position is load-bearing for existing fixtures |
| **does not show** | that the position was ever approved, or that the conflict is settled |

An implementation that is expensive to reverse is still an unapproved
implementation. Recording the cost of reversal is not a reason to accept it; it
is a reason not to reverse it casually while §7.4 is open.

The reverse does not hold either. Nine tests passing under the current guard does
not mean the guard is right — `attestor_validator_rejects_unsupported_issuer`
(`admission.rs:2839`) writes `'someone-else'` into the row, which **either**
baseline constant refuses, so it cannot distinguish which constant the guard
compares against. `#767` adds the test that closes that gap; it is held under
§7.4 for the same reason this section exists.

### 7.4 Owner ruling and the required document amendment

The I Owner-proxy answered the issuer-allowlist question on 2026-11-23 in Issue #763, comment #7097007415.

The ruling is that distinct issuer identifiers are permitted under one I-controlled trust-authorization policy. The policy admits exactly two development-baseline identifiers: `i-owner-proxy/dev-baseline-v1` for authorization-decision records and `i-attestor-proxy/dev-baseline-v1` for attestation records. The two record families retain separate deterministic encodings, records, and validators. `I_DEV_BASELINE_ATTESTOR` stays, and PR #747 stands.

The earlier characterization in this section that the layered reading was “plausible and unapproved” is withdrawn. The layered reading is now authorized by the I Owner-proxy ruling cited above. The prior statement that only the I Owner may answer the question is also no longer operative: the question has been answered in that ruling.

The I Owner-proxy ruling does not amend the text of `I-OWNER-DECISION-001 §2.3` by comment. That document must retain its original 2026-11-21 decision text and receive a dated clarification beneath the existing §2.3 paragraph. The clarification must cite Issue #763 comment #7097007415. Until that document amendment merges, §2.3 remains textually unamended; the interpretation governing this decision is the one recorded in the cited Owner-proxy ruling.

This is a section-scoped amendment to the application of `OWNER-DECISION-001 §2.3`, not supersession of the entire Owner Decision document. The relationship is recorded here in the decision text. The `supersedes` metadata remains empty because DM-13 treats each `supersedes` entry as a repository-relative file path and therefore cannot represent a section-level target without declaring the entire source document superseded.

| Item | State |
|---|---|
| `canonical_conflict_status` | `Under-Review` until the dated §2.3 clarification merges and is verified |
| `#747` implementation | stands, normatively confirmed by the I Owner-proxy ruling in Issue #763 comment #7097007415 |
| `OWNER-DECISION-001 §2.3` | original 2026-11-21 text retained; dated clarification required by the 2026-11-23 ruling |
| New issuer identifiers or allowlist members | exactly two identifiers are authorized, one per record family; no third identifier, per-call-site substitute, or expanded allowlist without a new ruling |

The two authorized identifiers remain:

- `i-owner-proxy/dev-baseline-v1` — authorization-decision records
- `i-attestor-proxy/dev-baseline-v1` — attestation records

A future proposal to introduce a third issuer identifier requires a new ruling. The first test for such a proposal must follow the stored-row shape of `attestor_validator_rejects_decision_issuer_on_stored_row` (`admission.rs:2864`): write the proposed issuer into a stored row and assert that the validator refuses it.
