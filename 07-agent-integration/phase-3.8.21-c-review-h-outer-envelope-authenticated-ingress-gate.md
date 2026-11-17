# Phase 3.8.21 — C Review: H Outer-Envelope Authenticated Ingress Gate
# Phase 3.8.21 — C 复审：H 外层 Envelope 认证 Ingress Gate

- Owner perspective: C — Provider Outcome Semantic Authority
- H Unified 1.2.14 schema Blob: `09fcd1fa29fe24255fbd87cae79dafb406594a59`
- CSubmitOutcome 1.0.1 schema Blob: `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda`
- C profile candidate: `AIMBA-C-CRYPTO-1.0` (not registered/frozen by this review)
- H envelope auth validator Blob: `5c5079765f468eaf40690c0c7cbd6b03275a1ff8`
- H Provider Outcome validator Blob: `b8cd692d261df7a31a0f65c3e003693e305f73a2`
- H envelope-auth test Blob: `ddf34e9c30edfc378a9482a30837ce04c4abcf97`
- H Provider Outcome test Blob: `da1454ed985c84160c4cb6a0462df9d1225fab7f`
- H exact closure Blob: `860c896a388597a4378eda5aa323f276390acf34`
- H CI run `44073888935`, commit `0e212731073b36e4fa9ffda8467e60806da1b380`, job `134006790527`: **60 tests / SUCCESS**
- Decision: **ACCEPT AUTHENTICATION-BOUNDARY SEPARATION AS REFERENCE INTERFACE; OUTER SIGNER/P0/PROFILE NOT APPROVED**
- Provenance: delegated C-role review; **not an independent human C Owner signature**.

## 1. C authority boundary / C 权威边界

C confirms these are separate signed/authority objects:
1. immutable CSubmitOutcome 1.0.1 object P0/digest/signature;
2. outer BMCP envelope digest/signature/integrity proof;
3. H transport/session/channel binding;
4. I trust/key-status/issuer/Principal verification;
5. I terminal, D clearance, Storage resolution and COC commit proofs.

C object signature authenticates only the exact C object under its C-owned profile. It does not authenticate the outer H envelope or the transport principal. Conversely, an outer H envelope signature cannot establish provider outcome truth or replace the C object signature.

C 确认以下对象彼此独立：不可变 CSubmitOutcome Object P0/Digest/Signature；外层 BMCP Envelope Digest/Signature/Integrity Proof；H Transport/Session/Channel Binding；I Trust/Key Status/Issuer/Principal Verification；以及 I Terminal、D Clearance、Storage Resolution、COC Commit Proof。

C Object Signature 仅认证 C 自有 Profile 下的精确 C Object，不能认证外层 H Envelope 或 Transport Principal。反之，外层 H Envelope Signature 也不能证明 Provider Outcome Truth 或替代 C Object Signature。

## 2. Signer-role decision / Signer 角色决议

C does **not** approve automatic reuse of `AIMBA-C-CRYPTO-1.0` for the outer envelope. That profile's current P0/signature projection is scoped to CSubmitOutcome 1.0.1. Reusing it for a different envelope P0/message domain without a separately reviewed domain-separated profile is rejected.

C **不批准**将 `AIMBA-C-CRYPTO-1.0` 自动复用于外层 Envelope。该 Profile 当前 P0/Signature Projection 的范围是 CSubmitOutcome 1.0.1。未经单独审查的 Domain-Separated Profile，不得把它复用于不同 Envelope P0/Message Domain。

C also does not decide that H gateway or C adapter is the approved outer signer. The signer may be the C adapter origin, H gateway attestor or a separate authority only after:
- the signer role and issuer relationship are explicitly named;
- C approves any claim that the signer represents a C-owned Provider Outcome;
- I approves trust/key registration and revocation policy;
- H publishes an exact P0 field allowlist and signing preimage;
- replay and transport binding are bound to the exact signer/session/audience.

C 同样不决定 H Gateway 或 C Adapter 哪一个已获准成为外层 Signer。只有在明确命名 Signer Role/Issuer 关系、C 批准其对 C-owned Provider Outcome 的代表性声明、I 批准 Trust/Key 注册与撤销策略、H 发布精确 P0 Allowlist/Signing Preimage，并将 Replay/Transport Binding 绑定到精确 Signer/Session/Audience 后，才可决定。

## 3. Review of H reference gate / H Reference Gate 复审

C accepts the separation implemented by H:
- protected transport context is supplied out-of-band;
- sender issuer/authority/subject/audience/channel claims are compared to protected context;
- integrity, key status, channel binding and identity registry are separate verifier callbacks;
- owner_authority and subject_ref are resolved through registry policy rather than equated to sender authority strings;
- replay reservation occurs only after all preceding authentication checks pass;
- same-digest replay returns the prior durable result without re-running domain validation;
- conflict is INVALID and unavailable replay authority is UNKNOWN;
- the authenticated wrapper is the only intended ingress path; direct local Provider Outcome validators are not authenticated acceptance APIs.

C 接受 H 已实现的边界分离：Protected Transport Context 从 Payload 外提供；Sender Issuer/Authority/Subject/Audience/Channel Claim 与 Protected Context 比对；Integrity、Key Status、Channel Binding、Identity Registry 是独立 Callback；owner_authority 与 subject_ref 由 Registry Policy 解析，不强行等同 Sender Authority 字符串；只有所有前置认证成功后才预留 Replay；Same-Digest Replay 返回既有 Durable Result 而不重跑 Domain Validator；Conflict=INVALID、Replay Authority 不可用=UNKNOWN；Authenticated Wrapper 才是预期 Ingress 入口，旧本地 Validator 不是认证 Acceptance API。

Test 17 is an interface capability demonstration only. It does not authorize an H gateway signer or any particular signer arrangement. All authentication callbacks remain test doubles.

Test 17 仅证明接口可表达某种授权关系，不授权 H Gateway Signer 或任何具体 Signer 方案。所有 Authentication Callback 仍为 Test Double。

## 4. C disposition / C 侧决议

**Delegated C-role decision: ACCEPT the H reference authentication/identity/replay boundary as a candidate interface only. C object P0/signature remains separate. Outer-envelope signer role, P0 allowlist, signature profile and production key lifecycle remain OPEN. NOT FROZEN.**

**角色模拟 C 侧决议：仅接受 H Reference Authentication/Identity/Replay Boundary 作为候选接口。C Object P0/Signature 保持独立。Outer Envelope Signer Role、P0 Allowlist、Signature Profile 与生产 Key Lifecycle 仍 OPEN，不冻结。**
