# Session H Phase 3.5 Reprocessing Change Log

- Owner: H / BMCP Protocol & Agent Context Adapter
- Branch: `session-h-bmcp-protocol`
- Reprocessing base HEAD: `a830628ec0f15a960277412c67c2197565ca1dc4`
- Review baseline: `main` @ `8a6414158c9c056c1638222534e1993d1bbc99d2`
- Status: **H candidate contract reprocessed; cross-owner approval OPEN; runtime conformance NOT RUN.**

## 1. Why reprocessing was required

The prior H change log incorrectly stated that the requested D/E/H/I cross-module review was absent. The review is present on `main` and was read in this pass. Its actual disposition is Conditional Pass for continued integration, not contract freeze or implementation sign-off.

The previous H package also needed tighter alignment to C's final immutable request boundary, B's typed-reference distinctions, I's exact target inventory/state model, and G's per-Context/per-delivery authority. This reprocessing supersedes earlier H Phase 3.5 candidate wording where it is weaker or ambiguous.

## 2. Source branch heads read

| Owner | Branch | HEAD | Inputs consumed |
|---|---|---|---|
| B | `session-b-domain-model-phase3` | `66adf6bdcf5ec69a146fe75afe20ce3b85af8448` | `02-domain-model/typed-reference-registry.md`; `02-domain-model/scope-and-permission-model.md` |
| C | `session-c-agent-integration-2026-11-16` | `35de58ddc93c5f1e554596cdfc430cd6c392d355` | `07-agent-integration/phase-3.5-agent-identity-applied-attestation-untrusted-memory.md` |
| D | `session-d-memory-brain-2026-11-16` | `da8e5882d0b238d765d00b2225b79eea45a483b1` | `03-memory-brain/forget-fence-and-completion-contract.md`; operation-level producer/publication gate |
| G | `session-g-memory-context` | `3d2c065be863bc1d349faaeece6f6eaa0047abae` | `06-memory-context/context-versioning.md`; `06-memory-context/context-reconciliation.md` |
| I | `session-i-security-governance-2026-11-16` | `5591ad3620ec3f5d74194bd79556dcf3e25bea07` | `09-security-governance/principal-actor-and-authorization-contract.md`; `09-security-governance/forget-retention-backup-and-erasure-policy.md` |
| H | `session-h-bmcp-protocol` | `a830628ec0f15a960277412c67c2197565ca1dc4` | Envelope/versioning, Adapter capability/attestation, Context delivery/ACK, Forget/reconnect, Adapter Forget ACK and conformance matrix |

The branch heads above were resolved from branch refs, not copied from stale historical source snapshots.

## 3. H-owned artifact updated

Updated:
- `08-bmcp-protocol/phase-3-5-identity-applied-ack-reconnect-contract.md`

The reprocessed contract now contains:
1. Envelope Identity Mapping with PrincipalRef, IssuerRef, AgentRef, AdapterRef/instance, ProducerRef/ProducerIdentity, ActorRef, ScopeRef, EnvironmentRef, RuntimeSession, PermissionEpoch, ForgetFence, ContextVersion, DeliveryId/attempt and CapabilityEpoch.
2. Explicit protected transport authentication versus untrusted payload self-assertion.
3. Applied evidence stages separated from G delivery state: Delivered, Managed Region Materialized, Final Request Submitted and Execution Started.
4. C's exact final immutable request proof tuple, including FinalRequestBoundaryId, InferenceRequestId, AppliedContentDigest/profile, protected-region integrity and anti-replay/integrity evidence.
5. Seven action-specific Forget ACK classes mapped only as candidate evidence for I Pending/Confirmed/Failed/Unknown/PolicyException; I retains target-state and global-completion authority.
6. I TargetId and sealed inventory binding; distinction between I producer-domain inventory epoch and D per-work-item registration high-water.
7. Reconnect's seven ordered stages and fail-closed stale/offline/unsupported behavior.
8. Tier 1/2/3 capability ceiling, downgrade/epoch rules, compatibility behavior, OPEN items and 20 design conformance cases.

No B/C/D/G/I semantic authority document was modified.

## 4. Cross-module alignment decisions retained

- **B:** ActorRef is typed attribution, ScopeRef is a typed ownership/applicability boundary, neither is credential or permission. PrincipalRef, AgentRef, AdapterRef and ProducerRef remain distinct types. EnvironmentRef's exact contract owner remains OPEN as C states.
- **C:** Full Applied requires exact final immutable request submitted at the actual runtime/provider handoff boundary; pre-submit hooks/intermediate buffers are insufficient. Tier 2/3 cannot claim Full.
- **D:** ForgetFence is an opaque canonical token. H does not mint/order it locally and does not claim D producer barrier implementation.
- **G:** ContextVersion is immutable and per-Context; delivery/application is per delivery and Adapter/session. Late ACK cannot roll back current target.
- **I:** H ACK is bounded evidence only. I owns TargetId, sealed inventory, per-target status, PolicyException and Global Forget Completion. Offline/unsupported never become implicit success.

## 5. Cross-review disposition

| Finding | H disposition |
|---|---|
| CR-P0-02 / INT-P0-02 identity binding | **OPEN** — H mapping is candidate; B/I approval and I currentness semantics remain required |
| CR-P1-05 H ACK → I target mapping | **H proposal delivered; I approval OPEN** — exact TargetId, inventory seal, action/coverage evidence mapped |
| CR-P1-01 / INT-P0-03 D/E/Storage atomic producer gate | **External OPEN** — not H-owned; no end-to-end Forget closure claimed |
| CR-P1-02 typed cursor coordination | **External OPEN** — H preserves typed opaque namespace separation |
| CR-P0-01 Fact/Claim | **ADR-BLOCKED** — no H schema promotion |

## 6. Verification and non-claims

- Static source-document review: performed for listed files/heads.
- GitHub branch update: performed only on H-owned Phase 3.5 candidate document and this H-owned change log.
- Runtime Adapter conformance: NOT RUN.
- Fault injection/crash/reconnect tests: NOT RUN.
- Security certification/penetration testing: NOT RUN.
- Provider/backup physical erasure: NOT evidenced.
- I global Forget completion: NOT claimed.
- Cross-module approval and BMCP schema freeze: NOT claimed.

## 7. Final H disposition

**CANDIDATE — READY FOR OWNER REVIEW, NOT READY FOR FREEZE.**

The reprocessing closes the H documentation gap for the requested mapping/evidence proposals. It does not close the cross-owner approvals or implementation gates.
