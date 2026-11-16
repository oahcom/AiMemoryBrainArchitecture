# G Owner — JF-10 ↔ COC Bridge Applied-Evidence Acceptance

- Owner: G — Memory Context
- Branch: `session-g-memory-context`
- Decision mode: delegated G-boundary review performed centrally under the user's instruction to accept the remaining work; not an independent human signature.
- Exact A CGH package: `reviews/integration/phase-3.6-cgh-applied-1.1-causal-order-decision-package.md`, Blob `4961ffefc0f9920efb8425a9b2a7af42d8f64819`
- Exact A COC/JF-10 bridge: `reviews/integration/phase-3.6-causal-order-coordinator-deployment-architecture.md`, Blob `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d`
- H JF-10 bridge schema candidate: `08-bmcp-protocol/schemas/bmcp.applied-ack-1.1.0-jf10-bridge.schema.json`, Blob `a8a945cc3623c2907003b93625e3c79742150944`
- G Applied/Forget contract: `06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md`, Blob `aa3afa73d8a76cc6f025839c52bfbff6a983046a`
- G Context versioning: `06-memory-context/context-versioning.md`, Blob `05c0739d0c22576a1fd5affc7d73c078c89049b1`
- Date: 2026-11-17
- Decision: **ACCEPT WITH ENUMERATED EXCEPTIONS — G APPLIED/EVIDENCE BOUNDARY ONLY**

## 1. Decision

G accepts the exact A CGH-APPLIED-1.1 package and A COC/JF-10 bridge as the causal-order evidence source for G's Full Applied validation, subject to the binding rules below. This acceptance does not make G a COC participant authority, I authorization authority, D Forget authority, Storage visibility authority, C provider-outcome authority or H wire-schema authority.

## 2. G-owned acceptance conditions

1. G may record Full Applied only after validating the exact C-owned final-request/provider submit outcome, H integrity/transport evidence, I terminal authorization evidence, D lineage-bound clearance/barrier evidence, and the COC terminal proof bound to the same immutable transaction/digest/reservation tuple.
2. COC intent, quorum position, recovery batch, I COMMIT_WON, D clearance, Storage prepared receipt, H ACK or reservation alone is never sufficient for Full Applied.
3. COC records are ordering/participant-accounting evidence only. G does not infer owner decisions from COC observations and does not compare COC/I/D/Storage positions.
4. Any COC outage, missing/invalid quorum prefix, pending owner-local cutoff, incomplete recovery batch, unresolved pre-batch participant, stale owner high-water, missing I terminal, incomplete D lineage barrier, unknown Storage resolution or unknown C provider outcome blocks new Full Applied promotion and protected current use.
5. Historical Applied remains immutable only if it was validly committed under the predicate effective at that time. Current-use is separately recomputed against current Context head/version, I authorization/PermissionEpoch, D fence/lineage, Scope/Environment, RuntimeSession and Adapter capability.
6. Recovery-batch completion does not imply provider success or Applied. C must still supply determinate CSubmitOutcome and the common terminal proof must bind it.

## 3. Exceptions and owner boundaries

- G does not validate COC consensus/quorum durability, leader election or snapshot signatures; those remain Storage/COC infrastructure responsibilities.
- G does not decide the I single-use CommitAuthorizationReceipt or revocation terminal outcome.
- G does not decide D fence generation, request/effective position, lineage inventory or barrier semantics.
- G does not decide Storage's exact-XID commit/rollback or VisibilityPointer/PublicationReceipt transaction.
- G does not decide C provider idempotency or actual provider acceptance.
- G does not approve H cryptographic algorithms, key custody or generated SDK interoperability.
- Multi-I-PolicyDomain atomicity remains BLOCKED / NOT ACCEPTED.
- G's Applied validator/persistence implementation and COC/JF-10 end-to-end conformance remain NOT VERIFIED / NOT RUN.

## 4. Required G conformance

Required fixtures: valid complete terminal proof; I revocation-first; D fence-first; provider UNKNOWN; COC quorum unavailable; recovery batch missing one request; pre-batch participant omitted; owner high-water regression; stale checkpoint/RESTORE_FENCED; same identity/digest replay; changed digest conflict; old historical Applied invalidated for current use after Forget/revocation; and H capability downgrade.

A PASS requires executable G implementation, exact schema/version, current owner lookups, deterministic race/fault injection, durable Applied readback and independent review. This document is a design-level acceptance only; no implementation, integration test, production activation, Global Forget completion or physical erasure is claimed.