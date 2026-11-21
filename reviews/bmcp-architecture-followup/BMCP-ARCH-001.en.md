# BMCP Architecture Completion — Semantic Contract & Engineering Handoff

- Work Item: BMCP-ARCH-FOLLOWUP-001; Document: BMCP-ARCH-001; Version: 0.1.0
- Status: CANDIDATE / ARCHITECTURE_PARTIAL — not a frozen protocol specification
- Main baseline: bb49dc121c195d7fb2ffa0ffbb9d376186b802fc
- H source snapshot: session-h-bmcp-protocol @ 3e8b33df18b9e6fc757ca84ff07a12faebc78e74
- Peers: [中文版本](BMCP-ARCH-001.zh-CN.md) | [English](BMCP-ARCH-001.en.md)
- Scope: architecture semantics, phase boundaries, dependency map, acceptance plan and engineering handoff.
- Excluded: Runtime code; H-owned wire/schema/transport/ACK/Validator decisions; D/I authority changes; Fact/Claim ADR decision.

## 1. Disposition

**ARCHITECTURE_PARTIAL.** This is a candidate semantic synthesis and engineering handoff, not a protocol freeze.

H's live branch contains candidate Envelope, versioning, canonicalization, error taxonomy, Delivery/ACK, Forget/reconnect, strict JSON parser reference and conformance material. These files remain H-owned; their existence is not approval or freeze. H's lifecycle handoff says Wire Schema NOT FROZEN; its conformance matrix is a candidate test specification, not Runtime evidence.

The Compiler Fact/Claim mapping remains ADR-BLOCKED. BMCP MUST NOT freeze canonical Fact/Claim payload fields. D owns Canonical Identity/Lifecycle and D Forget Fence; I owns authorization and PermissionEpoch. BMCP consumes those authorities and MUST NOT create substitutes.

Issue #7's recorded binding remains IMPLEMENTATION_BINDING=DEFERRED_TO_ENGINEERING_PHASE. GitHub currently reports Issue #7 CLOSED / not_planned under the Owner phase-closure ruling; this work does not reopen or alter it. Deferral is not Runtime authorization.

**Naming conflict:** the public BMCP guide expands BMCP as “Brain Memory Context Protocol”; task wording also uses “Brain Memory Control Protocol”. This document uses “BMCP” only. H / Architecture Governance must settle the canonical expansion before any rename.

## 2. Exact source ledger

Main pins are from fetched origin/main at the baseline above. H pins are from the live fetched H branch.

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
| 13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/fact-claim-identity-adr.md | main | 958e7f3a3a909ee5b6d9fb38ebf3a72b3a9bd593 | ADR-BLOCKED |

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
| B | Fact/Claim meaning and canonical domain decisions | only owner-approved typed refs/payloads | B-ADR-FACT-CLAIM-001 ADR-BLOCKED |
| D | canonical identity, lifecycle, canonical commit/revision, Forget Fence | pass typed refs to D and consume D receipts/currentness | exact Runtime API binding |
| I | Principal trust, authorization, PermissionEpoch, revocation, global Forget policy | protected principal context and current authorization decision | exact approved interface/profile |
| C | Agent/Adapter boundary, telemetry, final inference request | C adapter maps Agent request to registered BMCP operation | MCP/Adapter mapping and request identity |
| G | Context membership/version, ChangeSet, delivery intent, Applied state | carry Context operations and evidence; G decides Context/Applied | exact field/API mapping and consumer acceptance |
| Storage | durable transaction, visibility and persistence | only through owning service; receipts passed through | no direct BMCP-to-Storage write path; topology deferred |

### 6.1 Memory Compiler

BMCP is not the Memory Compiler. E owns Candidate IR and the compiler pipeline. BMCP may carry an E-owned ingress/candidate object only under E's current schema/receipt contract. Preserve the distinctions: transport receipt/delivery; E durable AcceptedReceipt; compiler execution/candidate; D producer admission/canonical commit; dependency registration/final publication; F indexing/G Context activation.

B's current preferred Fact/Claim Option A (separate Fact attestation and Claim proposition) remains ADR-BLOCKED / NOT APPROVED. BMCP MUST NOT freeze a Fact/Claim discriminator, canonical identity, schema, DDL or wire payload from that recommendation. Until formal decision and consumer acceptance, keep dependent payload opaque or use only approved candidate-neutral refs.

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
- DECISION_REQUIRED: canonical BMCP expansion; whether message_id is request identity or distinct request_id; exact response correlation; requiredness of version/type/payload schema/idempotency; operation registry and unknown-operation behavior.
- CURRENT_FACTS: H envelope is CANDIDATE; public guide says “Brain Memory Context Protocol”; task wording says “Brain Memory Control Protocol”.
- H_OWNED_CONTRACTS: envelope, versioning and wire names remain H-owned.
- CROSS_MODULE_CONFLICT: C Request/Attempt IDs, H Message ID and domain Operation ID are not interchangeable.
- OPTIONS: retain existing expansion and message_id; or publish a distinct command ID with explicit mapping.
- RECOMMENDED_OPTION: preserve H ownership; keep IDs distinct; publish mapping before freeze.
- MEMORY_COMPILER_IMPACT: E receipt/idempotency identity remains distinct.
- AGENT_INTEGRATION_IMPACT: C request/attempt mapping must be explicit.
- D_I_IMPACT: no authority changes; identity claims still validated by D/I.
- RUNTIME_IMPLEMENTATION_IMPACT: request/response correlation blocked pending H mapping.
- REQUIRED_AUTHORITY: H, with C/E/G consumer review.
- OWNER_DECISION: PENDING_H_CONFIRMATION
- EVIDENCE: H envelope Blob 5547ecd78d118bd63e571e5daad87194d9b694e4.
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
- OWNER_DECISION: PENDING_H_CONFIRMATION
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
- OWNER_DECISION: PENDING_H_CONFIRMATION
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
- OWNER_DECISION: PENDING_H_CONFIRMATION
- EVIDENCE: H envelope Blob 5547ecd78d118bd63e571e5daad87194d9b694e4.
- FOLLOW_UP_ACTIONS: H publishes taxonomy and vectors.

### 7.2 Owner decision requests

**DECISION_REQUEST_ID: BMCP-DR-001**
- MODULE: BMCP
- ISSUE_OR_ADR: B-ADR-FACT-CLAIM-001 (13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/fact-claim-identity-adr.md)
- DECISION_REQUIRED: decide canonical Fact/Claim model and identity/version relationship; approve exact schema and consumer mapping only through ADR authority.
- CURRENT_FACTS: B currently prefers Option A (separate Fact attestation and Claim proposition), but ADR is ADR-BLOCKED / NOT APPROVED; I-04/P-04 and domain overview are inconsistent.
- H_OWNED_CONTRACTS: future wire field/schema mapping remains H-owned and unfrozen.
- CROSS_MODULE_CONFLICT: E Candidate IR, D identity/lifecycle and H payload mapping cannot finalize a shared model while ADR is blocked.
- OPTIONS: (A) approve Option A with examples/consumer review; (B) approve another explicit model and reconcile I-04/P-04; (C) keep payload opaque and defer dependent operations.
- RECOMMENDED_OPTION: C interim; do not treat B's preference as approval.
- MEMORY_COMPILER_IMPACT: E remains candidate-neutral; no canonical Fact/Claim output schema.
- AGENT_INTEGRATION_IMPACT: C carries only opaque approved refs.
- D_I_IMPACT: D/I semantics unchanged; review consumers after B decision.
- RUNTIME_IMPLEMENTATION_IMPACT: no final Fact/Claim payload/schema/migration until decision.
- REQUIRED_AUTHORITY: authorized Architecture Governance decision-maker + B; D/E/I/H consumer review as applicable. Named governance decision-maker is NOT_RECORDED.
- OWNER_DECISION: PENDING_OWNER_DECISION
- EVIDENCE: ADR Blob 958e7f3a3a909ee5b6d9fb38ebf3a72b3a9bd593.
- FOLLOW_UP_ACTIONS: identify authority; issue exact ADR disposition; then update consumers.

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
- OWNER_DECISION: PENDING_OWNER_DECISION
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
- OWNER_DECISION: PENDING_OWNER_DECISION
- EVIDENCE: C guide Blob c4e076887634a9e8e46df076efb0f4b70d816e0a.
- FOLLOW_UP_ACTIONS: C/H publish mapping and conformance cases; no parallel API.

## 8. Runtime acceptance plan — NOT RUN

Every row is a future Runtime requirement. No test below was executed by this work item. Design documents/reference models are not Runtime PASS.

| ID / scenario | OWNER | PRECONDITION | EXPECTED_RESULT | TEST_METHOD | DEPENDENCY | ACCEPTANCE_STATUS |
|---|---|---|---|---|---|---|
| AT-01 Valid request parse | H + BMCP | H-decoded authenticated envelope; supported version; registered operation | one normalized request; Parse has no side effect | golden envelope + operation schema | H envelope/registry | BLOCKED_BY_H_CONTRACT |
| AT-02 Invalid request parse | H | malformed envelope / missing required field | reject before Execute; sanitized stable error | negative envelope vectors | H Validator | BLOCKED_BY_H_CONTRACT |
| AT-03 Unsupported version | H | no common major | VERSION_UNSUPPORTED; no downgrade/dispatch | version negotiation matrix | H version contract | BLOCKED_BY_H_CONTRACT |
| AT-04 Missing parameters | H + operation owner | required payload field absent | validation rejection; no service call | per-operation negative schema vector | H + domain schema | BLOCKED_BY_H_CONTRACT |
| AT-05 Unknown operation | H | unregistered family/operation | reject before side effect | registry negative/fuzz test | H registry | BLOCKED_BY_H_CONTRACT |
| AT-06 Unauthorized | I + H | authenticated principal denied by current I policy | deny; no protected call; no cross-scope leak | authorization negative integration | I API/epoch + H binding | BLOCKED_BY_OWNER_DECISION |
| AT-07 Request/response correlation | H | request has message_id/correlation_id | response causation references request; correlation preserved | multi-message round-trip | H request identity | BLOCKED_BY_H_CONTRACT |
| AT-08 Execution success | domain owner + BMCP | Parse/validation/auth pass; owner returns success receipt | response contains exact owner result; ACK separate | service contract integration | E/D/G API | BLOCKED_BY_OWNER_DECISION |
| AT-09 Execution failure | domain owner + H | owner returns definitive failure | preserve failure; no false success | fault-injected service result | owner error + H mapping | BLOCKED_BY_H_CONTRACT |
| AT-10 Timeout | owner + H | timeout before/after possible side effect | UNKNOWN until owner reconciliation; same key | crash/timeout at each boundary | owner lookup/reconcile | BLOCKED_BY_OWNER_DECISION |
| AT-11 ACK receipt | H | valid ACK for one stated boundary | record only that boundary; no implied execution/persistence | ACK schema/consumer test | H ACK | BLOCKED_BY_H_CONTRACT |
| AT-12 ACK lost | H + owner | side effect may complete; ACK/response lost | UNKNOWN; reconcile same identity; no blind duplicate | network fault + journal reconciliation | H ACK + owner idempotency | BLOCKED_BY_H_CONTRACT |
| AT-13 Duplicate request | owner + H | same idempotency identity and digest | original result; no second side effect | concurrent duplicate/replay | owner idempotency | BLOCKED_BY_OWNER_DECISION |
| AT-14 Duplicate ACK | H + consumer | same ACK ID/digest then same ID/different digest | idempotent replay; changed digest conflict; no mutation | ACK replay/mutation vectors | H ACK + D/G/I mapping | BLOCKED_BY_H_CONTRACT |
| AT-15 Validator rejection | H + owner | invalid envelope/schema/critical extension | reject at correct layer; no later stage | layered negative suite | H Validator + domain schema | BLOCKED_BY_H_CONTRACT |
| AT-16 Forget Fence conflict | D + I + H | stale/unknown D fence or I epoch | fail-closed; no protected apply/commit; suppression retained | both race orders + authority outage | D/I currentness APIs | BLOCKED_BY_OWNER_DECISION |
| AT-17 Canonical Identity conflict | D (+ B ADR for Fact/Claim) | payload ref mismatches D identity or Fact/Claim unresolved | reject/quarantine; no mint/coercion | forged/mismatch identity vectors | D API; B ADR | BLOCKED_BY_OWNER_DECISION |
| AT-18 Serialization stability | H | exact schema/profile/version | same semantic object => approved canonical bytes/digest | cross-language golden vectors | H canonicalization/signature | BLOCKED_BY_H_CONTRACT |
| AT-19 Unicode | H | valid/invalid UTF-8, supplementary chars, normalization edges, duplicate keys | preserve valid Unicode per profile; reject invalid/ambiguous form | cross-language Unicode/malformed bytes | H wire decode/canonicalization | BLOCKED_BY_H_CONTRACT |
| AT-20 Request/response consistency | H + domain owner | request ID/correlation/operation/idempotency fixed | response links exact request and returns only owner result | end-to-end trace assertions | H correlation + owner result | BLOCKED_BY_H_CONTRACT |

BLOCKED_BY_H_CONTRACT means an H-owned wire/transport/ACK/Validator decision or exact mapping is missing. BLOCKED_BY_OWNER_DECISION means an authority-owned domain contract/API or ADR is missing. All tests remain NOT RUN until authorized Runtime and exact build exist; dependency labels are not test results.

## 9. Runtime engineering handoff / Issue #7 entry

Keep the binding unchanged: IMPLEMENTATION_BINDING=DEFERRED_TO_ENGINEERING_PHASE.

Issue #7 is currently CLOSED / not_planned under the Owner phase-closure ruling; its body retains the deferral and engineering-entry checklist. This work does not edit Issue #7 or declare Runtime entry.

**All entry conditions are required:**
1. BMCP semantic contract accepted by accountable architecture authority; unresolved semantics enumerated.
2. H freezes versioned Wire, Transport, ACK and Validator contracts, including error/conformance mappings.
3. H/C/E/D/I/G accept cross-module Request/Response/Receipt/ACK mappings as applicable.
4. Fact/Claim ADR formally decided, or dependent operations explicitly excluded/opaque; E Candidate IR and receipt APIs pinned.
5. C/H accept Agent Integration / MCP-to-BMCP adapter boundary; MCP is not a substitute protocol.
6. D/I publish exact callable interfaces for identity/lifecycle, Forget Fence, authorization and PermissionEpoch currentness.
7. Canonical Runtime repository/branch (or authorized new repo), accountable engineering owner/maintainers, build, CI, test commands and artifact provenance designated.
8. Deployment topology, persistent storage, queues, recipient adapters, observability, recovery and operator responsibilities documented.
9. Full acceptance suite runs on immutable Runtime commit with reproducible raw evidence; UNKNOWN/recovery/race cases fail closed.
10. Independent security/domain review and required Owner acceptance complete. No production activation implied.

| Workstream | Next artifact | Responsible authority | Entry status |
|---|---|---|---|
| H | frozen envelope/version, wire decode, ACK, Validator, error/conformance | H | BLOCKED_BY_H_CONTRACT |
| B / Governance | formal Fact/Claim ADR and schema impact | B + authorized governance | BLOCKED_BY_OWNER_DECISION |
| D | canonical identity/lifecycle/Fence API and receipts | D | BLOCKED_BY_OWNER_DECISION |
| I | authorization/PermissionEpoch/revocation API | I | BLOCKED_BY_OWNER_DECISION |
| E | Candidate IR, AcceptedReceipt and service boundary | E | BLOCKED_BY_OWNER_DECISION |
| C | Agent/MCP adapter-to-BMCP mapping | C + H | BLOCKED_BY_OWNER_DECISION |
| G | ContextVersion/Delivery/Applied/ACK mapping | G + H | BLOCKED_BY_OWNER_DECISION |
| Engineering leadership | canonical Runtime repo/team/CI/deployment authority | Engineering leadership | DEFERRED_TO_ENGINEERING_PHASE |
| BMCP architecture integration | refresh source pins after Owner responses | BMCP architecture lead | NOT STARTED |

## 10. Governance and verification

- Issue #7: CLOSED / not_planned; body retains IMPLEMENTATION_BINDING=DEFERRED_TO_ENGINEERING_PHASE. No status edit.
- Issue #3: CLOSED / not_planned as superseded. Its historical body says Applied Contract Frozen = NO and Test Executed / Passed = NO / NO; closure does not prove a new BMCP core freeze.
- Issue #43: closed as superseded by Owner phase-closure ruling. This is a candidate architecture handoff, not Runtime implementation.
- Main fetched SHA: bb49dc121c195d7fb2ffa0ffbb9d376186b802fc; H branch HEAD: 3e8b33df18b9e6fc757ca84ff07a12faebc78e74.
- No Runtime code or H-owned source file modified.
- Runtime acceptance tests: NOT RUN — no Runtime authorization/repository.
- Independent semantic parity review: PENDING. H/Owner responses: PENDING.

## 11. Bilingual change manifest

| Document / version | English path | Chinese path | Source revision | Parity |
|---|---|---|---|---|
| BMCP-ARCH-001 / 0.1.0 | reviews/bmcp-architecture-followup/BMCP-ARCH-001.en.md | reviews/bmcp-architecture-followup/BMCP-ARCH-001.zh-CN.md | main bb49dc121c195d7fb2ffa0ffbb9d376186b802fc; H 3e8b33df18b9e6fc757ca84ff07a12faebc78e74 | author-prepared pair; independent parity review PENDING |

The coverage register records this as a review/handoff pair only. It does not change “BMCP Protocol detailed contracts (7 core specifications)”; bilingual normative core-spec coverage remains NOT STARTED.

## 12. Final status

- ARCHITECTURE_DELIVERABLE_STATUS: **ARCHITECTURE_PARTIAL**
- PARSE_CONTRACT_STATUS: candidate semantic boundary specified; H wire/decode mapping pending
- EXECUTE_CONTRACT_STATUS: CANDIDATE; D/I/E/G APIs and Fact/Claim decision pending
- RESPOND_CONTRACT_STATUS: CANDIDATE; H response envelope/correlation mapping pending
- H_DEPENDENCY_STATUS: **BLOCKED_BY_H_CONTRACT**
- CROSS_MODULE_DEPENDENCIES: H, B, C, D, E, G, I
- OWNER_DECISIONS_REQUIRED: BMCP-DR-001..003
- ISSUE_7_STATUS: IMPLEMENTATION_BINDING=DEFERRED_TO_ENGINEERING_PHASE; GitHub CLOSED / not_planned; unchanged
- RUNTIME_IMPLEMENTATION_STATUS: NOT AUTHORIZED / NOT STARTED
- PR / Commit: populate only after successful push and PR creation; no merge authorized

**Next action:** H answers H-CONFIRM-001..004 first; B/Architecture Governance, D, I and C resolve their requests; BMCP architecture integration refreshes exact pins and publishes a successor. Runtime remains deferred until all engineering-entry conditions are evidenced.
