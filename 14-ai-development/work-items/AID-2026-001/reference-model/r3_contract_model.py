
"""R3 contract-level reference model.

This is an abstract in-memory contract model, not a production storage
implementation or proof of transaction/WAL durability.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ContractViolation(RuntimeError):
    pass


class Lifecycle(str, Enum):
    ACTIVE = "Active"
    FORGOTTEN = "Forgotten"


class Phase(str, Enum):
    REQUESTED = "Requested"
    AUTHORIZED = "Authorized"
    SUPPRESSION_COMMITTED = "SuppressionCommitted"
    CLEANUP = "CleanupInProgress"
    COMPLETED = "Completed"
    FAILED = "Failed"


class Reconciliation(str, Enum):
    UNKNOWN = "UNKNOWN"
    PENDING = "PENDING"
    COMPLETED = "ReconciliationCompleted"


@dataclass(frozen=True)
class Authorization:
    issuer_known: bool = True
    signature_valid: bool = True
    audience_matches: bool = True
    operation_matches: bool = True
    request_hash_matches: bool = True
    purpose_matches: bool = True
    scope_matches: bool = True
    not_before: int = 0
    expires_at: int = 100
    permission_epoch: int = 7
    nonce_unused: bool = True
    delegation_current: bool = True
    nonce: str = "auth-nonce-default"

    def valid(self, now: int, epoch: int) -> bool:
        return all((
            self.issuer_known,
            self.signature_valid,
            self.audience_matches,
            self.operation_matches,
            self.request_hash_matches,
            self.purpose_matches,
            self.scope_matches,
            self.nonce_unused,
            self.delegation_current,
            bool(self.nonce),
            self.not_before <= now < self.expires_at,
            self.permission_epoch == epoch,
        ))


@dataclass(frozen=True)
class MemoryIdentity:
    memory_id: str
    identity_version: int = 1


@dataclass(frozen=True)
class LifecycleEvent:
    event_id: str
    event_type: str
    operation_id: str
    attempt_id: str


@dataclass(frozen=True)
class IdempotencyIdentity:
    operation_id: str
    attempt_id: str
    idempotency_key: str
    request_hash: str


@dataclass(frozen=True)
class AuthorizationReference:
    permission_epoch: int
    receipt_id: str
    nonce: str


@dataclass(frozen=True)
class SuppressionProof:
    proof_id: str
    commit_id: str
    suppression_complete: bool
    inventory_revision: int


@dataclass(frozen=True)
class FenceTombstone:
    fence_generation: int
    tombstone_id: str
    committed: bool


@dataclass(frozen=True)
class AtomicCommit:
    """The six semantic members of one atomic commit."""
    memory_identity: MemoryIdentity
    lifecycle_event: LifecycleEvent
    idempotency_identity: IdempotencyIdentity
    authorization_reference: AuthorizationReference
    suppression_proof: SuppressionProof
    fence_tombstone: FenceTombstone
    commit_id: str


@dataclass
class R3Model:
    memory_id: str
    lifecycle: Lifecycle = Lifecycle.ACTIVE
    phase: Phase = Phase.REQUESTED
    fence_generation: int = 0
    permission_epoch: int = 7
    inventory_revision: int = 0
    attempt_id: str | None = None
    lease_fence: int = 0
    reconciliation: Reconciliation = Reconciliation.UNKNOWN
    outbox: dict = field(default_factory=dict)
    required_targets: set = field(default_factory=set)
    target_results: dict = field(default_factory=dict)
    unknown_required_targets: set = field(default_factory=set)
    replicas: dict = field(default_factory=dict)
    backup_manifest: dict | None = None
    restore_quarantined: bool = True
    restore_reconciled: bool = False
    atomic_tuple: dict = field(default_factory=dict)
    atomic_commit: AtomicCommit | None = None
    audit: list = field(default_factory=list)
    operation_registry: dict = field(default_factory=dict)
    nonce_registry: set = field(default_factory=set)
    legal_hold: bool = False
    exception: dict | None = None
    governance_projection_complete: bool = False
    d_completion: bool = False
    commit_counter: int = 0
    cache_entries: dict = field(default_factory=dict)
    index_snapshot_fence: int = 0
    context_version: int = 0
    pending_delta: list = field(default_factory=list)
    revocation_state: str = "CURRENT"

    ATOMIC_FIELDS = (
        "memory_identity",
        "lifecycle_event",
        "idempotency_identity",
        "authorization_reference",
        "suppression_proof",
        "fence_tombstone",
    )

    def _validate_authorization(
        self,
        auth: Authorization | None,
        now: int,
        current_epoch: int,
    ) -> None:
        """Revalidate authorization at the actual commit boundary.

        Phase is deliberately not an authorization input. A caller cannot
        obtain commit authority by changing phase alone.
        """
        if auth is None:
            raise ContractViolation("authorization reference required")

        if current_epoch != self.permission_epoch:
            raise ContractViolation("caller PermissionEpoch is stale")

        if self.revocation_state == "UNKNOWN":
            raise ContractViolation("authorization currentness is UNKNOWN")

        if self.revocation_state == "REVOKED":
            raise ContractViolation("authorization revoked")

        if not auth.valid(now, self.permission_epoch):
            raise ContractViolation("invalid or expired authorization")

        if auth.nonce in self.nonce_registry:
            raise ContractViolation("authorization nonce replay")

    def revoke_authorization(self) -> int:
        """Advance PermissionEpoch and make older authorizations unusable."""
        self.permission_epoch += 1
        self.revocation_state = "REVOKED"
        self.audit.append("AUTHORIZATION_REVOKED")
        return self.permission_epoch

    def authorize_and_suppress(
        self,
        auth: Authorization,
        now: int,
        current_epoch: int,
        operation_id: str,
        attempt_id: str = "attempt-1",
        idempotency_key: str | None = None,
        request_hash: str = "default-hash",
    ) -> AtomicCommit:
        if self.phase != Phase.REQUESTED:
            raise ContractViolation("authorization must precede suppression")

        if self.legal_hold:
            raise ContractViolation("Legal Hold prevents suppression")

        # Initial validation is useful for the workflow transition.
        # commit_suppression repeats it independently at the commit boundary.
        self._validate_authorization(auth, now, current_epoch)

        self.phase = Phase.AUTHORIZED
        return self.commit_suppression(
            operation_id,
            attempt_id,
            idempotency_key,
            request_hash,
            auth=auth,
            now=now,
            current_epoch=current_epoch,
        )

    def commit_suppression(
        self,
        operation_id: str,
        attempt_id: str = "attempt-1",
        idempotency_key: str | None = None,
        request_hash: str = "default-hash",
        fail_before_commit: bool = False,
        auth: Authorization | None = None,
        now: int = 10,
        current_epoch: int | None = None,
    ) -> AtomicCommit:
        # Phase is a workflow guard only. It never substitutes for auth.
        if self.phase != Phase.AUTHORIZED:
            raise ContractViolation("authorization workflow phase required")

        if self.legal_hold:
            raise ContractViolation("Legal Hold prevents suppression")

        if not operation_id or not attempt_id:
            raise ContractViolation("operation and attempt identity required")

        if current_epoch is None:
            current_epoch = self.permission_epoch

        # CRITICAL: independently revalidate at every commit entry,
        # including idempotent retries. Do this BEFORE operation lookup.
        self._validate_authorization(auth, now, current_epoch)

        key = idempotency_key or operation_id
        existing = self.operation_registry.get(key)

        if existing:
            if existing["request_hash"] != request_hash:
                raise ContractViolation(
                    "idempotency key reused with different hash"
                )

            # A new valid authorization nonce authorizes the retry.
            # The previously consumed nonce cannot be replayed to obtain
            # an idempotent response.
            self.nonce_registry.add(auth.nonce)
            self.audit.append("IDEMPOTENT_COMMIT_REUSED")
            return existing["commit"]

        self.commit_counter += 1
        commit_id = f"commit-{self.commit_counter}"
        next_fence = self.fence_generation + 1
        next_revision = self.inventory_revision + 1

        proof = SuppressionProof(
            proof_id=f"suppression-{commit_id}",
            commit_id=commit_id,
            suppression_complete=True,
            inventory_revision=next_revision,
        )

        # Bind the real, validated Authorization Nonce.
        authorization = AuthorizationReference(
            permission_epoch=auth.permission_epoch,
            receipt_id=f"receipt-{commit_id}",
            nonce=auth.nonce,
        )

        proposed = AtomicCommit(
            memory_identity=MemoryIdentity(self.memory_id),
            lifecycle_event=LifecycleEvent(
                event_id=f"event-{commit_id}",
                event_type="SuppressionCommitted",
                operation_id=operation_id,
                attempt_id=attempt_id,
            ),
            idempotency_identity=IdempotencyIdentity(
                operation_id=operation_id,
                attempt_id=attempt_id,
                idempotency_key=key,
                request_hash=request_hash,
            ),
            authorization_reference=authorization,
            suppression_proof=proof,
            fence_tombstone=FenceTombstone(
                fence_generation=next_fence,
                tombstone_id=f"tombstone-{commit_id}",
                committed=True,
            ),
            commit_id=commit_id,
        )

        self._validate_atomic_commit(proposed)

        if fail_before_commit:
            self.audit.append("ATOMIC_TUPLE_ABORTED")
            raise ContractViolation("atomic commit aborted")

        # One in-memory publication point for all six semantic members.
        self.atomic_commit = proposed
        self.atomic_tuple = {
            name: getattr(proposed, name) for name in self.ATOMIC_FIELDS
        }
        self.fence_generation = next_fence
        self.inventory_revision = next_revision
        self.outbox[operation_id] = "SUPPRESSION_COMMITTED"
        self.operation_registry[key] = {
            "request_hash": request_hash,
            "commit": proposed,
        }

        # Consume the actual authorization nonce only after commit succeeds.
        self.nonce_registry.add(auth.nonce)
        self.phase = Phase.SUPPRESSION_COMMITTED
        self.audit.append("SUPPRESSION_COMMITTED")

        # The committed D suppression event is the sole lifecycle trigger.
        self.forgotten_transition(
            "SuppressionCommitted",
            authorization_reference=authorization,
            suppression_proof=proof,
        )
        return proposed

    def _validate_atomic_commit(self, commit: AtomicCommit) -> None:
        if set(self.ATOMIC_FIELDS) != {
            "memory_identity", "lifecycle_event", "idempotency_identity",
            "authorization_reference", "suppression_proof",
            "fence_tombstone",
        }:
            raise ContractViolation("atomic tuple schema mismatch")

        if commit.memory_identity.memory_id != self.memory_id:
            raise ContractViolation("memory identity mismatch")

        if commit.lifecycle_event.event_type != "SuppressionCommitted":
            raise ContractViolation("wrong lifecycle event")

        if (
            commit.lifecycle_event.operation_id
            != commit.idempotency_identity.operation_id
        ):
            raise ContractViolation("operation identity mismatch")

        if (
            commit.lifecycle_event.attempt_id
            != commit.idempotency_identity.attempt_id
        ):
            raise ContractViolation("attempt identity mismatch")

        if commit.suppression_proof.commit_id != commit.commit_id:
            raise ContractViolation("suppression proof commit mismatch")

        if not commit.suppression_proof.suppression_complete:
            raise ContractViolation("suppression proof incomplete")

        if not commit.fence_tombstone.committed:
            raise ContractViolation("Fence/Tombstone not committed")

        if not commit.authorization_reference.nonce:
            raise ContractViolation("authorization nonce missing")

    def forgotten_transition(
        self,
        trigger: str,
        authorization_reference: AuthorizationReference | None = None,
        suppression_proof: SuppressionProof | None = None,
    ) -> None:
        if self.lifecycle == Lifecycle.FORGOTTEN:
            raise ContractViolation("Forgotten is terminal")

        if trigger != "SuppressionCommitted":
            raise ContractViolation(
                "only SuppressionCommitted triggers Forgotten"
            )

        if authorization_reference is None or suppression_proof is None:
            raise ContractViolation(
                "I authorization and D suppression proof required"
            )

        if self.atomic_commit is None:
            raise ContractViolation("no committed atomic tuple")

        committed = self.atomic_commit

        if authorization_reference != committed.authorization_reference:
            raise ContractViolation("authorization reference mismatch")

        if suppression_proof != committed.suppression_proof:
            raise ContractViolation("suppression proof mismatch")

        if authorization_reference.receipt_id == "":
            raise ContractViolation("authorization receipt missing")

        if suppression_proof.commit_id != committed.commit_id:
            raise ContractViolation(
                "authorization/suppression commit mismatch"
            )

        if not suppression_proof.suppression_complete:
            raise ContractViolation("suppression is not complete")

        self.lifecycle = Lifecycle.FORGOTTEN

    def advance_fence(self, generation: int) -> None:
        if generation <= self.fence_generation:
            raise ContractViolation("Fence must increase monotonically")
        self.fence_generation = generation

    def read_allowed(self, observed_fence, online=True) -> bool:
        return bool(
            online
            and observed_fence is not None
            and self.lifecycle != Lifecycle.FORGOTTEN
            and observed_fence >= self.fence_generation
        )

    def producer_admission(self, observed_fence: int) -> bool:
        return self.read_allowed(observed_fence)

    def register_dependency(self, dependency: str, observed_fence: int) -> None:
        if not self.producer_admission(observed_fence):
            raise ContractViolation("producer admission fenced")
        self.audit.append(f"DEPENDENCY:{dependency}")

    def recall_cache_fill(self, key: str, value: Any, observed_fence: int) -> None:
        # A delayed fill must recheck Fence at publication.
        if not self.read_allowed(observed_fence):
            raise ContractViolation("stale cache fill rejected")
        self.cache_entries[key] = (value, observed_fence)

    def recall_return(self, key: str, observed_fence: int):
        if not self.read_allowed(observed_fence):
            raise ContractViolation("recall return fenced")
        entry = self.cache_entries.get(key)
        if entry is None or entry[1] < self.fence_generation:
            raise ContractViolation("cache entry absent or stale")
        return entry[0]

    def rebuild_index(self, snapshot_fence: int, identities: set) -> set:
        if snapshot_fence < self.fence_generation:
            raise ContractViolation(
                "stale index snapshot cannot be published"
            )
        self.index_snapshot_fence = snapshot_fence
        return (
            set(identities)
            if self.lifecycle != Lifecycle.FORGOTTEN
            else set()
        )

    def offline_snapshot(self, context_version: int) -> dict:
        return {
            "context_version": context_version,
            "fence": self.fence_generation,
        }

    def queue_offline_delta(self, delta: dict) -> None:
        self.pending_delta.append(delta)

    def reconnect(self, snapshot: dict, deltas: list[dict]) -> int:
        if snapshot["fence"] < self.fence_generation:
            raise ContractViolation("offline snapshot predates Fence")

        version = snapshot["context_version"]
        for delta in deltas:
            if delta["context_version"] <= version:
                raise ContractViolation(
                    "stale or replayed ContextVersion"
                )
            version = delta["context_version"]
            if (
                delta.get("operation") == "Forget"
                and delta.get("memory_id") == self.memory_id
            ):
                raise ContractViolation(
                    "offline Forget cannot reverse canonical Forget"
                )

        self.context_version = version
        return version

    def context_remove(self) -> None:
        self.audit.append("CONTEXT_REMOVE")
        # Context removal is not canonical Forget.

    def set_required_targets(self, targets) -> None:
        self.required_targets = set(targets)
        self.target_results = {}
        self.unknown_required_targets = set()
        self.inventory_revision += 1
        self.d_completion = False

    def mark_target(self, target: str, result: str) -> None:
        if target not in self.required_targets:
            raise ContractViolation("target absent from sealed inventory")

        self.target_results[target] = result
        if result in {
            "UNKNOWN", "UNSUPPORTED", "NOT_EVIDENCED", "FAILED"
        }:
            self.unknown_required_targets.add(target)
        else:
            self.unknown_required_targets.discard(target)

    def domain_complete(self) -> bool:
        complete = (
            bool(self.required_targets)
            and not self.unknown_required_targets
        )
        complete = complete and all(
            self.target_results.get(target) in {
                "SUCCEEDED", "ERASED", "CLEANED"
            }
            for target in self.required_targets
        )
        self.d_completion = complete
        return complete

    def completion_projection_allowed(self) -> bool:
        evidence_complete = (
            bool(self.required_targets)
            and not self.unknown_required_targets
            and all(
                self.target_results.get(target) in {
                    "SUCCEEDED", "ERASED", "CLEANED"
                }
                for target in self.required_targets
            )
        )
        return evidence_complete and self.d_completion

    def set_governance_projection(self, complete: bool) -> None:
        self.governance_projection_complete = complete

    def start_attempt(self, attempt: str) -> int:
        if not attempt or attempt == self.attempt_id:
            raise ContractViolation("fresh attempt_id required")
        self.attempt_id = attempt
        self.lease_fence += 1
        self.reconciliation = Reconciliation.PENDING
        return self.lease_fence

    def commit_stage(self, attempt: str, lease: int, stage: str) -> None:
        if attempt != self.attempt_id or lease != self.lease_fence:
            raise ContractViolation("stale attempt/lease fence")
        self.audit.append("STAGE:" + stage)

    def reconcile(self, outcome: str) -> Reconciliation:
        self.reconciliation = (
            Reconciliation.COMPLETED
            if outcome in {"APPLIED", "NOT_APPLIED"}
            else Reconciliation.UNKNOWN
        )
        return self.reconciliation

    def retry(self, attempt: str) -> int:
        if self.reconciliation != Reconciliation.COMPLETED:
            raise ContractViolation("reconcile before retry")
        return self.start_attempt(attempt)

    def replay_outbox(self, event: str) -> bool:
        if event in self.outbox:
            return False
        self.outbox[event] = "PENDING"
        return True

    def promote_replica(self, replica: str, fence: int) -> None:
        if fence < self.fence_generation:
            raise ContractViolation("stale replica cannot be promoted")
        self.replicas[replica] = fence

    def set_backup_manifest(self, manifest: dict | None) -> None:
        self.backup_manifest = manifest

    def backup_coverage(self) -> str:
        manifest = self.backup_manifest
        if (
            not manifest
            or not manifest.get("authenticated")
            or not manifest.get("copies")
        ):
            return "UNKNOWN"
        return "KNOWN"

    def begin_restore(self, restored_fence: int) -> None:
        self.restore_quarantined = True
        self.restore_reconciled = False
        if restored_fence < self.fence_generation:
            self.audit.append("STALE_RESTORE_FENCE")

    def reconcile_restore(
        self, applied_fence: int, all_later_forgets: bool
    ) -> None:
        if (
            applied_fence < self.fence_generation
            or not all_later_forgets
        ):
            raise ContractViolation("restore reconciliation incomplete")
        self.restore_reconciled = True
        self.restore_quarantined = False

    def restore_query_allowed(self) -> bool:
        return self.restore_reconciled and not self.restore_quarantined

    def revoke_race(
        self,
        ordering: str,
        auth: Authorization | None = None,
        now: int = 10,
    ) -> str:
        """Construct state transitions for the three revocation outcomes.

        These are deterministic sequential interleavings, not a proof of
        concurrent linearizability.
        """
        if auth is None:
            auth = Authorization(nonce=f"race-{ordering}")

        if ordering == "REVOCATION_WON":
            if self.phase == Phase.REQUESTED:
                self.phase = Phase.AUTHORIZED
            self.revoke_authorization()
            try:
                self.commit_suppression(
                    "race-op",
                    auth=auth,
                    now=now,
                    current_epoch=self.permission_epoch,
                )
            except ContractViolation:
                return "REVOCATION_WON"
            raise ContractViolation("revocation unexpectedly lost")

        if ordering == "COMMIT_WON":
            self.authorize_and_suppress(
                auth,
                now,
                self.permission_epoch,
                "race-op",
            )
            self.revoke_authorization()
            return "COMMIT_WON"

        if ordering == "UNKNOWN":
            if self.phase == Phase.REQUESTED:
                self.phase = Phase.AUTHORIZED
            self.revocation_state = "UNKNOWN"
            self.audit.append("AUTHORIZATION_CURRENTNESS_UNKNOWN")
            try:
                self.commit_suppression(
                    "race-op",
                    auth=auth,
                    now=now,
                    current_epoch=self.permission_epoch,
                )
            except ContractViolation:
                return "UNKNOWN"
            raise ContractViolation("UNKNOWN authorization was committed")

        raise ContractViolation("unknown race ordering")

    def set_exception(self, exception: dict) -> None:
        required = {
            "approver", "scope", "basis", "expires_at", "controls"
        }
        if not required.issubset(exception):
            raise ContractViolation("exception integrity fields missing")
        if (
            not exception["approver"]
            or not exception["scope"]
            or not exception["basis"]
        ):
            raise ContractViolation(
                "exception approval/scope/basis empty"
            )
        if not exception["controls"]:
            raise ContractViolation("exception controls missing")
        self.exception = dict(exception)

    def exception_valid(self, now: int) -> bool:
        if self.exception is None:
            return False
        return now < self.exception["expires_at"]

    def apply_expired_exception(self, now: int) -> None:
        if self.exception is not None and not self.exception_valid(now):
            self.exception = None
            self.audit.append("EXCEPTION_EXPIRED_OR_REVOKED")
