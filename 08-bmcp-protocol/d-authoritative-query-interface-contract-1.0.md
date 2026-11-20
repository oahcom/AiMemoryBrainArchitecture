# D Authoritative Query Interface Contract — 1.0

- Contract ID: `D-AUTH-QUERY-1.0`
- Status: **D OWNER NORMATIVE CONTRACT — implementation NOT VERIFIED; endpoint NOT ESTABLISHED; production use NOT AUTHORIZED**
- Owner: D Domain Owner
- D Owner Decision ID: `D-OWNER-2026-11-19-007`
- Scope: AID-2026-010 / Issue #43 / F-43-01 / F3
- H mapping input: `08-bmcp-protocol/phase-3.8.35-h-owner-decision-f43-01-f3-d-1.3.1-mapping.md`, exact Blob `004fc0261b447771e73a0f8cfdd34ec1f8b33e49`
- D contract baseline: 1.3.1, Blob `12b71e770f4e977c7f147694a644066bc2ce11b9`
- D-002 proof baseline: Blob `4c8672a68e4339e40b5d8cb98eb073af8c98c1a5`
- Preceding D decision: `D-OWNER-2026-11-19-006` (ACCEPT WITH EXPLICIT LIMITATIONS)
- This document defines a normative interface contract. It does not claim an endpoint, transport, schema artifact, signing key, receipt instance, ledger proof, test, or Runtime implementation exists.

## 1. Purpose, authority and conformance boundary

This contract defines the authoritative read-only query dependency named `ResolveForgetFenceSnapshotProof`. It resolves one already-installed ForgetOperation and returns authenticated evidence for its immutable D BarrierSnapshotReceipt, D-002 conditions C1–C6, and independently evaluated currentness/revocation state.

The interface MUST NOT install, move, reset, replace, advance, or recapture a fence cutoff. It MUST NOT turn a query into a new admission operation. A timeout or missing response is UNKNOWN/BLOCKED, never proof of commit or abort.

Only the D ForgetFence authority, D ProducerWork Registration Ledger authority, and the D-owned ledgers named below may issue authoritative evidence. H caches, local replicas without a proved currentness chain, TEST callbacks, fixtures, static JSON, and caller-supplied claims are not D authority.

This is a normative design contract. Until an implementation repository, authoritative storage, trust root, endpoint/transport, and operational key registry are designated and independently verified, every operation described here remains **SPECIFIED / NOT ESTABLISHED AS CALLABLE**.

## 2. Nominal type and namespace registry

Every field below is a distinct nominal type. JSON strings are transport encodings only. A verifier MUST first bind the exact field name and contract version to its nominal type and authority; it MUST NOT infer type from a JSON primitive, numeric magnitude, similar name, or common serialization.

### 2.1 Eight D Owner Snapshot fields

| H field | D nominal type | Authoritative source | Required namespace / identity | Immutable receipt binding |
|---|---|---|---|---|
| `producer_registration_high_water` | `ProducerRegistrationHighWater` (sequence of `ProducerRegistrationSequence`) | D ProducerWork Registration Ledger authority | Exact `BrainAuthorityId` + `ProducerRegistrationLedgerId` + `ProducerRegistryVersion` | Exact `BarrierSnapshotReceiptRef` + digest; same value as Install receipt `captured_producer_registration_high_water` under C4 |
| `forget_fence_generation_high_water` | `ForgetFenceGeneration` | D ForgetFence authority/generation ledger | Exact `BrainAuthorityId` + `ForgetFenceNamespaceId` | Same immutable receipt's `ForgetFenceCursor` generation and fence-state version |
| `work_item_high_water` | `ProducerWorkItemHighWater` | D ProducerWork Item Ledger authority | Exact `BrainAuthorityId` + `ProducerWorkItemLedgerId` | Receipt's typed `DFieldBinding` entry for field name, ledger identity, value, and snapshot digest |
| `attempt_high_water` | `ProducerWorkAttemptHighWater` | D ProducerWork Attempt Ledger authority | Exact `BrainAuthorityId` + `ProducerWorkAttemptLedgerId` | Receipt's typed `DFieldBinding` entry for field name, ledger identity, value, and snapshot digest |
| `barrier_generation` | `BarrierGeneration` | D Forget Barrier Generation Ledger authority | Exact `BrainAuthorityId` + `ForgetBarrierLedgerId` | Receipt's typed `DFieldBinding` entry, bound to the same barrier snapshot identity |
| `barrier_root` | `BarrierRootDigest` (SHA-256 digest) | D Forget Barrier Reconciliation Ledger authority | Exact `BrainAuthorityId` + `ForgetBarrierLedgerId` + barrier snapshot identity | Receipt carries exact root and the corresponding signed ledger checkpoint/proof reference |
| `dependency_closure_cursor` | `DependencyClosureCursor` (opaque, non-arithmetic cursor) | D Dependency Inventory authority | Exact `BrainAuthorityId` + `DependencyInventoryLedgerId` + source-lineage identity | Receipt's typed `DFieldBinding` entry binds cursor bytes and inventory checkpoint to receipt digest |
| `dependency_closure_root` | `DependencyClosureRootDigest` (SHA-256 digest) | D Dependency Inventory authority | Same dependency inventory namespace and lineage as closure cursor | Receipt carries root and its consistency/inclusion proof, bound to the exact closure cursor and receipt digest |

The ledger IDs above are stable, opaque nominal identities. They MUST be assigned by D authority and persisted in the receipt. They are not inferred from a path, service name, H owner, tenant label, or caller input. Where a deployment has not assigned an identity, the field is unavailable and the proof is UNKNOWN/BLOCKED; a verifier MUST NOT invent one.

For the six fields beyond the two D-002 critical high-waters, this contract introduces the nominal types and binding requirements. It does not assert that a corresponding ledger or persisted field binding currently exists.

### 2.2 Decimal encoding and range

The following nominal types are high-waters/generations and MUST each be validated independently:

- `ProducerRegistrationHighWater`
- `ForgetFenceGeneration`
- `ProducerWorkItemHighWater`
- `ProducerWorkAttemptHighWater`
- `BarrierGeneration`

For each type, the mathematical domain is the integer range `0..2^63-1`. The wire representation is a JSON string containing ASCII decimal digits only.

- Canonical output grammar: `0` or `[1-9][0-9]*`.
- Input parsing MUST accept leading zeroes as required by D contract 1.3.1 §5.1. Leading zeroes MUST be canonicalized within that one nominal type before the value is emitted in a signed response or included in a digest projection.
- Negative sign, plus sign, whitespace, separators, exponent, fraction, Unicode digits, empty string, and values greater than `2^63-1` are invalid.
- The type tag and namespace identity are mandatory alongside the decimal string in the receipt binding. A bare decimal string is never a typed value.
- No conversion to a shared integer domain for cross-field comparison is permitted. No cross-type equality, ordering, subtraction, range comparison, aliasing, or derivation is permitted.
- The only D-002 high-water equality is between Install receipt `captured_producer_registration_high_water` and BarrierSnapshotReceipt `producer_registration_high_water`, both typed `ProducerRegistrationHighWater`, for the same operation/fence/snapshot identity.

The three digest/cursor fields are not high-waters: `barrier_root` and `dependency_closure_root` are lowercase 64-hex SHA-256 digests; `dependency_closure_cursor` is an opaque, byte-preserved cursor. They MUST NOT be parsed as decimal values.

### 2.3 Required receipt field-binding record

The immutable `BarrierSnapshotReceipt` MUST bind every one of the eight fields through a closed-world ordered `d_field_bindings` collection. Each entry contains:

- `field_name` — exact H field spelling;
- `nominal_type_id` — exact D nominal type identifier;
- `authority_id` — stable D authority identity;
- `namespace_id` — exact ledger/namespace identity;
- `lineage_id` — source lineage where applicable;
- `canonical_value` — canonical decimal string, digest, or opaque cursor encoding as defined by that type;
- `source_checkpoint_ref` and `source_checkpoint_digest`;
- `snapshot_receipt_digest` — exact digest of the enclosing BarrierSnapshotReceipt;
- `binding_version` — this contract version or a later explicitly compatible version.

The set MUST contain exactly the eight required field names once each. Duplicate, missing, unknown, wrong-type, wrong-authority, wrong-namespace, wrong-lineage, or wrong-snapshot entries fail closed. The enclosing receipt digest is calculated over the canonical projection in §6; self-reference is avoided by computing the receipt content digest over the receipt body with its digest/signature envelope fields excluded, then signing the envelope that names that body digest.

## 3. Authoritative identity and H snapshot binding

### 3.1 D authoritative identity tuple

The authoritative D snapshot identity is the following typed tuple, not a concatenated scalar:

```
DAuthoritativeSnapshotIdentity {
  brain_authority_id: BrainAuthorityId,
  producer_registration_ledger_id: ProducerRegistrationLedgerId,
  producer_registry_version: ProducerRegistryVersion,
  forget_operation_id: ForgetOperationId,
  idempotency_identity: ForgetIdempotencyIdentity,
  canonical_request_digest: CanonicalRequestDigest,
  target_set_digest: TargetSetDigest,
  forget_fence_cursor: ForgetFenceCursor {
    forget_operation_id: ForgetOperationId,
    forget_fence_generation: ForgetFenceGeneration,
    target_set_digest: TargetSetDigest
  },
  installation_canonical_commit_cursor: CanonicalCommitCursor,
  barrier_snapshot_receipt_ref: BarrierSnapshotReceiptRef,
  barrier_snapshot_receipt_digest: SHA256Digest,
  producer_registration_high_water: ProducerRegistrationHighWater,
  fence_state_version: FenceStateVersion,
  d_snapshot_identity: DSnapshotIdentity
}
```

All tuple members are nominally typed. The tuple MUST be identical across Install receipt, BarrierSnapshotReceipt, authenticated query response and consistency proof context. The receipt reference is an immutable locator; its digest is the content identity. Neither alone replaces the tuple.

### 3.2 H-to-D binding claim

The H identity tuple is:

```
HOwnerSnapshotIdentity {
  owner_snapshot_ref: OwnerSnapshotRef,
  owner_snapshot_digest: SHA256Digest,
  owner_snapshot_attestation_ref: OwnerSnapshotAttestationRef,
  owner_snapshot_attestation_digest: SHA256Digest
}
```

The D response MUST include an authenticated `OwnerSnapshotBindingClaim` containing the complete H tuple, the complete D authoritative identity tuple, the exact D receipt ref+digest, the H schema/mapping revision and Blob digest, and the binding result. The claim asserts that the named H owner snapshot and attestation were constructed from and attest to this exact D BarrierSnapshotReceipt—not merely that the references coexist.

The binding claim MUST be included in the signed canonical response projection. H MUST verify both H attestation validity and D signature validity, then compare every identity member byte-for-byte/nominally. A missing H reference, missing digest, mismatch, unresolvable reference, or a claim not signed by D authority yields UNKNOWN/BLOCKED or INVALID for an explicit contradiction. H MUST NOT substitute a different receipt with numerically equal fields.

## 4. ResolveForgetFenceSnapshotProof request

The request is read-only and MUST be authenticated by an authorized H consumer identity. The conceptual schema is:

```
ResolveForgetFenceSnapshotProofRequest {
  interface_version: "1.0",
  d_contract_revision: "1.3.1",
  d_contract_blob_sha256: "12b71e770f4e977c7f147694a644066bc2ce11b9",
  d_query_contract_revision: "1.0",
  d_query_contract_blob_sha256: <exact published Blob SHA>,
  h_mapping_blob_sha256: "004fc0261b447771e73a0f8cfdd34ec1f8b33e49",
  request_id: RequestId,
  request_nonce: Nonce256,
  requester_identity: HConsumerIdentity,
  brain_authority_id: BrainAuthorityId,
  producer_registration_ledger_id: ProducerRegistrationLedgerId,
  forget_operation_id: ForgetOperationId,
  idempotency_identity: ForgetIdempotencyIdentity,
  canonical_request_digest: CanonicalRequestDigest,
  target_set_digest: TargetSetDigest,
  expected_fence_cursor?: ForgetFenceCursor,
  expected_installation_canonical_commit_cursor?: CanonicalCommitCursor,
  expected_snapshot_ref?: BarrierSnapshotReceiptRef,
  expected_snapshot_digest?: SHA256Digest,
  expected_producer_registry_version?: ProducerRegistryVersion,
  owner_snapshot_identity?: HOwnerSnapshotIdentity,
  consistency_requirement: "D_AUTHORITATIVE_LINEARIZABLE",
  include_currentness_and_revocation: true
}
```

The request authentication envelope MUST bind the exact canonical request bytes, requester identity, request ID, nonce, interface/contract revisions and mapping Blob SHA. Expected fields are comparison anchors only; they MUST NOT instruct D to create or recapture state. Retries use a new request ID/nonce but the same ForgetOperationId, idempotency identity and original digests. A retry MUST resolve the original durable receipt.

## 5. Response evidence model

### 5.1 Response envelope and request correlation

The response MUST include:

- exact `request_id`, `request_nonce`, and `request_digest` from the authenticated request;
- `response_id`, `interface_version`, D contract revision+Blob digest, query-contract revision+Blob digest, H mapping Blob digest;
- D authority identity and signing key ID;
- complete D authoritative identity tuple from §3.1;
- immutable BarrierSnapshotReceipt ref, content digest and receipt body;
- H-to-D OwnerSnapshotBindingClaim when H identity was supplied;
- all eight typed field bindings from §2.3;
- six condition evidence records from §5.2;
- currentness and revocation evidence from §5.3;
- authoritative snapshot identity and observed authority commit cursor from §5.4;
- proof classification from §5.5;
- canonicalization profile identifier and response body digest;
- signature envelope from §6.

The request ID/nonce/digest MUST match the request exactly. A mismatch, missing nonce, wrong mapping digest, incompatible contract revision, duplicate response ID under a different body, or invalid signature fails closed. A response to another request MUST never be replayed as this request's answer.

### 5.2 C1–C6 evidence records

Each condition record has this common shape:

```
ConditionEvidence {
  condition_id: "C1" | "C2" | "C3" | "C4" | "C5" | "C6",
  result: "PROVEN" | "MISMATCH" | "UNAVAILABLE",
  evidence_kind: EvidenceKind,
  authority_id: DAuthorityId,
  source_ledger_id: DLedgerId,
  source_checkpoint_ref: CheckpointRef,
  source_checkpoint_digest: SHA256Digest,
  covered_range: EvidenceCoverage,
  operation_identity_digest: SHA256Digest,
  barrier_snapshot_receipt_digest: SHA256Digest,
  evidence_payload_ref: EvidencePayloadRef,
  evidence_payload_digest: SHA256Digest
}
```

The payload MUST be resolvable and independently verifiable. A status enum, ref, digest, count, or root without its defined payload and proof is insufficient.

**C1 — Authority/ledger/registry identity.** Payload contains BrainAuthorityId, ProducerRegistrationLedgerId, namespace identity, ProducerRegistryVersion, authority-issued registry checkpoint and proof of exact equality across Install receipt and BarrierSnapshotReceipt. Coverage is the exact registry version and ledger identity for this operation. Source: D Producer Registration Ledger authority plus D ForgetFence install authority.

**C2 — Operation/idempotency identity.** Payload contains ForgetOperationId, idempotency identity, canonical request digest, exact target-set digest, durable idempotency record ref/digest, and replay disposition. Coverage is the one operation identity and its durable outcome. Source: D ForgetOperation/idempotency authority.

**C3 — Fence/cursor identity.** Payload contains the complete ForgetFenceCursor tuple, ForgetFenceGeneration, installation CanonicalCommitCursor, FenceStateVersion and durable install receipt ref/digest. Coverage is the fence installation event and the exact operation. Source: D ForgetFence authority and commit ledger.

**C4 — Same-typed cutoff equality.** Payload contains both original receipt values and type tags, namespace/ledger identity and snapshot digest: Install `captured_producer_registration_high_water` and Capture `producer_registration_high_water`. Both MUST be `ProducerRegistrationHighWater` and exact equal after independent canonicalization. Coverage is the same operation/fence/receipt. Source: D Install receipt and D BarrierSnapshotReceipt. Any inequality is MISMATCH; missing binding is UNAVAILABLE.

**C5 — Immutable receipt and ledger consistency.** Payload contains complete BarrierSnapshotReceipt, receipt body digest, all eight field bindings, checkpoint refs/digests and a verifiable ledger consistency proof under §7. Coverage includes the exact ledger checkpoint intervals and snapshot boundary. Source: D snapshot authority and each named D ledger authority. A pointer or root alone is insufficient.

**C6 — Linearized registration ordering and disposition.** Payload contains the D serialization-order proof; linearization event identity/cursor for InstallForgetFence; registration event range; pre-fence accepted registration inclusion proof; post-fence ordinary registration rejection/quarantine/cleanup-only disposition records; publication eligibility decisions; and inventory/disposition roots with inclusion proofs. Coverage MUST span every registration and covered publication/admission event in the affected authority/lineage through the receipt's declared checkpoint. It MUST demonstrate no admitted-but-unaccounted publishable work. Source: the same D-authoritative ordering domain used by RegisterProducerWork and InstallForgetFence, plus D registration and publication/admission ledgers. Counts and aggregate roots without per-range completeness/consistency proofs are insufficient.

Every condition evidence record MUST carry the exact same `barrier_snapshot_receipt_digest` and operation identity digest. Cross-receipt mixing is invalid. Any UNAVAILABLE condition makes the aggregate at most UNKNOWN/BLOCKED; any explicit contradiction makes it INVALID, subject to the stale classification rule below.

### 5.3 Currentness and revocation evidence

Currentness is independent of C1–C6 and MUST be read from one authoritative D state snapshot. The response contains:

```
CurrentnessEvidence {
  authority_id: DAuthorityId,
  fence_state_version: FenceStateVersion,
  queried_snapshot_identity: DSnapshotIdentity,
  authoritative_current_snapshot_identity: DSnapshotIdentity,
  currentness_result: "CURRENT" | "STALE" | "UNKNOWN",
  state_checkpoint_ref: CheckpointRef,
  state_checkpoint_digest: SHA256Digest,
  state_consistency_proof_ref: ProofRef,
  state_consistency_proof_digest: SHA256Digest,
  revocation_result: "NOT_REVOKED" | "REVOKED" | "UNKNOWN",
  revocation_record_ref?: RevocationRecordRef,
  revocation_record_digest?: SHA256Digest,
  revocation_checkpoint_ref: CheckpointRef,
  revocation_checkpoint_digest: SHA256Digest,
  revocation_consistency_proof_ref: ProofRef,
  revocation_consistency_proof_digest: SHA256Digest
}
```

The state and revocation checkpoint records MUST be D-authority authenticated and included in the signed response projection. If revoked, the response MUST include the exact revocation record and reason code; if not revoked, it MUST prove absence through the declared revocation checkpoint and coverage boundary. Absence from a cache or one replica is not proof of non-revocation.

No TTL, local wall clock, cache age, or H-side state can establish currentness. A proven newer authoritative state version yields STALE. Explicit revocation yields INVALID. Unavailable state or revocation proof yields UNKNOWN/BLOCKED.

### 5.4 Joint binding of authoritative identity and observed cursor

`authoritative_snapshot_identity` MUST equal the complete D identity tuple in §3.1. `observed_at_authority_commit_cursor` MUST identify the exact D authority commit/checkpoint at which the query's linearizable read was evaluated.

Both MUST appear in the same signed response projection and be bound to:
1. the request ID/nonce/digest;
2. the BarrierSnapshotReceipt ref+digest;
3. the C1–C6 evidence digest set;
4. currentness and revocation checkpoint refs+digests;
5. the D signing identity/key ID.

The observed cursor MUST be at or after the receipt's installation commit cursor within the same CanonicalCommitCursor domain. This is a same-type, same-authority ordering check only. It MUST NOT be compared to any high-water or generation. If the authority cannot prove the read was linearizable at that cursor, the response is UNKNOWN/BLOCKED.

### 5.5 Machine-verifiable aggregate classification

The verifier MUST apply this truth table in order:

1. Invalid response authentication, request correlation, canonical encoding, contract revision, receipt digest, identity tuple, or explicit C1–C6 mismatch → **INVALID**.
2. Explicit revocation → **INVALID**, regardless of C1–C6.
3. Proven authoritative state-version supersession/currentness mismatch → **STALE**, unless explicit revocation already requires INVALID.
4. Any C1–C6 UNAVAILABLE, missing proof payload, missing checkpoint, unavailable currentness/revocation evidence, unproven linearizable read, or incomplete coverage → **UNKNOWN**; H operational disposition is **BLOCKED**.
5. **VALID** only if all C1–C6 are PROVEN for the same receipt digest and identity tuple, signature/request correlation pass, currentness is CURRENT, revocation is NOT_REVOKED, and all proof payloads/checkpoints verify.
6. No partial condition set, schema-only validation, matching watermarks, cached VALID, or successful transport response can yield VALID.

The response MUST carry both `proof_status` and the individual condition/currentness/revocation records. The verifier recomputes the aggregate; it MUST NOT trust a server-provided VALID label without independently applying this rule.

## 6. D response authentication and signing-key lifecycle

### 6.1 Trust root and signing identity

The D authority MUST publish a versioned trust-root manifest through an independently authenticated D governance channel. The manifest binds:
- `d_authority_id` and authority scope;
- `signing_identity_id` and `key_id`;
- algorithm identifier and protocol version;
- public key bytes and fingerprint;
- activation checkpoint/cursor;
- key status and revocation metadata;
- manifest revision, digest and governance signature.

For interface 1.0, the mandatory response signature algorithm is **Ed25519 (RFC 8032)** and the response body digest is **SHA-256**. Algorithm agility requires a new explicit allowlisted algorithm/version entry; unknown or downgraded algorithms fail closed. Private signing keys MUST be held by the D authority's protected signing boundary and MUST NOT be exposed to H or callers.

A signature proves possession of a key, not that the key is authorized. The verifier MUST validate the trust chain, authority scope, key status at signing checkpoint, and current revocation state.

### 6.2 Canonical response projection

The signed projection is `D-ResolveForgetFenceSnapshotProof-Response-v1`. It is canonical JSON under RFC 8785 JCS, UTF-8 encoded, with:
- duplicate object keys rejected before canonicalization;
- all high-waters represented as canonical decimal JSON strings plus explicit nominal type/namespace bindings;
- digests represented as lowercase 64-character SHA-256 hex strings;
- opaque refs/cursors preserved byte-for-byte according to their type encoding;
- no floating-point values;
- no omitted-vs-null ambiguity: each schema field defines required, optional, or explicit-null behavior;
- arrays ordered by the contract-defined stable key (condition IDs C1..C6; field bindings by the eight-field order in §2.1; checkpoint/proof arrays by ledger identity then checkpoint cursor).

The signature input is the UTF-8 bytes of the canonical projection with only `signature` and transport-only fields excluded. The response envelope carries the projection digest, algorithm, key ID, signing identity, signature bytes and trust-root manifest digest. The signed projection includes request correlation, exact contract/mapping Blob digests, D identity tuple, receipt digest, eight field bindings, C1–C6 evidence digests, currentness/revocation evidence digests, authoritative snapshot identity and observed authority commit cursor.

Any semantic field not covered by the projection MUST NOT affect proof status. Any field affecting proof status MUST be covered. Canonicalization mismatch or an unrecognized projection version fails closed.

### 6.3 Key lifecycle

- **Activation:** a key is valid only at/after its authority-signed activation checkpoint. A key cannot sign a response claiming an earlier activation.
- **Rotation:** publish the next key and signed trust manifest before activation; old and new keys may overlap for a bounded, explicitly declared checkpoint interval. Each response names exactly one key. Rotation MUST NOT change historical receipt bytes or identity.
- **Overlap:** during overlap, both keys may validate only within their declared authority scope and checkpoint interval. The verifier selects validity by signed authority checkpoint, not local clock.
- **Retirement:** retired keys cannot sign new responses after the retirement checkpoint. Historical signatures remain verifiable only if the key was valid at the signed checkpoint and no compromise/revocation rule invalidates them.
- **Compromise:** publish an authenticated compromise record with affected key ID and effective authority checkpoint/range. Responses in the affected range are INVALID unless a separately governed recovery proof establishes integrity.
- **Revocation:** publish a signed revocation record and include its checkpoint proof in currentness/revocation evidence. Revoked keys cannot authenticate new responses. Whether historical signatures survive revocation is determined by the compromise effective range; unknown range yields UNKNOWN/BLOCKED.
- **Manifest rollback:** trust-root manifest sequence/checkpoint regression is rejected. If continuity/anti-rollback cannot be proven, authentication is UNKNOWN/BLOCKED.
- **Emergency root rotation:** requires a separately authenticated governance transition binding old root, new root, effective checkpoint and continuity proof. An unanchored new root is not trusted.

No signing key, key registry, trust-root manifest, rotation record, or production signature is asserted to exist today.

## 7. Versioned ledger consistency proof format

### 7.1 Format identifier and digest rules

The required proof format is `D-Ledger-Consistency-Proof-v1`. Hash function: SHA-256. Merkle tree construction follows the RFC 6962 domain-separated shape:
- leaf hash: `SHA256(0x00 || canonical_leaf_bytes)`;
- node hash: `SHA256(0x01 || left_hash || right_hash)`;
- empty tree root: `SHA256(empty_bytes)`.

All leaves are canonical JCS records. A proof MUST identify the exact ledger authority, ledger namespace, source lineage, checkpoint sequence, checkpoint cursor, leaf-index range, tree size, root digest, and receipt binding. A root without inclusion/consistency paths is insufficient.

### 7.2 Proof object

```
LedgerConsistencyProofV1 {
  proof_format: "D-Ledger-Consistency-Proof-v1",
  hash_algorithm: "SHA-256",
  tree_algorithm: "RFC6962-MERKLE-SHAPE-v1",
  authority_id: DAuthorityId,
  ledger_id: DLedgerId,
  namespace_id: DNamespaceId,
  lineage_id: SourceLineageId,
  checkpoint_id: CheckpointId,
  checkpoint_cursor: CanonicalCommitCursor,
  tree_size: uint64,
  root_digest: SHA256Digest,
  previous_checkpoint_digest: SHA256Digest,
  covered_from_cursor: CanonicalCommitCursor,
  covered_through_cursor: CanonicalCommitCursor,
  receipt_ref: BarrierSnapshotReceiptRef,
  receipt_digest: SHA256Digest,
  inclusion_proofs: [MerkleInclusionProof],
  consistency_proof: MerkleConsistencyPath,
  checkpoint_signature_ref: SignedCheckpointRef,
  checkpoint_signature_digest: SHA256Digest
}
```

The checkpoint signature MUST be authenticated under §6 and bind every field in the checkpoint header, including previous checkpoint digest, tree size/root, cursor range, ledger/namespace/lineage identity and receipt ref+digest. A verifier checks inclusion paths for all claimed records and the append-only consistency path between the prior trusted checkpoint and this checkpoint. It also verifies monotonic checkpoint sequence/cursor in the same ledger cursor domain.

### 7.3 C5 and C6 coverage

For C5, the proof covers all receipt-bound ledger records and proves the receipt's ledger checkpoint is included in the named ledger history. For C6, the proof set additionally includes registration events, fence installation event, ordering/serialization record, inventory membership, disposition records and publication/admission outcomes over the declared coverage interval. The serialization-order proof MUST bind a single linearization point and demonstrate complete event coverage; Merkle inclusion alone does not prove ordering or completeness.

A proof with a gap, fork, unknown prior checkpoint, rollback, missing event range, inconsistent receipt digest, invalid signature, or unresolvable source record is INVALID if contradictory and otherwise UNKNOWN/BLOCKED. Multi-ledger snapshots carry one proof per ledger identity; they are not collapsed into a synthetic shared cursor.

This format is normative and does not assert that any D ledger currently emits it.

## 8. Failure, retry and recovery rules

- Timeout, transport failure, absent authority, unavailable key manifest, or partial response → UNKNOWN/BLOCKED.
- Exact retry resolves the original ForgetOperation and receipt. It never creates a new cutoff.
- Changed request/target digest under the same idempotency identity → IDEMPOTENCY_CONFLICT.
- Receipt ref with wrong digest, identity tuple mismatch, or same-type C4 inequality → INVALID.
- Proven newer fence state version → STALE.
- Explicit fence or key revocation → INVALID.
- Restore without ledger continuity, checkpoint consistency and anti-rollback proof → UNKNOWN/BLOCKED.
- Partial namespace success remains local; aggregate proof remains UNKNOWN/BLOCKED until every required namespace independently verifies.
- Reconciliation appends evidence; it does not mutate the original receipt, cutoff, checkpoint history, or signature.

## 9. Normative requirements versus implementation evidence

| Capability | Normative requirement in this contract | Current evidence status |
|---|---|---|
| Eight typed D field bindings | Required by §§2–3 | Contract-defined here; actual ledger bindings NOT VERIFIED |
| Immutable BarrierSnapshotReceipt binding | Required by §§2–3 | No real D receipt supplied/verified |
| H owner snapshot/attestation binding claim | Required by §3.2 | No live D claim or H↔D verification |
| ResolveForgetFenceSnapshotProof endpoint | Read-only interface defined by §§1, 4–5 | NOT ESTABLISHED AS CALLABLE / NOT DEPLOYED |
| Request authentication/correlation | Required by §§4–5 | No transport/auth implementation verified |
| Ed25519 response signing and trust root | Required by §6 | No production key/manifest/signature verified |
| Key rotation/revocation | Required by §6.3 | NOT IMPLEMENTED / NOT VERIFIED |
| C1–C5 operational proof payloads | Required by §5.2 | No real authority payloads/receipts verified |
| C6 serialization/inclusion/disposition proof | Required by §5.2 and §7.3 | No real D Runtime evidence available |
| Ledger consistency proof v1 | Required by §7 | No emitted proof or verifier execution verified |
| Currentness/revocation proof | Required by §5.3 | No authoritative state read verified |
| Runtime conformance/CI | Must be independently tested | NOT RUN / NOT VERIFIED |

This contract deliberately does not claim that an endpoint, schema file, signing identity, receipt, serialization proof, ledger proof, or test exists. The interface is not production-authorized by this normative definition.

## 10. Decision and finding boundary

**D Owner Decision ID:** `D-OWNER-2026-11-19-007`

**D Owner decision:** ACCEPT the normative definition of `D-AUTH-QUERY-1.0` as the D authoritative query interface contract for F-43-01/F3, subject to exact Blob/commit readback and A Integration review.

This decision:
- supplements D contract 1.3.1; it does not rewrite or silently amend its existing Blob;
- defines the missing nominal field, identity-binding, authentication, evidence, currentness, key-lifecycle and consistency-proof requirements;
- does not assert implementation, deployment, production readiness, or conformance;
- does not close F-43-01/F3 or F-43-01/F1;
- does not authorize H production consumption;
- leaves A Integration responsible for independent verification and Finding Ledger status.

**Implementation gate:** F3 cannot be considered operationally closed solely because this normative document exists. A Integration must verify the exact contract Blob and decide whether the remaining finding criterion is normative contract closure or requires additional implementation evidence under the governing R35 decision.


## 11. 2026-11-20 F3 same-Blob mapping acceptance and attribution recheck

**Finding:** F-43-01/F3 — P1 — OPEN. This addendum separates normative same-Blob mapping acceptance from independent-human identity attribution and operational consumer conformance.

### 11.1 Exact same-Blob decisions
- Accepted H mapping artifact: `08-bmcp-protocol/phase-3.8.35-h-owner-decision-f43-01-f3-d-1.3.1-mapping.md`, Blob `004fc0261b447771e73a0f8cfdd34ec1f8b33e49`.
- H role-labelled disposition: Issue #43 comment [#7021638212](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/43#issuecomment-7021638212), decision `H-OWNER-2026-11-19-003`, ACCEPT WITH EXPLICIT LIMITATIONS, same Blob.
- D role-labelled disposition: Issue #43 comment [#7021655866](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/43#issuecomment-7021655866), decision `D-OWNER-2026-11-19-005`, ACCEPT WITH EXPLICIT LIMITATIONS, same Blob.
- D query contract correction delivered by existing PR #321: Head `7af4e4c409a6522d961b15d9622c92c7551be5f9`, contract Blob `6f2d583dec8487b321795a006266ee4229c7fd80`; the accepted mapping Blob is pinned in the contract, and the superseded mapping Blob `e60bdd4cbfef79850596001f01cb56e622b7d79d` is not the active pin.

### 11.2 Attribution boundary
Both role-labelled decision comments above expose the same GitHub login `oahcom`. The repository evidence therefore verifies two role-labelled, same-Blob decision records, but does **not** authenticate two distinct human signers or establish independent-human acceptance. This document does not infer distinct identity from role labels, comment wording, or a shared account, and does not sign for either Owner.

**Integration disposition:** normative D/H mapping content is mutually recorded as ACCEPT WITH EXPLICIT LIMITATIONS for the exact Blob above; independent-human attribution remains NOT VERIFIED. F3 is not marked DECIDED/CLOSED on that basis.

### 11.3 Consumer implementation and test boundary
- Existing H TEST-profile correction PR #322 Head: `0ce618ac503f641cf31e66092ae823c14bf8af7b`.
- Validator Blob: `49644a181c578fecb312218c08ce23caa62f603b`; regression-test Blob: `e66264ad30df6594e00836524accfdeb54160cee`.
- The patch covers five independent D high-water/generation fields, signed-64-bit bounds, leading-zero canonicalization and digest projection. The recorded focused local report is 13/13 PASS (Python 3.13.5; PR #322 review comment #5988025205); this is not a full repository suite.
- Exact-Head Actions runs `44681841687` and `44681841601` recorded FAILURE; the available job evidence had no executed steps and log retrieval returned HTTP 404 `BlobNotFound`. No CI PASS or test-level failure cause is inferred.
- No callable D query endpoint, real D BarrierSnapshotReceipt, authenticated response, authoritative currentness/revocation read, H production consumer, or end-to-end C1–C6 operational trace is established by these document/TEST-profile artifacts.

### 11.4 Finding and return
- **F-43-01/F3 — P1 — OPEN** — return: PR #321 (D query contract), PR #322 (H TEST-profile validator), Issue #25 (operational D/Storage authority), Issue #43 (cross-owner finding ledger).
- Normative same-Blob D/H role dispositions: recorded with explicit limitations.
- Independent-human attribution: NOT VERIFIED.
- H consumer TEST-profile patch: delivered; exact-Head CI: FAILURE / NOT PASS.
- Callable D query, receipt/currentness and production/end-to-end evidence: NOT ESTABLISHED / NOT RUN.

This is an evidence addendum, not an independent signature, not production acceptance, and not F3 closure. No Owner authority is transferred by this document.
