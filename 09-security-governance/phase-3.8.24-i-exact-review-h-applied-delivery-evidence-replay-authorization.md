# Phase 3.8.24 — I Exact Review: H Applied Delivery Evidence Replay Authorization
# Phase 3.8.24 — I 精确审查：H Applied Delivery Evidence Replay Authorization

- Owner domain: I — Security, Identity and Governance.
- Mode: delegated I-role exact review; **not an independent human I Owner signature**.
- I branch reviewed: \`session-i-security-governance-2026-11-16@ea949896f891f0a08ef5fe9358edadc8a49e546f\`.
- Normative I current authorization source: Phase 3.7 Blob \`e3b1b5d99eb36ac0b395854d8c19287d2b64b752\`.
- I replay acceptance source: Phase 3.8.23 Blob \`85cdbad04ae4b688338cdf2b667c21d2f02d8b96\`.
- H branch reviewed: \`session-h-bmcp-protocol@b14e388e9e8ecc19f9c51fed67818e9cc69ef4d9\`.
- H validator Blob: \`8febb915ec321cc37cf159b2f5b917a3f945726c\`.
- H test Blob: \`77cb66b895c5293a2f4883b1d5cb69775e71d00c\`.
- H hardening addendum Blob: \`4c220e998fc6ba700157598b0384dc3134cf8575\`.
- H Applied Delivery Evidence CI: run \`44181762581\`, **SUCCESS, 29/29 tests**.
- Disposition: **ACCEPT SEPARATE I REPLAY-AUTHORIZATION CALLBACK AS REFERENCE BOUNDARY WITH CONDITIONS; PRODUCTION I AUTHORITY NOT VERIFIED**.

## 1. I decision scope

I reviews only the current I authorization/PermissionEpoch and issuer/key-status portion of H's SAME_DIGEST_REPLAY disclosure gate. D ForgetFence is an independent conjunctive check and is reviewed by D, not I.

I Phase 3.7 requires current authorization at each protected boundary: authenticated issuer and principal/workload/actor, delegation, action/resource/purpose/audience/Scope/Environment, PolicyDomainRef, I-issued PermissionEpoch, current policy/revocation/registry state and exact request/work-item/artifact/region binding. Cached ALLOW or historical receipt is not perpetual authority. UNKNOWN/stale/revoked/unverifiable state means DENY/PAUSE and quarantine.

I Phase 3.8.23 further requires rechecking current I authorization/PermissionEpoch, key status, audience/scope and applicable D Forget fence before returning SAME_DIGEST_REPLAY; prior result references must not be disclosed to stale or revoked callers.

## 2. Exact H callback boundary

H now exposes a distinct tri-state callback:

\`verify_current_i_replay_authorization(envelope, original_result_ref)\`

H runs this callback before returning \`original_result_ref\` from SAME_DIGEST_REPLAY. False => INVALID and no result reference; None/exception => UNKNOWN and no result reference. The D check is separate and cannot be substituted by I.

**I accepts this as the correct reference-code boundary**, provided the production I adapter verifies:
- authenticated caller principal/workload/actor and delegation chain;
- issuer/key ID/version/status at replay time, including revocation/compromise state;
- action, resource, purpose, audience, Scope and Environment;
- exact PolicyDomainRef and current I PermissionEpoch/current policy/revocation/registry state;
- exact request, work item, artifact/region and original-result binding;
- any I-local sequencer/ledger continuity required by the applicable replay profile.

PermissionEpoch is opaque and local to its PolicyDomain. It MUST NOT be numerically compared with D, COC, Storage, F or G positions. A previous successful signature check or original acceptance is not enough to disclose a result to a caller whose current authorization has changed.

## 3. Fail-closed requirements

- I callback True: may proceed to the separate D callback; this is not by itself permission to disclose.
- I callback False: INVALID; no original result reference.
- I callback unavailable/exception/None: UNKNOWN; no original result reference.
- D callback must independently pass before disclosure.
- Neither I nor D may infer the other's state.
- Replay authorization must be re-evaluated at the time of replay disclosure, not merely at original message acceptance.

## 4. Remaining production gates

This review does not register the H profile, issuer, trust root or key; does not implement the I PolicyDomain sequencer/authorization service; and does not prove production key custody, revocation propagation, durable replay storage, or external anti-rollback. The H callback remains an injected adapter seam. H's test callback is a deterministic test double, not a live I service.

**Final disposition:** I replay callback boundary **ACCEPTED AS REFERENCE CANDIDATE WITH CONDITIONS**; production I authorization adapter and trust registry **OPEN / NOT VERIFIED**; H profile registration and durable replay **OPEN**; no I trust Gate or production activation is passed.

---

## 5. 中文完整结论

I 本次只审查 H SAME_DIGEST_REPLAY 披露门中的 I 当前授权/PermissionEpoch/Issuer-Key Status 部分。D ForgetFence 是独立的合取条件，归 D 审查，不归 I 代替。

I Phase 3.7 要求每个受保护边界重新验证当前授权：认证 Issuer/Principal/Workload/Actor、Delegation、Action/Resource/Purpose/Audience/Scope/Environment、PolicyDomainRef、I 签发的 PermissionEpoch、当前 Policy/Revocation/Registry，以及精确 Request/WorkItem/Artifact/Region 绑定。缓存 ALLOW 或历史 Receipt 不是永久授权。UNKNOWN/陈旧/撤销/不可验证必须 DENY/PAUSE 并隔离。

H 现在提供独立的 \`verify_current_i_replay_authorization(envelope, original_result_ref)\` Tri-state Callback，并在返回 SAME_DIGEST_REPLAY 的 \`original_result_ref\` 前执行。False 为 INVALID 且不返回引用；None/异常为 UNKNOWN 且不返回引用。D 检查独立执行，不能由 I 代替。

I 将该 Callback 接口作为正确的参考边界有条件接受。生产 I Adapter 必须在重放时重新验证认证主体/Delegation、Issuer Key 当前状态、Action/Resource/Purpose/Audience/Scope/Environment、PolicyDomainRef/PermissionEpoch/当前 Policy/Revocation/Registry，以及精确 Request/WorkItem/Artifact/Region/Result 绑定。

PermissionEpoch 是 PolicyDomain 内不透明值，禁止与 D/COC/Storage/F/G 位置进行数值比较。原始签名验证成功或历史接受成功，不足以授权当前调用方读取 Result Ref。

本审查不注册 H Profile/Issuer/Trust Root/Key，不实现 I PolicyDomain Sequencer/Authorization Service，也不证明生产 Key Custody、Revocation Propagation、Durable Replay 或 Anti-rollback。H Callback 仍是注入适配器接缝，测试 Double 不是真实 I 服务。

最终状态：I Replay Callback **参考候选有条件接受**；生产 I Authorization Adapter/Trust Registry **OPEN / NOT VERIFIED**；H Profile Registration 和 Durable Replay **OPEN**；不代表 I Trust Gate 或生产激活通过。

## 6. Current H code-head delta — 2026-11-18

The original 29-test snapshot above is historical. H's current Owner branch is `session-h-bmcp-protocol@4386f67a61f7968da4c3603f28cc8a5100714f9f`. The final H successor commit adds a Unified 1.2.15 structural-conformance document; the replay code and tests are unchanged at the Blob level.

Current exact H pins:
- Applied Delivery Evidence schema Blob: `2ce8776ca5ee5e014b234dc3eb34a7cb7961e608`.
- Validator Blob: `43f402e4a09034da197ac24856cddbd496c9c75f`.
- Conformance test Blob: `98242cc193a77b27d58b39353ccc031201992614`.
- Hardening addendum Blob: `4c220e998fc6ba700157598b0384dc3134cf8575`.

The exact 30-test code Head reviewed in the later H/C pass is `4c16410f8b20b8fc2bc8c7609eb7bf07d83f317e`; run [#44187702465](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44187702465) is SUCCESS, 30/30. Its validator/test Blobs match the current H Owner branch pins above. This is code-blob equivalence, not a claim that CI ran on the later documentation-only branch HEAD `4386f67...`.

The 30-test suite retains the I replay callback boundary:
- `verify_current_i_replay_authorization(envelope, original_result_ref)` is independently evaluated for SAME_DIGEST_REPLAY before the original result reference is returned.
- False => INVALID and no result reference; None/exception => UNKNOWN and no result reference.
- Current key-status verification remains a separate earlier check; I replay authorization must additionally revalidate principal/workload/delegation, action/resource/purpose/audience/scope/environment, PolicyDomainRef, current PermissionEpoch, revocation/registry state and exact request/result binding.
- D's current ForgetFence callback remains a separate conjunctive authority and is not accepted by I's result.

**Updated disposition:** the I callback shape remains ACCEPTED AS REFERENCE CANDIDATE WITH CONDITIONS on the current code Blob. The callback is still injected; there is no live I authorization/PermissionEpoch/key-status adapter, production trust registration, revocation propagation, or durable replay implementation. This delegated I-role review is not an independent human I Owner signature and does not pass I36 governance or production activation.

### 中文：当前 H 代码 Head 差异

上方 29 项测试快照已是历史记录。H 当前 Owner 分支为 `session-h-bmcp-protocol@4386f67a61f7968da4c3603f28cc8a5100714f9f`。最后的 H 后继提交只增加 Unified 1.2.15 结构符合性文档，Replay 代码和测试 Blob 未改变。

当前 H 精确来源：Schema `2ce8776...`、Validator `43f402e...`、Tests `98242cc...`、Hardening Addendum `4c220e9...`。后续 30 项精确代码 Head `4c16410...` 的 Run #44187702465 SUCCESS，30/30；其 Validator/Tests Blob 与当前 H Owner 分支一致。这是代码 Blob 等价，不表示 CI 运行在仅增加文档的后续分支 Head 上。

当前 30 项测试仍保留独立的 I Replay Callback：SAME_DIGEST_REPLAY 时，在返回 Original Result Ref 前执行 `verify_current_i_replay_authorization`；False 为 INVALID 且不返回引用，None/异常为 UNKNOWN 且不返回引用。Key Status 仍是独立的前置检查；I Replay Authorization 还必须在重放时重新验证主体/Delegation、Action/Resource/Purpose/Audience/Scope/Environment、PolicyDomainRef、当前 PermissionEpoch、Revocation/Registry 和精确 Request/Result 绑定。D ForgetFence 是另一个独立合取权威，不归 I 代替。

更新结论：I Callback 结构在当前代码 Blob 上仍**有条件接受为参考候选**；它仍是注入接缝，没有真实 I Authorization/PermissionEpoch/Key Status Adapter、生产 Trust Registration、Revocation Propagation 或 Durable Replay。此委派 I 角色审查不是独立人类 I Owner 签名，也不代表 I36 Governance 或生产激活通过。
