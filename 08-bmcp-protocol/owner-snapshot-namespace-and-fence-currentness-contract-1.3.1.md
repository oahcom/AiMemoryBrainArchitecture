# Owner Snapshot Namespace and Fence Currentness Contract — Successor 1.3.1

- Contract version: **1.3.1**
- Status: **D OWNER ACCEPTED — normative successor only; implementation NOT VERIFIED; conformance NOT RUN; no production authorization**
- Supersedes for D-owner normative use: the complete v1.3.0 §5 scalar rule in both English and Chinese, plus all scalar-comparison rows in both English and Chinese §8 tables. All other v1.3.0 rules remain unchanged unless expressly amended below.
- Exact predecessor: main commit 4f82e3a48a35e9fd73e7920f0c6a559b77aaf0dc; 08-bmcp-protocol/owner-snapshot-namespace-and-fence-currentness-contract.md; Blob d83cde77e98db2e74cf6827d874b0babb4157304.
- Owner decision: D-OWNER-2026-11-19-003; proof package: 03-memory-brain/d-002-six-condition-operational-proof-2026-11-19.md.
- Source semantic decision: D-OWNER-2026-11-19-002, Issue #25 comment 7015682819, Issue #43 comment 7015684625.
- This successor is a D Owner normative decision. It is not H Owner acceptance, not a D/H common-baseline acceptance, not implementation evidence, and not production readiness.

## 1. Normative delta and precedence

This document is a versioned successor amendment to D contract 1.3.0. It preserves the 1.3.0 namespace identity and canonicalization algorithm except for the explicit Unicode data-version binding in §4 below. It replaces the entire 1.3.0 §5 scalar comparison rule in both English and Chinese and removes all three scalar-comparison rows from both English and Chinese §8 tables. If any 1.3.0 text elsewhere appears to permit a cross-type comparison, numeric inequality proof, or Capture-created cutoff, this successor and D Owner Decision -002/-003 prevail.

## 2. Typed high-water definitions

1. ProducerRegistrationHighWater is the high-water of ProducerRegistrationSequence in the D ProducerWork Registration Ledger namespace, scoped to the exact Brain Authority and Producer Registration Ledger identity. Its authority source is the D producer-work registration ledger and immutable BarrierSnapshotReceipt.
2. ForgetFenceGeneration is allocated by the D ForgetFence authority and belongs only to the ForgetFence namespace.
3. H producer_registration_high_water maps only to ProducerRegistrationHighWater / ProducerRegistrationSequence.
4. H forget_fence_generation_high_water maps only to ForgetFenceGeneration.
5. These fields have distinct nominal types, units, sequences, and authority sources. They MUST NOT be numerically compared, cast, substituted, or used to derive one another. Decimal-string serialization does not alter nominal type.
6. CanonicalCommitCursor, Fence state version, ProducerRegistryVersion, ProducerRegistrationHighWater, and ForgetFenceGeneration remain separate nominal types. No arithmetic or ordering relation may be inferred across these types.

## 3. Capture semantics

1. InstallForgetFence establishes the immutable producer-registration cutoff at its D-authoritative linearization point and persists it as captured_producer_registration_high_water of type ProducerRegistrationHighWater.
2. CaptureProducerRegistrationHighWater retrieves and verifies that already-established cutoff and its immutable snapshot binding. Capture is not a new admission operation and MUST NOT set, reset, advance, or replace the cutoff.
3. A Capture request before durable fence installation MUST return FENCE_NOT_INSTALLED or UNKNOWN; it MUST NOT return a later ledger tip as a new cutoff.
4. Repeated Capture for the same fence/snapshot identity MUST return the same immutable BarrierSnapshotReceipt. Reconciliation checkpoints may append evidence but MUST NOT mutate the original cutoff or erase unresolved entries.

## 4. Canonicalization data-version binding

The 1.3.0 §4 algorithm is retained with this mandatory data-version pin:

1. **Unicode data version:** Unicode **15.1.0**.
2. **Normative source:** Unicode Standard Annex #15 (Unicode Normalization Forms) and the Unicode Character Database 15.1.0 distribution, including CaseFolding.txt, DerivedNormalizationProps.txt, PropList.txt, and NormalizationTest.txt. Implementations MUST use the versioned 15.1.0 data, not the host runtime's unspecified “current” Unicode data.
3. **Bound algorithm:** for each of the first three namespace segments, apply NFKC using UCD 15.1.0, then Unicode Default Case Folding using UCD 15.1.0 common/full mappings (statuses C/F; exclude Turkic T mappings), then NFKC again using UCD 15.1.0, then trim the UCD 15.1.0 White_Space property. The fourth version segment retains the existing NFKC-and-trim behavior and MUST NOT be case-folded. Decode-once, strict UTF-8, delimiter-injection rejection, canonical re-encoding and idempotence requirements remain unchanged.
4. **Implementation binding:** every conforming validator/build MUST expose unicode_data_version = "15.1.0", verify the actual normalization/case-folding/White_Space data source version at runtime or build time, and fail closed if it differs. The implementation MUST pin the versioned UCD artifacts and record SHA-256 for each artifact in a checked-in lock manifest. A runtime default or a version string not tied to the actual data source is insufficient.
5. **Conformance:** run the complete Unicode 15.1.0 NormalizationTest.txt corpus and D-specific vectors covering compatibility normalization, fullwidth solidus rejection, U+3000 whitespace, Default Case Folding, percent-decoding, malformed UTF-8, double-decoding rejection, and canonicalization idempotence.
6. **Upgrade/migration:** a Unicode data upgrade requires a new normative contract revision and an explicit migration plan. The plan MUST compare old/new canonical outputs over the complete namespace corpus and adversarial vectors; identify collisions, splits, and changed equivalence classes; preserve historical canonical IDs; and require explicit namespace migration with continuity proof. No silent recanonicalization, mixed-version comparison, or implicit identity inheritance is permitted. If continuity cannot be proven, the result is UNKNOWN and migration is blocked.
7. This version pin is a normative contract decision. It does not claim that any existing validator, runtime, vendored UCD bundle, or production deployment has already been updated or verified.

## 5. D-002 six-condition proof rule (normative replacement for 1.3.0 §5)

The D-002 proof is valid only when **all six** conditions below hold conjunctively for the same immutable operation and snapshot. No condition may be omitted, merged, or inferred from a field name, numeric magnitude, schema presence, or one successful operation.

1. Same BrainAuthorityId, Producer Registration Ledger identity/namespace, and ProducerRegistryVersion.
2. Same ForgetOperationId, idempotency identity, canonical request digest, and exact target-set digest.
3. Same ForgetFenceCursor / ForgetFenceGeneration and installation CanonicalCommitCursor.
4. The InstallForgetFence durable receipt's captured_producer_registration_high_water equals the CaptureProducerRegistrationHighWater BarrierSnapshotReceipt's producer_registration_high_water as the same nominal ProducerRegistrationHighWater type and same immutable snapshot. Equality is required. Greater-than or less-than is never a success case.
5. The BarrierSnapshotReceipt binds the identities above plus a D-authoritative ledger consistency proof/reference.
6. The D serialization proof establishes that every accepted registration ordered before the fence linearization point has sequence <= H and is included in the barrier; ordinary covered registrations ordered after the fence are rejected/quarantined or explicitly cleanup-only and cannot publish.

### 5.1 Type and comparison rule

The words installed and captured MUST NOT be used as untyped scalar variables. Where legacy field labels must be parsed, they MUST be resolved by exact schema/version mapping to the typed fields in Condition 4. Each serialized high-water field MUST independently be a non-negative decimal integer, with no sign, whitespace, separator, exponent, or fraction; leading zeroes remain accepted and canonicalized within that field's own nominal type; the value range is 0 through 2^63-1. Parsing/canonicalization is performed independently and does not authorize cross-type comparison. The only comparison is typed equality of the same immutable ProducerRegistrationHighWater cutoff. No greater-than or less-than success rule exists. Neither value may be interpreted as ForgetFenceGeneration. The two H high-water fields MUST never be compared with one another.

### 5.2 Result classification

- All six conditions proven from the same authoritative evidence => VALID, subject to independent currentness and revocation checks.
- Explicit identity, operation, cursor, snapshot or same-typed cutoff mismatch => INVALID (or STALE where the authoritative state-version rule specifically requires STALE).
- Missing/unavailable ledger, registry, receipt, consistency proof, serialization order, or anti-rollback evidence => UNKNOWN / BLOCKED; never VALID.
- Any partial condition set is not a successful proof.

### 5.3 Capture, concurrency, replay and crash

1. Install and RegisterProducerWork share one D-authoritative linearizable ordering domain per affected Brain Authority/source lineage. A registration ordered before fence installation is included at/below H; a covered ordinary registration ordered after it is rejected/quarantined or cleanup-only and cannot publish.
2. Fence installation atomically persists the effective fence, generation, registry version, immutable registration cutoff, target binding, inventory snapshot/watermark, receipt and recoverable outbox intent. No success receipt precedes durable commit.
3. Capture retrieves the install-bound immutable snapshot; it never creates a second cutoff. Capture before installation fails closed.
4. Exact replay of the same operation/idempotency identity/digest returns the original receipt and cutoff. Changed digest or target digest under the same identity returns IDEMPOTENCY_CONFLICT.
5. Lost response after durable commit is resolved by lookup/replay of the same operation identity. Timeout alone proves neither commit nor abort.
6. Crash before commit leaves no successful receipt; retry uses the same identity. Crash after commit recovers the exact original receipt. Partial or uncertain persistence remains UNKNOWN/BLOCKED and cannot authorize publication or barrier closure.
7. Restore/recovery MUST prove ledger continuity and anti-rollback of fence generation/state version. A stale replica, cached VALID result, or lower restored version cannot establish currentness. Unprovable continuity remains UNKNOWN.
8. Multi-namespace operations are proved independently per namespace. No high-water arithmetic or substitution crosses namespaces. Partial success is retained locally but aggregate completion remains OPEN/UNKNOWN until every required namespace independently satisfies all six conditions.
9. Fence currentness/state-version and revocation remain independent checks. Revocation/replacement and state-version comparison use one authoritative state snapshot; mismatch => STALE, explicit revocation => INVALID, unavailable => UNKNOWN. No TTL or local clock substitutes.
10. Already executed fade/forget effects are not automatically reversed or re-executed because a proof later becomes STALE, INVALID, or UNKNOWN.

## 6. §8 decision-table replacement

Delete all three scalar comparison rows (installed = captured, installed > captured, installed < captured) from both the English §8 table and its Chinese counterpart. The affected predecessor rows are English lines 259–261 and Chinese lines 546–548 in the exact 1.3.0 Blob identified in the header. The entire scalar comparison table in §5 is replaced in both languages.

Replace them with:
- Same typed immutable ProducerRegistrationHighWater, same operation/fence/snapshot binding, and all six D-002 conditions proven | VALID (then evaluate currentness/revocation independently).
- Explicit binding or same-typed cutoff mismatch | INVALID (or STALE only where the authoritative state-version rule requires it).
- Required authority/ledger/receipt/consistency/serialization evidence unavailable | UNKNOWN.

## 7. Acceptance and evidence boundary

D Owner accepts this 1.3.1 normative successor and the semantic proof rule. The D operation contract remains the operation baseline for RegisterProducerWork, InstallForgetFence, CaptureProducerRegistrationHighWater, ResolveProducerWork and ReconcileForgetBarrier.

This acceptance does not claim a production implementation, a verified validator, a successful race/crash/restore test run, CI PASS, D/H joint acceptance, schema freeze, or production authorization. Those require separate exact-head evidence and independent review.
