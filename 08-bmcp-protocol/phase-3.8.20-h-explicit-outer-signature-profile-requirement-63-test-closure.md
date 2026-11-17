# Phase 3.8.20 — H Explicit Outer Signature-Profile Requirement and Exact 63-Test CI
# Phase 3.8.20 — H 明确 Outer Signature-Profile 要求与精确 63 项 CI

- Owner perspective: H — BMCP Protocol / Envelope / Adapter Authentication
- Status: **63/63 EXACT-HEAD TESTS PASS; SIGNATURE PROFILE ID REQUIRED; PROFILE REGISTRATION / SIGNER ROLE / OUTER P0 / PRODUCTION TRUST OPEN; NOT PRODUCTION / NOT FROZEN**
- H Unified 1.2.14 schema Blob: `09fcd1fa29fe24255fbd87cae79dafb406594a59`
- CSubmitOutcome 1.0.1 schema Blob: `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda`
- H envelope auth validator Blob: `a863acd01abcb147db2bd23a3b8bb1985d81bc78`
- H Provider Outcome validator Blob: `b8cd692d261df7a31a0f65c3e003693e305f73a2`
- H envelope-auth test Blob: `3469c5268d3558c777ea9f16058e00570517ff54`
- H Provider Outcome test Blob: `da1454ed985c84160c4cb6a0462df9d1225fab7f`
- H positive fixture Blob: `f911027c848d21dd36fb87ba64a201a1455787a7`
- C crypto interop test Blobs: `5559fb7a612c8dd92345ceae3a6aa62f4faae41a` / `a49d588ea6f840927fe21ad8c41cd8089dceac29`
- Exact H Provider Outcome CI run: `44075215559`
- Exact tested commit: `a36c34897545316942c7cda8da5d8bea7dacec5b`
- Exact job: `134011346259` (`provider-outcome`) — **completed / success**
- Test result: **63 tests, 0 failures** (36 H/C Provider Outcome + 21 outer-envelope-auth + 6 Python/Node crypto interop)
- Predecessor reference-gate closure: Phase 3.8.19, Blob `860c896a388597a4378eda5aa323f276390acf34`
- Gap analysis: Phase 3.8.18, Blob `fbb7553b0bd0c7a9714304983882ca2cc1fa9cc1`
- Provenance: delegated H-role source/test work and exact GitHub Actions readback; **not an independent human H Owner decision**.
- English and Chinese are normative peers.

## 1. Exact delta / 精确差异

The H outer-envelope gate now requires a non-empty `signature_profile_id` in its minimum authentication field set. The common schema exposes this property as optional, but its description states that semantic validation requires it for protected owner-signed records. The reference ingress gate now enforces that semantic requirement before invoking any trust callbacks.

H Outer Envelope Gate 现在在最小认证字段集中要求非空 `signature_profile_id`。Common Schema 将该属性定义为 Optional，但字段描述明确：受保护 Owner-signed Record 的 Semantic Validation 必须要求它。Reference Ingress Gate 现于调用 Trust Callback 前强制执行该语义要求。

The gate does not infer a signature profile from `canonicalization_profile_id`. The integrity callback must resolve the exact profile from authenticated issuer/key configuration; a missing profile identifier is INVALID, a proven unregistered/mismatched profile is INVALID, and unavailable profile registry state is UNKNOWN.

Gate 不从 `canonicalization_profile_id` 推断 Signature Profile。Integrity Callback 必须从认证 Issuer/Key 配置解析精确 Profile；缺少 Profile Identifier 为 INVALID；已证明未注册/不匹配为 INVALID；Profile Registry 不可用为 UNKNOWN。

## 2. Exact CI / 精确 CI

Run `44075215559` completed successfully on exact commit `a36c34897545316942c7cda8da5d8bea7dacec5b`, job `134011346259`. Raw job output records `Ran 63 tests in 27.693s` and `OK`.

The 21 outer-auth tests now include:
- missing `signature_profile_id` is INVALID even when `canonicalization_profile_id` exists;
- an unregistered/mismatched signature profile is INVALID;
- unavailable signature-profile registry is UNKNOWN;
- gateway signer versus C-owned message authority remains registry-decided, not hardcoded;
- replay reservation does not occur before successful integrity/key checks.

Run `44075215559` 在精确 Commit `a36c348...`、Job `134011346259` 上成功。Raw Log 记录 `Ran 63 tests in 27.693s` 与 `OK`。21 项 Outer-Auth 测试新增 Signature Profile 必填、未注册/不匹配 INVALID、Registry 不可用 UNKNOWN，以及 Signer/Owner Role 分离和 Replay 顺序验证。

## 3. Evidence ceiling / 证据上限

**PROVEN:** local semantic requirement for signature_profile_id; callback orchestration; tri-state missing/unregistered/unavailable handling; protected-context claim checks; replay ordering; authenticated-wrapper ordering; 63 exact-head tests passing.

**NOT PROVEN:** production signature profile registration, outer-envelope P0 allowlist/preimage, cryptographic digest/signature verification, C/I signer-role decision, production trust/key lifecycle, real channel binding, durable replay state, authenticated gateway deployment, provider truth or COC/Storage durability.

**已证明：** signature_profile_id 的本地语义要求、Callback 编排、三态 Missing/Unregistered/Unavailable 处理、Protected Context Claim 检查、Replay 顺序、Authenticated Wrapper 顺序、63 项精确 HEAD 测试通过。

**未证明：** 生产 Signature Profile 注册、Outer Envelope P0 Allowlist/Preimage、真实密码学 Digest/Signature 验证、C/I Signer Role 决策、生产 Trust/Key Lifecycle、真实 Channel Binding、Durable Replay State、认证 Gateway 部署、Provider Truth 或 COC/Storage Durability。

All authentication callbacks remain deterministic test doubles. This closure does not authorize C profile reuse, choose C adapter/H gateway/separate attestor, or approve any production key/trust root.

所有 Authentication Callback 仍为确定性 Test Double。本闭环不授权 C Profile 复用，不选择 C Adapter/H Gateway/独立 Attestor，也不批准任何生产 Key/Trust Root。

## 4. H disposition / H 侧结论

**Delegated H-role decision: ACCEPT the 63-test local reference-ingress interface evidence and explicit signature_profile_id requirement as a candidate. Outer-envelope P0, signer role, signature profile registration, production trust/key lifecycle, real transport binding and durable replay remain OPEN. NOT FROZEN.**

**角色模拟 H 侧决议：接受 63 项本地 Reference-Ingress 接口证据及明确的 signature_profile_id 要求作为候选。Outer Envelope P0、Signer Role、Signature Profile Registration、Production Trust/Key Lifecycle、真实 Transport Binding 与 Durable Replay 仍 OPEN，不冻结。**
