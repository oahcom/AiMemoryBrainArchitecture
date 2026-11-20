# WORK ITEM: PROPOSED AID-2026-026
# Fact and Claim Semantic Architecture Decision
# REQ-07 MQ-01

## 1. IDENTITY AND ROLE

You are a Domain Architecture Designer and Epistemic Modeling Researcher.

Primary requirement:
REQ-07 — Issue #347
https://github.com/oahcom/AiMemoryBrainArchitecture/issues/347

Related requirement:
REQ-06 — Issue #346

Coordination hub:
https://github.com/oahcom/AiMemoryBrainArchitecture/issues/345

Finding:
MQ-01 — Fact/Claim identity is unresolved; the inspected implementation lacks a distinct Fact type.

Proposed Work Item ID: AID-2026-026.

Formal allocation must be checked before use.

## 2. OBJECTIVE

Produce a precise and implementable semantic decision for the relationship between:

- Fact.
- Claim.
- Inference.
- Hypothesis.
- Observation.
- Source.
- Evidence.
- User correction.

The objective is to resolve the domain ambiguity before changing persistent storage or production APIs.

## 3. BASELINE

Repository:
https://github.com/oahcom/AiMemoryBrainArchitecture

Last verified main:
c970c4a61b623c1f127624f60666b0a27e7e0594

R1 evidence:
https://github.com/oahcom/AiMemoryBrainArchitecture/issues/347#issuecomment-7036654407

Relevant Blob SHAs:

- epistemic-and-temporal-semantics.md: 8c03a20db1ed54c90db1d5c4c64f5ea7b1324ed7
- lifecycle-model.md: c1daa6225e75ea40d7f86e5ef6916b4f3849a1f8
- scope-and-permission-model.md: b5215ae27bd65a6c89c185b496f730b6cd52efa9
- memory-domain/src/lib.rs: 5d90a36d99b8be4ca4f3c8d5837b4e9830558842

Re-read all files at current main before deciding.

## 4. INVESTIGATION

Determine:

1. Whether Fact is an independently persistent domain entity.
2. Whether Claim is an attributed proposition.
3. Whether a Fact can be supported by multiple Claims.
4. Whether contradictory Claims can coexist.
5. How Inference references evidence.
6. How Hypothesis differs from unverified Claim.
7. How user corrections affect existing entities.
8. How temporal validity is represented.
9. How provenance is preserved.
10. How uncertainty and authorization remain separate.

Compare mature semantic and provenance models, including W3C PROV-O and relevant epistemic or temporal modeling approaches.

Do not import an external ontology wholesale without checking compatibility with existing Brain invariants.

## 5. DESIGN OPTIONS

At minimum compare:

A. Fact and Claim as distinct domain entities.

B. Claim as the canonical entity with verified Fact as a derived or qualified state.

C. A proposition-centric model with independent evidence and epistemic status.

For each, analyze:

- Persistence implications.
- Provenance.
- Contradiction.
- Temporal validity.
- Corrections.
- Forget.
- Retrieval.
- Backward compatibility.
- Migration cost.
- Query complexity.

Recommend the smallest model that preserves the required semantics.

## 6. REQUIRED OUTPUT

A. MQ-01 root-cause analysis.
B. Existing domain-model mapping.
C. Semantic glossary.
D. State-transition model.
E. Three-option comparison.
F. Recommended ADR.
G. Persistence impact.
H. API and compatibility impact.
I. Migration and rollback proposal.
J. Executable domain-test specification.
K. Adversarial contradiction and provenance cases.
L. Unresolved decisions.

Explicitly identify which parts of the decision can be made at the domain-model level and which require further governance or Owner decisions.

## 7. AUTHORITY

Do not modify main.

Do not change production schemas.

Do not appoint acceptance authority.

Do not treat the recommended ADR as an adopted standard.

Do not close MQ-01 based on design completion.

Do not claim tests passed unless actually run.

Formal Work Item registration must precede substantive R2 execution.

## 8. ACCEPTANCE

The ADR is acceptable only if:

1. All five epistemic categories are distinguished.
2. Provenance and authority are separate.
3. Contradictory claims can be represented safely.
4. Temporal validity is explicit.
5. User correction and Forget interactions are defined.
6. Three alternatives are compared.
7. Existing invariants are preserved or explicitly challenged.
8. Migration implications are documented.
9. Regression tests are reproducible.
10. Remaining governance decisions are explicit.

Next task: independent domain-model and epistemic-semantics review.
