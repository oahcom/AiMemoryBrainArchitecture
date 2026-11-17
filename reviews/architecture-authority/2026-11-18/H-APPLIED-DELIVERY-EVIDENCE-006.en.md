# A Exact Review — H Applied Delivery Evidence 1.0.0
# Session 4 / Review A-H-ADE-006

- Review baseline: H `6608cde89d959257db612d8ff8080f631333f3f3`; G `763b3d31e910db8fd29c6e4dbaff9273b7fb66b8`; C `88992da30331121b81cf2773acab11d921daf281`; I `0d071bf1ee7cc71912398c6ae57e4496e08f44ab`; Main `e52594f181d2edb77448adcfed64a0fbdffaf3aa`.
- Status: **DEFERRED — CANDIDATE IMPLEMENTATION WITH OPEN P0 CONDITIONS**
- Scope: exact source review of H Applied Delivery Evidence 1.0.0 candidate and its G/C/I consumer/security boundaries.
- Independence: delegated A review in the coordinating session; not independent human Owner approval.

## 1. Executive decision

H has added a distinct `APPLIED_DELIVERY_EVIDENCE_RECORDED` message family 1.0.0 without widening Unified 1.2.15's C Provider Outcome Gateway P0. The live H tree contains the schema, reference validator, 11-test suite, workflow and bilingual Phase 3.8.24 decision. The schema explicitly carries all seven HDeliveryBindingIdentity members and a separate HObservationRecordIdentity.

The bounded CI evidence is real:
- H Applied Delivery Evidence run `44130722532`: SUCCESS, 11 tests, exact tested commit `4e65a2ee0c6ac1c52a36f5d830ec7685dc4967e6`.
- H Recovery Cutoff run `44130722851`: SUCCESS on the same commit.
- Current H HEAD `6608cde...` is one documentation-only commit after that tested commit. The schema, validator, tests and workflow did not change in that final commit. This is code-tree continuity, not a run attached literally to current HEAD.

These facts justify **candidate/conformance progress only**. They do not establish production cryptography, a deployed trust registry, durable replay, runtime Adapter integration, C/G/I acceptance, crash/restore safety or Full Applied authorization.

**A disposition: DEFERRED.** Keep H-ADE-001..003 OPEN. No schema freeze, technology freeze, Gate release, merge, deployment or production activation.

## 2. Exact artifacts reviewed

| Artifact | Exact Blob |
|---|---|
| H schema `08-bmcp-protocol/schemas/bmcp.applied-delivery-evidence-1.0.0.schema.json` | `2ce8776ca5ee5e014b234dc3eb34a7cb7961e608` |
| H validator `08-bmcp-protocol/validators/applied_delivery_evidence_validator.py` | `2f6de24eea737cf75a16ead7495bea4627bb1bb4` |
| H tests `08-bmcp-protocol/tests/conformance/applied_delivery_evidence/test_applied_delivery_evidence.py` | `bb2bb6c94cc73293f736c6dcd450ab32bffc6ee5` |
| H workflow `.github/workflows/h-applied-delivery-evidence-conformance.yml` | `7bd9bf3a4141d1e239d0f165e2e98fdd25961254` |
| H Phase 3.8.24 EN | `f193113f142506b0d0848c7131f780db93a83aef` |
| H Phase 3.8.24 ZH | `2c612ff11f9e3da784eeb5a9033aceb5bf01b55f` |
| G Phase 3.8.22 Applied contract | `bd297873bc1e593280484a43cb44b56058d9c4ff` |
| CSubmitOutcome 1.0.1 schema | `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda` |
| C Phase 3.8.27 gateway order review | `3ca06dbfd7d59483e9604b7a68df924c719f60aa` |
| I Phase 3.8.23 replay order review | `85cdbad04ae4b688338cdf2b667c21d2f02d8b96` |

## 3. Accepted boundaries and evidence ceiling

1. `HDeliveryBindingIdentity` = (adapter_instance_ref, runtime_session_ref, delivery_id, delivery_attempt_id, inference_request_id, final_request_boundary_id, adapter_capability_epoch).
2. `HEvidenceIdentity` = (HDeliveryBindingIdentity, evidence_kind).
3. `HObservationRecordIdentity` = (issuer_ref, sender_authority_ref, sender_subject_ref, message_id, message_nonce, signing_sequence_namespace_ref, signing_record_sequence).
4. These are three different identity domains. The H Gateway ingress replay ledger, H Adapter observation ledger and G Applied idempotency ledger must remain distinct.
5. H's separate 1.0.0 family correctly avoids mutating Unified 1.2.15's C Provider Outcome P0 allowlist.
6. H Phase 3.8.23 accepts G identity semantics with enumerated exceptions and explicitly states wire mapping was not frozen. C Phase 3.8.23 reviews C/G identity joins, not the new H 1.0.0 family. C Phase 3.8.27 and I Phase 3.8.23 accept the corrected C-before-H-signing order for the separate gateway-attestation path; neither constitutes exact approval of the new Adapter evidence family.
7. I's `AIMBA-I-CRYPTO-1.0` is an I-authored profile and must not be inherited by H. H profile registration and H trust/key authority remain open.

## 4. Blocking Condition Records

### H-ADE-001 — Strict JSON parser does not reject duplicate object keys

- **Issue:** H validator invokes `json.loads(raw_envelope.decode("utf-8"))` directly. The standard decoder silently collapses duplicate object keys before JSON Schema validation and P0 construction.
- **Evidence:** Validator Blob `2f6de24...`; current 11 tests do not include duplicate-key negative vectors.
- **Risk:** HIGH — signed-message ambiguity and parser differential.
- **Blocking:** YES for authenticated production use.
- **Allowed while open:** bounded candidate tests and shadow-only evaluation.
- **Forbidden while open:** production acceptance of this message family; claiming strict signed-byte parsing.
- **Owner:** H.
- **Close criteria:** reject duplicate keys before object materialization; add tests for duplicate top-level and nested members, including identity, digest, signature and authority fields; rerun exact-current-HEAD CI; publish parser/test Blob pins and result.
- **Deadline/Gate:** before H wire-conformance Gate can pass; blocks production trust/activation.
- **Verification evidence:** exact parser source, negative vectors, exact-head workflow run and independent source readback.

### H-ADE-002 — CSubmitOutcome semantic join is not explicit

- **Issue:** H schema carries C outcome references, record sequence and payload digest, but no explicit outcome value. The reference validator exposes `verify_c_final_boundary`; it does not define a separate CSubmitOutcome resolver/verifier contract. C schema 1.0.1 contains authoritative `Outcome`, `SideEffectStatus`, `FinalRequestBoundaryRef`, `RequestDigest`, `ActualInferenceRequestId` and immutable record identity. G requires determinate successful provider handoff evidence before Full Applied.
- **Evidence:** H schema Blob `2ce8776...`; H validator Blob `2f6de24...`; C schema Blob `a631bc7...`; G contract Blob `bd29787...`.
- **Risk:** HIGH — an H evidence record could be treated as Applied-ready without proving that the referenced immutable C record is the exact `HANDOFF_ACCEPTED` / `PROVEN_OCCURRED` outcome for the same final request.
- **Blocking:** YES for Full Applied and cross-owner wire freeze.
- **Allowed while open:** H may carry opaque C refs/digests as candidate evidence; C remains sole provider-truth authority.
- **Forbidden while open:** H minting or asserting C provider truth; G Full Applied based only on H evidence.
- **Owners:** H (wire/validator), C (semantic authority), G (consumer predicate).
- **Close criteria:** exact CSubmitOutcome 1.0.1 field-to-H mapping; tri-state resolver/verifier for issuer, immutable record identity/sequence, digest, outcome and side-effect status, final boundary/request digest/inference request equality and successor lineage; explicit C/G review; positive and negative mutation vectors.
- **Deadline/Gate:** before C/H/G Applied contract Gate or Full Applied enablement.
- **Verification evidence:** version-pinned mapping, callback contract, tests and C/G exact decisions.

### H-ADE-003 — Current authorization recheck before replay result disclosure is underspecified

- **Issue:** I Phase 3.8.23 requires SAME_DIGEST_REPLAY to re-read the original durable result and recheck current I authorization/PermissionEpoch, key status, audience/scope and applicable D Forget fence. H validator has no explicit current-authorization/PermissionEpoch callback before returning `original_result_ref`; `commit_observation` is an injected seam whose contract does not state this requirement.
- **Evidence:** I Phase 3.8.23 Blob `85cdbad...`; H validator Blob `2f6de24...`.
- **Risk:** HIGH — stale or revoked callers may learn a prior durable result reference.
- **Blocking:** YES for replay acceptance and production trust.
- **Allowed while open:** local replay callback tests that do not expose production result refs.
- **Forbidden while open:** returning a durable prior-result reference without a current authorization check.
- **Owners:** H and I; G/D for applicable consumer/fence ordering.
- **Close criteria:** define and implement current authorization/audience/scope/PermissionEpoch recheck before any replay result ref is returned; define D fence re-evaluation at the correct G decision boundary; test revoked key/permission, stale epoch, changed audience/scope and unavailable I/D state; obtain exact I/H/G review.
- **Deadline/Gate:** before I trust/replay Gate and G Applied Gate pass.
- **Verification evidence:** callback/API contract, durable replay implementation tests, negative vectors, exact source pins and owner decisions.

## 5. Non-blocking but mandatory production seams

- The Phase 3.8.24 test canonicalizer is sorted-key JSON and explicitly not the production H canonicalization profile.
- H production signature profile, key registry, issuer/signer registration, trust roots, key custody, revocation precedence and anti-rollback must be H/I-approved; I's profile cannot be inherited.
- Durable observation replay storage, crash-safe reservation/commit, same-digest original-result retrieval, changed-digest conflict handling and retention are not implemented by the reference validator.
- Runtime Adapter integration, capability epoch issuance, real transport identity, cross-language vectors, SDK generation, crash/restore and multi-replica linearization are not established.
- G Applied persistence and D Forget fence remain separate authorities; H evidence cannot itself commit G Applied.

## 6. Required next sequence

1. H closes H-ADE-001 with strict parsing and exact-head CI.
2. H/C/G jointly close H-ADE-002 with exact C outcome semantics and request-boundary mapping.
3. H/I/G/D close H-ADE-003 with replay authorization/fence recheck ordering and tests.
4. H/I publish an H-owned production profile/registry decision and independent vectors; no I-profile inheritance.
5. H/G/Storage provide durable replay and crash/restore evidence; G retains sole Applied authority.
6. A re-reads all exact artifacts at current Owner HEAD and issues a new decision. Until then, overall architecture remains DEFERRED / ARCHITECTURE_NOT_READY.

## 7. Final A disposition

**DEFERRED — candidate implementation with bounded CI success; H-ADE-001, H-ADE-002 and H-ADE-003 remain OPEN and blocking for their respective protected paths.** No architecture freeze, schema freeze, Full Applied activation, Gate release, merge or production authorization is granted by this review.
