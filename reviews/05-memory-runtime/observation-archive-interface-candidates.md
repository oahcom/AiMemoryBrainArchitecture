# Observation Archive Interface Candidates

**Owner:** F — Memory Runtime Architect  
**Status:** PROPOSED / OPEN / cross-owner approval required  
**Implementation status:** NOT_IMPLEMENTED  
**Baseline impact:** none; candidates only  
**Branch:** `session-f-memory-runtime`

> This document proposes conceptual contracts, not frozen wire schemas. Field names and shapes require owner review. No new canonical memory type is introduced.

## 1. Status legend

- **PROPOSED** — F candidate semantics; not approved/frozen.
- **OPEN** — unresolved design or dependency.
- **NEEDS_G_APPROVAL** — G must approve Context-facing semantics and payload.
- **NEEDS_D_E_I_APPROVAL** — D/E/I must approve canonical lineage, publication, Forget, retention or authorization semantics.
- **NOT_IMPLEMENTED** — no production implementation is claimed.

## 2. Ownership map

| Contract / data | Owner | Status |
|---|---|---|
| Archive capture, immutable blob, manifest, metadata index | F | PROPOSED / NOT_IMPLEMENTED |
| Archive retention class and policy authorization | I + Storage; D where canonical lineage applies | NEEDS_D_E_I_APPROVAL |
| Archive object target/inventory/Forget mapping | I + D | NEEDS_D_E_I_APPROVAL |
| RecallSession, ReadCursor, ReadReceipt, ReadBudget | F | PROPOSED / NOT_IMPLEMENTED |
| Scope/Permission decision and PermissionEpoch | I/H | OPEN; F consumes only |
| Canonical Memory lifecycle/Forget Fence | D | OPEN; F consumes only |
| Canonical event/index projection semantics | E | OPEN; archive metadata index must not masquerade as E index |
| F-to-G RecallResult and CandidateReference | F/G | NEEDS_G_APPROVAL |
| Context Entry, Context Version, compaction, delivery | G (with H/C) | G-owned; F has no mutation API |
| Archive storage encryption/key and physical deletion evidence | I/Storage | NEEDS_D_E_I_APPROVAL |

## 3. ArchiveObjectManifest

**Status:** PROPOSED / NEEDS_D_E_I_APPROVAL / NOT_IMPLEMENTED

Purpose: immutable metadata binding one archive object revision to exact source bytes and governed access/retention.

Candidate fields:
- `schema_version`
- `archive_object_id` — opaque, never reused
- `archive_object_revision` — immutable manifest revision
- `content_hash` — algorithm-qualified digest of exact stored bytes
- `content_length_bytes`
- `media_type`, `encoding`, `representation_version`
- `source_kind`, `source_identity_ref`, `source_revision` (nullable only with explicit unknown/not-provided state)
- `captured_at`, `observed_at`, optional `source_event_time`
- `principal_ref`, trusted `scope_refs`, applicable Agent/instance/session/task/environment refs
- `producer_ref`, `correlation_id`, optional parent/lineage refs
- `page_map_version`, optional index generation refs
- `classification_ref`, `retention_class_ref`, `expires_at`
- `integrity_state`, `archive_state`

Rules:
1. Same object revision is immutable. New bytes create a new revision or object with explicit lineage.
2. Hash verifies bytes, not authorization, source authenticity or semantic truth.
3. Normalized text, page maps, previews, summaries and embeddings are derivatives bound to source hash and transformation version.
4. No archive manifest becomes Canonical Memory.
5. Exact schema, hash algorithm, retention vocabulary and lineage semantics remain OPEN pending D/I/Storage.

## 4. ArchiveLocator

**Status:** PROPOSED / NEEDS_G_APPROVAL / NOT_IMPLEMENTED

Candidate fields:
- `archive_object_id`
- `archive_object_revision`
- `content_hash`
- `source_revision`
- `selector_capabilities` (page/range/keyword/entity/time supported)
- `scope_ref_digest` (opaque binding only; not a grant)
- `locator_expiry`
- `integrity_state`

Rules:
- Locator is not a bearer credential or authorization grant.
- Every use revalidates current I Permission and applicable D Forget Fence.
- No name-only or path-only reference is sufficient to bypass revision/hash binding.
- G must not dereference without F/I authorization path.

## 5. RecallIntent (G → F)

**Status:** PROPOSED / NEEDS_G_APPROVAL / NOT_IMPLEMENTED

Purpose: request a bounded, authorized read plan; not a Context mutation.

Candidate fields:
- `schema_version`, `request_id`, `correlation_id`
- authenticated session/principal binding (resolved by H/I, not trusted from payload)
- `purpose` and requested source/object references
- selectors: exact page(s), byte/text range, entity IDs, time interval, keyword/phrase, structured predicate
- desired completeness and consistency requirement
- read budgets: max objects, pages, bytes, calls, wall time
- optional G budget hint: desired max excerpt bytes/tokens
- deadline/cancellation
- optional Context ID/ContextVersion as read-only correlation hints only

Rules:
- Query text and caller-supplied scope labels never grant access.
- F resolves actual authorization through I/H.
- ContextVersion is not an F mutation token and cannot be created/advanced by F.
- Selector coordinate system must be explicit for non-byte ranges.

## 6. RecallSession

**Status:** PROPOSED / NEEDS_D_E_I_APPROVAL / NOT_IMPLEMENTED

Candidate fields:
- `recall_session_id`
- authenticated principal/security domain
- normalized trusted ScopeRefs
- applicable Agent/instance/session/task/environment
- purpose and policy version
- I `permission_epoch_ref` with domain/issuer
- D `forget_fence_ref/generation` where applicable
- exact archive object revision/hash/source revision
- selector-plan digest
- `read_budget_id`
- issued cursor generation and expiry
- state: active / complete / partial / stale / suppressed / expired / cancelled

Rules:
- Session binds one exact source revision per object read stream.
- Every continuation rechecks authorization and fence.
- No implicit cross-session reuse.
- Offline session cannot resume before authority refresh and reconciliation.

## 7. ReadBudget

**Status:** PROPOSED / OPEN / NOT_IMPLEMENTED

Candidate dimensions:
- max object count
- max metadata candidates
- max pages and bytes
- max read calls and concurrent reads
- max decompression/CPU work
- max wall-clock
- optional summary/model-call budget (default zero)
- optional G injection hint (advisory; G owns actual Context budget)

Budget accounting policy OPEN:
- decide whether an exact idempotent receipt replay consumes budget again;
- distinguish reserved, consumed, released and failed work;
- no unbounded retries or continuation loops;
- budget exhaustion always produces explicit partial result.

## 8. ReadCursor

**Status:** PROPOSED / NEEDS_D_E_I_APPROVAL / NOT_IMPLEMENTED

Candidate fields:
- `cursor_id`, `cursor_generation`
- `recall_session_id`
- exact `archive_object_id/revision/content_hash/source_revision`
- selector-plan digest and coordinate system
- next page/range offset
- consumed/covered ranges
- previous receipt ID
- expiry and integrity/MAC metadata

Rules:
1. Cursor is continuation state, never authorization.
2. Cursor cannot cross object, revision, hash, scope or selector plan.
3. Current permission and Forget state must be revalidated on every continuation.
4. Revocation, Forget, source mismatch, expiry or unverifiable checkpoint invalidates it.
5. EOF is terminal and returns no next cursor.
6. Arbitrary range requests are separate budgeted selectors unless a specific sequential cursor mode is defined.
7. Cursor concurrency/lease semantics remain OPEN pending tests.

## 9. ReadReceipt

**Status:** PROPOSED / NEEDS_G_APPROVAL / NEEDS_D_E_I_APPROVAL / NOT_IMPLEMENTED

Candidate fields:
- `receipt_id`, `request_id`, `recall_session_id`
- exact object ID/revision/hash/source revision
- selector and returned page/range
- returned byte length and optional content hash
- integrity verification result
- permission epoch and Forget fence checkpoint observed
- source revision state
- bytes/pages/calls budget consumed
- remaining coverage / next cursor or EOF
- completeness, omissions and failure reason
- timestamp and correlation ID

Rules:
- Receipt proves what F returned under a specific checkpoint, not that the model understood it or that the content is true.
- Receipt must not disclose protected object existence when authorization fails.
- Receipt retention is subject to I policy and Forget handling.
- G can cite receipt/range but must reauthorize when materializing content.

## 10. ObservationRecallResult (F → G)

**Status:** PROPOSED / NEEDS_G_APPROVAL / NOT_IMPLEMENTED

Candidate fields:
- request/correlation IDs
- authorized candidate references and bounded excerpts
- source object revision/hash/source revision
- exact ranges/page selectors and ReadReceipt refs
- source provenance/classification and untrusted-data marker
- per-source and per-index freshness/completeness
- omitted selectors/channels and budget exhaustion
- integrity, stale, unavailable, suppressed and partial reason codes
- estimated bytes/tokens and retrieval cost metrics
- no Context Version output and no mutation instruction

Rules:
- G decides whether anything enters Context.
- F does not silently convert a partial result to complete.
- F does not summarize away evidence without explicit derivative provenance.
- G revalidates D/I state and its own Context constraints before committing.

## 11. CompletenessMetadata

**Status:** PROPOSED / NEEDS_G_APPROVAL / NOT_IMPLEMENTED

Candidate dimensions:
- requested selector/scope
- executed adapters/index generations
- exact source revision/hash
- covered page/range/entity/time intervals
- known unserved ranges
- omitted channels and reasons
- candidate/read budget exhaustion
- timeout/cancellation
- integrity and source revision status
- permission/fence checkpoint status

Candidate states:
- `complete`: requested bounded selector fully executed and verified
- `empty_complete`: requested bounded selector fully executed and no match found
- `partial`: known omissions, truncation, timeout or budget exhaustion
- `degraded`: fallback path with reduced coverage/freshness
- `stale`: source/index revision mismatch
- `unavailable`: source/storage/auth dependency unavailable
- `suppressed`: Forget/revocation blocks access
- `unknown`: authority or integrity cannot be established

OPEN: final enum and typed error mapping require H/G review.

## 12. Cache and WorkingSetObservationEntry

**Status:** PROPOSED / NEEDS_D_E_I_APPROVAL / NOT_IMPLEMENTED

Candidate Working Set entry:
- ArchiveLocator
- exact object revision/hash/source revision
- scope and principal binding
- I PermissionEpoch
- D ForgetFence ref/generation where applicable
- F-local invalidation generation
- page map/index generation
- optional bounded preview/page bytes
- classification, retention and expiry
- last access and quota accounting

Rules:
- References/metadata preferred over raw bytes.
- Cached bytes, previews, summaries and embeddings inherit source sensitivity and Forget lineage.
- Key dimensions are not authorization; every hit revalidates.
- If I/D authority is unavailable, stale entry is quarantined, not downgraded to miss.
- TTL never substitutes for Forget/revocation.
- GPU VRAM is not a default archive/cache tier.

## 13. Forget / Revocation Hooks

**Status:** PROPOSED / NEEDS_D_E_I_APPROVAL / NOT_IMPLEMENTED

F consumes, but does not define:
- I PermissionEpoch and resource-level authorization/revocation;
- D ForgetFence and canonical derivative lineage where applicable;
- I target inventory / target evidence requirements.

Required F operations:
- suppress object and descendants before payload access;
- invalidate/revoke cursors and RecallSessions;
- cancel in-flight reads/fills;
- invalidate raw page, preview, summary, embedding and query caches;
- block late fill publication and final serialization;
- persist per-target/per-partition suppression evidence;
- reconcile missed notifications using authoritative snapshot + contiguous replay;
- quarantine on checkpoint gaps or unavailable authority.

F does not declare global Forget completion or physical erasure.

## 14. F/G Acceptance Contract

**Status:** PROPOSED / NEEDS_G_APPROVAL / NOT_IMPLEMENTED

F guarantees:
- only currently authorized archive candidates/references leave F;
- every returned excerpt is bound to exact bytes/revision/hash/range;
- completeness/freshness and omissions are explicit;
- F does not mutate Context;
- every page/cache return/final handoff is checked against current permission/Forget state.

G guarantees:
- no F locator is treated as permission;
- G validates candidate lifecycle, scope, classification and Context fit;
- G alone creates/updates Context Entry and ContextVersion;
- G does not infer semantic truth or Applied from an archive receipt;
- G triggers governed Forget/reconciliation through D/I/H contracts.

Cross-owner open points:
1. Whether G wants locator-only, excerpt+locator, or both.
2. What exact completeness evidence G requires for Context inclusion.
3. Whether a Context Entry can point to an archive revision that may expire before the Context.
4. How G invalidates Context projections when archive source expires/Forget occurs.
5. Which correlation fields are mandatory across H/C delivery evidence.

## 15. Approval Checklist

| Owner | Required decision |
|---|---|
| F | Own Runtime capture, archive, read, cursor, cache and completeness mechanics |
| G | Approve RecallIntent/ObservationRecallResult semantics; preserve ContextVersion authority |
| D | Approve canonical lineage/Forget interaction and any governed derivative mapping |
| E | Confirm no collision with canonical index publication; clarify any event feed dependencies |
| H | Approve authenticated request/correlation/cancellation/error envelope |
| I | Approve Scope/Permission, archive classification, retention, target inventory and revocation semantics |
| A | Integration architecture acceptance after owner decisions |

**No implementation is authorized by this candidate document.**
