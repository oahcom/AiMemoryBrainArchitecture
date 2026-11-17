# Canonical Domain Invariants
# 规范领域不变量

- ID: B-INVARS-001
- Status: CANDIDATE INVARIANT SET — NOT EXECUTED
- Source baseline: main @ b372b62c640a2b656e54b6db62a4ee67d7d8c001
- Owner boundary: B defines domain-level invariants; D/E/F/G/H/I/Storage define and execute owner-local enforcement.

## 1. Identity invariants / 身份不变量

| ID | Invariant | Positive condition | Negative condition |
|---|---|---|---|
| ID-001 | Identity is stable across ordinary content mutation | Memory label/content/version changes retain MemoryId | Recompute ID from content or digest |
| ID-002 | Assigned canonical IDs are never silently reused | Retired/forgotten ID remains historical and non-reassignable | Reassign an old ID to a new object |
| ID-003 | Version identity is distinct from aggregate identity | MemoryVersion references stable MemoryId and unique version ID | Treat MemoryVersionId as new MemoryId |
| ID-004 | Typed refs preserve type and namespace | Consumer resolves ActorRef only as ActorRef in declared namespace | Cast PrincipalRef/AgentRef/ScopeRef through untyped string |
| ID-005 | Ref is not proof of identity or permission | Verifier + I registry resolve identity; I authorizes action | Payload-supplied ActorRef authenticates caller |
| ID-006 | Cross-tenant identity resolution is explicit | Issuer/security domain/tenant namespace matches authoritative mapping | Resolve by subject string alone |

## 2. Relationship invariants / 关系不变量

| ID | Invariant | Positive condition | Negative condition |
|---|---|---|---|
| REL-001 | Relation endpoints satisfy type constraints | Relation type allows both endpoint kinds | Attach a Memory to a Person-only relation |
| REL-002 | Derivation direction is explicit | Target has source refs and lineage | Source/target reversed or ambiguous |
| REL-003 | Derived object has complete lineage or explicit gap | All direct/transitive source versions resolved, or unavailable reason recorded | Publish a derivative with unknown required ancestry |
| REL-004 | Unapproved derivation cycles are rejected | Graph is acyclic under current candidate policy | Create cycle without explicit approved semantics |
| REL-005 | Reference is not ownership or permission | Cross-scope link is separately authorized | Infer access from graph adjacency or parent scope |
| REL-006 | Context entry binds exact source version | Entry references exact MemoryId + MemoryVersionId | ContextVersion scalar used as MemoryVersion |

## 3. Temporal invariants / 时间不变量

| ID | Invariant | Positive condition | Negative condition |
|---|---|---|---|
| TMP-001 | Temporal axes are non-interchangeable | Occurred/Observed/Recorded/Valid/Transaction times retain separate meanings | One timestamp populates all fields |
| TMP-002 | Unknown time is explicit | Unknown/approximate retains source text and precision | Missing time interpreted as epoch/always-valid |
| TMP-003 | Valid Time and Record/Transaction Time histories remain distinct | Query can distinguish valid-at T from known-by T2 where supported | Backdated correction overwrites historical knowledge |
| TMP-004 | Temporal correction is provenance-bearing | New immutable assertion/revision records reason and source | Silent mutation of historical Valid Time |
| TMP-005 | Time order is not inferred from independent clocks alone | Causal order uses owner-authoritative cursor/receipt | Wall-clock comparison substitutes for causal proof |

## 4. Evidence and provenance invariants / 证据与溯源不变量

| ID | Invariant | Positive condition | Negative condition |
|---|---|---|---|
| EVD-001 | Verified Claim requires evidence and method | Claim references evidence and verification method | Confidence score alone promotes to Verified |
| EVD-002 | Evidence role/strength is Claim-relative | Link records support/refute/qualify role per Claim | Evidence has one global strength reused for all Claims |
| EVD-003 | Source, Evidence and Provenance are distinct | Source origin, evidence material and derivation trace are independently identified | Derived summary is represented as original source |
| EVD-004 | Provenance names exact inputs where available | Input object/version/digest/method version recorded | Model/method guessed after the fact |
| EVD-005 | Unavailable evidence is not nonexistence | State records expired/forgotten/external unavailable | Missing blob treated as proof that source never existed |
| EVD-006 | Forget retention does not preserve forgotten plaintext | Only permitted non-reconstructive audit metadata retained | Provenance excerpt/digest side channel reconstructs forgotten content |

## 5. State invariants / 状态不变量

| ID | Invariant | Positive condition | Negative condition |
|---|---|---|---|
| ST-001 | State is typed by subject and owner | Memory lifecycle uses Memory state machine | Universal status enum used for all entities |
| ST-002 | Epistemic status is independent from Memory lifecycle | Active Memory may contain Disputed Claim | Memory Active interpreted as Claim Verified |
| ST-003 | Terminality is owner-defined | Transition checks subject's exact state machine | Same-named state from another module is assumed equivalent |
| ST-004 | Forgotten is not a ForgetOperation phase | D operation phases separate from Memory Forgotten lifecycle | Memory.status = Forgetting treated as canonical |
| ST-005 | Applied, Recorded, Committed, Visible and Published are distinct | Each requires correct issuer/evidence | ACK/COMMIT_WON/local state treated as Published or Applied |
| ST-006 | Unknown is not success | Unresolved outcome remains Unknown/InDoubt/Blocked | Timeout/lost ACK converts to success |

## 6. Forget and deletion invariants / 遗忘与删除不变量

| ID | Invariant | Positive condition | Negative condition |
|---|---|---|---|
| FGT-001 | Forget is not ordinary Delete | D ForgetOperation/Fence governs suppression and lineage | Generic row deletion called Forget |
| FGT-002 | Request, authorization, decision, execution and proof are distinct | Request ref, I decision, D fence, per-target receipts and I global result separate | One status field represents whole Forget |
| FGT-003 | D suppression is not global completion | D CanonicalSuppressionComplete scoped to D barrier | D declares all backups/external copies erased |
| FGT-004 | Logical suppression is not physical purge | Storage/backup operator emits target-scoped purge proof | Missing row/tombstone treated as physical erase |
| FGT-005 | No resurrection by new ID/content equality | New ingestion checks active fences and lineage/source ancestry | Same content reintroduced with new ID bypasses Forget |
| FGT-006 | Historical evidence does not authorize current use | Applied/history retained under I policy but current-use eligibility recomputed | Old Applied/ACK authorizes resend after revocation/Forget |

## 7. Operation and protocol invariants / 操作与协议不变量

| ID | Invariant | Positive condition | Negative condition |
|---|---|---|---|
| OPR-001 | Protocol object is not domain operation | Request references an operation ID/type | Request payload itself becomes canonical Memory |
| OPR-002 | Receipt proves only declared boundary | Receipt includes issuer, scope, operation, version and result | ACK expanded beyond declared coverage |
| OPR-003 | Retry preserves logical identity and digest | Same key+same digest idempotent; changed digest conflict | Retry creates new operation to evade fence |
| OPR-004 | Owner-local cursors/epochs are typed | D cursor, I PermissionEpoch, F watermark, G version, Storage XID kept separate | Compare unrelated counters as global order |
| OPR-005 | Publication requires Storage authority | VisibilityPointer and PublicationReceipt read back | I COMMIT_WON or E local Published state exposes bytes |

## 8. Authentication and physical-order invariants / 认证与物理顺序不变量

| ID | Invariant | Positive condition | Negative condition |
|---|---|---|---|
| AUTH-001 | C origin signature, H transport authentication and I authorization are separate | Each is verified by its authority and bound to exact message/context | Treat payload sender claim or H gateway receipt as C origin proof |
| AUTH-002 | C object P0 and outer-envelope P0 are distinct | Both are independently computed/verified under exact profile and object | Reuse C object P0 as outer-envelope P0 without explicit approval |
| AUTH-003 | Missing trust evidence is UNKNOWN, never VALID | Missing profile/key history/anti-rollback/principal fails closed | Treat absent trust data as permissive |
| AUTH-004 | Protected transport context is verifier-produced | Context is constructed only by authenticated adapter and bound to channel/session | Caller constructs context from payload claims |
| AUTH-005 | Replay reservation is durable and ordered | Reservation/acceptance/prior-result publication have explicit crash-safe semantics | In-memory replay set or reserve before required auth checks |
| SER-001 | SerializationRevision is local to one physical anchor | Revision compares only within one AuthoritySerializationAnchorRef | Compare to D FenceGeneration, I PermissionEpoch, C sequence, COC position or XID |
| SER-002 | SerializationTransitionRef idempotency includes immutable digest | Same ref/same digest replays same result | Same ref/different digest silently accepted |

## 9. Candidate executable test catalogue / 候选可执行测试目录

| Test ID | Setup | Expected result | Owner |
|---|---|---|---|
| T-ID-01 | Change Memory label/content and create next version | MemoryId stable; MemoryVersionId new | D/Storage |
| T-ID-02 | Reuse retired ID under different object | Reject | B/D/Storage |
| T-ID-03 | Submit forged PrincipalRef/ActorRef in payload | Not authenticated; fail closed | H/I |
| T-REL-01 | Relation with disallowed endpoint type | Reject with invariant ID | B/E |
| T-REL-02 | Derived artifact missing ancestor source version | Quarantine/private | E/D/Storage |
| T-TMP-01 | Event occurred before observation and later durable recording | All time axes remain distinct | C/E/D |
| T-TMP-02 | Approximate time “early May” | Preserve uncertainty/source text; no exact fabricated instant | E |
| T-EVD-01 | Mark Claim Verified without evidence/method | Reject | E/D |
| T-EVD-02 | One Evidence supports and refutes different Claims | Per-link roles retained | B/E |
| T-ST-01 | Active Memory contains Disputed Claim | Valid; lifecycle and epistemic dimensions independent | D/F |
| T-ST-02 | I COMMIT_WON but Storage participant not committed | Not Published; remain private/unknown | I/Storage/E |
| T-ST-03 | Context delivered ACK without C final submit proof | Not Applied | H/C/G |
| T-FGT-01 | D fence wins before derived publication | Reject/quarantine; no visibility | D/E/Storage |
| T-FGT-02 | D suppression completes but backup target unresolved | Not global Forget complete | D/I/Storage |
| T-FGT-03 | Reimport same forgotten source under new Memory ID | Block by lineage/fence policy | D/E/I |
| T-OPR-01 | Same operation key with changed digest | Conflict | Owner operation |
| T-OPR-02 | Compare PermissionEpoch with ForgetFenceGeneration | Type error/reject | I/D/B |

## 10. Validation status / 验证状态

- Test specifications: recorded above.
- JSON Schema: NOT CREATED; core identity/Fact-Claim/Applied schemas are not stable enough to freeze.
- Executable tests: NOT RUN; this repository is an architecture definition repository and Issue #7 identifies runtime implementation location/owner as unresolved.
- Property-based tests: TO_VALIDATE after nominal type/identity and state machine decisions stabilize.
- Fault injection: NOT RUN; JF-10 P0 remains open (Issue #10).

## 11. Gate status / 门禁状态

B4 is NOT READY. Invariants are candidate and owner-scoped; test specifications are not executable proof. No schema or runtime conformance is claimed.

B4 尚未就绪。不变量仍为候选且按 Owner 划分；测试规范不是可执行证明。不宣称 Schema 或运行时一致性。
