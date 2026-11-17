# Session 1 — R: Principal System-wide Architecture Risk Assessment
# 会话 1 — R：首席全系统架构风险评估

- Review ID: R-SWRA-001
- Repository: oahcom/AiMemoryBrainArchitecture
- Review date: 2026-11-17 (Asia/Singapore)
- Role: R — Principal System-wide Architecture Risk Assessment
- Tracking issue: #43 — ARCH-CONSOL-001
- Review branch: review/r-principal-system-wide-risk-2026-11-17
- Parent integration snapshot: review/arch-consol-001-system-wide-2026-11-17 @ d7a3379fd51660912200a6131bcd037c0f53583c
- Main snapshot read: main @ b372b62c640a2b656e54b6db62a4ee67d7d8c001
- Status: PRELIMINARY RISK DISPOSITION — NOT READY FOR ARCHITECTURE FREEZE
- Normative languages: English and Chinese are semantic peers.
- Authority boundary: This is an independent system-wide risk assessment. It does not approve, replace, or reinterpret Owner decisions.

---

## 1. Executive disposition / 总体结论

**EN — NOT READY.** The architecture has a coherent high-level separation of Brain, Agent, canonical memory, projections, context, protocol, authorization and storage responsibilities. The principal risk is not that these boundaries are inherently wrong. It is that several correctness guarantees depend on cross-authority ordering, physical serialization, closed-world inventory and recovery evidence that are still candidates, blocked decisions or unproven compositions.

The most fundamental blocker is the absence of a selected and fully specified physical serialization topology for the D ForgetFence / producer-admission / Storage final-visibility boundary. A logically correct protocol is not enough: its decisive operations must share one real linearization mechanism, and the protected read path must honor that same authority. The second major blocker is the absence of an integrated, adversarially verified state machine across D, E, I, Storage and COC. Forget/restore anti-resurrection, Fact/Claim semantics, identity/governance, Applied/provider evidence and production trust are additional high-impact dependencies.

The assessment is **NOT READY FOR ARCHITECTURE FREEZE**. This does not mean the architecture is impossible. It means the current evidence does not justify declaring the whole system correct, composable or production-deployable. A candidate schema, owner-role simulation, passing schema/reference test or engine-capability probe is not an end-to-end proof.

**中文 — 暂不具备冻结条件。** 当前架构已经形成较清晰的高层边界，区分了 Brain、Agent、Canonical Memory、投影、Context、协议、授权和 Storage 职责。主要风险并不是这些边界本身必然错误，而是多个正确性保证依赖跨权威排序、物理序列化、封闭世界清单和恢复证据；这些事项仍有候选方案、阻塞决策或未证明的组合。

最根本的阻塞，是 D ForgetFence / Producer Admission / Storage 最终可见性边界尚无已选定且完整定义的物理序列化拓扑。逻辑协议正确还不够：决定性操作必须共享真实的线性化机制，受保护读路径也必须服从同一权威。第二个重大阻塞，是 D、E、I、Storage 与 COC 尚无完整且经过对抗性验证的集成状态机。Forget/Restore 防复活、Fact/Claim 语义、身份治理、Applied/Provider 证据和生产信任仍是其他高影响依赖。

本次结论为 **NOT READY FOR ARCHITECTURE FREEZE（不具备架构冻结条件）**。这不代表架构不可行，而是现有证据不足以宣称整个系统正确、可组合或可生产部署。候选 Schema、角色模拟、通过的 Schema/参考模型测试或数据库能力探针，都不能替代端到端证明。

### 1.1 Evidence vocabulary / 证据状态词汇

- **VERIFIED / 已核实：** The exact repository fact, artifact identity, issue state or bounded test result was directly read from GitHub in this review. This does not mean the architecture guarantee itself is proven.
- **PARTIALLY VERIFIED / 部分核实：** A bounded part of the claim has evidence, but material assumptions, integrations or operational conditions remain unproven.
- **NOT PROVEN / 尚未证明：** No sufficient evidence was found to establish the claimed system property.
- **BLOCKED / 阻塞：** An explicit unresolved decision, approval or prerequisite prevents acceptance.

风险概率为定性评估，不是统计频率或故障率。Probability is based on the explicit open/blocking state, number of dependent authorities and known unverified transitions. Severity describes the consequence if the failure occurs. Risk Level is Critical where a plausible failure can invalidate canonical correctness, authorization, publication visibility or Forget safety; High where it can block major workflows or production acceptance; Medium/Low are used only for bounded and recoverable effects.

### 1.2 Rating method / 评级方法

| Probability / 概率 | Basis / 依据 |
|---|---|
| High / 高 | The trigger is already present as an explicit blocker, missing decision, incompatible pin or unproven mandatory transition. |
| Medium / 中 | The risk depends on a future scale, topology or integration condition, but current architecture does not yet constrain it sufficiently. |
| Low / 低 | The trigger is remote and bounded by existing controls; no such rating is used to minimize current P0/P1 blockers. |

| Impact / 影响 | Meaning / 含义 |
|---|---|
| Critical / 致命 | Can invalidate system correctness, expose forbidden data, resurrect forgotten data, duplicate external side effects or make canonical state indeterminate. |
| High / 高 | Can prevent a core workflow, cross-owner acceptance, recoverability or production operation. |
| Medium / 中 | Material but bounded degradation, with a known containment path. |
| Low / 低 | Local and readily recoverable effect. |

---

## 2. System-wide Risk Register / 全系统风险登记册

### RSK-01 — No selected physical linearization topology for canonical publication / 权威发布缺少已选定的物理线性化拓扑

- **Probability / 概率:** High / 高 — the Storage topology ADR explicitly remains ADR-BLOCKED and says no deployed topology is selected.
- **Impact / Severity / 影响严重度:** Critical / 致命 — a non-linearizable fence/visibility boundary can publish an artifact after ForgetFence wins, or leave the canonical outcome ambiguous.
- **Risk Level / 风险等级:** **CRITICAL**
- **Description / 描述:** D requires ProducerWork registration, dependency completeness, PublicationParticipant admission and ForgetFence installation to have one authoritative order. Storage requires the final visibility pointer, receipt, outcome and outbox to commit atomically. The logical contract does not identify a selected physical substrate that proves the D fence decision and Storage visibility commit share a single linearization point.
- **Affected Components / 影响组件:** B, D, E, I, Storage, F/G read paths, COC where recovery evidence is consumed.
- **Root Cause / 根本原因:** Semantic ownership and physical transaction ownership are correctly separated, but the shared physical serialization mechanism is still a candidate. Option A (one serializable transaction domain per Canonical Memory authority) and Option B (separate services plus durable linearizable coordinator) remain alternatives. Option C check-then-write is rejected.
- **Trigger Conditions / 触发条件:** D and Storage are deployed separately; a stale replica/cache is used; the D fence changes between check and commit; an ACK is lost; a process/primary fails between durable steps; or a visibility reader bypasses the authoritative pointer.
- **Failure Consequences / 失败后果:** A forgotten or unauthorized derivative may become visible; a barrier may close while publication remains possible; pointer/receipt/outcome may disagree; recovery may be unable to determine whether publication occurred.
- **Mitigation Strategy / 缓解策略:** Storage and D must jointly select and specify Option A or B. Define transaction/lock/consensus boundaries, exact row ownership, read authority, participant tuple, idempotency, stale replica/cache exclusion, failure recovery and anti-rollback. Keep COC and I's PolicyDomain sequencer as separately typed authorities unless an explicit ADR proves otherwise.
- **Required Architecture Decision / 必需架构决策:** Storage topology ADR, with explicit D and I acceptance and A integration disposition. A preference is not a decision.
- **Responsible Owner / 责任 Owner:** Storage (physical substrate), D (ForgetFence semantics), I (authorization proof), A (integration gate); no one Owner may decide for the others.
- **Verification Evidence / 验证证据:** Storage branch HEAD 17be31915b06d98d7f822e6e5270b8cde39eb0bb; topology ADR Blob 1ef47d4e5711c7db73a24d249adf1992be1f6aa4; visibility contract Blob 175ee7b1349cfdb79a19898b311a88391ed88010; Issue #10 and #25. ADR states T1–T8 OPEN and NO DEPLOYED TOPOLOGY SELECTED.
- **Evidence Status / 证据状态:** **BLOCKED** for topology decision; **NOT PROVEN** for system linearizability.
- **Residual Risk / 剩余风险:** Even after an ADR, actual database, replica, cache, restore and operator behavior can diverge from the model; physical fault evidence is still required.
- **Blocking Gate / 阻塞门禁:** Issue #43 G4 and G5; architecture freeze must remain blocked.
- **Source References / 来源:** Storage topology ADR; Storage visibility contract; D ForgetFence contract; Issues #10, #25, #43.

### RSK-02 — Cross-owner publication state machine lacks integrated adversarial proof / 跨 Owner 发布状态机缺少集成对抗性证明

- **Probability / 概率:** High / 高 — the contracts describe the sequence, but the current evidence does not prove every cross-owner ordering and crash window as one model.
- **Impact / Severity / 影响严重度:** Critical / 致命 — incompatible local terminal states can produce visible data without all required predicates or leave barriers permanently unresolved.
- **Risk Level / 风险等级:** **CRITICAL**
- **Description / 描述:** The proposed order is Storage PREPARE hidden → D PublicationParticipant admission → I single-use authorization consumption → Storage final visibility commit → independent D/I closeout. Each participant has its own ledger, identity, receipt and terminal state. A complete end-to-end proof must show both serial orders for every race and crash/ACK-loss behavior across the entire tuple.
- **Affected Components / 影响组件:** D, E, I, Storage, H, COC, F, G, A.
- **Root Cause / 根本原因:** Owner-local contracts and bounded reference suites do not by themselves prove their composition. The integration proof must model all durable boundaries, independent authorities, retries, stale leases, unknown states and read visibility.
- **Trigger Conditions / 触发条件:** Crash after hidden prepare; D admission ACK loss; I COMMIT_WON versus revocation; Storage commit ACK loss; participant row missing; stale lease; duplicate request with changed digest; delayed outbox; restore while participants remain unresolved.
- **Failure Consequences / 失败后果:** D may believe a participant is held while Storage cannot find it; I may believe authorization was consumed while Storage outcome is unknown; one module may close while another remains open; an artifact may be exposed prematurely or remain indefinitely unavailable.
- **Mitigation Strategy / 缓解策略:** Build one integrated executable/reference state machine over exact owner contracts. Enumerate both serial orders for Fence/Participant, Revocation/COMMIT_WON, close/send, prepare/commit, and restore/replay. Inject crash before and after every durable write and ACK. Assert pointer, receipt, outcome, outbox, D barrier, I hold, C outcome and COC prefix after every trace. UNKNOWN must never become success, abort or terminality.
- **Required Architecture Decision / 必需架构决策:** A system-wide state/causal model and explicit cross-owner transition contract, with each Owner accepting only its own predicates.
- **Responsible Owner / 责任 Owner:** A coordinates; D/E/I/Storage own their local transitions; H owns wire evidence; C owns provider truth.
- **Verification Evidence / 验证证据:** D Blob 17e53890dd6cce9bea9eacc1be2e64b0ef55ac78; E Blob 475fee41e5eea527af4edefbfe88c58c86967d0a; I Blob 54bab0484bd232a5a258e65e34cc7425288b39a6; Storage Blob 175ee7b1349cfdb79a19898b311a88391ed88010; Issue #25 and #29 remain open. Issue #29 records candidate H recovery suites; it explicitly says those suites do not prove live COC quorum, real owner-ledger adapters, deployed topology or physical recovery.
- **Evidence Status / 证据状态:** **PARTIALLY VERIFIED** for local semantic contracts and bounded reference suites; **NOT PROVEN** for integrated cross-owner correctness.
- **Residual Risk / 剩余风险:** State-space explosion and hidden interleavings remain possible unless the model has explicit invariants, exhaustive bounded exploration and independent review.
- **Blocking Gate / 阻塞门禁:** Issue #43 G3/G4; Issue #25 and #29.
- **Source References / 来源:** D/E/I/Storage exact artifacts above; Issue #25; Issue #29; Issue #43.

### RSK-03 — Forget, inventory and restore cannot yet prove system-wide anti-resurrection / Forget、清单与恢复尚不能证明全系统防复活

- **Probability / 概率:** High / 高 — Global Forget inventory/governance approvals and cross-owner restore proof remain open.
- **Impact / Severity / 影响严重度:** Critical / 致命 — forgotten or revoked information can reappear through derivatives, backups, recipients, replay, restore or late-discovered producers.
- **Risk Level / 风险等级:** **CRITICAL**
- **Description / 描述:** Forget safety is larger than deleting canonical rows. It must cover every derivative-capable producer, direct/transitive lineage, indexes, embeddings, caches, summaries, Context snapshots, queues, DLQ/replay, exports, recipients, replicas, backups and restored copies. D's local fence and I's global inventory epoch are distinct authorities; neither alone proves the complete universe.
- **Affected Components / 影响组件:** D, I, E, F, G, H, Storage, C/Agent integrations, external recipients and backup/restore systems.
- **Root Cause / 根本原因:** The architecture depends on a closed-world, authenticated and current Producer/Recipient/Backup inventory plus complete lineage and owner-local release proofs. The global registry, coverage approvals, exception policy and end-to-end composition are not yet formally closed.
- **Trigger Conditions / 触发条件:** New producer or recipient joins; scope/capability/owner changes; late lineage discovery; backup/export exists outside the inventory; old snapshot is restored; index/cache rebuild runs from stale data; queue/DLQ replays after a Forget.
- **Failure Consequences / 失败后果:** Forgotten information may be reintroduced into retrieval or Context; Global Forget may be falsely reported complete; external recipients or backups may retain data beyond policy.
- **Mitigation Strategy / 缓解策略:** I must define and approve the authoritative closed-world inventory, target seal, inventory epoch, join/leave/change invalidation and unsupported-target policy. D must define lineage and barrier completeness. E/F/G must map every derivative and replay path to D lineage. Storage must restore in RESTORE_FENCED and reconcile D/I ledgers, COC prefixes, owner high-waters and exact RestoreReadinessManifest before any serving. Unknown remains quarantined.
- **Required Architecture Decision / 必需架构决策:** I global inventory and Global Forget governance decision; D producer/lineage coverage decision; Storage restore/readiness protocol; cross-owner acceptance of Issue #20.
- **Responsible Owner / 责任 Owner:** I (inventory and Global Forget policy), D (ForgetFence and lineage), E/F/G (producer/derivative semantics), Storage (physical restore), H (evidence schemas).
- **Verification Evidence / 验证证据:** D ForgetFence Blob 4da0b61ba3656a768ea56b4a2a24e09da4e21cd5; E lifecycle Blob 4fb9e58511941f59b4d777336f8f85ad88ecccf1; F lifecycle Blob 29e9504c75d737c2dd200ebc3306eda555f0b0ac; G lifecycle Blob c1de241ec69834377d9b0e24aa4770a809796d4b; I authorization/restore Blob e3b1b5d99eb36ac0b395854d8c19287d2b64b752; Issue #4, #5 and #20 remain open.
- **Evidence Status / 证据状态:** **PARTIALLY VERIFIED** for owner-local fail-closed rules; **BLOCKED** for governance approvals; **NOT PROVEN** for end-to-end anti-resurrection.
- **Residual Risk / 剩余风险:** Physical erasure, offline recipients, legally retained backups and external onward copies may require policy exceptions and independently auditable evidence even after logical suppression is proven.
- **Blocking Gate / 阻塞门禁:** Issue #43 G2/G3/G4/G7; Issues #4, #5, #20.
- **Source References / 来源:** D/E/F/G/I exact artifacts above; Storage v3.2.3 normative body and v3.2.5 manifest; Issues #4, #5, #20, #29.

### RSK-04 — Fact/Claim semantic authority remains contradictory and ADR-blocked / Fact/Claim 领域权威仍有冲突且 ADR 阻塞

- **Probability / 概率:** High / 高 — the ADR explicitly records no formal decision authority, no approver and no approved option.
- **Impact / Severity / 影响严重度:** High / 高 — canonical identity, revision, evidence attachment, conflict handling and downstream schemas may be built on incompatible semantics.
- **Risk Level / 风险等级:** **HIGH**
- **Description / 描述:** Governance invariants I-04 and design principle P-04 describe Fact and Claim as distinct concepts, while the current domain overview models Claim as the canonical proposition and Fact as a qualified interpretation. B's ADR compares separate Fact attestation versus Claim-only qualification and explicitly remains ADR-BLOCKED.
- **Affected Components / 影响组件:** B, D, E, F, G, H, I and all canonical storage/API/schema consumers.
- **Root Cause / 根本原因:** The semantic choice changes identity, revision, attestation authority, provenance, conflict links, authorization and consumer behavior. It cannot be settled by a naming convention or a downstream schema.
- **Trigger Conditions / 触发条件:** D freezes canonical IDs or persistence schema; E assigns canonical references; F/G/H publish typed fields; a consumer assumes FactRef or treats a Claim qualification as a separate attestation.
- **Failure Consequences / 失败后果:** Duplicate or incompatible identities; migration breakage; inferred claims promoted to facts; evidence attached to the wrong object; historical adjudication cannot be reconstructed.
- **Mitigation Strategy / 缓解策略:** Formal governance authority must decide Option A or B, record rationale and impact analysis, reconcile I-04/P-04/README/terminology, and obtain B/D/E/F/G/H/I consumer dispositions. Until then, dependent canonical identity fields remain candidate/blocked.
- **Required Architecture Decision / 必需架构决策:** ADR-001 Fact/Claim decision by Architecture Governance with B's recommendation and consumer impact review.
- **Responsible Owner / 责任 Owner:** B for domain recommendation; formally designated Architecture Governance for decision; D/E/F/G/H/I for consumer impact.
- **Verification Evidence / 验证证据:** B branch HEAD 0df144ae25c2039c9934395fc88b2d17080eb119; ADR Blob a1024938ff5baba069cf128c69496a44e143330c and canonical-model ADR Blob df77e4a93cb8fef689ae7c828888d960cbf381d6. ADR states formal authority/approver NOT RECORDED and approved option NONE.
- **Evidence Status / 证据状态:** **BLOCKED**.
- **Residual Risk / 剩余风险:** Even after decision, historical data migration and semantic interpretation require compatibility rules and regression fixtures.
- **Blocking Gate / 阻塞门禁:** Issue #43 G2/G3; no canonical schema freeze for affected fields.
- **Source References / 来源:** B ADR-001 artifacts; main I-04/P-04; domain overview; Issue #43.

### RSK-05 — Identity, Scope, Principal and PolicyDomain governance is not fully authorized / Identity、Scope、Principal 与 PolicyDomain 治理尚未完整授权

- **Probability / 概率:** High / 高 — I36-GOV-01..10 remain GOVERNANCE-BLOCKED and external inventory decisions remain open.
- **Impact / Severity / 影响严重度:** Critical / 致命 for a cross-scope authorization failure; High / 高 for blocked cross-domain workflows.
- **Risk Level / 风险等级:** **HIGH**
- **Description / 描述:** Typed Principal, Actor, Scope, Environment, issuer, delegation, cross-issuer linking, PolicyDomain and PermissionEpoch contracts must compose consistently. I owns authorization and revocation; B owns domain type semantics; other Owners consume these types. Multi-PolicyDomain atomicity is explicitly blocked; PermissionEpoch is PolicyDomain-local and must not be compared across domains.
- **Affected Components / 影响组件:** B, C, D, E, F, G, H, I, Storage, Agent and Environment adapters.
- **Root Cause / 根本原因:** Technical taxonomies and candidate proof contracts do not equal formal governance approval. Trusted issuer admission, delegation, scope inheritance, environment federation, emergency access, revocation SLA and actor/principal binding require accountable external authority.
- **Trigger Conditions / 触发条件:** Cross-scope sharing; cross-environment memory; delegated workload; principal re-linking; issuer key rotation/revocation; break-glass; a Forget or publication operation spanning multiple PolicyDomains.
- **Failure Consequences / 失败后果:** Unauthorized disclosure or mutation; incorrect identity attribution; stale authorization accepted; cross-domain partial completion misreported as atomic; fail-closed behavior blocks legitimate operations indefinitely.
- **Mitigation Strategy / 缓解策略:** Close I36-GOV-01..10 with named authorities and signed evidence. Define a hard supported atomicity boundary (one PolicyDomain per atomic operation unless a separately approved coordinator exists). Specify cross-domain partial-result orchestration and typed, incomparable authority-local epochs. Preserve DENY/QUARANTINE/UNKNOWN for unknown identity or scope.
- **Required Architecture Decision / 必需架构决策:** I identity/trust governance decisions, PolicyDomain atomicity ADR and B typed identity/Scope mapping acceptance.
- **Responsible Owner / 责任 Owner:** I (authorization/governance); B (domain types); A (integration).
- **Verification Evidence / 验证证据:** I branch HEAD 28df608b075e619563c6367a8a1c171185c1faaf; I authorization contract Blob e3b1b5d99eb36ac0b395854d8c19287d2b64b752; Issue #4 and #5 explicitly list unresolved inventory and I36-GOV-01..10; Issue #29/Issue #10 preserve Multi-PolicyDomain BLOCKED.
- **Evidence Status / 证据状态:** **BLOCKED** for governance approval; **PARTIALLY VERIFIED** for technical fail-closed semantics.
- **Residual Risk / 剩余风险:** External issuers, legal jurisdictions and emergency approvers may add policy constraints not represented by the current technical model.
- **Blocking Gate / 阻塞门禁:** Issue #43 G2/G4/G7; Issues #4 and #5.
- **Source References / 来源:** I authorization/restore contract; I principal/actor contract; Issues #4, #5, #10, #29.

### RSK-06 — Applied and Provider Outcome are not one frozen end-to-end evidence chain / Applied 与 Provider Outcome 尚未形成统一冻结的端到端证据链

- **Probability / 概率:** High / 高 — Issue #3 explicitly records Applied Contract Frozen = NO and Test Executed/Passed = NO/NO.
- **Impact / Severity / 影响严重度:** High / 高 — false Applied claims, duplicated provider side effects, stale or forgotten context reaching a provider, or inability to establish what request was actually submitted.
- **Risk Level / 风险等级:** **HIGH**
- **Description / 描述:** Context delivery, Adapter materialization, final immutable inference request, provider handoff, provider acceptance, model execution and user delivery are distinct events. The system must bind the exact final request to G ContextVersion/Delivery, C egress admission/attempt/outcome, H authenticated Adapter evidence, I current authorization and D Forget/lineage clearance. No single local ACK proves the whole chain.
- **Affected Components / 影响组件:** C, G, H, I, D, Agent Adapter, provider-specific transport adapters.
- **Root Cause / 根本原因:** Each authority proves a different fact. The exact final-request identity, complete managed-region digest, Applied predicate, Provider Outcome schema/validator and current-use semantics must be frozen together; role-simulated mapping is not independent Owner approval or runtime proof.
- **Trigger Conditions / 触发条件:** Context transformation after delivery; reconnect/replay; final request differs from acknowledged context; gate close races send; provider timeout/lost response; provider lacks idempotency lookup; later Forget/revocation changes current-use eligibility.
- **Failure Consequences / 失败后果:** System reports Applied without proof of the final request; retries cause duplicate external effects; historical Applied is mistaken for current permission; ambiguous provider handoff is incorrectly treated as no send.
- **Mitigation Strategy / 缓解策略:** Freeze one immutable final-request boundary and digest after all transformations. Specify the exact G Applied predicate and historical-vs-current-use rule. Bind C's immutable Provider Outcome to the same request and provider idempotency key. H must publish exact versioned wire/validator and negative vectors. Execute real adapter close-vs-send and same-key recovery tests. Keep UNKNOWN/IN_DOUBT blocking.
- **Required Architecture Decision / 必需架构决策:** Joint C/G/H/I/D Applied and Provider Outcome freeze with explicit independent Owner decisions; H 1.2.13 / CSubmitOutcome 1.0.1 mapping is currently a candidate, not production authorization.
- **Responsible Owner / 责任 Owner:** G (Context-side Applied); C (provider side-effect truth); H (wire/authenticated evidence); I (authorization); D (Forget/lineage).
- **Verification Evidence / 验证证据:** Issue #3 remains open and explicitly says Frozen NO / tests NO / implementation NO. C egress review Blob 5a27f79087d3a5e01dd23e818d8c7ea0fdb61d1d says adapter implementation/runtime conformance OPEN and 15 vectors SPECIFIED/NOT RUN. C Phase 3.8.12 mapping Blob 92ed89a308ad97f6846960bb7182e0916949978e is L1/L2 candidate only. H run 44063916718 completed SUCCESS on commit c326e561145e9558f48f199128814643d8720e45; the C artifact reports 20/20 tests. This is bounded provider-outcome conformance, not an actual provider adapter race or full Applied proof.
- **Evidence Status / 证据状态:** **PARTIALLY VERIFIED** for schema/reference-level mapping; **NOT PROVEN** for full Applied and real provider side-effect behavior.
- **Residual Risk / 剩余风险:** Providers differ in idempotency, request lookup, timeout semantics and execution reporting; no universal exactly-once provider guarantee can be assumed.
- **Blocking Gate / 阻塞门禁:** Issue #43 G2/G3/G4/G7; Issue #3.
- **Source References / 来源:** C egress review; C Phase 3.8.12 mapping; H 1.2.13 schema/mapping; G lifecycle contract; Issue #3; run 44063916718.

### RSK-07 — COC and JF-10 recovery domains may be locally sound but are not proven as one recoverable system / COC 与 JF-10 恢复域各自设计不等于整体恢复已证明

- **Probability / 概率:** High / 高 — Issue #10 Gate A remains PARTIAL PASS/OPEN, Gate B/C remain blocked; Issue #29 retains physical topology and integration blockers.
- **Impact / Severity / 影响严重度:** Critical / 致命 for an incorrect recovery decision; High / 高 for indefinite outage if fail-closed.
- **Risk Level / 风险等级:** **HIGH**
- **Description / 描述:** COC is a quorum-committed causal-order log for recovery batches/manifests and participant accounting. JF-10 is a separately gated I/Storage prepared-participant same-XID bridge. COC is not I's sequencer and does not decide JF-10 COMMIT/ABORT. Their separate authority is correct, but the end-to-end bridge, durable evidence exchange and restore ordering must be demonstrated.
- **Affected Components / 影响组件:** A/COC, Storage, I, D, C, H, E and restore control paths.
- **Root Cause / 根本原因:** Multiple durable authorities have independent positions, prefixes, participant identities and failure domains. The system must not compare their counters or assume that a COC prefix implies an I/D owner decision or a Storage terminal outcome. Some current evidence is capability CI or reference fixtures, not a live persistent COC plus owner-ledger integration.
- **Trigger Conditions / 触发条件:** COC quorum outage; I/D request arrives during outage; prepared participant survives restart; coordinator loses ACK; old primary rejoins; snapshot rollback; participant appears in one authority but not another.
- **Failure Consequences / 失败后果:** Missing participant, duplicate resolution, wrong-XID resolution, premature gate release, split-brain publication or indefinite IN_DOUBT.
- **Mitigation Strategy / 缓解策略:** Preserve distinct COC, JF-10, I, D and Storage state machines. Specify exact bridge identities and digest bindings. Prove cutoff batch completeness, two-way JoinProof, same-XID resolution, old-primary fencing, quorum loss/recovery, snapshot rollback and owner-local release. Do not treat engine capability CI as live COC proof.
- **Required Architecture Decision / 必需架构决策:** A/Storage/I/D exact-version bridge and recovery acceptance; selected durable COC implementation profile and operator custody; explicit COC-to-JF-10 composition contract.
- **Responsible Owner / 责任 Owner:** A (COC integration), Storage (durable COC and prepared XID), I (terminal authorization), D (Forget barrier), H (wire evidence), C (provider outcomes).
- **Verification Evidence / 验证证据:** Issue #10 remains open: Gate A PARTIAL PASS/OPEN; Gate B persistent COC and Gate C deterministic fault injection BLOCKED. Issue #29 records H reference suites and candidate JoinProof but states they do not prove live COC quorum or physical topology. Issue #43 comment 6944732092 explicitly separates COC from JF-10.
- **Evidence Status / 证据状态:** **PARTIALLY VERIFIED** for bounded PostgreSQL 18.7 capability probes and reference tests; **NOT PROVEN** for complete live COC/JF-10/owner-ledger recovery.
- **Residual Risk / 剩余风险:** Even a passing fault campaign is bounded by the selected consensus, storage, network and operator failure model; disaster recovery and human operations require separate evidence.
- **Blocking Gate / 阻塞门禁:** Issue #43 G3/G4/G5; Issue #10 Gate B/C; Issue #29.
- **Source References / 来源:** Issue #10; Issue #29; Issue #43 comments 6944704060 and 6944732092; Storage v3.2.3 and v3.2.5 manifest.

### RSK-08 — Exact-version currentness and evidence freshness are not yet closed-loop controlled / 精确版本当前性与证据时效尚未形成闭环控制

- **Probability / 概率:** High / 高 — the live Owner heads have advanced beyond the Phase 2 evidence ledger, and the current successor manifest is explicitly not jointly accepted or frozen.
- **Impact / Severity / 影响严重度:** High / 高 — a consumer can validate one schema/contract while another Owner relies on a different revision or superseded proof.
- **Risk Level / 风险等级:** **HIGH**
- **Description / 描述:** A branch name is mutable; a path is not a version; a schema artifact revision is not necessarily a wire-family version; and a decision over one Blob does not automatically apply to its successor. The Phase 2 ledger is a historical snapshot, not a currentness oracle. Current live heads now contain H Unified 1.2.13, C Phase 3.8.12 and Storage v3.2.5 manifest, while the old ledger describes earlier baselines.
- **Affected Components / 影响组件:** A–I, Storage, all schemas, validators, manifests, cross-owner reviews and CI evidence.
- **Root Cause / 根本原因:** Exact pins are recorded, but no single continuously enforced mechanism invalidates dependent approvals and blocks merge/freeze whenever any source Blob, schema, validator, policy or branch head changes.
- **Trigger Conditions / 触发条件:** Owner pushes a successor; schema version advances; a manifest updates without all consumer reviews; a branch is force-updated; an older CI run is cited against a newer Blob; bilingual counterpart changes independently.
- **Failure Consequences / 失败后果:** False approval by stale evidence; schema/validator mismatch; one Owner assumes another accepted a successor; audit cannot reconstruct which contract was actually reviewed.
- **Mitigation Strategy / 缓解策略:** Maintain a machine-checkable evidence ledger with branch HEAD, commit, path, Blob SHA, artifact version, wire-family version, status, approving authority, consumer set, CI-tested commit and supersession edges. At every gate, re-fetch all sources and fail closed on changed pins. Do not infer approval from presence in a successor manifest.
- **Required Architecture Decision / 必需架构决策:** A repository-wide currentness and supersession policy, with exact Owner acceptance recorded per immutable source set.
- **Responsible Owner / 责任 Owner:** A (integrated ledger/gates); each Owner (own source and acceptance); H/Storage (wire and successor manifests).
- **Verification Evidence / 验证证据:** Main HEAD b372b62c640a2b656e54b6db62a4ee67d7d8c001; Phase 2 review branch HEAD d7a3379fd51660912200a6131bcd037c0f53583c; current live Owner heads recorded in §3; Storage v3.2.5 manifest Blob bea90697e7a61d43bed00543d636a5cdf40cf5ca states NOT JOINTLY ACCEPTED / NOT FROZEN and says prior decisions do not transfer automatically.
- **Evidence Status / 证据状态:** **VERIFIED** that the historical ledger is stale relative to the live snapshot; **NOT PROVEN** that all dependent approvals are continuously invalidated and refreshed.
- **Residual Risk / 剩余风险:** A commit can advance immediately after review readback; final gate must use a reproducible snapshot/compare-and-set process.
- **Blocking Gate / 阻塞门禁:** Issue #43 G1/G2/G6/G7.
- **Source References / 来源:** Phase 2 exact evidence ledger; live Owner branch HEADs; Storage v3.2.5 manifest; Issue #43.

### RSK-09 — Production trust, cryptographic profile and anti-rollback authority remain candidates / 生产信任、密码配置与防回滚权威仍属候选

- **Probability / 概率:** High / 高 — I36 governance approvals remain blocked and I's crypto profile is identified as a candidate rather than production approval.
- **Impact / Severity / 影响严重度:** Critical / 致命 for forged owner evidence or rollback acceptance; High / 高 for inability to verify signed evidence across recovery.
- **Risk Level / 风险等级:** **HIGH**
- **Description / 描述:** H wire schemas and I signed P0 projections specify which fields are protected, but production trust also requires named issuer authority, root admission, key custody, rotation/revocation, historical verification, canonicalization agreement, anti-rollback anchor and operational separation of duties. Schema correctness and a test-only signature helper do not establish a production trust service.
- **Affected Components / 影响组件:** I, H, C, Storage, COC, D and all owner receipt verifiers.
- **Root Cause / 根本原因:** Cryptographic object shape and semantic projection are ahead of formal trust governance and production custody decisions. Independent language implementations, external trust roots and anti-rollback anchors are not proven by one-language candidate tests.
- **Trigger Conditions / 触发条件:** Key compromise; issuer rotation; historical receipt verification; cross-language canonicalization mismatch; restore to a stale key-status snapshot; missing external anti-rollback anchor; untrusted signer or audience substitution.
- **Failure Consequences / 失败后果:** Forged or replayed owner evidence accepted; valid historical evidence rejected; restored state rolls back trust or revocation; gate releases based on stale trust.
- **Mitigation Strategy / 缓解策略:** I and Security Governance approve issuer/principal/key lifecycle and custody. H and I freeze canonicalization/signature profile and exact P0 allowlists. Require independent implementations to agree on canonical bytes, digest, signature input and error behavior. Anchor anti-rollback outside the restored database failure domain and test revocation/rotation/restore.
- **Required Architecture Decision / 必需架构决策:** Formal I36-GOV-01..10 approvals and production crypto/trust profile decision; H/I exact-version interoperability acceptance.
- **Responsible Owner / 责任 Owner:** I (trust and governance), H (wire/canonicalization), Storage (durable key/anti-rollback integration), C/D (consumer verification).
- **Verification Evidence / 验证证据:** I Phase 3.8.9 Blob 5c0e2049513d391dfc118f4f629a5ec95de456d6 labels the P0 projection a candidate and profile/production approval separate; Issue #5 remains open. H schema/reference CI is bounded evidence, not production trust-root or custody evidence.
- **Evidence Status / 证据状态:** **PARTIALLY VERIFIED** for exact signed field projections and bounded validators; **BLOCKED** for governance; **NOT PROVEN** for production trust and anti-rollback.
- **Residual Risk / 剩余风险:** Hardware security modules, cloud KMS, issuer federation and operator controls introduce deployment-specific failure modes.
- **Blocking Gate / 阻塞门禁:** Issue #43 G2/G4/G5/G7; Issue #5.
- **Source References / 来源:** I Phase 3.8.9; I crypto profile; H Unified 1.2.13 and validator artifacts; Issue #5; Issue #29.

### RSK-10 — Architecture governance and protocol complexity may exceed implementation and operational capacity / 架构治理与协议复杂度可能超过工程及运维承载能力

- **Probability / 概率:** Medium / 中 — complexity is already visible in the number of authorities, gates, ledgers and exact-version bindings, but actual engineering capacity and target workload are not yet established.
- **Impact / Severity / 影响严重度:** High / 高 — excessive coordination cost, slow delivery, fragile operations, difficult debugging and a system whose safety protocol is too complex to implement or operate correctly.
- **Risk Level / 风险等级:** **HIGH**
- **Description / 描述:** The architecture spans A–I, Storage, COC, JF-10, multiple owner-local ledgers, typed cursors/epochs, signed receipts, manifests, recovery joins, private staging, multiple gates and separate terminal proofs. This complexity may be justified by the safety requirements, but no evidence yet demonstrates that the complete protocol is the minimum sufficient design or that the future engineering/operator team can reliably implement, test, observe and recover it.
- **Affected Components / 影响组件:** Entire system; architecture governance, Owner workflow, runtime engineering, Storage/COC operations, security and support.
- **Root Cause / 根本原因:** Complexity is accumulating through local safety requirements and cross-owner proof obligations without a measured system-wide complexity budget, operational staffing model, bounded initial deployment scope or demonstrated vertical slice. The technology blueprint is CANDIDATE, and the runtime implementation repository/engineering owner are not designated in Issue #7.
- **Trigger Conditions / 触发条件:** Every new workflow adds another independent sequencer, epoch, proof, gate or manifest; cross-owner review latency grows; the number of crash combinations outstrips the test harness; operational staff cannot explain why an operation is IN_DOUBT; no one owns end-to-end incident resolution.
- **Failure Consequences / 失败后果:** Implementation stalls; teams bypass gates; hidden coupling appears; operational runbooks become unmanageable; latency/cost becomes unacceptable; recovery depends on a few people understanding undocumented state interactions.
- **Mitigation Strategy / 缓解策略:** Require an explicit complexity and operability assessment for every new authority, ledger, coordinator and proof. Establish a minimum viable safety envelope and a bounded pilot: one Canonical Memory authority, one PolicyDomain, one producer class, one index family, one Context/Adapter path and one provider. Prove end-to-end behavior before adding multi-domain or multi-region features. Define operator actions, IN_DOUBT handling, observability, RPO/RTO and staffing. Measure resource envelope and workload before selecting topology.
- **Required Architecture Decision / 必需架构决策:** A technology/topology decision package that includes complexity budget, deployment mode, operational ownership, failure model, resource/performance budget and phased capability boundaries.
- **Responsible Owner / 责任 Owner:** A (system integration and complexity control); all Owners (justify their local protocol burden); designated engineering and operations authority (implementation and operability).
- **Verification Evidence / 验证证据:** README states Architecture definition and implementation not started by design; ARCHITECTURE_ROADMAP places technology evaluation before implementation; TAB-001 remains CANDIDATE in Issue #43; Issue #7 asks for canonical runtime repository and accountable engineering owner; Storage topology ADR leaves T1–T8 open. No measured complexity/operability evidence was found in the reviewed baseline.
- **Evidence Status / 证据状态:** **VERIFIED** for architecture-only status and missing designation recorded in Issue #7; **NOT PROVEN** for whether complexity exceeds future capacity (no capacity/benchmark/operability evidence).
- **Residual Risk / 剩余风险:** A disciplined pilot may show that the complexity is necessary and manageable; conversely, removing proof obligations without a threat model may weaken correctness.
- **Blocking Gate / 阻塞门禁:** Issue #43 G5/G8; Issue #7; TAB-001.
- **Source References / 来源:** README; ARCHITECTURE_ROADMAP; TAB-001; Issue #7; Storage topology ADR; Issue #43.

---

## 3. Live evidence snapshot / 实时证据快照

The following HEADs were fetched from the repository's branch listing and each selected artifact was read from its named branch during this review. The HEAD is a snapshot, not a permanent pin. Selected Blob SHAs identify the exact content read.

| Owner | Branch | HEAD commit | Selected exact artifact and Blob |
|---|---|---|---|
| A | session-a-integration-2026-11-16 | d72dbac6e0f739cd00ac986176b78ec5cd385d88 | Phase 3.8.6 integration review: bfbff1e697a7ef2092b4438ccddddf7336e66b15 |
| B | session-b-domain-model-phase3 | 0df144ae25c2039c9934395fc88b2d17080eb119 | ADR-001 Fact/Claim: a1024938ff5baba069cf128c69496a44e143330c; canonical-model ADR: df77e4a93cb8fef689ae7c828888d960cbf381d6 |
| C | session-c-agent-integration-2026-11-16 | f3251081c49e697fe4739a252e27f59e2ecd0a8f | Provider egress review: 5a27f79087d3a5e01dd23e818d8c7ea0fdb61d1d; Phase 3.8.12 mapping: 92ed89a308ad97f6846960bb7182e0916949978e |
| D | session-d-memory-brain-2026-11-16 | 97e68fbd225bdf0ac71860c01077481afc162d50 | ForgetFence contract: 4da0b61ba3656a768ea56b4a2a24e09da4e21cd5; publication contract: 17e53890dd6cce9bea9eacc1be2e64b0ef55ac78 |
| E | session-e-memory-compiler-2026-11-16 | fdb4f67a83083d995930b88f93975b5ee36080f3 | Phase 3.8 publication orchestration: 475fee41e5eea527af4edefbfe88c58c86967d0a; Phase 3.7 lifecycle: 4fb9e58511941f59b4d777336f8f85ad88ecccf1 |
| F | session-f-memory-runtime | 8d5ef89ce9b1ff1471ffd1a03fe4f289addb0af3 | Phase 3.7 lifecycle: 29e9504c75d737c2dd200ebc3306eda555f0b0ac |
| G | session-g-memory-context | f9ca0ddc36e17f74041506f17039f0202d13042e | Phase 3.7 lifecycle: c1de241ec69834377d9b0e24aa4770a809796d4b |
| H | session-h-bmcp-protocol | f809be092a6c04db7982cc1bdbdd9c88787a4286 | Unified 1.2.13 schema: 8e7f6a6c9663388863db88548f9c37d0fdb1bd97; RecoveryJoin 1.0.2: 4b664e3bce465499bcdfd93796349a4ba7074002; Phase 3.8.9 mapping: 37e8c41a580a51df8aa0188d90dd6b1d798d69f0 |
| I | session-i-security-governance-2026-11-16 | 28df608b075e619563c6367a8a1c171185c1faaf | Authorization/restore: e3b1b5d99eb36ac0b395854d8c19287d2b64b752; Phase 3.8.9 P0 allowlists: 5c0e2049513d391dfc118f4f629a5ec95de456d6 |
| Storage | session-storage-consistency-forget-atomicity-2026-11-16 | 17be31915b06d98d7f822e6e5270b8cde39eb0bb | Normative Storage v3.2.3 body: 5cee0d58575adc0fb3dd20a5c7ab68c2a2711792; v3.2.5 successor manifest: bea90697e7a61d43bed00543d636a5cdf40cf5ca; topology ADR: 1ef47d4e5711c7db73a24d249adf1992be1f6aa4; visibility contract: 175ee7b1349cfdb79a19898b311a88391ed88010 |

### 3.1 Repository and tracking facts / 仓库与跟踪事实

- Main HEAD read: b372b62c640a2b656e54b6db62a4ee67d7d8c001.
- Existing A integration review branch: review/arch-consol-001-system-wide-2026-11-17 @ d7a3379fd51660912200a6131bcd037c0f53583c.
- Existing Draft PR #44 tracks Phase 2. This R report is a separate risk-assessment artifact and must not overwrite A's work.
- Issue #43 remains OPEN.
- Issues #3, #4, #5, #7, #10, #20, #25 and #29 were read and remain OPEN in the fetched repository snapshot.
- The Phase 2 exact evidence ledger records earlier Owner HEADs. It is useful historical evidence, but it is not the current source of truth after branches advanced. R re-fetched the live Owner HEADs and selected source Blobs above.

### 3.2 Bounded test evidence / 有界测试证据

- H Provider Outcome run 44063916718: GitHub Actions reports completed / success on commit c326e561145e9558f48f199128814643d8720e45. C's Phase 3.8.12 review reports 20/20 tests. This is bounded schema/reference conformance only.
- H Recovery Cutoff run 44042074640: GitHub Actions reports completed / success on commit fb9a2ab8b528c2b7010d935372f76a14d6676755. Issue #29 describes a 93-method candidate suite. This does not prove live COC quorum, owner-ledger adapters or physical topology.
- Issue #10 records PostgreSQL 18.7 capability evidence across prepared-XID, restart/promotion, restore and response-loss fixtures. Gate A remains PARTIAL PASS / OPEN; Gate B and Gate C remain BLOCKED. These fixtures do not prove the project's selected production topology or full D/I/COC integration.
- No test result in this section is treated as proof of end-to-end system correctness.

---

## 4. Critical Architecture Risk Analysis / 关键架构风险分析

### 4.1 What can invalidate system correctness? / 哪些风险会使系统正确性无法成立？

1. RSK-01: The final visibility point is not tied to a selected physical linearization domain. This can invalidate the central rule that a winning ForgetFence prevents later publication.
2. RSK-02: Cross-owner state transitions have not been proven as one complete state machine. Locally valid receipts can compose into an invalid global state.
3. RSK-03: The system cannot yet prove that every derivative, recipient, backup and restored copy is covered by Forget and current authorization.
4. RSK-04: Canonical Fact/Claim identity semantics remain blocked. Downstream schemas cannot safely freeze a disputed identity model.
5. RSK-05: Identity and PolicyDomain governance approvals remain blocked. A typed authorization protocol is not sufficient without approved principals, issuers, scope and delegation rules.

### 4.2 Which mechanisms look safe but lack proof? / 哪些机制看似安全但缺乏证明？

- **Serializable database / SERIALIZABLE 数据库:** The isolation level name alone does not prove the actual D and Storage rows share the same transaction domain, that every protected read uses the authoritative primary, or that failover/restore preserves the required order.
- **Prepared XID / Prepared XID:** A PostgreSQL capability probe does not prove COC intent registration, I decision, D barrier, Storage visibility and recovery are correctly coupled in the deployed application.
- **COC quorum prefix / COC Quorum 前缀:** A committed prefix proves the COC log's own order, not I authorization, D ForgetFence clearance, C provider outcome or Storage publication outcome.
- **Signed receipt / 签名 Receipt:** A valid signature proves possession of a key over specified bytes, not that the signer was an approved authority, that the key was current, that the proof is fresh, or that the referenced owner ledger is complete.
- **Applied ACK / Applied ACK:** Adapter acknowledgement proves only the exact protocol boundary defined by the contract; it does not prove provider handoff, model execution, attention or user-visible delivery.
- **Private staging / 私有暂存:** Staging is safe only if object URLs, indexes, caches, logs, metrics, backups and restore readers cannot expose the object before the authoritative visibility pointer commits.
- **Fail-closed UNKNOWN / UNKNOWN 失败关闭:** This is safe only if every consumer, retry worker, restore path and operator procedure preserves UNKNOWN and cannot silently convert it into timeout success, abort or release.
- **Bilingual documentation / 双语文档:** Parity improves comprehension but does not establish semantic agreement between independent Owners or prove the protocol.

### 4.3 Can locally correct modules compose incorrectly? / 局部正确的模块是否可能组合后错误？

**Yes. This is a primary system risk.** Examples:

- D records a valid producer registration; E correctly retries at least once; Storage correctly stages privately. If final visibility does not share D's fence linearization domain, the composition can still publish after Forget wins.
- I correctly issues a single-use authorization receipt; Storage correctly commits a local transaction; COC correctly records a prefix. If the exact participant tuple is not bound across all three authorities, the global operation can be ambiguous.
- F correctly rebuilds an index from its snapshot; G correctly restores a Context snapshot; D has already forgotten a source. If current lineage/fence checks are not mandatory at final read and activation, forgotten content can reappear.
- H correctly validates a schema version; C consumes a newer object revision; Storage's manifest pins an older revision. Each validator can pass locally while the system has no single agreed contract.
- G correctly records historical Applied; I later revokes permission; C retries a prior request. If historical application is confused with current-use eligibility, a stale request can be resubmitted.
- C correctly treats provider timeout as UNKNOWN; an orchestration retry creates a new idempotency key. The provider may execute twice even though C's local state machine is correct.

---

## 5. Unresolved Architecture Decisions / 未解决架构决策

| Decision ID | Required decision / 必须决策 | Accountable authority / 责任权威 | Current status / 当前状态 | Blocks / 阻塞 |
|---|---|---|---|---|
| UAD-01 | Fact vs Claim canonical model, identity and revision semantics / Fact 与 Claim 的规范模型、身份及修订语义 | Architecture Governance + B | ADR-BLOCKED | Canonical schema, references, consumer contracts |
| UAD-02 | D/Storage physical serialization topology: Option A or B / D/Storage 物理序列化拓扑 | Storage + D; I review | ADR-BLOCKED; no topology selected | Final visibility and ForgetFence correctness |
| UAD-03 | Authoritative producer/recipient/backup inventory, inventory epoch/seal and Global Forget completion / 权威 Producer/Recipient/Backup 清单及 Global Forget 完成 | I | Governance OPEN/BLOCKED | Forget completeness and restore release |
| UAD-04 | I36-GOV-01..10 issuer, principal, delegation, scope, environment, revocation and actor binding / I36-GOV-01..10 身份信任治理决策 | I + external governance authorities | GOVERNANCE-BLOCKED | Authorization and security acceptance |
| UAD-05 | Supported atomicity scope for multi-PolicyDomain operations / 多 PolicyDomain 操作的原子性范围 | I + A | BLOCKED | Cross-domain Forget/publication |
| UAD-06 | One exact C/G/H/I/D Applied and Provider Outcome evidence chain / C/G/H/I/D Applied 与 Provider Outcome 证据链 | C, G, H, I, D | Candidate mapping; Issue #3 Frozen NO | Provider submission and Applied acceptance |
| UAD-07 | COC ↔ JF-10 bridge, persistent coordinator profile and recovery ownership / COC 与 JF-10 桥接、持久协调器及恢复责任 | A, Storage, I, D, C, H | Design artifacts exist; physical/operational proof open | Recovery and JF-10 P0 |
| UAD-08 | Production trust profile, key custody, issuer roots and external anti-rollback / 生产信任配置、密钥托管、Issuer Root 与外部防回滚 | I + Security Governance + H/Storage | Candidate; governance approval open | Signed evidence acceptance |
| UAD-09 | Canonical runtime repository, accountable engineering owner and code-contract traceability / 权威 Runtime 仓库、工程责任人与代码追溯 | Project authority / A coordination | Issue #7 OPEN | Engineering readiness and implementation binding |
| UAD-10 | Technology/topology choice, resource envelope, RPO/RTO, SLO and operational staffing / 技术拓扑、资源预算、RPO/RTO、SLO 与运维人员 | Architecture Governance + Storage + engineering/operations | TAB-001 CANDIDATE; topology gates open | Production deployment |

No R assessment may decide UAD-01 through UAD-10 on behalf of their accountable authorities. The required action is to preserve each item as OPEN/BLOCKED until the named authority supplies an exact decision and evidence.

R 不得代替上述责任权威决定 UAD-01 至 UAD-10。必须保留 OPEN/BLOCKED 状态，直至责任权威提供精确决议及证据。

---

## 6. Risk Dependency Analysis / 风险依赖关系分析

### 6.1 Dependency graph / 依赖图

~~~mermaid
flowchart TD
  UAD1["UAD-01 Fact/Claim semantics"]
  UAD4["UAD-04 Identity and governance"]
  UAD3["UAD-03 Inventory and Global Forget"]
  UAD2["UAD-02 Physical serialization topology"]
  R2["RSK-02 Integrated publication state machine"]
  R3["RSK-03 Forget / restore anti-resurrection"]
  R6["RSK-06 Applied / Provider Outcome"]
  UAD7["UAD-07 COC / JF-10 recovery"]
  UAD8["UAD-08 Production trust"]
  UAD9["UAD-09 Runtime engineering ownership"]
  UAD10["UAD-10 Technology / operations"]
  R8["RSK-08 Version currentness"]
  FREEZE["Architecture freeze / deployment acceptance"]
  UAD1 --> R2
  UAD4 --> R2
  UAD3 --> R3
  UAD2 --> R2
  UAD2 --> R3
  R2 --> UAD7
  UAD4 --> UAD8
  UAD8 --> R6
  UAD1 --> R8
  UAD2 --> R8
  R2 --> R8
  R3 --> R8
  R6 --> R8
  UAD7 --> UAD10
  UAD9 --> UAD10
  R8 --> FREEZE
  R2 --> FREEZE
  R3 --> FREEZE
  R6 --> FREEZE
  UAD10 --> FREEZE
~~~

### 6.2 Root-first interpretation / 根本性解释

- **First-order prerequisites:** domain semantics (UAD-01), identity/authorization governance (UAD-04), global inventory (UAD-03), physical serialization (UAD-02). These define what the system is allowed to store, authorize, publish and forget.
- **Composition prerequisites:** integrated publication state machine (RSK-02), Forget/restore anti-resurrection (RSK-03), Applied/provider evidence (RSK-06), and COC/JF-10 recovery (UAD-07).
- **Evidence-control prerequisite:** currentness and exact-version binding (RSK-08) must be continuously applied to every decision above; it is not a one-time document task.
- **Production prerequisites:** production trust (UAD-08), implementation ownership (UAD-09), and technology/operations (UAD-10).

A downstream task cannot close an upstream dependency by inventing a local workaround. For example, a schema cannot settle Fact/Claim semantics; a Storage transaction cannot approve I authorization; a COC prefix cannot prove D lineage; and a passing reference test cannot select a production topology.

下游任务不能通过自行补充局部方案来关闭上游依赖。例如 Schema 不能替代 Fact/Claim 决议；Storage 事务不能批准 I 授权；COC 前缀不能证明 D Lineage；参考测试通过不能替代生产拓扑选择。

---

## 7. Risk Closure Criteria / 风险关闭条件

No Critical or High risk is closed by document publication alone. Closure requires the following minimum evidence:

| Risk | Minimum closure criteria / 最低关闭条件 | Required authority / 必需权威 | Status now / 当前状态 |
|---|---|---|---|
| RSK-01 | Approved Option A/B; exact serialization domain; row/lock ownership; authoritative read path; failover/restore semantics; deterministic fence-vs-commit proof; D/I/Storage exact acceptance | Storage, D, I, A | BLOCKED |
| RSK-02 | Integrated executable/reference model; both serial orders; crash before/after every durable boundary; lost ACK, duplicate/replay, stale lease, digest conflict, UNKNOWN; invariant checker and independent Owner reviews | A, D, E, I, Storage, H, C as applicable | NOT PROVEN |
| RSK-03 | Approved closed-world inventory/seal; complete producer/recipient/backup/restore map; transitive lineage; owner-local gate releases; restore-fenced replay; anti-resurrection test across all derivatives | I, D, E, F, G, H, Storage | BLOCKED |
| RSK-04 | Formal ADR decision by authorized governance body; baseline reconciliation; immutable identity/revision rules; migration impact; consumer acceptance | Architecture Governance, B, D/E/F/G/H/I | BLOCKED |
| RSK-05 | Signed I36-GOV-01..10 decisions; approved principal/issuer/delegation/scope/environment model; explicit PolicyDomain atomicity boundary; negative cross-scope tests | I and external governance authorities; B/A consumers | BLOCKED |
| RSK-06 | Frozen final-request identity and digest; G Applied predicate; C immutable outcome semantics; H exact wire/validator; D/I currentness binding; real adapter send/close race and provider same-key recovery | C, G, H, I, D | NOT PROVEN |
| RSK-07 | Persistent COC implementation profile; exact COC/JF-10 bridge; same-XID resolution; two-way JoinProof; quorum outage, split-brain, restore and fault-injection campaign; owner-local release proofs | A, Storage, I, D, C, H | BLOCKED |
| RSK-08 | Machine-checkable exact-version ledger; all dependent Owner approvals bound to exact Blob; changed-source invalidation; fresh gate readback; bilingual parity | A and every source Owner | PARTIALLY VERIFIED |
| RSK-09 | Approved production trust roots and key custody; exact crypto/canonicalization profile; independent cross-language vectors; key rotation/revocation and anti-rollback restore tests | I, H, Storage, Security Governance | BLOCKED |
| RSK-10 | Bounded pilot and complexity budget; named engineering/operations owner; resource and workload measurements; runbooks; SLO/RPO/RTO; demonstrated recoverability and incident handling | A, Storage, engineering/operations, all Owners | NOT PROVEN |

### 7.1 Global evidence rule / 全局证据规则

For every closure package record:
1. Exact branch, commit, path and Blob SHA.
2. Exact Owner decision and whether it is independently attributable or a role simulation.
3. Exact schema/wire-family version and validator revision.
4. Test source, test run, tested commit, environment, test count, skipped cases and failure output.
5. Explicit evidence ceiling: logical model, schema, reference model, physical capability, integrated conformance, deployed operation or production acceptance.
6. Chinese/English semantic parity.
7. Residual risk and next gate.

Every UNKNOWN, missing proof, stale pin or unverifiable owner must remain blocking. No inferred approval.

---

## 8. Root-first Risk Remediation Recommendations / 根本性优先整改建议

This is an ordered recommendation, not an authorization to change Owner-owned decisions.

### Priority 0 — Establish the conditions under which the system can be correct / 优先级 0：建立系统正确成立的条件

1. **B + Architecture Governance:** Resolve Fact/Claim semantics before canonical identity/schema freeze. Keep all dependent canonical references neutral until the ADR is approved.
2. **I + external governance:** Close identity, issuer, delegation, Scope, Environment, PolicyDomain and Global Forget governance. Explicitly decide the supported atomicity boundary.
3. **Storage + D + I:** Select the physical D/Storage serialization topology. Do not allow an implementation to substitute process mutex, queue order, check-then-write or stale replica behavior.

### Priority 1 — Prove the irreversible safety boundaries / 优先级 1：证明不可逆安全边界

4. **A + D + E + I + Storage + H:** Build and independently review the integrated publication state machine. Include every durable boundary, both race orders, ACK loss, crash, replay, stale lease and unknown state.
5. **I + D + E + F + G + H + Storage:** Close the complete Forget inventory, lineage, derivative, recipient and restore anti-resurrection proof. Treat backup/restore as a first-class data path, not a later operational detail.
6. **C + G + H + I + D:** Freeze and prove the final request / Applied / Provider Outcome chain. Require actual adapter race and provider idempotency evidence before claiming submission safety.

### Priority 2 — Close recovery and evidence integrity / 优先级 2：关闭恢复与证据完整性

7. **A + Storage + I + D + C + H:** Prove COC/JF-10 composition while keeping their authority domains separate. Execute deterministic quorum, same-XID, split-brain, restore and fault campaigns.
8. **A + all Owners:** Make the exact-version ledger machine-checkable and continuously refreshed. A source Blob change must invalidate dependent approvals until re-reviewed.
9. **I + H + Storage:** Complete production trust profile, key custody, cross-language canonicalization, revocation and external anti-rollback.

### Priority 3 — Prove engineering and operational affordability / 优先级 3：证明工程与运维可承受

10. **A + designated engineering/operations authority:** Define a narrow pilot and a complexity budget. Start with one canonical authority, one PolicyDomain, one producer class, one derivative/index path, one Context/Adapter path and one provider. Do not introduce multi-PolicyDomain or multi-region complexity until the single-domain failure model is proven.
11. **Storage + engineering/operations:** Define topology, resource envelope, capacity, latency, retention, observability, runbooks, RPO/RTO, SLO and named on-call responsibility. Validate on representative workloads and fault scenarios.
12. **A + all Owners:** Only then recommend an architecture freeze disposition with explicit residual blockers and owner-signed acceptance.

---

## 9. Answers to the mandatory questions / 必答问题

### A. What are the ten most fundamental risks? / 当前最根本的十项风险是什么？

RSK-01 through RSK-10 above, ordered by system correctness, semantic authority, atomicity, security, integration, recovery, evidence freshness and operability.

### B. Which risks can invalidate system correctness? / 哪些风险可能使整个系统正确性无法成立？

RSK-01, RSK-02 and RSK-03 are direct correctness threats. RSK-04 and RSK-05 undermine the meaning and authorization of canonical operations. RSK-06 and RSK-07 can invalidate externally visible side-effect and recovery claims.

### C. Which architecture decisions have not closed? / 哪些架构决策没有闭环？

UAD-01 through UAD-10. The most immediate blockers are Fact/Claim ADR, D/Storage topology, I36 governance/global inventory, multi-PolicyDomain semantics, Applied/provider evidence, COC/JF-10 recovery and technology/operations.

### D. Which risks amplify during integration? / 哪些风险在模块集成时放大？

RSK-01/02/03/05/06/07/08. They cross independent authorities and durable ledgers. Their interaction can produce a globally invalid state even if each module's local contract is internally consistent.

### E. Which risks cause major implementation rework if deferred? / 哪些风险现在不处理会造成重大返工？

RSK-04 (identity/schema), RSK-05 (principal/scope/PolicyDomain), RSK-01 (transaction boundary), RSK-06 (final request and outcome identity), RSK-08 (version binding) and RSK-09 (signed proof projection and trust profile). These affect persistent IDs, migrations, wire schemas, APIs, transaction boundaries and audit evidence.

### F. Which risks block production deployment? / 哪些风险直接阻止生产部署？

RSK-01, RSK-02, RSK-03, RSK-05, RSK-06, RSK-07 and RSK-09. RSK-10 prevents a credible operability and capacity acceptance. Issue #7 and TAB-001 remain important engineering prerequisites, but absence of implementation is not treated as proof that the architecture itself is infeasible.

### G. Are there apparently safe mechanisms without verifiable proof? / 是否存在看似安全但没有可验证证明的机制？

Yes: serializable transaction, prepared XID, COC quorum, signed receipt, Applied ACK, private staging and fail-closed UNKNOWN. Their evidence ceilings are detailed in §4.2.

### H. Can individually correct modules compose incorrectly? / 是否存在模块分别正确、组合后却不正确？

Yes. Examples are detailed in §4.3: D/E/Storage publication, I/COC/Storage authorization, F/G restore after Forget, H/C/Storage version drift and G historical Applied versus current I authorization.

### I. Can architecture governance complexity exceed engineering value? / 架构治理复杂度是否可能超过工程收益？

Yes, this is RSK-10 and is rated High with Medium probability. It is a credible risk, not a verified conclusion. The system's safety requirements may justify substantial complexity, but no evidence yet demonstrates minimum sufficient protocol complexity, engineering capacity, operational staffing or a bounded end-to-end pilot. Simplification must be driven by threat model and evidence, not by deleting safety checks.

---

## 10. Overall gate disposition / 总体门禁结论

| Gate | R disposition / R 评估 | Reason / 原因 |
|---|---|---|
| G1 — Exact current source pins | PARTIAL / 部分通过 | Live Owner heads and selected Blobs were re-read, but source branches continue to advance and dependent approval refresh is not yet machine-enforced. |
| G2 — Authority and consumer acceptance | BLOCKED | Fact/Claim, I36 governance and exact cross-owner approvals remain open. |
| G3 — End-to-end state/causal model | BLOCKED | Integrated publication, Forget/restore and Applied composition are not proven as one model. |
| G4 — P0/P1 race, crash, recovery, identity and trust | BLOCKED | Bounded tests exist; integrated physical and trust proof is incomplete. |
| G5 — Technology/topology feasibility | BLOCKED | D/Storage topology ADR remains blocked; TAB-001 is candidate; production trust and operations are not accepted. |
| G6 — Chinese/English semantic parity | PARTIAL / 部分通过 | Current reviewed artifacts contain bilingual peers, but full repository-wide semantic parity is outside this R snapshot and must be independently checked at PR acceptance. |
| G7 — A integration disposition and independent Owner decisions | BLOCKED | Existing A Phase 2 is preliminary; role simulation is not independent Owner approval. |
| G8 — Architecture freeze recommendation | **NOT READY** | Critical and High risks remain open or unproven. |

### 10.1 Final status classification / 最终状态分类

**VERIFIED / 已核实**
- Repository main and live Owner branch HEADs recorded in this report were fetched from GitHub.
- Selected source Blobs and the open issue states listed above were read back.
- The B Fact/Claim ADR explicitly remains blocked.
- The Storage D/Storage topology ADR explicitly has no selected deployed topology.
- Issue #3 explicitly says Applied Contract Frozen = NO.
- Issue #5 explicitly keeps I36-GOV-01..10 governance-blocked.
- Issue #10 records Gate A PARTIAL PASS/OPEN and Gate B/C blockers.
- The cited H Actions runs report successful completion for their bounded test commits.

**PARTIALLY VERIFIED / 部分核实**
- Owner-local semantic contracts for producer registration, publication, authorization, provider egress, Context, restore and signed projections exist.
- Bounded H schema/reference suites and PostgreSQL capability probes have passed as recorded, with explicit evidence ceilings.
- C has accepted the H 1.2.13 / CSubmitOutcome 1.0.1 mapping as an L1/L2 candidate, not a production freeze.

**NOT PROVEN / 尚未证明**
- One physical linearization domain actually composes D fence and Storage final visibility.
- Complete integrated cross-owner publication correctness under every required race/crash/ACK-loss condition.
- End-to-end Forget and restore anti-resurrection across all producers, derivatives, recipients and backups.
- Full Applied/provider outcome correctness at a real provider adapter.
- Live persistent COC/JF-10/owner-ledger recovery as one system.
- Production trust, key custody, anti-rollback and operational acceptance.
- Whether total architecture complexity is affordable for the eventual engineering/operations team.

**BLOCKED / 阻塞**
- Fact/Claim ADR-001.
- Storage/D physical serialization topology.
- I36-GOV-01..10 and Global Forget governance/inventory decisions.
- Multi-PolicyDomain atomicity.
- Applied contract freeze.
- JF-10 P0 Gate B/C and production activation.
- Canonical implementation repository/engineering owner designation and TAB-001 technology freeze.

---

## 11. Scope limits and non-claims / 范围限制与非声明

1. This report is an architecture risk assessment, not an implementation, security certification, legal/privacy approval or production readiness certificate.
2. A–I and Storage HEADs are snapshots taken during this review. They must be re-fetched before a later acceptance decision.
3. Owner-role simulations are not independent Owner approvals. This report does not manufacture such approvals.
4. A CI success is reported only for the exact run and commit cited; it is not generalized to other revisions or production.
5. No production provider, database topology, COC cluster, HSM/KMS, operator team or deployment environment is assumed.
6. No Owner-owned normative artifact was modified by this assessment. Remediation recommendations preserve each Owner's decision authority.
7. Architecture freeze, merge, Gate closure and production activation are not authorized by this report.

---

## 12. R sign-off / R 评估签署

**R disposition: NOT READY FOR ARCHITECTURE FREEZE.**

The project should proceed by resolving root correctness prerequisites before adding further protocol detail or starting implementation-dependent work. The highest-value next step is not another broad documentation expansion. It is an Owner-authorized decision and proof package for (1) Fact/Claim semantics, (2) D/Storage physical serialization, (3) I governance/inventory, and (4) the integrated publication/Forget/recovery state machine.

**R 最终意见：不具备架构冻结条件。**

项目应先解决根本正确性前置条件，再继续增加协议细节或进入依赖实现的工作。当前价值最高的下一步不是继续大规模扩充文档，而是由责任 Owner 完成以下决策与证明包：

1. Fact/Claim 领域语义决议；
2. D/Storage 物理序列化拓扑决议；
3. I 身份治理与全局 Inventory 决议；
4. 发布、Forget 和恢复的集成状态机证明。

This report does not close Issue #43 or any Owner gate. It is submitted for independent review and reconciliation with A's Phase 2 integration report.

本报告不关闭 Issue #43 或任何 Owner Gate，提交目的为独立复审，并与 A 的 Phase 2 集成报告进行收敛。
