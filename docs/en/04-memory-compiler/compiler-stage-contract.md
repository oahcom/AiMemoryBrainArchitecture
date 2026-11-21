<!-- Target: docs/en/04-memory-compiler/compiler-stage-contract.md | Insert: new standalone compiler-stage contract; no modification to existing contracts. -->

# Memory Compiler Stage Contract

**Work Item:** GAP-01-COMPILER-CORE-001  
**Owner:** E — Memory Compiler Architect  
**Baseline:** `360d88c99a47018ce78b870379be3ee43841a837`  
**Status:** CANDIDATE implementation contract; implementation conformance required.

## 1. Authority and boundaries

The Memory Compiler MUST transform durably accepted Events into staged derivatives with explicit provenance.

The Compiler MUST NOT declare Canonical Truth, authorize Forget, approve schemas, approve public APIs, or independently advance Storage visibility.

The following distinctions are mandatory:

- Accepted MUST NOT imply Compiled.
- Compiled MUST NOT imply Canonical.
- Staged MUST NOT imply Published.
- PublicationParticipant Admission MUST NOT imply successful Producer Admission.
- Producer Admission MUST NOT substitute for PublicationParticipant Admission.
- `DECIDED FOR CONVERGENCE` MUST NOT be interpreted as `ACCEPTED`.

The existing Event Store Contract remains authoritative for Accepted Receipt, idempotency identity and compile-intent persistence.

The existing Extraction and Normalization contract §19.1 and §19.2 remains authoritative for publication ordering.

## 2. Stage inventory

| Order | Stage | Input | Output |
|---|---|---|---|
| 1 | Ingestion | Accepted Event, Receipt, durable intent | Ingested Event |
| 2 | Extraction | Ingested Event, immutable payload | Extraction IR |
| 3 | Normalization | Extraction IR | Normalized IR |
| 4 | Staging | Normalized IR, lineage, dependency registration | `PREPARED_HIDDEN` derivative |
| 5 | Publication Gate | Staged derivative, authoritative admission evidence | Publication disposition |

Every stage MUST have:

1. An immutable logical identity.
2. Explicit typed input and output.
3. A deterministic parameter digest.
4. Structured provenance.
5. An explicit failure classification.
6. An idempotent retry identity.
7. A recoverable execution state.

## 3. Shared provenance contract

Every stage output MUST carry:

| Field | Requirement |
|---|---|
| `source_event_id` | Exact immutable source Event identity |
| `source_payload_digest` | Exact accepted source digest |
| `stage_output_id` | Immutable stage output identity |
| `upstream_outputs` | Exact upstream output identities |
| `compiler_version` | Pinned compiler implementation version |
| `parameter_digest` | Digest of the exact stage parameters |
| `stage_name` | Exact producing stage |
| `attempt_generation` | Worker attempt generation |

Provenance MUST be structured data.

A stage MUST NOT replace an upstream identity with a display string, inferred identity, or mutable reference.

Changing source digest, compiler version, or effective stage parameters MUST create a distinct logical output identity.

Retrying identical inputs with identical parameters MUST preserve the logical stage identity.

## 4. Stage contracts

### 4.1 Ingestion

**Input**

- Durable Accepted Event.
- Original Accepted Receipt.
- Exact source payload reference and digest.
- Durable compile-intent record.

**Output**

- Immutable `IngestedEvent`.
- Source lineage.
- Original receipt identity.

**Preconditions**

- Event acceptance MUST be durable.
- Compile intent MUST be durably recorded.
- Scope authorization MUST precede receipt replay.
- Source authorization MUST be checked before payload dereference.

**Failure semantics**

- Missing receipt: `REJECTED`.
- Missing compile intent: `BLOCKED`.
- Payload digest mismatch: `FAILED`.
- Unknown authorization: fail closed.
- Duplicate accepted Event: return the existing logical ingestion result.

**Idempotency**

The ingestion identity MUST derive from the accepted Event identity and source digest.

**Reentrancy**

Ingestion MAY be re-entered after crash recovery. Re-entry MUST NOT create a second Accepted Receipt or compile intent.

### 4.2 Extraction

**Input**

- `IngestedEvent`.
- Immutable payload.
- Extraction parameter set.
- Current authorization evidence.

**Output**

- `ExtractionIR`.
- Source spans and source locators.
- Extraction method receipt.
- Provenance.

**Preconditions**

- Ingestion MUST be complete.
- Payload integrity MUST be verified against the accepted digest.
- Source authorization MUST be current.
- Scope MUST be preserved.
- Current Forget Fence MUST be evaluated.

**Failure semantics**

- Invalid source span: `FAILED`.
- Unsupported modality: `REJECTED`.
- Ambiguous content: preserve ambiguity in the IR.
- Model unavailable: `RETRYABLE`.
- Unknown policy or Fence state: fail closed.

**Idempotency**

Extraction identity MUST derive from Event identity, source version, digest, Scope, parser version, model version and policy version.

**Reentrancy**

The same extraction identity MUST return the same durable result or resume the same incomplete attempt.

Partial parser failure MUST NOT silently promote incomplete content to complete extraction.

### 4.3 Normalization

**Input**

- `ExtractionIR`.
- Explicit normalization parameters.
- Upstream provenance.

**Output**

- `NormalizedIR`.
- Normalized temporal and textual representations.
- Unresolved ambiguity records.
- Provenance.

**Preconditions**

- Extraction MUST be complete.
- Every normalized element MUST retain its source lineage.
- Scope and epistemic distinctions MUST be preserved.
- Normalization MUST NOT invent canonical identity.

**Failure semantics**

- Invalid transformation: `FAILED`.
- Unresolvable temporal value: preserve `UNKNOWN`.
- Ambiguous entity: preserve ambiguity.
- Unsupported semantic conversion: `REJECTED`.

**Idempotency**

The same IR and parameter digest MUST produce the same logical normalized output.

**Reentrancy**

Normalization MUST be restartable without changing upstream Extraction IR.

### 4.4 Staging

**Input**

- `NormalizedIR`.
- Complete direct and transitive dependency set.
- Provenance.
- Successful Producer Admission evidence.
- Authoritative canonical commit references when available.

**Output**

- Immutable staged derivative.
- Complete lineage registration.
- Dependency registration identity.
- Publication tuple identity.
- State `PREPARED_HIDDEN`.

**Preconditions**

- Producer Admission MUST have succeeded.
- The exact Producer participant MUST be durably recorded.
- `DependencyClosurePersisted(P)` MUST equal TRUE.
- The exact dependency closure MUST NOT be narrowed.
- D canonical commits MUST satisfy §19.1 ordering.
- Storage MUST durably persist the exact publication tuple as `PREPARED_HIDDEN`.

**Failure semantics**

- Incomplete dependency closure: `BLOCKED`.
- Missing Producer Admission: `REJECTED`.
- Missing canonical commit: `BLOCKED`.
- Storage preparation failure: `FAILED`.
- Unknown dependency persistence: fail closed.

**Idempotency**

Staging MUST use the exact operation identity and immutable upstream lineage.

A retry MUST NOT create an alternative publication identity for an already terminally rejected operation.

**Reentrancy**

Staging MUST resume the original staged identity after crash recovery.

**Visibility**

A staged derivative MUST remain invisible until:

1. Complete lineage is durably registered.
2. Complete dependency closure is durably registered.
3. Required canonical commits are confirmed.
4. Exact Storage tuple is durably `PREPARED_HIDDEN`.
5. PublicationParticipant Admission succeeds.
6. Protected visibility processing authorizes advancement.

`PREPARED_HIDDEN` MUST use the existing §19.2 meaning. No independent staged visibility state is introduced.

### 4.5 Publication Gate

**Input**

- Exact staged derivative.
- Exact publication tuple.
- PublicationParticipant identity.
- Current Forget Fence evidence.
- Authoritative Storage preparation evidence.
- Canonical commit evidence.

**Output**

One of:

- `PUBLISHED`
- `SUPPRESSED`
- `BLOCKED`
- `FAILED`

**Preconditions**

- The exact staged identity MUST be verified.
- Successful Producer Admission MUST be independently verified.
- Successful PublicationParticipant Admission MUST be independently verified.
- Storage MUST confirm the exact `PREPARED_HIDDEN` tuple.
- Dependency closure MUST remain complete.
- Current protected visibility authorization MUST be established.

**Failure semantics**

- Second-stage Admission rejected: `SUPPRESSED`.
- Missing evidence: `BLOCKED`.
- Conflicting evidence: fail closed.
- Unknown Fence: `BLOCKED`.
- Stale worker generation: `SUPPRESSED`.
- Storage visibility advancement failure: preserve hidden state or recover the authoritative terminal disposition.

**Idempotency**

Publication MUST be idempotent for the exact publication identity.

A retry MUST NOT turn a rejected PublicationParticipant Admission into successful Admission.

**Reentrancy**

Publication recovery MUST consult authoritative terminal evidence. It MUST NOT reconstruct authorization from worker-local state.

## 5. Publication ordering

The following order is mandatory:

1. Resolve I authorization and Scope.
2. D Forget Fence evaluation and Producer Admission.
3. Durable complete dependency registration.
4. Private immutable E staging.
5. D ClaimRevision/FactRevision canonical commit.
6. Recoverable association of canonical revisions, dependency registration and Publication Intent.
7. E publication preparation.
8. Storage protected visibility advancement after required records are confirmed.
9. G ContextVersion commit using exact immutable canonical revision references.
10. Logical completion.

The additional PublicationParticipant Admission order in §19.2 MUST be preserved:

1. Producer Admission and durable participant recording.
2. Dependency closure registration.
3. D canonical commit.
4. Storage durable `PREPARED_HIDDEN` tuple.
5. PublicationParticipant Admission.
6. Protected visibility processing.

The two admission operations MUST remain distinct.

The ForgetFence/Admission ordering anchor and per-BrainAuthorityRef serialization anchor MUST refer to the same authoritative ordering anchor.

## 6. Execution and recovery state machine

The Compiler execution state MUST use the following lifecycle:

```text
PENDING
   |
   v
LEASED
   |
   v
RUNNING
   |
   v
STAGED
   |
   v
PREPARED_HIDDEN
   |
   v
PUBLICATION_ADMISSION
   |
   +------> PUBLISHED
   |
   +------> SUPPRESSED
   |
   +------> BLOCKED
   |
   +------> FAILED
```

Terminal states:

- `PUBLISHED`
- `SUPPRESSED`
- `FAILED`

`BLOCKED` MUST remain recoverable and MUST NOT be treated as terminal success.

### 6.1 Retry

- Retryable failure MUST return to `PENDING`.
- Retry MUST preserve the logical stage identity.
- Retry MUST increment attempt generation.
- A terminally suppressed publication MUST NOT be retried into publication success under the same identity.
- An independently authorized operation MUST receive a new operation identity.

### 6.2 Lease

- A worker MUST hold a valid lease before stage execution.
- Lease ownership MUST identify worker, operation and generation.
- Lease expiration MUST make the previous generation ineligible for publication.
- Lease renewal MUST NOT change logical output identity.
- Concurrent lease acquisition MUST be serialized by the authoritative lease provider.

### 6.3 Crash recovery

- A completed stage MUST have a durable result and recoverable next-stage intent.
- Recovery MUST identify the last durable stage result.
- Recovery MUST resume from that result rather than repeating an externally visible effect.
- Unknown commit outcome MUST remain unresolved.
- Recovery MUST use the original operation identity.
- Recovery MUST re-check authorization and Forget Fence before sensitive processing.

### 6.4 Late-worker suppression

A worker whose lease generation is stale MUST NOT publish.

A late worker MUST NOT:

- Overwrite a newer stage result.
- Replace a terminal disposition.
- Restore a suppressed derivative.
- Advance a Storage tuple.
- Convert `PREPARED_HIDDEN` into visible state.
- Reuse a rejected PublicationParticipant identity.

The authoritative publication boundary MUST reject stale generations.

A terminal publication disposition MUST be immutable for its exact publication identity.

## 7. Evidence and provenance

Every output MUST preserve:

- Exact source Event identity.
- Source digest.
- Exact upstream output identities.
- Compiler version.
- Parameter digest.
- Stage identity.
- Attempt generation.
- Durable dependency registration identity.
- Publication identity where applicable.

Evidence MUST distinguish direct source evidence from derived interpretation.

Extraction MUST NOT fabricate source spans.

Normalization MUST NOT erase unresolved ambiguity.

Staging MUST NOT declare CandidateProposition canonical.

The Compiler MUST preserve D's existing Claim identity decision without extending it into unapproved Fact-specific modeling.

## 8. Cross-owner authority boundaries

| Operation | Required authority | E authority |
|---|---|---|
| Accepted Receipt | Event Store | Consume only |
| Producer Admission | D authoritative Fence/Admission | Invoke and preserve exact evidence |
| Dependency closure | Authoritative dependency registrar | Supply exact dependency set |
| ClaimRevision commit | D | Submit candidate material |
| FactRevision commit | D | Record unresolved dependency |
| `PREPARED_HIDDEN` persistence | Storage | Submit exact publication tuple |
| PublicationParticipant Admission | D authoritative Fence/Admission | Invoke and preserve exact evidence |
| Protected visibility advancement | Storage and applicable D/I authorization | No independent authority |
| ContextVersion commit | G | Supply exact immutable references |
| Forget authorization | I/D authoritative policy boundary | Re-check and obey |

E MUST NOT implement substitute authorization decisions.

E MUST NOT introduce a second Forget Fence, independent ordering anchor, or independent publication transaction domain.

## 9. Implementation conformance

The reference crate MUST implement deterministic in-process stage execution and type-safe stage boundaries.

The reference crate MUST NOT claim production durability, distributed atomicity, canonical commit authority or production publication authorization.

Every unimplemented authority integration MUST be explicitly identified as `NOT IMPLEMENTED` with a named dependency.

**NOT IMPLEMENTED:** The production `PublicationAuthority` adapter is absent; it depends on Owner D's authoritative Admission/Fence and canonical/dependency evidence, Owner I's current authorization evidence, and the Storage authority owner's `PREPARED_HIDDEN` and protected-visibility confirmation.

Schema, DDL, Public API, H Wire Format, production keys, Trust Root, Crypto Profile and Storage L4 approval remain `NOT APPROVED`.

---

## 9. Verification performed

| Check | Command | Result |
|---|---|---|
| Build | `cargo build --offline -p memory-compiler` | PASS with default features; no C compiler invoked |
| Tests | `cargo test --offline -p memory-compiler` | PASS, 30 passed / 0 failed / 0 ignored |
| SQLite adapter | `cargo test --offline -p memory-compiler --features sqlite` | PASS, 30 passed / 0 failed / 1 ignored |
| Dependencies | `Cargo.toml` | `rusqlite` is optional behind the non-default `sqlite` feature; the default compiler/admission suite has no SQLite native build dependency |

Toolchain actually used: `cargo 1.100.0` / `rustc 1.100.0` on Linux x86_64. The default test command was also run with `CC=/bin/false` and `CXX=/bin/false`, confirming that it does not invoke a C compiler.

The 30 default tests comprise 23 compiler/execution-state tests and 7 admission-port tests. The one ignored feature-gated integration test exercises SQLite cross-connection transaction/locking serialization. It remains ignored in the ordinary feature-enabled suite because it requires an explicit integration run on a host with SQLite build/link support; it was also explicitly run with `-- --ignored` on this C-capable Linux host and passed (1 passed / 0 failed).

The default feature set can therefore be built and tested without a C toolchain. Enabling the optional `sqlite` adapter still builds bundled SQLite and requires a suitable C toolchain; the stated Windows machine still cannot run that one SQL integration test until it has SQLite build/link support. The port-level tests prove the in-memory admission semantics (idempotency, conflict detection, dependency completeness, state transitions, fence ordering and gate receipt behavior); neither they nor the local SQLite integration test prove production D/Storage/I integrations.
