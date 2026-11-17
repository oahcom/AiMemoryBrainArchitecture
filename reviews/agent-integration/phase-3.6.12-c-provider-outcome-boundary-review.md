# C — Provider Outcome Boundary Review Against Unified Schema 1.2.5

- Owner perspective: C — Agent Integration / Provider Boundary
- Status: **CONDITIONAL ACCEPTANCE — C OWNER ARTIFACT PIN AND PROVIDER-SPECIFIC VECTORS REQUIRED**
- Reviewed H schema: `08-bmcp-protocol/schemas/bmcp.coc-jf10-unified-1.2.5.schema.json`
- Exact schema blob: `164ec3c436558d5d93032edc51e127d15e03db4d`
- Reviewed Storage COC protocol: `reviews/storage-consistency/phase-3.6.3-coc-durable-log-and-recovery-protocol.md`
- Exact Storage COC blob: `5b950a3a29bd7a5276b92a49a9114d700718b987`

## 1. Decision

**ACCEPT WITH ENUMERATED AMENDMENTS** for the cross-protocol Provider Outcome boundary. C's own canonical Provider Outcome source artifact was not located and pinned in this pass; therefore this is not a final exact-version C Owner decision and must not be represented as such.

## 2. Required outcome semantics

The schema's exact wire enum is:
`HANDOFF_ACCEPTED | HANDOFF_REJECTED | NOT_INVOKED | UNKNOWN | IN_DOUBT`.

C must preserve these semantics:
- `HANDOFF_ACCEPTED`: actual handoff to the identified provider for the exact final request is proven. It does not prove durable downstream visibility or global completion.
- `HANDOFF_REJECTED`: authoritative provider rejection for the exact request. It is not automatically equivalent to NOT_INVOKED; if a side effect may have occurred, preserve UNKNOWN/IN_DOUBT.
- `NOT_INVOKED`: requires authoritative proof that no provider handoff occurred. Missing request row, timeout, lost ACK, worker crash or empty queue is insufficient.
- `UNKNOWN` / `IN_DOUBT`: nonterminal and non-expiring. Preserve attempt identity and evidence; no retry-as-new-operation or success inference.

## 3. Exact evidence binding

Every CSubmitOutcome must bind, without substitution:
- CSubmitOutcomeRef and canonical digest;
- ProviderRef, ProviderAdapterRef and ProviderIdempotencyKeyRef;
- ProviderRequestRef / ProviderReceiptRef when applicable;
- final request boundary identity and RequestDigest;
- TransactionRef and applicable participant/reservation/prepare attempt/participant ledger tuple;
- C owner admission identity/digest, owner ledger/version/sequence/high-water/root;
- exact COC ParticipantIntentRef or explicit null plus non-empty COC absence reason;
- C-authored provider outcome evidence, or authoritative no-handoff/not-invoked proof, or explicit unknown reason.

C alone creates CSubmitOutcome. Storage, I, D, COC and H may validate or reference it but cannot synthesize it.

## 4. Batch / Manifest gate interaction

Storage COC §§17.1–17.7 correctly require C reservation/provider-attempt/provider-outcome high-waters in the frozen C admission ledger and include applicable owner-local admissions in the canonical union manifest even when no COC ParticipantIntentRef exists.

C must keep provider invocation/retry closed after Batch commit and after Manifest commit until exact S4 pair readback is complete and semantically joined. A COC ACK, batch membership, manifest membership, Storage resolution, I terminality or D clearance is not Provider Outcome evidence.

After a possible handoff, recovery uses same-key authoritative provider lookup/idempotency. If the provider cannot authoritatively resolve the outcome, preserve UNKNOWN/IN_DOUBT and keep affected gates closed. Provider-specific same-key behavior is an activation prerequisite; do not claim universal exactly-once semantics.

## 5. Required C amendments / evidence

1. Pin the canonical C Provider Outcome contract and CSubmitOutcome schema/adapter contract by exact path, commit and blob.
2. Define per-provider proof semantics for accepted, rejected, not-invoked, unknown and in-doubt outcomes, including whether rejection can follow a side effect.
3. Supply race vectors: gate close vs provider handoff; handoff vs timeout/ACK loss; Batch vs Manifest commit; pair readback vs retry; provider lookup vs concurrent retry.
4. Prove same-key lookup behavior and idempotency scope for each provider adapter; otherwise classify uncertain handoff as IN_DOUBT.
5. Bind all outcomes to the same immutable final request boundary and request digest; a changed payload requires a new attempt identity and must conflict with prior identity.
6. Provide signed evidence verification and append-only enrichment rules. Late provider receipt/lookup evidence may enrich an outcome but must not rewrite the original attempt identity.

## 6. Review boundary

The Storage COC and H schema artifacts were fetched and inspected. The C-specific canonical artifact was not recovered; the above is a protocol-boundary assessment only. This role-simulated report is not an independent human Owner signature. No provider sandbox, executable adapter test, exactly-once guarantee, implementation conformance or production activation is claimed.
