# Phase 3.9.0 — A Integration Review: CSubmitOutcome 1.0.0, H Validator and CI Evidence

- Owner perspective: A — Principal Integration Architect
- Scope: immutable C outcome object schema, C signature projection, I crypto governance review, H wire mapping/validator core, C/H executed structural CI, Storage exact binding.
- Disposition: **ACCEPT DESIGN + STRUCTURAL/SEMANTIC CI; DO NOT FREEZE**
- Provenance: delegated A-role simulation at user's direction; not independent human A Owner approval.

## 1. Exact evidence set

| Owner | Artifact | Exact Blob | Review |
|---|---|---|---|
| C | CSubmitOutcome 1.0.0 schema | `b5e87fa8df8463cf4cdc1ebc6867e643dcf5924c` | Closed Draft 2020-12 object; exact attempt tuple |
| C | 10 structural/semantic vectors | `e14eab2bed41f30af10a073b8e6523512128e78e` | Synthetic; signature placeholders |
| C | Phase 3.8.8 signature projection | `06d9264124d85896ccd44ef7789d9af245d8255b` | Candidate P0 and domain-separated preimage |
| C | Phase 3.8.9 schema/conformance contract | `7939c84e950b50f3ec44e4e2fbe5e7f93e544c2e` | CI evidence bounded correctly |
| I | Phase 3.8.6 crypto binding review | `a4d0be0e5bbf6122e2d86e59a48e62586869fd23` | Structural binding accepted; profile not registered |
| H | Validator core | `e8f737326bc4791e8d7acf917b4725dbb7171fad` | Fail-closed core; external callbacks injected |
| H | Phase 3.8.6 wire mapping | `248ded774fcc5504289636daa39a50d5f17b0d62` | Exact duplicate and external proof disposition |
| H | Phase 3.8.5 validator contract | `9152cff0564446f27c29d14e02b1532b0ebe7c9d` | Semantic validation and INVALID/UNKNOWN rules |
| H | H unit/fixture tests | `1f17bdcef6004eca165644ce96bcf35d3b10c3f8` | 7 tests, CI executed |
| Storage | Current exact version manifest | `6d6140bb83b5ea336470223eff72b0edaf16faaa` | Current C/H/I/A pins recorded |

## 2. Integration findings

### 2.1 Immutable object boundary — ACCEPT

C now has a separate immutable `CSubmitOutcome` object schema, distinct from the BMCP envelope. The object contains the gate and attempt generations, provider/account/adapter/endpoint/region/API operation, idempotency namespace/key, exact request boundary/digest, C admission/ledger position, outcome/evidence, COC intent/reservation pair, owner signature reference and crypto metadata.

The 1.2.11 BMCP envelope remains a transport/protocol projection. H must dereference `c_submit_outcome_ref`, verify the digest, validate the C object schema and compare every duplicated inline field. This resolves the previously identified missing-inline tuple fields without pretending they are present in the envelope.

### 2.2 Outcome semantics — ACCEPT AS DESIGN

The five outcomes remain distinct. NOT_INVOKED requires durable no-handoff proof. HANDOFF_REJECTED does not imply no side effect. UNKNOWN/IN_DOUBT remain nonterminal and cannot authorize retry-as-new-operation. COC intent/reservation is a complete pair or explicit null pair plus reason; C owner-local admission remains mandatory either way.

### 2.3 H mapping and authority boundaries — ACCEPT WITH CONDITIONS

H's map covers the duplicated C-owned fields, including provider request/receipt/lookup/no-handoff refs, unknown reason, owner signature ref, actual inference request ID and COC intent/reservation aliases. Independent COC commit/record/position, prepared participant, I terminal, D clearance, participant ledger and Storage proof fields remain external evidence and are delegated to authenticated COC/owner authority callbacks.

A confirms this separation: C must not sign or assert I/D/Storage/COC facts as C-owned truth; H must not ignore those envelope proofs; callbacks must authenticate each authority independently.

### 2.4 Validator core — ACCEPT AS INTEGRATION INTERFACE

The H validator core:
- strictly parses raw UTF-8 JSON with duplicate-key and non-finite rejection;
- validates envelope and immutable object schemas separately;
- recomputes the candidate C-P0 digest;
- compares duplicated wire fields with the immutable object;
- applies local outcome/COC/high-water predicates;
- uses tri-state authority callbacks for profile registration, C signature/key status, provider evidence, C owner ledger, COC joins and anti-rollback/currentness;
- returns INVALID on contradiction, UNKNOWN on unavailable authority evidence, and VALID only if every required check returns true.

This is an integration core, not a production-connected validator. The callbacks are not wired to deployed authority stores, key registries, provider evidence systems, C ledgers or COC.

## 3. Executed evidence reviewed

### C CI

- Run: `44055965702`
- Commit: `a0c197fa94e71c52758fadaa335a686815485dd7`
- Result: SUCCESS; 3 tests.
- Scope: JSON Schema self-validation, ten synthetic expected-result vectors, explicit placeholder-signature/profile-not-registered assertions.

### H CI

- Run: `44055791045`
- Commit: `7d5c7324cabde76d99df49c55220219a491e03c0`
- Result: SUCCESS; 7 tests.
- Scope: duplicate JSON key rejection, malformed UTF-8/non-finite rejection, digest/preimage message-type binding, owner high-water semantic predicate, missing-callback fail-closed check, and all ten vendored C schema/vector cases.

These are genuine executed CI runs. They do not constitute cryptographic signature verification, profile registration, provider proof authentication, ledger membership, COC quorum, adapter race testing or production readiness.

## 4. Remaining freeze blockers

| Gate | Required evidence | Status |
|---|---|---|
| I C profile registration | Registered `AIMBA-C-CRYPTO-1.0`, C trust root, key-status ledger and lifecycle approval | OPEN |
| C crypto vectors | Real test-only Ed25519 key, exact JCS bytes/digest/preimage/signature, positive and negative vectors | NOT RUN |
| Independent C crypto interop | Python and JavaScript verifier agreement, pinned runtime/build/CI logs | OPEN |
| H crypto implementation | Strict Base64url decoding, Ed25519 verification, trust chain and anti-rollback integration | NOT CONNECTED |
| C owner ledger | Append-only durable record inclusion/currentness and restore evidence | OPEN |
| C provider adapter | Gate close/send races, crash windows, partial write, lost ACK, same-key lookup, expiry, failover and hidden retry tests per provider | NOT RUN |
| COC/Storage deployment | Durable quorum/Batch/Manifest/owner-ledger joins and readback | OPEN |
| A freeze review | Re-review exact registered profile, executable crypto/adapter evidence and deployment proof | NOT GRANTED |

## 5. Non-negotiable invariants

1. INVALID dominates UNKNOWN when a contradiction is proven.
2. Missing authoritative evidence is UNKNOWN, never success.
3. UNKNOWN/IN_DOUBT cannot release gates or authorize a new provider operation.
4. A valid signature authenticates an assertion; it does not prove the provider actually performed the claimed side effect.
5. No COC quorum, I authorization, D clearance, Storage commit, H ACK or G Applied record can synthesize provider handoff truth.
6. No exactly-once or production-readiness claim without provider-specific executed evidence.

## 6. Final decision

**ACCEPT DESIGN AND THE TWO BOUNDED STRUCTURAL/SEMANTIC CI RUNS. DO NOT FREEZE.**

The immutable C object, H dereference design and cross-owner proof boundaries are coherent at the design level. C and H structural/semantic tests pass at their exact pinned commits. The C crypto profile remains unregistered, all fixture signatures remain placeholders, H authority callbacks are not production-connected, and provider adapter/COC/Storage deployment evidence is absent.

This review authorizes no production provider egress, Full Applied, Global Forget Completion or universal exactly-once behavior. All Owner decisions are delegated role simulations, not independent human Owner signatures.
