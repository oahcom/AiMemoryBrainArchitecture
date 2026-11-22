---
document_metadata:
  domain: domain-model
  role: decision-record
  lifecycle:
    approval:
      decision_status: Approved
      approver: "Project Owner delegate under Issue #305 comment 7042461592"
      decision_date: "2026-11-21"
      approved_version:
        scheme: git
        value: "003fa0063e1e359bc91de8c2950366f757bd1210"
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "Issue #305 comment 7042461592"
        - "02-domain-model/domain-model-overview.md @ 5b86fe23ab7c670b4ae13331b56572aee35f5d00"
        - "02-domain-model/core-entities.md @ 06a914699813e36d8bfd69e96c46debb3c3e0cf3"
        - "B ADR branch session-b-domain-model-phase3 @ 2faf8ec38f14dba49e7263d7a60804dae1a74ee2"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-21"
      last_verification_note: "Live GitHub readback of cited main and B-branch artifacts; semantic decision only, no implementation schema freeze."
    usage_status: Active
    modification_status: Pending-Reapproval
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
    canonical_scope: "Project Owner decision: Fact and Claim semantics and identity"
    canonical_scope_id: "domain-model/fact-claim-identity"
    canonical_scope_keywords:
      - fact
      - claim
      - attestation
      - identity
      - revision
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Normative
  bilingual_counterpart:
    source: "14-ai-development/adr/OWNER-DECISION-FACT-CLAIM-001.md"
---

# OWNER DECISION — FACT / CLAIM SEMANTICS AND IDENTITY

- Decision ID: OWNER-DECISION-FACT-CLAIM-001
- Related ADR: B-ADR-FACT-CLAIM-001
- Decision date: 2026-11-21 UTC
- Decision authority: Project Owner delegate under Issue #305, comment 7042461592
- Capacity: consolidated architecture-owner session under the Owner's standing instruction
- Evidence posture: `INDEPENDENCE_UNVERIFIABLE` because this decision records no prompt-pairing evidence with the implementation session; a shared GitHub account is not grounds for denying independence. No independent human signature is claimed.

## 1. Decision

**DECIDED: select Option A (separate Fact attestation and Claim proposition) with I1 (stable Claim identity plus immutable Claim revisions).**

This is a semantic architecture decision for the development baseline. It resolves the conceptual and identity/version questions in B-ADR-FACT-CLAIM-001.

It does NOT freeze JSON Schema, database DDL, storage layout, public API, BMCP wire fields, or Runtime implementation.

## 2. Adopted semantics

1. Claim is an attributable proposition thread: what an actor, source, or process asserts, observes, reports, infers, questions, disputes, corrects, or withdraws.
2. ClaimRevision is one immutable assertion state under a stable Claim identity.
3. Fact is a separately identified, governed attestation/adjudication object. It is not a synonym for Verified Claim, a confidence threshold, or a guarantee of objective truth.
4. FactRevision is one immutable attestation state. It MUST reference exact ClaimRevisionRef values, exact Evidence and Provenance references, Scope, attestor identity, method and immutable method version, the applicable I authorization decision, validity/recording context, and correction/revocation lineage.
5. A Claim may exist without any Fact. A Verified Claim does not automatically create a Fact. A Fact may attest to, qualify, narrow, or supersede one or more exact Claim revisions.
6. Historical ClaimRevision and FactRevision records are append-only and MUST NOT be silently overwritten. A Fact MUST NOT follow a mutable/latest Claim revision.

## 3. Identity and revision choice

Adopt I1:

- ClaimRef is stable for one proposition identity within its declared identity and Scope boundary.
- Each immutable assertion state receives an exact ClaimRevisionRef.
- FactRef is stable for one governed attestation thread.
- Each immutable attestation state receives an exact FactRevisionRef.
- A proposition-identity change creates a new Claim. A non-identity-changing evidence, provenance, epistemic, or editorial update creates a new ClaimRevision under the existing ClaimRef, according to DOMAIN-MODEL-001 §2.4.
- A change to the attestation result or its evidence/method basis creates a new FactRevision, never an in-place mutation.
- Scope changes do not transfer identity or access rights. Cross-Scope authorization is independently checked.

Adopt the exact Claim identity classification in the current DOMAIN-MODEL-001 §2.4. Ambiguous classification fails closed and requires an explicit governed decision; text similarity alone never merges Claims.

## 4. Authority allocation

| Concern | Authority |
|---|---|
| Claim/Fact semantic vocabulary and epistemic meaning | Domain Model |
| Canonical ClaimRef / ClaimRevisionRef / FactRef / FactRevisionRef allocation, lifecycle, revision commit and ConflictSet lifecycle | D |
| Principal and attestor authorization, PermissionEpoch, revocation, retention and global Forget policy | I |
| D ForgetOperation / ForgetFence generation and ordering; I policy binding and global completion | D + I within their respective authority |
| Immutable physical persistence and atomic commit implementation | Storage, consuming D's canonical commit contract |
| Candidate extraction and proposal generation | E; no canonical ID minting and no Fact from extraction confidence |
| Retrieval and Context consumption | F/G; exact revision-pinned references only |
| Wire representation, protocol envelope and Adapter transport | H; no wire fields frozen by this decision |

No authority may infer permission from Scope or infer truth from confidence, a model score, or a transport acknowledgement.

## 5. Consumer requirements

- E / Memory Compiler retains neutral CandidateProposition and ExtractionIR; it may submit Claim proposals but MUST NOT mint canonical identities. A Fact proposal requires an explicit authorized attestation operation and its Evidence/Provenance.
- D owns canonical identity, immutable revision persistence, lifecycle and canonical ConflictSet decisions. D validates expected-parent/currentness and commit semantics.
- I authorizes protected operations and attestors using current PermissionEpoch and policy. BMCP and E do not duplicate I's authority.
- F/G consume exact ClaimRevisionRef and FactRevisionRef; no semantic-similarity resolution, latest-head substitution, or unqualified mutable lookup.
- H may carry opaque, version-pinned references. Exact wire names, requiredness, serialization and schemas remain H-owned and unfrozen.
- Storage persists immutable revisions and implements the D-defined atomic commit boundary. This decision selects no physical engine or topology.

## 6. Reconciliation and supersession

This decision supersedes the earlier C2 / Option B candidate recommendation in B-ADR-FACT-CLAIM-001. It aligns the conceptual model with current main DOMAIN-MODEL-001 and core-entities.md, and with I-04 / P-04, which distinguish Fact from Claim.

The older ADR text remains historical evidence of the decision process. This record supersedes only the earlier statement that no semantic option has been selected. B-ADR-FACT-CLAIM-001 remains ADR-BLOCKED for canonical schema freeze and downstream implementation mapping until its own §8 conditions are satisfied: B/D/E/F/G/H/I consumer mapping, migration/compatibility plan, conformance scenarios, and evidence. No consumer may treat this semantic selection as schema-freeze authority.

The terminology entry Fact / Claim must be split into Claim, ClaimRevision, Fact, and FactRevision. The canonical BMCP expansion remains Brain Memory Context Protocol.

## 7. Explicit non-decisions

This decision does not approve a Fact verification policy, attestor role catalogue, or universal truth threshold; freeze field-level JSON Schema, DDL, indexes, or database topology; authorize Runtime implementation or migrations; define BMCP wire payload fields or ACK semantics; close physical Forget, restore, publication, or production acceptance gates; or claim independent human review or signature.

Those items remain subject to their own evidence and acceptance criteria.

## 8. Required follow-up

1. Update the B ADR status and source pins to reference this semantic selection while keeping ADR-BLOCKED for schema freeze until all B-ADR-FACT-CLAIM-001 §8 conditions are evidenced.
2. Reconcile canonical terminology and bilingual domain readers.
3. Update Memory Compiler and BMCP handoff documents to consume Option A + I1 without freezing wire/storage schemas.
4. Keep Issue #7 IMPLEMENTATION_BINDING=DEFERRED_TO_ENGINEERING_PHASE unchanged.
5. Record Runtime tests as NOT RUN until an authorized Runtime repository and executable target exist.

## 9. Acceptance

The semantic decision is accepted for the development architecture baseline. Exact implementation contracts remain Candidate until responsible consumer artifacts are version-pinned and reviewed.
