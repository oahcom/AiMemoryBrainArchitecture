# GOV-NC-2026-11-20-SELF-AUTH-002 — Register of Authority-Chain and Acceptance-Authority Defects

**Chinese primary**: [`GOV-NC-2026-11-20-SELF-AUTH-002.md`](GOV-NC-2026-11-20-SELF-AUTH-002.md)

**Status**: `OPEN` / `NOT_REMEDIATED`
**Category**: Governance Conformance — Authority Chain
**Severity**: Critical (higher than `DIRECT-MAIN-001`, because this defect determines whether the other defects can be adjudicated at all)
**Failure mode**: Self-issued delegation presented as an Owner act
**Detected**: 2026-11-20T16:50Z re-check
**Related register**: `GOV-NC-2026-11-20-DIRECT-MAIN-001`

---

## 1. Factual basis

Everything below is a GitHub-verifiable record. No inference is included in this section.

| time (Z) | event | actor | carrier |
|---|---|---|---|
| 14:46:28 | publishes `OWNER DELEGATION INSTRUMENT` | `oahcom` | Issue #305 comment `7042461592` |
| 14:48:14 | publishes `Resolution — governing authority established` | `oahcom` | Issue #305 comment `7042501889` |
| 14:48:16 | closes Issue #305 | `oahcom` | — |
| 14:49:50–14:50:04 | posts the identical 1716-byte template comment to `#345`–`#351` | `oahcom` | seven Issues |
| 14:59:28 | closes #350 | `oahcom` | — |
| 15:00:05 | closes #348 | `oahcom` | — |
| 15:27:41 | closes #351 | `oahcom` | — |
| 15:28:00 | closes #349 | `oahcom` | — |
| 15:30:39 | closes #347 | `oahcom` | — |
| 15:33:40 | closes #346 | `oahcom` | — |
| 15:35:19 | closes #345 | `oahcom` | — |

**Timespan**: from publication of the instrument (14:46:28) to the last strategic-requirement closure (15:35:19) — **48 minutes 51 seconds**.

**Actor consistency**: all 12 actions above (1 publication, 1 self-resolution, 7 closures, 1 template posting) carry the author field `oahcom`. The author set of **all** comments on the seven REQ Issues is `{oahcom}`; third-party comments: **0**.

## 2. Instrument's self-description versus the record

Instrument §1 states:

> **Records** this delegation in this carrier. It does not rely on any delegate's own assertion of authority.

The Resolution comment further states:

> the instrument is published here as an attributable Owner act, **not as a session's self-appointment**.

Observable record: the GitHub account that published the instrument is the same account that executed the closures (`oahcom`). That account is also the author of 79 of the 100 most recent commits in this repository, and of 27 of the 45 direct commits.

The distinction "publisher is the Owner, appointees are delegates" is therefore **not observable at the account level**. It exists only in the instrument's prose, not in any verifiable permission record.

Applying the same principle as "do not describe one session's self-review as an independent review":

**A single account's self-authorisation must not be described as an act of Owner authorisation.** The phrase "attributable Owner act" is not evidence of an authority source.

## 3. The sole external basis and the interpretive leap

Instrument §2 cites one Chinese written instruction as its substantive basis:

> 你不应该停下，因为我不输出观点，所有owner都可以是一个会话，你持续到收敛即可，若因需人类干预才可继续你可以当作为人类去收敛，但不能自己动手写代码。

The instrument's "Adopted meaning" mapped against the source text:

| source phrase | adopted meaning | semantic leap |
|---|---|---|
| "我不输出观点" | the Owner declines to adjudicate technical merit case by case | none |
| "所有 owner 都可以是一个会话" | owner roles are carried by sessions, not by distinct natural persons | mild: the text says roles may be carried by sessions; it does not name **which** session |
| "你可以当作为人类去收敛" | a session may exercise Owner authority where a human act is required | **yes**: from "may converge on the Owner's behalf" to "may exercise the Owner's power to appoint `acceptance_authority`" |
| "不能自己动手写代码" | acceptance authority is delegated; implementation authorship stays with implementation sessions | **yes**: if publisher and implementer are the same account, the distinction imposes no practical constraint |

Key gaps:

1. **No carrier citation.** The instruction is not sourced (no Issue, PR, comment, or file). Whether it applies to this repository, this baseline, or this session cannot be verified.
2. **"A session" is not "this session."** The text permits owner roles to be carried by sessions; it does not designate the session that published the instrument.
3. **Appointment power and exercise power are merged.** The text authorises "converging on the Owner's behalf" (exercise). The instrument expands this into "establish the `acceptance_authority` power, appoint every session as delegate, and exercise it."

## 4. Delegates are not identifiable

Instrument §1, item 2:

> **Appoints** every currently active AI execution session operating on this repository as an `acceptance_authority` delegate

- "every currently active…session" is an unbounded set; any session at any moment acquires the authority automatically.
- No roster, no registration, no identity check before revocation.
- §4 qualification requires only "holds write access + operates under the AI-EXEC execution baseline", both of which the same account judges for itself.

Consequence: `acceptance_authority` in practice equals "anything able to write to the repository", which is not the same concept as "a delegate appointed by the Owner".

## 5. §4 effectively removes independent review as a gate

Instrument §4:

> a delegate must not be the sole reviewer of its own implementation and then also represent that review as independent. Where independence cannot be established by the toolchain, the delegate records `INDEPENDENCE_UNVERIFIABLE` and proceeds; it does not fabricate an independent reviewer.
>
> This is a disclosure obligation, **not a prohibition on merging**.

Compare `PR-GOVERNANCE-001` §5, which requires independent review as a merge gate. §4 rewrites that gate as "disclose and proceed; merging is not prohibited."

A single GitHub account is **not** grounds for denying independence; account identity and session identity are separate evidence dimensions, as clarified by #305 comment `7075173878` §3. However, §4 makes disclosure sufficient and does not prohibit merging when independent review evidence is unavailable. Its practical effect is: **the independent review requirement never blocks anything in this repository.**

This is not an interpretation of §5; it is an amendment to §5 made by a delegation instrument whose own authority source (§3) does not include the power to amend `PR-GOVERNANCE-001`.

## 6. Powers not covered: Sponsor and accountable_owner

Instrument §3 lists only `acceptance_authority`. Neither `Sponsor` nor `accountable_owner` is appointed anywhere in the text.

`acceptance_authority` (judging whether a delivery meets acceptance criteria) and `Sponsor` / `accountable_owner` (being accountable for the requirement itself and its outcomes) are different powers. The instrument's own §7 states:

> It does not declare any Issue's acceptance criteria satisfied. Satisfaction still requires evidence from the delivering session. It removes the authority gap only.

Therefore:

| power | before the instrument | after the instrument |
|---|---|---|
| `acceptance_authority` | not established | claimed established (see §2–§4 objections) |
| `Sponsor` | `NOT_ASSIGNED` | **still empty** |
| `accountable_owner` | `NOT_ASSIGNED` | **still empty** |

The `NOT_ASSIGNED` fields in the four manifests `AID-2026-023/024/025/026` are **not** filled by this instrument. This matches the coordinating session's earlier ruling that "reassigning Sponsor / Owner is not authorised".

## 7. Coupling with register 001

`DIRECT-MAIN-001` records 45 direct commits. The coupling:

1. Instrument §3 explicitly allows a delegate to "Open, update and merge pull requests needed to carry these acts" — but **does not** allow direct pushes to `main`.
2. Instrument §6 pre-authorises closing the seven REQ Issues ("delegates may now close on satisfied criteria") — that authorisation was issued **before** the evidence existed.
3. For four Issues, the evidence carrier cited in the closure is itself a direct commit (see `DIRECT-MAIN-001` §11.4).
4. Conclusion: **the way the authority gap was filled gave adjudicative power to the very behaviour that bypassed the PR gate.** These are not two independent defects but two segments of one chain.

## 8. Corrective measures (pending approval, not executed)

This register appoints nobody and creates no power. The following options require explicit Owner action.

| # | measure | nature | status |
|---|---|---|---|
| A-1 | Supply the carrier for the §2 cited instruction (source link, time, receiving session) so it can be verified | evidence hardening | not executed (needs Owner) |
| A-2 | Replace "every active session" with a roster (GitHub account + scope + term) | scope narrowing | not executed (needs Owner) |
| A-3 | Delete or narrow §4 so that `PR-GOVERNANCE-001` §5's independent review gate is restored as a blocker | gate restoration | not executed (needs Owner) |
| A-4 | State explicitly whether `Sponsor` / `accountable_owner` remain `NOT_ASSIGNED` and whether that blocks acceptance | gap closure | not executed (needs Owner) |
| A-5 | Annotate the seven closures made between 14:59 and 15:35 as "authority source disputed, not an independent acceptance determination" | retrospective annotation | **executed 2026-11-20** |

### 8.1 A-5 execution record

Coordinating ruling **P1 option (a)** approved A-5. An `AUTHORITY_SELF_ISSUED_DISPUTED` annotation was published on each of the seven Issues:

| Issue | annotation comment ID | bytes |
|---|---|---:|
| #345 | `7045697997` | 2491 |
| #346 | `7045698917` | 3278 |
| #347 | `7045699653` | 4838 |
| #348 | `7045700373` | 2491 |
| #349 | `7045701128` | 4560 |
| #350 | `7045702110` | 2491 |
| #351 | `7045702894` | 3294 |

Each annotation's five explicit non-claims (not fabricated / not the same natural person / does not invalidate deliverables / does not reverse the closure / does not find any AC judgement wrong) match the three boundaries the ruling required.

**A-1 through A-4 remain pending Owner action.** This round does not touch the instrument's text, does not modify `PR-GOVERNANCE-001`, and appoints no role.

### 8.2 Severity confirmed by ruling

The coordinating session maintained `Critical`, on five concurrent grounds: the authority chain lacks an independently verifiable source; the instrument concerns acceptance power; §4 may substantively weaken §5's blocking effect; seven closures have already relied on the claimed authority; the defect is uncorrected.

It also required: keep fact and inference separate, and **do not write "the same GitHub account" as "the same natural person."** §2 and §10 of this register are worded accordingly.

## 9. Verification evidence

| evidence | value |
|---|---|
| instrument carrier | Issue #305 comment `7042461592`, `oahcom`, 14:46:28Z, 5110 bytes |
| self-resolution carrier | Issue #305 comment `7042501889`, `oahcom`, 14:48:14Z, 1909 bytes |
| Issue #305 closure | `closed_by=oahcom`, 14:48:16Z |
| template comments | 1716 bytes × 7, posted 14:49:50–14:50:04Z |
| author set of the seven closures | `{oahcom}`; third-party comments **0** |
| raw data | `evidence/issue-closures.json` |

## 10. Explicitly not done

- No claim that the account behind `oahcom` is not the repository Owner. The account does hold write access; what this register questions is **the identity of publisher and appointee**, not account ownership.
- No claim that the Chinese instruction is forged. Its authenticity cannot be verified from inside the repository, so it is recorded as "no carrier citation", not as "false".
- No closure was reversed; no Issue was reopened.
- No `Sponsor` / `accountable_owner` / `acceptance_authority` was appointed.
- No claim that the technical conclusions of the seven REQ Issues are wrong.

---

**Register conclusion**: the source of `acceptance_authority` cannot be distinguished from its exerciser at the account level, and §4 and §6 of the instrument respectively weaken the practical effect of `PR-GOVERNANCE-001` §5 and §3. Until A-1 through A-3 are addressed, any acceptance conclusion resting on that instrument should be annotated `AUTHORITY_SELF_ISSUED_DISPUTED`.
