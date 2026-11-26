---
document_metadata:
  domain: protocol
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "Work Item AID-2026-099"
        - "Issues #1212, #1208, #1135"
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Candidate only; implementation, production durability, multi-replica linearizability and cross-owner acceptance are not claimed."
    usage_status: Active
    modification_status: Modified
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "H BMCP idempotency namespace, request deduplication, durable receipt, linearization and replay boundary"
    canonical_scope_id: "bmcp-protocol/h-idempotency-replay-boundary"
    canonical_scope_keywords:
      - bmcp
      - idempotency
      - namespace
      - replay
      - durable-receipt
      - linearization
      - unknown
      - attempt-identity
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "08-bmcp-protocol/h-idempotency-namespace-and-replay-boundary-contract.md"
    zh-CN: "docs/zh-CN/08-bmcp-protocol/h-idempotency-namespace-and-replay-boundary-contract.md"
---

# H Idempotency Namespace and Replay Boundary Contract

- Contract ID: H-IDEMPOTENCY-REPLAY-001; version 0.1.0.
- Status: **Draft / Candidate / Informative**; not approved, not normative, not a wire/schema freeze.
- Work item: AID-2026-099 (PROVISIONAL).
- H owns BMCP request identity, transport attempts, protocol receipts and replay disclosure. H does not own C provider outcome truth, G Applied, D ForgetFence, I authorization policy or Storage physical atomicity.

## 1. Reading rules and vocabulary

This is a candidate proposal, not evidence of implementation. MUST/MUST NOT below are proposed contract requirements, not currently approved normative rules. DOCUMENTED_ONLY checkpoints test whether this text defines a rule. EVIDENCE_REQUIRED checkpoints require exact-version implementation, storage, conformance or Owner evidence; prose alone cannot pass.

- **Logical operation:** one semantic intent, stable across transport retries.
- **Idempotency key:** caller-generated stable token naming that operation within an explicit authority/scope/operation namespace.
- **Attempt ID:** one concrete ingress/transport execution. Every retry is a new attempt.
- **Receipt:** immutable evidence of admission or a terminal result; not proof of C provider success or G Applied.
- **Duplicate:** request disposition, not a durable lifecycle state.

## 2. Authority boundaries and exact source pins

| Concern | Authority | H boundary |
|---|---|---|
| BMCP envelope, request/key binding, transport Attempt, protocol receipt and replay response | H | This candidate defines the proposed H-side boundary |
| Provider handoff outcome and immutable CSubmitOutcome | C | H resolves/authenticates the exact C record; never rewrites C Outcome or SideEffectStatus |
| Applied decision and AppliedAttestation / DeliveryAttempt join | G | H receipt/ACK is never Applied; G alone owns Applied |
| ForgetOperation, Fence generation, target lineage and suppression | D | H rechecks D currentness before replay disclosure; cannot create, advance or clear Fence |
| Current authorization, PermissionEpoch, issuer/key status and replay authorization | I | H calls I-owned current authorization; historical signature is insufficient |
| Business mutation, idempotency atomicity, commit/recovery and physical storage | Storage | H consumes Storage evidence; it does not define backend schema or transaction protocol |

Read from main at **d5107f68a7f1b61f5f2f7352fadf828aae06cf1c**:
- 07-agent-integration/applied-evidence-contract.md — Blob **273efdd1b02bd9302fc968f07c6d094da2582a6e**. H receipt/ACK is not Applied; retry keeps logical Delivery ID and uses a distinct Attempt ID; G projects Applied only from verified immutable C/H evidence.
- 06-memory-context/phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.md — Blob **833815e37ac8d7505d93a0a115421dafe3eb08ad**. G owns the unique durable per-request Applied decision; H evidence is only one predicate; applicable JF-10 requires Storage same-GID terminal resolution and atomic VisibilityPointer/PublicationReceipt or non-publication proof.
- 01-system-architecture/forget-fence-and-completion-contract.md — Blob **760a1d48011f2a66c23abcf825a3d067e79b8821**. D owns ForgetOperation/Fence and canonical suppression; I owns authorization, retention and global completion; H owns wire, Adapter local state, reconnect and trustworthy application/clear acknowledgement.
- 08-bmcp-protocol/owner-snapshot-namespace-and-fence-currentness-contract.md — Blob **d83cde77e98db2e74cf6827d874b0babb4157304**. Its namespace is D's ProducerWork Registration Ledger namespace, not H idempotency; do not alias or reuse it.
- 02-domain-model/phase-1-storage-trait-contract.md — Blob **22ca7cd3777e0132e25f084084610f1e90b60d21**. Candidate Storage seam: immutable version, current-version CAS, idempotency record and canonical commit sequence form one recoverable boundary; same key/same digest may return original receipt; same key/different digest is IdempotencyConflict. Shape tests do not prove backend atomicity/durability.
- H Phase 3.8.25 — Blob **afa294bc42a8488e4569e6a8bdf5437c7a90e247**; H Phase 3.8.26 — Blob **7b73491c765091728af6f5306b9efd502cf7f30a**. They require independent current I authorization and D Fence checks before replay disclosure, and exact CSubmitOutcome record/sequence/payload-digest/final-boundary joins. Resolver/verifier seams remain unverified.

**Storage / AID-2026-098 dependency:** AID-2026-098 has since been merged into main via PR #1283 (merge commit cdba0b7360b81ba2693c57f0d89ad2e28832272c); see AID-2026-098. The Storage contract is available at 10-storage-consistency/storage-physical-consistency-contract.md, docs/en/10-storage-consistency/storage-physical-consistency-contract.md, and docs/zh-CN/10-storage-consistency/storage-physical-consistency-contract.md. Its 18 checkpoints comprise 10 DOCUMENTED_ONLY and 8 EVIDENCE_REQUIRED; this is candidate documentation, not implementation or conformance evidence. This is a correction of an outdated baseline-availability statement only: it changes no normative conclusion in AID-2026-099, and HIR-06's reference to AID-2026-098 remains valid. This proposal reserves Storage atomicity and persistence details to AID-2026-098 and does not invent or duplicate them. Before cross-owner freeze, pin its exact path/version/blob and verify H/Storage mapping. The Storage Trait above is only a candidate seam, not a substitute. <!-- corrected_by: AID-2026-108 -->

## 3. Idempotency namespace and key ownership

### 3.1 Proposed lookup identity

The complete tuple is the lookup identity, never the raw key alone:

**HIdempotencyIdentity = (protocol_domain, authority_ref, tenant_or_scope_ref, operation_kind, key_profile, idempotency_key)**

- protocol_domain: fixed H/BMCP domain discriminator and contract family.
- authority_ref: authority owning this operation namespace.
- tenant_or_scope_ref: already-resolved tenant/canonical scope identity, not a display string.
- operation_kind: separates semantically distinct commands.
- key_profile: agreed opaque-key encoding/version.
- idempotency_key: opaque caller-generated value.

**Default scope is per authority + tenant/scope + operation kind**, not per-agent, per-session or per-attempt. Agent and Session are bound request attributes and authorization inputs, not default dedupe dimensions. An explicitly agent-owned operation may add a stable agent_authority_ref only through a separately reviewed profile. Session rotation/reconnect must not create a new logical operation. Attempt ID is never part of the idempotency key.

### 3.2 Generation and collision isolation

1. The initiating Producer/Client generates one opaque key before first send and retains it across retry/reconnect.
2. H MUST NOT mint a new key merely because of timeout, lost ACK or reconnect.
3. Each transport execution receives a fresh H Attempt ID.
4. The key profile must provide collision-resistant uniqueness appropriate to deployment. Entropy/encoding details remain OPEN pending H/I security review; no UUID/hash/cryptographic algorithm is selected here.
5. Namespace components must use an unambiguous, versioned, length-delimited canonical tuple encoding. Ambiguous delimiter concatenation is prohibited.
6. The same raw key in another authority, tenant/scope or operation kind is a different identity. Same full tuple with a different request digest is Conflict, not a second operation.
7. A key must not be derived solely from mutable Session ID, Agent display name, timestamp, payload digest or Attempt ID.

### 3.3 Request digest binding

The first accepted request binds the full namespace tuple to one immutable request digest and exact final request boundary. Digest algorithm, canonical serialization, volatile transport-field treatment and profile negotiation remain owned by the applicable C/H contract and must be pinned consistently; this proposal does not define a competing digest profile. A retry must reproduce the same semantic digest. Changed semantic payload requires a new logical operation and new key.

## 4. Deduplication window and persistence

- Deduplication begins when the authoritative H replay ledger durably reserves the full tuple and binds its request digest; not in an in-memory cache.
- The record and replay-protection tombstone remain available for at least the maximum retry/recovery/replay horizon declared by the owning policy. No fixed duration is invented here. If no finite safe horizon is defined, the identity cannot silently expire while replay could still cause an effect.
- Expiry of response body/telemetry does not permit key reuse. A compact tombstone must reject conflicting reuse for the required horizon.
- H protocol receipt/replay metadata resides in the H-owned durable ledger. Business mutation, immutable domain version, CAS, idempotency record and canonical commit sequence are Storage-owned and must follow AID-2026-098.
- H admission receipt does not prove Storage business commit. Storage prepared receipt alone is not G Applied.
- If H and Storage ledgers cannot be atomically updated under the applicable Storage/COC contract, the operation stays Pending/Unknown until reconciliation proves its terminal result.

## 5. Linearization points

There are two distinct points:

1. **H admission linearization:** the authoritative H replay ledger commits a unique reservation for the full tuple, request digest, logical operation reference and first Attempt ID, with a durable admission receipt. Concurrent contenders must serialize to one winner. Before this point the request is not durably accepted; after it, retries resolve to the same logical operation.
2. **Domain-effect linearization:** the Storage AID-2026-098 commit point for the business mutation and its idempotency receipt/canonical commit sequence as one recoverable boundary. H does not define that transaction and H admission does not imply it occurred.

C final request boundary, CSubmitOutcome and G Applied linearization remain independently governed by C and G. H linearization does not imply provider handoff, Adapter application or G Applied.

## 6. Durable receipt and immutability

Candidate minimum receipt fields (vocabulary only; not a frozen schema):

~~~yaml
receipt_schema: h-idempotency-receipt/0.1
receipt_id: <stable opaque ID>
protocol_domain: <H/BMCP domain>
namespace:
  authority_ref: <authority>
  tenant_or_scope_ref: <resolved scope>
  operation_kind: <operation>
  key_profile: <profile version>
  idempotency_key: <opaque key>
logical_operation_id: <stable logical operation ID>
request_digest: {profile: <pinned profile>, value: <digest>}
final_request_boundary_ref: <immutable boundary ref>
first_attempt_id: <H attempt ID>
observed_attempt_id: <current/retry attempt ID>
receipt_state: <PENDING | SUCCEEDED | FAILED>
disposition: <NEW | DUPLICATE | CONFLICT>
admitted_at: <UTC timestamp>
terminal_at: <UTC timestamp or null>
domain_commit_ref: <Storage-owned ref or null>
c_outcome_ref: <C-owned immutable ref or null>
applied_attestation_ref: <evidence ref consumed by G or null>
issuer: {authority_ref: <H authority>, key_ref: <verification key ref>}
integrity: {profile: <pinned profile>, digest: <receipt digest>, proof_ref: <signature or immutable proof>}
~~~

The receipt also binds authenticated caller/principal and I authorization-decision reference, without treating either as current replay authorization. Sensitive payload plaintext is not copied into the receipt.

- receipt_id, namespace tuple, logical operation ID, request digest, final boundary and first Attempt ID are immutable after admission.
- Retry creates a new Attempt ID and append-only observation; it never overwrites the receipt or earlier attempt evidence.
- State changes are append-only transition/evidence records. A mutable latest-status projection may be cached but is not the audit source.
- A terminal receipt cannot be rewritten from SUCCEEDED to FAILED or vice versa. Correction uses a new linked record with issuer/reason; original remains.
- Receipt digest/signature authenticates exact immutable fields and evidence refs. Cryptographic profile remains OPEN pending H/I registration and acceptance.

## 7. Failure and duplicate semantics

| State/disposition | Meaning | Rule |
|---|---|---|
| Unknown | No authoritative durable reservation/terminal record can be established, or lookup/recovery authority is unavailable. Epistemic state; not proof of no side effect. | Retry same tuple/key/digest with new Attempt ID; query/reconcile authoritative ledger. Never claim success or safe-to-create-new-key. |
| Pending | Durable H reservation exists; no authoritative terminal domain outcome yet. | Same-key/same-digest retry returns Pending/existing receipt; reconcile Storage/C evidence; do not execute another logical operation. |
| Failed | Authoritative durable terminal failure recorded. | Same key returns same terminal failure. A new semantic attempt after terminal failure is a new logical operation with a new key and explicit successor link. |
| Duplicate | Current request matches existing tuple/key/digest. Response disposition, not stored lifecycle state. | Return existing receipt/state; no repeated side effect. Recheck I authorization and D Fence before protected disclosure. |
| Conflict | Same full tuple/key, different request digest. | Reject IdempotencyConflict; do not mutate old receipt or create another operation. |

Timeout, connection loss, crash, missing ACK, unavailable ledger, unverifiable signature or incomplete recovery are Unknown/Pending, not Failed. Failed requires authoritative terminal failure evidence. A validation/authorization rejection before H admission is non-accepted and must not be misreported as durable operation failure.

## 8. Replay and crash recovery

1. Retry of the same logical operation reuses full tuple, key, logical operation ID and request digest.
2. Every transport execution gets a fresh Attempt ID. Attempt evidence is append-only under logical operation + Attempt ID.
3. Recovery resolves existing H receipt, then Storage AID-2026-098 transaction/receipt. Absence in a stale replica or timeout does not prove “not committed”.
4. If Storage reports committed, H may return the immutable result reference only after current replay authorization and Fence checks. Durable terminal abort/failure is returned as terminal. Unresolved Storage means Pending/Unknown and reconciliation, not repeated business side effect.
5. Crash after H reservation but before domain commit leaves Pending reservation for reconciliation. Crash after domain commit but before H terminal projection requires reading Storage commit receipt and appending H terminal observation; never repeat the mutation.
6. New logical operation, changed semantic payload or explicit successor after terminal result uses a new key and logical operation ID. It may link to predecessor but never reuse receipt identity.

### 8.1 C/G Applied join

- H receipt/delivery ACK proves H protocol/transport facts only.
- H evidence joins exact immutable CSubmitOutcome by record ref, sequence, payload digest and final request boundary; if C supplies ActualInferenceRequestId it must equal H inference request ID.
- C alone owns Outcome and SideEffectStatus. H cannot infer provider success from transport ACK or rewrite C outcome.
- G alone owns durable Applied. G consumes authenticated H evidence, C outcome, COC/Storage same-GID terminal proof, I authorization, D Fence lineage and G predicates.
- Under AID-2026-091 AP-02/AP-09, logical Delivery ID stays stable across retries while each retry uses a distinct DeliveryAttempt ID. H Attempt ID must map explicitly to that identity. Retry receipt never overwrites prior AppliedAttestation. Lost ACK remains Unknown/Pending, never Applied.

## 9. Fence and replay disclosure

A historically valid receipt is not perpetual permission to disclose its result. Before returning an existing result or protected receipt fields, H independently rechecks:
- I current authorization, PermissionEpoch, issuer/key status, principal/delegation, audience and scope;
- D current ForgetOperation/Fence/lineage applicability and currentness.

Both checks fail closed: either False/denied means no protected disclosure; either Unknown/unavailable/exception means no disclosure and a non-disclosing Unknown/authorization-pending response; only both current and valid permit the allowed receipt/result reference. D owns Fence generation/lineage/suppression. I owns authorization/revocation and global Forget policy. H cannot clear Fence or treat replay as permission to re-materialize forgotten content. Historical receipt remains immutable even when current-use/disclosure eligibility is revoked.

## 10. Non-goals and unresolved decisions

This proposal does not define Storage schema, database transaction, WAL/fsync profile, COC same-GID protocol, VisibilityPointer or PublicationReceipt; these belong to Storage/AID-2026-098. It does not define CSubmitOutcome or G Applied semantics, D namespace canonicalization/Fence generation, I policy, crypto/key/hash/canonical-JSON/entropy profiles, or a fixed dedupe TTL. It does not claim production multi-replica linearizability, durable replay, crash recovery or runtime conformance.

Open decisions: H/I acceptance of key/receipt profiles; exact AID-2026-098 Storage pin and retention mapping; H Attempt ID ↔ C/G DeliveryAttempt mapping; C/G/H acceptance of digest/final-boundary join; D/I replay callback evidence; Owner acceptance of H admission linearization.

## 11. Reviewer checkpoints

PASS/FAIL must be recorded against exact document version and evidence. DOCUMENTED_ONLY may pass by text inspection. EVIDENCE_REQUIRED cannot pass from prose or a local shape test.

| ID | PASS iff | FAIL iff | Evidence |
|---|---|---|---|
| HIR-01 | Full tuple has protocol domain, authority, resolved scope, operation kind, key profile and opaque key | Raw key alone or ambiguous tuple | DOCUMENTED_ONLY |
| HIR-02 | Producer creates one key per logical operation and retains it across retries | Key rotates on timeout/reconnect | DOCUMENTED_ONLY |
| HIR-03 | Agent/session are bound attributes, not default dedupe dimensions; Attempt is separate | Session/Agent/Attempt splits one logical operation | DOCUMENTED_ONLY |
| HIR-04 | Namespace encoding is unambiguous and cross-domain isolated | Ambiguous concatenation/cross-scope alias | DOCUMENTED_ONLY |
| HIR-05 | Dedup starts at durable H reservation; tombstone exceeds replay horizon | Memory-only or early expiry allows duplicate effect | EVIDENCE_REQUIRED |
| HIR-06 | Storage mutation, version/CAS, idempotency receipt and commit sequence follow AID-2026-098 | H invents Storage atomicity or partial write is treated committed | EVIDENCE_REQUIRED |
| HIR-07 | H admission LP is durable unique reservation; domain-effect LP is Storage-owned | Admission conflated with business commit | DOCUMENTED_ONLY |
| HIR-08 | Concurrent same-key contenders produce one logical operation and durable receipt | Two winners or no recoverable winner | EVIDENCE_REQUIRED |
| HIR-09 | Receipt binds namespace, digest, logical operation, first/current Attempt, boundary, issuer and proof refs | Identity/provenance missing or mutable | DOCUMENTED_ONLY |
| HIR-10 | Receipt identity immutable; transitions append-only | Retry overwrites receipt/terminal outcome | DOCUMENTED_ONLY |
| HIR-11 | Timeout/crash/unavailable resolver/unverifiable evidence stays Unknown/Pending | Uncertainty inferred as success or terminal failure | DOCUMENTED_ONLY |
| HIR-12 | Pending duplicate returns existing receipt without second logical execution | Pending duplicate starts another side effect | EVIDENCE_REQUIRED |
| HIR-13 | Failed requires durable authoritative terminal failure | Transient/ambiguous error becomes terminal Failed | DOCUMENTED_ONLY |
| HIR-14 | Same key/same digest is Duplicate; different digest is Conflict | Mismatch returns old success or mutates receipt | EVIDENCE_REQUIRED |
| HIR-15 | Same logical retry reuses key/logical ID; every transport retry gets fresh Attempt ID | Attempt reused or ordinary retry gets new key | DOCUMENTED_ONLY |
| HIR-16 | Crash before/after Storage commit reconciles without repeating effect | Recovery loses committed result or repeats mutation | EVIDENCE_REQUIRED |
| HIR-17 | H Attempt maps to distinct C/G DeliveryAttempt; G Applied needs its own full evidence | H ACK/receipt promoted to Applied or overwrites evidence | EVIDENCE_REQUIRED |
| HIR-18 | Replay disclosure rechecks I authorization and D Fence independently, fail-closed | Historical receipt/signature bypasses current I/D | EVIDENCE_REQUIRED |

## 12. Disposition

**DOCUMENTED CANDIDATE ONLY.** The proposal separates H idempotency, C outcome, G Applied, D Fence, I authorization and Storage atomicity. It does not establish cross-owner acceptance, availability of AID-2026-098, or implementation conformance. All EVIDENCE_REQUIRED checkpoints remain OPEN. No runtime, validator, schema, workflow, deployment or Issue state is changed.
