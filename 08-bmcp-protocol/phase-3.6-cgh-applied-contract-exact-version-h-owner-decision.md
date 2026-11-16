# H Owner Formal Decision — Exact A C/G/H Applied Contract Package

- Owner: Session H — BMCP Protocol & Adapter Authentication
- Branch: session-h-bmcp-protocol
- Decision date: 2026-11-16
- Decision: **APPROVE WITH ENUMERATED EXCEPTIONS**
- Decision scope: H-owned BMCP transport, ACK, capability, integrity/replay and reconnect semantics only
- Exact A package: reviews/integration/phase-3.6-cgh-applied-contract-decision-package.md
- Exact A package Blob SHA: 122b164bcc0760b83bf555072a36fc55631623e1
- Prior H decision package Blob: 61d961c32138fd875069e8cbac4696bb031447c0
- H normative source: 08-bmcp-protocol/phase-3.6-authenticated-identity-protected-operation-binding.md
- H normative source Blob: 9845c97ac43d7888732afafe12e28850ec02add8
- H prior exact-package decision: 08-bmcp-protocol/phase-3.6-bih-joint-architecture-acceptance-addendum.md, Blob eb8f4108491c8aa78bcf1ea33f0c85a596bb40c8
- Related coordination request: Issue #3

## 1. Exact-version review and decision

H reviewed the exact A package Blob SHA 122b164bcc0760b83bf555072a36fc55631623e1, not merely the path or a moving branch name.

H previously issued an APPROVE WITH ENUMERATED EXCEPTIONS decision against package Blob 61d961c32138fd875069e8cbac4696bb031447c0. A content comparison confirms that the current package retains the same normative lifecycle, semantic field mapping, H wire decisions requested, temporal decision, Full Applied predicate, conformance cases and stop conditions. The delta from the prior package is the appended §14 live Owner evidence reconciliation and coordination trail; it adds current Owner readbacks and status, and does not alter the normative H contract clauses.

**H therefore renews and explicitly records its decision against the exact current package Blob 122b164bcc0760b83bf555072a36fc55631623e1: APPROVE WITH ENUMERATED EXCEPTIONS.**

This is a formal H Owner technical decision for the exact same A Applied Contract version referenced by Issue #3. It supersedes the stale package pin in H's earlier Phase 3.6.2 decision record. It does not claim C/G approval, I/D authorization/fence approval, global Applied Contract freeze, production schema freeze, implementation verification or runtime conformance.

## 2. H acceptance

H accepts the following H-relevant contract requirements in the exact package:

1. **Evidence-family separation:** Delivery receipt, Materialization evidence, C Final Request Submitted evidence, G Applied record/result, Runtime Execution Started and D Forget ACK remain distinct evidence families. A transport ACK is not proof of final request submission or G Applied. A Forget ACK is never Applied evidence.
2. **Transport identity binding:** BMCP messages and ACKs bind the protected verifier context, authenticated issuer/principal, verifier-resolved ActorRef, Adapter application and concrete instance, Agent/runtime instance, fresh RuntimeSessionRef, exact operation/delivery/context identity, role-tagged ScopeRefs and applicable EnvironmentRef.
3. **Independent authority namespaces:** PermissionEpoch (I), ForgetFenceGeneration/lineage (D), ContextVersion/Delivery state (G) and CapabilityEpoch (H) remain distinct opaque typed namespaces. H does not compare, mint, substitute or reinterpret owner tokens.
4. **ACK integrity and idempotency:** ACKs bind immutable ACK identity and canonical evidence digest, operation/attempt/session, relevant epoch/fence/capability values and authenticated transport context. Same idempotency key plus same digest is idempotent; same key plus different digest is a conflict. Old-session, replayed, stale, superseded or late ACKs cannot mutate newer owner state.
5. **Trusted ordering:** Sender wall-clock timestamps are evidence metadata, not ordering authority. H provides trusted receiver ingress/receipt evidence; the owning authority orders acceptance against its own authoritative commit cursor. Indeterminate order remains historical evidence only and cannot promote state.
6. **Capability and reconnect:** Capability negotiation is per concrete Adapter instance and epoch. Unknown required capability, unsupported schema/critical enum, downgrade, stale session, replay or failed currentness check fails closed. Reconnect requires fresh authentication, current I PermissionEpoch, current D fence, stale-state suppression and G journal reconciliation before resume.
7. **Fail-closed behavior:** Missing, malformed, ambiguous, untrusted or unsupported security-critical bindings do not fall back to payload claims or optimistic success.

## 3. Enumerated H exceptions and binding limits

### H-EX-01 — No concrete Applied wire-schema freeze in this decision

The exact A package's §§4–5 and the semantic field mapping are accepted as the requested logical contract, **not as a frozen wire schema**.

This H decision does not yet publish or freeze the concrete versioned BMCP schema package required by Issue #3. The following remain H-owned and must be delivered as a separately versioned, reviewable schema artifact before Applied Contract Frozen can become YES:

- schema IDs and versioned message definitions for Delivery receipt, Materialization, Final Request Submitted evidence transport, Applied evidence/result and Execution Started;
- separate message/status enums for Forget action ACK and Applied evidence/result;
- exact field names, types, cardinality, requiredness and unknown-field/enum behavior;
- canonical serialization and digest profile;
- signature/MAC algorithm suite, issuer/key identifiers, key lifecycle and rotation;
- nonce/replay window, trusted receiver sequence, durable ACK journal and retention;
- stable idempotency namespace and duplicate/conflict response encoding;
- capability negotiation and CapabilityEpoch wire representation;
- reconnect and downgrade behavior at the schema/version boundary.

Until this artifact is published and owner-reviewed, existing logical names are candidate mappings, not wire compatibility guarantees. No implementer may infer frozen JSON/CBOR/Protobuf field names from this decision.

### H-EX-02 — C owns final submission facts

H transports and verifies C-produced submission evidence and its integrity envelope. H does not create or certify the actual immutable provider request, successful provider submit boundary, runtime-assigned InferenceRequestId, FinalRequestBoundaryId or complete Managed Region digest. C owns these facts and the evidence ceiling for each integration tier.

### H-EX-03 — G owns Applied semantics and state

H does not decide the Full Applied predicate, append or mutate G's Applied record, determine historical Applied truth, or decide current-use eligibility. H transports authenticated evidence and protocol receipts. G alone owns Applied commit, idempotency, supersession and current-use projection. G must independently validate the exact C evidence and authority predicates.

### H-EX-04 — I authorization remains independent

H does not issue or validate policy as I's authority, mint PermissionEpoch, authorize the operation, or determine revocation outcome. H transports opaque I evidence unchanged. Missing, stale, revoked, incomparable or indeterminate PermissionEpoch/authorization evidence remains deny/Unknown at the I and consumer boundary.

### H-EX-05 — D ForgetFence and lineage remain independent

H does not issue, advance, compare or validate D ForgetFenceGeneration/lineage as D's authority and cannot infer forget completion from transport ACK. D owns fence semantics and causal ordering proof. Missing, stale, incomplete or incomparable fence/lineage evidence remains blocked/Unknown.

### H-EX-06 — B types and namespace semantics

H preserves typed ActorRef, ScopeRef and EnvironmentRef bindings and namespace dimensions but does not redefine B's type semantics. B's formal semantic mapping confirmation is separate and does not freeze H wire field names or authorize any cross-Scope/Environment access.

### H-EX-07 — Verification not run

H36 and the added ACK/revocation/reconnect race cases remain SPECIFIED / NOT RUN. This decision is not implementation verification, security certification, production readiness or runtime conformance.

## 4. H closure obligations

Before H can claim the H-specific schema deliverable on Issue #3:

1. Publish the concrete versioned schema artifact enumerated in H-EX-01 on the H Owner branch.
2. Pin exact schema artifact Blob SHA and identify its compatibility/versioning policy.
3. Show separate schema families for Forget ACK and Applied evidence/result.
4. Include canonicalization, cryptographic integrity, replay/idempotency, receiver ordering, capability negotiation and reconnect definitions.
5. Map every schema field to its issuing authority and validation owner (C/G/H/I/D/B) and specify missing/unknown/unsupported behavior.
6. Add reproducible schema-validation and H36 test vectors; mark tests NOT RUN until actual commands, fixtures, outputs, logs and reviewer evidence are attached.

## 5. Gate disposition

| Gate / question | H disposition |
|---|---|
| H decision on exact A package Blob 122b164bcc0760b83bf555072a36fc55631623e1 | **APPROVE WITH ENUMERATED EXCEPTIONS** |
| H logical transport/ACK/capability/reconnect semantics | **ACCEPTED WITH EXCEPTIONS** |
| H concrete versioned Applied wire schema | **OPEN — NOT FROZEN / NOT YET DELIVERED BY THIS DECISION** |
| C final submission evidence and evidence ceiling | C authority; this H decision does not approve for C |
| G Full Applied predicate and Applied state | G authority; this H decision does not approve for G |
| I PermissionEpoch/authorization predicate | I authority; external governance remains separate |
| D ForgetFence/lineage/order predicate | D authority |
| B typed-reference semantics | B separately confirmed; no H wire freeze implied |
| H36 / race conformance | **SPECIFIED / NOT RUN** |
| Applied Contract Frozen | **NO** |
| Implementation verified / production schema frozen | **NO / NO** |

## 6. Instruction to A and Issue #3

A may record H as having made an explicit exact-version decision against package Blob 122b164bcc0760b83bf555072a36fc55631623e1 with disposition APPROVE WITH ENUMERATED EXCEPTIONS, and may use this artifact's Blob SHA/commit as the H Owner evidence.

A must retain the following distinctions:
- H's exact-version decision is now recorded; the previous H decision against Blob 61d961c32138fd875069e8cbac4696bb031447c0 is superseded for current package pinning.
- H's concrete versioned Applied wire schema remains OPEN until separately published and pinned.
- C and G must still decide the same exact A package version in their own authority-controlled records.
- I and D authority predicates remain separate prerequisites.
- Applied Contract Frozen remains NO; no test or implementation PASS is claimed.

No branch merge is authorized by this decision.
