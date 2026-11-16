# Phase 3.6 — A exact-version review: COC persistence, recovery cutoff and JF-10 bridge

Date: 2026-11-17  
Owner: A — Principal Integration Architect  
Review status: **ACCEPT WITH BLOCKING CLARIFICATIONS / AMENDMENTS REQUIRED**  
Scope: architecture and cross-owner contract review only; no implementation or conformance claim.

## 1. Exact review set

This review is bound to the following readback-verified blobs:

| Owner | Artifact | Branch | Blob |
|---|---|---|---|
| A | `reviews/integration/phase-3.6-causal-order-coordinator-deployment-architecture.md` | `session-a-integration-2026-11-16` | `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d` |
| I | `09-security-governance/phase-3.6.2-jf10-v2-i-owner-disposition.md` | `session-i-security-governance-2026-11-16` | `8069ff86988396442c8d9dc3fd58653683abe2f3` |
| D | `03-memory-brain/forget-fence-operation-and-publication-gate.md` | `session-d-memory-brain-2026-11-16` | `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5` |
| C | `07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md` | `session-c-agent-integration-2026-11-16` | `45a48249717c8cddb07ab96197730ef93d406c22` |
| H | `08-bmcp-protocol/phase-3.6-authenticated-identity-protected-operation-binding.md` | `session-h-bmcp-protocol` | `e7ca5ce4ece5d8fd77fe0760e49a85afa0133248` |
| D / Storage | `03-memory-brain/phase-3.6.2-jf10-cross-authority-recovery-protocol.md` | `session-d-memory-brain-2026-11-16` | `94679897e84a6f58fd8b9467b5249e1a885cb0b0` |
| H schema candidate | `08-bmcp-protocol/schemas/bmcp.applied-ack-1.1.0-jf10-bridge.schema.json` | `session-h-bmcp-protocol` | `a8a945cc3623c2907003b93625e3c79742150944` |

The A architecture's §11 and §12 are the normative COC-outage and JF-10 bridge text under review. This review does not reopen already accepted authority boundaries; it tests whether the exact-version texts compose without missing safety evidence.

## 2. A's decision

**ACCEPT WITH BLOCKING CLARIFICATIONS / AMENDMENTS REQUIRED.**

The core architecture is sound in these respects:

1. COC is an ordering / durable participant-accounting authority, not the JF-10 COMMIT/ABORT authority.
2. I's policy-domain sequencer alone consumes the single-use authorization receipt and commits the terminal decision.
3. Storage alone resolves the exact preallocated XID and owns atomic visibility / PublicationReceipt.
4. D alone owns ForgetFence, lineage and barrier effectiveness.
5. C alone reports the actual provider outcome; H transports authenticated owner evidence without synthesizing authority.
6. COC, I, D and Storage positions remain distinct typed orders; local wall-clock/sequence metadata cannot establish cross-owner order.
7. UNKNOWN / IN_DOUBT remains nonterminal; private bytes, locks and barriers are retained; no timeout, missing row, lost ACK, stale replica or process death may infer an outcome.
8. The scope remains one I PolicyDomain only.

The following issues must be closed before the protocol is treated as an exact, fully specified persistence/recovery contract.

## 3. Blocking findings

### A-COC-R1 — Recovery Cutoff Batch completeness and closure boundary

**Finding: INCOMPLETE NORMATIVE BINDING.**

A §11.2 requires collecting every durable I/D request received during the outage, appending one immutable batch after the last committed pre-outage entry, enumerating all affected pre-batch participants, and checking monotonic owner high-water marks. H §12.9.2 adds stronger transport evidence: per-owner request-set completeness attestations, pre-batch prefix position/root, canonical request sets, union digest, quorum commit proof, participant-set digest/completeness proof and owner high-water attestations.

The A normative text does not yet define the protocol-level construction and verification of these completeness proofs, or the exact snapshot/closure boundary for each owner's outage request set.

**Required amendment:**
- Each owner must expose a durable monotonic outage-request high-water mark (or equivalent complete append-only request ledger) whose capture is serialized with local gate closure.
- Each owner must attest the complete canonical request set through that exact high-water mark; the attestation binds owner identity, request-set digest, count/empty-set state, high-water mark and the outage/cutoff generation.
- The COC batch must bind the pre-batch quorum prefix position + root digest, both independently canonicalized owner request sets, their union digest, both owner completeness attestations where applicable, batch identity/digest and quorum commit proof.
- A request arriving after the captured owner high-water mark but before gate release must either be included in a subsequent committed batch or keep that owner's gate closed. No request may fall between batch snapshot and reopening.
- Same batch identity + same digest is idempotent; same identity with changed request set/prefix is a conflict. Batch creation/retry must not create a second causal cutoff for the same captured request set.

### A-COC-R2 — Owner-local Gate linearization and admission race

**Finding: SAFETY PROPERTY STATED, LINEARIZATION POINT NOT PRECISELY DEFINED.**

A §11.1 says the owner must durably persist PENDING_COC_CUTOFF and close admission before acknowledging the request, and the gate survives restart/failover. It does not identify the atomic serialization boundary between:
- recording/accepting the I revocation or D fence request;
- closing the affected local admission/receipt gate;
- operations already admitted but not yet durably registered in COC;
- capturing the owner's request high-water mark for the recovery batch.

**Required amendment from I and D independently:**
- Identify the exact owner-local transaction/CAS/sequencer linearization point that makes the gate effective.
- Prove no affected prepare, receipt issuance/consumption, reservation or provider admission can pass between request acceptance and durable gate closure.
- Define treatment of operations concurrently admitted before the local gate point but not yet COC-registered; they must be discoverable and included in reconciliation or rejected before side effects.
- Define idempotent duplicate request handling and conflicting same-reference/different-digest handling.
- Define the gate's scope key (target/source/ancestor and policy domain) and how scope expansion is handled without reopening a narrower gate.

A local timestamp or sequence is audit metadata only; it cannot substitute for the owner-local serialization proof.

### A-COC-R3 — Recovery batch participant-set completeness and gate release

**Finding: NEEDS OWNER-ATTESTED ENUMERATION CONTRACT.**

A §11.2 requires enumeration of every affected ParticipantIntentRef committed before the recovery batch, and reconciliation against I, D and C. H §12.9.2 requires a digest of the complete participant set, a completeness attestation against the committed COC prefix plus owner high-water attestations, and explicit distinction between a proven empty set and an absent/unenumerated set.

**Required amendment:**
- COC must produce an authoritative participant-set completeness proof bound to the exact pre-batch prefix/root and affected-domain/lineage query.
- I and D must separately attest their applicable owner high-water and per-participant reconciliation results; C must attest its provider outcome for any participant where C is applicable.
- Every entry must preserve exact ParticipantIntentRef, operation/request digest, owner boundary, policy domain and preallocated XID binding.
- Empty participant sets require an explicit completeness attestation; omission is invalid.
- I and D gate release are separate owner-signed decisions. COC cannot release either gate. REOPENED requires that owner's complete request set, every applicable pre-batch participant and monotonic high-water be verified. Otherwise REMAINS_CLOSED.
- A shared COC cutoff may continue blocking later affected intents after the local pending gate is cleared; the protocol must distinguish clearing the temporary outage gate from satisfying the effective I revocation / D fence.

### A-COC-R4 — C provider invocation must be conditional on I COMMIT_WON

**Finding: C ACCEPTANCE WORDING IS AMBIGUOUS.**

C's exact bridge contract says C must not invoke a provider until the I owner-final gate has produced an “authoritative terminal decision.” I has three terminal outcomes: COMMIT_WON, REVOCATION_WON and INDETERMINATE_ABORTED. Only COMMIT_WON authorizes forward progress to the provider boundary. REVOCATION_WON and INDETERMINATE_ABORTED require same-XID rollback/non-publication and MUST NOT permit provider invocation.

**Required C amendment:**
- Provider invocation is permitted only after an authoritative I **COMMIT_WON** for the exact immutable tuple, plus all required D clearance/fence predicates and the required COC/Storage registrations.
- I terminality alone is insufficient for provider invocation when outcome is ABORT/non-success.
- If the I outcome is REVOCATION_WON or INDETERMINATE_ABORTED, C must not invoke the provider; it must preserve the same participant/XID through Storage rollback and reconciliation.
- If I outcome is UNKNOWN/IN_DOUBT, C must not invoke the provider and must retain the participant as unresolved.
- C must explicitly define whether any C-owned pre-provider reservation is allowed before COMMIT_WON; if so, it must be non-side-effecting, durable/idempotent and separately typed from provider invocation.

### A-COC-R5 — Same-XID recovery bridge and terminal-state monotonicity

**Finding: CORE INVARIANT ACCEPTED; CROSS-OWNER TESTABLE STATE MACHINE STILL REQUIRED.**

The A/I/D/Storage texts correctly require:
- preallocated XID before Storage PREPARE;
- COC intent registration before PREPARE;
- Storage-signed PreparedParticipantReceipt for the exact XID and DB identity;
- COC prepared-participant registration before I owner-final-gate;
- I terminal decision and receipt consumption in one I transaction;
- COMMIT_WON => Storage forward-commit same XID;
- REVOCATION_WON / INDETERMINATE_ABORTED => Storage rollback same XID;
- COC outage after durable I COMMIT does not suspend Storage forward recovery;
- no alternate XID, heuristic outcome, timeout inference or reversal;
- Storage visibility and PublicationReceipt are atomically committed and authoritatively read back.

The executable state machine must additionally make these transitions explicit and conflict-detectable:
- INTENT_REGISTERED -> PREPARE_UNKNOWN -> PREPARED_REGISTERED -> I_TERMINAL_COMMIT / I_TERMINAL_ABORT -> STORAGE_RESOLVED -> COC_RECONCILED.
- Lost Storage PREPARE response: lookup by the original preallocated XID and canonical DB identity; never allocate a replacement.
- Lost COC append ACK: read quorum-confirmed prefix and idempotently detect the exact record/digest before retry.
- Lost I decision ACK: query the authoritative I sequencer by immutable operation/receipt/XID tuple; do not consume a second receipt.
- Lost Storage resolution ACK: query authoritative same-XID state and exact PublicationReceipt/non-publication proof.
- Contradictory terminal evidence or same XID observed with a different tuple/DB identity is CONFLICT and fail-closed.
- A terminal I COMMIT/ABORT is irreversible even if later COC observation or Storage resolution is delayed.

I, D and Storage must state their exact owner-authoritative lookup keys and proofs. H must map these as distinct typed references and must not infer terminality from a COC observation.

### A-COC-R6 — Exact-version reference and schema-scope drift

**Finding: EXACT-BUNDLE RECONCILIATION REQUIRED.**

Two version-binding issues were found in the reviewed set:

1. A §12 introduction cites an older I disposition Blob `1dedce596761807b25d337daf4a0d21bb797a197`, while the current I Owner artifact pinned by the current bridge bundle is Blob `8069ff86988396442c8d9dc3fd58653683abe2f3`.
2. H §12.9.0 says its recovery-batch schema addendum applies to older A package Blob `4961ffefc0f9920efb8425a9b2a7af42d8f64819` and companion COC Blob `fc3bac39ec64fda68b8cba5e1aada4e719e5acea`. H §12.10 accepts the current A Blob `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d` for the JF-10 bridge but says it does not change the §12.9 recovery-batch mapping.

**Required H decision:** explicitly state whether §12.9's recovery-batch mapping is also accepted for current A §11 Blob `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d`. If yes, publish a new exact-version mapping/append-only decision binding both current A §11 and §12. If no, identify the missing schema contract. Do not infer applicability from semantic similarity.

**Required A correction:** reconcile the stale I Blob reference. Any A Blob change creates a new exact version and therefore requires fresh I/D/C/H decisions against the new A Blob; this review does not silently transfer acceptance.

## 4. Required owner decisions

Each owner must append an owner-authored review on its own branch, with:
- exact A Blob `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d` and every other reviewed bundle Blob listed above;
- a disposition: **ACCEPT**, **ACCEPT WITH ENUMERATED AMENDMENTS**, **REJECT**, or **CANDIDATE / NO APPROVAL**;
- explicit answers to the findings assigned below;
- normative replacement text or exact amendment references for every accepted change;
- implementation / deployment / conformance status stated separately; no unrun test may be called PASS.

Owner assignments:
- **I:** A-COC-R1/R2/R3/R5/R6 as they affect I request completeness, local gate linearization, owner high-water, terminal decisions, receipt consumption and I gate release.
- **D:** A-COC-R1/R2/R3/R5/R6 as they affect D fence request completeness, lineage scope, barrier membership, high-water, D gate release and no premature fence effectiveness.
- **C:** A-COC-R1/R3/R4/R5 as they affect C-owned participant enumeration, provider invocation gate, same provider idempotency key and CSubmitOutcome reconciliation.
- **H:** A-COC-R1/R3/R5/R6 as wire-schema requiredness, canonicalization, signatures/attestations, replay/conflict rules, exact A §11/§12 applicability and message interoperability.
- **A:** integrate only after independent decisions; reconcile exact SHAs, update the COC normative text and publish a new exact-version bundle for re-review.

Storage is not being asked to make an Owner decision in this five-Owner round, but its existing same-XID participant/DB contract remains a dependency. Any change to Storage-owned semantics must be referred back to Storage rather than inferred by A.

## 5. Acceptance and execution boundary

- This is a documentation-level exact-version review.
- Recovery Cutoff Batch, Owner-local Gate, participant-set completeness and JF-10 same-XID recovery remain **SPECIFIED / NOT IMPLEMENTED / NOT CONFORMANCE-VERIFIED** unless separate evidence is published.
- H schema remains a candidate; generated schema, SDK interoperability, parser duplicate-key/canonical-byte enforcement and signature/key governance are not accepted by this review.
- C provider idempotency remains provider-specific and unverified.
- Persistent COC quorum implementation, operator, deployment and restore proof remain open.
- Gate B remains blocked by Gate A; Gate C remains blocked by Gate B. JF-10 P0 remains OPEN.
- Single I PolicyDomain only; multi-PolicyDomain atomicity remains BLOCKED.
- No merge, production activation or production readiness is authorized by this review.
