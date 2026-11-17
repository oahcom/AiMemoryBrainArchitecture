# P Proposal — C Envelope Signer Decision Reconciliation v0.1.0
# P 提案 — C Envelope Signer 决策协调 v0.1.0

- Status: **P COORDINATOR PROPOSAL / C OWNER DECISION REQUIRED / NOT NORMATIVE**
- Exact current C artifacts:
  - Corrected C decision candidate: `310e7e0073d3c32f594bc151f10c249c828ce30f`
  - C H-60-test review: `8fd6052cabf58a78962cc2e776398b2a40604bcd`
- H mapping: `4ba7e1699215d02224f805a15484b1da2e40c03f`
- I corrected review: `63d7bfc4ad08bd75e8c0a16c34b3c4ca95e76d00`

## 1. Conflict / 冲突

The corrected C decision candidate says the C provider adapter signs the outer C_PROVIDER_OUTCOME_RECORDED envelope and the immutable CSubmitOutcome object as two separate signed objects. H gateway receipt is additive only.

The later C review of H's 60-test reference gate still says signer/attestation is OPEN and recommends a distinct H-gateway attestation while preserving C object signature. That later review does not explicitly supersede or reaffirm the earlier C signer decision.

P cannot choose between these statements. The decision candidate itself is not an independent C Owner signature, and the later review is also a delegated role artifact.

## 2. Required C Owner reconciliation / 必需 C Owner 协调

C must publish one exact current decision artifact that states one of these alternatives without ambiguity:

**Option 1 — C-origin outer-envelope signature**
- C adapter signs the immutable CSubmitOutcome object under the existing C object profile.
- C adapter separately signs the outer envelope under a distinct C envelope P0/profile.
- H gateway receipt is optional/additive and cannot replace the C signature.
- I independently approves profile/trust/key registration.
- H implements exact JSON-Pointer extraction and verification.

**Option 2 — H-gateway receipt + authenticated C transport origin**
- C object remains signed by C under its own C object P0/profile.
- H gateway signs a distinct ingress receipt/attestation after independently authenticating the C adapter transport principal and exact received envelope.
- The receipt proves only gateway receipt/binding, not provider truth.
- C explicitly accepts the reduced/non-signature envelope origin model and specifies the transport-authenticated attribution contract.
- I approves H gateway signer trust and transport principal policy.

Option 1 is consistent with the corrected C decision candidate and the H/I two-object separation reviews. Option 2 resembles the later C 60-test review recommendation. P does not select either on C's behalf.

## 3. Exact profile/P0 requirements / 精确 Profile/P0 要求

Whichever option C adopts:
- keep C object P0 and outer envelope/receipt P0 distinct;
- never reuse `AIMBA-C-CRYPTO-1.0` for the outer object without a separately reviewed profile;
- include both `integrity_proof_ref` and `channel_binding_proof_ref` in any signed outer projection if serialized;
- distinguish issuer, signer, transport peer, message owner and provider semantic authority;
- bind exact H schema artifact revision, message family, audience, nonce, proof locators and all message-family fields;
- define absent/null/empty semantics exactly;
- keep provider truth, I authorization, D clearance, Storage resolution and COC durability as independent proof domains.

## 4. Closure evidence / 关闭证据

C must publish:
1. a supersession/reconciliation addendum referencing both current C artifacts by exact Blob;
2. updated C review of H 60-test ingress that agrees with the selected signer model;
3. exact C profile/P0 contract and independent cross-language vectors if Option 1 is selected;
4. exact transport-origin and gateway-receipt contract if Option 2 is selected;
5. explicit statement that this is not production authorization until I trust registration and H/Storage integration pass.

**No P coordinator simulation is counted as C Owner acceptance.**
