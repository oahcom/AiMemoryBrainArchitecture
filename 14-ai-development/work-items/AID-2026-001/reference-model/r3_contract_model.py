"""Abstract contract model for R3; not a production persistence implementation."""
from dataclasses import dataclass, field
from enum import Enum


class ContractViolation(RuntimeError): pass
class Lifecycle(str, Enum): ACTIVE="Active"; FORGOTTEN="Forgotten"
class Phase(str, Enum): REQUESTED="Requested"; AUTHORIZED="Authorized"; SUPPRESSION_COMMITTED="SuppressionCommitted"; CLEANUP="CleanupInProgress"; COMPLETED="Completed"; FAILED="Failed"
class Reconciliation(str, Enum): UNKNOWN="UNKNOWN"; PENDING="PENDING"; COMPLETED="ReconciliationCompleted"


@dataclass(frozen=True)
class Authorization:
    issuer_known: bool=True
    signature_valid: bool=True
    audience_matches: bool=True
    operation_matches: bool=True
    request_hash_matches: bool=True
    purpose_matches: bool=True
    scope_matches: bool=True
    not_before: int=0
    expires_at: int=100
    permission_epoch: int=7
    nonce_unused: bool=True
    delegation_current: bool=True
    def valid(self, now, epoch):
        return all((self.issuer_known,self.signature_valid,self.audience_matches,
                    self.operation_matches,self.request_hash_matches,self.purpose_matches,
                    self.scope_matches,self.nonce_unused,self.delegation_current,
                    self.not_before <= now < self.expires_at,self.permission_epoch == epoch))


@dataclass
class R3Model:
    memory_id: str
    lifecycle: Lifecycle=Lifecycle.ACTIVE
    phase: Phase=Phase.REQUESTED
    fence_generation: int=0
    permission_epoch: int=7
    inventory_revision: int=0
    attempt_id: str|None=None
    lease_fence: int=0
    reconciliation: Reconciliation=Reconciliation.UNKNOWN
    outbox: dict=field(default_factory=dict)
    required_targets: set=field(default_factory=set)
    target_results: dict=field(default_factory=dict)
    unknown_required_targets: set=field(default_factory=set)
    replicas: dict=field(default_factory=dict)
    backup_manifest: dict|None=None
    restore_quarantined: bool=True
    restore_reconciled: bool=False
    atomic_tuple: dict=field(default_factory=dict)
    audit: list=field(default_factory=list)
    ATOMIC_FIELDS=("memory_lifecycle","fence_generation","operation_phase","operation_id","inventory_revision","durable_outbox_intent")

    def authorize_and_suppress(self, auth, now, current_epoch, operation_id):
        if self.phase != Phase.REQUESTED: raise ContractViolation("authorization must precede suppression")
        if not auth.valid(now,current_epoch):
            self.phase=Phase.FAILED; self.audit.append("AUTHORIZATION_DENIED_FAIL_CLOSED")
            raise ContractViolation("invalid/unknown authorization; fail closed")
        self.phase=Phase.AUTHORIZED
        self.commit_suppression(operation_id)

    def commit_suppression(self, operation_id, fail_before_commit=False):
        if self.phase != Phase.AUTHORIZED: raise ContractViolation("I authorization required")
        proposed={"memory_lifecycle":Lifecycle.FORGOTTEN,"fence_generation":self.fence_generation+1,
                  "operation_phase":Phase.SUPPRESSION_COMMITTED,"operation_id":operation_id,
                  "inventory_revision":self.inventory_revision+1,
                  "durable_outbox_intent":{**self.outbox,operation_id:"SUPPRESSION_COMMITTED"}}
        if fail_before_commit:
            self.audit.append("ATOMIC_TUPLE_ABORTED")
            raise ContractViolation("atomic tuple aborted; no partial state visible")
        self.lifecycle=proposed["memory_lifecycle"]; self.fence_generation=proposed["fence_generation"]
        self.phase=proposed["operation_phase"]; self.inventory_revision=proposed["inventory_revision"]
        self.outbox=proposed["durable_outbox_intent"]; self.atomic_tuple=proposed
        self.audit.append("SUPPRESSION_COMMITTED")

    def forgotten_transition(self, trigger):
        if self.lifecycle==Lifecycle.FORGOTTEN: raise ContractViolation("Forgotten is terminal")
        if trigger!="SuppressionCommitted": raise ContractViolation("only SuppressionCommitted triggers Forgotten")
        self.lifecycle=Lifecycle.FORGOTTEN

    def advance_fence(self, generation):
        if generation<=self.fence_generation: raise ContractViolation("Fence must increase monotonically")
        self.fence_generation=generation

    def read_allowed(self, observed_fence, online=True):
        return bool(online and observed_fence is not None and self.lifecycle!=Lifecycle.FORGOTTEN and observed_fence>=self.fence_generation)

    def set_required_targets(self, targets):
        self.required_targets=set(targets); self.target_results={}; self.unknown_required_targets=set(); self.inventory_revision+=1

    def mark_target(self, target, result):
        if target not in self.required_targets: raise ContractViolation("target absent from sealed inventory")
        self.target_results[target]=result
        if result in {"UNKNOWN","UNSUPPORTED","NOT_EVIDENCED","FAILED"}: self.unknown_required_targets.add(target)
        else: self.unknown_required_targets.discard(target)

    def domain_complete(self):
        return bool(self.required_targets) and not self.unknown_required_targets and all(self.target_results.get(t) in {"SUCCEEDED","ERASED","CLEANED"} for t in self.required_targets)

    def start_attempt(self, attempt):
        if not attempt or attempt==self.attempt_id: raise ContractViolation("fresh attempt_id required")
        self.attempt_id=attempt; self.lease_fence+=1; self.reconciliation=Reconciliation.PENDING
        return self.lease_fence

    def commit_stage(self, attempt, lease, stage):
        if attempt!=self.attempt_id or lease!=self.lease_fence: raise ContractViolation("stale attempt/lease fence")
        self.audit.append("STAGE:"+stage)

    def reconcile(self, outcome):
        self.reconciliation=Reconciliation.COMPLETED if outcome in {"APPLIED","NOT_APPLIED"} else Reconciliation.UNKNOWN
        return self.reconciliation

    def retry(self, attempt):
        if self.reconciliation!=Reconciliation.COMPLETED: raise ContractViolation("reconcile before retry")
        return self.start_attempt(attempt)

    def replay_outbox(self, event):
        if event in self.outbox: return False
        self.outbox[event]="PENDING"; return True

    def promote_replica(self, replica, fence):
        if fence<self.fence_generation: raise ContractViolation("stale replica cannot be promoted")
        self.replicas[replica]=fence

    def set_backup_manifest(self, manifest): self.backup_manifest=manifest
    def backup_coverage(self):
        return "KNOWN" if self.backup_manifest and self.backup_manifest.get("authenticated") and self.backup_manifest.get("copies") else "UNKNOWN"

    def begin_restore(self, restored_fence):
        self.restore_quarantined=True; self.restore_reconciled=False
        if restored_fence<self.fence_generation: self.audit.append("STALE_RESTORE_FENCE")

    def reconcile_restore(self, applied_fence, all_later_forgets):
        if applied_fence<self.fence_generation or not all_later_forgets: raise ContractViolation("restore reconciliation incomplete")
        self.restore_reconciled=True; self.restore_quarantined=False

    def restore_query_allowed(self): return self.restore_reconciled and not self.restore_quarantined
