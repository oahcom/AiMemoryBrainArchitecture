# Development Readiness Register

- **Decision:** AID-2026-027
- **Architecture repository HEAD:** `f3bc21405aa6ad5a3ec271c04f7f4d8567d8bf33`
- **Integration review (`l2-05b`) blob:** `5685f22f32ac854b665112fc8225af197031a031`
- **Finding ledger blob:** `479747786fab47a47b7125761c2071921a87b436`
- **Scope:** Development-baseline readiness triage; this register is not architecture acceptance, production approval, or a grant of merge authority.

## 1. F-43-02 adjudication

**F-43-02: CLOSED by this decision.**

The previously identified Cargo.lock binding residual is resolved by the supplied execution evidence:

- The lock's recorded SHA-256 matches the actual Cargo.lock bytes: `a697d9051dc486f9707b1f1dd20f135ca922628805dcecf46a9e41078f751f24`.
- The lock binds `unicode-normalization` version `0.1.24`, and that package/version is present in the resolved Cargo.lock.
- Positive `cargo test -j 2` execution passed, including all 19,074 normalization records and 190,740 assertions.
- The decisive negative test forged the recorded Cargo.lock digest and recomputed both payload digests. Build failed with exit 101 and reported the expected forged digest and actual Cargo.lock digest.
- Restoring the lock restored a passing build.

The earlier Cargo.lock comment-append experiment is excluded as invalid evidence because Cargo normalizes the lock before invoking the build script.

No further F-43-02 residual is identified against its stated gate. The finding-ledger blob cited above still records the former BLOCKED status; that is a documentation synchronization task, not a reason to retain the technical finding as blocked.

## 2. Authoritative unresolved-item register

`BLOCKS-DEV-START` means the item genuinely prevents beginning development at the already authorized engineering-baseline scope. `DOES-NOT-BLOCK` means it remains a tracked action, acceptance condition, or scope-specific dependency, but is not a prerequisite to beginning that work.

| ID | 项目 | 当前状态 | 是否阻塞实际开发开工（BLOCKS-DEV-START / DOES-NOT-BLOCK） | 阻塞的实际内容 | 解除所需证据或决定 | 责任方 |
|---|---|---|---|---|---|---|
| F-43-01/F1 | D-authoritative callback and F1 operational proof | BLOCKED / OPEN | DOES-NOT-BLOCK | Blocks F1 operational closure and any claim of real authority-backed execution; does not block implementing the integration boundary. | Real D-authoritative callback, exercised end-to-end, with independently verifiable authority and Receipt evidence. Fixtures, mocks, and local receipts are insufficient. | D authority provider; D domain owner; project Owner for external dependency escalation |
| F-43-02 | UCD lock, version binding, and complete conformance | CLOSED by AID-2026-027; old ledger entry stale | DOES-NOT-BLOCK | No remaining development-entry blocker from this finding. | Synchronize the architecture finding ledger with this adjudication and retain the build/test evidence. | Architecture finding-ledger maintainer |
| R-01 | Storage atomic visibility | Critical / OPEN | DOES-NOT-BLOCK | Blocks acceptance of atomic visibility guarantees for affected storage paths; not the start of baseline storage development. | Executable concurrency/crash evidence establishing atomic visibility, plus the required joint D/I acceptance. | Storage domain; D/I integration owners |
| R-02 | Fact/Claim | Critical / BLOCKED; ADR-001 ADR-BLOCKED | DOES-NOT-BLOCK | Blocks implementation decisions that depend on unresolved Fact/Claim semantics; unrelated baseline development can proceed. | Owner decision resolving ADR-001, with resulting contract and acceptance criteria recorded. | B domain; project Owner for ADR decision |
| R-03 | Forget / Anti-Resurrection | Critical / NOT PROVEN | DOES-NOT-BLOCK | Blocks claiming Forget/Anti-Resurrection correctness; this is an implementation proof obligation, not an entry condition. | End-to-end implementation and adversarial evidence that forgotten data cannot reappear through restore, replay, or downstream paths. | F domain; Storage; D/I integration |
| R-04 | Applied / Provider Outcome | High / NOT PROVEN | DOES-NOT-BLOCK | Blocks production claims about provider application and outcome consistency. | Real provider execution and persisted outcome evidence correlated to the relevant operation. | G domain; provider integration owner |
| R-05 | Exact version drift | High / NOT PROVEN | DOES-NOT-BLOCK | Blocks exact-version consistency acceptance across components; does not block initial implementation. | Reproducible evidence binding component versions, schemas, artifacts, and runtime resolution. | H/E domains; release/build owner |
| R-06 | Identity & authorization | High / NOT PROVEN; I36-GOV-01..10 GOVERNANCE-BLOCKED | DOES-NOT-BLOCK | Blocks authorized production actions and claims of production identity enforcement; isolated baseline implementation can proceed without production authority. | Resolve I36-GOV-01..10 and demonstrate real identity, authorization, and Sequencer enforcement. | I domain; governance Owner |
| R-07 | Recovery / Restore | Components PARTIALLY VERIFIED; E2E NOT PROVEN | DOES-NOT-BLOCK | Blocks end-to-end recovery/restore acceptance, not development of the component path. | End-to-end restore/recovery execution with integrity, ordering, and anti-resurrection evidence. | Storage; F; recovery domain owners |
| R-08 | TOCTOU / Egress | High / PARTIALLY SPECIFIED | DOES-NOT-BLOCK | Blocks acceptance of affected egress/security guarantees; does not prevent baseline implementation. | Executable race/egress tests and a verified enforcement boundary matching the specified contract. | I domain; runtime/security owners |
| R-09 | Deployment & DR | High / PRODUCTION READINESS NOT PROVEN | DOES-NOT-BLOCK | Blocks production-readiness claims and deployment approval, not development-baseline work. | Deployment and disaster-recovery exercises with measured recovery evidence and operational sign-off. | Operations/deployment owner; project Owner |
| R-10 | Governance complexity | High / PARTIALLY VERIFIED (risk only) | DOES-NOT-BLOCK | Blocks a claim that governance complexity risk is fully controlled; not an engineering-entry dependency. | Demonstrated operating controls, ownership clarity, and evidence that the governance process is sustainable. | Project Owner; governance maintainers |
| G1 | Gate G1 | PARTIAL | DOES-NOT-BLOCK | Blocks G1 PASS; exact gate-specific scope remains governed by its recorded definition. | Complete the G1-defined evidence and obtain its required acceptance. | G1 gate owner; currently not identified in supplied evidence |
| G2 | Gate G2 | PARTIAL | DOES-NOT-BLOCK | Blocks G2 PASS, not initial baseline development. | Complete the G2-defined evidence and obtain its required acceptance. | G2 gate owner; currently not identified in supplied evidence |
| G3 | Gate G3 | NOT PASS | DOES-NOT-BLOCK | Blocks G3 acceptance; no evidence supplied that it is an engineering-entry prerequisite. | Satisfy the G3-defined criteria and record the acceptance evidence. | G3 gate owner; currently not identified in supplied evidence |
| G4 | Gate G4 | BLOCKED | DOES-NOT-BLOCK | Blocks G4 acceptance. The supplied status does not establish that it blocks all development. | Resolve the specific G4 blocker under its recorded gate definition; record the decision and evidence. | G4 gate owner and the party responsible for its recorded blocker |
| G5 | Gate G5 | PARTIAL | DOES-NOT-BLOCK | Blocks G5 PASS, not baseline development start. | Complete the G5-defined evidence and obtain its required acceptance. | G5 gate owner; currently not identified in supplied evidence |
| G6 | Gate G6 | NOT VERIFIED | DOES-NOT-BLOCK | Blocks G6 verification, not initial implementation. | Execute the G6-defined verification and retain its result. | G6 gate owner; currently not identified in supplied evidence |
| G7 | Gate G7 | PARTIAL | DOES-NOT-BLOCK | Blocks G7 PASS, not initial implementation. | Complete the G7-defined evidence and obtain its required acceptance. | G7 gate owner; currently not identified in supplied evidence |
| G8 | Gate G8 | NOT READY | DOES-NOT-BLOCK | Blocks architecture/system acceptance and any G8 readiness claim; it is not the engineering-baseline entry gate. | Satisfy all G8 prerequisites and record the required cross-domain acceptance. | Architecture Owner and relevant domain owners |
| B | Fact/Claim domain | Semantics undecided / ADR-BLOCKED | DOES-NOT-BLOCK | Blocks implementation slices whose correctness depends on unresolved Fact/Claim semantics. | Resolve ADR-001 and publish the binding domain contract. | B domain; project Owner |
| D | D authority domain | Semantics DECIDED; production unverified; cross-domain acceptance OPEN | DOES-NOT-BLOCK | Blocks real authority-backed acceptance, not baseline interface and contract development. | Real authority service/callback, production evidence, and cross-domain acceptance. | D domain; external authority provider |
| E | E lifecycle/build domain | Local lifecycle recorded; production build/publish unverified; E36 not run | DOES-NOT-BLOCK | Blocks production lifecycle/build acceptance. | Production build/publish evidence and execution of E36. | E domain; release/build owner |
| F | Runtime Forget domain | Runtime Forget semantics DECIDED; production Runtime unverified | DOES-NOT-BLOCK | Blocks production Runtime proof, not implementation of the decided semantics. | Real Runtime execution and Forget/Anti-Resurrection evidence. | F domain; Runtime owner |
| G | Context/Applied domain | Context ordering DECIDED; Applied production persistence unverified | DOES-NOT-BLOCK | Blocks production Applied persistence acceptance. | Real persistence/provider outcome evidence consistent with decided ordering. | G domain; provider/persistence owner |
| H | Schema/validator domain | Schema candidate 1.2.17; reference validator exists; production adapter unverified | DOES-NOT-BLOCK | Blocks production adapter acceptance, not baseline schema/validator work. | Production adapter implementation and contract/conformance evidence. | H domain; schema/validator owner |
| I | Identity/Sequencer domain | Technical baseline JOINT-DECIDED; production authorization/Sequencer unverified; I36 governance approval BLOCKED | DOES-NOT-BLOCK | Blocks production authorization and Sequencer acceptance. | Real service evidence and I36 governance approval. | I domain; governance Owner |
| Storage | Storage domain | L1 Option A selected; physical deployment unproven; L4 and joint D/I acceptance OPEN | DOES-NOT-BLOCK | Blocks physical deployment and joint acceptance; not baseline storage development. | L4 evidence, physical deployment validation, and joint D/I acceptance. | Storage domain; D/I integration owners |
| #11 | A–I Baseline rollout | OPEN | DOES-NOT-BLOCK | Blocks declaring the system-wide baseline rollout complete; it is not required to begin scoped engineering work. | Per-domain rollout evidence and recorded cross-domain acceptance. | Portfolio Owner; A–I domain owners |
| #24 | Owner Workflow / Scheduled Tasks | OPEN | DOES-NOT-BLOCK | Blocks completion of this portfolio capability, not baseline development. | Implement and verify the workflow/scheduling scope against its acceptance criteria. | Workflow portfolio owner; project Owner |
| #30 | Event-driven Worker Runtime | OPEN | DOES-NOT-BLOCK | Blocks completion of the worker-runtime portfolio item; the runtime is itself development work. | Implement and exercise the event-driven runtime with operational evidence. | Runtime/worker portfolio owner |
| #43 | System-wide consolidation | OPEN | DOES-NOT-BLOCK | Blocks system-wide consolidation/closure, not engineering-phase entry. | Reconcile findings, gates, domain acceptance, and evidence across the system. | Project Owner; architecture registrar |
| #254 | External architecture review | OPEN; per-item triage pending | DOES-NOT-BLOCK | Blocks completion of the external-review portfolio item, not the start of baseline development absent a recorded entry-gate requirement. | Per-item triage and review evidence, with findings dispositioned. | Architecture Owner; external reviewer when engaged |
| REQ-01 | Requirement record 01 | OPEN / RECORDED | DOES-NOT-BLOCK | Blocks acceptance of the requirement's implementation; supplied evidence does not identify it as a universal entry gate. | Recover its authoritative requirement text, assign an accountable owner, and record traceable acceptance criteria. | Requirement originator; project Owner |
| REQ-02 | Requirement record 02 | OPEN / RECORDED | DOES-NOT-BLOCK | Blocks acceptance of the requirement's implementation; not shown to block all development. | Recover authoritative text, assign owner, and record traceable acceptance criteria. | Requirement originator; project Owner |
| REQ-03 | Requirement record 03 | OPEN / RECORDED | DOES-NOT-BLOCK | Blocks acceptance of the requirement's implementation; not shown to block all development. | Recover authoritative text, assign owner, and record traceable acceptance criteria. | Requirement originator; project Owner |
| REQ-04 | Requirement record 04 | OPEN / RECORDED | DOES-NOT-BLOCK | Blocks acceptance of the requirement's implementation; not shown to block all development. | Recover authoritative text, assign owner, and record traceable acceptance criteria. | Requirement originator; project Owner |
| REQ-05 | Requirement record 05 | OPEN / RECORDED | DOES-NOT-BLOCK | Blocks acceptance of the requirement's implementation; not shown to block all development. | Recover authoritative text, assign owner, and record traceable acceptance criteria. | Requirement originator; project Owner |
| #7 | Canonical runtime repo / engineering owners / entry plan | OPEN; 17 comments; `IMPLEMENTATION_BINDING=DEFERRED_TO_ENGINEERING_PHASE`; E1–E8 handoff delivered at PR #327 | DOES-NOT-BLOCK | The outstanding checklist blocks formal completion of the entry checklist and accountable delegation, but does not negate the recorded decision to defer implementation binding to engineering phase. | Reconcile the checklist with the existing runtime repo and E1–E8 handoff; project Owner to identify engineering ownership and record the execution plan. | Project Owner; engineering ownership remains unassigned |
| #26 | Ubuntu self-hosted runner security acceptance | OPEN; `SECURITY_ACCEPTANCE_BLOCKED`; reopened | DOES-NOT-BLOCK | Blocks use of the unaccepted Ubuntu self-hosted runner and workflows dependent on it; does not block development through an already authorized safe environment. | Security acceptance evidence for the runner, or use a separately approved execution environment. | Runner/security owner; project Owner for environment decision |
| #37 | First executable GitHub-driven Owner Worker | OPEN; no assignee | DOES-NOT-BLOCK | Blocks completion of the first executable Owner Worker; this is a development deliverable, not a prerequisite to beginning development. | Implement and execute the first worker with auditable GitHub-driven evidence. | Project Owner; worker implementation owner to be assigned |
| #134 discrepancy | Platform merge gate | GitHub CLOSED (`completed` 2026-11-19T17:28Z); `l2-05` receipt still records unresolved | DOES-NOT-BLOCK | Blocks confidence in the accuracy of the architecture receipt, not development start. | Verify the GitHub closure record and closure artifact; reconcile the stale receipt without reopening or silently rewriting history. | Architecture registrar; #134 issue maintainer |
| #271 discrepancy | Qualified independent review | GitHub CLOSED (2026-11-19T17:16Z); `l2-05` receipt still says qualified review absent | DOES-NOT-BLOCK | Blocks confidence in the review-status record; closure alone does not prove the receipt's substantive claim was satisfied. | Inspect closure evidence and reviewer qualification; reconcile the receipt to the verified facts. | Architecture registrar; #271 issue maintainer |
| #275 discrepancy | HOLD item | GitHub CLOSED (2026-11-19T15:01Z); `l2-05` receipt still records HOLD | DOES-NOT-BLOCK | Blocks consistency of the portfolio record, not engineering entry. | Verify the closure event and disposition evidence; update the receipt to reflect the actual state. | Architecture registrar; #275 issue maintainer |

**Register counts:** `BLOCKS-DEV-START = 0`; `DOES-NOT-BLOCK = 39`.

The three GitHub closure discrepancies are deliberately not treated as proof that the underlying substantive concerns were satisfied. They require evidence reconciliation. The supplied GitHub state is authoritative for the issue's current OPEN/CLOSED state; the receipts remain authoritative evidence of what was previously recorded, not a reason to falsify either history.

## 3. Minimum gate set for actual development

The minimum gate set for entering the already recorded engineering phase is:

1. **Phase boundary and scope:** engineering-phase implementation binding is deferred to that phase; work remains development-baseline scope, without production activation or `main` authority.
2. **Canonical implementation target:** `oahcom/AiMemoryBrain` and the working branch are identified.
3. **Actionable handoff:** the E1–E8 engineering handoff has been delivered at PR #327, HEAD `934a76e18ba020d01c520a8484ed7fc37f96cff1`, blob `2d453d24ae5e65973ced964918b9f3687a5d3284`.
4. **Bounded execution:** unresolved operational and cross-domain proof obligations remain explicit exit criteria; no mocks or fixtures are represented as real authority evidence.
5. **No prohibited transition:** development does not imply production approval, architecture acceptance, role appointment, quota change, or merge to `main`.

**Entry verdict: SATISFIED — for scoped engineering-phase development-baseline work.**

The project-owner direction and #7's `IMPLEMENTATION_BINDING=DEFERRED_TO_ENGINEERING_PHASE` are consistent with entering engineering phase now. The E1–E8 handoff at PR #327 supplies the recorded handoff. **No further Owner decision is required merely to enter that phase at this bounded scope.**

This does not declare #7's entire checklist complete. Engineering ownership and the execution plan remain to be recorded by the project Owner; the unaccepted self-hosted runner must not be used until its security acceptance is resolved. Those are tracked operational actions, not grounds to hold all baseline development.

## 4. Development versus exit criteria

The R-01..R-10 findings, G1..G8 gates, domain acceptance rows, portfolio items, and REQ-01..REQ-05 remain tracked. Their unresolved state does not make them disappear; it means they must be addressed by the relevant implementation slice or before the corresponding acceptance/production transition.

In particular:

- F1 remains OPEN because no real D-authoritative callback exists. Building the integration boundary can proceed; claiming operational proof cannot.
- R-03, R-04, and R-07 are implementation-dependent proof obligations. They cannot reasonably be demanded as preconditions to starting the implementations that produce their evidence.
- R-02 remains a genuine blocker for Fact/Claim-dependent design decisions, not a universal blocker for unrelated development.
- #26 blocks use of that runner, not development in an approved alternative environment.
- G8 remains NOT READY and architecture remains NOT ACCEPTED. Neither is being waived by this entry ruling.

## 5. Governance boundary

This register is a readiness triage and decision record. It does not appoint roles, change quota state, authorize production activation, grant `main`-merge authority, or close F1. Any later acceptance must be supported by the corresponding real evidence and the existing governance process.
