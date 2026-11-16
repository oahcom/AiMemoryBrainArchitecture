# Module G — Memory Context Baseline & Redlines

- Proposal: G-MBR-0.1.0
- Status: **PROPOSED — prepared by Session P for G Owner review/adoption; NOT a G Owner decision**
- Intended Owner: G — Memory Context
- Source branch / HEAD: `session-g-memory-context` @ `f6e7c46da9963ffee02c7805330b3f14291ab540`
- Evidence: `06-memory-context/context-reconciliation.md` blob `87063aceebed1c30b7840045ada8e3f348732688`; `06-memory-context/context-versioning.md` blob `05c0739d0c22576a1fd5affc7d73c078c89049b1`; `06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md` blob `aa3afa73d8a76cc6f025839c52bfbff6a983046a`
- Project PB/PR: P proposal v0.1.0 only, not approved/active.

## 1. Module Mission
Maintain the desired, authorized, versioned Brain-managed Memory Context for each Context scope and reconcile it with canonical, policy, freshness and Adapter evidence.

## 2. Ownership Baseline
G owns Context membership/order/budget, immutable ContextVersion, ChangeSet, reconciliation, delivery intent and authoritative Applied record. C owns final-request evidence; H owns wire/Adapter receipt; D owns canonical memory/ForgetFence; I owns authorization; F owns retrieval freshness.

## 3. Capability Baseline
Create immutable snapshots and deltas; serialize changes by CAS or equivalent per-Context ordering; reconcile source/policy/freshness drift; create delivery intent; validate Applied predicates per Adapter/session/Context/Delivery/InferenceRequest; remove invalidated entries and preserve audit trail.

## 4. Domain Ownership
G owns desired managed Context state and Applied record, not canonical Memory truth, Agent protected prompt regions, BMCP wire, Adapter execution, identity/permission or global Forget completion.

## 5. Interface Baseline
Each Context has one authoritative monotonic sequence; each ChangeSet binds BaseVersion and TargetVersion; Snapshot and Delta represent same target. Prepared → Delivered → Materialized → Final Request Submitted → Applied → Execution Started are distinct evidence stages. Applied means exact version included in exact submitted request under valid predicates only.

## 6. Security Baseline
Every entry/delivery is reauthorized against I policy and D fence. Brain-managed region remains data-only and cannot alter System/Developer instructions, user original input or Agent safety policy. Unknown evidence blocks Applied.

## 7. Module Redlines
- G-PR-01 No Context edit may mutate Canonical Memory. CRITICAL.
- G-PR-02 No concurrent mutation may silently overwrite Context head; require CAS/serialization. HIGH.
- G-PR-03 No Delivered/Materialized evidence alone may be called Applied. CRITICAL.
- G-PR-04 No Applied claim without C final-request evidence, H Adapter evidence, I authorization and D fence predicates. CRITICAL.
- G-PR-05 No Context removal may be represented as canonical Forget or global erasure. CRITICAL.

## 8. Forbidden Cross-module Actions
No D canonical writes; no F retrieval policy/index writes; no H wire semantics; no C final request fabrication; no I permission decision; no mutation of protected Agent prompt regions.

## 9. Dependency Contracts
D canonical lifecycle/fence; I authorization/epoch; F retrieval completeness/freshness; H delivery/materialization/capability evidence; C final request submission evidence. C/G/H Applied contract freeze remains blocked; workflow implementation candidate and unverified.

## 10. Conformance Requirements
CAS conflicts; stale source/policy/fence; partial delta; duplicate/out-of-order delivery; adapter reconnect; delayed ACK; request digest mismatch; wrong managed region; final request transformation; removal after Forget; no false Applied tests.

## 11. Acceptance Criteria
G Owner accepts exact version; C/G/H agree same Applied contract version/digest; D/I predicates consumed; H evidence exact target/session/region; conformance tests prove negative paths and no false Applied.

## 12. Change Authority
G Owner decides Context semantics; C/H/I/D own their respective evidence and policy. Cross-boundary Applied contract requires all affected owners.

## 13. Open Decisions
Exact C/G/H Applied field mapping/version; workflow implementation and persistence; per-session/adapter state recovery; delivery idempotency and stale-ACK reconciliation; runtime conformance.

## 14. Explicit Non-Claims
No Context runtime implementation, Applied execution pass, model attention/understanding proof or global Forget completion.
