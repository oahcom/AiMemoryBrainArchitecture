# G Claim/Fact Context Visibility Addendum

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

G MUST NOT expose a new ContextVersion based only on a local pre-check followed by an independent unprotected head update.

## 3. Historical visibility

A ContextVersion committed before a later Forget does not grant perpetual access.

Historical Context reads and replay MUST re-evaluate current authorization and Forget suppression.

A forgotten ClaimRevision MUST NOT be disclosed through an existing FactRevision or historical ContextVersion.

## 4. UNKNOWN and recovery

UNKNOWN commit or lost acknowledgement MUST remain non-final.

Recovery MUST resolve the same operation and exact ContextVersion identity.

No retry may create duplicate visible ContextVersion state.

## 5. Storage boundary

The existing Storage L1 decision remains unchanged.

Storage L4 remains OPEN / NOT APPROVED.
