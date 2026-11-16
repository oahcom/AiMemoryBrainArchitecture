# Session H Phase 3 Targeted Remediation Change Log

- Owner: H / BMCP Protocol & Agent Context Adapter
- Branch: session-h-bmcp-protocol
- Starting H HEAD: fcc5103399b4c322e52d642cae5a2414969399a7
- Scope: CR-P1-05 and H responsibility within CR-P0-02
- Status: H design artifacts updated; cross-owner approvals and runtime conformance remain OPEN / NOT RUN.

## Source branches read

| Owner | Branch | HEAD SHA | Read inputs |
|---|---|---|---|
| H | session-h-bmcp-protocol | fcc5103399b4c322e52d642cae5a2414969399a7 | H protocol package, ACK, Adapter capability, delivery and conformance docs; Phase 3 task pack |
| I | session-i-security-governance-2026-11-16 | 8c91d99e450ab5e8862bd6a3301fa193e28e6cbb | Forget/Retention/Backup/Erasure Policy; Principal/Actor/Authorization Contract; Scope/Revocation Policy |
| D | session-d-memory-brain-2026-11-16 | 30dbffdc7d47af0888ecf7b42cfa686d2ec0c9d6 | Forget Fence and Completion Contract |
| G | session-g-memory-context | 3d2c065be863bc1d349faaeece6f6eaa0047abae | Context Versioning and Change Sets; Context Reconciliation |
| B | session-b-domain-model-phase3 | ab19afbf92f67fe0a7679e9aa3a35b015fed89f4 | Typed Reference and Scope Semantics |

The requested reviews/integration/phase-3-defghi-cross-module-contract-review.md was not present on H, A or main trees inspected. The Phase 3 remediation task pack was present and read. This missing review is an explicit source gap; no conclusions unique to that absent review are represented as read or closed.

## Changes delivered

1. Added adapter-forget-ack-and-target-binding.md:
   - Seven ACK postconditions, retry semantics and I Target State evidence mapping.
   - Mandatory identity/evidence binding for Adapter, Agent/runtime, Principal/Issuer, ActorRef, Session, ScopeRef, Managed Region, CapabilityEpoch, PermissionEpoch and D ForgetFence.
   - Distinct permission/fence namespaces and fail-closed rules.
   - Clear, Apply and reconnect ordering.
   - Ten required H-FRG conformance scenarios.
   - Explicit I/D/G/B/C open decisions and authority boundaries.
2. Updated forget-revocation-and-reconnect.md with normative ACK and reconnect refinement.
3. Updated message-envelope-and-versioning.md with explicit ACK identity/epoch fields and payload-claim rejection rules.
4. Updated adapter-capability-and-applied-attestation.md with capability coverage inventory and Applied-vs-Forget evidence separation.
5. Updated context-delivery-and-acknowledgement.md with final Apply gate and separate Forget ACK semantics.
6. Updated protocol-conformance-matrix.md with H-FRG-01..10; all remain design requirements / NOT RUN.

## Interface impact

| Owner | H contract consumed/produced | Required owner action |
|---|---|---|
| I | H emits capability-bounded per-instance/region ACK evidence; H consumes authenticated Principal and current PermissionEpoch | Approve target classes, evidence predicates, epoch API/currentness, PolicyException and global aggregation |
| D | H consumes ForgetOperation ID and opaque ForgetFence; emits Adapter-local evidence | Confirm token binding/validation and barrier target semantics |
| G | H consumes ContextVersion/Delivery ledger and provides clear/cancel + Applied evidence separately | Confirm per-session Adapter inventory and delivery status integration |
| B | H references ActorRef/ScopeRef authoritative types | Approve typed reference encoding/namespace mapping |
| C/runtime | H Applied proof uses final request boundary; Forget ACK remains separate | Confirm final submission hook/request identity |

## Acceptance criteria

- No transport Delivered state is described as Applied or Cleared.
- Every ACK is bounded by Adapter Instance, Agent/runtime Session, ScopeRef, Managed Region and CapabilityEpoch.
- SUPPRESSED, LOCAL_BUFFER_CLEARED, LOCAL_CACHE_PURGED and QUEUED_DELIVERY_CANCELLED prove distinct postconditions.
- FAILED, UNKNOWN and UNSUPPORTED cannot satisfy a target as success.
- I alone evaluates Target State, exceptions and global completion.
- PermissionEpoch and ForgetFence remain separate typed namespaces.
- Reconnect performs authenticated identity, current I epoch, current D fence, clear/reconcile, G version validation, reauthorization, apply, then separate Applied attestation.
- Offline and unverifiable state remain Pending/Unknown.
- Applied does not prove model attention/use; Forget ACK does not prove global completion/provider deletion.

## Unresolved / not passed

- I/B joint approval of ActorRef/ScopeRef and authenticated binding.
- I final Target State/evidence predicates, PermissionEpoch consistency and PolicyException policy.
- D final fence token/comparison API and target selector semantics.
- G per-session Adapter inventory and Context/Delivery wire semantics.
- C/runtime final request observation hook.
- Durable SDK implementation, crash consistency and all runtime conformance evidence.
- Missing Phase 3 cross-module review document noted above.
- No implementation, security certification, physical-erasure proof or Global Forget Completion is claimed.
