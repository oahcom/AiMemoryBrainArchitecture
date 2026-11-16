# Phase 3.6 — Cross-Branch Baseline Manifest

- Owner: Session A — Principal Integration Architect
- Discovery date: 2026-11-16
- Repository: `oahcom/AiMemoryBrainArchitecture`
- Status: **BASELINE DISCOVERED; CROSS-MODULE CLOSURE NOT ESTABLISHED**
- Purpose: establish a reproducible, branch-aware source baseline for DE-S, BIH and CFG. This manifest records evidence; it does not approve or freeze any Owner contract.
- Write scope: A-owned integration manifest only. No other Owner branch or file was modified.

## 1. Discovery method and integrity rules

1. Queried the repository's live branch list. The discovered refs are `main`, `session-a-integration-2026-11-16`, `session-b-domain-model-phase3`, `session-c-agent-integration-2026-11-16`, `session-d-memory-brain-2026-11-16`, `session-e-memory-compiler-2026-11-16`, `session-f-memory-runtime`, `session-g-memory-context`, `session-h-bmcp-protocol`, `session-i-security-governance-2026-11-16`, and `session-storage-consistency-forget-atomicity-2026-11-16`.
2. Resolved each branch ref to its current commit object and recorded the full 40-character HEAD SHA and commit subject. These are live refs queried for this manifest, not SHAs copied from historical review tables.
3. Read each listed artifact from its Owner branch ref. The recorded Blob SHA identifies the exact file bytes returned by GitHub.
4. A branch HEAD SHA identifies the branch tip; a Blob SHA identifies one file. They are not interchangeable.
5. A file absent from `main` but present on an Owner branch is an **Owner Branch Artifact**, not a missing artifact.
6. Embedded baseline tables in older documents are historical snapshots. Where they differ from this manifest's live refs, this manifest's discovery-time refs take precedence for this baseline only. Re-query all refs before closure review.
7. No branch was merged. No non-A-owned file was changed.
8. The A HEAD listed in §2 is the source snapshot immediately before this manifest was published. The A-owned manifest publication commit is a separate delivery commit and is reported in the delivery evidence; it is not substituted for the pre-write source HEAD used to establish the baseline.

## 2. Live branch inventory

| Workstream | Owner | Branch | Latest full HEAD SHA | HEAD commit subject |
|---|---|---|---|---|
| Integration / baseline | A | `session-a-integration-2026-11-16` | `5ce61e0982ce8e22b29f1267ca67c9a085a96a06` | docs(integration): record closure review commit evidence |
| Typed identity / domain model | B | `session-b-domain-model-phase3` | `ebf459800e2d0566182fba6b58252bf978dfafe5` | docs(domain): close Phase 3.6 typed identity and scope contracts |
| Final request / Agent evidence | C | `session-c-agent-integration-2026-11-16` | `a585307222b0169c007915c25ff8ed0da517f3e4` | docs(agent-integration): reprocess phase 3.5 identity and applied conformance |
| Forget authority / fence | D | `session-d-memory-brain-2026-11-16` | `808665c6c56ba60633f13ec34bbd9b9daeef0583` | docs(memory-brain): record exact Phase 3.6 source baseline manifest |
| Producer / compiler | E | `session-e-memory-compiler-2026-11-16` | `a19feb57c85819cc0e49ab39abfd945b268aa51e` | docs(E): record Phase 3.6 source baseline and joint decision requests |
| Runtime / retrieval | F | `session-f-memory-runtime` | `f86f9b536ea69d8e0fbb4bf290c7023ef0eada76` | docs(runtime): record current Phase 3.5 re-review findings |
| Context / Applied consumer | G | `session-g-memory-context` | `557c68fd863f73dd09f6fccb3b9e920740db2e9c` | docs(context): align Phase 3.5 forget reconciliation and applied evidence |
| BMCP / Adapter | H | `session-h-bmcp-protocol` | `1ee65928f123d92a4758b0de09bc8d6df1e46253` | docs(h): correct Phase 3.5 source review and evidence log |
| Trust / authorization | I | `session-i-security-governance-2026-11-16` | `d52cd47972bd9d1d17f0fe6f2ab09646d084a80b` | docs(security): link Phase 3.6 trust chain addendum |
| Persistence / atomicity | Storage | `session-storage-consistency-forget-atomicity-2026-11-16` | `3a14550648f21c0bc2725dac38b29e099c2f3196` | docs(storage): rebase Forget atomicity review on Phase 3.5 D E I contracts |
| Shared integration baseline | Repository | `main` | `8a6414158c9c056c1638222534e1993d1bbc99d2` | docs(integration): review D E H I phase 3 contracts |

## 3. Authoritative artifact manifest

The source branch HEAD in each row is the exact live tip recorded in §2. Each artifact entry includes its repository path and fetched Blob SHA.

| Workstream | Owner | Branch | HEAD SHA | Authoritative artifact(s): path @ Blob SHA | Status / evidence level | Dependencies |
|---|---|---|---|---|---|---|
| Phase 3.5 Closure Review | A | `session-a-integration-2026-11-16` | `5ce61e0982ce8e22b29f1267ca67c9a085a96a06` | `reviews/integration/phase-3.5-cross-module-closure-review.md` @ `a05f1d817514bbed7bddec1729d6598d0835ef3e`; `reviews/integration/contract-registry.md` @ `f108642470e6f9764a690ff82e5c1fd25f2a86e6`; `reviews/integration/typed-cursor-and-watermark-contract.md` @ `2818ae24c67864277da89d1bc52af373e8f8313a` | Artifact Exists. A Owner Decision: **BLOCKED for Contract Freeze**. Cross-module agreement not established; implementation evidence absent. | All Owner workstreams; latest branch refs must be re-read before final gate. |
| D Forget Fence | D | `session-d-memory-brain-2026-11-16` | `808665c6c56ba60633f13ec34bbd9b9daeef0583` | `03-memory-brain/forget-fence-operation-and-publication-gate.md` @ `b9f75456140eed6a34faa8d84be20436cd91c745`; `03-memory-brain/forget-fence-and-completion-contract.md` @ `1f0391bc49d007c44ec74165bd33d37412cc7990`; `03-memory-brain/commit-cursor-semantics.md` @ `4688a0ca487bf4d853c7f0220408abe8d743d159` | Artifact Exists. D Forget operation/fence semantics and per-authority CanonicalCommitCursor are Owner-decided. Callable interface, Storage realization and cross-owner conformance remain OPEN. | E producer admission/publication; Storage transaction and recovery; I PermissionEpoch and global inventory; F/G/H downstream suppression. |
| E Producer / Publish Gate | E | `session-e-memory-compiler-2026-11-16` | `a19feb57c85819cc0e49ab39abfd945b268aa51e` | `04-memory-compiler/compiler-state-and-producer-admission.md` @ `e59f517fff161ab882aa0ddc4a5bda513964ae1a`; `04-memory-compiler/forget-fence-and-derived-registration.md` @ `00e37ba56596e710513c8d0568acd79141d9101b`; `04-memory-compiler/phase-3.6-producer-publication-conformance.md` @ `a21f81dfe53ae6998818d2cc59e865f5dd1b839d`; `04-memory-compiler/decision-change-log.md` @ `a5a13c33c2096fc60086e18cd4f9bef59b0b2739` | Artifact Exists. E labels Phase 3.6 design contract complete, implementation NOT VERIFIED; E36-01..20 NOT RUN. D/Storage/I/F joint decisions explicitly requested and remain OPEN. | D semantic operations and fence; Storage serialization/visibility; I current authorization; F published-only indexing. |
| Storage Atomicity | Storage | `session-storage-consistency-forget-atomicity-2026-11-16` | `3a14550648f21c0bc2725dac38b29e099c2f3196` | `reviews/storage-consistency/forget-atomicity-storage-realization-review.md` @ `5e2d55c8b210997693a7f83d35a5a03588e4ae6b` | Artifact Exists. Proposed realization only; explicitly NOT IMPLEMENTED / NOT VERIFIED. No executed transaction, crash, failover or restore evidence. Named accountable engineering approver not recorded. | D linearization semantics; E dependency/publication contract; I authorization freshness and inventory; database/replica/restore implementation. |
| B Typed Identity / Scope | B | `session-b-domain-model-phase3` | `ebf459800e2d0566182fba6b58252bf978dfafe5` | `02-domain-model/typed-reference-and-scope-semantics.md` @ `e9a6bd21e06bc02a5208619f5a949217860b1c00`; `02-domain-model/ADR-001-fact-claim-semantics.md` @ `a1024938ff5baba069cf128c69496a44e143330c` | Artifact Exists. Typed identity/scope Phase 3.6 addendum remains CANDIDATE for cross-Scope, cross-Environment and PermissionEpoch governance. ADR-001 Fact/Claim remains **ADR-BLOCKED**. | I trust/authorization and policy-domain decisions; H wire serialization; C/D/E/F/G typed-reference consumption; Architecture Governance for ADR-001. |
| I Trust / Authorization | I | `session-i-security-governance-2026-11-16` | `d52cd47972bd9d1d17f0fe6f2ab09646d084a80b` | `09-security-governance/principal-actor-and-authorization-contract.md` @ `03765efac4bb1153f303ce0030f9e277d602e81d`; `09-security-governance/phase-3.6-principal-trust-chain-authorization-revocation.md` @ `74643a2f374179128d506c3b7e1d22da77119600`; `09-security-governance/global-forget-target-inventory-and-completion-evidence.md` @ `9100061fa986fb6676656169de3fcf9fc1c72664`; `09-security-governance/threat-model-and-adversarial-test-plan.md` @ `4227ac0e26228ca3504589efdee022b5d0802e12` | Artifact Exists. I Phase 3.6 trust-chain policy is CANDIDATE / GOVERNANCE-BLOCKED; tests are specified, not executed. I explicitly records no joint B/H/C approval and no Contract Freeze. | B ActorRef/ScopeRef semantics; H authenticated transport/wire; C Agent/Applied boundary; D/E/F/G protected operations; Architecture Governance and test execution. |
| H BMCP / Adapter | H | `session-h-bmcp-protocol` | `1ee65928f123d92a4758b0de09bc8d6df1e46253` | `08-bmcp-protocol/forget-revocation-and-reconnect.md` @ `695909360782987781e259187041618f495f1c8c`; `08-bmcp-protocol/message-envelope-and-versioning.md` @ `5547ecd78d118bd63e571e5daad87194d9b694e4`; `08-bmcp-protocol/context-delivery-and-acknowledgement.md` @ `bf9732cc39d156853b507c3a3a4e573159978f49`; `08-bmcp-protocol/adapter-capability-and-applied-attestation.md` @ `ed6b43a29aa368d772c701ffc83309a5aadf3c00`; `08-bmcp-protocol/adapter-forget-ack-and-target-binding.md` @ `5e2b33898cbc6a9c95e271ecd1d8a092d04c67f8` | Artifact Exists. H wire/ACK/Applied artifacts remain CANDIDATE and subject to B/I/D/G/C approval. No current joint sign-off or implementation conformance evidence. | B typed refs; I issuer/Principal/authorization and target inventory; D ForgetFence; G Context/delivery; C final request evidence. |
| C Final Request / Applied | C | `session-c-agent-integration-2026-11-16` | `a585307222b0169c007915c25ff8ed0da517f3e4` | `07-agent-integration/final-inference-boundary-attestation.md` @ `f3b254fcfd9a652a0ec68921e801f78d93bb5163`; `07-agent-integration/phase-3.5-agent-identity-applied-attestation-untrusted-memory.md` @ `52c20764e6d74ba16392ded461690f50147f0343` | Artifact Exists. C final-request semantic proof boundary DECIDED; evidence profile CANDIDATE; H/G/I implementation dependencies OPEN. | G exact ContextVersion/delivery target; H authenticated Adapter and final-request evidence; I authorization/PermissionEpoch; D Forget fence; B typed identity. |
| F Runtime | F | `session-f-memory-runtime` | `f86f9b536ea69d8e0fbb4bf290c7023ef0eada76` | `05-memory-runtime/phase-3.5-forget-suppression-and-cursor-consumption.md` @ `99f950f9fabe97969b5ad580c9c80e52930a1423` | Artifact Exists. F runtime safety semantics DECIDED; API/backend/cancellation behavior OPEN or TO_VALIDATE; implementation and adversarial execution not evidenced. | D canonical/fence; E published-only derivatives; I authorization/revocation; G Context; H reconnect/ACK; B typed references; C disclosure boundary. |
| G Context / Applied Consumer | G | `session-g-memory-context` | `557c68fd863f73dd09f6fccb3b9e920740db2e9c` | `06-memory-context/context-reconciliation.md` @ `87063aceebed1c30b7840045ada8e3f348732688`; `06-memory-context/context-versioning.md` @ `05c0739d0c22576a1fd5affc7d73c078c89049b1`; `06-memory-context/context-edit-operations.md` @ `10c94e85dfe89d20dcdb202cafc2bef767f076fc` | Artifact Exists. Reconciliation safety ordering and ContextVersion invariants DECIDED; workflow/object encoding remains CANDIDATE; H/C/I Applied and delivery conformance OPEN. | C final-request submission boundary; H delivery/ACK; F freshness/suppression; D/E canonical and producer evidence; I policy freshness and revocation. |

## 4. Evidence grading and agreement ledger

Use only these evidence grades:

1. **Artifact Exists** — exact path and Blob SHA have been read from the stated branch.
2. **Owner Decision** — the accountable Owner explicitly marks the relevant semantic decision DECIDED. A candidate proposal or change-log request is not a decision.
3. **Cross-module Agreement** — every affected authority/consumer Owner explicitly accepts the same contract. Silence, artifact presence, source consumption, or a one-sided request is not agreement.
4. **Implementation Evidence** — executable implementation, tests or runtime evidence with reproducible results.

Current discovery disposition:

| Contract family | Artifact Exists | Owner Decision | Cross-module Agreement | Implementation Evidence |
|---|---|---|---|---|
| D CanonicalCommitCursor | Yes | D decided per-authority global sequence | Not established for all E/F/G/Storage consumers | Not supplied |
| D/E/Storage Forget atomicity | Yes | D semantics decided; E design contract complete | D/E/Storage joint physical interface not approved | Not supplied; E36 suite NOT RUN |
| B/I/H identity trust chain | Yes | B has partial typed-reference decisions; I policy candidate/governance-blocked; H wire candidate | Not established | Not supplied; I36 suite NOT RUN |
| C/G/H Applied | Yes | C proof boundary and G safety invariants decided within their owners | Not established | Not supplied |
| F/G runtime/context suppression | Yes | F/G safety semantics decided within their owners | Not established across all consumers | Not supplied |
| Prompt injection / security conformance | Yes (requirements/test plans) | Threat requirements specified; risk acceptance not recorded | Not established | Not supplied; tests not executed |
| B Fact/Claim | Yes | **ADR-BLOCKED** | Not established | Not supplied |

## 5. Work-session dependency map

| Work session | Required Owners | Baseline inputs | Required joint closure |
|---|---|---|---|
| DE-S — Forget Atomicity | D, E, Storage; I as policy dependency; F/G/H as consumers | D operation/fence and completion contracts; E producer admission, Phase 3.6 publication conformance; Storage realization review; I global inventory | Exact shared serialization/visibility contract, permission recheck, crash recovery, late derivative suppression, reproducible race/fault tests and explicit owner acceptance. |
| BIH — Identity Trust | B, I, H; C/D/E/F/G consumers | B typed-reference/scope semantics + ADR status; I Phase 3.6 trust-chain contract; H envelope, authenticated transport, Adapter binding/ACK | Authenticated transport → issuer → Principal → delegation → typed ActorRef → Scope/Environment authorization → current PermissionEpoch → protected operation, with explicit B/I/H decisions and negative-test execution. |
| CFG — Context & Runtime | C, F, G; H/I/D dependencies | C final-request attestation; F runtime suppression/cursor contract; G Context reconciliation/versioning; H delivery/Applied; I authorization and revocation | One coherent Submitted-before-Applied evidence state machine; current Forget/permission checks across retrieval, cache, reconnect, replay and delivery; explicit owner acceptance and executed conformance. |

## 6. Known baseline drift and blockers

1. **Historical Phase 3.5 review:** the A review artifact contains historical branch snapshots. Its top-level decision remains BLOCKED. This manifest re-queries the live branch tips and does not treat the embedded older SHAs as current.
2. **D Phase 3.6 addendum:** D's operation-gate artifact records its own pre-edit discovery snapshot. It confirms D semantics but explicitly says E/Storage implementation and cross-module conformance remain open. Its embedded source table is not a replacement for this manifest.
3. **E Phase 3.6 source baseline:** E's current decision/change log records D at an earlier HEAD and I at an earlier HEAD, requests explicit D/Storage/I/F decisions, and states those confirmations remain OPEN. E's design conformance matrix is NOT RUN. Do not treat E's source-baseline table as a current all-owner snapshot.
4. **B/I/H identity:** B's Phase 3.6 scope/identity addendum leaves cross-Scope grants, cross-Environment federation and PermissionEpoch partitioning governance-blocked; ADR-001 remains ADR-BLOCKED. I's Phase 3.6 trust-chain contract is CANDIDATE / GOVERNANCE-BLOCKED and explicitly reports no joint B/H/C approval. H's wire and ACK contracts remain candidate.
5. **Storage:** the Storage report is a proposed design only, explicitly NOT IMPLEMENTED / NOT VERIFIED. No named accountable engineering approver is recorded.
6. **C/F/G:** their current branch tips remain on the recorded Phase 3.5 artifacts. These contain useful Owner semantics, but do not constitute Phase 3.6 cross-owner approval or test execution.
7. **Security:** I36-T01..T20 and other adversarial cases are specifications, not execution evidence. Prompt injection, forged identity, cross-scope, revocation-race and forget-race tests are not evidenced as run.
8. **Fact/Claim:** B's ADR-001 remains ADR-BLOCKED; no canonical schema or dependent wire fields may be frozen on this baseline.

## 7. Baseline use and refresh rule

- DE-S, BIH and CFG must cite the exact branch HEAD and artifact Blob SHA from this manifest when recording a decision.
- Any Owner branch commit after this manifest changes the baseline. Re-query that branch HEAD and re-read affected artifacts before treating later work as based on the same source.
- A joint decision requires an explicit, attributable acceptance from every affected Owner in an Owner-controlled artifact or decision record. A's registry records the decision; it does not create it.
- The next integration review must re-fetch every branch HEAD and relevant artifact, verify Blob SHAs, review all changed files since this snapshot, and distinguish design evidence from executable evidence.
- This manifest does not authorize branch merges, implementation sign-off, schema freeze or Contract Freeze.

## 8. Discovery-time disposition

**BASELINE ESTABLISHED FOR COORDINATION; PHASE 3.6 CLOSURE BLOCKED.**

The branch-aware artifact inventory is available and exact file blobs were read. Owner semantic decisions exist in bounded areas, but cross-module agreement is not demonstrated and implementation/test evidence is absent. P0 blockers remain, including Forget atomicity realization, identity/scope governance and Fact/Claim ADR approval. No Contract Freeze is authorized.
