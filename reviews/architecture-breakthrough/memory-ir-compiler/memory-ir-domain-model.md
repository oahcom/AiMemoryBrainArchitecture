# Memory IR Domain Model (Candidate)

- Research ID: MB-IR-001
- Status: CANDIDATE / NOT A B OWNER DECISION
- Authority boundary: compiler-internal representation only; canonical B objects remain B-owned.

## 1. Design rule

Memory IR is a *compilation artifact*, not a new canonical memory domain. It represents what a compiler stage currently knows, what it does not know, and how it knows it. It must not smuggle a decision about canonical Fact/Claim semantics into a type name.

Use a small typed envelope with extensible payloads and explicit evidence/provenance references. Avoid a universal ontology that requires every memory concept to be a first-class IR operation.

## 2. Proposed layered representation

| Layer | Name | Purpose | Must not do |
|---|---|---|---|
| L0 | Raw Source Envelope | Immutable source/event refs, digest, capture metadata, scope/admission refs | Rewrite source content or imply truth |
| L1 | Extraction IR | Typed mentions, candidate assertions, event candidates, evidence spans, uncertainty | Assign canonical Entity IDs or canonical Fact/Claim identity |
| L2 | Semantic IR | Validated candidate graph, temporal/scope qualifications, provenance DAG, conflict sets | Decide lifecycle/authority or erase disagreement |
| L3 | Commit Projection | Explicit mapping to the current D-owned request contract | Become an alternative canonical schema |

Each layer has a version and a lowering/upgrade policy. L0 should remain replayable subject to retention/privacy rules. L1/L2 can be regenerated from L0 when policy allows. L3 is tied to the exact D contract version and must be rejected if incompatible.

## 3. Candidate node vocabulary (not canonical object types)

- `EventCandidate`: a compiler view of a captured occurrence/report/transition.
- `EntityMention`: a string/span plus context; not an Entity identity.
- `AssertionCandidate`: a subject-predicate-object proposal with epistemic and temporal qualifiers. Neutral pending Fact/Claim ADR.
- `RelationCandidate`: typed relation proposal with unresolved/resolved endpoints.
- `EvidenceRef`: source reference, span, digest, source authority and availability state.
- `DerivationNode`: pass/model/rule execution and parent references.
- `ConflictSet`: mutually incompatible or potentially incompatible candidates, with reason and review disposition.
- `ProcedureCandidate`, `PreferenceCandidate`, `GoalCandidate`: optional semantic tags/payload profiles, not separate canonical types by default.
- `TemporalAssertion`: qualification attached to a candidate, not automatically a separate object.
- `ScopeRef`, `AuthorityRef`, `ConfidenceEstimate`, `LifecycleHint`: typed attributes, not interchangeable scalar fields.

Do not create separate IR node classes for every product idea. Start with a closed core union plus extension payloads whose namespace and schema version are explicit.

## 4. Minimum envelope

```json
{
  "ir_version": "0.1.0",
  "node_id": "stable-opaque-id",
  "node_kind": "assertion_candidate",
  "payload": {"subject_mention": "Mira", "predicate": "lives_in", "object": "Tokyo"},
  "qualification": {
    "epistemic": "reported",
    "valid_time": {"from": "2025-01-01", "to": null},
    "recorded_at": "2026-11-18T00:00:00Z",
    "scope_ref": "scope:opaque",
    "authority_ref": "authority:opaque",
    "confidence": {"value": 0.72, "kind": "model_estimate"}
  },
  "evidence_refs": ["evidence:opaque"],
  "provenance_ref": "derivation:opaque",
  "diagnostics": [],
  "extensions": {}
}
```

Illustrative only. Field names and enums are not frozen, and this is not a B canonical schema. In production, actor, permission, retention and Forget bindings must use the current Owner contracts, not this example.

## 5. Fact / Claim handling

The IR must not decide whether Fact and Claim are one object, two objects, or a specialization relation. Use a neutral candidate node and preserve the extraction's semantic intent as an uninterpreted tagged payload if needed. Lowering into canonical types is disabled until B's authorized ADR is approved and each consumer adopts the exact version.

A compiler IR may distinguish epistemic state (reported/inferred/verified/disputed/retracted) from lifecycle state (candidate/consolidated/active/superseded/archived/forgotten) as separate dimensions because the inspected B guidance explicitly treats them as orthogonal. The IR must not treat confidence as truth, authority as permission, or a verified label as an automatic commit instruction.

## 6. Entity resolution placement

Perform cheap lexical normalization and mention extraction before IR. Keep unresolved mentions in L1. Run candidate matching after L1, in a scope-filtered semantic pass, and record:
- candidate canonical IDs and resolver version;
- features/evidence used for the match;
- ambiguity score and alternatives;
- decision provenance (automatic, policy, human review);
- unresolved/abstained result.

Do not rewrite source mentions. Do not perform cross-scope lookup before authorization. Do not assign permanent Entity IDs in parsing.

## 7. Provenance and uncertainty

Provenance is a required IR edge for every derived node, not just an optional free-form field. Evidence is separate from derivation: evidence says what supports/refutes/qualifies a proposition; provenance says how the candidate was produced.

Represent unknowns explicitly. Conflict is a set/edge among candidates, not a single status overwriting one candidate. Supersession/expiry should be represented as qualified temporal/lifecycle relations, not deletion of prior evidence. A plan or goal remains a plan/goal candidate until outcome evidence exists.

## 8. Scope of candidate design

This model is intentionally smaller than the requested candidate catalogue. Procedure, Preference and Goal should initially be tags or payload profiles on AssertionCandidate/EventCandidate unless a distinct lifecycle, identity, query, or authorization requirement demonstrates that they need separate node kinds.
