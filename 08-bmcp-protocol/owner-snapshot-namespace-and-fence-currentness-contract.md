# Owner Snapshot Namespace and Fence Currentness Contract / 所有者快照命名空间与 Fence 当前性契约

- Contract version / 契约版本: **1.0.0 (CANDIDATE)**
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
- Version: 1.0.0 (CANDIDATE)
- Status: Decisions made, **implementation unverified**, **no consistency run executed**.
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
3. Its Ledger identity is migrated, replaced, or rebuilt such that the original identity no longer represents the current ledger.
4. Its original contract version is superseded by an incompatible version.
5. Its corresponding Ledger is revoked or retired.
6. Its canonical representation no longer conforms to the current specification.

`STALE` means that an identity may have been historically valid but is no longer current. `INVALID` means that the input itself violates identity or format constraints. These states MUST NOT be automatically converted into one another.

**NS-PR-05: Prohibition on interchangeability**

1. The ProducerWork Registration Ledger Namespace MUST NOT substitute for the ForgetFence namespace.
2. The ProducerWork Registration Ledger Namespace MUST NOT substitute for the I-side `inventory_epoch_ref`.
3. The composite-path field `producer_domain_inventory_epoch_ref` MUST NOT be treated as equivalent to `inventory_epoch_ref` without an explicit contractual mapping.
4. The ProducerWork Registration Ledger Namespace MUST NOT substitute for the canonical commit cursor.
5. The ProducerWork Registration Ledger Namespace MUST NOT substitute for generic `admission_high_water`.

**4. Canonicalization algorithm**

All namespace identifiers MUST be canonicalized in the following six steps, in exactly this order:

1. **Trim:** Remove leading and trailing Unicode White_Space from the entire input and each segment. Internal whitespace MUST NOT be automatically removed.
2. **Case:** Apply Unicode Default Case Folding to the first three segments. The fourth, version segment MUST NOT undergo case folding.
3. **Unicode normalization:** Apply NFC normalization to the first three segments.
4. **Delimiter handling:** Use ASCII `/` as the only segment delimiter. Exactly four segments are required. Empty segments and repeated delimiters are prohibited.
5. **Escaping:** Encode each segment using UTF-8. Non-unreserved bytes MUST use uppercase `%HH` percent encoding. Split segments first, then decode each segment exactly once. Double decoding and encoded delimiter injection are prohibited.
6. **Version segment handling:** The fourth segment MUST conform to `vMAJOR.MINOR.PATCH`. All three components MUST be non-negative decimal integers without leading zeros, except for the value zero itself.

Canonicalization MUST produce a unique and reproducible canonical representation.

Equivalent input examples:

| Input | Canonical |
|---|---|
| `AUTH-A/Class-X/Ledger-1/v1.2.0` | `auth-a/class-x/ledger-1/v1.2.0` |
| ` AUTH-A / CLASS-X / LEDGER-1 / v1.2.0 ` | `auth-a/class-x/ledger-1/v1.2.0` |
| `auth-a/class-x/ledger-1/v1.2.0` | `auth-a/class-x/ledger-1/v1.2.0` |

Inputs that MUST be considered non-equivalent:

1. `auth-a/class-x/ledger-1/v1.2.0` and `auth-a/class-x/ledger-1/v1.3.0`: different contract versions.
2. `auth-a/class-x/ledger-1/v1.2.0` and `auth-a/class-x/ledger-2/v1.2.0`: different Ledger identities.

Invalid segment counts, invalid version formats, empty segments, and inputs that cannot be legally decoded MUST be rejected. They MUST NOT be converted into valid identities through permissive parsing.

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
6. The existence of a field or the ability to parse a number MUST NOT establish that a Fence was installed or remains current.

**6. Currentness determination**

ForgetFence Currentness Proofs MUST NOT use explicit TTLs and MUST NOT have a time-based validity limit.

Currentness MUST use event-driven invalidation and authoritative state-version comparison.

1. Whenever a ForgetFence state change affects validity, D MUST advance the corresponding monotonically increasing state version.
2. A Currentness Proof MUST carry the Fence state version at issuance.
3. H MUST obtain the current authoritative state version from D.
4. The proof remains valid only when its version matches the current version and the Fence has not been revoked or replaced.
5. A mismatch between the proof version and current version MUST result in `STALE`.
6. An explicitly revoked Fence MUST result in `INVALID`.
7. Inability to obtain the authoritative current state version MUST result in `UNKNOWN`.
8. Local clocks, cache timestamps, and proof-file timestamps MUST NOT substitute for the authoritative state version.

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
9. H MUST verify the authorization relationship between the Key and Authority and the Key's validity at issuance.
10. The existence of an `issuer_key_id` alone MUST NOT be sufficient for acceptance.

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
| Ledger migrated but continuity cannot be confirmed | UNKNOWN | Suspend acceptance |
| Fence state version matches current version | VALID | Continue validating other constraints |
| Fence state version differs from current version | STALE | Obtain a new proof |
| Fence explicitly revoked | INVALID | Reject |
| Authoritative state version unavailable | UNKNOWN | MUST NOT pass |
| installed = captured | VALID | Accept |
| installed > captured | VALID | Accept |
| installed < captured | INVALID | Reject |
| High-water value contains non-decimal characters | INVALID | Reject |
| Mandatory issuer identity field missing | INVALID | Reject |
| Issuer Key authorization cannot be confirmed | UNKNOWN | MUST NOT pass |
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
8. The complete character whitelist and reserved-character set for percent encoding.
9. Input compatibility and raw-input rejection policies for leading zeros in high-water values.
10. Retry, caching, and recovery protocols when state-version retrieval fails.
11. Audit retention, replay, and compensation mechanisms for already executed fade/forget operations.
12. The authoritative state-query interface and transport protocol between D and H.

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
- 版本：1.0.0（CANDIDATE）
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
3. Ledger identity 迁移、替换或重建，导致原身份不再代表当前账本。
4. 原契约版本被不兼容的新版本取代。
5. 对应 Ledger 被撤销或退役。
6. 命名空间的 canonical representation 不再符合当前规范。

`STALE` 表示历史上可能有效、但当前性已经失效；`INVALID` 表示输入本身违反身份或格式约束。两者不得自动互相转换。

**NS-PR-05：禁止混用**

1. ProducerWork Registration Ledger Namespace 不可替代 ForgetFence namespace。
2. ProducerWork Registration Ledger Namespace 不可替代 I 侧 `inventory_epoch_ref`。
3. 组合路径中的 `producer_domain_inventory_epoch_ref` 不得未经明确契约映射就视为 `inventory_epoch_ref`。
4. ProducerWork Registration Ledger Namespace 不可替代 canonical commit cursor。
5. ProducerWork Registration Ledger Namespace 不可替代通用 `admission_high_water`。

**4. Canonicalization 算法**

所有命名空间标识符必须按以下六步顺序规范化：

1. **Trim**：移除整个输入及各段首尾 Unicode White_Space；内部空白不自动删除。
2. **大小写**：对前三段执行 Unicode Default Case Folding；第四段版本段不执行大小写折叠。
3. **Unicode 规范化**：对前三段执行 NFC 规范化。
4. **分隔符处理**：使用 ASCII `/` 作为唯一段分隔符；必须恰好四段，禁止空段及重复分隔符。
5. **转义**：各段采用 UTF-8 编码，非 unreserved 字节使用大写 `%HH` 百分号编码。先拆段后分段解码一次，禁止二次解码，禁止编码后的分隔符注入。
6. **版本段处理**：第四段必须符合 `vMAJOR.MINOR.PATCH` 格式，三个部分均为非负十进制整数，不允许前导零，数字零本身除外。

Canonicalization 必须产生唯一、可重复的 canonical representation。

等价输入示例：

| 输入 | Canonical |
|---|---|
| `AUTH-A/Class-X/Ledger-1/v1.2.0` | `auth-a/class-x/ledger-1/v1.2.0` |
| ` AUTH-A / CLASS-X / LEDGER-1 / v1.2.0 ` | `auth-a/class-x/ledger-1/v1.2.0` |
| `auth-a/class-x/ledger-1/v1.2.0` | `auth-a/class-x/ledger-1/v1.2.0` |

必须判定不等价：

1. `auth-a/class-x/ledger-1/v1.2.0` 与 `auth-a/class-x/ledger-1/v1.3.0`：契约版本不同。
2. `auth-a/class-x/ledger-1/v1.2.0` 与 `auth-a/class-x/ledger-2/v1.2.0`：Ledger identity 不同。

非法段数、非法版本格式、空段及无法合法解码的输入必须拒绝，不得通过宽松解析转换为合法身份。

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
6. 不得以字段存在或数值可解析推定 Fence 已安装或当前有效。

**6. 当前性判定**

ForgetFence Currentness Proof 不采用显式 TTL，不设置时间有效期上限。

采用事件驱动失效与权威状态版本比对机制：

1. 每次 ForgetFence 状态发生影响有效性的变更，D 必须推进对应的单调递增状态版本。
2. Currentness Proof 必须携带签发时的 Fence 状态版本。
3. H 必须取得 D 权威当前状态版本。
4. 证明版本与当前版本一致，且 Fence 未撤销、未替换时，证明保持有效。
5. 证明版本与当前版本不一致时，证明判定为 `STALE`。
6. Fence 明确撤销时，证明判定为 `INVALID`。
7. 无法取得权威当前状态版本时，判定为 `UNKNOWN`。
8. 禁止使用本地时钟、缓存时间或证明文件时间替代权威状态版本。

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
9. H 必须验证 Key 与 Authority 的授权归属及签发时有效性。
10. 不得仅凭 `issuer_key_id` 存在就接受证明。

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
| Ledger 迁移但连续性无法确认 | UNKNOWN | 暂停接受 |
| Fence 状态版本与当前版本一致 | VALID | 继续验证其他约束 |
| Fence 状态版本不一致 | STALE | 重新取得证明 |
| Fence 明确撤销 | INVALID | 拒绝 |
| 权威状态版本无法取得 | UNKNOWN | 不得通过 |
| installed = captured | VALID | 允许 |
| installed > captured | VALID | 允许 |
| installed < captured | INVALID | 拒绝 |
| 高水位包含非十进制字符 | INVALID | 拒绝 |
| 必需签发主体字段缺失 | INVALID | 拒绝 |
| 签发 Key 授权状态无法确认 | UNKNOWN | 不得通过 |
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
8. 百分号编码所允许的完整字符白名单及保留字符集合。
9. 高水位前导零的输入兼容策略及原始输入拒绝策略。
10. 状态版本读取失败后的重试、缓存及恢复协议。
11. Fade/forget 已执行操作的审计保留、重放及补偿机制。
12. D、H 之间权威状态查询接口及其传输协议。

未决项不得由实现自行推定为已经获得 D 契约授权。

**10. 一致性状态**

| 检查项目 | 状态 |
|---|---|
| IMPLEMENTATION | NOT_IMPLEMENTED |
| CONFORMANCE VECTORS | SPECIFIED_NOT_RUN |
| EXACT-HEAD CI | NOT_RUN |

本版本仅记录规范决定，不证明代码实现、组合 runtime 验证、CI 验证或生产环境一致性。

任何实现方在宣称符合本契约前，必须完成相应实现、精确版本验证及完整 conformance vectors 执行，并提供可核验的证据。
