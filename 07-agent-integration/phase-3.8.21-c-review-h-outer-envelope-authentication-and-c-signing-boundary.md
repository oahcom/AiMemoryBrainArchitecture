# Phase 3.8.21 — C Review: H Outer Envelope Authentication and C Signing Boundary
# Phase 3.8.21 — C 复审：H 外层 Envelope Authentication 与 C Signing 边界

- C authority: Provider Outcome Semantic Authority
- H gap/decision contract Blob: fbb7553b0bd0c7a9714304983882ca2cc1fa9cc1
- H Unified 1.2.14 schema Blob: 09fcd1fa29fe24255fbd87cae79dafb406594a59
- CSubmitOutcome 1.0.1 schema Blob: a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda
- C signature projection/profile contract: 06d9264124d85896ccd44ef7789d9af245d8255b
- Status: **ACCEPT GAP IDENTIFICATION; C ENVELOPE SIGNER/P0 DECISION REQUIRED; NO PROFILE REUSE APPROVED**
- Provenance: delegated C-role review; not an independent human C Owner signature.

## 1. C object and outer envelope are distinct / C Object 与外层 Envelope 独立

C confirms that AIMBA-C-CRYPTO-1.0 currently authenticates the immutable CSubmitOutcome object under C's C-P0 projection. It does not automatically authenticate the outer BMCP envelope, because the envelope is a distinct serialized object with additional sender, issuer, subject, audience, nonce, channel-binding, integrity-reference and message-family fields.

C 确认 AIMBA-C-CRYPTO-1.0 当前认证的是 CSubmitOutcome 不可变对象及其 C-P0 Projection。它不会自动认证外层 BMCP Envelope，因为 Envelope 是独立序列化对象，包含额外 Sender、Issuer、Subject、Audience、Nonce、Channel-Binding、Integrity Ref 与 Message Family 字段。

C does not authorize H to reuse the C object P0 or signature preimage for the outer envelope. C also does not authorize H to assume the C object signature implies the envelope is authentic.

C 不授权 H 将 C Object P0 或 Signature Preimage 复用到外层 Envelope；也不允许 H 假定 C Object Signature 能推出 Envelope 已认证。

## 2. C decision required / C 必须作出的决策

For C_PROVIDER_OUTCOME_RECORDED, C must explicitly decide whether:
- the C adapter signs a distinct envelope projection in addition to the immutable C object; or
- an H gateway signs a separate receipt/attestation over authenticated transport ingress, with a clearly distinct issuer and evidentiary meaning; or
- the message contract uses another explicitly owned signing model.

If C is the envelope signer, C must publish an exact envelope-specific P0 allowlist, domain separator, signature preimage, signer identity, profile identifier, key-status linkage and cross-language vectors. This must be a distinct signed-object contract, not silent reuse of the C object P0.

对于 C_PROVIDER_OUTCOME_RECORDED，C 必须明确决定：
- C Adapter 是否除不可变 C Object 外，还签署独立 Envelope Projection；
- 或 H Gateway 是否对已认证 Transport Ingress 签署独立 Receipt/Attestation，并明确不同 Issuer 与证据含义；
- 或采用其他有明确 Owner 的签名模型。

若由 C 签署 Envelope，C 必须发布精确 Envelope 专属 P0 Allowlist、Domain Separator、Signature Preimage、Signer Identity、Profile ID、Key Status Linkage 与跨语言向量。这必须是独立 Signed-Object 合同，不得静默复用 C Object P0。

## 3. C-owned invariants / C 自有不变量

Regardless of outer-envelope signer choice, C remains the sole semantic authority for CSubmitOutcome identity, C-P0 digest/signature, C sequence namespace, key-status ordering, ProviderAttempt, C Gate, provider/account/adapter/endpoint/region/API operation, idempotency, final request boundary, SideEffectStatus and provider evidence. The envelope cannot rewrite these facts.

无论外层 Envelope 由谁签署，C 仍独占 CSubmitOutcome Identity、C-P0 Digest/Signature、C Sequence Namespace、Key Status Ordering、ProviderAttempt、C Gate、Provider/Account/Adapter/Endpoint/Region/API、Idempotency、Final Request Boundary、SideEffectStatus 与 Provider Evidence 的语义权威。Envelope 不得改写这些事实。

## 4. C disposition / C 侧结论

**Delegated C-role decision: ACCEPT H's identification of outer-envelope authentication as a separate blocking contract gap. C signature-profile reuse is NOT APPROVED. A C-owned envelope signer/P0 decision is required before H can finalize the mapping. Production C trust/egress remain OPEN.**
