# Module B — Domain Model Baseline & Redlines

- Proposal: B-MBR-0.1.0
- Status: **PROPOSED — prepared by Session P for B Owner review/adoption; NOT a B Owner decision**
- Intended Owner: B — Domain Model
- Source branch / HEAD: `session-b-domain-model-phase3` @ `0cf703a3fec9921aeb8e6252a8ac4708b8b723b3`
- Evidence: `02-domain-model/typed-reference-registry.md` blob `08af297cb010f7e6ac5e3f29daa4469be112e12e`; `02-domain-model/ADR-001-fact-claim-semantics.md` blob `a1024938ff5baba069cf128c69496a44e143330c`; `02-domain-model/phase-3.6-typed-identity-trust-closure.md` blob `0a6b78a842e550b58533b797cdfcd2d954ed6826`
- Project PB/PR: P proposal v0.1.0 only, not approved/active.

## 1. Module Mission
Define stable domain meaning, identity/reference semantics and invariants for Memory Brain objects without conflating assertions, evidence, provenance, identity and authorization.

## 2. Ownership Baseline
B owns domain taxonomy, typed reference semantics, identity/reference type distinctions and domain-level invariants. B does not own credential validation, issuer trust, permission policy, wire encoding, canonical persistence, compiler execution, retrieval or Context operations.

## 3. Capability Baseline
Maintain typed object/reference registry; define lifecycle and immutability semantics; preserve provenance and time dimensions; define schema evolution and compatibility constraints; provide domain-level positive/negative conformance vectors. Unknown/incompatible reference types must fail closed.

## 4. Domain Ownership
B owns meaning of Event, Memory, Claim/Fact subject to ADR-001, Entity, Relation, Evidence, Provenance and typed references including PrincipalRef/ActorRef/ScopeRef semantics. I owns security trust and authorization decisions; H owns transport encoding/binding; D owns canonical identity/commit; E owns compiler lifecycle.

## 5. Interface Baseline
TypedRef is discriminated, namespaced and opaque; reference possession is not authentication or permission. Deserialization proves syntax/type only, not existence, trust, lifecycle or authorization. Exact wire encodings remain with H and relevant consumer acceptance.

## 6. Security Baseline
No payload-supplied ID, display name, email, model name or caller string is an authenticated identity. Credentials/secrets must not be embedded in references. Permission is I-owned and cannot be inferred from ScopeRef.

## 7. Module Redlines
- B-PR-01 Never collapse Identity, Reference, Credential, Authenticated Binding and Permission. Severity CRITICAL.
- B-PR-02 Never infer truth from model output, extraction confidence or reference syntax. HIGH.
- B-PR-03 Never change Fact/Claim semantics without ADR-001 authority decision and migration approval. CRITICAL.
- B-PR-04 Never freeze wire field encoding under B's domain decision alone. HIGH.
- B-PR-05 Never let a typed reference grant authorization or bypass issuer/scope checks. CRITICAL.

## 8. Forbidden Cross-module Actions
B must not validate credentials or issue permission decisions (I); define BMCP wire schema (H); commit canonical memory (D); publish compiler artifacts (E); mutate retrieval indexes (F); update Context state (G).

## 9. Dependency Contracts
Consumers include C/D/E/F/G/H/I. Principal/ActorRef/ScopeRef semantics require B/I/H joint exact-version acceptance. Fact/Claim remains **ADR-BLOCKED**; no option or recommendation is a decision.

## 10. Conformance Requirements
Unknown discriminator rejection; namespace/issuer preservation; immutable-version vs mutable-head distinction; credential/reference confusion rejection; cross-scope reference misuse; Fact/Claim migration and provenance tests after ADR decision.

## 11. Acceptance Criteria
B Owner accepts exact proposal version; all domain terms link to owner decisions/ADRs; OPEN semantics remain blocked; affected consumers accept the same typed-reference contract; schemas and tests are versioned.

## 12. Change Authority
B Owner decides B-owned domain semantics subject to approved project constraints. ADR-001 authority remains explicitly unresolved in source; cross-owner reference contracts require affected Owners.

## 13. Open Decisions
ADR-001 Fact/Claim authority and selected model; exact identity registry authority/issuer lifecycle; typed reference serialization compatibility with H; B/I/H acceptance and migration plan.

## 14. Explicit Non-Claims
No ADR-001 approval; no wire schema freeze; no credential or permission policy approval; no implementation/conformance claim.
