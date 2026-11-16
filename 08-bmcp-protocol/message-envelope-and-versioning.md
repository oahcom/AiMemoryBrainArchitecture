# BMCP Message Envelope and Versioning

- Status: **CANDIDATE — exact Principal/ActorRef and permission fields ADR-BLOCKED on I; event/domain fields OPEN with C/D/E/G**
- Owner: H (wire representation and compatibility rules)
- Baseline: `main` @ `8e57f38e1f81a26280f0d56d6a40d6b98c5c6ac2`

## 1. Envelope shape

The following is a logical field map, not a frozen JSON Schema. Names and exact types for dependent identity/domain fields remain subject to owner review.

| Field | Requiredness | Meaning / rule |
|---|---|---|
| `protocol` | Required | Constant family identifier, candidate value `bmcp` |
| `protocol_version` | Required | Negotiated major.minor version |
| `message_id` | Required | Globally unique immutable message identifier |
| `message_type` | Required | Registered family + operation discriminator |
| `sent_at` | Required | Sender timestamp in RFC 3339 UTC; advisory, not ordering authority |
| `expires_at` | Conditional | Required for expiring delivery/control operations |
| `correlation_id` | Required for multi-message workflow | Stable workflow/turn/delivery correlation |
| `causation_id` | Optional | Immediate parent message/event ID |
| `idempotency` | Required for state-changing/retryable operation | Owner-defined namespace + key + payload digest |
| `source` | Required | Logical producer/application identity assertion; not authentication |
| `recipient` | Required when addressed | Logical destination selector |
| `scope_ref` | Conditional | Opaque owner-defined Scope reference; never grants permission |
| `context_ref` | Context family only | G-owned Context identifier |
| `context_version` | Context family only | G-owned typed version token; exact structure OPEN with G |
| `permission_epoch` | Conditional / I-defined | I-issued authorization epoch; do not mint or interpret locally |
| `forget_fence` | Conditional / D+I-defined | D canonical fence token with I policy binding; do not synthesize |
| `capability_epoch` | Adapter state-changing messages | Adapter's negotiated capability revision |
| `payload_content_type` | Required | Registered media/schema identifier |
| `payload_schema_version` | Required for typed payload | Payload schema version distinct from protocol version |
| `payload` | Required | Typed data; untrusted, non-executable |
| `extensions` | Optional | Namespaced extension map; cannot override core fields |
| `integrity` | Required on authenticated production channel | Canonical payload digest and transport/message authentication reference |

The envelope intentionally distinguishes protocol version, payload schema version, Context version, permission epoch, Forget fence and capability epoch. They are separate authorities and MUST NOT be collapsed into a generic `generation`.

## 2. Version negotiation

**CANDIDATE negotiation sequence:**
1. Adapter and gateway exchange a Capability Negotiation message over an authenticated transport.
2. Each advertises supported protocol major versions, minor-version range, message families, payload schema IDs, maximum message size, compression algorithms, acknowledgement modes, supported delivery semantics and conformance tier.
3. Both select the highest mutually supported major version and compatible minor version, plus the intersection of capabilities.
4. The negotiated result is bound to the transport session and a monotonically updated Adapter capability epoch.
5. If there is no common major version, state-changing traffic is rejected with `VERSION_UNSUPPORTED`; no silent downgrade.
6. Reconnect repeats negotiation. Previously negotiated capability is not presumed valid after process identity, binary, policy, or capability change.

Compatibility rules:
- A **major** version may remove/rename fields or change semantics and requires explicit negotiation.
- A **minor** version may add optional fields, message types, or capabilities without changing existing meanings.
- A **patch** version corrects clarifications/bugs without wire semantic change.
- Payload schema versioning is independent. A protocol-compatible envelope may still carry a payload schema the receiver cannot interpret.
- A sender MUST NOT send a required capability or required payload field unless negotiated/supported.
- No fallback may weaken authentication, authorization, Forget handling, or Applied proof.

## 3. Required, optional and unknown fields

- Missing required core fields: reject with `ENVELOPE_INVALID`.
- Missing conditional field when its condition applies: reject.
- Unknown optional extension field: preserve or safely ignore; never reinterpret it as a core field.
- Unknown required field: reject with `REQUIRED_FIELD_UNSUPPORTED`.
- Extensions MUST use a reverse-DNS or registered namespace and MUST NOT shadow reserved names.
- Unknown message family or operation: reject with `MESSAGE_TYPE_UNSUPPORTED`.
- Unknown non-security enum value: retain raw value where safe and return `ENUM_UNSUPPORTED` or route to a declared extension handler; do not silently map to a known value.
- Unknown security-, authorization-, lifecycle-, delivery-, or revocation-critical enum: fail closed; do not apply the operation.
- An unknown enum MUST NOT be converted to a permissive default.

## 4. Canonical serialization and integrity

**CANDIDATE:** JSON as the interoperable logical representation, canonicalized with RFC 8785 JSON Canonicalization Scheme (JCS) before hashing/signature. Binary encodings MAY be negotiated later but must preserve equivalent canonical semantics and a defined canonicalization profile.

Rules:
1. Reject duplicate object keys, invalid UTF-8, non-finite numbers, invalid Unicode, ambiguous numeric encodings and non-canonical timestamp forms where schema disallows them.
2. Canonicalization is applied to the exact signed/digested object according to a versioned profile. The profile states whether `integrity` itself is excluded from the digest input.
3. Digest algorithm and signature algorithm are explicit identifiers; do not infer from key length or implementation defaults.
4. Transport TLS authenticates the channel; message-level integrity is additionally required for durable queued/replayed or cross-boundary messages where transport protection no longer spans the full lifecycle.
5. Integrity metadata can include `canonicalization_profile`, `digest_algorithm`, `payload_digest`, `signing_key_id`, `signature_algorithm`, `signature`, and `signed_at`. Actual key ownership/rotation and principal binding are I/security responsibilities.
6. A digest proves byte/semantic integrity under the selected canonicalization profile, not truth, authorization, or successful application.

## 5. Authenticated identity binding

- The transport/security layer MUST provide an authenticated principal binding from I's approved mechanism.
- H maps that binding to the operation's authorized producer/Adapter identity through I's contract.
- Payload `ActorRef`, `producer_id`, `agent_id`, `session_id`, and `scope_ref` are claims or selectors only.
- A mismatch between authenticated binding and payload claims is rejected or quarantined according to I's policy; it is never resolved by trusting the payload.
- Authorization is checked at ingress and again at sensitive processing/application boundaries using the current I-defined permission epoch.
- H does not define grant inheritance, delegation rules, Principal taxonomy, revocation policy, or permission evaluation logic.

## 6. Error taxonomy

| Class / code | Retry? | Meaning |
|---|---|---|
| `ENVELOPE_INVALID` | No, until corrected | Missing/invalid required envelope data |
| `VERSION_UNSUPPORTED` | No | No compatible protocol major version |
| `MESSAGE_TYPE_UNSUPPORTED` | No | Unknown family/operation |
| `REQUIRED_FIELD_UNSUPPORTED` | No | Receiver cannot process required field |
| `ENUM_UNSUPPORTED` | Usually no | Unknown enum; critical enums fail closed |
| `INTEGRITY_FAILED` | No; security event | Digest/signature mismatch |
| `AUTHENTICATION_FAILED` | No; re-authenticate | Transport principal not authenticated |
| `IDENTITY_BINDING_MISMATCH` | No; investigate | Payload identity conflicts with authenticated binding |
| `NOT_AUTHORIZED` | No unless policy epoch changes | I policy denies operation |
| `PERMISSION_EPOCH_STALE` | Re-negotiate/re-authorize | Sender/recipient uses stale policy epoch |
| `FENCE_STALE` | Reconcile only | Forget/revocation fence superseded operation |
| `CONTEXT_BASE_MISMATCH` | Snapshot/rebase flow | Delta base does not match current G Context |
| `DUPLICATE_REPLAY` | Return prior result | Same idempotency key and same digest |
| `IDEMPOTENCY_CONFLICT` | No | Same key with different digest |
| `EXPIRED` | No | Deadline passed |
| `SUPERSEDED` | No; fetch current state | Newer authoritative operation exists |
| `RATE_LIMITED` / `RESOURCE_EXHAUSTED` | Backoff | Quota or capacity limit |
| `TRANSIENT_UNAVAILABLE` | Yes, bounded | Temporary transport/service failure |
| `INTERNAL_ERROR` | Bounded, with same key | Unexpected failure; no success inferred |

Errors include stable code, retryability, retry-after when safe, correlation ID, and sanitized detail. They MUST NOT disclose protected payloads, secrets, or cross-scope existence.

## 7. Idempotency and replay

- Idempotency namespace is defined by the operation owner (E for durable ingress, G for Context changes/delivery semantics, D/I for Forget controls); H transports it.
- A repeated key with identical canonical digest returns the original operation/receipt result and MUST NOT repeat side effects.
- Same key with different digest returns `IDEMPOTENCY_CONFLICT`.
- A new message ID does not defeat operation-level idempotency.
- Receivers retain deduplication state for the owner-defined replay horizon. Expired deduplication state is not permission to replay stale or revoked operations.
- Replay always rechecks current authorization, permission epoch, Forget fence, expiry and Context base version.

## 8. Cursor and version discipline

H uses correlation IDs and delivery IDs for protocol tracing, not as replacements for domain cursors. Keep distinct:
- E source Event cursor / durable receipt;
- D canonical commit cursor and per-aggregate revision;
- D lifecycle-event cursor;
- F per-index/per-partition publication watermark;
- D/I Forget fence;
- G ContextVersion;
- H delivery ID / delivery attempt sequence;
- Adapter capability epoch;
- Agent/inference request ID.

All cursor types, ordering, gap, replay and causal relationships remain with their owning modules. H MUST treat unknown typed tokens as opaque and MUST NOT compare unrelated tokens numerically.

## 9. Freeze conditions

Before marking this document DECIDED, H requires:
- I-approved transport principal binding and permission-epoch contract;
- C-approved telemetry and final-request boundary identifiers;
- D-approved typed canonical references and Forget fence shape;
- E-approved Accepted receipt/idempotency fields;
- G-approved ContextVersion and ChangeSet wire mapping;
- cross-module agreement on error codes and cursor correlation.
