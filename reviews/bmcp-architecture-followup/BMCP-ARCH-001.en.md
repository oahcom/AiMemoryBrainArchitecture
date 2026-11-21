# BMCP Architecture Completion — Semantic Contract & Engineering Handoff

- Work Item: BMCP-ARCH-FOLLOWUP-001; Document: BMCP-ARCH-001; Version: 0.2.0
- Status: CANDIDATE / ARCHITECTURE_PARTIAL — not a frozen protocol specification
- Main baseline: c138654c942dc93b5a36eccb2ff0e41452156429
- H source snapshot: session-h-bmcp-protocol @ 3e8b33df18b9e6fc757ca84ff07a12faebc78e74
- Peers: [中文版本](BMCP-ARCH-001.zh-CN.md) | [English](BMCP-ARCH-001.en.md)
- Scope: architecture semantics, phase boundaries, dependency map, acceptance plan and engineering handoff.
- Excluded: Runtime code; H-owned normative wire/schema/transport/ACK/Validator edits; D/I authority changes; C's Agent/MCP-to-BMCP mapping decision. Owner Fact/Claim semantics are already decided; exact consumer/wire mapping remains Candidate.

## 1. Disposition

**ARCHITECTURE_PARTIAL.** This is a candidate semantic synthesis and engineering handoff, not a protocol freeze.

H's live branch contains candidate Envelope, versioning, canonicalization, error taxonomy, Delivery/ACK, Forget/reconnect, strict JSON parser reference and conformance material. These files remain H-owned; their existence is not approval or freeze. H's lifecycle handoff says Wire Schema NOT FROZEN; its conformance matrix is a candidate test specification, not Runtime evidence.

The merged Owner semantic decision approves Fact/Claim Option A + I1; exact compiler/domain consumer mapping remains Candidate. BMCP MUST NOT freeze canonical Fact/Claim wire payload fields. D owns Canonical Identity/Lifecycle and D Forget Fence; I owns authorization and PermissionEpoch. BMCP consumes those authorities and MUST NOT create substitutes.

Issue #7's recorded binding remains IMPLEMENTATION_BINDING=DEFERRED_TO_ENGINEERING_PHASE. GitHub currently reports Issue #7 CLOSED / not_planned under the Owner phase-closure ruling; this work does not reopen or alter it. Deferral is not Runtime authorization.

**Canonical name:** the repository canonical terminology at `00-governance/terminology.md` defines BMCP as **Brain Memory Context Protocol** (main `c138654c942dc93b5a36eccb2ff0e41452156429`, terminology Blob `b8770fbb58e4fac087698043c40a57531b1d244d`). The initial dispatch phrase “Brain Memory Control Protocol” is non-canonical for this repository and is rejected. H must retain “Context” in protocol documentation; no naming decision remains open.

## 2. Exact source ledger

Main pins are from fetched origin/main at c138654c942dc93b5a36eccb2ff0e41452156429. H pins are from H branch session-h-bmcp-protocol @ 3e8b33df18b9e6fc757ca84ff07a12faebc78e74.

| Source | Ref | Blob SHA | Status / use |
|---|---|---|---|
| docs/en/08-bmcp-protocol/bmcp-guide.md | main | 228d28671955c977f653bef5b537554e431f9137 | CANDIDATE overview / H ownership |
| 08-bmcp-protocol/protocol-overview.md | H 3e8b33df18b9e6fc757ca84ff07a12faebc78e74 | b88ef3a6fd3be293e7c2e77d9652f386b169bc47 | CANDIDATE |
| 08-bmcp-protocol/message-envelope-and-versioning.md | same H ref | 5547ecd78d118bd63e571e5daad87194d9b694e4 | CANDIDATE; H-owned |
| 08-bmcp-protocol/context-delivery-and-acknowledgement.md | same H ref | bf9732cc39d156853b507c3a3a4e573159978f49 | CANDIDATE; G semantics / H wire |
| 08-bmcp-protocol/adapter-forget-ack-and-target-binding.md | same H ref | 5e2b33898cbc6a9c95e271ecd1d8a092d04c67f8 | CANDIDATE; H wire, D/I/G authority |
| 08-bmcp-protocol/phase-3.7-h-lifecycle-handoff-envelope-semantics-not-frozen.md | same H ref | b2a2648d5576511f68fdb9d87ce4388a1fedd5e9 | NOT FROZEN |
| 08-bmcp-protocol/protocol-conformance-matrix.md | same H ref | 075b2ac6ebe9bda4ec83de04fad07e8027e6a440 | CANDIDATE tests; no Runtime PASS |
| 08-bmcp-protocol/runtime_reference/strict_json_parser.py | same H ref | 3b9b3da645448c773c95a9dcd3c57c8c109bb2da | Reference model, not production transport |
| docs/en/04-memory-compiler/README.md | main | 5f50d470bf26d46dfffad48ad23059fc7a36c489 | E/D/I ownership |
| docs/en/04-memory-compiler/compiler-overview.md | main | c89a256afda105ceac3db75d743ab58d177ef586 | E pipeline |
| docs/en/04-memory-compiler/accepted-receipt-and-idempotency-contract.md | main | f2a4007f4b17e33de9bcd183c57ee504cfeef6cd | CANDIDATE E receipt |
| docs/en/07-agent-integration/agent-integration-guide.md | main | c4e076887634a9e8e46df076efb0f4b70d816e0a | C-owned Agent boundary |
| docs/en/03-memory-brain/forget-fence-and-completion-contract.md | main | c791895333ab6140f035f4f622d5dee9325d422d | D/I Forget boundary |
| docs/en/03-memory-brain/forget-fence-operation-and-publication-gate.md | main | 9c054932994bb078e2834df8bd66f73895aa04f5 | D lifecycle/Fence |
| 13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/fact-claim-identity-adr.md | main | 958e7f3a3a909ee5b6d9fb38ebf3a72b3a9bd593 | historical ADR; semantic decision superseded; consumer mapping Candidate |
| 14-ai-development/adr/OWNER-DECISION-FACT-CLAIM-001.md | main @ `c138654c942dc93b5a36eccb2ff0e41452156429` | Blob `d59756a8eb454480804c482ca03c68345ab5abf2` | Approved Owner semantic selection: Option A + I1; does not freeze schema |
| docs/en/03-memory-brain/memory-versioning.md | main | 4efbd26db9586f6fcf1897f42ffba287d625b903 | D revision/consumer freeze boundary |
| docs/en/03-memory-brain/commit-cursor-semantics.md | main | 2de7fe35229372ae5b06093e5e031c2c243fbd7c | D cursor semantics |
| docs/en/09-security-governance/security-governance-guide.md | main | 061c5847b3df879eeaf3c71e5eae0bfa162b276a | I Principal/authorization/PermissionEpoch |
| docs/zh-CN/09-security-governance/security-governance-guide.md | main | 372d27c79dc79d09bcdb0f142c979efdba1c2b6e | I bilingual peer |
| 07-agent-integration/agent-integration-overview.md | main | 073ff4ddf71fbcaf959107bb06ab724bfa48e63b | C canonical Agent boundary |
| 07-agent-integration/adapter-capability-tiers.md | main | 09c5932350c48f950ee16f6b246f54e661f0c420 | C capability tiers |
| 07-agent-integration/inference-boundary-model.md | main | e2d5cb6abd9ec40da6e3680531de5944fc8b14df | C inference boundary |
| 07-agent-integration/telemetry-model.md | main | 9bb4a77e4bd79caaf3e1faeaf77c6b42858998f0 | C telemetry |
| 14-ai-development/adr/OWNER-DECISION-FACT-CLAIM-001.md | main | d59756a8eb454480804c482ca03c68345ab5abf2 | Approved semantic decision; Option A + I1 |
| PR #436 protocol index/provider_outcome tests | PR head 1ffed9ed127df98b2f823a66ec80ea43d08cb9dc | open, not merged | structural-only provider outcome evidence |

This is a bounded source ledger, not a claim that every H artifact or consumer was independently reviewed.

## 3. File ownership matrix and allowed changes

| File / area | Owner | This work item | Boundary |
|---|---|---|---|
| 08-bmcp-protocol/** | H | Read only | No H schema, validator, ACK, transport or spec edits |
| docs/{en,zh-CN}/08-bmcp-protocol/** | H / docs governance | Read only | No guide/status rewrite |
| 04-memory-compiler/** and compiler docs | E; dependent semantics B/D/I | Read only | No Compiler or Fact/Claim changes |
| 07-agent-integration/** and C contract | C | Read only | No Agent/MCP policy changes |
| D Memory Brain / Forget contracts | D | Read only | No identity/lifecycle/Fence changes |
| I authorization / PermissionEpoch | I | Read only | No Principal/permission/global Forget changes |
| reviews/bmcp-architecture-followup/BMCP-ARCH-001.en.md | This BMCP architecture work item | Create | Candidate synthesis / handoff only |
| reviews/bmcp-architecture-followup/BMCP-ARCH-001.zh-CN.md | Same | Create | Semantic peer |
| docs/governance/translation-status.md | Governance register | Metadata-only | Register review pair; preserve H core-spec status |

No Rust source, tests, JSON Schema, transport/validator implementation or production configuration is in scope.

## 4. Parse / Execute / Respond contract

### 4.1 Layer boundary

1. **Wire / Transport Decode — H:** framing, channel authentication, bytes-to-text/UTF-8 decoding, strict wire syntax, canonicalization/integrity and envelope decoding.
2. **Protocol Parse — BMCP semantic layer:** accepts only a decoded envelope plus protected authenticated peer context; checks protocol requiredness, version/capability compatibility and registered family/operation; normalizes a typed request.
3. **Execute — operation owner/service:** routes to an allowlisted handler; obtains I authorization; validates D identity/lifecycle/Fence; invokes the owning domain service.
4. **Respond — BMCP semantics + H serialization:** builds a correlated business result or classified error. H owns wire representation and serialization.
5. **ACK — H evidence family:** independently reports transport or Adapter observation. ACK is not the business response or domain receipt.

Raw bytes MUST NOT enter BMCP semantic Parse. Co-location in a future process does not merge these authorities.

### 4.2 Parse

**Input:** H-decoded envelope and protected authenticated transport context. Payload identity is an assertion only; authenticated Principal comes from trusted channel/security context and I binding.

**Candidate logical fields:** protocol family/version; message identity; family+operation discriminator; payload and payload schema/content type; correlation and optional causation; idempotency tuple for state-changing operations; source/recipient selectors; conditional Scope/Environment refs; applicable owner-issued PermissionEpoch, ForgetFence, ContextVersion, CapabilityEpoch; expiry and integrity result.

H's candidate envelope names protocol, protocol_version, message_id, message_type, payload_content_type, payload_schema_version, payload, correlation_id, causation_id, idempotency, scope_ref, permission_epoch, forget_fence and capability_epoch. These are source names, **not approved field names/requiredness/schema**.

**Normalized internal request (not a wire schema):**

| Member | Meaning | Authority |
|---|---|---|
| protocol_version | negotiated version | H |
| message_id | immutable message identity; candidate request correlation key | H |
| correlation_id / causation_id | workflow correlation / immediate causal parent | H |
| operation_ref | registered family + operation | H registry; semantic owner defines operation |
| parameters | typed payload; opaque until owner validation | operation owner |
| idempotency_ref | owner-scoped key + canonical semantic digest | operation owner; H transports |
| authenticated_principal | protected peer identity, never payload-derived | I-approved binding |
| scope_ref / environment_ref | opaque typed domain refs | B/I/D as applicable |
| permission_epoch | I-issued authorization freshness | I |
| forget_fence_ref | D-issued barrier evidence with I policy binding as required | D/I |
| context_version / capability_epoch | independent opaque tokens | G / H |

Message identity, negotiated version, registered operation and typed payload are required at the semantic boundary. Correlation is required for multi-message/asynchronous operations. Idempotency is required for state-changing/retryable operations. Scope, Environment, PermissionEpoch, ForgetFence, ContextVersion and CapabilityEpoch are conditionally required by the operation owner; no wildcard default may be invented. Causation and namespaced non-critical extensions may be optional. Unknown critical fields/enums/operations fail closed under H's eventual compatibility contract.

Parse failures: malformed decoded envelope; missing required field; unsupported version; unknown operation; unsupported critical extension; invalid parameter shape; expired request. Parse MUST NOT call memory services, authorize side effects, mint identities or mutate domain state.

H's candidate negotiation forbids silent major downgrade. Exact major/minor/patch and payload-schema negotiation remain H-owned.

**H request-ID question:** current envelope defines message_id, not a separate request_id. H must decide whether message_id is the request identity referenced by response causation_id, or whether a distinct stable command identity is required. BMCP MUST NOT add a wire request_id unilaterally.

### 4.3 Execute

Execute begins only after Parse succeeds. This is a semantic dispatch contract, not a Runtime scheduler specification.

1. Resolve operation_ref through a versioned allowlisted registry; unknown/disabled operations reject before side effects.
2. Use protected authenticated identity and ask I's approved interface for current authorization and PermissionEpoch. Payload Principal/Actor/Producer/Scope claims do not authenticate themselves.
3. Invoke the operation owner's validator. H validates protocol/wire structure, not domain truth or business permission.
4. For canonical Memory operations, use D-owned identity/lifecycle/revision operations. BMCP does not mint CanonicalRef, choose lifecycle transitions or allocate canonical cursors.
5. Revalidate D Forget Fence and I authorization/PermissionEpoch at every D/I-protected boundary, including immediately before irreversible/visibility-changing work. Stale, unavailable, incomparable or unknown results block the action. D Fence and I PermissionEpoch are distinct typed namespaces; never compare/coerce/substitute.
6. Call the owning service (e.g. E ingress/receipt, D canonical lifecycle, G Context/Delivery). BMCP does not write canonical storage directly or implement the service state machine.
7. Same owner-scoped idempotency key + same semantic digest returns original operation/receipt without repeating side effects. Same key + different digest is conflict. Resolve uncertain commits using the same key and authoritative lookup; never mint a new key to escape UNKNOWN.
8. Timeout, lost response, process loss or uncertain durable outcome remains UNKNOWN until owner reconciliation. Timeout proves neither failure, abort, success nor non-invocation. Never blindly retry non-idempotent effects.
9. Concurrency follows owner CAS/sequencer/fence/transaction rules. BMCP message order, wall-clock time and correlation IDs are not domain commit order. Cancellation is not rollback.
10. Return the actual owner receipt/result without upgrading its meaning. E AcceptedReceipt means durable ingress acceptance under E's contract; it does not mean compile, canonical commit, publication or Applied.

No concrete operation catalogue or callable Runtime service API is frozen here.

### 4.4 Respond

A business response is the semantic result of an operation; an ACK is a separate transport/Adapter observation.

Logical response: negotiated protocol version; new immutable response message identity; request association; operation discriminator; mutually exclusive success/result or failure/error; owner-issued result/receipt/evidence refs; and H-approved safe retry metadata.

**Candidate correlation:** response causation_id references request message_id; response correlation_id preserves workflow correlation; response has its own message_id. H must confirm; this is not a frozen wire rule.

Success exists only when the operation owner returns its defined successful terminal/receipt. Transport send success, HTTP 2xx, queue acceptance or ACK receipt is not business success. Failure preserves the owner's outcome and distinguishes pre-execution rejection, domain conflict, authorization denial, timeout/unknown and internal failure. UNKNOWN must not become definitive success/failure.

H owns response field names, encoding, canonicalization, signatures, versioning and transport. Redact protected payloads, secrets, credentials, internal paths and cross-scope existence. Existence disclosure follows I policy. Stable code, correlation and retryability are returned only when safe; detailed diagnostics stay in protected logs.

## 5. ACK, Validator and error semantics

### 5.1 ACK (H-owned)

H's candidate design distinguishes Prepared/Delivered/Applied/Rejected/Expired/Superseded/Unknown and separate Forget ACK classes such as SUPPRESSED, local buffer/cache/queue action, FAILED and UNKNOWN. A Forget ACK is not an Applied ACK.

| Question | Current evidence | Disposition |
|---|---|---|
| Purpose | bounded observation for one identified message/delivery/action | H candidate |
| Receipt? | some ACKs report transport/delivery receipt; boundary varies by family | H must map each family |
| Execution complete? | no general inference | H confirmation |
| Durable persistence? | only owner-specific receipt proves its durable boundary | E/Storage + H mapping |
| Timeout/lost ACK | Unknown until reconciliation | H candidate; retry profile H-owned |
| Duplicate ACK | same stable ACK ID+digest idempotent; same ID/different digest conflict | H candidate; consumer owns state |
| Correlation | exact operation/delivery/attempt/session/target/evidence tuple | H wire mapping; D/G/I consume |

H must confirm ACK families, evidence boundary, persistence point, correlation tuple, retry horizon, replay/retention and consumer mapping. This document does not design ACK.

### 5.2 Validator layers

| Layer | Owner | Input | Output / failure |
|---|---|---|---|
| Transport framing, byte decode, UTF-8, duplicate-key/canonical JSON, integrity, authenticated channel | H using I-approved trust | raw bytes/channel | decoded authenticated envelope or wire rejection; no business execution |
| Envelope structure, protocol version, required/critical fields, registered family | H | decoded envelope | protocol-valid envelope or H error |
| Operation parameter shape/schema | H for protocol schema mechanics; operation owner for semantic constraints | typed payload + registry entry | valid shape or validation rejection; schema version pinned |
| Business authorization / PermissionEpoch | I | authenticated Principal + operation + scope + current epoch | allow/deny/unknown; unknown fail-closed |
| Canonical identity/lifecycle/Forget Fence | D; I for policy binding | typed canonical refs + operation + fence context | owner-authenticated validity/currentness or reject/unknown |
| Fact/Claim schema and identity | B decision, D identity/lifecycle, E candidate producer | Candidate IR / proposed canonical object | BLOCKED until ADR and consumer acceptance |
| ContextVersion / ChangeSet / Delivery | G | Context payload + exact base/target | G validation result; H only encodes/transports |
| Runtime result/receipt | executing domain owner | validated and authorized operation | owner result/receipt; H Validator cannot infer |

H Validator MUST NOT become the business authorization engine, canonical schema authority or Forget/PermissionEpoch authority.

### 5.3 Error taxonomy (candidate crosswalk, not frozen enum)

H's candidate envelope lists ENVELOPE_INVALID, VERSION_UNSUPPORTED, MESSAGE_TYPE_UNSUPPORTED, REQUIRED_FIELD_UNSUPPORTED, ENUM_UNSUPPORTED, INTEGRITY_FAILED, AUTHENTICATION_FAILED, IDENTITY_BINDING_MISMATCH, NOT_AUTHORIZED, PERMISSION_EPOCH_STALE, FENCE_STALE, CONTEXT_BASE_MISMATCH, DUPLICATE_REPLAY, IDEMPOTENCY_CONFLICT, EXPIRED, SUPERSEDED, RATE_LIMITED, RESOURCE_EXHAUSTED, TRANSIENT_UNAVAILABLE and INTERNAL_ERROR. They remain candidate pending H's exact versioned contract.

| Requested class | Existing H candidate / gap | Status |
|---|---|---|
| INVALID_REQUEST | ENVELOPE_INVALID; alias/scope needs H | BLOCKED_BY_H_CONTRACT |
| UNSUPPORTED_VERSION | VERSION_UNSUPPORTED | BLOCKED_BY_H_CONTRACT |
| INVALID_PARAMETERS | no exact generic code; owner-specific validation may apply | BLOCKED_BY_H_CONTRACT |
| UNKNOWN_OPERATION | MESSAGE_TYPE_UNSUPPORTED | BLOCKED_BY_H_CONTRACT |
| UNAUTHORIZED | distinguish authentication from I policy denial: AUTHENTICATION_FAILED vs NOT_AUTHORIZED | BLOCKED_BY_H_CONTRACT |
| FORBIDDEN | candidate NOT_AUTHORIZED; I controls concealment vs not-found | BLOCKED_BY_H_CONTRACT |
| NOT_FOUND | no generic H code confirmed; I controls existence disclosure | BLOCKED_BY_H_CONTRACT |
| CONFLICT | specific candidates IDEMPOTENCY_CONFLICT, CONTEXT_BASE_MISMATCH, FENCE_STALE, SUPERSEDED; no frozen generic code | BLOCKED_BY_H_CONTRACT |
| VALIDATION_FAILED | keep protocol, domain-schema, authorization and integrity failures distinct | BLOCKED_BY_H_CONTRACT |
| EXECUTION_FAILED | owner defines definitive failure vs UNKNOWN; H mapping unconfirmed | BLOCKED_BY_H_CONTRACT |
| TIMEOUT | uncertain side-effect boundary means UNKNOWN; TRANSIENT_UNAVAILABLE does not prove failure | BLOCKED_BY_H_CONTRACT |
| INTERNAL_ERROR | candidate INTERNAL_ERROR; redaction/retry policy needs H | BLOCKED_BY_H_CONTRACT |

Conceptual error response: stable code, retryable flag, optional safe retry-after, correlation ref and sanitized detail. Exact fields, mapping and retry policy belong to H. Do not ship requested labels as wire enums without H approval.

## 6. Cross-module dependency matrix

| Module | Authority | BMCP consumes / interaction | Open dependency |
|---|---|---|---|
| H | wire envelope/version, transport, ACK encoding, Validator, protocol conformance | authenticated decoded envelope; family registry; response/ACK serialization | exact Wire/Transport/ACK/Validator remains CANDIDATE / NOT FROZEN |
| E | ingress acceptance, Candidate IR, compiler stages/lineage, AcceptedReceipt | typed ingress operation; return E receipt/result unchanged | callable API and wire mapping; AcceptedReceipt is not canonical commit |
| B | Fact/Claim meaning and canonical domain decisions | only owner-approved typed refs/payloads | Owner decision Option A + I1 approved; exact consumer mapping Candidate |
| D | canonical identity, lifecycle, canonical commit/revision, Forget Fence | pass typed refs to D and consume D receipts/currentness | exact Runtime API binding |
| I | Principal trust, authorization, PermissionEpoch, revocation, global Forget policy | protected principal context and current authorization decision | exact approved interface/profile |
| C | Agent/Adapter boundary, telemetry, final inference request | C adapter maps Agent request to registered BMCP operation | MCP/Adapter mapping and request identity |
| G | Context membership/version, ChangeSet, delivery intent, Applied state | carry Context operations and evidence; G decides Context/Applied | exact field/API mapping and consumer acceptance |
| Storage | durable transaction, visibility and persistence | only through owning service; receipts passed through | no direct BMCP-to-Storage write path; topology deferred |

### 6.1 Memory Compiler

BMCP is not the Memory Compiler. E owns Candidate IR and the compiler pipeline. BMCP may carry an E-owned ingress/candidate object only under E's current schema/receipt contract. Preserve the distinctions: transport receipt/delivery; E durable AcceptedReceipt; compiler execution/candidate; D producer admission/canonical commit; dependency registration/final publication; F indexing/G Context activation.

The merged Owner decision selects Option A + I1 for Fact/Claim semantics. This does not approve a Fact/Claim discriminator, canonical wire identity, schema, DDL or payload fields. Exact consumer mappings remain Candidate until responsible artifacts are version-pinned and reviewed; keep dependent payload opaque or use only approved candidate-neutral refs.

### 6.2 Agent Integration / MCP

C owns Agent/Adapter semantics; H owns BMCP wire/transport. Agent, Agent Runtime, Model, Provider, Tool, Session and Principal remain distinct. An MCP Server may expose Agent-facing tool/resource/prompt interfaces; it is not BMCP, does not define BMCP wire compatibility and does not replace D/I/G/E authority checks.

If used as an adapter/gateway, MCP Server maps authenticated Agent action to a registered BMCP operation; preserves message/request/correlation/idempotency identities; forwards protected principal context, not payload identity claims; uses BMCP/H transport rather than a parallel wire protocol; cannot write canonical Memory or mint PermissionEpoch/ForgetFence; and returns the owner result. MCP tool success is not canonical commit, E acceptance or Applied. Exact MCP-to-BMCP mapping is a C/H decision, not frozen here.

### 6.3 D/I

D is authoritative for Canonical Identity/Lifecycle and D-issued Forget Fence. I is authoritative for Principal trust, authorization, PermissionEpoch and global Forget policy. BMCP carries opaque issuer-typed refs and asks the issuing authority to validate currentness. It creates no parallel identity, authorization, epoch, fence or global completion mechanism. PermissionEpoch and ForgetFenceGeneration are distinct namespaces. If either authority is unavailable or returns stale/unknown/incomparable evidence, protected memory remains suppressed and execution stops.

## 7. H confirmation and Owner decision requests

H-owned questions go to H first; they are not disguised as Owner decisions.

### 7.1 H confirmation requests

**H-CONFIRM-001 — Envelope / request identity**
- MODULE: BMCP / H
- ISSUE_OR_ADR: H message-envelope-and-versioning.md; protocol-overview.md
- DECISION_REQUIRED: whether message_id is the request identity or a distinct request_id; exact response correlation; requiredness of version/type/payload schema/idempotency; operation registry and unknown-operation behavior.
- CURRENT_FACTS: canonical BMCP expansion is settled by `00-governance/terminology.md` as Brain Memory Context Protocol. H envelope remains CANDIDATE; current candidate uses message_id and does not define a separate request_id.
- H_OWNED_CONTRACTS: envelope, versioning and wire names remain H-owned.
- CROSS_MODULE_CONFLICT: C Request/Attempt IDs, H Message ID and domain Operation ID are not interchangeable.
- OPTIONS: (A) use message_id as request identity and bind response causation to it; (B) introduce a distinct request_id/command identity with explicit message_id mapping.
- RECOMMENDED_OPTION: H decides the exact identity model; C Request/Attempt, H Message/Request and domain Operation IDs remain distinct unless a versioned mapping explicitly relates them.
- MEMORY_COMPILER_IMPACT: E receipt/idempotency identity remains distinct.
- AGENT_INTEGRATION_IMPACT: C request/attempt mapping must be explicit.
- D_I_IMPACT: no authority changes; identity claims still validated by D/I.
- RUNTIME_IMPLEMENTATION_IMPACT: request/response correlation blocked pending H mapping.
- REQUIRED_AUTHORITY: H, with C/E/G consumer review.
- OWNER_DECISION: ACCEPTED_SEMANTICALLY_BY_OWNER_DELEGATE; NOT_WIRE_FROZEN
- EVIDENCE: `00-governance/terminology.md` Blob b8770fbb58e4fac087698043c40a57531b1d244d; H envelope Blob 5547ecd78d118bd63e571e5daad87194d9b694e4.
- FOLLOW_UP_ACTIONS: H publishes versioned mapping; consumers review.

**H-CONFIRM-002 — Wire decode / Parse boundary**
- MODULE: BMCP / H
- ISSUE_OR_ADR: H envelope and strict JSON reference
- DECISION_REQUIRED: exact split for transport framing, byte decoding, canonicalization/integrity and post-decode protocol Parse; duplicate keys, invalid UTF-8/Unicode, depth/size and critical extensions.
- CURRENT_FACTS: strict parser is a reference model, not production transport; semantic Parse here accepts decoded authenticated envelopes only.
- H_OWNED_CONTRACTS: raw Wire Decode and envelope structural validation.
- CROSS_MODULE_CONFLICT: H byte-decoding/transport duties must not move into BMCP semantics.
- OPTIONS: H owns raw bytes/envelope validation; BMCP owns operation resolution/request normalization.
- RECOMMENDED_OPTION: keep this split.
- MEMORY_COMPILER_IMPACT: E receives only parsed typed ingress requests.
- AGENT_INTEGRATION_IMPACT: Adapter/gateway uses H transport boundary.
- D_I_IMPACT: no authority change.
- RUNTIME_IMPLEMENTATION_IMPACT: raw bytes must not enter semantic parser.
- REQUIRED_AUTHORITY: H.
- OWNER_DECISION: ACCEPTED_SEMANTICALLY_BY_OWNER_DELEGATE; NOT_WIRE_FROZEN
- EVIDENCE: strict parser Blob 3b9b3da645448c773c95a9dcd3c57c8c109bb2da.
- FOLLOW_UP_ACTIONS: H publishes stage contract and vectors.

**H-CONFIRM-003 — ACK families / retry**
- MODULE: BMCP / H
- ISSUE_OR_ADR: H delivery/ACK and Forget ACK contracts
- DECISION_REQUIRED: ACK family, exact evidence boundary, persistence point, correlation tuple, duplicate/replay handling, retry horizon and consumer.
- CURRENT_FACTS: H separates Delivery lifecycle, Forget action ACK and Applied; lost ACK remains Unknown until reconciliation.
- H_OWNED_CONTRACTS: ACK wire/transport encoding and retransmission behavior.
- CROSS_MODULE_CONFLICT: generic ACK must not imply execution, durable commit, Applied or Forget completion.
- OPTIONS: keep separate ACK families, each one bounded observation.
- RECOMMENDED_OPTION: retain separation and explicit consumer mapping.
- MEMORY_COMPILER_IMPACT: E AcceptedReceipt remains distinct from transport ACK.
- AGENT_INTEGRATION_IMPACT: Adapter reports only observable boundary.
- D_I_IMPACT: D/I independently evaluate Fence/target satisfaction.
- RUNTIME_IMPLEMENTATION_IMPACT: ACK implementation waits for H and consumer acceptance.
- REQUIRED_AUTHORITY: H; D/I/G/E review their own consumption.
- OWNER_DECISION: ACCEPTED_SEMANTICALLY_BY_OWNER_DELEGATE; NOT_WIRE_FROZEN
- EVIDENCE: H ACK Blob 5e2b33898cbc6a9c95e271ecd1d8a092d04c67f8.
- FOLLOW_UP_ACTIONS: H publishes ACK-to-consumer matrix.

**H-CONFIRM-004 — Validator / error mapping**
- MODULE: BMCP / H
- ISSUE_OR_ADR: H envelope and conformance matrix
- DECISION_REQUIRED: validator layers, canonical error enum, response schema, retryability/redaction; map twelve requested classes without collapsing authn/authz/validation/conflict/unknown.
- CURRENT_FACTS: H taxonomy is candidate; requested generic labels are not all existing H codes.
- H_OWNED_CONTRACTS: wire/protocol Validator and error serialization.
- CROSS_MODULE_CONFLICT: domain validators and I authorization remain owner-owned.
- OPTIONS: preserve specific H codes; add aliases only with lossless versioned mapping.
- RECOMMENDED_OPTION: retain specific classes; publish layered validation and mapping.
- MEMORY_COMPILER_IMPACT: E errors remain distinct from protocol errors.
- AGENT_INTEGRATION_IMPACT: C maps Agent-facing errors without changing canonical meaning.
- D_I_IMPACT: D/I decisions remain authoritative.
- RUNTIME_IMPLEMENTATION_IMPACT: error mapping blocked until H contract.
- REQUIRED_AUTHORITY: H; domain owners approve their outcomes.
- OWNER_DECISION: ACCEPTED_SEMANTICALLY_BY_OWNER_DELEGATE; NOT_WIRE_FROZEN
- EVIDENCE: H envelope Blob 5547ecd78d118bd63e571e5daad87194d9b694e4.
- FOLLOW_UP_ACTIONS: H publishes taxonomy and vectors.


### 7.1.1 H owner confirmation dispositions — ACCEPTED_SEMANTICALLY_BY_OWNER_DELEGATE / NOT_WIRE_FROZEN

**Authority/capacity:** consolidated Project Owner delegate acting in the H protocol-owner role under Issue #305 comment 7042461592 and the Owner's standing instruction. This is not an independent human H signature. Evidence posture remains `INDEPENDENCE_UNVERIFIABLE`.

**Exact H source snapshot:** branch `session-h-bmcp-protocol` @ `3e8b33df18b9e6fc757ca84ff07a12faebc78e74`.
- Protocol overview Blob: `b88ef3a6fd3be293e7c2e77d9652f386b169bc47`
- Message envelope/versioning Blob: `5547ecd78d118bd63e571e5daad87194d9b694e4`
- Context delivery/acknowledgement Blob: `bf9732cc39d156853b507c3a3a4e573159978f49`
- Adapter Forget ACK/target binding Blob: `5e2b33898cbc6a9c95e271ecd1d8a092d04c67f8`
- Strict JSON parser reference Blob: `3b9b3da645448c773c95a9dcd3c57c8c109bb2da`
- Phase 3.7 lifecycle handoff Blob: `b2a2648d5576511f68fdb9d87ce4388a1fedd5e9`
- Protocol conformance matrix Blob: `075b2ac6ebe9bda4ec83de04fad07e8027e6a440`

#### H-CONFIRM-001 — Message/request identity: ACCEPT with boundary

- `message_id` is the unique immutable identity of one BMCP message.
- `correlation_id` groups one workflow/turn/delivery; `causation_id` identifies the immediate parent message/event.
- State-changing/retryable operations additionally require owner-scoped idempotency identity plus canonical payload digest.
- There is **no separate core envelope `request_id`** in the current H candidate. C retains AgentRequestId and AgentAttemptId as C-owned identities. C maps one Agent request to one or more BMCP messages using correlation/causation without collapsing Agent request, Agent attempt, BMCP message, transport attempt or idempotency identity.
- This accepts logical identity separation only; field encoding, namespace syntax and wire schema are not frozen.

#### H-CONFIRM-002 — Raw Wire Decode vs semantic Parse: ACCEPT

- H owns authenticated transport binding, framing/raw-byte intake, strict UTF-8/JSON decoding, duplicate-key/non-finite/depth/size rejection, envelope structural validation, protocol version/capability and integrity checks.
- BMCP semantic Parse begins only after successful decode and envelope validation. It resolves registered family/operation and dispatches to the owning domain authority.
- Semantic Parse MUST NOT re-parse raw bytes or bypass H's strict decoder. H decode MUST NOT infer B/D/E/F/G/I business semantics.
- The strict parser Blob is a non-production reference model, not a Runtime parser or implementation PASS.

#### H-CONFIRM-003 — ACK family/evidence/retry: ACCEPT with explicit non-equivalence

- Delivery lifecycle remains Prepared / Delivered / Applied / Rejected / Expired / Superseded / Unknown. Timeout or missing evidence is Unknown, never inferred success.
- Delivered proves transport endpoint receipt only. Applied is accepted only with G-owned context/application semantics and required C inference-boundary evidence; H transports/verifies evidence but does not mint G Applied.
- Forget ACKs are separate from Applied. Adapter-local SUPPRESSED, LOCAL_BUFFER_CLEARED, LOCAL_CACHE_PURGED, QUEUED_DELIVERY_CANCELLED, FAILED, UNKNOWN and UNSUPPORTED prove only the declared target/region/session/capability slice. I alone evaluates global target satisfaction and PolicyException.
- ACK identity/evidence digest is stable for one completed action; retransmission reuses it. Transport attempt identity may change. Same operation key + same target digest is idempotent; same key + different digest is conflict. Missing ACK after local success remains Unknown until query/reconciliation.
- No ACK implies model attention, comprehension, provider deletion, physical erasure or global Forget completion.

#### H-CONFIRM-004 — Validator layers/error mapping: ACCEPT with authority split

1. Transport/security integration authenticates peer/workload Principal; I owns Principal and authorization policy. Payload identity fields are assertions only.
2. H validates raw syntax, envelope requiredness/unknown-critical behavior, protocol version/capability, integrity, replay and idempotency.
3. Domain validators remain with their authorities: B semantics; D canonical identity/lifecycle/ForgetFence; E admission/receipt; F retrieval; G ContextVersion/delivery/Applied; I authorization/PermissionEpoch/Forget policy.
4. C owns final inference-request boundary evidence; H cannot infer Applied from a transport ACK.
5. Error classes preserve Authentication, Authorization, Validation, Unsupported, Conflict, Expired, RateLimited/ResourceExhausted, Internal and Unknown. Existing code labels remain Candidate until H's separate versioned wire contract is reviewed; no error enum is frozen.

**Disposition for all four confirmations:** `ACCEPTED_SEMANTICALLY_BY_OWNER_DELEGATE`; `NOT_WIRE_FROZEN`. Do not mark H's seven normative core specifications complete, do not claim cross-owner consumer acceptance, and do not close H implementation/conformance work. H must refresh its source branch against current main and submit normative bilingual spec/registry changes under H ownership.

### 7.2 Owner decision requests

**DECISION_REQUEST_ID: BMCP-DR-001**
- MODULE: BMCP
- ISSUE_OR_ADR: B-ADR-FACT-CLAIM-001 (13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/fact-claim-identity-adr.md)
- DECISION_REQUIRED: reconcile B-ADR-FACT-CLAIM-001 with the Owner semantic selection, then complete the required consumer mapping and acceptance before any canonical schema or wire-field freeze.
- CURRENT_FACTS: The merged Owner decision record `OWNER-DECISION-FACT-CLAIM-001` (main Blob `d59756a8eb454480804c482ca03c68345ab5abf2`; PR #446 merge commit `ad5ca81a32b413aef3f9b5bccd06030aabde8275`) selects Option A (separate Fact attestation and Claim proposition) with I1 (stable Claim identity plus immutable ClaimRevision). It supersedes the B ADR as the live semantic decision request; the B ADR remains historical evidence. Exact consumer implementation mappings, migration/compatibility and conformance remain Candidate until responsible artifacts are version-pinned and reviewed; no wire fields are approved.
- H_OWNED_CONTRACTS: future wire field/schema mapping remains H-owned and unfrozen; this semantic selection approves no wire field.
- CROSS_MODULE_CONFLICT: semantic direction is selected, but E Candidate IR, D identity/lifecycle, I authorization/attestor policy, and H payload mapping still require exact consumer acceptance and source pins before a shared schema can be frozen.
- OPTIONS: (A) preserve the selected Option A + I1 semantic direction while keeping payload fields opaque until the 消费者契约验收 gate is complete; (B) reopen the semantic choice only through a superseding Owner decision.
- RECOMMENDED_OPTION: A; do not treat semantic selection as schema approval.
- MEMORY_COMPILER_IMPACT: E remains candidate-neutral; no canonical Fact/Claim output schema.
- AGENT_INTEGRATION_IMPACT: C carries only opaque approved refs.
- D_I_IMPACT: D/I semantics unchanged; review consumers after B decision.
- RUNTIME_IMPLEMENTATION_IMPACT: no final Fact/Claim payload/schema/migration until decision.
- REQUIRED_AUTHORITY: Owner semantic selection is recorded in PR #446 (merged) under the standing Owner instruction; B/D/E/F/G/H/I consumer mapping and acceptance remain required for schema freeze.
- OWNER_DECISION: SEMANTIC_DIRECTION_APPROVED_OPTION_A_I1; WIRE_SCHEMA_MAPPING_CANDIDATE
- EVIDENCE: `OWNER-DECISION-FACT-CLAIM-001` PR #446 (merged) @ `ad5ca81a32b413aef3f9b5bccd06030aabde8275`; B ADR Blob 958e7f3a3a909ee5b6d9fb38ebf3a72b3a9bd593.
- FOLLOW_UP_ACTIONS: B updates ADR status/source pins; D/E/F/G/H/I record exact consumer mappings and acceptance; publish migration/compatibility plan and conformance scenarios; keep payload opaque until responsible consumer artifacts are version-pinned and reviewed.

**DECISION_REQUEST_ID: BMCP-DR-002**
- MODULE: BMCP
- ISSUE_OR_ADR: D canonical identity/lifecycle and Forget Fence; I authorization/PermissionEpoch contracts
- DECISION_REQUIRED: publish exact callable authority interfaces, typed request/receipt and currentness result vocabulary BMCP must consume; no ownership/semantics change requested.
- CURRENT_FACTS: D owns canonical identity/lifecycle and D Fence; I owns authorization/PermissionEpoch; H envelope references depend on these contracts.
- H_OWNED_CONTRACTS: H maps approved refs to wire fields after D/I publish.
- CROSS_MODULE_CONFLICT: ownership is clear; exact callable interfaces/error mappings are not established in the mainline guide.
- OPTIONS: (A) publish versioned D/I service contracts and H mapping; (B) keep refs opaque until then.
- RECOMMENDED_OPTION: B now; require A before Runtime entry.
- MEMORY_COMPILER_IMPACT: E consumes D/I semantics without copying authority.
- AGENT_INTEGRATION_IMPACT: MCP/Adapter cannot bypass D/I.
- D_I_IMPACT: no authority change; exact interface publication and consumer review only.
- RUNTIME_IMPLEMENTATION_IMPACT: protected handlers blocked until API/currentness evidence exists.
- REQUIRED_AUTHORITY: D and I; H confirms wire mapping afterwards.
- OWNER_DECISION: DEFERRED_TO_D_I_OWNER_CONTRACT_PUBLICATION; H MUST NOT INVENT AUTHORITY API OR CURRENTNESS SEMANTICS
- EVIDENCE: H overview Blob b88ef3a6fd3be293e7c2e77d9652f386b169bc47; D Forget Blob c791895333ab6140f035f4f622d5dee9325d422d.
- FOLLOW_UP_ACTIONS: D/I publish interfaces/vectors; H maps; BMCP updates crosswalk.

**DECISION_REQUEST_ID: BMCP-DR-003**
- MODULE: BMCP
- ISSUE_OR_ADR: C Agent Integration canonical contract / guide
- DECISION_REQUIRED: confirm Agent/MCP-to-BMCP operation mapping, Request/Attempt/Message identity, authenticated Principal handoff and final inference boundary.
- CURRENT_FACTS: C owns Agent/Adapter semantics; H owns BMCP wire/transport; C guide assigns wire schema/message semantics to H and Agent-side requirements to C.
- H_OWNED_CONTRACTS: H confirms transport/envelope/ACK mapping first.
- CROSS_MODULE_CONFLICT: MCP tool success, Agent request completion, BMCP business completion and domain receipt are distinct.
- OPTIONS: (A) MCP Server is C-owned adapter mapping to BMCP operations; (B) MCP Server exposes a parallel canonical Brain API.
- RECOMMENDED_OPTION: A; reject B as bypass/duplicate-authority risk.
- MEMORY_COMPILER_IMPACT: MCP ingress still uses E AcceptedReceipt and D admission.
- AGENT_INTEGRATION_IMPACT: C defines adapter mapping and preserves Agent/Runtime/Model/Provider/Tool/Session/Principal distinctions.
- D_I_IMPACT: canonical identity/lifecycle and authorization remain D/I-owned.
- RUNTIME_IMPLEMENTATION_IMPACT: gateway waits for H mapping and C acceptance.
- REQUIRED_AUTHORITY: C + H; D/I review authority-bearing identity mapping.
- OWNER_DECISION: OPEN_C_MAPPING_TRACKED_ISSUE_449; MCP_SERVER_IS_AGENT_FACING_ADAPTER_ONLY
- EVIDENCE: C guide Blob c4e076887634a9e8e46df076efb0f4b70d816e0a; `07-agent-integration/agent-integration-overview.md` and `08-bmcp-protocol` ownership boundary.
- FOLLOW_UP_ACTIONS: C/H publish mapping and conformance cases; no parallel API.



### 7.3 Resolved-vs-open decision register

| Item | Disposition | Exact boundary / next owner |
|---|---|---|
| Canonical BMCP name | RESOLVED — Brain Memory Context Protocol | Main terminology Blob `b8770fbb58e4fac087698043c40a57531b1d244d`; “Brain Memory Control Protocol” is non-canonical |
| Fact/Claim semantics | RESOLVED — Option A + I1 | Merged Owner decision PR #446; Blob `d59756a8eb454480804c482ca03c68345ab5abf2` |
| Fact/Claim field/wire schema | CANDIDATE / NOT FROZEN | B/D/E/F/G/H/I consumer artifacts must be version-pinned and reviewed; no payload fields approved |
| H-CONFIRM-001..004 | ACCEPTED_SEMANTICALLY_BY_OWNER_DELEGATE / NOT_WIRE_FROZEN | H owns normative wire/spec updates; no independent H signature is claimed |
| BMCP-DR-002 | DEFERRED_TO_D_I_OWNER_CONTRACT_PUBLICATION | D/I publish exact callable interface/IDL/currentness vocabulary; H must not invent authority APIs |
| BMCP-DR-003 / MCP mapping | OPEN — Issue #449 | C publishes exact Agent/MCP-to-BMCP mapping; H reviews only its wire/transport side |
| BMCP Runtime / AT-01..AT-20 | NOT AUTHORIZED / NOT RUN | Issue #7 implementation binding remains deferred |

**D/I evidence for BMCP-DR-002 (ownership evidence, not callable API publication):**
- D: `docs/en/03-memory-brain/forget-fence-and-completion-contract.md` Blob `c791895333ab6140f035f4f622d5dee9325d422d`; `forget-fence-operation-and-publication-gate.md` Blob `9c054932994bb078e2834df8bd66f73895aa04f5`; `memory-versioning.md` Blob `4efbd26db9586f6fcf1897f42ffba287d625b903`; `commit-cursor-semantics.md` Blob `2de7fe35229372ae5b06093e5e031c2c243fbd7c`.
- I: `docs/en/09-security-governance/security-governance-guide.md` Blob `061c5847b3df879eeaf3c71e5eae0bfa162b276a`; Chinese mirror Blob `372d27c79dc79d09bcdb0f142c979efdba1c2b6e`.
- These sources define domain semantics and operation names, not a complete callable API/IDL or frozen wire representation. D names RegisterProducerWork, InstallForgetFence, PublishDerivedIfFenceCurrent, CompleteProducerWork, ResolveProducerWork and ReconcileForgetBarrier. I defines PermissionEpoch, AuthorizationDecisionRef, revocation/currentness and evidence acceptance; no frozen public authorize() endpoint/schema exists.
- Ruling: D remains sole authority for canonical ForgetOperation/Fence and producer-barrier semantics; I remains sole authority for Principal authorization, PermissionEpoch, revocation and global Forget policy. BMCP carries opaque owner-issued refs/epochs and calls only the owning authority's validation/currentness operation after publication. PermissionEpoch and ForgetFence are distinct nominal types. Missing/stale/unavailable/indeterminate evidence fails closed.

**C mapping boundary:** Issue #449 is open and records that MCP Server, if selected, is C's northbound Agent-facing Adapter/Gateway, not BMCP and not a parallel Brain API. C must map Agent request/attempt identities to H message_id/correlation_id/causation_id, preserve Principal provenance and I authorization, and distinguish tool result, BMCP business response, transport ACK, E receipt and G Applied. No C response or acceptance is recorded yet.

## 8. Runtime acceptance plan — NOT RUN

Every row is a future Runtime requirement. No test below was executed by this work item. Design documents/reference models are not Runtime PASS.

### 8.1 Existing conformance evidence — bounded, not full-protocol PASS

- Main `c138654c942dc93b5a36eccb2ff0e41452156429`: `python3 -m unittest discover -s 08-bmcp-protocol/tests/conformance/applied_delivery_evidence -p 'test_*.py' -v` — **30 passed, 0 failed**, exit 0. This is the Applied Delivery Evidence conformance suite only.
- Open PR #436 exact head `1ffed9ed127df98b2f823a66ec80ea43d08cb9dc`: `python3 -m unittest discover -s 08-bmcp-protocol/tests/conformance/provider_outcome -p 'test_*.py' -v` — **10 run; 5 passed; 5 skipped; 0 failed**, exit 0. Skipped CPO-02/04/05/09/10 explicitly require Owner C's authoritative semantic validator. This is structural schema conformance only; it does not validate C semantics or cryptographic signatures.
- PR #436's bilingual protocol index and provider_outcome test are still an open PR, not mainline integration. Its index marks RecoveryJoin 1.0.2 schema/validator/test as not delivered.
- These results do not establish full BMCP conformance. The strict JSON parser is a reference model, not production transport. `tests/protocol_test.rs` and `crates/bmcp` are absent.
- AT-01..AT-20 remain **PLANNED_NOT_RUN**. No Runtime repository/authorization exists in this architecture phase.
