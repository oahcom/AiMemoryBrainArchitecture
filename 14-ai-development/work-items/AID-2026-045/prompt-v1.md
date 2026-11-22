# AID-2026-045-PROMPT v1 — Complete accepted-socket regression hygiene and exact-head verification

## User dispatch

Repository: `oahcom/AiMemoryBrainArchitecture`.
Tracking carrier: PR #614 (REQ-08 / REQ-09 BMCP server reliability).
Base: `main` at `792565ac60795ece14f8575774a72563c69e8b1f`.
Current PR head: `bab4e464830421b7e3b0c0273b928b8e52f55cdc`.
Task: finish the review follow-up for the accepted-socket blocking-mode fix without expanding its scope.

## Authorized scope

- In `crates/bmcp-server/tests/rt_scenarios.rs`, make `rt_01_readiness_only_after_bind` guarantee child-process cleanup even if readiness, address parsing, or connectability assertions fail. Use an RAII child guard or an equivalent cleanup structure that runs on every exit path.
- Preserve the test's core assertion: readiness is emitted only after a real listener has bound and the reported address is connectable.
- Keep the accepted-socket `set_nonblocking(false)` behavior in `accept_loop` unchanged unless a failing test proves a narrowly scoped correction is required.
- Do not weaken `rt_12` idle-connection or `rt_13` fragmented-request assertions.
- Keep the known distinction explicit: `set_read_timeout` is an idle timeout, not an absolute monotonic deadline. Absolute slow-drip handling belongs to Issue #615, not this task.
- Keep the separate MCP `tools/call` CallToolResult defect in Issue #617 out of scope.
- Update PR #614 body and this AID manifest with exact-head verification evidence.

## Explicit non-goals

- Do not implement slow-drip/absolute-deadline handling.
- Do not change MCP response serialization, evidence schema, authentication, tenant isolation, storage, or production activation.
- Do not add unrelated tests or modify other crates.
- Do not push directly to `main`; update the existing PR #614 branch.

## Verification requested

Run `cargo test -p bmcp-server` on the exact final PR head. Include at least one Windows run because the original regression is Windows-specific; include a Linux run if an authorized Rust toolchain is available. Record exact HEAD SHA, `rustc --version`, `cargo --version`, OS/architecture, full command, raw exit code, and concise output. Also run `cargo fmt --all -- --check` and targeted Clippy where available. If Cargo or the native compiler is unavailable, report NOT RUN. Do not treat the prior run on `18e14a...` as verification of the rebased head `bab4e464...`.

## Acceptance criteria

1. Child process cleanup runs even when any readiness/connectivity assertion fails; no orphan `bmcp-server` process or bound port remains.
2. The readiness test still proves bind-before-ready using a real child process and real socket.
3. All 10 `bmcp-server` tests pass on the exact final head on Windows; record environment and output.
4. Linux test evidence is recorded if available; otherwise explicitly NOT RUN.
5. The absolute slow-drip deadline remains separately tracked by #615.
6. PR #614 and AID-2026-045 record exact-head evidence and the remaining boundaries.

## Provenance

Frozen from the independent technical review on PR #614 and the current user instruction to continue convergence. The original implementation prompt is not available in this context; this v1 prompt governs only the remaining review follow-up and does not fabricate the original author prompt or session ID.
