# E Owner Acceptance — A Context Optimization / Observation Archive

- Owner: E — Memory Compiler Architect
- Decision: **ACCEPT WITH CONDITIONS**
- Reviewed A commit: `6caa6034c92c4d3dcf7b2d34ca899b62c3756f1f`
- A live branch HEAD re-queried: `a480a713db358b30dc4cf7c9157025b3c116e439`; decision is pinned to requested commit.
- E branch: `session-e-memory-compiler-2026-11-16`; observed pre-write HEAD: `541f7b50f0e52021d6cb892318cc581d2cd8cde3`.

## 1. Exact A artifacts reviewed

| Path | Blob SHA |
|---|---|
| reviews/integration/nvidia-context-optimization-system-integration-review.md | `b53db1ecb7830a7f1057d09c8ef73aceab942cea` |
| reviews/integration/context-optimization-system-contract-candidates.md | `55257bdf85a56a78df96b797b063bc49d91f5a6d` |
| reviews/integration/context-optimization-conformance-plan.md | `1c941c3e55be1e539a76ef89f297c168296c7db2` |
| reviews/integration/context-optimization-owner-decision-register.md | `36581cf286ddf2516f571eb823fddc9cf8707d80` |

## 2. E baseline / dependency evidence

Reviewed E `04-memory-compiler/forget-fence-and-derived-registration.md` (Blob `00e37ba56596e710513c8d0568acd79141d9101b`) and `04-memory-compiler/phase-3.6-joint-producer-publication-decision.md` (Blob `aaa15de9d6e3a6ce74b11fda376369d6a49659ab`). E's contract explicitly says D/E/Storage atomic registration and final publication gate remain OPEN/BLOCKING; its joint decision records architecture only and runtime/fault tests NOT RUN.

## 3. Formal decision and accepted boundary

E accepts A's separation and prohibition:
- F Archive metadata/catalog/cache is not E's Canonical Index.
- Runtime Archive observation and ReadReceipt are not Canonical Memory or Canonical Evidence by default.
- G TSS, Context compaction, CompactionLineage and LossLedger are G Context projections/audit records, not canonical publication authority.
- Any output intended to become Canonical Derived Artifact must be admitted as E compiler work, have complete immutable transitive lineage registered with D, pass current I authorization/PermissionEpoch and D ForgetFence checks at the authoritative final Publication Gate, and become visible only after atomic durable publication receipt.
- Compaction alone never grants Canonical Derived Registration or publication rights.

Compiler-managed objects may include extraction/normalization proposals, derived propositions, embeddings/indexable derivatives and canonical-derived summaries *only when explicitly admitted through E's producer/work contract*. Runtime-only Archive pages, F cache entries, G TSS/ContextVersion/DeliveryIntent, ReadCursor/ReadReceipt, and G compaction snapshots are not E canonical artifacts. If E consumes any of these as sources for canonical compilation, E records exact source identity/revision/hash, Scope, epistemic status and transitive lineage; it does not acquire their lifecycle authority.

## 4. Publication gate requirements

Before visibility, the final gate must validate atomically at one authoritative serialization point:
1. stable root WorkItemId / producer registration receipt and complete target/producer classification;
2. current AttemptId + LeaseEpoch; stale workers cannot stage/publish/terminalize;
3. immutable ArtifactId/digest and DerivationRunId;
4. complete dependency set digest, exact source revisions/hashes and transitive ancestors;
5. D ForgetFence/current generation and barrier admission/terminality;
6. I PermissionEpoch/current authorization for actor, source, target, purpose and scope;
7. no missing/unknown/revoked/forgotten/expired/stale source or dependency receipt;
8. durable atomic visibility marker + PublicationReceipt + required outbox/receipt-consumption evidence.

Staging, queue acceptance, compiler completion, object-store existence, local provenance, registration request/receipt alone, or outbox delivery is not publication. Unknown/ambiguous gate outcome remains private and must be reconciled from durable authoritative receipt. A changed dependency set requires a new registration receipt. Same idempotency key + same digest returns prior result; same key + different digest conflicts.

Forget after publication must suppress canonical reads and all registered derivatives under D/I authority; replay, rebuild, retry, reconnect or restore must not republish. E cannot declare global Forget completion or physical erasure.

## 5. Cross-owner findings

- **B↔E:** typed references and epistemic semantics are B-owned; E stores them losslessly as lineage inputs but does not redefine domain truth. A source locator is not a compiler artifact identity.
- **C↔E:** G compaction output used in Agent Context remains non-canonical. If a separately requested canonical derivative is produced, it enters E's producer/work admission and D gate; Agent delivery or C Applied evidence cannot substitute for publication.
- **E↔H:** BMCP may report derived artifact visibility/status only from authoritative D/E publication receipts. Transport ACK, Recall receipt, or local cache visibility cannot claim canonical publication.
- **D/Storage:** atomic D registration + final gate transaction semantics and recovery remain unresolved; architecture-only acceptance does not supply an executable API or database proof.

## 6. P0 / P1

**P0**
- D/E/Storage atomic dependency registration + final visibility gate is explicitly OPEN/BLOCKING.
- No proof that gate and Forget fence have one defensible serialization/linearization point or crash recovery outcome.
- No executable negative test evidence for missing lineage, stale PermissionEpoch, fence race, post-Forget replay or ambiguous commit.

**P1**
- F archive and G compaction producer classes/targets need D/I classification and registration policy; runtime-only vs canonical-derived must be explicit.
- B's Observation/Evidence/DerivedSummary semantics and G's CompactionLineage/LossLedger need stable typed mapping.
- H protocol needs distinct non-canonical archive/read states versus canonical publication states; no ACK may infer publication.

## 7. Required negative tests — NOT RUN

| # | Preconditions / sequence | Expected protocol + Agent behavior | Retry / evidence | Status / owner |
|---|---|---|---|---|
| 1 | ReadReceipt exists, no application | No canonical effect; Agent application separate | Receipt only, no publication/applied record | NOT RUN; F/C |
| 2 | Adapter delivery retry | No compiler publication side effect; stable delivery dedupe | delivery/attempt IDs | NOT RUN; C/H |
| 3 | Context v superseded by v+1 | Old G projection not republished as canonical | Context supersession evidence | NOT RUN; G/C/H |
| 4 | Offline reconnect contains old derived payload | H suppresses; E/D gate refuses any replayed publish | fence, registration and gate receipt | NOT RUN; H/D/E/I |
| 5 | ACK success but evidence missing | No compiler state advancement | stage-specific ACK + missing evidence | NOT RUN; H/C |
| 6 | Cursor crosses ContextVersion | Reject at F/H; no compiler side effect | session/cursor binding | NOT RUN; F/H |
| 7 | Source revision changed | Dependency mismatch; recompile/re-register, never silently reuse | source revision/hash and new dependency digest | NOT RUN; E/B/F |
| 8 | G compaction summary incorrectly registered as canonical | Reject unless separately admitted as E WorkItem with full lineage and D gate | producer class, work ID, gate denial | NOT RUN; E/D/G |
| 9 | Publication request omits ancestor | Keep staged/private; reject incomplete set | dependency completeness receipt | NOT RUN; E/D/Storage |
| 10 | Forget then old artifact replay | Suppress; no visibility pointer/outbox republish | fence/barrier and gate trace | NOT RUN; D/E/I/Storage |
| 11 | Client ignores STALE status | No stale source can enter compiler input; fail closed | typed stale failure and compiler rejection | NOT RUN; F/E/H |
| 12 | duplicate work request | same key+digest returns same receipt; no duplicate artifact | WorkItemId, AttemptId, digest | NOT RUN; E/D |
| 13 | timeout during publication commit | pending/unknown until receipt reconciliation; never report published optimistically | prepared-XID/receipt/visibility state | NOT RUN; E/D/Storage |
| 14 | permission revoked during compile | gate denies; staged data remains private/quarantined | PermissionEpoch and denial receipt | NOT RUN; I/E/D |
| 15 | recall succeeds, delivery fails | no effect on canonical publication; Context delivery separately fails | Recall and Delivery records distinct | NOT RUN; F/G/H/E |

## 8. Cross-owner dependencies, freeze and implementation

Requires D/Storage exact atomic registration/publication semantics; I authorization and revocation currentness; B stable typed source/epistemic semantics; F/G classification of runtime versus canonical derivatives; H protocol status mapping; C separation of Context application and canonical publication.

**Interface freeze:** NOT APPROVED. E accepts authority separation and publication safety invariants, not executable registration/gate schema.
**Implementation:** NOT AUTHORIZED. E36 and fault/recovery suites remain NOT RUN.
**Next gate:** D/E/Storage pin atomic API, transaction owner, linearization and recovery; I/B/F/G pin producer/target/lineage semantics; H maps canonical publication result as a separate protocol family.
