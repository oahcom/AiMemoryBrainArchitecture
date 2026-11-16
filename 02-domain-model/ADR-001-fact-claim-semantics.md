# ADR-001 — Fact / Claim Domain Semantics

- **Status:** **ADR-BLOCKED — no formal Architecture Governance decision recorded**
- **Owner:** B — Domain Model (analysis and recommendation only)
- **Decision authority:** Architecture Governance / formally designated decision-maker
- **Related:** DM-001, INT-P0-01, INT-P0-02, INT-P1-02, INT-P1-06
- **Last reviewed baseline:** `session-b-domain-model-phase3` @ `ab19afbf92f67fe0a7679e9aa3a35b015fed89f4`

## 1. Context

The repository baseline is inconsistent:

- `00-governance/architecture-invariants.md` I-04 and `00-governance/design-principles.md` P-04 distinguish Fact from Claim.
- README language also lists facts and claims as distinct domain concepts in its principles.
- `02-domain-model/domain-model-overview.md` currently states that Claim is the canonical proposition object and Fact is a qualified interpretation, not a separate object.
- The existing domain model has no approved independent Fact identity/revision contract, while D/E consumer mapping requires a stable decision before canonical schema and wire fields can be frozen.

This is a normative baseline conflict, not a naming-only discrepancy. B cannot resolve it unilaterally.

## 2. Decision drivers

1. Preserve distinction between a proposition/assertion and an adjudicated/attested fact, if the product requires both.
2. Preserve provenance, evidence, time, Scope and authority for every assertion.
3. Prevent extraction confidence or model output from being promoted to truth.
4. Support correction, retraction, conflict and immutable history.
5. Avoid duplicating every Claim as a Fact where no separate attestation use case exists.
6. Keep Compiler proposal, D canonical identity/commit, I authorization and H wire boundaries separate.
7. Avoid a breaking migration of I-04/P-04/README without explicit governance approval.

## 3. Option A — Fact is a separate attestation object

**Model:** Claim is an attributable proposition thread with immutable ClaimRevision. Fact is a separate, independently addressable attestation/adjudication object (with FactRevision) that references one or more exact ClaimRevisionRefs and records the authorized attestor, method, evidence basis, validity and decision history.

**Advantages**
- Preserves the existing governance language that Fact and Claim are distinct concepts.
- Makes the difference between “someone asserted P” and “an authorized process attested P” explicit and auditable.
- Supports attestations over multiple Claim revisions, explicit adjudication, expiry/revocation and domain-specific verification.
- Avoids overloading Claim epistemic status with both assertion provenance and institutional attestation semantics.

**Costs / risks**
- Adds a distinct identity, revision, lifecycle and authorization surface.
- Requires explicit attestation use cases, authorized attestor roles, methods, revocation and supersession semantics.
- Risks duplicating Claim/Evidence metadata if Fact is not narrowly defined as an attestation over exact ClaimRevisionRefs.
- Requires D to own canonical Fact identity/commit if adopted; E may only submit a proposal.

**Required constraints**
- Fact MUST reference exact ClaimRevisionRef(s), not a mutable Claim head.
- Fact MUST carry attestor ActorRef, method/version, evidence refs, ScopeRefs, validity, decision time, issuer/authority and immutable revision history.
- No model confidence, extraction score, repetition count or heuristic alone creates a Fact.
- A Fact does not erase, overwrite or silence incompatible Claim revisions.
- Fact creation/revocation requires explicit I-authorized operation and D canonical commit.

## 4. Option B — Fact is a qualification/view of ClaimRevision

**Model:** Claim is the only canonical proposition identity. “Fact” is a qualified interpretation or view of an exact ClaimRevision (e.g. Verified/fact-qualified), without a separate Fact identity or persistence object.

**Advantages**
- Simpler canonical graph, fewer identity and lifecycle objects.
- Avoids duplicated Claim/Fact storage and cross-object consistency problems.
- Aligns with the current Domain Model Overview and existing Claim epistemic-status vocabulary.
- Keeps evidence and provenance attached directly to ClaimRevision.

**Costs / risks**
- Conflicts with current I-04/P-04/README distinction unless Governance formally revises those baselines.
- “Fact” may become an ambiguous label for a Verified Claim, weakening the distinction between assertion and attestation.
- Multiple attestations, attestors, verification scopes or revocation histories may be difficult to represent without reintroducing a separate object.
- A qualified view may be mistaken by consumers as a stronger truth guarantee than its method supports.

**Required constraints**
- The qualification MUST be attached to an exact immutable ClaimRevision and include method, authority, evidence, time and Scope.
- No free-floating Fact label or confidence-only promotion.
- Historical fact-qualified views resolve to the exact ClaimRevision and qualification evidence at that time.
- Governance MUST explicitly update I-04/P-04/README/terminology and dependent contracts before this option can be normative.

## 5. B recommendation (not a decision)

**B recommends Option A as the preferred candidate**, because it preserves the current governance distinction and gives an auditable home to explicit attestation without treating every Claim as verified. This recommendation is conditional on confirming a real product requirement for independent attestation and on D/I agreeing the identity, lifecycle and authorization boundaries.

This is not an approval. B has no authority to approve or amend Architecture Governance invariants. Option A MUST remain labelled CANDIDATE until the formal decision authority records a decision.

## 6. Decision record — intentionally blocked

| Required record | Current value |
|---|---|
| Formal decision authority / named governance body | **NOT RECORDED** |
| Named approver(s) with decision authority | **NOT RECORDED** |
| Decision timestamp | **NOT RECORDED** |
| Approved option | **NONE** |
| Approval record / meeting or governance artifact | **NONE** |
| Decision rationale accepted by authority | **NONE** |
| Required baseline updates | **NOT AUTHORIZED** |
| Status | **ADR-BLOCKED** |

No implicit approval is inferred from review comments, branch existence, B recommendation, consumer implementation, or a commit authored by a module owner.

## 7. Consequences while blocked

- E MUST retain neutral CandidateProposition/ExtractionIR; it MUST NOT assign canonical ClaimRef or FactRef.
- D MUST NOT freeze canonical Fact/Claim schema, IDs, storage or API shape based on Option A or B.
- F/G MUST NOT assume FactRef or collapse fact-qualified semantics into a stable canonical field.
- H MUST NOT freeze Fact/Claim wire fields.
- C telemetry remains source/producer observation, not Fact attestation.
- Consumer mapping in `fact-claim-consumer-mapping.md` remains CANDIDATE; all canonical Fact/Claim identity portions are ADR-BLOCKED.
- Existing overview language is recorded as current domain proposal/baseline text, not as governance resolution of I-04/P-04.

## 8. Reopening / approval checklist

The ADR may leave BLOCKED only when the repository contains:
1. a named formal Architecture Governance authority and its decision rights;
2. named approver(s) acting in that authority;
3. an explicit Option A or Option B decision;
4. timestamped approval record and accepted rationale;
5. impact analysis and authorized changes to I-04/P-04/README/terminology and dependent modules;
6. B/D/E/H/I consumer mapping sign-off;
7. migration and compatibility plan for existing references and data;
8. conformance scenarios and evidence.

Until all items exist, status remains **ADR-BLOCKED**.
