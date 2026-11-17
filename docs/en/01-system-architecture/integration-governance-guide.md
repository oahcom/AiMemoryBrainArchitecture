# Principal Integration & Contract Governance Guide

- Document ID: DOC-INTEGRATION-001
- Version: 1.0
- Owner: A — Principal Integration Architect
- Source: A owner branch, Phase 3.5 Contract Registry and typed cursor/watermark coordination
- Chinese counterpart: [系统集成与契约治理指南](../../zh-CN/01-system-architecture/integration-governance-guide.md)
- Status: CANDIDATE coordination guide; no contract freeze or implementation approval

## 1. Why A exists

A maintains the cross-module system view. A coordinates contract dependencies, records which Owner has authority over each semantic token, identifies contradictions, and determines whether cross-module evidence is sufficient to advance an integration gate.

A is not a substitute domain owner. A's registry records and reconciles decisions; it does not create, approve, or override B–I contracts.

## 2. Evidence dimensions must remain separate

| Evidence dimension | What it proves | What it does not prove |
|---|---|---|
| Artifact Exists | Exact file is present and readable at a cited branch/HEAD | Owner approval or implementation |
| Owner Decision | Accountable Owner explicitly labels a semantic decision DECIDED in its artifact | Cross-module acceptance or runtime behavior |
| Cross-module Agreement | Affected authority owners/consumers accept the same contract and boundaries | Persistence correctness or tests passing |
| Implementation Evidence | Executable behavior and reproducible tests support the claim | Production approval unless governance gates also pass |

A document's status is not upgraded merely because it appears in a registry. A review conclusion is not an implementation test result.

## 3. Contract registry responsibilities

For every cross-module contract, record:
- Contract ID and exact document path.
- Owner and semantic authority.
- Consumer modules and their expected behavior.
- Exact branch, HEAD commit, and artifact revision reviewed.
- Status: DECIDED, CANDIDATE, ADR-BLOCKED, OPEN, TO_VALIDATE, NOT_RUN.
- Cross-owner acceptance evidence.
- Implementation/test evidence, separately from design evidence.
- Known incompatibilities, dependencies, and next closure action.

The registry must distinguish “file exists,” “Owner decided,” “consumers agree,” and “runtime proved.” Do not infer one from another.

## 4. Typed cursor and epoch governance

Tokens are typed and namespaced. A consumer must never compare, cast, increment, subtract, sort, or substitute values from different namespaces as if they were one scalar sequence.

Key namespaces include:
- CanonicalCommitCursor — D; one total order per Canonical Memory Authority.
- AggregateRevision — D; one aggregate only.
- LifecycleEventCursor — D; one Memory only.
- IndexWatermark — F; one index/channel partition, carrying D's applied-through cursor.
- ForgetFenceGeneration/Cursor — D; one Forget authority/operation and target lineage.
- Producer registration/high-water tokens — E/D contract boundary.
- PermissionEpoch — I; authorization policy generation.
- ContextVersion — G; one Context's authoritative sequence.
- AdapterCapabilityEpoch — H/C; one Adapter capability declaration epoch.

These are not interchangeable. Canonical commit progress is not index application; index watermark is not Forget completion; ContextVersion is not Applied; ForgetFenceGeneration is not PermissionEpoch.

## 5. Integration gates

A should coordinate closure in dependency order:
1. Domain and identity semantics: Fact/Claim ADR, typed Principal/ActorRef/ScopeRef, issuer/delegation binding.
2. Forget and revocation: durable fence, producer barriers, derivative inventory, local suppression, backup/external-copy policy, global completion evidence.
3. Cross-module contracts: accepted receipts, cursor/watermark namespaces, Context delivery/Applied, recovery bridges.
4. Conformance: shared contract suites, race/fault injection, security tests.
5. Performance/resource validation after correctness-critical contracts stabilize.

A gate advances only when the required owners accept the exact contract and evidence exists at the required level. A candidate proposal or document presence is not sufficient.

## 6. Current cross-module blockers

- Fact/Claim remains ADR-BLOCKED; dependent schemas must not freeze.
- Principal/ActorRef/ScopeRef/ProducerIdentity and PermissionEpoch binding require B/I/H/C agreement.
- D/E/Storage producer admission, Forget Fence installation, dependency registration, and final publication need one proven atomic/linearizable boundary.
- I's global Forget evidence vector must map H Adapter ACK classes and D/E/F/G local target states.
- F must prove scope-first retrieval, cache/index anti-resurrection, and typed watermark consumption.
- G/H/C/I must prove final-request Applied semantics and offline reconnect behavior.
- JF-10/COC same-XID recovery and participant integration need executable evidence.

## 7. What A must not claim

A must not:
- Call a CANDIDATE registry a contract freeze.
- Treat an Owner's local decision as cross-module agreement.
- Treat a source document or a design review as implementation evidence.
- Treat an index watermark as proof of Forget completion.
- Treat Applied as model comprehension.
- Treat a successful local cleanup as global physical erasure.
- Approve a blocked ADR through documentation wording.

## 8. Integration acceptance

An integration finding closes only when:
1. The accountable semantic Owner has made or accepted the decision.
2. Every affected consumer has reconciled the same exact version.
3. The registry records exact branch/commit/file evidence.
4. Required implementation, fault, security, or performance evidence is attached.
5. Both language versions are semantically aligned under GOV-DOC-001.

See the [A owner branch](https://github.com/oahcom/AiMemoryBrainArchitecture/tree/session-a-integration-2026-11-16/reviews/integration) for the live coordination artifacts.
