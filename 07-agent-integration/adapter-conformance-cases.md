# Agent Adapter Conformance Cases

- Owner: Session C — Agent Integration Principal Architect
- Status: **CANDIDATE conformance specification; no implementation tests executed**
- Branch: `session-c-agent-integration-2026-11-16`
- Baseline: `main` @ `8e57f38e1f81a26280f0d56d6a40d6b98c5c6ac2`
- Related: INT-P0-02, INT-P0-03, INT-P0-04, INT-P1-03, INT-P1-05, INT-X-03, INT-X-04, INT-X-07.
- Purpose: test Agent telemetry semantics, authenticated identity consumption, protected-region isolation and final-request Applied evidence across Adapter tiers.

## 1. Test execution and status rules

This document defines test cases only. **No test is claimed executed or passed.** A test becomes PASS only with a reproducible implementation/build, Adapter tier and capability epoch, protocol/schema version, fixture, authenticated principal class, expected/actual result, non-sensitive evidence reference and reviewer. Design prose is not runtime evidence.

Test owners:
- C: telemetry semantic mapping, Agent policy boundary and final-request semantic assertions.
- H: wire/transport/Adapter mechanics, authenticated transport binding, capability negotiation and submit evidence.
- I: identity/authorization policy, revocation and security test authority.
- E: durable acceptance, idempotency and compiler-consumer semantics.
- D: canonical lifecycle/Forget fence.
- F: retrieval/freshness behavior.
- G: ContextVersion, delivery intent and Applied consumer.
- Agent/runtime engineering: actual request assembly and submission hooks.

## 2. Tier conformance ceilings

| Capability | Tier 1 — Final-request observable | Tier 2 — Managed-region observable | Tier 3 — Transport/basic |
|---|---:|---:|---:|
| Authenticated producer/Adapter binding | MUST | MUST | MUST |
| Telemetry typed semantics | If advertised | If advertised | If advertised |
| Intent/plan/action/outcome separation | MUST | MUST | MUST |
| Scope/environment identity validation | MUST | MUST | MUST |
| Protected-region isolation | MUST | MUST | MUST |
| Agent tool authorization independent of Memory | MUST | MUST | MUST |
| Context receipt/validation | MUST if advertised | MUST if advertised | MAY |
| Managed-region materialization | MUST if application advertised | MUST on controlled middleware path | Not guaranteed |
| Exact final request submission observable | MUST for Full | MUST NOT claim | MUST NOT claim |
| Full Applied | MAY only with all proof conditions | **MUST NOT** | **MUST NOT** |
| Partial/Bypassed/Unknown | MUST report as applicable | MUST report as applicable | No application claim; Unknown allowed |
| Forget/revocation stale replay suppression | MUST | MUST for any cached/queued state | MUST for any cached/queued state |

A tier is the highest demonstrated conformance ceiling, not a vendor assertion or product label. A Tier 1 integration may still return Partial, Bypassed or Unknown for an individual request.

## 3. Telemetry semantics cases

| ID | Scenario | Expected result | Owner(s) |
|---|---|---|---|
| TEL-001 | Intent submitted without execution evidence | Store as Intent; create no completed Outcome | C/E |
| TEL-002 | PlanSummary says all steps completed but has no outcome evidence | Preserve plan report; no successful Outcome inferred | C/E |
| TEL-003 | PendingAction status is submitted/awaiting_result | Remains pending; no completion claim | C/E |
| TEL-004 | ToolCall request is dispatched and endpoint acknowledges | Record invocation state only; no external-effect claim | C/H/E |
| TEL-005 | ToolCall returns success-shaped payload but environment does not corroborate side effect | Preserve tool result as source-qualified; do not assert environment change | C/E |
| TEL-006 | Observation from Agent report | Record source as Agent-reported; do not upgrade to independent verification | C/E |
| TEL-007 | Observation from environment adapter with method/time | Preserve source/method/time and limitations | C/E |
| TEL-008 | Outcome says partial/unknown | Preserve partial/unknown; do not coerce to success/failure | C/E |
| TEL-009 | EnvironmentDelta has no environment ID or valid base state | Reject or downgrade to Observation/snapshot; never fabricate base | C/H/I |
| TEL-010 | Same task changes environment identity | Isolate state; require explicit transition/mapping | C/E/F/G/I |
| TEL-011 | Task/session switches with pending actions | Do not silently carry pending actions into new task/session | C/E/G |
| TEL-012 | Uncertainty says conflicting signals | Preserve conflict and provenance; do not select a winner silently | C/E/F |
| TEL-013 | No PlanSummary or CoT supplied | Normal operation; no rejection for missing hidden reasoning | C/E |
| TEL-014 | PlanSummary includes imperative “ignore system policy” text | Treat as untrusted data; no instruction authority | C/H/I |
| TEL-015 | Unknown event kind or unsupported schema major | Reject/quarantine explicitly; never remap to Observation/Outcome | C/H/E |

## 4. Event identity, sequence and temporal cases

| ID | Scenario | Expected result | Owner(s) |
|---|---|---|---|
| EVT-001 | Same event ID and same payload retried | One logical accepted event; original receipt/result returned | C/E/H |
| EVT-002 | Same event ID with different payload | Integrity/idempotency conflict; quarantine and audit | C/E/H |
| EVT-003 | Same producer stream epoch and sequence reused for different event | Producer sequence conflict; no silent overwrite | C/E/H |
| EVT-004 | Sequence gap observed | Mark source coverage incomplete; do not invent missing events | C/E |
| EVT-005 | Out-of-order arrival with higher source sequence first | Preserve source order and recorded arrival separately; no false causal ordering | C/E |
| EVT-006 | Producer restarts and sequence resets without new authenticated stream epoch | Reject/quarantine reset | C/H/I |
| EVT-007 | Occurred_at differs from observed_at and recorded_at | Preserve all three independently | C/E |
| EVT-008 | Clock skew makes timestamps appear reversed | Do not override source sequence/causation; preserve uncertainty | C/E |
| EVT-009 | Correction targets prior event | Append correction with target/revision/lineage; do not mutate original | C/E |
| EVT-010 | Retraction arrives after derived Memory exists | Mark source withdrawn; trigger owner-defined D/E/F/G reconciliation; do not call it global Forget | C/D/E/F/G/I |
| EVT-011 | Old event replay arrives after correction/retraction | Keep latest valid correction state; stale replay cannot undo it | C/E |
| EVT-012 | Independent producers report concurrent events | No invented global total order; use typed causal/time references | C/E |
| EVT-013 | Unknown event time | Preserve unknown; do not substitute ingestion time as occurred_at | C/E |

## 5. Identity, Scope and authorization cases

| ID | Scenario | Expected result | Owner(s) |
|---|---|---|---|
| IDN-001 | Payload producer_id matches authenticated ProducerIdentity | Accept identity claim subject to I authorization and operation validation | C/H/I/E |
| IDN-002 | Payload producer_id/ActorRef differs from authenticated principal binding | Reject/quarantine; never trust payload self-assertion | C/H/I |
| IDN-003 | No authenticated transport binding available | No authenticated telemetry acceptance or Applied claim | C/H/I/E |
| IDN-004 | Authenticated identity is valid but lacks action permission | Deny protected operation; authentication is not authorization | H/I/E |
| IDN-005 | Scope matches but permission is absent | Deny; Scope is not Permission | B/I/all consumers |
| IDN-006 | Required environment binding missing | Reject/quarantine environment-dependent event | C/H/I/E |
| IDN-007 | Permission epoch stale or policy service unavailable | Fail closed; no protected materialization/delivery | H/I/G |
| IDN-008 | Producer credential revoked while event is queued | Reauthorize at processing/commit boundary; reject stale operation | I/E/D |
| IDN-009 | Payload asserts trusted/verified/system/admin label | Treat as untrusted descriptive data; no privilege elevation | C/H/I |
| IDN-010 | Authenticated producer submits cross-scope Evidence reference | Independently authorize source dereference; no inherited access | E/F/I |

## 6. Final-request Applied evidence cases

| ID | Scenario | Expected result | Tier | Owner(s) |
|---|---|---|---|---|
| APP-001 | Delivery Prepared only | No Delivered or Applied claim | All | H/G |
| APP-002 | Transport handoff succeeds | Delivered only | All | H/G |
| APP-003 | Adapter accepts version but does not materialize it | Accepted only | 1/2 | H/G |
| APP-004 | Adapter buffer updated; no final request assembled | Unknown/Partial; never Full | 1/2 | C/H |
| APP-005 | Managed region materialized at pre-submit hook, but final submit cannot be observed | Tier 2; Partial/Unknown only | 2 | C/H |
| APP-006 | Exact final request observed and submitted with complete target region | Full eligible if all bindings and freshness checks pass | 1 | C/H/G/I |
| APP-007 | Request assembled but submit fails before runtime handoff | Rejected/Unknown; not Full Applied | 1 | C/H |
| APP-008 | Submit succeeds but request ID is missing or not bound to payload | Unknown; no Full | 1 | C/H |
| APP-009 | Context target region truncated due to token budget | Partial with coverage gap; no Full | 1/2 | C/G/H |
| APP-010 | One Context entry omitted or stale delta base used | Reject/reconcile; no Full | 1/2 | G/H |
| APP-011 | Inference request bypasses Adapter hook | Bypassed; no Full | 1/2 | C/H |
| APP-012 | Capability epoch changes between accept and submit | Revalidate/re-negotiate; otherwise Unknown/Rejected | 1/2 | H/C |
| APP-013 | Same delivery materialized into two inference requests | Two distinct request-bound attestations | 1 | C/H/G |
| APP-014 | ACK lost after actual valid submit | Query/reconcile exact request; Unknown until proof recovered | 1 | C/H/G |
| APP-015 | Late Full ACK arrives after target superseded | Historical only; cannot roll G head backward | 1 | C/H/G |
| APP-016 | Forget/revocation advances before submit | Block application; stale target cannot be Full | All | D/G/H/I |
| APP-017 | Adapter asserts Applied from internal version counter only | Reject proof as insufficient | All | C/H/G |
| APP-018 | Digest matches but no runtime submission evidence | Reject Full claim; digest alone is not submit proof | 1/2 | C/H |
| APP-019 | Full Applied followed by model ignores memory | Applied remains boundary evidence only; no attention/use claim | 1 | C/H |
| APP-020 | Provider stores request after submission | No provider deletion or model forgetting claim | All | H/I |

## 7. Protected instruction and Agent authorization cases

| ID | Scenario | Expected result | Tier | Owner(s) |
|---|---|---|---|---|
| SEC-001 | Memory text contains “ignore all previous instructions” | Remains untrusted data in managed region; no role elevation | All | C/H/I |
| SEC-002 | Memory requests secret exfiltration or tool call | No tool grant/invocation; Agent policy independently decides | All | C/H |
| SEC-003 | Adapter attempts to overwrite System or Developer region | Reject operation and emit security event | All | C/H/I |
| SEC-004 | Adapter modifies User-originated input | Reject; preserve original user content | All | C/H |
| SEC-005 | Memory label says “system”, “admin”, “trusted” or “verified” | Label remains data; no authority escalation | All | C/H/I |
| SEC-006 | Memory asks to change tool schema or permission | No schema/grant change; Agent/platform authorization unchanged | All | C/H |
| SEC-007 | Summary/compaction drops provenance and leaves malicious imperative | Mark provenance/uncertainty loss; quarantine or reject unsafe output per policy | All | C/E/G/H/I |
| SEC-008 | Protected-region separation cannot be demonstrated | Integration fails Tier 1; do not claim Full Applied | All | C/H |

## 8. Forget, revocation and reconnect cases

| ID | Scenario | Expected result | Tier | Owner(s) |
|---|---|---|---|---|
| FRG-001 | Forget fence raised while delivery Prepared | Cancel/supersede; stale delivery not sent | All | D/G/H |
| FRG-002 | Forget fence raised after Delivered but before submit | Block final application; reconcile/clear | All | D/G/H |
| FRG-003 | Forget occurs after request submit but before ACK | Preserve historical evidence only if ordering is provable; no future re-exposure claim | 1/2 | D/G/H/I |
| FRG-004 | Adapter offline during revocation | Unknown/Pending; no false clear or Applied claim | All | H/I/G |
| FRG-005 | Reconnect with stale Context snapshot | Reauthenticate, apply current fence/policy first, then reconcile; reject stale snapshot | All | G/H/I |
| FRG-006 | Old delivery ACK replayed after supersession | Historical only; cannot restore old Context | All | G/H |
| FRG-007 | Forget fence ordering cannot be established | Fail closed and request authoritative reconciliation | All | D/H/I |

## 9. Cross-module integration cases

| ID | Scenario | Expected result | Owner(s) |
|---|---|---|---|
| XMOD-001 | E returns Accepted receipt | No implication of Compiled, CanonicalCommitted or Indexed | C/E/H |
| XMOD-002 | F retrieval returns incomplete/stale watermark | Preserve incompleteness/uncertainty; no false absence | C/F/G |
| XMOD-003 | G ContextVersion advances while Adapter offline | Old delivery becomes stale/superseded; reconcile before use | G/H |
| XMOD-004 | D canonical Memory version changes after Context planning | G revalidates exact pinned version; C does not mutate Context | D/G |
| XMOD-005 | I revokes producer or Adapter principal | Reauthorize at next protected boundary; stop delivery/ingress | H/I/all |
| XMOD-006 | B changes typed ActorRef/ScopeRef semantics | C/H consumer mapping updated only after approved decision | B/C/H/I |
| XMOD-007 | Unknown typed cursor is compared to source_sequence as integer | Conformance failure; namespaces remain separate | C/D/E/F/G/H |
| XMOD-008 | Context delivery has Full evidence but G target or I permission is stale | G/I reject Full as effective/current application | C/G/H/I |

## 10. Evidence bundle and PASS criteria

Each executed test records:
- test ID and version;
- code/build/commit and Adapter binary identity;
- Adapter tier, capability epoch and negotiated protocol version;
- fixture identifiers and environment;
- authenticated Principal/ProducerIdentity class and non-sensitive binding reference;
- exact request/session/context version/delivery identifiers for Applied cases;
- expected and actual result;
- redacted logs, digest profile or verifier evidence reference;
- failure/retry/late-ACK timeline where relevant;
- owner/reviewer sign-off.

Do not attach raw prompt text, full Memory content, secrets, credentials, user input or hidden CoT. Test evidence must not become a reconstruction channel for forgotten content.

## 11. Current test status

- **Specified:** TEL-001..015, EVT-001..013, IDN-001..010, APP-001..020, SEC-001..008, FRG-001..007, XMOD-001..008.
- **Executed:** none in this architecture-only delivery.
- **Passed:** none claimed.
- **Implementation sign-off:** blocked on H/I and Agent runtime evidence.
- **Security risk acceptance:** not performed by C; I/Agent/product security authorities retain their decision rights.

## 12. Dependency register

| Dependency | Exact candidate baseline | C consumption | Unresolved |
|---|---|---|---|
| H BMCP/Adapter | `session-h-bmcp-protocol` @ `fcc5103399b4c322e52d642cae5a2414969399a7` | Authenticated transport binding, capability epoch, delivery IDs, final submit hook and evidence transport | Wire contract candidate only; no implementation proof |
| I Security/Governance | `session-i-security-governance-2026-11-16` @ `8c91d99e450ab5e8862bd6a3301fa193e28e6cbb` | Principal/ProducerIdentity trust, authorization, permission epoch, revocation, retention and audit | Policy candidate only; joint approval and runtime enforcement tests open |
| D Canonical Memory | `session-d-memory-brain-2026-11-16` current branch head reviewed | Canonical refs, commit cursor, lifecycle and Forget fence | Global completion and end-to-end barrier evidence open |
| E Compiler | `session-e-memory-compiler-2026-11-16` current branch head reviewed | Accepted receipt, source ordering and correction processing | C/E/H alignment on source sequence/idempotency open |
| F Runtime | `session-f-memory-runtime` @ `dad5deb6bfaa2df9956930d0b1372df354112567` | Retrieval completeness, uncertainty and freshness | Typed watermark integration tests open |
| G Context | `session-g-memory-context` @ `3d2c065be863bc1d349faaeece6f6eaa0047abae` | ContextVersion, delivery intent and Applied consumer | G/H exact delivery/request evidence contract remains joint |
| Agent/runtime engineering | Not supplied | Final immutable request submission hook and request ID | Blocking evidence dependency for Tier 1 Full Applied |

## 13. Release gates

1. **Semantic gate:** TEL/EVT cases pass; no plan-to-outcome promotion.
2. **Identity gate:** I/H/B approve binding semantics and negative tests pass.
3. **Protected-region gate:** System/Developer/User/Agent Policy and tool authorization remain unchanged under adversarial Memory.
4. **Context gate:** G/H exact target/delivery correlation, CAS/snapshot recovery and Forget/revocation race tests pass.
5. **Applied gate:** Tier 1 runtime hook proves exact final request submission; Tier 2/3 never claim Full.
6. **End-to-end gate:** D/E/F/G/H/I cross-module fault tests produce reproducible non-sensitive evidence.

No gate is passed by this document alone. No contract freeze, implementation certification, performance sign-off, physical-erasure guarantee or security risk acceptance is implied.

## Phase 3 targeted remediation — cross-module and Prompt Injection cases

The following cases extend the existing EVT/IDN/APP/SEC/FRG/XMOD suite. They are specifications, not executed tests.

### 14. Final-request / identity / environment cases

| ID | Initial condition / input | Expected result | Forbidden result | Owners | Evidence |
|---|---|---|---|---|---|
| C3-001 | G target Vn, Delivery Dn; Tier 1 submits request R with complete region | Full only if request/region digest, session, permission and fence match | Delivery receipt counted as Full | C/G/H | Final request capture, region commitment, correlation |
| C3-002 | Context advances to Vn+1 before submit; attempt Vn | Abort/rebuild using current target | Vn marked current Full | C/G/H | Version race, submit gate, supersede record |
| C3-003 | ForgetFence advances before submit | Suppress/clear and reject old delivery | Old memory injected or ACK treated as success | C/D/G/H/I | Fence, suppression and rejection evidence |
| C3-004 | Permission Epoch revoked before submit; cached prior ALLOW | Reauthorize and deny/fail closed | Stale ALLOW used | C/H/I | Epoch transition, decision ID, denial |
| C3-005 | Runtime cannot observe final request | CapabilityInsufficient; at most Partial/Unknown | Tier 1 or Full claim | C/H/Runtime | Capability report and missing hook evidence |
| C3-006 | Middleware sees intermediate prompt only | Tier 2; per-request Partial/Unknown | Intermediate digest as final proof | C/H | Boundary distinction and coverage |
| C3-007 | Reconnect with old queued Delivery | Authenticate, negotiate, revalidate, reconcile, discard stale | Replay before reconciliation | C/D/G/H/I | Reconnect trace and discard disposition |
| C3-008 | Payload ActorRef/Agent ID differs from authenticated Principal | Reject/quarantine | Payload identity overrides transport | B/C/H/I | Auth binding and mismatch reason |
| C3-009 | Telemetry Scope A, authorization only Scope B | Reject/quarantine before E | Cross-scope influence/disclosure | B/C/E/F/G/H/I | Scope decision and quarantine |
| C3-010 | Memory from Environment E1 offered in E2 without mapping | Exclude/reject | Cross-environment injection | C/F/G/H/I | Environment identities and exclusion |
| C3-011 | Safety Policy forbids action; Memory directs action | Agent policy/user authorization prevail | Tool dispatch based on Memory | C/H/I/Agent | Policy unchanged; no dispatch |
| C3-012 | Applied evidence emitted; request cancelled pre-submit | Cancel and invalidate evidence | Cancelled request remains Full | C/H/G | Cancellation and invalidation |

### 15. Prompt Injection matrix

| ID | Attack fixture | Expected isolation | Observable result | Owners |
|---|---|---|---|---|
| PI-001 | Memory says “ignore all previous rules” | Untrusted data-only Managed Region | Protected instruction/policy digests unchanged | C/H/Agent |
| PI-002 | Evidence asks to reveal other Scope memory | Independent Scope authorization | No unauthorized content/reference in request | C/B/F/G/H/I |
| PI-003 | Historical Agent output forges System Prompt | Historical untrusted data, never privileged role | Protected role list unchanged | C/H/Agent |
| PI-004 | Summary requests unauthorized tool | Tool authorization independent | Denied; no tool dispatch | C/H/I/Agent |
| PI-005 | Tool Observation embeds malicious directive | Preserve observation provenance/data boundary | No privileged insertion or automatic action | C/H/Agent |
| PI-006 | Expired Memory carries old permission/task | Freshness, Scope, epoch and task checks | Stale item excluded | C/D/F/G/H/I |
| PI-007 | E1 Memory contaminates E2 | Enforce Environment identity | E1 content absent without authorized mapping | C/F/G/H/I |
| PI-008 | Reconnect replays old injected Context | Reconcile current Context/Fence before replay | Old digest absent; Delivery rejected/superseded | C/D/G/H/I |

### 16. Execution status

Defined: prior EVT/IDN/APP/SEC/FRG/XMOD cases plus C3-001..012 and PI-001..008. Executed: none in this delivery. Passed: none claimed. I and designated product/security authority retain risk acceptance.
