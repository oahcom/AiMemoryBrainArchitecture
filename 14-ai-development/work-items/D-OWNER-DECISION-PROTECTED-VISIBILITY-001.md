# D-OWNER-DECISION-PROTECTED-VISIBILITY-001 — Protected visibility authorization issuer

**Status:** DECIDED (owner-proxy decision; development-baseline and current repository contract)  
**Decided by:** Owner D acting within the D-owned publication authority boundary  
**Decision date:** 2026-11-21  
**Baseline:** `main @ 6edf116`  
**Scope:** GAP-14-B; `PublicationProof::protected_visibility_authorized`  
**Compatibility:** Phase 1 freeze unchanged; no Rust, schema, public API, or `DomainError` changes.

## 1. Decision

**D decides that `protected_visibility_authorized` remains permanently `false` under the current development baseline and repository contract. The authoritative boundary is the joint Storage and applicable D/I authorization boundary specified by `compiler-stage-contract.md` §8: Storage owns the protected visibility state transition, while the applicable D/I authorities must independently establish their respective authorization conditions. No single local component, including D's owner-proxy development-baseline issuer or E's `AdmissionStore`, may substitute for this joint authority. No authoritative, verifiable, durable authorization record and validator currently exist that can lawfully establish the flag as true. No local issuer, caller assertion, development trust anchor, or delegated shortcut is authorized.**

This decision closes the third question in GAP-14-B for the current baseline.

The decision does not collapse protected visibility authorization into PublicationParticipant Admission. They are independent proof conditions and must remain independently established.

## 2. Issuer identity and authority-boundary analysis

### 2.1 The normative authority is already named

`docs/en/04-memory-compiler/compiler-stage-contract.md` §8 defines:

| Operation | Required authority | E authority |
|---|---|---|
| Protected visibility advancement | Storage and applicable D/I authorization | No independent authority |

The authority assignment is therefore not missing at the normative boundary.

It identifies a composite authority:

1. **Storage** owns the actual protected visibility advancement and the authoritative storage state.
2. **D** supplies the applicable D-owned Fence, lineage, and publication authorization evidence where required by the exact operation.
3. **I** supplies the applicable I-owned authorization decision where required by the exact operation.
4. **E** may invoke the operation and preserve exact evidence, but MUST NOT decide or manufacture authorization.

The phrase "Storage and applicable D/I authorization" MUST NOT be simplified to "D authorization alone", "Storage preparation alone", or "E publication authority".

### 2.2 C's protected-provider contract confirms the cross-owner evidence boundary

`docs/en/07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md`, in the JF-10 prepared-participant / COC bridge binding, requires C not to invoke a protected provider side effect until all of the following exist for the exact immutable operation tuple:

- a quorum-committed `JF10_PREPARE_INTENT_REGISTERED`;
- a Storage-signed `PreparedParticipantReceipt`, durably registered as `JF10_PREPARED_PARTICIPANT_REGISTERED`;
- an authoritative terminal decision from the I owner-final gate.

The same contract preserves D's Fence and lineage obligations, including the exact participant and operation binding.

This confirms that protected operations rely on independent owner evidence. It does not authorize C, E, or a local SQLite ledger to replace those issuers.

The C contract's provider-side-effect requirements are relevant evidence of the cross-owner boundary. They do not, by themselves, define a new local publication-visibility issuer or make provider submission equivalent to publication visibility advancement.

### 2.3 These authorities are not existing local implementations

None of the following is equivalent to the required composite authority:

- `AdmissionStore` in `crates/memory-compiler/src/admission.rs`;
- `AdmissionPublicationAuthority`;
- `d-owner-proxy/dev-baseline-v1`;
- a local boolean or request field;
- a test-only publication authority.

`AdmissionStore` is an E-side local SQLite lifecycle ledger. Its publication receipt and producer/dependency records do not establish Storage's protected visibility decision or the applicable D/I authorization.

A local record that merely stores an assertion that visibility was authorized would not become authoritative by being durable.

## 3. Record, type, and validator

**Not applicable under this baseline.**

No local authorization record, reference type, table, or validator is designated by this decision.

The current repository does not provide a complete authoritative chain that can establish all required facts:

| Required evidence | Authority | Current limitation |
|---|---|---|
| Exact Storage publication preparation and protected visibility state | Storage | Storage owns the state, but the required cross-owner authorization record and complete validation chain are not available to E |
| Applicable D Fence/lineage authorization | D | No complete local publication-visibility issuer is established |
| Applicable I owner-final authorization | I | No local substitute may issue or infer the decision |
| Exact tuple binding across owner evidence | Applicable owners / coordinator | The C contract specifies the cross-owner evidence requirements, but does not establish a complete local production validator |
| Composite authorization consumed by the compiler | Storage and applicable D/I authorities | No authoritative local record and validator |

The existing `publication_receipts` and `publication_preparations` records are not a substitute for the required authorization.

A record describing `PreparedHidden` proves a preparation state. It does not prove permission to advance protected visibility.

Likewise, a publication receipt, COC intent, I decision, D clearance, or Storage receipt considered individually MUST NOT be promoted into the complete composite authorization.

No new table, local issuer, reference type, or validator is authorized by this decision.

## 4. Why the flag must remain false

The current baseline has no legitimate way to establish `protected_visibility_authorized = true`.

The reasons are:

1. `OWNER-DECISION-PUBLICATION-RECORD-001` D3 records zero occurrences of `protected_visibility_authorized` outside `crates/memory-compiler/src/lib.rs`, with no policy input or table.
2. `compiler-stage-contract.md` §8 explicitly assigns protected visibility advancement to Storage and applicable D/I authorization, while denying E independent authority.
3. The C JF-10 bridge requires independent COC, Storage, and I evidence for protected operations. Its specified evidence chain cannot be replaced by a local assertion.
4. The E-side `AdmissionStore` does not own Storage visibility or I authorization.
5. No complete local record and validator bind the required owner evidence to the exact publication tuple.
6. No delegation instrument authorizes a local development issuer to act for Storage or I.

Creating a local issuer under these conditions would convert an unverifiable claim into an apparent authorization witness.

That is a substitute authorization decision, not an implementation of the existing authority contract.

**Therefore `protected_visibility_authorized` MUST remain permanently false within this baseline and current contract.**

"Permanent" here means that no implementation under this baseline may turn the flag true. A change requires a new, explicit cross-owner decision and verified authoritative integration; it is not an automatic consequence of future component availability.

### Delegation decision

**Delegation is not authorized under this baseline.**

D cannot delegate Storage's visibility-state authority or I's authorization authority on their behalf.

A future cross-owner delegation would require, at minimum:

- explicit authorization from each affected authority owner;
- an immutable, verifiable delegation instrument;
- exact scope, operation, tuple, and permitted action binding;
- issuer identity and integrity verification;
- validity period and generation/replay constraints;
- explicit revocation semantics and durable revocation evidence;
- a verifier that rejects expired, revoked, mismatched, or incomplete delegation evidence.

No such instrument or verifier is established here.

A local development proxy, configuration flag, caller-provided boolean, or E-side registry is not a delegation instrument.

## 5. Relationship to prior decisions

### D3 — `OWNER-DECISION-PUBLICATION-RECORD-001`

D3 recorded `protected_visibility_authorized` as unsourced.

This decision refines the finding:

- the normative authority boundary is already specified in §8;
- the missing element is not an unnamed authority category;
- the missing elements are the concrete authoritative evidence, issuer integration, durable binding, and verifier.

D3's fail-closed outcome remains unchanged.

### D7.1 / D7.2

D7.1 permanently withheld `publication_participant_admitted` under the current baseline because COC quorum, Storage signing, and I's terminal decision cannot be manufactured by a local D/E registry.

D7.2 assigned those external dependencies to COC, Storage, and I.

This decision is consistent with both:

- it does not invent a local protected-visibility issuer;
- it does not confuse participant admission with protected visibility authorization.

The two flags are distinct authorization conditions, even though they are consumed together by the final suppression branch.

### `D-OWNER-DECISION-PARTICIPANT-ADMISSION-001`

This decision adopts the same development-baseline rule:

- no local record can mint missing external authority;
- no caller assertion can become authoritative evidence;
- no development proxy can substitute for an external owner;
- false remains the required production adapter output.

It does not reopen or modify the participant-admission decision.

### GAP-14-B

This decision supplies the third and final answer:

1. `canonical_commit_confirmed`: D6 — permanently false under the current contract.
2. `publication_participant_admitted`: D7 — permanently false under the current baseline.
3. `protected_visibility_authorized`: this decision — permanently false under the current baseline.

All three questions are now DECIDED.

## 6. Phase 1 compatibility

This is a documentation-only decision.

It does not change:

- `PublicationProof` or its eight fields;
- the Phase 1 frozen contract;
- `dm2_14` expectations or inputs;
- Rust source, schemas, DDL, serialization, public APIs, or `DomainError`;
- the `Blocked`, `Suppressed`, or `Published` disposition definitions.

The existing gate semantics remain unchanged:

```rust
if !proof.producer_admitted
    || !proof.dependency_closure_complete
    || !proof.canonical_commit_confirmed
    || !proof.storage_prepared_hidden
{
    return Ok(PublishedDerivative {
        derivative: staged,
        disposition: PublicationDisposition::Blocked,
    });
}

if !proof.publication_participant_admitted
    || !proof.protected_visibility_authorized
{
    return Ok(PublishedDerivative {
        derivative: staged,
        disposition: PublicationDisposition::Suppressed,
    });
}
```

The distinction is material:

- The first four conditions are publication prerequisites. Failure produces `Blocked`.
- The last two conditions are independent authorization conditions. Failure produces `Suppressed`.

Protected visibility authorization is therefore not merely another name for participant admission or storage preparation.

### Production reachability conclusion

Because D7.1 requires `publication_participant_admitted = false`, the `Published` branch is permanently unreachable in production under the current baseline and contract.

Even if all other six flags become true, the second authorization condition still fails.

If the first four conditions are satisfied, the disposition is `Suppressed`, not `Published`.

If any of the first four conditions fails, the disposition remains `Blocked`.

This is an explicit consequence of the adopted authority model, not an implementation defect to be repaired by setting a flag to true.

## 7. What this does not decide

The following remain **OUT-OF-SCOPE (dev-baseline)**:

- production cryptographic suite, canonicalization, signature algorithms, and key policy;
- Storage signing-key custody, rotation, revocation, and HSM;
- Storage production visibility-transition implementation and deployment;
- COC quorum algorithm, membership, consensus, failover, and operational deployment;
- I's production authorization sequencer and terminal-decision implementation;
- D's production Fence/Admission integration consuming exact Storage and I evidence;
- cross-owner delegation policy and delegation-instrument implementation;
- production tuple-binding, interoperability, and end-to-end conformance;
- production publication activation and any future decision to permit `Published`.

This decision does not approve a future issuer or promise that future component availability will automatically authorize publication.

Any future proposal to change this flag to true requires a new cross-owner decision specifying the actual issuers, records, validators, tuple-binding rules, delegation rules if applicable, and production verification evidence.

## 8. Closure criteria

1. `compiler-stage-contract.md` §8 continues to identify Storage and applicable D/I authorization as the required authority for protected visibility advancement; E has no independent authority.
2. `protected_visibility_authorized` remains `false` in the production adapter under this baseline.
3. No local protected-visibility issuer, authorization table, reference type, caller-controlled boolean, or development trust-anchor shortcut is introduced.
4. `AdmissionStore` and its publication receipts are not represented as Storage visibility authorization or D/I authorization.
5. The C JF-10 protected-operation evidence requirements remain intact and are not represented as a completed local publication-visibility implementation.
6. No delegation to D's owner-proxy, E, a local registry, or a development trust anchor is implied or introduced.
7. `PublicationProof` eight fields, Phase 1 freeze, and `dm2_14` inputs remain untouched; normal validation must record unchanged `dm2_14` PASS before release.
8. GAP-14-B references this decision as its third completed ruling.
9. The production disposition remains `Blocked` when any of the first four prerequisites is false and `Suppressed` when the first four pass but either independent authorization condition is false.
10. Any future transition to `true` requires a new cross-owner decision naming the exact Storage and applicable D/I issuers, durable evidence, validators, tuple-binding rules, and production verification.
11. The current production conclusion is recorded accurately: `Published` is unreachable under the current baseline and contract because `publication_participant_admitted` remains permanently false.

---

**Final ruling:** `protected_visibility_authorized = false` for the current development baseline. No local issuer or delegation is authorized. GAP-14-B's three decision questions are complete. `Published` remains unreachable in production under the current contract.
