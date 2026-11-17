# AID-2026-001 — Preliminary Cross-Owner Governance Assessment
# 初步跨 Owner 治理评估

**Status:** PRELIMINARY / ROLE-LENS ONLY — NOT NINE INDEPENDENT REVIEWS  
**Target:** AI-STD-001 v1.0, AI-PROC-001 v1.0, AI-TPL-001 v1.0 (all PROPOSED)  
**Base:** `main` at `55d44b9276456f88bd2193de8b06aff146c228a4`  
**Purpose:** Record issues visible from the governance text before independent Owner sessions execute the prompts.

## 1. Provenance limitation

This assessment was prepared in the coordinating conversation after reading the governance documents. It is not nine separate Owner sessions, does not contain nine independent signatures, and cannot satisfy the independent-review gate in AI-STD-001 §3.2. The A–I sections below are review lenses and preliminary hypotheses for the actual Owner sessions to confirm, reject or refine.

The owner branch lookup confirmed the named A–I branches exist, but several guessed document paths were not found. This assessment therefore does not claim complete inspection of every Owner branch. Each dedicated reviewer must record exact source paths and SHAs it actually reads.

## 2. Cross-cutting preliminary findings

### GOV-P1-01 — Project governance authority is not explicitly identified
**Severity:** P1  
**Evidence:** AI-STD-001 §3.2 assigns an Acceptance Authority “according to project governance”; §12 says the baseline needs explicit approval by the project's governance authority. No role, decision procedure, quorum, approval record or escalation path is defined in the target documents. A's role is Principal Integration and integration decision-making, which is not automatically equivalent to authority to approve project-wide governance policy.  
**Required change:** Define Project Governance Authority separately from A. Specify who can approve the initial baseline and normative amendments, required approval evidence, effective date/version, and how conflicts/escalations are decided. A may recommend and integrate; it must not self-grant policy authority.  
**Closure:** I and A provide domain/integration recommendations; project sponsor/governance authority explicitly approves the named version.

### GOV-P1-02 — Cross-module review and sign-off evidence is not sufficiently formalized
**Severity:** P1  
**Evidence:** AI-PROC-001 §3 Pattern C and §7 distinguish owner and integration review, but no mandatory parent Work Item schema requires each child Owner's disposition, exact reviewed SHA, unresolved dissent, or approval scope.  
**Required change:** Require a parent Work Item plus Owner child records for multi-owner tasks. Each Owner signs only its boundary, against exact source/target SHAs. A records integration disposition separately. Project acceptance remains separate.  
**Closure:** Manifest/template and lifecycle updated; a sample multi-owner record demonstrates the chain without treating a coordinator's simulated roles as independent.

### GOV-P1-03 — Risk-to-verification matrix is underspecified
**Severity:** P1  
**Evidence:** AI-STD-001 §4 defines R0–R3 but gives only broad R2/R3 review requirements. AI-PROC-001 §5 says CI “should” run checks and leaves required checks selected by class/risk without a normative matrix.  
**Required change:** Add a mandatory matrix by task class and risk. Define minimum checks for ARCH/IMPL/TEST/SEC/MIG/PERF/DOC/OPS, including when build, unit, integration, contract, fault, security, migration, rollback and benchmark evidence are required. Use MUST for merge-blocking checks; define a waiver authority and expiry for NOT RUN.  
**Closure:** Owner review confirms domain-specific additions; Testing/Quality specialist reviews the matrix.

### GOV-P1-04 — Prompt hash byte-level canonicalization is undefined
**Severity:** P1  
**Evidence:** AI-STD-001 §5 and AI-TPL-001 §3 require SHA-256 but do not define the exact hashed artifact, encoding, BOM policy, line-ending policy, whitespace treatment or whether front matter/attachments/addenda are included.  
**Required change:** Define hash over exact stored prompt file bytes as committed (UTF-8, no implicit normalization; line endings are part of bytes), record file path, byte length and digest algorithm. Every run addendum/attachment must be separately hashed and linked; a prompt hash must not be recomputed from rendered chat text.  
**Closure:** Template updated and a deterministic verification example/test added.

### GOV-P1-05 — Independent reviewer clean-room requirements are incomplete
**Severity:** P1  
**Evidence:** AI-STD-001 §3.2 requires a separate session/agent and says role simulation is not independent, but does not specify reviewer inputs, access to implementation author narrative, clean review order, or whether same conversation lineage can count.  
**Required change:** Require a distinct session with no authorship of the change; reviewer receives prompt, task criteria, diff, source contracts and raw test evidence, and must independently inspect the diff before reading the author's self-assessment where practicable. Reviewer records session provenance and conflicts. A single coordinating session cannot produce independent sign-offs by changing personas.  
**Closure:** Prompt pack and review template enforce provenance and evidence-first review.

### GOV-P2-01 — Cross-cutting specialists lack a stable registration and authority model
**Severity:** P2  
**Evidence:** AI-STD-001 §3.1 names Storage/Consistency, Testing/Quality, Observability/Performance and Release but does not define their authority, required review triggers, appointment or record path.  
**Required change:** Define specialist registry, scope, reviewer triggers and limits. Specialist findings do not transfer module decision rights.

### GOV-P2-02 — Retrospective bootstrap work needs a first-class evidence-gap state
**Severity:** P2  
**Evidence:** AI-PROC-001 §7 allows retrospective records and AI-STD-001 §12 disclaims retroactive certification, but the manifest has no explicit bootstrap/retrospective flag or missing-evidence reason taxonomy.  
**Required change:** Add `record_origin: contemporaneous | retrospective_bootstrap`, evidence completeness and `NOT_RECORDED` reasons. Do not fabricate original prompt IDs/hashes or reviewers.

## 3. Preliminary Owner lenses — pending independent confirmation

### A — Integration
- Verify GOV-P1-01 and GOV-P1-02.
- Add conflict matrix, dissent preservation and exact reviewed SHA discipline.
- Ensure A's integration disposition is distinct from project-level policy approval.

### B — Domain model
- Ensure requirement, assumption, proposal, decision and canonical domain object are typed distinctly in work records.
- Require schema/ADR ownership, compatibility review and generated schema/fixture review.
- Prevent candidate domain semantics from becoming normative through prompt wording alone.

### C — Agent integration
- Require explicit no-raw-CoT, no protected system/developer prompt extraction, and no instruction elevation of retrieved memory.
- Require inference-boundary, Adapter identity, telemetry semantics and final-request Applied evidence for relevant tasks.
- Preserve model/Agent neutrality and distinguish intent/plan from observed outcome.

### D — Memory Brain
- Classify Forget, canonical write ordering, provenance integrity and recovery as R3.
- Require producer barrier/fence race tests and distinguish logical suppression, asynchronous cleanup and physical erasure.
- Prevent a local Owner test from being represented as global Forget completion.

### E — Memory Compiler
- Require tests for accepted receipt vs canonical commit, idempotency conflicts, lease expiry, retry/DLQ/replay and late derivative suppression.
- Require durable lineage/dependency registration before derivative visibility and final publication gate evidence.
- Prevent extraction output from being promoted to canonical truth without owner-governed process.

### F — Memory Runtime
- Require Scope-before-Candidate, stale cache/Working Set suppression, in-flight retrieval finalization and index rebuild race tests.
- Define workload/hardware/warm-cold conditions for performance claims.
- Keep activation recommendation distinct from Context version ownership.

### G — Memory Context
- Require immutable ContextVersion/CAS and state-machine tests for delivery, invalidation, stale ACK and reconciliation.
- Keep Context Remove distinct from canonical Forget.
- Applied must bind exact managed region and final inference request evidence; local buffer write is insufficient.

### H — Protocol
- Require exact wire schema versioning, canonical encoding, golden vectors, compatibility tests and replay/anti-replay evidence.
- Distinguish authenticated transport identity from payload claims.
- Define unknown outcomes and typed cursor/epoch namespaces; prohibit cross-namespace comparison.

### I — Security and governance
- Require explicit threat model, authenticated Principal/ActorRef/ScopeRef mapping, least privilege and permission epoch currentness.
- Treat memory, evidence, prompts and generated summaries as untrusted data; add prompt-injection/adversarial test gates.
- Define secret redaction and safe test fixture rules.
- Define who may accept residual R3 security/privacy/deletion risk; A alone should not.

## 4. Preliminary disposition

**CONDITIONAL PASS FOR CONTINUED REVIEW ONLY. NOT READY FOR FORMAL BASELINE APPROVAL.**

The current documents provide a strong operating-model foundation, but GOV-P1-01 through GOV-P1-05 must be resolved or explicitly dispositioned before a formal baseline can be recommended. The nine Owner reports remain pending. No code tests, CI checks, independent reviews, or project-level approval are claimed by this preliminary assessment.
