# AID-2026-083 - C/G Applied evidence format, authority and acceptance
Authority: user-authorized operator (delegated by account owner)
Date: 2026-11-26
Base: main 8dfcfb32e0fa4ce65d705bcef6d8c37375424900
Issues: #1124, #1135, #1180

Define a verifiable logical Applied evidence bundle and exact landing points. G owns the final Applied record/projection. C owns final immutable inference-request boundary facts and Adapter application observation. H owns BMCP envelope, transport/ACK, capability and signature/key evidence. I owns authorization/PermissionEpoch; D owns ForgetFence freshness.

The C-G-APPLIED-EVIDENCE/1.0 bundle binds context_id, exact context_version, context_session_id, delivery_id, delivery_attempt_id, agent/adapter/adapter_instance/runtime_instance/runtime_session, inference_request_id, final_request_boundary_id/type, adapter_capability_epoch, managed_region_id/revision, expected and observed managed_region_digest, managed_region_inventory_digest, digest_profile, coverage=COMPLETE, C FINAL_REQUEST_SUBMITTED and APPLIED_CONTEXT_OBSERVED refs, C outcome record ref/sequence/payload digest, H signed envelope (issuer, audience, message id/nonce, signing sequence namespace/sequence, signature profile, key id/version, payload digest, signature, integrity proof), current D ForgetFenceCursor and I authorization decision/PermissionEpoch.

Digest profile is SHA-256 over a versioned canonical managed-region serialization; expected and observed digest must be identical; inventory digest binds exact ordered entry/revision inventory. Tier 1 requires COMPLETE coverage. Existing H schema bmcp.applied-delivery-evidence-1.0.0 is a mapping reference only; no schema/wire freeze is claimed.

Landing: C immutable final-boundary evidence in its C outcome record; H signed protocol envelope in its immutable evidence archive; G durable Applied Ledger stores an append-only AppliedRecord and opaque refs/digests to both C/H artifacts, keyed by full delivery attempt/request identity. Storage may provide physical durability but is not evidence issuer or Applied authority. Physical URI/backend remains H/G-owned and OPEN; do not invent one.

Projection: G adds no Accepted lifecycle state. G stores authoritative C/H Accepted evidence ref as attempt metadata bound to stable DeliveryId+AttemptId. Accepted is not Applied. Local Stored/Materialized/Received or file write is not Applied. G commits Applied only after exact identity match, both C evidence kinds, valid H integrity, complete coverage and equal digests, current I authorization and D fence, and no supersession/revocation before final request boundary. Unknown ordering stays Unknown/pending.

PASS/FAIL:
- CG-A1 PASS iff every identity field is bound to the same DeliveryId+AttemptId+InferenceRequest+Boundary; otherwise FAIL.
- CG-A2 PASS iff both C FINAL_REQUEST_SUBMITTED and APPLIED_CONTEXT_OBSERVED artifacts exist and causally bind the same exact request; otherwise FAIL.
- CG-A3 PASS iff coverage is COMPLETE and expected/observed SHA-256 managed-region digests and inventory commitments match; otherwise FAIL.
- CG-A4 PASS iff H verifies issuer/audience/message/nonce/sequence/key-version/signature/payload integrity; otherwise FAIL.
- CG-A5 PASS iff G stores an immutable append-only AppliedRecord referencing exact C/H artifacts and is idempotent for same attempt+digest; otherwise FAIL.
- CG-A6 PASS iff current I PermissionEpoch and D ForgetFence are checked at the final boundary and ambiguous ordering stays Unknown; otherwise FAIL.
- CG-A7 PASS iff G creates no Accepted state and stores C/H Accepted evidence ref on the stable attempt; otherwise FAIL.
- CG-A8 PASS iff local persistence/materialization alone cannot produce G Applied and no claim of model comprehension is made; otherwise FAIL.

Modify only G/C architecture documents and EN/ZH-CN mirrors, this Work Item directory and INDEX.md. Do not modify Runtime/product code, tests, H schema/wire, validators, deployment or production. Create independent branch and Draft PR; do not merge. Keep #1124, #1135, #1180 OPEN. G/C/H/I/D retain their own exact-version acceptance authority.