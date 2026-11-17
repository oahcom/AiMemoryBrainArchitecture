# Phase 3.8.25 — C Exact Re-review: H Gateway Attestation P0 Candidate (Digest Encoding Corrected)
# Phase 3.8.25 — C 精确复审：H Gateway Attestation P0 候选（Digest Encoding 已修正）

- H P0 candidate: Phase 3.8.20, Blob `a08bff1145dfeccac3e583e065055ca7dfdcb189`
- H Unified 1.2.14 schema digest convention: Blob `09fcd1fa29fe24255fbd87cae79dafb406594a59`, `^[0-9a-f]{64}$`
- CSubmitOutcome 1.0.1 digest convention: Blob `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda`, `^[a-f0-9]{64}$`
- Prior C review of H P0: Phase 3.8.24, Blob `f7201c344e29c67e9bb6398756665cb007122080` (predecessor P0 Blob only)
- C signer model: Phase 3.8.23, Blob `65aa82bac678e317325b1673121b92c04121b4f4`
- Status: **ACCEPT CORRECTED DIGEST ENCODING; RETAIN C-OWNED SEMANTIC CONDITIONS; NOT FROZEN**
- Provenance: delegated C-role exact re-review; not an independent human C Owner signature.

## 1. Exact correction / 精确修正

The previous H P0 draft described the digest encoding as unpadded Base64url. That did not match either the current H envelope schema or the immutable C object schema, both of which define SHA-256 digest strings as 64-character lowercase hexadecimal.

The corrected H P0 Blob `a08bff...` now specifies:
- digest: SHA-256 encoded as 64-character lowercase hexadecimal;
- signature: Ed25519 encoded as unpadded Base64url.

C independently read both schema definitions and confirms the encoding distinction is correct. This is a material P0 correction; the earlier C Phase 3.8.24 review does not transfer to the changed H P0 Blob.

上一版 H P0 将 Digest Encoding 写为无 Padding Base64url，与当前 H Envelope Schema 和不可变 C Object Schema 均不一致；两者都规定 SHA-256 Digest String 为 64 字符小写十六进制。

修正后的 H P0 Blob `a08bff...` 现规定：
- Digest：SHA-256，64 字符小写十六进制；
- Signature：Ed25519，无 Padding Base64url。

C 已独立读取两个 Schema 定义，确认编码区分正确。这是实质 P0 修正；前序 C Phase 3.8.24 不自动转移到变更后的 H P0 Blob。

## 2. C conditions retained / C 条件继续保留

C retains every condition in Phase 3.8.24:
- C object ref/digest and all duplicated wire fields are bound exactly;
- C owner signature evidence ref is included and independently verified;
- raw origin bytes are hashed before parsing/normalization and retained/referenced;
- origin transport context binds the authenticated C adapter to C `AdapterRef` under explicit registry policy;
- H attestation is issued only after C object schema/digest/signature verification;
- H attestation never proves provider truth and cannot terminalize UNKNOWN/IN_DOUBT;
- `integrity_proof_ref` must resolve to immutable evidence bound to P0 digest, signature, profile, key version and signing sequence;
- `signature_profile_id` must be conditionally required by schema 1.2.15;
- origin C→H and H→receiver channel bindings remain distinct;
- replay/receipt crash recovery must be idempotent and durable.

C 继续保留 Phase 3.8.24 的全部条件：C Object Ref/Digest 与重复 Wire Field 精确绑定；C Owner Signature Evidence 独立验证；Raw Origin Bytes 在 Parse/Normalize 前 Hash 并留存；Origin Transport Context 通过显式 Registry Policy 将认证 C Adapter 与 C `AdapterRef` 绑定；C Object Schema/Digest/Signature 验证后才能签发 H Attestation；H Attestation 不证明 Provider Truth，也不能终结 UNKNOWN/IN_DOUBT；Integrity Proof 必须是绑定 P0/Digest/Signature/Profile/Key Version/Sequence 的不可变证据；Schema 1.2.15 必须条件性要求 `signature_profile_id`；两个 Channel Binding 必须分离；Replay/Receipt Crash Recovery 必须 Durable/Idempotent。

## 3. C disposition / C 侧结论

**Delegated C-role decision: ACCEPT the corrected H P0 digest/signature encoding as a candidate. C semantic conditions remain mandatory. No H profile registration, H key approval, production gateway attestation or C provider egress is authorized. NOT FROZEN.**

**角色模拟 C 侧决议：接受修正后的 H P0 Digest/Signature Encoding 作为候选。C 语义条件仍为强制要求。不授权 H Profile 注册、H Key 批准、生产 Gateway Attestation 或 C Provider Egress。不冻结。**
