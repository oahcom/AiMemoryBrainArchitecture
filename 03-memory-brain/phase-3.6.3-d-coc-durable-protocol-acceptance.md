# D Owner — Exact COC Durable Protocol ForgetFence-Boundary Acceptance

- Exact Storage protocol Blob: `4ac63ac79491e79ec0c9114ef73941c73d7bbf25`
- A COC architecture Blob: `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d`
- D fence/publication gate Blob: `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5`
- Decision: **ACCEPT WITH D-OWNED FENCE / LINEAGE CONDITIONS**
- Mode: delegated D-boundary review under user instruction; not independent human sign-off.

D accepts the COC protocol's D-facing ordering contract:
1. D remains sole authority for ForgetOperation, ForgetFence, target/source/ancestor lineage, ProducerRegistrationHighWater, barrier snapshot and CanonicalSuppressionComplete.
2. COC D_FENCE_REQUEST_RECORDED is an ordering/cutoff fact only. It does not advance ForgetFenceGeneration or establish fence effectiveness.
3. If COC is unavailable after D receives a request, D durably closes affected lineage admission as PENDING_COC_CUTOFF. Local sequence/time is audit metadata, not cross-owner order.
4. Recovery batch must include all D outage requests and enumerate every affected pre-batch participant. Missing request, participant, lineage, high-water or log prefix keeps D gate closed/UNKNOWN.
5. D clearance and fence effectiveness require complete lineage and authoritative participant terminal evidence. IN_DOUBT is never released by TTL, worker death, queue deletion, timeout or COC observation.
6. COC, I, Storage and D positions remain distinct; COC cannot mint D clearance.

Exceptions: D's durable ledger/API/locks and production barrier implementation remain NOT VERIFIED. The COC protocol does not prove D/Storage atomic visibility integration, physical erasure or Global Forget completion. Multi-policy-domain atomicity remains blocked. D36/JF10/COC runtime conformance remains NOT RUN.