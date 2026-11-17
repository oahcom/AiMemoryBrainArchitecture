# Migration and Risk Analysis

- Status: CANDIDATE PLAN; no migration authorized.

## 1. Recommended migration path

1. **Freeze nothing.** Keep current E pipeline and D commit contract authoritative.
2. **Shadow IR.** Generate L0/L1 IR beside existing candidate production for a narrow source type; do not change canonical writes.
3. **Compare.** Measure accepted candidate parity, provenance graph closure, diagnostics, conflict proposals, replay, CPU/memory and model-token overhead.
4. **Owner review.** E reviews stage ownership/pass contracts; B reviews only domain mapping and retains Fact/Claim ADR block; D reviews commit projection; I reviews scope/retention/Forget implications.
5. **Conformance.** Add fixtures for retries, source unavailability, changed prompt/rules, resolver snapshot changes, cross-scope denial, Forget fence advancement, duplicate delivery and canonical CAS conflicts.
6. **Canary one output class.** Only after approvals, map one candidate type through IR to the existing D contract with a rollback switch.
7. **Expand or remove.** Keep IR only if measured quality/operability gain exceeds added storage, migration and cognitive cost.

## 2. Main risks

| Risk | Severity | Mitigation |
|---|---|---|
| IR becomes competing canonical model | Critical | Mark non-authoritative; no direct persistence as canonical; D projection only |
| Fact/Claim decision smuggled into node kinds | Critical | Neutral AssertionCandidate; hard block affected lowering |
| Provenance retention conflicts with Forget/privacy | Critical | Owner-defined retention, redaction and tombstone policy; no unconditional raw retention |
| Old IR unreadable after schema evolution | High | Versioned readers, explicit upgrades, golden fixtures, fail-closed unknown major |
| Model nondeterminism mislabeled deterministic | High | R0-R3 replay classes; store immutable response refs |
| Entity resolution changes with catalogue | High | Pin resolver snapshot; invalidate dependent passes |
| IR overhead exceeds value | Medium | Shadow-mode cost and complexity budget; no framework until evidence |
| Diagnostics leak protected content | High | Store refs and redacted messages; enforce scope before dereference |
| Incremental cache bypasses live policy | Critical | Treat authorization/Forget as live gates, not cache keys alone |
| Duplicate candidate paths drift | Medium | One lowering adapter and conformance suite |

## 3. Rollback

Shadow generation can be disabled without changing canonical writes. If a canary path is later approved, keep the direct pipeline as fallback until parity and rollback are demonstrated. Canonical versions already committed are not rewritten by an IR rollback. Any recompile must use current Permission/Forget checks and idempotency rules.

## 4. Open questions for Owners

- E: what is the authoritative current stage/work-item schema and whether a candidate IR already exists in detailed E contracts?
- B: what is the authorized Fact/Claim ADR disposition and stable identity rule for Claims across Memory versions?
- D: what exact current commit request schema should L3 target, and what validation belongs at D?
- I: which source/provenance data may be retained, redacted, or tombstoned after Forget?
- Storage/Consistency: where can immutable IR blobs live and what recovery/retention guarantees apply?
- C/F/G/H: which downstream consumers need IR metadata, and which must never see it?

## 5. Non-goals

This proposal does not solve extraction truthfulness, model hallucination, external-source reliability, identity ambiguity, authorization correctness, cross-owner publication atomicity, physical Forget, or production runtime readiness. It does not close Issue #43 blockers or authorize schema freeze.
