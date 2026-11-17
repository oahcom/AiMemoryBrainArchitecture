# H — Exact-Version Review: Unified COC/JF-10 Schema 1.2.7
# H 精确版本审查：统一 COC/JF-10 Schema 1.2.7

- Owner perspective: H — BMCP Protocol & Schema
- Reviewed artifact: `08-bmcp-protocol/schemas/bmcp.coc-jf10-unified-1.2.7.schema.json`
- Exact Blob: `e9748a5b904d2b975e47a32a0cbb31de31636854`
- Compared prior artifact: 1.2.6 Blob `ea8d644df17ea88ed368980b7d5930cd33934fd2`
- Decision: **ACCEPT WITH ENUMERATED AMENDMENTS — STRUCTURAL ENVELOPE ONLY**
- Status: **NOT FROZEN / SEMANTIC AND INTEROPERABILITY GATES OPEN**
- Review mode: delegated H-role simulation at user's direction; not independent human Owner signature.
- Language: English and Chinese are normative peers.

## 1. Exact diff / 精确差异

Compared with 1.2.6, the 1.2.7 schema introduces:
1. Optional `$defs.commonEnvelope.properties.signature_profile_id` as a distinct field from `canonicalization_profile_id`.
2. Description clarifications that `key_id_ref` is an authenticated issuer/owner key reference and `key_version` is immutable.
3. An updated common envelope description stating protected owner-signed records require `signature_profile_id` by semantic validation.
4. Artifact revision changes to 1.2.7 while the on-wire protocol-family `schema_version` remains 1.2.0.

This is a narrow but useful improvement: canonical byte normalization and cryptographic signature profile are different concepts and must not be conflated.

## 2. H disposition / H 审查结论

H accepts the structural field addition **with amendments**. The schema is not sufficient by itself because `signature_profile_id` is optional in the JSON Schema. For every protected owner-signed record, the semantic validator MUST require it. The validator MUST reject missing, empty, unknown, untrusted, wrong-owner, wrong-audience, wrong-purpose, downgraded or incompatible profile identifiers.

The profile identifier is a reference, not authority. A receiver MUST resolve it through an authenticated trust registry controlled by the relevant authority (I for identity/authorization signatures). It MUST NOT trust a payload-supplied profile definition, algorithm choice or public key.

## 3. Required signature binding / 签名绑定要求

For a protected owner-signed record, the verified signature input MUST bind at least:
- exact schema artifact revision and on-wire schema family/version;
- signature_profile_id and canonicalization_profile_id as distinct typed identifiers;
- owner authority, issuer, key_id_ref and immutable key_version;
- audience, message purpose/type, scope and relevant PolicyDomain;
- exact canonical payload bytes and digest domain;
- issuance/expiry/acceptance semantics, nonce/replay identity and applicable anti-rollback anchor.

A profile change MUST NOT silently reinterpret historical signatures. Rotation, revocation, compromise, backdating, historical verification and key-status freshness require I-owned normative rules and executable negative vectors.

## 4. H tests and evidence boundary / 测试与证据边界

The current H 66-case CI suite does not load or validate unified schema 1.2.7; its schema tests target Recovery Cutoff 1.0.4 and RecoveryJoin 1.0.0. Therefore this exact 1.2.7 review is a static structural review only. No 1.2.7-specific schema validator PASS, signature-profile vector, downgrade test or independent-language interoperability is claimed.

Required additions before freeze:
1. Add 1.2.7 to the schema candidate integrity suite and pin its exact Blob.
2. Add semantic tests proving signature_profile_id is mandatory for protected owner-signed records and optional only for explicitly unsigned/non-protected message families.
3. Add missing/unknown/wrong-owner/wrong-audience/wrong-purpose/profile-downgrade/key-version-rollback negative vectors.
4. Add I trust-registry resolution and historical key-status verification contract.
5. Add two independent language implementations producing identical canonical bytes and signature preimages under the selected profile.

## 5. H final decision / H 最终裁决

**ACCEPT WITH ENUMERATED AMENDMENTS** for the structural addition of an explicit signature profile reference. This is not cryptographic profile approval, semantic conformance, wire interoperability, schema freeze or production activation.

中文：H 有条件接受 1.2.7 增加独立的 `signature_profile_id` 字段。该字段必须与 Canonicalization Profile 分离；对受保护的 Owner 签名记录，语义验证器必须强制要求该字段，并通过 I 控制的可信注册表解析，不能信任 Payload 自带的算法或密钥定义。当前 66 项 CI 并未覆盖统一 Schema 1.2.7，因此本次仅为静态结构审查，不是 1.2.7 测试通过或密码学批准。

