# Phase 3.11.1 — CSubmitOutcome 1.0.1 Explicit Sequence Namespace Amendment

- Owner: C — Provider Outcome immutable object
- Supersedes for new records: CSubmitOutcome 1.0.0 schema Blob `b5e87fa8df8463cf4cdc1ebc6867e643dcf5924c`
- New schema: `schemas/c-submit-outcome-1.0.1.schema.json`, Blob `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda`
- New ten-case fixture pack: Blob `c447f8c2908469c52cb52a448101495a331277c5`
- C key-status event schema: Blob `908b293eba337e9fa75864cea3704e28a1a8d82e`
- C key-status lifecycle contract: Phase 3.11.0 Blob `9339b168165a7a3dd34def5236ad61cfd3163418`
- Status: PROPOSED 1.0.1 immutable revision; 1.0.0 remains historical and unchanged.
- Provenance: delegated C-role simulation at user's direction; not independent human C Owner approval.

## 1. Why 1.0.1 exists

The 1.0.0 object carried `record_sequence` but did not explicitly identify the sequence namespace in which that value is meaningful. The key-status event schema separately carried `sequence_namespace_ref`. Without an explicit equality join, H could not prove that CSubmitOutcome signing sequence and C key-status transition sequence belonged to the same monotonic ordering domain.

A must not infer this relationship from issuer labels or wall-clock timestamps. C therefore publishes a new immutable schema revision rather than mutating 1.0.0.

## 2. New normative field

CSubmitOutcome 1.0.1 adds required:

- `sequence_namespace_ref`: opaque C authority-issued sequence namespace reference.

For a protected CSubmitOutcome, H MUST verify:
1. `sequence_namespace_ref` equals the namespace of the C key-status event ledger and the authoritative C signing sequencer.
2. `record_sequence` is allocated by that same durable linearizable C sequencer.
3. Each CKeyStatusEvent `event_sequence` is allocated in the same namespace.
4. No cross-process wall-clock comparison, local counter, database auto-increment from an unrelated store or event arrival order is used as a substitute.
5. The current key-status ledger head and external anti-rollback checkpoint are at least as new as the signing sequence and event chain being evaluated.

A missing/mismatched namespace is INVALID. An unavailable authoritative sequencer, key-status ledger or checkpoint is UNKNOWN.

## 3. Immutable version rules

- Schema ID: `urn:aimba:schema:c-submit-outcome:1.0.1`.
- Schema version/artifact revision: `1.0.1`.
- The 1.0.0 schema and its vectors remain immutable historical artifacts.
- New records MUST use 1.0.1 once the corresponding H wire dereference/validator bundle is accepted.
- A 1.0.0 object cannot be silently interpreted as 1.0.1; version mismatch is INVALID.
- The C candidate profile ID remains `AIMBA-C-CRYPTO-1.0` and is still NOT REGISTERED.

## 4. Updated candidate crypto vectors

The 1.0.1 candidate vectors include `sequence_namespace_ref=C/sequencer/provider-outcome` in C-P0. Therefore all P0 digests, signatures and static expected fingerprints are version-specific and differ from 1.0.0.

Artifacts:
- Crypto manifest: `c_crypto_profile_vector_1_0_1.json`, Blob `3a5fb8502091636135a298de5891d728b550ba50`.
- Expected crypto fingerprints/signatures: Blob `34e49a49551390f52198b1fa557e15a32a3f6ee2`.
- Python tests: `test_c_crypto_profile_1_0_1.py`, Blob `c798379b43e77f264782a4b5ea7ad8282d779d8d`.
- Node oracle: `c_crypto_profile_reference_1_0_1.mjs`, Blob `27d2e512db86bfd1cf6b9227280ee18a3a791d19`.
- Structural tests: `test_c_submit_outcome_1_0_1.py`, Blob `0357c7fc22c714ce50ed4ce4771510431f2b1637`.

## 5. Executed C CI evidence

- Run: `44059935858`.
- Exact tested commit: `b49966361b4b3121a2ebf4105b4e0c57a612e945`.
- Result: SUCCESS; 19 tests total.
- Includes 1.0.1 Draft 2020-12 schema validation, ten structural/semantic vectors, five outcome-family candidate Ed25519 signatures, every-present-field mutation rejection, Python/Node candidate byte/digest/preimage/signature agreement, and 64-byte signature/32-byte public key checks.
- Python 3.12 and Node.js 22; deterministic public test-only seed.

This run validates the candidate construction for 1.0.1. It does not register the C profile, activate a C key, verify governance key custody, or prove production key status/anti-rollback.

## 6. Decision

**C ACCEPTS 1.0.1 AS THE CURRENT PROPOSED IMMUTABLE OBJECT REVISION FOR EXPLICIT SEQUENCE-NAMESPACE BINDING. NOT FROZEN.**

H owns the exact BMCP 1.2.12 → CSubmitOutcome 1.0.1 wire mapping and validator. Its consumer artifact is bound by the Storage successor bundle manifest rather than cross-pinned here. I reviews the signed field inventory and governance key-status binding. A reviews the exact C/H/I/Storage bundle before any freeze decision.

No production egress, profile registration, key activation, exactly-once property or production readiness is claimed.


## 7. H independent 1.0.1 verification

H has updated its validator to require CSubmitOutcome 1.0.1 and the explicit sequence namespace:
- BMCP schema 1.2.12 Blob `a54f66914a819d77f00c6af04e76453ff9f654ee`.
- H exact mapping is a separate H-owned consumer artifact; its current exact Blob is bound in the Storage successor bundle manifest. C does not pin H's consumer artifact here, avoiding a cyclic source/consumer reference.
- H validator core Blob `1a92c0cf7146e2884bd38232005dd9a55d558a85`.
- H independent Python 1.0.1 verifier Blob `5559fb7a612c8dd92345ceae3a6aa62f4faae41a`.
- H Node 1.0.1 oracle Blob `07c34b03aff94e1dfbbd1aa056ac849debeb3348`.
- H CI run `44060704553`, exact commit `8c377a7218b70621d2348b47341d4cf4755b3733`: SUCCESS, 17 tests.

H's 17-test run validated the 1.0.1 schema namespace field, recomputed all five 1.0.1 candidate crypto vectors, verified signatures and field mutations, matched H Python/Node output to static expected values, and retained the earlier 1.0.0/key-status tests as historical checks.

This is independent candidate-only validation. It does not prove a production C sequencer, key-status ledger, governance trust root or anti-rollback checkpoint exists.


## 8. Source/consumer pinning rule

C's immutable object schema and this C-owned semantic amendment are source artifacts. H's wire mapping and validator are consumer artifacts. To avoid a cyclic Blob-reference graph, C does not pin H's mapping Blob; the Storage successor exact-version manifest binds both independently. H MUST pin this exact C source Blob and the applicable I review Blob. I's review pins the C source Blob but does not pin H's mapping. A consumes the Storage bundle manifest and reviews the exact join.

**中文：** C 的不可变对象 Schema 与本修订是源权威工件；H 的 Wire Mapping/Validator 是消费方工件。为避免 Blob 引用形成循环，C 不反向绑定 H 的 Mapping Blob；由 Storage 后继精确版本清单分别绑定两者。H 必须绑定本 C 源 Blob 与适用的 I Review Blob；I Review 绑定 C 源 Blob，不反向绑定 H Mapping；A 最终审查 Storage Bundle Manifest 中的精确 Join。
