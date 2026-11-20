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

from r3_contract_model import EvidenceRecord, canonical_evidence_valid


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

    def has_current_evidence(
        self,
        generation: int,
        operation_id: str,
        evidence_registry: Dict[str, EvidenceRecord],
    ) -> bool:
        if (
            self.state in {
                TargetState.PENDING,
                TargetState.IN_PROGRESS,
                TargetState.FAILED,
                TargetState.UNKNOWN,
                TargetState.UNSUPPORTED,
                TargetState.ACKNOWLEDGED,
                TargetState.POLICY_RETAINED,
            }
            or self.fence_generation != generation
            or self.capability != "supported"
            or not self.evidence_ref
            or not self.evidence_kind
        ):
            return False

        record = evidence_registry.get(self.evidence_ref)
        if not isinstance(record, EvidenceRecord):
            return False

        if (
            record.evidence_ref != self.evidence_ref
            or record.evidence_kind != self.evidence_kind
            or record.capability != self.capability
        ):
            return False

        return canonical_evidence_valid(
            evidence_record=record,
            target_id=self.target_id,
            operation_id=operation_id,
            required_action=self.required_action,
            current_generation=generation,
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
    evidence_registry: Dict[str, EvidenceRecord] = field(default_factory=dict)
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

    def record_target(
        self,
        target_id: str,
        state: TargetState,
        evidence_ref: str,
        evidence_kind: str,
        *,
        domain_target: bool = False,
        capability: str = "supported",
    ) -> None:
        inventory = self.domain_targets if domain_target else self.cross_system_targets
        if target_id not in inventory:
            raise ContractError("target is not in the current sealed inventory")
        if not isinstance(evidence_ref, str) or not evidence_ref.strip():
            raise ContractError("evidence_ref is required")
        if not isinstance(evidence_kind, str) or not evidence_kind.strip():
            raise ContractError("evidence_kind is required")

        target = inventory[target_id]
        target.state = state
        target.fence_generation = self.fence_generation
        target.evidence_ref = evidence_ref
        target.evidence_kind = evidence_kind
        target.capability = capability

    def evaluate_domain(self) -> bool:
        if self.phase not in {
            Phase.CLEANUP_IN_PROGRESS,
            Phase.DOMAIN_COMPLETION_EVALUATED,
        }:
            raise ContractError("domain evaluation requires cleanup")

        accepted = {TargetState.CLEANED, TargetState.ERASED}
        complete = all(
            target.state in accepted
            and target.has_current_evidence(
                self.fence_generation,
                self.operation_id,
                self.evidence_registry,
            )
            for target in self.domain_targets.values()
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
            record = (
                self.evidence_registry.get(target.evidence_ref)
                if target.evidence_ref
                else None
            )

            if target.state == TargetState.POLICY_RETAINED:
                exception_evidence_valid = (
                    isinstance(record, EvidenceRecord)
                    and record.evidence_ref == target.evidence_ref
                    and record.target_id == target.target_id
                    and record.operation_id == self.operation_id
                    and record.required_action == target.required_action
                    and record.evidence_generation == self.fence_generation
                    and record.evidence_kind == "policy-retention"
                    and record.capability == "supported"
                    and record.state == TargetState.POLICY_RETAINED.name
                    and target.fence_generation == self.fence_generation
                    and target.capability == "supported"
                )
                if (
                    exception_evidence_valid
                    and target.exception_approved
                    and target.exception_expires is not None
                    and target.exception_expires > now
                ):
                    exception_used = True
                    continue
                all_accepted = False
                break

            if target.state == TargetState.ACKNOWLEDGED:
                notify_evidence_valid = (
                    target.required_action == "notify"
                    and isinstance(record, EvidenceRecord)
                    and record.evidence_ref == target.evidence_ref
                    and record.target_id == target.target_id
                    and record.operation_id == self.operation_id
                    and record.required_action == "notify"
                    and record.evidence_generation == self.fence_generation
                    and record.evidence_kind == "notify-receipt"
                    and record.capability == "supported"
                    and record.state == TargetState.ACKNOWLEDGED.name
                    and target.fence_generation == self.fence_generation
                    and target.capability == "supported"
                )
                if notify_evidence_valid:
                    continue
                all_accepted = False
                break

            if not target.has_current_evidence(
                self.fence_generation,
                self.operation_id,
                self.evidence_registry,
            ):
                all_accepted = False
                break

            if target.state in accepted:
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


# === STEP 3 module-level additions (session-authored, L0 verbatim) ===
def register_target_evidence(
    operation: ForgetOperation,
    target_id: str,
    evidence_ref: str,
    evidence_kind: str,
    state: TargetState,
    *,
    domain_target: bool = False,
    capability: str = "supported",
) -> EvidenceRecord:
    inventory = (
        operation.domain_targets
        if domain_target
        else operation.cross_system_targets
    )
    if target_id not in inventory:
        raise ContractError("evidence target is not in the current inventory")

    target = inventory[target_id]
    if target.evidence_ref != evidence_ref:
        raise ContractError("evidence_ref does not match recorded target")
    if target.evidence_kind != evidence_kind:
        raise ContractError("evidence_kind does not match recorded target")
    if capability != target.capability:
        raise ContractError("evidence capability does not match target")
    if evidence_ref in operation.evidence_registry:
        raise ContractError("evidence_ref already registered")
    if not isinstance(state, TargetState):
        raise ContractError("state must be a forget_model.TargetState")

    # Translate the Forget enum into the canonical R3 state vocabulary.
    # This mapping is deliberately action-sensitive.
    if state == TargetState.CLEANED and target.required_action == "suppress":
        canonical_state = "SUCCEEDED"
    elif state == TargetState.CLEANED and target.required_action == "cleanup":
        canonical_state = "CLEANED"
    elif state == TargetState.ERASED and target.required_action == "erase":
        canonical_state = "ERASED"
    else:
        # ACKNOWLEDGED and POLICY_RETAINED are validated only by their
        # dedicated governance branches; other non-success states remain
        # non-canonical and cannot satisfy completion.
        canonical_state = state.name

    record = EvidenceRecord(
        evidence_ref=evidence_ref,
        target_id=target_id,
        operation_id=operation.operation_id,
        required_action=target.required_action,
        evidence_generation=operation.fence_generation,
        evidence_kind=evidence_kind,
        capability=capability,
        state=canonical_state,
    )
    operation.evidence_registry[evidence_ref] = record
    return record

