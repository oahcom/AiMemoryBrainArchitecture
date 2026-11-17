# C/G/H Cross-Owner Contract Consistency Review — Corrected Current Baseline

- Date: 2026-11-17
- Review: independent cross-owner audit, corrected after reading the separate exact-version Owner addenda, current H full-path closure and current C/G role reviews.
- PR #28 remains Draft/Open.
- This version supersedes the earlier same-path report. The earlier audit had false-positive gaps because it initially read only the base C/G/H contracts and missed the separate exact-version C addendum, H schema/mapping decisions and later full-path artifacts.

## 1. Exact current evidence baseline

| Authority | Artifact | Exact Blob / evidence |
|---|---|---|
| C exact CGH-APPLIED-1.1 recovery-batch acceptance | C Phase 3.6 C-submit / I / D causal-order addendum | 45a48249717c8cddb07ab96197730ef93d406c22 |
| C normative provider outcome semantics | C Phase 3.8.4 normative Provider Submit Outcome contract | 819705037da89834e10b6dd2ec6e66c1b8c70886 |
| C immutable object schema | CSubmitOutcome 1.0.1 JSON Schema | a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda |
| C current full-path review | C Phase 3.8.19 review of H 38-test closure | 24337b79cfea6264a8a6f11fa414578fc559716c |
| H wire schema | Unified 1.2.14 / wire 1.3.0 | 09fcd1fa29fe24255fbd87cae79dafb406594a59 |
| H authority-join mapping | H Phase 3.8.10 / integrated mapping | 579dd2a91edf47b86e744e897ba6668b839944bd / 1cbe74eba69325510d6b1019d971661f965eabf8 |
| H full-path validator/test/fixture | Validator / test / fixture | eab961a08d41e871f38543b18ee60cf024977414 / 540056d7c4f290c31290b17c264c69cfd76b1cb2 / c80247a6ecfbb4a29ff0993e8e2aea4829d00626 |
| H full-path closure | H Phase 3.8.14 | cda025fb157815570b3280fa5ff168d5e62453b1 |
| H exact CI | Run / commit / job | 44070924346 / 77a9d5e2e716ba33387f0beb1195f864ed8ac54f / 133996627914 SUCCESS |
| G current consumer review | G Phase 3.8.18 delegated review | 1894860c76336f8739d354b72beed3992cffd17e |
| G Applied source | G Phase 3.6 Applied / Forget contract | aa3afa73d8a76cc6f025839c52bfbff6a983046a |

Supporting candidate schemas include H RecoveryCutoff 1.0.5 (Blob 75cd1fedefd50a6ed570b5afaa2d1f9cc4c6a4c7) and RecoveryJoin 1.0.2 (Blob 4b664e3bce465499bcdfd93796349a4ba7074002). These remain separate schema families and do not replace H Unified 1.2.14 or CSubmitOutcome 1.0.1.

## 2. Corrected disposition

**C/G/H design-level consumer mapping: ACCEPTED WITH ENUMERATED CONDITIONS at the delegated L1/L2 level; NOT FROZEN.**

The earlier P1 claims that C had no exact 1.1 recovery-batch decision or no CSubmitOutcome object contract were incorrect. C's separate Owner addendum accepts the exact A/COC recovery-batch pair with enumerated exceptions; C's normative Provider Outcome contract and 1.0.1 schema define the immutable C-owned provider outcome. C explicitly retains provider-specific same-key idempotency and crash recovery as unverified conditions.

The earlier claim that H had no concrete schema was also too broad. H has Unified 1.2.14 / wire 1.3.0, exact C object mapping, a full local H-envelope + C-object validator path, and a documentation-derived JSON Schema candidate. H's full-path run now reports 38 methods: 32 H validator unit/fixture methods plus six C crypto-interoperability methods. The exact provider-outcome job passed on the pinned commit.

G has now issued a delegated G-role consumer review of the exact CSubmitOutcome 1.0.1 × H Unified 1.2.14 mapping, preserving G's exclusive Applied authority and specifying the Outcome × SideEffectStatus mapping. This is not an independent human G Owner signature.

## 3. Cross-owner semantic checks

| Concern | Current result | Boundary |
|---|---|---|
| C provider outcome and side-effect semantics | PASS at contract/schema level | C owns immutable outcome; Outcome and SideEffectStatus are separate |
| H wire mapping and full local validator path | PASS at L1/L2 candidate level | Exact schemas/object joins/digest/negative mutations are tested locally |
| G Applied consumption | ACCEPT WITH G-OWNED CONDITIONS at delegated review level | G alone decides Full Applied and current-use projection |
| I/D/Storage/COC authority separation | PASS as interface architecture | Test callbacks are not production authority verification |
| Historical Applied vs current-use | PASS at contract level | Later revocation/fence invalidates current-use without rewriting valid history |
| Forget/late work/unknown ordering | FAIL CLOSED by contract | Unknown or missing proof cannot promote Applied or release barriers |
| Execution Started/model use/completion | Separate evidence families | Provider acceptance does not prove execution or model attention |

Important digest distinction: C RequestDigest binds the full immutable final request; G Managed Region digest/inventory binds the complete managed memory region; C object digest and H envelope payload digest are further distinct scopes. They must be joined to the same request but must not be conflated or assumed equal.

## 4. Findings — updated status

### XCH-36-001 — C producer evidence contract
**CLOSED at L1/L2 contract-definition level.** C exact recovery-batch decision, normative CSubmitOutcome contract and 1.0.1 schema are now pinned. **Still OPEN for provider-specific same-key lookup/idempotency, crash/restart/failover recovery and real provider issuer truth.**

### XCH-36-002 — H wire/schema/full-path mapping
**CLOSED at L1/L2 schema/validator-candidate level.** H Unified 1.2.14, CSubmitOutcome 1.0.1 mapping and 38-method full-path CI are pinned. **Still OPEN for production schema/IDL generation, production trust/key governance, live authority callbacks and interoperability/deployment.**

### XCH-36-003 — Exact-version C/G/H consumer acceptance
**CLOSED at delegated technical-review level with explicit limits.** C and H exact mapping reviews exist; G Phase 3.8.18 accepts the same exact C/H mapping within G's authority. **Independent human Owner signatures and global freeze are not established.**

### XCH-36-004 — Cross-authority ordering and digest namespace
**CLOSED at reviewed design level.** COC, I, D, Storage, C request, Managed Region and H envelope digest/position domains remain distinct; no local clock, receiver sequence or unrelated authority cursor may substitute for the required owner proof. Keep the exact version pins; do not merge or compare opaque positions across authorities.

### XCH-36-005 — Runtime and production evidence
**OPEN.** L1/L2 local full-path tests passed, but all ten authority callbacks in the positive fixture are deterministic test doubles. No production trust root, live C sequencer/key-status ledger, provider truth/same-key lookup, live I/D/Storage proof verification, COC quorum durability, Storage same-GID physical recovery, G Applied persistence, multi-replica egress serialization or production deployment is proven. G adversarial race/reconnect/replay/restore suites remain SPECIFIED / NOT RUN.

## 5. Remaining production gates

1. I governance trust-root/profile registration, C key lifecycle, HSM/KMS custody, key rotation/revocation and anti-rollback.
2. Provider-specific authoritative idempotency and same-key lookup, including crash/restart/failover and no retry-as-new after ambiguous handoff.
3. Live I/D/Storage authority verifiers and proof-currentness joins; no test-double substitution.
4. Named COC operator, durable quorum/participant registry, outage recovery, restore and high-water proof.
5. Selected Storage topology and physical same-GID prepared/commit/rollback, visibility/non-publication and restore guarantees.
6. G Applied durable persistence/validator implementation and L3/L4 adversarial conformance.
7. Independent human Owner/governance approval, shared release manifest and production authorization.
8. Multi-PolicyDomain atomicity remains BLOCKED / NOT ACCEPTED.

## 6. Final gate

- C/H L1/L2 local full-path validation: **PASS**.
- G L1/L2 consumer review: **ACCEPT WITH ENUMERATED CONDITIONS (delegated role review)**.
- C/G/H global Applied contract frozen: **NO**.
- Production authority integration: **OPEN / NOT VERIFIED**.
- G Applied runtime/persistence: **NOT VERIFIED**.
- L3/L4 end-to-end conformance: **NOT RUN / OPEN**.
- Production activation / provider egress authorization: **NOT AUTHORIZED**.
- PR #28: **Draft/Open; no merge authorized**.

This corrected review does not claim global Forget completion, physical erasure, provider exactly-once, model attention, or production readiness.
