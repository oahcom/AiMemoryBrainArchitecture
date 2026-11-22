# AID-2026-045-PROMPT v1 — Close the accepted-socket test-harness cleanup gap

## User dispatch

Repository: `oahcom/AiMemoryBrainArchitecture`.
Baseline: PR #614 merged at `c9f4a7fe021f53e101b3977fc12b6f7fc50ca29b`.
Current base: `main` at `87f54bb44d9cd2872d7faf7c5c146dd85cae6fc1`.
Tracking scope: REQ-08 / REQ-09, Issues #348 and #349.
Task: deliver a bounded follow-up for the remaining `rt_01` child-process cleanup and startup-wait defect. PR #614 is already merged; do not attempt to update its closed branch.

## Authorized scope

- Modify only `crates/bmcp-server/tests/rt_scenarios.rs` and the focused AID evidence.
- Make `rt_01_readiness_only_after_bind` guarantee child-process cleanup if readiness, address parsing, connection, or any assertion fails. Use an RAII child guard or an equivalent cleanup structure that runs on every exit path.
- Add a bounded startup/readiness wait. A failed or hung child must not leave the test blocked indefinitely.
- Preserve the core assertion: readiness is emitted only after a real listener has bound and the reported address is connectable.
- Keep the accepted-socket `set_nonblocking(false)` behavior in `accept_loop` unchanged unless a failing test proves a narrowly scoped correction is required.
- Preserve `rt_12` idle-connection and `rt_13` fragmented-request coverage.
- Deliver through a new PR linked to AID-2026-045; do not modify `main` directly.

## Explicit non-goals

- Do not implement absolute slow-drip deadlines; Issue #615 owns that behavior. `set_read_timeout` remains an idle timeout.
- Do not change MCP `tools/call` response serialization; Issue #617 / AID-2026-044 owns that.
- Do not change evidence schema, authentication, tenant isolation, storage, unrelated crates, or production activation.
- Do not reopen PR #614 solely for this test-harness follow-up.

## Verification requested

Run `cargo test -p bmcp-server` on the exact final follow-up PR head. Include at least one Windows run because the original regression was Windows-specific; include Linux if an authorized Rust toolchain is available. Record exact HEAD SHA, `rustc --version`, `cargo --version`, OS/architecture, full command, raw exit code, and concise output. Also run `cargo fmt --all -- --check` and targeted Clippy where available. If Cargo or the native compiler is unavailable, report NOT RUN. The prior PR #614 test report is not verification of this new follow-up.

## Acceptance criteria

1. Child process cleanup runs on every exit path, including assertion failures; no orphan `bmcp-server` process or bound port remains.
2. Startup/readiness waiting is bounded and fails with a diagnostic rather than hanging.
3. Readiness still proves bind-before-ready using a real child process and real socket.
4. All `bmcp-server` tests pass on the exact final head on Windows; record environment and output.
5. Linux test evidence is recorded if available; otherwise explicitly NOT RUN.
6. The absolute slow-drip deadline remains separately tracked by #615.
7. The follow-up PR and AID-2026-045 record exact-head evidence and all limitations.

## Provenance

Frozen from the separate-session technical review of PR #614 and its post-merge residual finding, plus the current user instruction to continue convergence. The original PR #614 implementation prompt is not available; this v1 prompt governs only the remaining follow-up and does not fabricate the original author prompt or session ID.
