# Phase 3.8.4 — G Exact Review of C Provider Submit Outcome Contract
# Phase 3.8.4 — G 对 C Provider Submit Outcome 合同的精确审查

- Reviewer: G — Memory Context / Applied State
- Branch: `session-g-memory-context`
- Exact C source reviewed: `07-agent-integration/phase-3.8.4-c-normative-provider-submit-outcome-contract.md`
- C source Blob: `819705037da89834e10b6dd2ec6e66c1b8c70886`
- G Applied source: `06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md`
- G Applied Blob: `aa3afa73d8a76cc6f025839c52bfbff6a983046a`
- H schema: `bmcp.coc-jf10-unified/1.2.8`, Blob `70b892797d07489936300a26c0dedfafe1d6e746`
- Decision: **ACCEPT WITH ENUMERATED AMENDMENTS — G APPLIED CONSUMER SEMANTICS**
- English and Chinese are normative peers.

## 1. G decision / G 决议

G accepts C's five-value outcome algebra and confirms that G Full Applied may consume only a C-authored `HANDOFF_ACCEPTED` record that binds the exact final immutable request, ContextVersion, Delivery attempt, managed-region digest, authenticated Adapter/session, and required owner evidence.

G rejects any inference that transport ACK, provider-call intent, I COMMIT_WON, D clearance, COC membership, Storage visibility or a local C status alone proves Full Applied. The exact C outcome is necessary but not sufficient: G still evaluates the complete Applied predicate.

G 接受 C 的五值 Outcome 代数，并确认 G 的 Full Applied 只能消费 C 撰写的 `HANDOFF_ACCEPTED` 记录；该记录必须绑定精确最终不可变 Request、ContextVersion、Delivery Attempt、Managed Region Digest、认证 Adapter/Session 及所需 Owner Evidence。

G 拒绝从 Transport ACK、Provider Call Intent、I COMMIT_WON、D Clearance、COC Membership、Storage Visibility 或 C 本地状态单独推断 Full Applied。精确 C Outcome 是必要条件，但不是充分条件；完整 Applied Predicate 仍由 G 独立判断。

## 2. Outcome-to-Applied mapping / Outcome 到 Applied 的映射

| C outcome | G Full Applied | G current-use treatment |
|---|---|---|
| HANDOFF_ACCEPTED | Eligible for evaluation only; not automatic acceptance | Revalidate current I/D/Scope/Context/session/capability |
| HANDOFF_REJECTED | Forbidden | No Full Applied; retain rejection evidence |
| NOT_INVOKED | Forbidden | No Full Applied; new delivery/attempt requires fresh gate checks |
| UNKNOWN | Forbidden | Suppress protected region; reconcile same attempt |
| IN_DOUBT | Forbidden | Suppress protected region; keep relevant barriers held; no new provider attempt |

HANDOFF_ACCEPTED does not prove execution started, completion, model attention, memory use, response correctness or user delivery. Those remain separate evidence families.

HANDOFF_ACCEPTED 不证明执行开始、完成、模型注意、记忆使用、响应正确或用户交付；这些均为独立证据族。

## 3. Binding conditions / 约束条件

1. C's `request_digest` must equal the exact digest bound by G's FinalRequestSubmitted evidence and the complete Managed Region digest; a digest for only the region is not a substitute for the full request digest.
2. C's `final_request_boundary_id`, actual `InferenceRequestId`, ContextId/ContextVersion, DeliveryId/attempt, Adapter/session, Scope/Environment and CapabilityEpoch must join exactly to G's target and H's authenticated delivery/materialization evidence.
3. C outcome identity is immutable. Same identity/digest is idempotent; changed digest is conflict. Late provider receipt or same-key lookup may enrich history but cannot rewrite G's prior Applied predicate or silently promote a different request.
4. G retains historical Applied only if the full predicate was valid at the submission order point. Current-use eligibility is separately recomputed after later Forget/revocation/supersession.
5. UNKNOWN/IN_DOUBT and any unresolved COC/owner-order evidence keep the region suppressed. G must not infer “no revocation/fence” from missing coordinator records.
6. C's signature profile must be C-owned and independently trusted; G does not inherit I's signature algorithm or key authority. H validates structure/integrity; I resolves issuer/key trust as specified by governance.

## 4. Required L3 reference cases / L3 参考验证

G requires:
- HANDOFF_ACCEPTED + exact complete predicate → Full Applied may be committed;
- HANDOFF_ACCEPTED with request/region/Context/Delivery mismatch → reject;
- HANDOFF_REJECTED / NOT_INVOKED → never Full Applied;
- UNKNOWN / IN_DOUBT → no promotion and protected content suppressed;
- later revocation/fence after valid Applied → preserve historical Applied, invalidate current-use;
- revocation/fence before submit → no Full Applied;
- late provider receipt after UNKNOWN → append-only enrichment; no retroactive use without full re-evaluation;
- same C outcome identity with changed digest → conflict/quarantine;
- COC quorum proof valid but C outcome invalid, and converse → no Full Applied.

## 5. Final G disposition / G 最终结论

**ACCEPT WITH ENUMERATED AMENDMENTS — G APPLIED CONSUMER SEMANTICS.**

G accepts C Blob `819705037da89834e10b6dd2ec6e66c1b8c70886` as the exact C-owned semantic source for this review. This decision composes with G Applied Blob `aa3afa73d8a76cc6f025839c52bfbff6a983046a` and H schema 1.2.8 only. It does not claim G implementation, persistence, runtime conformance, C provider implementation or shared Applied wire freeze.

**有条件接受 — G Applied 消费语义。** 本决定仅绑定精确 C Blob、G Applied Blob 与 H Schema 1.2.8，不声明 G 实现、持久化、运行时符合性、C Provider 实现或共享 Applied Wire 冻结。
