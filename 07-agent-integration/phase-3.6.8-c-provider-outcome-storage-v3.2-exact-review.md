# Phase 3.6.8 — C Exact-Version Review: Provider Outcome Across Storage v3.2 Recovery Cutoff

- Owner perspective: C — Agent Integration / Provider Side-Effect Boundary
- Status: **ACCEPT WITH ENUMERATED C-OWNED EXCEPTIONS — DESIGN REVIEW ONLY**
- Reviewed Storage v3.2 Blob: `e7ab80cdf8af5e0d50c407b06a5deb618d1e2ae6`
- Reviewed companion COC/PostgreSQL §14 Blob: `8ac17816476f280ab6fb3afca0688aa03e37de1d`
- C source contract Blob: `45a48249717c8cddb07ab96197730ef93d406c22`
- I Phase 3.6.8 proposal Blob: `929b30ba10ac627927d3959e0777b467846b268d`
- D Phase 3.6.8 proposal Blob: `0668667daeb936bf223ab049277ea2a4117c3b09`
- Project phase: ARCHITECTURE DESIGN; NOT IMPLEMENTED / NOT VERIFIED

## 1. C authority boundary and decision

**C DECISION: ACCEPT WITH ENUMERATED C-OWNED EXCEPTIONS**, limited to C's authenticated final-request boundary, provider invocation, provider idempotency namespace and actual provider outcome evidence.

C accepts the v3.2 order as a required recovery safety barrier:
1. owner-local C side-effect admission closes and freezes C's admitted participant/provider-outcome inventory;
2. COC quorum prefix P and the I/D/C owner snapshots are frozen;
3. the canonical Participant Manifest payload is constructed against P;
4. `COC_RECOVERY_CUTOFF_BATCH` is quorum committed and binds ManifestId/Digest/count;
5. the separate `PARTICIPANT_SET_RECONCILIATION` / Manifest Record is quorum committed and binds the exact preceding Batch position/digest;
6. both records are linearly read back and all cross-bindings verified;
7. only then may participant-specific recovery/reconciliation begin.

C confirms the key negative condition: **S2 Batch commit alone is not permission to invoke/retry a provider, and S3 Manifest commit without S4 read-back is also insufficient.** The C provider gate remains closed until S4 succeeds and all participant-specific I/D/Storage predicates are independently validated. This is an outage/recovery gate, not a new authorization decision.

## 2. Provider Outcome is an independent C-owned fact

C alone creates `CSubmitOutcome` from the actual provider/runtime boundary observation. It is not derivable from:
- I `COMMIT_WON`, authorization receipt consumption or PermissionEpoch;
- D clearance, ForgetFence or barrier status;
- Storage `PreparedParticipantReceipt`, same-XID COMMITTED result or `PublicationReceipt`;
- COC Batch/Manifest commit, participant reservation or coordinator status;
- H transport ACK, message delivery or schema validation;
- G Applied / current-use state.

The outcome describes provider handoff only. It MUST NOT be interpreted as model-result correctness, user-visible delivery, G Applied or global completion.

### 2.1 Required immutable CSubmitOutcome tuple

Each C outcome record MUST bind:
- `CSubmitOutcomeRef`, immutable outcome ID, outcome generation and canonical outcome digest;
- authenticated C authority/issuer, provider adapter identity/version and protected runtime boundary;
- `CausalOrderCoordinatorRef`, domain, TransactionRef and exact ParticipantIntentRef;
- exact `ParticipantReservationRef` and reservation position/digest;
- provider identity/endpoint profile and stable provider idempotency-key reference (secret key material is never logged);
- provider request/reference ID and authoritative same-key lookup/query reference;
- exact final request digest, canonicalization profile and `FinalRequestBoundaryId`;
- actual provider receipt reference/digest when returned;
- actual `InferenceRequestId` when returned; absence is explicit and cannot be fabricated;
- exact PreparedParticipantRef/GID/DatabaseIncarnationRef/PrepareAttemptRef+Generation/ParticipantLedgerRef+Version/ParticipantTupleDigest when the provider operation is JF-10 coupled;
- exact I terminal decision ref/digest and I sequencer position;
- exact D clearance/fence/barrier tuple applicable to the request;
- Storage resolution / PublicationReceipt references when applicable, kept distinct from provider handoff;
- outcome enum, evidence source, observation boundary and trusted receiver/owner sequence; wall-clock is audit metadata only.

C outcome evidence is append-only. A later provider lookup enriches/reconciles the same CSubmitOutcome lineage; it does not rewrite the original observation or mint a new provider idempotency identity.

### 2.2 Terminal vocabulary and evidence

The C-owned provider outcome vocabulary is:
- `HANDOFF_ACCEPTED`: provider acceptance/handoff is authoritatively established for the exact final request and same idempotency key; bind actual provider receipt and provider request identity where the provider supplies them.
- `HANDOFF_REJECTED`: definitive evidence establishes that the provider did not accept/receive the protected request. A local validation error before provider invocation is a distinct `NOT_INVOKED` disposition and is not a provider rejection.
- `UNKNOWN` / `IN_DOUBT`: timeout, process death, lost response, contradictory receipt, ambiguous provider acceptance, unavailable same-key lookup or inability to prove whether handoff occurred.

Only the first two are terminal provider-boundary outcomes. UNKNOWN is durable, non-expiring and blocking. A missing provider receipt is not by itself proof of rejection; a local HTTP error is not proof of no handoff unless the adapter/provider contract proves that property.

### 2.3 Invocation and retry gate

For a new protected provider invocation, C MUST require:
1. exact quorum-committed COC participant intent and required Storage prepared participant registration;
2. I authoritative `COMMIT_WON` for the exact complete participant/attempt/ledger tuple and single-use receipt consumption;
3. D's current lineage-bound admission/clearance evidence and applicable ForgetFence check;
4. current C reservation and final-request digest/boundary;
5. COC availability and a current, verified recovery state.

If recovery is in progress, C additionally requires the exact Batch + Manifest Record pair and S4 linearizable read-back. A Batch alone, a staged Manifest payload, or a Manifest Record not yet read back never permits provider invocation.

For a previously invoked operation with UNKNOWN outcome, after S4 C may query/reconcile only the same provider idempotency key and same immutable request/participant tuple. It MUST NOT retry as a new transaction, allocate a new XID, change request digest, or mint a replacement key. A repeat invocation using the same key is allowed only if the provider-specific contract proves idempotent same-key semantics and the query result remains authoritative. Otherwise preserve UNKNOWN and hold I/D barriers.

### 2.4 C snapshot completeness

C's owner-local cutoff attestation must enumerate all C-owned admitted provider operations, including:
- reserved but not invoked;
- invocation started with ACK/response missing;
- provider accepted/rejected but CSubmitOutcome persistence/COC append delayed;
- same-key lookup pending;
- worker restarted, retry queued, or outcome evidence contradictory;
- terminal outcome known locally but not durably reflected in C's owner ledger.

The attestation binds C GateGeneration, C request/outcome high-water, canonical member count/root, provider idempotency-key references, and per-member state. Empty set is an explicit attested empty array; missing C inventory is not empty. Any late-discovered pre-cutoff invocation reopens C reconciliation and invalidates the prior C snapshot. A post-high-water request remains blocked or belongs to a subsequent cutoff.

## 3. C ↔ Storage v3.2 review findings

| Finding | C disposition | Required invariant |
|---|---|---|
| S0 owner freeze and prefix P | ACCEPT | C gate closure and C provider-outcome inventory are frozen before batch construction |
| S1 manifest payload | ACCEPT | Every pre-P C participant is represented; manifest staging is not a commit or permission |
| S2 Batch commit | ACCEPT | Batch binds exact C snapshot and ManifestDigest; S2 alone cannot start provider recovery |
| S3 Manifest Record | ACCEPT | Record references exact committed Batch; payload digest/count/member set match |
| S4 linearizable read-back | ACCEPT | Both exact records and all owner generations are current before any provider lookup/retry or participant recovery |
| crash after S2 | ACCEPT | Remain fenced; resume same BatchId/ManifestId/Digest and append only the missing Manifest Record |
| unknown provider result | ACCEPT WITH C CONDITION | Same-key authoritative query only; never retry as new operation; no terminal inference |
| later C high-water / late discovery | ACCEPT WITH C CONDITION | Reopen C snapshot/reconciliation; no silent merge into old batch |

No C-owned evidence permits C to release I's Gate, D's Forget Fence, Storage locks, COC RecoveryEpoch or G Applied.

## 4. C-owned exceptions and required evidence

1. **Provider-specific idempotency remains unresolved until proven per provider.** Generic exactly-once semantics are not assumed. Each production adapter needs a documented same-key lookup/retry contract, provider receipt semantics and crash/failover recovery proof.
2. **Outcome persistence must be durable before C reports terminality.** A provider response observed only in volatile memory is not a durable CSubmitOutcome. If process death can occur between provider handoff and C outcome persistence, the same provider key must support authoritative recovery or the outcome remains UNKNOWN.
3. **Provider acceptance is not model completion.** `HANDOFF_ACCEPTED` means the provider accepted/handoff was established, not that inference completed, content is correct, or user received it.
4. **C does not define H wire bytes.** H must schema-map every CSubmitOutcome field and preserve typed references/digests; C verifies semantic tuple equality at its own boundary.
5. **Runtime tests remain NOT RUN.** C-CO-01..10 and provider-specific crash/duplicate/timeout/failover tests remain specified, not passed.

## 5. Required negative and positive C cases — specified, not executed

- C-PO-01: reject provider invocation after S2 Batch but before S3 Manifest Record.
- C-PO-02: reject provider invocation after S3 but before S4 read-back.
- C-PO-03: accept S4 only when BatchPosition < ManifestRecordPosition and all digests/counts/P/RecoveryEpoch match.
- C-PO-04: provider ACCEPTED requires authoritative same-key evidence and exact request/final-boundary binding.
- C-PO-05: provider REJECTED requires definitive no-handoff proof; local pre-invocation failure maps to NOT_INVOKED.
- C-PO-06: timeout/lost ACK/process death remains UNKNOWN; no retry-as-new-operation.
- C-PO-07: same-key recovery returns original provider outcome and same CSubmitOutcome lineage.
- C-PO-08: same idempotency key with changed request digest/participant tuple is CONFLICT.
- C-PO-09: late pre-cutoff C participant reopens C snapshot and blocks release.
- C-PO-10: C outcome never implies Storage publication, G Applied or Forget completion.

**Disposition:** C accepts the Storage v3.2 recovery ordering and Provider Outcome semantic contract with the enumerated C-owned exceptions. This is a role-based exact-version design review, not provider-vendor approval, independent human Owner signature, implementation PASS, interoperability result or production authorization.

## 6. Provenance

Assistant-authored role-based C review proposal committed at the user's direction. It is not a cryptographic signature and does not prove independent human C Owner authorship or approval.
