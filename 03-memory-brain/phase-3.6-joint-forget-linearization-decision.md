# Phase 3.6 — D Joint Architecture Decision: Forget Fence Linearization

- Decision authority: user-delegated DE-S Joint Architect (ChatGPT acting across D, E and Storage)
- Date: 2026-11-16
- Status: **JOINT ARCHITECTURE DECISION RECORDED / IMPLEMENTATION NOT VERIFIED**
- Branch: `session-d-memory-brain-2026-11-16`
- Scope: D-owned ForgetOperation, ForgetFence, producer registration/barrier and canonical publication semantics only.

## 1. Stable work identity and barrier accounting

1. `WorkItemId` is the stable root identity for one admitted producer obligation. It MUST survive retry, DLQ movement/replay, worker recovery, lease renewal/expiry and transport redelivery. Those events do not create a new barrier obligation.
2. Every execution attempt has a fresh `AttemptId`; every lease grant has a monotonically fenced `LeaseEpoch`. A stale lease/attempt MUST NOT stage a dependency set, publish, or terminalize the root work.
3. Every recompile has a fresh `DerivationRunId`, linked to the same root `WorkItemId` when it is another derivation of the same admitted obligation. A recompile MUST NOT silently reset the Forget barrier cutoff or escape an installed fence.
4. If recompile creates independently schedulable work, it is represented as a registered child WorkItem with an explicit parent/root lineage and its own durable registration receipt. The root barrier remains open until all registered descendants are terminal and no descendant can publish. No implicit/unregistered child work is permitted.
5. A multi-output root is terminal only when every declared output has a complete dependency disposition and every attempt/replay/child path is durably resolved; DLQ, queue deletion, timeout, lease expiry and process death are not terminal states.

## 2. Linearization decisions

The per-Canonical-Memory-authority serialization order MUST include `RegisterProducerWork`, `InstallForgetFence`, complete `RegisterDerivedDependency`, final publication visibility commit and barrier-visible terminal disposition.

- Admission first: durable registration sequence `n` commits; a later fence captures a high-water `H >= n`. The work is tracked by that barrier and cannot publish across the active fence.
- Fence first: the fence and immutable high-water snapshot commit; later ordinary admission is durably rejected or assigned only an explicitly authorized cleanup disposition. It cannot obtain an execution lease.
- Publish first: visibility commit is ordered before the fence and is part of the pre-fence state requiring reconciliation.
- Fence first: publication is denied; a staged artifact remains private.
- No third outcome is valid. Cached fence reads, queue-first admission, sequence allocation outside the serialization domain, and check-then-write publication are forbidden.

## 3. Final publication predicate

At the single authoritative visibility commit, all of the following MUST hold in the same serialization decision:
- latest applicable ForgetFence and all ancestor/source-lineage fences are current and do not suppress the artifact;
- root WorkItem registration and complete dependency-registration receipt set are durable;
- current AttemptId and LeaseEpoch are authorized and not superseded;
- lineage, source references, scope and artifact digest match the registered work;
- I-authoritative PermissionEpoch/revocation decision is current for the exact action/resource/scope;
- the visibility pointer/record changes atomically with the committed PublicationReceipt.

A D-issued token or an earlier successful check is not a publication permit. D owns the Forget predicate; E owns producer execution; Storage owns the physical commit mechanism; I remains the authority for authorization freshness.

## 4. Barrier completion and late derivatives

A barrier may be declared drained only when every captured work item and registered descendant is terminal, every possible publication path is closed, and the evidence is tied to the exact fence generation/high-water snapshot. A late derivative, newly discovered producer, changed inventory epoch or replay that can still publish invalidates/reopens the relevant completion proof. D-local barrier drainage is not Global Forget completion.

## 5. Decision boundary and verification

This document records the architecture decision under the user's explicit delegation of D/E/Storage responsibilities to one joint architect. It does not claim approval by an absent independent Owner, implementation, a deployed linearizable database, passing tests, global Forget completion or physical erasure. D36 race/fault cases remain **NOT RUN** until executable evidence is attached.
