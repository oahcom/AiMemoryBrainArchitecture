# U-011 Independent Bilingual Semantic Review

- Work Item: AID-2026-001
- Review unit: U-011 / independent bilingual semantic review
- Disposition: FAIL — GOV-DOC-001 bilingual gate not satisfied
- Review baseline commit: 5a24134200f55d6f559a452d509b8dbcd9753719
- Branch: `remediation/aid-2026-001-forget-contract-closure-2026-11-18`
- Repository: `oahcom/AiMemoryBrainArchitecture`
- Reviewer role: independent bilingual semantic reviewer; not the Owner-I authoring session
- Conflict check: no direct authorship conflict identified from the available record

## 1. Exact reviewed artifacts

| Language | Path | Introduced commit | Git Blob SHA | UTF-8 bytes |
|---|---|---|---|---:|
| EN | `14-ai-development/work-items/AID-2026-001/owner-i-r3-governance-rules-u011-v1.md` | `443fbd08ee7275c22ab61e8b354888759b7d53c0` | `241f1ac4c63758bb791eb9b7d94bdfaf70eda66d` | 24388 |
| ZH-CN | `14-ai-development/work-items/AID-2026-001/owner-i-r3-governance-rules-u011-v1.zh-CN.md` | `e1a1f2016e3ad4fb6905e0b069b1c2f5863b85ff` | `ba8f2b0569c834cc384dce0c01b5d918c10a3d0b` | 23192 |

Both exact blobs were fetched successfully by their supplied Blob SHA. The fetched content's UTF-8 byte counts independently match the supplied counts. The branch-resolved file reads returned the same two Blob SHAs. The supplied baseline commit was fetched successfully; Issue #41's latest U-011 registration comment identifies it as the branch head at that registration point. No claim is made that this connector exposed a separate live refs/heads SHA read.

## 2. Chapter-by-chapter semantic crosswalk

| EN section | ZH section | Result | Review note |
|---|---|---|---|
| §1 Authority and invariants | §1 权责与不变量 | PASS | I/D/Storage/Executor authority boundaries and the U-010 Forgotten premise align. |
| §2 Decision envelope and authorization receipt | §2 决策信封与授权回执 | PASS | Required fields, authenticity, binding, scope and replay protections align. |
| §3 PermissionEpoch and revocation race | §3 PermissionEpoch 与撤权竞态 | PASS | Monotonic epoch, authoritative currentness, epoch vector and winner rules align. |
| §4 I authorization precondition | §4 I 侧治理授权前置条件 | PASS | Commit-time authorization gate is not converted into downstream cleanup or physical-erasure prerequisites. |
| §5 Retention/Legal Hold exceptions | §5 保留与 Legal Hold 例外 | PASS | Default deny/defer, authority, record, least privilege, effect boundaries and no resurrection align. |
| §6 Required-target policy and inventory | §6 必需目标策略与清单 | PASS | I policy vs D/Executor discovery ownership, sealing, unknown targets and reassessment align. |
| §7 Governance/result typing | §7 治理评估及例外/结果类型 | PASS | Types remain distinct; ExceptionApproved is not Succeeded; global compliance constraints align. |
| §8 Conformance tests | §8 一致性测试用例 | PASS | I-U011-T01..T16 and their required assertions align in substance. |
| §9 Finding dispositions | §9 Finding 处置 | PASS | Finding IDs, severity, candidate status and Issue #41 reflow align. |
| §10 Approval and remaining gates | §10 批准与剩余门禁 | PASS | Owner-I, D same-SHA, Storage, H/transport, independent review and R3 gates align. |
| §11 Bilingual semantic parity | §11 双语语义一致性 | FAIL | EN retains a stale statement that the Chinese translation is pending; ZH says the complete Chinese counterpart has been authored. |
| §12 Explicit non-claims | §12 明确不作出的声明 | PASS | No implementation, R3 execution, formal approval or finding closure is claimed in either version. |

The Chinese artifact additionally contains a final section titled “双语对应关系与维护约束” with no corresponding English section. It imposes explicit ongoing requirements: update both languages in the same change set, keep state/field/Finding/test identifiers and authority/negative constraints aligned, preserve code identifiers, and bind bilingual PASS to an exact Head. These are normative maintenance constraints, not merely explanatory translation notes. They should be mirrored in English or removed from Chinese if they are not intended to be normative.

## 3. Normative differences

### I-U012-001 — stale translation status in EN §11

**EN source:**

> This file is an English working master with bilingual headings and limited Chinese labels only; it is NOT a complete bilingual artifact. Complete Chinese translation and independent semantic-parity review are PENDING.

**ZH source:**

> 本文件是英文工作稿的完整中文对应稿。两种语言版本旨在逐条保持相同的规范语义……

> 当前完成的是作者侧翻译；独立双语语义一致性审查尚未执行，不得标记为 PASS。

**Difference type:** stale status / factual semantic drift. The EN statement that complete Chinese translation is pending conflicts with the separately supplied, exact-Blob Chinese counterpart and the ZH statement that the translation is complete. The EN statement that the English file alone is not a bilingual artifact is not itself problematic; the pending-translation claim is.

**Recommended correction:** revise EN §11 to state that this English working master has a separately maintained complete Chinese counterpart at the exact ZH path; author-side translation is complete; independent semantic-parity review is the current pending gate. Do not claim PASS until the independent review passes.

### I-U012-002 — Chinese-only normative maintenance section

**ZH-only source (final section):**

> 任一语言版本发生规范性变更时，另一语言版本必须在同一变更集中同步更新。

> 任何状态值、字段名、Finding ID、测试 ID、权限边界、否定性约束和强制性要求均须保持一致；代码标识符不翻译、不改名。

**EN counterpart:** no corresponding final section or equivalent complete list of ongoing maintenance obligations is present. EN §11 does require the final joined contract to contain the same rules in both languages in one frozen change set, but it does not mirror all the explicit maintenance constraints in the Chinese-only section.

**Difference type:** Chinese-only normative addition / scope asymmetry.

**Recommended correction:** add an equivalent English “Bilingual correspondence and maintenance constraints” section, preserving the same requirements, or remove the Chinese-only section if those requirements are not intended to be part of this contract. Prefer mirroring the requirements.

## 4. Required critical semantic points

| Point | EN↔ZH result | Rationale |
|---|---|---|
| COMMIT_WON | PASS | Commit serializes before revocation epoch advance; successful durable commit enters Forgotten; later revocation cannot roll back, remove fence or resurrect Memory. |
| REVOCATION_WON | PASS | Revocation serializes first; commit-time epoch mismatch rejects authorization; no successful suppression commit or Forgotten claim. |
| UNKNOWN | PASS | Unprovable order/current epoch/policy/transaction outcome fails closed before confirmed commit; reconcile; if durable SuppressionCommitted is later proven successful, Forgotten remains terminal. |
| PermissionEpoch | PASS | Monotonic, never reused/decreased, authoritative current-value check, full applicable epoch vector. |
| SuppressionCommitted ⇒ Forgotten | PASS | §1.3 and §3.2 in both versions make successful durable SuppressionCommitted the sole D-domain trigger; I authorization is pre-commit, not a post-commit governance-completion condition. |
| ExceptionApproved ≠ Succeeded | PASS | §5.3 and §7.1 in both versions prohibit treating an approved exception as target success or evidence of target action. |

No conflict with the stated D-side U-010 adjudication was found in these six critical points.

## 5. GOV-DOC-001 gate

**Disposition: FAIL.**

The exact GOV-DOC-001 source file could not be resolved through the available repository paths during this review; this is recorded as a retrieval limitation, not as evidence that the document does not exist. The review nevertheless establishes a substantive bilingual status mismatch and a Chinese-only normative addition. The available repository execution guidance also requires bilingual review to assess meaning/identifiers/statuses/examples/links and treats missing or materially inconsistent bilingual content as BLOCKED/NOT DONE; the repository's bilingual coverage guidance says an unupdated counterpart must be marked STALE and must not resolve an open issue by stronger wording in translation.

The failure is based on the two exact reviewed blobs, not on author-side structural/token parity claims.

## 6. Existing finding disposition

- **I-U011-007 / P2 / Issue #41**
- Decision: **RETAIN OPEN**.
- Reason: the independent review has now been performed, but it did not pass. The two §11/maintenance-section differences above require correction in both language artifacts and a fresh independent exact-Blob review.
- Closure condition: corrected EN and ZH artifacts; exact Blob SHA and UTF-8 byte count for each; same-change-set bilingual update; fresh independent semantic-parity PASS; Issue #41 registration.
- This review does not grant Owner-I approval, Owner-D same-SHA approval, Storage approval, D/I bilateral approval, acceptance, activation or R3 evidence.

## 7. Registration and quota

- Reflow carrier: existing Issue #41.
- Review artifact: this file, on the existing remediation branch.
- No new Issue or PR.
- Open PR preflight immediately before registration: 12; quota freeze respected.
- No production or implementation claim.

