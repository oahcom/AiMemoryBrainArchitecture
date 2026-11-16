# Session F — Phase 3.5 Reprocessing Change Log

- Owner: Session F — Memory Runtime Principal Architect
- Repository: `oahcom/AiMemoryBrainArchitecture`
- Branch: `session-f-memory-runtime`
- Reprocessing base HEAD: `8b16a3621cbe2be4badac1799822b64824532b25`
- Review baseline: `main@8a6414158c9c056c1638222534e1993d1bbc99d2`
- Status: **F consumer documentation reprocessed; runtime and cross-owner conformance OPEN / NOT RUN.**

## 1. Current dependency branch heads read

| Owner | Branch | HEAD SHA | Disposition consumed |
|---|---|---|---|
| D | `session-d-memory-brain-2026-11-16` | `da8e5882d0b238d765d00b2225b79eea45a483b1` | Canonical cursor and Forget fence semantics decided; operation semantics explicit; API/schema and Storage atomic realization OPEN |
| E | `session-e-memory-compiler-2026-11-16` | `c2f14408ba62447c11172d65b93a279fef96d175` | Candidate producer/derived publication enforcement; D/E/Storage gate remains OPEN |
| I | `session-i-security-governance-2026-11-16` | `5591ad3620ec3f5d74194bd79556dcf3e25bea07` | Candidate PermissionEpoch, sealed target inventory and global Forget evidence vector |
| G | `session-g-memory-context` | `3d2c065be863bc1d349faaeece6f6eaa0047abae` | ContextVersion/reconciliation/delivery remain G-owned |
| H | `session-h-bmcp-protocol` | `1ee65928f123d92a4758b0de09bc8d6df1e46253` | Reprocessed candidate identity/ACK/reconnect contract; B/C/D/G/I approvals OPEN |
| C | `session-c-agent-integration-2026-11-16` | `35de58ddc93c5f1e554596cdfc430cd6c392d355` | Final immutable inference request boundary; F cannot claim Applied |
| B | `session-b-domain-model-phase3` | `66adf6bdcf5ec69a146fe75afe20ce3b85af8448` | Typed ActorRef/ScopeRef semantics candidate; not credentials or grants |
| F | `session-f-memory-runtime` | `8b16a3621cbe2be4badac1799822b64824532b25` | Reprocessing base; this commit series advances F only |

The cross-module Phase 3 D/E/H/I review was read from main at the exact baseline above. It is a Conditional Pass for continued integration, not contract freeze or implementation sign-off.

## 2. F-owned files updated

- `05-memory-runtime/retrieval-engine.md`
- `05-memory-runtime/working-set-and-cache.md`
- `05-memory-runtime/runtime-overview.md`
- `05-memory-runtime/phase-3.5-forget-suppression-and-cursor-consumption.md`

Only F-owned paths were modified.

## 3. Reprocessing findings

1. Replaced stale statement that D/E contracts were absent.
2. Added D ProducerRegistrationSequence/HighWater and RegistrationReceipt as a separate typed consumer concern; it is not CanonicalCommitCursor, ForgetFenceGeneration, PermissionEpoch or IndexWatermark.
3. Aligned F rebuild/backfill/replay with D semantic operations: RegisterProducerClass, RegisterProducerWork, RegisterDerivedDependency, PublishDerivedIfFenceCurrent, CompleteProducerWork, ResolveProducerWork and ReconcileForgetBarrier. These are semantic operations, not claims of callable APIs.
4. Preserved the blocking D/E/Storage question: callable API/schema and transaction/CAS or equivalent recoverable visibility gate remain OPEN; F keeps staged index generations private/quarantined if unavailable.
5. Bound F local invalidation evidence to I-owned TargetId/seal only when supplied by I; F reports per-partition/cache/Working Set evidence and never decides global completion.
6. Kept IndexWatermark partition-local, contiguous and tied to D CanonicalCommitCursor; no cross-partition scalar and no Forget proof.
7. Clarified cache/Working Set behavior: F-local invalidation generation only; current I PermissionEpoch and D fence are revalidated; lost/gapped notification quarantines until reconciliation; reconnect authenticates and reconciles before restore.
8. Retained ActivationRecommendation as advisory only; G owns ContextVersion and H/C own application/final-request evidence.

## 4. OPEN items

- D/E/Storage callable operation schemas, shared linearization and atomic/recoverable visibility protocol — BLOCKING.
- E source baseline still cites an older D HEAD in its detailed contract; E should reconcile it to D current owner contract.
- I PermissionEpoch currentness/fan-out, target inventory feed/seal and per-target evidence acceptance — OPEN.
- G F-consumer envelope and reconciliation trigger schema — OPEN.
- B/I/H identity and typed ScopeRef/ActorRef binding approvals — OPEN.
- ANN backend pre-filter, cancellation/final-return race, cache/reconnect, index replay and performance thresholds — TO_VALIDATE.
- H Adapter ACK and C Full Applied evidence are not F proof and remain downstream.

## 5. Conformance and test status

The ten F35 cases remain normative test specifications: F35-01 through F35-10 (fence race, permission revocation, stale cache, old-data rebuild, lagging watermark, late derivative, cross-Scope candidate, reconnect old Working Set, duplicate invalidation, one lagging partition).

**Static contract review and repository read-back only.** Runtime conformance, concurrent race tests, fault injection, cache-loss/reconnect tests, ANN pre-filter tests, rebuild/replay tests, security tests and performance benchmarks were **NOT RUN / NOT CLAIMED**.

## 6. Write commits

- `05-memory-runtime/retrieval-engine.md` — commit `10f811af37b95e08f6b62a41101ed3831d478916`, blob `1fbfc0ff07b66c0ff68c3cea5271261c9d7fc0af`
- `05-memory-runtime/working-set-and-cache.md` — commit `5baf6d1c8ed921ecca85e73f41697770c786fc36`, blob `a934491950c876701e8ac592a0e6aaea983b44e3`
- `05-memory-runtime/runtime-overview.md` — commit `b704baffe30b8eba0273bbcf0f4bc0c99490143f`, blob `b7a948f014c3ad882a35a18bfc8ce025b26ab85a`
- `05-memory-runtime/phase-3.5-forget-suppression-and-cursor-consumption.md` — commit `f08dec0cb2af2104157fa544bb605b2176373ee3`, blob `5f657909734c530e8c6611d16c0cab7057e21db2`
