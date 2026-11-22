# AID-2026-044-PROMPT v1 — Implement MCP tools/call CallToolResult and tool-error semantics

## User dispatch

Repository: \`oahcom/AiMemoryBrainArchitecture\`.
Tracking issue: #617 (REQ-08 / BMCP MCP server).
Base: \`main\` at \`2ed5d951b34572696242762c7b35519ac4288098\` (observed 2026-11-22).
Task: make the BMCP server's \`tools/call\` response conform to MCP protocol version \`2024-11-05\`, and distinguish tool execution errors from JSON-RPC protocol/request errors.

## Authorized scope

- Modify only the \`bmcp-server\` request/response path and its focused tests, unless an additional file is required for a standards-conforming decoder fixture.
- Return a valid MCP \`CallToolResult\` for every successful \`tools/call\`, with \`content\` as a list of content blocks. Use a \`text\` block containing the current JSON payload; do not rely on later-version \`structuredContent\` unless protocol version negotiation is deliberately upgraded.
- For the \`validate\` tool, semantically invalid evidence is the expected validation outcome: return a normal tool result whose payload reports \`valid: false\`; do not mark ordinary validation failure as a tool execution error.
- For the \`digest\` tool, semantically invalid evidence is a tool execution failure: return a \`CallToolResult\` with \`isError: true\`, not a JSON-RPC \`-32602\` error.
- Preserve JSON-RPC protocol/request errors for malformed envelopes, missing required call parameters, unknown methods, and unknown tool names.
- Keep \`tools/list\`, initialization, protocol-version negotiation, and existing validator semantics unchanged.
- Add structural response tests for valid validate, invalid validate, valid digest, invalid digest, malformed call params, unknown tool name, and unknown method.
- Add a standards-conforming MCP client/decoder interoperability fixture if an available dependency or existing fixture supports it.
- Register this work item and keep the AID manifest, frozen prompt, and INDEX row consistent.

## Explicit non-goals

- Do not change the evidence schema, \`_tri_state\`, \`AppliedDeliveryChecks\`, cryptographic verification, tenant isolation, production identity, or the 21 missing message parsers.
- Do not implement the absolute slow-drip connection deadline; that is tracked separately by #615.
- Do not modify unrelated Rust crates, public APIs, storage schemas, or production activation paths.
- Do not push directly to \`main\`; deliver through a PR linked to #617.

## Verification requested

Run \`cargo test -p bmcp-server\`, relevant protocol/server tests, \`cargo fmt --all -- --check\`, and \`cargo clippy --workspace --all-targets -- -D warnings\` where the environment permits. Record exact HEAD SHA, Rust/Cargo versions, OS/architecture, full commands, raw exit codes, and concise outputs. If the Rust toolchain or native compiler is unavailable, report NOT RUN and do not claim PASS. GitHub-hosted Actions currently fail before steps due billing; the self-hosted runner has no Cargo on PATH as of run \`44991500213\`, so verify the toolchain before treating any test command as executed.

## Acceptance criteria

1. Every successful \`tools/call\` result is structurally a valid \`CallToolResult\` with \`content\` containing at least one text block.
2. \`validate\` returns \`valid: false\` as an ordinary validation result when evidence is invalid.
3. \`digest\` returns \`isError: true\` for semantically invalid evidence and does not return a JSON-RPC error object for that tool execution failure.
4. Malformed request envelopes, missing required parameters, unknown methods, and unknown tool names preserve protocol/request error behavior.
5. Tests parse the response JSON structurally; substring-only assertions are insufficient.
6. Existing \`tools/list\`, initialize, validator, and evidence semantics remain unchanged.
7. The change is registered as AID-2026-044 and linked to #617; exact-head verification and all limitations are recorded.

## Provenance

Frozen from the user instruction to continue REQ-08 convergence and the evidence-backed Owner finding recorded in #348 comment \`7075050295\` / issue #617. The current execution interface does not expose a stable platform session UUID; no synthetic ID or raw-payload hash is asserted.
