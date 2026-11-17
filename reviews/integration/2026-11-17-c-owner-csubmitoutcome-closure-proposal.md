# C Owner Closure Proposal — Provider Receipt and Immutable CSubmitOutcome for CGH-APPLIED-1.1

- Date: 2026-11-17
- Status: **PROPOSAL FOR C OWNER REVIEW — NOT AN OWNER DECISION**
- C source baseline: `07-agent-integration/phase-3.6-final-request-evidence-contract.md`, Blob `fd2f47ba6c89bb270e9f2bec956873cb7ae3592b`.
- G decision baseline: recovery-batch A package Blob `4961ffefc0f9920efb8425a9b2a7af42d8f64819`; COC companion Blob `fc3bac39ec64fda68b8cba5e1aada4e719e5acea`.
- H candidate baseline: `08-bmcp-protocol/adapter-capability-and-applied-attestation.md`, Blob `74be8374a67da385a5f0f8e34c7aef2b38b72bcf`, §§11.8–11.9.
- Purpose: provide C with a bounded amendment proposal that closes the producer-side gap without transferring COC, I, D, Storage or G authority to C.

## 1. Decision requested from C

C should review and, if accepted, publish an exact-version Owner addendum that defines:
1. the C-issued reference to the actual Provider/Runtime handoff receipt (`c_provider_receipt_ref`);
2. the immutable C-owned submit outcome record (`c_submit_outcome_ref` / `CSubmitOutcome`);
3. the exact identity/digest binding from that outcome to the submitted request and the relevant participant intent;
4. deterministic ACCEPTED / REJECTED / UNKNOWN semantics and the resulting Applied eligibility;
5. append-only correction, idempotency, conflict, replay and recovery behavior;
6. the exact 1.1 package/version C is accepting, with enumerated exceptions.

This proposal is not C approval and must not be recorded as such.

## 2. Proposed authority boundary

- **C owns:** observation of its integration's actual provider/runtime handoff; validation of the provider receipt; issuance and integrity protection of its immutable CSubmitOutcome; correlation to the exact final request and participant intent.
- **Provider/Runtime owns:** the underlying provider/runtime receipt and request identity assigned at that boundary. C may issue an authenticated reference/attestation to it, but must not fabricate provider facts.
- **COC owns:** causal-order transaction, reservation, terminal proof, recovery-batch completeness and participant-set reconciliation. C only binds/references these objects; C does not issue them.
- **I owns:** authorization terminal evidence, sequencer position and revocation cutoff; any I owner-local gate release.
- **D owns:** lineage coverage, ForgetFence request cutoff/effective position; any D owner-local gate release.
- **Storage owns:** same-XID resolution and terminal visibility/non-publication evidence when Storage participates.
- **H owns:** BMCP envelope/schema/ACK/capability transport and authenticated preservation of owner-issued evidence. H cannot mint C outcome or owner gate release.
- **G owns:** Full Applied decision, durable Applied fact and current-use projection. G validates the complete evidence set; no C evidence directly changes Applied state.

## 3. Proposed CSubmitOutcome semantic contract

The following is a minimum semantic contract. C Owner must approve or revise the exact field schema; this proposal does not freeze field names beyond the H candidate references already present in §11.9.

### 3.1 Required binding

The C-issued outcome and Provider receipt reference must be bound to:
- actual runtime/provider-assigned `InferenceRequestId`;
- exact `FinalRequestBoundaryId` and boundary type/profile;
- exact post-transformation request digest and canonicalization/digest profile;
- exact `ContextId/ContextVersion`, `DeliveryId/DeliveryAttemptId` where this request carries managed context;
- authenticated Agent/Adapter/Runtime/Session bindings already required by C;
- exact participant/request identity and the causal-order transaction reference where the participant belongs to a COC transaction;
- provider/runtime receipt identity, evidence issuer, integrity/signature/key reference, schema version and audit/correlation references.

A local render, local queue acceptance, middleware callback, H transport ACK, Adapter materialization receipt, timeout or COC recovery observation is not a Provider receipt and cannot be substituted.

### 3.2 Outcome enum and meaning

| Outcome | Required meaning | Applied consequence |
|---|---|---|
| `ACCEPTED` | Authenticated provider/runtime evidence establishes successful handoff of this exact request | May satisfy only the C provider-outcome predicate; never directly means Applied |
| `REJECTED` | Authenticated provider/runtime evidence establishes deterministic rejection before successful handoff | Cannot support Full Applied; retain immutable negative outcome |
| `UNKNOWN` | Handoff outcome cannot be determined, receipt is missing/ambiguous, or evidence conflicts | Participant remains IN_DOUBT; no Full Applied; protected current use remains suppressed |

A successful local submit call is not enough unless it is the agreed authoritative provider/runtime handoff boundary and is backed by the required receipt. C must define whether retries produce a new InferenceRequestId, a new outcome identity, or a linked superseding attempt; it must never silently rewrite the prior outcome.

### 3.3 Immutability and identity

- CSubmitOutcome is append-only and immutable after issuance.
- Its identity must bind the exact request, boundary, participant/request identity and evidence kind.
- Same identity + same canonical digest is idempotent and returns the original disposition.
- Same identity + changed digest is CONFLICT and quarantine; no last-write-wins.
- Corrections are new linked superseding records; no in-place mutation.
- Evidence from a superseded request/session/attempt remains historical only and cannot be rebound to a new request or capability epoch.
- Missing, stale, unauthenticated or contradictory provider evidence yields UNKNOWN/IN_DOUBT, never inferred ACCEPTED.

## 4. COC and recovery-batch integration

C must not create `CausalOrderTerminalProof`, `recovery_batch_ref`, participant-set completeness attestations, owner high-water attestations, participant reconciliation entries, or I/D/Storage terminal evidence.

C should:
1. bind its CSubmitOutcome to the exact COC transaction/participant/request digest when such a participant exists;
2. publish the C-issued outcome reference and digest for the C participant entry;
3. preserve the distinction between C provider outcome and COC transaction terminalization;
4. accept that a COC terminal proof can exist only after all required participant outcomes are determinate and reconciled;
5. keep UNKNOWN C outcome IN_DOUBT; COC observation cannot turn it into ACCEPTED;
6. never release I/D owner-local gates. Only I or D may issue its own `owner_gate_release_attestation_ref`.

A C provider ACCEPTED outcome is necessary for the C participant to be determinate, but it is not sufficient for the whole COC transaction to be terminal or for G to accept Applied.

## 5. Required negative cases

All cases remain **SPECIFIED / NOT RUN** until executable fixtures and durable artifacts are attached.

| ID | Scenario | Expected C disposition | Forbidden |
|---|---|---|---|
| C-CO-01 | Actual provider receipt proves exact request accepted | Immutable ACCEPTED CSubmitOutcome | C directly marks Applied |
| C-CO-02 | Provider deterministically rejects before handoff | Immutable REJECTED outcome | Treat as accepted submit |
| C-CO-03 | Provider receipt absent or timeout leaves handoff ambiguous | UNKNOWN / IN_DOUBT | Infer acceptance from timeout or local call |
| C-CO-04 | Receipt request ID or digest mismatches C final request | Reject/quarantine; UNKNOWN | Bind receipt to another request |
| C-CO-05 | Same outcome identity and same digest replay | Idempotent original result | Duplicate promotion |
| C-CO-06 | Same outcome identity but changed digest | CONFLICT / quarantine | Last-write-wins |
| C-CO-07 | Late receipt after superseding request/session | Historical only; no current pointer rollback | Rebind old receipt |
| C-CO-08 | C outcome ACCEPTED but I/D/Storage participant remains pending | C remains ACCEPTED; overall transaction remains IN_DOUBT | Claim participant terminal proof or release gate |
| C-CO-09 | COC recovery observation but no C provider receipt | C outcome UNKNOWN | COC substitutes for provider evidence |
| C-CO-10 | I/D owner gate release absent or issued by wrong owner | Gate remains closed | C/H/COC synthesizes REOPENED |

## 6. Exact-version decision checklist for C Owner

Before recording acceptance, C must verify:
- exact C source Blob and exact H §11.9 source Blob are pinned;
- exact G recovery-batch A/COC package pair is pinned;
- C-owned provider receipt/outcome schema and semantics are explicit;
- C's evidence is correlated to the exact request and participant intent/digest;
- C does not own COC terminal proof, I/D gate release, Storage outcome or G Applied;
- UNKNOWN and missing evidence fail closed;
- C's conformance cases and implementation status remain accurately labeled.

**Proposed decision template (must be completed by C Owner, not this reviewer):**
- Decision: PENDING C OWNER REVIEW
- Exact package Blob(s): to be pinned by C
- Accepted C-owned clauses: to be enumerated by C
- Exceptions / dependencies: to be enumerated by C
- C-CO-01..10: SPECIFIED / NOT RUN until executed
- Implementation / runtime: NOT VERIFIED until evidence exists

## 7. Non-claims

This proposal does not establish C Owner approval, G Applied acceptance, H wire/schema freeze, I authorization approval, D Forget closure, Storage topology/atomicity, COC deployment, implementation correctness, runtime conformance, global Forget completion or physical erasure.
