# Canonical Identity Semantics
# 规范身份语义

- ID: B-ID-001
- Status: CANDIDATE DOMAIN SEMANTICS; cross-owner binding OPEN
- Baseline: main `b372b62c640a2b656e54b6db62a4ee67d7d8c001`
- Related B technical baseline: `session-b-domain-model-phase3:02-domain-model/phase-3.6-typed-identity-trust-closure.md`, Blob `0a6b78a842e550b58533b797cdfcd2d954ed6826`
- Current B formal type confirmation: `02-domain-model/phase-3.6-b-owner-formal-actor-scope-environment-type-mapping-confirmation.md`, Blob `3a1e77889cd9a90cd5822d9f0cb3437880868706` (supersedes earlier readback Blob 729a706860b1259115816265e847a29683c3c233)
- B exact CGH-APPLIED-1.1 recovery-batch type confirmation: included in current B formal artifact Blob `3a1e77889cd9a90cd5822d9f0cb3437880868706`; exact A package Blob `4961ffefc0f9920efb8425a9b2a7af42d8f64819`; companion COC Blob `fc3bac39ec64fda68b8cba5e1aada4e719e5acea`
- Related I artifact: `session-i-security-governance-2026-11-16:09-security-governance/phase-3.6-identity-trust-policy-joint-closure.md`, Blob `0cbf6bb7480db873790c454817593a9b1c5548ba`
- Related H artifact: `session-h-bmcp-protocol:08-bmcp-protocol/phase-3.6-authenticated-identity-protected-operation-binding.md`, current readback Blob `e7ca5ce4ece5d8fd77fe0760e49a85afa0133248`

## 1. Purpose and authority / 目的与权威边界

Identity semantics must distinguish a domain object's identity, a typed reference, a security Principal, a caller's identity claim, authenticated transport context, and authorization. A serialized identifier is never proof of the presenter, registration, or permission.

身份语义必须区分领域对象身份、类型化引用、安全 Principal、调用方身份声明、认证传输上下文和授权。序列化标识符永远不能证明呈现者身份、注册状态或权限。

B owns domain reference types and identity invariants. I owns issuer trust, Principal registration/resolution, delegation, authorization, revocation and PermissionEpoch. H owns authenticated transport and wire binding. C/D/E/G own operation-specific producer/consumer boundaries. These are non-substitutable authorities.

B 负责领域引用类型和身份不变量。I 负责 Issuer 信任、Principal 注册/解析、委托、授权、撤销和 PermissionEpoch。H 负责认证传输和 Wire 绑定。C/D/E/G 负责各自操作边界。上述权威不可互相替代。

## 2. Canonical distinctions / 规范区分

| Term | Canonical meaning | Must not be confused with |
|---|---|---|
| Domain Identity | Stable identity of a domain object within its declared identity namespace | Content digest, display label, external identifier |
| Typed Reference | Typed, namespaced pointer to a registered identity/object | Authentication credential, grant, permission |
| Identity Claim | Untrusted caller/payload assertion about an identity | Authenticated identity |
| Authentication Credential | Protected proof material validated by a verifier under I policy | Domain Ref or ActorRef |
| Authenticated Principal | I-resolved security subject after trust/credential/issuer/audience/revocation checks | Domain Entity or AgentRef |
| ActorRef | Immutable per-operation attribution binding to a verified Principal and acting/delegation context | PrincipalRef, bearer token, reusable user ID |
| Permission | I policy decision for a specific Principal/action/resource/purpose/scope/audience/current epoch | ScopeRef or any identifier |
| ScopeRef | Typed namespace/ownership/applicability boundary | Permission grant |
| EnvironmentRef | Stable identity of a world/save/simulation/device-fleet/external state domain | Display name, coordinates, environment revision |
| RuntimeSessionRef | Bounded runtime/session identity for correlation and binding | Conversation history, long-lived Agent identity |

## 3. Identity stability rules / 身份稳定性规则

### 3.1 Domain object identity

1. Identity is opaque and non-semantic; content edits do not change object identity.
2. A new immutable version/revision receives its own version identity while the parent aggregate identity remains stable.
3. An identity, once assigned, is never silently recycled or reused.
4. A display label, alias, normalized text, embedding, or content digest is not a canonical identity.
5. The same content may legitimately exist as multiple domain objects in different ownership, purpose, time, or source contexts.
6. Merge/split is an explicit identity-governance operation with retained lineage and reference migration; no silent ID reassignment.
7. Supersession creates an explicit predecessor/successor relation; it does not make IDs aliases.
8. Forget does not authorize identity reuse. Reappearance of equivalent content must pass D/I lifecycle, suppression, provenance and admission rules; content equality cannot resurrect a forgotten object.

### 3.2 Version identity

Memory identity remains stable across immutable Memory Versions. MemoryVersionId identifies one immutable snapshot. ContextVersion is a separate G-owned identity and is never cast to MemoryVersionId. Claim identity across Memory Versions remains OPEN until the Fact/Claim and Claim identity ADRs are resolved; current embedded ClaimSnapshot representation must not be assumed to settle it.

Memory 身份在不可变 Memory Version 之间保持稳定；MemoryVersionId 标识一个不可变快照。ContextVersion 是 G 所有的独立身份，不得转换为 MemoryVersionId。Claim 跨 Memory Version 的身份仍为 OPEN，必须等待 Fact/Claim 和 Claim identity ADR；当前嵌入式 ClaimSnapshot 表示不能被当作该问题已解决。

## 4. Typed identity namespace / 类型化身份命名空间

The existing B Phase 3.6 proposal defines the following distinct reference types. This inventory records B's typed semantic proposal, not a claim that all consumer contracts or governance approvals are complete.

现有 B Phase 3.6 提案定义以下不同引用类型。本清单记录 B 的类型语义提案，不表示所有消费者契约或治理批准均已完成。

| Type | Namespace / identity boundary | Authority |
|---|---|---|
| PrincipalRef | Issuer + tenant/security domain + Principal kind + opaque subject ID | I registry; B type semantics |
| IssuerRef | Trust domain / issuer registry + opaque issuer ID | I |
| ActorRef | Per-operation attribution namespace; immutable ID | B type; I validates; H binds |
| AgentRef | Agent registry + tenant/security domain | Agent/deployment registry; I binding |
| AdapterRef | Adapter application registry + tenant/security domain; instance separate | H registry; I Principal trust |
| ProducerRef | Issuer + tenant/security domain + producer namespace | I registration; E/D enforce |
| ScopeRef | Scope authority + tenant/security domain + scope kind + opaque Scope ID | B type; I/G registry/policy |
| EnvironmentRef | Environment authority + tenant/project + environment kind + opaque ID | Environment registry; I bridge policy |
| RuntimeSessionRef | Issuer + runtime/Agent/Adapter instance + session namespace | H/platform session authority; I trust policy |

A consumer must preserve type discriminator, issuer/authority namespace and security-domain dimensions. Weakening a typed reference into an untyped string loses essential semantics and is prohibited where it creates ambiguity.

消费者必须保留类型判别符、Issuer/Authority 命名空间和安全域维度。在会造成歧义时，将类型化引用弱化为无类型字符串会丢失必要语义，必须禁止。

## 5. Reference and trust resolution order / 引用与信任解析顺序

The following is the B/I/H semantic dependency order; it is not a wire schema or a replacement for owner-specific executable workflow:

以下是 B/I/H 的语义依赖顺序，不是 Wire Schema，也不替代 Owner 专属的可执行流程：

1. H/platform authenticates protected transport/session/workload context.
2. I validates issuer, credential/key, audience, validity and revocation; resolves PrincipalRef.
3. Resolve AgentRef, AdapterRef, ProducerRef and RuntimeSessionRef through authoritative registries and bind them to the authenticated Principal.
4. Compare payload identity claims with verifier-produced bindings; mismatch/unknown required binding fails closed.
5. Resolve ActorRef from verifier-produced operation context; validate Principal, Issuer and delegation attribution.
6. Resolve ScopeRef and EnvironmentRef against authoritative registries; validate type, namespace, status, parent and compatibility.
7. I authorizes the exact Principal + Actor + action + resource + purpose + audience + Scope/Environment + delegation tuple.
8. Revalidate current PermissionEpoch and the independent D ForgetFence at the owner-defined final commit/disclosure boundary.

## 6. Non-equivalence invariants / 不等价不变量

- PrincipalRef ≠ AgentRef ≠ AdapterRef ≠ ProducerRef.
- ActorRef ≠ PrincipalRef and is not reusable across materially different operations/session/delegation context.
- ScopeRef does not grant Permission.
- EnvironmentRef ≠ Environment ScopeRef ≠ Environment revision.
- RuntimeSessionRef ≠ Session ScopeRef ≠ Conversation.
- Ref resolution ≠ authentication; authentication ≠ authorization.
- PermissionEpoch ≠ D ForgetFenceGeneration; neither may be compared, converted or substituted.
- Domain Entity identity ≠ Security Principal identity, even when a person/Agent is represented in both domains.

## 7. Unresolved namespace questions / 未决命名空间问题

1. Canonical Tenant vs Workspace vs Project vs User Scope taxonomy and parent/child algebra: OPEN; I/A confirmation required.
2. Whether one Principal may be federated across multiple tenant/security domains and under which issuer mapping: I GOVERNANCE-BLOCKED.
3. Environment Registry Authority designation and closed-world registry completeness: NOT VERIFIED; cross-environment access remains fail closed.
4. Exact typed Ref wire names/encoding and authenticated context fields: H-owned; no B unilateral freeze.
5. Canonical Agent logical identity vs runtime instance/session relationships: C/I/H confirmation required.
6. ExternalId uniqueness and issuer-scoped collision behavior: I policy OPEN.
7. Claim identity across Memory Versions: B ADR OPEN.
8. Whether Session and Conversation are separate domain entities: C/G OPEN; do not conflate with RuntimeSessionRef or Session ScopeRef.

## 8. Conflict and decision status / 冲突与决策状态

- B Phase 3.6 typed identity proposal Blob `0a6b78...` labels itself JOINT-DECIDED technical baseline, but explicitly says no separate B-session signature is claimed and implementation tests were not run.
- I's current identity-trust closure Blob `0cbf6bb...` says technical baseline JOINT-DECIDED but external governance approvals remain GOVERNANCE-BLOCKED and implementation/conformance NOT VERIFIED.
- H current protected-operation binding Blob `e7ca5c...` says governance and consumer acceptance OPEN; implementation/conformance NOT VERIFIED.
- B formally APPROVED ActorRef/ScopeRef/EnvironmentRef semantic type mapping for the exact BIH package (A Blob `a45ae90b318a79bf009d14f4d917611881e9e214`) and exact CGH-APPLIED-1.1 recovery-batch pair above. C/F/G BIH consumer design decisions were recorded ACCEPT WITH ENUMERATED EXCEPTIONS; H ACCEPTED the BIH package. The separate CGH-APPLIED-1.1 C/D/G/H/I/B decisions are also recorded with enumerated exceptions, while Storage confirmed its architecture interface with changes.
- These are exact-version semantic/design acceptances only. They do not freeze H wire encoding, close I36-GOV-01..10, prove runtime conformance or production readiness. Applied Contract Frozen remains NO; COC/Storage physical implementation and fault tests remain open.

## 9. Decision record / 决策记录

**B-ID-DEC-001 — Preserve distinct typed references and separate reference from trust**
- Context: payload identity, authenticated principal, domain scope and authorization had been at risk of being conflated.
- Alternatives: untyped string IDs; one universal Actor/User ID; distinct typed references with verifier/registry binding.
- Candidate decision: preserve distinct typed references; no implicit casts; reference never proves authentication or permission.
- Consequences: safer cross-module validation, but requires registries, explicit mappings and schema compatibility.
- Affected owners: B, I, H, C, D, E, G.
- Reversal condition: only a documented domain case proving two concepts are semantically identical without loss of namespace, lifecycle, authority or trust semantics.
- Status: CANDIDATE FOR B CANONICAL MODEL; existing delegated technical decision retained as evidence, no new cross-owner approval inferred.

## 10. Gate status / 门禁状态

B identity semantics are sufficiently explicit for continued model reconciliation, but B2/B3 remain open. This document does not resolve Fact/Claim, Tenant/Workspace, external governance, cross-owner wire binding or runtime conformance. No schema freeze or authorization for implementation is claimed.

B 身份语义已足以继续领域模型协调，但 B2/B3 仍未通过。本文件不解决 Fact/Claim、Tenant/Workspace、外部治理、跨 Owner Wire 绑定或运行时一致性问题。不宣称 Schema 冻结或实现授权。
