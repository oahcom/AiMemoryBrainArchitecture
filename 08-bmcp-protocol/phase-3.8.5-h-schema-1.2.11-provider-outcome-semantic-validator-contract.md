# Phase 3.8.5 — H Semantic Validator Contract for Schema Artifact 1.2.11 / C Provider Outcome

- Owner: H — BMCP Protocol and Interoperability
- Exact schema: `bmcp.coc-jf10-unified-1.2.11.schema.json`, Blob `4f1e103ab4b2ac961d77179dba0b65093532ea40`
- Wire family: `schema_version=1.3.0`; artifact revision: `1.2.11`
- C source amendment: Phase 3.8.6, Blob `392a3fd43790db59cb8aa5b3c919ca98e4bcddb4`
- Status: PROPOSED exact-revision validator contract; NOT FROZEN / NOT IMPLEMENTED / NOT EXECUTED.
- Provenance: delegated H-role simulation at user's direction, not independent human Owner approval.

## 1. Validation result model

Every message is evaluated in ordered layers:
1. Strict transport framing and UTF-8/JSON parsing.
2. JSON Schema validation against exact artifact revision 1.2.11.
3. Canonicalization and exact envelope/profile checks.
4. Owner signature and key-status/trust validation.
5. Message-family semantic invariants.
6. Typed-reference dereference and cross-record joins.
7. COC quorum/record-chain and Storage Batch/Manifest proof validation where applicable.
8. Currentness, anti-rollback and recovery-cutoff gate decision.

Outcomes:
- `VALID`: all required evidence is present, authoritative, current and consistent.
- `INVALID`: cryptographic, digest, schema, identity, enum, projection or cross-record contradiction.
- `UNKNOWN`: required authoritative evidence or currentness cannot be obtained, including unavailable provider lookup, key status, owner ledger, anti-rollback anchor or proof locator.
- `NOT_APPLICABLE`: only where the exact schema/contract defines a typed non-applicable branch with proof; never inferred from missing data.

INVALID and UNKNOWN both fail closed. UNKNOWN is not converted to empty, success, NOT_INVOKED or safe retry. Preserve the evidence and affected gate/barrier.

## 2. Exact schema and envelope rules

- Require artifact revision 1.2.11 and wire family 1.3.0 exactly for this profile; reject downgrade and ambiguous mixed-revision payloads.
- Validate the common envelope against the exact 1.2.11 schema and bind artifact revision in every protected signature.
- Duplicate JSON keys MUST be rejected before object materialization.
- Absent, null, empty string, empty array and empty object remain distinct.
- Reject unknown critical fields, invalid UTF-8, non-I-JSON values, non-finite numbers and unsafe numeric identifiers.
- Never infer a message authority from a filename, transport peer name or untrusted payload field; resolve authenticated authority and message-family ownership.

## 3. Signature/canonicalization requirements

The H/I candidate profile `AIMBA-I-CRYPTO-1.0` / `RFC8785-JCS-1.0` / `AIMBA-ED25519-SHA256-1.0` is I-only and is not automatically applicable to C. H requires a C-owned or explicitly jointly approved C profile with:
- exact immutable profile bundle ID and version;
- canonicalization profile and digest algorithm;
- exact C message-family projection allowlist;
- payload digest and domain-separated signature preimage;
- key ID/version and authenticated C trust/key-status evidence;
- anti-rollback and historical verification behavior;
- strict Base64url and Ed25519 verification only if the C/I governance profile explicitly adopts that candidate suite.

Until C/I publish and H pins the C profile, protected C Provider Outcome records cannot reach VALID; return UNKNOWN/UNSUPPORTED_PROFILE and block dependent release.

## 4. C Provider Outcome semantic validation

For `C_PROVIDER_OUTCOME_RECORDED`:
- enforce exact enum: `HANDOFF_ACCEPTED`, `HANDOFF_REJECTED`, `NOT_INVOKED`, `UNKNOWN`, `IN_DOUBT`;
- dereference immutable `c_submit_outcome_ref`, recompute its digest and compare every duplicated wire value;
- validate the complete attempt tuple: C admission ref/digest, C gate ref/generation, ProviderAttemptRef/generation, provider/account/adapter/endpoint/region, idempotency namespace/key, final request boundary and request digest;
- validate C owner ledger/version/sequence/high-water/root and prove referenced admission is included exactly once in the C owner-local snapshot;
- validate ParticipantIntent/Reservation pair or explicit null+reason, and join it to exact request digest and causal transaction;
- validate provider receipt/no-handoff/not-invoked/lookup evidence independently under its issuer's trust profile.

### 4.1 Outcome predicates

| Outcome | Required semantic predicate |
|---|---|
| HANDOFF_ACCEPTED | Authenticated provider/transport evidence proves exact request crossed handoff for exact attempt; no claim of inference completion or downstream Applied |
| HANDOFF_REJECTED | Authenticated rejection for exact attempt; not a no-side-effect proof unless a separate authoritative no-handoff proof exists |
| NOT_INVOKED | Authoritative Adapter/transport proof that exact attempt never crossed handoff; no receipt/egress commitment contradiction |
| UNKNOWN | Nonterminal reason and preserved original tuple; authoritative resolution unavailable |
| IN_DOUBT | Nonterminal ambiguity after possible handoff; same-key lookup/reconciliation only |

- A provider lookup proof must match provider/account/endpoint, namespace/key, ProviderAttemptRef/generation, FinalRequestBoundaryRef and RequestDigest. Same key with different request digest is INVALID.
- Lookup result absence is NOT_INVOKED only when provider capability contract guarantees authoritative complete absence for the relevant retention/consistency window. Otherwise UNKNOWN.
- Provider key retention expiry before authoritative reconciliation is UNKNOWN/IN_DOUBT, never permission to retry with a new key.
- Any provider failover or account/region/endpoint change is a new operation requiring fresh authorization/admission; it cannot inherit the previous attempt.

## 5. C Gate linearization semantic validation

H validates C evidence, it does not operate C's gate. Verify:
- CommitEgress and CloseEgressGate use the same durable serialization authority and monotonic gate generation.
- Close-wins implies no transport bytes for any older uncommitted admission.
- Commit-wins implies the exact attempt is included in close's in-flight set.
- crash after EGRESS_COMMITTED before durable transport result => UNKNOWN/IN_DOUBT.
- no process-local mutex/cached OPEN flag is accepted as multi-replica proof.
- SDK retries, redirects, stream continuations and failover cannot bypass fresh gate admission.
- C outcome's gate generation/attempt generation and request digest match the immutable C admission/reservation and provider evidence.

## 6. COC / Storage joins

- C owner-local admission is independently enumerated even when COC ParticipantIntentRef is null; null requires explicit reason and never means no C admission.
- If ParticipantIntentRef exists, validate exact ParticipantIntent -> ParticipantReservation chain and request digest equality.
- COC Recovery Cutoff Batch must precede Participant Manifest record. Validate exact ManifestId/content digest/count/high-water and Batch position/digest; then validate Manifest record's back-reference and record digest. Do not collapse content digest, Batch digest and Manifest record digest.
- C owner Gate Release remains blocked until exact S4 Batch/Manifest pair readback and semantic join are VALID.
- I authorization, D clearance, Storage Prepared/COMMITTED, H ACK, COC quorum or G Applied cannot synthesize provider handoff truth.

## 7. Error precedence and evidence preservation

- INVALID dominates UNKNOWN when an independently provable contradiction exists.
- Otherwise any missing/unavailable required authoritative proof yields UNKNOWN.
- Preserve original raw bytes, parsed canonical projection, schema artifact revision, validator version, all dereference refs/digests and decision trace.
- A later proof does not rewrite an earlier result; append a new validation/reconciliation record linked to the original.
- Validator MUST NOT mutate C owner records, I receipts, D fences, Storage ledger or provider outcomes.

## 8. Required conformance vectors

H must publish exact 1.2.11 vectors for:
1. all five outcome values, valid and invalid conditional proof combinations;
2. gate generation stale/current, close-wins and commit-wins;
3. provider attempt generation mismatch;
4. same-key same-digest versus same-key different-digest;
5. provider/account/endpoint/namespace mismatch;
6. authoritative no-handoff versus timeout/lost ACK/worker death;
7. rejection after possible side effect;
8. UNKNOWN/IN_DOUBT key expiry and unavailable lookup;
9. contradictory receipts and append-only supersession;
10. C admission ledger high-water/root and COC intent/reservation joins;
11. null ParticipantIntentRef with/without absence reason;
12. schema artifact downgrade, signature profile downgrade, duplicate JSON keys and unknown critical fields;
13. C signature projection mutation of every signed field;
14. Batch-before-Manifest and three-digest mismatch.

Execution record must identify exact schema/validator/vector blobs, language/runtime versions, command, CI run, pass/fail counts and retained output. A checked-in test file is not evidence that it ran.

## 9. Freeze gate

This contract is PROPOSED. It does not freeze 1.2.11 because the current schema's structural message does not alone carry every C gate/attempt semantic value and no exact C signature profile/vector bundle is yet pinned. H will only accept a later exact bundle after C's amendment, I candidate profile addendum Blob `1bcddbaaa4a9ca730d492a6554941becac305668`; C candidate review Blob `794d1dc49f034152407e3a42ba5ac937ea3539f8`. H schema/validator updates, independent cross-language execution and Storage/A exact pin review.

No tests, production readiness, provider-specific exactly-once or implementation acceptance are claimed.


## 10. Exact 1.2.11 wire mapping and current cross-owner inputs

The exact JSON Pointer/requiredness inventory and inline-versus-dereference matrix are maintained in H Phase 3.8.6, Blob `4f0e2a04009f2ac2f0c1e67d8ea6c104b07780e3`. It confirms that the 1.2.11 C branch does **not** inline CGateRef/CGateGeneration, ProviderAttemptRef/Generation, provider account, endpoint, region or API operation. These values MUST be obtained from the immutable C object referenced by `c_submit_outcome_ref`, then compared to provider evidence and all duplicated wire values. Missing members in an authoritative C object are INVALID; unavailable dereference/currentness is UNKNOWN.

Current C/I dependencies:
- C exact semantic signature projection proposal: Phase 3.8.8 Blob `a0e38c781d8aa2da5242dfce121e74b5141663d8`.
- I governance disposition: Phase 3.8.5 Blob `41fc0f508ae75e8c16012966160e9e2a1e368881`, conditional acceptance of the suite in principle only; no profile registration or deployment approval.
- C review of I candidate: Phase 3.8.7 Blob `794d1dc49f034152407e3a42ba5ac937ea3539f8`.
- C semantic amendment: Phase 3.8.6 Blob `392a3fd43790db59cb8aa5b3c919ca98e4bcddb4`.

The profile remains unregistered. C outcome records cannot be declared VALID merely because the common envelope carries SHA-256 and a signature; exact C profile registration, authenticated C key-status evidence, H projection implementation and independent vector execution remain mandatory.


## 11. CSubmitOutcome immutable object schema and test-harness binding

C's immutable object schema is `urn:aimba:schema:c-submit-outcome:1.0.0`, exact Blob `b5e87fa8df8463cf4cdc1ebc6867e643dcf5924c`. C's schema/conformance contract is Blob `eac5a6b02405aa554bd53095303e364bf25479de`.

The proposed H dereference pipeline MUST:
1. Validate the BMCP 1.2.11 envelope against exact schema Blob `4f1e103ab4b2ac961d77179dba0b65093532ea40`.
2. Resolve `c_submit_outcome_ref` under authenticated C object-store authority; reject a payload-supplied object as a trust anchor.
3. Validate the dereferenced object against exact C schema Blob `b5e87fa8df8463cf4cdc1ebc6867e643dcf5924c`.
4. Recompute and verify the object digest using the final registered C profile; current profile remains unregistered, so this gate is presently blocked.
5. Compare every duplicated wire member to the immutable C object, including provider/adapter/idempotency/request/outcome/evidence/COC and owner-ledger fields.
6. Validate C gate generation, provider attempt generation, provider account, endpoint, region and API operation from the C object and correlate provider evidence to the exact same tuple.
7. Independently verify C owner ledger membership/currentness, provider evidence issuer trust and COC intent/reservation/quorum joins.

C fixture pack Blob `e14eab2bed41f30af10a073b8e6523512128e78e` contains ten synthetic structural/semantic cases. C harness Blob `92e8e9e607566eafa6ad89110202dbeed0fc43cb` uses JSON Schema Draft 2020-12 plus selected semantic predicates. It does not verify signatures, provider issuer trust, ledger inclusion, gate linearizability or COC quorum. Fixture signatures are placeholders. The harness is NOT EXECUTED.

H must classify an absent required C object member or a proven digest/identity contradiction as INVALID. Unavailable object retrieval, currentness, key status or external authoritative proof is UNKNOWN. Both outcomes fail closed. No cross-language or production acceptance is implied.


## 12. H validator implementation interface (not executed)

H has added a fail-closed validator core:
- `08-bmcp-protocol/validators/provider_outcome_validator.py`, Blob `e8f737326bc4791e8d7acf917b4725dbb7171fad`.
- It performs strict JSON parsing helpers, separate BMCP/C-object schema validation, C-P0 digest recomputation, duplicated wire/object comparison and selected local semantic predicates.
- Trust-dependent operations are injected tri-state callbacks: C profile registration, C signature/key status, provider evidence issuer, C owner ledger membership/currentness, COC join and anti-rollback/currentness.
- Missing callback or unavailable evidence yields UNKNOWN; proven contradiction yields INVALID; INVALID dominates UNKNOWN.

This is an integration seam only. The caller MUST use `parse_strict_json` for raw bytes. The callbacks must be backed by authenticated authorities and must never trust payload-supplied public keys. The module is not yet connected to production key registries, object storage, provider trust, C ledgers or COC. It has not been executed against the full H schema or C fixtures.


## 13. Executable H unit/fixture test and currentness

H unit/fixture tests:
- Test file Blob `1f17bdcef6004eca165644ce96bcf35d3b10c3f8`.
- Requirements Blob `a90afd258a50582c33f0f7c7f5e979600322ae86`.
- Exact vendored C schema Blob `b5e87fa8df8463cf4cdc1ebc6867e643dcf5924c`.
- Exact vendored C vector fixture Blob `e14eab2bed41f30af10a073b8e6523512128e78e`.
- Workflow Blob `5f3a483c96594e3fd215fd6295e8937b9523cce0`.

The H Provider Outcome workflow run `44055334361` completed SUCCESS at commit `4837831c6c22973aba15be18e5376e56266b697b`, with 7 tests passing. That run predates the latest C schema fields `OwnerSignatureRef` and `ActualInferenceRequestId`, the complete optional wire mapping and the latest H callback changes. It is historical evidence only; it is NOT current validation of the latest code.

A new run is required after the latest H/C fixture synchronization. No signature, provider issuer, C ledger, COC quorum or production integration test is covered by these 7 unit/fixture tests.


## 14. I exact C schema review

I Phase 3.8.6 exact review Blob `cdfaa1c112210d65f9fd24fc1f5eb3caf8514fec` accepts the structural C object crypto binding only. It does not register/deploy the profile, trust root or key custody. It requires strict UTF-8/JCS/I-JSON handling, duplicate-key rejection, exact C-P0 coverage, strict Base64url decoding to 64 bytes, message_type domain binding, anti-rollback and independent cross-language signature vectors.

The H implementation core is Blob `e8f737326bc4791e8d7acf917b4725dbb7171fad`; the H unit/fixture test is Blob `1f17bdcef6004eca165644ce96bcf35d3b10c3f8`. The core exposes injected tri-state authority callbacks and must return UNKNOWN when profile registration or trust/currentness callbacks are absent. The COC and owner proof callbacks receive both envelope and immutable C object so they can validate independent COC/Storage/I/D refs without incorrectly folding them into C-P0.
