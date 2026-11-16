# Module C — Agent Integration, Telemetry & Final Request Baseline

- Proposal: C-MBR-0.1.0
- Status: **PROPOSED — prepared by Session P for C Owner review/adoption; NOT a C Owner decision**
- Intended Owner: C — Agent Integration
- Source branch / HEAD: `session-c-agent-integration-2026-11-16` @ `702263dee9b40cf78fe95481731f52adb775c0d2`
- Evidence: `07-agent-integration/telemetry-event-and-identity-contract.md` blob `2bd9e640bd0c1d2c8b768da1e06b06096bc2a79e`; `07-agent-integration/security-and-untrusted-memory-boundary.md` blob `b32aeeb0b7b226cd3770d2af82b0ddfbf35a511d`; `07-agent-integration/phase-3.6-final-request-evidence-contract.md` blob `fd2f47ba6c89bb270e9f2bec956873cb7ae3592b`
- Project PB/PR: P proposal v0.1.0 only, not approved/active.

## 1. Module Mission
Define how Agent-side telemetry, request-bound evidence and Brain-managed Memory Context integrate with Agent/runtime boundaries without taking over Agent reasoning, planning, action selection or tool authority.

## 2. Ownership Baseline
C owns telemetry semantics, producer assertion quality, request/turn correlation, final-request submission evidence and Agent-side protected-region boundary. H owns wire; G owns Context desired/applied state; I owns identity/authorization; D owns ForgetFence; Agent/runtime owns planning/action/tool execution.

## 3. Capability Baseline
Accept structured source-qualified observations/outcomes without requiring hidden chain-of-thought; distinguish intent/plan from completed outcome; bind final request evidence to actual immutable request and submit boundary; preserve managed Memory region isolation; report unavailable observability as Unknown/Bypassed rather than success.

## 4. Domain Ownership
C owns telemetry meaning and evidence stage. C does not own canonical Event/Memory commit (D/E), permission policy (I), BMCP encoding (H), ContextVersion/Applied record (G) or retrieval (F).

## 5. Interface Baseline
Prepared, Delivered, Materialized, Final Request Submitted, Applied and Execution Started are distinct. C emits final-request evidence; G evaluates Applied with H Adapter evidence and I/D authorization/fence predicates. Telemetry producer claims are not authenticated identity.

## 6. Security Baseline
Memory, Evidence, Provenance, Retrieved Summary, Tool Observation, External Content and transformed/compacted derivatives remain untrusted data. System/Developer instructions, User Original Input, Agent Safety Policy and Agent-owned Context are protected from Brain mutation. If region isolation cannot be established, reject application or report Bypassed/Unknown.

## 7. Module Redlines
- C-PR-01 Never request or persist complete hidden CoT/private scratchpads as a prerequisite. HIGH.
- C-PR-02 Never promote Agent intent/plan/telemetry claim into verified completed outcome without evidence. CRITICAL.
- C-PR-03 Never elevate Memory or Summary into instruction authority. CRITICAL.
- C-PR-04 Never claim Materialized/Submitted/Applied from Delivered ACK alone. CRITICAL.
- C-PR-05 Never mutate protected prompt regions or authorize tool actions through Brain content. CRITICAL.

## 8. Forbidden Cross-module Actions
C cannot redefine H wire, G Applied predicate, I Principal/Permission, D canonical Forget state or Agent tool policy. It cannot silently rewrite user original input or system/developer instruction regions.

## 9. Dependency Contracts
B/I/H typed identity binding; D ForgetFence; G Context version/delivery; H Adapter capability and receipt; runtime/provider submit-boundary evidence. C/G/H exact Applied contract remains freeze-blocked; implementation and execution unverified.

## 10. Conformance Requirements
Prompt injection and summary laundering; protected-region overwrite; telemetry replay/correlation; plan-vs-outcome confusion; malformed/missing final-request evidence; exact request/digest/region binding; delayed/duplicate ACK; unknown capability and fail-closed cases.

## 11. Acceptance Criteria
C Owner accepts exact version; C/G/H agree exact evidence fields and predicate; I/D authority predicates are consumed without redefinition; negative tests show protected-region isolation; runtime evidence is reproducible.

## 12. Change Authority
C Owner decides C semantics; H/G/I/D decide their respective boundaries. Cross-boundary changes require affected Owners; security threat-model approval requires I.

## 13. Open Decisions
H/I authenticated producer binding; C/G/H common Applied evidence version/digest; runtime/provider observability profile; I threat-model approval; end-to-end adversarial test evidence.

## 14. Explicit Non-Claims
No H wire freeze, G Applied approval, I authorization approval, runtime enforcement proof or system readiness claim.
