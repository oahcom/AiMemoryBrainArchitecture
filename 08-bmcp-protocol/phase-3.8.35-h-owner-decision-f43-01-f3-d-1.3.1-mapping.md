# H Owner Decision — F-43-01/F3 D 1.3.1 Consumer Mapping

- Decision ID: **H-OWNER-2026-11-19-003**
- Predecessor decision: **H-OWNER-2026-11-19-002**, Issue #43 comment `7021522737` (typed mapping acceptance); this decision extends that acceptance only to the expanded C1–C6 consumption mapping and abstract query request/response in this exact document.
- Owner: **H Domain Owner**
- Scope: **AID-2026-010 / Issue #43 / F-43-01 / F3 only**
- Decision: **ACCEPT WITH EXPLICIT LIMITATIONS**
- D successor: 08-bmcp-protocol/owner-snapshot-namespace-and-fence-currentness-contract-1.3.1.md
- Exact D successor Blob: 12b71e770f4e977c7f147694a644066bc2ce11b9
- D successor Commit: b03e31c7dafea77b610cd49b402dab273dae2412
- D-002 proof package Blob: 4c8672a68e4339e40b5d8cb98eb073af8c98c1a5
- D Owner Decision: D-OWNER-2026-11-19-003
- H schema: bmcp.coc-jf10-unified-1.2.17.schema.json, Blob 1b8f44675f30919764481d33755c566ef5cf1ea8
- H TEST validator: owner_snapshot_semantics_1_2_17.py, Blob d9dc43ff0136751aba20cffa4db3f280d16edc67
- H branch: `session-h-bmcp-protocol`; reviewed baseline HEAD `de5d7b63ff8555a9bbd58f9dd64d4c28fbc7e5cc`.
- Decision artifact commit chain: `33c25d32176ddd5f5ee34fb7bbd507aad67be4df` (parent: reviewed baseline above), followed by clarification commit `940963af09fe25ffb862b69ac5f272050cf000f2` (current branch HEAD at this decision).

## 1. Independent H decision

H independently reviewed the exact D 1.3.1 Blob and D-002 proof package. D Owner's ACCEPT is treated as D-source authority, not as H's decision.

**H DECISION: ACCEPT WITH EXPLICIT LIMITATIONS.**

H accepts the normative field mapping, nominal-type separation, C1-C6 consumption rules and abstract query dependency below. This is not a D/H jointly frozen wire schema, deployed endpoint, runtime verification or production authorization. D Runtime has not designated an implementation repository or authoritative storage. No callable D runtime endpoint was established.

This decision is limited to F-43-01/F3. It does not decide F1, close F3, or authorize production consumption.

## 2. Independent field mapping matrix

H 1.2.17 carries D-specific values in owner_specific_high_waters using the closed-world ownerSpecificHighWatersD shape. JSON Schema uses strings; nominal types arise from exact D field identity and authority, not the JSON primitive.

| D field / nominal type | D authority | H field / interface | H type and conversion | Missing / unknown / stale / conflict | H decision |
|---|---|---|---|---|---|
| producer_registration_high_water — ProducerRegistrationHighWater / ProducerRegistrationSequence | D ProducerWork Registration Ledger, scoped to exact Brain Authority + Producer Registration Ledger identity; immutable BarrierSnapshotReceipt | owner_specific_high_waters.producer_registration_high_water; query response producer_registration_high_water | JSON string; canonical non-negative decimal representation for this type only, range 0..2^63-1. Preserve field identity. No arithmetic with other counters. | Missing/unavailable UNKNOWN/BLOCKED; explicit mismatch against Install receipt's same-typed cutoff INVALID; superseded snapshot STALE; ledger identity conflict INVALID. | ACCEPT, subject to canonical output and authoritative receipt limitations. |
| forget_fence_generation_high_water — ForgetFenceGeneration | D ForgetFence authority / generation state in ForgetFence namespace | owner_specific_high_waters.forget_fence_generation_high_water; query response forget_fence_generation | JSON string; canonical non-negative decimal representation for this type only. Never cast, compare or derive from ProducerRegistrationHighWater. | Missing/unavailable UNKNOWN/BLOCKED; explicit generation mismatch INVALID or STALE only under D state-version rule; revocation independently INVALID/STALE. | ACCEPT. |
| work_item_high_water — D ProducerWork ledger high-water | D ProducerWork ledger | owner_specific_high_waters.work_item_high_water | Opaque D-local decimal string; not registration sequence or commit cursor. | Missing UNKNOWN/BLOCKED; conflict INVALID; superseded snapshot STALE. | ACCEPT, D-local only. |
| attempt_high_water — D attempt sequence | D ProducerWork attempt ledger | owner_specific_high_waters.attempt_high_water | Opaque D-local decimal string; not work-item or fence generation. | Same fail-closed classifications. | ACCEPT, D-local only. |
| barrier_generation — D barrier-generation type | D Forget barrier state | owner_specific_high_waters.barrier_generation | Opaque D-local decimal string; separate from ForgetFenceGeneration and H owner_gate_generation. | Same fail-closed classifications. | ACCEPT, D-local only. |
| barrier_root — D barrier root digest | D barrier snapshot/reconciliation ledger | owner_specific_high_waters.barrier_root | Lowercase 64-hex SHA-256 digest, compared only with same named root in same snapshot. | Missing UNKNOWN/BLOCKED; malformed or mismatch INVALID; stale snapshot STALE. | ACCEPT. |
| dependency_closure_cursor — D dependency-closure cursor | D dependency inventory | owner_specific_high_waters.dependency_closure_cursor | Opaque cursor string; never parse as registration sequence, fence generation or CanonicalCommitCursor. | Missing UNKNOWN/BLOCKED; incompatible binding INVALID; old snapshot STALE. | ACCEPT. |
| dependency_closure_root — D dependency-closure root digest | D dependency inventory | owner_specific_high_waters.dependency_closure_root | Lowercase 64-hex SHA-256 digest bound to exact closure cursor and snapshot. | Missing UNKNOWN/BLOCKED; mismatch INVALID; stale STALE. | ACCEPT. |

### Common D snapshot fields consumed by H

| D concept | H carrier | Rule |
|---|---|---|
| D owner identity | owner="D" | Must match D owner key; no owner substitution. |
| Owner gate identity/generation | owner_gate_ref, owner_gate_generation | H gate values only; not ForgetFenceGeneration. |
| Scope generation | scope_generation_ref | Opaque scope version; not inferred from gate/fence generation. |
| Request/admission ledgers | request_high_water, admission_high_water, counts, digests and roots | H gate snapshot completeness only; not substitutes for D ProducerRegistrationHighWater or D-002 proof. |
| D owner ledger root | owner_ledger_root | Frozen-ledger digest; does not prove C1-C6 alone. |
| Owner snapshot attestation | owner_snapshot_attestation_ref, owner_snapshot_attestation_digest; release-level owner_snapshot_ref / owner_snapshot_digest where present | Immutable opaque identity + digest; must be resolved and verified against D authority. |
| Anti-rollback anchor | anti_rollback_anchor_ref | Must be checked by D-authoritative currentness/anti-rollback evidence; H cache/clock insufficient. |
| Owner-specific values digest | owner_specific_high_waters_digest | Binds complete D object under a mutually agreed canonical profile. Existing TEST helper digest is not production profile. |

**Shape boundary:** H schema carries eight D owner-specific values and generic snapshot/attestation references. It does not inline the full InstallForgetFence receipt, BarrierSnapshotReceipt, C1-C6 evidence, FenceCursor tuple or installation CanonicalCommitCursor. H must not infer those facts from the eight-value object. They must be obtained through the D-authoritative query dependency in §5. The binding from H owner snapshot reference/attestation to exact D BarrierSnapshotReceipt must be explicit in a future D/H interface contract; it is not assumed from similar names.

## 3. Mandatory nominal-type isolation

1. ProducerRegistrationHighWater is the high-water of ProducerRegistrationSequence in the D ProducerWork Registration Ledger, scoped to exact Brain Authority and Producer Registration Ledger identity. Authority: D registration ledger and immutable BarrierSnapshotReceipt.
2. ForgetFenceGeneration is allocated by D ForgetFence authority and belongs only to the ForgetFence namespace.

H mappings:
- producer_registration_high_water maps only to ProducerRegistrationHighWater.
- forget_fence_generation_high_water maps only to ForgetFenceGeneration.

**Forbidden:** numerical comparison, cast, conversion to a common scalar, ordering comparison, subtraction, cross-field range comparison, aliasing, substitution or deriving one from the other. Decimal syntax validation, if required, is performed independently inside each nominal field and never creates a common comparable value. Their equality is not a D-002 condition.

The only D-002 equality is between InstallForgetFence receipt captured_producer_registration_high_water and CaptureProducerRegistrationHighWater receipt producer_registration_high_water: both are the same nominal ProducerRegistrationHighWater for the same immutable operation/fence/snapshot. Greater-than/less-than is never a success case.

D 1.3.1 §5.1 accepts and canonicalizes leading zeroes within each nominal type. H's current TEST validator requires canonical decimal lexical form (0 or non-zero-leading digits) independently for each D high-water, but it does not enforce D's upper bound of 2^63-1; it only applies the decimal lexical regex (plus the schema's string length bound). Therefore the proposed H↔D boundary requires D to emit the canonicalized decimal string and bind that exact representation in its receipt/digest, while a future H production validator must independently enforce the D range 0..2^63-1. H will not rewrite signed receipt bytes. Non-canonical representation is INVALID; missing canonicalization provenance or unverified range is UNKNOWN/BLOCKED. This is an explicit interoperability/implementation precondition, not a claim of current D Runtime support.

## 4. H consumption of D-002 C1-C6

All six conditions are **conjunctive** and must hold for one exact immutable ForgetOperation/fence/snapshot tuple. H does not treat schema shape or a subset as proof.

| Condition | D normative fact | H consumption | Failure behavior |
|---|---|---|---|
| C1 — Authority, ledger identity, registry version | Same BrainAuthorityId, Producer Registration Ledger identity/namespace, ProducerRegistryVersion | H pins expected authority and ledger identity; D response returns all three. H checks exact equality across Install receipt and BarrierSnapshotReceipt. Registry version remains its own nominal version. | Explicit mismatch INVALID; unavailable/incomplete registry or ledger UNKNOWN/BLOCKED. |
| C2 — Operation/idempotency | Same ForgetOperationId, idempotency identity, canonical request digest, exact target-set digest | H pins original operation ID, idempotency identity and digests; D proof binds them to durable Install receipt and snapshot. Exact replay reuses same identity/digests. | Changed digest under same identity INVALID / IDEMPOTENCY_CONFLICT; missing record UNKNOWN/BLOCKED. Never mint a new operation/cutoff for recovery. |
| C3 — Fence cursor/generation/install commit cursor | Same ForgetFenceCursor / ForgetFenceGeneration and installation CanonicalCommitCursor | H consumes typed FenceCursor tuple (ForgetOperationId, ForgetFenceGeneration, TargetSetDigest), generation and installation CanonicalCommitCursor from D immutable receipt. No numeric comparison with registration high-water. | Explicit mismatch INVALID or STALE only under D state-version rule; missing evidence UNKNOWN/BLOCKED. |
| C4 — Install/Capture exact equality | Install receipt captured cutoff equals Capture receipt producer_registration_high_water as same nominal type and same snapshot | H checks exact typed equality only after C1-C3 identity binding. Never compares either with ForgetFenceGeneration. | Same-type inequality INVALID; missing receipt/type UNKNOWN/BLOCKED. |
| C5 — Receipt identity + ledger consistency | BarrierSnapshotReceipt binds C1-C4 plus D-authoritative ledger consistency proof/reference | H resolves exact immutable receipt through D query; verifies identity/digest, authority/ledger binding, consistency proof and D proof status. Pointer/digest alone insufficient. | Malformed/contradictory proof INVALID; unavailable/incomplete consistency evidence UNKNOWN/BLOCKED. |
| C6 — Linearized ordering/disposition | Accepted pre-fence registrations included at/below H; covered post-fence ordinary registrations rejected/quarantined or cleanup-only and cannot publish | H consumes D serialization proof and disposition/inventory evidence. No admitted-but-unaccounted publishable work may remain. Counts/roots alone do not prove C6. | Explicit violation INVALID; unresolved order, registry gap, partial inventory or missing lineage UNKNOWN/BLOCKED; barrier remains open. |

### Aggregate classification

- C1 AND C2 AND C3 AND C4 AND C5 AND C6 proven from same D-authoritative evidence => D proof candidate VALID.
- Explicit identity/operation/cursor/snapshot/same-typed cutoff mismatch => INVALID, or STALE only where D authoritative state-version rule requires it.
- Missing/unavailable ledger, registry, receipt, consistency proof, serialization order or anti-rollback evidence => UNKNOWN/BLOCKED. Partial success never becomes VALID.
- Currentness/state-version and revocation are independent checks after C1-C6: authoritative state-version mismatch => STALE; explicit revocation => INVALID; unavailable authority state => UNKNOWN/BLOCKED. Six conditions do not replace currentness/revocation.
- H consumes D-authoritative proof status for D-owned semantics; H does not mint D receipts, reorder D events, infer missing evidence or declare D barrier drained.

## 5. H-required D authoritative query interface (abstract dependency)

### 5.1 Name, responsibility and status

**Proposed interface:** ResolveForgetFenceSnapshotProof.

**Responsibility:** resolve one already-installed ForgetOperation/Fence to its immutable D BarrierSnapshotReceipt, return D-002 C1-C6 evidence and classification, and independently return currentness/revocation state. Read/resolve only; it must never create, move, reset or advance a fence cutoff.

**Status:** H abstract dependency / normative proposal only — **NOT IMPLEMENTED / NOT DEPLOYED / NOT VERIFIED**. D operation contract describes semantic operation names, not callable public APIs. No D Runtime repository, authoritative storage, endpoint URL, transport, authentication contract or live ledger was established from the exact D artifacts.

### 5.2 Request (conceptual; not an existing JSON schema)

    ResolveForgetFenceSnapshotProofRequest {
      interface_version: "1.0";
      d_contract_revision: "1.3.1";
      d_contract_blob_sha256: "12b71e770f4e977c7f147694a644066bc2ce11b9";
      d_schema_artifact_revision: "NOT_PUBLISHED";
      brain_authority_id: BrainAuthorityId;
      producer_registration_ledger_id: ProducerRegistrationLedgerId;
      forget_operation_id: ForgetOperationId;
      idempotency_identity: ForgetIdempotencyIdentity;
      canonical_request_digest: CanonicalRequestDigest;
      target_set_digest: TargetSetDigest;
      expected_fence_cursor?: ForgetFenceCursor;
      expected_snapshot_ref?: BarrierSnapshotReceiptRef;
      expected_snapshot_digest?: SHA256Digest;
      expected_producer_registry_version?: ProducerRegistryVersion;
      owner_snapshot_ref?: OwnerSnapshotRef;
      owner_snapshot_attestation_ref?: OwnerSnapshotAttestationRef;
      owner_snapshot_attestation_digest?: SHA256Digest;
      consistency_requirement: "D_AUTHORITATIVE_LINEARIZABLE";
      include_currentness_and_revocation: true;
    }

Inputs are typed opaque identities/digests except where their own type defines local encoding. Expected values are comparison anchors, not instructions to create or recapture state.

### 5.3 Response (conceptual; not an existing deployed schema)

    ResolveForgetFenceSnapshotProofResponse {
      interface_version: "1.0";
      d_contract_revision: "1.3.1";
      d_contract_blob_sha256: SHA256Digest;
      d_schema_artifact_revision: "NOT_PUBLISHED";
      authority: {
        brain_authority_id: BrainAuthorityId;
        producer_registration_ledger_id: ProducerRegistrationLedgerId;
        producer_registry_version: ProducerRegistryVersion;
      };
      operation: {
        forget_operation_id: ForgetOperationId;
        idempotency_identity: ForgetIdempotencyIdentity;
        canonical_request_digest: CanonicalRequestDigest;
        target_set_digest: TargetSetDigest;
      };
      fence: {
        forget_fence_cursor: ForgetFenceCursor;
        forget_fence_generation: ForgetFenceGeneration;
        installation_canonical_commit_cursor: CanonicalCommitCursor;
        fence_state_version: FenceStateVersion;
      };
      immutable_snapshot: {
        barrier_snapshot_receipt_ref: BarrierSnapshotReceiptRef;
        barrier_snapshot_receipt_digest: SHA256Digest;
        captured_producer_registration_high_water: ProducerRegistrationHighWater;
        producer_registration_high_water: ProducerRegistrationHighWater;
        producer_registry_version: ProducerRegistryVersion;
        ledger_consistency_proof_ref: LedgerConsistencyProofRef;
        ledger_consistency_proof_digest: SHA256Digest;
        serialization_order_proof_ref: SerializationOrderProofRef;
        included_pre_fence_registration_set_root: SHA256Digest;
        post_fence_disposition_set_root: SHA256Digest;
      };
      d002_conditions: {
        C1: "PROVEN" | "MISMATCH" | "UNAVAILABLE";
        C2: "PROVEN" | "MISMATCH" | "UNAVAILABLE";
        C3: "PROVEN" | "MISMATCH" | "UNAVAILABLE";
        C4: "PROVEN" | "MISMATCH" | "UNAVAILABLE";
        C5: "PROVEN" | "MISMATCH" | "UNAVAILABLE";
        C6: "PROVEN" | "MISMATCH" | "UNAVAILABLE";
      };
      proof_status: "VALID" | "INVALID" | "UNKNOWN" | "BLOCKED";
      currentness: {
        state_version: FenceStateVersion;
        status: "CURRENT" | "STALE" | "REVOKED" | "UNKNOWN";
        revocation_ref?: RevocationRef;
      };
      authoritative_snapshot_identity: DSnapshotIdentity;
      observed_at_authority_commit_cursor: CanonicalCommitCursor;
    }

Both C4 values are explicitly ProducerRegistrationHighWater. No common scalar is exposed and no comparison with ForgetFenceGeneration is defined. C1-C6 entries are independent conjunct evidence bound to one immutable receipt; D must authenticate the response under a D-authoritative identity/key scheme, still to be specified by D.

### 5.4 Authority, immutability, linearization and statuses

- Authority: only D authoritative ForgetFence authority and ProducerWork Registration Ledger answer. H cache, replica, local DB, COC manifest, static fixture or unverifiable signed payload is not authoritative.
- Snapshot identity: receipt ref + digest + operation/fence tuple form immutable identity. Repeated query returns same receipt/cutoff. Reconciliation may append checkpoints but cannot mutate original receipt/cutoff.
- Consistency: linearizable/serializable D-authoritative snapshot; prove RegisterProducerWork and InstallForgetFence share the same ordering domain. No split reads, TTL or local wall clock.
- VALID: all six C1-C6 proven for same tuple and independent currentness is CURRENT with no revocation.
- INVALID: explicit identity/operation/cursor/same-typed cutoff/receipt/serialization mismatch, invalid proof authentication, or explicit revocation.
- STALE: D authoritative state-version proves queried fence/snapshot was superseded or is no longer current.
- UNKNOWN: authority cannot establish answer, evidence missing, ledger gap, timeout, transport failure, partial persistence or no currentness proof.
- BLOCKED: H operational disposition while proof is UNKNOWN, unavailable, version-incompatible or unsafe. BLOCKED is not a successful D proof.
- Incompatible interface/contract/schema revision fails closed. Response states exact D contract revision and Blob digest. D schema revision remains NOT_PUBLISHED.

### 5.5 Timeout, retries, recovery and revision binding

- Timeout/no response => UNKNOWN/BLOCKED, never abort or success.
- Retry is read-only with exact same operation ID, idempotency identity, request digest and target digest. Resolve original receipt; never create a new identity, generation or cutoff.
- After lost Install ACK, resolve original operation/receipt first. Capture only retrieves install-bound immutable snapshot; it does not create a cutoff.
- Unproven ledger continuity, anti-rollback or currentness after restore => UNKNOWN/BLOCKED.
- Interface v1.0 is proposed to bind to D contract revision 1.3.1 and exact Blob SHA above. No D 1.3.1 JSON Schema artifact exists in reviewed evidence; d_schema_artifact_revision remains NOT_PUBLISHED. H wire schema 1.2.17 is not a D schema.

## 6. Existing interfaces vs proposed dependencies

| Item | Evidence/status | H classification |
|---|---|---|
| D InstallForgetFence | Normative operation in D operation contract; no callable API asserted | SPECIFIED / NOT ESTABLISHED AS CALLABLE |
| D CaptureProducerRegistrationHighWater | Normative read/verification operation; immutable receipt semantics specified | SPECIFIED / NOT ESTABLISHED AS CALLABLE |
| D ResolveProducerWork | Normative read/resolve operation in D operation contract §3.8 | SPECIFIED / NOT ESTABLISHED AS CALLABLE |
| D ReconcileForgetBarrier | Normative reconciliation operation in D operation contract §3.9 | SPECIFIED / NOT ESTABLISHED AS CALLABLE |
| ResolveForgetFenceSnapshotProof | New H-required aggregate query interface defined here | ABSTRACT DEPENDENCY / PROPOSED / NOT IMPLEMENTED |
| H schema 1.2.17 ownerSpecificHighWatersD | Exact schema exists; eight D fields structurally defined | STRUCTURAL WIRE SHAPE ONLY |
| H validate_owner_snapshot_1_2_17 | TEST-profile validator; attestation/currentness/anti-rollback injected | TEST PROFILE ONLY; NOT PRODUCTION VALIDATION |

No item is represented as a deployed endpoint. No API invocation, live ledger query or production attestation verification was performed.

## 7. Conversion and fail-closed rules

1. JSON serialization preserves each D field name and string value exactly. No aliases or generic high_water field.
2. Decimal syntax/range validation is local to each nominal type. H never casts the two critical fields to a shared integer or compares magnitudes. D must canonicalize output before signing/digesting.
3. Digests are lowercase 64-character SHA-256 strings, checked only against exact named object/receipt under the same canonical profile.
4. Opaque refs/cursors/versions are byte-preserving identifiers. No trimming, case folding, URI normalization or parsing unless that exact D type defines it.
5. Unknown additional D owner-specific fields fail schema validation; missing required fields fail closed. New D revision requires a new exact mapping review.
6. Stale/revoked snapshot is not rescued by matching high-waters. Six conditions do not substitute for currentness/revocation.
7. D 1.3.1 Unicode 15.1.0 namespace canonicalization is D-owned. H treats canonical D namespace identities as opaque and verifies D binding; H does not recanonicalize with host Unicode tables.

## 8. Explicit limitations, assumptions and unresolved items

**Normative mapping accepted; runtime not accepted:**

1. D Runtime implementation repository and authoritative storage are unspecified. No live query endpoint, callable API, service authentication contract, deployment identity, consistency implementation or operations/SLO contract.
2. D has not published a D 1.3.1 JSON Schema artifact. This decision binds to exact normative contract and D-002 proof Blobs, not an invented D schema revision.
3. D/H must explicitly bind H owner_snapshot_ref / attestation to D BarrierSnapshotReceiptRef. This is not inferred from similar names.
4. D must define/authenticate proof response, key identity/rotation/revocation, canonical digest projection and ledger consistency proof format. H TEST helper digest prefix is not production-approved.
5. D must guarantee canonicalized decimal wire output for both nominal high-waters while preserving distinct nominal types. H TEST validator rejects leading-zero decimal strings and does not rewrite signed payloads. It also does not enforce the D upper bound 2^63-1; a production H validator must add per-nominal-type range checks before any proof is eligible.
6. C6 requires D serialization/inclusion/disposition proof; it cannot be established from schema fields, aggregate counts or static fixtures. No race, crash, restore, anti-rollback or barrier-reconciliation runtime test was run.
7. H validator uses injected attestation, ledger-currentness and anti-rollback callbacks; it has no live D adapter. Structural schema validity is not semantic validity.
8. No D or H runtime repository was named for this query interface; no production capability is inferred.

These are blocking limitations on runtime consumption and production authorization. Normative mapping acceptance waives none of them.

## 9. Verification and execution record

- Exact source review: D successor Blob 12b71e770f4e977c7f147694a644066bc2ce11b9; D proof Blob 4c8672a68e4339e40b5d8cb98eb073af8c98c1a5; H schema Blob 1b8f44675f30919764481d33755c566ef5cf1ea8; H TEST validator Blob d9dc43ff0136751aba20cffa4db3f280d16edc67.
- Repository tests for this decision: **NOT RUN**.
- D endpoint/query: **NOT RUN — no callable endpoint identified**.
- Production cryptographic attestation/currentness/anti-rollback: **NOT RUN / NOT VERIFIED**.
- CI: **NOT RUN for this decision artifact**.
- No test command, runtime environment or test output is claimed.

## 10. Formal H Owner disposition

**Decision ID:** H-OWNER-2026-11-19-003

**Decision:** **ACCEPT WITH EXPLICIT LIMITATIONS** — H independently accepts the normative D 1.3.1 field mapping, nominal-type separation, C1–C6 conjunctive consumption mapping, and the abstract `ResolveForgetFenceSnapshotProof` request/response contract as the required H dependency, limited to the exact D/H Blobs listed in this document. This decision is the expanded-artifact follow-on to H-OWNER-2026-11-19-002 (Issue #43 comment `7021522737`); it does not replace or broaden that earlier typed-mapping decision. §8 limitations are binding preconditions. No production endpoint is accepted or authorized.

**Finding boundary:**
- H decision is only F-43-01/F3 mapping; predecessor H-OWNER-2026-11-19-002 is preserved at Issue #43 comment `7021522737`.
- F-43-01/F3 remains OPEN pending D/H acceptance of same exact mapping Blob, interface contract verification, A Integration readback/acceptance and A's authoritative Finding Ledger update.
- This does not decide F-43-01/F1 implementation status.
- It does not alter D Owner contract or D Owner decision.
- It does not authorize production H consumption.
