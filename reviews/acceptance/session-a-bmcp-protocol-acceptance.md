# H Owner Acceptance — A Context Optimization / Observation Archive

- Owner: H — BMCP Protocol Architect
- Decision: **ACCEPT WITH CONDITIONS**
- Reviewed A commit: `6caa6034c92c4d3dcf7b2d34ca899b62c3756f1f`
- A live branch HEAD re-queried: `a480a713db358b30dc4cf7c9157025b3c116e439`; decision pinned to requested commit.
- H branch: `session-h-bmcp-protocol`; observed pre-write HEAD: `242d8ab5da890181e762561bb3d3a662287fb63c`.

## 1. Exact A artifacts reviewed

| Path | Blob SHA |
|---|---|
| reviews/integration/nvidia-context-optimization-system-integration-review.md | `b53db1ecb7830a7f1057d09c8ef73aceab942cea` |
| reviews/integration/context-optimization-system-contract-candidates.md | `55257bdf85a56a78df96b797b063bc49d91f5a6d` |
| reviews/integration/context-optimization-conformance-plan.md | `1c941c3e55be1e539a76ef89f297c168296c7db2` |
| reviews/integration/context-optimization-owner-decision-register.md | `36581cf286ddf2516f571eb823fddc9cf8707d80` |

## 2. H baseline and related decisions reviewed

Reviewed:
- `08-bmcp-protocol/adapter-capability-and-applied-attestation.md`, Blob `ed6b43a29aa368d772c701ffc83309a5aadf3c00` — C final-request proof profile and I authorization binding remain OPEN.
- `08-bmcp-protocol/context-delivery-and-acknowledgement.md`, Blob `bf9732cc39d156853b507c3a3a4e573159978f49` — CANDIDATE; G owns Context semantics, H wire/Adapter transport.
- `08-bmcp-protocol/forget-revocation-and-reconnect.md`, Blob `695909360782987781e259187041618f495f1c8c` — CANDIDATE; D fence and I global policy dependencies remain open.

## 3. Formal decision

H accepts A's protocol *semantic separation* only. No concrete BMCP schema, wire enum or compatibility profile is frozen.

### Protocol type boundary

Protocol-visible types should include:
- RecallRequest/RecallIntent (authenticated principal/session binding external to caller claims; bounded selector, scope, purpose, budget, deadline, request/idempotency ID, protocol/schema version);
- RecallResponse with request/session IDs, typed ArchiveLocator(s), exact source revision/hash/range, ReadReceipt, completeness/omissions, budget usage and explicit terminal status;
- RecallContinuation/Cursor with opaque cursor, RecallSession binding, selector digest, Archive object/source revision, authorization/fence checkpoint and expiry;
- DeliveryIntent/ContextDelivery with logical DeliveryId, AttemptId, ContextId, exact target ContextVersion, Snapshot or Delta base/target, payload digest, expiry and idempotency key;
- stage-specific DeliveryAck / Rejection / Unknown outcome;
- AppliedAttestation / AppliedResult, distinct from transport ACK, requiring C Tier-1 evidence for Full and G acceptance;
- Cancel/Supersede and ReconnectReconcile messages;
- typed error envelope with retryability and authoritative stage.

Internal-only unless explicitly exposed by owner contract: F cache entries, page-map internals, physical Archive manifests, ReadBudget counters, G compaction working buffers, LossLedger storage DTOs, E WorkItem/lease internals, D commit cursor internals. Wire types carry opaque typed refs rather than mirror internal database DTOs.

### Minimum Recall request / response

Request: protocol major/minor + schema ID, request/idempotency ID, authenticated session binding, purpose, trusted Scope binding, bounded selector/range, budget, deadline/cancellation, optional context correlation (not authority).

Response: same request ID, RecallSession ID, explicit status (COMPLETE / EMPTY_COMPLETE / PARTIAL / DEGRADED / STALE / SUPPRESSED / UNAVAILABLE / UNKNOWN / CANCELLED / EXPIRED), locator + immutable revision/hash, range/coordinate profile, ReadReceipt, completeness/omission details, budget consumed, next cursor only when valid, retry/recovery hint and trace correlation.

A successful HTTP/RPC response means only transport/request handler completion. A RecallResponse status means F's recall outcome. ReadReceipt means F returned exact bytes/range under recorded checks. Neither is Context Applied or canonical publication.

### ACK and Applied semantics

- Transport ACK: endpoint accepted the delivery bytes (Delivered).
- Adapter materialization result: managed region staged/installed locally (not necessarily final request).
- AppliedAttestation: integrity-protected evidence of exact final request submission; H transports it, C validates proof profile, G decides Applied.
- Full Applied: only Tier-1 adapter, exact target version/digest, final request ID/boundary, current authorization/fence, protected-region integrity and G predicate all pass.
- Tier-2 may be Partial/Unknown; Tier-3 cannot claim Full.
- Forget ClearAcknowledgement is a separate ACK family and reports Adapter-local suppression/clear only, never global Forget completion.

## 4. Cursor, error, idempotency and reconnect requirements

Cursor MUST bind one RecallSession, exact Archive object revision/hash, source revision, selector digest/coordinate system, security principal/scope binding, PermissionEpoch, applicable D fence checkpoint and expiry. It MUST NOT be reused across ContextVersion, session, principal, scope, source revision or selector. ContextVersion is G-owned and correlation only.

Minimum error semantics (exact numeric/string codes remain H schema work):
- STALE — source/object/context base revision no longer current; do not use; re-open/reconcile.
- REVOKED — current permission denied/epoch revoked; fail closed.
- FORGOTTEN / SUPPRESSED — D fence/Forget policy blocks target lineage.
- INCOMPLETE / PARTIAL — bounded read not complete; never treat as full.
- BUDGET_EXCEEDED — explicit non-success/partial result with consumed budget.
- CONTEXT_BASE_MISMATCH — Delta base does not match receiver's reconciled version.
- IDEMPOTENCY_CONFLICT — same key, different digest.
- UNKNOWN / IN_DOUBT — timeout/crash; reconcile by stable ID.
- UNAVAILABLE / UNSUPPORTED / INVALID_CURSOR / EXPIRED / CANCELLED.

Idempotency: stable logical request/delivery ID across retries, distinct attempt IDs; identical key+digest returns durable prior outcome; same key with different digest conflicts. ACK loss after application must be reconciled from immutable evidence, not blindly re-applied.

Reconnect order: authenticate current session; obtain current I PermissionEpoch and D ForgetFence; locally suppress affected content/queues before replay; reconcile G Context target and superseded deliveries; discard stale cursors; fetch a fresh authorized Snapshot or contiguous Delta; only then restore managed region. If authority/order is unknown, keep content suppressed and outcome Unknown. Offline lease/grace must not bypass current revocation/fence.

## 5. Cross-owner findings

- **B↔H:** B semantic refs are not wire schemas; H must preserve discriminator, issuer/namespace and exact version. Unknown/incompatible type rejects. H cannot infer auth from ScopeRef/locator possession.
- **C↔H:** delivery transport ACK and final request Applied evidence are distinct message families/states. Issue #3 explicitly requires exact-version C/G/H (plus I/D/B) decisions; this record does not close it.
- **E↔H:** Canonical Derived publication status can only be exposed from authoritative D/E gate receipt. Recall/Delivery ACK is not publication ACK.
- **F/G↔H:** Recall and Context Delivery are separate request lifecycles; a Recall cursor is not a Context delta cursor. ContextVersion cannot be parsed or compared by H.

## 6. P0 / P1

**P0**
- Exact BMCP Recall/Applied schema and end-to-end state mapping are not frozen; no executable schema conformance or offline replay tests.
- C final request evidence profile and I authorization binding remain open; D ForgetFence currentness is not concretely bound to every read/delivery/reconnect boundary.
- No evidence proves ACK loss, timeout and duplicate replay reconcile without duplicate application or stale disclosure.

**P1**
- Pin canonical schema IDs, protocol version negotiation, backward compatibility/deprecation and unknown-field/type behavior.
- Bind cursor to auth/permission/fence/source revision and define page/cancel terminality.
- Finalize error code registry, retryability, idempotency retention/dedupe horizon and status query/reconciliation.
- Distinguish archive recall, context delivery, applied evidence, clear ACK and canonical publication status families.

## 7. Required negative tests — NOT RUN

| # | Preconditions / sequence | Expected protocol + Agent behavior | Retry / evidence | Status / owner |
|---|---|---|---|---|
| 1 | F sends ReadReceipt only | Recall success only; no Applied | ReadReceipt + absent AppliedAttestation | NOT RUN; F/H/C |
| 2 | Adapter submit fails then retry | stable logical DeliveryId, new AttemptId; dedupe | key/digest/attempt receipt | NOT RUN; C/H |
| 3 | old ContextVersion applied then newer target | late old ACK cannot reactivate; historical fact retained | supersession and Applied evidence | NOT RUN; G/H/C |
| 4 | reconnect replays old version | suppress before queue replay; reconcile fresh Snapshot | fence/epoch/current version | NOT RUN; H/G/I |
| 5 | ACK success but no Applied proof | Delivered or Unknown, never Applied | ACK stage + missing attestation | NOT RUN; H/C/G |
| 6 | cursor continued across ContextVersion | INVALID_CURSOR / STALE; new RecallSession | cursor binding tuple | NOT RUN; F/H |
| 7 | source revision changed | STALE; no silent locator retarget | old/new revision hashes | NOT RUN; F/H/G |
| 8 | G compaction artifact incorrectly published | no BMCP Published status absent E/D receipt | gate result and lineage | NOT RUN; E/D/H |
| 9 | incomplete source accepted by gate | reject/quarantine; no positive publication status | dependency digest + gate trace | NOT RUN; E/D/Storage |
| 10 | Forget then stale derived replay | FORGOTTEN/SUPPRESSED; no delivery | fence + publication receipt + reconnect trace | NOT RUN; D/E/H/I |
| 11 | client ignores STALE | Adapter refuses use; protocol terminal error surfaced | stale response + local suppression | NOT RUN; H/C |
| 12 | duplicate same delivery | return prior result; apply once | dedupe key + digest + prior result | NOT RUN; H/C |
| 13 | timeout after remote handoff | UNKNOWN/IN_DOUBT; query/reconcile; no blind retry | delivery ID, attempt ID, status query | NOT RUN; H/C/G |
| 14 | permission revoked in session | REVOKED, invalidate cursor/cache and block reconnect | current PermissionEpoch + denial | NOT RUN; I/H/F |
| 15 | Recall success but delivery fails | separate successful Recall and failed/unknown Delivery; no Applied | both lifecycle traces | NOT RUN; F/G/H/C |

## 8. Cross-owner dependencies, freeze and implementation

Requires B stable semantic ref registry; C final-request evidence and adapter tier proof; G ContextVersion/Applied/supersession authority; F Recall/cursor/completeness semantics; D/I fence and permission currentness; E canonical publication gate; Storage durability/recovery.

**Interface freeze:** NOT APPROVED. H accepts message-family separation and semantic rules only; wire schema remains candidate.
**Implementation:** NOT AUTHORIZED. BMCP conformance and Adapter reconnect tests are NOT RUN.
**Next gate:** publish versioned Recall/Delivery/Applied/Error schemas; obtain exact C/G/I/D/B decisions on Applied; obtain F/G/D/I Recall/Forget acceptance; run cursor/reconnect/idempotency/timeout negative suite.
