# B-02 Phase 8 — Issuer State-Machine Repair Specification and Cross-Owner Evidence Correction

# B-02 第八阶段 — Issuer 状态机修复规范与跨 Owner 证据纠偏

- Review baseline / 审查基线: `main` @ `b3c666e67982cb3d3374e759cfb6552c7765aacb`
- H / `session-h-bmcp-protocol`: `0d36324457e39bd50ad56ae902d477c4ea765b61`
- C / `session-c-agent-integration-2026-11-16`: `71047cdb51139ca4080ac67f451e38a48698859d`
- I / `session-i-security-governance-2026-11-16`: `0d071bf1ee7cc71912398c6ae57e4496e08f44ab`
- D / `session-d-memory-brain-2026-11-16`: `194c4c8d64972547cdbcf3fe64bd806c4d1d6a2f`
- Storage / `session-storage-consistency-forget-atomicity-2026-11-16`: `830a559bd2f4ec72608f5a51e1a0b43779f2b989`
- Role: A integration review and remediation design. This is not an Owner implementation or Owner approval.

## 1. Corrections to the previous A report

The previous Phase 7 report was too broad in two places. This phase corrects the record using exact Owner-branch evidence.

### 1.1 I has reviewed the 1.2.15 schema, P0 and corrected order — but has not registered production trust

I Phase 3.8.22 exact schema review Blob:
`6ba4ce3a93f2adf6f8961d4927d9b87deb9696bf`

I Phase 3.8.23 exact replay/acceptance-order re-review Blob:
`85cdbad04ae4b688338cdf2b667c21d2f02d8b96`

I Phase 3.8.21 digest-encoding re-review Blob:
`a16ab74f2cb5cfc67c04073bfa49dfb076383c91`

These reviews accept the H 1.2.15 structural trust-carrier candidate, corrected lowercase-hex digest / unpadded-Base64url signature encoding, and corrected receiver/replay acceptance order. They explicitly do **not** register the H profile, trust root, issuer, key custody, key-status history, revocation, anti-rollback, production transport identity or replay store. Their provenance is delegated I-role review, not independent human I Owner registration.

**Corrected disposition:** I contract-level review = ACCEPT WITH CONDITIONS; production I registration = OPEN. Do not label I's 1.2.15 review as wholly absent.

### 1.2 C has reviewed corrected issuance order — but not an executable H Issuer implementation

C Phase 3.8.26 schema review Blob:
`c5ff68814be49ec5e6e2c081004e7fa058d276fa`

C Phase 3.8.27 corrected ordering review Blob:
`3ca06dbfd7d59483e9604b7a68df924c719f60aa`

C accepts the contract order: authenticate original C adapter and capture raw origin context; validate C object schema/digest/signature/sequence/provider evidence/semantics; only then sign H gateway P0; receiver independently validates H and C; replay reservation/durable acceptance follows all required checks. C also explicitly says H P0/schema remain candidates and production C key/trust/provider-adapter evidence remains open.

**Corrected disposition:** C schema + order contract review = ACCEPT WITH CONDITIONS; C exact review of current H receiver validator Blob `9cc426d4c26deb452f39daff34c1008dd535e969`, a distinct issuer executable, and exact H CI run = not demonstrated by these two reviews.

### 1.3 D has only earlier 1.2.14 outer-auth boundary review

D Phase 3.8.14 Blob:
`4b512ad717296c6f8ab5b074048f2169dd9f6df2`

D Phase 3.8.13 Blob:
`152627e00b96355e2ff370acd643a51168c4c78c`

These reviews preserve D's authority boundary: H authentication does not mint D clearance or prove lineage completeness, late-discovery closure, barrier terminality or D-local release CAS. They review the 1.2.14 outer-auth interface and do not constitute an exact review of H 1.2.15 integrated mapping/issuer. D 1.2.15 exact review remains OPEN.

## 2. H implementation inspection: receiver exists; issuer does not

H current receiver validator Blob:
`9cc426d4c26deb452f39daff34c1008dd535e969`

The file header accurately calls it a reference integration implementation and says trust, signer, origin transport, key status, integrity evidence and durable replay are deployment seams/callbacks.

The receiver implementation sequence is:
1. strict parse H envelope and C object;
2. validate H 1.2.15 schema;
3. compare H sender/audience/channel with protected receiver context;
4. construct H P0 and check payload digest / signature encoding;
5. call H profile, key-status, H signature, integrity, identity/delegation and origin-receipt callbacks;
6. independently call C Provider Outcome validator;
7. only after C result VALID call durable replay/ingress commit callback;
8. for replay, re-check authorization before disclosing prior result.

That is a receiver-side verification flow. It does not implement H's pre-sign issuer path.

A recursive H branch-tree inspection found the receiver validator and related tests but no distinct issuer/signing-pipeline implementation entrypoint. H P0 contract Blob `93b83ac35114d20d64579d919c0699886940f0fa` requires C verification before H signing, but contract prose plus receiver code is not executable issuer proof.

## 3. Normative issuer pipeline required from H

The following is the acceptance contract for the H Owner to implement. It is intentionally a specification, not code added to H's protected branch.

```text
receive_original_C_bytes
  -> authenticate_C_adapter_and_capture_immutable_origin_receipt
  -> strict_parse_C_object
  -> validate_exact_CSubmitOutcome_1.0.1_schema
  -> verify_C_object_P0_digest_and_C_signature
  -> verify_C_key_status_and_C_sequence_namespace
  -> verify_C_semantics_and_provider_evidence
  -> verify_origin_receipt_to_C_AdapterRef_binding
  -> require_all_C_checks == VALID
  -> resolve_I_approved_H_issuer_profile_and_delegation
  -> reserve_H_signing_operation_idempotently
  -> canonicalize_exact_H_P0_and_compute_digest
  -> invoke_H_signer_for_reserved_operation
  -> persist_signature_and_immutable_H_attestation
  -> publish_attestation_to_receiver
```

Hard precondition:

`C_VALID == true` must be established before any H signing operation is created or invoked. C INVALID or UNKNOWN must not allocate an H signing sequence, invoke HSM/KMS signing, create an H signature, or publish a signed H attestation.

An audit-only unsigned ingress receipt may be retained if its state and semantics are clearly distinct from an H-signed Gateway Attestation and from a semantically accepted Provider Outcome.

### 3.1 State machine and crash/retry contract

| Durable state | Entry condition | Permitted next action | Crash/retry rule |
|---|---|---|---|
| ORIGIN_CAPTURED | C adapter authenticated; immutable raw bytes and receipt pinned | C validation | Retry same origin/message identity; never replace raw bytes |
| C_VALIDATED | C schema, P0, signature, key status, sequence, evidence and semantics all VALID | reserve H signing operation | INVALID/UNKNOWN terminal for this attempt; no signer invocation |
| H_SIGN_RESERVED | C_VALIDATED plus I-approved profile/delegation; idempotency key unique | build immutable H P0 | Reservation is durable and bound to C digest, origin receipt digest, message ID, nonce, audience and profile |
| H_SIGN_REQUESTED | exact P0 digest/preimage fixed; signer request has stable operation ID | reconcile signer result | Retry same operation ID; never allocate a second sequence for same operation |
| H_SIGNED | signer result cryptographically verified and durably recorded | persist immutable attestation | Signature, key version, sequence, P0 digest and evidence record must be bound |
| ATTESTATION_COMMITTED | immutable envelope and integrity evidence durable | publish/dispatch | Dispatch retry sends the same immutable envelope |

Additional rules:
- H signing sequence is monotonic within its own namespace; it is never reused. Gaps are acceptable if reservation is durable and auditable.
- A crash after reservation must recover the same reservation and sequence. It must not silently allocate a replacement sequence.
- A timeout after an HSM/KMS request is UNKNOWN until the exact operation ID is reconciled. Do not call the signer under a new operation ID.
- The signing API must be idempotent by operation ID, or the issuer must provide an equivalent durable reconciliation protocol. A process-local lock/cache is insufficient.
- The immutable signed envelope is not visible to the receiver until its signature and evidence record are durably committed.
- If signer outcome cannot be reconciled, preserve UNKNOWN; do not synthesize success or retry with a new message ID.
- Receiver revalidation remains mandatory and independent. Issuer validation does not bypass receiver checks.

### 3.2 Required negative tests

H must add tests proving:
1. C schema INVALID → H signer call count = 0; no H signing reservation.
2. C P0 digest mismatch → signer call count = 0.
3. C signature INVALID → signer call count = 0.
4. C key status UNKNOWN/revoked/compromised → signer call count = 0.
5. C sequence namespace mismatch/rollback → signer call count = 0.
6. C provider semantics UNKNOWN/IN_DOUBT → no signed H attestation.
7. origin raw-byte digest or AdapterRef relation mismatch → INVALID and no signing.
8. I profile/issuer/delegation unavailable → UNKNOWN and no signing.
9. crash after H_SIGN_RESERVED → recover same operation and sequence.
10. timeout after HSM request → reconcile same operation ID; no second sequence.
11. crash after signature but before persistence → reconcile exact signature operation and persist same immutable envelope.
12. duplicate delivery → same reservation / same envelope; no second semantic acceptance.
13. changed C digest under same message identity → INVALID conflict.
14. receiver must independently reject forged H signature, stale key, stale authorization, invalid C object and D fence mismatch.
15. UNKNOWN must never be coerced to VALID by a retry wrapper.

The tests must include real independent cryptographic verification vectors for C and H signatures. Deterministic callbacks remain useful unit doubles but are not production crypto evidence.

## 4. Cross-owner acceptance matrix

| Owner | Evidence already present | Remaining exact action |
|---|---|---|
| H | 1.2.15 schema/P0/mapping, receiver validator and tests; exact workflow run SUCCESS | publish issuer executable path + crash-safe state machine + tests; publish 1.2.15 integrated authority-join successor |
| C | Phase 3.8.26 schema review and 3.8.27 order review | exact-review current receiver validator, issuer code/tests, and exact CI bundle after H publishes them |
| I | Phase 3.8.21/22/23 reviews for encoding, schema and replay order | separate registration decision for exact H issuer/profile/trust root/key custody/key status/revocation/anti-rollback and production transport |
| D | Phase 3.8.13/14 outer-auth boundary reviews | exact 1.2.15 review preserving D clearance, lineage, fence, late-discovery, barrier terminality and final release CAS |
| Storage | v3.3.2 historical manifest for H 1.2.14 + C 1.0.1 | new immutable successor manifest only after H/C/I/D exact artifacts and reviews stabilize |
| A | Phase 7 role remediation report and this Phase 8 specification | same-bundle readback and disposition only; cannot sign for any Owner |

## 5. Storage bundle rule

Storage current Phase 3.6.22 manifest Blob:
`5c614375e10698e4931d83deb57d20321445e068`

It is v3.3.2 and remains a historical H 1.2.14 + C 1.0.1 bundle. Do not mutate or reinterpret it. A successor must bind exact:
- H 1.2.15 schema, P0, integrated mapping, issuer implementation and receiver validator;
- H/C/I/D validator/test evidence;
- exact workflow Blob, run ID, commit SHA, job ID and test summary;
- C schema/order/validator reviews;
- I registration or explicitly unregistered status;
- D 1.2.15 clearance/lineage review;
- Storage COC reservation/commit/absence/recovery semantics;
- source maturity of every evidence item (contract, candidate, deterministic double, CI-tested, physical, operational).

Storage must not publish a 1.2.15 accepted bundle while the H issuer path or I/D authority evidence is missing.

## 6. Current exact dispositions

- H 1.2.15 schema shape: **CANDIDATE; C/I contract reviews exist**
- H P0 corrected order: **CONTRACT ACCEPTED WITH CONDITIONS by C and I role reviews**
- H receiver validator: **REFERENCE IMPLEMENTATION; exact current Blob not yet reviewed by C/I/D**
- H issuer pre-sign executable chain: **OPEN / NOT FOUND**
- H 1.2.15 integrated authority-join successor: **OPEN / NOT FOUND**
- C exact review of current validator/issuer implementation: **OPEN**
- I production profile/issuer/key/trust registration: **OPEN**
- D exact H 1.2.15 currentness/Forget/lineage review: **OPEN**
- Storage 1.2.15 successor manifest: **OPEN**
- H CI path + exact-head run 44079842914 / job 134027249681: **PASS — bounded workflow execution only**
- B-02: **PARTIAL / OPEN**
- G1–G8: no PASS declared; no architecture freeze recommended.

## 7. Governance and provenance

This Phase 8 artifact is an A-side review specification only. It changes no Owner branch, main, prior PR, or Issue #43. Role-based review evidence cited here is explicitly delegated role work and not an independent human Owner signature. No production trust registration, Gate release, implementation authorization, merge, deployment or activation is claimed.

## 8. Exact evidence ledger

| Artifact | Exact pin |
|---|---|
| Main | `b3c666e67982cb3d3374e759cfb6552c7765aacb` |
| H HEAD | `0d36324457e39bd50ad56ae902d477c4ea765b61` |
| C HEAD | `71047cdb51139ca4080ac67f451e38a48698859d` |
| I HEAD | `0d071bf1ee7cc71912398c6ae57e4496e08f44ab` |
| D HEAD | `194c4c8d64972547cdbcf3fe64bd806c4d1d6a2f` |
| Storage HEAD | `830a559bd2f4ec72608f5a51e1a0b43779f2b989` |
| H P0 corrected contract | `93b83ac35114d20d64579d919c0699886940f0fa` |
| H schema | `860fc4cec658db7d2703cd6adf72aa31a2723f6d` |
| H schema mapping | `2dc30f193d9c4f4bdc05ca4c137103687db28924` |
| H receiver validator | `9cc426d4c26deb452f39daff34c1008dd535e969` |
| H workflow | `2ad679952ce5499a16c8fffa0a1543e26460e6eb` |
| H CI run / job | `44079842914` / `134027249681` |
| C Phase 3.8.26 | `c5ff68814be49ec5e6e2c081004e7fa058d276fa` |
| C Phase 3.8.27 | `3ca06dbfd7d59483e9604b7a68df924c719f60aa` |
| I Phase 3.8.21 | `a16ab74f2cb5cfc67c04073bfa49dfb076383c91` |
| I Phase 3.8.22 | `6ba4ce3a93f2adf6f8961d4927d9b87deb9696bf` |
| I Phase 3.8.23 | `85cdbad04ae4b688338cdf2b667c21d2f02d8b96` |
| D Phase 3.8.13 | `152627e00b96355e2ff370acd643a51168c4c78c` |
| D Phase 3.8.14 | `4b512ad717296c6f8ab5b074048f2169dd9f6df2` |
| Storage v3.3.2 | `5c614375e10698e4931d83deb57d20321445e068` |

---
End of Phase 8 review.
