---
document_metadata:
  domain: ai-development
  role: work-record
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
        - "14-ai-development/work-items/AID-2026-323/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "This record transcribes operator-supplied read-only measurements and derives bounded conclusions without claiming independent validation."
    usage_status: Active
    modification_status: Modified
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "Records the evidence and decision alternatives for AID-2026-323 without establishing or amending repository-wide governance requirements."
    canonical_scope_id: "ai-development/aid-2026-323-evidence"
    canonical_scope_keywords:
      - "AID-2026-323"
      - "principal-distinctness"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# AID-2026-323 — Evidence and Decision Record

## 1. Purpose and decision question

Issue #1285 concerns the principal-level distinctness requirement in `14-ai-development/PR-GOVERNANCE-001.md`, §5 item (2).

The decision question is:

**Should the repository introduce a minimal, verifiable principal registry to enforce principal-level distinctness, or should the normative requirement be downgraded to a textual-value constraint with principal-level distinctness explicitly recorded as unverifiable?**

This record does not decide between those alternatives. It establishes what the supplied repository measurements prove, what they do not prove, the precise changes each alternative would require, and the evidence and authority necessary to choose.

The evidence baseline is:

`5670357db7a836d4f26838dbaf99494af41e2b65`

All E1–E4 measurements below are operator-supplied read-only observations on that base. They are not represented as independently reproduced measurements.

## 2. Measured evidence

### E1. Normative requirement

The English normative text is at:

`14-ai-development/PR-GOVERNANCE-001.md:142`

The relevant paragraph states:

> (2) **Isolation**: that session must not be the `implementing_ai_session` of any related work item; AI role simulation inside one session is not an independent assessment, per §5 above. The manifest must carry `sponsor`, `accountable_owner` and `implementing_ai_session` at the same time, each of them either at top level or inside the `session_evidence` entries and never in both places; `sponsor` and `accountable_owner` may identify the same principal, but `accountable_owner` and `implementing_ai_session` must identify different principals, and textual differences between their values do not establish that distinction, which is determined by principal identity.

The Chinese normative text is at:

`14-ai-development/PR-GOVERNANCE-001.md:146`

The relevant item states:

> (2) **隔离约束** —— 该会话不得是任何相关工作项的 `implementing_ai_session`；同会话内角色扮演自评按 §5 原文不构成独立评估。manifest 必须同时携带 `sponsor`、`accountable_owner` 和 `implementing_ai_session` 三个字段，每个字段或位于顶层、或位于 `session_evidence` 条目内，不得两处并存；`sponsor` 与 `accountable_owner` 可以指向同一主体，但 `accountable_owner` 与 `implementing_ai_session` 必须指向不同主体，且字段值的字符串不同不构成主体独立性的证据，主体独立性必须按主体身份判定。

The paragraph's closing sentence at English line 142 and Chinese line 149 states that the requirement is exemptible only through an exception record naming this paragraph; an exception naming §5 or reviewer independence generally does not cover it.

**Finding:** The normative requirement is explicitly about principal identity, not merely string inequality. Its text also expressly rejects textual differences as evidence of principal independence.

### E2. No repository principal registry or resolution surface

The operator ran:

`git ls-files | grep -i principal`

The complete tracked-path result was:

```text
09-security-governance/principal-actor-and-authorization-contract.md
docs/en/02-domain-model/principal-actor-binding-mapping.md
docs/en/09-security-governance/principal-actor-and-authorization-contract.md
docs/zh-CN/02-domain-model/principal-actor-binding-mapping.md
docs/zh-CN/09-security-governance/principal-actor-and-authorization-contract.md
```

There are five tracked paths. They are prose contracts and bilingual mirrors, not a principal data registry, machine-readable identity schema, or list of resolved principals.

The complete tracked-file inventory of `09-security-governance/` is:

```text
09-security-governance/README.md
09-security-governance/forget-retention-backup-and-erasure-policy.md
09-security-governance/global-forget-target-inventory-and-completion-evidence.md
09-security-governance/principal-actor-and-authorization-contract.md
09-security-governance/scope-and-revocation-policy.md
09-security-governance/security-and-identity-overview.md
```

None of these six tracked files is a principal registry.

The closest identity contract contains the following measured content:

`09-security-governance/principal-actor-and-authorization-contract.md:52`

```text
- Status: **CANDIDATE semantic contract; joint approval required from B/H and Architecture Governance**
```

Line 59:

```text
A Principal is a stable, opaque security subject established by an authenticated issuer. Candidate principal kinds:
```

Line 68:

```text
A Principal identifier is namespaced by issuer and tenant/security domain. Display names, email strings, model names, user-supplied IDs and payload claims are descriptive only. Principal IDs are not reused after retirement.
```

Line 319 delegates the end-to-end trust-chain sequence, Issuer Trust Registry requirements, and Producer/Agent/Adapter/Runtime Session binding rules to:

`phase-3.6-principal-trust-chain-authorization-revocation.md`

The operator ran:

`git ls-files | grep phase-3.6-principal-trust-chain`

Result:

```text
0 tracked paths
```

The referenced upstream document is not tracked in the repository.

The principal/actor mapping also delegates identity resolution:

- `docs/en/02-domain-model/principal-actor-binding-mapping.md:62`
- `docs/zh-CN/02-domain-model/principal-actor-binding-mapping.md:62`

Both assign `authenticated_principal_ref` to "I Principal registry, trusted Issuer" and mark the row "Candidate until joint B/H/Governance approval".

Finally:

`01-system-architecture/system-boundaries.md:218`

```text
| SB-01 | OPEN | Define canonical principal and workload identity model in Security/BMCP specs. |
```

**Finding:** The repository contains a candidate semantic definition and references to a future registry/trust-chain dependency. It does not contain the registry, the referenced upstream trust-chain document, or an approved and operational identity-resolution surface. SB-01 remains OPEN in the measured baseline.

### E3. No gate reads or resolves the comparison

The operator inspected:

`scripts/governance/session_evidence/validate.py`

Measured findings:

- `MANIFEST_FIELDS` at lines 1041–1049 contains:
  - `implementing_ai_session`
  - `executed_prompt_snapshot_file`
  - `executed_prompt_sha256`
  - `executed_prompt_bytes`
  - `executed_prompt_provenance`
  - `session_reference_status`
  - `session_evidence_ref`
- `sponsor` and `accountable_owner` are absent from that list.
- The string `principal` occurs **0** times in the file.

The operator ran:

`grep -rn accountable_owner scripts/`

The complete result was exactly one line:

```text
scripts/ci/check_work_item_manifest_schema.py:20:    "id_status", "sponsor", "accountable_owner", "acceptance_authority",
```

The corresponding search:

`grep -rn sponsor scripts/`

similarly finds only the required-key tuple.

Nothing under `scripts/` compares `accountable_owner` with `implementing_ai_session`. Nothing under `scripts/` resolves either value through an identity table.

**Finding:** The measured validators establish neither principal identity nor principal-level distinctness. The only measured reference to `accountable_owner` in scripts is membership in a required-key tuple. The session-evidence validator does not consume the two-field comparison or a principal-resolution source.

### E4. Actual values across all work-item manifests

The operator ran a read-only script over:

`14-ai-development/work-items/*/manifest.yaml`

Number of manifests found: **128**.

#### accountable_owner

12 distinct non-null values:

```text
  91  USER-PRINCIPAL-DELEGATED
  18  None
   5  NOT_ASSIGNED
   3  Integration Owner
   2  A
   2  USER-PRINCIPAL-DELEGATED (session-eligible per D-2026-1120-02)
   1  Project Owner adoption authority; not inferred from this session
   1  Project Owner (adoption authority)
   1  USER-PRINCIPAL-DELEGATED (Owner instrument, Issue
   1  USER-PRINCIPAL-DELEGATED (session-eligible under the user's continuous instruction in this session: "所有 owner 都可以是一个会话，你持续到收敛即可")
```

#### sponsor

8 distinct values:

```text
  93  USER-PRINCIPAL-DELEGATED
  24  None
   4  project user
   2  USER-PRINCIPAL-DELEGATED (human principal via D-2026-1120-02)
   2  NOT_ASSIGNED
   1  USER-PRINCIPAL-DELEGATED (current user delivery instruction)
   1  USER-PRINCIPAL-DELEGATED (human principal via the continuous instruction in this session: "所有 owner 都可以是一个会话，你持续到收敛即可")
   1  user-authorized operator (delegated by account owner)
```

#### implementing_ai_session

38 distinct non-null values; full distribution:

```text
  41  None
  36  NOT_RECORDED
   5  opencode-go/deepseek-v4.1-flash
   3  session-r44-reg-b
   3  session-r45-coordinator
   3  req05-convergence-session-identity-not-recorded
   3  ChatGPT-GPT-6
   2  owner-proxy-2026-11-26
   2  a904-opencode-author
   1  session-966-ownerproxy
   1  session-266-056-wording
   1  session-799-orchestrator
   1  session-req01-r32
   1  session-req01-r34
   1  session-req01-r35
   1  a955
   1  session-903-fixture-collision
   1  session-w1081-tests
   1  session-1029-declared-vs-protected
   1  session-wo01-r47-coordinator
   1  session-w1088-edited-trigger
   1  session-a1084
   1  a1078-pr1078-rebase-session
   1  a1081-opencode-author
   1  a944-opencode-author
   1  a925-opencode-author
   1  a752-opencode-author
   1  session-283-f02-residuals
   1  NOT_AVAILABLE
   1  session-evidence-fail-closed-session
   1  owner-proxy-2026-11-26-104
   1  session-evidence-coverage-gap-record-session
   1  a827-opencode-author
   1  NOT_EXPOSED_BY_PLATFORM
   1  ChatGPT-GPT-6-S6-C
   1  GOVREC-2026-11-27
   1  S6-B
   1  ChatGPT-GPT-6-S6-A
   1  6b090a00-c1b0-83ec-ad26-9668c882a144
```

#### Cross-field measurements

The operator supplied these additional measurements over the same 128 manifests:

```text
both non-null and byte-identical (accountable_owner == implementing_ai_session): 0
overlap of the two value sets: []
distinct accountable_owner values: 12
distinct implementing_ai_session values: 38
```

The operator's measured characterization is that the two fields are drawn from disjoint vocabularies:

- The owner side uses delegation/role vocabulary such as `USER-PRINCIPAL-DELEGATED`, `NOT_ASSIGNED`, `A`, and `Integration Owner`.
- The session side uses execution-handle vocabulary such as `session-r44-reg-b`, `a904-opencode-author`, `ChatGPT-GPT-6`, and model names such as `opencode-go/deepseek-v4.1-flash`.

Zero rows are byte-identical. The prohibition on byte-identical values is therefore never triggered by a direct comparison on this measured dataset.

Furthermore, **79 of 128 rows** carry no identity handle in the session field:

```text
None: 41
NOT_RECORDED: 36
NOT_AVAILABLE: 1
NOT_EXPOSED_BY_PLATFORM: 1
```

The principal contract at `09-security-governance/principal-actor-and-authorization-contract.md:68` classifies model names and user-supplied IDs as descriptive only. Consequently, the largest class of session identifiers cannot be treated as principal identifiers merely because they are populated.

**Finding:** The observed field-value distributions establish that textual equality is not a useful discriminator in this dataset. They do not establish that the corresponding accountable owners and implementing sessions belong to different principals.

## 3. Unsatisfiability proof

### 3.1 What the requirement demands

E1 makes the required proposition:

`principal(accountable_owner) != principal(implementing_ai_session)`

This is a statement about the identity of two subjects.

It is not equivalent to:

`accountable_owner != implementing_ai_session`

The normative text expressly says that textual differences do not establish principal independence.

### 3.2 What would be required to decide the proposition

To establish the proposition from repository artifacts, a repository-verifiable mechanism would need, at minimum:

1. A defined and approved principal identity model.
2. A trusted identity-resolution source or registry.
3. An unambiguous resolution from each manifest field value to a principal identity.
4. A rule for handling absent, ambiguous, untrusted, or unresolved identity references.
5. A validation gate that reads both resolved identities and asserts that they differ.

The measured repository state does not provide these elements.

### 3.3 Proof from the measurements

**First: no usable identity-resolution surface exists.**

E2 identifies all five tracked paths containing `principal`. They are prose contracts and bilingual mirrors. The candidate contract delegates trust-chain and registry requirements to an upstream document that has zero tracked paths. SB-01 is explicitly OPEN.

There is therefore no measured, approved repository registry through which the two field values can be resolved.

**Second: the available values do not supply an alternative resolution mechanism.**

E4 identifies 12 distinct non-null accountable-owner values and 38 distinct non-null implementing-session values. Their value sets have an empty intersection.

That empty intersection proves only that their textual representations differ. It does not prove that they denote different subjects.

The 79 rows with missing or non-recorded session handles make a direct identity determination even less possible. The candidate contract's line 68 further disallows treating model names and user-supplied IDs as authoritative principal identities.

**Third: no measured gate makes the comparison.**

E3 shows that the session-evidence validator does not contain the term `principal`, does not read `accountable_owner`, and does not resolve the two fields. The other measured script reference to `accountable_owner` is only a required-key tuple. No measured script compares the two values or consults an identity table.

**Fourth: the existing textual comparison cannot replace the missing identity comparison.**

E4 reports zero byte-identical non-null pairs. Even if a direct inequality check were added, it would establish only textual inequality. The normative clause explicitly rejects that as proof of principal distinctness.

### 3.4 Conclusion

On the measured baseline, the principal-distinctness proposition is **neither verifiable nor refutable from the available repository artifacts**.

This is an artifact-based unsatisfiability finding, not a claim that the two principals are actually identical, that they are actually different, or that an external identity authority could never establish their relationship.

More precisely:

- There is no measured principal-resolution surface.
- There is no measured principal registry.
- The referenced upstream trust-chain document is absent.
- The identity contract remains CANDIDATE and requires joint approval.
- SB-01 remains OPEN.
- No measured gate reads or enforces the principal-level comparison.
- The observed textual values cannot establish the required identity relationship.

Accordingly, the repository cannot currently produce a defensible pass or fail determination for the principal-level distinctness requirement.

A non-empty field, a different string, a model name, a session handle, or a delegation label is not a substitute for a trusted principal resolution.

This conclusion follows from E1–E4; it does not adopt the issue reporter's assertions without examination.

## 4. Convergence path A — introduce a minimal principal registry

### 4.1 Decision intent

Retain the existing normative obligation in §5 item (2), but introduce the smallest trusted and machine-verifiable identity-resolution mechanism sufficient to determine whether the accountable owner and implementing AI session are different principals.

This path must not become a general-purpose identity platform.

### 4.2 Minimum required registry content

The registry must contain only the information necessary to resolve the two manifest fields into stable principal identities.

A principal record must contain, at minimum:

1. `principal_id`: a stable, opaque identifier for the principal.
2. `issuer`: the authenticated issuer establishing that identity.
3. `tenant_or_security_domain`: the namespace in which the identifier is valid.
4. `principal_kind`: sufficient to distinguish the relevant human, service, or agent/session principal categories.
5. `bindings`: explicit, field-qualified references mapping the accepted source value to that principal.

The `principal_id` must be unique within its issuer and tenant/security-domain namespace. Retired principal identifiers must not be reused.

Each binding must identify:

- The source field: `accountable_owner` or `implementing_ai_session`.
- The exact source value being resolved.
- The target `principal_id`.
- The trusted issuer or provenance establishing the binding.

The registry must reject ambiguous bindings. A source value must not resolve to multiple principals within the same applicable namespace and field.

A field-qualified binding is necessary because the two existing fields use different vocabularies. An owner-side delegation label and a session-side execution handle must not be treated as equivalent merely because a human-readable description suggests a relationship.

An unresolved value must remain unresolved. It must not be silently converted into a principal based on display name, model name, free-form description, or operator assumption.

### 4.3 Minimum resolution and gate behavior

The resolution procedure must:

1. Read `accountable_owner` from its permitted manifest location.
2. Read `implementing_ai_session` from its permitted manifest location.
3. Resolve each field independently using its field-qualified registry binding.
4. Verify that each resolution identifies exactly one trusted principal.
5. Compare the resulting principal identities, including their issuer and tenant/security-domain namespace.
6. Assert that the resolved principals are different.

The gate's essential assertion is:

`resolve(accountable_owner).principal_id != resolve(implementing_ai_session).principal_id`

The comparison must operate on the canonical, namespace-qualified principal identity, not on the original field strings.

Both resolutions must succeed before the distinctness assertion can pass.

Missing, ambiguous, malformed, untrusted, or unresolvable bindings must fail closed. An unresolved identity must not be interpreted as proof of distinctness.

The existing exception mechanism remains governed by the normative paragraph's own exception requirements. A general reviewer-independence exception must not be treated as covering this paragraph.

### 4.4 Explicit exclusions

The minimal registry does not include:

- General user-account management.
- Authentication implementation.
- Authorization policy or permission evaluation.
- Credential storage.
- Token issuance or validation.
- Session lifecycle management.
- Model identity or model-version identity as a substitute for principal identity.
- Workload attestation beyond what is strictly needed to establish the binding.
- A general identity-provider integration framework.
- Cross-tenant identity correlation.
- Historical identity reconstruction where no trusted evidence exists.
- Automatic inference of principal identity from prose, display names, email strings, or model names.

Those capabilities are outside the narrow requirement and must not be introduced under the justification of satisfying §5(2).

### 4.5 Exact change surface

This path requires a separate implementation and approval carrier. The following is the bounded intended change surface, not an assertion that any file has been created or modified.

| Repository surface | Required change |
|---|---|
| `09-security-governance/principal-actor-and-authorization-contract.md` | The Principal definition and identifier rules around lines 59–68 must receive an approved, minimal registry and binding specification. The CANDIDATE status at line 52 must be resolved through its required joint approval. |
| `09-security-governance/principal-registry.yaml` | Introduce the minimal machine-readable registry, with the principal records and field-qualified trusted bindings defined above. This is a proposed new path, not an existing file. |
| `scripts/ci/check_work_item_manifest_schema.py` | Extend the relevant manifest validation so that the required fields and permitted locations are checked consistently with the identity-resolution contract. |
| `scripts/governance/session_evidence/validate.py` | Add the principal-resolution and distinctness assertion, or establish an explicitly integrated validator that this gate invokes. The resulting enforcement must not be a string-inequality substitute. |
| `14-ai-development/PR-GOVERNANCE-001.md` | The §5 item (2) paragraph at English line 142 and Chinese line 146 may require an independently approved clarification describing the registry-backed enforcement. No change is authorized by this work item. |

The registry and gate implementation must not be treated as approved merely because this decision record describes them.

### 4.6 Dependency and cost

<badge color="warning">Depends on OPEN SB-01</badge>

This path depends on SB-01:

`01-system-architecture/system-boundaries.md:218`

```text
| SB-01 | OPEN | Define canonical principal and workload identity model in Security/BMCP specs. |
```

The repository's principal contract also requires joint B/H and Architecture Governance approval.

The implementation cost therefore cannot honestly be stated as a fixed, self-contained script change. It depends on:

- Resolving the canonical principal/workload identity model.
- Establishing trusted issuer and binding semantics.
- Obtaining the required contract approval.
- Providing a usable registry source.
- Integrating and testing fail-closed resolution.

The minimal record and gate described above bound the eventual implementation scope, but they do not eliminate the upstream identity-model dependency.

Until SB-01 is resolved and the required contract is approved, this path cannot be represented as implementation-ready.

### 4.7 Verifiable acceptance criteria

Path A is accepted only when all the following evidence exists in its separate implementation carrier:

**A1 — Approved identity contract**

The principal identity and binding contract has the required B/H and Architecture Governance approval. The approved text defines the namespace, stable identifier, issuer, and binding semantics needed by the gate.

**A2 — Machine-readable registry**

A tracked registry exists. Every principal record contains the required minimum fields. Every binding is field-qualified, issuer-backed, unambiguous, and resolves to an existing principal record.

**A3 — Positive resolution**

A fixture or equivalent controlled test demonstrates that two different manifest field values can resolve to the same principal. The gate rejects this case.

**A4 — Negative resolution**

A fixture or equivalent controlled test demonstrates that two trusted values resolve to two different canonical principal identities. The gate accepts this case.

**A5 — Fail-closed behavior**

Tests demonstrate rejection of:

- An absent owner binding.
- An absent session binding.
- An ambiguous binding.
- An unknown principal reference.
- An untrusted issuer.
- A namespace mismatch.
- An unresolved session handle.
- An attempt to use a model name or descriptive label as authoritative principal identity.

**A6 — Actual manifest integration**

The validator reads both permitted manifest locations, respects the prohibition against duplicate placement, resolves both values, and evaluates the canonical principal identities rather than merely comparing the strings.

**A7 — Repository enforcement**

The relevant CI gate invokes the identity comparison and fails when a fixture demonstrates principal collision. The tests are executed and their results are recorded.

**A8 — Governance alignment**

Any required clarification to PR-GOVERNANCE-001 is carried through its own approval chain and separate carrier. The implementation does not claim that this work item authorized a canonical-document change.

### 4.8 Failure mode if path A is wrong

If the registry is adopted and later found to be wrong, the primary failure is a false identity distinction or a false identity collision.

Examples include:

- Two different principals being incorrectly assigned the same identifier.
- One principal being represented by multiple identifiers without a trusted correlation rule.
- A session binding being assigned to the wrong human or service principal.
- A compromised or untrusted issuer establishing a misleading binding.
- An incomplete registry incorrectly rejecting legitimate work.
- An incorrect namespace rule causing identities from separate security domains to be treated as identical.

The operational consequence is that the gate may incorrectly accept a non-independent assessment or incorrectly reject a genuinely independent one.

The corrective response must be to repair the identity model, registry, and bindings under their approval and provenance requirements, then rerun the acceptance tests. Disabling the comparison or silently falling back to textual inequality is not an acceptable repair.

## 5. Convergence path B — downgrade §5(2)

### 5.1 Decision intent

Replace the unimplementable principal-level distinctness obligation with an explicitly limited textual constraint:

> The `accountable_owner` and `implementing_ai_session` values must both be non-empty and must not be byte-identical. Principal-level distinctness is recorded as unverifiable.

This is a deliberate reduction of the normative obligation, not an implementation of the existing principal-level requirement.

### 5.2 Exact normative replacement

The proposed replacement for the relevant English requirement is:

> The manifest must carry `sponsor`, `accountable_owner` and `implementing_ai_session` at the same time, each of them either at top level or inside the `session_evidence` entries and never in both places. `sponsor` and `accountable_owner` may identify the same principal. The `accountable_owner` and `implementing_ai_session` values must each be non-empty and must not be byte-identical. These textual constraints do not establish principal-level distinctness. Principal-level distinctness is unverifiable from repository artifacts and is recorded as unverifiable; satisfaction of this paragraph must not be interpreted as evidence that the two values identify different principals.

The corresponding Chinese normative replacement must communicate the same reduced obligation and preserve the explicit statement that主体独立性不可验证 and is not established by textual inequality.

The replacement must preserve the paragraph's exception semantics consistently with the revised requirement.

### 5.3 Obligation explicitly given up

This path gives up the obligation to establish that `accountable_owner` and `implementing_ai_session` represent different real-world or security principals.

It retains only these machine-checkable constraints:

1. Both values are present in the permitted manifest location.
2. Both values are non-empty.
3. Their byte representations are not identical.

No principal registry is implied by these checks.

### 5.4 What a reader may no longer infer

After this downgrade, a reader may not infer any of the following from a passing manifest or gate:

- That the accountable owner and implementing session are different principals.
- That the accountable owner is independent of the implementation session.
- That a human owner and an AI session are distinct security subjects.
- That different names, labels, model names, or session handles correspond to different identities.
- That reviewer independence has been established by this particular field comparison.
- That the manifest has been checked against a trusted identity authority.

A passing textual check establishes only textual compliance with the reduced requirement.

It does not establish principal independence.

### 5.5 Exact change surface

This path also requires a separate approval and implementation carrier.

| Repository surface | Required change |
|---|---|
| `14-ai-development/PR-GOVERNANCE-001.md` | Replace the English §5 item (2) paragraph at line 142 and its Chinese counterpart at line 146 with the approved reduced requirement. Preserve consistent bilingual semantics and exception handling. |
| `scripts/ci/check_work_item_manifest_schema.py` | Extend or integrate validation to enforce non-empty `accountable_owner` and `implementing_ai_session` values in the permitted locations. |
| `scripts/governance/session_evidence/validate.py` | Integrate the non-empty and byte-inequality checks, or establish an explicitly invoked validator for them. Do not describe the checks as principal resolution. |
| `14-ai-development/work-items/` manifest documentation and applicable guidance | Update any directly applicable explanatory text that continues to describe the reduced textual check as proof of principal-level independence. |

The canonical paragraph is the central normative change surface. The other changes are required to make the reduced obligation enforceable and prevent documentation from continuing to imply the abandoned identity guarantee.

No such changes are authorized or performed by this work item.

### 5.6 Verifiable acceptance criteria

Path B is accepted only when all the following evidence exists in its separate approval and implementation carrier:

**B1 — Canonical approval**

The revised English and Chinese §5(2) text is approved through the canonical document's required approval chain.

**B2 — Explicit obligation reduction**

The approved text states all three conditions:

- Both values must be non-empty.
- The values must not be byte-identical.
- Principal-level distinctness is recorded as unverifiable.

It must not imply that the textual comparison proves identity independence.

**B3 — Required-field and placement validation**

The validator rejects:

- A missing `accountable_owner`.
- A missing `implementing_ai_session`.
- An empty value.
- Duplicate placement in both permitted manifest locations.

**B4 — Byte-identical rejection**

A test with byte-identical non-empty values is rejected.

**B5 — Byte-different acceptance**

A test with two non-empty, byte-different values is accepted by the reduced textual constraint, even when no principal registry exists.

**B6 — No identity claim**

The gate output, documentation, and acceptance evidence do not label a byte-different pair as principal-distinct or independently verified.

**B7 — Explicit unverifiable state**

The applicable evidence or decision-record mechanism records principal-level distinctness as unverifiable rather than silently treating the absence of an identity registry as proof of distinctness.

**B8 — Regression and governance verification**

The relevant tests are executed, results are recorded, and the approved canonical wording is consistent across both language versions and the applicable implementation guidance.

### 5.7 Failure mode if path B is wrong

If this downgrade is later found to be insufficient, the principal risk is that the reduced textual constraint permits two values belonging to the same principal.

A manifest can pass because its values differ while both values actually refer to the same underlying subject.

This is not a hidden validator defect under path B; it is the explicit consequence of giving up principal-level verification.

If the resulting governance risk is unacceptable, the Owner must initiate a separately approved restoration of the principal-level obligation and resolve the identity-model dependency before claiming that the original guarantee is enforceable.

The existing reduced gate must not be retrospectively described as having established principal independence.

## 6. Comparison of the two paths

| Decision dimension | Path A — minimal registry | Path B — downgrade |
|---|---|---|
| Existing principal-level obligation | Retained | Given up |
| Machine-verifiable result | Canonical principal identities differ | Non-empty values are byte-different |
| Trusted identity resolution | Required | Not required |
| Registry | Required | Not required |
| SB-01 dependency | Yes; currently OPEN | Not required for the reduced textual check |
| Contract approval | Required | Canonical-document approval required |
| Main implementation cost | Identity model, registry, trusted bindings, fail-closed gate | Textual validation and accurate disclosure |
| False assurance risk | Incorrect registry or bindings | Readers mistakenly treating textual difference as identity independence |
| What a passing check establishes | Distinct resolved principals | Textual compliance only |

Neither path is authorized by this record.

The two paths are alternatives, not cumulative requirements. A hybrid that retains the existing principal-level wording while implementing only byte-inequality checks is not an acceptable convergence outcome.

## 7. Decision ownership and evidence required

### 7.1 Decision authority

The choice belongs to the accountable Owner of the canonical `PR-GOVERNANCE-001.md` requirement, acting through the document's applicable governance and approval chain.

Architecture Governance is a required participant in resolving the candidate principal contract described at:

`09-security-governance/principal-actor-and-authorization-contract.md:52`

For path A, the canonical identity-model dependency also requires resolution of SB-01 through the responsible Security/BMCP specification owners and the joint approval identified by the candidate contract.

For path B, the Owner must explicitly approve the reduction of the existing normative obligation. The authoring session cannot make that reduction on the Owner's behalf.

No individual Owner identity or approval is asserted by this record. The manifest's `acceptance_authority` remains:

`Owner acceptance not recorded`

### 7.2 Evidence that would settle the choice

Evidence supporting path A must include:

1. A recorded SB-01 resolution defining the canonical principal and workload identity model.
2. The approved principal contract and its issuer/namespace semantics.
3. A concrete registry and binding specification.
4. Evidence that both manifest values can be resolved to authenticated principal identities.
5. A working fail-closed gate and tests demonstrating same-principal rejection and different-principal acceptance.

Evidence supporting path B must include:

1. An explicit Owner decision accepting the loss of principal-level distinctness as a verifiable obligation.
2. Approval of the exact revised English and Chinese normative text.
3. Confirmation that the reduced obligation is sufficient for the intended governance risk.
4. A passing implementation of the non-empty and byte-inequality requirements.
5. Explicit documentation that principal-level distinctness remains unverifiable.

The decisive question for the Owner is:

**Is principal-level distinctness a mandatory governance guarantee that must justify resolving SB-01 and funding the minimal registry, or is textual non-identity with an explicit unverifiable status sufficient for the intended risk boundary?**

Until that decision and its supporting evidence are recorded, neither path is selected.

## 8. Canonical-document and work-item boundary

**This work item does not modify `14-ai-development/PR-GOVERNANCE-001.md`.**

`PR-GOVERNANCE-001.md` is Canonical and Approved.

Any modification to that document requires its own approval chain and its own carrier. This requirement applies equally to:

- Retaining §5(2) with a registry-backed enforcement clarification.
- Downgrading §5(2) to the reduced textual constraint.
- Changing the English and Chinese normative wording.
- Altering its exception or enforcement semantics.

This work item is a non-canonical, informative decision record. It records measured evidence, establishes the current verification limitation, describes two convergence paths, and recommends that the accountable Owner make an explicit choice.

It does not amend normative text, create an exception, authorize a registry, implement a gate, approve a downgrade, or claim that either path has been accepted.

The canonical source remains unchanged by this work item.

## 9. Recommendation and disposition

The evidence supports one immediate recommendation:

**Do not claim that the existing repository satisfies or enforces principal-level distinctness.**

The measured evidence establishes that no repository-verifiable mechanism currently determines that proposition.

The Owner should make an explicit decision between:

- Path A, retaining the stronger guarantee and accepting the SB-01-dependent identity-model and registry work; or
- Path B, explicitly reducing the guarantee and ensuring that textual compliance is never represented as principal-level independence.

This authoring session does not select the path.

No Owner acceptance is asserted. No implementation is claimed. No CI result is claimed. No PR merge is claimed.

Issue #1285 remains OPEN pending the Owner's decision and the corresponding separately authorized carrier.
