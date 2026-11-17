# Closed Issue Resolution & Design Quality Audit — 2026-11-17

- Repository: `oahcom/AiMemoryBrainArchitecture`
- Audit role: cross-issue technical audit / Storage coordination perspective
- Status: **AUDIT COMPLETE FOR ALL CURRENTLY CLOSED ISSUES AND CLOSED PRs DISCOVERED**
- Scope: actual closure evidence, exact-version Owner decisions, architecture quality, later superseding findings, and remaining gates.
- This audit is not an A integration decision, not an Owner approval, and does not alter any module's authority.

# 1. Executive summary / 执行摘要

The repository's closed-items API readback returned three completed Issues (#6, #8, #9) and one closed-but-unmerged draft PR (#12). No merged PR was returned by the closed-PR listing.

**Overall conclusion:** the three Issues were closed against their stated *narrow decision-request scopes*. Their closure evidence is real and mostly well-scoped. None proves end-to-end implementation, production deployment, global Forget completion, or JF-10 P0 closure.

A later exact-version integration review of the same A COC architecture Blob found six blocking clarifications (R1–R6), now tracked by open Issue #14. Therefore #8/#9 are valid narrow decision closures, but they must not be interpreted as final approval of the complete COC persistence/recovery protocol.

**中文结论：** 三个 Issue 的局部 Owner 决策任务有真实证据支撑；但系统级恢复协议尚未闭合。后续 A 精确版本审查发现的 R1–R6 是当前更高优先级的集成阻塞，必须以 Issue #14 的新审查门为准。

# 2. Closed item inventory / 已关闭项目清单

| Item | GitHub state | What was actually closed | Audit disposition |
|---|---|---|---|
| Issue #6 | closed / completed | C/F/G exact-version BIH consumer design acceptance | Correct narrow closure |
| Issue #8 | closed / completed | JF-10 ↔ COC architecture/interface Owner decision bundle | Correct narrow closure; later integration blockers remain |
| Issue #9 | closed / completed | D and Storage exact acceptance of the complete pinned bridge bundle | Correct narrow closure; no implementation gate closed |
| PR #12 | closed, draft, **not merged** | Isolated PostgreSQL 18.7 CI validation branch | Not a merged code change; do not count as integrated implementation |

No other closed Issue or closed PR was returned by the repository's `state=closed&per_page=100` API readback at audit time.

# 3. Issue #6 — BIH consumer acceptance

**Issue:** https://github.com/oahcom/AiMemoryBrainArchitecture/issues/6  
**Closed:** 2026-11-16T14:41:29Z  
**Target A package:** `a45ae90b318a79bf009d14f4d917611881e9e214`

## 3.1 Closure evidence

A's tracking register records exact Owner-branch readbacks:

- C: `07-agent-integration/phase-3.6-final-request-evidence-contract.md`, Blob `fd2f47ba6c89bb270e9f2bec956873cb7ae3592b`, ACCEPT WITH ENUMERATED EXCEPTIONS.
- F: `05-memory-runtime/phase-3.6-runtime-forget-suppression-and-invalidation.md`, Blob `ce59252dbbdc5d10d016704797e9ba12d5a941bd`, ACCEPT WITH ENUMERATED EXCEPTIONS.
- G: `06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md`, Blob `5406b3f2558daa3f5915f6bb46e808be8d90d3ca`, ACCEPT WITH ENUMERATED EXCEPTIONS.
- H's exact package acceptance: Blob `fe437a3d44790f249f613d1e6cafc0db40d45b10`.
- A's joint BIH package: Blob `a45ae90b318a79bf009d14f4d917611881e9e214`.

The exact artifact hashes are recorded in A's closure register and Issue #6 comments. The closure condition—separate C/F/G decisions against one A package—was satisfied.

## 3.2 Design quality

**Strong design principles**

1. Typed identity is a selector, not authentication. PrincipalRef, IssuerRef, ActorRef, Producer/Adapter identity, ScopeRef and EnvironmentRef are distinct; payload self-assertion cannot create trust.
2. I is the authority for issuer trust, identity resolution, delegation, authorization, revocation and opaque per-PolicyDomain PermissionEpoch. Consumers revalidate at their own protected boundaries.
3. PermissionEpoch and D ForgetFence are independent authorities. They are not interchangeable, numerically comparable or reducible to one generic version.
4. C's evidence stages are separated: Prepared → Delivered → Materialized → Final Request Submitted → Applied → Execution Started. A transport ACK or materialization does not prove final request submission or Applied.
5. G's Applied record is a historical fact about an exact ContextVersion included in an exact submitted request. It does not prove model attention, understanding, recall or correctness. Historical truth and current-use eligibility are separate.
6. F filters before candidate emission and rechecks at protected dereference, cache hit/fill, materialization and final return. Index freshness is a per-partition vector; a gap cannot be treated as deletion.
7. Reconnect is a new trust boundary: authenticate, refresh capability/permission/fence, reconcile, suppress stale state, then restore. No restore-then-clean-up.
8. Fail-closed behavior is specified for unknown, stale, malformed, mismatched or unsupported evidence.

**Quality judgment:** high quality for a cross-owner identity and consumer-boundary contract. It makes authority boundaries explicit and avoids the common error of equating transport delivery, context materialization and actual model use.

## 3.3 What Issue #6 did NOT close

- I36-GOV-01..10 external governance approvals remain BLOCKED.
- I36/H36 and C/F/G runtime suites remain SPECIFIED / NOT RUN.
- C/G/H common Applied-contract convergence is separate; the BIH acceptance does not freeze the Applied wire contract.
- Overall Phase 3.6 G10 and architecture freeze remain BLOCKED / NOT AUTHORIZED.

**Audit verdict:** Issue #6 was correctly closed for its exact consumer-acceptance subrequirement. It would be incorrect to cite it as global identity-governance approval or runtime conformance.

# 4. Issue #8 — JF-10 ↔ COC architecture/interface decision

**Issue:** https://github.com/oahcom/AiMemoryBrainArchitecture/issues/8  
**Closed:** 2026-11-16T15:42:59Z  
**A architecture Blob:** `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d`

## 4.1 What the architecture gets right

The design establishes a clear authority decomposition:

- COC: cross-owner ordering, durable participant accounting and recovery observations; not the JF-10 COMMIT/ABORT authority.
- I: sole policy-domain sequencer, single-use authorization receipt consumption and terminal authorization decision.
- Storage: exact preallocated XID prepare/resolution and atomic local visibility/PublicationReceipt.
- D: ForgetFence, lineage, participant barrier and effective-fence semantics.
- C: actual provider side-effect result and immutable CSubmitOutcome.
- H: authenticated wire transport and typed evidence preservation.
- G: Applied and current-use state.

The bridge sequence is directionally sound:

1. Quorum-commit prepare intent and preallocated XID identity before Storage PREPARE.
2. Storage durably prepares the exact XID, keeps bytes private and locks retained, then issues PreparedParticipantReceipt.
3. COC records the prepared participant before I's owner-final-gate decision.
4. I consumes the single-use receipt and makes the durable terminal decision.
5. Storage resolves the same XID in the direction of I's decision; visibility and PublicationReceipt commit atomically.
6. C reports the actual provider result; unknown provider outcomes remain IN_DOUBT.
7. D does not release the barrier until all required owner outcomes and lineage obligations are authoritative.

The COC-outage model also has the right safety direction: owner-local pending gates close first; a quorum-committed recovery batch captures outage requests; pre-batch participants are enumerated; each owner reopens only its own gate after its own high-water and reconciliation proof. Wall clocks and local owner positions are not used to invent cross-owner order.

## 4.2 Owner evidence and scope

Issue #8 records exact decisions from I, D, Storage, C and H, with enumerated exceptions. H's five JF-10 message families and the JSON Schema candidate are documentation-level evidence. The scope is explicitly one I PolicyDomain; multi-PolicyDomain atomicity remains blocked.

## 4.3 Post-closure CI — what it actually proves

Workflow run `43904569127`, head `bd104eaf63c7234a45fd780d484bc41ae15dd988`, succeeded. The job compiled the Python reference validator and ran 10 unit tests.

The tests cover valid lifecycle, changed-XID conflict, prepared receipt XID binding, I revocation cutoff evidence, Storage commit/rollback publication evidence, D barrier terminality, UNKNOWN nonterminal behavior, multi-domain rejection and reconciliation lookup consistency.

**This is a PASS for an in-memory Python reference validator only.** The validator's own docstring explicitly excludes cryptographic signature verification, COC quorum proofs and owner-authoritative database lookups. It is not a persistent COC, not a live I/D/Storage integration test, and not a DB/provider crash-recovery proof.

## 4.4 Concrete quality finding in the validator

The current `validate_bridge()` checks I terminal outcomes and Storage terminal outcomes independently, but does not enforce the required cross-authority mapping:

- I `COMMIT_WON` must require Storage `COMMITTED` for the same XID.
- I `REVOCATION_WON` or `INDETERMINATE_ABORTED` must require Storage `ROLLED_BACK` for the same XID.

As written, a record set with I `COMMIT_WON` and Storage `ROLLED_BACK` can pass if the rollback fields and reconciliation lookup agree; likewise I `REVOCATION_WON` plus Storage `COMMITTED` can pass if the Storage commit fields are internally consistent. This is a missing cross-message invariant, not a missing signature check.

The multi-domain unit test also supplies an optional `policy_domain_refs` list, while the normative message family uses the singular typed `policy_domain_ref`. The test should be tied directly to the canonical schema/decoder path, not only a helper-only alternate field.

**Required validator correction:** add an explicit I-outcome → Storage-resolution truth table and negative tests for both contradictory combinations; validate the actual canonical wire representation and ensure every message binds the same PolicyDomainRef. Keep signature/quorum/owner lookup claims outside the validator unless those verifiers are genuinely implemented.

## 4.5 Why the later A review matters

On 2026-11-17, A re-reviewed the same exact A architecture Blob and issued **ACCEPT WITH BLOCKING CLARIFICATIONS / AMENDMENTS REQUIRED**, recorded in:

- Artifact: `reviews/integration/phase-3.6-coc-persistence-exact-version-review.md`
- Blob: `fdf63550696948f77dc37c0a3788276ac4d525f5`
- Issue: https://github.com/oahcom/AiMemoryBrainArchitecture/issues/14

A found six blockers:

- R1: Recovery Cutoff Batch completeness, owner request high-water and post-high-water request handling.
- R2: exact owner-local gate linearization against in-flight admissions.
- R3: complete pre-batch participant-set proof and separate owner-signed gate release.
- R4: C provider invocation must require I `COMMIT_WON`, not merely any terminal I outcome.
- R5: explicit same-XID recovery state machine, authoritative lookup keys and monotonic terminal-state handling.
- R6: stale I Blob reference and H recovery-batch schema applicability drift between old and current A package versions.

These findings do not retroactively invalidate the narrow Owner decisions already recorded. They show that the broader persistence/recovery composition was not yet fully specified. Issue #14 is the controlling open review gate.

**Audit verdict:** Issue #8 was correctly closed for the exact Owner architecture/interface decision request. It was not a final COC persistence/recovery acceptance. The later R1–R6 findings are substantive and must be resolved before a protocol freeze.

# 5. Issue #9 — D and Storage exact full-bundle acceptance

**Issue:** https://github.com/oahcom/AiMemoryBrainArchitecture/issues/9  
**Closed:** 2026-11-16T16:20:46Z

## 5.1 Closure evidence

The issue records exact D and Storage Owner decisions against the corrected bridge bundle:

- D: Blob `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5`, commit `1460fbd17ee38ea4044dc6c75cfe49039c7fc585`.
- Storage: Blob `67d5d9b7c1f7979f5dda417ca30bb4b6f521cb45`, commit `a231b74e1ff3742435548ffe4efbcdeb8a59fccf`.
- Common JF-10 v2 protocol: Blob `94679897e84a6f58fd8b9467b5249e1a885cb0b0`.
- The bundle also binds A `a3c51ec...`, I `8069ff...`, C `45a482...`, H mapping `e7ca5c...` and H schema candidate `a8a945...`.

Both D and Storage decisions are ACCEPT WITH ENUMERATED EXCEPTIONS and architecture/interface only.

## 5.2 Design quality

**D's accepted contract** correctly treats a quorum-committed prepare intent before the fence cutoff as a prospective barrier participant, even before Storage's prepared receipt is recorded. Fence-first rejects. Participant-first retains the D barrier until I terminal evidence, Storage same-XID resolution, C provider outcome where applicable and D lineage obligations are authoritative. UNKNOWN/IN_DOUBT, outage, stale replica and lost ACK cannot release the barrier.

**Storage's accepted contract** correctly binds a preallocated XID, participant digest, operation identity and canonical DB identity; requires durable PREPARE and retained locks/private bytes; forbids alternate XID and heuristic resolution; and makes VisibilityPointer, PublicationReceipt, owner outcome, receipt-consumption evidence and outbox one atomic local visibility transaction. The authoritative read path must return the exact same-XID result; stale replicas/caches are not decision sources.

**Audit judgment:** strong separation of authority and good failure semantics. Issue #9 is a legitimate exact-version confirmation subgate.

## 5.3 What Issue #9 did NOT close

- Selected production DB engine, version, topology and operator.
- COC quorum persistence and restore.
- Provider-specific idempotency and outcome lookup.
- Generated H schema/SDK interoperability and cryptographic governance.
- JF10-COC-01..10 and owner runtime conformance.
- Multi-PolicyDomain atomicity.

**Audit verdict:** correctly closed for D/Storage exact-bundle decision only; not JF-10 P0 closure.

# 6. Closed PR #12 — PostgreSQL 18.7 capability probe

**PR:** https://github.com/oahcom/AiMemoryBrainArchitecture/pull/12  
**State:** closed, draft, `merged=false`, `merged_at=null`.

This was explicitly an isolated validation PR; no merge was requested. Its patch adds a validation note and relaxes a PostgreSQL version assertion from exact `18.7` to `18.7 ` prefix matching. It has no review submissions or review threads.

**Audit verdict:** do not count PR #12 as a merged implementation change. It is a closed validation branch, not integrated code. Any PostgreSQL capability claims must be traced to the actual workflow runs and exact Storage probe source, not to the PR's closed state.

# 7. Cross-issue quality assessment / 跨 Issue 质量判断

| Dimension | Assessment | Reason |
|---|---|---|
| Authority separation | Strong | I/D/C/Storage/H/G responsibilities are explicitly non-substitutable |
| Identity and trust model | Strong | Typed refs, protected verifier context, no payload self-assertion |
| Fail-closed behavior | Strong in design | UNKNOWN, stale, missing and mismatched evidence block progress |
| Concurrency/linearization | Incomplete at COC outage boundary | R2 identifies missing precise owner-local serialization point |
| Recovery completeness | Incomplete | R1/R3 require exact request and participant set completeness proofs |
| Provider side-effect gate | Needs normative correction | R4 clarifies COMMIT_WON-only provider invocation |
| Wire/schema precision | Candidate, not frozen | H schema candidate has explicit implementation and exact-version limits |
| Executable proof | Narrow partial evidence | 10 in-memory semantic tests; not COC quorum, live owner, DB/provider E2E |
| Production readiness | Not established | Gate A partial/open; Gate B/C blocked; production activation not authorized |

# 8. Current controlling gates / 当前有效状态

The current A tracking register and Issue #10 distinguish the following:

- Issue #14 R1–R6 exact-version Owner review: OPEN.
- Gate A: PARTIAL PASS / OPEN. PostgreSQL 18.7 CI has useful bounded evidence, but deep WAL-archive PITR still has a failing recovery-target/required-segment case and needs exact-target WAL correction plus stronger negative/read-path checks.
- Gate B persistent COC: BLOCKED pending Gate A acceptance and actual deployment binding.
- Gate C integrated end-to-end implementation/fault injection: BLOCKED pending Gate B.
- JF-10 P0: OPEN.
- Multi-PolicyDomain atomicity: BLOCKED.
- Production activation: NOT AUTHORIZED.

A's latest tracking record also states that the actual Canonical Authority executable/DB adapter, production failure domains/storage, real I/D control-ledger high-waters, human operator/on-call, runbook, failover routing, monitoring and RPO/RTO remain unresolved.

# 9. Recommended next actions / 后续顺序

1. **Resolve Issue #14 R1/R2 first:** I and D each specify their exact local gate linearization transaction/CAS, durable in-flight admission inventory, request high-water capture and no-gap reopening rule.
2. **Resolve R3:** COC produces an authoritative pre-batch participant manifest bound to exact prefix/root; I, D and C provide owner-specific completeness attestations; empty set is explicitly proven.
3. **Resolve R4:** C contract changes provider invocation to require I `COMMIT_WON` plus all required D predicates. Abort and UNKNOWN never invoke provider.
4. **Resolve R5:** publish one exact same-XID state machine with owner-authoritative lookup keys and irreversible terminal outcomes; add validator cross-outcome checks and contradictory-outcome tests.
5. **Resolve R6:** H explicitly binds or rejects the recovery-batch schema mapping for current A §§11–12; A removes stale I Blob references and publishes a new A Blob if normative text changes.
6. **Re-review the exact successor bundle:** I/D/C/H each publish independent Owner artifacts against the same new Blob set; A then issues a fresh integration decision.
7. Only after that, continue Gate A's deep PITR and production-binding evidence; then Gate B COC deployment; then Gate C end-to-end tests.

**Do not reopen #6/#8/#9 merely because later gates remain open.** Keep their historical closure scopes intact, while using Issue #14 and Issue #10 as the active blockers. Reopen a closed item only if its own stated closure predicate is shown to have been false or its exact accepted artifact is superseded in a way that invalidates that narrow decision.

---

# English summary

The three closed Issues have genuine, exact-version decision evidence and were closed within their narrow scopes. Issue #6 closes C/F/G's BIH consumer design acceptance; Issue #8 closes the named JF-10/COC architecture-interface decision bundle; Issue #9 closes D/Storage's exact full-bundle acceptance. None closes implementation, deployment, global Forget or JF-10 P0.

The later A review of the same COC architecture found six blocking integration clarifications (R1–R6), now tracked in open Issue #14. The most important are owner-local gate linearization, complete recovery-batch request/participant enumeration, COMMIT_WON-only provider invocation, same-XID recovery state monotonicity, and exact-version schema binding. A 10-test Python semantic-validator CI run is useful but narrowly scoped; source inspection reveals it does not enforce the I-terminal-outcome to Storage-resolution mapping. Closed PR #12 was draft and unmerged.

The architecture has strong authority separation and fail-closed principles, but COC persistence/recovery is not yet a freeze-ready protocol. Gate A remains partial/open, Gate B/C remain blocked, JF-10 P0 remains open, multi-PolicyDomain atomicity remains blocked, and production activation is not authorized.
