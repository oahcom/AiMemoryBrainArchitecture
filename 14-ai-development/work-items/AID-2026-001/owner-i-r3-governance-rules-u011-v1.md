# Owner I U-011 — Authorization, Revocation, PermissionEpoch and Governance Evidence Contract
# Owner I U-011 — 授权、撤权、PermissionEpoch 与治理证据契约

- Work Item: AID-2026-001
- Dispatch: relay-011; instruction source: ChatGPT user instruction; supplied timestamp: 2026-11-18 22:35 +08:00
- Conversation ID: UNAVAILABLE_TO_EXECUTING_SESSION (not fabricated)
- Role prompt: CHATGPT-OWNER-I-001 v2.0; `14-ai-development/prompts/owners/I/owner-session-v2.md`; source blob `abf8551e37580f1e18a8f956ba453d88918a87b2`; source commit: `6b5db2918cffc2281deb22fd9858a37dbaeec726`; prompt SHA-256: NOT_VERIFIED
- Global rules: AI-EXEC-001 v1.0 ADOPTED; AI-EXEC-002 v1.0 ADOPTED
- Baseline: remediation/aid-2026-001-forget-contract-closure-2026-11-18 @ `eb6aa17c9cefb51434234cdb0f5503197416b9bf` (dispatch-supplied and Issue #41 U-010 comment corroborated; recheck before any later write)
- Class/Risk: ARCH / SEC / DOC; R3
- Status: I-SIDE CONTRACT CANDIDATE; formal Owner-I approval NOT CLAIMED; D/I same-SHA approval NOT GRANTED
- Language status: English working master; complete Chinese translation PENDING; bilingual semantic parity NOT SATISFIED
- Reflow: existing Issue #41; no new Issue/PR

## 1. Authority and invariants / 权责与不变量

1. I owns security principals, authenticated actor/delegation, authorization decisions, PermissionEpoch, revocation ordering, privacy/retention/legal-hold policy, global required-target policy, governance assessment and exception approval/evidence.
2. D alone owns canonical Memory lifecycle, the meaning and trigger of Forgotten, ForgetOperation phase semantics and D-domain completion. This contract does not redefine them.
3. The D-side U-010 decision is treated as the interface premise: a successful durable `SuppressionCommitted` is the sole D-domain transition trigger to `Forgotten`; I authorization is a pre-commit condition, not a post-commit governance-completion condition. After commit, later failure, revocation or unknown status MUST NOT resurrect the Memory or lower/remove the fence.
4. Storage alone approves and proves durable serialization, atomic commit and visibility. Executors prove only their own capability-bounded target actions. I cannot approve either boundary on their behalf.
5. `Forgotten`, `DDomainCompletion`, `GovernanceAssessment`, each `PerTargetResult`, exception disposition and `PhysicalErasureEvidence` are separate typed facts. No single boolean or label may collapse them into “deleted everywhere”.
6. This is a candidate contract artifact. It is not an adopted production policy, implementation, test result, Owner-I formal approval, D/I same-SHA approval, Storage approval, acceptance or activation.

## 2. Authenticated authorization decision and receipt / 认证授权决策与回执

### 2.1 Decision envelope

An authorization decision MUST be a verifiable, immutable decision envelope containing at least:

- `decision_id`: globally unique, non-reusable identifier;
- `issuer_id` and issuer key/version: trusted I-authorized decision issuer;
- `subject_principal_id`: authenticated requesting principal;
- `actor_principal_id`: effective actor, if acting through delegation;
- `delegation_chain`: ordered, verifiable delegation references and constraints; empty only when direct authority applies;
- `action`: explicit operation (e.g. `FORGET`);
- `resource_scope`: stable target/resource identifiers and explicit scope boundaries;
- `purpose`: declared purpose bound to the request;
- `policy_id`, `policy_version`, and policy evaluation context/revision;
- `permission_epoch`: the I-issued monotonic epoch for the authorization subject/policy domain;
- `decision`: `ALLOW` or `DENY`; no implicit allow;
- `not_before`, `expires_at`, and `issued_at`;
- `request_hash`: digest of the canonical request fields, including action, principal/delegation, scope, purpose and applicable preconditions;
- `audience`: the intended service/operation/commit boundary;
- `nonce` or equivalent replay-resistant identifier;
- `provenance` and cryptographic integrity/authenticity material.

The envelope MUST be signed or otherwise authenticated by a trusted I-authorized issuer. A caller-supplied boolean, unsigned payload, log line, UI state, executor acknowledgement, or possession of a decision ID alone is not an authorization receipt. Verification MUST establish issuer trust, signature/integrity, audience, request binding, validity window, nonce/replay status, delegation constraints and policy version.

### 2.2 Authorization receipt

A commit-bound authorization receipt is the verified decision plus the verification outcome and commit-attempt binding. It MUST include:

- the complete decision-envelope reference and immutable digest;
- verification result and verifier identity/version;
- the exact `operation_id`, request hash, actor, action, target scope and purpose;
- the applicable PermissionEpoch and policy revision;
- the commit-attempt/transaction identity and the serialization-point check result;
- decision and verification timestamps from trusted time sources;
- a unique receipt ID and integrity-protected provenance.

A receipt is valid only for its exact audience, operation, request hash, scope, purpose, policy context, epoch and validity interval. It is not transferable to another operation or wider scope. Any material request change requires a new decision and receipt.

## 3. PermissionEpoch and revocation race protocol / PermissionEpoch 与撤权竞态协议

### 3.1 Epoch semantics

1. I maintains a monotonically increasing PermissionEpoch for each defined authorization subject/policy domain. Epoch values MUST never be reused or decrease.
2. Any authorization-affecting change (revocation, delegation withdrawal, privilege reduction, principal disablement, policy change that invalidates prior grants) MUST atomically advance the relevant epoch in the I authorization authority.
3. A decision is current only if its epoch equals the authoritative current epoch for every applicable authorization domain at the serialization check. “Issued recently”, cache freshness, queue order or a previously successful preflight is not a substitute.
4. Epoch comparison MUST be performed against an authoritative, linearizable or equivalently fenced current-value source. If the current epoch cannot be read or proven, the result is UNKNOWN and the operation fails closed before commit.
5. If a request depends on multiple principals/delegations/policies, its receipt binds the complete epoch vector, not a single convenient epoch. Any mismatch invalidates the receipt.

### 3.2 Winner rule at the commit serialization point

Authorization and revocation MUST share one deterministic serialization order at the durable suppression commit boundary. The rule is:

- **COMMIT_WON**: the commit transaction validates the authenticated receipt, current epoch vector, policy revision, scope and validity, and atomically records the suppression/fence at a serialization point before the revocation epoch advance takes effect. Storage must prove the ordering and durable atomicity. The Memory enters Forgotten at that successful commit as defined by D. A later revocation does not roll back the commit, remove the fence or resurrect Memory.
- **REVOCATION_WON**: the revocation/epoch advance serializes first. The commit-time epoch comparison detects the mismatch and rejects the authorization. No suppression commit is reported as successful and no Forgotten transition is claimed. A new authorization decision is required if policy permits retry.
- **UNKNOWN**: the system cannot prove which event serialized first, cannot establish authoritative epoch/current policy, or cannot prove the durable transaction outcome. Before a confirmed commit, fail closed and do not claim success; reconcile transaction state before retry. If durable `SuppressionCommitted` is later proven to have succeeded, D's terminal Forgotten rule applies and must not be undone.

A preflight authorization check is advisory only. The authoritative check MUST be repeated inside or atomically coupled to the transaction that establishes the suppression commit. A time-of-check/time-of-use gap between epoch validation and commit is prohibited. The exact mechanism (transactional compare-and-swap, serialization lock, fenced epoch token, or equivalent) is an implementation choice for Storage and the responsible implementation Owners; I specifies the security property, not Storage's internal mechanism.

### 3.3 Failure and replay

Invalid signature/issuer, wrong audience, request-hash mismatch, scope expansion, expired/not-yet-valid receipt, revoked delegation, stale epoch, policy revision mismatch, nonce replay, unavailable authoritative epoch, or UNKNOWN ordering MUST fail closed before commit. Retries MUST be idempotent and bound to the same operation/request identity; a changed request requires a new decision. An ambiguous transaction result MUST be reconciled against durable commit evidence before retrying a destructive action.

## 4. I governance completion precondition at SuppressionCommitted / SuppressionCommitted 的 I 治理前置条件

I's authorization precondition for the D-owned commit is satisfied only when all of the following are verified at the commit serialization point:

1. The decision envelope is authentic and issued by a currently trusted I-authorized issuer.
2. The authenticated subject, effective actor and delegation chain are valid and authorized for the exact action.
3. The action, operation, target scope, purpose and canonical request hash match exactly.
4. The decision is `ALLOW`, within its validity interval and addressed to the committing service/operation.
5. Every applicable PermissionEpoch equals the authoritative current epoch; no relevant revocation or policy invalidation serialized first.
6. The applicable policy version/revision is current and permits the requested operation.
7. No applicable legal hold or mandatory retention rule prohibits this operation or the requested scope. If a hold/retention rule requires defer or denial, I MUST return that outcome, not silently override it.
8. The receipt is replay-safe and has not been consumed for a different operation or incompatible commit attempt.
9. The commit-time verifier can provide integrity-protected evidence of the checks and their serialization relationship.

This list defines I's security authorization gate only. It is NOT a prerequisite that all downstream cleanup, all cross-system targets, all retention periods, or physical erasure be complete before D may perform its `SuppressionCommitted` transition. Those are separately evaluated under the applicable policy and typed governance assessment. If a particular legal/retention rule prohibits suppression itself, authorization is denied/deferred before commit; it must not be represented as a post-commit delay of Forgotten.

## 5. Retention and Legal Hold exceptions / 保留与 Legal Hold 例外

### 5.1 Default and authority

Retention/Legal Hold is deny/defer by default where applicable law, binding policy or a valid hold prohibits deletion or suppression of the affected data. Only an explicitly designated I policy authority may approve a permitted, narrowly scoped exception. Requesters, executors, D, Storage or an automated workflow cannot self-approve an I exception. If applicable law does not permit an exception, no I approval can create one.

### 5.2 Required exception record

Every exception decision MUST have an immutable record containing:

- `exception_id`, decision ID and status (`PENDING`, `APPROVED`, `DENIED`, `EXPIRED`, `REVOKED`, `SUPERSEDED`);
- named approving I authority, authenticated principal, role/authority basis and delegation evidence;
- affected operation, exact target IDs, data classes, systems/regions and scope boundaries;
- legal-hold identifier or retention policy identifier/version, jurisdiction and cited basis (subject to privilege controls);
- explicit reason, necessity/proportionality rationale and alternatives considered;
- exact permitted action and prohibited actions;
- residual data/exposure description, access restrictions and compensating controls;
- evidence references, provenance, integrity metadata and decision timestamp;
- effective time, expiry, next review date, accountable policy owner;
- re-evaluation triggers, including hold release/change, policy change, scope/target change, evidence expiry, restore, access-control change or expiry;
- disposition after expiry/revocation and required follow-up action.

An exception MUST be least-privilege, target-specific, purpose-bound and time-bounded. Blanket, indefinite, implicit or retroactive exceptions are prohibited. Material scope changes require a new decision. Expiry does not silently renew an exception.

### 5.3 Effect boundaries

An approved retention/legal-hold exception:
- does not change D's Forgotten state or reverse a committed suppression;
- does not authorize ordinary access, retrieval, derivation, delivery, replay or restoration of suppressed content;
- does not prove executor success, target cleanup or physical erasure;
- does not set any `PerTargetResult` to `Succeeded`;
- does not itself establish global `GovernanceAssessment.Compliant`;
- may support only a separately typed `CompliantWithException` assessment when every required policy condition and compensating control is evidenced;
- must produce `Deferred` or `NonCompliant` where the legal/policy basis does not permit an exception or required controls/evidence are missing.

A legal hold may require preservation of specifically identified evidence. Such evidence must be isolated, access-controlled, purpose-limited, integrity-protected and retained only for the authorized period. It must not contain unnecessary Forgotten content; evidence references and minimal metadata are preferred.

## 6. Cross-system required-target policy interface / 跨系统必需目标策略接口

### 6.1 I policy versus D/executor discovery

I owns the global policy declaring which target classes and obligations are mandatory for a given data class, jurisdiction, operation and policy revision. D owns its domain dependency/inventory contract and domain discovery semantics. Each executor owns discovery and capability reporting within its system boundary. I does not dictate the internal discovery algorithm and cannot claim an executor has discovered all local targets without evidence.

The policy interface MUST define:
- policy ID/version/revision and effective interval;
- applicable data classes, jurisdictions, operation types and principal/purpose conditions;
- required target classes and obligations (suppression, access denial, derived-data cleanup, replica/backup treatment, recipient evidence, restore fencing, etc.);
- conditional applicability rules and explicit exclusions with rationale;
- required evidence type, freshness window, provenance and accepted terminal result per target class;
- unsupported-capability treatment and escalation owner;
- inventory revision/seal requirements and invalidation triggers;
- exception eligibility and required authority/evidence.

### 6.2 Inventory revision and sealing

Each assessment binds to an immutable inventory revision containing at least inventory ID, revision, discovery source/owner, discovered-at time, scope, policy revision, target identities/classes, capability states, exclusions and integrity digest. D/executors provide the inventory facts they own; I evaluates coverage against the I policy.

An inventory may be considered sealed for assessment only when the responsible discovery owners attest that the declared discovery process completed for that revision, all known sources were queried, unresolved discovery errors are represented, and exclusions are explicit. “Sealed” means fixed input for one assessment, not proof that no undiscovered target exists.

Unknown, unregistered, newly discovered, unsupported or unexplained mandatory target classes MUST prevent `Compliant`. New targets or a new inventory revision invalidate the prior assessment and require reassessment. Policy revision changes, new data-class/jurisdiction facts, restore events, evidence expiry or relevant permission/hold changes also trigger reassessment.

I may define mandatory coverage and accept/reject evidence against policy; I MUST NOT invent target discovery facts or mark a target action successful. If completeness cannot be demonstrated, the assessment is `Pending`, `Deferred` or `NonCompliant`, never `Compliant`.

## 7. Governance assessment and exception/result typing / 治理评估与例外/结果类型

The following are distinct types and MUST NOT be coerced into one another:

- `PerTargetResult` (executor-owned): `NotStarted`, `InProgress`, `Succeeded`, `Failed`, `Unknown`, `Unsupported`, `NotEvidenced`.
- `ExceptionDecision` (I-owned): `Pending`, `Approved`, `Denied`, `Expired`, `Revoked`, `Superseded`, with immutable exception reference.
- `GovernanceAssessment` (I-owned): `Pending`, `Compliant`, `NonCompliant`, `Deferred`, `CompliantWithException`.
- `DDomainCompletion` (D-owned) and `MemoryLifecycle` (D-owned) remain as defined by D; I only consumes their typed references.

Rules:
1. `ExceptionApproved` is not a `PerTargetResult` and MUST NOT be stored, displayed, aggregated or mapped as `Succeeded`.
2. An approved exception records a policy disposition for a residual obligation; it is not evidence that the target action occurred.
3. `CompliantWithException` is allowed only if each exception is valid, applicable, in scope, unexpired, independently approved and supported by required controls/evidence, and every other mandatory target/obligation meets policy.
4. A required target that is pending, failed, unknown, unsupported or not evidenced blocks `Compliant`; partial success cannot be aggregated as global compliance.
5. Governance assessment MUST cite the exact inventory revision, policy revision, authorization receipt, target evidence set and exception decisions it evaluated.
6. The assessment is invalidated by inventory/policy changes, exception expiry/revocation, new legal hold, evidence expiry, restore, or any material change to authorization or target scope.
7. Neither `Compliant` nor `CompliantWithException` rewrites D's `Forgotten` or D-domain completion state, and neither proves physical erasure absent target-specific evidence.

## 8. Required conformance cases / 必需一致性测试

These are test specifications only; none is claimed executed.

| Test ID | Scenario | Required assertion |
|---|---|---|
| I-U011-T01 | forged/unknown issuer or invalid signature | authorization rejected; no commit |
| I-U011-T02 | audience, operation, request hash, purpose or scope mismatch | receipt rejected; no commit |
| I-U011-T03 | expired/not-yet-valid receipt or replayed nonce | fail closed; no commit |
| I-U011-T04 | current PermissionEpoch differs from receipt epoch | stale receipt rejected |
| I-U011-T05 | revocation epoch serializes before commit | REVOCATION_WON; no commit |
| I-U011-T06 | commit serializes before later revocation | COMMIT_WON; durable Forgotten remains terminal; no resurrection |
| I-U011-T07 | serialization/current epoch cannot be proven | UNKNOWN; fail closed before commit and reconcile |
| I-U011-T08 | delegation revoked or narrowed during race | epoch/currentness check rejects stale delegation |
| I-U011-T09 | Legal Hold/mandatory retention prohibits action | deny/defer; no exception unless legally/policy permitted |
| I-U011-T10 | exception missing approver, scope, basis, expiry or controls | exception invalid; no compliant-with-exception assessment |
| I-U011-T11 | exception approved but target action not performed | target remains non-success; no false Succeeded |
| I-U011-T12 | required target unknown/unsupported/unregistered | GovernanceAssessment cannot be Compliant |
| I-U011-T13 | new target/inventory or policy revision after assessment | previous assessment invalidated; reassess |
| I-U011-T14 | exception expiry/revocation or hold change | reassess; no silent renewal |
| I-U011-T15 | all target evidence present but D domain completion absent | I assessment does not declare D completion |
| I-U011-T16 | D Forgotten committed while cleanup remains pending | Forgotten remains terminal; GovernanceAssessment remains separately pending/noncompliant as applicable |

Execution requires a reproducible harness, fixtures, commands, output, environment and exact tested commit SHA. Current status: NOT RUN / NOT EVIDENCED.

## 9. Finding dispositions / Finding 处置

| Finding | Severity | I-side disposition in U-011 | Reflow |
|---|---|---|---|
| I-U009-001 | P1 | Receipt envelope, validation, PermissionEpoch vector and COMMIT_WON / REVOCATION_WON / UNKNOWN ordering specified; implementation, H/transport binding and race tests remain open | Issue #41 |
| I-U009-002 | P1 | D trigger conflict accepted as resolved on D side: I defines only the commit-time security authorization precondition in §4; exact joined D/I contract and same-SHA approval remain open | Issue #41 |
| I-U009-003 | P1 | Typed retention/legal-hold exception authority, record schema, bounded effect and deny/defer rules specified; legal-policy validation and implementation remain open | Issue #41 |
| I-U009-004 | P2 | I global required-target policy interface, inventory revision/sealing and invalidation rules specified; D/executor discovery and evidence remain their owners' responsibility | Issue #41 |
| I-U009-005 | P2 | ExceptionDecision separated from PerTargetResult; ExceptionApproved cannot map to Succeeded; GovernanceAssessment rules specified | Issue #41 |
| I-U011-006 | P2 | Dispatch conversation ID unavailable to this execution context; relay-011 and supplied timestamp retained without fabrication | Issue #41 |

These are author-side candidate resolutions, not closure claims. Each finding remains OPEN_PENDING_INDEPENDENT_REVIEW_AND_REQUIRED_OWNER_EVIDENCE until its objective closure conditions are met.

## 10. Approval and remaining gates / 批准与剩余门禁

- This artifact is an I-side candidate contract for integration into the joined D/I contract.
- AI-EXEC-002 §5 prohibits treating AI role-play as Owner approval. Accordingly, this session does not claim formal Owner-I approval merely by writing in the Owner-I role. The accountable Owner-I authority must approve this exact artifact/Blob or the final joined exact content SHA through the project's recognized approval mechanism.
- Owner D must approve the same exact joined bilingual content SHA. Approval of separate files, different commits, summaries or different hashes is not same-SHA approval.
- Storage must separately approve and evidence durable serialization/atomicity/visibility. This contract does not prescribe or approve Storage internals.
- H/transport and other affected Owners must acknowledge principal, audience, delegation, target/scope and evidence bindings within their own boundaries.
- Independent integration/security review, bilingual semantic-parity review and reproducible R3 runtime/race/fault-injection tests remain PENDING / NOT RUN.
- D-R3-D-003 remains a bilateral gate. AID-2026-001 remains BLOCKED_PENDING_R3_EVIDENCE.
- No production activation, acceptance, merge-to-main or implementation completion is authorized or claimed.

## 11. Bilingual semantic parity / 双语语义对等

This English working master has a separately maintained complete Chinese counterpart at `14-ai-development/work-items/AID-2026-001/owner-i-r3-governance-rules-u011-v1.zh-CN.md`. Author-side translation is complete. The independent bilingual semantic review of the prior exact pair (EN Blob `241f1ac4c63758bb791eb9b7d94bdfaf70eda66d`; ZH Blob `ba8f2b0569c834cc384dce0c01b5d918c10a3d0b`; review baseline `5a24134200f55d6f559a452d509b8dbcd9753719`) completed with **FAIL**, identifying `I-U012-001` and `I-U012-002` (both P2; reflowed to Issue #41). Those findings are being remediated in this bilingual change set and remain open pending a fresh independent review of the corrected exact Head. Do not mark bilingual parity PASS or use these files alone as an approved joined contract. The final joined contract must incorporate the same rules in both language versions in one frozen change set and be reviewed against GOV-DOC-001.

## 12. Explicit non-claims / 明确不作出的声明

No production authorization service, epoch store, transaction protocol, exception workflow, inventory discovery, target execution, Storage atomicity or audit pipeline is claimed implemented. No R3 test was run. No formal Owner-I or D/I same-SHA approval is claimed. No finding is closed by this document alone.


## Bilingual correspondence and maintenance constraints

- English working master: `owner-i-r3-governance-rules-u011-v1.md`
- Chinese counterpart: `owner-i-r3-governance-rules-u011-v1.zh-CN.md`
- Both files belong to the same AID-2026-001 / U-011 rule version.
- When either language version receives a normative change, the other language version MUST be updated in the same change set.
- All state values, field names, Finding IDs, test IDs, authority boundaries, negative constraints and mandatory requirements MUST remain aligned; code identifiers MUST NOT be translated or renamed.
- Translation completion does not mean independent semantic review has passed; bilingual PASS may be recorded only by an independent reviewer bound to the exact Head.
- Both files remain candidate contracts; translation does not automatically make either file an ADOPTED production policy.