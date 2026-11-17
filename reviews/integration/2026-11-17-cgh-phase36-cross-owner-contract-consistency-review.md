# C/G/H Phase 3.6 Cross-Owner Contract Consistency Review

- Date: 2026-11-17
- Review type: independent cross-owner contract audit (not translation-only review)
- Repository: `oahcom/AiMemoryBrainArchitecture`
- PR: #28, `docs/bilingual-coverage-completion`
- Exact source baselines:
  - C `07-agent-integration/phase-3.6-final-request-evidence-contract.md`, branch `session-c-agent-integration-2026-11-16`, Blob `fd2f47ba6c89bb270e9f2bec956873cb7ae3592b`.
  - G `06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md`, branch `session-g-memory-context`, Blob `aa3afa73d8a76cc6f025839c52bfbff6a983046a`.
  - H `08-bmcp-protocol/adapter-capability-and-applied-attestation.md`, branch `session-h-bmcp-protocol`, current Blob `0dca3dc5463a02be0e19524811afbae87795baf5`.
- Related exact G decision anchors:
  - CGH-APPLIED-1.1 candidate A package Blob `d4eef4aecf94f922f7933c1e1fec14a69ad17dec`.
  - Recovery-batch A package Blob `4961ffefc0f9920efb8425a9b2a7af42d8f64819`.
  - Companion COC Blob `fc3bac39ec64fda68b8cba5e1aada4e719e5acea`.

## 1. Executive disposition

**C/G/H cross-owner contract: NOT READY TO FREEZE.**

The six-stage lifecycle is semantically aligned, and authority boundaries are mostly consistent: C produces final-request/provider-side evidence, H owns Adapter protocol/capability and preserves authenticated owner evidence, and G alone accepts Applied. However, G's latest CGH-APPLIED-1.1 recovery-batch decision requires evidence that the current C producer contract does not yet define as a C-issued output or explicit consumed reference set. H §11.8 recognizes the new evidence bridge but remains a candidate mapping reservation, not a frozen schema or implemented wire contract.

This is a substantive P1 contract gap, not a translation defect. No Owner decision or implementation status is upgraded by this review.

## 2. Cross-owner alignment that is sound

| Topic | C | H | G | Result |
|---|---|---|---|---|
| Lifecycle | Distinguishes Prepared, Delivered, Materialized, Final Request Submitted, Applied, Execution Started | Distinguishes transport, materialization, submit evidence and Applied attestation | Defines the same six stages and owns Applied | Aligned |
| Final submit authority | C emits evidence only after exact post-transformation request crosses successful runtime/provider submit boundary | H cannot infer C provider outcome | G requires C evidence and validates predicate | Aligned in principle |
| Applied authority | C explicitly does not mutate Applied | H explicitly does not own Applied acceptance | G is sole Applied authority | Aligned |
| Capability ceiling | Tier 2/3 and bypass/unknown cannot claim Full | Tier 1/2/3 ceilings; Full requires final request observation | Full Applied rejects incomplete/unknown coverage | Aligned |
| Historical/current-use split | Historical evidence retained; later revocation/fence invalidates current use | Later Forget/revocation invalidates current-use without rewriting valid history | Immutable historical Applied; current-use projection separately recomputed | Aligned |
| Duplicate and late evidence | Same identity/digest idempotent; changed digest conflict; late evidence cannot roll back | Same identity/digest and replay rules | Same identity/digest idempotency and no rollback | Aligned |
| Forget ordering | Unknown order => Unknown/suppressed | Cannot infer cross-authority ordering from receiver/time/ACK | Unknown ordering => no new Full Applied and suppress current use | Aligned in principle |

## 3. Findings

### XCH-36-001 — C producer contract does not define the G CGH-APPLIED-1.1 C evidence set

**Severity: P1 — freeze blocker**

G's latest recovery-batch amendment requires, at minimum:
- exact C provider receipt and immutable `CSubmitOutcome`;
- a determinate `CausalOrderTerminalProof` binding the same transaction, request/participant digest, reservation and terminal outcome;
- recovery-batch evidence and complete pre-batch participant enumeration/reconciliation, owner high-water attestations, and owner-specific I/D/Storage terminal evidence before a new Full Applied promotion.

The current C source (Blob `fd2f47...`) requires an actual runtime/provider-assigned `InferenceRequestId`, a successful submit boundary, and a generic submission outcome, but does not define the `CSubmitOutcome` evidence object, actual provider receipt contract, or the exact 1.1 causal-order/recovery-batch evidence bindings and references. Its latest explicit exact-version Owner decision remains CGH-APPLIED-1.0; no C acceptance of the exact 1.1 recovery-batch package is present in this source.

**Required closure**
1. C Owner must define the C-owned provider handoff receipt and immutable `CSubmitOutcome` fields, identity, digest, success/failure/unknown semantics, idempotency and replay behavior.
2. C must explicitly bind its outcome to the exact request, FinalRequestBoundaryId, delivery attempt, participant intent/request digest and causal-order transaction where applicable.
3. C must consume/reference, but must not mint, COC terminal proof and recovery-batch/participant evidence. Ownership of COC, I, D and Storage evidence remains with their respective authorities.
4. C Owner must issue an exact-version decision against the current 1.1 recovery-batch package (or publish a successor package and rebind the decision).

Until closed, G cannot safely treat the C producer contract as satisfying the complete 1.1 predicate.

### XCH-36-002 — H §11.8 is a candidate mapping, not a frozen or implemented 1.1 wire contract

**Severity: P1 — freeze blocker**

The current H source Blob `0dca3d...` includes §11.8 and enumerates the causal-order, recovery-batch, participant completeness, owner high-water, I terminal, D lineage/cutoff/effective-position and conditional Storage same-XID evidence references. It correctly prohibits H from minting or inferring COC, I, D, C-provider or Storage outcomes and keeps the ordering domains distinct.

But §11.8 explicitly remains a candidate reservation. It states that the current JSON Schema/SDK is not thereby proven to contain the fields and requires H to publish an exact additive schema version after relevant C/G/I/D/Storage confirmations. G names `bmcp.applied-ack/1.1.0` as a target, but this audit found no evidence in the reviewed H source that this target is already a published, frozen schema/SDK implementation.

**Required closure**
1. H publishes the exact versioned schema and SDK field mapping for the 1.1 evidence bridge.
2. H provides machine-readable required/optional/conditional field rules, empty-set attestation semantics, UNKNOWN/IN_DOUBT handling, integrity coverage, replay identity and compatibility rules.
3. H obtains exact-version C/G/I/D/Storage confirmations; H must not interpret those confirmations as transferring authority to H.
4. H supplies executable schema/serialization/verification fixtures. Status remains NOT RUN until evidence exists.

### XCH-36-003 — Exact-version decision chain is incomplete across Owners

**Severity: P1 — freeze blocker**

G has accepted its own Applied predicate and recovery-batch prerequisites with enumerated exceptions. H has recorded the 1.1 bridge as a candidate. C's current source records a CGH-APPLIED-1.0 decision and does not record acceptance of the exact 1.1 recovery-batch evidence profile. The shared contract therefore has no demonstrated exact-version C/G/H acceptance chain for the latest G decision package.

**Required closure:** A shared package/version must pin the exact C, G and H source Blobs plus the exact A/COC decision package Blobs. Each Owner must explicitly accept that same package/version within its own authority and list exceptions. Do not infer acceptance from a downstream consumer mapping or a previous 1.0 decision.

### XCH-36-004 — Pre-1.1 ordering language needs an explicit supersession rule

**Severity: P2 — normative ambiguity**

Earlier G/C clauses refer to owner commit cursors, trusted receiver receipt sequences and generic boundary timestamps/monotonic sequence. The 1.1 H bridge correctly states that COC, I, D and Storage ordering domains are distinct and cannot be compared or substituted; wall-clock, H receiver sequence, arrival order, timeout, missing ACK or reconnect cannot establish cross-authority order.

The later 1.1 decision appears intended to refine the older generic language, but the reviewed source set does not provide one concise precedence statement identifying which older ordering formulations are superseded for 1.1.

**Required closure:** G/C/H publish a normative precedence note: for CGH-APPLIED-1.1, only the exact owner-issued evidence and CausalOrderTerminalProof under the named profile establish the required cross-participant terminal disposition; local sequences remain local and are never numerically compared. Preserve older 1.0 behavior only for the exact 1.0 package.

### XCH-36-005 — Execution, recovery and Forget race evidence remains unexecuted

**Severity: P1 for production readiness; not a translation blocker**

C conformance, G-36/CGH and H conformance cases remain SPECIFIED / NOT RUN. G explicitly states that the coordinator/operator and durable participant/order service are not designated/deployed/verified and that G's validator/persistence has not been shown consuming the full recovery-batch evidence set. No implementation or production pass is claimed.

**Required closure:** Execute deterministic tests for provider handoff outcomes, same-XID resolution, recovery-cutoff batches, missing/incomplete participant enumeration, I revocation races, D fence races, Storage terminal visibility/non-publication, replay, changed digest, reconnect, and unknown-order suppression. Attach durable artifacts and Owner sign-off. Contract acceptance alone is not runtime verification.

## 4. Authority and evidence ownership matrix

| Evidence | Producer/authority | H role | G role |
|---|---|---|---|
| Final immutable request / provider handoff / CSubmitOutcome | C + actual runtime/provider receipt | Authenticate envelope and preserve opaque evidence | Validate; never synthesize |
| CausalOrderTerminalProof / recovery batch | COC coordinator/order authority | Validate schema/integrity and preserve references | Require before new Full Applied |
| I authorization terminal / sequencer / revocation cutoff | I | Preserve authenticated references | Validate; no policy inference |
| D lineage / fence request cutoff / effective position | D | Preserve authenticated references | Validate; no fence inference |
| Storage same-XID terminal resolution / visibility | Storage | Preserve authenticated references | Require when Storage participates |
| Adapter capability / ACK / session / wire integrity | H | Own and authenticate | Consume; no Applied promotion from ACK alone |
| Applied fact and current-use projection | G | No authority | Sole owner |

## 5. Corrected H source pin and prior report supersession

The current H Owner source was re-read at Blob `0dca3dc5463a02be0e19524811afbae87795baf5`. The current EN and zh-CN companions both pin this exact Blob and contain §11.8. The earlier H parity report published in this PR used the prior source SHA `db59b63e322d7255b8b400f47859dcac32bb3027`; it is superseded by the current-source review and must not be used as evidence for the current H source revision.

## 6. Final decision

- C/G/H semantic alignment for the six-stage lifecycle and core authority boundaries: **PASS WITH ENUMERATED EXCEPTIONS**.
- CGH-APPLIED-1.1 recovery-batch evidence completeness across C/G/H: **BLOCKED**.
- H 1.1 schema/SDK freeze: **NOT ESTABLISHED**.
- Exact-version C/G/H joint acceptance: **NOT ESTABLISHED**.
- Runtime/conformance/production verification: **NOT VERIFIED / NOT RUN**.
- PR #28 remains Draft/Open; this review does not authorize merge.

No finding in this report upgrades any Owner status, approves implementation, proves global Forget completion or proves physical erasure.
