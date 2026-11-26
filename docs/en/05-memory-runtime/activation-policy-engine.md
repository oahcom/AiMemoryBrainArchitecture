---
document_metadata:
  domain: memory-runtime
  role: design-specification
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
        - "AID-2026-082"
        - "source branch: session-f-memory-runtime"
        - "source commit: 1908ce4d233b20f7cafd00cb679affd01bd15174"
        - "original source blob: b7f5d85468f5262e472769a1991b812ac4a64f5b"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Exact source Blob pinned; EN mirror body retained; semantic review pending."
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
    canonical_status: Non-Canonical
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords:
      - bilingual-mirror
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "05-memory-runtime/activation-policy-engine.md"
    en: null
    zh-CN: "docs/zh-CN/05-memory-runtime/activation-policy-engine.md"
---

# Memory Activation Policy Engine

**Owner:** Session F — MR-02  
**Status:** DECIDED boundary semantics; CANDIDATE policy model; TO_VALIDATE weights/thresholds.

## 1. Purpose
Evaluate whether an authorized retrieved Memory candidate is useful and safe to recommend for a task/context, and whether it should be proposed now, deferred, or excluded. This is decision support for G, not a context editor or Agent planner.

## 2. Scope
Includes eligibility, relevance/utility assessment, risk-aware recommendations, rationale, budget estimate, expiry/refresh hints, and preservation of conflict/evidence. Excludes truth adjudication, canonical lifecycle changes, Context Version ownership, final prompt assembly, Agent planning and tool authorization.

## 3. Responsibilities / Non-Responsibilities
Activation separates:
1. **Existence:** canonical Memory/Version exists.
2. **Relevance:** related to current task, entities, environment or time.
3. **Context suitability:** safe/useful/valid to propose for this Context and budget.
4. **Urgency:** propose now, defer, or require explicit Recall.

A memory can exist but be irrelevant; relevant but invalid; valid but unsafe to inject; suitable but non-urgent. None changes canonical truth.

## 4. Inputs / Outputs
Inputs: authorized CandidateMemory; task/environment/session signals; explicit Recall purpose; read-only Context summary/version hint from G; budget hint; policy/config version; permission and Forget epochs.

Output ActivationRecommendation: candidate/version refs; decision (CANDIDATE: recommend_now, recommend_deferred, exclude, require_explicit_recall); reason codes and per-factor evidence; urgency/expiry/refresh hints; estimated token/byte cost; unresolved conflict/evidence warnings; policy version and freshness timestamp. G may accept, reject, transform, compact or defer. Recommendation is not ContextEntry or Context Version.

## 5. Data Model
ActivationFeatures: semantic_relevance; entity_match_strength; temporal_relevance/validity; decision_impact/task criticality; risk/sensitivity; context_coverage_gap; lifecycle eligibility; epistemic status; method-qualified confidence; source trust; evidence support/refute/qualify balance; provenance completeness; injection cost; freshness/index lag; duplicate/context-present state.

ActivationDecision: policy_id/version, candidate ref, outcome, reason list, feature snapshot, uncertainty, evaluated_at, expires_at, authorization/Forget epochs.

## 6. Routing / Decision Flow
    Authorized candidates
      -> canonical lifecycle, validity, permission and Forget hard gates
      -> semantic/entity/temporal relevance
      -> decision impact and Context coverage gap
      -> epistemic status, Evidence, trust and provenance
      -> risk, sensitivity and injection cost
      -> policy + budget
      -> recommend now / defer / explicit Recall / exclude

### Factor semantics
- Semantic relevance: similarity/lexical relation, not truth.
- Entity match: exact canonical identity outweighs ambiguous name overlap (weight CANDIDATE).
- Temporal relevance: overlap with requested/active valid interval and freshness; unknown remains unknown.
- Decision impact: expected consequence of omission; never authorization.
- Risk: sensitivity, harmfulness, uncertainty, conflict and injection-risk indicators. High risk may require explicit review.
- Context coverage gap: whether G context already contains equivalent valid information; Runtime sees authorized summary only.
- Validity: lifecycle, valid-time, supersession and Forget state from D/I.
- Confidence, Trust and Evidence are separate; confidence is not truth, trust is not permission, evidence may support/refute/qualify.
- Injection cost: tokens/bytes/distraction/latency; low cost never overrides safety.

## 7. Policy Model and Weights
**DECIDED:** no weighted score can override hard eligibility gates.  
**CANDIDATE:** two stages: (1) hard gate for authorization, Forget, lifecycle, valid-time, Evidence/source access and prohibited-content policy; (2) soft utility rank over eligible candidates using feature vector, task class and budget.

Linear weighted score, learned ranker or rule table may be evaluated. Every weight and threshold is CANDIDATE/TO_VALIDATE; no numeric weight is normative without labelled task evaluation. Preserve deterministic baseline and policy version. LLM activation is not default and cannot override hard gates.

## 8. INT-P0-04 Prompt Injection
Memory text, summaries, Evidence excerpts, entity labels and relation qualifiers are untrusted data. Activation never interprets them as commands, tool requests, policy changes or developer instructions. Preserve source/provenance, source type, epistemic/lifecycle state, trust/evidence roles, sensitivity/risk flags and untrusted-data marker.

A malicious memory may still influence an LLM after injection; Runtime cannot guarantee model obedience. It can avoid elevating authority, minimize content, isolate risky candidates, attach provenance labels and recommend review. Agent-side policy remains responsible for tool/action authorization. Text delimiters are not a security boundary.

## 9. Claim / Conflict — INT-P1-02
Do not silently choose a winner among conflicting Claims. Preserve Conflict Set membership, support/refute Evidence, temporal applicability and disputed/retracted/superseded state. For explicit conflict queries, include both sides with compact evidence summary. For narrow current-state tasks, a current non-disputed view may be recommended only if D lifecycle semantics say eligible, while retaining conflict markers. Defer/require explicit Recall when ambiguity is material. Runtime cannot adjudicate truth or mutate Claim status. Claim revision identity and Conflict Set contract remain OPEN pending B/D/E.

## 10. Scope / Permission
Only authorized candidates enter policy evaluation. Recheck permission/Forget epoch before output. Evidence may be more restricted than Memory; inaccessible Evidence is represented unavailable/restricted, not fetched. No score grants access.

## 11. Version / Freshness
Recommendation binds exact Memory Version and policy version. If canonical version, lifecycle, valid-time, policy, permission epoch or Forget fence changes before handoff, mark stale and re-evaluate. Expiry is a hint, not canonical TTL. G independently validates before Context commit.

## 12. Cache Semantics
Cache deterministic feature computations keyed by candidate version, query/task fingerprint, Context summary version, policy version, authorization epoch, Forget epoch and temporal time bucket. Invalidate on canonical version/lifecycle, Evidence/Provenance update, Context version, policy, revocation, Forget and environment/task change. Never cache final Context decisions.

## 13. Failure Handling
Missing required safety metadata: fail closed or require explicit Recall. Optional feature source failure: emit explicit uncertainty/partial feature set only if policy permits. G unavailable: no Context mutation is inferred. Unknown policy version rejects activation.

## 14. Performance Budget
Deterministic bounded CPU work over candidate features. No synchronous large-LLM call on default path. Bound candidates, evidence summaries, conflict expansion and token estimation. Optional model classification is isolated, asynchronous/opt-in and TO_VALIDATE; it cannot delay hard safety checks.

## 15. Observability
Track outcomes, feature availability, policy version, reason codes, stale rate, false positives/negatives, token cost, risk exclusions, conflict preservation and G acceptance/rejection feedback. Do not log memory text or Evidence payloads.

## 16. Interfaces
From Retrieval: exact candidate/version, match features, completeness, freshness, lifecycle and provenance refs. From D/I: validity/lifecycle, epistemic status, trust metadata, current Forget/permission. From G: read-only Context summary/version and budget hint. To G: ActivationRecommendation and evidence-aware CandidateMemory with reasons, uncertainty, version and expiry. Provisional until G/D/E/I/H review; include schema/policy version, authorization/Forget epoch and typed partial/failure semantics.

## 17. Test Scenarios
Exists but irrelevant; relevant but expired; valid but disputed; suitable but not urgent. High similarity cannot override Scope/Forget/retraction. Prompt-injection text remains inert data. Preserve support and refutation. Do not conflate Trust/confidence/relevance. Avoid duplicate Context version. Re-evaluate if policy/permission changes before handoff. Model feature unavailable but deterministic path works. G rejection causes no Context mutation by F.

## 18. Dependencies and Open Questions
D lifecycle/Claim/Conflict/Trust; E freshness/Provenance update feed; G Context summary/budget/acceptance; I risk/sensitivity policy and revocation; H trusted request envelope. OPEN: policy scope/task taxonomy, Conflict Set shape, Evidence rubric, G context sufficiency signal. TO_VALIDATE: weights, thresholds, utility calibration, risk trade-offs and activation benefit.
