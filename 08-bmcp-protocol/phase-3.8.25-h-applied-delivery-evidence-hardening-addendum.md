# Phase 3.8.25 — H Applied Delivery Evidence 1.0.0 Hardening Addendum
# Phase 3.8.25 — H Applied Delivery Evidence 1.0.0 加固补充

- Parent candidate: Phase 3.8.24, schema Blob \`2ce8776ca5ee5e014b234dc3eb34a7cb7961e608\`.
- Scope: H-ADE-001 duplicate JSON member rejection and H-ADE-003 current authorization before replay-result disclosure.
- Status: **CANDIDATE REMEDIATION BRANCH; EXACT CI AND H/I/D OWNER ACCEPTANCE PENDING**.
- This addendum does not amend CSubmitOutcome semantics, G Applied acceptance, I authorization policy, or D ForgetFence authority.

## 1. Duplicate-key parsing

The reference validator now parses with an \`object_pairs_hook\` that rejects duplicate member names at every JSON object depth before schema validation, P0 construction, digest comparison or signature callback invocation. This prevents the default decoder's last-value-wins behavior from hiding conflicting signed fields.

The candidate test suite adds top-level and nested duplicate-member negative vectors. The schema's \`additionalProperties: false\` remains necessary but is not a substitute for duplicate-aware raw JSON parsing.

## 2. Replay disclosure authorization

The validator contract now requires \`verify_current_replay_authorization(envelope, original_result_ref)\` for \`SAME_DIGEST_REPLAY\`. The callback is tri-state:
- True: the original result reference may be returned.
- False: INVALID; do not disclose the result reference.
- None or exception: UNKNOWN; do not disclose the result reference.

The callback contract must recheck current I authorization/PermissionEpoch, current key status, audience/scope and applicable D ForgetFence at the owner-defined decision boundary. A historical signature and same digest do not confer perpetual disclosure authorization.

Candidate tests cover denial, UNKNOWN and callback exception; all assert that \`original_result_ref\` is absent.

## 3. Remaining blockers

- H-ADE-002 / C/G mapping remains OPEN: the immutable CSubmitOutcome 1.0.1 resolver, full COutcomeRecordIdentity authentication and exact field equality are not implemented by this addendum.
- H production trust roots, H key/profile registration, production canonicalization/signature, durable replay ledger, crash-safe reservation and runtime Adapter integration remain OPEN.
- The new callback is an adapter seam. This branch does not implement I or D authority ledgers and cannot claim their production checks.
- G has not yet issued a successor consumer decision for this H 1.0.0 family.
- No C/G/H Full Applied freeze or production activation is implied.

## 4. Verification required

Run the H Applied Delivery Evidence conformance workflow against the exact final head; read back validator, tests and workflow pins; obtain H review of this addendum and exact I/D review of the replay authorization callback contract. The branch remains a candidate until those steps complete.

**Disposition: H-ADE-001 and H-ADE-003 remediation proposed in reference code; production/owner closure NOT YET VERIFIED. H-ADE-002 remains OPEN.**
