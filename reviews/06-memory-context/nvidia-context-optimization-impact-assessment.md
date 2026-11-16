# NVIDIA Context Optimization Impact Assessment

**Owner:** G — Memory Context Architect  
**Branch:** `session-g-memory-context`  
**Status:** RESEARCH ASSESSMENT / PROPOSED ONLY — no baseline or implementation change  
**Assessment date:** 2026-11-17  
**Scope:** Brain-owned Context lifecycle, compaction, semantic handoff, observation references, fidelity, versioning, reconciliation and Forget safety.

> Evidence discipline. This report separates (A) claims and results stated in the papers/project documentation, (B) behavior directly inspected in the public SoL-Pi source/tests, (C) G's architectural inference, and (D) proposals requiring validation or cross-owner approval. The research was performed by the G Owner; it is not an independent external review. No SoL-Pi experiment is represented as an AiMemoryBrain performance result.

## 1. Executive Summary

### 1.1 Main conclusion

The strongest transferable idea across both papers is **not “summarize more aggressively.” It is to separate a compact, forward-looking working state from an immutable, selectively recallable evidence history, and to compact only at meaningful state transitions under an explicit economic and correctness gate.**

G already has most of the necessary architectural homes: Context Planner, Context Editor, Budget Manager, Context Sufficiency, Compact operation, immutable Context Versions, Snapshot/Delta, Reconciler and Forget tombstones. Therefore this assessment recommends extending those semantics and evidence contracts—not creating a new Context subsystem.

### 1.2 What G should adopt, adapt, and reject

| Disposition | Mechanism | G decision |
|---|---|---|
| ADOPT (concept) | Subtask-boundary compaction candidate | Use completion boundaries as evaluation opportunities, never as unconditional compaction commands |
| ADAPT | SoL-Pi economic gate | Replace fixed benchmark/config constants with G-specific marginal utility, confidence bounds, cost model, recovery cost and safety vetoes |
| ADAPT | Semantic State / SAC handoff | Maintain a typed, versioned Task Semantic State projection; SAC is an optional operating mode only after task-class validation |
| ADOPT (concept) | ObservationPack stable handle + exact recall | Add reference metadata to existing Context Entry/source-ref contracts; do not create an independent retrieval/index subsystem |
| ADAPT | Evidence-Preserving Reducer | Reuse deterministic source-hash and exact-quote verification as one layer; add epistemic, temporal, scope, permission and negative-evidence checks |
| ADAPT | Immutable archive + targeted rehydration | Keep source evidence immutable and recallable under current authorization; archive retention must obey Forget and I policy |
| REJECT as G authority | Action Fusion | It changes action execution/tool semantics; belongs to Agent/Adapter/Runtime, not G |
| REJECT as-is | SoL-Pi default thresholds, cache ratios, 10KiB/4KiB thresholds, 2 full sends, excerpt sizes | Workload/runtime-specific experiment settings, not production requirements |
| REJECT | Summary as canonical truth | Compaction never creates Canonical Memory or upgrades evidence status |
| REJECT | Direct transplantation of Pi session-log lifecycle | G's versioning, producer registration, D publication gate, I authorization and H Applied proof are stricter and remain mandatory |

### 1.3 Highest-priority engineering recommendations

1. Add a **G-owned compaction decision record** to the existing Budget Manager/Compact workflow, including estimated future request horizon, marginal context savings, compaction write/cache cost, recovery cost, confidence and reason.
2. Define a **Task Semantic State (TSS)** as a versioned Context projection distinct from Canonical Memory and from Agent-private working state.
3. Add a **Context Observation Reference** as a typed reference contract, initially represented through existing Context Entry source/projection references. A separate durable object should be decided only if cross-context sharing, retention, paging, revocation or lineage demands prove that a simple ref is insufficient.
4. Introduce a **six-axis fidelity validator** with hard rejection conditions, exact source anchors and a recoverable source archive. No fidelity score can override hard constraints.
5. Extend the existing Compact operation and ContextVersion/ChangeSet metadata; publish compacted artifacts only through the existing D producer-registration/dependency-registration/final publication gate and current I authorization.
6. Make Forget invalidation apply to semantic states, observation references, compacted derivatives, snapshots, deltas, caches and pending recall, not only visible entries.
7. Benchmark against FHA, EoCC-like and selective-observation baselines using paired task outcomes and frozen held-out tasks. Efficiency is accepted only behind capability non-regression gates.

## 2. Paper-by-Paper Technical Analysis

### 2.1 Paper 1 — “You don't need long context” (arXiv:2611.05306)

**Primary source:** https://arxiv.org/abs/2611.05306  
**Accessible full-text cross-check:** https://www.alphaxiv.org/abs/2611.05306  
**Version reviewed:** v1, submitted 2026-11-03; 31-page technical report according to the indexed paper record.

#### 2.1.1 FHA, EoCC and SAC are different operating regimes

- **Full-History Accumulation (FHA):** append each action and observation to one conversation. It preserves conversational trace in the active context but causes context growth and repeated input.
- **End-of-Conversation Compaction (EoCC):** continue normally until a configured threshold, ask the model for a bounded handoff, then start a fresh conversation with the original task and compacted state. A larger total context limit reserves room for the compaction turn; failure to complete compaction before the hard limit is a run failure/termination risk.
- **Single-Action Compaction (SAC):** each conversation receives the task and current semantic state, takes exactly one environment action, observes the result, updates the state, and is discarded. The next action starts from the new state.

These are research regimes, not three interchangeable compaction algorithms. SAC changes the execution granularity and history visibility, not merely the summary length. It should not be imposed on G's Context lifecycle: G does not control Agent action selection or execution.

#### 2.1.2 Compaction prompt and handoff structure

The paper's Appendix A handoff prompt is oriented toward *future task continuation*, not retrospective narrative summarization. The intended output preserves:
- the original task/goal and completion criteria;
- current progress and what remains;
- decisions and constraints needed for subsequent work;
- artifacts, paths, or pointers that must be revisited;
- a concise next-step plan.

The prompt asks for bounded state and discourages preserving irrelevant history. The critical design insight is that a handoff should answer “what must the next invocation know to continue correctly?” rather than “what happened in chronological order?”

**G inference:** For Memory Context, this handoff must be augmented with structured provenance, epistemic labels, validity intervals, Scope, permission and Forget metadata. A free-form task note alone cannot meet Brain guarantees.

#### 2.1.3 Long-horizon results: encouraging, not universal

The paper evaluates EoCC with Claude Opus 4.5 and GPT-5.6 Sol over six long-horizon benchmarks and several context thresholds. The accessible full-text summary reports that no more than 5 of 22 configurations per model lost more than two percentage points versus the corresponding FHA baseline; some configurations improved and others regressed.

SAC is evaluated on SWE-bench Verified and Terminal-Bench 2.1. Reported scores:
- Claude Opus 4.5: SWE-bench Verified 70.2% vs 70.0% baseline; Terminal-Bench 2.1 51.8% vs 47.2%.
- GPT-5.6 Sol: SWE-bench Verified 82.4% vs 84.4%; Terminal-Bench 2.1 84.3% vs 87.6%.

The paper therefore supports “SAC did not catastrophically collapse on these two software/terminal task suites,” not “SAC is lossless.” GPT-5.6 Sol's reported declines are 2.0 and 3.3 percentage points.

The serving-throughput result is separate: configured 16K versus 256K context produced 3.6x, 5.6x and 7x decode throughput for three tested open-weight models on H100/vLLM. This is not a claim that tasks finish 7x faster or API bills fall by 7x.

#### 2.1.4 Selective Input Reading

For long-input tasks, source documents are stored as files rather than injected wholesale into the initial prompt. The agent searches and reads bounded excerpts with ordinary tools (e.g. head/sed/awk). This converts a long-input burden into selective observations over a long horizon.

The paper reports strong LOONG results for both tested models and settings, but it also calls out limitations:
- the Needle-in-a-Haystack results are partly attributable to lexical overlap between needles and search terms;
- LongBench v2 is not uniformly improved;
- selective reading changes what the model receives; it does not prove long-context reasoning is intrinsically worse;
- selective access requires reliable recall and may fail when search terms or the task's relevant evidence are unknown.

**G inference:** Selective reading maps naturally to Observation Reference + authorized paging. The source must remain immutable and recallable; a handle is not evidence that the model can recover the correct range.

#### 2.1.5 Semantic State Space Models (SSSM)

The paper proposes SSSMs as a future training direction: a model would read a natural-language state, take an action, register its outcome and update the state for the next invocation. It is not a demonstrated new model architecture or a validated production memory database.

**G inference:** The useful architectural concept is an explicit state transition artifact. We should not claim SSSM capabilities, train a new model, or make natural-language state the canonical store. G should own only the Brain Context projection; the Agent retains its private work state and action policy.

#### 2.1.6 Long-context limitations and failure cases

The paper's coin-toss illustration demonstrates that lossy compaction can drop an outcome that becomes important later. The remedy proposed is selective search over the original transcript rather than assuming history never matters.

Other risks for G:
- rare negative constraints may be omitted from a fluent summary;
- chronology can be flattened, causing “before/after” or current/superseded confusion;
- a summary can preserve an answer but lose its evidence;
- future task needs are not always predictable at compaction time;
- an incorrect summary can become a repeated error when used as the only next-state input.

**Conclusion:** Adopt forward-looking state and selective evidence recall; never delete the source lineage merely because the current prompt no longer carries it.

### 2.2 Paper 2 — “SoL-Pi: Recursively Scaling Auto-Research Loops for Efficient Agent Harness” (arXiv:2609.20519)

**Paper:** https://arxiv.org/abs/2609.20519  
**Official project:** https://nvlabs.github.io/SoL-Pi/  
**Official source:** https://github.com/NVlabs/SoL-Pi  
**Source revision inspected:** repository tree on `main`, tree SHA `219568034fa54ed121ede80961655e33dfb9d0e3`.

#### 2.2.1 Research process and evidence quality

The project describes 152 proposed directions, six proposal families and four surviving mechanisms. The paper/project pipeline includes:
1. trajectory rollouts;
2. map-reduce analysis across trajectories;
3. mechanism proposal;
4. implementation loop;
5. a separate reviewer;
6. in-trajectory validation;
7. frozen, isolated held-out validation.

The authors describe 535 executable development environments (495 repository tasks derived from issue/PR pairs plus 40 synthetic verifier-driven tasks) and a held-out EdgeBench suite of 51 tasks. Candidates must satisfy a predeclared capability tolerance and improve at least one efficiency metric; surviving candidates are selected on a Pareto frontier.

This is a meaningful methodology lesson for G: separate proposal, implementation, review, in-sample validation and sealed held-out validation. It is not proof that all four mechanisms transfer to a governed multi-tenant Brain Context domain.

The paper explicitly notes that per-mechanism tolerances can accumulate when mechanisms are combined. The assembled harness retained roughly 94% of Pi's average score, so composition has a measurable capability trade-off.

#### 2.2.2 Online Context Compact (OCC)

**Paper/project behavior:** completed plan steps become candidate compaction boundaries. OCC does not compact merely because a step completed. It estimates future requests and expected token/cache economics, and may also compact near the native context-window limit when a compaction can shorten the context.

**Inspected implementation:**
- `online-context-compact/plan.ts`: validates bounded plan shape (maximum 128 steps, bounded strings), stable step IDs and statuses; detects only transitions from non-completed to completed as a new boundary. It warns when a step ID is reused with a changed goal or when more than one step is in progress.
- `state.ts`: appends versioned state entries to the session log, restoring plan, progress, request counts, boundary request counts, context-growth estimates, compaction count and cache debt.
- `economics.ts`: estimates requests remaining from completed boundary request counts and remaining boundaries; optionally applies a lower-bound adjustment using observed variance; caps the horizon using remaining context-window capacity and observed context-token growth.
- It calculates archive tokens, memo tokens, savings, projected post-compaction context, cache-write/read incremental cost, break-even requests, combined break-even with carried cache debt, first-compaction scaling, subsequent-compaction margin, cooldown and window-protection.
- `extension.ts`: observes public Pi context/provider request events and invokes native compaction after context transforms; a generic continuation reminder is used after success. Recoverable failure can resume the active task without compaction; cancellation is not treated as a successful compaction.
- The default implementation values (e.g. 20K retained tail, 16,384-token window reserve, first-compaction scaling, 1.5 subsequent margin, two-request cooldown) are implementation defaults, not evidence-backed constants for G.

**Important limitation:** project compatibility docs state the standalone extension uses a Pi 0.85.1 default retained-tail assumption because the public extension context does not expose the configured retained-tail setting. A programmatic factory can override it. It also notes that later-loaded third-party context transformers are outside the observed context-growth estimate. This is a concrete example of a cost model whose measurement boundary may be incomplete.

**G decision:** adopt boundary-driven reevaluation and economic reasoning. Redesign the economics with G's multi-dimensional budget, uncertainty and recovery costs. Do not import Pi's token-only approximation or static defaults.

#### 2.2.3 ObservationPack

**Inspected implementation:**
- `observation.ts` defines stable `obs_<24 hex>` IDs, SHA-256 content hash, source path, tool name, text, byte/line/token counts.
- Tool results above 10 KiB are archived; the first two provider requests carry the full observation; later context projections replace it with a stable handle, source sizes, a compact complete-line head/tail excerpt and an `obs_recall` instruction.
- Recall uses bounded byte-offset chunks, limits, UTF-8 boundary handling and regular-file/no-follow file opens.
- `index.ts` projects only provider context; stored session history remains intact. Evidence-Preserving Reducer receipts are excluded from repacking so that a verified receipt is not replaced by a generic excerpt.
- Tests cover threshold behavior, repeated provider projection, stable handles, recall offsets, filesystem paths and symlink defenses.

**Strength:** it separates “what the next model call sees” from “what the source archive retains,” and makes the exact source recallable.

**G gap:** a local file path and session ID do not constitute a Brain-grade provenance/security identity. G needs source revision, source hash, immutable lineage, Scope, principal/tenant, Agent/task/environment binding, access scope, permission epoch, Forget fence, validity and revocation checks at every recall. Paging must be range-bounded and audited.

#### 2.2.4 Evidence-Preserving Reducer (EPR)

**Inspected implementation:**
- Reducible diagnostic outputs are selected through a command/result eligibility gate; nested tool results are skipped.
- Original content is archived and hashed before the reducer call.
- The reducer prompt treats the log as untrusted data, requests a bounded JSON receipt, forbids diagnosis/fix recommendations, and asks for exact contiguous quotations with evidence kinds (fatal, failure, warning, target, summary).
- `receipt.ts` verifies schema, source SHA-256, expected status versus observed error state, quote length and exact quote occurrence in source; a failing log with failure signals must retain at least one fatal/failure quote.
- The reducer result is accepted only if it is smaller; likely-secret detection, unsupported command/result shape, model failure, invalid JSON, invalid source hash, unverifiable quote or mismatch all cause original-output fallback.
- Reducer model provider/model are configured and resolved through Pi's model registry; remote reduction can expose logs to a second model provider.

**Strength:** the reducer is a candidate generator, not a trusted author. A deterministic verifier checks a narrow set of claims and the original remains the fallback.

**Limit:** exact quote existence does not prove that the quote is sufficient, correctly classified, current, representative, non-misleading or authorized. A receipt can quote true lines yet omit the decisive counterexample. Secret detection is explicitly not complete. This cannot satisfy G's six-axis fidelity alone.

#### 2.2.5 Action Fusion

Action Fusion combines a file edit/write and an immediately adjacent follow-up command when no intermediate inspection is required. It reduces a model round trip, but can alter execution semantics. The code guards against changed file contents before running the follow-up command; tests cover paths and validation behavior.

**G decision:** do not adopt into G. It belongs to tool/runtime orchestration and must be reviewed by the Agent/Adapter owners. G may consume the resulting observation and verifier evidence but cannot authorize or execute the action.

#### 2.2.6 Results and limits

The paper reports EdgeBench cost/token improvements against Pi but also a lower aggregate score for the complete stack. The official project reports approximately 94% of Pi's average score, 45–49% fewer tokens and roughly one-third lower cost versus Pi on the tested backends. It also reports a Terminal-Bench 4 comparison where SoL-Pi solved fewer tasks than Pi/Codex in that experiment, at lower API-equivalent cost.

These results are not an AiMemoryBrain service-level guarantee. They use specific models, task distributions, runtime, prices and configurations. The project also explicitly warns that the combined stack can accumulate per-mechanism capability losses.

## 3. Existing G Architecture Assessment

The six baseline documents were read on `session-g-memory-context`:
- `06-memory-context/context-architecture.md`
- `06-memory-context/context-manager.md`
- `06-memory-context/context-edit-operations.md`
- `06-memory-context/context-versioning.md`
- `06-memory-context/context-reconciliation.md`
- `06-memory-context/context-budget-and-sufficiency.md`

### 3.1 Existing homes — do not duplicate

| Research requirement | Existing G home | Gap / extension required |
|---|---|---|
| Boundary detection and candidate plan | Context Planner / Manager | Add explicit semantic-boundary signal and boundary confidence; no new planner |
| Cost/sufficiency | Budget Manager + Context Sufficiency | Add expected remaining demand, compaction cost, recovery cost and confidence |
| Compaction operation | Context Edit Operations: Compact | Add fidelity report, source coverage and validation outcome |
| Immutable result | Context Versioning / ChangeSet | Add compaction lineage, parent version and TSS revision linkage |
| Source drift | Context Reconciliation | Reconcile observation refs, derived states and archive availability |
| Evidence lineage | Context Entry source/evidence refs | Add typed ObservationRef contract and access/revocation checks |
| Delivery | Snapshot/Delta + H | Prevent stale compacted projections from re-entering applied context |
| Forget | Existing G tombstone + D/I/H protocol | Extend invalidation to all derivatives and recall handles |

### 3.2 Architectural boundaries confirmed

The existing architecture correctly distinguishes Canonical Memory, Brain-owned Memory Context and Adapter-attested Applied Context. G owns desired Context state, not Agent-private working state, retrieval ranking/indexes, BMCP transport or Agent actions. Context Remove is not Forget. Compaction is a derived Context artifact, not Canonical Memory. Applied remains an Adapter proof at the final inference boundary.

### 3.3 Critical existing constraint

Current G Phase 3.5 design requires D producer registration and complete dependency lineage before derivative work/publication, and a D final publication gate with current I authorization. If the shared/recoverable publication boundary cannot be proven, the staged artifact remains private and no Context head or sendable delivery is advanced. This rule applies to compacted Context and Observation-derived artifacts without exception.

## 4. Mechanism-Level Comparison

| Mechanism | Research value | G fit | Decision |
|---|---|---|---|
| FHA | Reference baseline, preserves all transcript | Useful as benchmark/control, not target state | Keep as experimental baseline |
| EoCC | Lower active context, periodic state handoff | Fits existing Compact lifecycle | Adapt with validation and versioning |
| SAC | Extreme compact state between actions | Useful stress test for TSS completeness | Do not make default |
| Selective Input Reading | Avoid full injection of large inputs | Fits Observation Reference and paging | Adopt concept; strict auth on recall |
| SSSM | Explicit language state between invocations | Inspires Task Semantic State | Adapt concept; not a model/brain module |
| OCC | Boundary + expected payback decision | Fits Budget Manager | Adapt |
| ObservationPack | Stable handles + exact recall | Fits Context Entry/source refs | Adopt concept, harden object contract |
| EPR | Model-generated receipt + deterministic checks | Fits Compact fidelity pipeline | Adapt, never trust summary alone |
| Action Fusion | Avoid redundant action round trip | Outside G | Reject for G ownership |

## 5. Proposed Context Lifecycle Model

### 5.1 Lifecycle stages

1. **Observe:** ingest candidate tool/Agent/environment observation metadata as a scoped reference. G does not ingest private CoT.
2. **Admit:** verify identity, Scope, environment binding, permission epoch, Forget fence, source revision/hash, classification and lineage before making a reference eligible.
3. **Project:** Context Planner chooses active entries and a task-specific semantic-state projection under existing vector budget and sufficiency.
4. **Accumulate:** retain source refs, verified progress, unresolved issues and recent observations while the current task continues.
5. **Boundary Evaluate:** at a completed subtask, verified milestone, phase transition, budget pressure or impending window risk, Budget Manager evaluates whether compaction is beneficial.
6. **Prepare Compact:** create a private candidate projection and fidelity report. Preserve full source refs and immutable pre-compaction Context version.
7. **Validate:** run hard fidelity gates and task-specific sufficiency checks. Any uncertain/failed hard gate rejects.
8. **Publish:** register derivative producer and full dependency lineage with D; recheck current I authorization and D ForgetFence at the final visibility gate. No local check-then-publish.
9. **Version:** successful non-no-op compaction creates a new immutable ContextVersion and ChangeSet; retain parent/source lineage and diff metadata.
10. **Deliver/Apply:** Snapshot/Delta flow through H; only Adapter final-boundary evidence can establish Applied.
11. **Recall/Reconcile:** authorized paging can rehydrate evidence. Source revisions, permissions, Forget, expiry and delivery drift trigger existing Reconciler.
12. **Forget:** deny/tombstone first; invalidate compacted derivatives, observation refs, TSS revisions, snapshots/deltas, recall/cache and pending delivery before physical cleanup.

### 5.2 Subtask boundary semantics

A boundary is a *decision opportunity*, not a command to compact. Valid boundary signals include:
- a plan step changes from active to completed with supporting evidence;
- a task phase transitions (discovery → implementation → verification);
- a verified artifact or checkpoint is committed;
- a task is paused/handoff is requested;
- predicted context pressure threatens a hard limit.

A step marked “completed” by a model is only a reported state. If a boundary's completion semantics require a verifier, G must retain the distinction between declared completion and independently verified completion. G does not itself decide that the Agent may proceed.

## 6. Dynamic Compaction Decision Model

### 6.1 Inputs

Use the existing Budget Manager; add the following candidate measurements:

- (C_a): estimated tokens/bytes in the active source segment that compaction can remove from repeated context.
- (C_m): expected compacted semantic-state size.
- (C_w): write/rewrite cost, including compaction request, cache-prefix discontinuity, validation and publication overhead.
- (C_r): expected recovery cost if a later task needs omitted evidence (lookup, paging, rehydration, additional inference, possible lost work).
- (H): expected number of future provider requests before task/session end or next full reset.
- (p_i): probability that omitted information will be needed again, stratified by evidence/requirement class.
- (G_c): expected context-growth per future request.
- (W): remaining safe context-window capacity, including protected reserve.
- (Q): confidence interval / uncertainty for H, (p_i), (G_c), and model token estimates.
- (S): hard safety/sufficiency/fidelity state.
- (F): current Forget, authorization, source lineage and Scope validity.

### 6.2 Decision principle

A compaction candidate is eligible only if all hard constraints pass. For eligible candidates, compare the expected avoided repeated cost against rewrite and expected recovery costs:

[
V_{compact} = H cdot (C_a-C_m) - C_w - sum_i p_i C_{r,i}
]

This is a conceptual value function, not a production formula or direct port of SoL-Pi. Use a conservative lower confidence bound for (H) and savings, and an upper confidence bound for recovery cost. The model should also account for cache behavior separately rather than assuming token counts equal monetary cost.

Decision:
- compact when conservative expected value is positive by a calibrated margin and all hard gates pass;
- defer when the value is uncertain or boundary is weak;
- compact for window protection only when the compact candidate passes fidelity/safety and the uncompressed context is at risk;
- reject if compacted state is not smaller, recovery is unavailable, or a hard fidelity/scope/permission/Forget check fails.

### 6.3 Dynamic threshold

Avoid a fixed “compact at N tokens” rule. Derive the trigger from:
- predicted remaining horizon;
- context growth rate and variance;
- distance to hard window limit;
- active vs deferred evidence;
- marginal savings;
- source recall cost and availability;
- compaction latency and model price;
- cache-prefix reuse loss;
- compaction count and recent compaction debt.

A boundary can cause a low-cost *evaluation* even when the threshold is not met. A cooldown/hysteresis term should prevent repeated compaction on nearly identical state. A compaction is not eligible if the prior compaction has not reconciled/published, or if a previous failure left an unresolved candidate.

### 6.4 Avoid repeated compaction

Use a source-membership fingerprint and compaction profile version. If no eligible source entries changed, the previous compacted output remains valid for that source set and profile; do not recompute. If output expansion cost exceeds future savings, defer. If a compacted TSS is compacted again, fidelity must be evaluated against the original source lineage, not merely the previous summary.

### 6.5 Cost and complexity

Complexity: **medium-high**. Most measurements fit Budget Manager, but horizon estimates and cache economics require telemetry from C/H/runtime. Cross-owner approvals: F for source recall costs and completeness; H/C for request/token/cache metrics; I/D for safety gates. No new service is required.

## 7. Semantic State Model

### 7.1 Separate three authorities

- **Canonical Memory:** D-owned, governed facts/claims/entities/relations/evidence. TSS cannot mutate or promote it.
- **Task Semantic State (TSS):** G-owned, versioned, scoped projection of the current task's continuation-relevant state. It is a working context artifact, not a truth authority.
- **Agent-private working state:** plans, scratch work, local files, internal reasoning, execution state and other private details owned by the Agent/runtime. G does not claim completeness or ownership.

### 7.2 Proposed TSS contents

| Field group | Required content |
|---|---|
| Identity | TSS ID/revision; Context ID/Version; Principal/Scope; Agent/instance; Session; Task; Environment when applicable |
| Goal | Original task intent reference and explicit completion criteria; preserve source/user authority |
| Progress | Completed, in-progress, pending, blocked; distinguish declared vs verified |
| Verified facts | Exact claims with Canonical Memory/evidence/Observation refs, epistemic state and verifier receipt |
| Decisions | Chosen design/decision plus actor, rationale category, time and evidence refs; not hidden CoT |
| Constraints | Scope, hard requirements, non-goals, permissions, environment invariants, time/quantity/unit qualifiers |
| Uncertainty | Unknowns, conflicts, missing evidence, retrieval incompleteness, confidence and last validation |
| Failures | Attempt fingerprint, exact failure evidence refs, rejected hypothesis and why it was rejected; do not infer absence from a compact note |
| Artifacts | Immutable artifact refs, source revisions/hashes, locations and authorized recall capability |
| Next work | Explicit remaining tasks, dependencies and blockers; descriptive only, never executable action authority |
| Temporal state | Valid-time, observed-at, superseded/retraction and expiry markers |
| Provenance | Producer, model/profile, source lineage, compaction lineage, validation report and output hash |

### 7.3 Semantic labels

Each statement must preserve at least one explicit epistemic label:
- **Observed:** directly returned by an authenticated observation source; observation itself may still be unverified.
- **Reported:** asserted by a user/Agent/external source without independent verification.
- **Inferred:** derived reasoning with derivation refs and uncertainty.
- **Verified:** passed a named verifier against an identified source/version and scope. “Verified” is bounded to that verifier's claim and time.

Do not silently promote Reported/Observed/Inferred to Verified. A verification receipt can itself expire or become stale when source revision, environment or policy changes.

### 7.4 Versioning and continuity

TSS has its own monotonically increasing revision within a ContextVersion lineage, but it is not a new global version authority. The authoritative visible state remains G ContextVersion. A TSS revision is bound to exact ContextVersion, source set, profile and task identity. A compaction creates a new immutable ContextVersion; its TSS revision points to its parent TSS and complete source lineage.

Multi-stage compaction must preserve original source references and accumulated loss ledger. The validator compares the new state with both the immediate parent and original source coverage. Never recursively summarize a summary without source-grounded validation.

### 7.5 Authority and epistemic failure

TSS is not a source of Canonical Fact. When a TSS claim conflicts with D canonical state, D wins; G invalidates/reconciles the projection. When source evidence is unavailable, TSS can preserve the claim as unresolved but cannot restate it as verified. A summary that lacks source evidence remains a lossy presentation, not a replacement source.

Complexity: **medium** for a structured projection over current Context; **high** if TSS is treated as an independently persisted subsystem. Recommendation: first implement as an existing Context projection and revisioned metadata, not a new module.

## 8. Observation Reference Design

### 8.1 Decision

G needs a typed **Context Observation Reference contract** for large tool outputs, long observation records and external inputs. Do not create a separate Observation Service or retrieval index in this assessment. Represent references through existing Context Entry/source refs initially. Revisit a separate object only if cross-Context deduplication, independent retention, paging, revocation or ownership requires its own lifecycle.

F owns retrieval algorithms and indexes. G owns Context membership and eligibility. D owns canonical memory and producer lineage. H owns transport. Observation Reference is not Canonical Memory and does not automatically become retrievable by every Agent.

### 8.2 Proposed fields

| Field | Meaning / validation |
|---|---|
| ObservationId | Stable opaque ID; never content-derived as sole identity |
| SourceReference | Typed source locator and source kind; no arbitrary path dereference |
| ContentHash | SHA-256 or approved digest of immutable bytes plus canonicalization profile |
| SourceRevision | Immutable revision/etag/commit/sequence or explicit “unversioned” state |
| Task/Agent/Environment Binding | Exact owner/task/session/environment binding; no cross-task implicit reuse |
| AccessScope | Typed ScopeRef, principal, allowed operation and classification |
| Validity | Observed-at, valid-time, expiry, source availability and supersession |
| Paging | Byte/line/page ranges, encoding, stable offset semantics, maximum limits |
| Provenance | Producer/tool/source identity, timestamp, request/correlation and transitive lineage |
| Revocation | ForgetFence cursor, permission epoch, tombstone state, recall deny state |
| Integrity | Hash, byte/line count, storage integrity and verification profile |
| Retention | Owner-defined retention class, storage location class and cleanup policy |

### 8.3 Recall contract

1. Authenticate caller and resolve exact Task/Agent/Environment/Scope.
2. Check current I PermissionEpoch and D ForgetFence for the observation's canonical/transitive lineage.
3. Check source revision and content hash; if drifted, return STALE_REFERENCE, never silently serve new bytes.
4. Validate access scope, validity, retention and revocation.
5. Read only requested bounded ranges; preserve encoding and offsets; include source hash and range in response.
6. Audit the recall decision and range; do not expose existence/size to unauthorized callers.
7. On failure, return typed status (denied, forgotten, expired, unavailable, stale, integrity-failed, out-of-range); do not fall back to an unscoped path.

### 8.4 Ownership options

- **G Context Entry/reference:** best initial fit because references are used only through a scoped Context projection; G controls eligibility and version membership.
- **F Retrieval Reference:** F may maintain an index/locator for finding candidate observations, but it must not become the authority for permission, Forget or source identity.
- **Independent data object:** only if an observation has lifecycle/retention/sharing independent of a Context. Requires an explicit owner, likely D/Storage/I coordination, and a separate approval. Not proposed now.

Complexity: **medium** for metadata and a read-through contract; **high** for durable storage, paging, retention and revocation. Cross-owner approvals: F (recall/query semantics), H/C (producer/source identity), D/Storage (lineage and durable artifact gate), I (Scope/classification/permission), E/D (Forget propagation).

## 9. Compaction Fidelity and Validation

### 9.1 Six hard fidelity axes

| Axis | Required preservation | Example failure |
|---|---|---|
| Semantic | Task goal, dependencies, relationships, negation, causal ordering | “A is not compatible with B” becomes “A compatible with B” |
| Evidence | Exact source refs, quotes/ranges, hash, verifier receipt, negative results | A test failure disappears from a success summary |
| Epistemic | Observed/Reported/Inferred/Verified and confidence | Reported user claim becomes verified fact |
| Temporal | Observed-at, valid-time, expiry, before/after, supersession | Old config becomes current |
| Constraint | Units, quantities, bounds, preconditions, exceptions, scope | “only if X” or “not above 5” is omitted |
| Scope/Permission | Principal, tenant, task, environment, classification, allowed recall | Cross-task observation is included in another task |

### 9.2 Validator architecture

A candidate compaction is accepted only if:
1. **Deterministic structural checks** pass: schema, required fields, size bounds, valid IDs, hashes, source lineage and exact range anchors.
2. **Source coverage checks** pass: every retained material claim maps to authorized source evidence; every critical source requirement is either preserved or explicitly declared omitted with a safe status.
3. **Negative/contrast checks** pass: negation, failed outcomes, counterexamples, exceptions, conflict alternatives and “not found” vs “not searched” remain distinguishable.
4. **Temporal/constraint checks** pass: dates, units, quantities, thresholds, conditions and valid-time are preserved.
5. **Epistemic checks** pass: no status promotion, conflict collapse or unsupported certainty.
6. **Scope/security checks** pass: all sources remain in same authorized binding; current permission and Forget fence are checked before publication and recall.
7. **Task sufficiency checks** pass: mandatory requirement coverage remains sufficient for the task profile.
8. **Size/economic checks** pass: result is smaller enough to justify write and recovery cost.

LLM-as-judge can be used as an advisory detector, never as the sole hard validator. Deterministic checks can verify structure and exact quotes but cannot fully prove semantic equivalence. High-risk compaction needs independent review or conservative no-compaction fallback.

### 9.3 Outcomes

- **ACCEPT:** all hard checks pass; publish new ContextVersion through D gate.
- **ACCEPT_WITH_DECLARED_GAPS:** only if task profile explicitly allows named non-critical gaps and sufficiency is Conditional; no hidden omissions.
- **REJECT:** semantic/epistemic/temporal/constraint/scope loss or unsupported claim.
- **QUARANTINE:** source hash mismatch, integrity issue, uncertain lineage, authorization unknown, Forget race or incomplete dependency registration.
- **ROLLBACK:** never mutate old version; retain it as historical/audit-only and create a compensating ChangeSet if a published successor is later found defective. Block delivery of defective version immediately.

### 9.4 Human escalation

Escalate when critical facts conflict, evidence cannot be recalled, a negative result may be material, high-impact decisions depend on the compacted state, or independent validation disagrees. G cannot decide user intent or Agent action. Preserve exact unresolved gaps.

## 10. Versioning and Reconciliation

### 10.1 Version rule

A successful non-no-op compaction changes desired Context content; therefore it creates one new immutable ContextVersion and ChangeSet. It must include:
- Base/Target ContextVersion and parent TSS revision;
- exact source ContextEntry IDs/revisions, MemoryVersion refs and ObservationRefs;
- source hashes and canonicalization profile;
- compaction model/algorithm/prompt/profile version;
- output hash and declared omissions/loss;
- fidelity report and sufficiency report;
- producer registration, dependency receipt and final D publication-gate evidence;
- I PermissionEpoch and D ForgetFence cursor used at final publication;
- created-at, actor/producer and correlation/causation.

A compaction must not mutate a historical snapshot or silently rewrite a prior version.

### 10.2 Snapshot/Delta behavior

- Snapshot is the complete desired state at TargetVersion, including TSS and current eligible references.
- Delta is a deterministic transition from exact BaseVersion to TargetVersion and includes the same compacted projection hash/lineage.
- Old Snapshot/Delta must be rejected if target is superseded, source revision changed, Scope/permission epoch stale, Forget fence advanced, schema/capability incompatible or base hash mismatch.
- Compacted entries cannot be reintroduced from a historical Delta just because the entry remains in the old archive.
- Applied proof remains per Adapter/session/inference request; compacted version does not imply Applied.

### 10.3 Reconciliation

Existing Reconciler handles source revision, expiry, permission, retrieval freshness, delivery drift and Forget. Extend its affected-reference inventory to TSS/ObservationRef/compaction lineage. Reconcile source status before attempting a new compaction. A stale or incomplete F index does not authorize dropping a reference; missing results remain incomplete/unknown.

## 11. Forget and Security Implications

### 11.1 Forget wins over compaction

The linearization rule must be: **Forget Fence/tombstone wins before any later compaction publication or recall can expose the target.** Compaction is a derivative producer and must register all transitive dependencies with D before execution/publication.

A race is handled as follows:
- If Forget fences first, compaction is blocked or quarantined; it cannot publish.
- If compaction publishes first, the subsequent Forget invalidates that compacted derivative and all downstream snapshots/deltas/caches/recall handles.
- If ordering/registration receipt is unknown, no visibility/sendability is allowed.

A compacted summary that paraphrases a forgotten fact is still a derivative containing that fact. Deleting only the direct source pointer is insufficient.

### 11.2 Required invalidation surfaces

- Observation archives and every page/range recall handle;
- TSS revisions and parent-derived summaries;
- Context Entries, compacted projections, ContextVersions and ChangeSets;
- Snapshot/Delta packages and outbox/queues;
- G caches and F caches/index projections (F owns cleanup of its own surfaces);
- pending delivery and Adapter managed-region state (H owns adapter clear);
- offline Adapter buffers and reconnect replay;
- historical audit material subject to I retention policy.

### 11.3 Offline adapters and stale recall

An offline Adapter remains Pending/Unknown. On reconnect it must authenticate, refresh I PermissionEpoch and D ForgetFence, discard stale local materialization and cached recall, reconcile current G head and obtain a safe Snapshot/clear set before use. A previously valid TSS or ObservationRef cannot authorize stale data after reconnect.

### 11.4 No weakening of owner boundaries

- D: canonical Forget identity, fence, producer registry, dependency ledger and publication gate.
- E: canonical change/retraction/Forget event propagation.
- F: retrieval/index/cache completeness and invalidation for F-owned data.
- G: Context/TSS/ObservationRef membership and derivative invalidation.
- H/C: delivery/application/Adapter final inference boundary and clear attestations.
- I: Scope, permission epochs, classification, target inventory and global Forget completion.
- Storage/Consistency: atomic/recoverable visibility and persistence proof.

G cannot claim physical erasure from external model/provider internals or erase already-processed tokens.

## 12. Failure Modes and Negative Tests

All cases below are **proposed test scenarios**, not tests already executed.

| ID | Failure injection | Required result |
|---|---|---|
| G-NC-01 | Compaction omits a negation (“not allowed”, “never”, “not compatible”) | Fidelity reject; old ContextVersion remains current |
| G-NC-02 | Reported/Observed/Inferred statement is relabeled Verified | Epistemic reject; preserve source label and uncertainty |
| G-NC-03 | Timestamp, unit, numeric bound or condition is dropped | Constraint/temporal reject; no publication |
| G-NC-04 | Two conflicting claims are merged into one synthetic fact | Reject or preserve both with conflict marker |
| G-NC-05 | Failure log compaction retains only success-like lines and omits failure evidence | Reject; original log/receipt remains available |
| G-NC-06 | ObservationRef source bytes change but ID is reused | Hash/revision mismatch; STALE_REFERENCE; no silent re-read |
| G-NC-07 | Forget Fence races with compaction after source read but before publication | D final gate rejects or artifact remains private/quarantined |
| G-NC-08 | Forget occurs after compact version publication but before Snapshot/Delta send | Tombstone invalidates version/derivative; no send/apply |
| G-NC-09 | Old TSS/Delta replays a forgotten paraphrase after Adapter reconnect | Reject replay; clear/quarantine; refresh permission/fence |
| G-NC-10 | Permission epoch changes between validation and recall | Recall denied; no cached bypass |
| G-NC-11 | Observation paging asks beyond allowed range or through path traversal/symlink | Reject; bounded read only; no arbitrary filesystem access |
| G-NC-12 | Repeated compaction recursively summarizes a previous summary with no source revalidation | Reject/quarantine; compare against original source lineage |
| G-NC-13 | Horizon estimate is unavailable or highly uncertain while no window risk exists | Defer economic compaction; keep current context |
| G-NC-14 | Compaction fails/cancels after boundary event | Preserve old ContextVersion; continue without compaction; record failure |
| G-NC-15 | Late old Snapshot/Delta/Applied ACK arrives after newer version or Forget | Historical evidence only; never roll back head or restore forbidden data |
| G-NC-16 | F index omits an observation due to lag/truncation | Mark completeness Unknown/Partial; do not infer absence or delete reference |

### 12.1 Test evidence requirements

Each PASS must include executable test ID, exact source fixtures, initial state, injected race/failure, expected and actual outcome, deterministic reproduction, logs/hashes and owner sign-off. A design table is not an executed test report.

## 13. Benchmark and Experimental Plan

### 13.1 Baselines

Run matched task sets across:
- FHA-like full context (reference control);
- EoCC-like periodic compaction;
- boundary-triggered dynamic compaction;
- selective ObservationRef with exact paging;
- boundary compaction + ObservationRef;
- TSS-based SAC-like single-action mode for a limited stress-test subset.

Do not conflate long-input selective reading with long-horizon compaction.

### 13.2 Task strata

Include long-horizon coding/research, multi-document QA, long logs, multi-step memory tasks, temporal updates, conflicts, negative constraints, environment-bound tasks, multi-Agent/task isolation, high-risk policy/permission cases, and Forget/reconnect races.

### 13.3 Metrics

- capability: task success, verifier pass rate, regression count, constraint violation, critical evidence recall;
- fidelity: six-axis failure rate, omission precision, epistemic promotion count, conflict preservation, source-anchor resolution;
- economics: input/output/cache tokens, provider cost, compaction call cost, recall call cost, total request count, latency, CPU/storage;
- recovery: exact evidence rehydration success, time-to-recall, stale ref rejection, recovery inference overhead;
- safety: unauthorized recall, post-Forget reinjection, stale Snapshot/Delta replay, offline reconnect leak;
- operational: compaction frequency, no-op rate, repeated-compaction rate, failure/fallback rate, publication-gate rejection, reconciliation lag.

### 13.4 Experimental controls

Use paired runs on same tasks/model/runtime and frozen prompts/profiles; randomize arm order; record model version and tokenizer; separate search/training from sealed held-out tasks; predeclare capability tolerances and stop conditions. Evaluate each mechanism independently before combinations. Do not feed held-out results back into candidate tuning. Include confidence intervals and task-level paired differences, not only aggregate mean.

### 13.5 Acceptance gate

A candidate may be considered for adoption only if:
1. all security/Forget invariants pass;
2. no critical fidelity regression occurs;
3. task capability remains within a predeclared non-regression margin;
4. at least one efficiency metric improves materially;
5. recovery latency and cost remain within declared service objectives;
6. cross-owner interfaces are approved and executable tests pass.

## 14. Cross-Owner Dependencies

| Owner | Required decision/interface |
|---|---|
| A — Integration | Accept system-level boundary: TSS is G Context projection, not canonical or Agent-private state; authorize benchmark gates |
| B — Domain Model | Typed ObservationRef/SourceRef and epistemic/temporal field compatibility |
| C — Agent Integration | Task/subtask boundary signals, declared-vs-verified completion and TSS handoff semantics; no private CoT dependency |
| D — Memory Brain | Canonical source lineage, producer registration, dependency registration, Forget fence and final publication gate for compacted derivatives |
| E — Compiler | Revision/retraction/Forget event ordering and derivative invalidation triggers |
| F — Runtime | Retrieval/reference lookup, paging/completeness, recall cost/latency and F cache/index invalidation |
| H — BMCP/Adapter | Snapshot/Delta encoding, observation reference delivery semantics, final-boundary Applied proof and clear/reconnect protocol |
| I — Security/Governance | Scope, classification, permission recheck, retention, Forget target inventory and global completion |
| Storage/Consistency | Durable immutable observation storage, range reads, hash verification, atomic/recoverable publish gate |

No interface is frozen by this assessment.

## 15. Adopt / Adapt / Reject / Open Questions

### ADOPT (concepts)
- Semantic-boundary evaluation opportunities.
- Forward-looking continuation state rather than narrative summary.
- Immutable source archive with exact, bounded recall.
- Evidence receipts verified against source hashes and exact quotations.
- Separate capability floors and held-out validation.
- Preserve failed attempts and negative evidence.

### ADAPT
- OCC economics → G vector budget, conservative horizon, recovery cost, cache discontinuity, uncertainty and safety veto.
- SAC → TSS stress test; retain normal multi-action Agent semantics unless a task class proves safe.
- ObservationPack → typed ObservationRef in existing G Entry/source refs with current authorization and Forget checks.
- EPR → candidate receipt + deterministic source verifier + six-axis semantic/epistemic validator + original fallback.
- Plan progress → verified boundary event contract; plan is a hint unless completion evidence is present.

### REJECT
- Copying SoL-Pi thresholds/default parameters into production.
- Treating a model-authored plan step or summary as verified completion.
- Replacing canonical memory with TSS or summary.
- Using exact-quote validation as a complete fidelity proof.
- Allowing local archive path or stable ID to bypass Scope/permission.
- Importing Action Fusion into G.
- Claiming SSSM is implemented/proven.
- Allowing compaction publication outside D/I producer/fence gate.

### OPEN QUESTIONS
1. Does B already define a typed generic source artifact reference that can carry ObservationRef without schema duplication?
2. Should F own a retrieval locator only, or is any persistent observation index needed at all?
3. What durable storage owner serves original observation bytes and range reads?
4. What does C/H expose as a reliable semantic boundary event, and how is declared completion distinguished from verifier-confirmed completion?
5. Which cost/latency telemetry is available from H/runtime, including cache-write and prefix-reuse discontinuity?
6. What retention class applies to observation archives and compacted derivatives under I policy?
7. Can D/Storage provide the required atomic or recoverable final visibility gate for all compacted artifacts?

## 16. Final Recommendations

1. **Extend existing G components only.** Add decision/evidence fields to Budget Manager, Compact operation, ContextVersion and Reconciler. No new module is proposed.
2. **Introduce TSS as a typed, revisioned Context projection.** Keep it distinct from Canonical Memory and Agent-private state.
3. **Adopt ObservationRef concept with strict recall contract.** Start as an existing Context Entry/source reference; do not create a new service.
4. **Require six-axis fidelity validation and exact lineage.** Deterministic checks plus conservative semantic validation; original fallback on uncertainty.
5. **Use economic compaction only after hard safety gates.** Subtask completion triggers evaluation, not automatic compaction.
6. **Create a new immutable ContextVersion for each successful compaction.** Keep parent, source set, hashes, loss report and D/I publication evidence.
7. **Make Forget dominate every lifecycle edge.** Tombstone first; invalidate TSS, archive references, compacted summaries, Snapshot/Delta, caches, recall and offline Adapter state.
8. **Run controlled experiments before thresholds or modes become DECIDED.** SoL-Pi results are motivating evidence, not our performance commitment.

**Direct answer to the central question:** SoL-Pi's Online Context Compact boundary + payback concept, ObservationPack stable-handle/paged-recall concept, and Evidence-Preserving Reducer's source-bound deterministic verification are worth adopting in adapted form. Their runtime constants, Pi session-log implementation, local archive assumptions, narrow quote-only fidelity and Action Fusion are not suitable as direct G mechanisms. G must preserve its existing versioning, source lineage, D publication gate, I authorization, H Applied proof and Forget responsibility boundaries.
 
## References and inspected implementation

### Papers / project
- Belcak et al., *You don't need long context*, arXiv:2611.05306: https://arxiv.org/abs/2611.05306
- Liu et al., *SoL-Pi: Recursively Scaling Auto-Research Loops for Efficient Agent Harness*, arXiv:2609.20519: https://arxiv.org/abs/2609.20519
- SoL-Pi official project and research results: https://nvlabs.github.io/SoL-Pi/
- SoL-Pi repository: https://github.com/NVlabs/SoL-Pi

### SoL-Pi source inspected
- `src/sol-pi/extensions/online-context-compact/{economics,extension,plan,state,projection,tools}.ts`
- `src/sol-pi/extensions/observation-pack/{observation,index,ledger}.ts`
- `src/sol-pi/extensions/evidence-preserving-reducer/{candidate,archive,provider,receipt,index}.ts`
- `docs/{configuration,compatibility}.md`, `SECURITY.md`
- `tests/online-context-compact-*.test.ts`, `tests/observation-pack.test.ts`, `tests/evidence-preserving-reducer.test.ts`, `tests/all-mechanisms.test.ts`

### G baseline inspected
- `06-memory-context/context-architecture.md`
- `06-memory-context/context-manager.md`
- `06-memory-context/context-edit-operations.md`
- `06-memory-context/context-versioning.md`
- `06-memory-context/context-reconciliation.md`
- `06-memory-context/context-budget-and-sufficiency.md`
