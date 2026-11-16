# B Owner — Exact CGH-APPLIED-1.1 Typed-Reference Acceptance

- Owner: B — Domain Model
- Branch: `session-b-domain-model-phase3`
- Decision mode: delegated B-boundary review performed centrally under the user's instruction to accept the remaining work; not an independent human signature.
- A package: `reviews/integration/phase-3.6-cgh-applied-1.1-causal-order-decision-package.md`
- Exact A package Blob: `4961ffefc0f9920efb8425a9b2a7af42d8f64819`
- Companion COC architecture: `reviews/integration/phase-3.6-causal-order-coordinator-deployment-architecture.md`
- Exact COC Blob: `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d`
- B typed identity baseline: `02-domain-model/phase-3.6-typed-identity-trust-closure.md`, Blob `0a6b78a842e550b58533b797cdfcd2d954ed6826`
- B joint BIH acceptance addendum: Blob `2abf2784051a4ef1430d4acfacbdfd234d7553fc`
- Date: 2026-11-17
- Decision: **ACCEPT WITH ENUMERATED BOUNDARIES — B-OWNED TYPE SEMANTICS ONLY**

## 1. Decision

B accepts the exact A CGH-APPLIED-1.1 package and companion COC bridge at the B domain-model boundary, subject to the typed-reference and identity constraints below. This is not an acceptance of COC consensus, I authorization, D ForgetFence semantics, Storage transaction semantics, H wire encoding, G Applied state, provider success, or production deployment.

## 2. B-owned semantic acceptance

1. All authority-bearing references remain distinct opaque types: PrincipalRef, IssuerRef, ActorRef, AgentRef, AdapterRef, ProducerRef, ScopeRef, EnvironmentRef, RuntimeSessionRef, PolicyDomainRef, CausalOrderDomainRef, CausalOrderTransactionRef, PublicationOperationId and StorageParticipantRef/XID references.
2. ActorRef is verifier-produced, immutable and operation-specific attribution. It is not a Principal alias, credential, grant or proof of authentication.
3. ScopeRef expresses ownership/applicability and is not interchangeable with EnvironmentRef, PolicyDomainRef or CausalOrderDomainRef.
4. COC, I, D and Storage positions remain distinct typed namespaces. No parsing, arithmetic, ordering, casting or substitution across COC epoch/index, I sequencer epoch/position, D fence cutoff/effective position, Storage transaction/XID position, CanonicalCommitCursor, ForgetFenceGeneration, PermissionEpoch or ContextVersion.
5. A caller-supplied reference is a selector/claim until authenticated and resolved by the authority responsible for it. COC may preserve and bind owner-issued references but cannot mint them.
6. Immutable request/participant tuples are compared by exact typed identity and canonical digest. Same identity + same digest is idempotent; same identity + changed digest is a conflict, not a merge.
7. The one-I-PolicyDomain limitation is explicit. Multi-policy-domain atomicity remains blocked; no best-effort cross-domain aggregation is a valid single operation.

## 3. Exceptions and retained blocks

- B does not decide I's Principal/issuer trust, grants, PermissionEpoch or revocation policy.
- B does not decide H's BMCP schema, encoding, canonicalization profile or signature format.
- B does not decide D's fence request/effective ordering, lineage closure or barrier completion.
- B does not decide Storage's XID, transaction isolation, commit/rollback or visibility pointer.
- B does not decide C's provider submission outcome or G's Full Applied predicate.
- Fact/Claim ADR-001 remains **ADR-BLOCKED**. This acceptance does not choose either candidate model and does not permit dependent canonical schema/wire fields to freeze.
- No domain schema, serialization, database or wire schema freeze is implied.

## 4. Required consumer behavior

Consumers must reject malformed, untyped, wrong-issuer, cross-domain or rebound references. Unknown, stale, mismatched or unverifiable references fail closed. A COC record position is not a substitute for an owner-issued I/D/Storage outcome. No component may derive authority by parsing an opaque reference string.

## 5. Conformance and non-claims

Required future tests: typed-reference round trips; cross-type substitution rejection; wrong issuer/authority rejection; empty/oversized reference rejection; same-key/same-digest replay; same-key/different-digest conflict; multi-policy-domain rejection; and compatibility tests for unknown fields/schema versions.

This is architecture/interface acceptance only. No runtime identity verifier, cryptographic signature implementation, schema interoperability, fuzzing, migration, provider integration, production deployment or independent human sign-off was performed.