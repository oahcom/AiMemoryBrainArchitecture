# H — BMCP Protocol Technology Architecture Review

- Document: TAR-AI-001 / TAB-001 v0.1
- Owner: H — BMCP Protocol Architect
- Branch: `session-h-bmcp-protocol`
- Reviewed branch HEAD: **PENDING exact parent-SHA verification during report publication**; H branch exists and branch-local protocol artifacts were fetched.
- Review date: 2026-11-17
- Report version: 1.0
- Verdict: **CONDITIONAL PASS**
- Review mode: static protocol/contract review; no SDK, transport, cryptographic or fault tests executed.

## 1. Executive Summary

H's BMCP design is a viable transport-independent protocol candidate. The envelope separates protocol version, payload schema version, ContextVersion, PermissionEpoch, ForgetFence and CapabilityEpoch; authenticated transport identity is distinct from payload ActorRef/producer claims; delivery lifecycle distinguishes Prepared, Delivered, Applied, Rejected, Expired, Superseded and Unknown; reconnect requires current authorization/fence/context reconciliation before replay. These are sound foundations.

The design is not freeze-ready. JSON with RFC 8785 canonicalization is a candidate, not an approved wire encoding; HTTP, local IPC and gRPC need a workload/platform comparison; Principal/ActorRef/ScopeRef and PermissionEpoch depend on B/I; ContextVersion and Delivery semantics depend on G; final-request Applied proof depends on C and actual Agent runtime hooks. D's Forget fence and I's target/global completion policy remain separate authorities. A valid protocol document does not establish authenticated identity implementation, secure key management, adapter conformance, or reliable final-request evidence.

## 2. Review Scope and Evidence

| Source | Ref / Blob SHA | Use |
|---|---|---|
| TAB-001 | main; blob `7b6f2d139217dbe13ab3a3af31bfbff525f20e71` | Protocol/transport candidate direction |
| TAR-AI-001 | main; blob `5a813edeccf7190d66dfd71a96ca581c48f8a4cb` | H review requirements |
| Phase 3 D/E/H/I review | main; blob `edaccb802e0425f2d47bd4b613fab4dfde107144` | D/E/H/I identity and Forget dependency findings |
| H Protocol Overview | H branch; blob `b88ef3a6fd3be293e7c2e77d9652f386b169bc47` | Ownership, message families, tiers |
| H Envelope and Versioning | H branch; blob `5547ecd78d118bd63e571e5daad87194d9b694e4` | Envelope, JSON/JCS candidate, identity and replay |
| H Context Delivery and Acknowledgement | H branch; blob `bf9732cc39d156853b507c3a3a4e573159978f49` | Delivery state machine and ACK |
| H Adapter Capability and Applied Attestation | H branch; blob `ed6b43a29aa368d772c701ffc83309a5aadf3c00` | Capability epoch and Full Applied proof |
| H Forget, Revocation and Offline Reconnect | H branch; blob `695909360782987781e259187041618f495f1c8c` | Suppression, clear ACK and reconnect |

Phase 3's earlier cross-module report records H design baseline `fcc5103399b4c322e52d642cae5a2414969399a7`; the current H branch HEAD was not independently returned by the GitHub file API and is not inferred from that historical commit.

## 3. Six-Dimension Review Matrix

| Dimension | Verdict | Finding |
|---|---|---|
| R1 Requirements & workload fit | CONDITIONAL | Envelope, delivery, retry, negotiation and offline semantics are described; payload size, message rates, connection counts, latency and retention horizons are unquantified. |
| R2 Dependencies & boundaries | CONDITIONAL | H respects G/C/I/D/B/E ownership; several required fields remain OPEN pending owner mappings. |
| R3 Candidate technology selection | OPEN / TO_VALIDATE | JSON/JCS, CBOR/MessagePack, HTTP, IPC and gRPC are compared conceptually but no interoperability/throughput/security prototype exists. |
| R4 Resource constraints | OPEN / TO_VALIDATE | Serialization/crypto overhead, buffering, durable queue size, reconnect bursts and evidence retention are not measured. |
| R5 Failure recovery & safety | CONDITIONAL | Retry/reconnect/Unknown semantics are strong; persistence, exactly-once-effect boundary, key rotation and partial failure require executable tests. |
| R6 Interface compatibility | CONDITIONAL | Version and epoch namespaces are separate; exact typed identity/permission/fence/context wire schema remains unfrozen. |

## 4. Component Dependency Analysis

1. **I → H:** I provides authenticated transport principal binding, authorization decision, Principal/ActorRef/ScopeRef semantics, PermissionEpoch, revocation, retention and global target policy. H transports and validates references but cannot define grants or mint epochs.
2. **B → H:** B owns typed ActorRef/ScopeRef and domain reference semantics. Payload identity fields remain claims and must be compared with authenticated transport binding.
3. **D → H:** D owns ForgetOperation and ForgetFenceGeneration. H treats fence tokens as opaque and uses owner-defined comparison/validation; it does not increment or numerically compare them.
4. **G → H:** G owns Context ID/ContextVersion/ChangeSet/Delivery intent. H transports snapshots/deltas, enforces exact base/target and reports Adapter outcomes.
5. **C → H:** C owns telemetry meaning and final inference boundary semantics. H encodes the attestation and capability contract; Tier 1 Full requires runtime submission evidence, not Adapter buffer state.
6. **E → H:** E owns durable Accepted receipt/idempotency semantics. H carries idempotency metadata but cannot conflate receipt with compile or canonical commit.
7. **H internal:** transport authentication → version/capability negotiation → envelope validation/integrity → family validation → owner authorization/semantic check → Adapter state transition → ACK/evidence. Every boundary rechecks expiry, idempotency and current governance epochs.

## 5. Candidate Technology Comparison

### Encoding

| Candidate | Strengths | Risks / limits | Disposition |
|---|---|---|---|
| JSON + RFC 8785 JCS | Debuggable, broad language support, canonical hashing profile available | Duplicate keys/number/timestamp normalization and signature profile must be strict; payload size | RECOMMEND first interoperability prototype, not freeze |
| CBOR | Compact typed binary encoding; suitable for constrained IPC/network | Canonical CBOR profile, cross-language diagnostics and schema tooling need definition | CANDIDATE if measured payload/CPU savings matter |
| MessagePack | Broad ecosystem and compactness | Less explicit canonicalization/schema discipline unless profile is added | CANDIDATE; lower priority than CBOR |
| Protobuf/gRPC schema | Generated SDKs, typed evolution and streaming ecosystem | Adds RPC/schema coupling; JSON/JCS evidence digest still needs defined canonical representation | CANDIDATE only if streaming/SDK needs justify |

### Transport

| Candidate | Strengths | Risks / limits | Disposition |
|---|---|---|---|
| HTTP(S) | Universal client support, proxies, observability, remote gateway fit | Connection/streaming overhead and retry ambiguity; TLS/auth configuration critical | RECOMMEND first remote/interoperability path |
| Unix domain socket / Windows named pipe | Local IPC, OS access controls, low overhead | Platform-specific implementation and credential mapping; Windows/Unix parity | RECOMMEND local transport prototype behind common interface |
| Loopback TCP | Cross-platform local fallback | Port binding, local threat surface and process identity concerns | CANDIDATE fallback with authenticated channel |
| gRPC | Bidirectional streaming and generated SDKs | More runtime/proxy complexity and schema toolchain | DEFER until measured need |

### SDK / runtime

- Rust core SDK is suitable for native Agent integrations and Brain host.
- Non-Rust Agent ecosystems need language-neutral HTTP contract and/or stable C ABI. Rust FFI must define ownership, panic containment, ABI versioning and thread/runtime rules.
- Sidecar can centralize credentials and protocol state but adds process supervision and local IPC; embedded library has lower latency but shares Agent process failure/security domain.
- No single deployment mode is universally optimal.

## 6. Resource Budget Analysis

No measured values are available. Size using:
- wire bytes/sec = message rate × mean encoded payload bytes × retry multiplier;
- durable queue disk = pending delivery count × retained payload/evidence bytes × retry/retention factor;
- memory = concurrent sessions × per-session state + in-flight decoded payloads + dedupe window + bounded outbound queues;
- reconnect burst = offline queued operations / reconnect window, bounded by rate limit and backpressure;
- crypto CPU = authenticated messages/sec × measured canonicalization + digest + signature verification cost.

Enforce maximum message size, bounded decompression, queue count/bytes, per-Principal rate limits, retry budgets, expiry, evidence size and retention. Do not buffer unlimited offline Context payloads. GPU VRAM is not a BMCP budget; inference worker scheduling remains separate.

## 7. Failure & Recovery Matrix

| Failure | Authority / recovery source | Required behavior | Proposed test |
|---|---|---|---|
| Network timeout after send | Stable message/delivery ID + recipient dedupe | Record Unknown; query/reconcile, do not infer delivery/application | H-REC-01 |
| Duplicate retry | Owner idempotency key + canonical payload digest | Same key/same digest returns prior result; changed digest conflicts | H-IDEM-01 |
| Reconnect after long offline period | I current identity/PermissionEpoch, D fence, G Context target | Authenticate, negotiate, fence/clear, reconcile, then apply current snapshot only | H-RCN-01 |
| Unsupported protocol major | Negotiated protocol contract | Reject state-changing traffic; no silent downgrade | H-COMP-01 |
| Unknown security enum/field | Versioned schema and I policy | Fail closed | H-SEC-01 |
| Adapter crash after buffer update before submit | C final-request boundary | Unknown/Partial; no Full Applied | H-APP-01 |
| Late ACK after supersession | G delivery history/current target | Historical evidence only; cannot roll back current target | H-ACK-01 |
| Stale PermissionEpoch / ForgetFence | I/D authoritative tokens | Reject or reconcile; no numeric cross-domain comparison | H-GOV-01 |
| Signature/key rotation | I key custody/rotation policy | Accept only valid active/retained verification keys under I policy | H-KEY-01 |
| Oversized/compressed payload bomb | Envelope size/decoder limits | Reject before unbounded allocation; emit sanitized error | H-ROBUST-01 |

## 8. Interface Compatibility Findings

- Keep protocol_version, payload_schema_version, ContextVersion, PermissionEpoch, ForgetFenceGeneration, CapabilityEpoch, Delivery ID/attempt, inference_request_id and source sequence separately typed.
- Principal/ActorRef/ScopeRef/ProducerIdentity are not frozen until B/I define typed refs and authenticated issuer/delegation mapping.
- ACK status is per-delivery/per-attempt. Delivered means endpoint transport acceptance; Applied means an accepted application attestation at declared coverage; neither means model attention or use.
- Full Applied binds exact ContextVersion, Delivery, inference_request_id, Agent/session, Adapter identity/instance, CapabilityEpoch, PermissionEpoch, ForgetFenceGeneration, managed-region digest, final-request submission evidence and protected-region integrity.
- The H candidate ACK classes SUPPRESSED, LOCAL_BUFFER_CLEARED, LOCAL_CACHE_PURGED, QUEUED_DELIVERY_CANCELLED, FAILED, UNKNOWN and UNSUPPORTED are local observations; I must map them to global target states.
- ProducerDomainInventoryEpoch (I), D per-work-item barrier/high-water, D ForgetFenceGeneration and F IndexWatermark are distinct and cannot be compared or substituted.
- Retry/replay must reauthorize and recheck fence/expiry/current Context base. Deduplication retention and idempotency namespace belong to operation owners.
- C's final-request boundary definition is compatible with H Tier 1; Tier 2 cannot claim Full.

## 9. Blocking Findings

| ID | Severity | Finding | Required closure |
|---|---|---|---|
| H-TAR-P1-001 | P1 | Authenticated Principal/ActorRef/ScopeRef/PermissionEpoch mapping is not approved | B/I/H decision and forged-identity/issuer/delegation tests |
| H-TAR-P1-002 | P1 | ContextVersion/Delivery and final Applied proof depend on exact G/C/H/I binding | Joint schema/profile and independent verifier tests |
| H-TAR-P1-003 | P1 | Forget ACK taxonomy not mapped to I global target inventory and D barrier | I/H/D/G mapping with Unknown/Unsupported/offline negative cases |
| H-TAR-P1-004 | P1 | Encoding/transport selection has no interoperability or performance evidence | JSON/JCS HTTP+IPC prototype; compare CBOR/gRPC only against measured criteria |
| H-TAR-P2-001 | P2 | Queue/evidence retention and reconnect backpressure budgets are unmeasured | Burst/reconnect/resource benchmark |
| H-TAR-P2-002 | P2 | Cryptographic profile/key rotation/OS secret custody remain I-dependent | Security ADR and key lifecycle tests |

## 10. Required ADRs

1. ADR-H-001: canonical envelope and JSON/JCS signing/digest profile; optional binary profile compatibility.
2. ADR-H-002: HTTP + local IPC transport profile and authenticated peer identity mapping.
3. ADR-H-003: protocol/schema evolution, required-field and unknown-enum compatibility rules.
4. ADR-H-004: ACK/evidence schema and Full Applied verifier profile, jointly C/G/I.
5. ADR-H-005: offline queue retention, dedupe horizon, retry/backpressure and capability epoch rules.

## 11. Required Prototypes and Tests

- JSON/JCS cross-language golden vectors including duplicate keys, Unicode, number/timestamp edge cases, canonicalization and signatures.
- Rust SDK + one non-Rust SDK/client conformance against the same vectors.
- HTTP and local IPC transport with authenticated identity mapping, reconnect and bounded retry.
- Capability negotiation downgrade/unknown-feature tests.
- Delivery ledger with lost ACK, duplicate ACK, timeout, late ACK, supersession and process crash.
- Full Applied verifier negative tests for every missing/mismatched binding field and final-submit evidence.
- Forget/revocation offline reconnect and Adapter clear matrix, including unsupported/unknown outcomes.
- Fuzz envelope/parser/decompression and test size/rate/queue exhaustion.

## 12. Verdict

**CONDITIONAL PASS** for BMCP architecture direction. H may prototype transport-independent contracts, JSON/JCS, HTTP and local IPC candidates. No encoding, transport, identity schema, ACK evidence profile or security guarantee is frozen. P1 findings block protocol freeze and implementation sign-off.

## 13. Evidence and Exact SHAs

- TAB-001 blob: `7b6f2d139217dbe13ab3a3af31bfbff525f20e71`
- TAR-AI-001 blob: `5a813edeccf7190d66dfd71a96ca581c48f8a4cb`
- Phase 3 D/E/H/I review blob: `edaccb802e0425f2d47bd4b613fab4dfde107144`
- H Protocol Overview blob: `b88ef3a6fd3be293e7c2e77d9652f386b169bc47`
- H Envelope blob: `5547ecd78d118bd63e571e5daad87194d9b694e4`
- H Delivery/Acknowledgement blob: `bf9732cc39d156853b507c3a3a4e573159978f49`
- H Capability/Applied blob: `ed6b43a29aa368d772c701ffc83309a5aadf3c00`
- H Forget/Reconnect blob: `695909360782987781e259187041618f495f1c8c`
- Historical H branch baseline in Phase 3 review: `fcc5103399b4c322e52d642cae5a2414969399a7` (not asserted current).
- Current branch HEAD: pending exact commit-parent verification; no fabricated SHA.
- No protocol, cryptographic, SDK, fault-injection or performance tests executed.
