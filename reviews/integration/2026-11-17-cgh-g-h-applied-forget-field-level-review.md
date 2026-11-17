# C/G/H Applied, Forget and Reconciliation — Field-Level Cross-Owner Review

- Date: 2026-11-17
- Scope: targeted independent review of the live C final-request evidence pair, G Applied/Forget/Reconciliation contract, H Adapter Capability/Applied Attestation contract, and the exact CGH-APPLIED-1.1 recovery-batch decision record.
- Review posture: delegated role simulation / repository-artifact review; not an independent human Owner signature.
- Disposition: **SEMANTIC ALIGNMENT PARTIAL; FIELD-LEVEL ACK IDENTITY CLARIFICATION REQUIRED; WIRE FREEZE BLOCKED.**

## 1. Exact source and decision pins

| Item | Branch / artifact | Blob SHA or exact reference |
|---|---|---|
| C Final Request Evidence | `session-c-agent-integration-2026-11-16` / `07-agent-integration/phase-3.6-final-request-evidence-contract.md` | `fd2f47ba6c89bb270e9f2bec956873cb7ae3592b` |
| C causal-order / recovery-batch addendum | `session-c-agent-integration-2026-11-16` / `07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md` | `45a48249717c8cddb07ab96197730ef93d406c22` |
| G Applied / Forget / Reconciliation | `session-g-memory-context` / `06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md` | `aa3afa73d8a76cc6f025839c52bfbff6a983046a` |
| H Adapter Capability / Applied Attestation | `session-h-bmcp-protocol` / `08-bmcp-protocol/adapter-capability-and-applied-attestation.md` | `74be8374a67da385a5f0f8e34c7aef2b38b72bcf` |
| Common A recovery-batch package | `CGH-APPLIED-1.1` | `4961ffefc0f9920efb8425a9b2a7af42d8f64819` |
| Companion COC architecture | `CausalOrderProfile/1.0` | `fc3bac39ec64fda68b8cba5e1aada4e719e5acea` |
| C exact-pair decision artifact | Issue #3 exact-decision reconciliation | `a72a3eb1e5207f67c01f804508311f42db9a6e0a` |
| H exact-pair decision artifact | Issue #3 exact-decision reconciliation | `22853b21d583d2cae75eb3ef1c580c68b4cf4c70` |
| G exact-pair decision artifact | G source decision / Issue #3 reconciliation | `aa3afa73d8a76cc6f025839c52bfbff6a983046a` |

The Issue #3 exact-decision record reports C, G and H each accepted the same A package Blob `4961ffefc0f9920efb8425a9b2a7af42d8f64819` plus COC companion `fc3bac39ec64fda68b8cba5e1aada4e719e5acea`, each with enumerated exceptions. This corrects any earlier statement that H had not accepted that exact semantic package.

**Critical scope distinction:** H's exact acceptance of the A/COC semantic package does not silently upgrade H Adapter Capability §11.8–11.9 from CANDIDATE to a frozen wire schema. The H source itself still says the §11.8–11.9 mapping is candidate and requires an additive exact schema/SDK mapping and relevant consumer confirmations. Exact package acceptance and exact wire-field/schema acceptance are separate decisions.

## 2. Six-stage lifecycle

All three contracts preserve the same six facts and authority boundaries:

1. **Prepared** — G commits an immutable ContextVersion and Delivery intent.
2. **Delivered** — H authenticates receipt of the exact DeliveryId/attempt.
3. **Materialized** — Adapter evidence identifies the exact managed region, revision/inventory and digest.
4. **Final Request Submitted** — C proves the actual immutable post-transformation request crossed the declared successful submit boundary.
5. **Applied** — G alone validates the complete predicate and commits the per-request Applied record.
6. **Execution Started** — a separate runtime/provider start receipt correlated to the same InferenceRequestId.

**Result: PASS at semantic level.** No stage may be inferred from its predecessor. In particular, transport ACK is not materialization; materialization is not final submit; C submission is not G Applied; Applied is not execution start, model attention, understanding, recall or correct behavior.

## 3. C-to-H-to-G field mapping

| Evidence concept | C producer contract | H carrier / attestation | G consumer predicate | Review |
|---|---|---|---|---|
| Request identity | Actual runtime/provider InferenceRequestId + FinalRequestBoundaryId and boundary type | `inference_request_id`, `final_request_boundary_id`, boundary type | Same exact request/boundary identity | Aligned |
| G target | ContextId/ContextVersion + DeliveryId/DeliveryAttemptId | `context_id`, `context_version`, `delivery_id`, `delivery_attempt_id` | Exact active, non-superseded G target/attempt | Aligned |
| Materialized state | Managed Region identity/inventory and actual complete digest | `materialized_context_version`, region ID/revision/inventory digest/coverage/content digest/profile | Complete target and region digest match | Aligned; Full requires COMPLETE |
| Identity | Authenticated Agent/Adapter/Runtime/Session protected bindings | verifier-resolved principal/actor/instance/session refs; transport principal is not a substitute | Current mutually bound identities; G consumes B/I semantics | Aligned by ownership; exact wire encoding remains open |
| Scope / Environment | Exact ScopeRef and applicable EnvironmentRef | `scope_ref`, `environment_ref` | Exact role-preserving scope/environment bindings | Aligned; no payload fallback |
| Authorization | I PermissionEpoch and decision at final submit | I-issued `permission_epoch_ref`, `permission_decision_ref`, plus I terminal/revocation evidence in §11.8 | Current I decision/epoch and causal terminal evidence | Aligned semantically; wire requiredness/profile not frozen |
| Forget | D ForgetFence generation/cursor and lineage validation | D fence generation/cursor/validation ref; §11.8 D lineage, request cutoff and effective position | Current D fence and complete lineage; suppress on unknown | Aligned semantically; preserve cutoff vs effective position |
| Capability | H CapabilityEpoch/profile | `adapter_capability_epoch`, capability profile and per-request coverage | Current exact Adapter/session capability epoch; Tier 1 only for Full | Aligned |
| Provider outcome | C causal addendum requires actual provider receipt and immutable CSubmitOutcome | §11.9 `c_provider_receipt_ref`, `c_submit_outcome_ref` | G requires determinate successful C outcome, not merely reservation/ACK | Semantically aligned; H field mapping still candidate |
| Causal terminal | CausalOrderTransaction/Intent/Reservation/TerminalProof and exact digest | §11.8 COC refs, terminal proof/digest, recovery batch and complete participant/high-water evidence | G accepts Full only after complete determinate causal proof | Semantically aligned; exact message-family schema not frozen |
| Owner gate release | I/D remain sole authorities | `owner_gate_release_attestation_ref` is owner-issued | G never treats COC/H observation as I/D release | Aligned |

The C Final Request Evidence base file and C causal-order addendum must be read as a composed producer contract. The base file alone does not contain the entire recovery-batch/provider-outcome evidence set; the separate C addendum supplies the exact CGH-APPLIED-1.1 acceptance and C-owned CSubmitOutcome/provider receipt requirements.

## 4. P1 — ACK/evidence identity tuple is not yet normatively unified

C §6 describes evidence identity as Adapter instance + Runtime Session + DeliveryId + attempt + evidence kind + digest. H §11.6 proposes the tuple:

`(adapter_instance_ref, runtime_session_ref, delivery_id, delivery_attempt_id, inference_request_id, final_request_boundary_id, evidence_kind, adapter_capability_epoch)`

H then compares the canonical payload digest separately: same tuple + same digest is idempotent; same tuple + changed digest is CONFLICT.

These are not byte-for-byte equivalent definitions. More importantly, if C treats the digest itself as part of the identity key, a changed digest may look like a different identity rather than a conflicting payload for the same identity.

**Required normative correction:**
- Define a stable evidence identity tuple that excludes the payload digest.
- Include the exact request/boundary and capability epoch in that stable tuple (or explicitly prove why a narrower identity is safe).
- Treat canonical payload digest as the immutable content bound to that identity, not as a key component.
- Same identity + same digest => return original durable disposition.
- Same identity + different digest => CONFLICT/quarantine; never last-write-wins.
- G's durable Applied idempotency key must be explicitly mapped to this evidence identity and the exact CausalOrderTransaction/ParticipantIntent/Reservation identity for the 1.1 profile.

Until C, G and H record this exact shared tuple, ACK idempotency is **semantically intended but not fully field-level frozen**.

## 5. Late evidence and supersession

C, H and G agree:
- Late evidence for an old/superseded attempt may be retained as historical evidence only.
- It cannot roll back a newer ContextVersion or Delivery attempt.
- Old Adapter/Runtime Session evidence cannot be rebound to a replacement session or CapabilityEpoch.
- A late ACK cannot promote Full Applied without all current authority and causal predicates.
- Changed digest under the same stable identity is conflict, not a second valid ACK.

**Result: PASS in semantic direction; exact shared identity tuple remains P1.**

## 6. Forget / revocation / provider-side-effect ordering

The combined 1.1 profile is not a single clock. The following authorities and order domains remain distinct:

- COC causal-order epoch/position/entry digest;
- I policy-domain sequencer epoch/position/decision digest;
- D fence request cutoff and later effective position;
- Storage transaction/resolution position;
- C actual provider receipt and CSubmitOutcome.

Normative race outcomes:
1. I revocation before receipt consumption may win and abort admission.
2. Once I has terminalized the exact receipt as COMMIT_WON, later revocation waits behind that unresolved participant; it is not silently reordered by H arrival time or wall clock.
3. D fence request before ParticipantIntent cutoff rejects that intent.
4. A D fence requested after the intent must account for the earlier unresolved participant and cannot become effective past it until safe terminal resolution.
5. C must not call the provider before durable intent, compatible I/D proofs and coordinator reservation.
6. Provider timeout/crash/ambiguous outcome remains UNKNOWN/IN_DOUBT; no retry as a new transaction, no new idempotency identity, and I/D barriers remain held.
7. A recovery batch must enumerate every pre-batch participant, prove completeness and owner high-water, and reconcile I/D/C/Storage outcomes. An absent list is not an empty list.
8. COC recovery observation is not itself I/D owner gate release. Only the relevant owner-signed disposition may reopen its gate.
9. If successful submit is proven before later effective Forget/revocation, retain historical Applied but immediately invalidate current-use. If Forget/revocation wins before submit, reject Full. If order is unknown, suppress and remain UNKNOWN/IN_DOUBT.

**Result: PASS at semantic-decision level for the exact 1.1 recovery-batch package, conditional on the enumerated exceptions.** H §11.8–11.9 still needs exact schema/SDK representation; production coordinator, provider idempotency and Storage/JF-10 remain unverified.

## 7. Forget behavior and reconciliation obligations

G's contract correctly keeps these distinct:
- Context Remove is membership removal, not Canonical Forget.
- D owns canonical ForgetOperation/Fence/lineage; G consumes D evidence.
- G installs durable deny tombstones and suppresses affected entries, ContextVersions, ChangeSets, Snapshots, Deltas, pending deliveries, caches/queues and reconnect state.
- G preserves a valid historical Applied fact but marks it InvalidatedForCurrentUse after later Forget/revocation.
- H Forget ACK is a separate evidence family from Applied Attestation and cannot prove global Forget or provider deletion.
- Reconnect is a new trust boundary: authenticate, renegotiate capability, refresh I/D authorities, reconcile tombstones and delivery ledger, reject stale Snapshot/Delta/ACK, then revalidate immediately before apply and final submit.
- Missing/unknown authority evidence fails closed; no stale payload or old ACK replay.

No global Forget completion, physical erasure, F index/cache purge, H local cache purge or provider-side deletion is proven by these contracts.

## 8. Findings and required closure

| ID | Severity | Finding | Closure evidence |
|---|---|---|---|
| CGH-FLD-01 | P1 | C and H evidence identity tuple differ; C includes digest in identity while H separates stable identity from digest | C/G/H exact shared identity tuple and negative changed-digest test |
| CGH-FLD-02 | P1 | H §11.8–11.9 is candidate mapping, not proof that all recovery/provider fields are present in frozen generated Applied ACK schema/SDK | Exact H schema/IDL/SDK version, requiredness/canonicalization, generated artifacts and readback |
| CGH-FLD-03 | P1 | G durable Applied idempotency key is not yet explicitly bound to H's exact evidence identity and COC participant identity | G-owned normative mapping and crash/replay/conflict tests |
| CGH-FLD-04 | P2 | C Final Request base contract and causal-order addendum must be tracked as a single composed evidence producer profile | Manifest binds both exact C Blob SHAs and schema version |
| CGH-FLD-05 | P2 | Distinct COC/I/D/Storage ordering domains must remain typed; no wall-clock or receiver-sequence fallback | Cross-owner negative tests for inversion, missing cutoff, incomplete recovery batch |
| CGH-FLD-06 | P2 | Historical Applied versus current-use invalidation must be checked under late ACK + Forget/revocation races | G persistence/recovery tests with deterministic race ordering |

## 9. Final disposition

- Six-stage lifecycle and authority split: **SEMANTIC PASS**.
- C/G/H exact CGH-APPLIED-1.1 recovery-batch semantic decisions: **RECORDED WITH ENUMERATED EXCEPTIONS** against A Blob `4961ffefc0f9920efb8425a9b2a7af42d8f64819` and COC Blob `fc3bac39ec64fda68b8cba5e1aada4e719e5acea`.
- C/H/G field-level contract: **PARTIAL; P1 identity tuple and exact wire schema closure remain open**.
- H Adapter Capability §11.8–11.9: **CANDIDATE MAPPING; NOT WIRE FROZEN**.
- G Applied persistence: **NOT VERIFIED**.
- C provider-specific same-key idempotency / recovery: **NOT VERIFIED**.
- COC deployment/operator and Storage/JF-10 production realization: **NOT VERIFIED / BLOCKED**.
- C/G/H conformance: **SPECIFIED / NOT RUN** for the remaining cross-owner race/recovery suite.
- Global Applied Contract Frozen: **NO**. Production activation/provider egress: **NOT AUTHORIZED**.

This review is not an Owner signature and does not authorize branch merge, architecture freeze or production activation.
