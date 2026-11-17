# Storage Design v2 — Session P Exact-Version Audit of A R1–R6

- Date: 2026-11-17
- Coordinator: Session P
- Status: **COORDINATOR TECHNICAL REVIEW INPUT — NON-NORMATIVE; NOT AN OWNER DECISION**
- Repository: `oahcom/AiMemoryBrainArchitecture`
- Exact Storage v2 target: `reviews/storage-consistency/phase-3.6-coc-durable-log-and-recovery-protocol-storage-design-v2.md`
- Target commit: `337fe8bffa178e64ad8e4750f1ede1d561424edc`
- Target Blob: `4ed4234ce548a814a9496adf7a14c4459ea9f7ce`
- A review source: `reviews/integration/phase-3.6-coc-persistence-exact-version-review.md`, Blob `fdf63550696948f77dc37c0a3788276ac4d525f5`
- Current Storage companion path re-fetched on 2026-11-17: `reviews/storage-consistency/phase-3.6.3-coc-durable-log-and-recovery-protocol.md`, Blob `8ac17816476f280ab6fb3afca0688aa03e37de1d`
- v2 header still pins companion Blob `86ff3b247d7565a0dcd1f2e4ed21b5ba70a6b0d7`; this is a **version-drift finding**, not an assumed equivalent.

## 1. Executive disposition

Storage v2 materially improves the design and directly addresses several of A's R1–R6 concerns. It is not yet safe to mark all six findings closed.

| Finding | Session P technical disposition | Why |
|---|---|---|
| R1 — cutoff request-set completeness | **SUBSTANTIALLY ADDRESSED IN PROPOSAL; OWNER PROOF REQUIRED** | §§5.2–5.6 define owner snapshots/high-waters, exact prefix, explicit empty manifest, batch/manifest cross-binding and subsequent batches. No independent I/D acceptance yet. |
| R2 — owner-local gate linearization | **PARTIALLY ADDRESSED; BLOCKING CLARIFICATION** | §5.2 states snapshot capture is atomic with gate closure, but does not name the owner-local serializable transaction/CAS/sequencer point, durable admission record, or exact serialization order for every receipt/admission operation. |
| R3 — participant completeness and release | **PARTIALLY ADDRESSED; BLOCKING CLARIFICATION** | Immutable prefix-bound manifest and independent I/D releases are specified. The relationship between C's already-admitted but not-yet-COC-registered work and the COC participant manifest needs an explicit joined admission manifest and reconciliation rule. D's per-fence lineage proof still needs a concrete canonical evidence contract. |
| R4 — C provider invocation | **SUBSTANTIALLY ADDRESSED IN PROPOSAL; C EVIDENCE REQUIRED** | §6.3 explicitly requires exact I COMMIT_WON plus all D predicates; abort/unknown block provider side effects; reservation is non-side-effecting. Provider-specific same-key lookup/idempotency remains an adapter-specific blocker. |
| R5 — same-XID recovery | **PARTIALLY ADDRESSED; VERSIONED IDENTITY BRIDGE REQUIRED** | v2 §§7.1–7.5 improve same-participant resolution, but v2's tuple remains less complete than the current companion protocol's §14.1–14.4, including DatabaseIncarnationRef, PrepareAttemptRef/generation, ParticipantLedgerRef/version and authoritative PREPARED readback. |
| R6 — exact-version/schema drift | **OPEN / BLOCKING** | v2 still pins companion Blob 86ff3..., while the live companion file now returns Blob 8ac178...; H schema remains candidate and no exact A §11/§12 wire mapping is demonstrated by the v2 document itself. |

## 2. Detailed findings

### R1 — Recovery Cutoff Batch completeness

**Positive:** v2 §§5.2–5.6 specify owner-local snapshots, separate I/D high-waters, explicit empty participant set, canonical sorted unique ParticipantIntentRefs, immutable manifest digest, a batch record that binds the manifest identity/digest/count, a separate manifest record cross-bound to the committed batch, linearizable readback, and subsequent batches for requests after captured high-water. Recovery remains fenced until both records and reconciliation are complete.

**Remaining condition:** I and D must each independently prove that their local snapshot is complete and atomically tied to their own gate generation/cursor. C must prove that every already-admitted provider participant is represented either in the COC prefix manifest or in a separately committed owner-admission manifest bound into the same RecoveryEpoch. A prose statement that C “captures every already admitted provider participant” is not yet a concrete set encoding, digest, count, stable identity and cross-binding rule.

**Required Owner evidence:** I/D/C append-only decisions against exact v2 Blob; H schema for owner snapshots, empty-set semantics, batch and manifest; negative vectors for omission, duplicate, stale projection, changed digest and post-high-water request.

### R2 — Owner-local Gate linearization

**Positive:** v2 §5.2 states that each owner closes its gate and captures a stable snapshot atomically; §5.6 requires post-high-water requests to remain behind the closed gate; §§6.1, 6.2 and 6.4 preserve I/D-only release authority and anti-rollback.

**Blocking gap:** “atomic with gate closure” is an invariant, not the required implementation-neutral linearization definition. The v2 text does not identify the exact owner-local serialization point (serializable transaction, durable CAS, or single-writer sequencer) that atomically:
1. validates and deduplicates the request;
2. allocates its owner-local sequence and persists the request/digest;
3. closes/increments the scoped gate generation;
4. prevents concurrent receipt issuance/consumption or D/C/E producer admission from crossing the close point;
5. durably accounts for operations admitted before the point but not yet registered in COC.

**Required amendment:** Each of I and D must define its own exact linearization primitive and durable in-flight admission ledger. C must define the corresponding pre-provider admission record and how it joins the RecoveryEpoch manifest. The same request ID/digest is idempotent; changed digest or scope expansion is a conflict requiring explicit owner resolution.

### R3 — Participant-set completeness and gate release

**Positive:** v2 §§5.3–5.5 require exact-prefix enumeration, immutable canonical manifest, independent I/D reconciliation and owner-signed release. §6.2 correctly separates D outage-gate release, effective ForgetFenceGeneration and producer barrier completion.

**Blocking gap:** the prefix manifest enumerates COC participant intents at or before P. A provider participant admitted before gate closure may exist in C's local durable state but not yet have a COC intent at P. The v2 says C captures it, but does not define a mandatory second manifest or deterministic join:
- stable CAdmissionRef / ProviderParticipantRef;
- immutable request digest and idempotency namespace/key reference;
- admission high-water, count and canonical root;
- state at the provider boundary (NOT_INVOKED / IN_PROGRESS / ACCEPTED / REJECTED / UNKNOWN);
- exact mapping to ParticipantIntentRef, or explicit orphan/pre-registration treatment;
- cross-binding of that set into the RecoveryEpoch and owner releases.

Likewise, D's per-fence affected-lineage membership manifest is required, but its canonical ordering, root/digest, source lineage snapshot/version, positive not-affected proof and unknown-lineage behavior need to be fixed by D and H. A global COC manifest cannot substitute for D's per-fence lineage authority.

**Required amendment:** Define a composite recovery inventory: (a) COC prefix participant manifest, (b) owner-local pre-cutoff admission manifests, and (c) D per-fence lineage membership manifests. Bind each by digest/count/high-water into the batch/RecoveryEpoch and require independent owner reconciliation before release.

### R4 — C provider invocation requires I COMMIT_WON

**Positive:** v2 §6.3 is explicit: only durable I COMMIT_WON for the exact bound operation/final-gate participant plus all required D predicates permits provider invocation. REVOCATION_WON, INDETERMINATE_ABORTED and other abort outcomes prohibit provider side effects; UNKNOWN/IN_DOUBT blocks. Pre-provider reservation is explicitly non-side-effecting. Provider ambiguity remains UNKNOWN and retries must use the same key and authoritative lookup where supported.

**Remaining condition:** C must provide adapter-specific evidence for namespace, key retention, lookup consistency, duplicate-submit semantics and ambiguous handoff recovery. If a provider cannot establish safe same-key recovery, the state remains IN_DOUBT; this cannot be waived by the COC protocol. I must independently accept the exact terminal proof binding/consumption; D must accept the exact predicates C consumes.

### R5 — Same-XID recovery and PreparedParticipant identity

**Positive:** v2 §§7.1–7.4 prohibit detached I tokens, bind I's terminal decision to the exact Storage final-gate participant, require same-participant forward commit/rollback, and preserve UNKNOWN/IN_DOUBT without heuristic or alternate-XID resolution. §7.5 correctly distinguishes PostgreSQL client-chosen PreparedTransactionGID from engine-assigned native XID.

**Blocking cross-version gap:** the live companion protocol file now returns Blob `8ac17816476f280ab6fb3afca0688aa03e37de1d`. Its §14.1–14.4 adds a more complete immutable tuple:
- PreparedParticipantRef;
- PreparedTransactionGID;
- PostgreSQLNativeXID observed from authoritative `pg_prepared_xacts` readback;
- CanonicalAuthorityDBRef and non-reusable DatabaseIncarnationRef;
- PostgreSQL system identifier/database OID/timeline/LSN as separate engine evidence;
- PrepareAttemptRef + monotonic generation;
- ParticipantLedgerRef + version;
- ParticipantTupleDigest;
- immutable original prepare coordinates and separate recovery observations;
- authoritative PREPARED readback and durable participant outcome ledger.

Storage v2 §7.5 does not yet reproduce the full tuple or state its precedence over the newer companion §14. v2 also uses generic DBIdentity/preallocated-XID language in §§7.1–7.4. The two documents therefore do not yet form one unambiguous normative identity contract.

**Required amendment:** Storage must repin the exact companion Blob and explicitly state normative precedence; reconcile v2 §§7.1–7.5 with current companion §14.1–14.4; update common JF-10 protocol, B nominal types and H schema; require I's exact terminal proof to consume the same immutable tuple and receipt identity. Absence from `pg_prepared_xacts` remains non-terminal without the durable outcome ledger and authoritative DB readback.

### R6 — Exact-version references and H schema applicability

**Blocking version drift:** v2 header §9 pins companion Blob `86ff3b247d7565a0dcd1f2e4ed21b5ba70a6b0d7`; the current live companion file read on this audit is Blob `8ac17816476f280ab6fb3afca0688aa03e37de1d`. The 8ac revision contains the expanded §14 identity contract. The v2 must either repin and reconcile to 8ac or explicitly freeze 86ff as its normative companion and prove no later source change is intended. Silent carry-forward is prohibited.

**Schema gap:** v2 §10 lists field classes and §13.1 says H must bind recovery schema applicability to exact A §11/§12. That is a requirement, not evidence that the H schema has done so. The current H schema candidate Blob `a8a945cc3623c2907003b93625e3c79742150944` remains a candidate; the v2 does not provide a concrete versioned mapping for the new batch/manifest/gate-release records and the complete GID/native-XID/DB-incarnation/prepare-attempt tuple.

**Required amendment:** H must publish an exact schema revision and positive/negative vectors pinned to the exact A §11/§12 and Storage companion/v2 bundle. H must explicitly state whether old §12.9 mappings are bound to current A §11, and reject downgrade, omitted required fields, null-vs-empty ambiguity, duplicate refs, wrong owner signatures and cross-authority position coercion.

## 3. Owner decision state — no inference

As of this audit:
- Issue #14 remains OPEN. Its comments do not contain independent I/D/C/H R1–R6 decisions.
- Issue #16 remains OPEN. Its status comment reports A/H/I reviews as coordinator-session role simulations (A conditional amendments; H/I candidate/no approval) and D/C exact-v2 decisions absent.
- Storage's v2 disposition table is a source-owner proposal response, not acceptance by A/I/D/C/H.
- Earlier decisions against Storage Blob 4ac63... or 86ff3... do not transfer to Blob 4ed423... or the current companion Blob 8ac178....

## 4. Required closure sequence

1. Storage publishes one canonical version vector and normative precedence between current companion Blob 8ac178... and v2 Blob 4ed423..., then reconciles the full PreparedParticipant tuple.
2. I and D publish their exact local linearization, admission manifests, high-water and independent release contracts.
3. C publishes the pre-provider/in-flight admission inventory and adapter-specific same-key recovery evidence; C's R4 disposition remains conditional until then.
4. H publishes exact schemas and canonical/signature envelope mapping for batch, manifest, owner gate release, C admission and PreparedParticipantReceipt/StorageResolutionProof.
5. A independently re-reviews the exact revised bundle and publishes its integration decision.
6. Only after the above may the design gate be reconsidered. Gate C implementation/fault injection remains a separate engineering gate.

## 5. Non-claims

This audit is not an Owner decision, implementation, test run, conformance PASS, protocol freeze, production database selection, production readiness or merge authorization. No Owner branch or main branch was modified. Session P's role is limited to coordinator analysis and evidence tracking.
