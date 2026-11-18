"""I Global Forget target-inventory/completion logical reference model."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, Optional, Tuple


class Blocked(RuntimeError):
    pass


class Conflict(RuntimeError):
    pass


@dataclass
class Target:
    target_id: str
    owner: str
    scope_refs: Tuple[str, ...]
    capability_profile: str
    required_action: str
    physical_erasure_required: bool = False
    state: str = "Pending"
    evidence_ref: Optional[str] = None
    failure_recorded: bool = False
    exception: Optional[dict] = None
    not_applicable: Optional[dict] = None


@dataclass(frozen=True)
class Evidence:
    operation_id: str
    target_id: str
    seal_id: str
    inventory_epoch: int
    owner: str
    scope_ref: str
    action: str
    capability_profile: str
    status: str
    evidence_ref: str
    integrity_valid: bool = True
    resolution_ref: Optional[str] = None


@dataclass(frozen=True)
class InventorySeal:
    seal_id: str
    inventory_epoch: int
    target_ids: Tuple[str, ...]
    digest: str
    signer: str


class GlobalForgetModel:
    COMPONENTS = (
        "ImmediateAccessSuppression", "ProducerBarrierCompletion",
        "DerivedArtifactCleanup", "RuntimeContextAdapterSuppression",
        "ExternalCopyHandling", "BackupRetentionRestore", "PhysicalErasure"
    )

    def __init__(self, operation_id: str = "forget-op-1") -> None:
        self.operation_id = operation_id
        self.inventory_epoch = 1
        self.targets: Dict[str, Target] = {}
        self.seal: Optional[InventorySeal] = None
        self.state = "Requested"
        self.suppression_established = False
        self.d_barrier_complete = False
        self.backup_restore_safe = False
        self.component_states = {name: "Pending" for name in self.COMPONENTS}
        self.component_proofs: Dict[str, dict] = {}
        self.authorized_exception_roles = {"privacy", "security", "storage", "data-owner"}

    def register_target(self, target: Target) -> None:
        if target.target_id in self.targets:
            prior = self.targets[target.target_id]
            if prior != target:
                raise Conflict("TargetId is immutable within an inventory epoch")
            return
        had_seal = self.seal is not None
        was_terminal = self.state in {"Completed", "CompletedWithPolicyException"}
        self.targets[target.target_id] = target
        self.inventory_epoch += 1
        self.seal = None
        self.state = "Reopened" if had_seal or was_terminal else "Requested"

    def seal_inventory(self, *, seal_id: str, digest: str, signer: str, gaps: Iterable[str] = ()) -> InventorySeal:
        if signer != "I-inventory-authority":
            raise Blocked("only I inventory authority may seal the target universe")
        if list(gaps):
            raise Blocked("unresolved registry gaps prohibit InventorySeal")
        if not self.targets:
            raise Blocked("empty inventory requires positive evidence of absence")
        for target in self.targets.values():
            if not target.owner or not target.scope_refs or not target.capability_profile or not target.required_action:
                raise Blocked("target identity/scope/capability/action is incomplete")
        self.seal = InventorySeal(seal_id, self.inventory_epoch,
                                  tuple(sorted(self.targets)), digest, signer)
        self.state = "InventorySealed"
        return self.seal

    def record_evidence(self, evidence: Evidence) -> str:
        if self.seal is None or self.seal.inventory_epoch != self.inventory_epoch:
            raise Blocked("current gap-free InventorySeal required")
        if evidence.operation_id != self.operation_id or evidence.seal_id != self.seal.seal_id:
            raise Blocked("evidence is not bound to this operation and seal")
        if evidence.inventory_epoch != self.inventory_epoch or evidence.target_id not in self.seal.target_ids:
            raise Blocked("stale epoch or target outside sealed inventory")
        target = self.targets[evidence.target_id]
        if (evidence.owner != target.owner or evidence.scope_ref not in target.scope_refs
                or evidence.action != target.required_action
                or evidence.capability_profile != target.capability_profile
                or not evidence.integrity_valid):
            target.state = "Unknown"
            return "UNKNOWN"
        if evidence.status == "CONFIRMED":
            if target.failure_recorded and not evidence.resolution_ref:
                target.state = "Failed"
                return "CONFLICT_REQUIRES_OWNER_RESOLUTION"
            target.state = "Confirmed"
            target.evidence_ref = evidence.evidence_ref
            target.failure_recorded = False
            return "CONFIRMED"
        if evidence.status == "FAILED":
            target.state = "Failed"
            target.failure_recorded = True
            target.evidence_ref = evidence.evidence_ref
            return "FAILED"
        target.state = "Unknown"
        target.evidence_ref = evidence.evidence_ref
        return "UNKNOWN"

    def approve_exception(self, target_id: str, *, approver_role: str, approver: str,
                          requester: str, scope_ref: str, reason: str,
                          expiry: int, now: int, signed_evidence: str) -> None:
        target = self.targets[target_id]
        if approver_role not in self.authorized_exception_roles or approver == requester:
            raise Blocked("exception requires an authorized independent approver")
        if scope_ref not in target.scope_refs or not reason or not signed_evidence or expiry <= now:
            raise Blocked("exception must be exact, scoped, justified, signed and unexpired")
        target.state = "PolicyException"
        target.exception = {"approver": approver, "role": approver_role,
                            "requester": requester, "scope": scope_ref,
                            "reason": reason, "expiry": expiry,
                            "signed_evidence": signed_evidence}

    def mark_not_applicable(self, target_id: str, *, proof_of_absence: str,
                            reviewer: str, target_owner: str) -> None:
        target = self.targets[target_id]
        if not proof_of_absence or not reviewer or reviewer == target_owner:
            raise Blocked("NotApplicable requires positive absence proof and independent review")
        target.state = "NotApplicable"
        target.not_applicable = {"proof": proof_of_absence, "reviewer": reviewer}

    def set_component(self, name: str, state: str, *, proof: Optional[str] = None,
                      reviewer: Optional[str] = None) -> None:
        if name not in self.component_states:
            raise KeyError(name)
        allowed = {"Pending", "Confirmed", "NotApplicable", "Failed", "Unknown"}
        if state == "PolicyException":
            raise Blocked("component policy exceptions require a separate governance workflow")
        if state not in allowed:
            raise ValueError(f"unsupported component state: {state}")
        if state in {"Confirmed", "NotApplicable", "Failed"} and (not proof or not reviewer):
            raise Blocked("terminal component state requires proof and verifier")
        self.component_states[name] = state
        if proof or reviewer:
            self.component_proofs[name] = {"proof": proof, "reviewer": reviewer}
        else:
            self.component_proofs.pop(name, None)

    def set_failed(self, target_id: str, evidence_ref: str) -> None:
        target = self.targets[target_id]
        target.state = "Failed"
        target.failure_recorded = True
        target.evidence_ref = evidence_ref

    def restore_backup(self, target_id: str, *, quarantined: bool,
                       current_control_ledger_replayed: bool,
                       suppression_revalidated: bool) -> None:
        if not (quarantined and current_control_ledger_replayed and suppression_revalidated):
            self.backup_restore_safe = False
            self.targets[target_id].state = "Unknown"
            self.state = "Reopened"
            raise Blocked("restored backup remains quarantined/unsafe")
        self.backup_restore_safe = True

    def expire_exceptions(self, now: int) -> None:
        for target in self.targets.values():
            if target.state == "PolicyException" and target.exception and target.exception["expiry"] <= now:
                target.state = "Unknown"
                target.exception = None
                self.state = "Reopened"

    def apply_inventory_change(self) -> None:
        self.inventory_epoch += 1
        self.seal = None
        self.state = "Reopened"

    def report_owner_evidence(self, owner: str, target_id: str) -> dict:
        return {"owner": owner, "target_id": target_id,
                "global_completion": "NOT_AUTHORIZED",
                "target_state": self.targets[target_id].state}

    def evaluate(self, *, now: int) -> str:
        if self.seal is None or self.seal.inventory_epoch != self.inventory_epoch:
            self.state = "Reopened"
            return self.state
        if not self.suppression_established or not self.d_barrier_complete or not self.backup_restore_safe:
            self.state = "CompletionEvaluated"
            return "Pending"
        for target in self.targets.values():
            if target.state == "PolicyException":
                if not target.exception or target.exception["expiry"] <= now:
                    self.state = "Reopened"
                    return self.state
            elif target.state == "NotApplicable":
                if not target.not_applicable or not target.not_applicable["proof"] or not target.not_applicable["reviewer"]:
                    return "Pending"
            elif target.state != "Confirmed":
                self.state = "CompletionEvaluated"
                return "Pending"
            if target.physical_erasure_required and target.required_action != "PHYSICAL_ERASURE":
                return "Pending"
        for name, state in self.component_states.items():
            proof = self.component_proofs.get(name, {})
            if state in {"Confirmed", "NotApplicable"}:
                if not proof.get("proof") or not proof.get("reviewer"):
                    return "Pending"
            else:
                # Component PolicyException is deliberately unsupported until a
                # separately authorized, scoped, expiring governance workflow exists.
                return "Pending"
        if any(t.state == "PolicyException" for t in self.targets.values()) or "PolicyException" in self.component_states.values():
            self.state = "CompletedWithPolicyException"
        else:
            self.state = "Completed"
        return self.state