# Context Optimization — System Conformance Plan

- Owner: A — integration test governance
- Status: PROPOSED; NOT RUN; no implementation certification.
- Rule: security/Forget tests are mandatory gates, not optional benchmarks.

## 1. Test ownership

| Test family | Primary | Partners | Required evidence |
|---|---|---|---|
| Archive capture/immutability/read/cursor/completeness | F | B, I, D, Storage | exact hashes, manifests, page receipts |
| Context selection/version/TSS/compaction/fidelity | G | B, C, D, F | ContextVersion, staged/commit, validator reports |
| Canonical registration/publication/Forget | D/E | F, G, I, Storage | registration/barrier receipts, gate traces |
| Principal/scope/PermissionEpoch/revocation | I | B, C, H, D, F, G | policy decisions, epochs, negative traces |
| BMCP Recall/ACK/reconnect | H | C, F, G, I, D | authenticated envelopes, delivery IDs |
| Final request boundary/protected regions | C | G, H, I | immutable request digest and boundary evidence |
| Cursor/watermark type safety | D/F/G/H | A, B | typed token traces and negative tests |
| Storage crash/restore/PITR | Storage | D, E, I, F, G, H | WAL/restore logs, fence readback, quarantine |
| Paired experiments | A | C, F, G, H, I | frozen config and per-task results |

Each test records repository, branch/commit, build digest, test ID, seed, exact config, model/provider, hardware, opaque authority refs, trace IDs, expected/actual result and reviewer.

## 2. End-to-end nominal tests

1. Capture large tool observation under authenticated principal/trusted scope. F registers eligible work, checks I permission and applicable D fence, stores immutable bytes/manifest and returns locator. Exact reread hash matches.
2. G issues bounded RecallIntent. F opens session, checks I epoch and D fence, returns excerpt/receipt/completeness. G validates and stages Context reference.
3. G commits ContextVersion by CAS. Verify F did not mutate Context and F/G did not mutate canonical Memory/index.
4. G runs boundary compaction; records economics, TSS, fidelity and lineage/loss. Commit only after hard checks and D/I gates.
5. H delivers exact target; Adapter applies only managed region at future inference boundary. C proves exact final request submission; G records Applied only after validating required owner evidence.
6. Change source revision, expire Archive, revoke permission and issue Forget. G marks reference stale/suppressed; H blocks future use.

## 3. F Archive tests

- Immutable revision cannot change bytes/hash; changed bytes require new revision/lineage.
- One read session never mixes source revisions.
- Hash mismatch, truncated blob, malformed page map and invalid encoding fail closed.
- Range reads are exact and bounded.
- Cursor binds session, object, revision, hash, selector and coordinate system.
- Cross-session/object/revision/scope/selector cursor reuse rejected.
- EOF terminal; timeout, partial page, budget exhaustion and index gap explicitly PARTIAL/UNKNOWN.
- Completeness reports omissions, stale indexes, omitted channels and budget use.
- F does not implicitly summarize or mutate Context.
- F catalog never masquerades as E canonical index; ANN only after measured approval.

## 4. Concurrency, crash and recovery

Every test records linearization point, stable idempotency/work key, D registration/barrier position, D fence, I PermissionEpoch, source revision, visibility gate, terminal disposition and recovery evidence.

| Race/fault | Required test |
|---|---|
| Forget × Archive Capture | Pause after admission, install fence, resume; late manifest/blob remains non-visible; replay same work ID after crash |
| Forget × Recall | Pause between pages, advance fence/epoch, resume cursor; no later page/final handoff discloses bytes |
| Forget × Cache Fill | Pause before cache publication, advance fence; late fill rejected and stale hit denied |
| Forget × Compaction | Stage candidate, advance fence before Context CAS; candidate rejected and old target invalidated for current use |
| Forget × Context Delivery | Fence before submit cancels/supersedes; after immutable submit preserves historical fact but blocks future use |
| Forget × Offline Reconnect | Queue Context offline, advance fence/epoch; reconnect suppresses before restore/replay |
| Forget × Archive Restore | Restore stale backup/index; quarantine until authoritative fence/lineage replay |
| Forget × Snapshot/Delta Replay | Replay stale snapshot/delta after fence; reject, reconcile authorized snapshot + contiguous replay |
| Crash after D registration | Recover same work identity; no unregistered duplicate |
| Crash after blob write before manifest | Orphan remains non-queryable until governed reconciliation |
| Crash after manifest before receipt | Same request returns idempotent receipt |
| Crash after Context CAS before delivery | Version remains authoritative; delivery independently reconciled |
| Crash after provider submit before ACK | C/H outcome UNKNOWN/IN_DOUBT; same identity recovery; no false Applied |

Pass requires zero post-fence disclosure and no unknown state converted to success. If no defensible linearization point exists, result is BLOCKED.

## 5. Forget negative tests

- Old locator after Forget suppressed; old cursor invalid.
- ReadReceipt replay cannot re-read payload or authorize access.
- Cache hit after permission revocation denied.
- Pre-fence cache fill completing post-fence cannot publish.
- F index rebuild from stale snapshot suppresses forgotten candidates.
- Outbox/DLQ replay of forgotten lineage quarantined.
- TSS/compaction derivative with forgotten ancestor invalidated and non-deliverable.
- G Snapshot/Delta replay with stale fence rejected.
- Offline Adapter cache/queue suppressed before restore.
- Archive restore/PITR with stale fence checkpoint remains quarantined.
- Same idempotency key/different digest conflicts.
- Missing producer registration/inventory gap keeps barrier open.
- Unknown I epoch/revocation gap fails closed.
- Denial does not leak protected object existence.

## 6. Permission/isolation tests

- Same Agent across two Environment Scopes cannot cross-read.
- In-scope object without evidence.read permission remains denied.
- Model/caller-supplied scope label cannot grant access.
- Revocation between page 1 and page 2 blocks page 2.
- Revocation between cache fill and hit blocks hit.
- Revocation between RecallResult and Context commit blocks commit.
- Offline reconnect with stale epoch blocks cache restoration.
- Locator/cursor copied to another principal/scope fails.
- Candidate counts/ranking do not disclose denied objects.
- Brain cannot alter System/Developer/User regions or tool authorization.
- Archive text is untrusted data.

Pass: zero unauthorized disclosure.

## 7. Context fidelity tests

- Goal/completion criteria and rare negative constraints survive.
- Reported/Inferred/Verified labels do not change without explicit B/D/E evidence transition.
- Conflicts remain explicit or are resolved with provenance.
- Event/observed/recorded/validity times remain distinct.
- Scope/Environment/task identity preserved.
- Every retained claim maps to exact source lineage.
- Omitted evidence recorded in Loss Ledger and rehydratable when retained/authorized.
- Validator rejects true-but-misleading quote, missing counterexample, stale revision and unauthorized source.
- Failed compaction leaves prior ContextVersion intact.
- Repeated compaction traces to original source.
- TSS is not Agent private state/CoT or Canonical Memory.

Pass: no critical constraint loss, epistemic upgrade, provenance break or silent source rebinding.

## 8. Archive Recall completeness tests

Exact fully executed range with verified bytes → COMPLETE. Fully executed bounded selector with no match → EMPTY_COMPLETE. Budget exhaustion/timeout/partial page/index lag/omitted channel → PARTIAL or DEGRADED. Source revision change → STALE. Fence/permission denial → SUPPRESSED. Authority/integrity unknown → UNKNOWN/UNAVAILABLE. EOF has no next cursor. Receipt proves returned range, not semantic truth. Locator-only result cannot be represented as injected evidence. F summary remains non-canonical and lineage-bound.

Pass: zero false completeness under truncation, timeout, budget and authority fault injection.

## 9. Performance benchmark

### 9.1 Groups

1. Full-History Accumulation.
2. Fixed-threshold EoCC-like.
3. Boundary-triggered compaction.
4. Cost-aware compaction.
5. Cost-aware + Observation Archive.
6. Group 5 + Evidence Fidelity Validation.
7. SAC independent stress test only.

### 9.2 Metrics

Task Success; Fact Accuracy; Constraint Retention; Evidence Recall Accuracy; Epistemic Status Preservation; Context Token Count; Input/Output Tokens; E2E latency; cache read/write cost; recall cost; compaction cost; recovery cost; Archive storage growth; Forget Leakage; False Completeness; P50/P95/P99 latency.

### 9.3 Controls

Predeclare capability floors. Freeze task set/seeds, model/provider/version, tokenizer, prompts, context window, hardware, runtime, cache/archive/index settings and parameters. Separate tuning from held-out. Paired comparisons on identical tasks/seeds. Report per-task outcomes, paired deltas, confidence intervals, tail latency and regressions. Run ablations and combinations. Hard gates: zero unauthorized leakage, false-complete, epistemic upgrade and critical constraint loss.

Phase-1 minimum: 30–50 curated tasks across long-horizon continuation, rare negative constraints, exact recall, source revision change, multi-scope isolation, epistemic preservation and Forget races; at least three repeats per task/configuration. SAC only on selected subset. G owns Context metrics; F Archive metrics; C/H request/cache telemetry; D/I security/Forget assertions; A paired protocol and gate aggregation.

## 10. Exit gates

- Design review: every affected Owner accepts exact candidate revision or records objection.
- Interface freeze: all fields, states, errors, versioning, idempotency and negative tests accepted by B–I and Storage; no P0.
- Rust gate: A records interface freeze and D/I/F/G/H/C/Storage accept Forget/permission/recovery design.
- Production gate: pinned deployment passes all conformance suites with security, recovery and performance evidence.

Current status: plan specified only; no tests claimed run or passed.
