# C/G/H Successor-Boundary Review — Applied ACK vs Provider Outcome 1.2.15

- Date: 2026-11-17
- Review mode: coordinated delegated C/G/H specialist-role review; **not independent human Owner signatures**
- Repository: `oahcom/AiMemoryBrainArchitecture`
- PR context: #28 remains Draft/Open; this report does not authorize merge or activation.
- Scope: exact current H Unified 1.2.15 schema candidate, C schema-shape review, G's current consumer pin, C Provider Submit Outcome semantics, and separation from the JF-10 Applied ACK schema family.

## 1. Exact source pins re-read

| Artifact | Branch / path | Exact Blob SHA | Current status |
|---|---|---|---|
| H Unified 1.2.15 schema | `session-h-bmcp-protocol` / `08-bmcp-protocol/schemas/bmcp.coc-jf10-unified-1.2.15.schema.json` | `860fc4cec658db7d2703cd6adf72aa31a2723f6d` | Exact candidate schema read back |
| H 1.2.15 mapping addendum | `session-h-bmcp-protocol` / `08-bmcp-protocol/phase-3.8.21-h-exact-schema-mapping-unified-1.2.15-gateway-attestation.md` | `2dc30f193d9c4f4bdc05ca4c137103687db28924` | Candidate mapping note; superseded by later code/CI evidence below |
| H 1.2.15 C validator | H branch / `08-bmcp-protocol/validators/provider_outcome_validator_1_2_15.py` | `90a2d4b6f5b05590e3e0a7daecb5a01d9bf525c0` | Local C-object/schema/semantic validator; authority callbacks required |
| H 1.2.15 gateway validator | H branch / `08-bmcp-protocol/validators/gateway_attestation_validator.py` | `9cc426d4c26deb452f39daff34c1008dd535e969` | Gateway-attested ingress/replay validator; production seams callback-injected |
| H 1.2.15 gateway tests | H branch / `08-bmcp-protocol/tests/conformance/provider_outcome/test_gateway_attestation_validator.py` | `9a5051b001a6e59d7b71e6dd175e84bb7d01d252` | 21 deterministic unit/fixture tests |
| H workflow (before fix) | H branch / `.github/workflows/h-provider-outcome-conformance.yml` | `4459d19f5b4eea058377d9819e48e81eed5c8c4b` | Stale 1.2.14-only path filters; superseded |
| H workflow (corrected) | H branch / `.github/workflows/h-provider-outcome-conformance.yml` | `2ad679952ce5499a16c8fffa0a1543e26460e6eb` | Includes 1.2.15 schema, both validators, envelope validator, test paths and workflow |
| H exact CI (pre-fix) | Run `44078755981`, commit `e3e4cab0aab2c68f9db98bd50bc387b1895c3773` | — | SUCCESS; 91 tests total, including 21 H 1.2.15 gateway tests |
| H exact CI (post-fix) | Run `44079842914`, commit `0d36324457e39bd50ad56ae902d477c4ea765b61` | — | SUCCESS; 91 tests total, including 21 H 1.2.15 gateway tests; callback fixtures are deterministic test doubles |
| C 1.2.15 schema review | `session-c-agent-integration-2026-11-16` / `07-agent-integration/phase-3.8.26-c-exact-review-h-unified-1.2.15-gateway-attestation-schema.md` | `c5ff68814be49ec5e6e2c081004e7fa058d276fa` | Delegated C-role accepts schema shape with conditions |
| G Applied source | `session-g-memory-context` / `06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md` | `aa3afa73d8a76cc6f025839c52bfbff6a983046a` | G-owned semantics; persistence implementation not verified |
| G exact full-path consumer review | `session-g-memory-context` / `06-memory-context/phase-3.8.18-g-exact-review-h-unified-1.2.14-csubmitoutcome-1.0.1-fullpath.md` | `1894860c76336f8739d354b72beed3992cffd17e` | Explicitly pins H 1.2.14 × CSubmitOutcome 1.0.1 |
| C normative Provider Submit Outcome | `session-c-agent-integration-2026-11-16` / `07-agent-integration/phase-3.8.4-c-normative-provider-submit-outcome-contract.md` | `819705037da89834e10b6dd2ec6e66c1b8c70886` | C semantic authority |
| CSubmitOutcome 1.0.1 schema | C branch / `07-agent-integration/schemas/c-submit-outcome-1.0.1.schema.json` | `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda` | Immutable C object schema |
| H JF-10 Applied ACK schema | H branch / `08-bmcp-protocol/schemas/bmcp.applied-ack-1.1.0-jf10-bridge.schema.json` | `a8a945cc3623c2907003b93625e3c79742150944`; distinct schema family | JF-10 bridge Applied ACK, not Provider Outcome |

The exact branch heads observed during this read were C `71047cdb51139ca4080ac67f451e38a48698859d`, G `3367438f7b6ba5fa1b7d7540a0fd03a72bbebdbe`, and H `e3e4cab0aab2c68f9db98bd50bc387b1895c3773`.

## 2. Version boundary: 1.2.15 is not yet a G-accepted consumer pin

H 1.2.15 is an immutable successor candidate for the Unified wire family (wire family remains 1.3.0). Its Provider Outcome branch adds conditional origin-transport receipt/digest, raw-ingress-byte digest, H signing-profile and sequence evidence. The H branch now contains both `provider_outcome_validator_1_2_15.py` and `gateway_attestation_validator.py`, plus a 21-test gateway-attestation suite. Exact H CI run `44078755981` on commit `e3e4cab0aab2c68f9db98bd50bc387b1895c3773` completed SUCCESS with 91 tests total, including those 21 1.2.15 gateway tests. This corrects the earlier mapping note's then-current statement that no validator/CI claim existed.

The test fixtures use deterministic callback doubles for protected transport, H/C signature/profile/key status, origin receipt, durable ingress/replay and owner-authority seams. The run is meaningful local candidate validation, but it does not establish production trust roots, real I registry/delegation, live owner ledgers, durable deployed replay storage, provider truth or production ingress.

The stale workflow was corrected on the H branch: its revision description now distinguishes 1.2.14 compatibility from 1.2.15 gateway-attested conformance, and its path filters include the 1.2.15 schema, both 1.2.15 validators, envelope-auth validator, conformance tests and workflow file. The corrected workflow was read back at Blob `2ad679952ce5499a16c8fffa0a1543e26460e6eb`; exact post-fix run `44079842914` on commit `0d36324457e39bd50ad56ae902d477c4ea765b61` completed SUCCESS with 91 tests, including 21 1.2.15 gateway tests. The CI trigger-wiring P1 is closed for these paths.

C's exact review accepts the 1.2.15 **schema shape only**, subject to C-owned semantic conditions, and predates the current validator/CI evidence. C must now review the exact 1.2.15 validator/test/CI pins. Among other conditions, H must authenticate the origin receipt, bind the original Adapter identity to the immutable C object, verify raw-byte digest, verify H and C signatures independently, enforce exact duplicated-field equality, and preserve C UNKNOWN/IN_DOUBT as nonterminal.

G's current Phase 3.8.18 full-path review remains pinned to H Unified 1.2.14 and CSubmitOutcome 1.0.1. It cannot be carried forward to 1.2.15 by implication. G must review the exact 1.2.15 schema, validator, fixture and CI artifacts before accepting that successor as a G Applied consumer input.

**Disposition:** H 1.2.15 = schema candidate; C = schema-shape acceptance with conditions; G = no 1.2.15 consumer acceptance evidenced. Cross-owner 1.2.15 full-path acceptance = OPEN.

## 3. Do not conflate Provider Outcome with Applied ACK

Two distinct message/evidence families are present:

1. **C Provider Outcome carried through H Unified**: CSubmitOutcome 1.0.1 is the immutable C-owned semantic object. H authenticates and validates the transport/envelope and exact object join. C remains the sole authority for provider handoff truth.
2. **BMCP Applied ACK 1.1.0 JF-10 bridge**: a separate schema family used for JF-10 bridge/Prepared-GID and Applied-boundary evidence.

The second is not the wire representation of the first. A successful H gateway attestation for C Provider Outcome does not itself create G Applied. Likewise, a JF-10 bridge Applied ACK does not prove provider handoff, G Applied persistence, or global Forget completion. The exact message family, schema artifact revision, immutable object reference and owning authority must remain explicit in every consumer contract.

## 4. Idempotency is at least three separate layers

### 4.1 C provider-attempt idempotency

C's normative contract defines a stable ProviderIdempotencyKeyRef for one logical provider attempt, scoped to provider/account/endpoint-model semantics and immutable RequestDigest. Resolving an uncertain handoff must reuse the same key and request digest; it is reconciliation of the same attempt, not a new send. UNKNOWN/IN_DOUBT blocks retry-as-new. Providers without authoritative same-key lookup cannot support an exactly-once claim.

### 4.2 H envelope/evidence replay and conflict handling

H must authenticate the exact C object and enforce duplicated wire/object equality, origin receipt and raw-byte integrity, signing-sequence/key-status linkage, and durable replay/currentness checks. H now has a local gateway validator and tests for exact revision, required origin fields, raw-byte digest, H/C signature separation, replay conflict, same-digest replay authorization and fail-closed UNKNOWN. The tests exercise callback contracts with deterministic doubles; they do not authenticate production authorities. H envelope replay identity (message identity/nonce + H P0 digest and durable prior-result reference) is distinct from G Applied commit idempotency.

### 4.3 G Applied commit idempotency

G's source contract says Applied is committed by exact request/attempt/evidence identity: same identity plus same digest returns the original disposition; same identity with changed digest is conflict/quarantine; late evidence cannot roll back a newer ContextVersion or Delivery attempt.

However, the current G source and 1.2.14 consumer review do not yet establish a fully pinned durable Applied persistence key/transaction contract that explicitly joins:
- the stable H evidence identity (digest compared as content, not silently folded into identity);
- CSubmitOutcomeRef + immutable C object digest and the exact provider attempt/request tuple;
- COC transaction / participant / reservation identity where applicable;
- G ContextVersion + DeliveryAttempt + InferenceRequestId + FinalRequestBoundaryId;
- the durable G Applied record key, uniqueness constraint, transaction boundary, duplicate-return behavior, changed-content conflict behavior, crash recovery and restore/replay behavior.

This is a **G-owned persistence-contract gap**, not a reason to change C provider idempotency semantics. The provider-attempt key, H evidence/replay identity and G Applied commit key must be distinct typed identities with explicit crosswalks.

## 5. Required closure work

| Priority | Owner | Required next artifact / proof | Gate |
|---|---|---|---|
| P1 | H | Obtain C's exact review of validator/test/CI pins; replace callback doubles with production-authority integration evidence before production claims | Workflow path wiring is corrected; H 1.2.15 remains candidate; local test pass is not production conformance |
| P1 | G | G Applied persistence/idempotency addendum defining durable key, uniqueness scope, exact C/H/COC crosswalk, same-digest replay, changed-digest conflict, supersession, crash recovery and restore fencing | No G persistence PASS before implementation/evidence |
| P1 | G + C + H | Exact 1.2.15 consumer matrix: each owner accepts the same immutable schema/mapping/validator/fixture/CI set; no predecessor-pin inheritance | No 1.2.15 full-path acceptance until exact decisions |
| P2 | C/H/G | Preserve distinct typed identifiers for ProviderIdempotencyKeyRef, H envelope/evidence identity, CSubmitOutcome identity and G Applied record identity; specify only the necessary equality/correlation edges | No cross-layer identity collapse |
| P2 | D/I/Storage/COC | Continue independent authority proof and recovery/restore acceptance; H or G must not self-assert those authorities | Production activation remains blocked |

## 6. Review disposition

- Six-stage lifecycle and authority separation: **SEMANTICALLY ALIGNED**.
- C Provider Outcome semantics and same-key uncertainty handling: **SPECIFIED; production provider truth/idempotency NOT VERIFIED**.
- H Unified 1.2.15 schema and local validator path: **CANDIDATE; 21 gateway tests included in 91-test H CI run SUCCESS; C exact validator/CI review still required; production authority seams NOT VERIFIED**.
- G consumer acceptance of H 1.2.15: **NOT EVIDENCED**.
- G Applied durable persistence/idempotency implementation: **NOT VERIFIED**.
- Applied ACK JF-10 bridge vs Provider Outcome distinction: **MUST REMAIN EXPLICIT**.
- Global C/G/H Applied contract freeze: **NO**.
- Production provider egress / activation: **NOT AUTHORIZED**.
- PR #28: **Draft/Open; no merge authorization**.

This report records a coordinated delegated technical review only. It does not alter any Owner decision, transfer approval from a predecessor Blob, or claim independent human Owner sign-off.
