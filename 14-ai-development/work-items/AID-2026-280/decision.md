---
document_metadata:
  domain: ai-development
  role: decision-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-280/evidence.md"
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-27"
      last_verification_note: "GitHub API source readback; this is a delegated proxy adjudication, not natural-person Owner signature."
    usage_status: Active
    modification_status: Draft
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  steward: "user-authorized operator (delegated by account owner)"
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "One-time proxy adjudication record for the AC8 EXIT-1/EXIT-2 carrier conflict; does not exercise reserved Owner authority."
    canonical_scope_id: "ai-development/req-04-ac8-conflict-adjudication"
    canonical_scope_keywords:
      - "req-04"
      - "ac8"
      - "exit-1"
      - "exit-2"
      - "scope-conflict"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---

# S8 — REQ-04 AC8 conflict adjudication

**裁定 = B**

**裁决性质：代理裁决，非自然人 Owner 签署。** This record determines the evidence and carrier status visible in the pinned repository state. It does not purport to make the reserved natural-person Owner scope decision or to appoint this session as acceptance authority.

## Decision

AC8 remains in REQ-04 for now because its text remains in the canonical Issue body and no effective, authorized scope change has been established. AID-2026-260 contains an EXIT-2 exclusion paragraph, but its own metadata marks it Unverified, Draft, Informative, and explicitly not a natural-person Owner signature. Issue #305 states that a session may not appoint itself or treat transcription of operational instructions as a constitutive delegation instrument. Thus the proxy scope statement cannot discharge AC1's OWNER_ACTION or lawfully change the Issue acceptance boundary.

AID-2026-254 does not satisfy AC8. Its declared root/domain fan-out is a reproducible scope-dispersion proxy, not direct measurement of elapsed attention time, human session/context transitions, reorientation cost, cognitive load, or Agent context-window/token cost. Its own evidence expressly disclaims several of those measurements. Keep it intact as an optional observation; do not represent it as an AC8 pass.

## Q1 — Can AC1 scope confirmation exclude an AC listed by the Issue?

**Yes in principle, but not by unilateral scope-document assertion.**

(a) Where the Issue itself expressly authorizes writing an exclusion into the Issue's exclusion scope (this Issue does: #265 body, final paragraph of “裁定摘要”), a listed AC can be excluded through that authorized route.

(b) Where the Issue does not authorize exclusion, an AC1 scope carrier cannot silently delete or downgrade an AC. A separate authority with power to amend the requirement would first have to authorize that change.

For an exclusion to be a legitimate scope decision rather than post-hoc deletion, all of the following are required:
1. The Issue's own text or a higher valid governance instrument authorizes the exclusion route.
2. The decision is made by the authority actually empowered to confirm scope; a proxy record must point to an independently effective delegation instrument. A session cannot appoint itself.
3. The canonical Issue body is amended so the acceptance list and exclusion statement agree; a comment alone is not a body amendment.
4. The exclusion states a reason, exact excluded dimension, boundary, and effective date/ref.
5. It provides an explicit alternative disposition: a separate work-item carrier, an explicitly out-of-scope observation, or a named residual decision path. “Not required” must not erase where the topic went.
6. The prior AC text/status and carrier history remain auditable; an excluded item is not marked [x] as if its acceptance condition passed.
7. The scope carrier and Issue body identify the signer/authority and do not claim natural-person Owner signature where none exists.

F3 satisfies condition 1. In this case conditions 2 and 3 are not satisfied: AID-260 is only an unverified proxy record and the Issue body was not changed. Therefore EXIT-2 is not an effective exclusion.

## Q2 — Is EXIT-2's basis in the AC1 carrier?

**Yes.** `14-ai-development/work-items/AID-2026-260/scope-confirmation.md:69`, blob `e6425787d2ae3c8aa3e2eb21e1adf7cc1542611a`. The reconciliation subsection is at lines 76–82 in the same blob. This confirms where the claim is recorded; it does not establish the authority needed to make it effective.

## Q3 — Post-hoc exclusion or prior scope decision?

The decisive clock is **canonical publication/effectiveness (merge to main)**, not the authoring timestamp of an unmerged branch file. Timeline (UTC):

| Time | Event | SHA / ID | Effect |
|---|---|---|---|
| 2026-11-26T10:07Z | #265 body restored; AC8 remains [ ] ABSENT | Issue body | AC8 exists as an acceptance item |
| 2026-11-26T13:36:32Z | AC8 ABSENT decision and EXIT-1 / EXIT-2 alternatives | comment 7193586920 | Explicitly authorizes either a work-item carrier or writing exclusion into this Issue; no choice made |
| 2026-11-27T03:41:45Z | AID-260 scope-confirmation first authored, including AC8 EXCLUDED | commit fdb348e2 (per supplied timeline) | Proposal exists on a branch; not yet canonical on main |
| 2026-11-27T03:57:44Z | AID-254 measurement PR merged | 40195e8bf96b9cc6aa254066b9b72968f29ac361 | EXIT-1 measurement becomes canonical first |
| 2026-11-27T04:08:07Z | AID-260 scope PR merged with exclusion text | 10d33b3f6c012e1c0d5649a5279cadb6d27b1a2f | EXIT-2 text becomes canonical after EXIT-1 merge |
| 2026-11-27T04:29:16Z | AID-260 reconciliation appended | a588cd9914949c2c9db7b2c5704d906fd3f05b70 | Reaffirms EXIT-2 after both carriers are on main |
| 2026-11-27T04:29:36Z | Comment 7209840981 posts [x] replacement line for comment use | 7209840981 | Does not edit Issue body |
| 2026-11-27T04:42:31Z | Latest unrelated #265 comment | 7210029242 | No AC8 effect |

**Classification:** post-hoc relative to AID-254's canonical merge, not a prior effective scope decision. The 03:41:45Z authoring time is earlier than PR #1370's merge but is not the effective date of an unmerged draft. Moreover, because the proxy author had no established constitutive delegation, the EXIT-2 text remains a recorded proposal/claim, not a valid scope amendment.

## Q4 — Does AID-254 satisfy AC8's “considered” wording?

**No, not on the evidence as written.** A fan-out proxy is relevant to work-scope dispersion and may inform a future consideration, but AID-254's evidence says it is not a claim about elapsed time, cognitive load, or observed human session count. It does not demonstrate that either human engineering attention cost or Agent context-window/token cost was actually assessed against an agreed REQ-04 acceptance boundary. The threshold of 3 roots is derived from the sample mean of 2.90; it is a scope proxy budget, not an empirically validated attention-cost threshold.

Concrete follow-up required before AC8 can be marked satisfied:
1. **Define the measurement population and unit:** Work Item / PR / review round; separately record human reviewer context handoffs and Agent context-window/token events. Do not combine unlike units.
2. **Record actual human transition events** in session evidence using pseudonymous role/session identifiers, ordered timestamp, source context, destination context, handoff reason, and reorientation duration. Do not record personal content.
3. **Record actual review burden:** number of distinct PRs and version families touched per review session, review-round count, and active review minutes, with an explicit inclusion/exclusion rule.
4. **Record Agent context cost separately:** context-window/token usage and reset/handoff counts only where reliable platform telemetry exists; otherwise mark NOT_MEASURED, never infer from path count.
5. **Provide a reproducible read-only command** (proposed interface, not implemented): `python3 scripts/measure_attention_context_cost.py --ref <commit> --cohort <N> --session-ledger <path> --format json`. Output must include cohort definition, missing-data counts, per-unit distributions, and exact source refs.
6. **Set thresholds from a declared baseline:** retain root fan-out ≤3 as an operational scope proxy only; derive human transition/reorientation soft threshold at the baseline p75 and hard threshold at p95 (or a separately approved absolute cap), publish sample size and confidence/limitations, and define split/escalation handling. Agent token thresholds must be separate.
7. **Evidence and review:** capture at least one reproducible cohort, independently recompute it from committed evidence, document limitations, and obtain the authority required to accept AC8. Until then AC8 remains [ ] PARTIAL.

## Q5 — Single ruling

**B — AC8 remains in scope; AID-2026-254 does not satisfy it.**

AID-2026-254 remains unchanged as an informative, optional fan-out measurement artifact. It is not retroactively converted into an AC8 acceptance carrier. A future authorized work item must perform the direct measurements above; this decision does not assign that implementation to AID-254.

## Q6 — Exact Issue #265 replacement lines

**AC8 (proposed canonical body line):**

```text
- [ ] Attention and context-switching costs are considered. / 考虑注意力和上下文切换成本。 — **PARTIAL**：AID-2026-254 的 declared root/domain fan-out 仅为 manifest scope-dispersion 代理指标，不直接测量耗时、人工上下文切换/重定向成本、认知负荷或 Agent context-window/token 成本；AC8 仍在 REQ-04 范围内，须补充分单位、可复算的实际测量与基线阈值，并经授权验收。carrier: AID-2026-254（可选代理观测，非 AC8 验收载体）；直接测量 carrier: NO_CARRIER_FOUND
```

**AC1 (retain as canonical body line):**

```text
- [ ] Owner confirms requirement scope. / Owner 确认需求范围。 — **OWNER_ACTION**。carrier: `NO_CARRIER_FOUND`（AID-2026-260 是未获有效授权的代理范围记录，不替代 Owner 对范围的确认）
```

Use [ ] for both: AC8 is not satisfied and AC1 remains an Owner action. Do not use [x] for an exclusion; exclusion is not completion. The Issue body is **not changed by this PR** because this session cannot claim the reserved Owner scope authority. The body/comment discrepancy is to be resolved by the authorized Owner/governance authority in the next step: update the Issue body itself (not merely a comment) and then record the resulting body digest. Until that happens, the current Issue body remains canonical and AC8 remains unchecked.

## Carrier correction ledger — C1–C6

| ID | Existing carrier / location | Required correction or disposition |
|---|---|---|
| C1 | Issue #265 body AC8 line vs comment 7209840981 | **Do not treat the comment's proposed [x] line as an Issue-body edit.** New adjudication comment records the [ ] PARTIAL line; canonical body remains unchanged pending authorized body update. |
| C2 | Comment 7209840981 AC8 line | The [x] marker is semantically wrong for an excluded or unsatisfied criterion. Replace in any future canonical body transcription with [ ] PARTIAL (line above); do not edit the historical comment. |
| C3 | Issue #265 AC1 line vs AID-260 “resolves AC1” claim | Keep AC1 [ ] OWNER_ACTION. AID-260's statement that it resolves AC1 must be qualified as a proxy proposal, not effective scope confirmation, until a valid delegation/Owner act exists. |
| C4 | AID-254 manifest line 2/objective and evidence.md:56,61 | Preserve the measurement and its disclaimer. Clarify its title/objective as “declared root/domain fan-out proxy for work-scope dispersion”; do not claim it measures cognitive load or actual context-switch cost. This correction belongs to the AID-254 maintainers, not this work item's file scope. |
| C5 | AID-260 scope-confirmation.md:69 | The sentence “no AID-2026-261 cost-measurement carrier is required” is unsupported and names an ID occupied by an unrelated governance-traceability item. Replace with “No AC8 direct-measurement carrier has been assigned; AID-2026-261 is unrelated.” |
| C6 | AID-260 scope-confirmation.md:86 | The issue-ready exclusion line is malformed (leading § and enclosing backticks). If retained as a proposal, rewrite as a plain blockquote beginning `>` and remove the enclosing backticks; it is not adopted by this B ruling. |

## Explicit Issue-body disposition

**改 / 不改：不改。** No PATCH is made to #265. AC1 is expressly OWNER_ACTION, and Issue #305 records that a session may not constitute its own delegation or appointment. Changing the body here would convert a non-authoritative proxy adjudication into a scope act. The body/comment mismatch is not left ownerless: the authorized Owner or independently empowered governance authority must update the AC8 and AC1 lines in the Issue body in the same step that records the valid scope act; that actor must then read back and record the before/after body SHA-256. Until then, the Issue body prevails over comment 7209840981.

## Attribution

user-authorized operator (delegated by account owner)  
Date: 2026-11-27  
**代理裁决，非自然人 Owner 签署。**
