# I-PRE-002 — Identity Binding Audit
# I-PRE-002 — 身份绑定审计

- Work Item: AID-2026-001
- Audit role: author-side engineering trace / NOT an independent Owner I review
- Audited PR Head: `4f8c5218c8d33f5fdb690a7c4bdb671639ebb807`
- Source comparison branch: `session-i-security-governance-2026-11-16`
- Disposition: **PARTIALLY SPECIFIED / JOINT CONTRACT OPEN / IMPLEMENTATION NOT EVIDENCED**

## 1. Executive result / 结论

The PR branch's DOC-SEC-001 defines the identity vocabulary and explicitly says that exact typed-reference semantics and wire fields require B/I/H joint approval. It does not itself close the field-level trust chain. A separate Owner-I candidate contract and Phase 3.6 trust-chain package on `session-i-security-governance-2026-11-16` provide substantially more detail, but those artifacts are not part of PR #42's 34-file change set and retain candidate/governance-blocked status. The BMCP guide on the PR branch also says authenticated Principal/ActorRef/ScopeRef binding remains dependent on B/I/H decisions.

PR 分支中的 DOC-SEC-001 定义了身份术语，并明确指出准确的类型引用语义和 Wire 字段仍需 B/I/H 联合批准，因此它本身尚未闭合逐字段信任链。另一个 Owner I 候选分支 `session-i-security-governance-2026-11-16` 中存在更完整的候选契约和 Phase 3.6 信任链材料，但这些文件不属于 PR #42 当前 34 个变更文件，且仍处于 Candidate / Governance-blocked 状态。PR 分支 BMCP 指南也明确指出认证 Principal/ActorRef/ScopeRef 绑定仍依赖 B/I/H 决议。

This is an artifact-level specification audit only. It does not establish that production authentication, cryptographic verification, issuer/key registries, authorization service, revocation propagation, or end-to-end enforcement exist.

这只是文档证据层面的规范审计，不证明生产认证、密码学验证、Issuer/Key Registry、授权服务、撤销传播或端到端执行机制已经存在。

## 2. Field-by-field authority and binding trace / 逐字段权威与绑定追踪

| Field / 字段 | Definition and authority / 定义与权威 | Required binding / 必需绑定 | Validation / 验证方 | Current evidence and gap / 当前证据与缺口 |
|---|---|---|---|---|
| Authenticated Transport Context | H owns BMCP transport binding; platform ingress owns non-BMCP ingress. | Protected channel/session, peer/workload proof, channel binding, nonce/replay context, audience and time. | Trusted transport verifier; I validates resulting security assertions. | I Phase 3.6 trust-chain table defines this stage. PR BMCP guide requires authenticated transport binding but does not specify its wire/verification contract. Production verifier NOT EVIDENCED. |
| Issuer / IssuerRef | I owns trusted issuer registry and trust policy. | Issuer, key ID, credential type, tenant/security domain, audience, subject namespace, nbf/exp, revocation and key status. | Cryptographic verifier plus I-governed trust registry. | Candidate contract and Phase 3.6 material define checks. Production trust root, key custody, registry and lifecycle NOT APPROVED/NOT EVIDENCED. |
| Principal / PrincipalRef | I owns security-subject policy and registry; identity provider/credential issuer authenticates. | Stable opaque subject namespaced by issuer and tenant/security domain; registered kind/status; no payload auto-registration. | I Principal Registry after issuer validation. | Detailed candidate contract defines this. PR guide only gives a short concept definition; production registry NOT EVIDENCED. |
| ProducerIdentity | I owns registration/trust semantics; H owns transport extraction/binding; C owns telemetry producer semantics. | Authenticated Principal + Issuer + registered producer/application/workload instance + credential/key validity + source kind/event-family allowlist + tenant/security domain + revocation/credential epoch. | H binds transport; I validates registry/policy; E compares payload producer claim and reauthorizes ingress. | Detailed candidate contract specifies mismatch rejection. PR guide summarizes fields but lacks executable binding evidence. |
| ActorRef | B owns typed-reference/domain semantics; H binds authenticated transport Principal; I validates security assertions. | PrincipalRef, IssuerRef, authentication-context reference, optional ProducerIdentity/delegation-chain/acting-for refs, authenticated time and authn strength; bound to exact operation/correlation. | H supplies verifier-authenticated binding; I validates; operation owners reject caller-constructed/payload-only ActorRef. | Candidate logical shape exists on I branch. B/H joint typed-reference and wire approval remains OPEN; no production proof. |
| Delegation | I owns grant/trust/revocation policy. | Signed grant ID/issuer, grantor/delegate, actions/resources, ownership/applicability scopes, audience, purpose, validity, parent chain, epoch/revocation handle and obligations. | I validates every link, bounded depth, no cycles/amplification, current grantor authority and revocation. | Detailed candidate rules exist. Production signing, registry, revocation and conformance NOT EVIDENCED. |
| ScopeRef / ScopeBinding | B owns typed ScopeRef semantics; I owns security use and authorization policy. | Authoritatively resolved typed bindings for required tenant/user/project/Agent/instance/task/session/environment dimensions, with provenance, status, validity and registry version. | B/domain resolver plus I policy; H transports authenticated claims; caller text is never authoritative. | B scope model defines typed dimensions; I scope policy defines registry binding. B/I/H joint approval remains OPEN; scope algebra/inheritance has OPEN decisions. |
| Permission / PolicyDecision | I owns policy and decision semantics. | Exact subject/actor/action/resource/ownership+applicability scopes/purpose/audience/delegation/policy version/PermissionEpoch/obligations/expiry/correlation. | I authorization authority; each boundary rechecks before protected operation and at final commit/disclosure linearization point. | Candidate contract defines request/response and fail-closed order. Production policy service and enforcement NOT EVIDENCED. |
| PermissionEpoch | I is sole logical authority. | Monotonic generation in a declared policy-domain namespace; bound to decision/lease and consumer high-water/currentness proof. | I authority and each consumer's currentness verifier. | Candidate semantics and revocation rules exist. Exact partitioning/consistency profile and production sequencer/service remain open/not verified. |
| Payload claims | No payload field is an authority. | actor_ref, producer_id, adapter_id, tenant/project/environment/issuer strings must be compared with authenticated context and registries. | Receiving boundary; mismatch rejects and audits. | Stated in I candidate scope policy and Phase 3.6 trust package; PR docs state the same general invariant. Executable conformance NOT RUN. |

## 3. End-to-end order / 端到端顺序

Candidate trust order:

`Authenticated Transport → Issuer Trust Validation → Principal Resolution → Producer/Adapter Binding → Delegation Validation → ActorRef Resolution → Scope Resolution → Authorization Decision → PermissionEpoch Currentness → Protected Operation`

Each stage must consume verifier/authority-owned evidence from the preceding stage. A later stage must not reconstruct trust from payload claims or skip an UNKNOWN/failed stage. Protected operations fail closed when identity, issuer, delegation, required Scope, policy, revocation or current PermissionEpoch cannot be established.

候选信任顺序：

`Authenticated Transport → Issuer Trust Validation → Principal Resolution → Producer/Adapter Binding → Delegation Validation → ActorRef Resolution → Scope Resolution → Authorization Decision → PermissionEpoch Currentness → Protected Operation`

每一阶段必须消费前序阶段由验证方/权威方产生的证据。后续阶段不得从 Payload Claim 重建信任，也不得跳过 UNKNOWN/失败阶段。身份、Issuer、Delegation、必需 Scope、Policy、Revocation 或当前 PermissionEpoch 无法确认时，受保护操作必须 Fail Closed。

## 4. Exact gaps / 明确缺口

1. **Joint ownership closure is absent from PR #42:** B typed-reference semantics, H transport/wire mapping, and I trust/policy must approve one exact joined contract. The PR guide records this dependency but no approval artifact is included in this PR.
2. **Wire-level binding is not frozen:** the logical ActorRef and authorization tuples are candidate semantics, not an approved BMCP schema.
3. **Production trust infrastructure is not evidenced:** no approved production trust root/profile, issuer/key registry, key custody, live transport/channel-binding verifier, durable replay authority or revocation sequencer is established by these documents.
4. **Enforcement and tests are not evidenced in this PR:** no executable end-to-end test proves payload spoofing rejection, producer/ActorRef mismatch rejection, delegation expiry/revocation, cross-tenant Scope denial, stale PermissionEpoch rejection, or final-boundary reauthorization.
5. **Scope model remains partly open:** parent/child and multi-owner scope algebra, policy language, cached decision semantics and revocation SLA are explicitly OPEN in B's scope model.
6. **Source-branch status must not be conflated with PR status:** the detailed I branch documents are candidate technical evidence, not merged PR #42 artifacts or formal production certification.

## 5. Required closure sequence / 建议闭合顺序

- B: approve exact PrincipalRef/ActorRef/ScopeRef typed-reference semantics and stable identity rules.
- H: publish exact BMCP wire fields and verifier-produced transport-context binding, including audience, channel/session binding, nonce/replay and authenticated provenance.
- I: approve issuer/key trust, Principal/Producer registry semantics, delegation, authorization tuple, PermissionEpoch namespace/currentness and revocation policy.
- B/H/I: record one versioned, exact joined contract and explicit approvals; do not infer approval from parallel candidate documents.
- C/E and every protected operation owner: bind their producer/operation claims to the authenticated context and current I decision at the required linearization points.
- Execute reproducible R3 tests with real implementation or clearly bounded test doubles; distinguish interface tests from production trust evidence.

## 6. Evidence references / 证据来源

PR #42 branch at audited Head:
- `docs/en/09-security-governance/security-governance-guide.md` §§3–4, 9–10.
- `docs/zh-CN/09-security-governance/security-governance-guide.md` §§3–4, 9–10.
- `docs/en/08-bmcp-protocol/bmcp-guide.md` §§2, 6, 10.
- `docs/zh-CN/08-bmcp-protocol/bmcp-guide.md` §§2, 6, 10.
- `02-domain-model/scope-and-permission-model.md` §§2–6, 8–14.
- `07-agent-integration/adapter-capability-tiers.md` §§4, 8, 11.

Owner I candidate branch `session-i-security-governance-2026-11-16`:
- `09-security-governance/principal-actor-and-authorization-contract.md`, Blob `03765efac4bb1153f303ce0030f9e277d602e81d`.
- `09-security-governance/phase-3.6-identity-trust-policy-joint-closure.md` (not restored on main; see AID-2026-107 §10), Blob `0cbf6bb7480db873790c454817593a9b1c5548ba`.
- `09-security-governance/phase-3.6-principal-trust-chain-authorization-revocation.md` (not restored on main; see AID-2026-107 §10) (candidate technical package).
- `09-security-governance/phase-3.8.18-i-exact-review-h-authenticated-ingress-envelope-trust-boundary.md` (not restored on main; see AID-2026-107 §10), Blob `73145f83df234ebb9e55cc07f0a82b0db9416b68`.

## 7. Status / 状态

- I-PRE-002: **DOCUMENTED AS AN OPEN JOINT-CONTRACT / IMPLEMENTATION GAP**.
- No normative B/H/I contract was silently changed or approved by this audit.
- No Owner I independent R3 review is claimed.
- No production security implementation or test PASS is claimed.
- YAML/schema/Manifest validation and CI: NOT RUN.
- Acceptance remains BLOCKED; PR #42 remains subject to fresh independent review and explicit acceptance; merge NOT AUTHORIZED.
