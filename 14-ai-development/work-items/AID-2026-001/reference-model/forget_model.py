"""Non-production executable reference model for the AID-2026-001 Forget proposal.

This model intentionally represents only contract-level invariants. It is not a
runtime implementation, persistence engine, authorization service, or proof of
production behavior.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from hashlib import sha256
from typing import Dict, Iterable, Optional


class Phase(str, Enum):
    REQUESTED = "Requested"
    AUTHORIZED = "Authorized"
    SUPPRESSION_COMMITTED = "SuppressionCommitted"
    INVENTORY_SEALED = "InventorySealed"
    CLEANUP_IN_PROGRESS = "CleanupInProgress"
    DOMAIN_COMPLETION_EVALUATED = "DomainCompletionEvaluated"
    COMPLETED = "Completed"
    FAILED = "Failed"
    CANCELLED = "Cancelled"


class MemoryState(str, Enum):
    ACTIVE = "Active"
    FORGOTTEN = "Forgotten"


class Governance(str, Enum):
    PENDING = "Pending"
    COMPLIANT = "Compliant"
    COMPLIANT_WITH_EXCEPTION = "CompliantWithException"
    NON_COMPLIANT = "NonCompliant"
    DEFERRED = "Deferred"


class TargetState(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SUPPRESSED = "suppressed"
    CLEANED = "cleaned"
    ERASED = "erased"
    EXPIRED = "expired"
    QUARANTINED = "quarantined"
    ACKNOWLEDGED = "acknowledged"
    POLICY_RETAINED = "policy_retained"
    FAILED = "failed"
    UNKNOWN = "unknown"
    UNSUPPORTED = "unsupported"


class ContractError(RuntimeError):
    pass


@dataclass
class Target:
    target_id: str
    owner_domain: str
    required_action: str
    state: TargetState = TargetState.PENDING
    fence_generation: int = 0
    evidence_ref: Optional[str] = None
    evidence_kind: Optional[str] = None
    capability: str = "supported"
    exception_approved: bool = False
    exception_expires: Optional[int] = None

    def has_current_evidence(self, generation: int) -> bool:
        return (
            self.state not in {TargetState.PENDING, TargetState.IN_PROGRESS,
                               TargetState.FAILED, TargetState.UNKNOWN,
                               TargetState.UNSUPPORTED}
            and self.fence_generation == generation
            and self.capability != "unsupported"
            and bool(self.evidence_ref)
            and bool(self.evidence_kind)
        )


@dataclass
class ForgetOperation:
    operation_id: str
    memory_id: str
    principal: str
    scope: str
    purpose: str
    phase: Phase = Phase.REQUESTED
    memory_state: MemoryState = MemoryState.ACTIVE
    fence_generation: int = 0
    inventory_revision: int = 1
    governance: Governance = Governance.PENDING
    domain_targets: Dict[str, Target] = field(default_factory=dict)
    cross_system_targets: Dict[str, Target] = field(default_factory=dict)
    checkpoints: Dict[str, str] = field(default_factory=dict)
    lease_fence: int = 0
    _request_hash: str = ""

    @staticmethod
    def canonical_request_hash(memory_id: str, principal: str, scope: str,
                               purpose: str, action: str = "forget") -> str:
        raw = "|".join((memory_id, principal, scope, purpose, action))
        return sha256(raw.encode("utf-8")).hexdigest()

    def authorize(self, allowed: bool) -> None:
        if self.phase != Phase.REQUESTED:
            raise ContractError("authorization is only valid from Requested")
        if not allowed:
            self.phase = Phase.FAILED
            self.governance = Governance.NON_COMPLIANT
            return
        self.phase = Phase.AUTHORIZED

    def suppress(self) -> int:
        if self.phase != Phase.AUTHORIZED:
            raise ContractError("suppression requires Authorized")
        # Abstract atomic commit: Memory terminal state, fence and operation phase
        # are treated as one indivisible model transition.
        self.fence_generation += 1
        self.memory_state = MemoryState.FORGOTTEN
        self.phase = Phase.SUPPRESSION_COMMITTED
        return self.fence_generation

    def cancel(self) -> None:
        if self.phase in {Phase.SUPPRESSION_COMMITTED, Phase.INVENTORY_SEALED,
                          Phase.CLEANUP_IN_PROGRESS,
                          Phase.DOMAIN_COMPLETION_EVALUATED,
                          Phase.COMPLETED, Phase.FAILED}:
            raise ContractError("cancel cannot remove suppression after linearization")
        if self.phase == Phase.CANCELLED:
            return
        self.phase = Phase.CANCELLED

    def seal_inventory(self, domain_targets: Iterable[Target],
                       cross_system_targets: Iterable[Target]) -> None:
        if self.phase != Phase.SUPPRESSION_COMMITTED:
            raise ContractError("inventory sealing requires SuppressionCommitted")
        self.domain_targets = {t.target_id: t for t in domain_targets}
        self.cross_system_targets = {t.target_id: t for t in cross_system_targets}
        for target in (*self.domain_targets.values(), *self.cross_system_targets.values()):
            target.fence_generation = self.fence_generation
        self.phase = Phase.INVENTORY_SEALED

    def start_cleanup(self) -> None:
        if self.phase != Phase.INVENTORY_SEALED:
            raise ContractError("cleanup requires sealed inventory")
        self.phase = Phase.CLEANUP_IN_PROGRESS

    def record_target(self, target_id: str, state: TargetState,
                      evidence_ref: str, evidence_kind: str,
                      *, domain_target: bool = False,
                      capability: str = "supported") -> None:
        inventory = self.domain_targets if domain_target else self.cross_system_targets
        if target_id not in inventory:
            raise ContractError("target is not in the current sealed inventory")
        target = inventory[target_id]
        target.state = state
        target.fence_generation = self.fence_generation
        target.evidence_ref = evidence_ref
        target.evidence_kind = evidence_kind
        target.capability = capability

    def evaluate_domain(self) -> bool:
        if self.phase not in {Phase.CLEANUP_IN_PROGRESS,
                              Phase.DOMAIN_COMPLETION_EVALUATED}:
            raise ContractError("domain evaluation requires cleanup")
        accepted = {TargetState.CLEANED, TargetState.ERASED}
        complete = all(
            t.state in accepted and t.has_current_evidence(self.fence_generation)
            for t in self.domain_targets.values()
        )
        self.phase = Phase.DOMAIN_COMPLETION_EVALUATED
        if complete:
            self.phase = Phase.COMPLETED
        return complete

    def evaluate_governance(self, now: int = 0) -> Governance:
        accepted = {TargetState.ERASED, TargetState.EXPIRED}
        all_accepted = True
        exception_used = False
        for target in self.cross_system_targets.values():
            if not target.has_current_evidence(self.fence_generation):
                all_accepted = False
                break
            if target.state in accepted:
                continue
            if (target.state == TargetState.POLICY_RETAINED
                    and target.exception_approved
                    and target.exception_expires is not None
                    and target.exception_expires > now):
                exception_used = True
                continue
            # ACK is accepted only for a notify action; it never means erase.
            if target.state == TargetState.ACKNOWLEDGED and target.required_action == "notify":
                continue
            all_accepted = False
            break
        if not all_accepted:
            self.governance = Governance.NON_COMPLIANT
        elif exception_used:
            self.governance = Governance.COMPLIANT_WITH_EXCEPTION
        else:
            self.governance = Governance.COMPLIANT
        return self.governance

    def public_result(self) -> str:
        if self.phase != Phase.COMPLETED:
            return "Incomplete"
        if self.governance == Governance.COMPLIANT:
            return "Completed"
        if self.governance == Governance.COMPLIANT_WITH_EXCEPTION:
            return "CompletedWithPolicyException"
        return "Incomplete"

    def expand_inventory(self, target: Target, *, domain_target: bool = False) -> None:
        if self.phase not in {Phase.INVENTORY_SEALED, Phase.CLEANUP_IN_PROGRESS,
                              Phase.DOMAIN_COMPLETION_EVALUATED, Phase.COMPLETED}:
            raise ContractError("inventory expansion requires an existing inventory")
        self.inventory_revision += 1
        inventory = self.domain_targets if domain_target else self.cross_system_targets
        inventory[target.target_id] = target
        target.fence_generation = self.fence_generation
        if domain_target:
            self.phase = Phase.CLEANUP_IN_PROGRESS
        # A cross-system-only expansion invalidates I's assessment but must not
        # rewrite D's already-completed domain result.
        self.governance = Governance.PENDING

    def acquire_lease(self) -> int:
        self.lease_fence += 1
        return self.lease_fence

    def commit_checkpoint(self, checkpoint_id: str, lease_fence: int,
                          evidence_ref: str) -> None:
        if lease_fence != self.lease_fence:
            raise ContractError("stale lease fence")
        self.checkpoints[checkpoint_id] = evidence_ref

    def restore_is_queryable(self, restored_fence_generation: int) -> bool:
        # A restored copy must apply the latest fence before serving.
        return restored_fence_generation >= self.fence_generation

    def context_remove(self, context_entries: set[str], entry_id: str) -> set[str]:
        # Context Remove is intentionally not a canonical Forget operation.
        updated = set(context_entries)
        updated.discard(entry_id)
        return updated


def idempotent_request(existing: Dict[str, tuple[str, str]], key: str,
                       request_hash: str, operation_id: str) -> str:
    prior = existing.get(key)
    if prior is None:
        existing[key] = (request_hash, operation_id)
        return operation_id
    prior_hash, prior_operation_id = prior
    if prior_hash != request_hash:
        raise ContractError("IDEMPOTENCY_CONFLICT")
    return prior_operation_id
