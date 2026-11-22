# D-OWNER-DECISION-PARTICIPANT-ADMISSION-001 — Publication participant admission issuer

**Status:** DECIDED (owner-proxy decision; development-baseline and current repository contract)  
**Decided by:** Owner D acting within the D-owned Fence/Admission authority boundary  
**Decision date:** 2026-11-21  
**Baseline:** `7d1a00714aed6e32e7ea4a28f041e15f43cda376`  
**Scope:** GAP-12 §5 step 4; `PublicationProof::publication_participant_admitted`  
**Compatibility:** Phase 1 freeze unchanged; no Rust, schema, public API, or `DomainError` changes.

## 1. Decision

**D decides option A for the current development baseline: `publication_participant_admitted` remains permanently `false` under the existing contract, because the §8 D authority is not the E-side `AdmissionStore`, and no D-side issuer can lawfully establish the required COC-quorum, Storage-signature, and I-terminal evidence; this decision does not prohibit a future, separately approved production integration after those external issuers exist.**

The designated authority boundary is **D authoritative Fence/Admission**, exactly as named in `compiler-stage-contract.md` §8. This names the authority responsible for the admission decision; it does not designate `AdmissionStore` as that issuer and does not create a local dev-baseline substitute.

For the current baseline, no local record, caller assertion, or development trust anchor may make the flag true. The production adapter must continue to report `false`.

## 2. Does §8's "D authoritative Fence/Admission" mean AdmissionStore?

**No.** The phrase in §8 identifies the required D authority boundary, not the concrete E-side SQLite implementation in `crates/memory-compiler/src/admission.rs`.

Evidence at the baseline:

1. The first lines of `admission.rs` describe it as an **E-side lifecycle state and local SQLite admission ledger**, and explicitly state that it "does not claim to be the D-authoritative producer ledger" or a cross-service D/Storage visibility transaction.
2. The schema at `admission.rs:261-292` contains five tables: `admission_meta`, `producer_registry`, `producer_work`, `dependency_edges`, and `publication_receipts`. It contains no publication-participant registry or record.
3. `AdmissionStore::final_publication_gate` at `admission.rs:738` is documented as a local SQLite serialization operation, not a D service API. It checks producer work and dependency closure and persists a local publication receipt; it does not verify COC quorum, Storage signatures, or an I terminal decision.
4. `publication_authority.rs:104` reports `publication_participant_admitted: false`.
5. `OWNER-DECISION-PUBLICATION-RECORD-001.md` D7.1 explicitly withdraws the earlier promise of a D-side publication-participant registry at E's level. D7.2 assigns the missing external dependencies to COC, Storage, and I.

The distinction is substantive: a local producer registry and publication receipt are not a D-issued publication-participant admission. The §8 row is an authority requirement, not proof that the named D authority has been implemented by `AdmissionStore`.

## 3. If yes: the reference type / record / validator

**Not applicable.** The answer in §2 is no, so this decision does not define a local reference type, append-only participant table, or local validator. Defining one in this baseline would contradict D7.1 and would convert external claims into a locally minted authorization witness.

The required evidence chain remains the one specified by the C contract:

- COC quorum evidence for the exact `JF10_PREPARE_INTENT_REGISTERED` participant and immutable operation tuple;
- a Storage-signed `PreparedParticipantReceipt`, durably registered as `JF10_PREPARED_PARTICIPANT_REGISTERED`;
- I's authoritative terminal decision for that exact immutable tuple.

The **admission decision issuer** is the D authoritative Fence/Admission boundary named by §8. COC, Storage, and I are the required upstream evidence issuers; none is interchangeable with D's admission decision. No local dev-baseline issuer is designated.

<!-- OPEN: The repository does not identify a deployed D service endpoint or a concrete D implementation that consumes all three external evidence families. This decision intentionally does not invent one. -->

## 4. If no: why the flag is false under this baseline

The C contract at `docs/en/07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md:137` is explicit:

> C MUST NOT invoke a protected provider side effect until the exact participant has a quorum-committed `JF10_PREPARE_INTENT_REGISTERED`, a Storage-signed `PreparedParticipantReceipt` is durably registered as `JF10_PREPARED_PARTICIPANT_REGISTERED`, and the I owner-final gate has produced an authoritative terminal decision for the exact immutable tuple.

GAP-13 records the following measured absence:

| Required element | Baseline evidence |
|---|---|
| JF10 Rust states | `grep -rn "JF10" --include="*.rs" crates/` → 0 |
| PreparedParticipantReceipt | Candidate schema only; it explicitly does not select a cryptographic suite or key policy |
| Validator | `protocol-index.md:55`: no dedicated validator or production conformance claim |
| C conformance | C-CO-01..10 and H-JF10-01..10 are SPECIFIED / NOT RUN |
| Storage signing key policy | No key custody, rotation, or verification implementation |

A local registry cannot manufacture any of those facts. A dev-baseline issuer such as `d-owner-proxy/dev-baseline-v1` would be a substitute signer for COC, Storage, and I, not merely a development implementation of D's own admission decision. It would contradict the evidence model in C §2 and the withdrawal in D7.1.

Therefore the flag is **permanently false within this baseline and the current contract**. It may be reconsidered only through a new owner decision after the external evidence issuers and D's consuming authority are implemented and verified. This is not a claim that those external systems can never be built.

## 5. Relationship to D7.1

**This decision upholds D7.1; it neither reverses nor narrows it.**

D7.1 withdrew the promise to build a D-side publication-participant registry as an E-level/local repair because the fact requires COC quorum, Storage signing, and I's terminal decision. The present decision adds the missing §8 interpretation:

- `D authoritative Fence/Admission` is the designated D authority boundary.
- `AdmissionStore` is not that boundary; it is explicitly an E-side local ledger.
- A future D implementation may consume the three external evidence families and issue an authoritative admission decision, but no such local substitute is authorized now.
- The D7.1 external dependencies remain prerequisites. No registry is created and no proof flag changes to true.

The earlier wording that the flag remains false "until" the external issuers exist is preserved: their eventual existence is a necessary condition, not an automatic authorization. D must separately verify the exact tuple and make the D-owned admission decision.

## 6. Phase 1 compatibility

This is a documentation-only decision. It does not change:

- `PublicationProof` or its eight fields;
- the Phase 1 frozen contract or `dm2_14` expectations;
- any Rust source, schema, serialization, public API, or `DomainError` variant;
- any observable publication disposition.

**Compatibility conclusion:** the Phase 1 contract is unchanged, so this decision introduces no Phase 1 incompatibility. `dm2_14` was not executable through the available GitHub-only workflow in this decision session; its runtime result is therefore **NOT RUN**, not claimed as a fresh PASS. It must continue to pass unchanged in the normal validation environment.

## 7. What this does not decide

The following remain **OUT-OF-SCOPE (dev-baseline)** and are not approved or simulated here:

- production cryptographic suite, canonicalization, signature verification, key custody, rotation, revocation, or HSM;
- COC quorum algorithm, membership, durable consensus, failover, or operational deployment;
- Storage's production signing profile and durable registration implementation;
- I's owner-final terminal decision implementation;
- D's production adapter/API that consumes the exact three-owner evidence tuple;
- production conformance, interoperability, and end-to-end publication.

**Production replacement path:** COC must expose a verifiable quorum-committed intent for the exact participant/operation digest; Storage must publish and operate a signing/key policy and durably register the signed prepared-participant receipt; I must provide the authoritative terminal decision for the exact immutable tuple; D must then implement the §8 Fence/Admission issuer that validates all three references and exact tuple binding. Only after those gates pass may a future D decision authorize a record-backed validator and permit the production adapter to source `publication_participant_admitted = true`. Missing, stale, unsigned, mismatched, or indeterminate evidence remains false/fail-closed.

## 8. Closure criteria

1. `compiler-stage-contract.md` §8 continues to identify D authoritative Fence/Admission as the required authority; `AdmissionStore` is not described as that authority.
2. `admission.rs` remains unchanged by this decision and continues to identify itself as an E-side local ledger.
3. No local `publication_participants` table, local participant issuer, or dev-baseline shortcut is introduced.
4. `publication_authority.rs` continues to report `publication_participant_admitted: false` until a later authorized integration exists.
5. The C contract's three evidence requirements remain intact; the GAP-13 measured absence is not represented as implementation or conformance.
6. GAP-12 §5 step 4 points to this decision.
7. Phase 1 freeze and `dm2_14` inputs remain byte-for-byte untouched; the normal validation environment records an unchanged `dm2_14` PASS before release.
8. Any future change to true requires a new D decision naming the exact issuer, record, validator, evidence-binding rules, and production verification; this document alone does not authorize it.
