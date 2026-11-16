# Module H — BMCP Protocol & Adapter Baseline & Redlines

- Proposal: H-MBR-0.1.0
- Status: **PROPOSED — prepared by Session P for H Owner review/adoption; NOT an H Owner decision**
- Intended Owner: H — BMCP Protocol
- Source branch / HEAD: `session-h-bmcp-protocol` @ `08cca6341c3c44ad8502c215eba2b1941a8febb7`
- Evidence: `08-bmcp-protocol/message-envelope-and-versioning.md` blob `5547ecd78d118bd63e571e5daad87194d9b694e4`; `08-bmcp-protocol/adapter-forget-ack-and-target-binding.md` blob `5e2b33898cbc6a9c95e271ecd1d8a092d04c67f8`; `08-bmcp-protocol/phase-3.6-h36-live-closure-addendum.md` blob `e94d39b9977fca61af50bb697f29116d707b3439`
- Project PB/PR: P proposal v0.1.0 only, not approved/active.

## 1. Module Mission
Define interoperable, versioned Brain–Agent/Adapter message transport, capability negotiation, delivery semantics, acknowledgements and reconnect behavior without owning domain or security policy.

## 2. Ownership Baseline
H owns BMCP wire envelope, protocol versioning, schema compatibility, Adapter capability declarations, transport delivery receipts, local application/clear attestations and reconnect gates. B owns typed domain references; I owns Principal/Permission/target policy; G owns Context state; D owns ForgetFence.

## 3. Capability Baseline
Versioned envelope and schema registry; idempotency/correlation; authenticated transport binding; capability negotiation; delivery and ACK classes; offline/reconnect replay; exact target/session/region binding; reject unknown critical fields and incompatible versions.

## 4. Domain Ownership
H does not define Principal identity or permission semantics, canonical Memory/Forget, ContextVersion/Applied predicate, compiler lifecycle or runtime index state. Wire representation must preserve owner-defined types and authority boundaries.

## 5. Interface Baseline
Envelope carries protocol/version/message/correlation/idempotency/source/recipient and conditional typed Scope/Context/PermissionEpoch/ForgetFence fields. Source assertion is not authentication. ACK evidence is scoped to authenticated Adapter instance, session, operation, target, region, capability and exact attempt. Delivered is not Applied, suppression or local purge.

## 6. Security Baseline
Use verifier/transport context for authenticated identity, not payload claims. Bind protected operations and ACKs to Principal/session/target/Scope/PermissionEpoch/ForgetFence and capability epoch. Unknown identity/permission fields remain blocked until B/I/H acceptance.

## 7. Module Redlines
- H-PR-01 No payload source/ActorRef claim alone proves authenticated identity. CRITICAL.
- H-PR-02 No wire schema freezes B/I-owned identity or permission semantics without their acceptance. CRITICAL.
- H-PR-03 No generic ACK may be interpreted as Applied, suppressed, cleared or globally forgotten. CRITICAL.
- H-PR-04 No ACK may exceed its authenticated Adapter/session/target/region evidence scope. CRITICAL.
- H-PR-05 No reconnect/replay may bypass current auth, capability, fence or idempotency checks. CRITICAL.

## 8. Forbidden Cross-module Actions
No permission issuance/revocation policy (I); no domain identity semantics (B); no canonical Forget state (D); no Context Applied decision (G); no global completion decision.

## 9. Dependency Contracts
B typed refs; I issuer trust/permission/target-state policy; D ForgetOperation/Fence; G ContextVersion/Applied; C final-request evidence. H36 remains NOT RUN; identity fields and event/domain fields retain OPEN/ADR-BLOCKED dependencies.

## 10. Conformance Requirements
Schema compatibility; unknown field handling; replay/idempotency; forged payload identity; wrong target/session/region; ACK scope; offline reconnect; capability downgrade; revocation/Forget during delivery; stale ACK; protocol downgrade and malformed version tests.

## 11. Acceptance Criteria
H Owner accepts exact version; B/I approve exact identity binding; G/C accept Applied mapping; D accepts fence mapping; H36 and protocol conformance tests run with reproducible evidence.

## 12. Change Authority
H Owner decides wire/compatibility semantics. B/I/G/C/D decide owned inputs and predicates. Any wire change affecting owner semantics requires their explicit acceptance.

## 13. Open Decisions
Exact Principal/ActorRef/ScopeRef/PermissionEpoch encoding and authenticated binding; event/domain fields; ACK-to-I target-state mapping; common C/G/H Applied digest; H36 test execution.

## 14. Explicit Non-Claims
No external governance approval, identity policy freeze, global Forget completion, H36 pass or runtime interoperability certification.
