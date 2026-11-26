# AID-2026-083 — Single authoritative Forget Fence decision
Authority: user-authorized operator (delegated by account owner)
Decision date: 2026-11-26
Repository: oahcom/AiMemoryBrainArchitecture
External evidence references: workflow AID-2026-11-26-FORGET-FENCE-01; Issues #1125 and #1211

Resolve the duplicate logical authority. D is the sole logical authority for ForgetOperation identity, typed canonical targets, source and derived-lineage coverage, Scope coverage, monotonic ForgetFence generation/cursor, canonical suppression and D-domain proof. Storage/Consistency owns physical durability, transaction/recovery mechanics and rebuildable storage projections; it does not issue a competing Forget decision, fence generation or cursor.

Decision clauses:
1. D's canonical ForgetFence contract is the sole authoritative logical source.
2. Namespace/partition is a scope attribute only; it cannot replace typed Memory/Version/source identity, Scope or transitive derived lineage.
3. Every Storage-local fence row is a derived, rebuildable projection of D's authoritative fence snapshot. It has no independent generation/cursor and cannot independently authorize reads or publication.
4. Physical persistence of D's authority may be implemented by Storage; physical location does not transfer logical authority.
5. A consumer unable to establish a current, correctly scoped, non-corrupt D snapshot fails closed for affected reads/publication.
6. Local suppression, D-domain completion, asynchronous cleanup and I-governed Global Forget Completion remain distinct outcomes.

PASS/FAIL:
FF-01 PASS iff exactly one logical issuer owns ForgetOperation and ForgetFence generation/cursor, namely D; otherwise FAIL.
FF-02 PASS iff Storage-local fence state is explicitly a rebuildable projection with no independent authority, sequence or cursor; otherwise FAIL.
FF-03 PASS iff the target model composes typed target, source identity, Scope and transitive derived lineage and does not use namespace as a substitute; otherwise FAIL.
FF-04 PASS iff stale, missing, corrupt or insufficiently scoped D authority blocks affected reads/publication; otherwise FAIL.
FF-05 PASS iff documents distinguish local suppression and D-domain proof from I-governed Global Forget Completion; otherwise FAIL.
FF-06 PASS iff EN and ZH-CN clauses are semantically equivalent and link the same canonical source; otherwise FAIL.
FF-07 PASS iff #1125 and #1211 receive this exact decision as comments and remain OPEN; otherwise FAIL.

This is a document-level direction decision, not implementation authorization, Owner acceptance, normative approval or production conformance. Modify only the listed D contract, System Boundaries source/mirrors and Work Item files/INDEX. No runtime/product code, tests, schemas, validator, workflows, deployment or production changes. Independent branch and Draft PR only; do not merge or close Issues.
