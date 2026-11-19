# Owner Snapshot Namespace and Fence Currentness Contract / 所有者快照命名空间与 Fence 当前性契约

- Contract version / 契约版本: **1.3.0 (CANDIDATE)**
- Revision / 修订: 1.3.0 incorporates review round 3 findings (normalization moved from NFC to NFKC so compatibility-equivalent inputs cannot diverge — a fullwidth `Ａ` previously yielded a different canonical than ASCII `A`; per-segment trimming moved after decoding and normalization so whitespace arriving via `%20` or U+3000 obeys the same rule as literal whitespace; step 5 percent-encoding equivalence scoped to segments passing step 2; segments whose NFKC form contains a compatibility-derived `/` are rejected) / 1.3.0 吸收第 3 轮审查发现（规范化由 NFC 改为 NFKC，使兼容等价输入不再分叉——全角 `Ａ` 此前与 ASCII `A` 得出不同 canonical；段落级 trim 移至解码与规范化之后，使经 `%20` 或 U+3000 到达的空白与字面空白同规则；第 5 步的百分号等价承诺限定于通过第 2 步的段；规范化后含兼容派生 `/` 的段一律拒绝）
- Revision / 修订: 1.2.0 incorporates review round 2 findings (canonicalization pipeline reordered so percent-decoding precedes case folding and NFC, removing a non-uniqueness defect between `%41UTH-A` and `AUTH-A`; step 1 parse declared single authoritative; decoded-UTF-8 validity and encoded-delimiter rejection made explicit; section 5 English list renumbered 1-11; case folding specified as Unicode canonical caseless matching to close the same defect class across normalization forms; idempotence required with NFC as sole normal form) / 1.2.0 吸收第 2 轮审查发现（规范化流水线重排：百分号解码先于大小写折叠与 NFC，消除 `%41UTH-A` 与 `AUTH-A` 产生不同 canonical 的非唯一性缺陷；第 1 步解析声明为单次权威；显式规定解码后 UTF-8 合法性校验与编码分隔符注入拒绝；第 5 节英文列表重编号为 1–11；大小写折叠改为 Unicode canonical caseless matching 以闭合同一缺陷类在规范化形式上的分叉；要求幂等且 NFC 为唯一规范形式）
- Revision / 修订: 1.1.0 incorporates review round 1 findings (ledger lifecycle classification unified with the section 8 decision table; Authority-level authorization revocation restored; prohibition on automatic rollback of executed fade/forget restored; percent-encoding character set, leading-zero policy, Fence replacement classification and state-version concurrency boundary made normative) / 1.1.0 吸收第 1 轮审查发现（Ledger 生命周期判定与第 8 节判定表统一；恢复 Authority 级授权撤销规则；恢复已执行 fade/forget 不得自动回滚的约束；百分号编码字符集、前导零策略、Fence 替换判定及状态版本并发边界转为规范要求）
- Status / 状态: **DECIDED / IMPLEMENTATION NOT VERIFIED / CONFORMANCE NOT RUN**
- Source decisions / 决定来源: Issue #25 comments `7008208052` (NS-PR-01..05), `7008249894` (FC-01..04), `7009205234` (four decisions)
- Authoring session / 起草会话: `6afee171-c0d8-83ee-8a90-1bae3d42d22c` (prompts `62/63/64/70/71/72`)
- Coordinator registration / 协调器登记: issue comment `7009205234`
- Nature / 性质: D-role session-authored normative decisions. **Not** a human Owner signature, **not** a contract freeze, **not** evidence of implementation or production readiness.
- 性质：D 角色会话起草的规范决定。**非** Owner 真人签署，**非**契约冻结，**非**实现或生产就绪证据。

---

## English

**1. Document identity and status**

- Document name: Owner Snapshot Namespace and Fence Currentness Contract
- Version: 1.3.0 (CANDIDATE)
- Status: Decisions made, **implementation unverified**, **no consistency run executed**.
- Revision 1.3.0 incorporates review round 3 findings: normalization moved from NFC to NFKC so that compatibility-equivalent inputs cannot diverge (a fullwidth `Ａ` previously produced a different canonical form than ASCII `A`); per-segment trimming moved to after decoding and normalization so that whitespace arriving through percent-encoding (`%20`) or compatibility decomposition (U+3000) obeys the same rule as literal whitespace, closing a second divergence path; the percent-encoding equivalence promise in step 5 is scoped to segments that pass step 2; and, because NFKC itself maps U+FF0F FULLWIDTH SOLIDUS to ASCII `/`, a segment whose normalized form contains a literal `/` is now an explicit rejection case.
- Revision 1.2.0 incorporates review round 2 findings: the canonicalization pipeline is reordered so that percent-decoding precedes case folding and NFC, eliminating a non-uniqueness defect where an encoded segment (`%41UTH-A`) and its literal equivalent (`AUTH-A`) produced different canonical forms; the parsed segments from step 1 are declared the single authoritative parse; UTF-8 validity of decoded bytes and rule-out of encoded-delimiter injection are made explicit; and the section 5 English list is renumbered so that items run 1-11 without a duplicate.
- Revision 1.2.0 also hardens the same defect class found in round 2: case folding is now specified as the Unicode canonical caseless matching sequence (NFC, then Default Case Folding, then NFC) so that inputs differing only in normalization form cannot diverge, and canonicalization is required to be idempotent with NFC as the sole accepted normal form.
- Revision 1.1.0 incorporates review round 1 findings: ledger lifecycle state classification unified with the section 8 decision table; Authority-level authorization revocation restored; the prohibition on automatic rollback of executed fade/forget restored; percent-encoding character set, high-water leading-zero policy, Fence replacement classification, and state-version concurrency boundary made normative.
- This document records D-side normative decisions and constraints; it does not constitute evidence of completed implementation.
- This document is not a human Owner signature, is not a contract freeze, and must not be used as evidence of production readiness.
- The normative decisions in this document must not be interpreted as evidence that existing schemas, validators, or runtimes already implement the corresponding behavior.

**2. Scope and out-of-scope**

In scope:

1. Identity, binding, canonicalization, and currentness of the ProducerWork Registration Ledger namespace.
2. Composition, validation, dual high-water comparison, version control, and revocation of ForgetFence Currentness Proofs.

Out of scope:

1. Cryptographic signature algorithms and their specific implementations.
2. Key registry schemas, key storage, and key distribution implementations.
3. Storage physical mappings, physical storage layouts, and underlying data migration.
4. H-side and I-side implementation details not defined by this contract.

**3. Namespace definition (NS-PR-01..05)**

**NS-PR-01: Nominal definition**

1. The ProducerWork Registration Ledger Namespace is an independent logical namespace governed by D, identifying the registration domain to which producer work registration records belong.
2. This namespace is independent of ForgetFence high-water marks and generic admission watermarks.
3. This namespace is not an alias, derived value, or replacement for `admission_high_water`.
4. This namespace is not a ForgetFence high-water mark, producer name, or individual work-record ID.
5. Namespace identity MUST NOT be derived from generic watermark fields.

**NS-PR-02: Identifier composition**

The namespace identifier MUST use the following four-segment structure:

`<authority_id>/<producer_class>/<ledger_id>/<contract_version>`

The four segments represent:

- `authority_id`: Canonical Memory Authority identity.
- `producer_class`: Producer classification.
- `ledger_id`: ProducerWork Registration Ledger identity.
- `contract_version`: Contract version.

All four segments are mandatory. Empty segments are prohibited.

**NS-PR-03: Binding relationships**

1. A namespace MUST bind to exactly one Canonical Memory Authority.
2. A namespace MUST include a Producer class identity.
3. A namespace MUST bind to an explicit Ledger identity.
4. Contract version participates in namespace identity; different versions produce different namespace identifiers.
5. When Authority, Producer class, Ledger identity, or contract version changes, the canonical identifier MUST be recalculated.
6. Ledger identity, Authority identity, and Producer class MUST NOT substitute for one another.

**NS-PR-04: Currentness**

A namespace MUST be considered `STALE` under any of the following conditions:

1. Its original Authority binding undergoes an incompatible change.
2. Its Producer class definition undergoes an incompatible change.
3. Its Ledger identity is migrated, replaced, or rebuilt and the continuity of the original identity has been confirmed as no longer current. Where continuity cannot be confirmed, the namespace MUST be classified as `UNKNOWN` rather than `STALE`.
4. Its original contract version is superseded by an incompatible version.
5. Its canonical representation no longer conforms to the current specification.

`STALE` means that an identity may have been historically valid but is no longer current. `INVALID` means that the input itself violates identity or format constraints. These states MUST NOT be automatically converted into one another.

Ledger lifecycle state MUST NOT be mapped to `STALE`. The following mappings are normative and MUST be applied exactly as recorded in section 8:

1. A namespace pointing to a revoked Ledger MUST be classified as `INVALID`.
2. A namespace pointing to a Ledger whose confirmed retirement is established MUST be classified as `INVALID`.
3. A namespace pointing to a Ledger that has been migrated but whose continuity cannot be confirmed MUST be classified as `UNKNOWN`.

Where a Ledger lifecycle condition and a namespace-identity staleness condition both appear to apply, the Ledger lifecycle mapping above takes precedence for determination purposes. A namespace MUST NOT be reported as `STALE` on Ledger lifecycle grounds alone.

**NS-PR-05: Prohibition on interchangeability**

1. The ProducerWork Registration Ledger Namespace MUST NOT substitute for the ForgetFence namespace.
2. The ProducerWork Registration Ledger Namespace MUST NOT substitute for the I-side `inventory_epoch_ref`.
3. The composite-path field `producer_domain_inventory_epoch_ref` MUST NOT be treated as equivalent to `inventory_epoch_ref` without an explicit contractual mapping.
4. The ProducerWork Registration Ledger Namespace MUST NOT substitute for the canonical commit cursor.
5. The ProducerWork Registration Ledger Namespace MUST NOT substitute for generic `admission_high_water`.

**4. Canonicalization algorithm**

All namespace identifiers MUST be canonicalized in the following six steps, in exactly this order. Decoding MUST precede normalization and case folding; applying either to a still-encoded segment is prohibited.

1. **Trim and split (single authoritative parse):** Remove leading and trailing Unicode White_Space from the entire input. Split the result on ASCII `/`, which is the only permitted segment delimiter; exactly four segments are required, and empty segments and repeated delimiters are prohibited. Individual segments are NOT trimmed at this step: per-segment trimming is performed in step 3, after decoding and normalization, so that whitespace arriving via percent-encoding or via compatibility decomposition is subject to exactly the same rule as literal whitespace. The four segments produced here are the single authoritative parse for steps 2 through 6; no later step may re-parse the input.
2. **Decode, exactly once:** Percent-decode each of the four segments one time only. A `%` that does not begin a valid `%HH` triplet MUST be rejected, not passed through. The decoded bytes MUST form valid UTF-8; otherwise the input MUST be rejected. Double decoding is prohibited. Because splitting has already occurred, a segment may decode into a literal `/`: that is encoded-delimiter injection and MUST be rejected rather than accepted as ordinary content.
3. **Normalize, case fold, and trim:** For each of the first three segments, apply NFKC, then Unicode Default Case Folding, then NFKC again, then remove leading and trailing Unicode White_Space. A segment that is empty after this step MUST be rejected. Applying case folding without the preceding normalization is prohibited. NFKC is required rather than NFC so that compatibility-equivalent inputs cannot diverge; the fullwidth `Ａ` and ASCII `A` case below is a required conformance vector. Because NFKC maps compatibility characters onto their ASCII counterparts, a segment MUST be checked again after normalization: a segment whose normalized form contains a literal `/` MUST be rejected, since NFKC maps U+FF0F FULLWIDTH SOLIDUS to ASCII `/` and would otherwise inject a segment boundary that step 2 never saw. The fullwidth-solidus case below is a required rejection vector. The fourth, version segment MUST be trimmed of leading and trailing Unicode White_Space and normalized with NFKC, but MUST NOT undergo case folding.
4. **Idempotence and normal form:** Canonicalization MUST be idempotent — applying it to an already canonical identifier MUST reproduce that identifier byte for byte. NFKC is the only accepted normal form; segments supplied in NFC, NFD, or NFKD form MUST NOT be treated as canonical, and MUST NOT be accepted without passing through step 3.
5. **Re-encode:** Emit each segment as its UTF-8 bytes, with bytes in the RFC 3986 unreserved set (`ALPHA / DIGIT / "-" / "." / "_" / "~"`) written literally and every other byte written as uppercase `%HH`. Lowercase `%hh` in the input MUST be normalized to uppercase. For segments that pass step 2, literal input and percent-encoded input that decode to the same text MUST produce an identical canonical representation; this equivalence MUST NOT be read as permitting an encoded `/`, which step 2 rejects. The `%41UTH-A` / `AUTH-A` and `%20` vectors below are required conformance vectors.
6. **Version segment handling:** The fourth segment MUST conform to `vMAJOR.MINOR.PATCH`. All three components MUST be non-negative decimal integers without leading zeros, except for the value zero itself.

Canonicalization MUST produce a unique and reproducible canonical representation.

Equivalent input examples:

| Input | Canonical |
|---|---|
| `AUTH-A/Class-X/Ledger-1/v1.2.0` | `auth-a/class-x/ledger-1/v1.2.0` |
| ` AUTH-A / CLASS-X / LEDGER-1 / v1.2.0 ` | `auth-a/class-x/ledger-1/v1.2.0` |
| `auth-a/class-x/ledger-1/v1.2.0` | `auth-a/class-x/ledger-1/v1.2.0` |
| `%41UTH-A/Class-X/Ledger-1/v1.2.0` | `auth-a/class-x/ledger-1/v1.2.0` |
| `auth-a/class-x/ledger%2D1/v1.2.0` | `auth-a/class-x/ledger-1/v1.2.0` |
| `auth-a/class-x/ledger%2d1/v1.2.0` | `auth-a/class-x/ledger-1/v1.2.0` |
| `ＡUTH-A/Class-X/Ledger-1/v1.2.0` (U+FF21 FULLWIDTH LATIN CAPITAL LETTER A) | `auth-a/class-x/ledger-1/v1.2.0` |
| `auth-a/class-x/%20ledger-1/v1.2.0` | `auth-a/class-x/ledger-1/v1.2.0` |
| `auth-a/class-x/%E3%80%80ledger-1/v1.2.0` (U+3000 IDEOGRAPHIC SPACE) | `auth-a/class-x/ledger-1/v1.2.0` |

Inputs that MUST be considered non-equivalent:

1. `auth-a/class-x/ledger-1/v1.2.0` and `auth-a/class-x/ledger-1/v1.3.0`: different contract versions.
2. `auth-a/class-x/ledger-1/v1.2.0` and `auth-a/class-x/ledger-2/v1.2.0`: different Ledger identities.

Inputs that MUST be rejected as `INVALID`:

1. Any segment count other than four, empty segments, and repeated delimiters.
2. Any segment that is empty after step 3, including one that becomes empty only after trimming decoded or compatibility-derived whitespace.
3. Any version segment not conforming to `vMAJOR.MINOR.PATCH`.
4. Any `%` not forming a valid `%HH` triplet.
5. Any segment whose decoded bytes are not valid UTF-8.
6. Any segment that decodes to content containing a literal `/` (encoded-delimiter injection), for example `auth-a/class-x/led%2Fa/v1.2.0`.
7. Any segment whose normalized form contains a literal `/` produced by compatibility normalization, for example `auth-a/class-x/led／ger-1/v1.2.0` (U+FF0F FULLWIDTH SOLIDUS).

Rejected inputs MUST NOT be converted into valid identities through permissive parsing.

**5. Dual high-water comparison**

Definitions:

- `captured`: The Producer Registration High Water actually captured by `CaptureProducerRegistrationHighWater`.
- `installed`: The ForgetFence High Water actually installed successfully by `InstallForgetFence`.

Both values MUST be obtained independently and MUST NOT be fabricated or derived from one another.

| Comparison | Determination | Handling |
|---|---|---|
| installed = captured | VALID | Accept |
| installed > captured | VALID | Accept |
| installed < captured | INVALID | Reject |

Additional requirements:

1. Both high-water values MUST use non-negative decimal integer representations.
2. Non-decimal representations, negative numbers, and non-integer representations MUST be classified as `INVALID`.
3. Each value MUST correspond to the actual result of its respective authoritative operation.
4. Deriving `captured` or `installed` from `admission_high_water` is prohibited.
5. Deriving `captured` or `installed` from `owner_high_water` is prohibited.
6. Leading zeros MUST be accepted and MUST NOT change the value. Comparison MUST be performed on the numeric value, never on the string form.
7. A representation consisting solely of zeros MUST be treated as the value zero, and the canonical rendering of zero is `0`.
8. The canonical decimal rendering of a high-water value MUST NOT contain leading zeros. Re-emitting a received value in canonical form MUST preserve its numeric value exactly.
9. A leading `+` or `-` sign, surrounding whitespace, thousands separators, exponent notation, and fractional parts MUST be classified as `INVALID`. They MUST NOT be normalized into a valid value.
10. Implementations MUST support values at least up to 2^63 - 1. A value exceeding the implementation's supported range MUST be classified as `INVALID`; silent truncation, wraparound, and floating-point coercion are prohibited.
11. The existence of a field or the ability to parse a number MUST NOT establish that a Fence was installed or remains current.

**6. Currentness determination**

ForgetFence Currentness Proofs MUST NOT use explicit TTLs and MUST NOT have a time-based validity limit.

Currentness MUST use event-driven invalidation and authoritative state-version comparison.

1. Whenever a ForgetFence state change affects validity, D MUST advance the corresponding monotonically increasing state version.
2. A Currentness Proof MUST carry the Fence state version at issuance.
3. H MUST obtain the current authoritative state version from D.
4. The proof remains valid only when its version matches the current version and the Fence has not been revoked or replaced.
5. A mismatch between the proof version and current version MUST result in `STALE`.
6. An explicitly revoked Fence MUST result in `INVALID`.
7. A Fence that has been replaced by a newer Fence, without an explicit revocation of the superseded Fence, MUST result in `STALE`, not `INVALID`.
8. Inability to obtain the authoritative current state version MUST result in `UNKNOWN`.
9. Local clocks, cache timestamps, and proof-file timestamps MUST NOT substitute for the authoritative state version.
10. **Concurrency boundary.** The revocation/replacement check and the state-version comparison MUST be evaluated against a single authoritative state version read. Splitting them across two reads is prohibited.
11. A proof MUST be re-evaluated against the authoritative state version at every use. Caching a `VALID` determination across distinct operations is prohibited.
12. When the state version advances between proof issuance and verification, the verification result MUST reflect the version actually read. The verifier MUST NOT retry until a matching version is observed in order to obtain `VALID`.

Boundary of the above: items 10-12 are behavioral obligations on the verifier. Storage-layer field names and transaction mechanisms (section 9, item 4) and the retry/cache/recovery protocol for a failed state-version retrieval (section 9, item 8) remain NOT_DECIDED as mechanisms. That an implementation mechanism is undecided MUST NOT be read as permission to violate items 10-12; conformance is judged on the observable property, not on a prescribed mechanism.

State definitions:

- `VALID`: The proof is complete, correctly bound, version-matched, successfully installed, and not revoked.
- `STALE`: The proof may previously have been valid, but its state version or currentness conditions are no longer valid.
- `INVALID`: The proof has an invalid format, missing mandatory fields, an explicit binding conflict, an invalid high-water value, or an explicit revocation.
- `UNKNOWN`: Necessary authoritative state or authorization information cannot be obtained, so validity cannot yet be determined.

Prohibitions:

1. `UNKNOWN` MUST NOT be treated as `VALID`.
2. `STALE` MUST NOT serve as valid authorization for current operations.
3. `INVALID` MUST NOT be converted to `VALID` through permissive parsing or field substitution.
4. The mere existence of a proof file MUST NOT establish currentness.
5. Loss of currentness, proof invalidation, or a downgrade to `STALE`, `INVALID`, or `UNKNOWN` MUST NOT cause any already executed fade or forget operation to be automatically rolled back, reversed, or re-executed. Already executed fade/forget effects persist independently of proof state.
6. Recovery, compensation, and replay for already executed fade/forget operations are not defined by this contract and remain NOT_DECIDED per section 9. Their absence of definition MUST NOT be read as authorizing automatic reversal.

**7. Issuer identity and keys**

Issuer identity MUST separate Authority identity from Key identity:

- `issuer_authority_id`: Mandatory; identifies the D-authorized issuing Authority.
- `issuer_key_id`: Mandatory; identifies the actual signing Key.

Normative requirements:

1. The issuing principal belongs to an Authority.
2. The actual signing key is identified by an independent Key identity.
3. Ledger identity MUST NOT substitute for issuer identity.
4. One Authority MAY manage multiple Keys and MAY rotate keys.
5. Activation of a new Key MUST NOT automatically revoke proofs previously issued by an old Key.
6. Following normal rotation, historical proofs legitimately issued by the old Key remain valid while the Fence state version remains current and the old Key has not been retroactively revoked.
7. Normal retirement of an old Key MUST NOT automatically invalidate historical proofs.
8. If an old Key is revoked due to compromise or authorization violations, proofs within the revocation scope MUST be classified as `INVALID`.
9. If the authorization of the issuing Authority itself is revoked, every proof that depends on that authorization MUST be classified as `INVALID`. This holds independently of the Key's own status: a Key that is itself uncompromised, unexpired, and never individually revoked MUST NOT preserve proof validity once the underlying Authority authorization is revoked.
10. Authority-level revocation MUST NOT be inferred from Key-level revocation, and Key-level revocation MUST NOT be inferred from Authority-level revocation. The two revocation scopes MUST be tracked and evaluated separately.
11. H MUST verify the authorization relationship between the Key and Authority and the Key's validity at issuance.
12. The existence of an `issuer_key_id` alone MUST NOT be sufficient for acceptance.

Specific signature algorithms, key registry schemas, key revocation timestamps, and historical revocation proof formats are not defined by this contract.

**8. Decision table**

| Input state | Determination | Handling |
|---|---|---|
| Namespace identifier missing | INVALID | Reject |
| Namespace identifier is an empty string | INVALID | Reject |
| Different casing but identical after canonicalization | VALID | Compare after canonicalization |
| Contains an invalidly decodable escape | INVALID | Reject |
| Contract version does not match the required version | STALE | Reject as current identity |
| Authority explicitly bound incorrectly | INVALID | Reject |
| Ledger revoked | INVALID | Reject |
| Ledger confirmed retired | INVALID | Reject |
| Ledger migrated but continuity cannot be confirmed | UNKNOWN | Suspend acceptance |
| Fence state version matches current version | VALID | Continue validating other constraints |
| Fence state version differs from current version | STALE | Obtain a new proof |
| Fence explicitly revoked | INVALID | Reject |
| Fence replaced by a newer Fence without explicit revocation | STALE | Obtain a new proof |
| Authoritative state version unavailable | UNKNOWN | MUST NOT pass |
| installed = captured | VALID | Accept |
| installed > captured | VALID | Accept |
| installed < captured | INVALID | Reject |
| High-water value contains non-decimal characters | INVALID | Reject |
| High-water value contains leading zeros | VALID | Compare numerically after canonicalization |
| High-water value exceeds the supported range | INVALID | Reject |
| Mandatory issuer identity field missing | INVALID | Reject |
| Issuer Key authorization cannot be confirmed | UNKNOWN | MUST NOT pass |
| Issuing Authority authorization revoked | INVALID | Reject at scope level |
| Old Key normally retired through rotation and proof remains current | VALID | Continue accepting |
| Old Key explicitly retroactively revoked | INVALID | Reject |

**9. NOT_DECIDED items**

The following matters are not defined by this version:

1. Specific cryptographic signature algorithms, signature envelopes, and verification implementations.
2. Physical and logical schemas of the key registry.
3. Key revocation timestamps, revocation propagation protocols, and the specific representation of historical proof retroactive revocation scopes.
4. Field names, transaction mechanisms, and persistence mechanisms for Fence state versions in the storage layer.
5. The specific serialization schema and field encoding of Currentness Proofs.
6. The Unicode data version used for Unicode normalization and Case Folding.
7. Namespace migration, historical identity inheritance, and cross-version migration protocols.
8. Retry, caching, and recovery protocols when state-version retrieval fails.
9. Audit retention, replay, and compensation mechanisms for already executed fade/forget operations.
10. The authoritative state-query interface and transport protocol between D and H.

The percent-encoding character set (section 4), the high-water leading-zero policy (section 5), the Fence replacement classification boundary (section 6), and the Authority-level revocation scope (section 7) are DECIDED by this version and MUST NOT be listed as undecided or deferred to implementer discretion.

Undecided items MUST NOT be treated by implementers as having already received D contractual authorization.

**10. Conformance status**

| Check | Status |
|---|---|
| IMPLEMENTATION | NOT_IMPLEMENTED |
| CONFORMANCE VECTORS | SPECIFIED_NOT_RUN |
| EXACT-HEAD CI | NOT_RUN |

This version records normative decisions only. It does not demonstrate code implementation, composite-runtime validation, CI verification, or production-environment consistency.

Before claiming conformance to this contract, an implementation party MUST complete the corresponding implementation, exact-version verification, and full execution of conformance vectors, and provide verifiable evidence.

---

## 中文

**1. 文档标识与状态**

- 文档名：Owner Snapshot Namespace and Fence Currentness Contract
- 版本：1.3.0（CANDIDATE）
- 修订：1.3.0 吸收第 3 轮审查发现——规范化由 NFC 改为 **NFKC**，使兼容等价输入不再分叉（此前全角 `Ａ` 与 ASCII `A` 得出不同 canonical）；段落级 trim 由「先 trim 再解码」改为「解码与规范化之后统一 trim」，使经 `%20` 编码到达或经 U+3000 兼容分解产生的空白与字面空白适用同一规则，闭合第二条分叉路径；第 5 步的百分号等价承诺限定于通过第 2 步的段；并因 NFKC 会把 U+FF0F 全角斜线映射为 ASCII `/`，将「规范化后含字面 `/` 的段」列为显式拒绝项。
- 修订：1.2.0 吸收第 2 轮审查发现——规范化流水线重排为「解码先于大小写折叠与 NFC」，消除 `%41UTH-A` 与 `AUTH-A` 产生不同 canonical 的非唯一性缺陷；第 1 步解析声明为第 2–6 步的单次权威解析；显式规定解码后字节必须为合法 UTF-8、编码分隔符注入必须拒绝；第 5 节英文列表重编号为 1–11（消除重复编号 6）；并将大小写折叠规定为 Unicode canonical caseless matching（NFC → 折叠 → NFC），补上同一缺陷类在规范化形式上的分叉口，同时要求幂等、NFC 为唯一规范形式。
- 修订：1.1.0 吸收第 1 轮审查发现——Ledger 生命周期判定与第 8 节判定表统一；恢复 Authority 级授权撤销规则；恢复已执行 fade/forget 不得自动回滚的约束；百分号编码字符集、前导零策略、Fence 替换判定及状态版本并发边界转为规范要求。
- 状态：决定已作出、**实现未验证**、**未执行任何一致性运行**。
- 本文记录 D 侧规范决定及其约束，不构成实现完成证明。
- 本文非 Owner 真人签署，非契约冻结，不得作为生产就绪证据。
- 本文中的规范决定不得被解释为现有 schema、validator 或 runtime 已经实现相应行为。

**2. 适用范围与不适用范围**

适用范围：

1. ProducerWork Registration Ledger 命名空间的身份、绑定、规范化及 currentness。
2. ForgetFence Currentness Proof 的构成、验证、双高水位比较、版本控制及撤销。

不适用范围：

1. 密码学签名算法及其具体实现。
2. 密钥注册表 schema、密钥存储及密钥分发实现。
3. Storage 物理映射、物理存储布局及底层数据迁移。
4. 未经本契约定义的 H、I 侧实现细节。

**3. 命名空间定义（NS-PR-01..05）**

**NS-PR-01：名义定义**

1. ProducerWork Registration Ledger Namespace 是 D 权威管理的独立逻辑命名空间，用于标识生产者工作注册记录所属的注册域。
2. 该命名空间独立于 ForgetFence 高水位及通用 admission 水位。
3. 该命名空间不是 `admission_high_water` 的别名、派生值或替代字段。
4. 该命名空间不是 ForgetFence 高水位、生产者名称或单条工作记录 ID。
5. 不得通过通用水位字段推导命名空间身份。

**NS-PR-02：标识符组成**

命名空间标识符采用四段结构：

`<authority_id>/<producer_class>/<ledger_id>/<contract_version>`

四段分别表示：

- `authority_id`：Canonical Memory Authority 身份。
- `producer_class`：生产者类别。
- `ledger_id`：ProducerWork Registration Ledger 身份。
- `contract_version`：契约版本。

四段均为必需组成部分，不允许空段。

**NS-PR-03：绑定关系**

1. 命名空间必须绑定唯一的 Canonical Memory Authority。
2. 命名空间必须包含 Producer class 身份。
3. 命名空间必须绑定明确的 Ledger identity。
4. 契约版本参与命名空间身份；版本不同即为不同命名空间标识符。
5. Authority、Producer class、Ledger identity 或契约版本发生变化时，必须重新计算 canonical identifier。
6. 不得将 Ledger identity、Authority identity 或 Producer class 相互替代。

**NS-PR-04：Currentness**

命名空间在以下情况必须视为 `STALE`：

1. 原 Authority 绑定发生不兼容变更。
2. Producer class 定义发生不兼容变更。
3. Ledger identity 迁移、替换或重建，且原身份的连续性已被确认为不再 current；若连续性无法确认，则命名空间必须判定为 `UNKNOWN`，不得判定为 `STALE`。
4. 原契约版本被不兼容的新版本取代。
5. 命名空间的 canonical representation 不再符合当前规范。

`STALE` 表示历史上可能有效、但当前性已经失效；`INVALID` 表示输入本身违反身份或格式约束。两者不得自动互相转换。

Ledger 生命周期状态不得映射为 `STALE`。以下映射为规范性要求，必须严格按第 8 节判定表执行：

1. 指向已撤销 Ledger 的命名空间必须判定为 `INVALID`。
2. 指向已确认退役 Ledger 的命名空间必须判定为 `INVALID`。
3. 指向已迁移但连续性无法确认的 Ledger 的命名空间必须判定为 `UNKNOWN`。

当 Ledger 生命周期条件与命名空间身份失效条件同时看似成立时，以本节 Ledger 生命周期映射为准进行判定。命名空间不得仅以 Ledger 生命周期为由被报告为 `STALE`。

**NS-PR-05：禁止混用**

1. ProducerWork Registration Ledger Namespace 不可替代 ForgetFence namespace。
2. ProducerWork Registration Ledger Namespace 不可替代 I 侧 `inventory_epoch_ref`。
3. 组合路径中的 `producer_domain_inventory_epoch_ref` 不得未经明确契约映射就视为 `inventory_epoch_ref`。
4. ProducerWork Registration Ledger Namespace 不可替代 canonical commit cursor。
5. ProducerWork Registration Ledger Namespace 不可替代通用 `admission_high_water`。

**4. Canonicalization 算法**

所有命名空间标识符必须按以下六步顺序规范化。百分号解码必须先于规范化与大小写折叠；对仍处于编码态的段执行规范化或折叠属禁止行为。

1. **Trim 与拆段（单次权威解析）**：先移除整个输入首尾的 Unicode White_Space；再按 ASCII `/` 拆段，`/` 是唯一允许的段分隔符，必须恰好四段，禁止空段及重复分隔符。**本步不逐段 trim**：段落级 trim 放在第 3 步、即解码与规范化之后执行，从而使经百分号编码到达的空白与经兼容分解产生的空白，与字面空白适用完全相同的规则。此处得到的四段是第 2 至第 6 步的唯一权威解析结果，后续任何步骤不得重新解析输入。
2. **解码，且仅一次**：对四段各执行一次百分号解码。不以合法 `%HH` 三元组开头的 `%` 必须拒绝，不得原样透传。解码所得字节必须构成合法 UTF-8，否则输入必须拒绝。禁止二次解码。由于拆段已先行完成，某段解码后可能得到字面 `/`：这属于编码后的分隔符注入，必须拒绝，不得作为普通内容接受。
3. **规范化、大小写折叠与 trim**：对前三段依次执行 NFKC → Unicode Default Case Folding → 再次 NFKC，然后移除首尾 Unicode White_Space。经本步后为空的段必须拒绝。缺少前置规范化的大小写折叠属禁止行为。此处要求 NFKC 而非 NFC，以使兼容等价输入不会分叉；下表中的全角 `Ａ` 与 ASCII `A` 为必需的一致性向量。由于 NFKC 会把兼容字符映射为对应 ASCII 字符，**规范化之后必须再检查一次段内容**：规范化后含字面 `/` 的段必须拒绝——NFKC 会把 U+FF0F 全角斜线映射为 ASCII `/`，否则将注入一个第 2 步从未见到的段边界。下表中的全角斜线为必需的拒绝向量。第四段版本段必须移除首尾 Unicode White_Space 并执行 NFKC 规范，但不得执行大小写折叠。
4. **幂等性与规范形式**：Canonicalization 必须幂等——对已是 canonical 的标识符再次执行，必须逐字节复现该标识符。NFKC 是唯一被接受的规范形式；以 NFC、NFD 或 NFKD 形式提供的段不得被视为 canonical，也不得绕过第 3 步被直接接受。
5. **重新编码**：将各段按其 UTF-8 字节输出，属于 RFC 3986 unreserved 集合（`ALPHA / DIGIT / "-" / "." / "_" / "~"`）的字节原样写出，其余所有字节以大写 `%HH` 写出。输入中的小写 `%hh` 必须归一化为大写。对通过第 2 步的段，字面输入与解码后文本相同的百分号编码输入必须产生完全相同的 canonical representation；该等价承诺不得被解释为允许编码后的 `/`——后者由第 2 步拒绝。下表中的 `%41UTH-A` / `AUTH-A` 与 `%20` 均为必需的一致性向量。
6. **版本段处理**：第四段必须符合 `vMAJOR.MINOR.PATCH` 格式，三个部分均为非负十进制整数，不允许前导零，数字零本身除外。

Canonicalization 必须产生唯一、可重复的 canonical representation。

等价输入示例：

| 输入 | Canonical |
|---|---|
| `AUTH-A/Class-X/Ledger-1/v1.2.0` | `auth-a/class-x/ledger-1/v1.2.0` |
| ` AUTH-A / CLASS-X / LEDGER-1 / v1.2.0 ` | `auth-a/class-x/ledger-1/v1.2.0` |
| `auth-a/class-x/ledger-1/v1.2.0` | `auth-a/class-x/ledger-1/v1.2.0` |
| `%41UTH-A/Class-X/Ledger-1/v1.2.0` | `auth-a/class-x/ledger-1/v1.2.0` |
| `auth-a/class-x/ledger%2D1/v1.2.0` | `auth-a/class-x/ledger-1/v1.2.0` |
| `auth-a/class-x/ledger%2d1/v1.2.0` | `auth-a/class-x/ledger-1/v1.2.0` |
| `ＡUTH-A/Class-X/Ledger-1/v1.2.0`（U+FF21 全角拉丁大写字母 A） | `auth-a/class-x/ledger-1/v1.2.0` |
| `auth-a/class-x/%20ledger-1/v1.2.0` | `auth-a/class-x/ledger-1/v1.2.0` |
| `auth-a/class-x/%E3%80%80ledger-1/v1.2.0`（U+3000 表意空格） | `auth-a/class-x/ledger-1/v1.2.0` |

必须判定不等价：

1. `auth-a/class-x/ledger-1/v1.2.0` 与 `auth-a/class-x/ledger-1/v1.3.0`：契约版本不同。
2. `auth-a/class-x/ledger-1/v1.2.0` 与 `auth-a/class-x/ledger-2/v1.2.0`：Ledger identity 不同。

必须判定为 `INVALID` 并拒绝：

1. 段数不为四、存在空段或重复分隔符。
2. 任一段在第 3 步后为空，包括仅在 trim 掉解码所得空白或兼容分解所得空白后才变空的情形。
3. 版本段不符合 `vMAJOR.MINOR.PATCH`。
4. 存在不构成合法 `%HH` 三元组的 `%`。
5. 任一段解码所得字节不是合法 UTF-8。
6. 任一段解码后内容包含字面 `/`（编码后的分隔符注入），例如 `auth-a/class-x/led%2Fa/v1.2.0`。
7. 任一段规范化后含由兼容规范化产生的字面 `/`，例如 `auth-a/class-x/led／ger-1/v1.2.0`（U+FF0F 全角斜线）。

被拒绝的输入不得通过宽松解析转换为合法身份。

**5. 双高水位比较**

定义：

- `captured`：`CaptureProducerRegistrationHighWater` 实际捕获的 Producer Registration High Water。
- `installed`：`InstallForgetFence` 实际成功安装的 ForgetFence High Water。

两者必须分别取得，不得相互伪造或推导。

| 比较关系 | 判定 | 处理 |
|---|---|---|
| installed = captured | VALID | 允许通过 |
| installed > captured | VALID | 允许通过 |
| installed < captured | INVALID | 拒绝证明 |

补充约束：

1. 两个高水位必须采用非负整数十进制表达。
2. 非十进制表达、负数、非整数表达均判定为 `INVALID`。
3. 两个值必须分别对应其权威操作的实际结果。
4. 禁止由 `admission_high_water` 推导 captured 或 installed。
5. 禁止由 `owner_high_water` 推导 captured 或 installed。
6. 前导零必须被接受，且不得改变数值；比较必须基于数值进行，不得基于字符串形式进行。
7. 全部由零构成的表示必须视为数值零，零的 canonical 渲染为 `0`。
8. 高水位值的 canonical 十进制渲染不得包含前导零；将收到的值按 canonical 形式重新输出时，必须精确保留其数值。
9. 前导 `+` 或 `-` 号、首尾空白、千位分隔符、指数记法及小数部分均判定为 `INVALID`，不得被归一化为合法值。
10. 实现必须至少支持至 2^63 - 1 的数值。超出实现支持范围的值必须判定为 `INVALID`；禁止静默截断、回绕及浮点强制转换。
11. 不得以字段存在或数值可解析推定 Fence 已安装或当前有效。

**6. 当前性判定**

ForgetFence Currentness Proof 不采用显式 TTL，不设置时间有效期上限。

采用事件驱动失效与权威状态版本比对机制：

1. 每次 ForgetFence 状态发生影响有效性的变更，D 必须推进对应的单调递增状态版本。
2. Currentness Proof 必须携带签发时的 Fence 状态版本。
3. H 必须取得 D 权威当前状态版本。
4. 证明版本与当前版本一致，且 Fence 未撤销、未替换时，证明保持有效。
5. 证明版本与当前版本不一致时，证明判定为 `STALE`。
6. Fence 明确撤销时，证明判定为 `INVALID`。
7. Fence 被更新的 Fence 替换、且被替换的 Fence 未被明确撤销时，证明判定为 `STALE`，不得判定为 `INVALID`。
8. 无法取得权威当前状态版本时，判定为 `UNKNOWN`。
9. 禁止使用本地时钟、缓存时间或证明文件时间替代权威状态版本。
10. **并发校验边界。** 撤销/替换检查与状态版本比对必须针对同一次权威状态版本读取完成；禁止将其拆分到两次读取。
11. 证明必须在每次使用时对权威状态版本重新求值；禁止将 `VALID` 判定跨不同操作缓存复用。
12. 当状态版本在签发与验签之间推进时，验签结果必须反映实际读取到的版本；验签方不得为取得 `VALID` 而反复重读直至观察到匹配版本。

上述条款的边界：第 10–12 项是对验签方的行为义务。存储层字段名与事务机制（第 9 节第 4 项）、状态版本读取失败后的重试/缓存/恢复协议（第 9 节第 8 项）作为**机制**仍属未决。机制未决不得被解释为可以违反第 10–12 项；一致性按可观测属性判定，不按指定机制判定。

三态及有效状态定义：

- `VALID`：证明完整、绑定正确、版本匹配、安装有效且未撤销。
- `STALE`：证明曾经有效，但状态版本或 currentness 条件已经失效。
- `INVALID`：证明格式错误、必需字段缺失、明确绑定冲突、非法高水位或明确撤销。
- `UNKNOWN`：无法取得必要的权威状态或授权信息，尚不能确定有效性。

禁止事项：

1. UNKNOWN 不得按 VALID 处理。
2. STALE 不得作为当前操作的有效授权依据。
3. INVALID 不得通过宽松解析或字段替换恢复为 VALID。
4. 不得仅因证明文件存在就推定 currentness。
5. 当前性丧失、证明失效或降级为 `STALE`、`INVALID`、`UNKNOWN`，不得导致任何已执行的 fade 或 forget 操作被自动回滚、反向执行或重新执行。已执行 fade/forget 的效力独立于证明状态持续存在。
6. 已执行 fade/forget 操作的恢复、补偿与重放机制不属于本契约已定义内容，按第 9 节仍为未决项；未定义不得被解释为授权自动反向执行。

**7. 签发主体与密钥**

签发主体身份采用 Authority 与 Key 分离的结构：

- `issuer_authority_id`：必需，标识 D 授权的签发 Authority。
- `issuer_key_id`：必需，标识实际签发所使用的 Key。

规范要求：

1. 签发主体归属 Authority。
2. 实际签名密钥由独立 Key identity 标识。
3. Ledger identity 不得替代签发主体身份。
4. 一个 Authority 允许管理多个 Key，并允许密钥轮换。
5. 新 Key 生效不自动撤销旧 Key 已签发的证明。
6. 正常轮换后，旧 Key 合法签发的历史证明，在 Fence 状态版本仍 current 且旧 Key 未被追溯撤销时继续有效。
7. 旧 Key 正常退役不自动导致历史证明失效。
8. 旧 Key 因泄露或授权违规被撤销时，受撤销范围影响的证明判定为 INVALID。
9. 签发 Authority 自身的授权被撤销时，依赖该授权的全部证明必须判定为 `INVALID`。此判定独立于 Key 自身状态：即使 Key 本身未被泄露、未过期、也未曾被单独撤销，也不得在底层 Authority 授权被撤销后继续维持证明有效。
10. 不得由 Key 级撤销推定 Authority 级撤销，也不得由 Authority 级撤销推定 Key 级撤销。两类撤销范围必须分别跟踪、分别求值。
11. H 必须验证 Key 与 Authority 的授权归属及签发时有效性。
12. 不得仅凭 `issuer_key_id` 存在就接受证明。

签名算法、密钥注册表 schema、密钥撤销时间戳及历史撤销证明格式不属于本契约的已定义内容。

**8. 判定表**

| 输入状态 | 判定 | 处理 |
|---|---|---|
| 命名空间标识符缺失 | INVALID | 拒绝 |
| 命名空间标识符为空串 | INVALID | 拒绝 |
| 大小写不同但规范化后相同 | VALID | 规范化后比较 |
| 存在无法合法解码的转义 | INVALID | 拒绝 |
| 契约版本与要求不匹配 | STALE | 不接受当前身份 |
| Authority 明确绑定错误 | INVALID | 拒绝 |
| Ledger 已撤销 | INVALID | 拒绝 |
| Ledger 已确认退役 | INVALID | 拒绝 |
| Ledger 迁移但连续性无法确认 | UNKNOWN | 暂停接受 |
| Fence 状态版本与当前版本一致 | VALID | 继续验证其他约束 |
| Fence 状态版本不一致 | STALE | 重新取得证明 |
| Fence 明确撤销 | INVALID | 拒绝 |
| Fence 被更新 Fence 替换且未明确撤销 | STALE | 重新取得证明 |
| 权威状态版本无法取得 | UNKNOWN | 不得通过 |
| installed = captured | VALID | 允许 |
| installed > captured | VALID | 允许 |
| installed < captured | INVALID | 拒绝 |
| 高水位包含非十进制字符 | INVALID | 拒绝 |
| 高水位包含前导零 | VALID | 规范化后按数值比较 |
| 高水位超出支持范围 | INVALID | 拒绝 |
| 必需签发主体字段缺失 | INVALID | 拒绝 |
| 签发 Key 授权状态无法确认 | UNKNOWN | 不得通过 |
| 签发 Authority 授权已撤销 | INVALID | 按范围拒绝 |
| 旧 Key 正常轮换退役且证明仍 current | VALID | 继续接受 |
| 旧 Key 明确被追溯撤销 | INVALID | 拒绝 |

**9. 未决项（NOT_DECIDED）**

以下事项不属于本版本已经确定的规范：

1. 具体密码学签名算法、签名封装及验签实现。
2. 密钥注册表的物理及逻辑 schema。
3. 密钥撤销时间戳、撤销传播协议及历史证明追溯撤销范围的具体表示。
4. Fence 状态版本在存储层的字段名、事务机制及持久化方式。
5. Currentness Proof 的具体序列化 schema 和字段编码。
6. Unicode 规范化及 Case Folding 所采用的 Unicode 数据版本。
7. 命名空间迁移、历史身份继承及跨版本迁移协议。
8. 状态版本读取失败后的重试、缓存及恢复协议。
9. Fade/forget 已执行操作的审计保留、重放及补偿机制。
10. D、H 之间权威状态查询接口及其传输协议。

百分号编码字符集合（第 4 节）、高水位前导零策略（第 5 节）、Fence 替换的判定边界（第 6 节）及 Authority 级撤销范围（第 7 节）属于本版本已经确定的内容，不得被列为未决项，也不得交由实现方自行裁量。

未决项不得由实现自行推定为已经获得 D 契约授权。

**10. 一致性状态**

| 检查项目 | 状态 |
|---|---|
| IMPLEMENTATION | NOT_IMPLEMENTED |
| CONFORMANCE VECTORS | SPECIFIED_NOT_RUN |
| EXACT-HEAD CI | NOT_RUN |

本版本仅记录规范决定，不证明代码实现、组合 runtime 验证、CI 验证或生产环境一致性。

任何实现方在宣称符合本契约前，必须完成相应实现、精确版本验证及完整 conformance vectors 执行，并提供可核验的证据。
