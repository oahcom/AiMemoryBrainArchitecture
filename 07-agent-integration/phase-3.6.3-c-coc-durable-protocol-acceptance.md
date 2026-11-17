# C Owner — Exact COC Durable Protocol Provider-Boundary Acceptance

- Exact Storage protocol Blob: `4ac63ac79491e79ec0c9114ef73941c73d7bbf25`
- A COC architecture Blob: `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d`
- C owner contract Blob: `45a48249717c8cddb07ab96197730ef93d406c22`
- Decision: **ACCEPT WITH C-OWNED PROVIDER-SIDE-EFFECT CONDITIONS**
- Mode: delegated C-boundary review under user instruction; not independent human sign-off.

C accepts the protocol only as a durable order/participant-accounting service. C's provider boundary remains authoritative:
1. A protected provider side effect requires a quorum-committed participant intent and all required I/D/Storage gates before invocation.
2. C alone records actual provider handoff as immutable CSubmitOutcome, bound to final request digest, FinalRequestBoundaryId, reservation, provider idempotency key, provider receipt and actual InferenceRequestId where supplied.
3. COC intent, reservation, I COMMIT_WON, D clearance, Storage prepared receipt or H ACK never proves provider success.
4. Provider timeout, lost response, process death or contradictory evidence remains UNKNOWN/IN_DOUBT. Retry must use the same participant, reservation and provider idempotency key; never mint a new operation.
5. COC outage, missing quorum prefix, unresolved recovery batch or owner-local cutoff prevents new protected provider side effects.
6. COC terminal proof may reference CSubmitOutcome but cannot synthesize or alter it.

Exceptions: provider-specific idempotency and same-key authoritative outcome lookup remain unverified; no production provider adapter or COC service is implemented; C-CO/JF10-COC runtime suites remain NOT RUN. Multi-I-PolicyDomain atomicity remains blocked. This is design acceptance only.