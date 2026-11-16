# C — Agent Integration Technology Architecture Review

- Document: TAR-AI-001 / TAB-001 v0.1
- Owner: C — Agent Integration Architect
- Branch: `session-c-agent-integration-2026-11-16`
- Reviewed source branch HEAD (pre-publication snapshot): `0a81f370bfc331872897ff83b6cbe051806cfc7b`; tree SHA: `b83522caa7739dab6960442ac8ade81f24742505`. The report publication commit is recorded separately in the execution summary.
- Review date: 2026-11-17
- Report version: 1.0
- Verdict: **CONDITIONAL PASS**
- Review mode: static Agent/Adapter architecture review; no framework integration, runtime hook, security or performance tests executed.

## 1. Executive Summary

C's design correctly treats Agent integration as a real runtime boundary rather than a thin API client. It defines telemetry semantics without requiring hidden chain-of-thought, separates Intent/Plan/PendingAction/ToolCall/Observation/Outcome, preserves producer-local sequence and environment identity, and defines Full Applied at the final immutable inference request actually submitted to the inference runtime. It also correctly restricts Tier 2 and Tier 3 from claiming Full Applied, preserves System/Developer/User/Agent policy regions, and keeps tool authorization with the Agent.

The architecture is implementable across heterogeneous Agents only as a capability-tiered integration strategy. Tier 1 requires a framework/runtime hook at the final submit boundary, a unique inference request ID and verifiable request-bound evidence. Many middleware or event/tool integrations will only reach Tier 2/3. Embedded SDK, sidecar and remote gateway have different trust, latency and failure trade-offs; none can manufacture observability that the Agent runtime does not expose.

Conditional acceptance is limited to design semantics. The critical dependencies remain OPEN: H wire/transport and ACK schema, I authenticated Principal/permission/revocation policy, G ContextVersion/Delivery authority, B typed references, and actual Agent framework final-submit hooks. C's conformance matrix explicitly states no cases were executed or passed. No Applied implementation claim, cross-framework compatibility or prompt-injection security certification is made.

## Upstream Owner Input Status (refreshed branch audit)

The following owner branches were refreshed for this review. No separate TAR-AI-001 technology-review report was present in the B, I, D or E branch trees at the reviewed snapshots; their absence is recorded as **OPEN**, not treated as acceptance or as permission to infer conclusions.

| Owner | Branch HEAD | TAR-AI-001 technology report | Relevant current input |
|---|---|---|---|
| B | `861fa9b2c3e1f572336543b15c7dc392493891db` | OPEN — not present | `ADR-001-fact-claim-semantics.md`, blob `a1024938ff5baba069cf128c69496a44e143330c`, remains **ADR-BLOCKED** |
| I | `1fc3b3293ebf2077edfd6ad253647d382173d9fa` | OPEN — not present | PermissionEpoch formal confirmation, blob `bae6a24fe3a374bc816993979a8fa9af52517dea`, is normative I technical baseline; external governance profile approval remains blocked |
| D | `9dd48eddb3c8f91d15dfa6981a7f53cc70bd4bf8` | OPEN — not present | Forget semantics, blob `1f0391bc49d007c44ec74165bd33d37412cc7990`, define D authority; D/E/Storage implementation closure remains open |
| E | `4402549c39824b89a0dc49973226187c62e056c5` | OPEN — not present | Producer admission, blob `e59f517fff161ab882aa0ddc4a5bda513964ae1a`, and derived publication, blob `00e37ba56596e710513c8d0568acd79141d9101b`, explicitly retain atomic registration/publication as OPEN / BLOCKING |

These are current owner artifacts, not substitutes for the missing owner technology reviews. The Phase 3 D/E/H/I cross-module review remains a conditional integration review, not a closure of the D/E/Storage publication linearization gap.

## 2. Review Scope and Evidence

| Source | Ref / Blob SHA | Use |
|---|---|---|
| TAB-001 | main; blob `7b6f2d139217dbe13ab3a3af31bfbff525f20e71` | Adapter deployment and protocol/inference boundary candidates |
| TAR-AI-001 | main; blob `5a813edeccf7190d66dfd71a96ca581c48f8a4cb` | C full-owner assignment and R1–R6 requirements |
| Phase 3 D/E/H/I review | main; blob `edaccb802e0425f2d47bd4b613fab4dfde107144` | H/I identity and Forget integration dependencies |
| C Telemetry Event and Identity Contract | C branch; blob `2bd9e640bd0c1d2c8b768da1e06b06096bc2a79e` | Event semantics and identity claims |
| C Final Inference Boundary and Applied Attestation | C branch; blob `f3b254fcfd9a652a0ec68921e801f78d93bb5163` | Final request boundary, proof tuple and tiers |
| C Adapter Conformance Cases | C branch; blob `6569cb558805ca1247df07f17e3fafa15334528b` | Telemetry, identity, Applied, security and Forget test specifications |
| H Protocol Overview | H branch; blob `b88ef3a6fd3be293e7c2e77d9652f386b169bc47` | Tier and message-family compatibility |
| H Capability/Applied contract | H branch; blob `ed6b43a29aa368d772c701ffc83309a5aadf3c00` | H/C final proof alignment |

Phase 3 records H candidate baseline `fcc5103399b4c322e52d642cae5a2414969399a7` and I baseline `8c91d99e450ab5e8862bd6a3301fa193e28e6cbb`. C branch exact current HEAD was not returned by the GitHub file reader; no historical commit is substituted for it.

## 3. Six-Dimension Review Matrix

| Dimension | Verdict | Finding |
|---|---|---|
| R1 Requirements & workload fit | CONDITIONAL | Tiered telemetry, delivery and Applied semantics are precise; framework-specific hooks, concurrency, context-window/tokenizer and latency workloads remain unmeasured. |
| R2 Dependencies & boundaries | CONDITIONAL | C/H/G/I/B responsibilities are correctly separated; final submit proof depends on actual runtime hooks and jointly accepted schemas. |
| R3 Candidate technology selection | OPEN / TO_VALIDATE | Embedded SDK, sidecar and remote gateway are viable alternatives; no Agent-framework compatibility prototype selects a default. |
| R4 Resource constraints | OPEN / TO_VALIDATE | Prompt assembly, serialization, queue, tokenization, retries and sidecar overhead have no measured budgets. |
| R5 Failure recovery & safety | CONDITIONAL | Crash/reconnect/clear/unknown semantics are specified; implementation and adversarial tests have not run. |
| R6 Interface compatibility | CONDITIONAL | Applied binding tuple is explicit; H/I/G/B exact field types and capability epochs remain OPEN. |

## 4. Component Dependency Analysis

1. **C → E:** C defines telemetry/event meaning and authenticated producer context requirements; E owns durable Accepted receipt, idempotency and compilation. Telemetry is not automatically canonical Memory.
2. **C ↔ H:** C defines Agent-side final request boundary, tier semantics and protected-region requirements; H owns BMCP envelope, transport, SDK protocol behavior, capability negotiation and ACK encoding.
3. **G → C/H:** G owns Context membership, ContextVersion, ChangeSet and Delivery intent. C/H apply only the exact G target and return per-request evidence. Adapter local version counters do not own G state.
4. **I → C/H:** I owns authentication/authorization policy, issuer/delegation, PermissionEpoch and revocation. Payload ActorRef/Agent/Adapter/Scope claims are never credentials.
5. **B → C/H/I:** B owns typed ActorRef/ScopeRef semantics. C preserves typed references and environment identity but cannot decide their canonical meaning.
6. **D → C/H/G:** D owns canonical ForgetOperation/fence. C/H must check the current fence before final submit and on reconnect; an old Applied ACK cannot reverse later suppression.
7. **Agent runtime → C:** the host runtime must expose a stable hook after all request transformations and at the actual immutable submission handoff. Without this, the integration is Tier 2 or Tier 3 only.

## 5. Adapter Deployment Candidate Comparison

| Deployment | Advantages | Risks / limitations | Best-fit candidate |
|---|---|---|---|
| Embedded SDK/library | Lowest local hop latency; can integrate with prompt assembly and submit hooks; no extra process | Shares Agent process crash/security domain; Rust FFI and dependency/runtime conflicts; upgrades coupled to Agent | Tier 1 when framework exposes stable final-submit hooks and language bindings |
| Sidecar/local process | Centralized credentials, queue/retry, language-neutral IPC, process isolation and independent upgrades | IPC latency, process supervision, local socket/pipe auth, stale local queue and availability coupling | Strong default candidate for heterogeneous local deployments; Tier 1 only if Agent exposes trusted final-request handoff to sidecar |
| Remote gateway client | Central policy/protocol endpoint, easier centralized operations and remote Agent support | Network latency/outage, remote trust boundary, provider residency, reconnect/backpressure; cannot see final prompt unless Agent reports trusted hook evidence | Tier 2/3 by default; Tier 1 only with cryptographically verifiable runtime submit hook |
| Event/tool compatibility | Minimal framework changes and broad reach | Cannot observe final request or guarantee Context application; event gaps and stale state | Tier 3; no Full Applied |

Recommendation: support a language-neutral BMCP client contract, a Rust reference SDK, and at least one sidecar/IPC reference implementation. Treat embedded SDK as an optimization/integration profile, not the only supported topology. Remote gateway requires explicit I policy and transport authentication.

## 6. BMCP Transport and SDK Compatibility

| Candidate | Strengths | Risks | Disposition |
|---|---|---|---|
| HTTP(S) | Broad language/framework support, remote gateway friendly, standard TLS/proxy tooling | Network retry ambiguity, streaming overhead, auth configuration | RECOMMEND initial cross-language baseline |
| Unix domain socket / Windows named pipe | Efficient local IPC, OS permission model | Platform-specific peer identity and packaging | RECOMMEND local sidecar transport prototype |
| Loopback TCP | Portable local fallback | Port binding and local attack surface | CANDIDATE with authenticated channel |
| gRPC | Generated SDKs and streaming | Additional schema/runtime complexity | DEFER pending streaming need |
| Rust FFI/C ABI | Enables native Rust integration | ABI stability, ownership, panic containment, thread/runtime boundaries | CANDIDATE for embedded adapters; not universal |
| Language-native HTTP SDK | Works across Python/JS/Java/.NET/Go ecosystems | Duplicated SDK behavior unless shared conformance vectors exist | RECOMMEND as compatibility path |

Reconnect sequence must authenticate, negotiate protocol/capability epoch, obtain current I PermissionEpoch and D ForgetFence, reconcile G Context/Delivery, clear/suppress stale managed state, then apply only current authorized delivery. Offline ACK remains Pending/Unknown; absence of ACK is never success.

## 7. Inference Boundary and Applied Proof

The C proof boundary is the final immutable request after all transformations and immediately before/at actual handoff to the inference runtime/provider interface. The required binding tuple is:

`(inference_request_id, agent_instance_id, session_id, context_id, context_version_id, delivery_id, adapter_id, adapter_instance_id, capability_epoch, boundary_id)`

The attestation also needs exact managed-region digest/profile, submission evidence, current authenticated Principal/producer binding, PermissionEpoch, ForgetFenceGeneration, G delivery status and protected-region integrity.

Full Applied is valid only if:
- exact G ContextVersion and Delivery match;
- every required managed-region entry is present in the exact submitted request with no hidden truncation/substitution;
- request ID and runtime submission event are verifiable;
- adapter instance and capability epoch are bound;
- current I authorization and D Forget fence pass at the submit boundary;
- System/Developer/User/Agent policy and tool-authorization regions remain unchanged;
- evidence integrity and digest canonicalization are independently verifiable.

Tier 2 can observe a managed region but not final submission: Partial/Unknown only. Tier 3 reports transport/receipt states only. Applied is not model attention, comprehension, memory, agreement or behavioral use.

## 8. Context Safety and Prompt Injection

- Brain-managed Memory is untrusted data and must occupy an explicitly delimited region.
- Adapter MUST NOT overwrite, reorder into, or synthesize into System/Developer/User content, Agent policy, tool definitions, credentials or tool authorization.
- Memory text cannot grant tool permissions or invoke tools.
- If the framework cannot preserve region separation, reject application or report Bypassed/Unknown; do not silently merge content into privileged instructions.
- Prompt injection cannot be made impossible by formatting alone. I/Agent security own threat modeling and risk acceptance; C/H must provide observable isolation controls and adversarial tests.
- Context compaction must preserve provenance, uncertainty, conflict and untrusted labels; a summary cannot launder hostile instructions into trusted policy.
- Environment, Scope and session identity must be explicit to prevent cross-environment or cross-Agent leakage.

## 9. Resource Budget Analysis

No benchmark numbers are claimed. Measure and bound:
- prompt assembly cost = entries × rendering cost + provenance expansion + policy/fence checks;
- serialized bytes = managed-region bytes + metadata + envelope/signature overhead;
- per-session queue = pending delivery count × payload/evidence bytes × retry retention;
- adapter RAM = decoded Context + current/previous snapshot + delta staging + dedupe window + in-flight request copies;
- token budget = model context window − protected prompt/user/tool/output/safety reservations − managed-region budget; exact tokenizer profile is model/provider-specific;
- IPC/network cost = request rate × encoded bytes × retry/reconnect multiplier.

Enforce per-Agent/session queue and memory quotas, maximum payload/context size, explicit truncation reporting, cancellation on revocation/Forget, bounded retry and backpressure. 12–16 GB VRAM is reserved for optional local inference workloads; C must not assume unlimited GPU capacity or co-locate heavy prompt processing with model inference without measurement.

## 10. Failure & Recovery Matrix

| Failure | Authority / recovery source | Required behavior | Proposed test |
|---|---|---|---|
| Embedded Adapter crash | Agent runtime + G delivery ledger | Delivery becomes Unknown; reconcile exact request before retry | C-REC-01 |
| Sidecar crash/restart | Durable local queue + H/G/D/I current state | Reauthenticate and reconcile before replay | C-REC-02 |
| Remote gateway unavailable | Agent local policy + G pending delivery | Continue safely without memory; do not block Agent safety/action policy | C-REC-03 |
| Offline Adapter | H reconnect + current I/D/G authority | Pending/Unknown; clear stale state before current snapshot | C-RCN-01 |
| Lost ACK after successful submit | C final request evidence + H/G ledger | Query/recover exact request-bound proof; Unknown until verified | C-ACK-01 |
| Context update while offline | G ContextVersion and Delivery history | Old delivery superseded; full snapshot if base gap | C-RCN-02 |
| Forget/permission revoke before submit | D fence + I PermissionEpoch | Suppress, clear, reject old delivery and do not emit Full | C-FRG-01 |
| Runtime cannot expose final submit hook | Framework capability | Downgrade to Tier 2/3; Full forbidden | C-TIER-01 |
| Tokenizer/window changes | Model profile + G budget | Rebudget/re-render; Partial/Insufficient if overflow | C-BUD-01 |
| Malicious Memory attempts role/tool escalation | Agent policy and protected-region boundary | Data-only treatment; no protected-region mutation or tool grant | C-SEC-01 |

## 11. Interface Compatibility Findings

- H owns wire schema/transport; C owns telemetry semantics and inference boundary requirements. C's binding tuple must be represented by H without H inventing domain semantics.
- G owns ContextVersion and Delivery intent; C/H bind exact values but do not increment or reinterpret them.
- I owns authenticated identity, authorization and PermissionEpoch. Payload producer_id/ActorRef/Agent ID/ScopeRef are claims only.
- D owns ForgetFenceGeneration; C/H validate opaque owner-issued tokens and must not compare them numerically with PermissionEpoch or CapabilityEpoch.
- CapabilityEpoch changes whenever Adapter binary/configuration/hook/region isolation changes in a way that can invalidate previous proof capability. Old attestations remain tied to the prior epoch.
- Agent frameworks that expose only event/tool callbacks cannot claim Tier 1 Full Applied.
- Rust FFI is optional; language-neutral HTTP/IPC conformance vectors are necessary for Python/JS/Java/.NET/Go or other heterogeneous runtimes.
- Tokenizer differences require per-model profile, not a canonical Memory schema dependency.
- C cannot assert global Forget completion, provider prompt deletion or model forgetting.

## 12. Blocking Findings

| ID | Severity | Finding | Required closure |
|---|---|---|---|
| C-TAR-P1-001 | P1 | Final immutable request submission hook is framework-specific and no concrete Agent runtime adapter is tested | Select at least one reference framework/runtime and prove request ID + submit evidence |
| C-TAR-P1-002 | P1 | H/I/G/B binding and wire/permission schemas remain candidate/open | Joint owner mapping and cross-language conformance vectors |
| C-TAR-P1-003 | P1 | Adapter deployment topology and language SDK strategy not selected by comparative prototype | Embedded vs sidecar vs gateway prototype with crash/latency/security comparison |
| C-TAR-P1-004 | P1 | Forget/revocation clear and offline ACK semantics not end-to-end executed | H/G/I/D race and reconnect tests with unknown/unsupported targets |
| C-TAR-P1-005 | P1 | Protected-region and prompt-injection guarantees are design-only | Adversarial fixtures with before/after protected-region integrity evidence |
| C-TAR-P2-001 | P2 | Tokenizer/window and per-session resource limits are unmeasured | Multi-framework/model profile benchmark |
| C-TAR-P2-002 | P2 | Rust FFI ABI and sidecar lifecycle details need prototype | ABI ownership/panic tests and supervisor/restart tests |

## 13. Required ADRs

1. ADR-C-001: supported Adapter deployment profiles and Tier 1/2/3 qualification.
2. ADR-C-002: final inference request boundary and evidence profile, jointly C/H/G.
3. ADR-C-003: reference SDK language strategy and Rust FFI/C ABI constraints.
4. ADR-C-004: Agent framework compatibility matrix and conformance certification policy.
5. ADR-C-005: managed-region rendering/tokenizer/window budget profile and safe truncation.

## 14. Required Prototypes and Tests

- At least one concrete Agent framework integration proving final immutable request submission, request ID and region digest; one middleware-only Tier 2 profile and one event/tool Tier 3 profile.
- Embedded SDK vs sidecar IPC vs remote gateway comparison for latency, crash isolation, credentials, queue durability, reconnect and observability.
- Cross-language HTTP/IPC golden vectors for envelope, idempotency, capability negotiation and ACK.
- Applied verifier negative tests: missing/mismatched ContextVersion, Delivery, inference_request_id, Adapter instance, capability epoch, permission epoch, Forget fence, region digest, protected-region integrity or submit receipt.
- Offline/reconnect/Forget/permission revocation races, including late ACK and stale snapshot.
- Prompt-injection adversarial tests preserving System/Developer/User/Agent policy digests and tool authorization.
- Tokenizer/context-window matrix, Unicode/code/tool-output payloads, truncation and compaction.
- Crash tests for embedded process, sidecar restart, remote gateway outage and local queue exhaustion.

## 15. Verdict

**CONDITIONAL PASS** for C's Agent Integration architecture direction. C's semantic boundary and proof model are suitable for implementation planning. Tier 1 must be limited to concrete runtimes with final-submit observability; Tier 2/3 remain useful but cannot claim Full Applied. Do not freeze SDK topology, identity schema, transport or Applied wire format until P1 dependencies and prototypes close.

## 16. Evidence and Exact SHAs

- TAB-001 blob: `7b6f2d139217dbe13ab3a3af31bfbff525f20e71`
- TAR-AI-001 blob: `5a813edeccf7190d66dfd71a96ca581c48f8a4cb`
- Phase 3 D/E/H/I review blob: `edaccb802e0425f2d47bd4b613fab4dfde107144`
- C Telemetry contract blob: `2bd9e640bd0c1d2c8b768da1e06b06096bc2a79e`
- C Final Inference Boundary blob: `f3b254fcfd9a652a0ec68921e801f78d93bb5163`
- C Adapter Conformance Cases blob: `6569cb558805ca1247df07f17e3fafa15334528b`
- H Protocol Overview blob: `b88ef3a6fd3be293e7c2e77d9652f386b169bc47`
- H Capability/Applied blob: `ed6b43a29aa368d772c701ffc83309a5aadf3c00`
- C conformance documents specify TEL/EVT/IDN/APP/SEC/FRG/XMOD and PI35 test cases; **executed: none, passed: none claimed**.
