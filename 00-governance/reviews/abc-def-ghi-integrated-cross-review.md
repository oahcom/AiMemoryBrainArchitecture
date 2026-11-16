# Unified A–I Module Baseline Review & Cross-Module Reconciliation

- Review ID: P-UNIFIED-MBR-REVIEW-001
- Review date: 2026-11-17
- Prepared by: Session P — integration coordination and evidence audit
- Repository: `oahcom/AiMemoryBrainArchitecture`
- Review branch: `session-p-project-governance-baseline`
- Status: **PROPOSED REVIEW — NOT OWNER APPROVAL / NOT PROJECT G0 RATIFICATION**
- Scope: A–I module baseline proposals, ABC / DEF / GHI cross-module boundaries, evidence freshness, dependency closure and remediation.
- Authority boundary: This report may reconcile evidence and identify inconsistencies. It does not adopt any module baseline, resolve another Owner's ADR, approve I governance, freeze a shared contract, authorize implementation or merge branches.

## 1. Executive disposition

All nine Owner branches contain a module baseline/redlines proposal or equivalent proposal artifact. All nine artifacts are explicitly PROPOSED / Owner review required / not APPROVED. This is a successful first-round document submission, not a completed module-baseline acceptance gate.

The current evidence supports:
- module mission and authority boundaries are substantially documented across A–I;
- each proposal distinguishes owned semantics from non-owned semantics;
- B ADR-001 remains ADR-BLOCKED;
- D's JF-10 v2 acceptance is limited to D-owned semantics and enumerated exceptions;
- C/G/H Applied is not frozen to one shared version/digest;
- I governance and Global Forget completion remain blocked;
- implementation and conformance evidence remain separate from design review.

The current evidence does **not** support:
- any of the nine module baselines being APPROVED;
- project G0 ratification or PGA appointment;
- common C/G/H Applied contract freeze;
- production JF-10 closure;
- effective I security/governance policy or Global Forget completion;
- architecture freeze or merge authorization.

## 2. Live branch and artifact evidence

Branch HEADs below were re-fetched from GitHub during this review. Blob SHAs identify the exact module proposal files fetched from those branch refs. The branch HEAD and artifact blob are different identifiers and must not be conflated.

| Module | Owner branch | Live HEAD SHA | Baseline artifact | Blob SHA | Status |
|---|---|---|---|---|---|
| A | `session-a-integration-2026-11-16` | `fb061aee907c28f7da198e68161ff57ebac160b7` | `reviews/integration/module-a-integration-governance-baseline-and-redlines.md` | `a43a8f2fa3d31681d64b79d584364fdae80f8866` | PROPOSED |
| B | `session-b-domain-model-phase3` | `861fa9b2c3e1f572336543b15c7dc392493891db` | `02-domain-model/module-b-domain-model-baseline-and-redlines.md` | `410d6cc62294e1a7ee5efa0cfe4ef496a8179326` | PROPOSED |
| C | `session-c-agent-integration-2026-11-16` | `2e5776029bc4271c33525f04c7d0f0708e4bbae8` | `07-agent-integration/module-c-agent-integration-baseline-and-redlines.md` | `c79da952efaa490083c88ccb4608d62f526fcbae` | PROPOSED |
| D | `session-d-memory-brain-2026-11-16` | `9dd48eddb3c8f91d15dfa6981a7f53cc70bd4bf8` | `03-memory-brain/module-baseline-and-redlines.md` | `84e402f471d452c7dab63a7db344f86b5b57bd7c` | PROPOSED |
| E | `session-e-memory-compiler-2026-11-16` | `4402549c39824b89a0dc49973226187c62e056c5` | `04-memory-compiler/module-baseline-and-redlines.md` | `7f037a7684723fdbddd593b3d131c7c348e2ccbe` | PROPOSED |
| F | `session-f-memory-runtime` | `a370d9a3bc0bd35a21a12dfe87d53c298237de8e` | `05-memory-runtime/module-baseline-and-redlines.md` | `d4756cabda3151999cbe1ddde0adb554458004a1` | PROPOSED |
| G | `session-g-memory-context` | `72a8066b4401f9586fe10775d545384b82736f07` | `reviews/governance/g-module-baseline-and-redlines-proposal.md` | `fb2eb805be385469b5ab5f25c4ef76f234feb4c2` | PROPOSED |
| H | `session-h-bmcp-protocol` | `242d8ab5da890181e762561bb3d3a662287fb63c` | `reviews/governance/h-module-baseline-and-redlines-proposal.md` | `a4d961ac7b7e1a5fdf59422a4ebe21a6db95ace1` | PROPOSED |
| I | `session-i-security-governance-2026-11-16` | `1fc3b3293ebf2077edfd6ad253647d382173d9fa` | `reviews/governance/i-module-baseline-and-redlines-proposal.md` | `b0493cf0366159c99536ee8847996916bc21c606` | PROPOSED |

The current A/C/F/G/H tips have advanced beyond earlier inventory snapshots. A, B and C baseline headers still cite older “prepared against” HEADs; those are historical source snapshots, not current branch tips. The technology reports also cite their reviewed source HEAD separately from their publication commits. This is not itself a semantic defect, but each report must explicitly distinguish source snapshot, report commit and current branch HEAD.

## 3. Template and structural conformity

The proposed 14-section template exists on the P coordination branch at:
`00-governance/module-baseline-and-redlines-template.md`, blob `408979f2125b67e7599118038b9a415a213399ee`.

It does **not** exist on `main` at the time of this review. The template on P is a governance proposal and is not yet an approved project-wide normative template.

Structural comparison:
- A has 13 second-level sections and lacks the template's distinct Section 14 evidence/version-history section.
- B and C each have 14 second-level sections.
- D, E and F each have 15 second-level sections; their numbering/section mapping needs a normalization check against the proposed template.
- G, H and I each have 14 second-level sections.

Action: retain the existing Owner documents as their own proposals; do not rewrite them centrally. Ask each Owner to map its current document to the proposed 14-section template after the project template itself is ratified or explicitly adopted for this rollout. At minimum, A must add a distinct evidence/version-history section; D/E/F must explain any additional section and ensure the required fourteen topics are all present.

## 4. ABC cross-review

### A — Integration Governance
A's baseline correctly limits A to integration coordination, evidence registries, dependency visibility and gate tracking. It explicitly denies A authority to override B–I or Storage semantics, approve project governance, or infer implementation/test acceptance.

Cross-review findings:
- A's integration baseline appropriately keeps Fact/Claim-dependent interfaces blocked by B ADR-001.
- A correctly requires the same exact Applied contract version and explicit C/G/H decisions.
- A's current baseline file was prepared against `f8b16ce08b3e1ab3b67e502a8f1d48702bd433a9`, while the live A branch HEAD is now `fb061aee907c28f7da198e68161ff57ebac160b7`. Keep the former as source provenance and add the latter as current publication/verification HEAD.
- A's phase 3.6 closure tracking file remains the authoritative integration workstream evidence register; its older internal source-snapshot table must not be mistaken for the current live branch inventory.

### B — Domain Model
B's baseline correctly owns logical domain semantics and typed reference meaning, not authentication, permission, wire encoding, canonical persistence or physical storage.

Cross-review findings:
- ADR-001 is explicitly ADR-BLOCKED; Option A is a recommendation only, not a decision.
- Principal/ActorRef/Issuer, ScopeRef, EnvironmentRef and permission binding require B/I/H alignment. Typed references alone do not authenticate an actor or grant authority.
- Consumer mappings are not consumer acceptance.
- B baseline's prepared-against HEAD is `0cf703a3...`; current B HEAD is `861fa9b2...`. Preserve provenance and record current HEAD.
- The 14-section document is structurally aligned with the proposed P template at heading-count level; Owner must still validate content completeness.

### C — Agent Integration
C correctly owns Agent-side telemetry and final inference-request boundary evidence, while G owns Applied, H owns protocol/transport evidence, I owns authorization and D owns ForgetFence.

Cross-review findings:
- C must not manufacture Applied or infer it from Delivered, Materialized or Submitted.
- C's final-request evidence must be cryptographically/integrity-bound to the exact final request, managed-region digest, session/Adapter/capability and current policy/fence predicates as required by the common profile.
- The C baseline prepared-against HEAD is `702263dee9...`; current C HEAD is `2e577602...`. The technology report's source HEAD is a separate snapshot and must be called out explicitly.
- C's technology review is a static architecture review; it does not prove Agent runtime hooks, request interception, or end-to-end Applied execution.

**ABC disposition:** authority boundaries are directionally consistent. No ABC contract freeze is granted. B ADR-001 and typed identity binding remain blockers; A must remain coordinator, not approver of B/C decisions.

## 5. DEF cross-review

### D — Memory Brain
D owns canonical memory and ForgetFence semantics, canonical cursor and producer barrier semantics. D does not own compiler work state, runtime index/cache, Context, Adapter protocol, I policy or Storage engine internals.

Current exact D decision is ACCEPT WITH ENUMERATED EXCEPTIONS for the single-I-PolicyDomain JF-10 v2 bundle, limited to D-owned ForgetFence, producer registration, dependency inventory, lineage and barrier semantics. This is architecture/interface acceptance only. It does not establish D implementation, durable ledger/locks, participant recovery, COC deployment, Storage physical correctness or production conformance. D36/JF10-01..13 and crash/fault suites remain NOT RUN; JF-10 P0 remains OPEN; multi-PolicyDomain atomicity remains BLOCKED.

### E — Memory Compiler
E owns compiler work/attempt/lease/retry/DLQ/replay, staging and derivative lineage. E does not own canonical Memory commit, I authorization, D fence, Storage visibility or G Context.

Cross-review findings:
- Staged/private artifacts must remain invisible until D registration/fence, current I authorization and Storage publication visibility all succeed.
- WorkItemId, AttemptId and LeaseId must remain distinct and fenced; retries/recompiles cannot escape root barrier accounting.
- E's module proposal must not imply that a chosen database or Storage capability probe constitutes production JF-10 acceptance.
- E's older database wording must be updated only to the extent supported by exact Storage evidence: PostgreSQL 18.7 is a capability-probe candidate with isolated single-node CI evidence; not a production Canonical Authority deployment decision.

### F — Memory Runtime
F owns retrieval, ranking, index/cache execution and runtime suppression/invalidation. It consumes D fences/cursors, I authorization, E publication state and G completeness/sufficiency but cannot redefine them.

Cross-review findings:
- Candidate backends (FTS5/Tantivy/ANN) remain candidates until workload benchmarks and deterministic rebuild/fence tests exist.
- Authorization and Forget filtering must occur before candidate emission and at final return; graph/provenance dereference must not bypass it.
- Cache TTL, capacity, latency SLO and technology freeze require measured workload evidence.
- F's technology report is static and conditional; it does not prove runtime suppression or index rebuild behavior.

### Storage / JF-10 evidence
The Storage branch contains the PostgreSQL 18.7 prepared-XID capability probe. PR #12 is closed; its description limits the probe to single-node CI and expressly excludes replication/failover, production restore, hardware durability, operator readiness and JF-10 P0 closure. PR closed state alone is not proof that every probe passed; the workflow run/result must be inspected before recording a pass.

**DEF disposition:** logical design responsibilities are coherent, and D's bounded architecture decision is real. The physical serialization/deployment, accountable operator, same-XID recovery/failover, atomic visibility and end-to-end crash/fault conformance remain OPEN. Do not repeat design review as if it were implementation validation.

## 6. GHI cross-review

### G — Memory Context
G owns Context membership/order/budget, ContextVersion, ChangeSet, reconciliation, delivery intent and authoritative Applied record. G consumes C final-request evidence, H delivery/materialization evidence, D canonical/Forget state, F retrieval completeness and I authorization.

Cross-review findings:
- Delivered, Materialized and Submitted are not Applied.
- Applied must bind exact ContextVersion, Delivery, inference request, Agent/session, Adapter identity/instance, CapabilityEpoch, PermissionEpoch, ForgetFenceGeneration, managed-region integrity and C-owned final-request submission evidence.
- G cannot declare canonical Forget or global erasure; Context removal is not Forget.
- G's technology report is a static conditional review. Persistence/recovery, token/window budget and Applied verifier negative tests remain unverified.

### H — BMCP Protocol
H owns wire envelope, versioning, compatibility, Adapter capability declarations, transport delivery receipts and reconnect/replay mechanics. H does not own Principal identity meaning, permission policy, Context Applied semantics, canonical Forget or global completion.

Cross-review findings:
- Payload ActorRef/source claims are not authenticated identity.
- JSON/RFC 8785 and HTTP/local IPC/gRPC remain candidates, not approved wire/transport decisions.
- ACK evidence is attempt- and target-scoped. Delivered is not Applied, local purge, suppression or global Forget.
- H36, SDK interoperability, generated schema, cryptographic binding and reconnect/fault tests remain NOT RUN.
- H's technology report is a static conditional review, not runtime interoperability certification.

### I — Security & Governance
I owns issuer trust, Principal/ActorRef authorization binding, delegation, PermissionEpoch, revocation, policy, Global Forget inventory/seal and completion/retention criteria.

Cross-review findings:
- I governance decisions I35-DEC and I36-GOV must remain Proposed/Governance-Blocked until named authorized approvers and exact effective policy versions are recorded.
- Inventory completeness needs a signed closed-world InventorySealReceipt and explicit target/exclusion/retirement treatment.
- External recipients, backups, restore targets and erasure exceptions need accountable owners and evidence.
- No downstream module can infer global completion from local ACK, Adapter purge, canonical tombstone or storage deletion.
- I's proposal must not imply that a candidate inventory contract is an operationally complete inventory.

**GHI disposition:** G/H Applied responsibilities are conceptually compatible but lack a common frozen schema/digest and explicit C/G/H acceptance. I authorization and global completion remain independent gates. No Applied or Global Forget freeze is granted.

## 7. Cross-group dependency reconciliation

| Contract / dependency | Authorities | Current disposition | Freeze condition |
|---|---|---|---|
| Fact / Claim semantics | B + designated ADR authority; affected consumers | ADR-001 ADR-BLOCKED | Formal ADR-001 decision with exact option, approver, timestamp, version and migration/consumer impact |
| Principal / ActorRef / Issuer / Scope / Environment binding | B + I + H; C/D/E/F/G consumers | OPEN / not fully accepted | Exact shared field semantics, authenticated transport binding, permission mapping, negative tests and each affected Owner's exact-version acceptance |
| JF-10 v2 single PolicyDomain | D + E + Storage + I; C/F/G/H consumers | D bounded architecture decision; engineering/governance OPEN | Named DB/platform operator, approved I sequencer interface, durable participant/visibility implementation, same-XID restart/failover recovery, atomic visibility, D36/JF10 and crash/fault tests |
| Applied proof / BMCP ACK | C + G + H; I/D/B predicate authorities | OPEN / not frozen | One schema/version/digest, explicit C/G/H acceptance, I/D/B predicate mapping, verifier and negative/transform/replay tests |
| Global Forget | I + D/E/F/G/H/Storage and external recipients/backups | GOVERNANCE-BLOCKED / operational evidence incomplete | Signed inventory seal, target-state matrix, external/backup/restore receipts, physical deletion evidence, approved exceptions and I36 governance approvals |
| Retrieval/backend technology | F + D/E/I/G/H consumers | Candidate only | Representative workload benchmark, authorization-before-emission tests, rebuild/fence and recovery evidence |
| BMCP wire/transport | H + B/I/C/G/D | Candidate only | Approved identity/profile dependencies, encoding/transport ADR, generated SDK interoperability and H36 tests |

## 8. Technology review coverage

Current technology architecture review reports found on Owner branches:
- C — Agent Integration Technology Architecture Review, static review / conditional.
- F — Memory Runtime Technology Architecture Review, static review / conditional.
- G — Memory Context Technology Architecture Review, static review / conditional.
- H — BMCP Protocol Technology Architecture Review, static review / conditional.

No separate TAR-AI-001 technology review report was found in the current B, I, D or E branch artifacts inspected for this review. This is an evidence-coverage gap, not an inference that those modules are technically rejected. Their architecture baselines and technology constraints still need to be checked against the A–I system blueprint; do not fabricate a technology verdict.

## 9. Required unified actions

1. Refresh source HEAD and blob SHA in every Owner artifact without overwriting historical provenance.
2. Each Owner records a specific decision on its own branch: ADOPT / ADOPT WITH EXCEPTIONS / REVISE / REJECT, exact proposal version and current branch HEAD. Session P cannot make this decision for them.
3. Normalize all nine documents against the proposed 14-section template after governance authority resolves whether the P template is the rollout standard.
4. B/ADR authority resolves ADR-001; B/I/H jointly pin typed identity and permission binding; consumers acknowledge exact versions.
5. C/G/H publish one Applied contract candidate with exact schema version and digest, then each records explicit acceptance; I/D/B predicate authorities confirm their fields without surrendering their own authority.
6. D/E/Storage/I finish JF-10 engineering and governance gates; inspect PR #12 workflow evidence and do not equate PR closure with probe pass.
7. I supplies governance approvals and signed Global Forget inventory/target-state evidence.
8. A updates the integration registry and gate vector only after exact evidence is present.
9. No architecture freeze, production sign-off or merge follows from this report.

## 10. Review verdict

**PASS WITH MAJOR OPEN BLOCKERS — DOCUMENTATION / BOUNDARY REVIEW ONLY.**

The nine module proposals are suitable as first-round review inputs. They are not yet approved module baselines. The cross-module architecture remains unfrozen. The highest priority is exact-version closure for Applied and typed identity, formal ADR-001 disposition, and JF-10 physical recovery/governance evidence. Global Forget remains I-governed and incomplete until its independent evidence gates close.

## 11. Explicit non-claims

This report does not:
- approve any A–I module baseline;
- resolve ADR-001;
- accept or freeze Applied, BIH identity or JF-10 as a production contract;
- approve I security policy or external governance;
- claim implementation, CI pass, conformance pass, production readiness or Global Forget completion;
- authorize branch merge, main modification or architecture freeze.
