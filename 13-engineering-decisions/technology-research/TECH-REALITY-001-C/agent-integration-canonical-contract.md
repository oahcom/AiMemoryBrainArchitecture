# C Canonical Integration Contract / C 规范集成合同

**Status: C-owned semantic requirements proposed; not cross-owner wire-frozen.**

## MUST / 必须
1. Agent, Agent Runtime, Model, Provider, Tool, Session and Principal MUST remain distinct concepts.
2. Every inference Request and Attempt MUST have stable identities and explicit idempotency scope.
3. Provider handoff, execution lifecycle, response receipt, parse, validation, tool execution, Brain commit/visibility and G Applied MUST be distinct evidence stages.
4. Model-generated content MUST NOT be promoted to Verified Claim or Canonical Memory solely because a model or Provider returned it.
5. Provider-native response metadata MUST be preserved where available; absent metadata MUST use explicit unavailable/not-reported/unknown/not-applicable semantics.
6. Retry after ambiguous handoff MUST reconcile the same Attempt and provider idempotency key before creating another Attempt.
7. Late and duplicate results MUST be appended as immutable observations; conflicts require reconciliation.
8. Tool side effects MUST be separately authorized, identified and evidenced; cancellation MUST NOT imply rollback.
9. Brain candidate and write operations MUST pass I authorization and D lifecycle/Forget checks. Agent/Tool has no direct canonical storage path.
10. C final-request evidence MUST bind the actual immutable post-transformation request and actual submit boundary. G alone decides Applied.
11. Trace, Correlation, Request, Attempt, Operation, Session and Principal identifiers MUST NOT be substituted for one another.
12. Telemetry MUST minimize sensitive content and MUST NOT be treated as immutable audit proof.

## MUST NOT / 禁止
- MUST NOT equate HTTP 200, provider acceptance, tool success or output parse with canonical operation success.
- MUST NOT claim NOT_INVOKED from timeout or lost acknowledgement alone.
- MUST NOT retry non-idempotent side effects blindly.
- MUST NOT accept Agent payload identity as authenticated Principal.
- MUST NOT let external Agent mutate canonical Memory or lifecycle state.
- MUST NOT sign C Provider Outcome with an unregistered/untrusted key or claim H/I registration from schema presence.
- MUST NOT use stale Context or Memory references after Forget/revocation invalidation.

## C-owned vs external authority / C 自有与外部权威
C owns Agent/Provider integration requirements, inference request/attempt semantics, Provider handoff evidence, tool integration evidence requirements and telemetry correlation requirements. B owns typed domain meaning; D owns canonical lifecycle/Forget; E owns derived-memory production; F owns retrieval/activation; G owns ContextVersion/Applied; H owns BMCP schema/wire/ACK; I owns identity/authorization/trust/privacy governance; Storage owns durable commit/visibility mechanics; A owns system integration and deployment decision.

## Compatibility / 兼容
C's historical CSubmitOutcome 1.0.1 and H Unified 1.2.15 are candidate artifacts only. This document does not change their schema, fields, signature profile, wire version or acceptance status. Any normative field-level change requires exact owner review and a successor immutable version.
