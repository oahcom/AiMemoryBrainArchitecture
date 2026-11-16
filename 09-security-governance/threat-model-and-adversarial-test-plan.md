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

