---
document_metadata:
  domain: ai-development
  role: decision-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: "user-authorized operator (delegated by account owner)"
      decision_date: "2026-11-27"
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-253/evidence.md"
        - "docs/en/13-engineering-decisions/req02-fts5-vs-like-decision.md"
        - "14-ai-development/adr/ADR-RUN-001-durable-store-and-transaction-boundaries.md"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-27"
      last_verification_note: "Bounded dispositions use current main-tree evidence; no production profile or Owner approval is inferred."
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
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "13-engineering-decisions/REQ04-MATURE-IMPLEMENTATION-DISPOSITIONS-001.md"
    en: null
    zh-CN: "docs/zh-CN/13-engineering-decisions/REQ04-MATURE-IMPLEMENTATION-DISPOSITIONS-001.md"
---

# REQ-04 — Mature implementation disposition records

- Decision record: REQ04-MATURE-IMPLEMENTATION-DISPOSITIONS-001
- Related issue: #265
- Decision date: 2026-11-27
- Decision authority: user-authorized operator (delegated by account owner)
- Attribution boundary: **代理裁决，非自然人 Owner 签署。** These are bounded delegated dispositions for AC4 evidence. They do not claim a natural-person Owner signature, cross-Owner acceptance, production approval, or a system-wide technology freeze.
- Overall status: four explicit DEFER decisions; none is an implicit rejection.

## 1. SQLite local profile — DEFER

**Decision:** DEFER selection of SQLite as the final L4 deployment/storage profile. Retain the existing SQLite adapter and tests as a bounded local reference implementation; do not promote it to the production or cross-host authority profile.

**Reason:** Main contains SQLite adapter crates and integration tests, and Phase 1 decision material records bounded same-process, independent-connection CAS and idempotency behavior. This does not establish a representative Brain workload, cross-process/multi-host linearizability, HA/failover behavior, or complete backup/restore correctness. ADR-RUN-001 remains PROPOSED and explicitly does not claim database deployment or recovery testing.

**Reopen when:** (a) D and Storage publish and accept exact logical row/write-set ownership and L4 profile; (b) a representative Brain workload is reproducibly benchmarked; (c) transaction atomicity and concurrency are tested across processes; (d) crash, failover, backup and restore tests cover required canonical state and derived projections; and (e) results are compared on equal terms with PostgreSQL and accepted by Storage/D/Engineering.

## 2. PostgreSQL server profile — DEFER

**Decision:** DEFER selection of PostgreSQL as the final L4 server profile. Do not infer that a mature server database is automatically the correct Brain storage authority.

**Reason:** Current main evidence does not contain a comparable PostgreSQL implementation/profile with representative Brain workload results, exact D/Storage transaction semantics, or complete HA/backup/restore acceptance. PostgreSQL maturity is a reason to evaluate it, not evidence that repository invariants are satisfied.

**Reopen when:** (a) a version-pinned PostgreSQL profile and schema/migration set are supplied; (b) the same representative workload and correctness vectors used for SQLite are run; (c) isolation, atomic write-set, idempotency, failover, backup/restore and operational burden are measured; (d) results are compared against SQLite; and (e) Storage/D/Engineering accept the exact profile and recovery contract.

## 3. Cedar PDP — DEFER

**Decision:** DEFER Cedar as a production Policy Decision Point. It may remain a bounded candidate evaluator behind an I-owned authorization interface; Cedar must not become the policy authority by virtue of being integrated.

**Reason:** The conflict register records Cedar as candidate only. Current evidence does not establish required wrapper conformance vectors, current-revocation behavior, fail-closed handling of evaluation errors/UNKNOWN, or I/Security Owner approval. Policy meaning, principal authority, revocation and PermissionEpoch remain I-owned.

**Reopen when:** (a) a version-pinned Cedar policy/model and wrapper contract are published; (b) allow/deny/unknown/error, malformed input, stale policy, revocation and replay vectors pass; (c) error and UNKNOWN paths demonstrably fail closed; (d) integration rechecks current I authorization at the required side-effect/disclosure boundary; and (e) I and Security Governance approve the exact version and evidence.

## 4. Tantivy — DEFER, NOT REJECTED

**Decision:** DEFER Tantivy as an alternative lexical index. This is **not a rejection** and does not extend the bounded SQLite FTS5 decision into a claim that FTS5 is universally superior.

**Reason:** The existing REQ02 lexical ADR selects FTS5 only for the bounded initial local lexical channel and explicitly records that no comparable FTS5-vs-Tantivy benchmark or operational comparison exists. The FTS5-vs-LIKE synthetic benchmark does not compare two mature full-text implementations and cannot establish Tantivy's inferiority.

**Reopen when:** (a) a reproducible FTS5-vs-Tantivy benchmark uses the same representative corpus, language/tokenization assumptions, query set and ranking/correctness criteria; (b) result parity/relevance, indexing throughput, update/delete churn, concurrent access, rebuild time, storage growth and latency are measured; (c) native adapter integration and authorization/Forget filtering are tested; and (d) a material advantage against agreed workload thresholds is shown and accepted by relevant Owners.

## 5. Consequences and limits

- These four decisions satisfy the consideration/disposition part of AC4; they do not select a production implementation.
- No product gains Canonical Truth, Evidence, Authorization, Forget, Lifecycle or Applied authority.
- CF-013 and CF-014 remain unresolved until their own closure evidence and Owner acceptance are supplied.
- This record is informative and non-canonical; it does not amend Owner contracts or the existing FTS5 ADR.
