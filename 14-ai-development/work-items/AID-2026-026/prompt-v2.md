# WORK ITEM: PROPOSED AID-2026-026 — PROMPT v2
# Inference and Hypothesis Semantic Boundary
# Forget Interaction and AID-2026-023 Interface
# REQ-07

## 0. VERSION AND SUPERSESSION

This is prompt v2.

It supersedes prompt v1, which scoped a Fact/Claim semantic adjudication.
That surface is owned by AID-2026-014 and must not be re-adjudicated here.

| version | status | execution basis |
|---|---|---|
| v1 | `FROZEN`, `superseded_by: scope_revision_v2` | no |
| v2 | this document | yes, once R2 is authorised |

v1's SHA-256 and byte count are unchanged in the manifest. v1 is preserved as
history, not overwritten. Do not treat v1 as the current instruction.

## 1. IDENTITY AND ROLE

You are a Domain Architecture Designer working on epistemic status modeling.

Primary requirement:
REQ-07 — Issue #347
https://github.com/oahcom/AiMemoryBrainArchitecture/issues/347

Coordination hub:
https://github.com/oahcom/AiMemoryBrainArchitecture/issues/345

Work Item: AID-2026-026.

## 2. WHAT THIS WORK ITEM OWNS — AND WHAT IT DOES NOT

**Owned here:**

- The semantic boundary between Inference and Hypothesis, and their distinction
  from each other, from Claim, and from an unidentified assertion.
- The identity rule for Inference and Hypothesis. If they are persisted types,
  what makes two of them the same one. If they are derived, what they are
  derived from.
- What must be invalidated in Inference/Hypothesis state when a supporting Claim
  or Evidence is forgotten, and what may survive a Forget operation.
- The interface contract this Work Item consumes from AID-2026-023: identifiers,
  invalidation signals, and completion acknowledgement.
- Contradiction and supersession behaviour for Inference and Hypothesis only,
  where AID-2026-014 has not already ruled.

**Owned by AID-2026-014 — cite, do not re-derive:**

| surface | owner |
|---|---|
| Fact and Claim basic semantics | AID-2026-014 |
| Whether Fact is an independently persistent entity | AID-2026-014 |
| Claim Identity and Claim Revision | AID-2026-014 |
| Evidence binding and historical immutability | AID-2026-014 |
| Fact Attestation authorisation | AID-2026-014 |
| Storage atomicity for Claim/Fact revision | AID-2026-014 |

A citation is not an adjudication. Where this Work Item needs a Fact/Claim rule,
reference AID-2026-014's ADR by identifier and use its conclusion as given.

Do not create a competing ADR for anything AID-2026-014 has decided. If you
believe AID-2026-014's ruling is wrong, record that as a finding against
AID-2026-014 — do not silently decide it differently here.

**Owned by AID-2026-023 — consume, do not redefine:**

Canonical Forget authorisation, propagation, denial, retention, and completion
rules. This Work Item specifies what Inference/Hypothesis needs from Forget, not
how Forget works.

## 3. BASELINE

Repository:
https://github.com/oahcom/AiMemoryBrainArchitecture

Re-read every referenced file at current `main` before deciding. Blob SHAs from
prior rounds are evidence of what was read then, not of what exists now.

Relevant normative sources (verify at HEAD, do not trust these pins blindly):

- `02-domain-model/epistemic-and-temporal-semantics.md`
- `02-domain-model/lifecycle-model.md`
- `02-domain-model/scope-and-permission-model.md`
- `crates/memory-domain/src/lib.rs`

Relevant prior art in this repository:

- AID-2026-014 manifest and its ADR (the Fact/Claim owner)
- AID-2026-023 manifest (the Forget boundary)
- `reviews/` for any prior epistemic-status analysis

State plainly which of these you actually read at which commit.

## 4. INVESTIGATION

Answer these, and mark each answer `DERIVED_FROM_SOURCE`, `INFERRED`, or
`UNDECIDED`:

1. Is Inference currently a distinct type, a status value on Claim, or absent?
2. Is Hypothesis currently a distinct type, a status value on Claim, or absent?
3. What is the operational difference between an Inference and a Hypothesis as
   the existing model uses those words? If the model does not distinguish them,
   say so rather than inventing a distinction.
4. Can an Inference exist without a supporting Claim or Evidence? What does the
   existing model require?
5. Can a Hypothesis be promoted to Claim, or is it a terminal classification?
6. What does the existing Forget model invalidate today, and does it reach
   Inference/Hypothesis at all?
7. If Inference/Hypothesis are derived rather than persisted, what is the
   derivation input, and what happens to the derivation when an input is
   forgotten?
8. Where AID-2026-014 has ruled on a neighbouring concept, what exactly did it
   rule, and does this Work Item's answer contradict it?

For each answer, cite the file and the specific section. "The model supports X"
without a citation is not an answer.

## 5. DESIGN OPTIONS

Compare at minimum:

A. **Inference and Hypothesis as distinct persisted entities**, with their own
   identity and lifecycle.

B. **Inference and Hypothesis as epistemic status values on Claim**, with no
   separate identity.

C. **Inference and Hypothesis as derived annotations**, recomputed from
   supporting Claims and Evidence rather than stored.

For each option, analyse:

- Identity: what makes two of them the same one.
- Persistence: what is stored, what is recomputed.
- Forget interaction: what must be invalidated, what may survive, and what
  happens to a derived annotation when its input disappears.
- Contradiction and supersession.
- Retrieval and query cost.
- Backward compatibility with the current model.
- Migration cost from the current state.

Recommend the smallest option that preserves required semantics. If the smallest
option is "the current model is already correct and only needs documenting," say
that — do not manufacture a change to justify the Work Item.

## 6. FORGET INTERACTION — EXPLICIT REQUIREMENT

This is the part most likely to be wrong, so it needs its own analysis.

For each of the three options:

- When a supporting Claim is forgotten, what happens to an Inference built on it?
- When supporting Evidence is forgotten, same question.
- When a Claim is forgotten but the Inference also had other support, does the
  Inference survive with reduced support, or is it invalidated?
- What signal does AID-2026-023 provide that an Inference's support has been
  forgotten? If no such signal exists, that is the interface gap to specify.
- How does this Work Item know Forget completed, so that it does not serve an
  Inference whose support is already gone?

A design that leaves an Inference readable after its only support was forgotten
is a data-safety defect, not a modelling preference. Say so if you find it.

## 7. REQUIRED OUTPUT

A. Current-state mapping: what the model actually has today, with citations.
B. Inference/Hypothesis boundary definition, with the distinction justified or
   explicitly declared absent.
C. Identity rule for each.
D. Three-option comparison.
E. Recommended option, with the smallest-model argument.
F. Forget interaction specification, per §6.
G. AID-2026-023 interface contract: signals consumed, signals expected,
   acknowledgement.
H. AID-2026-014 citation list: every Fact/Claim rule relied on, by identifier.
I. Contradiction and supersession behaviour for Inference/Hypothesis.
J. Executable domain-test specification.
K. Unresolved decisions, each with who must decide.
L. Explicit list of what this Work Item did not decide because AID-2026-014 owns
   it.

## 8. AUTHORITY

Do not modify `main`.

Do not change production schemas or DDL.

Do not appoint acceptance authority, sponsor, or accountable owner.

Do not treat the recommended ADR as an adopted standard.

Do not close MQ-01 on the basis of design completion.

Do not claim tests passed unless actually run. If a test was run against an
excerpt rather than the repository module graph, record
`NOT_VERIFIED_AT_REPOSITORY_SCOPE` — a fragment-level pass is not a
repository-level pass.

Do not re-adjudicate anything AID-2026-014 owns.

Formal Work Item registration and R2 authorisation must both precede substantive
R2 execution. Neither is implied by this prompt existing.

## 9. ACCEPTANCE

The ADR is acceptable only if:

1. Inference and Hypothesis are each either clearly distinguished, or the
   absence of a distinction is argued from the source rather than assumed.
2. The identity rule is stated for each, and is decidable — two readers applying
   it reach the same answer.
3. Three options are compared on the axes in §5.
4. The Forget interaction is specified per §6, including the case where support
   is partially forgotten.
5. The AID-2026-023 interface contract names the actual signals, not a
   description of what signals would be nice.
6. Every Fact/Claim rule relied on is cited to AID-2026-014 by identifier.
7. No Fact/Claim rule is re-decided here.
8. Existing invariants are preserved or explicitly challenged with reasons.
9. Test specifications are executable, not prose descriptions of tests.
10. Remaining governance decisions are listed with the role that must make them.

## 10. NEXT TASK

Independent domain review of the Inference/Hypothesis boundary and the Forget
interaction specification. That review is a separate session and a separate
Work Item; it is not this prompt's deliverable.
