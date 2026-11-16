# Threat Model and Adversarial Test Plan

- Owner: Session I
- Status: **CANDIDATE threat model; tests specified, not executed**
- Related: INT-P0-02/03/04, INT-X-02/03/04/07, CT-004..020.

## 1. Security objectives

Protect confidentiality, integrity, availability, provenance, scope isolation and lifecycle/Forget guarantees for canonical Memory, Evidence, Provenance, derived artifacts, retrieval results, Context delivery and Agent inference boundaries. Preserve Agent authority over reasoning, tool use and external actions.

Threat model covers malicious or compromised users, Agents, producers, Adapters, plugins, model-generated content, cross-tenant callers, compromised workers, stale caches/indexes, replayed messages, misconfigured external recipients, backup restore and provider-side retention beyond Brain control.

## 2. Assets and trust boundaries

Assets:
- Principal credentials, issuer trust, delegation grants and permission epochs;
- tenant/user/project/Agent/task/session/environment Scope bindings;
- Event payloads, canonical Memory/Claim/Entity/Relation, Evidence and Provenance;
- derived summaries, compactions, embeddings, indexes, Working Sets and caches;
- Context snapshots/deltas, delivery ledgers, Adapter managed regions and inference requests;
- Forget inventories, barriers, acknowledgements, backup catalogs and audit evidence.

Trust boundaries:
1. Agent/producer → authenticated ingress;
2. Compiler worker → source dereference and canonical commit;
3. Canonical Store → index/projection/retrieval;
4. Runtime → Context Manager;
5. Context Manager → Adapter transport and managed region;
6. Adapter → final inference request;
7. Brain → external recipient/provider;
8. primary/replica/backup → restore;
9. operational audit/support systems.

## 3. Adversary goals

- Forge or borrow another Principal/ProducerIdentity.
- Escape tenant/user/project/Agent/task/session/environment boundaries.
- Infer existence of inaccessible memories through candidate counts, graph traversal, timing or error messages.
- Poison memory with indirect prompt injection or malicious entity/provenance labels.
- Launder malicious instructions through summaries, compaction, paraphrase or provenance.
- Race revocation/Forget with ingestion, compile, commit, retrieval, cache fill, Context update, delivery or inference.
- Replay stale Accepted receipts, outbox events, ChangeSets, Adapter snapshots or acknowledgements.
- Restore forgotten data from backup or resurrect it via index rebuild/replay.
- Retain sensitive content in audit logs, tombstones, metrics, traces or support bundles.
- Exploit legal-hold/retention exception as an alternate retrieval path.
- Cause denial of service through fan-out, recursive provenance, oversized payloads or retry storms.

## 4. Prompt-injection threat model

### 4.1 Untrusted content classes

Treat all of the following as adversarial data even when internally generated or signed:
- retrieved Memory content and Claim text;
- Evidence snippets, OCR, documents, tool outputs and external URLs;
- Provenance method descriptions and source labels;
- Entity names, aliases, Relation predicates and qualifiers;
- user/Agent summaries, compactions, embeddings and generated paraphrases;
- cross-scope shared content and imported third-party Memory;
- telemetry PlanSummary, Intent and Outcome fields.

Authentication and integrity do not establish semantic safety. A validly signed Agent can submit malicious text; a genuine source can contain prompt injection.

### 4.2 Threat paths

- Direct instruction: “ignore prior instructions”, exfiltrate secrets, call tools, alter policy.
- Indirect instruction: malicious document or web page retrieved as Evidence.
- Authority laundering: text labelled “system”, “trusted”, “verified” or “admin” by a source or Entity label.
- Provenance laundering: hostile content summarized, quoted, embedded or transformed until its origin is obscured.
- Compaction laundering: safety caveat is dropped while imperative instruction survives.
- Cross-scope poisoning: content from one user/project/environment is indexed, summarized or linked into another.
- Retrieval poisoning: similarity/ranking manipulation makes adversarial content dominate relevant evidence.
- Temporal poisoning: stale or future-dated instructions appear authoritative.
- Tool/action confusion: a memory states that an action is authorized or completed when Agent policy has not authorized/performed it.

### 4.3 Required containment

- Keep Memory in a structurally separate managed-data region; never concatenate it into System/Developer policy or tool definitions.
- Use explicit source, trust, epistemic, temporal, scope and provenance metadata; these are context for evaluation, not a guarantee.
- Agent retains independent tool/action authorization. Memory text cannot grant tools, permissions or capabilities.
- Apply size/fan-out/depth bounds, source allow/deny policy, suspicious-instruction labeling and output escaping appropriate to the consumer.
- Preserve provenance and uncertainty through summaries/compaction; record omissions and allow expansion when retention permits.
- Reauthorize every referenced Evidence/Provenance object; prevent cross-scope lineage laundering.
- Where risk is high, exclude or quarantine untrusted content and require user/Agent review.
- Monitor injection patterns and downstream policy violations without retaining unnecessary raw content.

**Residual risk:** LLMs may still follow malicious text present in context despite delimiters, labels or policy prompts. No design can promise absolute immunity. Security depends on reducing exposure and authority, independent tool controls, monitoring, and risk acceptance.

## 5. Risk register

| ID | Risk | Impact | Baseline mitigation | Residual / acceptance |
|---|---|---|---|---|
| R-01 | forged identity / producer spoof | cross-principal access or false telemetry | authenticated transport binding, issuer trust, payload comparison | compromised issuer/runtime remains high; security owner accepts |
| R-02 | scope confusion / inheritance bug | cross-tenant disclosure | typed scope tuple, explicit grants, fail-closed | B/I/H semantic alignment and tests open |
| R-03 | revocation race | post-revocation read/write | permission epoch, final reauth, cancel in-flight | already disclosed bytes cannot be recalled |
| R-04 | stale index/cache candidate | forgotten/revoked content leak | fence and epoch in query/cache, canonical revalidation | F implementation and race tests open |
| R-05 | late derivative resurrection | forgotten content reappears | producer registration barrier, dependency inventory, closed watermark | D/E/I barrier proof open |
| R-06 | Adapter offline/stale delivery | stale content in inference | quarantine, reconnect reconciliation, Full Applied gating | H proof absent; G/C dependencies |
| R-07 | prompt injection in memory/evidence | tool misuse or data exfiltration | data-only region, source labels, independent Agent tool policy | model behavior cannot be guaranteed |
| R-08 | summary/compaction laundering | malicious instruction loses provenance | lineage, omission metadata, adversarial compaction tests | model summarizer and policy remain fallible |
| R-09 | audit reconstruction | Forget defeated by logs/tombstones | non-reconstructive tombstone and minimization | external logs/retention operators remain |
| R-10 | backup restore resurrection | forgotten content reappears | restore quarantine + persistent Forget ledger | storage implementation and restore drills open |
| R-11 | external recipient non-response | untracked copy persists | recipient registry, deletion request, Unknown state | outside technical control; exception/contract needed |
| R-12 | legal hold overreach | content retained/accessed too broadly | segregated hold, suppression, minimal retention | legal/privacy decision authority |
| R-13 | denial of service via fan-out/replay | degraded service or unbounded costs | quotas, bounded traversal, idempotency, cancellation | operational limits TO_VALIDATE |

## 6. Adversarial and conformance matrix

A test is PASS only with test artifact/version, environment, fixture, expected and actual result, owner sign-off and retained non-sensitive evidence. This document defines tests; none are claimed executed.

| Test ID | Scenario / attack | Required expected result | Owners |
|---|---|---|---|
| SEC-001 | Payload asserts another user/tenant/Agent/environment | identity mismatch; no receipt or access under forged identity | H/C/E/I |
| SEC-002 | Unknown/revoked issuer key or expired credential | fail closed; no cached ALLOW | H/I |
| SEC-003 | Delegation chain expired, revoked, cyclic or privilege-amplifying | deny; descendants invalidated | I/H |
| SEC-004 | Missing required environment Scope | deny; no fallback to default environment | B/C/E/F/I |
| SEC-005 | Same Memory visible, attached Evidence outside Scope | Memory metadata may be allowed; Evidence dereference denied | D/E/F/I |
| SEC-006 | Cross-scope ANN/lexical/graph/temporal candidate | blocked before candidate/count/fusion; no side channel | F/I |
| SEC-007 | Permission revocation between admission and canonical commit | commit aborts or reauthorizes at linearization point | D/I |
| SEC-008 | Permission revocation during retrieval/cache fill/finalization | no response/cache/Working Set disclosure after revocation fence | F/I |
| SEC-009 | Permission revocation during Context delivery or inference assembly | stale delivery/apply blocked; no Full Applied | C/G/H/I |
| SEC-010 | Permission event gap / offline epoch consumer | protected path pauses until authoritative resync | all |
| SEC-011 | Forget while compiler job leased/retrying/DLQ/replay | no derivative commit/publication after barrier | D/E/I |
| SEC-012 | Forget concurrent with canonical write | barrier orders commit vs suppression; no post-completion write | D/I |
| SEC-013 | Forget during in-flight retrieval/cache/index rebuild | candidate, cache and rebuilt index cannot re-expose target | F/I |
| SEC-014 | Forget during Context ChangeSet/Prepared/Delivered/late ACK | tombstone wins; late ACK stale; no reactivation | G/H/I |
| SEC-015 | Offline Adapter reconnects with stale snapshot | quarantine, fetch current policy/fence, clear/reconcile before apply | G/H/I |
| SEC-016 | Backup restore contains forgotten object | restore quarantined; fence applied before reads/indexing | I/storage |
| SEC-017 | External recipient unavailable or sends unverifiable ACK | Unknown; cannot satisfy completion without approved exception | I |
| SEC-018 | Legal hold present during Forget | immediate suppression; minimum isolated hold copy; explicit exception | I/legal/storage |
| SEC-019 | Audit tombstone/log contains source text or reversible digest | test fails; audit stores only non-reconstructive metadata | I/operations |
| SEC-020 | Prompt injection in retrieved Memory/Evidence | remains data-only; protected instructions/tool auth unchanged; incident observable | C/H/I |
| SEC-021 | Injection survives summary/compaction/paraphrase | provenance/uncertainty preserved; malicious instruction not promoted to authority | E/G/H/I |
| SEC-022 | Entity label/provenance says “system instruction” or “trusted” | label remains untrusted data; no role/authority escalation | D/E/F/G/H/I |
| SEC-023 | Cross-scope source enters shared summary or graph edge | sharing policy checked at every source and output; otherwise denied | B/D/E/F/G/I |
| SEC-024 | Malformed/unknown protocol enum or major schema version | explicit reject/compatibility path; no silent reinterpretation | H/I |
| SEC-025 | Replay old Applied attestation after revocation/Forget | reject as stale by delivery/request/permission/fence epoch | C/G/H/I |
| SEC-026 | Provenance cycle/fan-out and source unavailable | bounded traversal, explicit incomplete result, no recursive runaway | D/E/F/I |

## 7. Test execution requirements

- Use synthetic fixtures with distinct tenants, users, projects, Agent instances and environments.
- Include both positive authorized cases and negative cross-scope cases.
- Inject pauses between each check and its commit/disclosure linearization point.
- Run fault injection for worker crash, queue replay, partition loss, duplicate/out-of-order invalidation, offline Adapter, delayed ACK and backup restore.
- Capture policy version, permission epoch, ForgetFence, relevant typed watermarks, operation IDs and test version without recording raw protected content.
- Re-run after any change to policy evaluation, index backend, cache key, Adapter tier, Context rendering, backup process or retention configuration.

## 8. Risk acceptance

I may propose and document security risk. Acceptance authority is not automatically the I architect:
- cross-tenant isolation, credential forgery, revocation bypass or Forget resurrection: **not acceptable as routine residual risk**; requires remediation before release;
- model prompt-injection susceptibility: explicit acceptance by Agent/product security owner plus tool isolation and monitoring; cannot be accepted as “LLM immune”;
- external recipient/backup retention: only by authorized Privacy/Legal + data owner under a named PolicyException with expiry and disclosure;
- operational availability trade-offs: service owner may accept bounded downtime, never silent protected-data disclosure.



---

## Phase 3.5 threat-model extension — identity, inventory and global Forget

The following threats extend (and do not replace) SEC-001..SEC-026. Tests remain **NOT RUN**.

| ID | Threat / race | Required prevention or detection | Fail-closed / completion consequence | Owner(s) |
|---|---|---|---|---|
| SEC-027 | Cross-tenant / cross-user / cross-project / cross-Agent / cross-instance / cross-task / cross-session / cross-environment ScopeRef confusion | Resolve every typed ScopeRef against authoritative versioned registry; authorize ownership and applicability independently; require explicit environment binding | Deny/Indeterminate; no candidate, dereference, delivery or inference assembly | B + I + consuming owner |
| SEC-028 | Forged Principal, Issuer, ProducerIdentity, Agent instance, AdapterIdentity or ExternalRecipient identity | Verify issuer/key/audience/credential epoch and authenticated transport/workload binding; compare payload claims to authenticated identity | Reject/quarantine; audit security event; never create trusted inventory entry from payload claim | I + H + C |
| SEC-029 | Permission revocation races with old Context, cached ALLOW, lease, queue, retry, DLQ or final commit | Current PermissionEpoch at every protected boundary and at commit/disclosure linearization; invalidate leases/cache/Context on epoch gap | Pause/abort protected action; old Context or TTL cannot authorize | I + all boundary owners |
| SEC-030 | Old Context/snapshot/delta/ChangeSet or Applied/ACK replay after Forget/revocation | Bind to target, ContextVersion, delivery/request ID, session, PermissionEpoch and D fence; reject stale generations using owning authority | No reactivation or Full Applied; target remains Unknown/Pending until reconciled | G + H + I + C |
| SEC-031 | D work-item barrier confused with I ProducerDomainInventoryEpoch | Maintain separate typed fields, authority and validators; reconcile both proofs in global evaluator | Either missing proof blocks completion; no scalar roll-up | I + D + E |
| SEC-032 | New Producer/Recipient/backup route/Adapter region appears after inventory seal | Advance I inventory epoch, invalidate seal, enumerate target, reopen and reevaluate | Prior Completed proof becomes superseded/Reopened | I + domain owner |
| SEC-033 | Backup restore or index rebuild resurrects forgotten content from stale snapshot/WAL/replica | Restore to quarantine; apply persistent current Forget/revocation control ledger before query/index/delivery; verify all paths | Block serving; failed restore suppression reopens Forget | Storage + I + D/F |
| SEC-034 | External recipient or onward recipient retains an untracked copy | Authenticated recipient inventory, contractual/API obligations, target-bound deletion evidence and onward-copy accounting | Unknown or narrow PolicyException; never Confirmed from request receipt | I + Privacy/Legal + recipient owner |
| SEC-035 | H ACK spoofing, wrong Adapter/session/target/Scope/managed-region or stale CapabilityEpoch | Verify authenticated Adapter identity, capability epoch, session-at-ACK, target, ScopeRef, managed region, D fence and integrity proof | Invalid evidence => Unknown/Failed; cannot satisfy mandatory target | H + I |
| SEC-036 | Unsupported Adapter capability treated as successful purge | Map UNSUPPORTED to Unknown; require alternate control and independent exception approval | Completion blocked absent valid active PolicyException | H + I + risk approver |
| SEC-037 | Late derivative or derivative-of-derivative appears after seal/completion | Lineage registration, D barrier terminality, I domain epoch monitoring and late-discovery invalidation | Reopen; suppress and reconcile descendant before reevaluation | D + E + I |
| SEC-038 | PermissionEpoch, ForgetFenceGeneration, inventory epoch, ContextVersion or CapabilityEpoch numerically conflated | Typed namespace validation; owner-specific comparison APIs; reject unknown/mixed epoch | Fail closed; evidence invalid | I + D + F + G + H |
| SEC-039 | ACK/evidence replay, delayed contradictory ACK or evidence outside validity window | Bind evidence to operation/target/action/attempt/session/capability and verifier; enforce action-specific validity | Stale/contradictory evidence Unknown pending reconciliation; preserve audit history | H + I |
| SEC-040 | PolicyException used as broad bypass or remains after expiry | Exact target/scope/action binding, independent approval, hard expiry, compensating controls and expiry monitor | Expiry/revocation reopens; no ordinary retrieval/derivation/delivery | I + Privacy/Legal + data owner |
| SEC-041 | Audit tombstone/log reconstructs forgotten payload or stable low-entropy digest | Minimize to random opaque IDs/coarse class/state; test dictionary/correlation reconstruction; bounded retention | Audit control failure; no claim that Forget evidence is privacy-safe | I + Audit/Privacy |
| SEC-042 | Producer or Adapter identity revoked while an operation is in-flight | Invalidate credential/lease/session and reauthorize at each later boundary; preserve cleanup obligation under separate service authority | No protected work with revoked identity; global cleanup continues only under current delegated authority | I + H + E/D/G |

### Phase 3.5 adversarial acceptance gates

- Cross-scope tests must include distinct tenants, users, projects, Agent identities and instances, tasks, sessions and environments; negative tests must prove no side channel through counts, graph expansion, errors or timing.
- Revocation tests must pause execution between admission, source dereference, stage commit, dependency registration, canonical commit, delivery and final inference submission.
- ACK tests must vary Adapter, instance, capability epoch, session, ScopeRef, managed region, action, operation ID and evidence age independently.
- Inventory tests must add/remove/retire a domain, rotate its issuer, change Scope/capability, add an onward recipient and discover a late derivative while a Forget operation is sealed or evaluated.
- Restore tests must start from stale snapshots with old Context, queues, indexes and backups and prove control-ledger replay before any serving path.
- Global completion tests must prove that each mandatory Unknown/Failed/Unsupported/missing target blocks Completed, and that expiry of an exception reopens it.

A test PASS requires reproducible fixtures, environment, test version, expected/actual result, owner sign-off and non-sensitive evidence. No Phase 3.5 test execution is claimed.
