# C Owner Acceptance — A Context Optimization / Observation Archive

- Owner: C — Agent Integration Architect
- Decision: **ACCEPT WITH CONDITIONS**
- Reviewed A commit: `6caa6034c92c4d3dcf7b2d34ca899b62c3756f1f`
- A live branch HEAD re-queried: `a480a713db358b30dc4cf7c9157025b3c116e439`; this decision remains pinned to the requested commit.
- C branch: `session-c-agent-integration-2026-11-16`; observed pre-write HEAD: `2e5776029bc4271c33525f04c7d0f0708e4bbae8`.

## 1. Exact A artifacts reviewed

| Path | Blob SHA |
|---|---|
| reviews/integration/nvidia-context-optimization-system-integration-review.md | `b53db1ecb7830a7f1057d09c8ef73aceab942cea` |
| reviews/integration/context-optimization-system-contract-candidates.md | `55257bdf85a56a78df96b797b063bc49d91f5a6d` |
| reviews/integration/context-optimization-conformance-plan.md | `1c941c3e55be1e539a76ef89f297c168296c7db2` |
| reviews/integration/context-optimization-owner-decision-register.md | `36581cf286ddf2516f571eb823fddc9cf8707d80` |

A's conformance plan is PROPOSED / NOT RUN. No end-to-end runtime test evidence is claimed.

## 2. C baseline and boundary

Reviewed C `07-agent-integration/module-c-agent-integration-baseline-and-redlines.md` (Blob `c79da952efaa490083c88ccb4608d62f526fcbae`) and `07-agent-integration/phase-3.5-agent-identity-applied-attestation-untrusted-memory.md` (Blob `714b2701171ba43123d3ca3c36184678af7d8fea`). C owns Agent/Adapter telemetry semantics, inference-boundary evidence, managed-region isolation and C-side conformance. G owns Context target/version and Applied acceptance; H owns wire/transport/Adapter protocol; I owns identity/authorization; B owns typed refs.

## 3. Formal decision

C accepts the architectural separation:
- F Recall returning bytes/locator/ReadReceipt is not G selection, Adapter delivery, final request submission or Agent application.
- G ContextVersion and DeliveryIntent define the requested target, not proof that the Agent received/applied it.
- Adapter transport acceptance proves only endpoint receipt.
- Materialization in a managed region proves only local assembly at that Adapter boundary.
- C's strongest observable evidence is exact final inference request submission after all transformations, bound to request ID, target ContextVersion, managed-region digest, delivery/attempt, Adapter capability epoch and authenticated session.
- G alone accepts Applied under its per-request predicate; C evidence is an input, not G's state transition authority.

The four required stages are distinct:
1. **F Returned:** RecallResult / page receipt / source revision / completeness; proves what F returned only.
2. **G Selected:** immutable ContextVersion + selected source refs + compaction/lineage/loss record + DeliveryIntent; proves target construction only.
3. **Adapter Submitted/Materialized:** transport receipt and managed-region materialization evidence; proves endpoint receipt/materialization only.
4. **Agent Runtime Applied:** C Tier-1 final-request evidence plus G acceptance; exact final request crossed runtime submit boundary with full managed-region digest and target version. This still does not claim model attention, comprehension or use.

C will not accept a generic ReadReceipt or HTTP/RPC success as Applied evidence. Tier-2 adapters lacking final-submit observability can report Partial/Unknown only; Tier-3 transport-only adapters cannot claim Applied=Full.

## 4. Required evidence and failure semantics

For a Full Applied candidate, evidence must bind:
- immutable DeliveryId + AttemptId and idempotency identity;
- ContextId + exact target ContextVersion and actual applied version;
- InferenceRequestId / FinalRequestBoundaryId;
- Adapter identity + capability epoch and authenticated transport/session binding;
- exact canonical digest profile and digest of the managed region in the final submitted request;
- final submission receipt/hook evidence and submission timestamp;
- coverage Full, protected-region integrity, truncation/transformation outcome;
- current I PermissionEpoch and applicable D ForgetFence at the authoritative submission boundary;
- source lineage digest / ContextObservationReference set sufficient to trace the Context target to source revisions;
- evidence integrity/authenticity and producer provenance.

The Adapter must not write into System/Developer/User, Agent policy, tool authorization or credential regions. Archive/TSS content remains untrusted data.

Failure semantics:
- before handoff: Rejected/Expired/Superseded;
- ambiguous handoff/timeout/crash: Unknown/InDoubt, reconcile by stable delivery ID; no optimistic success;
- stale ContextVersion/source revision/permission/fence: reject/supersede and request fresh authorized Snapshot;
- partial/truncated materialization: Partial, never Full;
- duplicate identical attempt: return prior outcome without reapplying side effects;
- same idempotency key with different digest: conflict;
- old version arriving late: preserve historical proof only if it actually crossed boundary before supersession; never reactivate current use.

## 5. Cross-owner findings

- **B↔C:** typed source refs and Actor/Scope identities are provenance/binding inputs; they are not Agent Applied Evidence. C requires authenticated identity binding and exact final request proof.
- **C↔E:** compaction summaries are G Context projections; if E compiles canonical-derived artifacts, they require E/D registration and publication gate. Context compaction cannot grant canonical publication.
- **C↔H:** H transport ACK must identify its stage (Delivered/Rejected/Unknown); separate final-request attestation and G Applied acceptance. H's candidate attestation schema remains open with C/I.
- **C↔F/G:** cache/recall telemetry must correlate RecallId, source revision, selection, ContextVersion, DeliveryId, request ID and cache outcome. A cache hit must be reauthorized/revalidated under F/I/D rules before inclusion.

## 6. P0 / P1

**P0**
- No executable integrated proof joins F read → G Context commit → H delivery → C final request submit → G Applied acceptance with I/D checks and Forget/revocation races.
- Applied evidence profile and H schema are still candidates; Issue #3 requires explicit exact-version C/G/H/I/D/B decisions. A's documents do not close that issue.
- No evidence that current cache/Agent assembled prompt cannot use stale or forgotten content after reconnect.

**P1**
- C telemetry must expose correlated Recall, selection, compaction, DeliveryIntent, materialization, final request, Applied acceptance, cache hit/invalidation, token/cost, latency and task quality outcomes.
- Provider-specific final-request hooks, middleware transformations, request IDs and digest profile remain TO_VALIDATE.
- Offline reconnect, dedupe horizon and timeout reconciliation need executable adapter/provider conformance.
- TSS and loss ledger require G definition and B epistemic review.

## 7. Required negative tests — NOT RUN

| # | Preconditions / sequence | Expected protocol + Agent behavior | Retry / evidence | Status / owner |
|---|---|---|---|---|
| 1 | F ReadReceipt only; no G delivery | Agent must not claim applied | Read receipt + no Applied record | NOT RUN; F/C/G |
| 2 | Adapter submission fails then retry | same delivery key, new attempt; no duplicate region mutation | attempt IDs, digest, dedupe receipt | NOT RUN; C/H |
| 3 | v applied, then G commits v+1 | v historical only; stop new use of v | Applied evidence + supersession | NOT RUN; G/C/H |
| 4 | stale v queued offline | suppress before restore/replay; obtain current Snapshot | fence/epoch and reconnect trace | NOT RUN; H/G/I |
| 5 | positive ACK, no Applied evidence | remain Delivered/Unknown, not Applied | ACK stage + missing evidence record | NOT RUN; H/C/G |
| 6 | cursor reused across ContextVersion | reject; new Recall session | cursor binding tuple | NOT RUN; F/H |
| 7 | source revision changed | invalidate Context ref; do not silently substitute source | revision/hash mismatch trace | NOT RUN; F/G |
| 8 | compaction summary passed to canonical publisher | Agent may consume only as G Context if authorized; canonical publish blocked absent gate | lineage + gate denial | NOT RUN; G/E/D |
| 9 | missing source ancestor at publication | non-visible; no delivery of artifact | dependency set digest/receipt | NOT RUN; E/D/Storage |
| 10 | Forget then replay old derived output | reject/quarantine and suppress local copies | fence + D/E receipt + adapter suppression | NOT RUN; D/E/H/I |
| 11 | STALE response ignored by client | adapter/Agent boundary must refuse stale region | stale error + blocked request evidence | NOT RUN; H/C |
| 12 | duplicate request same key/digest | dedupe; apply once | logical ID, attempt ID, dedupe outcome | NOT RUN; H/C |
| 13 | timeout after submit | Unknown/InDoubt; reconcile by request/delivery ID | submit boundary event, timeout, reconciliation | NOT RUN; C/H/G |
| 14 | permission revoked mid-session | deny next read/submit; suppress cached protected region | PermissionEpoch + denial trace | NOT RUN; I/F/H/C |
| 15 | recall OK, delivery failure | no Agent Applied; keep delivery failed/unknown | RecallResult separate from delivery evidence | NOT RUN; F/G/H/C |

## 8. Cross-owner dependencies, freeze and implementation

Requires G's exact Context/Applied predicate and supersession behavior; H's versioned BMCP delivery/ACK/attestation schema and reconnect; F's recall/cache currentness; I's identity/PermissionEpoch/revocation; D's ForgetFence; B's reference/epistemic semantics; E/D publication separation; Storage recovery.

**Interface freeze:** NOT APPROVED. C accepts only the stage separation and evidence invariants above; no Applied wire schema freeze.
**Implementation:** NOT AUTHORIZED. Provider-specific proof hooks and integrated negative tests are NOT RUN.
**Next gate:** C/G/H pin exact Applied evidence contract; C/H prove final request observability per adapter tier; F/G/H/C run replay/cache/timeout fault tests; I/D supply authoritative fence/epoch validation.
