# Phase 3.6 Identity / Applied / Storage Source Audit — 2026-11-17

- Review ID: BSR-28-BATCH-AUDIT-001
- Target: PR #28, branch `docs/bilingual-coverage-completion`
- Review mode: independent source-artifact readback and exact Blob SHA comparison
- Result: targeted source inventory refreshed; detailed contract bilingual coverage remains incomplete
- This report does not approve architecture, freeze cross-owner contracts, or verify implementation.

## 1. Exact Owner source artifacts re-read

| Domain | Owner source path | Branch | Exact Blob SHA read now | Source status / evidence boundary |
|---|---|---|---|---|
| B typed reference / Scope | `02-domain-model/typed-reference-and-scope-semantics.md` | `session-b-domain-model-phase3` | `e9a6bd21e06bc02a5208619f5a949217860b1c00` | CANDIDATE; ClaimRef conditional on ADR-001; identity/Scope/Environment approvals remain open |
| B Principal / Actor mapping | `02-domain-model/principal-actor-binding-mapping.md` | `session-b-domain-model-phase3` | `bbbef919e1e2ffe158cda8d9b2c5e718efaae969` | CANDIDATE; INT-P0-02 / INT-X-03 OPEN |
| C final-request evidence | `07-agent-integration/phase-3.6-final-request-evidence-contract.md` | `session-c-agent-integration-2026-11-16` | `fd2f47ba6c89bb270e9f2bec956873cb7ae3592b` | C decisions recorded; C/G/H cross-owner freeze BLOCKED; implementation/execution NOT VERIFIED |
| G Applied/Forget reconciliation | `06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md` | `session-g-memory-context` | `aa3afa73d8a76cc6f025839c52bfbff6a983046a` | G decisions recorded; C/G/H freeze BLOCKED; implementation/execution NOT VERIFIED |
| H authenticated identity binding | `08-bmcp-protocol/phase-3.6-authenticated-identity-protected-operation-binding.md` | `session-h-bmcp-protocol` | `e7ca5ce4ece5d8fd77fe0760e49a85afa0133248` | JOINT-DECIDED technical baseline; governance/consumer acceptance OPEN; implementation/conformance NOT VERIFIED |
| H identity consumer/conformance status | `08-bmcp-protocol/phase-3.6-identity-binding-consumer-conformance-status.md` | `session-h-bmcp-protocol` | `8afb914731a34d8ab44331f54f1f39bfd8ec37ce` | Technical design JOINT-DECIDED; C/F/G consumer acceptance OPEN; governance BLOCKED; H36 NOT RUN |
| I identity trust policy | `09-security-governance/phase-3.6-identity-trust-policy-joint-closure.md` (not restored on main; see AID-2026-107 §10) | `session-i-security-governance-2026-11-16` | `0cbf6bb7480db873790c454817593a9b1c5548ba` | JOINT-DECIDED technical baseline; governance BLOCKED; implementation/conformance NOT VERIFIED |
| Storage visibility participant/outcome | `reviews/storage-consistency/phase-3.8-storage-visibility-participant-and-atomic-outcome-contract.md` | `session-storage-consistency-forget-atomicity-2026-11-16` | `175ee7b1349cfdb79a19898b311a88391ed88010` | Logical transaction proposal; physical topology and implementation proof OPEN |
| Storage serialization topology ADR | `reviews/storage-consistency/phase-3.8.2-storage-serialization-topology-adr.md` | `session-storage-consistency-forget-atomicity-2026-11-16` | `1ef47d4e5711c7db73a24d249adf1992be1f6aa4` | ADR-BLOCKED; candidate options only; no deployed topology selected |
| Storage JF-10 recovery | `reviews/storage-consistency/phase-3.6.2-jf10-cross-authority-recovery-protocol.md` | `session-storage-consistency-forget-atomicity-2026-11-16` | `94679897e84a6f58fd8b9467b5249e1a885cb0b0` | Candidate; I acceptance required; NOT IMPLEMENTED; NOT RUN; JF-10 P0 OPEN |
| Storage restore high-water/quarantine | `reviews/storage-consistency/phase-3.6.5-restore-control-highwater-and-quarantine-contract.md` | `session-storage-consistency-forget-atomicity-2026-11-16` | `4f656163aeba532a441eaed1d293a48e2363cb4a` | Candidate; exact I-D-A-Storage review required; restore remains fenced absent current control high-water proof |

These are exact file Blob SHAs returned by readback from the named Owner branches. They are not branch HEAD SHAs and do not imply source approval.

## 2. Findings

### BSR-28-005 — H identity status embeds a stale source Blob reference

- Severity: P1 — source-currentness / traceability
- Status: OPEN
- The H identity consumer/conformance status artifact (`8afb914731a34d8ab44331f54f1f39bfd8ec37ce`) records the historical H protected-operation binding Blob as `9845c97ac43d7888732afafe12e28850ec02add8`.
- A fresh read of the same path on the live `session-h-bmcp-protocol` branch returned `e7ca5ce4ece5d8fd77fe0760e49a85afa0133248`.
- The historic record must not be silently rewritten. H should append a dated currentness correction that identifies the new Blob, records whether BIH36-JD-01..17 semantics changed, and re-runs the exact source-to-status consistency check.
- The new PR #28 bilingual companion explicitly preserves the historical value and calls out the discrepancy. This is not closure of the Owner-side finding.

### BSR-28-006 — Storage topology ADR source reference changed since the prior audit

- Severity: P1 — source-currentness / topology governance
- Status: OPEN
- The earlier audit summary cited Storage topology Blob `080433f8e13a500522bc2754da64057edb0ae9d8`.
- Fresh readback of the same Owner branch path returned `1ef47d4e5711c7db73a24d249adf1992be1f6aa4`.
- Current source still declares ADR-BLOCKED, candidate options only, and no deployed topology selected.
- Refresh the Storage source inventory and inspect the delta before any translation or acceptance. Do not infer that a topology choice was made.

### BSR-28-007 — Detailed high-risk contracts remain outside PR #28

- Severity: P1 — bilingual scope / acceptance gate
- Status: OPEN
- PR #28 now includes a bilingual companion pair for H's identity consumer/conformance status report only. It does not add the H authenticated-identity normative contract, nor the B typed-reference/Principal mapping, C final-request, G Applied/Forget, I trust-policy, or Storage COC/JF-10/restore detailed contracts.
- The H status report is not counted as one of the seven H detailed core specifications.
- No B/C/G/H/I/Storage detailed contract set may be marked bilingual-complete or semantically accepted on the basis of this status report.
- Next translation batches must pin each exact source Blob SHA, preserve source state, create reciprocal language links, and receive independent semantic review.

## 3. Identity semantics independently rechecked

The refreshed B/H/I/C source material consistently distinguishes:
- IssuerRef, authenticated PrincipalRef, per-operation ActorRef, logical AgentRef, AdapterRef, ProducerRef, ScopeRef, EnvironmentRef and PermissionDecision;
- identity resolution from authentication, and authentication from authorization;
- protected verifier/transport context from caller-controlled payload claims;
- stable identity references from exact immutable version/revision references;
- Scope domain applicability/ownership from permission grants;
- PermissionEpoch, CapabilityEpoch, ForgetFenceGeneration, ContextVersion and owner-local cursors as distinct namespaces.

The B source remains CANDIDATE. The H protocol binding remains a joint technical baseline with governance/consumer acceptance OPEN. I governance remains BLOCKED. These statuses are not promoted by this review.

## 4. Applied proof boundary rechecked

C and G source contracts preserve the distinct evidence stages:

`Prepared → Delivered → Materialized → Final Request Submitted → Applied → Execution Started`

C evidence must bind the actual immutable post-transformation request at the observed successful submit boundary, including runtime-assigned InferenceRequestId, exact ContextVersion/Delivery identity, managed-region digest and current authorization/fence/capability bindings. G alone accepts Applied under its predicate. Applied does not prove model attention, understanding, memory use or correct behavior.

C/G/H cross-owner freeze remains BLOCKED; implementation and execution remain NOT VERIFIED. This is a source-semantic observation, not an Applied contract acceptance.

## 5. Storage/Consistency proof boundary rechecked

- Storage visibility proposal requires durable hidden participant preparation and an atomic final visibility transaction covering VisibilityPointer, PublicationReceipt/outcome and outbox.
- UNKNOWN remains private/nonterminal; timeout or missing ACK cannot imply commit or rollback.
- JF-10 remains candidate, requires I acceptance and same-XID recovery proof; implementation is NOT IMPLEMENTED and conformance NOT RUN.
- Restore begins quarantined/fenced and requires independent current owner control high-waters and participant reconciliation; no single cursor proves global safety.
- Physical topology remains ADR-BLOCKED; no PostgreSQL/XA/deployment capability is accepted by this source audit.

## 6. Disposition

1. Keep PR #28 Draft/Open and do not merge.
2. Add the H status report bilingual pair to the PR coverage overlay, explicitly separate from normative core-contract coverage.
3. Keep B Phase 3 identity, C/G/H Applied, I trust and Storage/Consistency detailed contracts pending.
4. Resolve BSR-28-005 in H's Owner branch and BSR-28-006 in Storage's Owner branch before relying on their manifests as current.
5. Continue with B typed-reference + Principal/Actor mapping as the next normative translation batch; then C/G/H Applied; then I and Storage/Consistency.
6. No implementation, conformance, production topology, or global architecture acceptance is claimed.
