# G Claim/Fact Context Visibility Addendum

> Normative relationship:
> The normative requirements in this bilingual
> addendum are merged into the canonical root
> section `06-memory-context/context-versioning.md`
> §13.3.
>
> This file is the English synchronized counterpart,
> not an independent competing protocol.
>
> The root §13.3 controls in case of textual drift.
>
> Lineage: Phase 3.8.27 G Claim/Fact Context
> Visibility Addendum; AID-2026-014 R5 FLIP_TO_B.

## 1. Exact revision references

A ContextVersion referencing ClaimRevision, FactRevision or derived artifacts MUST bind exact immutable revision references and the applicable ForgetFenceCursor.

G MUST NOT substitute a current Claim head for a pinned ClaimRevisionRef.

## 2. Protected commit

G MUST:

1. Revalidate current I authorization.
2. Revalidate the applicable D Forget Fence.
3. Verify all referenced Claim/Fact revisions.
4. Verify complete dependency-registration receipts.
5. Verify exact Storage visibility outcome where applicable.
6. Commit the immutable ContextVersion through the protected visibility protocol.
7. Publish only after authoritative commit resolution.

G MUST verify that every successfully admitted
operation has a durably visible participant record
under the authoritative Fence/Admission boundary.

G MUST NOT commit or expose a ContextVersion while
the corresponding participant admission outcome
remains UNKNOWN or its participant record is
not durably visible.

G MUST NOT expose a new ContextVersion based only on a local pre-check followed by an independent unprotected head update.

## 3. Historical visibility

A ContextVersion committed before a later Forget does not grant perpetual access.

Historical Context reads and replay MUST re-evaluate current authorization and Forget suppression.

A forgotten ClaimRevision MUST NOT be disclosed through an existing FactRevision or historical ContextVersion.

## 4. UNKNOWN and recovery

UNKNOWN commit or lost acknowledgement MUST remain non-final.

Recovery MUST resolve the same operation and exact ContextVersion identity.

No retry may create duplicate visible ContextVersion state.

Recovery MUST use the original Operation identity
across Admission, Fence, Canonical Commit, E Publication,
Storage Visibility and G Context Commit.

A later Forget Fence MUST account for every durably
admitted participant and MUST record an auditable
completion or suppression disposition.

The B ordering and T17/T18 invariants are
mandatory for every G ContextVersion derived
from protected canonical Claim/Fact content.

G MUST NOT bypass an admitted participant's
Forget barrier.

The physical realization gate in root §13.3
remains applicable.

## 5. Storage boundary

The existing Storage L1 decision remains unchanged.

Storage L4 remains OPEN / NOT APPROVED.
