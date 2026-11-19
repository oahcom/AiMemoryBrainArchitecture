# Provenance record — prompts/67-t4b-proceed.md (task-level T1)

This file exists to make the T1 file anchor of `F-REQ04-T3-T1-001` (Issue #265)
verifiable in-repo. The finding measured `GET /contents/prompts/67-t4b-proceed.md`
as **404** (`7020722257`) while the report and the evidence supply
(`7021042964`) claimed that path. This record binds the archived bytes to the
dispatch chain. It is a registration artifact only; it confers no authorization
and closes no finding on its own.

## Object

- Path: `prompts/67-t4b-proceed.md` (this directory; the exact path claimed by the report)
- Size: 1,733 bytes (UTF-8, LF line endings throughout)
- SHA-256 (raw bytes = LF-normalized): `1771e50fd73b6d68cf9bddd8b9a965faa8caa7e10b8b371c278658c194787d3a`
- Role: task-level **T1** — the proceed-after-provenance-gate execution instruction for the REQ04-T4B-RECON v0.2 work package. It is not the Owner A generic role prompt and does not replace T2.

## T1→T2 association (same actual instruction set)

- **T2** (authorized task body) = Issue #265 comment `6999990335`
  (`REQ04-T4B-RECON-PROMPT v0.2`, `2026-11-19T04:46:38Z`). Coordinator snapshot
  `prompts/60-t4b-recon-265.md` (21,100 bytes, CRLF): LF-normalized SHA-256
  `9b20c66c09ecd4556aec18b65ba18a0938782ab0f5f3665eed419cf9d7baa7f3`,
  matching the GitHub readback hash recorded at `7020450679`.
- **T1** (this file) is the post-gate proceed instruction: it embeds the
  provenance comparison result (`7008455212`) and orders the T4-B substantive
  review. T2 does not contain T1; T1 does not restate T2.

## Dispatch binding (pre-execution records)

- Verbatim T2 dispatch: `dispatch_verbatim.py`, payload 21,100 bytes SHA-256
  `8d96214d…` (LF-normalized equals T2), session HOLD on provenance, coordinator
  comparison registered `7008455212` (2026-11-19T11:59:50Z), gate granted.
- T1 dispatch: session `6afee3f1-314c-83ee-bafa-944c1d428ab8` (acct1), prompt
  `prompts/67-t4b-proceed.md`, POST 200 (respLen 12,820,092 / 353s), reply
  7,524 chars sha256 `0c50747ace48c191bfe9d30e4bd46f6112e186be1e22a9f4456ff54829a865da`,
  registered `7008606573` (2026-11-19T12:06:47Z).
- What this record proves: the archived bytes are the bytes dispatched as T1.
  What it does not prove: any in-session loading of other normative files; any
  human sign-off; any platform-axis independence (same `oahcom` identity).

## Tracking

- Finding: `F-REQ04-T3-T1-001` (P1/OPEN), Issue #265 (`7020395689`);
  evidence supply `7021042964`; incremental re-check `7020722257`.
- Closure decision (including independent review of this supply) rests with the
  governance side at #265. This file only removes the 404 anchor gap.
