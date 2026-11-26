---
document_metadata:
  domain: agent-integration
  role: guide
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "07-agent-integration/agent-integration-overview.md"
        - "PR #430 comments 7061007191, 7061333647 and 7061563540"
        - "Issue #449 comment 7061011800"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Source pins were refreshed to the live-main validation snapshot; the historical 13-section source is independently retrievable as non-canonical input. Exact C-H operation mapping remains open and Runtime is not authorized."
    usage_status: Active
    modification_status: Modified
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "Agent Integration explanatory architecture guide"
    canonical_scope_id: null
    canonical_scope_keywords:
      - agent-integration
      - MCP
      - BMCP
      - Agent Adapter
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    en: "docs/en/07-agent-integration/agent-integration-guide.md"
    zh-CN: "docs/zh-CN/07-agent-integration/agent-integration-guide.md"
---
# Agent Integration — Architecture Guide

- Document ID: DOC-AGENT-001 | Version: 1.1
- Owner: C — Agent Integration
- Normative source of truth: [C architecture overview](agent-integration-overview.md)
- Source document: this root guide (Informative / Non-Canonical)
- English reader mirror: [Agent Integration Architecture Guide](../docs/en/07-agent-integration/agent-integration-guide.md)
- Chinese reader mirror: [Agent 集成架构指南](../docs/zh-CN/07-agent-integration/agent-integration-guide.md)
- Status: Explanatory guide; family routing DECIDED; exact C-H operation mapping OPEN / DEPENDENCY_NOT_FROZEN

## 1. Purpose

This guide explains the Agent-facing integration boundary. It is explanatory only: the normative C source is the Agent Integration Architecture Overview. It does not define BMCP wire fields, transport, ACK encoding or a Runtime implementation.

## 2. The participants and authority

- **Agent Host / Agent:** owns reasoning, planning, tool execution, native Agent state and Agent safety policy.
- **C Agent Integration:** owns Agent-facing semantics, MCP dispatch mapping, C Agent request/attempt/turn/session identities, parameter validation and response mapping.
- **H Protocol Gateway / BMCP:** owns BMCP wire/envelope, transport, message/correlation/causation identifiers, ACK, Validator and capability negotiation.
- **B/D/E/F/G/I:** retain their domain authority: B vocabulary; D canonical identity/lifecycle/ForgetFence; E durable Event acceptance; F retrieval; G ContextVersion/ChangeSet/Applied; I Principal authorization/PermissionEpoch/global Forget.

## 3. MCP and BMCP are different interfaces

- MCP is the Agent Host ↔ C northbound tool/resource interface.
- BMCP (Brain Memory Context Protocol) is the C Agent Adapter ↔ Brain protocol via H.
- An MCP method or tool call is not a BMCP message. The MCP Server is an access adapter, not BMCP and not a parallel canonical Brain API.
- MCP success, HTTP 2xx, queue acceptance or H transport ACK cannot be reported as E Accepted or G Applied.
- Tool/resource names and exact schemas remain OPEN until the backend owner contracts and H operation registry are pinned and accepted. No placeholder operation is implied.

## 4. BMCP family routing from C

| Family | Direction at C | C disposition |
|---|---|---|
| Telemetry | Agent/Adapter → Brain | Expose only after H operation registration and I/C identity/authorization acceptance |
| Event Ingress | Producer/Agent → Brain | Require H registered ingress and E durable receipt/idempotency; MCP result is not E receipt by itself |
| Context Snapshot | Brain → Adapter | Inbound G-owned ContextVersion snapshot; not a generic MCP request/response |
| Context Delta | Brain → Adapter | Inbound G-owned exact-base/target ChangeSet; not a generic MCP request/response |
| Delivery | Brain → Adapter | H/G delivery lifecycle; C applies only the managed region at the declared inference boundary |
| Acknowledgement | Adapter → Brain | H-defined evidence; not MCP success and not G Applied |
| Capability Negotiation | Bidirectional | H-owned; no C-invented MCP tool or local negotiation substitute |
| Forget / Revocation | Brain/I → Adapter | C consumes D/I controls; no C-local Forget implementation |
| Administrative Governance | I/control plane → Adapter/Gateway | Control-plane only; no ordinary Agent tool absent explicit I policy/H registration |

Recall/Search is F-owned, not a BMCP family. Do not invent a BMCP Search operation. Any future MCP search tool requires a pinned F-owned query API and I/D authorization path.

## 5. Agent identity and H protocol identity

C retains `AgentRequestId`, `AgentAttemptId`, `AgentTurnId` and `AgentSessionId`. H owns `message_id`, `correlation_id` and `causation_id`. Do not invent a core `request_id`; `AgentAttemptId` is neither a transport attempt nor an idempotency key. The exact field-level crosswalk is OPEN / DEPENDENCY_NOT_FROZEN.

Authenticated Principal comes from I trust integration. Payload Principal, producer, Agent, Actor and Scope claims do not self-authenticate. H transport sender/audience binding is not a substitute for I authorization.

## 6. Idempotency and retry

State-changing replay uses an operation-owner-scoped idempotency identity bound to a canonical payload digest:

- Same identity + same digest returns the original result/receipt.
- Same identity + different digest conflicts.
- H message identity, correlation, causation and C AgentAttemptId are distinct from operation idempotency.
- H has selected RFC 8785 JCS as the logical JSON canonicalization basis; exact per-operation schema and integrity/signature profile remain OPEN.

## 7. Distinct outcomes

MCP tool result, BMCP business response, H transport ACK, E Accepted receipt, G Applied evidence, Forget ACK and I global Forget completion are distinct. No layer may upgrade one into another. Delivered is not Applied; Applied does not prove model attention or comprehension.

## 8. Active Recall versus Context delivery

Recall/Search belongs to F's retrieval/query interface and requires I authorization plus D lifecycle/ForgetFence checks. It is not a BMCP message family. Context Snapshot/Delta/Delivery belongs to the Brain-to-Adapter path: G owns ContextRef/ContextVersion/ChangeSet and Applied acceptance; H transports; C validates and applies only the managed region at the inference boundary.

## 9. Capability tiers and bounded reference models

Tier 1 requires final-request-observable inference-boundary evidence. Tier 2 is limited to middleware-controlled paths. Tier 3 supports telemetry/Recall and must not claim Full Applied. Tier does not grant permission.

PR #452 merged a bounded Rust tier-enforcement reference model at `48a03f694684f7a62bc5b337dc758c98e3cc0e5b`. It checks tier-to-operation authorization and protected-region/frozen-request rejection. It is not a production Adapter, MCP Server, BMCP negotiation/transport, telemetry pipeline, provider integration or proof of actual inference application.

PR #487 merged at `18b1c574433a6f3f600a9d2947b690084727aa75` adds a deterministic in-memory `ContextDeliveryAdapter`: exact-successor snapshot apply, clear/reset and disconnect/reconnect reporting. The crate reports eight unit tests. This is not real transport, durable delivery/session state, automatic retry, snapshot/delta reconciliation, production attestation or Runtime integration.

## 10. Security and failure handling

I owns authenticated Principal, authorization and current PermissionEpoch; D owns canonical identity/lifecycle and ForgetFence. Revalidate at protected operations and before replay-result disclosure. Stale/unknown authority fails closed. Memory and telemetry are untrusted data, never instructions; no private chain-of-thought is required.

A pre-dispatch failure may be retried if no side effect occurred. A timeout/lost response after dispatch is UNKNOWN pending reconciliation; cancellation is not rollback. Preserve Authentication, Authorization, Validation, Integrity, Conflict, Unknown/transient and owner-domain error distinctions. Sanitize error detail.

## 11. Offline and reconnect

Reconnect processes current I authorization/PermissionEpoch and D ForgetFence/revocation controls before cached context replay. Then revalidate Adapter/session identity, capability and ContextVersion. Apply a delta only with the exact base; otherwise request a full snapshot. Partial delivery/application is never Full Applied.

## 12. Current decision status

- Family-level MCP/BMCP routing: DECIDED by Issue #449 comment 7060351480.
- H logical identity/JCS/ACK/Validator principles: DECIDED at logical level by PR #428 comments 7060190878 and 7060264372.
- Exact H operation IDs, field names/types/requiredness, per-family schemas and MCP tool/resource names: OPEN / DEPENDENCY_NOT_FROZEN.
- D/I authority boundaries: DECIDED at semantic level; no API/schema freeze.
- E/G consumer acceptance and C-H operation mapping: OPEN.
- Issue #7: `IMPLEMENTATION_BINDING=DEFERRED_TO_ENGINEERING_PHASE`; no Runtime implementation authorized. All Runtime acceptance remains PLANNED_NOT_RUN / NOT AUTHORIZED.

## 13. Source pins

Live main snapshot at the start of this rebase/validation batch: `5a1964fa77f6dff024c8cef9e4e6a43f3bd051af`.

- C normative source `07-agent-integration/agent-integration-overview.md`: Blob `073ff4ddf71fbcaf959107bb06ab724bfa48e63b` before this follow-up.
- C capability tiers `07-agent-integration/adapter-capability-tiers.md`: Blob `60bce314c36313a14dffe476a6f2a5cf7aa03b37`.
- C capability-tier Chinese translation (Non-Canonical): `07-agent-integration/adapter-capability-tiers.zh-CN.md`, Blob `85a77163d1761a38074678983ad8d89ccf25d040`.
- C inference boundary `07-agent-integration/inference-boundary-model.md`: Blob `e2d5cb6abd9ec40da6e3680531de5944fc8b14df`.
- C telemetry `07-agent-integration/telemetry-model.md`: Blob `9bb4a77e4bd79caaf3e1faeaf77c6b42858998f0`.
- PR #487 in-memory reference-model README/source: Blobs `ee68705248f80972232ebf28a4713554f377908e` / `125ebfb382a43c8e7ea79b547f86eaa7b611e202`; eight tests, no production transport or Runtime proof.
- H current protocol index: Blob `a5b64941cdc783b385348de1b22e0eaace2c003d`; H Applied evidence addenda: `afa294bc42a8488e4569e6a8bdf5437c7a90e247` and `7b73491c765091728af6f5306b9efd502cf7f30a`.
- H RecoveryJoin 1.0.2 schema: Blob `bbac8742401249230c629e858d033a09cd8f3acb`; artifact presence only, not D proof adoption, production conformance, or a frozen C-H operation registry.
- G ContextVersion: Blob `1bfe7f1891e1f9da1ff7508f4e25a11bbf7f649b`; G Applied/Forget reconciliation: `aa3afa73d8a76cc6f025839c52bfbff6a983046a`.
- E Event Store contract: Blob `17b14591d76160a7c125903b41e7dae014c3c5df`.
- D/I semantic decisions: Issue #429 comments `7060243632` / `7060259541`; H logical decisions: PR #428 comments `7060190878` / `7060264372`.

The four C source documents remain the normative source baseline. This guide pair is explanatory and does not replace them.
