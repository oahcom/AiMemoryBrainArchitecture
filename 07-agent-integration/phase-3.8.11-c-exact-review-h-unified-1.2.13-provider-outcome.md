# Phase 3.8.11 — C Exact Review of H Unified Schema 1.2.13 Provider Outcome Mapping
# Phase 3.8.11 — C 对 H Unified Schema 1.2.13 Provider Outcome 映射的精确复审

- Owner perspective: C — Provider Outcome semantic authority
- Status: **ACCEPT WITH ENUMERATED AMENDMENTS as a mapping candidate; NOT WIRE-FROZEN**
- Project phase: **ARCHITECTURE DESIGN**
- H Unified schema 1.2.13: `08-bmcp-protocol/schemas/bmcp.coc-jf10-unified-1.2.13.schema.json`, Blob `88a33e26f3dbfa9b2f7286e72a5d98caae90dc67`
- H Phase 3.8.8 mapping: Blob `6b86fa62c248f2092815fe552e39eb5896f48630`
- CSubmitOutcome object schema 1.0.0: Blob `b5e87fa8df8463cf4cdc1ebc6867e643dcf5924c`
- C Phase 3.8.9 object/conformance contract: Blob `2ecdf44cae1bf71e9611dd5367c8f7bcf25dd7ac`
- C Phase 3.8.10 review of H 1.2.12: Blob `3a01f4e605d0d6def574cffd8fedd77eae5d24bd`
- C signature projection: Blob `06d9264124d85896ccd44ef7789d9af245d8255b`
- I C-crypto candidate addendum: Blob `1bcddbaaa4a9ca730d492a6554941becac305668`
- Provenance: delegated C-role review; **not an independent human C Owner signature**.

## 1. Exact review decision / 精确复审决议

C reviewed the exact H 1.2.13 schema and H Phase 3.8.8 mapping. The two blocking issues identified against H 1.2.12 are corrected at the structural-candidate level:

1. HANDOFF_REJECTED no longer unconditionally requires a no-handoff proof; it requires provider request and outcome evidence.
2. The ambiguous duplicate `participant_intent_ref` is removed; `coc_participant_intent_ref` is the single nullable COC intent field.

**C decision: ACCEPT WITH ENUMERATED AMENDMENTS as a mapping candidate.** This is not acceptance of a frozen wire contract, registered signature profile, implemented validator, provider adapter or production behavior.

C 已对精确 H 1.2.13 Schema 和 H Phase 3.8.8 映射进行复审。针对 H 1.2.12 的两个阻断问题已在结构候选层修正：
1. HANDOFF_REJECTED 不再无条件要求 No-Handoff Proof，而是要求 Provider Request 与 Outcome Evidence；
2. 删除语义重复的 `participant_intent_ref`，只保留单一 nullable 的 `coc_participant_intent_ref`。

**C 决议：作为映射候选 ACCEPT WITH ENUMERATED AMENDMENTS。** 这不等于 Wire 冻结、签名配置注册、验证器实现、Provider Adapter 或生产行为验收。

## 2. C semantic confirmation / C 语义确认

The following are accepted as exact candidate mappings:
- C `record_ref/payload_digest` ↔ H `c_submit_outcome_ref/c_submit_outcome_digest`;
- C `Outcome` ↔ H `provider_outcome`;
- C `ProviderRef/AdapterRef/IdempotencyKeyRef/FinalRequestBoundaryRef/RequestDigest/CausalOrderTransactionRef` ↔ the corresponding H inline fields;
- C `OutcomeEvidenceRef` ↔ H `provider_outcome_evidence_ref`;
- C admission/ledger identity and currentness tuple ↔ H owner admission/ledger fields;
- C `COCParticipantIntentRef/ReservationRef` ↔ H `coc_participant_intent_ref/participant_reservation_ref`;
- C ProviderAttempt and gate tuple remain in the immutable C object and are mandatory H dereference inputs.

C's ProviderAttemptRef/Generation remains distinct from Storage's `prepare_attempt_ref/generation`. C's owner ledger remains distinct from Storage's `participant_ledger_ref/version`. H's envelope digest, C object digest and C provider evidence digest remain three separate digest domains.

以下映射作为精确候选接受：C 对象 Ref/Digest、Outcome、Provider/Adapter/Idempotency Key/Final Request/Request Digest/Transaction、Outcome Evidence、C Admission/Owner Ledger 及 COC Intent/Reservation，分别映射至对应 H Wire 字段。C ProviderAttempt 与 Gate 元组仍必须从不可变 C 对象解引用。C ProviderAttempt 不得与 Storage PrepareAttempt 混淆；C Owner Ledger 不得与 Storage Participant Ledger 混淆；H Envelope Digest、C Object Digest、Provider Evidence Digest 是三个独立摘要域。

## 3. Outcome predicate acceptance / Outcome 谓词接受

- HANDOFF_ACCEPTED: requires C `SideEffectStatus=PROVEN_OCCURRED`, provider request, receipt, outcome evidence and a valid COC reservation/intent pair.
- HANDOFF_REJECTED: H structural requirements now align with C; semantic validation must inspect C `SideEffectStatus`. `PROVEN_NONE` requires authoritative no-handoff proof; `POSSIBLE_OR_UNKNOWN` remains nonterminal/blocking; `PROVEN_OCCURRED` remains an occurred side effect and must be reconciled.
- NOT_INVOKED: requires C no-handoff + not-invoked proofs and `SideEffectStatus=PROVEN_NONE`.
- UNKNOWN / IN_DOUBT: requires unknown reason and `SideEffectStatus=POSSIBLE_OR_UNKNOWN`; same attempt/key/request tuple is retained.

HANDOFF_ACCEPTED 必须证明副作用已发生并具有 Provider Request/Receipt/Outcome Evidence 与有效 COC Reservation/Intent。HANDOFF_REJECTED 必须检查 C 对象 SideEffectStatus：PROVEN_NONE 需要权威 No-Handoff Proof；POSSIBLE_OR_UNKNOWN 保持非终态/阻塞；PROVEN_OCCURRED 必须按已发生副作用协调。NOT_INVOKED 必须有 No-Handoff 与 Not-Invoked Proof，且 PROVEN_NONE。UNKNOWN/IN_DOUBT 必须保留原 Attempt/Key/Request 元组。

## 4. Enumerated conditions / 明确保留条件

1. **H semantic validator:** MUST dereference the exact immutable C object, compare all duplicated fields, verify the C object digest and enforce SideEffectStatus-dependent predicates. The H helper/callback remains TEST-ONLY; no production verifier is claimed.
2. **I profile registration:** `AIMBA-C-CRYPTO-1.0` remains a candidate. I must register or reject it and approve trust roots, key lifecycle, historical key-status verification and anti-rollback.
3. **Canonical interoperability:** C/H must execute independent Python/JavaScript canonical-byte, digest and signature vectors against the exact H 1.2.13 and C 1.0.0 blobs after I registration.
4. **Provider proof:** provider-specific lookup/idempotency namespace, retention, authoritative lookup consistency and same-key recovery must be proven per supported adapter. A schema test does not prove provider truth.
5. **Storage/COC join:** Storage must bind C owner admission/outcome to the exact RecoveryBatch/Manifest/RecoveryJoin and same PreparedParticipant tuple; Storage evidence cannot synthesize C outcome.
6. **A integration:** A must re-review the exact current Storage/C/H/I/D bundle; no prior A acceptance transfers.

## 5. Test and evidence boundary / 测试与证据边界

The following older bounded CI remains accurately scoped:
- C schema/selected semantic suite: run `44055965702`, 3 passed.
- C candidate Python/Node JCS/Ed25519 suite: run `44057463855`, 7 passed.
- H independent candidate Python/Node JCS/Ed25519 suite: run `44057944517`, 10 passed.

These runs used the C object schema 1.0.0 and candidate test vectors; they did **not** test H schema 1.2.13. No H13-C01..C23 execution is claimed. The C profile remains unregistered, test keys are not production secrets, and no live provider adapter, C gate race, I/D sequencer, Storage/COC bridge or production runtime was tested by these runs.

既有受限 CI 的范围保持不变：C Schema/语义 3 项、C 候选 Python/Node JCS/Ed25519 7 项、H 独立候选验证 10 项。它们均未测试 H 1.2.13；不声称 H13-C01..C23 已执行。C 配置仍未注册，测试密钥不是生产密钥，真实 Provider Adapter、Gate Race、I/D Sequencer、Storage/COC Bridge 与生产 Runtime 均未由这些运行验证。

## 6. C disposition / C 侧结论

**Delegated C-role decision: ACCEPT WITH ENUMERATED AMENDMENTS for H 1.2.13 mapping candidate. NOT WIRE-FROZEN.**

H 1.2.13 closes the identified structural incompatibilities, but the semantic validator, exact-version vectors, I profile registration, provider-specific recovery proof and Storage RecoveryJoin remain open. JF-10 P0 remains OPEN; no production activation, exactly-once, Multi-PolicyDomain, Global Forget completion or physical Forget is claimed.

**角色模拟 C 侧决议：对 H 1.2.13 映射候选 ACCEPT WITH ENUMERATED AMENDMENTS，不冻结 Wire。** 结构性问题已修正，但语义验证器、精确版本向量、I 配置注册、Provider 恢复证明及 Storage RecoveryJoin 仍未闭合。JF-10 P0 仍 OPEN。
