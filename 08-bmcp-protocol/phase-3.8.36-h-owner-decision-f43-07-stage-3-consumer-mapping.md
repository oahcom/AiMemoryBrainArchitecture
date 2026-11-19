# H Owner Decision — F-43-07 Stage 3 Consumer Mapping Independent Acceptance

- **Decision ID:** `H-OWNER-2026-11-20-001`
- **Finding:** F-43-07 — P1 — OPEN / BLOCKED pending A Integration
- **Disposition:** **ACCEPT WITH LIMITATIONS**
- **Work Item / authority:** AID-2026-012; Accountable Owner: H Owner
- **Prompt basis:** AI-EXEC-001 v1.1 + AI-EXEC-002 v1.1
- **H carrier branch:** `session-h-bmcp-protocol`
- **H pre-decision HEAD:** `d4fb6f199a9546ab48bbba2c6b926c92f27e7fc3`
- **Reviewed D decision:** `D-OWNER-2026-11-19-008`
- **Reviewed D commit:** `8fbef916785986fa1867ddf2eb3e3a5e4b366c5e`
- **Reviewed D file:** `08-bmcp-protocol/d-publication-storage-coc-participantref-mapping-boundary-1.0.md`
- **Reviewed D Blob:** `05a24f7eab663f66a3153d79adfab699b275f1a6`
- **D Owner #43 anchor:** `7022904207`
- **Stage 2 prerequisite:** `STORAGE-OWNER-2026-11-20-002` — ACCEPT WITH LIMITATIONS; A R43 review `A-OWNER-INTEGRATION-R43-2026-11-20`, #43 comment `7023454401`.

This is H's independent disposition of the H consumer-side interpretation of the exact D Blob above. It is not acceptance of D-owned or Storage-owned semantics on their behalf, and it does not decide any COC-owned schema, applicability, append, quorum, or canonical-copy rule.

## 1. Decision boundary

H **accepts with limitations** the D draft's core consumer mapping principle: the three participant references are distinct nominal identities, each issued and governed by its own authority and namespace; cross-domain relations are exact, typed evidence bindings, not identifier conversion or identity aliasing.

This acceptance applies only to the normative H consumption boundary for the exact D Blob. It does not mean that the proposed cross-domain mapping is already represented by a frozen H wire schema, that the necessary owner endpoints or proofs exist, or that a transaction is safe to publish/release in production.

## 2. Exact H semantic paths and binding rules

The following are semantic paths for H's consumer contract, not a claim that these names are already fields in an adopted JSON schema.

### 2.1 D Publication participant

Consume the D-owned record as one indivisible binding:

- `D.authority_id`
- `D.publication_participant_ledger_id`
- `D.publication_participant_ref`
- `D.entry_digest`
- `D.publication_operation_id`
- `D.canonical_publication_request_digest`
- `D.publication_tuple_digest`
- the D-owned immutable artifact/version/content, dependency-set, scope and source/target-lineage digests required by the D record.

H treats `D.publication_participant_ref` as an opaque D-local locator and `D.entry_digest` as the digest of that exact immutable D entry. Neither field alone is a valid binding. H MUST authenticate the D authority and namespace and verify that the ref, digest and operation tuple are bound together by D-issued evidence.

### 2.2 Storage visibility participant

Consume the Storage-owned record independently:

- `Storage.authority_id`
- `Storage.storage_visibility_participant_ledger_id`
- `Storage.storage_visibility_participant_ref`
- `Storage.participant_digest`
- `Storage.publication_operation_id`
- `Storage.publication_tuple_digest`
- `Storage.artifact_version` and `Storage.artifact_content_digest`
- `Storage.state` and `Storage.state_version`
- `Storage.database_incarnation_id`
- `Storage.durable_prepare_receipt.ref` and `Storage.durable_prepare_receipt.digest`.

The prepare receipt consumed under D §§2.2/3.1/6.1 is the receipt for the exact StorageVisibilityParticipantRef in PREPARED_HIDDEN. It MUST NOT be conflated with the separate F-43-06A RecoveryJoinProof identity/bytes/digest/receipt. H accepts Storage Stage 2 limitation 1 as binding interpretation.

H MUST NOT mint, rename, rewrite, infer or substitute a Storage ref, digest, namespace, receipt or state. Storage authority must authenticate its own evidence and incarnation.

### 2.3 COC participant intent (conditional)

Only when COC's own authoritative applicability decision says the COC join is required, consume:

- `COC.authority_id`
- `COC.participant_ledger_id` / quorum-log identity
- `COC.participant_intent_ref`
- `COC.intent_digest`
- `COC.transaction_identity` and `COC.request_digest`
- `COC.participant_tuple_digest`
- `COC.append_position_or_term` (opaque COC-local cursor)
- `COC.quorum_receipt.ref` and `COC.quorum_receipt.digest`
- the COC-authenticated member bindings containing the exact D ref+entry digest+authority/ledger and exact Storage ref+participant digest+authority/ledger, plus the shared operation/request/tuple correlation digests.

H accepts no COC applicability enum, quorum algorithm, threshold, participant cardinality, append linearization or physical implementation as decided by D or Storage. The field paths above describe the evidence H needs to consume if COC supplies an accepted authoritative contract; they do not impose a schema on COC.

## 3. Identity, operation and evidence validation

1. The D, Storage and COC refs are three distinct nominal types. Equal strings, similar field names, equal operation IDs, equal tuple digests, a shared database, a common transport envelope or matching transaction IDs do not establish identity equality or commit.
2. `PublicationOperationId`, canonical request digest and publication tuple digest are correlation anchors only. H verifies the full immutable operation tuple and each authority-local ref+digest independently.
3. Each receipt/proof must authenticate its issuing authority and bind its own namespace, exact ref, exact digest, immutable operation identity, applicable state/version and incarnation/cursor. H also verifies member-level inclusion/consistency for a required COC join.
4. A Storage receipt proves only the Storage fact it names; a D admission receipt proves only D admission; a COC quorum receipt proves only the COC append/commit fact within COC's accepted proof semantics. No receipt crosses authority boundaries.
5. Ref-only, digest-only, count-only, transaction-ID-only, transport ACK, cached response or caller assertion is insufficient. Missing, unresolvable or contradictory binding members cannot be completed by H inference.

## 4. Currentness versus lifecycle status

H separates two axes:

- **Identity/currentness:** whether the exact authority, namespace/incarnation, immutable ref+digest and operation binding are still the authoritative current record/proof for the requested read point.
- **Lifecycle status:** the owner-issued state of that record (for example Storage PREPARED_HIDDEN, D admitted/unresolved or an owner-defined terminal state, and COC applicability/intent lifecycle when COC applies).

`CURRENT` means only that the exact identity/evidence is current under the issuing authority's currentness contract. It MUST NOT be interpreted as `ACTIVE`, PREPARED, COMMITTED, VISIBLE, quorum-appended, release-eligible, or authorization granted. Likewise, a lifecycle label cannot repair stale or unverified identity evidence.

H MUST preserve owner-local status vocabularies. It MUST NOT compare D admission positions/fence generations with Storage transaction/commit positions or COC append positions/terms, nor coerce one owner's recovery enum into another owner's enum. H consumer acceptance is a third, independent decision axis and is not an owner lifecycle state.

## 5. Required H classifications and fail-closed behavior

| Condition | H classification | Required consumer behavior |
|---|---|---|
| Exact, authenticated, current ref+digest and operation tuple; all required owner proofs verified | ACCEPTED EVIDENCE (for the named fact only) | Continue only within the specific H consumer operation and its independently authorized policy |
| Stale authority epoch, namespace/incarnation, record version, proof, or superseded artifact pin | STALE / BLOCKED | Reject as current evidence; refresh from the owning authority. Never fall back to cache or a newer/different identity |
| Invalid authentication, digest mismatch, ref/digest mismatch, changed immutable tuple, contradictory owner proofs, or conflicting terminal outcomes | INTEGRITY_CONFLICT | Fail closed; quarantine conflicting observations and preserve them for owner investigation; do not overwrite or repair the original record |
| Owner cannot establish commit, non-commit, applicability, currentness or complete readback | UNKNOWN / BLOCKED | No publish, no visibility inference, no terminalization, no barrier release, no authorization |
| Required receipt absent, unavailable, unresolvable or not bound to the exact record | UNKNOWN / BLOCKED | Treat as missing proof, not as proof of absence or abort |
| COC ParticipantIntentRef absent and no authenticated COC NOT_REQUIRED proof | UNKNOWN / BLOCKED | Do not infer COC is out of scope and do not accept the D/Storage pair as a complete cross-domain join |
| Authenticated COC NOT_REQUIRED proof valid for the exact operation/scope/version | COC not applicable (COC fact only) | Omit the COC intent branch only for that proven scope; retain D and Storage evidence requirements |
| Required COC join, but exact intent/member binding or quorum proof unavailable | UNKNOWN / BLOCKED | Do not treat D or Storage receipts as a substitute for COC append/quorum evidence |

A positive H mapping result is not a release decision. Each owner retains its own release predicate and barrier authority.

## 6. Retry, replay, changed digest and crash/recovery

- **Exact retry, same authority-local identity and complete immutable digest:** resolve the original record and return/consume the original ref+digest and original receipt/proof. Do not mint a replacement ref because an ACK was lost.
- **Same PublicationOperationId or owner-local identity, changed request/tuple/artifact/dependency/scope/lineage/participant binding digest:** classify as immutable identity conflict / INTEGRITY_CONFLICT. Never overwrite, rebind or silently fork the original record.
- **Replay of a terminal operation:** accept only the original terminal receipt/proof for the exact identity and digest. A second, conflicting terminal result is quarantined as INTEGRITY_CONFLICT.
- **Duplicate COC append:** COC's own accepted idempotency/uniqueness rule must resolve whether the request is the original append. H does not decide COC duplicate semantics. Until COC returns the exact original intent and quorum proof, remain UNKNOWN/BLOCKED.
- **Lost ACK / delayed response:** ACK loss or timeout is not abort, no-effect, non-commit or permission to create a new identity. Reconcile against the owning authority using the same identity.
- **Crash after Storage prepare but before receipt delivery:** Storage must return the original exact PREPARED_HIDDEN ref+digest and prepare receipt; H remains UNKNOWN/BLOCKED until authenticated readback succeeds.
- **Crash after D admission:** D's participant remains unresolved until D supplies its authoritative current record and required Storage terminal evidence; H does not infer terminality or release.
- **Crash after required COC append but before quorum receipt delivery:** COC must resolve the original intent and return its original quorum proof; H must not infer append from D admission or create a second logical participant.
- **Crash after Storage visibility commit but before D/COC closeout:** each owner independently reconciles its own record. Missing closeout ACK does not undo a Storage commit, but does not let H mark D/COC terminal or release their barriers.
- **Restore, rollback, stale incarnation, forked quorum history or broken ledger continuity:** UNKNOWN/BLOCKED unless the owning authority proves continuity and exact identity; contradictory digest/history is INTEGRITY_CONFLICT. Wall clock, timeout, process death, missing row, cached VALID or a single non-linearizable absent read is never proof of abort/no-effect.

## 7. Stage 2 limitations and required owner follow-up

H incorporates the five A-confirmed Stage 2 boundaries recorded in A R43 #43 comment 7023454401:

1. Storage PREPARED_HIDDEN participant prepare receipt is distinct from the F-43-06A RecoveryJoinProof durable receipt.
2. COC alone owns quorum algorithm/threshold, ParticipantIntent schema/cardinality and applicability.
3. Storage owns canonical RecoveryJoinProof bytes; COC owns its quorum-committed binding envelope, not a competing canonical content copy.
4. COC applicability remains unresolved until COC supplies its own authoritative decision/proof.
5. H consumer mapping/currentness is H-owned; this decision supplies that H design-level disposition only.

### D / Storage modification assessment

- **No D or Storage successor is required solely for H's acceptance of this exact D Blob.** A R43 records that no D successor is mandatory solely to satisfy Storage Stage 2 on this exact Blob.
- D §§3.2, 5.3, 6 and 8.2 remain conditional COC proposals. They must be read as requiring COC's own applicability and append/quorum authority; H does not adopt their proposed COC enums as a COC schema. COC must independently accept them or publish an authoritative equivalent, including scope/version binding and exact member-level proof.
- D §§2.2, 3.1 and 6.1 must retain the Storage participant PREPARED_HIDDEN receipt meaning and must not merge it with RecoveryJoinProof receipt semantics. Storage Stage 2 limitation 1 governs.
- If a later D/Storage revision changes any exact ref, digest, authority/namespace, receipt type, operation binding, canonical-copy rule or recovery guarantee, this H decision does not transfer; affected Owners must re-review the successor's exact Commit/Blob.
- If the parties later choose to encode these semantic paths in a concrete H wire/schema contract, that requires a separate H-owned schema/version decision and exact compatibility review. This document does not define or freeze such a schema.

## 8. Explicit non-grants and remaining gates

This decision does **not** grant:
- H wire/schema freeze or adoption;
- production release, deployment, visibility activation or authorization to consume unverified evidence;
- Runtime implementation or Runtime conformance;
- acceptance of Storage durability/atomicity/receipt semantics on Storage's behalf;
- acceptance of COC applicability, participant cardinality, quorum, append or canonical-copy semantics on COC's behalf;
- A Integration approval or Finding closure.

No tests, live endpoints, production receipts, real COC quorum, runtime execution or production conformance are claimed by this normative review.

**F-43-07 remains OPEN / BLOCKED** pending COC's independent authority disposition where applicable, D/Storage/H same-exact-version decisions and A's final cross-domain integration ruling.
