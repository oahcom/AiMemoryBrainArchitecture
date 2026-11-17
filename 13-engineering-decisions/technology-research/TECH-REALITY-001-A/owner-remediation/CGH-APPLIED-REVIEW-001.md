# CGH-APPLIED-REVIEW-001 — Exact C/G/H Applied Evidence Consumer Review
# C/G/H Applied 证据消费者精确审查

- Date: 2026-11-18
- Repository: \`oahcom/AiMemoryBrainArchitecture\`
- Review baseline: \`main@a2b8babb1cacfcfbcd590b147bdf34ce162944c2\`
- Review branch heads: C \`session-c-agent-integration-2026-11-16@a9a587e9f73266c74c84c65fda1beeb4246f5a80\`; G \`session-g-memory-context@ed6ad0b316b721e49d2fe560ae9f7e6c647ca661\`; H \`session-h-bmcp-protocol@6608cde89d959257db612d8ff8080f631333f3f3\`.
- Mode: delegated C/G/H technical-role review and exact repository-source inspection; **not independent human Owner signatures**.
- Disposition: **REQUEST CHANGES / CANDIDATE ONLY / APPLIED FREEZE BLOCKED**.
- This review is a non-normative integration audit. It does not amend C, G, H, I or D authority contracts.

## 1. Executive decision

The C/G/H Applied evidence path is **not ready for shared wire freeze or Full Applied activation**.

The review found substantive progress:
- C has a normative final-request evidence contract and immutable CSubmitOutcome 1.0.1 schema.
- G has a detailed Applied identity, evidence revision, persistence, recovery and current-use contract.
- H has a separate Applied Delivery Evidence 1.0.0 message family, schema, reference validator, tests and bounded CI.
- H correctly keeps Applied Delivery Evidence separate from Unified 1.2.15 C Provider Outcome Gateway Attestation and from the JF-10 Applied ACK schema family.

But three P0 defects/gaps remain in H's Applied Delivery Evidence candidate, and G's consumer contract/persistence acceptance is not yet updated to the new exact H family:
1. Duplicate JSON object keys are not rejected before parsing.
2. Same-digest replay can return the prior result reference without the current I authorization/PermissionEpoch, audience/scope and applicable D fence recheck required by I.
3. CSubmitOutcome 1.0.1 reference/identity/equality is delegated to a callback but not normatively resolved or exercised against a real C fixture; C's review explicitly says the mapping is not accepted/verified.
4. G's Phase 3.8.22 contract pins H Unified 1.2.15 while the newer H Applied Delivery Evidence 1.0.0 is a separate family. The G contract has not been revised to consume that exact schema/validator and preserve the three identity domains.
5. G's durable Applied ledger, unique identity enforcement, crash/restart/restore and multi-replica idempotency remain specified, not implemented or run.

**Disposition:** keep all H Applied Delivery Evidence 1.0.0, C/G/H consumer integration, and Full Applied activation as candidate/open. Do not treat H's 11-test CI as proof of C/G/I semantic joins or production trust. Do not treat G's normative draft as implemented persistence.

## 2. Exact artifacts and evidence pins

| Authority | Artifact | Exact Blob / branch evidence | Status and scope |
|---|---|---|---|
| C | Phase 3.6 Final Request Evidence (EN source) | \`fd2f47ba6c89bb270e9f2bec956873cb7ae3592b\` | C producer semantics; evidence only when actual final immutable request crosses observed submit boundary |
| C | CSubmitOutcome 1.0.1 schema | \`a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda\` | Immutable C-owned provider outcome shape; semantic truth remains C-owned |
| C | Phase 3.8.23 C/G Applied identity review | \`4860c627b4d7e84e23fb39ad83411674f3b88c7b\` | Accepts C identity semantics for exact G Phase 3.8.22 with exceptions; does not accept H wire mapping or G persistence implementation |
| C | Phase 3.8.27 H gateway ordering review | \`3ca06dbfd7d59483e9604b7a68df924c719f60aa\` | Accepts C-before-H-signing order for Unified 1.2.15 Gateway Attestation path; **not** approval of H Applied Delivery Evidence 1.0.0 |
| C | C review of H Applied Delivery Evidence | \`3300d95b3074a7bf6690718e0ab7f6cbd9afb9ae\` | H identity shape candidate accepted; C outcome mapping not accepted/verified |
| G | Phase 3.8.22 Applied persistence contract | \`bd297873bc1e593280484a43cb44b56058d9c4ff\` | G normative design draft; implementation not verified; exact H consumer mapping and COC/Storage acceptance still required |
| H | Applied Delivery Evidence 1.0.0 schema | \`2ce8776ca5ee5e014b234dc3eb34a7cb7961e608\` | Separate H evidence message family; includes HDeliveryBindingIdentity and HObservationRecordIdentity |
| H | Applied Delivery Evidence reference validator | \`2f6de24eea737cf75a16ead7495bea4627bb1bb4\` | Test/conformance reference only; injected authority callbacks |
| H | Applied Delivery Evidence tests | \`bb2bb6c94cc73293f736c6dcd450ab32bffc6ee5\` | 11 deterministic tests; callbacks are test doubles |
| H | Phase 3.8.24 candidate contract | \`f193113f142506b0d0848c7131f780db93a83aef\` | Explicitly not production cryptographic or durable replay service |
| H | A exact review H-ADE-006 | \`44f79fc037a3aa15d171781fecf5a924e10a0388\` | DEFERRED; H-ADE-001..003 remain open |
| I | Phase 3.8.23 replay/current-authorization review | \`85cdbad04ae4b688338cdf2b667c21d2f02d8b96\` | Requires current authorization recheck before SAME_DIGEST_REPLAY result reference disclosure |
| Cross-owner | C/G/H Applied field-level review | \`e6d8155973137eefd469619357e8135de227e3a0\` | Semantic alignment partial; ACK identity and wire freeze blocked |
| Cross-owner | C/G/H provider-outcome successor review | \`db32ce41609b53f096269b4b5b3456c3bec216b6\` | Distinguishes Provider Outcome, Applied ACK and Applied Delivery Evidence; 1.2.15 G acceptance not implied |

## 3. Findings

### CGH-P0-001 — H parser accepts duplicate JSON object keys

**Evidence**
- H validator Blob: \`2f6de24eea737cf75a16ead7495bea4627bb1bb4\`.
- Its ingress path calls \`json.loads(raw_envelope.decode("utf-8"))\` directly.
- Python's default JSON decoder accepts duplicate object names and keeps the last value. The resulting object is then passed to JSON Schema validation and P0 construction.
- \`additionalProperties: false\` cannot detect the discarded duplicate because it is no longer present in the materialized object.
- H-ADE-006 independently records this as H-ADE-001 and notes that the 11-test suite has no duplicate-key negative vectors.

**Risk / disposition:** P0 for authenticated signed evidence. Different parsers or signature verifiers can interpret the same raw bytes differently; duplicate identity, digest, signature or authority fields can be hidden by parser collapse.

**Required H remediation**
1. Parse with a duplicate-key-rejecting object-pairs hook before schema validation or P0 construction.
2. Reject duplicates at every nesting depth, not only top-level.
3. Add negative vectors for duplicate identity, payload digest, signature, issuer/authority, and nested fields.
4. Bind signature verification to the exact accepted raw-byte/canonicalization profile.
5. Run the updated suite and workflow against the exact current H code HEAD; publish parser/test/workflow Blob pins.

**Acceptance evidence:** parser source, all duplicate-key tests, exact-head CI, independent readback. Until then no production acceptance of this message family.

### CGH-P0-002 — SAME_DIGEST_REPLAY discloses original result without current authorization recheck

**Evidence**
- H validator Blob \`2f6de24eea737cf75a16ead7495bea4627bb1bb4\` returns \`VALID_REPLAY\` and \`original_result_ref\` immediately after the injected \`commit_observation\` callback reports \`SAME_DIGEST_REPLAY\`.
- \`AppliedDeliveryChecks\` has no current-I-authorization, PermissionEpoch, audience/scope or D Forget-fence recheck callback.
- I Phase 3.8.23 Blob \`85cdbad04ae4b688338cdf2b667c21d2f02d8b96\` explicitly requires reading the original durable result and rechecking current I authorization/PermissionEpoch, key status, audience/scope and applicable D Forget fence before returning SAME_DIGEST_REPLAY; it forbids disclosure to revoked/stale callers.
- Existing H tests exercise a replay callback stub; they do not exercise revoked/stale current authorization.

**Risk / disposition:** P0 information-disclosure and stale-authority risk. A valid historical signed observation is not perpetual authorization to retrieve its result reference.

**Required H/I/D remediation**
1. Add an explicit tri-state current-authority check before any original result reference is returned.
2. Recheck current I PermissionEpoch/decision, key status, audience and scope; apply the D fence check at the correct owner-defined decision boundary.
3. On unavailable I/D state return UNKNOWN and disclose no result reference.
4. Add negative tests for revoked permission, stale epoch, changed audience/scope, revoked key and unavailable I/D authority.
5. Define whether the recheck occurs before or after durable replay lookup, while ensuring no result reference escapes before it passes.

**Acceptance evidence:** callback/API contract, tests with negative vectors, durable replay implementation evidence, exact I/H/D review. Do not treat a valid signature or same digest as current authorization.

### CGH-P0-003 — CSubmitOutcome 1.0.1 immutable record join is not implemented/proven

**Evidence**
- H schema Blob \`2ce8776ca5ee5e014b234dc3eb34a7cb7961e608\` carries \`c_submit_outcome_ref\`, \`c_outcome_record_ref\`, \`c_outcome_record_sequence\`, \`c_outcome_payload_digest\`, and \`final_request_boundary_id\`.
- C schema Blob \`a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda\` defines a C-owned immutable record identity including \`issuer_authority_ref\`, \`sequence_namespace_ref\`, \`record_ref\`, and \`record_sequence\`, plus \`Outcome\`, \`SideEffectStatus\`, \`FinalRequestBoundaryRef\`, \`RequestDigest\`, \`ActualInferenceRequestId\` and provider-attempt lineage.
- H validator exposes \`verify_c_final_boundary\` as an injected callback; it does not define a normative immutable C record resolver or itself enforce the exact C identity/equality joins.
- H's 11-test positive fixture sets all callbacks to \`True\`; no test loads C's actual 1.0.1 fixture and mutates each duplicated C field.
- C review Blob \`3300d95b3074a7bf6690718e0ab7f6cbd9afb9ae\` explicitly says C outcome mapping is not accepted/verified and requests a normative \`c_submit_outcome_ref\` resolution contract or explicit C issuer/sequence namespace, exact equality checks and cross-schema vectors.

**Risk / disposition:** P0 for Full Applied. An H envelope must not imply a successful provider handoff or bind an arbitrary C display/reference string to a different immutable C outcome record.

**Required C/H/G remediation**
1. Define \`c_submit_outcome_ref\` as a resolvable, authenticated immutable CSubmitOutcome 1.0.1 record reference, or add the missing C issuer/sequence namespace fields.
2. Resolve and authenticate the full \`COutcomeRecordIdentity\`; do not substitute H issuer/signing namespace.
3. Enforce exact equality of record ref, record sequence, payload digest, final request boundary, actual inference request ID and request digest where applicable.
4. Consume C-owned \`Outcome\`/side-effect semantics from C authority; only determinate \`HANDOFF_ACCEPTED\` with \`PROVEN_OCCURRED\` and required provider/participant evidence can qualify for Full Applied evaluation.
5. Add positive and negative cross-schema fixtures for each equality field, UNKNOWN/unavailable resolver, successor observation and changed-digest conflict.
6. Obtain exact C and G review of the new H schema/validator/test pins.

### CGH-P1-004 — G's consumer pin does not yet consume the separate H Applied Delivery Evidence 1.0.0 family

**Evidence**
- G Phase 3.8.22 Blob \`bd297873bc1e593280484a43cb44b56058d9c4ff\` pins H Unified 1.2.15 and describes that schema's missing HDeliveryBindingIdentity members.
- H Applied Delivery Evidence 1.0.0 is a distinct message family with its own schema Blob \`2ce8776...\`; it includes all seven HDeliveryBindingIdentity members and the seven HObservationRecordIdentity members.
- H Phase 3.8.24 explicitly says this new family does not modify Unified 1.2.15 C Provider Outcome P0.
- A-H-ADE-006 says H identity shape exists as a candidate, but C/G/I acceptance and production boundaries remain open.

**Risk / disposition:** P1 integration drift. The newer H evidence family is not accepted by implication through G's earlier Unified 1.2.15 review. G's old statement about missing properties may be accurate for Unified 1.2.15 but must not be read as a statement about the separate H 1.0.0 family.

**Required G/H/C remediation**
1. Publish a G successor consumer addendum pinning the exact H Applied Delivery Evidence 1.0.0 schema and validator.
2. Preserve the three separate identity domains: HDeliveryBindingIdentity, HEvidenceIdentity and HObservationRecordIdentity; map G Applied idempotency identity separately.
3. Define the authenticated C outcome resolver join and exact G acceptance predicate.
4. Obtain exact C/H/G decisions on the same schema/validator/test Blob set. Do not inherit approval from Unified 1.2.15 or JF-10 Applied ACK 1.1.0.

### CGH-P0-005 — G durable Applied persistence and restore conformance remains specified, not implemented

**Evidence**
- G Phase 3.8.22 Blob \`bd297873bc1e593280484a43cb44b56058d9c4ff\` labels itself G-owned normative design draft; implementation not verified.
- §9 requires a machine-readable Applied record with stable identity, evidence revision, C/H/COC/I/D/Storage proof refs, G ledger sequence/high-water, restore epoch and current-use invalidation projection.
- §10 enumerates G-AP-P01..P18 but explicitly marks conformance obligations SPECIFIED / NOT RUN and requires durable DB crash injection, restart, multi-replica duplicate submissions, stale checkpoint restore and owner high-water regression tests.
- The merged PR #114 contains only the two standalone in-memory reference models; it does not add G production persistence, schema, unique indexes, database adapter or restore tests.

**Risk / disposition:** P0 for production Full Applied. A detailed state model does not provide durable exactly-once local Applied decision semantics or restore fencing.

**Required G remediation**
1. Generate and pin the machine-readable G Applied schema/SDK mapping.
2. Define the stable logical identity key and database uniqueness/transaction boundary; same identity+same digest returns original receipt, changed digest conflicts/quarantines.
3. Implement durable evidence revision and immutable Applied ledger commit.
4. Add database crash/restart and multi-replica concurrency tests, including duplicate request, crash during commit, stale restore snapshot, high-water regression and old D/I authority snapshot.
5. Revalidate current-use before protected use and final request submission; preserve historical Applied as an audit fact while separately invalidating current use.
6. Obtain exact G Owner acceptance and cross-owner C/H/COC/I/D/Storage review.

## 4. What is accepted, and what is not

| Area | Current evidence | Disposition |
|---|---|---|
| C final-request stage semantics | C Phase 3.6 source | Specified; no production boundary proof |
| CSubmitOutcome 1.0.1 object structure | C schema + C bounded tests | Candidate structure; C remains sole provider-truth authority |
| C/G identity semantics | C Phase 3.8.23 exact review of G Phase 3.8.22 | ACCEPT WITH ENUMERATED EXCEPTIONS for the reviewed C/G identity scope only |
| C-before-H-signing gateway order | C Phase 3.8.27 | Accepted as reference order for Unified 1.2.15 gateway path only |
| H Applied Delivery Evidence 1.0.0 schema shape | H schema + H 11-test CI | Candidate conformance evidence; A review DEFERRED |
| H C outcome mapping | C-REVIEW-001 | NOT ACCEPTED / NOT VERIFIED |
| H replay current authorization | I Phase 3.8.23 + A-H-ADE-006 | OPEN / P0 |
| G H-1.0.0 consumer pin | No exact G successor decision found in reviewed sources | OPEN |
| G Applied durable persistence/restore | G Phase 3.8.22 design draft | SPECIFIED / NOT RUN / NOT IMPLEMENTED |
| Full C/G/H Applied | No end-to-end evidence | NOT PROVEN / NOT FROZEN |

## 5. Required closure sequence

1. **H:** fix duplicate-key parsing and replay current-authorization disclosure; add negative vectors.
2. **H + C:** publish immutable CSubmitOutcome resolver/equality contract and cross-schema fixtures.
3. **G:** publish exact H 1.0.0 consumer successor decision and generated Applied identity/persistence mapping.
4. **G + Storage/COC:** implement durable Applied ledger and same-GID/restore joins; run required crash/concurrency/restore tests.
5. **C/G/H/I/D:** exact-review the same artifact pins; preserve owner-specific authority and tri-state UNKNOWN behavior.
6. **Independent reviewer:** re-read the exact final branch heads and all evidence pins; do not self-approve.

Until all applicable items close: Full Applied remains blocked, current-use remains fail-closed on UNKNOWN, and no global Applied freeze or production activation is authorized.

## 6. 中文结论与整改要求

C/G/H Applied 证据链目前**不能进入共同 Wire Freeze，也不能启用 Full Applied**。

已取得的进展包括：C 的 Final Request Evidence 与 CSubmitOutcome 1.0.1；G 的 Applied 身份、证据版本、持久化和恢复设计；H 独立的 Applied Delivery Evidence 1.0.0 Schema、参考 Validator、测试和有限 CI。H 正确地将该消息族与 Unified 1.2.15 Provider Outcome Gateway Attestation、JF-10 Applied ACK 分开。

但仍有五项阻塞：

1. **P0：H JSON Parser 未拒绝重复对象键。** 默认 \`json.loads\` 会折叠重复键，Schema 无法再发现被覆盖字段。必须在解析阶段拒绝所有层级重复键，并补齐身份、Digest、Signature、Authority 等负向测试。
2. **P0：H SAME_DIGEST_REPLAY 返回原结果引用前没有当前授权复核。** I 要求重查 PermissionEpoch、当前授权、Key Status、Audience/Scope 和适用 D Forget Fence。任一权威不可用时必须 UNKNOWN，不能披露 Result Ref。
3. **P0：CSubmitOutcome 1.0.1 精确关联尚未实现/证明。** H 当前仅注入 \`verify_c_final_boundary\` 回调，测试把所有回调设为 True；没有真实 C Fixture 的跨 Schema 精确相等验证。C 已明确表示映射 NOT ACCEPTED / NOT VERIFIED。
4. **P1：G 尚未对独立 H Applied Delivery Evidence 1.0.0 建立精确消费者版本决议。** G 现有 Phase 3.8.22 仍引用 Unified 1.2.15。不能把旧消息族的审查自动继承给新消息族。
5. **P0：G Applied Durable Persistence/Restore 仍是设计，不是实现。** G-AP-P01..P18 标记 SPECIFIED / NOT RUN；尚无生成 Schema/SDK、唯一索引、数据库事务、崩溃恢复、多副本并发和旧快照恢复证明。

**明确接受范围：**
- C 对 G Phase 3.8.22 的 C/G 身份语义：带枚举例外接受；
- C 对 Unified 1.2.15 Gateway 的 C-before-H-signing 顺序：作为参考顺序接受；
- H 1.0.0 Schema/Validator：候选级测试证据；
- H C Outcome Mapping：未接受/未验证；
- G H-1.0.0 消费者 Pin：开放；
- G Durable Applied Persistence：未实现/未验证；
- Full C/G/H Applied：未证明、未冻结。

**整改顺序：** H 修复重复键和 Replay Disclosure；H/C 固化 C Outcome Resolver 与跨 Schema 测试；G 发布 H 1.0.0 精确消费者决议及持久化映射；G/Storage/COC 完成数据库持久化、同 GID 与恢复测试；C/G/H/I/D 对同一组精确 Blob 进行审查；最后由独立审查者核验最终 Head。

在全部关闭之前，Full Applied 保持阻塞；UNKNOWN 时必须 fail-closed；不得宣布全局 Applied Freeze 或生产激活。
