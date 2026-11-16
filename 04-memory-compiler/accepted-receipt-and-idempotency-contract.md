# Accepted Receipt and Idempotency Contract

**Status:** CANDIDATE — E-owned semantics; storage realization and cross-module envelope remain OPEN pending Storage/Consistency, H and I approval.  
**Owner:** Session E — Memory Compiler.  
**Integration:** INT-P1-03, INT-P1-04, INT-P1-06, INT-X-01, INT-X-06.  
**Authority boundary:** E owns ingress durability and compile intent. D owns canonical commit/cursor. F owns index publication/watermark. H owns wire envelope and authenticated transport. I owns identity, authorization, retention and audit policy.

## 1. Normative state distinctions

These are separate milestones, not aliases and not a single success flag.

| State | Meaning | Authority / evidence |
|---|---|---|
| Received | Request bytes/envelope reached an ingress process; may be volatile | No durability promise |
| Accepted | Immutable source Event reference, payload reference/digest, idempotency receipt and compile intent are durably recoverable | E receipt lookup returns stable receipt; acceptance transaction committed |
| Processed | A worker completed the configured source decode/validation and recorded its stage result | E stage journal |
| Compiled | A versioned ExtractionIR/candidate bundle and its lineage were durably recorded | E compilation journal and provenance refs |
| CanonicalCommitted | D confirmed the canonical write and returned its authoritative commit/version reference | D response/outcome lookup; E only records the reference |
| Indexed | F confirmed application to the relevant index partition(s), with typed publication watermark(s) | F acknowledgement/watermark; E only records the reference |

**Accepted MUST NOT mean Processed, Compiled, CanonicalCommitted or Indexed.** A timeout after the durable acceptance transaction does not undo Accepted. A caller can query/replay the original receipt by idempotency identity. No Accepted response is sent before the acceptance durability point.

## 2. Ingress identity and idempotency

### 2.1 Key scope

The proposed idempotency namespace is the tuple:

`(authenticated_issuer, authenticated_producer_ref, security_domain_ref, event_family, idempotency_key)`

- `authenticated_issuer` and `authenticated_producer_ref` are bound by H's authenticated transport/session, not trusted from payload claims.
- `security_domain_ref` is the tenant or equivalent isolation domain supplied/validated under I policy. Exact type and whether ScopeRef participates are **OPEN with I/B/H**.
- `event_family` prevents accidental key collision between semantically distinct ingress APIs.
- The key is not globally unique and is not scoped to a future canonical Memory ID.
- The same key in a different authenticated producer namespace is a different idempotency identity, subject to I's delegation policy.

The key must be stable across transport retries and caller reconnects. A new logical event requires a new key.

### 2.2 Payload hash

Compute a versioned digest over the immutable semantic request:

- exact payload bytes or an immutable payload-object digest;
- event family and source identity/version;
- validated security-domain and Scope metadata;
- semantically relevant source timestamps, environment binding and declared content type;
- canonical envelope semantic fields after H-defined normalization.

Exclude transport attempt number, retry timestamp, connection ID, trace/span IDs and other delivery-only metadata. Do not hash a mutable URL as a substitute for payload bytes. Store `hash_algorithm`, `canonicalization_version` and `payload_digest`; H must define the wire canonicalization before interoperability freeze.

### 2.3 Required key outcomes

| Existing idempotency identity | Incoming digest | Required result |
|---|---|---|
| No record | Any valid digest | Create one durable receipt/event/compile intent |
| Existing | Same digest | Return the original receipt ID, Event ID, accepted_at and current processing status; do not create a second Event or intent |
| Existing | Different digest | Reject with `IDEMPOTENCY_KEY_REUSE_CONFLICT`; do not overwrite or create another Event |
| Existing content-free Forget tombstone | Same or different digest | Suppress replay and return a policy-safe forgotten/rejected outcome; never reconstruct payload or work |

Comparison is against the stored digest and canonicalization version. A version mismatch must be resolved by a defined migration/compatibility path, never by silently treating the request as new.

### 2.4 Receipt replay

Receipt replay is a read/reconciliation of the original durable acceptance record. It returns the same receipt identity and current milestone references. It does not re-run parsing, create a new source event, renew retention, or bypass a Forget fence. A caller may separately request a controlled reprocess/recompile; that is a new attempt identity linked to the original Event and is subject to current policy and Forget checks.

### 2.5 Retention horizon

Receipt and idempotency retention MUST cover the maximum of:
- supported client retry/reconnect horizon;
- supported queue, lease and DLQ residence horizon;
- supported operator replay/recovery horizon;
- audit and dispute obligations imposed by I.

The numeric horizon and legal hold/retention-class rules are **OPEN with I**. Expiration of payload content does not authorize key reuse while an idempotency tombstone is required. After Forget, retain only the minimum non-reconstructive suppression record required by I/D to prevent replay; do not retain source text, payload bytes, reversible references or content-derived metadata merely to support deduplication. The tombstone expiry/replay policy is I-owned.

## 3. Durable acceptance protocol

### 3.1 Preferred realization: immutable blob + transactional inbox/outbox

Where payload bytes live in object storage and metadata lives in a transactional database:

1. Authenticate producer and authorize `event.ingest` under I; validate envelope and size/type constraints.
2. Write payload to immutable, content-addressed or otherwise immutable storage; verify durable completion and digest. A temporary/staged object is not Accepted.
3. In one database transaction, insert:
   - immutable Event row with stable Event ID and source identity;
   - immutable payload reference, digest and retention classification;
   - unique idempotency row with namespace tuple, digest and receipt ID;
   - durable Accepted receipt with accepted_at and state=Accepted;
   - compile-intent/outbox row with stable intent ID and initial status.
4. Commit the transaction. **This commit is the Accepted linearization point.**
5. Only after commit, return Accepted receipt to caller. Dispatcher consumes outbox at least once.

The uniqueness constraint on the idempotency tuple serializes concurrent same-key requests. On a unique-key race, read the winner and apply same-digest replay or different-digest conflict. Never use check-then-insert without a uniqueness/serialization guarantee.

An orphaned staged blob from a crash before step 3 is not Accepted and may be garbage-collected only after a safe grace period and reference check. A committed Event must never point to an unverified or mutable payload.

### 3.2 Equivalent WAL/journal realization

If a single transactional database is unavailable, use a durable write-ahead journal whose commit record atomically binds Event identity, payload digest/reference, idempotency identity, receipt and compile intent. Recovery must replay committed journal records idempotently and ignore incomplete records. The journal must be fsynced/replicated to the durability level promised by Accepted before acknowledging. A best-effort queue publish followed by a separate receipt write is not equivalent.

### 3.3 Crash-window matrix

| Crash window | Durable state | Recovery rule | Caller-visible result |
|---|---|---|---|
| Before immutable payload write | None | Caller retries same key | Not Accepted |
| During payload write / before verification | Staged or incomplete blob only | Resume/clean staged object; no Event/receipt | Not Accepted |
| After blob verified, before DB/journal commit | Orphan immutable blob possible | Retry same key; dedupe at transaction; later GC orphan | Not Accepted |
| During acceptance transaction before commit | Transaction rolls back or journal lacks commit marker | Retry same key | Not Accepted |
| After acceptance commit, before HTTP/transport response | Event + payload ref + idempotency + receipt + intent durable | Retry returns original receipt | Accepted |
| After response, before dispatcher wakeup | Durable outbox remains pending | Poll/restart dispatcher | Accepted |
| After worker lease, before stage commit | Lease may expire; no committed stage result | Reacquire with same intent/attempt fencing; recheck Forget | Accepted, not yet Processed |
| After stage result, before next-stage dispatch | Stage result/outbox transaction durable | Outbox redelivery; consumer deduplicates | Milestone remains durable |
| After D commit, before E records response | D may have committed | Query D by stable operation key; record same commit; never blind-create | CanonicalCommitted only after D evidence |
| After F applied, before E records ACK | F may have applied | Query/replay by stable publication ID; F deduplicates | Indexed only after F evidence |

## 4. Event ordering and typed cursors

Three cursor families are intentionally distinct:

1. **Source Event cursor (E ingress-owned):** `SourceEventCursor{partition_id, offset}`. Monotonic only within a declared ingress/source partition. It orders durable acceptance records in that partition; it does not assert global real-world chronology or canonical commit order. Per-producer source sequence/timestamp is separate metadata and may be late, duplicated or out of order.
2. **Canonical commit cursor (D-owned):** E stores the exact typed D cursor/commit reference returned by D. Its scope, global/per-aggregate shape, gap semantics and transaction visibility remain D + Storage/Consistency decisions. E MUST NOT allocate, increment, reinterpret or synthesize it.
3. **Index publication watermark (F-owned):** `IndexPublicationWatermark{index_id, partition_id, applied_position}`. It advances only after the corresponding partition has durably applied all preceding required changes. E MUST NOT claim Indexed from an outbox dispatch or a D commit.

An E outbox sequence/dispatch offset is a fourth E-local transport checkpoint; it is not a canonical cursor or F watermark. A scalar integer MUST NOT be copied across these namespaces.

## 5. Retry and processing rules

- At-least-once dispatch is assumed. Every consumer has a durable inbox/deduplication key and commits its local effect plus inbox/checkpoint atomically, or uses an equivalent recoverable journal.
- Worker attempts are distinct from immutable Event and receipt identity. Attempt count, lease owner, lease expiry and retry schedule are operational metadata.
- A retry never mutates the original payload or receipt. Changed payload is a new Event/key.
- Unknown D commit outcome is resolved by querying D with the stable operation key. Never blind retry with a new key.
- DLQ is a durable state of the same intent, not a new Event. Replay preserves Event ID, receipt ID and source digest, creates a new attempt ID, and reauthorizes under current policy/fence.
- Recompile pins new compiler/schema/model/prompt versions and creates new IR/provenance revisions; it does not rewrite earlier outputs or renew expired permissions.
- Model/provider outage cannot revoke Accepted durability.

## 6. Interface impact

| Boundary | E provides/consumes | Authority not owned by E | Required failure behavior |
|---|---|---|---|
| H → E | Authenticated producer binding, versioned envelope, payload digest/ref, idempotency key, source identity, correlation IDs | H wire/serialization/authentication mechanism | Reject malformed/unauthenticated input; never trust payload actor assertion |
| I → E | Authorization decision/epoch, retention class, ingest permission and current Forget state | I policy, delegation, revocation and retention | Fail closed for protected processing when policy/fence cannot be established |
| E → D | Stable canonical write operation key, expected version, candidate/evidence/provenance refs | D canonical IDs, commit and canonical cursor | Query unknown outcome; record only D-confirmed commit |
| E → F | Post-D-commit publication request/reference and source lineage metadata | F projection and index watermark | At-least-once replay; do not mark Indexed until F evidence |
| E → G | Canonical change/outbox event reference where applicable | G ContextVersion and reconciliation | E does not write Context or infer Applied |

## 7. Conformance tests

- Concurrent same key/same digest creates exactly one Event, receipt and compile intent.
- Concurrent same key/different digest produces one winner and one conflict, never overwrite.
- Crash after acceptance commit but before response returns the original receipt on retry.
- Crash before acceptance commit never returns Accepted and cannot leave a visible compile intent.
- Blob write succeeds but DB commit fails: retry creates one acceptance; orphan cleanup cannot delete a referenced payload.
- Dispatcher duplicates, worker crashes, lease expiry and DLQ replay do not duplicate stage effects.
- D commit succeeds but response is lost: operation lookup recovers the same canonical commit.
- F applies but ACK is lost: publication replay is idempotent and watermark does not regress.
- Payload expiry/Forget tombstone prevents same-key replay from reconstructing source or work.
- Source sequence gaps, late timestamps and out-of-order arrivals do not corrupt canonical cursor or index watermark.

## 8. Open dependencies

- **OPEN — H:** BMCP envelope, canonicalization, producer binding, receipt wire representation and error encoding; H package must be read before these become normative.
- **OPEN — I:** principal/security-domain binding, authorization epoch, retention classes, receipt/tombstone horizon, audit minimization and legal hold exceptions.
- **OPEN — D + Storage/Consistency:** canonical cursor shape, commit operation lookup and atomicity boundary.
- **OPEN — F:** exact per-index/per-partition watermark acknowledgement contract.
- **OPEN — C:** source identity/sequence semantics and late-event policy.
- **OPEN — Storage/Engineering:** database/outbox/WAL product and replication/fdatasync durability target.
- **ADR-BLOCKED — B/Governance:** no CandidateProposition/ExtractionIR to canonical Claim mapping until ADR-001 is approved.
