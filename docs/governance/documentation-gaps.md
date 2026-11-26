---
document_metadata:
  domain: security-governance
  role: work-record
  lifecycle:
    approval:
      decision_status: Under-Review
      approver: NOT_RECORDED
      decision_date: NOT_RECORDED
      approved_version: null
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "00-governance/architecture-document-management-policy.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Records gaps observed during the GOV-DOC-002 rollout; no independent verification of each gap's status exists."
    usage_status: Active
    modification_status: Unchanged
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
    normative_status: Informative
    canonical_conflict_status: None
---

# Documentation gaps / 文档缺口登记

Referenced-but-missing normative documents. Each entry records a link that could not be resolved during the GOV-DOC-002 rollout.

指向但缺失的规范文档。每条记录在 GOV-DOC-002 推行过程中无法解析的链接。

This file is governed by GOV-DOC-002 even though `docs/` as a whole is not: the policy cites it in three places as the record of what remains unclosed, so a change here that escaped the gate would let the governance record drift outside governance. It is listed individually in `GOVERNED_FILES` rather than by directory, to keep the exception as small as its reason.

本文件虽位于整体不受治理的 `docs/` 下，仍受 GOV-DOC-002 治理：条例三处引用它作为"尚未闭合事项"的记录，因此若对它的修改能绕过门禁，治理记录本身就会漂移到治理之外。它在 `GOVERNED_FILES` 中按单文件登记，而非按目录，以使例外的范围与理由一样小。

| ID | Missing document | Referenced from | Disposition |
|---|---|---|---|
| GAP-01 | `phase-3.5-forget-suppression-and-cursor-consumption.md` (Phase 3.5 Runtime Forget Suppression and Typed Cursor Consumer Contract) | `docs/en/05-memory-runtime/{retrieval-engine, runtime-overview, working-set-and-cache}.md`, `docs/zh-CN/05-memory-runtime/{retrieval-engine, runtime-overview, working-set-and-cache}.md` | OPEN — never committed to this repository. Referencing text preserved; links replaced with an explicit missing-document marker. Content must NOT be reconstructed by an agent. |
| GAP-02 | Governance enforcement on direct pushes to `main` | `00-governance/architecture-document-management-policy.md` §8, `.github/workflows/document-management.yml` | PARTIAL — `--require-changed` runs on both pull requests (PR base) and direct pushes (`github.event.before`). Residual gap: the first push of a branch has no base commit, so the workflow falls back to the whole-tree scan. That scan now returns **INCOMPLETE (exit 2)** while backlog remains, so it fails loudly rather than reporting a pass it cannot justify — but it still cannot prove the *newly added* files are classified, only that a backlog exists. Closing it requires branch protection that mandates pull requests. |
| GAP-03 | Honesty of an exclusion reason in the scope registry | `00-governance/architecture-document-management-policy.md` §2, `00-governance/document-scope-registry.yaml` | PARTIAL — the ninth review showed this was not only unproven but already violated: `docs/` was excluded as "not documentation" while 26 of its files are architecture documents (minimum-runnable architecture, canonical transaction, source-of-truth inventory), and their own `DRAFT / NON-NORMATIVE` header is a value of `lifecycle.approval.decision_status`, not a reason to be outside classification. That directory is now `backlog`: scanned, counted, and reported as unclassified. What remains unresolved is narrower: DM-14 can check that an exclusion names `not-documentation` and gives a bilingual reason, but it cannot check that the claim is true. `reviews/` (196 Markdown files, review transcripts) is the only large exclusion still resting on that basis. Closing it requires a human to defend the exclusion, which is a review duty, not a machine check. |
| GAP-04 | A mirror can be **stale while its annotation count agrees** | `scripts/check_bilingual_docs.py` (existence), `00-governance/architecture-document-management-policy.md` §9.1 (`M-05`) | OPEN — found three times on 2026-11-25/26, and the third time is the one that names the gap. `check_bilingual_docs.py` proves both files exist and point at each other; it does not read either body. Counting annotations across the three copies catches drift in *density* — it caught `docs/zh-CN/.../OWNER-DECISION-REVIEW-INDEPENDENCE-001.md` carrying seven fewer notes than root, and later root carrying one fewer than zh. It does **not** catch a body that was rendered stale while its count stayed plausible: `GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036` had its English segment corrected on 2026-11-24 and its **Chinese segment inside `docs/en` left at the old text**, still asserting a retracted and verifiably false claim (that no document defines independence at the session level — zero hits; the real counts on `1259f1af` are 8 / 10 / 11 / 6), while the three copies sat at 2 / 4 / 2 annotations and looked consistent. Only a byte comparison of the bodies finds that, and only where the root body is itself Chinese, so the mirror is expected to be identical rather than a translation. A whole-tree check on that narrower class (root body ≥15% CJK, 25 groups) is currently clean: 25 / 25 identical. Closing this properly needs the same check as a gate rule, which means deciding that "root body is Chinese ⇒ zh mirror must be byte-identical" is a contract and not a coincidence — that is a policy decision (`M-05` territory), not a tooling change. |

## GAP-04 detail / 详情

The failure mode is worth stating separately because the obvious detector is the wrong one.

A stale mirror and a correct mirror can carry the same number of dated annotations, the same front matter, the same headings, and the same length. The difference lives inside one paragraph. Any check that counts something — annotations, CJK characters, headings, line counts — is looking at a projection of the body, and the projection agreed in all three cases found so far.

What does work, on the class of documents where it is well defined: **compare the bodies directly**. For a document whose root body is Chinese, the `docs/zh-CN` mirror is not a translation and should be byte-identical; a diff is drift. For a document whose root body is English, the zh mirror is a translation and a byte diff proves nothing — that case stays with `M-05` and a human.

The boundary matters, because applying byte comparison to translated pairs would generate 42 false positives on this tree, which is exactly how a real signal gets buried.

失效模式值得单独写明，因为最显然的检测手段是错的那个。

陈旧镜像与正确镜像可以带同样多的日期注记、同样的 front matter、同样的标题、同样的长度。差别只在某一段里。任何"计数"式检查——注记数、汉字数、标题数、行数——看的都是正文的一个投影，而迄今为止发现的三个案例里，这个投影全都一致。

真正有效的，是在定义清楚的那一类文档上：**直接比正文**。根正文为中文的文档，其 `docs/zh-CN` 镜像不是译文，本应逐字节相同，出现差异就是漂移。根正文为英文的文档，zh 镜像是译文，字节差异不说明任何问题——那一类仍归 `M-05` 与人工审查。

这个边界很重要：若把字节比对套到译文对上，本树会产出 42 个假阳性，而那正是真信号被埋掉的方式。

## GAP-01 detail / 详情

Six references across the `05-memory-runtime` specifications cite this contract as the authoritative source for the F consumer matrix, retrieval-stage suppression matrix, cache/Working Set invalidation, index rebuild, and ten conformance specifications.

`05-memory-runtime` 各规范中共有六处引用将该契约视为 F Consumer Matrix、Retrieval-stage Suppression Matrix、Cache/Working Set Invalidation、Index Rebuild 及十项 Conformance Specification 的权威来源。

The file does not exist in the working tree or in the git history reachable from `main`. Because the referenced normative content is unavailable, the references are **not** satisfiable by rewriting them to a different file, and the content MUST NOT be invented.

该文件在工作树与 `main` 可达历史中均不存在。由于被引用的规范内容不可得，**不能**通过改指其他文件来满足这些引用，其内容也禁止臆造。

Required resolution / 需要的处置：

1. The owning party for `05-memory-runtime` supplies the actual contract, or
2. the six referencing passages are amended to state that the contract is not yet published.

1. 由 `05-memory-runtime` 责任方提供该契约原文；或
2. 将六处引用改写为「该契约尚未发布」。

Until then, any consumer reading `05-memory-runtime` MUST treat the forget-suppression and typed-cursor semantics as **not specified in a published normative document**.

在此之前，任何阅读 `05-memory-runtime` 的消费者 MUST 将 forget-suppression 与 typed-cursor 语义视为**尚无已发布的规范文档定义**。
