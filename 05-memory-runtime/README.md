---
# provenance: RECONSTRUCTED_FROM_MIRROR
document_metadata:
  domain: "memory-runtime"
  role: "guide"
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: git
        value: null
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Applicable-To-Current-Version
      evidence_reference:
        - "AID-2026-083"
        - "provenance: RECONSTRUCTED_FROM_MIRROR"
        - "EN source mirror docs/en/05-memory-runtime/memory-runtime-guide.md blob a45b868efe1367fb9934c17191109d8d87f48fab"
        - "ZH-CN source mirror docs/zh-CN/05-memory-runtime/memory-runtime-guide.md blob 0e0df43de9c55f8e41d6ed596d50471798fb23cc"
        - "authoritative root source blob: NOT_FOUND"
        - "reconstructed_date: 2026-11-26"
        - "executed_by: user-authorized operator (delegated by account owner)"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Root README reconstructed from the existing EN guide mirror. No authoritative root source blob was found in F branch. ZH-CN guide counterpart was compared; no material semantic divergence identified. Owner acceptance pending."
    usage_status: Active
    modification_status: Modified
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: "Candidate"
    canonical_scope: "Mirror-derived reconstruction of the Memory Runtime root reading guide; informative candidate only"
    canonical_scope_id: "memory-runtime/runtime-architecture-guide"
    canonical_scope_keywords:
      - "runtime"
      - "retrieval"
      - "working-set"
      - "forget-suppression"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: "docs/en/05-memory-runtime/README.md"
    zh-CN: "docs/zh-CN/05-memory-runtime/README.md"
---

> **Reconstruction notice:** This root document was reconstructed on 2026-11-26 from the existing English mirror `docs/en/05-memory-runtime/memory-runtime-guide.md` (original mirror blob `a45b868efe1367fb9934c17191109d8d87f48fab`). No authoritative source blob for this root path was found in the corresponding Owner branch `session-f-memory-runtime` at `1908ce4d233b20f7cafd00cb679affd01bd15174`; the mirror blob is not an authoritative source blob. The ZH-CN counterpart `docs/zh-CN/05-memory-runtime/memory-runtime-guide.md` (blob `0e0df43de9c55f8e41d6ed596d50471798fb23cc`) was reviewed for semantic alignment. Only the counterpart link was redirected to the exact-name ZH-CN README mirror. Status: **Draft / Candidate / Informative**. Executed by `user-authorized operator (delegated by account owner)`. This reconstruction does not establish Owner acceptance, approval, or Normative authority.

# Memory Runtime — Architecture Guide

- Document ID: DOC-RUNTIME-001
- Version: 1.0
- Owner: F — Memory Runtime
- Source: F owner branch, Runtime overview and consumer contracts
- Chinese counterpart: [记忆运行时架构指南](../docs/zh-CN/05-memory-runtime/README.md)
- Status: Explanatory guide; topology is CANDIDATE, numeric budgets TO_VALIDATE, consumer schemas OPEN

## 1. Purpose

Memory Runtime is the Brain's bounded online read and activation layer. It receives Recall requests, resolves authorization and Scope, searches canonical and derived representations, returns evidence-bearing candidates, recommends what may be activated, and maintains disposable runtime Working Sets and caches.

It is not an Agent Runtime, planner, tool executor, Canonical Store, Compiler, or Context Version authority. Default Recall should be deterministic and must not synchronously depend on a large LLM.

## 2. Authority boundaries

F owns:
- Runtime Session lifecycle and request-local execution state.
- Query interpretation and retrieval routing.
- Scope-filtered candidate retrieval, fusion, deduplication, and ranking.
- Completeness/freshness semantics and typed index-watermark consumption.
- Activation recommendations and bounded Working Sets/caches.
- Scheduling, admission, cancellation, and read-path freshness checks.

F does not own canonical Memory/Claim/Entity/Relation identity, versions, lifecycle, or authoritative Forget state (D); compilation and canonical/index publication (E); ContextEntry mutation or ContextVersion (G); global permission/retention/audit policy (I); Agent planning or external action authorization.

## 3. Read path

~~~text
Recall Request + authenticated Principal / Scope
        ↓
Authorization and current policy context
        ↓
Query interpretation and retrieval routing
        ↓
Scope-first filtering
        ↓
Structured / lexical / semantic / temporal / relational candidates
        ↓
Fusion, deduplication, freshness and completeness evaluation
        ↓
Evidence-bearing RetrievalResult
        ↓
ActivationRecommendation to G / caller
~~~

Scope and authorization must be applied before ranking, aggregation, or result counts that could leak protected information. Results reference exact immutable canonical Memory versions. Retrieval does not create Memory and does not advance ContextVersion.

## 4. RetrievalResult vs ActivationRecommendation

RetrievalResult reports what was found, under which query and consistency conditions, with candidate references, evidence summaries, match channels, freshness/completeness indicators, and uncertainty warnings.

ActivationRecommendation suggests include, defer, or exclude with reason codes, urgency/expiry hints, and budget estimates. It is not a Context edit. G owns Context membership, ordering, versioning, and delivery intent.

Telemetry is an untrusted relevance signal. It does not authorize access and does not prove that an asserted task outcome occurred.

## 5. Working Sets and caches

Working Sets and caches are bounded, disposable projections—not canonical memory. They must be isolated by authenticated identity, Scope, policy/permission epoch, and relevant Forget generation. They need explicit size/TTL/admission/eviction limits and observability.

A cache hit must not bypass current authorization or Forget suppression. Invalidation and generation checks must prevent stale cache fills, in-flight reads, or rebuilds from reintroducing forgotten or revoked content.

## 6. Freshness, cursors, and watermarks

F consumes D's CanonicalCommitCursor and the per-partition IndexWatermark contract. Cursor namespaces must remain typed and must not be collapsed into one generic integer. A watermark proves only the contiguous canonical commit prefix accounted for by that index partition; it does not prove Forget completion or physical deletion.

Runtime results should expose freshness and completeness rather than silently presenting stale or partial results as complete.

## 7. Forget suppression and anti-resurrection

F must:
- Cancel or safely finalize in-flight retrieval under the current Forget generation.
- Suppress affected candidates before they can be returned or activated.
- Invalidate Working Sets and caches using generation-aware checks.
- Prevent delayed cache fills from restoring stale content.
- Rebuild indexes only from canonical data filtered through current Forget fences and policy.
- Track per-index watermarks and expose lag/failure.
- Re-check current authorization at the read boundary.

The target is zero unauthorized or forgotten-content disclosure. The exact guarantee must be proven by race, crash, rebuild, and cache-invalidation tests—not inferred from a successful unit test.

## 8. Failure and degradation

| Condition | Expected behavior |
|---|---|
| Vector index unavailable | Use permitted alternate channels or return partial/unavailable status |
| LLM unavailable | Default Recall continues without large-model inference |
| Index lag | Report freshness/completeness; do not claim fully current results |
| Permission service unavailable | Fail closed for protected reads |
| Forget generation changes mid-read | Revalidate/suppress before returning results |
| Cache invalidation delayed | Generation checks prevent stale content from being served |
| Worker or query timeout | Cancel bounded work and return explicit timeout/partial status |

## 9. Performance and resource controls

F must bound query concurrency, fan-out, candidate count, evidence expansion, Working Set size, cache memory, index access, and cancellation latency. Numeric limits remain TO_VALIDATE until measured on declared hardware and representative corpora. Track p50/p95/p99 latency, recall/quality, index lag, cache hit ratio, memory use, and cancellation/revocation propagation.

## 10. Interfaces and non-guarantees

Inputs include authenticated Principal and resolved Scope, Recall query/filters/purpose, task/session/environment references, evidence/result budgets, deadline/cancellation, untrusted telemetry signals, D canonical metadata, E commit/publication events, index watermarks, and current policy configuration.

Outputs include RetrievalResult, CandidateMemory references with exact version IDs, evidence/provenance summaries, completeness/freshness vectors, warnings, and ActivationRecommendation.

F does not guarantee truth, authorization for external actions, Context application, model comprehension, or global Forget completion.

## 11. Validation still required

- Scope-first retrieval and zero cross-scope leakage.
- Cursor/watermark gap, lag, and recovery behavior.
- Forget races against in-flight reads, cache fills, and index rebuilds.
- Permission revocation and policy epoch changes.
- Bounded memory, fan-out, concurrency, and cancellation.
- Representative retrieval quality and p95/p99 measurements.

See the [F owner branch](https://github.com/oahcom/AiMemoryBrainArchitecture/tree/session-f-memory-runtime/05-memory-runtime) for detailed Runtime contracts.
