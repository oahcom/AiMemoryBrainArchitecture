# Session 4 — A: H Unified 1.2.15 Validator / CI / Trust Exact Review
# Session 4 — A：H Unified 1.2.15 Validator / CI / Trust 精确审查

- Review date: 2026-11-18
- Repository: `oahcom/AiMemoryBrainArchitecture`
- Review mode: read-only source review; this report is an A coordination artifact, not an H/C/I Owner approval.
- Main baseline: `b3c666e67982cb3d3374e759cfb6552c7765aacb` (tree `7096e0bc3fdc9a390fccff388f9261522fa424f2`)
- H branch HEAD: `0d36324457e39bd50ad56ae902d477c4ea765b61`
- C branch HEAD: `71047cdb51139ca4080ac67f451e38a48698859d`
- I branch HEAD: `0d071bf1ee7cc71912398c6ae57e4496e08f44ab`
- Storage branch HEAD: `830a559bd2f4ec72608f5a51e1a0b43779f2b989`
- Overall disposition: **DEFERRED**
- H 1.2.15 evidence status: **LOCAL VALIDATOR + EXACT-HEAD CI PASS; CROSS-OWNER EXACT REVIEW PARTIAL; PRODUCTION TRUST / ISSUANCE / DURABLE REPLAY OPEN**
- No schema freeze, no production authorization, no Gate B/C advancement.

## 1. Executive determination

H 1.2.15 has materially progressed beyond a schema-only candidate. The current H branch contains the 1.2.15 schema, a dedicated local provider-outcome validator, a gateway-attestation receiver validator, a 21-method gateway-attestation test class, and a workflow that includes those tests. GitHub Actions has a successful Provider Outcome run on the exact current H HEAD.

This establishes bounded local L1/L2 reference evidence. It does **not** establish production authentication, production signer registration, H gateway issuance ordering, durable replay, or live I/D/Storage authority integration. C's schema review explicitly said validator/CI had not yet been reviewed; the later C order review accepts the corrected sequence as a reference contract but does not pin/review the current validator Blob. I's later order review pins a predecessor gateway-validator Blob, not the current implementation.

Therefore, do not treat the 1.2.15 bundle as jointly accepted, frozen, production-ready, or eligible to replace the H 1.2.14 bundle in Storage v3.3.2.

## 2. Exact artifacts and execution evidence

| Artifact | Exact Blob / SHA | Finding |
|---|---|---|
| H Unified schema 1.2.15 | `860fc4cec658db7d2703cd6adf72aa31a2723f6d` | Structural candidate; not frozen |
| H 1.2.15 C mapping | `2dc30f193d9c4f4bdc05ca4c137103687db28924` | Mapping candidate |
| H local C Provider Outcome validator | `90a2d4b6f5b05590e3e0a7daecb5a01d9bf525c0` | Explicitly not secure ingress; injected authority callbacks |
| H gateway-attestation validator | `9cc426d4c26deb452f39daff34c1008dd535e969` | Receiver/reference validator; callbacks are deployment seams |
| H gateway-attestation tests | `9a5051b001a6e59d7b71e6dd175e84bb7d01d252` | Includes positive and fail-closed cases |
| H Provider Outcome workflow | `2ad679952ce5499a16c8fffa0a1543e26460e6eb` | Includes 1.2.15 schema, validator and conformance test paths |
| H gateway P0 contract candidate | `93b83ac35114d20d64579d919c0699886940f0fa` | Candidate only; profile not registered |
| CSubmitOutcome 1.0.1 schema | `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda` | C object structural source |
| C review 3.8.26 | `c5ff68814be49ec5e6e2c081004e7fa058d276fa` | Schema accepted with C-owned conditions; validator/CI not reviewed |
| C order review 3.8.27 | `3ca06dbfd7d59483e9604b7a68df924c719f60aa` | Corrected issuance/receiver/replay order accepted as reference contract |
| I review 3.8.22 | `6ba4ce3a93f2adf6f8961d4927d9b87deb9696bf` | Schema accepted as trust-carrier candidate; no registration |
| I order review 3.8.23 | `85cdbad04ae4b688338cdf2b667c21d2f02d8b96` | Corrected order accepted as reference contract; production trust/replay open |
| Storage v3.3.2 manifest | `5c614375e10698e4931d83deb57d20321445e068` | Still pins H 1.2.14, not 1.2.15 |

Exact current-H-HEAD workflow evidence:
- H Provider Outcome Conformance run **44079842914**, job **134027249681**, tested commit `0d36324457e39bd50ad56ae902d477c4ea765b61`: **SUCCESS**, raw log: **91 tests, 0 failures**.
- H Recovery Cutoff Conformance run **44079842878**, job **134027249428**, same tested commit: **SUCCESS**, raw log: **288 tests, 22 skipped, 0 failures**.
- Provider Outcome run: https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44079842914
- Recovery Cutoff run: https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44079842878

The Provider Outcome workflow executes `python -m unittest discover` across the full provider_outcome test directory. The 91-test result is exact-H-HEAD evidence, not merely the presence of test source. The 288-test run is adjacent H recovery/wire evidence; it is not 1.2.15 gateway-trust proof.

## 3. Technical findings

### H1215-F01 — Exact-head local conformance is demonstrated
**Severity:** Medium; non-blocking for reference-candidate status.  
The current H HEAD runs both workflows successfully. The gateway test class exercises revision pinning, required origin fields, owner-authority constraint, digest/raw-byte mismatch, signing-sequence syntax, missing profile registry as UNKNOWN, H-signature failure before ingress commit, origin mismatch, C-signature independent failure, unavailable C signature as UNKNOWN/no durable commit, P0 mutation, unknown-field rejection, replay authorization, and unavailable durable state.

**Evidence ceiling:** tests inject deterministic callbacks. Test assertions prove callback orchestration and local tri-state behavior, not production trust or cryptographic key verification.

### H1215-F02 — C and I accept schema/order candidates, not the current executable bundle
**Severity:** High; blocking for cross-owner closure.  
C 3.8.26 accepts schema shape with C-owned conditions and expressly states validator/CI not yet reviewed. C 3.8.27 accepts the corrected order: authenticate original C adapter and capture raw ingress; validate C object/schema/digest/signature/semantics before H signing; receiver independently validates H attestation and C object; durable replay/acceptance only after required checks. It does not pin the current gateway validator Blob `9cc426...` or the exact CI run.

I 3.8.22 accepts the schema only as a trust-carrier candidate and explicitly leaves profile registration, issuer/key approval, custody, key status, revocation, historical verification and anti-rollback open. I 3.8.23 accepts the order as a reference contract but pins gateway validator Blob `d16ca2e...`, whereas the current H validator is Blob `9cc426...`. The I review therefore cannot be represented as exact review of the current validator implementation.

### H1215-F03 — Issuance-order proof is missing
**Severity:** Critical; blocking.  
The current `validate_gateway_attested_provider_outcome` function is a receiver-side validator for an already-signed H envelope. It verifies the H attestation and only then calls the C provider-outcome validator. That is not itself a defect in a receiver verifier; however, it cannot prove C's required **issuer-side** order that H validates C schema/digest/signature/sequence/provider evidence/semantics *before it creates or signs* the H P0. No exact issuer implementation, signing service boundary, or issuance-order test evidence was found in the current H tree.

Required closure: H must provide the exact issuer path or an explicit architecture boundary proving where C verification precedes H signing, with tests proving invalid/UNKNOWN C objects cannot cause H signatures to be issued.

### H1215-F04 — Production trust and replay remain callback seams
**Severity:** Critical; blocking.  
The gateway validator's profile registration, key status, H signature, integrity evidence, identity/delegation, origin receipt, durable replay commit, and replay-disclosure authorization are injected callbacks. The module itself says it is a reference integration implementation, not production cryptography or a deployed trust service. The C validator likewise says missing authority callbacks return UNKNOWN and that it is not a production-ready trust implementation.

Required closure includes an I-approved immutable profile/issuer/signer registry; trust-root/key custody and lifecycle; durable H signing sequencer and authenticated key-status history; origin transport verifier and immutable raw-byte receipt; real H signature and integrity-evidence verification; durable replay reservation/result with crash recovery; and current I authorization/PermissionEpoch, key status, audience/scope and D Forget-fence recheck before prior-result disclosure.

### H1215-F05 — Cross-review pins require refresh
**Severity:** High; blocking.  
I 3.8.23 pins an older gateway validator Blob `d16ca2e...`, not current `9cc426...`. C 3.8.27 references C 3.8.26 review Blob `78fd99...`, while the current C 3.8.26 file on its branch is Blob `c5ff688...`. The C schema review explicitly did not review validator/CI. These are version-binding gaps, not proof that the underlying contracts are wrong.

Required closure: H publishes a frozen candidate bundle manifest with exact schema, mapping, P0, issuer/receiver validators, all fixtures/tests, workflow and successful run/job evidence; C and I then review those exact Blobs and test evidence. Any changed Blob requires re-review.

### H1215-F06 — Storage bundle remains on 1.2.14
**Severity:** Critical for successor adoption; blocking.  
Storage v3.3.2 Blob `5c614375...` binds H Unified 1.2.14 Blob `09fcd1...`, not 1.2.15. The old 60-test CI and reviews cannot be transferred to the new schema/validator. No Storage successor manifest should be published as accepted until H/C/I exact closure is complete.

## 4. Required closure conditions

| ID | Owner | Required closure evidence | Gate |
|---|---|---|---|
| H1215-C01 | H | Exact issuer-side C-before-H-signing implementation or formally specified trust boundary; tests prove C INVALID/UNKNOWN cannot be H-signed | Gate A, B |
| H1215-C02 | H | Immutable exact bundle manifest: schema, mapping, P0, validator(s), fixtures, tests, workflow, run/job SHA and evidence ceiling | Gate A |
| H1215-C03 | C | Exact re-review of current H validator/issuer path, all 12 conditional fields, C duplicate-field mapping, independent C signature, C UNKNOWN/IN_DOUBT nonterminal behavior, and exact CI run | Gate A, B |
| H1215-C04 | I | Exact review and formal registration decision for H profile, issuer/authority/subject/delegation, trust root, key custody/lifecycle, sequence/key-status history, revocation precedence, historical verification and anti-rollback | Gate A, B, C |
| H1215-C05 | H + I | Real origin transport receipt and raw-byte verification; production H P0 digest/signature and immutable integrity record; no test-double-only evidence | Gate B, C |
| H1215-C06 | H + I + Storage | Durable replay identity/result reservation, crash recovery, same-message recovery, ambiguous commit UNKNOWN, current authorization and D Forget-fence checks before replay disclosure | Gate B, C |
| H1215-C07 | Storage + C + I + A | Successor exact-version manifest binding H 1.2.15 and exact C/I reviews; then fresh D/Storage/A exact-bundle review | Gate A, B, C |

Every condition remains OPEN. No deadline is invented: each closes only on the specified evidence being published and exact-version read back. Delegated role reviews are not independent human Owner signatures.

## 5. Disposition and allowed scope

**A disposition: DEFERRED.** H 1.2.15 may continue as a non-production reference candidate and may be used for synthetic conformance testing. It is not jointly accepted, not frozen, not production-ready, and not authorized for production ingress. Storage v3.3.2 remains the current pinned manifest and continues to bind 1.2.14.

Do not:
- claim C/I production trust registration or Owner approval;
- treat injected test callbacks as real authority services;
- infer issuer-side signing-order correctness from receiver-side verification tests;
- transfer 1.2.14 CI/review evidence to 1.2.15;
- publish a successor manifest as accepted before exact H/C/I closure;
- advance Gate B/C, merge PRs, close Issues, or authorize production.

The next execution should be H exact-bundle publication and issuer-side closure, followed by C exact executable/CI review, I exact trust/registration review, Storage successor manifest, and A exact-bundle rereview.


## Publication boundary clarification — 2026-11-18

This PR publishes the review record itself. Any statement above that says not to merge PRs refers to merging the H 1.2.15 implementation/candidate as an approved or production-ready change. It does not prohibit publication of this non-normative audit artifact. Merging this documentation PR does not close any finding, authorize a protected operation, freeze a schema, advance a Gate, or approve production use.