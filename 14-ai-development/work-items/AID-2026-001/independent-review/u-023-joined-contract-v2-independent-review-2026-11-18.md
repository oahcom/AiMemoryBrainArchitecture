# AID-2026-001 U-023 — Joined Contract v2 Independent Review

- Review type: independent read-only content / governance review; report is evidence supplement only
- Repository: oahcom/AiMemoryBrainArchitecture
- Reviewed branch: remediation/aid-2026-001-forget-contract-closure-2026-11-18
- Frozen review Head: 5b12fdcc50fb7173dd44d8d2c9bad4dda08c42ad
- Parent: 0fd19d60b3698adf2b6de343e99df39d5031aac5
- Reviewed artifact: 14-ai-development/work-items/AID-2026-001/forget-lifecycle-joined-contract-proposal-v2.md
- Reviewed Blob: 28ce1f735be6781b8de32a310d50e24cb457f01e
- UTF-8 bytes independently counted from fetched content: 41927
- Commit metadata author login: oahcom; human author identity: UNVERIFIABLE; no author claim relied upon
- Conflict of interest: none identified
- Governance inputs read: AI-EXEC-001 v1.0 Blob d9fbdca4542ded8977c9092e6b8276cc4fdbed6a; AI-EXEC-002 v1.0 Blob c1d1e5bffe0a92af701e59c7f2627350b1d9fddf; GOV-DOC-001 v1.0 Blob b51b054b9f1022133666542680df74dfe19de2fb
- Comparison inputs read: U-010 Blob e12bc3beaf7327f7646fa090cb1fe2cda023cacf; U-011 EN Blob c9daf61a538a175718e1bb492797cb2b5a51547a; U-011 ZH Blob d03d26bbdc96ee9df7f532144d331a3a06be3866; D/I matrix Blob 6c6b3715f95f0aa9c29ad2fd42d15d8b2bae77b2; v1 Blob 96882570d44f6a3c6d60a30b1edb0e405bde5efc; Owner D v2 prompt Blob 7005788694b4f89513c62a5d58adcfa74b6c14ec; Owner I v2 prompt Blob abf8551e37580f1e18a8f956ba453d88918a87b2

## 1. Verdict

**GOV-DOC-001: FAIL.**

The v2 text materially improves the G-04 content and correctly preserves the core Forgotten trigger, but it does not satisfy the repository's bilingual-document structure and review requirements. It also drops several already-present v1 normative requirements, so the delta is not limited to additive completion. The I-U011 test mapping is not a faithful T01–T16 crosswalk.

This is a document review only. It is not Owner D approval, Owner I approval, same-SHA bilateral approval, Storage approval, implementation evidence, R3 test evidence, integration acceptance, or production authorization. AID-2026-001 remains BLOCKED_PENDING_R3_EVIDENCE.

## 2. Eight mandatory deliverables — independent disposition

| # | Mandatory deliverable | Result | Evidence / reason |
|---|---|---|---|
| 1 | Bilingual joined contract v2 | REJECT | One combined file exists, but GOV-DOC-001 §4 requires both Chinese and English files for every changed architecture document; §3/§7 require reciprocal links and linked counterparts. The v2 file has no separate EN/ZH counterpart paths or reciprocal links. |
| 2 | Complete D state-machine crosswalk | REJECT | The 11-phase set and phase-to-phase transition table exist, but v2 omits the v1 phase-to-Memory/public-result crosswalk and several D-owned semantics: CompletedWithPolicyException projection, detailed target-state vocabulary, and complete retry/checkpoint/idempotency behavior. |
| 3 | I authorization envelope/receipt, PermissionEpoch and revocation races | ACCEPT — document specification | §§3.1–3.4 specify signed envelope fields, verifier/operation/transaction-bound receipt, monotonic epoch vector, authoritative serialization-point currentness, COMMIT_WON / REVOCATION_WON / UNKNOWN, and nine commit-time checks. No implementation or race execution is implied. |
| 4 | Governance exceptions and per-target evidence | ACCEPT — document specification | §§4.1–4.4 specify deny/defer default, designated I authority, immutable exception fields, bounded effect, inventory policy/seal/invalidation, and append-only target evidence/provenance. No case-specific approval or discovery attestation is implied. |
| 5 | DFI ↔ I-U011 test mapping | REJECT | §6.2 changes the meanings/positions of original I-U011 test IDs and omits original T12 and T15 assertions. DFI-013…022 are collapsed into one grouped row rather than individually mapped. |
| 6 | Bilingual item-by-item semantic verification | REJECT | The DFI and I-U011 tables in §6 are English-only. The file's §7 assertion of item-by-item parity is not sufficient evidence and is contradicted by the missing Chinese test tables. |
| 7 | New Blob SHA / UTF-8 bytes / commit SHA | ACCEPT | Exact branch Head/commit, Blob SHA and 41,927 UTF-8 bytes were independently fetched/read back and the byte count recomputed. |
| 8 | Closure evidence for every G-04 sub-gap | REJECT | A–I have substantial textual coverage, but C retains an unguarded transition ambiguity and J is incomplete/mis-mapped. A table asserting closure evidence does not cure the underlying omissions. |

## 3. G-04 A–J independent assessment

| Gap | Result | Clause-level basis |
|---|---|---|
| G04-A | ACCEPT — document content | §2.1–2.2 includes AuthorizationPending and Blocked in the 11-phase set and supplies EN/ZH transition tables. |
| G04-B | ACCEPT — document content | §2.1 establishes DomainCompletionEvaluated as canonical and prohibits persisted/API/test use of CompletionEvaluated. This matches the U-010 terminology. |
| G04-C | PARTIAL — retain open | §2.3 defines Failed as terminal for a failed attempt, preserves operation_id, creates attempt_id, appends event history, and requires explicit recovery/reconciliation for Failed → CleanupInProgress. However, §2.2 also permits Failed → DomainCompletionEvaluated without an equivalent explicit recovery guard, reconciliation requirement, or stated event precondition. The recovery model is therefore not fully closed. |
| G04-D | ACCEPT — document content | §§3.1–3.2 contain issuer/key version, subject/effective actor, delegation, action, exact scope/targets, purpose, policy context, PermissionEpoch, decision, validity times, request_hash, audience, nonce, provenance/signature; receipt binds verifier identity/version, operation, transaction/serialization, epoch vector, trusted times and integrity evidence. |
| G04-E | ACCEPT — document content | §3.3 defines monotonic/non-reused PermissionEpoch, authoritative current vector at serialization, complete multi-principal vector, and all three winner outcomes. Storage proof remains a separate gate. |
| G04-F | ACCEPT — document content | §3.4 enumerates nine checks and expressly states authorization only permits the commit; it does not require downstream cleanup/governance completion. I authorization remains a precondition, not the Forgotten trigger. |
| G04-G | ACCEPT — document content | §§4.1–4.2 include named approving I authority, authenticated principal, role/authority basis/delegation, operation, exact targets/data classes/systems/regions/scope, policy ID/version, jurisdiction/basis, decision status, rationale, permitted/prohibited actions, residual exposure, controls, evidence integrity, decision/effective/expiry times, next review, accountable owner, reevaluation triggers and expiry/revocation follow-up. |
| G04-H | ACCEPT — document content | §4.3 specifies policy ID/version/revision, applicability, mandatory target classes/actions, exclusions, accepted evidence/freshness/provenance, unsupported-capability escalation, seal criteria and invalidation triggers. |
| G04-I | ACCEPT — document content | §5 separates PerTargetResult, ExceptionDecision, GovernanceAssessment, DDomainCompletion, MemoryLifecycle and PhysicalErasureEvidence; ExceptionApproved ≠ Succeeded is explicit. |
| G04-J | REJECT — incomplete mapping | §6.2 does not preserve the source U-011 test-ID/scenario mapping. Original T12 (unknown/unsupported/unregistered required target) and T15 (target evidence present but D-domain completion absent) are absent as such. Several later IDs are shifted, duplicated or repurposed. |

## 4. Exact comparison findings

### 4.1 Core trigger and authority — PASS

v2 §1 says: “A successful, durable SuppressionCommitted is the sole trigger” for the atomic Forgotten transition; I authorization is a “mandatory pre-commit condition, not the trigger”; I governance completion is “not a precondition for Forgotten.”

This agrees with U-010 §1 and §3.2–3.4, which state that Forgotten occurs at successful durable SuppressionCommitted, that I authorization is a precondition, and that post-commit cleanup, D completion and I governance remain separate. It also agrees with U-011 §1.3. No regression was found in this core invariant:

SuppressionCommitted ⇒ Forgotten; no resurrection; I authorization is precondition only; I governance completion is not a Forgotten precondition.

v2 §10 preserves the same-exact-content-SHA D/I approval requirement. The candidate remains PROPOSED and non-normative.

### 4.2 v1 semantic regression — FAIL

The v2 change is not limited to filling G-04. The following v1 requirements are absent or materially weakened in v2:

1. **Reauthorization before each irreversible/protected stage.** v1 §6.4 requires current principal/delegation, PermissionEpoch/authorization, scope, retention/legal hold, policy version, fence generation and target ownership/capability to be rechecked before each irreversible or protected stage. v2 §3.4 defines the nine checks at the SuppressionCommitted serialization point; §2.3 mentions current checks for a recovery action. It does not preserve the general per-stage reauthorization requirement.
2. **Request idempotency.** v1 §6.1 scopes the request key by authenticated principal, effective Scope, target identity and operation type; defines the canonical request hash; requires same-key/same-hash reuse and same-key/different-hash IDEMPOTENCY_CONFLICT. v2 has no equivalent normative rule. DFI-007 merely states the expected test assertion.
3. **Checkpoint and lease fencing.** v1 §6.2 defines checkpoint identity as operation_id + inventory_revision + target_id + stage + action_version, unique attempt IDs, lease owner, monotonic lease_fence, stale-worker rejection and serialized/CAS concurrent retry. v2 §4.4 retains attempt_id/lease_fence as evidence fields, but does not retain these execution rules. DFI-008 is an assertion without the normative mechanism/guard.
4. **Retry classes and reconciliation.** v1 §6.3 distinguishes retryable, reconcile-before-retry and terminal conditions, and prohibits blind retry of uncertain non-idempotent physical actions. v2 §2.3 only covers selected recovery/reconciliation cases; the complete classification is missing.
5. **Governance-compliance predicate.** v1 §5.1 defines ten required conditions for I to record Compliant, including current authorization/policy, sealed inventory, all target terminal evidence, suppression at mandatory boundaries, derivative cleanup, controlled storage/replica requirements, backup expiry/bounded exception, recipient evidence, audit integrity and no unresolved hold/unknown/unsupported target. v2 §5 gives general type and exception rules but omits this full predicate.
6. **CompletedWithPolicyException projection.** v1 §§3.1–3.2 and §5.3 define this only as a derived public projection when D-domain result is Completed AND I GovernanceAssessment is CompliantWithException. v2 does not preserve that explicit condition.
7. **Public status projection.** v1 §5.4 requires API/UI to expose D result, I assessment and per-stage status distinctly and prohibits collapsing partial success into “deleted everywhere”/“Forget complete”. v2 has typed facts, but no equivalent public projection rule.
8. **Target-state vocabulary.** v1 §4.1 enumerates target_state values such as pending, in_progress, suppressed, cleaned, erased, expired, quarantined, acknowledged, policy_retained, failed and unknown, plus target_class and required_action vocabularies. v2 §4.4 retains a target_state field but does not define its value set or carry forward the full field vocabulary.

The v2 additions to authorization envelope, receipt, epoch races, Legal Hold, inventory sealing and result typing are useful. They do not justify silently dropping the above v1 rules. Restore these requirements in v2 or explicitly mark each proposed change as a deliberate, owner-approved semantic change; the latter cannot be decided by this review.

### 4.3 I-U011-T01…T16 mapping — FAIL

The original U-011 §8 mapping includes:
- T12: required target unknown/unsupported/unregistered → GovernanceAssessment cannot be Compliant.
- T13: new target/inventory or policy revision after assessment → prior assessment invalidated; reassess.
- T14: exception expiry/revocation or hold change → reassess; no silent renewal.
- T15: all target evidence present but D-domain completion absent → I must not declare D completion.
- T16: D Forgotten committed while cleanup remains pending → Forgotten remains terminal; governance remains separately pending/noncompliant as applicable.

v2 §6.2 instead maps:
- T12 to the T13 inventory-change scenario;
- T13 to the T16 Forgotten/cleanup-pending scenario;
- T14 to a new missing-receipt-field scenario;
- T15 to a duplicate/subset of request purpose/scope mismatch and nonce replay;
- T16 to the original T14 exception expiry/revocation scenario.

Consequently, original T12 and T15 are not represented under their required assertions, and the original IDs no longer map faithfully to the source specification. T14's added receipt-field check is useful but must not displace the original cases. DFI-013…022 are likewise grouped into a single row, so there is no individual test-ID-to-clause/scenario/expected-result mapping for those ten cases.

### 4.4 Bilingual semantic and structural review — FAIL

GOV-DOC-001 v1.0:
- §3 requires the same requirements, failure modes, state machines, examples, tables and acceptance criteria, plus reciprocal links and exact source traceability.
- §4 requires both Chinese and English files for each new or changed architecture document and a terminology/status parity check.
- §7 requires both language versions to exist and be linked, stable identifiers/statuses to match, and review evidence to be recorded.

v2 is one combined file and has no separate EN/ZH counterpart paths or reciprocal links. More concretely, §6.1's DFI table and §6.2's I-U011 table are English-only; the scenarios and required assertions have no Chinese counterpart. Therefore the single-file layout and missing translated test tables do not meet the cited GOV-DOC-001 requirements. The claim in §7 that the pair has been verified item-by-item cannot substitute for the absent counterpart material.

Within the paired clauses that are actually present in both languages, no material normative drift was found in the sampled core rules: phase names/transitions, DomainCompletionEvaluated, Failed recovery wording, signed envelope/receipt, PermissionEpoch, the three winner outcomes, nine checks, Legal Hold exception fields, inventory seal/invalidation, typed results, ExceptionApproved ≠ Succeeded, same-SHA approval and non-claims. This limited sample does not change the overall FAIL.

## 5. Finding disposition

All findings below use the required three fields: ID + severity + return carrier.

### Existing U021 findings

- **U021-G04-001 — P1 — Issue #41 — KEEP OPEN.** The candidate contains substantial textual coverage for G04-A through G04-I, but the independent review is FAIL, G04-C/J are not fully closed, and the recorded closure condition still includes independent review and D/I same-SHA approval.
- **U021-G04-002 — P1 — Issue #41 — KEEP OPEN.** The canonical identifier is corrected, but GOV-DOC-001 structure/parity fails and schema/API/test-oracle consistency is not evidenced.
- **U021-G04-003 — P1 — Issue #41 — KEEP OPEN.** The three ordering outcomes are specified, but Storage serialization/atomicity proof and reproducible race/recovery tests remain absent.
- **U021-G04-004 — P1 — Issue #41 — KEEP OPEN.** The test mapping is not faithful to U-011 T01–T16, DFI-013…022 are not individually mapped, and all execution evidence remains NOT RUN.

### New independent findings

- **U023-GOV-001 — P1 — Issue #41 — OPEN.** The one-file bilingual candidate lacks the paired EN/ZH file structure and reciprocal links required by GOV-DOC-001 §§3–4, and §6's test tables are English-only. Remedy: publish linked EN and ZH counterpart files in the same change set and translate every normative test table/scenario/assertion.
- **U023-REG-001 — P1 — Issue #41 — OPEN.** v2 drops or weakens v1's per-stage reauthorization, request idempotency, checkpoint/lease fencing, retry classification/reconciliation, full GovernanceAssessment.Compliant predicate, CompletedWithPolicyException projection, public-status projection and target_state vocabulary. Remedy: restore the v1 requirements or obtain explicit D/I decision on each semantic change and preserve traceability.
- **U023-TEST-001 — P1 — Issue #41 — OPEN.** v2 §6.2 misaligns I-U011-T12…T16 and omits the original unknown-required-target and D-completion-absent assertions; DFI-013…022 are grouped rather than individually crosswalked. Remedy: restore one-to-one source test IDs and map each DFI ID separately to clause, scenario and expected assertion.

## 6. Final gate and boundaries

- GOV-DOC-001: **FAIL**.
- G04-A/B/D/E/F/G/H/I: document text present; this is not Owner approval or implementation closure.
- G04-C: PARTIAL; retain open.
- G04-J: FAIL; retain open.
- Eight-deliverable claim: **4 ACCEPT / 4 REJECT** (items 1, 2, 5, 6, 8 rejected; items 3, 4, 7 accepted).
- D/I same-SHA approval: NOT GRANTED / NOT EVIDENCED.
- Storage approval: NOT CLAIMED / NOT EVIDENCED.
- Independent integration review: PENDING.
- Reproducible R3 tests: NOT RUN / NOT EVIDENCED.
- Overall: AID-2026-001 remains BLOCKED_PENDING_R3_EVIDENCE.

No PR or Issue was created. No source/runtime implementation was changed. No approval, merge, acceptance, production activation, Storage atomicity or R3 PASS is claimed.
