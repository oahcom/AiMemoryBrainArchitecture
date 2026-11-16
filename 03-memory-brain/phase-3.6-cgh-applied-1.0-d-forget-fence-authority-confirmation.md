# D Owner Authority Confirmation — CGH-APPLIED-1.0 ForgetFence and Lineage

- Owner: Session D — Memory Brain
- Branch: `session-d-memory-brain-2026-11-16`
- Decision: **APPROVE WITH ENUMERATED EXCEPTIONS — D-OWNED FENCE / LINEAGE SEMANTICS ONLY**
- Common contract: `CGH-APPLIED-1.0`
- Exact A decision package: `reviews/integration/phase-3.6-cgh-applied-contract-decision-package.md`
- Exact package Blob SHA: `122b164bcc0760b83bf555072a36fc55631623e1`
- Controlling D decision: `03-memory-brain/phase-3.6-joint-forget-linearization-decision.md`
- Controlling DE-S consumer acceptance: `03-memory-brain/phase-3.6-bih-identity-consumer-acceptance.md`

## 1. Decision

D confirms the D-owned ForgetFence, lineage and canonical-mutation ordering semantics consumed by CGH-APPLIED-1.0. This decision does not make D the authority for I PermissionEpoch, B typed-reference meanings, C final-request evidence, G Applied state or H wire transport.

D approves the package's rule that a Full Applied historical fact requires proof that the exact final submission boundary was ordered against the applicable ForgetFence and every relevant ancestor/source-lineage fence. Wall-clock timestamps, local cache observations or a fence token copied from an earlier operation are not sufficient ordering evidence.

## 2. Normative D confirmation

1. D owns ForgetOperation, ForgetFence/ForgetFenceGeneration, source and ancestor lineage, canonical memory mutation and D-local producer/work barrier semantics.
2. ForgetFenceGeneration is an opaque D-authoritative namespace. It is not PermissionEpoch, CapabilityEpoch, ContextVersion, DeliveryAttemptId, RuntimeSessionRef or a storage cursor.
3. The applicable fence check covers the exact target and all required source/ancestor lineage. Missing, incomplete, stale, incomparable or unresolved lineage fails closed.
4. The D serialization order must include producer/work registration, fence installation, complete derived-dependency registration, final publication visibility commit and barrier-visible terminal disposition.
5. If the relevant ForgetFence is ordered before the final submission boundary, the request is ineligible for Full Applied and protected memory remains suppressed.
6. If the final submission boundary is proven to precede the relevant fence, the historical ordering fact may be retained; the later fence still invalidates current-use eligibility. D does not authorize G to serve or reuse the historical context.
7. If the order cannot be established by authoritative causal/serialization evidence, the result is UNKNOWN. No Full Applied promotion or success claim is permitted.
8. A fence-first outcome blocks later ordinary admission/publication across the active fence. A participant/work-first outcome must remain tracked until its exact terminal resolution; process death, timeout, lease expiry, queue deletion or DLQ movement is not terminal proof.
9. D-local barrier drainage or ProducerRegistrationHighWater does not prove global producer inventory completeness, TargetInventorySeal or Global Forget completion. Those remain I-owned external inventory authorities.
10. The final D mutation/publication gate independently validates current I authorization and D ForgetFence. Neither check substitutes for the other.

## 3. Enumerated exceptions and limits

1. D confirms the semantics, not a deployed cross-owner sequencer shared by C, I and D. This artifact does not establish that the C FinalRequestBoundaryId can be causally ordered against D's fence in production.
2. A shared causal receipt, common serialization domain or other explicit authority-approved proof is still required to distinguish submit-before-fence from fence-before-submit. Independent wall clocks are insufficient.
3. Where the exact order or lineage coverage is absent, CGH must retain UNKNOWN/INDETERMINATE and suppress current use; it must not infer a favorable ordering.
4. This does not approve I governance or PermissionEpoch service deployment, C's producer evidence completeness, G's Applied predicate/commit, H's wire encoding or B's semantic types.
5. D36 race/fault tests and production runtime conformance remain NOT RUN / NOT VERIFIED.
6. This is not Global Forget completion, physical erasure evidence or approval to close JF-10 P0.

## 4. Exact CGH-APPLIED-1.0 disposition

- D ForgetFence authority and namespace: **CONFIRMED**.
- D target/source/ancestor lineage coverage requirement: **CONFIRMED**.
- Fence-first versus participant/submission-first semantics: **CONFIRMED**.
- Ambiguous ordering fail-closed behavior: **CONFIRMED**.
- Production C-submit/D-fence causal bridge: **OPEN / NOT ESTABLISHED**.
- D36 runtime conformance: **NOT RUN**.
- Global inventory seal / Global Forget: **NOT APPROVED BY D-LOCAL EVIDENCE**.

This decision is pinned to the exact A package Blob above. It is not approval of another package revision unless the changed revision is reviewed explicitly.
