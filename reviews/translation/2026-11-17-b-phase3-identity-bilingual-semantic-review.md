# B Phase 3 Identity Bilingual Semantic Parity Review — 2026-11-17

- Review ID: BSR-28-B-IDENTITY-001
- Target: PR #28, branch `docs/bilingual-coverage-completion`
- Scope: two exact B Owner-branch Phase 3 identity artifacts and their Chinese/English companions
- Review mode: source-pinned, section-by-section semantic and structural cross-check
- Disposition: **PAIRING COMPLETE; TARGETED SEMANTIC REVIEW PASS WITH SOURCE-STATUS LIMITATIONS**
- This review is not B Owner approval, I governance approval, H wire freeze, D/E schema acceptance, ADR-001 approval, or implementation/conformance verification.

## 1. Exact source and companion bindings

| Artifact | Owner source branch | Exact source Blob SHA | English companion Blob SHA | Chinese companion Blob SHA |
|---|---|---|---|---|
| Typed Reference and Scope Semantics | `session-b-domain-model-phase3` | `e9a6bd21e06bc02a5208619f5a949217860b1c00` | `fa9c71f10d0cd797f2f213c1e0130388b3f1c85a` | `67d1d6d7011cf8c722d38273542cf4859d0a2491` |
| Principal / Actor Binding and Consumer Compatibility Matrix | `session-b-domain-model-phase3` | `bbbef919e1e2ffe158cda8d9b2c5e718efaae969` | `b3c4ff7fb36eebc2284c3169e6c73db1659c7f34` | `03e9173955b61ad7fa778b510bc9756cb6435271` |

The English companions retain the Owner source content with companion metadata and reciprocal language links. Both Chinese companions identify the exact Owner source Blob and link back to English.

## 2. Structural parity checks

| Check | Typed Reference / Scope | Principal / Actor |
|---|---:|---:|
| Source heading count | 37 | 16 |
| English heading count | 37 | 16 |
| Chinese heading count | 37 | 16 |
| Source Markdown table rows (including header/separator) | 11 | 80 |
| English table rows | 11 | 80 |
| Chinese table rows | 11 | 80 |
| Source sections preserved in order | PASS | PASS |
| Reciprocal language links | PASS | PASS |
| Exact source Blob pin recorded | PASS | PASS |

No missing numbered section or table row was found in the companion pair readback.

## 3. Semantic invariants reviewed

### 3.1 Typed references and namespace
- BrainAuthority is part of canonical identity; opaque IDs are authority-local and never reused.
- Scope is not an ID namespace and a Scope hint is not permission.
- Stable identity references remain distinct from exact immutable version/revision references.
- ClaimRef and ClaimRevisionRef remain conditional on ADR-001; no canonical Claim identity is authorized while INT-P0-01 is blocked.
- Entity identity is not inferred from labels; Evidence access is independently restricted; Event producer-local IDs are namespaced by authenticated producer/source identity.
- TimeValue/TimeInterval preserve precision, uncertainty, half-open interval semantics, and the distinction among Event Time, Recorded At, Commit/Transaction Time and Valid Time.

### 3.2 Scope / Environment / Permission
- ScopeRef, EnvironmentRef, Permission and I Policy Domain remain orthogonal.
- Owner Scope and applicability Scope remain separate roles; they are not flattened into an unordered union.
- Containment does not imply permission/visibility inheritance.
- Cross-Scope and cross-Environment access default-deny; explicit grants/bridges require I policy and exact binding.
- Scope mismatch remains a domain validation result; Permission Denied remains an authorization result.
- Missing/ambiguous required EnvironmentRef remains INDETERMINATE/block, not wildcard/default.

### 3.3 Principal / Actor / Agent / Adapter / Producer
- Issuer, authenticated Principal, per-operation ActorRef, logical AgentRef, AdapterRef, ProducerRef, ScopeRef, EnvironmentRef and PermissionDecision remain distinct.
- Authentication precedes payload identity resolution; protected verifier/transport context is authoritative, not payload claims.
- ActorRef is verifier-issued, per-operation, historically immutable and not a durable permission/bearer token.
- Delegation does not convert identity or transfer ownership; acting-for semantics and effective authority remain I-governed.
- Revocation preserves historical attribution but does not establish current permission; in-flight effects remain policy/owner-bound and unresolved.
- Producer origin remains distinct from executing collector; D work registration remains distinct from I ProducerDomain inventory.
- PermissionEpoch, ForgetFence, CapabilityEpoch, RuntimeSessionRef and owner-local cursors are not interchangeable.

### 3.4 Consumer field mapping
- C telemetry fields remain claims to compare with trusted bindings, not credentials.
- D author/scope/environment aliases remain typed and migration remains D-owned.
- E preserves origin producer, collector, ActorRef, Scope/Environment through ingress/retry/compile/publication.
- H source/recipient and protected auth context remain candidate wire mappings; this translation does not freeze wire names/encodings.
- I remains the authorization owner; Scope resolution is not authorization.

## 4. Source state preserved — not promoted

| Gate / decision | Preserved state |
|---|---|
| B typed-reference and Scope contract | CANDIDATE |
| B Principal/Actor mapping | CANDIDATE |
| INT-P0-02 / INT-X-03 identity freeze | OPEN |
| ClaimRef / ClaimRevisionRef and ADR-001 | ADR-BLOCKED |
| I36-GOV-01..06 | GOVERNANCE-BLOCKED / OPEN as stated by source |
| H wire names/encoding | CANDIDATE / OPEN |
| C telemetry field confirmation | CANDIDATE / OPEN |
| D/E field alias and EnvironmentRef migration | OPEN |
| Runtime session issuer/lifetime/binding | OPEN |

No source decision status was promoted in translation or in this review.

## 5. Findings and limits

- No material Chinese/English semantic divergence was found in the reviewed two companion pairs.
- The source contains candidate proposals and unresolved policy decisions. The review confirms translation parity with those candidate statements; it does not validate that the proposed architecture is approved or feasible.
- The malformed punctuation in the source EventRef uniqueness tuple is not repeated in the Chinese prose; the intended tuple semantics remain `(BrainAuthority, event_id)`. If the Owner wants literal source errata, B should correct the source artifact in a separately versioned commit.
- The English companion mirrors the exact source body; source wording issues are therefore not silently edited in the English companion.
- No executable identity tests, cross-owner consumer acceptance, H transport conformance, I policy execution, D/E schema migration or production behavior were tested here.

## 6. Disposition

1. Mark these two Phase 3 source artifacts **PAIRED** in the PR coverage register.
2. Record targeted bilingual semantic parity as PASS, with source candidate/blocked statuses unchanged.
3. Keep INT-P0-02 / INT-X-03 OPEN and ADR-001 ADR-BLOCKED.
4. Obtain B Owner confirmation and I/H/C/D/E cross-owner review before freezing identity semantics or public fields.
5. Continue next with C/G/H Applied detailed contract companions, then I identity trust and Storage/Consistency detailed contracts.
6. Keep PR #28 Draft/Open; do not merge on the basis of this review.
