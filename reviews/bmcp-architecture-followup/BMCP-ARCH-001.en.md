# BMCP Architecture Completion — Semantic Contract & Engineering Handoff

- Work Item: BMCP-ARCH-FOLLOWUP-001; Document: BMCP-ARCH-001; Version: 0.2.2
- Status: CANDIDATE / ARCHITECTURE_PARTIAL — not a frozen protocol specification
- Main baseline: c58878fce24528a0842b4f8887c93ddbf465b566
- H source snapshot: session-h-bmcp-protocol @ 3e8b33df18b9e6fc757ca84ff07a12faebc78e74
- Peers: [中文版本](BMCP-ARCH-001.zh-CN.md) | [English](BMCP-ARCH-001.en.md)
- Scope: architecture semantics, phase boundaries, dependency map, acceptance plan and engineering handoff.
- Excluded: Runtime code; H-owned normative wire/schema/transport/ACK/Validator edits; D/I authority changes; C's Agent/MCP-to-BMCP mapping decision. Owner Fact/Claim semantics are already decided; exact consumer/wire mapping remains Candidate.

## 1. Disposition

**ARCHITECTURE_PARTIAL.** This is a candidate semantic synthesis and engineering handoff, not a protocol freeze.

H's live branch contains candidate Envelope, versioning, canonicalization, error taxonomy, Delivery/ACK, Forget/reconnect, strict JSON parser reference and conformance material. These files remain H-owned; their existence is not approval or freeze. H's lifecycle handoff says Wire Schema NOT FROZEN; its conformance matrix is a candidate test specification, not Runtime evidence.

The merged Owner semantic decision approves Fact/Claim Option A + I1; exact compiler/domain consumer mapping remains Candidate. BMCP MUST NOT freeze canonical Fact/Claim wire payload fields. B owns semantic vocabulary and epistemic meaning. D owns canonical ID allocation, revision commit/currentness, lifecycle, lineage, ConflictSet and D ForgetOperation/Fence. I owns Principal/Actor authorization, attestor authorization, PermissionEpoch, revocation, retention/legal-hold/backup and global Forget policy/evaluation. BMCP/H/C consume opaque owner-issued refs and MUST NOT create substitutes.

Issue #7's recorded binding remains IMPLEMENTATION_BINDING=DEFERRED_TO_ENGINEERING_PHASE. GitHub currently reports Issue #7 CLOSED / not_planned under the Owner phase-closure ruling; this work does not reopen or alter it. Deferral is not Runtime authorization.

**Canonical name:** the repository canonical terminology at `00-governance/terminology.md` defines BMCP as **Brain Memory Context Protocol** (main `c58878fce24528a0842b4f8887c93ddbf465b566`, terminology Blob `b8770fbb58e4fac087698043c40a57531b1d244d`). The initial dispatch phrase “Brain Memory Control Protocol” is non-canonical for this repository and is rejected. H must retain “Context” in protocol documentation; no naming decision remains open.

## 2. Exact source ledger

Current main source pins are from fetched origin/main at c58878fce24528a0842b4f8887c93ddbf465b566. Historical decision/test evidence is separately labeled with its original commit where applicable. H pins are from H branch session-h-bmcp-protocol @ 3e8b33df18b9e6fc757ca84ff07a12faebc78e74.

| Source | Ref | Blob SHA | Status / use |
|---|---|---|---|
| 00-governance/terminology.md | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | b8770fbb58e4fac087698043c40a57531b1d244d | Canonical BMCP name / terminology authority |
| docs/en/08-bmcp-protocol/bmcp-guide.md | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | 228d28671955c977f653bef5b537554e431f9137 | CANDIDATE overview / H ownership |
| 08-bmcp-protocol/protocol-overview.md | H 3e8b33df18b9e6fc757ca84ff07a12faebc78e74 | b88ef3a6fd3be293e7c2e77d9652f386b169bc47 | CANDIDATE |
| 08-bmcp-protocol/message-envelope-and-versioning.md | same H ref | 5547ecd78d118bd63e571e5daad87194d9b694e4 | CANDIDATE; H-owned |
| 08-bmcp-protocol/context-delivery-and-acknowledgement.md | same H ref | bf9732cc39d156853b507c3a3a4e573159978f49 | CANDIDATE; G semantics / H wire |
| 08-bmcp-protocol/adapter-forget-ack-and-target-binding.md | same H ref | 5e2b33898cbc6a9c95e271ecd1d8a092d04c67f8 | CANDIDATE; H wire, D/I/G authority |
| 08-bmcp-protocol/phase-3.7-h-lifecycle-handoff-envelope-semantics-not-frozen.md | same H ref | b2a2648d5576511f68fdb9d87ce4388a1fedd5e9 | NOT FROZEN |
| 08-bmcp-protocol/protocol-conformance-matrix.md | same H ref | 075b2ac6ebe9bda4ec83de04fad07e8027e6a440 | CANDIDATE tests; no Runtime PASS |
| 08-bmcp-protocol/runtime_reference/strict_json_parser.py | same H ref | 3b9b3da645448c773c95a9dcd3c57c8c109bb2da | Reference model, not production transport |
| 08-bmcp-protocol/schemas/bmcp.recovery-join-1.0.2.schema.json | H @ `3e8b33df18b9e6fc757ca84ff07a12faebc78e74` | 4b664e3bce465499bcdfd93796349a4ba7074002 | H source schema; filename/$id is 1.0.2 but Envelope schema_version const is 1.0.0 |
| docs/en/04-memory-compiler/README.md | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | 5f50d470bf26d46dfffad48ad23059fc7a36c489 | E/D/I ownership |
| 06-memory-context/README.md | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | 684490d1c4e2c3aeb0236a9083abf9a144f2744c | G Context subsystem overview |
| 06-memory-context/context-architecture.md | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | 56fcc0ea112d423ef69a3f00e9d626bf4230ca0e | G Context architecture / ownership |
| 06-memory-context/context-versioning.md | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | 1bfe7f1891e1f9da1ff7508f4e25a11bbf7f649b | G ContextVersion / ChangeSet / CAS semantics |
| 06-memory-context/context-reconciliation.md | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | 87063aceebed1c30b7840045ada8e3f348732688 | G reconciliation semantics |
| 06-memory-context/context-manager.md | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | ecc0549137a1738c197d02d12d94a1eb971ed6b5 | G Context Manager boundary |
| docs/en/04-memory-compiler/compiler-overview.md | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | c89a256afda105ceac3db75d743ab58d177ef586 | E pipeline |
| docs/en/04-memory-compiler/accepted-receipt-and-idempotency-contract.md | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | f2a4007f4b17e33de9bcd183c57ee504cfeef6cd | CANDIDATE E receipt |
| docs/en/07-agent-integration/agent-integration-guide.md | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | c4e076887634a9e8e46df076efb0f4b70d816e0a | C-owned Agent boundary |
| docs/en/03-memory-brain/forget-fence-and-completion-contract.md | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | c791895333ab6140f035f4f622d5dee9325d422d | D/I Forget boundary |
| docs/en/03-memory-brain/forget-fence-operation-and-publication-gate.md | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | 9c054932994bb078e2834df8bd66f73895aa04f5 | D lifecycle/Fence |
| 13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/fact-claim-identity-adr.md | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | 958e7f3a3a909ee5b6d9fb38ebf3a72b3a9bd593 | historical ADR; semantic decision superseded; consumer mapping Candidate |
| 14-ai-development/adr/OWNER-DECISION-FACT-CLAIM-001.md | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` (approval origin `c138654c942dc93b5a36eccb2ff0e41452156429`) | Blob `d59756a8eb454480804c482ca03c68345ab5abf2` | Current source pin; Owner semantic approval is historical evidence (Option A + I1), not schema freeze |
| docs/en/03-memory-brain/memory-versioning.md | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | 4efbd26db9586f6fcf1897f42ffba287d625b903 | D revision/consumer freeze boundary |
| docs/en/03-memory-brain/commit-cursor-semantics.md | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | 2de7fe35229372ae5b06093e5e031c2c243fbd7c | D cursor semantics |
| docs/en/09-security-governance/security-governance-guide.md | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | 061c5847b3df879eeaf3c71e5eae0bfa162b276a | I Principal/authorization/PermissionEpoch |
| docs/zh-CN/09-security-governance/security-governance-guide.md | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | 372d27c79dc79d09bcdb0f142c979efdba1c2b6e | I bilingual peer |
| 07-agent-integration/agent-integration-overview.md | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | 073ff4ddf71fbcaf959107bb06ab724bfa48e63b | C canonical Agent boundary |
| 07-agent-integration/adapter-capability-tiers.md | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | ca422000ec98cca543fd96b59710346949f7d82e | C capability tiers |
| 07-agent-integration/inference-boundary-model.md | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | e2d5cb6abd9ec40da6e3680531de5944fc8b14df | C inference boundary |
| 07-agent-integration/telemetry-model.md | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | 9bb4a77e4bd79caaf3e1faeaf77c6b42858998f0 | C telemetry |
| 08-bmcp-protocol/protocol-index.md | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | a5b64941cdc783b385348de1b22e0eaace2c003d | Main BMCP protocol artifact index; RecoveryJoin 1.0.2 entry |
| 08-bmcp-protocol/protocol-index.zh-CN.md | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | 2fe06d9424821eb96eb006dbb391914c1375afae | BMCP 协议工件索引；RecoveryJoin 1.0.2 条目 |
| 08-bmcp-protocol/schemas/bmcp.recovery-join-1.0.2.schema.json | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | bbac8742401249230c629e858d033a09cd8f3acb | RecoveryJoin 1.0.2 structural JSON Schema; not H wire freeze |
| 08-bmcp-protocol/validators/recovery_join_validator.py | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | fe62c77e1db5ba28704267ac9dd80a2d396d1499 | Structural validation + injected D authority callbacks; candidate reference |
| 08-bmcp-protocol/tests/conformance/recovery_cutoff/test_recovery_join_1_0_2.py | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | 7ae54e0f7777ea2f41b7870e331aa8f388338a6c | RecoveryJoin 1.0.2 typed binding / unknown-state tests |
| 08-bmcp-protocol/tests/conformance/recovery_cutoff/test_recovery_join_schema_artifact.py | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | 3af71ec41cb3be968ebedd5d26a12291f1969b2e | RecoveryJoin schema/index/fixture tests |
| crates/memory-context/tests/e2e_negative_paths.rs | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | 8db9a6f573e3ce91136c2f2378ce50e902a0d079 | G cross-crate SQLite Store→Context negative E2E tests |
| crates/memory-store/src/lib.rs | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | 6059b3f088922c87f49993a6cbd80c49a884a1c8 | G MemoryStore implementation source |
| crates/memory-domain/src/lib.rs | main @ `c58878fce24528a0842b4f8887c93ddbf465b566` | b96cb2f74c56ab8a28da7e3ceffcf4adcb1b98d4 | Canonical Claim/Fact revision domain types |
| PR #436 protocol index/provider_outcome tests | PR head 1ffed9ed127df98b2f823a66ec80ea43d08cb9dc; merge commit 02f61194fd4e12993b4c83f7fac8382eee20f5d8 | merged into main | structural-only provider outcome evidence; 5 pass / 5 semantic skips |
| C family boundary decision | PR #430 comment 7060351480; Issue #449 comment 7060126722 | Owner-delegate decision; no independent human C signature claimed | Family direction decided; exact H operation registry/C-H mapping remains OPEN |
| H confirmation scope correction | PR #428 comment 7060351041; H scope correction comment 7060264372 | Owner-delegate logical choices only; INDEPENDENCE_UNVERIFIABLE | H-CONFIRM-001..004 each PARTIALLY_DECIDED / EXACT_ARTIFACT_MAPPING_OPEN |
| B domain-model-overview.md | B branch session-b-domain-model-phase3 @ 840202a98cf40a0b3f194afb84bed4d5f3326658 | Blob 4d1debc0ec19b3917f9e76d04bb66da4df4cd346 | B accepts Option A + I1; source reconciliation pending |
| D memory-versioning.md | D branch session-d-memory-brain-2026-11-16 @ b525e1f8fee2471a131e4a38efda99804045e424 | Blob af747f339d03bdd4684b6ed60fca05957dc8e1fb | D identity/revision/ConflictSet boundary; schema/currentness gate open |
| D forget-fence-and-completion-contract.md | same D ref | Blob 1f0391bc49d007c44ec74165bd33d37412cc7990 | D ForgetOperation/Fence authority |
| I principal-actor-and-authorization-contract.md | I branch session-i-security-governance-2026-11-16 @ 8abddf814467b271344a9814613a6b7ca6a446c6 | Blob 03765efac4bb1153f303ce0030f9e277d602e81d | I Principal/Actor/attestor authorization boundary |
| I scope-and-revocation-policy.md | same I ref | Blob 71df6aaf21bb1767cd9fe5c947581b871325e023 | I PermissionEpoch/revocation |
| I global-forget-target-inventory-and-completion-evidence.md | same I ref | Blob 9100061fa986fb6676656169de3fcf9fc1c72664 | I retention/global Forget evaluation |

The eight H Blob pins above were re-fetched from the live `session-h-bmcp-protocol` branch for this update; all eight resolve to the listed Blob SHAs at branch HEAD `3e8b33df18b9e6fc757ca84ff07a12faebc78e74`. This is a bounded source ledger, not a claim that every H artifact or consumer was independently reviewed.

### 2.3 B/D/I Owner decision pins

- B Owner decision: PR #429 comment 7060251435; B source branch `session-b-domain-model-phase3 @ 840202a98cf40a0b3f194afb84bed4d5f3326658`; `domain-model-overview.md` Blob `4d1debc0ec19b3917f9e76d04bb66da4df4cd346`.
- D Owner decision: PR #429 comment 7060243632; D source branch `session-d-memory-brain-2026-11-16 @ b525e1f8fee2471a131e4a38efda99804045e424`; `memory-versioning.md` Blob `af747f339d03bdd4684b6ed60fca05957dc8e1fb`; Forget contract Blob `1f0391bc49d007c44ec74165bd33d37412cc7990`.
- I Owner decision: PR #429 comment 7060259541; I source branch `session-i-security-governance-2026-11-16 @ 8abddf814467b271344a9814613a6b7ca6a446c6`; Principal/Actor contract Blob `03765efac4bb1153f303ce0030f9e277d602e81d`; Scope/Revocation Blob `71df6aaf21bb1767cd9fe5c947581b871325e023`; Global Forget inventory Blob `9100061fa986fb6676656169de3fcf9fc1c72664`.

## 3. File ownership matrix and allowed changes

| File / area | Owner | This work item | Boundary |
|---|---|---|---|
| 08-bmcp-protocol/** | H | Read only | No H schema, validator, ACK, transport or spec edits |
| docs/{en,zh-CN}/08-bmcp-protocol/** | H / docs governance | Read only | No guide/status rewrite |
| 04-memory-compiler/** and compiler docs | E; dependent semantics B/D/I | Read only | No Compiler or Fact/Claim changes |
| 07-agent-integration/** and C contract | C | Read only | No Agent/MCP policy changes |
| D Memory Brain / Forget contracts | D | Read only | No identity/lifecycle/Fence changes |
| I authorization / PermissionEpoch | I | Read only | No Principal/permission/global Forget changes |
| reviews/bmcp-architecture-followup/BMCP-ARCH-001.en.md | This BMCP architecture work item | Create | Candidate synthesis / handoff only |
| reviews/bmcp-architecture-followup/BMCP-ARCH-001.zh-CN.md | Same | Create | Semantic peer |
| docs/governance/translation-status.md | Governance register | Metadata-only | Register review pair; preserve H core-spec status |

No Rust source, tests, JSON Schema, transport/validator implementation or production configuration is in scope.

## 4. Parse / Execute / Respond contract

### 4.1 Layer boundary

1. **Wire / Transport Decode — H:** framing, channel authentication, bytes-to-text/UTF-8 decoding, strict wire syntax, canonicalization/integrity and envelope decoding.
2. **Protocol Parse — BMCP semantic layer:** accepts only a decoded envelope plus protected authenticated peer context; checks protocol requiredness, version/capability compatibility and registered family/operation; normalizes a typed request.
3. **Execute — operation owner/service:** routes to an allowlisted handler; obtains I authorization; validates D identity/lifecycle/Fence; invokes the owning domain service.
4. **Respond — BMCP semantics + H serialization:** builds a correlated business result or classified error. H owns wire representation and serialization.
5. **ACK — H evidence family:** independently reports transport or Adapter observation. ACK is not the business response or domain receipt.

Raw bytes MUST NOT enter BMCP semantic Parse. Co-location in a future process does not merge these authorities.

### 4.2 Parse

**Input:** H-decoded envelope and protected authenticated transport context. Payload identity is an assertion only; authenticated Principal comes from trusted channel/security context and I binding.

**Candidate logical fields:** protocol family/version; message identity; family+operation discriminator; payload and payload schema/content type; correlation and optional causation; idempotency tuple for state-changing operations; source/recipient selectors; conditional Scope/Environment refs; applicable owner-issued PermissionEpoch, ForgetFence, ContextVersion, CapabilityEpoch; expiry and integrity result.

H's candidate envelope names protocol, protocol_version, message_id, message_type, payload_content_type, payload_schema_version, payload, correlation_id, causation_id, idempotency, scope_ref, permission_epoch, forget_fence and capability_epoch. These are source names, **not approved field names/requiredness/schema**.

**Normalized internal request (not a wire schema):**

| Member | Meaning | Authority |
|---|---|---|
| protocol_version | negotiated version | H |
| message_id | immutable message identity; candidate request correlation key | H |
| correlation_id / causation_id | workflow correlation / immediate causal parent | H |
| operation_ref | registered family + operation | H registry; semantic owner defines operation |
| parameters | typed payload; opaque until owner validation | operation owner |
| idempotency_ref | owner-scoped key + canonical semantic digest | operation owner; H transports |
| authenticated_principal | protected peer identity, never payload-derived | I-approved binding |
| scope_ref / environment_ref | opaque typed domain refs | B/I/D as applicable |
| permission_epoch | I-issued authorization freshness | I |
| forget_fence_ref | D-issued barrier evidence with I policy binding as required | D/I |
| context_version / capability_epoch | independent opaque tokens | G / H |

Message identity, negotiated version, registered operation and typed payload are required at the semantic boundary. Correlation is required for multi-message/asynchronous operations. Idempotency is required for state-changing/retryable operations. Scope, Environment, PermissionEpoch, ForgetFence, ContextVersion and CapabilityEpoch are conditionally required by the operation owner; no wildcard default may be invented. Causation and namespaced non-critical extensions may be optional. Unknown critical fields/enums/operations fail closed under H's eventual compatibility contract.

Parse failures: malformed decoded envelope; missing required field; unsupported version; unknown operation; unsupported critical extension; invalid parameter shape; expired request. Parse MUST NOT call memory services, authorize side effects, mint identities or mutate domain state.

H's candidate negotiation forbids silent major downgrade. Exact major/minor/patch and payload-schema negotiation remain H-owned.

**H request-ID question:** current envelope defines message_id, not a separate request_id. H must decide whether message_id is the request identity referenced by response causation_id, or whether a distinct stable command identity is required. BMCP MUST NOT add a wire request_id unilaterally.

### 4.3 Execute

Execute begins only after Parse succeeds. This is a semantic dispatch contract, not a Runtime scheduler specification.

1. Resolve operation_ref through a versioned allowlisted registry; unknown/disabled operations reject before side effects.
2. Use protected authenticated identity and ask I's approved interface for current authorization and PermissionEpoch. Payload Principal/Actor/Producer/Scope claims do not authenticate themselves.
3. Invoke the operation owner's validator. H validates protocol/wire structure, not domain truth or business permission.
4. For canonical Memory operations, use D-owned identity/lifecycle/revision operations. BMCP does not mint CanonicalRef, choose lifecycle transitions or allocate canonical cursors.
5. Revalidate D Forget Fence and I authorization/PermissionEpoch at every D/I-protected boundary, including immediately before irreversible/visibility-changing work. Stale, unavailable, incomparable or unknown results block the action. D Fence and I PermissionEpoch are distinct typed namespaces; never compare/coerce/substitute.
6. Call the owning service (e.g. E ingress/receipt, D canonical lifecycle, G Context/Delivery). BMCP does not write canonical storage directly or implement the service state machine.
7. Same owner-scoped idempotency key + same semantic digest returns original operation/receipt without repeating side effects. Same key + different digest is conflict. Resolve uncertain commits using the same key and authoritative lookup; never mint a new key to escape UNKNOWN.
8. Timeout, lost response, process loss or uncertain durable outcome remains UNKNOWN until owner reconciliation. Timeout proves neither failure, abort, success nor non-invocation. Never blindly retry non-idempotent effects.
9. Concurrency follows owner CAS/sequencer/fence/transaction rules. BMCP message order, wall-clock time and correlation IDs are not domain commit order. Cancellation is not rollback.
10. Return the actual owner receipt/result without upgrading its meaning. E AcceptedReceipt means durable ingress acceptance under E's contract; it does not mean compile, canonical commit, publication or Applied.

No concrete operation catalogue or callable Runtime service API is frozen here.

### 4.4 Respond

A business response is the semantic result of an operation; an ACK is a separate transport/Adapter observation.

Logical response: negotiated protocol version; new immutable response message identity; request association; operation discriminator; mutually exclusive success/result or failure/error; owner-issued result/receipt/evidence refs; and H-approved safe retry metadata.

**Candidate correlation:** response causation_id references request message_id; response correlation_id preserves workflow correlation; response has its own message_id. H must confirm; this is not a frozen wire rule.

Success exists only when the operation owner returns its defined successful terminal/receipt. Transport send success, HTTP 2xx, queue acceptance or ACK receipt is not business success. Failure preserves the owner's outcome and distinguishes pre-execution rejection, domain conflict, authorization denial, timeout/unknown and internal failure. UNKNOWN must not become definitive success/failure.

H owns response field names, encoding, canonicalization, signatures, versioning and transport. Redact protected payloads, secrets, credentials, internal paths and cross-scope existence. Existence disclosure follows I policy. Stable code, correlation and retryability are returned only when safe; detailed diagnostics stay in protected logs.

## 5. ACK, Validator and error semantics

### 5.1 ACK (H-owned)

H's candidate design distinguishes Prepared/Delivered/Applied/Rejected/Expired/Superseded/Unknown and separate Forget ACK classes such as SUPPRESSED, local buffer/cache/queue action, FAILED and UNKNOWN. A Forget ACK is not an Applied ACK.

| Question | Current evidence | Disposition |
|---|---|---|
| Purpose | bounded observation for one identified message/delivery/action | H candidate |
| Receipt? | some ACKs report transport/delivery receipt; boundary varies by family | H must map each family |
| Execution complete? | no general inference | H confirmation |
| Durable persistence? | only owner-specific receipt proves its durable boundary | E/Storage + H mapping |
| Timeout/lost ACK | Unknown until reconciliation | H candidate; retry profile H-owned |
| Duplicate ACK | same stable ACK ID+digest idempotent; same ID/different digest conflict | H candidate; consumer owns state |
| Correlation | exact operation/delivery/attempt/session/target/evidence tuple | H wire mapping; D/G/I consume |

H must confirm ACK families, evidence boundary, persistence point, correlation tuple, retry horizon, replay/retention and consumer mapping. This document does not design ACK.

### 5.2 Validator layers

| Layer | Owner | Input | Output / failure |
|---|---|---|---|
| Transport framing, byte decode, UTF-8, duplicate-key/canonical JSON, integrity, authenticated channel | H using I-approved trust | raw bytes/channel | decoded authenticated envelope or wire rejection; no business execution |
| Envelope structure, protocol version, required/critical fields, registered family | H | decoded envelope | protocol-valid envelope or H error |
| Operation parameter shape/schema | H for protocol schema mechanics; operation owner for semantic constraints | typed payload + registry entry | valid shape or validation rejection; schema version pinned |
| Business authorization / PermissionEpoch | I | authenticated Principal + operation + scope + current epoch | allow/deny/unknown; unknown fail-closed |
| Canonical identity/lifecycle/Forget Fence | D; I for policy binding | typed canonical refs + operation + fence context | owner-authenticated validity/currentness or reject/unknown |
| Fact/Claim schema and identity | B decision, D identity/lifecycle, E candidate producer | Candidate IR / proposed canonical object | BLOCKED until ADR and consumer acceptance |
| ContextVersion / ChangeSet / Delivery | G | Context payload + exact base/target | G validation result; H only encodes/transports |
| Runtime result/receipt | executing domain owner | validated and authorized operation | owner result/receipt; H Validator cannot infer |

H Validator MUST NOT become the business authorization engine, canonical schema authority or Forget/PermissionEpoch authority.

### 5.3 Error taxonomy (candidate crosswalk, not frozen enum)

H's candidate envelope lists ENVELOPE_INVALID, VERSION_UNSUPPORTED, MESSAGE_TYPE_UNSUPPORTED, REQUIRED_FIELD_UNSUPPORTED, ENUM_UNSUPPORTED, INTEGRITY_FAILED, AUTHENTICATION_FAILED, IDENTITY_BINDING_MISMATCH, NOT_AUTHORIZED, PERMISSION_EPOCH_STALE, FENCE_STALE, CONTEXT_BASE_MISMATCH, DUPLICATE_REPLAY, IDEMPOTENCY_CONFLICT, EXPIRED, SUPERSEDED, RATE_LIMITED, RESOURCE_EXHAUSTED, TRANSIENT_UNAVAILABLE and INTERNAL_ERROR. They remain candidate pending H's exact versioned contract.

| Requested class | Existing H candidate / gap | Status |
|---|---|---|
| INVALID_REQUEST | ENVELOPE_INVALID; alias/scope needs H | BLOCKED_BY_H_CONTRACT |
| UNSUPPORTED_VERSION | VERSION_UNSUPPORTED | BLOCKED_BY_H_CONTRACT |
| INVALID_PARAMETERS | no exact generic code; owner-specific validation may apply | BLOCKED_BY_H_CONTRACT |
| UNKNOWN_OPERATION | MESSAGE_TYPE_UNSUPPORTED | BLOCKED_BY_H_CONTRACT |
| UNAUTHORIZED | distinguish authentication from I policy denial: AUTHENTICATION_FAILED vs NOT_AUTHORIZED | BLOCKED_BY_H_CONTRACT |
| FORBIDDEN | candidate NOT_AUTHORIZED; I controls concealment vs not-found | BLOCKED_BY_H_CONTRACT |
| NOT_FOUND | no generic H code confirmed; I controls existence disclosure | BLOCKED_BY_H_CONTRACT |
| CONFLICT | specific candidates IDEMPOTENCY_CONFLICT, CONTEXT_BASE_MISMATCH, FENCE_STALE, SUPERSEDED; no frozen generic code | BLOCKED_BY_H_CONTRACT |
| VALIDATION_FAILED | keep protocol, domain-schema, authorization and integrity failures distinct | BLOCKED_BY_H_CONTRACT |
| EXECUTION_FAILED | owner defines definitive failure vs UNKNOWN; H mapping unconfirmed | BLOCKED_BY_H_CONTRACT |
| TIMEOUT | uncertain side-effect boundary means UNKNOWN; TRANSIENT_UNAVAILABLE does not prove failure | BLOCKED_BY_H_CONTRACT |
| INTERNAL_ERROR | candidate INTERNAL_ERROR; redaction/retry policy needs H | BLOCKED_BY_H_CONTRACT |

Conceptual error response: stable code, retryable flag, optional safe retry-after, correlation ref and sanitized detail. Exact fields, mapping and retry policy belong to H. Do not ship requested labels as wire enums without H approval.

## 6. Cross-module dependency matrix

| Module | Authority | BMCP consumes / interaction | Open dependency |
|---|---|---|---|
| H | wire envelope/version, transport, ACK encoding, Validator, protocol conformance | authenticated decoded envelope; family registry; response/ACK serialization | exact Wire/Transport/ACK/Validator remains CANDIDATE / NOT FROZEN |
| E | ingress acceptance, Candidate IR, compiler stages/lineage, AcceptedReceipt | typed ingress operation; return E receipt/result unchanged | callable API and wire mapping; AcceptedReceipt is not canonical commit |
| B | Fact/Claim meaning and canonical domain decisions | only owner-approved typed refs/payloads | Owner decision Option A + I1 approved; exact consumer mapping Candidate |
| D | canonical identity, lifecycle, canonical commit/revision, Forget Fence | pass typed refs to D and consume D receipts/currentness | exact Runtime API binding |
| I | Principal trust, authorization, PermissionEpoch, revocation, global Forget policy | protected principal context and current authorization decision | exact approved interface/profile |
| C | Agent/Adapter boundary, telemetry, final inference request | C adapter maps Agent request to registered BMCP operation | MCP/Adapter mapping and request identity |
| G | Context membership/version, ChangeSet, delivery intent, Applied state | carry Context operations and evidence; G decides Context/Applied | exact field/API mapping and consumer acceptance |
| Storage | durable transaction, visibility and persistence | only through owning service; receipts passed through | no direct BMCP-to-Storage write path; topology deferred |

### 6.1 Memory Compiler

BMCP is not the Memory Compiler. E owns Candidate IR and the compiler pipeline. BMCP may carry an E-owned ingress/candidate object only under E's current schema/receipt contract. Preserve the distinctions: transport receipt/delivery; E durable AcceptedReceipt; compiler execution/candidate; D producer admission/canonical commit; dependency registration/final publication; F indexing/G Context activation.

The merged Owner decision selects Option A + I1 for Fact/Claim semantics. This does not approve a Fact/Claim discriminator, canonical wire identity, schema, DDL or payload fields. Exact consumer mappings remain Candidate until responsible artifacts are version-pinned and reviewed; keep dependent payload opaque or use only approved candidate-neutral refs.

### 6.2 Agent Integration / MCP

C owns Agent/Adapter semantics; H owns BMCP wire/transport. MCP is the Agent Host ↔ C northbound tool/resource interface. BMCP is the C Agent Adapter ↔ Memory Brain protocol boundary via H. MCP methods are not BMCP messages; an MCP Server is a C-owned Agent Adapter/Gateway, not BMCP and not a parallel canonical Brain API. A C MCP Server may cross into BMCP only through a registered H family/operation whose exact versioned contract is pinned and accepted. Agent, Agent Runtime, Model, Provider, Tool, Session and Principal remain distinct.

| Logical BMCP family | Direction relative to C Adapter | C disposition for MCP mapping |
|---|---|---|
| Telemetry | Agent/Adapter → Brain | Agent-facing tool only after H registers the exact operation and I/C identity/authorization binding is accepted |
| Event Ingress | Producer/Agent → Brain | Only through H's registered ingress operation and E durable receipt/idempotency contract; MCP result is not E acceptance unless the E receipt is returned |
| Context Snapshot | Brain → Adapter | Inbound delivery to C; not a generic MCP request/response operation |
| Context Delta | Brain → Adapter | Inbound delivery to C; G owns version/base/ChangeSet semantics; not a generic MCP request/response operation |
| Delivery | Brain → Adapter | Inbound H/G delivery lifecycle; C applies only the managed region at the declared inference boundary |
| Acknowledgement | Adapter → Brain | C emits H-defined evidence; not MCP success and not a substitute for G Applied |
| Forget / Revocation | Brain/I → Adapter, with authorized control requests | C consumes D/I owner-issued controls; Agent-facing requests route only to I/D-authorized operations, never a C-local Forget implementation |
| Administrative Governance | I/control plane → Adapter/Gateway | Control-plane only; no ordinary Agent tool exposure absent explicit I policy and H operation registration |

F-owned Retrieval/Recall is not a BMCP message family in the current H family inventory. C MUST NOT invent a BMCP Search operation. Any future MCP memory-search tool requires a separately pinned F-owned query API and I/D authorization path; until then it is unavailable / dependency-not-ready.

Identity mapping is logical only: C retains AgentRequestId, AgentAttemptId, AgentTurnId and AgentSessionId as C-owned identities. H `message_id` identifies each BMCP message; H `correlation_id` groups the workflow; H `causation_id` identifies the immediate parent BMCP message/event. AgentRequestId may be a local workflow-correlation input, but MUST NOT be serialized as a newly invented H `request_id`; each H message has its own H `message_id`. AgentAttemptId is not a transport attempt ID or operation idempotency key. State-changing operations use the operation owner's idempotency identity plus canonical payload digest; same identity/digest replays, while same identity/different digest conflicts.

C may provide final-request-boundary evidence only at the declared capability tier; H transports it and G owns Applied acceptance. MCP tool success, HTTP 2xx, H transport ACK, E AcceptedReceipt and G Applied are distinct outcomes. This is a family-level routing decision only: MCP tool/resource names, schemas, H operation IDs/registry, exact wire fields, ACK schema, transport and consumer acceptance remain OPEN under Issue #449.

### 6.3 D/I

D is authoritative for Canonical Identity/Lifecycle and D-issued Forget Fence. I is authoritative for Principal trust, authorization, PermissionEpoch and global Forget policy. BMCP carries opaque issuer-typed refs and asks the issuing authority to validate currentness. It creates no parallel identity, authorization, epoch, fence or global completion mechanism. PermissionEpoch and ForgetFenceGeneration are distinct namespaces. If either authority is unavailable or returns stale/unknown/incomparable evidence, protected memory remains suppressed and execution stops.

## 7. H confirmation and Owner decision requests

H-owned questions go to H first; they are not disguised as Owner decisions.

### 7.1 H confirmation requests

**H-CONFIRM-001 — Envelope / request identity**
- MODULE: BMCP / H
- ISSUE_OR_ADR: H message-envelope-and-versioning.md; protocol-overview.md
- DECISION_REQUIRED: whether message_id is the request identity or a distinct request_id; exact response correlation; requiredness of version/type/payload schema/idempotency; operation registry and unknown-operation behavior.
- CURRENT_FACTS: canonical BMCP expansion is settled by `00-governance/terminology.md` as Brain Memory Context Protocol. H envelope remains CANDIDATE; current candidate uses message_id and does not define a separate request_id.
- H_OWNED_CONTRACTS: envelope, versioning and wire names remain H-owned.
- CROSS_MODULE_CONFLICT: C Request/Attempt IDs, H Message ID and domain Operation ID are not interchangeable.
- OPTIONS: (A) use message_id as request identity and bind response causation to it; (B) introduce a distinct request_id/command identity with explicit message_id mapping.
- RECOMMENDED_OPTION: logical identity concepts are decided as distinct: message_id, correlation_id, causation_id and operation-level idempotency. Operation registry, per-family field requiredness and exact request/response schema remain OPEN.
- MEMORY_COMPILER_IMPACT: E receipt/idempotency identity remains distinct.
- AGENT_INTEGRATION_IMPACT: C request/attempt mapping must be explicit.
- D_I_IMPACT: no authority changes; identity claims still validated by D/I.
- RUNTIME_IMPLEMENTATION_IMPACT: request/response correlation blocked pending H mapping.
- REQUIRED_AUTHORITY: H, with C/E/G consumer review.
- OWNER_DECISION: PARTIALLY_DECIDED / EXACT_ARTIFACT_MAPPING_OPEN; INDEPENDENCE_UNVERIFIABLE
- EVIDENCE: `00-governance/terminology.md` Blob b8770fbb58e4fac087698043c40a57531b1d244d; H envelope Blob 5547ecd78d118bd63e571e5daad87194d9b694e4.
- FOLLOW_UP_ACTIONS: H publishes versioned mapping; consumers review.

**H-CONFIRM-002 — Wire decode / Parse boundary**
- MODULE: BMCP / H
- ISSUE_OR_ADR: H envelope and strict JSON reference
- DECISION_REQUIRED: exact split for transport framing, byte decoding, canonicalization/integrity and post-decode protocol Parse; duplicate keys, invalid UTF-8/Unicode, depth/size and critical extensions.
- CURRENT_FACTS: RFC 8785 JCS is selected as the logical JSON canonicalization basis. Exact signed-object bytes, digest exclusion, signature suite, key lifecycle and I crypto-profile acceptance remain OPEN. Strict parser is a reference model, not production transport; semantic Parse here accepts decoded authenticated envelopes only.
- H_OWNED_CONTRACTS: raw Wire Decode and envelope structural validation.
- CROSS_MODULE_CONFLICT: H byte-decoding/transport duties must not move into BMCP semantics.
- OPTIONS: H owns raw bytes/envelope validation; BMCP owns operation resolution/request normalization.
- RECOMMENDED_OPTION: keep this split.
- MEMORY_COMPILER_IMPACT: E receives only parsed typed ingress requests.
- AGENT_INTEGRATION_IMPACT: Adapter/gateway uses H transport boundary.
- D_I_IMPACT: no authority change.
- RUNTIME_IMPLEMENTATION_IMPACT: raw bytes must not enter semantic parser.
- REQUIRED_AUTHORITY: H.
- OWNER_DECISION: PARTIALLY_DECIDED / EXACT_ARTIFACT_MAPPING_OPEN; INDEPENDENCE_UNVERIFIABLE
- EVIDENCE: strict parser Blob 3b9b3da645448c773c95a9dcd3c57c8c109bb2da.
- FOLLOW_UP_ACTIONS: H publishes stage contract and vectors.

**H-CONFIRM-003 — ACK families / retry**
- MODULE: BMCP / H
- ISSUE_OR_ADR: H delivery/ACK and Forget ACK contracts
- DECISION_REQUIRED: ACK family, exact evidence boundary, persistence point, correlation tuple, duplicate/replay handling, retry horizon and consumer.
- CURRENT_FACTS: ACK evidence must be durably recorded before transmission and replayed idempotently; missing ACK remains UNKNOWN. H separates Delivery lifecycle, Forget action ACK and Applied. Physical persistence topology/adapter and Storage acceptance remain OPEN.
- H_OWNED_CONTRACTS: ACK wire/transport encoding and retransmission behavior.
- CROSS_MODULE_CONFLICT: generic ACK must not imply execution, durable commit, Applied or Forget completion.
- OPTIONS: keep separate ACK families, each one bounded observation.
- RECOMMENDED_OPTION: retain separation and explicit consumer mapping.
- MEMORY_COMPILER_IMPACT: E AcceptedReceipt remains distinct from transport ACK.
- AGENT_INTEGRATION_IMPACT: Adapter reports only observable boundary.
- D_I_IMPACT: D/I independently evaluate Fence/target satisfaction.
- RUNTIME_IMPLEMENTATION_IMPACT: ACK implementation waits for H and consumer acceptance.
- REQUIRED_AUTHORITY: H; D/I/G/E review their own consumption.
- OWNER_DECISION: PARTIALLY_DECIDED / EXACT_ARTIFACT_MAPPING_OPEN; INDEPENDENCE_UNVERIFIABLE
- EVIDENCE: H ACK Blob 5e2b33898cbc6a9c95e271ecd1d8a092d04c67f8.
- FOLLOW_UP_ACTIONS: H publishes ACK-to-consumer matrix.

**H-CONFIRM-004 — Validator / error mapping**
- MODULE: BMCP / H
- ISSUE_OR_ADR: H envelope and conformance matrix
- DECISION_REQUIRED: validator layers, canonical error enum, response schema, retryability/redaction; map ten logical error classes without collapsing authn/authz/validation/conflict/unknown.
- CURRENT_FACTS: fail-closed validation order and distinct logical error classes are DECIDED. Exact enum spellings, wire schema, retry profile and owner-specific error mapping remain OPEN; current H taxonomy is still candidate at wire level.
- H_OWNED_CONTRACTS: wire/protocol Validator and error serialization.
- CROSS_MODULE_CONFLICT: domain validators and I authorization remain owner-owned.
- OPTIONS: preserve specific H codes; add aliases only with lossless versioned mapping.
- RECOMMENDED_OPTION: retain specific classes; publish layered validation and mapping.
- MEMORY_COMPILER_IMPACT: E errors remain distinct from protocol errors.
- AGENT_INTEGRATION_IMPACT: C maps Agent-facing errors without changing canonical meaning.
- D_I_IMPACT: D/I decisions remain authoritative.
- RUNTIME_IMPLEMENTATION_IMPACT: error mapping blocked until H contract.
- REQUIRED_AUTHORITY: H; domain owners approve their outcomes.
- OWNER_DECISION: PARTIALLY_DECIDED / EXACT_ARTIFACT_MAPPING_OPEN; INDEPENDENCE_UNVERIFIABLE
- EVIDENCE: H envelope Blob 5547ecd78d118bd63e571e5daad87194d9b694e4.
- FOLLOW_UP_ACTIONS: H publishes taxonomy and vectors.


### 7.1.1 H logical confirmation dispositions — PARTIALLY_DECIDED / EXACT_ARTIFACT_MAPPING_OPEN

**Authority/capacity:** consolidated Project Owner delegate acting in the H protocol-owner role under Issue #305 comment 7042461592 and the Owner's standing instruction. This is not an independent human H signature. Evidence posture remains `INDEPENDENCE_UNVERIFIABLE`.

**Exact H source snapshot:** branch `session-h-bmcp-protocol` @ `3e8b33df18b9e6fc757ca84ff07a12faebc78e74`.
- Protocol overview Blob: `b88ef3a6fd3be293e7c2e77d9652f386b169bc47`
- Message envelope/versioning Blob: `5547ecd78d118bd63e571e5daad87194d9b694e4`
- Context delivery/acknowledgement Blob: `bf9732cc39d156853b507c3a3a4e573159978f49`
- Adapter Forget ACK/target binding Blob: `5e2b33898cbc6a9c95e271ecd1d8a092d04c67f8`
- Strict JSON parser reference Blob: `3b9b3da645448c773c95a9dcd3c57c8c109bb2da`
- Phase 3.7 lifecycle handoff Blob: `b2a2648d5576511f68fdb9d87ce4388a1fedd5e9`
- Protocol conformance matrix Blob: `075b2ac6ebe9bda4ec83de04fad07e8027e6a440`

#### H-CONFIRM-001 — Message/request identity: PARTIALLY_DECIDED / EXACT_ARTIFACT_MAPPING_OPEN

- `message_id` is the unique immutable identity of one BMCP message.
- `correlation_id` groups one workflow/turn/delivery; `causation_id` identifies the immediate parent message/event.
- State-changing/retryable operations additionally require owner-scoped idempotency identity plus canonical payload digest.
- There is **no separate core envelope `request_id`** in the current H candidate. C retains AgentRequestId and AgentAttemptId as C-owned identities. C maps one Agent request to one or more BMCP messages using correlation/causation without collapsing Agent request, Agent attempt, BMCP message, transport attempt or idempotency identity.
- This accepts logical identity separation only; field encoding, namespace syntax and wire schema are not frozen.

#### H-CONFIRM-002 — Raw Wire Decode vs semantic Parse: PARTIALLY_DECIDED / EXACT_ARTIFACT_MAPPING_OPEN

- H owns authenticated transport binding, framing/raw-byte intake, strict UTF-8/JSON decoding, duplicate-key/non-finite/depth/size rejection, envelope structural validation, protocol version/capability and integrity checks.
- BMCP semantic Parse begins only after successful decode and envelope validation. It resolves registered family/operation and dispatches to the owning domain authority.
- Semantic Parse MUST NOT re-parse raw bytes or bypass H's strict decoder. H decode MUST NOT infer B/D/E/F/G/I business semantics.
- The strict parser Blob is a non-production reference model, not a Runtime parser or implementation PASS.

#### H-CONFIRM-003 — ACK family/evidence/retry: PARTIALLY_DECIDED / EXACT_ARTIFACT_MAPPING_OPEN

- Delivery lifecycle remains Prepared / Delivered / Applied / Rejected / Expired / Superseded / Unknown. Timeout or missing evidence is Unknown, never inferred success.
- Delivered proves transport endpoint receipt only. Applied is accepted only with G-owned context/application semantics and required C inference-boundary evidence; H transports/verifies evidence but does not mint G Applied.
- Forget ACKs are separate from Applied. Adapter-local SUPPRESSED, LOCAL_BUFFER_CLEARED, LOCAL_CACHE_PURGED, QUEUED_DELIVERY_CANCELLED, FAILED, UNKNOWN and UNSUPPORTED prove only the declared target/region/session/capability slice. I alone evaluates global target satisfaction and PolicyException.
- ACK identity/evidence digest is stable for one completed action; retransmission reuses it. Transport attempt identity may change. Same operation key + same target digest is idempotent; same key + different digest is conflict. Missing ACK after local success remains Unknown until query/reconciliation.
- No ACK implies model attention, comprehension, provider deletion, physical erasure or global Forget completion.

#### H-CONFIRM-004 — Validator layers/error mapping: PARTIALLY_DECIDED / EXACT_ARTIFACT_MAPPING_OPEN

1. Transport/security integration authenticates peer/workload Principal; I owns Principal and authorization policy. Payload identity fields are assertions only.
2. H validates raw syntax, envelope requiredness/unknown-critical behavior, protocol version/capability, integrity, replay and idempotency.
3. Domain validators remain with their authorities: B semantics; D canonical identity/lifecycle/ForgetFence; E admission/receipt; F retrieval; G ContextVersion/delivery/Applied; I authorization/PermissionEpoch/Forget policy.
4. C owns final inference-request boundary evidence; H cannot infer Applied from a transport ACK.
5. Error classes preserve Authentication, Authorization, Validation, Unsupported, Conflict, Expired, RateLimited/ResourceExhausted, Internal and Unknown. Existing code labels remain Candidate until H's separate versioned wire contract is reviewed; no error enum is frozen.

**Current status for each of H-CONFIRM-001..004:** `PARTIALLY_DECIDED / EXACT_ARTIFACT_MAPPING_OPEN`, with `INDEPENDENCE_UNVERIFIABLE`. The logical decisions recorded in PR #428 comments 7060351041 and 7060264372 are accepted only within their stated scope; exact registry/schema/requiredness/crypto/persistence/error/consumer artifacts remain open. Do not mark H's seven normative core specifications complete or claim independent H signature, cross-owner consumer acceptance, or H implementation/conformance closure.

### 7.1.2 H scope correction — logical decision vs exact artifact status

H scope correction is recorded in PR #428 comment 7060264372. The four requests are **not fully closed**:
- H-CONFIRM-001: logical message identity, workflow correlation, immediate causation and operation idempotency are DECIDED. Operation-family registry, per-family field requiredness, exact request/response schema and exact wire names/types remain OPEN.
- H-CONFIRM-002: RFC 8785 JCS is selected as the logical canonicalization basis. Exact signed-object bytes, digest exclusion, signature suite, key lifecycle and I cryptographic-profile acceptance remain OPEN.
- H-CONFIRM-003: durable ACK record before transmission and idempotent replay are DECIDED; missing ACK remains UNKNOWN. Physical persistence topology/adapter and Storage acceptance remain OPEN.
- H-CONFIRM-004: fail-closed validation order and distinct logical error classes are DECIDED. Exact enum spellings, wire schema, retry profile and owner-specific mapping remain OPEN.

The earlier broad acceptance wording is superseded by this scope correction. H remains the owner of exact normative wire artifacts; no schema, crypto profile, persistence topology or error enum is frozen here.

### 7.2 Owner decision requests

**DECISION_REQUEST_ID: BMCP-DR-001**
- MODULE: BMCP
- ISSUE_OR_ADR: B-ADR-FACT-CLAIM-001 (13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/fact-claim-identity-adr.md)
- DECISION_REQUIRED: reconcile B-ADR-FACT-CLAIM-001 with the Owner semantic selection, then complete the required consumer mapping and acceptance before any canonical schema or wire-field freeze.
- CURRENT_FACTS: The merged Owner decision record `OWNER-DECISION-FACT-CLAIM-001` (main Blob `d59756a8eb454480804c482ca03c68345ab5abf2`; PR #446 merge commit `ad5ca81a32b413aef3f9b5bccd06030aabde8275`) selects Option A (separate Fact attestation and Claim proposition) with I1 (stable Claim identity plus immutable ClaimRevision). It supersedes the B ADR as the live semantic decision request; the B ADR remains historical evidence. Exact consumer implementation mappings, migration/compatibility and conformance remain Candidate until responsible artifacts are version-pinned and reviewed; no wire fields are approved.
- H_OWNED_CONTRACTS: future wire field/schema mapping remains H-owned and unfrozen; this semantic selection approves no wire field.
- CROSS_MODULE_CONFLICT: semantic direction is selected, but E Candidate IR, D identity/lifecycle, I authorization/attestor policy, and H payload mapping still require exact consumer acceptance and source pins before a shared schema can be frozen.
- OPTIONS: (A) preserve the selected Option A + I1 semantic direction while keeping payload fields opaque until the 消费者契约验收 gate is complete; (B) reopen the semantic choice only through a superseding Owner decision.
- RECOMMENDED_OPTION: A; do not treat semantic selection as schema approval.
- MEMORY_COMPILER_IMPACT: E remains candidate-neutral; no canonical Fact/Claim output schema.
- AGENT_INTEGRATION_IMPACT: C carries only opaque approved refs.
- D_I_IMPACT: D/I semantics unchanged; review consumers after B decision.
- RUNTIME_IMPLEMENTATION_IMPACT: no final Fact/Claim payload/schema/migration until decision.
- REQUIRED_AUTHORITY: Owner semantic selection is recorded in PR #446 (merged) under the standing Owner instruction; B/D/E/F/G/H/I consumer mapping and acceptance remain required for schema freeze.
- OWNER_DECISION: SEMANTIC_DIRECTION_APPROVED_OPTION_A_I1; WIRE_SCHEMA_MAPPING_CANDIDATE
- EVIDENCE: `OWNER-DECISION-FACT-CLAIM-001` PR #446 (merged) @ `ad5ca81a32b413aef3f9b5bccd06030aabde8275`; B ADR Blob 958e7f3a3a909ee5b6d9fb38ebf3a72b3a9bd593.
- FOLLOW_UP_ACTIONS: B updates ADR status/source pins; D/E/F/G/H/I record exact consumer mappings and acceptance; publish migration/compatibility plan and conformance scenarios; keep payload opaque until responsible consumer artifacts are version-pinned and reviewed.

**DECISION_REQUEST_ID: BMCP-DR-002**
- MODULE: BMCP
- ISSUE_OR_ADR: D canonical identity/lifecycle and Forget Fence; I authorization/PermissionEpoch contracts
- DECISION_REQUIRED: publish exact callable authority interfaces, typed request/receipt and currentness result vocabulary BMCP must consume; no ownership/semantics change requested.
- CURRENT_FACTS: D owns canonical identity/lifecycle and D Fence; I owns authorization/PermissionEpoch; H envelope references depend on these contracts.
- H_OWNED_CONTRACTS: H maps approved refs to wire fields after D/I publish.
- CROSS_MODULE_CONFLICT: ownership is clear; exact callable interfaces/error mappings are not established in the mainline guide.
- OPTIONS: (A) publish versioned D/I service contracts and H mapping; (B) keep refs opaque until then.
- RECOMMENDED_OPTION: D/I authority boundaries are DECIDED; exact callable API/IDL/currentness vocabulary remains OPEN and must be published by D/I. Until then BMCP carries opaque owner-issued refs and fails closed; H/BMCP/C MUST NOT invent authority APIs.
- MEMORY_COMPILER_IMPACT: E consumes D/I semantics without copying authority.
- AGENT_INTEGRATION_IMPACT: MCP/Adapter cannot bypass D/I.
- D_I_IMPACT: no authority change; exact interface publication and consumer review only.
- RUNTIME_IMPLEMENTATION_IMPACT: protected handlers blocked until API/currentness evidence exists.
- REQUIRED_AUTHORITY: D and I; H confirms wire mapping afterwards.
- OWNER_DECISION: DECIDED_AT_AUTHORITY_BOUNDARY; EXACT_CALLABLE_API_IDL_SCHEMA_DEFERRED_TO_D_I_VERSIONED_CONTRACTS; H/BMCP/C MUST NOT INVENT AUTHORITY API OR CURRENTNESS SEMANTICS
- EVIDENCE: H overview Blob b88ef3a6fd3be293e7c2e77d9652f386b169bc47; D Forget Blob c791895333ab6140f035f4f622d5dee9325d422d.
- FOLLOW_UP_ACTIONS: D/I reconcile their existing source/mirrors and publish versioned callable contracts/IDL/currentness vectors; H maps only after publication; BMCP consumes exact owner-issued refs and updates its crosswalk.

**DECISION_REQUEST_ID: BMCP-DR-003**
- MODULE: BMCP
- ISSUE_OR_ADR: C Agent Integration canonical contract / guide
- DECISION_REQUIRED: confirm Agent/MCP-to-BMCP operation mapping, Request/Attempt/Message identity, authenticated Principal handoff and final inference boundary.
- CURRENT_FACTS: C Owner comment PR #430 comment 7060351480 decides family-level routing. MCP is Agent Host ↔ C northbound; BMCP is C Agent Adapter ↔ Brain via H. The logical family matrix and identity mapping are recorded in §6.2. Issue #449 comment 7060126722 supplies the binding semantic direction.
- H_OWNED_CONTRACTS: H owns exact operation IDs/registry, versioned schemas, wire fields, ACK encoding and transport. C cannot invent H fields or operation IDs.
- CROSS_MODULE_CONFLICT: Family direction is decided, but exact H operation registry, schemas, C tool/resource names and C/H consumer acceptance remain OPEN under Issue #449. MCP tool success, BMCP business outcome, transport ACK, E receipt and G Applied remain distinct.
- OPTIONS: (A) C-owned MCP Agent Adapter/Gateway maps to registered H BMCP families/operations; (B) MCP exposes a parallel canonical Brain API.
- RECOMMENDED_OPTION: A is DECIDED at family-routing level; reject B. Keep exact C/H operation mapping OPEN until pinned H contracts and consumer acceptance exist.
- MEMORY_COMPILER_IMPACT: MCP ingress still uses E AcceptedReceipt and D admission.
- AGENT_INTEGRATION_IMPACT: C retains AgentRequestId/AgentAttemptId/AgentTurnId/AgentSessionId; maps workflow correlation to H correlation_id without adding request_id; exact C tool/resource and H operation bindings remain open.
- D_I_IMPACT: canonical identity/lifecycle and authorization remain D/I-owned.
- RUNTIME_IMPLEMENTATION_IMPACT: gateway waits for H mapping and C acceptance.
- REQUIRED_AUTHORITY: C + H; D/I review authority-bearing identity mapping.
- OWNER_DECISION: PARTIALLY_DECIDED; MCP_IS_AGENT_HOST_TO_C_NORTHBOUND; BMCP_IS_C_ADAPTER_TO_BRAIN_VIA_H; FAMILY_DIRECTION_DECIDED_PER_PR_430_COMMENT_7060351480; EXACT_H_OPERATION_IDS_SCHEMAS_C_TOOL_RESOURCE_NAMES_AND_CONSUMER_ACCEPTANCE_OPEN_UNDER_ISSUE_449
- EVIDENCE: C guide Blob c4e076887634a9e8e46df076efb0f4b70d816e0a; `07-agent-integration/agent-integration-overview.md` and `08-bmcp-protocol` ownership boundary.
- FOLLOW_UP_ACTIONS: C reconciles the family matrix and logical identity mapping into its canonical source/mirrors; C/H publish and accept exact versioned operation mapping under [Issue #449](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/449); H reviews only H-owned Wire/Transport artifacts; no parallel API.



### 7.3 Resolved-vs-open decision register

| Item | Disposition | Exact boundary / next owner |
|---|---|---|
| Canonical BMCP name | RESOLVED — Brain Memory Context Protocol | Main terminology Blob `b8770fbb58e4fac087698043c40a57531b1d244d`; “Brain Memory Control Protocol” is non-canonical |
| Fact/Claim semantics | RESOLVED — Option A + I1 | Merged Owner decision PR #446; Blob `d59756a8eb454480804c482ca03c68345ab5abf2` |
| Fact/Claim field/wire schema | CANDIDATE / NOT FROZEN | B/D/E/F/G/H/I consumer artifacts must be version-pinned and reviewed; no payload fields approved |
| H-CONFIRM-001..004 | PARTIALLY_DECIDED / EXACT_ARTIFACT_MAPPING_OPEN | Logical semantics decided with INDEPENDENCE_UNVERIFIABLE; exact registry/schema/crypto/Storage/error artifacts remain open |
| BMCP-DR-002 | DECIDED_AT_AUTHORITY_BOUNDARY / CALLABLE_API_IDL_SCHEMA_DEFERRED | D/I are authoritative; exact callable API/IDL/Schema/Crypto/Storage/Wire Mapping remains D/I/H-owned and open |
| BMCP-DR-003 / MCP mapping | PARTIALLY_DECIDED — Issue #449 | MCP is C-owned Agent Adapter/Gateway; exact C/H operation mapping remains open |
| BMCP Runtime / AT-01..AT-20 | NOT AUTHORIZED / NOT RUN | Issue #7 implementation binding remains deferred |

**D/I evidence for BMCP-DR-002 (ownership evidence, not callable API publication):**
- D: `docs/en/03-memory-brain/forget-fence-and-completion-contract.md` Blob `c791895333ab6140f035f4f622d5dee9325d422d`; `forget-fence-operation-and-publication-gate.md` Blob `9c054932994bb078e2834df8bd66f73895aa04f5`; `memory-versioning.md` Blob `4efbd26db9586f6fcf1897f42ffba287d625b903`; `commit-cursor-semantics.md` Blob `2de7fe35229372ae5b06093e5e031c2c243fbd7c`.
- I: `docs/en/09-security-governance/security-governance-guide.md` Blob `061c5847b3df879eeaf3c71e5eae0bfa162b276a`; Chinese mirror Blob `372d27c79dc79d09bcdb0f142c979efdba1c2b6e`.
- These sources define domain semantics and operation names, not a complete callable API/IDL or frozen wire representation. D names RegisterProducerWork, InstallForgetFence, PublishDerivedIfFenceCurrent, CompleteProducerWork, ResolveProducerWork and ReconcileForgetBarrier. I defines PermissionEpoch, AuthorizationDecisionRef, revocation/currentness and evidence acceptance; no frozen public authorize() endpoint/schema exists.
- Ruling: D/I Owner comments 7060243632 and 7060259541 DECIDE this authority boundary. D remains sole authority for canonical ID/revision/currentness, lifecycle, ConflictSet, ForgetOperation/Fence and producer-barrier semantics; I remains sole authority for Principal/Actor/attestor authorization, PermissionEpoch, revocation, retention/legal-hold/backup and global Forget policy/evaluation. BMCP carries opaque owner-issued refs/epochs and calls only the owning authority's validation/currentness operation after publication. PermissionEpoch and ForgetFence are distinct nominal types. Missing/stale/unavailable/indeterminate evidence fails closed. Exact callable APIs/IDL/schema remain open and must be published by D/I.

**C mapping boundary:** PR #430 comment 7060351480 decides family-level routing; [#449](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/449) remains OPEN for exact H operation IDs/schemas, C tool/resource names and consumer acceptance. MCP is Agent Host ↔ C northbound; BMCP is C Agent Adapter ↔ Brain via H. AgentRequestId may be a local workflow-correlation input but MUST NOT become a newly invented H `request_id`; H assigns each message its own `message_id`, with `correlation_id` for workflow and `causation_id` for the immediate parent. Event Ingress/Telemetry/Forget/Admin require registered H operations and owner authorization; Context Snapshot/Delta/Delivery are inbound; Acknowledgement is Adapter evidence, not MCP success or G Applied. Recall/Search is F-owned and is not a current BMCP family; do not invent Search.

### 7.4 B/D/I Owner decisions (delegated roles; no independent human signatures claimed)

- **B — PR #429 comment 7060251435:** accepts Option A + I1. Claim is an attributable proposition thread; ClaimRevision is immutable; Fact is a separate governed attestation; FactRevision binds exact ClaimRevisionRef(s), Evidence/Provenance and authorized attestor/method context. B owns semantic vocabulary; D owns canonical identity; I owns authorization.
- **D — PR #429 comment 7060243632:** accepts Option A + I1 as canonical-domain input. D owns ClaimRef/ClaimRevisionRef and FactRef/FactRevisionRef allocation, revision commit/currentness, lifecycle, lineage, ConflictSet and ForgetOperation/ForgetFence. Exact immutable-revision transaction/currentness, schema, migration/compatibility, consumer acceptance and conformance remain OPEN.
- **I — PR #429 comment 7060259541:** accepts Option A + I1 as security-policy input. Fact creation/revision is a protected action requiring authenticated Principal/Actor binding, exact attestor authorization and current I-issued PermissionEpoch at final authorization/commit. Cached ALLOW/session/lease/ACK is not reusable authorization. I owns attestor authorization, revocation, retention/legal-hold/backup and global Forget evaluation. Exact policy partitioning, issuer/registry binding and consumer mapping remain OPEN.

**Required source reconciliation:** B must update its domain-model-overview and B-ADR status/source pins; D must update existing memory-versioning/Forget sources and mirrors; I must update existing Principal/Actor authorization and Forget sources/mirrors. Current source statements that semantic selection is undecided/ADR-blocked are stale as to semantic selection, but schema/API/implementation gates remain open.

## 8. Runtime acceptance plan — NOT RUN

Every row is a future Runtime requirement. No test below was executed by this work item. Design documents/reference models are not Runtime PASS.

### 8.1 Existing conformance evidence — bounded, not full-protocol PASS

- Current main `6c5597a62ada7f56d1956b9c60409f329d2819c5`, test file blob `903764ab08a7d3dd17ba13f5c40e8c4129958bb5`: `python3 -m unittest discover -s 08-bmcp-protocol/tests/conformance/applied_delivery_evidence -p 'test_*.py' -v` — **38 passed, 0 failed**, exit 0, reproduced on a clean clone. This is the Applied Delivery Evidence conformance suite only. The earlier `30 passed` figure was measured against test file blob `98242cc193a77b27d58b39353ccc031201992614` at `c138654c…` and `713774c3…`; it is superseded, not contradicted.
- PR #436 (merged at `02f61194fd4e12993b4c83f7fac8382eee20f5d8`), source head `1ffed9ed127df98b2f823a66ec80ea43d08cb9dc`: `python3 -m unittest discover -s 08-bmcp-protocol/tests/conformance/provider_outcome -p 'test_*.py' -v` — **10 run; 5 passed; 5 skipped; 0 failed**, exit 0. Skipped CPO-02/04/05/09/10 explicitly require Owner C's authoritative semantic validator. This is structural schema conformance only; it does not validate C semantics or cryptographic signatures.
- PR #436's bilingual protocol index and provider_outcome test are now integrated into main. Its index still marks RecoveryJoin 1.0.2 schema/validator/test as not delivered; five semantic test methods remain skipped pending C's authoritative validator.
- These results do not establish full BMCP conformance. The strict JSON parser is a reference model, not production transport. `tests/protocol_test.rs` and `crates/bmcp` are absent.
- AT-01..AT-20 remain **PLANNED_NOT_RUN**. No Runtime repository/authorization exists in this architecture phase.

The following Acceptance Tests (AT-01 through AT-20) define the expected behavioral coverage, ownership, preconditions, verification methods, dependencies, and current acceptance blockers. They are specification-level acceptance criteria, not evidence of completed test execution.

| ID / Scenario | OWNER | PRECONDITION | EXPECTED_RESULT | TEST_METHOD | DEPENDENCY | ACCEPTANCE_STATUS |
|---|---|---|---|---|---|---|
| AT-01 | Valid request parse | H + BMCP | H decodes and authenticates the Envelope; version is supported; Operation is registered | One normalized Request; Parse has no side effects | Golden Envelope + Operation Schema | H Envelope/Registry | BLOCKED_BY_H_CONTRACT |
| AT-02 | Invalid request parse | H | Envelope format is invalid / required fields are missing | Rejected before Execute; stable, redacted Error | Negative Envelope Vector | H Validator | BLOCKED_BY_H_CONTRACT |
| AT-03 | Unsupported version | H | No common major version | VERSION_UNSUPPORTED; no downgrade or dispatch | Version Negotiation Matrix | H Version Contract | BLOCKED_BY_H_CONTRACT |
| AT-04 | Missing parameters | H + Operation Owner | Required Payload fields are missing | Validation rejection; Service is not invoked | Per-Operation negative Schema Vector | H + Domain Schema | BLOCKED_BY_H_CONTRACT |
| AT-05 | Unknown Operation | H | Family/Operation is not registered | Rejected before side effects | Negative Registry tests / Fuzz | H Registry | BLOCKED_BY_H_CONTRACT |
| AT-06 | Unauthorized request | I + H | The authenticated Principal is denied by the current I Policy | Deny; protected services are not invoked; no cross-Scope information is disclosed | Negative Authorization integration tests | I API/Epoch + H Binding | BLOCKED_BY_OWNER_CONTRACT |
| AT-07 | Request/Response correlation | H | Request has message_id/correlation_id | Response Causation references the Request; Correlation is preserved | Multi-message Round-trip | H Request Identity | BLOCKED_BY_H_CONTRACT |
| AT-08 | Successful execution | Domain Owner + BMCP | Parse/validation/authorization pass; Owner returns a successful Receipt | Response contains the exact Owner Result; ACK remains independent | Service Contract integration tests | E/D/G API | BLOCKED_BY_OWNER_CONTRACT |
| AT-09 | Failed execution | Domain Owner + H | Owner returns a definitive failure | Failure is preserved; success is not fabricated | Injected Service Fault | Owner Error + H Mapping | BLOCKED_BY_H_CONTRACT |
| AT-10 | Timeout | Owner + H | Timeout occurs potentially before or after side effects | UNKNOWN until Owner Reconciliation; same Key is used | Crash/Timeout at each boundary | Owner Lookup/Reconcile | BLOCKED_BY_OWNER_CONTRACT |
| AT-11 | ACK Receipt | H | A valid ACK is received for a declared boundary | Only that boundary is recorded; execution/persistence is not inferred | ACK Schema/Consumer | H ACK | BLOCKED_BY_H_CONTRACT |
| AT-12 | Lost ACK | H + Owner | Side effects may have completed; ACK/Response is lost | UNKNOWN; Reconcile using the same identity; no blind retry | Network Fault + Journal Reconcile | H ACK + Owner Idempotency | BLOCKED_BY_H_CONTRACT |
| AT-13 | Duplicate Request | Owner + H | Same idempotency identity and digest | Original result is returned; no duplicate side effects | Concurrent Duplicate/Replay | Owner Idempotency | BLOCKED_BY_OWNER_CONTRACT |
| AT-14 | Duplicate ACK | H + Consumer | Same ACK ID/Digest, followed by the same ID with a different Digest | Replay is idempotent; changed digest causes Conflict; state is not changed | ACK Replay/Mutation Vector | H ACK + D/G/I Mapping | BLOCKED_BY_H_CONTRACT |
| AT-15 | Validator rejection | H + Owner | Envelope/Schema/Critical Extension is invalid | Rejected at the correct layer; does not enter subsequent stages | Layered negative test suite | H Validator + Domain Schema | BLOCKED_BY_H_CONTRACT |
| AT-16 | Forget Fence conflict | D + I + H | D Fence or I Epoch is Stale/Unknown | Fail-closed; protected Apply/Commit is not executed; suppression is preserved | Both Race orderings + authoritative service failure | D/I Currentness API | BLOCKED_BY_OWNER_CONTRACT |
| AT-17 | Canonical Identity conflict | D (Fact/Claim additionally depends on B ADR) | Payload Ref does not match D Identity, or Fact/Claim remains unresolved | Reject/Quarantine; no identity is issued or converted | Forged/Mismatch Identity Vector | D API; B ADR | BLOCKED_BY_OWNER_CONTRACT |
| AT-18 | Serialization stability | H | Exact Schema/Profile/Version | Semantically equivalent objects produce approved Canonical Bytes/Digest | Cross-language Golden Vector | H Canonicalization/Signature | BLOCKED_BY_H_CONTRACT |
| AT-19 | Unicode | H | Valid/invalid UTF-8, supplementary characters, normalization boundaries, duplicate Keys | Valid Unicode is preserved according to the Profile; invalid/ambiguous forms are rejected | Cross-language Unicode/malformed-byte tests | H Wire Decode/Canonicalization | BLOCKED_BY_H_CONTRACT |
| AT-20 | Request/Response consistency | H + Domain Owner | Request ID/Correlation/Operation/Idempotency are fixed | Response correlates to the exact Request and returns only the Owner Result | End-to-end Trace assertions | H Correlation + Owner Result | BLOCKED_BY_H_CONTRACT |

BLOCKED_BY_H_CONTRACT means that an H-owned Wire/Transport/ACK/Validator decision or exact mapping is missing. BLOCKED_BY_OWNER_CONTRACT means that an authoritative Owner domain contract/API or ADR decision is missing. All tests remain NOT RUN until runtime authorization and an exact Build are available. Dependency labels are not test results.


## 9. Runtime engineering handoff / Issue #7 entry conditions

Keep the binding unchanged: `IMPLEMENTATION_BINDING=DEFERRED_TO_ENGINEERING_PHASE`.

Issue #7 is currently CLOSED / not_planned under the Owner phase-closure ruling; its body retains the deferral and engineering-entry checklist. This work does not edit Issue #7 or declare Runtime entry.

**All conditions below are required before Runtime entry:**
1. BMCP semantic contract is accepted by the responsible architecture authorities; unresolved semantics are explicitly listed.
2. H freezes versioned Wire, Transport, ACK and Validator contracts, including Error/Conformance Mapping.
3. H/C/E/D/I/G accept the required cross-module Request/Response/Receipt/ACK mappings.
4. Owner Option A + I1 semantics are approved. Exact consumer mapping remains Candidate until B/D/E/F/G/H/I/Storage contracts are version-pinned and reviewed; E Candidate IR and receipt APIs are precisely pinned.
5. C publishes Agent Integration / MCP-to-BMCP mapping under Issue #449 and H reviews it; MCP must not replace BMCP.
6. D/I publish exact callable interfaces for Identity/Lifecycle, Forget Fence, Authorization and PermissionEpoch currentness. Their authority boundaries are decided; API/IDL/schema remain open.
7. A canonical Runtime repository/branch (or authorized new repository), engineering Owner/maintainer, build, CI, test commands and artifact provenance are designated.
8. The relevant authorities record deployment topology, persistence, queues, recipient adapters, observability, recovery and operator responsibilities.
9. The full acceptance suite executes on an immutable Runtime commit with reproducible raw evidence; UNKNOWN/Recovery/Race paths fail closed.
10. Independent security/domain review and required Owner acceptance are complete. No production activation is implied.

| Workstream | Next artifact | Authority | Entry status |
|---|---|---|---|
| H | Versioned Envelope/Version, Wire Decode, ACK, Validator and Error/Conformance | H | PARTIALLY_DECIDED / EXACT_ARTIFACT_MAPPING_OPEN |
| B / Governance | Reconcile approved semantic decision into exact consumer contracts; schema remains Candidate | B + D/E/F/G/H/I | SEMANTIC_ACCEPTED / SOURCE_RECONCILIATION_AND_SCHEMA_GATE_OPEN |
| D | Canonical Identity/Lifecycle/Fence API and Receipt | D | AUTHORITY_BOUNDARY_DECIDED / CALLABLE_API_IDL_OPEN |
| I | Authorization/PermissionEpoch/Revocation API | I | AUTHORITY_BOUNDARY_DECIDED / CALLABLE_API_IDL_OPEN |
| E | Candidate IR, AcceptedReceipt and service boundary; five-stage Rust reference pipeline only | E | INTEGRATED_DOCS_AND_CONSUMER_GATE_OPEN |
| C | Agent/MCP Adapter-to-BMCP mapping | C + H | PENDING_C_MAPPING_ISSUE_449 |
| G | ContextVersion/Delivery/Applied/ACK mapping | G + H | OWNER_CONSUMER_MAPPING_PENDING |
| Engineering Leadership | Canonical Runtime repository/team/CI/deployment authority | Engineering Leadership | DEFERRED_TO_ENGINEERING_PHASE |
| BMCP architecture integration | Refresh source pins and incorporate B/D/I/H/C rulings | BMCP architecture lead | IN_PROGRESS |

## 10. Governance and verification

- Validation snapshot: exact base / merge-base `c58878fce24528a0842b4f8887c93ddbf465b566`; exact candidate head is recorded in the PR delivery report. The PR base ref is `bmcp-validation-base-c588`, pinned to `c58878fce24528a0842b4f8887c93ddbf465b566`. Owner GitHub Compare verification records `c58878fce24528a0842b4f8887c93ddbf465b566` as an ancestor of the then-observed live `main` `2998f6321b90888d65ac9d972a169f86482e08b`: `ahead_by=16`, `behind_by=0`, and `merge_base_commit=c58878f`. An empty local `git merge-base` result from a shallow clone is not evidence of unrelated histories. This round intentionally does not chase live main; the controlled base remains fixed at C588. The previous `713774c` batch is historical only.
- Main source ledger §2 was refreshed from `c58878fce24528a0842b4f8887c93ddbf465b566`; all listed Main Blob pins were resolved against that exact commit. H source branch was re-read at `session-h-bmcp-protocol @ 3e8b33df18b9e6fc757ca84ff07a12faebc78e74`; all eight H Blob pins were re-fetched and match. EN/ZH source-ledger SHA sets are identical.
- Main changes incorporated into the dependency review: #472 G ContextVersion/ChangeSet/CAS documentation and implementation; `crates/memory-context/tests/e2e_negative_paths.rs` (SQLite Store→Context negative-path coverage); canonical Claim/Fact revision types; BMCP RecoveryJoin 1.0.2 schema, index, structural validator and conformance fixtures/tests. RecoveryJoin validator returns `STRUCTURALLY_VALID` for schema-only success and requires injected D-authoritative callbacks for proof/currentness; without callbacks the result is `UNKNOWN`, not VALID. It does not freeze H wire/transport or substitute for D authority. The G E2E tests cover foreign-scope denial, Candidate lifecycle rejection, stale revision rejection, budget overflow and file-backed SQLite restart; they do not provide Forget/tombstone public-operation coverage, H ACK binding or C final-request Applied evidence.
- BMCP-DR-002 remains DECIDED at D/I authority-boundary level only. BMCP-DR-003 remains PARTIALLY_DECIDED; exact C-H operation registry/mapping remains OPEN. H-CONFIRM-001..004 remain PARTIALLY_DECIDED / EXACT_ARTIFACT_MAPPING_OPEN; `INDEPENDENCE_UNVERIFIABLE` remains. AT-01..AT-20 remain **PLANNED_NOT_RUN**; Provider Outcome's five C semantic skips remain unresolved.
- Issue #7 remains CLOSED / not_planned with `IMPLEMENTATION_BINDING=DEFERRED_TO_ENGINEERING_PHASE`. No wire/schema/API freeze, Runtime, transport implementation, deployment, production activation or Issue #7 change.
- `git diff --check c58878fce24528a0842b4f8887c93ddbf465b566...HEAD`: PASS, exit 0 (rerun after final commit).
- `python3 scripts/check_document_management.py --require-changed c58878fce24528a0842b4f8887c93ddbf465b566`: FAIL, exit 1; two baseline DM-06 errors in `08-bmcp-protocol/protocol-index.md` and `.zh-CN.md` (`Canonical` requires `authority.canonical_scope_id`). The PR changes neither index file. Reported inventory: 501 governed documents, 18 classified / 483 unclassified. No out-of-scope metadata changes were made.


**Separate baseline finding — explicitly outside #453:** Owner independently verified `08-bmcp-protocol/protocol-index.md` (Blob `a5b64941cdc783b385348de1b22e0eaace2c003d`) and `08-bmcp-protocol/protocol-index.zh-CN.md` (Blob `2fe06d9424821eb96eb006dbb391914c1375afae`) at the Owner-checked main snapshot. Both contain `authority.canonical_status`, `authority.normative_status`, and `authority.canonical_conflict_status`, but omit `authority.canonical_scope_id` (DM-06). The Chinese path is the repository-root `08-bmcp-protocol/protocol-index.zh-CN.md`, not `docs/zh-CN/`. These two files are not among #453's three changed paths. Owner authorized a separate H-owned bilingual repair carrier in principle, but it is not opened while the repository exceeds its open-PR quota. Do not guess the scope ID or weaken DM-06; this is not a #453 repair.
- `python3 scripts/ci/audit_runner_admission.py`: PASS; 1 self-hosted job audited / 0 violations; exit 0.
- `BASE_SHA=c58878fce24528a0842b4f8887c93ddbf465b566 HEAD_SHA=$(git rev-parse HEAD) PR_BODY='BILINGUAL-MANIFEST: COMPLETE' python3 scripts/check_bilingual_docs.py`: PASS; 77 frozen / 0 new gaps / 21 exemptions; exit 0. Registration history: 21 sources re-enumerated (18 later registrations, 3 exact legacy allowlist matches), 0 errors. Three changed Markdown paths outside `NORMATIVE_ROOTS` are explicitly noted as not pairing-checked. The gate's same-commit registration-history rule remains present; the old 21 errors were not reproduced on this snapshot.
- `python3 scripts/check_bilingual_docs_full.py --source-revision c58878fce24528a0842b4f8887c93ddbf465b566`: FAIL; 467 in-scope Markdown / 112 exempt / 81 violations; exit 1. Full path-by-path classification follows.

### GOV-DOC-001 full-tree inventory at the c58878f snapshot

The exact command `python3 scripts/check_bilingual_docs_full.py --source-revision c58878fce24528a0842b4f8887c93ddbf465b566` returned **467 in-scope Markdown / 112 exempt / 81 violations / exit 1**. This is a path-counterpart inventory, not semantic translation review. The 81 findings classify as follows:

### Path-by-path classification of the 81 frozen GOV-DOC-001 findings

Every listed source exists at frozen base `c58878fce24528a0842b4f8887c93ddbf465b566`; all 81 findings are therefore pre-existing at Stage A base. The first 77 are NORMATIVE_ROOTS mirror-pair failures (both expected `docs/en/<source>` and `docs/zh-CN/<source>` paths are absent). The final four are Phase-0 report pairing failures (no side-by-side `.en.md`/`.zh-CN.md` pair or required `docs/en/14-ai-development` mirror). Owner labels below are routing classifications from path/domain, not a new assignment of canonical ownership. All are excluded from #453; disposition is owner-scoped backlog triage, no bulk cleanup.

| # | Exact source path | Owner / routing | Rule | At c588 | Disposition |
|---:|---|---|---|---|---|
| 01 | `00-governance/architecture-document-management-policy.md` | Repository Governance | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 02 | `00-governance/reports/gov-doc-001-full-scan-2026-11-20.md` | Repository Governance | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 03 | `00-governance/templates/document-metadata-template.md` | Repository Governance | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 04 | `02-domain-model/phase-2-domain-extension.md` | B — Domain Model | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 05 | `02-domain-model/phase-2-domain-extension.zh-CN.md` | B — Domain Model | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 06 | `06-memory-context/context-architecture.md` | G — Memory Context | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 07 | `06-memory-context/context-budget-and-sufficiency.md` | G — Memory Context | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 08 | `06-memory-context/context-edit-operations.md` | G — Memory Context | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 09 | `06-memory-context/context-implementation-coverage.md` | G — Memory Context | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 10 | `06-memory-context/context-implementation-coverage.zh-CN.md` | G — Memory Context | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 11 | `06-memory-context/context-manager.md` | G — Memory Context | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 12 | `06-memory-context/context-reconciliation.md` | G — Memory Context | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 13 | `06-memory-context/context-versioning.md` | G — Memory Context | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 14 | `06-memory-context/phase-3.7-g-local-lifecycle-producer-derivative-queue-recall-context-restore.md` | G — Memory Context | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 15 | `06-memory-context/phase-3.8.4-g-c-provider-outcome-consumer-review.md` | G — Memory Context | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 16 | `06-memory-context/phase-3.8.5-g-storage-logical-serialization-topology-impact-review.md` | G — Memory Context | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 17 | `06-memory-context/phase-3.8.6-g-review-storage-serialization-anchor.md` | G — Memory Context | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 18 | `07-agent-integration/adapter-capability-tiers.md` | C — Agent Integration | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 19 | `07-agent-integration/adapter-capability-tiers.zh-CN.md` | C — Agent Integration | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 20 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/README.md` | B — Domain Model research | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 21 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/baseline-currentness-and-owner-source-audit.md` | B — Domain Model research | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 22 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/baseline-owner-branch-snapshot-errata.md` | B — Domain Model research | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 23 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/bilingual-parity-audit.md` | B — Domain Model research | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 24 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/canonical-domain-entity-inventory.md` | B — Domain Model research | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 25 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/canonical-domain-glossary.md` | B — Domain Model research | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 26 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/canonical-domain-invariants.md` | B — Domain Model research | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 27 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/canonical-domain-model.md` | B — Domain Model research | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 28 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/canonical-domain-relationships.md` | B — Domain Model research | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 29 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/canonical-identity-semantics.md` | B — Domain Model research | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 30 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/canonical-state-semantics.md` | B — Domain Model research | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 31 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/canonical-temporal-evidence-semantics.md` | B — Domain Model research | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 32 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/cross-owner-canonical-semantics-matrix.md` | B — Domain Model research | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 33 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/domain-model-complexity-assessment.md` | B — Domain Model research | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 34 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/domain-model-decision-record.md` | B — Domain Model research | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 35 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/domain-semantics-conflict-register.md` | B — Domain Model research | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 36 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/evidence/README.md` | B — Domain Model research | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 37 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/evidence/official-reference-validation.md` | B — Domain Model research | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 38 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/existing-domain-model-baseline.md` | B — Domain Model research | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 39 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/fact-claim-identity-adr.md` | B — Domain Model research | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 40 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/latest-cross-owner-source-reconciliation.md` | B — Domain Model research | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 41 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/mature-domain-model-research.md` | B — Domain Model research | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 42 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/post-merge-currentness-and-governance-reconciliation.md` | B — Domain Model research | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 43 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/validation/README.md` | B — Domain Model research | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 44 | `13-engineering-decisions/technology-architecture-blueprint.md` | Architecture / Engineering Leadership (owner not resolved by this scan) | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 45 | `13-engineering-decisions/technology-research/TECH-REALITY-001-A/README.md` | Architecture / Technology research (owner not resolved by this scan) | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 46 | `13-engineering-decisions/technology-research/TECH-REALITY-001-A/architecture-complexity-audit.md` | Architecture / Technology research (owner not resolved by this scan) | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 47 | `13-engineering-decisions/technology-research/TECH-REALITY-001-A/baseline/architecture-baseline.md` | Architecture / Technology research (owner not resolved by this scan) | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 48 | `13-engineering-decisions/technology-research/TECH-REALITY-001-A/deployment-topology-comparison.md` | Architecture / Technology research (owner not resolved by this scan) | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 49 | `13-engineering-decisions/technology-research/TECH-REALITY-001-A/independent-review-handoff.md` | Architecture / Technology research (owner not resolved by this scan) | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 50 | `13-engineering-decisions/technology-research/TECH-REALITY-001-A/mature-project-research.md` | Architecture / Technology research (owner not resolved by this scan) | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 51 | `13-engineering-decisions/technology-research/TECH-REALITY-001-A/open-questions.md` | Architecture / Technology research (owner not resolved by this scan) | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 52 | `13-engineering-decisions/technology-research/TECH-REALITY-001-A/owner-dependency-register.md` | Architecture / Technology research (owner not resolved by this scan) | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 53 | `13-engineering-decisions/technology-research/TECH-REALITY-001-A/owner-remediation/CGH-APPLIED-REVIEW-001.md` | Architecture / Technology research (owner not resolved by this scan) | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 54 | `13-engineering-decisions/technology-research/TECH-REALITY-001-A/owner-remediation/OWNER-REMEDIATION-001.md` | Architecture / Technology research (owner not resolved by this scan) | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 55 | `13-engineering-decisions/technology-research/TECH-REALITY-001-A/owner-technology-review-synthesis.md` | Architecture / Technology research (owner not resolved by this scan) | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 56 | `13-engineering-decisions/technology-research/TECH-REALITY-001-A/research-evidence-register.md` | Architecture / Technology research (owner not resolved by this scan) | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 57 | `13-engineering-decisions/technology-research/TECH-REALITY-001-A/rust-ecosystem-assessment.md` | Architecture / Technology research (owner not resolved by this scan) | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 58 | `13-engineering-decisions/technology-research/TECH-REALITY-001-A/technology-capability-matrix.md` | Architecture / Technology research (owner not resolved by this scan) | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 59 | `13-engineering-decisions/technology-research/TECH-REALITY-001-A/technology-recommendation.md` | Architecture / Technology research (owner not resolved by this scan) | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 60 | `13-engineering-decisions/technology-research/TECH-REALITY-001-A/workload-model.md` | Architecture / Technology research (owner not resolved by this scan) | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 61 | `13-engineering-decisions/technology-research/TECH-REALITY-001-C/README.md` | C — Agent Integration research | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 62 | `13-engineering-decisions/technology-research/TECH-REALITY-001-C/agent-integration-boundary.md` | C — Agent Integration research | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 63 | `13-engineering-decisions/technology-research/TECH-REALITY-001-C/agent-integration-canonical-contract.md` | C — Agent Integration research | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 64 | `13-engineering-decisions/technology-research/TECH-REALITY-001-C/agent-integration-conflict-register.md` | C — Agent Integration research | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 65 | `13-engineering-decisions/technology-research/TECH-REALITY-001-C/agent-integration-cross-owner-contract-matrix.md` | C — Agent Integration research | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 66 | `13-engineering-decisions/technology-research/TECH-REALITY-001-C/agent-integration-decision-record.md` | C — Agent Integration research | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 67 | `13-engineering-decisions/technology-research/TECH-REALITY-001-C/agent-integration-failure-semantics.md` | C — Agent Integration research | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 68 | `13-engineering-decisions/technology-research/TECH-REALITY-001-C/agent-integration-technology-assessment.md` | C — Agent Integration research | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 69 | `13-engineering-decisions/technology-research/TECH-REALITY-001-C/agent-integration-telemetry.md` | C — Agent Integration research | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 70 | `13-engineering-decisions/technology-research/TECH-REALITY-001-C/agent-integration-validation-plan.md` | C — Agent Integration research | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 71 | `13-engineering-decisions/technology-research/TECH-REALITY-001-C/evidence/README.md` | C — Agent Integration research | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 72 | `13-engineering-decisions/technology-research/TECH-REALITY-001-C/existing-integration-baseline.md` | C — Agent Integration research | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 73 | `13-engineering-decisions/technology-research/TECH-REALITY-001-C/inference-boundary-and-trust-model.md` | C — Agent Integration research | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 74 | `13-engineering-decisions/technology-research/TECH-REALITY-001-C/provider-integration-research.md` | C — Agent Integration research | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 75 | `13-engineering-decisions/technology-research/TECH-REALITY-001-C/provider-outcome-and-execution-evidence.md` | C — Agent Integration research | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 76 | `13-engineering-decisions/technology-research/TECH-REALITY-001-C/tool-execution-boundary.md` | C — Agent Integration research | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 77 | `13-engineering-decisions/technology-research/TECH-REALITY-001-C/validation/README.md` | C — Agent Integration research | GOV-DOC-001 NORMATIVE_ROOTS: both language mirrors absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 78 | `14-ai-development/research/phase-0/SESSION-1-GITHUB-WORKFLOW-REPORT.md` | Engineering Governance / Phase-0 operations | GOV-DOC-001 Phase-0 report: side-by-side pair / docs/en mirror absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 79 | `14-ai-development/research/phase-0/SESSION-2-PROMPT-RUN-PROVENANCE-REPORT.md` | Engineering Governance / Phase-0 operations | GOV-DOC-001 Phase-0 report: side-by-side pair / docs/en mirror absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 80 | `14-ai-development/research/phase-0/SESSION-3-QUALITY-REVIEW-DEFECT-REPORT.md` | Engineering Governance / Phase-0 operations | GOV-DOC-001 Phase-0 report: side-by-side pair / docs/en mirror absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |
| 81 | `14-ai-development/research/phase-0/SESSION-4-ADOPTION-ISOLATION-REPORT.md` | Engineering Governance / Phase-0 operations | GOV-DOC-001 Phase-0 report: side-by-side pair / docs/en mirror absent | Pre-existing | Exclude #453; owner-scoped backlog, no bulk cleanup |

### Frozen-snapshot embedded-bilingual registration re-enumeration

The gate registry contains 21 embedded-bilingual source records at C588: 18 were registered in commits later than their source-file creation commits; three are the explicitly named legacy same-commit exceptions, each with an exact creation/allowlist SHA match. `check_embedded_registration_history()` returned an empty error list. The gate's `exemptions: 21` line counts registered embedded-bilingual sources; it is not 21 violations. Thus the 21 same-commit errors reported against the historical `713774c` batch are **not reproduced** at C588. The history rule is unchanged.

| # | Registered source path | Source-add commit | Registration-add commit | C588 result |
|---:|---|---|---|---|
| 01 | `00-governance/bilingual-documentation-policy.md` | `cd1ab0fb346c770d779b1d8d24297f6811a1a74f` | `32a35f422ba6442d1f700cfb327f348c0740a7f2` | Registered after source creation |
| 02 | `14-ai-development/ai-development-standard.md` | `55d44b9276456f88bd2193de8b06aff146c228a4` | `e949d82b6cc3681a04631aa429e1bc2ab815305b` | Registered after source creation |
| 03 | `00-governance/architecture-document-management-policy.md` | `0c73f639bf7392a5381d0cc0d9cafd53017bfe05` | `0c73f639bf7392a5381d0cc0d9cafd53017bfe05` | Legacy same-commit exception; exact allowlist SHA match |
| 04 | `00-governance/architecture-document-metadata.schema.yaml` | `0c73f639bf7392a5381d0cc0d9cafd53017bfe05` | `965a66b9a92cd4c2b20f4b6100721c779be7f784` | Registered after source creation |
| 05 | `00-governance/drafts/GOV-DOC-001-v1.2-DRAFT.md` | `04d35f90d6f1389ee17dc8fba1a32600bd7ac8ec` | `04d35f90d6f1389ee17dc8fba1a32600bd7ac8ec` | Legacy same-commit exception; exact allowlist SHA match |
| 06 | `00-governance/bilingual-governance-migration-register.md` | `a77219fa2834af0c4535e6692029adaec2e62638` | `88c251178d510d247f28137c3821cee982cedd5e` | Registered after source creation |
| 07 | `00-governance/templates/bilingual-issue-template.md` | `a77219fa2834af0c4535e6692029adaec2e62638` | `88c251178d510d247f28137c3821cee982cedd5e` | Registered after source creation |
| 08 | `00-governance/templates/bilingual-umbrella-requirement-template.md` | `a77219fa2834af0c4535e6692029adaec2e62638` | `88c251178d510d247f28137c3821cee982cedd5e` | Registered after source creation |
| 09 | `00-governance/templates/bilingual-commit-message.md` | `a77219fa2834af0c4535e6692029adaec2e62638` | `88c251178d510d247f28137c3821cee982cedd5e` | Registered after source creation |
| 10 | `00-governance/templates/repository-policy-inheritance.md` | `a77219fa2834af0c4535e6692029adaec2e62638` | `88c251178d510d247f28137c3821cee982cedd5e` | Registered after source creation |
| 11 | `00-governance/templates/document-metadata-template.md` | `ae37a41900f1950a8d78d4be9e1f6a27b2edb1bb` | `b45430428c1e65cae36a9f7d63a11a78008a8f8a` | Registered after source creation |
| 12 | `00-governance/reports/bilingual-baseline-remediation-report.md` | `a77219fa2834af0c4535e6692029adaec2e62638` | `88c251178d510d247f28137c3821cee982cedd5e` | Registered after source creation |
| 13 | `00-governance/reports/f06-object-reconciliation.md` | `9990b645555aef83714ff92c97255110b1fa0960` | `9990b645555aef83714ff92c97255110b1fa0960` | Legacy same-commit exception; exact allowlist SHA match |
| 14 | `14-ai-development/AI-EXEC-UNIFICATION-RULING-001.md` | `1f97c3fae65828266a0c3cb1d1e8d4e6cb330856` | `e949d82b6cc3681a04631aa429e1bc2ab815305b` | Registered after source creation |
| 15 | `14-ai-development/AI-EXEC-INDEPENDENCE-RULING-001.md` | `1957faa6349613280576bfa5f2a3a7107f6cb719` | `e949d82b6cc3681a04631aa429e1bc2ab815305b` | Registered after source creation |
| 16 | `14-ai-development/PR-GOVERNANCE-001.md` | `3754d049db840b049728afd814faac968bf10749` | `e949d82b6cc3681a04631aa429e1bc2ab815305b` | Registered after source creation |
| 17 | `14-ai-development/prompt-and-evidence-template.md` | `55d44b9276456f88bd2193de8b06aff146c228a4` | `e949d82b6cc3681a04631aa429e1bc2ab815305b` | Registered after source creation |
| 18 | `14-ai-development/prompt-authoring-standard.md` | `6faa3b038c02bce27b3b4443d6f1be95cf5c5beb` | `e949d82b6cc3681a04631aa429e1bc2ab815305b` | Registered after source creation |
| 19 | `14-ai-development/iteration-lifecycle.md` | `55d44b9276456f88bd2193de8b06aff146c228a4` | `e949d82b6cc3681a04631aa429e1bc2ab815305b` | Registered after source creation |
| 20 | `14-ai-development/owner-automation-operating-model.md` | `6faa3b038c02bce27b3b4443d6f1be95cf5c5beb` | `e949d82b6cc3681a04631aa429e1bc2ab815305b` | Registered after source creation |
| 21 | `14-ai-development/README.md` | `55d44b9276456f88bd2193de8b06aff146c228a4` | `e949d82b6cc3681a04631aa429e1bc2ab815305b` | Registered after source creation |

The 81 mirror findings and registration-history results are separate dimensions. The C588 re-enumeration above shows 21 registered embedded-bilingual source records, 18 later registrations and three exact legacy allowlist matches, with zero history errors. No history rule was weakened or bypassed.

- `python3 scripts/governance/bilingual/test_bilingual_scripts.py`: PASS, 13/13; exit 0.
- `python3 scripts/test_check_document_management.py`: PASS, 214/214; exit 0. Expected negative-fixture diagnostics are emitted during the test run.
- `python3 -m unittest discover -s 08-bmcp-protocol/tests/conformance/applied_delivery_evidence -p 'test_*.py' -v`: PASS, 30/30; exit 0.
- `python3 -m unittest discover -s 08-bmcp-protocol/tests/conformance/provider_outcome -p 'test_*.py' -v`: 10 run / 5 passed / 5 skipped / 0 failed; exit 0. CPO-02/04/05/09/10 remain skipped pending Owner C's authoritative semantic validator.
- `python3 -m unittest discover -s 08-bmcp-protocol/tests/conformance/recovery_cutoff -p 'test_*.py' -v`: FAIL, 31 run / 28 passed / 3 failed; exit 1. Failures: duplicate-member parser test expects the specific duplicate-key detail but validator returns generic `invalid JSON: ValueError`; schema/index test cannot find the exact `message_type` entry in protocol-index; valid full-message fixture fails six non-empty object constraints. These are current-main RecoveryJoin artifacts, not modified by this PR.
- `python3 -m unittest discover -s 06-memory-context/reference-model -p 'test_g_applied_ledger.py' -v`: PASS, 8/8; exit 0.
- `cargo test --offline -p memory-context --test e2e_negative_paths`: NOT COMPLETED; compilation failed with `Disk quota exceeded` / LLVM output-stream I/O errors; exit 101. No Rust G E2E PASS is claimed.
- Separate-session semantic/bilingual review has since been completed; prompt-pairing provenance remains unverified (`SESSION_SEPARATION_RECORDED_PROMPT_UNVERIFIED`). The 20-row AT matrix is still itemized only in ZH; EN records aggregate `PLANNED_NOT_RUN`. This asymmetry is explicitly disclosed, not represented as parity.
- No H-owned normative file, G implementation, C/D/I authority file, governance gate, schema or baseline registry was modified. PR scope remains exactly three files.

## 11. Bilingual change manifest

| Document / version | English path | Chinese path | Source revision | Parity |
|---|---|---|---|---|
| BMCP-ARCH-001 / 0.2.2 | reviews/bmcp-architecture-followup/BMCP-ARCH-001.en.md | reviews/bmcp-architecture-followup/BMCP-ARCH-001.zh-CN.md | main c58878fce24528a0842b4f8887c93ddbf465b566; H 3e8b33df18b9e6fc757ca84ff07a12faebc78e74; B/D/I owner pins in §2/§7 | Separate-session semantic/bilingual review completed; prompt-pairing provenance not verified (SESSION_SEPARATION_RECORDED_PROMPT_UNVERIFIED) |

The coverage register records this as a review/handoff pair only. It does not change “BMCP Protocol detailed contracts (7 core specifications)”; bilingual normative core-spec coverage remains NOT STARTED.

## 12. Final status

- ARCHITECTURE_DELIVERABLE_STATUS: **ARCHITECTURE_PARTIAL**
- PARSE_CONTRACT_STATUS: logical boundary decided; JCS basis selected; exact signed bytes/crypto profile and H wire mapping remain open.
- EXECUTE_CONTRACT_STATUS: CANDIDATE; Option A + I1 selected; D/I authority boundaries decided; callable API/IDL/schema deferred to D/I contracts; C mapping open.
- RESPOND_CONTRACT_STATUS: CANDIDATE; logical ACK/response distinctions decided; exact H envelope/field mapping and Storage persistence topology remain open.
- H_DEPENDENCY_STATUS: **PARTIALLY_DECIDED / EXACT_ARTIFACT_MAPPING_OPEN**; INDEPENDENCE_UNVERIFIABLE
- CROSS_MODULE_DEPENDENCIES: H, B, C, D, E, G, I, Storage
- OWNER_DECISIONS_REQUIRED: BMCP-DR-001 semantic direction RESOLVED / consumer-schema gate OPEN; BMCP-DR-002 authority boundary DECIDED / callable API- IDL deferred; BMCP-DR-003 MCP adapter boundary PARTIALLY DECIDED / exact C mapping OPEN under Issue #449.
- ISSUE_7_STATUS: `IMPLEMENTATION_BINDING=DEFERRED_TO_ENGINEERING_PHASE`; GitHub CLOSED / not_planned; unchanged.
- RUNTIME_IMPLEMENTATION_STATUS: NOT AUTHORIZED / NOT STARTED
- PR / Commit: PR #453 was merged into the pinned validation branch `bmcp-validation-base-c588` at merge commit `7c7801db396b92c57ad37020fe170f65f25e43ce`; this snapshot merge is not a merge to live `main`. Separate-session semantic/bilingual review has been completed; prompt-pairing provenance remains unverified (SESSION_SEPARATION_RECORDED_PROMPT_UNVERIFIED). The artifact remains ARCHITECTURE_PARTIAL and does not freeze protocol/schema or authorize Runtime.
- DECIDED — ENGLISH-SIDE ERROR-CLASS INVENTORY RECONCILIATION: Owner decision `BMCP-ARCH-001-OWNER-DECISION-H-CONFIRM-004-ERROR-INVENTORY-001` establishes an authoritative inventory of ten logical error classes, in order: Authentication, Authorization, Validation, Unsupported, Conflict, Expired, RateLimited, ResourceExhausted, Internal and Unknown. The §7.1.1 taxonomy already represents eight classes individually; RateLimited and ResourceExhausted are represented together by the existing `RateLimited/ResourceExhausted` entry and are distinguished as two logical classes by this decision. No additional classes are established. Accordingly, the unsupported `twelve requested classes` wording in §7.1 H-CONFIRM-004 DECISION_REQUIRED is corrected to `ten logical error classes`. This adopts the recorded RECOMMENDED_OPTION to retain specific classes and publish layered validation and mapping, without inventing additional classes for which no authoritative names or definitions exist. H-CONFIRM-004 remains `PARTIALLY_DECIDED / EXACT_ARTIFACT_MAPPING_OPEN`, with `INDEPENDENCE_UNVERIFIABLE`. Exact enum spellings, wire response schema, versioning, retry profile, redaction, layered validator-to-error mapping, owner-specific outcome mappings and domain-owner approvals, consumer mappings and acceptance, and H's separate versioned wire-contract review remain OPEN. This decision does not freeze protocol or schema, authorize Runtime, promote `ARCHITECTURE_PARTIAL`, change `MAINLINE_DELIVERABLE=NOT_AVAILABLE`, or constitute an independent human H signature.

**Next action:** B/D/I reconcile their existing source/mirror documents and refresh pins; H publishes versioned normative wire artifacts and closes the remaining registry/schema/crypto/Storage/error sub-items; C publishes exact Agent/MCP-to-BMCP mapping under Issue #449; E integrates the five-stage Rust compiler docs and consumer boundaries; BMCP refreshes the bilingual handoff. Runtime remains deferred until every engineering-entry condition is evidenced.
