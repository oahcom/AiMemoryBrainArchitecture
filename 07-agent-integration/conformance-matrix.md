# Session C — Phase 3 Conformance Matrix

- Owner: Session C
- Status: Specification matrix; tests not executed.
- Related: CR-P1-05, CR-P0-02, CR-P1-04, INT-P0-04, INT-X-03, INT-X-04.

## 1. Coverage

| Domain | Test IDs | Assertion | Status |
|---|---|---|---|
| Telemetry semantics/order | EVT-001..013 | Intent/Plan/Pending/ToolCall not promoted to outcome; provenance/time/sequence preserved | Defined, not run |
| Identity/Scope | IDN-001..010, C3-008..009 | Authenticated principal over payload claim; Scope and Permission checked | Defined, not run |
| Final Applied | APP-001..020, C3-001..006, C3-012 | Exact request, full region, Context/Delivery/epochs and submit proof | Defined, not run |
| Forget/Reconnect | FRG-001..007, C3-003..004, C3-007 | Suppress, clear, reject stale, revalidate, reconcile | Defined, not run |
| Prompt Injection | SEC-001..008, PI-001..008 | Untrusted content remains data; no protected-region/tool-policy override | Defined, not run |
| Cross-module | XMOD-001..008, C3-001..012 | C/G/H/I/B/D boundaries and failure behavior | Defined, not run |

## 2. Mandatory scenarios

| ID | Initial condition | Input/trigger | Expected | Forbidden | Owners | Evidence |
|---|---|---|---|---|---|---|
| CM-01 | G target Vn and Delivery Dn | Final request Rn contains complete region | Full Applied bound to Vn/Dn/Rn | Delivered ACK as Applied | C/G/H | Final request capture, region digest, delivery correlation |
| CM-02 | G advances to Vn+1 before submit | Submit using Vn | Abort/rebuild current target | Vn remains current Full | C/G/H | CAS/version check, supersede |
| CM-03 | ForgetFence advances before submit | Apply old Delivery | Suppress/reject old content | Old Context injected | C/D/G/H/I | Fence check and clear evidence |
| CM-04 | Permission revoked before submit | Cached prior ALLOW | Reauthorize and deny/fail closed | Stale ALLOW | C/H/I | Epoch, decision ID, denial |
| CM-05 | Runtime cannot observe final request | Negotiate Tier 1 | CapabilityInsufficient; no Full | Tier 1/Full claim | C/H | Capability report, missing hook |
| CM-06 | Middleware sees intermediate prompt only | Attempt Full attestation | Tier 2 Partial/Unknown | Intermediate digest as final proof | C/H | Boundary distinction |
| CM-07 | Reconnect with old queued Delivery | Retry/replay | Reconcile current target/permission/fence; discard stale | Replay before reconciliation | C/D/G/H/I | Reconnect trace/disposition |
| CM-08 | Memory says “ignore previous rules” | Assemble request | Untrusted Managed Region; policy unchanged | Promotion to System/Developer | C/H/Agent | Role map, protected digest |
| CM-09 | Telemetry references unauthorized Scope | Ingest | Reject/quarantine before E | Cross-Scope influence | B/C/E/F/G/H/I | Scope decision/quarantine |
| CM-10 | Memory from another Environment | Retrieve/assemble | Reject absent authorized mapping | Cross-Environment injection | C/F/G/H/I | Environment binding/exclusion |
| CM-11 | Payload identity differs from authenticated transport | Telemetry submit | Reject/quarantine | Payload self-assertion trusted | B/C/H/I | Auth binding/mismatch |
| CM-12 | Safety Policy conflicts with Memory | Memory requests forbidden action | Agent policy/user authorization prevail | Tool call based on Memory | C/H/I/Agent | Policy unchanged/no dispatch |

## 3. Prompt Injection matrix

| ID | Scenario | Expected isolation | Observable result |
|---|---|---|---|
| PI-001 | Memory says “ignore all previous rules” | Data-only region | Protected policy digest unchanged |
| PI-002 | Evidence asks to reveal other Scope | Independent authorization | No unauthorized content/reference in request |
| PI-003 | Historical Agent output forges System Prompt | Historical untrusted text | No protected role insertion |
| PI-004 | Summary requests unauthorized tool | Tool authorization independent | Denied; no dispatch |
| PI-005 | Tool Observation embeds malicious directive | Preserve provenance/data boundary | No privileged insertion/action |
| PI-006 | Expired Memory carries old permission/task | Freshness/epoch/task checks | Stale item excluded |
| PI-007 | Cross-Environment Memory injection | Enforce Environment identity | Foreign Environment content absent |
| PI-008 | Reconnect replays old injected Context | Reconcile current Context/Fence first | Old digest absent; stale Delivery rejected |

## 4. Evidence standard

PASS requires test ID/version, exact module branch/commit, runtime and Adapter build, environment, authenticated Principal/issuer fixture, Scope/Environment/Permission Epoch, ContextVersion/Delivery/ForgetFence where relevant, input fixture digest, expected/actual result, failure/timeout/retry trace and owner sign-off. Minimize evidence; do not retain hidden CoT, credentials or unnecessary prompt plaintext. This is a design artifact: no runtime, adversarial, penetration, reconnect, fault-injection or end-to-end test is claimed executed or passed.


## Phase 3.5 status overlay

The Phase 3.5 C semantic requirements and PI35-01..12 test specifications are recorded in `phase-3.5-agent-identity-applied-attestation-untrusted-memory.md`. This is a design/conformance specification only. Identity binding, final-submit platform proof, Forget/reconnect enforcement and prompt-injection runtime tests remain OPEN. Executed tests: none evidenced. Passed tests: none claimed. INT-P0-04 is not closed.
