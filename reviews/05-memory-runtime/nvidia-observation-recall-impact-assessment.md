# NVIDIA Observation Archive, Selective Recall & Retrieval Optimization — F Impact Assessment

**Owner:** F — Memory Runtime Architect  
**Status:** RESEARCH COMPLETE / ARCHITECTURE CANDIDATES ONLY  
**Decision class:** PROPOSED; no baseline or implementation change  
**Branch:** `session-f-memory-runtime`  
**Research date:** 2026-11-17  
**Inputs:** F runtime baseline on this branch; G Context Architecture on `session-g-memory-context`; NVIDIA arXiv:2611.05306; NVlabs/SoL-Pi public repository, documentation, configuration, compatibility/security notes and visible issue/PR history.

> This report is an impact assessment, not an implementation claim. Proposed APIs and data models below are not frozen contracts. No Rust implementation, existing baseline file, canonical schema, Context Version or other Owner branch is changed.

## 1. Executive Summary

### 1.1 Finding

**Yes: AiMemoryBrainArchitecture needs an independent Observation Archive capability within the F Runtime boundary, coordinated with G through a narrow, explicit read/selection contract.** It is not a new canonical memory type, not a second Brain, and not an automatic promotion path into Canonical Memory.

The problem is real and not covered by the current F Retrieval Engine alone: F can retrieve authorized canonical Memory candidates across structured, lexical, vector, graph, temporal and provenance channels, but large transient observations and source documents need a byte-preserving, version-bound, bounded-read substrate. Treating every log/tool output as Canonical Memory would pollute the domain model; treating it as a G Context Entry would confuse retained source material with the bounded working view.

Recommended ownership:
- **F owns** archive object lifecycle mechanics for Runtime observations: immutable byte capture, content hash, source revision binding, locators, paging/range reads, read sessions/cursors/receipts, observation metadata indexes, read budgets, cache/Working Set, completeness/freshness and safe failure behavior.
- **G owns** whether a retrieved excerpt/reference is selected into Brain-owned Context, Context Entry lifecycle, compaction policy, Context Version, ChangeSet, Snapshot/Delta and delivery coordination.
- **D owns** canonical Memory identity, canonical lifecycle and authoritative Forget state for canonical objects and any governed derivative lineage.
- **E owns** canonical commit/index publication and canonical projections; it does not thereby own F's ephemeral observation archive.
- **I/H own** policy/identity/authenticated protocol semantics. F consumes current authorization and Forget fences; it does not mint authority or declare Forget complete.
- **C/Adapter** remains responsible for what was actually materialized/applied at an inference boundary.

### 1.2 Evidence-based architectural implications

1. NVIDIA's *You don't need long context* distinguishes the amount of source/history that exists from the amount that must be in active model context. It explicitly proposes retaining conversation history and selectively reading it when needed; it does not argue that history is never needed.
2. SoL-Pi ObservationPack provides a concrete harness pattern: archive eligible large tool outputs locally, replace repeated provider-context projection with a compact handle/preview, and expose exact paged recall. It leaves stored session history intact.
3. SoL-Pi's Evidence-Preserving Reducer illustrates a distinct evidence-preserving summarization pattern: a reduced receipt is acceptable only if its quoted evidence can be checked against the archived source; on failure the original tool result remains the fallback.
4. Neither research system supplies AiMemoryBrainArchitecture's multi-principal authorization, D-owned Forget Fence, typed cursor, derivative-producer publication gate, cross-session governance or G Context versioning. Those must be designed from existing project invariants, not copied from the reference implementations.
5. Archive metadata needs structured/lexical indexing; only explicitly useful observation fragments should be eligible for semantic embedding. ANN is not a general-purpose log paging mechanism.

### 1.3 Decision recommendation

**ADOPT the capability boundary; ADAPT the mechanisms; REJECT direct adoption of SoL-Pi defaults/paths/cache ratio as production policy; keep schemas OPEN pending G/D/E/H/I review.**

No numeric page size, TTL, retention period, cache quota, ANN threshold or compaction threshold is approved by this report.

## 2. Paper Technical Analysis

### 2.1 Paper 1 — *You don't need long context* (arXiv:2611.05306)

**Source and evidence scope.** The 31-page v1 paper dated 3 Nov 2026 was inspected for its methodology, benchmark sections, SAC results and discussion. This assessment relies on the relevant main-paper sections; it does not claim an exhaustive independent reproduction of every appendix table. Its core distinction is between long-horizon history and long-input source material. The paper defines FHA (Full-History Accumulation), EoCC (End-of-Conversation Compaction) and SAC (Single-Action Compaction); these are paper-defined harness regimes, not production archive protocols.

#### FHA — Full-History Accumulation

- **Actual mechanism:** append every assistant action and environment observation to one conversation; do not remove or replace history during the run.
- **Problem addressed:** baseline for workflows whose prompt grows with every action and observation.
- **Why it is costly:** later generated tokens are more expensive/slower at greater context depth for the measured attention-based deployments; the paper reports 3.6x, 5.6x and 7x decode-throughput-derived cost differences between 16K and 256K windows for three tested open-weight deployments.
- **Conditions:** model/hardware/serving stack, KV-cache behavior, concurrency and context length matter. The reported cost curve is not a universal pricing formula.
- **Failure mode:** context growth can cause latency, cost and window pressure; it preserves more raw interaction in the active conversation but does not solve authorization, retention or search.
- **Evidence:** paper's measured serving throughput and benchmark baselines.
- **Runtime implication:** keep FHA-like complete history only in a durable source/archive layer where retention is permitted, not in every future inference context.

#### EoCC — End-of-Conversation Compaction

- **Actual mechanism:** continue a normal interaction until a configured threshold; ask the model for a bounded task-relevant handoff; start a fresh conversation with the original task and compacted state; repeat.
- **Problem addressed:** reduce active context while preserving task progress.
- **Why it can work:** many future actions depend on current state, next steps and key artifacts, not every historical token.
- **Conditions:** the task must admit a useful bounded handoff; threshold must leave room for compaction; the harness must resume with the original task and compacted state.
- **Failure/fallback:** compaction is lossy; if important detail is omitted, later actions can fail. A failed/unfinished compaction must not be treated as a valid handoff. Retained raw history/selective recall is the recovery path.
- **Evidence:** six long-horizon benchmarks; across evaluated configurations the accuracy changes vary rather than being uniformly zero. The paper reports at most 5 of 22 threshold configurations losing more than 2 percentage points for either model, and estimated cost savings of 2.2x–8.8x for Opus 4.5 and 2.4x–5.0x for GPT 5.6 Sol.
- **Runtime implication:** G's compaction is a Context operation. F can preserve retrievable source evidence but must not author or commit G's compacted Context Version.

#### SAC — Single-Action Compaction

- **Actual mechanism:** one inference context receives the task and current semantic state, performs exactly one environment action, observes its result, updates semantic state, then the harness starts a fresh conversation for the next action.
- **Problem addressed:** extreme control of active context on long-horizon tasks.
- **Why it can work:** the handoff carries forward task state rather than a transcript; each next action begins from a compact state.
- **Conditions:** state updates must retain enough future-relevant information; one-action-per-context orchestration is supported; model/tool overhead is acceptable.
- **Failure/fallback:** omission in semantic state is lossy. The paper's coin-toss example shows that a later need for the exact ith outcome cannot be met if only a bounded state survives. Retained searchable history is the proposed remedy.
- **Evidence:** on two coding benchmarks, SAC median peak context is 7–9K tokens, maximum 15–37K versus 130–200K for baselines. Claude Opus 4.5 matches/improves the reported baseline; GPT 5.6 Sol is down 2.0 and 3.3 points on SWE-bench Verified and Terminal-Bench 2.1 respectively. This is not evidence that every workload tolerates SAC.
- **Runtime implication:** SAC is a possible Agent harness policy, not an F default. F should make exact historical observations retrievable irrespective of the number of turns.

#### Selective Input Reading

- **Actual mechanism:** store long inputs as documents in the environment filesystem; the task tells the agent which documents exist; agent uses ordinary tools such as `sed`, `awk`, and `head` to read selected ranges. Long-input tasks are thereby converted into long-horizon tasks with bounded reads.
- **Problem addressed:** large source input need not be loaded wholesale into every inference request.
- **Why effective:** most benchmark questions require a small subset of source material; bounded excerpts plus iterative reading can provide enough evidence.
- **Conditions:** source must be addressable; agent needs a way to discover relevant portions; file semantics and exact source identity must remain stable; the task must permit incremental search.
- **Failure/fallback:** search miss, wrong range, source revision drift, incomplete coverage or overlooked distributed evidence. Preserve original source and return incomplete/unknown when the read plan cannot establish coverage.
- **Evidence:** seven long-input benchmarks; the paper reports broadly flat or improved scores for most tested cases and very large estimated cost savings in some tasks. These results are benchmark-specific and not a guarantee for arbitrary private corpora.
- **Runtime implication:** this directly motivates Archive Locator, bounded range/page access, source revision binding, read receipts and completeness metadata.

#### Semantic State / SSSM

The paper proposes Semantic State Space Models as a future post-training direction: a model reads a natural-language description of conversation state, selects/takes an action, registers the outcome and updates the state for the next invocation. This is a research proposal, not a demonstrated AiMemoryBrainArchitecture component or a complete formal state model. F should not create an authoritative Semantic State object. G may decide how a compact, non-authoritative task/context rendering is managed; Agent state remains distinct from canonical Memory and Brain-owned Context.

#### What is demonstrated versus inferred

- **Demonstrated:** shorter live contexts can retain strong benchmark performance in the tested regimes; selective reading can work on the tested long-input suites; exact history may still be required for some later queries.
- **Not demonstrated:** universal accuracy equivalence; an authorization-safe multi-tenant archive; production retention/forget semantics; optimal page sizes; no-recall guarantees; a general SSSM implementation.
- **F inference:** an archive plus controlled selective-read protocol can decouple source retention from active context. This is an architecture inference supported by the experiments, not a direct result of the paper.

### 2.2 Paper 2 — NVlabs/SoL-Pi

**Inspection scope.** Reviewed the official README, configuration, compatibility and security documentation; the documented ObservationPack/Evidence-Preserving Reducer/Online Context Compact behavior; test strategy/compatibility statements; and visible issue/PR history concerning paging EOF, archive restoration, long-line previews, second-send replacement, reducer archive-byte verification and no-session behavior. The available public GitHub connector did not expose NVlabs/SoL-Pi as an installed repository for direct checkout/file fetch in this session; therefore individual source/test files were not independently executed here. Source-level statements below are limited to behavior documented by the project and corroborating visible maintenance artifacts. This is an explicit evidence limitation, not a claim that CI was run by F.

#### ObservationPack

- **Actual mechanism:** the extension registers a context projection handler and an `obs_recall` tool; large tool outputs are archived under a session-derived local directory. Provider-context projection substitutes repeated large results with a stable handle and short preview. Original session history remains stored; the projection is not a destructive rewrite of the underlying session.
- **Recall:** handle-based exact paged reads expose a bounded portion of the archived observation. The source's original bytes and a JSONL ledger are kept under the session-specific archive directory.
- **Why useful:** repeated tool outputs no longer need to be resent in full on every provider request; only selected pages are brought back when needed.
- **Conditions:** stable session identity and storage directory; correct context event ordering; agent can call the recall tool; the archive remains available; tool output can be safely captured and projected.
- **Failure/fallback:** archive lookup/read or projection failures should preserve original content / fail open where possible. However, visible no-session issue #39 documents a failure path where runtime-root resolution occurred outside the per-message catch and caused an extension error; this demonstrates that fail-open claims require testing at every handler boundary. Visible PR #123 addresses EOF cursor semantics; #116 addresses one-line preview behavior; #97 addresses archive evidence restoration after session forks.
- **Evidence:** official compatibility documentation says ObservationPack changes only provider-visible messages, leaving stored history intact, and records original bytes plus JSONL ledger locally. Visible PR/issue history shows real edge-case maintenance; this is stronger than relying on README slogans but is not an independent F-run test.
- **Adaptation:** preserve raw observation immutability and exact range/page recall, but add Brain-owned authorization, Forget, retention, source-revision and offline-reconnect semantics absent from a local agent extension.

#### Evidence-Preserving Reducer (EPR)

- **Actual mechanism:** receives eligible diagnostic tool results, archives original material, asks a configured reducer model for a compact receipt, and validates output against source evidence (including source hash and exact quote checks). It falls back to original result when eligibility, provider/model, call, schema, source-hash, quote, size or likely-secret checks fail.
- **Why useful:** compression can lower prompt cost without making unverified model-generated claims authoritative; exact quotations can be checked against retained source.
- **Conditions:** configured model route/authentication, eligible input, archive integrity, exact quote semantics and secret screening.
- **Failure/fallback:** original tool result is retained when reducer checks fail. Secret detector is explicitly a precaution, not a complete scanner; remote reduction is unsafe for logs that must remain local unless separately authorized.
- **Evidence:** official compatibility/security/configuration documentation describes these paths. The public maintenance list includes PR #114 to verify existing archive bytes before decoding, #112 to constrain full-output fallback, #98 to preserve command execution status and #113 to report savings from visible tool content.
- **Adaptation:** use deterministic evidence validation for optional generated excerpts; never treat a reducer receipt as source truth, Canonical Memory or a Context Version. Retain provenance from each excerpt to the immutable archive object and exact range.

#### Online Context Compact (OCC)

- **Actual mechanism:** tracks plan boundaries, progress, context growth/request estimates and compaction debt in versioned custom session-log entries; uses native Pi compaction at a subtask boundary only when economic/window-pressure conditions justify it; after success sends a generic continuation reminder and resumes. Configuration includes a cache write/read ratio, with defaults and behavior documented by SoL-Pi.
- **Why useful:** completed subtasks are natural candidate points for compaction, and a compaction is useful only if expected future savings repay its write/recompute cost.
- **Conditions:** public Pi APIs/events and tested lifecycle behavior; plan boundary quality; valid context usage estimate; correct extension event order; continuation behavior.
- **Failure/fallback:** on compaction refusal/error/cancel, do not pretend state advanced; continue without compaction or report error according to runtime state. The compatibility doc notes Pi-specific abort/settlement/continuation behavior and that cancellation/exit does not auto-resume.
- **Evidence:** official configuration and compatibility docs describe exact state, APIs and constraints; current test strategy uses real public SessionManager and deterministic faux provider. Test integration verifies compaction and continuation but not live-provider savings.
- **Adaptation:** G owns Brain Context compaction/versioning. F may expose cost/working-set observations and archive recall, not run OCC against G Context or copy SoL-Pi's single ratio as production policy.

#### Action Fusion

Action Fusion fuses a file mutation and a follow-up command within a per-file queue and verifies the target hash immediately before the command. Compatibility docs explicitly note the queue does not cover external processes or unrelated extensions. This is peripheral to the requested archive scope, but its lesson is relevant: local serialization and a pre-action hash check do not establish global isolation or an atomic cross-system transaction. F's archive immutability and read consistency need explicit revision checks and publication semantics.

#### Configuration, security and tests

- All four mechanisms are opt-in and disabled by default; project config is considered only for trusted projects; project config replaces rather than merges user config.
- Configuration schema rejects unknown keys, unsupported versions and invalid value types. The documented `cacheWriteReadRatio` default is 12.5, but this is an economic heuristic used by OCC, not a universal cost model or model-price lookup.
- ObservationPack and EPR archives are local and session-derived; the docs state that archived files are not automatically deleted at session end. Temporary-session modes may use OS temporary directories and are not guaranteed to survive cleanup or support recovery.
- SoL-Pi runs with the host process's filesystem/process/network/credential permissions; it is not a sandbox. Project-local config is trusted-project-only. EPR's likely-secret detector is not complete.
- The compatibility document reports 19 test files / 140 tests for the stated Pi versions, type checking, package inspection, public API checks and offline startup. It describes test doubles over public extension APIs and real SessionManager, including Pi package integration and OCC continuation tests. Those tests establish integration behavior, not real-provider savings or AiMemoryBrainArchitecture security conformance.
- Visible issue/PR history contains important edge cases: no-session archive root failure (#39), cursor-at-EOF behavior (#123), one-line preview (#116), fork restore (#97), archive byte verification (#114), and full-output fallback constraints (#112). These show why a production design needs explicit EOF, restore, hash, preview and fail-open tests.

### 2.3 Mechanism disposition

| Mechanism | Disposition | F adaptation |
|---|---|---|
| FHA | REJECT as default active-context policy | retain only where source retention policy allows; never replay all by default |
| EoCC | ADAPT | G-owned Context compaction; preserve F archive references |
| SAC | OPEN / task-harness choice | test on suitable Agent workflows; not an F policy |
| Selective Input Reading | ADOPT | immutable archive + bounded exact recall |
| Semantic State / SSSM | OPEN research | no new authority type; preserve state owner boundaries |
| ObservationPack | ADAPT strongly | stable handle, preview, exact pages, immutable bytes, stronger governance |
| Evidence-Preserving Reducer | ADAPT optionally | deterministic quote/hash validation; original fallback |
| Online Context Compact | G-only adaptation | F supplies costs/availability; G decides Context version |
| Action Fusion | OUT OF SCOPE | only lessons about concurrency and hash-before-action |

## 3. Existing F Architecture Assessment

### 3.1 Baseline read

Read on `session-f-memory-runtime`:
- `05-memory-runtime/runtime-overview.md`
- `05-memory-runtime/retrieval-engine.md`
- `05-memory-runtime/activation-policy-engine.md`
- `05-memory-runtime/working-set-and-cache.md`
- `05-memory-runtime/runtime-scheduling.md`

Read G's `06-memory-context/context-architecture.md` on `session-g-memory-context`.

The F baseline already establishes:
- F is the bounded online read/activation execution layer, not canonical storage, compiler, Agent planner or Context Version authority.
- Retrieval uses structured/entity/full-text/vector/graph/temporal/provenance channels.
- Scope-before-Candidate is a hard invariant; no global ANN top-k followed by application post-filter.
- Candidate versions, canonical status, lifecycle, per-index/per-partition watermarks, completeness and freshness are explicit.
- Working Sets/caches are disposable and keyed by principal/scope/environment/permission epoch/Forget fence/version/index generation as appropriate.
- cache hit is reauthorized; stale entries are discarded; auth failure is fail-closed.
- D owns Forget Fence; I owns PermissionEpoch; F owns IndexWatermark; G owns ContextVersion. They are not interchangeable.
- final return/G handoff rechecks current authority; notification/cancellation is not the safety proof.
- G alone changes Context and decides ContextVersion; F's ActivationRecommendation is advisory.

### 3.2 Gap

The existing F baseline does not yet define a first-class immutable observation object and its recall protocol. Existing RetrievalResult is centered on canonical Memory candidate refs. Existing WorkingSetEntry is similarly centered on Memory ID/Version and index watermarks. Large raw tool outputs, environment snapshots, intermediate logs and external source documents cannot safely be represented as if they were Canonical Memory candidates.

Adding archive objects to the Canonical Memory Index would blur ownership and invite every log to become a vector record. Adding archive bytes to G Context would defeat G's bounded-context role and couple context membership to storage lifecycle. The missing capability is therefore an F-owned archive/recall subsystem with a typed bridge to G.

### 3.3 Compatibility

The proposal extends F's existing read-path invariants:
- same Scope-before-Candidate requirement before archive metadata candidates or payload bytes are exposed;
- same exact version/revision and per-partition completeness semantics;
- same final I/D authority checkpoint before disclosure;
- same cache key and invalidation principles;
- new archive-specific source revision/hash/retention/expiry/cursor dimensions.

It does not change the meaning of Canonical Memory, RetrievalResult for canonical Memory, ActivationRecommendation or G Context.

## 4. Observation Archive Architecture

### 4.1 Object classes and strict separation

| Class | Meaning | Owner / authority | Archive treatment |
|---|---|---|---|
| Runtime Observation | transient tool output, environment observation, intermediate execution artifact | F Runtime session, subject to I policy | archive if size/reuse/audit policy justifies; session/tenant scoped; never auto-promote |
| Canonical Memory | governed Brain memory with canonical ID/version/lifecycle | D | not an Observation Archive object; refer to it via canonical typed reference |
| Context Entry | G-owned selected reference/rendering in a Context Version | G | may reference archive locator only if G policy permits and F can reauthorize later; no ownership transfer |
| External Raw Material | document, webpage, file, imported corpus or source evidence | source/provider or governed ingestion owner | F may hold a controlled immutable capture/copy or locator, with explicit source revision and rights/retention metadata; F does not declare it canonical |

An archive capture does not establish truth, relevance, ownership, user preference or long-term memory eligibility. Any promotion to Canonical Memory must go through existing D/E governed ingestion/compilation pathways, with its own provenance and authorization.

### 4.2 Proposed logical components

1. **Archive Capture Adapter:** accepts eligible observation payloads from trusted Runtime tool adapters; records capture identity, session/task/environment scope, source producer and timestamps.
2. **Immutable Blob Store:** stores bytes/content-addressed payload or encrypted immutable object; append-only metadata versions; no in-place rewrite.
3. **Archive Manifest / Metadata Catalog:** maps ArchiveObjectId to content hash, size, media type, encoding, source revision, scope, retention/expiry, sensitivity, origin, chunk/page map, integrity state and Forget suppression state.
4. **Archive Metadata Index:** structured filters, exact/lexical terms, temporal and source/entity metadata; no automatic vector embedding.
5. **Recall Planner:** maps RecallQuery to authorized metadata search and bounded selectors (page, range, entity, time, keyword).
6. **Read Session Manager:** records exact object revision, cursor, budget, deduplication receipts and completion state.
7. **Archive Cache Adapter:** caches manifests, page/chunk bytes or derived previews under strict version/auth/fence keys.
8. **F-to-G Recall Bridge:** sends immutable CandidateReference / RecallEvidence / Completeness to G; no Context mutation API.

These are logical responsibilities; a modular-monolith implementation is a candidate and no separate microservice is required.

### 4.3 Archive identity and immutability

Candidate identity fields:
- `archive_object_id`: opaque globally unique ID, never reused.
- `archive_object_revision`: immutable archive manifest revision.
- `content_hash`: cryptographic digest (candidate SHA-256 or stronger policy-approved hash) of exact stored bytes; include algorithm identifier.
- `source_revision`: source-system revision/ETag/commit/generation when available; distinguish absent from unknown.
- `source_identity`: typed producer/source locator; not an authorization credential.
- `captured_at`, `observed_at`, optional `source_event_time`.
- `scope_refs`, `principal_ref`, Agent/instance/session/task/environment refs as required.
- `content_length`, media type, encoding, newline/normalization metadata, chunking/index format version.
- retention class, expiry, legal/policy hold if applicable, sensitivity/classification and authorization binding.
- origin lineage and optional parent/derived-object references.

Exact hash applies to stored bytes. Any normalized text, decoded view, page map, summary or excerpt must be a separately versioned derivative bound to the original content hash and transformation version. Hash is integrity evidence, not identity authorization, authenticity, or proof that source is truthful.

Immutable means no overwrite at the same object revision. A changed capture creates a new revision/object with explicit supersession/lineage relation; readers must not silently follow a mutable path to new bytes.

### 4.4 Storage and retention

Candidate storage topology:
- encrypted local/session-scoped blob storage for short-lived Runtime observations;
- optional durable encrypted object storage for observations whose policy explicitly requires persistence beyond session lifetime;
- metadata/catalog separate from blob payload;
- append-only read receipts and invalidation evidence only to the extent allowed by policy;
- explicit lifecycle sweeper with policy-defined TTL/retention; no indefinite temp-directory accumulation.

Storage is not canonical Memory. Archive durability class must be explicit: ephemeral, session-retained, policy-retained or external-locator-only. Expiration and Forget are distinct: expiry is retention lifecycle; Forget is an authoritative suppression operation that may apply across archive derivatives and references.

Authorization is checked before metadata candidate visibility, before blob open, on each page/range, before cache return and before G handoff. Metadata fields themselves may be sensitive; do not leak object existence/counts.

### 4.5 Forget suppression

Archive object Forget is not self-authorized by F. The policy owner (I) and canonical/lineage authority (D where relevant) define the target and applicable fence. F consumes the target/fence and:
- marks matching archive object and descendants/derivatives unreadable immediately;
- revokes ReadCursor / RecallSession capabilities and prevents cursor advancement;
- cancels reads and cache fills, but does not rely on cancellation alone;
- blocks stale cache hits before byte access and before serialization;
- invalidates page, preview, reducer-summary and query caches;
- records per-object/per-partition suppression/invalidation evidence for I;
- prevents offline Runtime from restoring the object on reconnect;
- prevents rebuild/replay from resurrecting a forgotten object.

A F-local suppression receipt does not mean physical erasure or global Forget completion. I decides completion across the closed-world inventory; storage/provider backups and external sources require their own governed handling.

## 5. Selective Input Reading

### 5.1 Query-to-selector planning

Recall planner accepts an authenticated RecallQuery with trusted Scope and policy context plus optional filters:
- object/source identity and exact source revision;
- entity IDs (not merely ambiguous display strings);
- absolute or bounded time interval;
- exact terms/phrases and lexical query;
- page number / page range;
- byte/character range with explicit coordinate system;
- structured record selectors where a source adapter supports them;
- maximum bytes/pages/results and deadline.

Planning sequence:
1. authenticate and resolve Scope/Permission with I;
2. obtain current D Forget Fence / relevant archive suppression state;
3. compile trusted scope predicate before metadata candidate generation;
4. select structured, temporal, lexical and source-specific index adapters;
5. authorize each candidate before exposing locator metadata;
6. bind exact ArchiveObjectRevision + content hash + source revision;
7. calculate read plan and reserve budgets before opening payload;
8. read exact requested page/range, verify stored-byte hash or chunk hash and source binding;
9. emit ReadReceipt with returned range and remaining/unread coverage;
10. recheck permission/fence before returning bytes to caller/G.

### 5.2 Range and page semantics

- All byte ranges are half-open `[start,end)` over exact stored bytes; text ranges must name their coordinate system (UTF-8 byte, Unicode scalar/code point, UTF-16 code unit, or line/column). Do not mix coordinates.
- A page selector resolves against an immutable page map generated from one exact content hash and segmentation version. Page numbers cannot be reused across a changed content hash.
- Entity/time selectors are metadata filters returning bounded source spans, not semantic proof that the whole object was searched.
- Keyword lookup uses an inverted index or bounded scan. ANN is not needed for exact pagination.
- Return source hash, object revision, exact range, page ID, encoding and integrity result with every excerpt.
- For binary/structured data, use adapter-defined records/ranges; never pretend byte offsets are text lines.

### 5.3 Prevent duplicate and infinite reads

Use an explicit RecallSession per caller/workflow with:
- immutable session scope + authorization binding;
- exact object revision/hash;
- read budget counters (bytes, pages, calls, tokens, wall time);
- issued cursor generation and consumed receipt set;
- visited range/page set or interval coverage map;
- bounded retry count;
- max page count and max continuation depth;
- expiry and cancellation state.

A page receipt is idempotent by (RecallSessionId, ArchiveObjectId, revision, hash, selector, page/range). Repeating a read may return the same verified page without double-counting budget only if policy permits and the exact receipt remains valid; otherwise charge each read. The policy must be explicit. No opaque cursor alone can authorize payload access.

A cursor is monotonic within a single immutable object revision and selector plan; it cannot jump backwards, change object, or change hash. Arbitrary range reads may be supported as separately budgeted selectors but do not mutate the sequential page cursor. EOF is explicit; final page has no next cursor. Empty page is not automatically EOF unless the archive adapter confirms it.

### 5.4 Read budget and incompleteness

Budget dimensions:
- max bytes/pages per object and total;
- max objects and metadata candidates;
- max read calls and concurrent reads;
- max context-injection tokens (G decides final Context budget);
- wall-clock/deadline and CPU/decompression budget;
- optional model-assisted summarization budget (off by default).

Budget exhaustion returns typed partial status and precise omissions. The Agent/G must distinguish:
- complete for exact requested selector;
- partial due to budget/deadline/channel failure;
- unavailable due to source/access/integrity issue;
- stale due to revision mismatch;
- suppressed due to Forget/revocation;
- empty_complete only when the requested bounded selector was successfully searched and contained no result.

A top-k or one page never proves the entire archive is complete.

### 5.5 Source revision changes

If the external source changes:
- old archived bytes remain bound to old hash/revision if retention permits;
- a new capture is a new immutable revision;
- cursor/RecallSession for old revision can continue only if old revision remains authorized and retained;
- no automatic cursor rebinding to the new revision;
- return SourceRevisionMismatch / Stale when caller requested “latest” and the latest revision differs;
- caller may explicitly start a new RecallSession against the new revision.

## 6. Recall Session and Cursor Model

### 6.1 Candidate conceptual records

- **ArchiveLocator:** opaque object ID, revision, content hash, source revision, scope reference and authorized locator capabilities. Locator is not bearer authority.
- **RecallSession:** session ID, authenticated principal, scope set, purpose, policy/permission epoch, D Forget Fence reference, object revision/hash, selector plan, budget, expiry, state and correlation ID.
- **ReadCursor:** cursor ID/generation, RecallSession, exact object revision/hash, selector plan hash, next offset/page, consumed coverage, last receipt and expiry.
- **ReadReceipt:** receipt ID, selector, exact returned range/pages, hash verification, source revision, bytes returned, remaining coverage, completeness/failure reason, permission/fence checkpoint and timestamp.
- **SourceRevisionBinding:** typed source identity + immutable source revision + content hash + capture metadata.
- **CompletenessMetadata:** requested scope/selector, executed adapters, coverage, omissions, budget exhaustion, stale/freshness and integrity.
- **ReadBudget:** reserved/consumed dimensions, limit and accounting policy.

These are proposed Runtime records, not Canonical Memory or ContextEntry.

### 6.2 Cursor integrity and replay

Cursor token may be opaque server-side ID or authenticated encrypted token; it must bind the fields above and be integrity-protected. Do not embed raw content or long-lived bearer permission. Every continuation revalidates current I permission and D Forget Fence. Cursor expiry, revocation, Forget, source revision mismatch or authorization failure invalidates it. Cursor state is never accepted as proof of prior authorization.

ReadReceipt is append-only within retention policy and is evidence of what F returned, not proof the model understood or used it. A G Context Entry can refer to a receipt/range, but G must resolve authorization again when materializing it.

### 6.3 EOF and completeness

EOF is a terminal cursor state. A terminal receipt records exact end offset and no continuation cursor. Client must not infer EOF from missing content, empty output, transport truncation or an absent field unless protocol explicitly says so. The SoL-Pi visible PR about dropping next_offset from final header is a useful interoperability lesson: terminal paging semantics must be unambiguous.

## 7. Runtime Working Set and Cache

### 7.1 Admission

An ObservationReference enters the F Working Set only after:
1. authenticated session and Scope resolution;
2. candidate-level authorization before metadata exposure;
3. exact archive revision/hash verification;
4. current D/I fence check;
5. byte/entry quota reservation;
6. sensitivity-aware admission policy.

Working Set stores references/metadata by default. It may store bounded preview/page bytes only when authorization, classification and memory quota allow. It is not G Context and must not be auto-projected as context.

### 7.2 Cache layers

| Cache | Contents | Default |
|---|---|---|
| Locator/manifest cache | identity, revision, hash, page map, retention metadata | preferred |
| Page/chunk cache | exact immutable bytes for a specific range | opt-in, small, encrypted where persisted |
| Preview cache | bounded deterministic preview bound to source hash + renderer version | preferred if policy allows |
| Recall-result cache | selector result + exact receipt/completeness | only if full auth/freshness key matches |
| Summary cache | derived summary with model/prompt/version and evidence refs | disabled until validated |
| ANN embedding cache | embeddings for explicitly eligible chunks only | not default |

Cache keys include Principal/security domain, canonical ScopeRefs, Agent/instance/session/task/environment where applicable, I PermissionEpoch domain/issuer, D ForgetFence reference/generation, F-local invalidation generation, object ID/revision/content hash, selector/query fingerprint, policy/classification, page-map/index generation and transformation version.

Every hit rechecks I authorization and D fence before bytes are returned. A stale entry is dropped/quarantined, not treated as a miss when D/I authority is unavailable. TTL is only a capacity optimization.

### 7.3 Content version, permission and Forget

- New archive revision/hash invalidates old “latest” lookup results; exact historical revision may remain usable only if policy allows.
- Permission epoch changes invalidate affected cache namespaces immediately, regardless of physical eviction delay.
- Forget fence advances: suppress before payload read; invalidate references, bytes, previews, summaries, embeddings, query results and in-flight fills; old cursor becomes unusable.
- Offline process must authenticate, fetch current PermissionEpoch and Forget Fence, reconcile cursor/session state and discard stale working-set material before restoring access.
- No restore-first-clean-later.
- A cached summary is content-derived data and inherits source sensitivity/authorization/Forget lineage; it is not exempt because it is short or model-generated.

### 7.4 12–16GB VRAM constraint

12–16GB is a reference model deployment VRAM budget, not a Runtime RAM quota. F must separately measure CPU RAM, page cache, disk IO, storage capacity, GPU VRAM and model inference queue. Archive payloads and ordinary caches should be disk/CPU-memory based; do not use scarce VRAM for raw observation caching. Optional embedding/reranking may share GPU with the local model and must be admitted as best-effort, isolated work. A GPU outage must not disable exact range/page recall.

## 8. Retrieval / Archive Index Boundary

### 8.1 Separate index responsibilities

An **Observation Archive Metadata Index** is recommended, logically separate from the Canonical Memory Index.

- Structured index: object ID/revision, source/producer, scope, session/task/environment, timestamps, media type, size, classification, retention/expiry, integrity state, source revision and lineage.
- Full-text/inverted index: exact words, rare terms, phrases and line-oriented diagnostics, with Scope-before-Candidate inside backend.
- Temporal index: observed/source event intervals and bounded time selection.
- Optional entity metadata: explicitly extracted entity IDs with source spans and extraction provenance; not canonical Entity identity unless D confirms it.
- ANN index: only selected, policy-approved, semantically useful text chunks where query paraphrase materially improves recall; no default embedding of every stdout/stderr/log/trace.

### 8.2 What needs ANN?

Potential ANN candidates: human-authored long-form observation notes; selected natural-language summaries with evidence-linked source spans; explicitly curated external documents. Usually no ANN needed for: raw JSON/tool payloads, compiler/build logs, stack traces, metrics, line-numbered execution logs, binary blobs, deterministic table records or exact ID/time/range reads.

All embedding records are derived indexes. They must bind source object revision/hash, chunk range, embedding model/version, index generation and authorization dimensions. Forget/version changes suppress derived vectors too. Vector similarity does not prove completeness or evidence support.

### 8.3 Prevent unbounded archive growth

Admission and retention must be policy-driven:
- capture only eligible observation classes or size/reuse thresholds established by measurement;
- classify before persistent archive;
- define per-session/per-principal/global byte and object quotas;
- explicit retention class/expiry and cleanup workflow;
- deduplicate identical bytes only within a safe authorization/storage domain; never use global content-address existence as a side channel;
- cap metadata, page count, chunk count, index postings and read amplification;
- backpressure and reject/defer low-priority archive writes under storage pressure;
- maintain inventory and orphan-blob reconciliation;
- do not keep temp-session archives forever by accident;
- no archive object automatically becomes Canonical Memory.

## 9. Cost and Resource Model

### 9.1 Cost components

For a candidate source object of size (S), page size (P), query read volume (R), number of reads (n), context injection (T), and cache hit ratio (h), compare:

- Full read: storage read (S) + decode/parse + inject all (S_t) tokens.
- Selective read: metadata query + index cost + page/range IO for (R) bytes + repeated page overhead + inject only selected (R_t) tokens.
- Summary: one-time summarization compute/write + summary storage + later summary read; still needs source recall for exact questions.
- Cache: hit validation + memory/disk lookup versus uncached page retrieval; cache write cost and invalidation complexity must be included.
- Missed evidence: expected recovery cost (re-query, re-run tool, re-open source, wrong decision or task failure).
- Authorization/Forget checks: fixed per request/page cost, not optional overhead to be optimized away.

### 9.2 Candidate break-even model

Let:
- (C_f(S)): cost of full read + full context injection;
- (C_m): metadata search cost;
- (C_p(R,P)): page/range IO and decode cost;
- (C_i(R_t)): selected-context injection cost;
- (C_s): one-time summary generation/write cost;
- (C_c): cache write/storage/invalidation amortized cost;
- (C_v): per-read authorization, fence, hash and version validation cost;
- (C_r): expected cost of omitted-evidence recovery, weighted by probability of omission and task impact.

Then selective recall is beneficial only when:

[
C_m + C_p(R,P) + C_i(R_t) + C_v + C_c + C_r < C_f(S)
]

For repeated reads, compare amortized archive/write cost plus cache validation against repeated full reads. The optimal page size and cache admission threshold depend on observed read locality, object size distribution, latency and failure/recovery costs. They must be swept experimentally, not chosen by intuition.

### 9.3 Experimental parameters

Sweep, rather than hardcode:
- object sizes and payload types;
- page sizes and overlap/context windows;
- first-page preview length;
- read count and reuse distance;
- range-vs-page query mix;
- cold/warm cache and cache write/read ratio;
- metadata/index selectivity and candidate fan-out;
- authorization and fence recheck latency;
- local storage throughput and CPU decompression;
- summarization model latency/token cost and exact-quote validation failure;
- omitted-evidence rate and task recovery cost.

Report P50/P95/P99 latency, bytes read/written, tokens injected, model calls, cache hit/miss, duplicate pages, archive storage growth, CPU/RAM/disk/VRAM, recall accuracy, exact evidence coverage and false-complete rate.

### 9.4 Resource accounting

- CPU: capture hashing, parsing, indexing, page map, decompression, exact quote verification, selector execution.
- RAM: bounded manifest/candidate buffers, cursor/receipt state, small page cache.
- Disk/object store: immutable raw blobs, manifests, indexes, receipts and derived previews.
- GPU/VRAM: optional embeddings/rerank/summarizer only; no raw archive residency assumption.
- Network: only external source capture/retrieval where explicitly authorized; never implicit remote reducer calls.

## 10. Forget and Authorization

### 10.1 Scope-before-Candidate

Every archive metadata query must compile trusted scope predicate before candidate materialization. Every object and every child source/attachment/page index is reauthorized before dereference. Do not globally search then filter application-side. Candidate counts, existence, timing, cursor errors and cache metrics must not reveal unauthorized objects.

### 10.2 Epoch/fence binding

RecallSession and protected caches bind:
- authenticated Principal and security domain;
- canonical ScopeRefs;
- applicable Agent/instance/session/task/environment;
- I PermissionEpoch (with domain/issuer);
- D ForgetFence reference/generation where object/lineage is governed by D;
- F-local invalidation generation;
- exact archive object revision/hash/source revision;
- selector and metadata/index generation.

The key/token is not an authorization grant. Each page read performs current authorization/fence checks. F does not mint D's fence or I's PermissionEpoch.

### 10.3 Forget during read

Required sequence:
1. Forget notification/fence advancement triggers immediate suppression and cancellation of matching in-flight reads/fills.
2. Reader must recheck authoritative current fence/permission before every subsequent page and before response serialization.
3. If Forget linearizes before the final disclosure checkpoint, no affected bytes may be returned; discard buffered result and invalidate cursor/session.
4. If a response was already disclosed before Forget linearized, record the prior disclosure receipt; no system can retroactively erase tokens already observed by a model/provider. Subsequent reads and future context delivery must be blocked.
5. On uncertainty, fail closed and report suppressed/unknown, not empty_complete.

### 10.4 Offline reconnect

Offline Runtime must not continue reading from stale local cache based on an old permission/fence snapshot. Reconnect order:
authenticate → current I PermissionEpoch → current D ForgetFence/target state → reconcile archive inventory and cursor checkpoints → invalidate/quarantine stale Working Set/cache → resume only exact authorized revisions. G Context target/delivery reconciliation is performed by G/H before any stale Context materialization is reused. No local archive reference bypasses this order.

### 10.5 External sources and retention

External raw material may have independent license, source access, deletion and retention rules. F cannot assume it may retain indefinitely or make a source copy immutable by policy fiat. Capture policy must record provenance and retention authority; source changes create new revisions. A source that cannot be retained may use an external locator and bounded authorized fetch, with source revision/integrity uncertainty reported.

## 11. G/F Cross-Module Contract

### 11.1 F provides to G

- RetrievalResult and ObservationRecallResult;
- authorized CandidateReference / ArchiveLocator (opaque, non-bearer);
- exact object revision, content hash, source revision and source range;
- ReadReceipt and evidence/integrity metadata;
- per-channel/per-object completeness and freshness;
- explicit omissions, budget exhaustion, stale source, integrity failure and authorization denial without existence leakage;
- bounded excerpt/preview plus provenance and classification;
- optional estimated byte/token cost and recommended read plan.

### 11.2 G decides and owns

- whether candidate is relevant and admissible to Brain-owned Context;
- Context Entry creation/removal/defer and tier;
- Context ordering, coverage and budget allocation;
- whether an archive reference or materialized excerpt is appropriate for a Context;
- compaction and semantic rendering;
- Context ChangeSet, Context Version, Snapshot/Delta and Applied workflow.

### 11.3 Prohibited cross-boundary behavior

- F MUST NOT create/update/delete G Context Entries or Context Versions.
- F MUST NOT decide Semantic State authority or Canonical Memory truth.
- F MUST NOT automatically promote observations to Canonical Memory.
- F MUST NOT declare D/I Forget complete.
- G MUST NOT treat F locator as a permission grant; it revalidates current authority on dereference/materialization.
- G MUST NOT treat an archive receipt as proof of semantic correctness, canonical acceptance or Applied.
- Neither side may use an archive to bypass I scope/permission or D Forget Fence.

### 11.4 Proposed handshake

G sends a read-only RecallIntent (purpose, required scope, exact selectors, desired completeness, byte/token budget hint, deadline, current ContextVersion only as correlation/hint). F authorizes and returns a RecallResult with exact references/excerpts/receipts, completeness/freshness and warnings. G validates source/lifecycle/authority and independently decides Context mutation. G's ContextVersion is not input to F as a mutation token and is never generated by F.

## 12. Failure and Recovery Scenarios

| Failure | Required behavior | Completeness/result |
|---|---|---|
| Blob missing/corrupt/hash mismatch | quarantine object; do not emit unverified bytes | unavailable/integrity_failed |
| Source revision changed | do not silently rebind cursor; require new session | stale/source_revision_mismatch |
| Page cursor replay/out-of-order | reject or idempotently replay exact receipt under policy | explicit cursor_replay / duplicate |
| EOF continuation attempt | terminal cursor; no next cursor | complete for requested selector |
| Read budget exhausted | stop before additional read; report unserved ranges | partial/budget_exhausted |
| I authorization unavailable | fail closed; do not expose metadata/payload/cache | unavailable/authorization_unknown |
| D Forget Fence unavailable | suppress protected read; quarantine cursor/cache | suppressed_or_unknown |
| Cache invalidation event lost | recheck authoritative epochs/fence on read; quarantine if checkpoint gap | stale/quarantined |
| Offline reconnect after Forget | refresh I/D before restore; discard stale local state | blocked until reconciliation |
| Summary quote/source mismatch | reject summary; return original or exact archive page if authorized | reducer_rejected/fallback |
| Storage pressure | admission control; reject/defer capture; do not silently drop acknowledged data | archive_write_deferred/rejected |
| Partial metadata index | bounded canonical/archive catalog fallback only if authorized; otherwise partial | partial/index_lag |

## 13. Benchmark and Experimental Plan

### 13.1 Normal tests (minimum 5)

1. **Large tool output, repeated context requests:** archive once, project compact handle/preview, ensure original bytes remain exact, repeated requests do not replay full payload, explicit recall returns correct page.
2. **Multi-page selective recall:** query pages/ranges in sequence; validate exact offsets/hash, receipts, cursor progression and terminal EOF.
3. **Mixed selector retrieval:** source + time interval + entity ID + keyword; ensure structured/lexical/temporal planning and source spans are consistent.
4. **Warm/cold cache comparison:** identical authorized read; verify identical content/receipt semantics and measure latency/bytes.
5. **Source revision rollover:** capture v1 then v2; v1 cursor remains bound to v1 or is denied by retention policy; latest query resolves v2; no silent cursor rebind.
6. **Evidence-preserving summary:** reducer proposes exact quotes; accept only exact source-verified quotes; original archive remains accessible.
7. **G handoff boundary:** F returns candidate/receipt/completeness; G can accept/defer/reject without F changing ContextVersion.

### 13.2 Negative tests (minimum 5)

1. **Cross-principal/scope locator reuse:** same ArchiveLocator/cursor under another principal/scope; no metadata or bytes leak.
2. **Forget before first page:** old locator and cursor fail even if bytes/cache exist.
3. **Forget during multi-page read:** first page may be disclosed before fence; all subsequent pages and buffered not-yet-disclosed response bytes suppressed after fence.
4. **Permission revoked after cache fill:** cache hit denied; stale summary/page not served.
5. **Corrupt/tampered blob or ledger:** hash mismatch; no partial unverified content; object quarantined.
6. **Cursor tamper/replay/EOF misuse:** altered selector/hash/offset or terminal cursor rejected; no infinite read.
7. **Prompt injection in archived output:** content remains untrusted data; does not modify tool policy or scope.
8. **Retention expiry/external rights revoked:** archive access denied and cleanup workflow reported; no indefinite local retention.
9. **ANN leakage/post-filter trap:** unauthorized objects never enter ANN/lexical candidate buffers or observable counts.
10. **Summary stale after source update/Forget:** derived summary cache suppressed and cannot be used as substitute source.

### 13.3 Concurrency and recovery tests (minimum 3)

1. **Forget vs read race:** pause after authorization/first page; advance D fence and I epoch; resume reader; assert final checkpoint blocks disclosure and cursor invalidated.
2. **Concurrent cursor consumers:** two clients attempt same cursor/page; deterministic idempotency or one-writer lease; no skipped/duplicated ranges or budget double-spend.
3. **Crash/restart during archive write:** crash after blob write before manifest commit and after manifest stage before publication; orphan cleanup/recovery never exposes incomplete object.
4. **Lost invalidation event + offline restart:** local checkpoint behind; reconnect anti-entropy detects gap and quarantines before cache/Working Set restore.
5. **Source revision race:** source changes while read session opens; read binds one exact revision/hash or fails; never mixes bytes from two revisions.

### 13.4 Experimental acceptance gates

- zero unauthorized candidate/payload leakage in negative tests;
- zero false-complete result under truncation, timeout, index gap or budget exhaustion;
- exact byte/hash verification for every returned range;
- no cursor can cross object revision/hash or survive applicable Forget/revocation;
- measured reduction in injected tokens and repeated bytes without unacceptable task accuracy/recovery penalty;
- measured storage growth/retention compliance under realistic observation volume;
- page size/cache/ANN decisions selected by paired experiments with confidence intervals and per-task outcome analysis.

## 14. Adopt / Adapt / Reject / Open Questions

### Adopt
- immutable raw observation preservation;
- stable locator/handle and bounded exact page/range recall;
- source hash/revision binding;
- explicit completeness, omission and EOF semantics;
- evidence-to-source traceability;
- metadata catalog distinct from Canonical Memory Index;
- fail-closed auth/Forget checks and stale cache suppression.

### Adapt
- ObservationPack's context projection: F exposes compact refs; G decides what enters Context.
- EPR's quote validation: use deterministic checks, preserve original on failure, never elevate generated summary to authority.
- online compaction economics: expose measured cost telemetry to G; G owns Context compaction.
- session-local archive: support governed retention classes and controlled durable storage, not temp-directory assumptions.

### Reject
- SoL-Pi's local host process permissions as a security model;
- session directory as sufficient multi-tenant isolation;
- automatic persistent archive retention without lifecycle cleanup;
- fixed cacheWriteReadRatio 12.5 as a production constant;
- automatic vectorization of all large observations;
- raw observations becoming Canonical Memory or Context by default;
- cancellation alone as Forget correctness;
- treating hash as authorization/authenticity;
- treating summary/receipt as proof of truth or semantic completeness.

### Open questions
1. Which observation producers/classes are eligible for durable archive capture, and who approves the retention matrix (I/D)?
2. Does F archive all eligible bytes or store external locators for selected source types?
3. Which object classes are subject to D's canonical lineage Forget Fence versus I-owned archive-only targets? Needs D/I target inventory semantics.
4. What is the authoritative archive storage boundary and encryption/key ownership? Needs I/Storage approval.
5. What source revision abstraction is common across tool outputs, files, external documents and environment snapshots?
6. Should page maps use line-based, byte-based or format-specific record boundaries for each adapter?
7. What is the minimum G recall contract and what evidence does G require before Context inclusion?
8. What is the consistency/linearization point for a page read concurrent with Forget?
9. What quotas and retention periods are justified by workload measurements and policy?
10. Which observations, if any, merit semantic embedding after filtering/redaction and explicit opt-in?

## 15. Final Recommendations

1. Approve an F-owned Observation Archive capability as a **non-canonical, governed Runtime evidence substrate**.
2. Keep its metadata index logically separate from Canonical Memory Index; use structured/full-text/temporal indexes by default and ANN only for measured semantic retrieval needs.
3. Implement immutable content + source revision/hash binding before exposing recall cursors.
4. Make RecallSession, ReadCursor, ReadReceipt, ReadBudget and CompletenessMetadata explicit candidate concepts; cursors are locators/state, never bearer authorization.
5. Enforce Scope-before-Candidate for metadata and payload; revalidate I permission and D Forget Fence before every page/cache return/final disclosure.
6. Bind derived previews/summaries/embeddings to source hash, transformation version and lineage; all inherit source access/Forget constraints.
7. Let G decide Context inclusion, compression and ContextVersion. F returns references, bounded excerpts, evidence, freshness and incompleteness only.
8. Keep default Recall deterministic and no-LLM. Optional reducer/summarizer is isolated, opt-in and fail-open to the original archive representation.
9. Benchmark page size, cache policy, retention, ANN eligibility and cost break-even on real workloads. Do not import SoL-Pi's 12.5 ratio or any paper threshold as project defaults.
10. Obtain D/E/G/H/I review before freezing schemas or implementing. No changes to current F baseline are made by this report.

**Final answer:** We need an independent Observation Archive capability in F because transient large observations require immutable storage, exact selective reads, cursors, budgets, integrity, retention and cache/Forget suppression—responsibilities not owned by Canonical Memory or G Context. It belongs to **F as the Runtime archive/recall mechanism**, with **G as the Context selection/version authority**, connected by an explicit read-only evidence/reference contract. It is neither F-only end-to-end nor G-owned storage; it is F/G collaboration with D/E/H/I authority boundaries preserved.
