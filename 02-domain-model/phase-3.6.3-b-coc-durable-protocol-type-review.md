# B Owner — Exact COC Durable Protocol Type-Boundary Review

- Exact Storage protocol Blob: `4ac63ac79491e79ec0c9114ef73941c73d7bbf25`
- A COC architecture Blob: `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d`
- B typed identity baseline Blob: `0a6b78a842e550b58533b797cdfcd2d954ed6826`
- Decision: **ACCEPT WITH BINDING B TYPE CONSTRAINTS**
- Mode: delegated B-boundary review under user instruction; not independent human sign-off.

B accepts the protocol's immutable reference and namespace model within B's domain-type authority:
1. COC CoordinatorEpoch/Index/ConfigurationEpoch, I sequencer epoch/position/PermissionEpoch, D fence cutoff/effective position/ForgetFenceGeneration, Storage XID/transaction position, CanonicalCommitCursor and ContextVersion remain distinct types.
2. CausalOrderDomainRef, PolicyDomainRef, ScopeRef, EnvironmentRef, PrincipalRef, ActorRef, ProducerRef, RuntimeSessionRef and owner-specific operation references are not interchangeable.
3. Opaque refs are issuer-namespaced; no embedded-ID parsing, numeric coercion, lexical cross-authority ordering or cast is permitted.
4. Stable OperationId + canonical digest idempotency is accepted; same identity with changed authority, participant, digest, XID or boundary is a conflict.
5. COCCommitReceipt proves only COC log commitment. It does not prove I authorization, D clearance, Storage visibility, C provider success or G Applied.

Exceptions: B does not approve Raft implementation, signature algorithm, H encoding, I policy, D fence semantics, Storage transaction profile or COC deployment. Fact/Claim ADR-001 remains ADR-BLOCKED; no domain schema or wire freeze is implied.

Required conformance: typed round-trip; cross-type substitution rejection; issuer mismatch; malformed/empty ref rejection; same-digest replay; changed-digest conflict; and no cross-authority position comparison. No runtime/fuzz/schema interoperability tests are claimed.