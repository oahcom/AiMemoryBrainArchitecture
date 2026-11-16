# BMCP Protocol Conformance Matrix

- Status: **CANDIDATE test specification; no implementation evidence exists**
- Owner: H; cross-module test owners are identified per row.
- Release gate: design review only. This matrix does not certify a runtime implementation.

## 1. Tier summary

| Capability | Tier 1: final-request observable | Tier 2: managed-region observable | Tier 3: transport/basic |
|---|---:|---:|---:|
| Protocol negotiation and version validation | MUST | MUST | MUST |
| Authenticated transport principal binding | MUST (I mechanism) | MUST (I mechanism) | MUST (I mechanism) |
| Required/optional field validation | MUST | MUST | MUST |
| Canonical serialization / integrity verification | MUST | MUST | MUST |
| Telemetry/Event Ingress transport | MUST if advertised | MUST if advertised | MAY |
| Context Snapshot / Delta validation | MUST if advertised | MUST if advertised | MAY |
| Exact G base/target version handling | MUST | MUST | If Context delivery advertised |
| Idempotency / duplicate replay handling | MUST | MUST | MUST for state-changing ops |
| Final inference request observation | MUST | MUST NOT claim | MUST NOT claim |
| Full Applied attestation | MAY, only with proof | MUST NOT | MUST NOT |
| Partial / Bypassed / Unknown coverage | MUST | MUST | MUST NOT claim application; Unknown may be reported |
| Forget/revocation suppression and reconnect | MUST | MUST | MUST for any cached/queued state |
| Protected region isolation | MUST | MUST | MUST NOT modify any prompt region |
| Model attention/use assertion | MUST NOT | MUST NOT | MUST NOT |

Tier 1/2/3 are ceilings. A Tier 1 adapter may still return Partial, Bypassed or Unknown for a particular request.

## 2. Protocol and envelope tests

| ID | Scenario | Expected result | Tier | Owner(s) |
|---|---|---|---|---|
| ENV-001 | Missing required message_id | Reject ENVELOPE_INVALID | All | H |
| ENV-002 | Unknown optional namespaced extension | Ignore/preserve without changing semantics | All | H |
| ENV-003 | Unknown required field | Reject REQUIRED_FIELD_UNSUPPORTED | All | H |
| ENV-004 | Unknown message type | Reject MESSAGE_TYPE_UNSUPPORTED | All | H |
| ENV-005 | Unknown non-security enum | Explicit ENUM_UNSUPPORTED or registered extension path; never map silently | All | H + payload owner |
| ENV-006 | Unknown authorization/revocation enum | Fail closed | All | H + I |
| ENV-007 | Unsupported major version | VERSION_UNSUPPORTED; no downgrade | All | H |
| ENV-008 | Optional minor extension | Process if understood; otherwise safely ignore | All | H |
| ENV-009 | Duplicate JSON keys / invalid canonical form | Reject before integrity validation/application | All | H |
| ENV-010 | Payload digest/signature mismatch | INTEGRITY_FAILED; no state change | All | H + I |
| ENV-011 | Same idempotency key and same digest | Return original receipt/result | All | H + operation owner |
| ENV-012 | Same idempotency key and different digest | IDEMPOTENCY_CONFLICT | All | H + operation owner |
| ENV-013 | Expired message | EXPIRED; no application | All | H |
| ENV-014 | Payload ActorRef differs from authenticated principal binding | Reject/quarantine; never trust payload self-assertion | All | I + H |
| ENV-015 | Stale permission epoch | Reauthorize or reject; no protected operation | All | I + H |
| ENV-016 | Unrelated cursor types compared as integers | Conformance failure; opaque owner-typed tokens only | All | H + A |

## 3. Context delivery and acknowledgement tests

| ID | Scenario | Expected result | Tier | Owner(s) |
|---|---|---|---|---|
| DEL-001 | Prepared only | No Delivered/Applied claim | All | H |
| DEL-002 | Transport endpoint receipt | Delivered only | All | H |
| DEL-003 | Delta base equals current G version | Atomic apply candidate | 1/2 | G + H |
| DEL-004 | Delta base mismatch | Reject CONTEXT_BASE_MISMATCH; request Snapshot | 1/2 | G + H |
| DEL-005 | Snapshot target older than current | Reject stale Snapshot | 1/2 | G + H |
| DEL-006 | Duplicate identical delivery | Idempotent prior result; no duplicate effects | All | H + G |
| DEL-007 | Same delivery key with different digest | IDEMPOTENCY_CONFLICT | All | H + G |
| DEL-008 | Newer Context target before old apply | Old delivery Superseded | 1/2 | G + H |
| DEL-009 | Timeout after transport handoff | Unknown until reconciliation | All | H |
| DEL-010 | Late ACK after Superseded | Historical only; cannot restore old target | All | G + H |
| DEL-011 | Retry after Expired | New authorized logical delivery required | All | G + H |
| DEL-012 | Partial materialization | Partial, never Full | 1/2 | H + C + G |
| DEL-013 | Managed region bypassed | Bypassed | 1/2 | H + C |
| DEL-014 | No final request observation | Tier 2/3; Full forbidden | 2/3 | H + C |
| DEL-015 | Full request and valid submit evidence | Full may be accepted after G/I validation | 1 | H + C + G + I |
| DEL-016 | Adapter internal buffer changed but runtime submit absent | Full rejected | All | H + C |
| DEL-017 | Model attention/use inferred from Applied | Conformance failure | All | H + C |

## 4. Forget, revocation and reconnect tests

| ID | Scenario | Expected result | Tier | Owner(s) |
|---|---|---|---|---|
| FRG-001 | Forget fence raised while delivery Prepared | Supersede/cancel; do not send stale target | All | D + G + H |
| FRG-002 | Forget fence raised while delivery Delivered | Prevent new application; reconcile any in-flight submit | All | D + G + H |
| FRG-003 | Forget after submit before ACK | Historical attestation only if provable; current target remains suppressed | 1/2 | D + G + H |
| FRG-004 | Adapter offline during revocation | Pending/Unknown; no false clear ACK | All | I + H |
| FRG-005 | Reconnect with stale local Snapshot | Clear/suppress first, then reject stale Snapshot | All | D + G + H + I |
| FRG-006 | Old fence replay after restart | Reject as stale; persistent suppression marker remains | All | D + H |
| FRG-007 | Fence ordering unknown | Fail closed and request authoritative reconciliation | All | D + I + H |
| FRG-008 | Delta gap after offline period | Request full Snapshot; do not guess | 1/2 | G + H |
| FRG-009 | Local cache purge unsupported | Report UNSUPPORTED/UNKNOWN; no deletion claim | All | H + I |
| FRG-010 | Provider-retained prompt | Explicitly outside Adapter clear guarantee | All | H + I |
| FRG-011 | Late Applied ACK after revocation | Historical only; never restores access | All | I + G + H |
| FRG-012 | Adapter crashes between suppression and ACK | Reconnect resumes from persisted marker; no stale replay | All | H + I |

## 5. Telemetry and Event Ingress tests

| ID | Scenario | Expected result | Tier | Owner(s) |
|---|---|---|---|---|
| ING-001 | Intent submitted as completed outcome | Preserve Intent semantics; never auto-promote | All | C + E |
| ING-002 | Telemetry Accepted receipt returned | Durable receipt only; not Compiled/CanonicalCommitted/Indexed | All | E + H |
| ING-003 | Same source sequence duplicate | Owner-defined idempotent replay | All | C + E + H |
| ING-004 | Same idempotency key different payload | Conflict | All | E + H |
| ING-005 | Environment-dependent event missing environment identity | Reject/quarantine per C/I contract | All | C + I + H |
| ING-006 | Payload self-asserts ActorRef | Compare with transport principal; never authenticate from payload | All | I + H |
| ING-007 | Durable acceptance interrupted before ACK | Query/retry same key returns original receipt or explicit unknown | All | E + H |
| ING-008 | Unknown C-owned event enum | Do not reinterpret as a different event kind | All | C + H |

## 6. Security and protected-region tests

| ID | Scenario | Expected result | Tier | Owner(s) |
|---|---|---|---|---|
| SEC-001 | Memory text contains fake system/developer instruction | Remains data in managed region; no instruction elevation | All | C + H + I |
| SEC-002 | Memory payload requests tool execution | No tool grant or invocation; Agent policy remains authoritative | All | C + H |
| SEC-003 | Adapter attempts to overwrite protected prompt region | Reject and emit security event | All | C + H |
| SEC-004 | Cross-scope delivery | I denies; no payload disclosure/application | All | I + H + G |
| SEC-005 | Revoked principal uses cached permission epoch | Reject/reconcile; no stale access | All | I + H |
| SEC-006 | Digest/log includes raw sensitive memory unexpectedly | Privacy conformance failure; minimize evidence | All | H + I |

## 7. Reliability, fault injection and state invariants

| ID | Scenario | Expected result | Tier | Owner(s) |
|---|---|---|---|---|
| REL-001 | Duplicate message after process restart | Dedup state returns original result within retention horizon | All | H + operation owner |
| REL-002 | Lost ACK after successful handoff | Unknown until reconciliation; no blind duplicate side effect | All | H |
| REL-003 | Adapter process crash while Prepared | Recover Prepared or Unknown; never infer Applied | All | H |
| REL-004 | Brain unavailable | Agent remains operable; no new Applied claim | All | C + H |
| REL-005 | Capability changes on upgrade | New capability epoch and renegotiation | All | H |
| REL-006 | Context target superseded while queued offline | Drop/supersede stale queue item | All | G + H |
| REL-007 | Expiry while offline | Expired on reconnect; no extension by retry | All | H |
| REL-008 | Unverifiable ordering of late ACK | Keep Unknown; do not upgrade | All | H + G |
| REL-009 | Protected region unchanged but model ignores memory | Applied remains boundary attestation only | All | C + H |
| REL-010 | No implementation evidence attached | Test remains NOT RUN, not PASS | All | Test owner |

## 8. Acceptance gates

| Gate | Required evidence | Current status |
|---|---|---|
| G0 — Wire correctness | Schema validation, version negotiation, canonicalization, error tests | OPEN; design only |
| G1 — Identity/authentication | I-approved principal binding, permission epoch and negative tests | BLOCKED on I |
| G2 — Ingress/receipt | E receipt/idempotency contract and crash-window tests | OPEN |
| G3 — Context delivery | G version/CAS/delivery contract and snapshot/delta tests | OPEN |
| G4 — Applied proof | C final-request semantics, Tier 1 evidence hook and verifier tests | BLOCKED on C/runtime implementation |
| G5 — Forget/reconnect | D fence, I global policy, G reconciliation and offline race tests | BLOCKED on D/I/G |
| G6 — Security boundary | Protected-region tests and Agent authorization tests | OPEN; residual prompt-injection risk remains |
| G7 — End-to-end conformance | Cross-module fault injection with reproducible evidence | NOT STARTED |

## 9. Decision and evidence discipline

Each test result must record build/commit, Adapter tier and capability epoch, protocol version, fixture, authenticated principal class (non-sensitive identifier), expected result, actual result, logs/evidence reference, and reviewer. No document-only assertion is a runtime PASS.

No test in this matrix authorizes:
- global contract freeze;
- physical deletion guarantee;
- model-attention/use claim;
- security certification;
- performance sign-off.
