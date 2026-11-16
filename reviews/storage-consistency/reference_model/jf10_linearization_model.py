"""JF-10 executable reference state machine.

This is a deterministic protocol model, NOT a production coordinator, database
participant, or durability implementation. It intentionally has no I/O.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, FrozenSet, Optional


class ProtocolError(RuntimeError):
    pass


class Blocked(ProtocolError):
    pass


class Decision(str, Enum):
    UNKNOWN = "UNKNOWN"
    COMMIT = "COMMIT_WON"
    ABORT = "ABORT_WON"


class ParticipantState(str, Enum):
    INTENT = "INTENT"
    PREPARED = "PREPARED"
    IN_DOUBT = "IN_DOUBT"
    COMMITTED = "COMMITTED"
    ABORTED = "ABORTED"


@dataclass(frozen=True)
class AuthorizationReceipt:
    receipt_id: str
    operation_id: str
    request_digest: str
    policy_domain: str


@dataclass
class Operation:
    operation_id: str
    work_item_id: str
    request_digest: str
    manifest_digest: str
    xid: str
    policy_domain: str
    fence_generation: int
    state: ParticipantState = ParticipantState.INTENT
    decision: Decision = Decision.UNKNOWN
    receipt: Optional[AuthorizationReceipt] = None


class CoordinatorModel:
    """Models I's single-domain terminal decision contract; in-memory only."""

    def __init__(self) -> None:
        self._decisions: Dict[str, Decision] = {}
        self._bindings: Dict[str, tuple[str, str, str]] = {}
        self._receipts: Dict[str, AuthorizationReceipt] = {}

    def decide(self, operation_id: str, request_digest: str,
               policy_domains: FrozenSet[str], receipt: AuthorizationReceipt,
               decision: Decision = Decision.COMMIT) -> Decision:
        if len(policy_domains) != 1:
            raise Blocked("multi-policy-domain atomicity is not supported")
        domain = next(iter(policy_domains))
        if receipt.operation_id != operation_id or receipt.request_digest != request_digest:
            raise ProtocolError("receipt is not bound to this operation and digest")
        if receipt.policy_domain != domain:
            raise ProtocolError("receipt policy domain mismatch")
        binding = (request_digest, domain, receipt.receipt_id)
        prior = self._bindings.get(operation_id)
        if prior is not None and prior != binding:
            raise ProtocolError("stable operation identity was rebound")
        if receipt.receipt_id in self._receipts and self._receipts[receipt.receipt_id] != receipt:
            raise ProtocolError("receipt identifier collision")
        existing = self._decisions.get(operation_id)
        if existing is not None:
            if existing != decision:
                raise ProtocolError("terminal coordinator decision is immutable")
            return existing
        self._bindings[operation_id] = binding
        self._receipts[receipt.receipt_id] = receipt
        self._decisions[operation_id] = decision
        return decision

    def lookup(self, operation_id: str) -> Decision:
        return self._decisions.get(operation_id, Decision.UNKNOWN)


class DPublicationGate:
    """Serializes D forget-fence advancement against prepared publication work."""

    def __init__(self) -> None:
        self.generation = 1
        self.closed = False
        self.prepared_operations: set[str] = set()

    def admit_prepare(self, operation_id: str, captured_generation: int) -> None:
        if self.closed or captured_generation != self.generation:
            raise Blocked("D fence is closed or captured generation is stale")
        self.prepared_operations.add(operation_id)

    def terminal(self, operation_id: str) -> None:
        self.prepared_operations.discard(operation_id)

    def begin_forget(self) -> int:
        if self.prepared_operations:
            raise Blocked("participant-first ordering: resolve prepared XIDs before fence")
        self.closed = True
        self.generation += 1
        return self.generation

    def finish_forget(self) -> None:
        self.closed = False


class ProducerManifest:
    """E stable work/publication identity; attempt IDs are not publication identity."""

    def __init__(self) -> None:
        self._frozen: Dict[str, tuple[str, str]] = {}

    def freeze(self, work_item_id: str, operation_id: str, manifest_digest: str) -> None:
        value = (operation_id, manifest_digest)
        prior = self._frozen.get(work_item_id)
        if prior is not None and prior != value:
            raise ProtocolError("WorkItemId cannot be rebound to another operation/manifest")
        self._frozen[work_item_id] = value

    def assert_retry(self, work_item_id: str, operation_id: str, manifest_digest: str,
                     attempt_id: str) -> str:
        del attempt_id
        if self._frozen.get(work_item_id) != (operation_id, manifest_digest):
            raise ProtocolError("retry does not match frozen producer manifest")
        return operation_id


class StorageParticipantModel:
    """Models prepared participant and atomic visibility publication."""

    def __init__(self, gate: DPublicationGate) -> None:
        self.gate = gate
        self.operations: Dict[str, Operation] = {}
        self._xid_owner: Dict[str, str] = {}
        self.visibility_pointers: Dict[str, str] = {}
        self.publication_receipts: Dict[str, str] = {}
        self.owner_outcomes: Dict[str, str] = {}
        self.consumed_receipts: set[str] = set()
        self.outbox: set[str] = set()

    def prepare(self, operation: Operation) -> Operation:
        prior = self.operations.get(operation.operation_id)
        if prior is not None:
            identity = (prior.request_digest, prior.manifest_digest, prior.xid,
                        prior.policy_domain, prior.work_item_id)
            requested = (operation.request_digest, operation.manifest_digest, operation.xid,
                         operation.policy_domain, operation.work_item_id)
            if identity != requested:
                raise ProtocolError("PublicationOperationId cannot be rebound")
            return prior
        if operation.xid in self._xid_owner and self._xid_owner[operation.xid] != operation.operation_id:
            raise ProtocolError("prepared XID is already bound to another operation")
        self.gate.admit_prepare(operation.operation_id, operation.fence_generation)
        operation.state = ParticipantState.PREPARED
        self.operations[operation.operation_id] = operation
        self._xid_owner[operation.xid] = operation.operation_id
        return operation

    def recover(self, operation_id: str, coordinator: CoordinatorModel) -> ParticipantState:
        op = self.operations[operation_id]
        decision = coordinator.lookup(operation_id)
        if decision == Decision.UNKNOWN:
            op.state = ParticipantState.IN_DOUBT
            return op.state
        op.decision = decision
        if decision == Decision.ABORT:
            if op.state == ParticipantState.COMMITTED:
                raise ProtocolError("cannot roll back a committed publication")
            op.state = ParticipantState.ABORTED
            self.gate.terminal(operation_id)
            return op.state
        if op.receipt is None:
            raise ProtocolError("COMMIT_WON requires the exact authorization receipt")
        if op.receipt.receipt_id in self.consumed_receipts:
            if self.owner_outcomes.get(operation_id) == "COMMITTED":
                return ParticipantState.COMMITTED
            raise ProtocolError("authorization receipt was already consumed")
        # One modeled atomic local transaction. These facts become visible together.
        self.visibility_pointers[operation_id] = op.manifest_digest
        self.publication_receipts[operation_id] = op.receipt.receipt_id
        self.owner_outcomes[operation_id] = "COMMITTED"
        self.consumed_receipts.add(op.receipt.receipt_id)
        self.outbox.add(operation_id)
        op.state = ParticipantState.COMMITTED
        self.gate.terminal(operation_id)
        return op.state

    def reader_can_see(self, operation_id: str) -> bool:
        return operation_id in self.visibility_pointers


def make_operation(operation_id: str = "pub-001", work_item_id: str = "work-001",
                   request_digest: str = "req-sha256", manifest_digest: str = "manifest-sha256",
                   xid: str = "xid-001", policy_domain: str = "domain-001",
                   fence_generation: int = 1) -> Operation:
    return Operation(operation_id, work_item_id, request_digest, manifest_digest,
                     xid, policy_domain, fence_generation)
