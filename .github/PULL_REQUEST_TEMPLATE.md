# Pull Request / Pull Request 描述

## Work item and traceability / 工作项与可追溯性
- Work Item ID:
- Related issue(s):
- AI-assisted work: YES | NO
- Session evidence reference(s): path list, or N/A when the answer above is NO
- Related PR(s):
- Session ID / Prompt ID + version + SHA-256:
- Accountable Owner:
- Implementing session / author:
- Independent reviewer (GitHub login):
- Integration / Acceptance authority:
- PR-GOVERNANCE-001 status / 标准状态: PROPOSED | ADOPTED | EXCEPTION

### Per-Issue AI session evidence / 每个 Issue 的 AI 会话证据
One row per Related Issue; the status must equal that Issue's own declaration. `LEGACY_UNDECLARED` is only for an Issue created before the gate's effective time that carries no declaration.
每个 Related Issue 一行，状态须与该 Issue 自身的声明一致；仅对门禁生效时间之前创建且未声明的 Issue 使用 `LEGACY_UNDECLARED`。

| Related Issue | Issue AI-assisted work | Evidence refs for this Issue |
| --- | --- | --- |
| #NNN | YES or NO | path, or N/A |

## Change / 变更
- Objective / 目标:
- Scope and non-goals / 范围与非目标:
- Changed paths / 变更路径:
- Base branch + exact base SHA:
- Head branch + exact Head SHA:
- Why this is a distinct integration unit (if a new PR) / 新建 PR 的独立性理由:

## Decisions and authority / 决策与权威
- [ ] PROPOSED
- [ ] ACCEPTED (include authority and decision record)
- [ ] REJECTED
- [ ] UNRESOLVED
- Decision records and exact source pins / 决策记录与精确源版本:
- Affected Owner(s) and explicit approval references / 受影响 Owner 与明确批准证据:

## Verification — exact Head only / 验证——仅接受精确 Head 证据
- Exact tested Head SHA:
- Required/applicable check names:
- Each check conclusion + workflow/run URL:
- Missing / pending / skipped / failed checks and reason:
- Commands, environment and reproducible results:
- Security / compatibility / migration / fault cases:
- Checks NOT RUN and reasons:
- Has Head changed since these checks? If yes, refresh all evidence:

## Review independence / 审查独立性
- Independent reviewer GitHub login:
- Review state: APPROVED | COMMENTED | REQUESTED_CHANGES | NOT_REVIEWED
- Review commit SHA:
- Same-session / delegated-role disclosure (independence is session-level; identity is only the carrier):
- Owner approvals required and exact evidence:
- Unresolved review conversations / blocking findings:

A COMMENT is not an APPROVE. Independence is a property of the reviewing session, not of the GitHub account: a separate session reviewing a change it did not author is independent and may report through the same identity. AI role simulation inside the authoring session is not independent review and is not Owner approval.
COMMENT 不是 APPROVE。独立性是审查会话的属性，不是 GitHub 账号的属性：未撰写该变更的另一个会话即构成独立审查，可沿用同一身份报告。在撰写会话内做 AI 角色模拟不构成独立审查，也不构成 Owner 批准。

## Bilingual documentation / 双语文档
- Chinese paths:
- English paths:
- Parity evidence:
- GOV-DOC-001 gate result:
- Manifest: BILINGUAL-MANIFEST: COMPLETE | PENDING | BILINGUAL-EXCEPTION: APPROVED
- Exception Owner / source revision / missing path / due date / tracking Issue / approval evidence (if applicable):

## Merge decision / 合并决策
- Disposition: MERGE | HOLD | REMEDIATE | SUPERSEDED | REJECT
- Exact current Head SHA re-read immediately before merge:
- Mergeability / conflict status:
- Dependency PRs and verified merge states:
- Branch protection/ruleset status as read from GitHub API:
- Are required checks and independent approvals actually enforced by platform? YES | NO | UNKNOWN
- If NO/UNKNOWN, record the limitation and administrator escalation; do not claim a hard gate:
- Expected Head SHA supplied to merge operation:
- Merge method:

## Closeout / 结项
- [ ] Work Item index updated at `14-ai-development/work-items/INDEX.md` where applicable
- [ ] Related Issue/PR links updated bidirectionally where practical
- Actual merge status (do not claim before merge):
- Target branch:
- Actual merge commit SHA:
- Post-merge readback SHA and verification:
- Remaining work / follow-up Owner / due condition:

Do not mark a check PASS unless it ran on the exact stated Head SHA. A passing check from another PR or earlier Head is not evidence for this PR. A PR merge proves repository integration only; it does not imply domain Owner acceptance, security acceptance, production readiness or deployment success. An `AI-SESSION-EVIDENCE: PRESENT` verdict from the session-evidence gate means the declared files exist in the Head tree and their bytes are unchanged; it does not mean the evidence is authentic, complete, or produced by the model it claims.
除非检查确实运行于上述精确 Head SHA，否则不得标记 PASS。其他 PR 或旧 Head 的成功检查不能作为本 PR 的证据。PR 合并只证明仓库集成，不代表领域 Owner 验收、安全验收、生产就绪或部署成功。session-evidence 门禁的 `AI-SESSION-EVIDENCE: PRESENT` 结论只表示所声明的文件存在于 Head 树中且字节未发生变化，不代表证据真实、完整或由其所声称的模型产出。

Reference / 规范依据: [PR-GOVERNANCE-001](../14-ai-development/PR-GOVERNANCE-001.md), [Issue #130](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/130), [P0 Issue #134](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/134).
