# Phase 3.6 — H Six-Dimension Self-Review

- Review authority: Joint BIH Decision Architect, under the user's explicit delegation.
- Subject: H — BMCP Protocol & Adapter Authentication.
- Reviewed branch: `session-h-bmcp-protocol`
- Reviewed contract: `08-bmcp-protocol/phase-3.6-authenticated-identity-protected-operation-binding.md`
- Reviewed contract blob: `dd143147726496021e2189e583ad30cb10d8b616`
- Review result: **CONDITIONAL PASS — protocol security model is directionally complete; wire-level and ACK ordering details remain underspecified.**
- Scope: design/document review only; no runtime conformance tests executed.

## 1. Responsibility and authority boundary — PASS
H owns BMCP envelope, serialization, Adapter authentication integration, ACK transport and reconnect. B owns Ref semantics; I owns trust and authorization; C/D/E/F/G own their semantic and final enforcement boundaries. H does not claim message integrity equals authorization.

## 2. Identity and type semantics — PASS WITH FINDING
The field matrix distinguishes protected auth context from payload claims and separates Principal, Actor, Adapter, Producer, Scope, Environment and session identities.

**H36-SR-01 — P1:** `auth.authentication_context_ref` is named but its type, issuer, lifecycle, audience binding and replay semantics are undefined. Align with B's AuthenticationContextRef gap: either register a typed reference contract or keep it verifier-internal and non-wire-visible.

## 3. Trust and authentication chain — PASS WITH FINDINGS
H correctly obtains protected transport context and delegates issuer/Principal/delegation/authorization validation to I. Adapter instance authentication is separate from AdapterRef claim.

**H36-SR-02 — P1:** Protected auth context is not cryptographically bound to exact BMCP message bytes/session/channel (channel-binding/exporter value, message nonce, audience and canonical digest coverage). A valid context could be replayed or misbound across sessions/messages. Define H's binding profile; never place raw credentials in payload.

## 4. Authorization and boundary control — PASS WITH FINDING
The operation matrix covers producer admission, compiler publication, retrieval, context delivery, ACK, forget ACK, event ingress, reconnect and administrative operations. PermissionEpoch and ForgetFence remain separate.

**H36-SR-03 — P1:** Field matrix uses “EnvironmentRef if applicable” and “ActorRef where applicable”, while JD-10 requires applicable members and fail-closed behavior. Define operation-specific requiredness profiles and deterministic applicability; sender omission must not evade authorization.

## 5. Protocol and lifecycle — CONDITIONAL
Reconnect order is explicit; old sessions cannot inherit ACK authority; ACK idempotency and anti-replay are specified.

**H36-SR-04 — P1:** ACK ordering is ambiguous when an ACK arrives after revocation but carries a pre-revocation observed timestamp. JD-15 says post-revocation ACKs are historical only, while the base text allows an owning authority to validate event-time ordering. Specify trusted sequencing/commit cursor and authoritative receipt time; never trust Adapter wall-clock time alone.

**H36-SR-05 — P1:** “Same ACK ID + same digest returns original result” needs an idempotency namespace (issuer + Adapter instance + operation scope), retention period and conflict behavior after session rotation.

## 6. Failure semantics and evidence — CONDITIONAL
Failure taxonomy is strong and 18 adversarial tests are specified but not executed. Unknown critical fields and protocol major downgrade fail closed.

**H36-SR-06 — P0 DOCUMENT CONSISTENCY:** Section 8 still says B acceptance of exact H mapping is OPEN, I policy is a candidate and H has no independent approval/readback, while the joint-decision section states the delegated technical baseline is decided. Correct state: joint technical mapping is decided under delegated authority; separate owner-session signatures and external governance approvals are not claimed; consumer acceptance and implementation remain open.

**H36-SR-07 — P1:** Add tests for channel/session misbinding, message replay across session, ACK cross-Adapter collision, ACK arrival/revocation race, duplicate-key/canonicalization and capability downgrade with a valid old session.

## Final disposition
- Six-dimension result: **CONDITIONAL PASS**.
- P0: reconcile stale Owner Decision/Cross-module Agreement statements with joint technical decision.
- P1: specify message/channel binding, auth-context reference disposition, per-operation requiredness, ACK ordering/namespace/retention and add adversarial tests.
- Governance approval remains GOVERNANCE-BLOCKED; runtime conformance remains NOT RUN.
- No BMCP schema freeze, production security certification or implementation PASS is claimed. ADR-001 remains ADR-BLOCKED.

## 7. Remediation disposition — design-level closure

The H findings H36-SR-01..07 have been addressed in the controlling H contract Section 10, committed separately on this branch. The contract now defines AuthenticationContextRef as verifier-internal, cryptographic channel/session/message binding, operation-specific Requiredness Registry, trusted receiver/owner-sequencer ACK ordering, stable ACK idempotency namespace and retention, additional conformance cases, and corrected delegated decision status.

- H36-SR-01..06: **RESOLVED at protocol-contract level**.
- H36-SR-07: **TEST CASES SPECIFIED; NOT RUN**.
- Global BMCP schema freeze and production cryptographic profile approval: **NOT CLAIMED / OPEN**.
- Runtime conformance: **NOT VERIFIED / NOT RUN**.
- Overall: **DESIGN FINDINGS CLOSED; IMPLEMENTATION/GOVERNANCE CONDITIONAL**.
