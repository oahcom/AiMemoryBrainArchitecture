# Phase 3.6.6 — ADR-001 Fact/Claim Decision Readiness and Cross-Owner Impact Package

- Owner: A — Principal Integration Architect
- Canonical ADR Blob: `df77e4a93cb8fef689ae7c828888d960cbf381d6`
- B semantics proposal Blob: `a1024938ff5baba069cf128c69496a44e143330c`
- Fact/Claim consumer mapping Blob: `dd45a37199c9b69ab6b68f65e051a484a04691d4`
- Status: **DECISION PACKAGE READY / ADR-BLOCKED / NO OPTION APPROVED**
- Date: 2026-11-17

## 1. Decision required

Architecture Governance must choose exactly one canonical model:

- **Option A:** Fact and Claim are distinct canonical domain objects. A Fact is an explicit attestation object linked to one or more exact immutable ClaimRevisionRefs, with attestor, authority, method, evidence, time and Scope.
- **Option B:** Claim is the only canonical proposition object; Fact is a qualified view/state of an exact ClaimRevision, with method, authority, evidence, time and Scope. No independent Fact identity exists.

B recommends Option A as the preferred candidate because it preserves the current governance distinction and provides an auditable home for independent attestation. This remains a recommendation, not a decision.

## 2. Baseline conflict and evidence

The canonical ADR records that current governance baselines I-04/P-04/README distinguish Fact from Claim, while the current domain overview/model has Fact/Claim conflation. Option A preserves the current governance distinction but introduces a separate identity/lifecycle and cross-object consistency obligation. Option B simplifies the graph but requires Architecture Governance to explicitly amend the existing baseline/terminology.

The repository does not currently contain a named formal Architecture Governance authority, named approver(s), timestamped decision, approved option or accepted rationale. No decision can be inferred from B's recommendation, downstream implementation, review silence or a commit.

## 3. A's recommended decision path

**Recommend Option A as the default candidate**, subject to Architecture Governance confirming that independent attestation is a product requirement. The reason is baseline preservation: without an explicit governance change, Option B would silently weaken the existing Fact/Claim distinction.

Option A must not be interpreted as “high confidence means Fact.” Fact creation requires an explicit attestation action over an exact ClaimRevisionRef, by an authorized attestor, using a declared method, evidence set, time and Scope. Multiple attestations may coexist and be independently revoked/superseded. A Fact never overwrites or mutates the underlying ClaimRevision.

If Architecture Governance determines that no independent attestation product requirement exists, it may choose Option B, but must explicitly amend I-04/P-04/README and terminology through its authorized change process before Option B becomes normative.

## 4. Cross-owner impact matrix

| Owner | If Option A | If Option B | Current safe behavior while blocked |
|---|---|---|---|
| B — Domain Model | Define FactRef as separate attestation identity linked to ClaimRevisionRef(s); own attestation lifecycle and authority semantics. | No FactRef; define qualified-view state on ClaimRevision. | Claim/Evidence/Provenance/ClaimRevision remain candidates; no canonical Fact ID. |
| D — Memory Brain | Persist Fact attestation separately from ClaimRevision; independent correction/revocation/supersession lifecycle; atomic links. | Persist qualification metadata on ClaimRevision; no second canonical object. | No canonical Fact schema/table/API freeze. |
| E — Compiler | CandidateProposition/ExtractionIR remains neutral; only explicit authorized attestation path may create Fact. | Compiler maps qualification evidence to ClaimRevision view after policy approval. | No canonical ClaimRef/FactRef assignment by extraction or confidence. |
| F — Runtime | Retrieval can distinguish assertions from attested Facts and filter by attestation authority/method/Scope. | Retrieval renders qualified ClaimRevision views without separate Fact identity. | No FactRef index or canonical fact filter. |
| G — Context | Render Claim and Fact attestation separately; pin exact ClaimRevisionRef and FactRef/evidence for historical views. | Render qualified view pinned to exact ClaimRevisionRef and qualification evidence. | No conflation of Context Remove with Claim/Fact lifecycle. |
| H — BMCP | FactRef/attestation message fields only after approved schema/version and I/D semantics. | No independent FactRef wire identity; qualified ClaimRevision fields only. | No Fact/Claim wire schema freeze. |
| I — Security/Governance | Authorize attestor PrincipalRef/IssuerRef, method, Scope, revocation and evidence visibility. | Authorize qualification transition on exact ClaimRevision. | I-04/P-04 remain authoritative; no attestation authority inferred. |
| C — Agent Integration | Provider/source telemetry is Evidence/Provenance, never Fact attestation by itself. | Provider/source telemetry remains Evidence supporting a qualified ClaimRevision view. | No automatic fact promotion from model confidence or provider output. |

## 5. Migration and conformance requirements

Whichever option is chosen, the following remain mandatory:

1. ClaimRef and immutable ClaimRevisionRef semantics; corrections append revisions rather than mutate history.
2. Evidence and Provenance remain first-class, source-attributed and independently access-controlled.
3. Epistemic status, verification/attestation, lifecycle, temporal validity and Scope are orthogonal dimensions; no overloaded status enum.
4. ConflictSet groups exact ClaimRevisionRefs and does not silently choose a winner.
5. Retraction, correction and temporal as-of queries preserve historical assertions and evidence.
6. Confidence alone never promotes a Claim to a Fact or verified state.
7. Forget/revocation suppresses all derived Fact/Claim/Evidence projections and prevents late replay resurrection.
8. Existing 15 consumer conformance scenarios in `fact-claim-consumer-mapping.md` must be run against the approved model, with exact build and owner evidence.
9. Migration plan must cover existing references, data, APIs, wire fields, index projections and Context snapshots.

## 6. Formal approval record required

Before ADR-001 can leave BLOCKED, the repository must contain:

- Named formal Architecture Governance body and decision rights.
- Named approver PrincipalRef(s) acting under that authority, with authenticated approval evidence.
- Exact Option A or Option B choice, timestamp and accepted rationale.
- Exact baseline changes to I-04/P-04/README/terminology if Option B, or confirmation of existing baseline if Option A.
- Cross-owner B/D/E/F/G/H/I/C sign-off against the exact approved model.
- Migration/compatibility plan and conformance test evidence.

No owner, including A, may self-approve the Architecture Governance decision. User delegation to continue engineering work is not itself an ADR decision unless the authorized governance record explicitly says so.

## 7. Work that may proceed without the ADR

- Neutral CandidateProposition/ExtractionIR and source Evidence/Provenance capture.
- Non-normative ClaimRevision/ConflictSet proposals and conformance test fixtures.
- Storage/Forget/restore infrastructure that does not depend on FactRef identity.
- Retrieval/context adapters that preserve unknown candidate state and do not label content as Fact.

Canonical Fact/Claim identity, schema, IDs, API/wire contract and production data migration remain blocked.

## 8. Final disposition

**ADR-001 remains ADR-BLOCKED.** A recommends Option A but does not approve it. This package makes the decision and impact surface explicit; it does not alter I-04/P-04/README or freeze any module schema. TAB-001 remains CANDIDATE / NOT FROZEN and production activation remains NOT AUTHORIZED.