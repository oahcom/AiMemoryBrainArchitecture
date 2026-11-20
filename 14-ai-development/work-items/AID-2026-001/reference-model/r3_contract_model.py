"""
变更清单
========

基于 R3-FSTOR-20261118-01 原稿修订。

F-STOR-01 — 三阶段原子发布协议
1. staged 阶段：候选 AtomicCommit 与所有待发布投影完成交叉校验。
2. 唯一权威发布点：self.atomic_commit = proposed。
3. published 阶段：从权威提交记录核验全部已发布投影。
4. expected_revision / expected_fence 显式绑定 proof / tombstone
   构造时的快照值；不再根据 published 状态推算 expected 值。
5. 发布点前后发生异常时，恢复完整提交快照。

F-STOR-02 — 提交锁与故障注入
1. 所有提交、授权撤销和幂等重试共享 _commit_lock。
2. 保留 COMMIT_PROJECTION_STEPS 故障注入点。
3. atomic_commit 仍是唯一权威提交记录；其余均为受锁保护的投影。
4. 本模型只模拟进程内临界区，不声称物理 Crash/WAL/Failover 保证。

F-OI-01 — Nonce 投影与恢复
1. nonce_registry 不再作为独立权威状态。
2. nonce_registry 由 atomic_commit.authorization_reference.nonce
   和已提交 retry_audit 中的 nonce 推导。
3. 原子提交发布后重建投影；异常回滚时恢复快照。
4. recover_nonce_registry() 模拟恢复后从权威记录重建投影。
5. 授权校验前重建投影，避免投影丢失导致已消费 Nonce 重放。

F-OI-02 — 幂等重试独立审计
1. existing 分支为新授权创建独立 retry_audit 记录。
2. 记录原 operation ID、原 commit ID、新授权 receipt、新 Nonce、
   PermissionEpoch、request hash 和重试结果。
3. 重试不创建新 AtomicCommit，不推进 Fence，不修改 SuppressionCommitted
   lifecycle event，也不重复写入 SUPPRESSION_COMMITTED。
4. retry_audit 纳入 Nonce 投影的重建来源。

保留项
======
- U-049 既有授权、完成条件与生命周期约束不回退。
- DFI-013：revoke_race 仍明确是确定性顺序交错，不声称并发线性化证明。
- DFI-021：本文件仍是抽象内存模型，不声称物理持久化或灾难恢复保证。
- 本文件未执行测试；测试执行状态为 NOT RUN。
"""

import hashlib
import json
from dataclasses import dataclass, field
from enum import Enum
from threading import RLock
from typing import Any, Optional, Protocol


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


# ------------------------------------------------------------------
# F-OI-04: Verifiable authorization receipt credential
# ------------------------------------------------------------------

EXPECTED_RECEIPT_ISSUER = "authority.example"
EXPECTED_RECEIPT_AUDIENCE = "forget-contract-r3"
EXPECTED_RECEIPT_PURPOSE = "SUPPRESSION_COMMIT"
REQUIRED_RECEIPT_SCOPE = frozenset({"suppression:commit"})


@dataclass(frozen=True)
class ReceiptCredential:
    """An immutable, issuer-signed authorization receipt.

    Every field participates in the binding that the verifier checks.
    A plain string is *not* a valid receipt — only a fully populated
    ReceiptCredential that passes a trusted ReceiptVerifier counts.
    """
    receipt_id: str
    issuer: str
    audience: str
    operation: str
    request_hash: str
    purpose: str
    scope: frozenset
    permission_epoch: int
    nonce: str
    not_before: int
    expires_at: int
    signature: str
    # OD-001: resource-level binding. When set, the credential is bound to
    # a specific memory_id and principal; cross-resource use must be rejected.
    resource_id: str = ""
    principal: str = ""


@dataclass(frozen=True)
class EvidenceRecord:
    """Immutable, explicitly registered evidence metadata.

    Registration makes an evidence_ref resolvable in this in-memory model.
    It does not claim that the underlying evidence is cryptographically
    authentic or durably stored.
    """

    evidence_ref: str
    target_id: str
    operation_id: str
    required_action: str
    evidence_generation: int
    evidence_kind: str
    capability: str
    state: str


@dataclass(frozen=True)
class AuditRecord:
    """In-memory structured audit metadata; not a signed audit artifact."""

    authenticated_principal: str
    tenant_id: str
    operation_id: str
    scope: tuple[str, ...]
    timestamp: int
    action: str
    result: str
    integrity_ref: str
    integrity_hash: str


def _audit_record_digest(record: AuditRecord) -> str:
    payload = {
        "authenticated_principal": record.authenticated_principal,
        "tenant_id": record.tenant_id,
        "operation_id": record.operation_id,
        "scope": list(record.scope),
        "timestamp": record.timestamp,
        "action": record.action,
        "result": record.result,
        "integrity_ref": record.integrity_ref,
    }
    canonical = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()
class ReceiptVerifier(Protocol):
    """Protocol for verifying authorization receipt authenticity.

    Production verifiers MUST check cryptographic signature validity
    and confirm the credential was issued by a trusted authority.
    """
    def verify(self, cred: ReceiptCredential, now: int) -> bool:
        ...


class TrustAllReceiptVerifier:
    """Test-only verifier that accepts any well-formed credential.

    Does NOT constitute cryptographic signature verification evidence.
    Used to isolate context-binding tests from signature verification.
    """
    def verify(self, cred: ReceiptCredential, now: int) -> bool:
        return bool(cred.receipt_id) and bool(cred.signature)


class RejectingReceiptVerifier:
    """Test-only verifier that rejects every credential."""
    def verify(self, cred: ReceiptCredential, now: int) -> bool:
        return False


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
    receipt: Optional[ReceiptCredential] = None

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
            self.receipt is not None,
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
    receipt: Optional[ReceiptCredential] = None


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


def canonical_evidence_valid(
    *,
    evidence_record: dict | EvidenceRecord | None,
    target_id: str,
    operation_id: str,
    required_action: str,
    current_generation: int,
) -> bool:
    """Return whether an evidence record satisfies the canonical contract.

    This function validates record metadata. Registry resolution is checked
    by R3Model._has_valid_evidence before this predicate is called.
    """
    if evidence_record is None:
        return False

    if isinstance(evidence_record, EvidenceRecord):
        record = {
            "evidence_ref": evidence_record.evidence_ref,
            "target_id": evidence_record.target_id,
            "operation_id": evidence_record.operation_id,
            "required_action": evidence_record.required_action,
            "evidence_generation": evidence_record.evidence_generation,
            "evidence_kind": evidence_record.evidence_kind,
            "capability": evidence_record.capability,
            "state": evidence_record.state,
        }
    elif isinstance(evidence_record, dict):
        record = evidence_record
    else:
        return False

    required_fields = {
        "evidence_ref",
        "target_id",
        "operation_id",
        "required_action",
        "evidence_generation",
        "evidence_kind",
        "capability",
        "state",
    }
    if not required_fields.issubset(record):
        return False

    evidence_ref = record.get("evidence_ref")
    if not isinstance(evidence_ref, str) or not evidence_ref.strip():
        return False

    if record.get("target_id") != target_id or not target_id:
        return False

    if record.get("operation_id") != operation_id or not operation_id:
        return False

    if record.get("required_action") != required_action or not required_action:
        return False

    generation = record.get("evidence_generation")
    if (
        isinstance(generation, bool)
        or not isinstance(generation, int)
        or generation != current_generation
    ):
        return False

    evidence_kind = record.get("evidence_kind")
    if not isinstance(evidence_kind, str) or not evidence_kind.strip():
        return False

    capability = record.get("capability")
    if capability != "supported":
        return False

    state = record.get("state")
    if state not in {"SUCCEEDED", "ERASED", "CLEANED"}:
        return False

    allowed_kinds = {
        "erase": {"erasure-proof"},
        "cleanup": {"cleanup-proof", "snapshot-proof"},
        "suppress": {"suppression-proof"},
    }
    if evidence_kind not in allowed_kinds.get(required_action, set()):
        return False

    allowed_states = {
        "erase": {"ERASED", "SUCCEEDED"},
        "cleanup": {"CLEANED", "SUCCEEDED"},
        "suppress": {"SUCCEEDED"},
    }
    if state not in allowed_states.get(required_action, set()):
        return False

    return True


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
    target_evidence: dict = field(default_factory=dict)
    unknown_required_targets: set = field(default_factory=set)
    replicas: dict = field(default_factory=dict)
    backup_manifest: dict | None = None
    restore_quarantined: bool = True
    restore_reconciled: bool = False
    atomic_tuple: dict = field(default_factory=dict)
    atomic_commit: AtomicCommit | None = None
    audit: list = field(default_factory=list)
    operation_registry: dict = field(default_factory=dict)

    # Derived projection only. Authority is atomic_commit + retry_audit.
    nonce_registry: set = field(default_factory=set)

    # Each entry is a committed, independent idempotent-retry audit record.
    retry_audit: list = field(default_factory=list)

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
    # Structured metadata is additive; legacy string audit remains unchanged.
    structured_audit: list[AuditRecord] = field(default_factory=list)
    receipt_verifier: Any = field(
        default_factory=RejectingReceiptVerifier,
    )

    # Trusted context. Empty defaults deliberately deny authorization.
    authenticated_principal: str = ""
    tenant_id: str = ""
    trusted_scope_bindings: frozenset = field(default_factory=frozenset)

    # Evidence is resolvable only after explicit registration.
    evidence_registry: dict = field(default_factory=dict)

    # Required action is sealed per target; default is deny-by-default.
    target_required_actions: dict = field(default_factory=dict)

    _commit_lock: Any = field(
        default_factory=RLock,
        init=False,
        repr=False,
        compare=False,
    )

    ATOMIC_FIELDS = (
        "memory_identity",
        "lifecycle_event",
        "idempotency_identity",
        "authorization_reference",
        "suppression_proof",
        "fence_tombstone",
    )

    COMMIT_PROJECTION_STEPS = (
        "atomic_tuple",
        "fence_generation",
        "inventory_revision",
        "outbox",
        "operation_registry",
        "nonce_registry",
        "phase",
        "lifecycle",
        "atomic_commit",
    )

    def append_structured_audit(
        self,
        *,
        operation_id: str,
        scope,
        timestamp: int,
        action: str,
        result: str,
        integrity_ref: str,
    ) -> AuditRecord:
        """Append structured metadata using the model's trusted context.

        This creates an in-memory integrity digest, not a signature or
        tamper-proof persistent audit record.
        """
        if (
            not isinstance(self.authenticated_principal, str)
            or not self.authenticated_principal.strip()
        ):
            raise ContractViolation("audit authenticated principal missing")

        if (
            not isinstance(self.tenant_id, str)
            or not self.tenant_id.strip()
        ):
            raise ContractViolation("audit tenant_id missing")

        if not isinstance(operation_id, str) or not operation_id.strip():
            raise ContractViolation("audit operation_id missing")

        if (
            isinstance(timestamp, bool)
            or not isinstance(timestamp, int)
            or timestamp < 0
        ):
            raise ContractViolation("audit timestamp must be a non-negative integer")

        if not isinstance(action, str) or not action.strip():
            raise ContractViolation("audit action missing")

        if not isinstance(result, str) or not result.strip():
            raise ContractViolation("audit result missing")

        if not isinstance(integrity_ref, str) or not integrity_ref.strip():
            raise ContractViolation("audit integrity_ref missing")

        if isinstance(scope, str):
            raise ContractViolation("audit scope must be an iterable of strings")

        try:
            normalized_scope = tuple(sorted(set(scope)))
        except (TypeError, ValueError):
            raise ContractViolation("audit scope must contain strings")

        if (
            not normalized_scope
            or any(
                not isinstance(item, str) or not item.strip()
                for item in normalized_scope
            )
        ):
            raise ContractViolation("audit scope must contain non-empty strings")

        record = AuditRecord(
            authenticated_principal=self.authenticated_principal,
            tenant_id=self.tenant_id,
            operation_id=operation_id,
            scope=normalized_scope,
            timestamp=timestamp,
            action=action,
            result=result,
            integrity_ref=integrity_ref,
            integrity_hash="",
        )
        record = AuditRecord(
            **{
                **{
                    name: getattr(record, name)
                    for name in record.__dataclass_fields__
                    if name != "integrity_hash"
                },
                "integrity_hash": _audit_record_digest(record),
            }
        )
        self.structured_audit.append(record)
        return record

    @staticmethod
    def audit_record_integrity_valid(record: AuditRecord) -> bool:
        if not isinstance(record, AuditRecord):
            return False
        return (
            bool(record.integrity_hash)
            and record.integrity_hash == _audit_record_digest(record)
        )
    def _derive_nonce_registry(self) -> set:
        """Derive consumed Nonces from committed authority records.

        The authoritative sources are:
        - atomic_commit.authorization_reference.nonce
        - committed retry_audit entries

        nonce_registry itself is deliberately not an authority source.
        """
        consumed = set()

        committed = self.atomic_commit
        if committed is not None:
            nonce = committed.authorization_reference.nonce
            if nonce:
                consumed.add(nonce)

        for entry in self.retry_audit:
            nonce = entry.get("nonce")
            if nonce:
                consumed.add(nonce)

        return consumed

    def _rebuild_nonce_registry(self) -> set:
        """Rebuild the Nonce projection from committed authority records."""
        self.nonce_registry = self._derive_nonce_registry()
        return set(self.nonce_registry)

    def _derive_receipt_registry(self) -> set:
        """Derive used authorization receipts from committed authority."""
        used = set()
        committed = self.atomic_commit
        if committed is not None:
            receipt = committed.authorization_reference.receipt_id
            if receipt:
                used.add(receipt)
        for entry in self.retry_audit:
            receipt = entry.get("authorization_receipt")
            if receipt:
                used.add(receipt)
        return used

    def recover_nonce_registry(self) -> set:
        """Simulate recovery by rebuilding Nonce projection from authority.

        This is an in-memory reconstruction contract. It does not model
        physical storage recovery, WAL replay, or crash durability.
        """
        with self._commit_lock:
            return self._rebuild_nonce_registry()

    def _validate_authorization(
        self,
        auth: Authorization | None,
        now: int,
        current_epoch: int,
        request_hash: str = "",
        operation_id: str = "",
    ) -> None:
        """Revalidate authorization and all trusted-context bindings.

        Phase is deliberately not an authorization input. Trusted context
        comes from R3Model construction, never from the receipt itself.
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

        cred = auth.receipt
        if cred is None:
            raise ContractViolation("authorization receipt missing")

        if not self.receipt_verifier.verify(cred, now):
            raise ContractViolation("authorization receipt verification failed")

        if cred.issuer != EXPECTED_RECEIPT_ISSUER:
            raise ContractViolation("receipt issuer mismatch")
        if cred.audience != EXPECTED_RECEIPT_AUDIENCE:
            raise ContractViolation("receipt audience mismatch")
        if cred.purpose != EXPECTED_RECEIPT_PURPOSE:
            raise ContractViolation("receipt purpose mismatch")
        if cred.permission_epoch != auth.permission_epoch:
            raise ContractViolation("receipt PermissionEpoch mismatch")
        if cred.nonce != auth.nonce:
            raise ContractViolation("receipt nonce mismatch")

        if not cred.operation:
            raise ContractViolation("receipt operation missing")
        if not operation_id:
            raise ContractViolation("operation_id missing")
        if cred.operation != operation_id:
            raise ContractViolation("receipt operation mismatch")
        if not cred.request_hash or cred.request_hash == "default-hash":
            raise ContractViolation(
                "receipt request hash missing or placeholder"
            )
        if not request_hash or request_hash == "default-hash":
            raise ContractViolation(
                "request hash missing or placeholder"
            )
        if cred.request_hash != request_hash:
            raise ContractViolation("receipt request_hash mismatch")

        if not (cred.not_before <= now < cred.expires_at):
            raise ContractViolation("receipt validity window expired")

        # Mandatory trusted-context bindings. Empty defaults deny access.
        if (
            not isinstance(self.authenticated_principal, str)
            or not self.authenticated_principal.strip()
        ):
            raise ContractViolation("trusted authenticated_principal missing")

        if (
            not isinstance(self.tenant_id, str)
            or not self.tenant_id.strip()
        ):
            raise ContractViolation("trusted tenant_id missing")

        if not isinstance(cred.principal, str) or not cred.principal.strip():
            raise ContractViolation("receipt principal missing")

        if cred.principal != self.authenticated_principal:
            raise ContractViolation("receipt principal mismatch")

        if not isinstance(cred.resource_id, str) or not cred.resource_id.strip():
            raise ContractViolation("receipt resource_id missing")

        if cred.resource_id != self.memory_id:
            raise ContractViolation(
                "receipt resource_id does not match target memory"
            )

        required_scope = frozenset({
            "suppression:commit",
            f"tenant:{self.tenant_id}",
            f"memory:{self.memory_id}",
            f"operation:{operation_id}",
        })

        if not required_scope.issubset(cred.scope):
            raise ContractViolation("receipt scope insufficient")

        if not required_scope.issubset(self.trusted_scope_bindings):
            raise ContractViolation("trusted scope binding insufficient")

        # Treat nonce_registry as a cache/projection, never as authority.
        # Rebuild before replay detection so projection loss cannot permit
        # reuse of a Nonce already represented by committed authority.
        self._rebuild_nonce_registry()

        if auth.nonce in self.nonce_registry:
            raise ContractViolation("authorization nonce replay")

        if cred.receipt_id in self._derive_receipt_registry():
            raise ContractViolation("authorization receipt replay")

    def revoke_authorization(self) -> int:
        """Advance PermissionEpoch and make older authorizations unusable."""
        with self._commit_lock:
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
        request_hash: str = "",
    ) -> AtomicCommit:
        with self._commit_lock:
            if self.phase != Phase.REQUESTED:
                raise ContractViolation(
                    "authorization must precede suppression"
                )

            if self.legal_hold:
                raise ContractViolation("Legal Hold prevents suppression")

            self._validate_authorization(
                auth,
                now,
                current_epoch,
                request_hash=request_hash,
                operation_id=operation_id,
            )

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

    def _commit_snapshot(self) -> dict:
        """Capture every mutable projection touched by commit publication."""
        return {
            "atomic_commit": self.atomic_commit,
            "atomic_tuple": dict(self.atomic_tuple),
            "fence_generation": self.fence_generation,
            "inventory_revision": self.inventory_revision,
            "outbox": dict(self.outbox),
            "operation_registry": dict(self.operation_registry),
            "nonce_registry": set(self.nonce_registry),
            "retry_audit": list(self.retry_audit),
            "phase": self.phase,
            "lifecycle": self.lifecycle,
            "commit_counter": self.commit_counter,
            "audit": list(self.audit),
        }

    def _restore_commit_snapshot(self, snapshot: dict) -> None:
        """Restore the complete commit projection after an aborted publish."""
        self.atomic_commit = snapshot["atomic_commit"]
        self.atomic_tuple = dict(snapshot["atomic_tuple"])
        self.fence_generation = snapshot["fence_generation"]
        self.inventory_revision = snapshot["inventory_revision"]
        self.outbox = dict(snapshot["outbox"])
        self.operation_registry = dict(snapshot["operation_registry"])
        self.nonce_registry = set(snapshot["nonce_registry"])
        self.retry_audit = list(snapshot["retry_audit"])
        self.phase = snapshot["phase"]
        self.lifecycle = snapshot["lifecycle"]
        self.commit_counter = snapshot["commit_counter"]
        self.audit = list(snapshot["audit"])

    @staticmethod
    def _inject_commit_failure(
        fail_at: str | None,
        completed_step: str,
    ) -> None:
        """Test-only fault injection after a named projection step."""
        if fail_at == completed_step:
            raise ContractViolation(
                f"injected commit publication failure: {completed_step}"
            )

    def _validate_forgotten_candidate(
        self,
        trigger: str,
        authorization_reference: AuthorizationReference | None,
        suppression_proof: SuppressionProof | None,
        committed: AtomicCommit,
    ) -> None:
        """Validate Forgotten transition against a proposed commit record."""
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

        if authorization_reference != committed.authorization_reference:
            raise ContractViolation("authorization reference mismatch")

        if suppression_proof != committed.suppression_proof:
            raise ContractViolation("suppression proof mismatch")

        if not authorization_reference.receipt_id:
            raise ContractViolation("authorization receipt missing")

        # F-OI-04 / Owner I: the reference stores receipt_id and nonce as
        # copied fields next to the full credential. Nothing above forces
        # those projections to agree with the credential they claim to
        # describe, so a record could carry a credential for one receipt
        # and advertise another. Make the relation a checked invariant.
        if authorization_reference.receipt is None:
            raise ContractViolation(
                "authorization reference is missing its receipt credential"
            )

        if (
            authorization_reference.receipt.receipt_id
            != authorization_reference.receipt_id
        ):
            raise ContractViolation(
                "authorization receipt id does not match its credential"
            )

        if authorization_reference.receipt.nonce != authorization_reference.nonce:
            raise ContractViolation(
                "authorization nonce does not match its credential"
            )

        if (
            authorization_reference.receipt.permission_epoch
            != authorization_reference.permission_epoch
        ):
            raise ContractViolation(
                "authorization PermissionEpoch does not match its credential"
            )

        if suppression_proof.commit_id != committed.commit_id:
            raise ContractViolation(
                "authorization/suppression commit mismatch"
            )

        if not suppression_proof.suppression_complete:
            raise ContractViolation("suppression is not complete")

    def _append_retry_audit(
        self,
        original: AtomicCommit,
        auth: Authorization,
        request_hash: str = "",
    ) -> dict:
        """Append an independent audit record for an idempotent retry.

        Caller holds _commit_lock and has already validated the new
        authorization and the original authoritative commit.
        """
        identity = original.idempotency_identity

        if request_hash != identity.request_hash:
            raise ContractViolation(
                "retry request hash differs from original commit"
            )

        if auth.nonce in self.nonce_registry:
            raise ContractViolation("authorization nonce replay")

        retry_number = len(self.retry_audit) + 1
        receipt_id = auth.receipt.receipt_id

        record = {
            "retry_id": f"retry-{retry_number}",
            "operation_id": identity.operation_id,
            "commit_id": original.commit_id,
            "authorization_receipt": receipt_id,
            "authorization_credential": auth.receipt,
            "issuer": auth.receipt.issuer,
            "audience": auth.receipt.audience,
            "operation": auth.receipt.operation,
            "request_hash": auth.receipt.request_hash,
            "purpose": auth.receipt.purpose,
            "scope": tuple(sorted(auth.receipt.scope)),
            "permission_epoch": auth.permission_epoch,
            "nonce": auth.nonce,
            "retry_result": "REUSED_EXISTING_COMMIT",
        }

        self.retry_audit.append(record)

        # Nonce consumption for this retry is represented by the committed
        # retry audit record; the set is rebuilt as its derived projection.
        self._rebuild_nonce_registry()
        self.audit.append("IDEMPOTENT_COMMIT_REUSED")
        return record

    def commit_suppression(
        self,
        operation_id: str,
        attempt_id: str = "attempt-1",
        idempotency_key: str | None = None,
        request_hash: str = "",
        fail_before_commit: bool = False,
        auth: Authorization | None = None,
        now: int = 10,
        current_epoch: int | None = None,
        fail_at: str | None = None,
    ) -> AtomicCommit:
        """Publish one validated commit under the in-memory commit lock.

        Three phases:
        1. staged validation of the proposed record and staged projections;
        2. one authoritative assignment to self.atomic_commit;
        3. published validation against that authoritative record.

        The atomic_commit reference is the sole authoritative publication
        record. Other commit-related fields are projections protected by
        the model's in-process commit lock.

        fail_at is an in-memory test hook. Supported values are the names in
        COMMIT_PROJECTION_STEPS. It does not model a physical crash.
        """
        with self._commit_lock:
            if self.legal_hold:
                raise ContractViolation("Legal Hold prevents suppression")

            if not operation_id or not attempt_id:
                raise ContractViolation(
                    "operation and attempt identity required"
                )

            if current_epoch is None:
                current_epoch = self.permission_epoch

            self._validate_authorization(auth, now, current_epoch,
                                         request_hash=request_hash,
                                         operation_id=operation_id)

            key = idempotency_key or operation_id
            existing = self.operation_registry.get(key)

            # F-D-NEW-01: idempotent retry path must be reachable
            # regardless of current workflow phase. The phase whitelist
            # applies only to first-commit below.
            if existing:
                if existing["request_hash"] != request_hash:
                    raise ContractViolation(
                        "idempotency key reused with different hash"
                    )

                original = existing["commit"]

                # F-D-NEW-02: a retry may only reuse a commit that was made
                # for the same operation under the same idempotency key.
                # request_hash alone is not an identity: two distinct
                # operations can hash identically, and a credential bound to
                # operation-B must never retrieve operation-A's commit.
                if original.idempotency_identity.operation_id != operation_id:
                    raise ContractViolation(
                        "idempotency key bound to a different operation"
                    )

                if (
                    original.idempotency_identity.idempotency_key
                    != key
                ):
                    raise ContractViolation(
                        "idempotency key mismatch on retry"
                    )

                if (
                    original.idempotency_identity.request_hash
                    != request_hash
                ):
                    raise ContractViolation(
                        "idempotency request hash mismatch on retry"
                    )

                # U-058 (a): the registry entry must point at the very object
                # that is authoritative, not merely at an equal one. Value
                # equality would let a swapped-but-identical commit stand in
                # for the published authority.
                if self.atomic_commit is not original:
                    raise ContractViolation(
                        "operation registry is not backed by authoritative "
                        "atomic commit"
                    )

                self._validate_atomic_commit(
                    original,
                    expected_nonce=original.authorization_reference.nonce,
                    expected_revision=original.suppression_proof.inventory_revision,
                    expected_fence=original.fence_tombstone.fence_generation,
                    published=True,
                    live_state=False,
                )

                # F-OI-02: this is an independent retry authorization audit.
                # It does not mutate the original commit, Fence, outbox,
                # lifecycle event, phase, or operation registry.
                retry_snapshot = self._commit_snapshot()
                try:
                    self._append_retry_audit(
                        original,
                        auth,
                        request_hash,
                    )
                except Exception:
                    self._restore_commit_snapshot(retry_snapshot)
                    raise

                return original

            # First-commit path: phase whitelist applies here only.
            if self.phase not in {
                Phase.AUTHORIZED,
                Phase.SUPPRESSION_COMMITTED,
            }:
                raise ContractViolation(
                    "authorization workflow phase required"
                )

            if self.phase == Phase.SUPPRESSION_COMMITTED:
                raise ContractViolation(
                    "committed phase requires an existing idempotency record"
                )

            if self.atomic_commit is not None:
                raise ContractViolation(
                    "authoritative commit already exists"
                )

            snapshot = self._commit_snapshot()

            try:
                next_counter = self.commit_counter + 1
                commit_id = f"commit-{next_counter}"
                next_fence = self.fence_generation + 1
                next_revision = self.inventory_revision + 1

                # These values are the construction snapshot. Both staged
                # and published validation compare against these exact values.
                expected_revision = next_revision
                expected_fence = next_fence

                proof = SuppressionProof(
                    proof_id=f"suppression-{commit_id}",
                    commit_id=commit_id,
                    suppression_complete=True,
                    inventory_revision=expected_revision,
                )

                authorization = AuthorizationReference(
                    permission_epoch=auth.permission_epoch,
                    receipt_id=auth.receipt.receipt_id,
                    nonce=auth.nonce,
                    receipt=auth.receipt,
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
                        fence_generation=expected_fence,
                        tombstone_id=f"tombstone-{commit_id}",
                        committed=True,
                    ),
                    commit_id=commit_id,
                )

                if fail_before_commit:
                    raise ContractViolation("atomic commit aborted")

                self._validate_forgotten_candidate(
                    "SuppressionCommitted",
                    authorization,
                    proof,
                    proposed,
                )

                # Stage all non-authoritative projections under the lock.
                self.atomic_tuple = {
                    name: getattr(proposed, name)
                    for name in self.ATOMIC_FIELDS
                }
                self._inject_commit_failure(fail_at, "atomic_tuple")

                self.fence_generation = expected_fence
                self._inject_commit_failure(fail_at, "fence_generation")

                self.inventory_revision = expected_revision
                self._inject_commit_failure(fail_at, "inventory_revision")

                self.outbox[operation_id] = "SUPPRESSION_COMMITTED"
                self._inject_commit_failure(fail_at, "outbox")

                self.operation_registry[key] = {
                    "request_hash": request_hash,
                    "commit": proposed,
                }
                self._inject_commit_failure(
                    fail_at, "operation_registry"
                )

                # Do not consume the Nonce in an independently authoritative
                # write before atomic_commit. Its consumption is derived from
                # the record published at the single authority point.
                self._inject_commit_failure(fail_at, "nonce_registry")

                self.phase = Phase.SUPPRESSION_COMMITTED
                self._inject_commit_failure(fail_at, "phase")

                self.lifecycle = Lifecycle.FORGOTTEN
                self._inject_commit_failure(fail_at, "lifecycle")

                self.commit_counter = next_counter

                # PHASE 1: staged validation. atomic_commit is still the
                # pre-publication value (None for this first commit).
                self._validate_atomic_commit(
                    proposed,
                    expected_nonce=auth.nonce,
                    expected_revision=expected_revision,
                    expected_fence=expected_fence,
                    published=False,
                )

                # PHASE 2: the single authoritative publication point.
                self.atomic_commit = proposed

                # The nonce projection is now derivable from the published
                # authority record. It is rebuilt while still holding lock.
                self._rebuild_nonce_registry()

                self._inject_commit_failure(fail_at, "atomic_commit")

                # PHASE 3: validate published authority and every projection.
                self._validate_atomic_commit(
                    proposed,
                    expected_nonce=auth.nonce,
                    expected_revision=expected_revision,
                    expected_fence=expected_fence,
                    published=True,
                )

                self.audit.append("SUPPRESSION_COMMITTED")
                return proposed

            except Exception:
                self._restore_commit_snapshot(snapshot)
                self.audit.append("ATOMIC_TUPLE_ABORTED")
                raise

    def _validate_atomic_commit(
        self,
        commit: AtomicCommit,
        expected_nonce: str | None = None,
        expected_revision: int | None = None,
        expected_fence: int | None = None,
        published: bool = False,
        live_state: bool = True,
    ) -> None:
        """Cross-validate six semantic members and their projections.

        expected_revision and expected_fence are construction-snapshot
        values supplied by the caller. They are not recomputed from current
        mutable model fields based on the published flag.
        """
        if set(self.ATOMIC_FIELDS) != {
            "memory_identity",
            "lifecycle_event",
            "idempotency_identity",
            "authorization_reference",
            "suppression_proof",
            "fence_tombstone",
        }:
            raise ContractViolation("atomic tuple schema mismatch")

        if set(self.atomic_tuple) not in (
            set(),
            set(self.ATOMIC_FIELDS),
        ):
            raise ContractViolation("atomic tuple projection schema mismatch")

        if not commit.commit_id:
            raise ContractViolation("commit identity missing")

        if commit.memory_identity.memory_id != self.memory_id:
            raise ContractViolation("memory identity mismatch")

        if commit.memory_identity.identity_version < 1:
            raise ContractViolation("memory identity version invalid")

        event = commit.lifecycle_event
        identity = commit.idempotency_identity
        authorization = commit.authorization_reference
        proof = commit.suppression_proof
        tombstone = commit.fence_tombstone

        if not event.event_id:
            raise ContractViolation("lifecycle event identity missing")

        if event.event_type != "SuppressionCommitted":
            raise ContractViolation("wrong lifecycle event")

        if not event.operation_id or not event.attempt_id:
            raise ContractViolation("lifecycle event identity incomplete")

        if not identity.operation_id or not identity.attempt_id:
            raise ContractViolation("idempotency operation identity incomplete")

        if not identity.idempotency_key or not identity.request_hash:
            raise ContractViolation("idempotency key/hash missing")

        if event.operation_id != identity.operation_id:
            raise ContractViolation("operation identity mismatch")

        if event.attempt_id != identity.attempt_id:
            raise ContractViolation("attempt identity mismatch")

        if not authorization.receipt_id or not authorization.nonce:
            raise ContractViolation("authorization reference incomplete")

        if authorization.permission_epoch != self.permission_epoch:
            raise ContractViolation(
                "AuthorizationReference PermissionEpoch mismatch"
            )

        # F-STOR-20261119-01 / F-OI-04 residual: the scalar projection
        # fields must agree with the embedded immutable credential. A
        # record whose receipt_id / nonce / epoch were copied from a
        # different credential must not validate.
        cred = authorization.receipt
        if cred is None:
            raise ContractViolation(
                "authorization reference is missing its credential"
            )
        if cred.receipt_id != authorization.receipt_id:
            raise ContractViolation(
                "authorization receipt_id does not match credential"
            )
        if cred.nonce != authorization.nonce:
            raise ContractViolation(
                "authorization nonce does not match credential"
            )
        if cred.permission_epoch != authorization.permission_epoch:
            raise ContractViolation(
                "authorization epoch does not match credential"
            )

        if (
            expected_nonce is not None
            and authorization.nonce != expected_nonce
        ):
            raise ContractViolation(
                "AuthorizationReference nonce binding mismatch"
            )

        if not proof.proof_id:
            raise ContractViolation("suppression proof identity missing")

        if proof.commit_id != commit.commit_id:
            raise ContractViolation("suppression proof commit mismatch")

        if not proof.suppression_complete:
            raise ContractViolation("suppression proof incomplete")

        if expected_revision is None:
            expected_revision = proof.inventory_revision

        if proof.inventory_revision != expected_revision:
            raise ContractViolation(
                "SuppressionProof inventory revision mismatch"
            )

        if not tombstone.tombstone_id:
            raise ContractViolation("Fence/Tombstone identity missing")

        if not tombstone.committed:
            raise ContractViolation("Fence/Tombstone not committed")

        if expected_fence is None:
            expected_fence = tombstone.fence_generation

        if tombstone.fence_generation != expected_fence:
            raise ContractViolation(
                "FenceTombstone generation mismatch"
            )

        expected_tuple = {
            name: getattr(commit, name)
            for name in self.ATOMIC_FIELDS
        }

        if published:
            # Published-state checks must only run after the authority point.
            if self.atomic_commit != commit:
                raise ContractViolation(
                    "authoritative atomic commit projection mismatch"
                )

            if self.atomic_tuple != expected_tuple:
                raise ContractViolation("atomic tuple projection mismatch")

            # Forgotten is an irreversible terminal lifecycle. The check is
            # independent of live_state so idempotent retry can never restore
            # a Forgotten record to any other lifecycle (F-OI-03).
            if self.lifecycle != Lifecycle.FORGOTTEN:
                raise ContractViolation(
                    "Forgotten lifecycle projection missing"
                )

            # live_state=False is the idempotent-retry context: retries must
            # not mutate phase/lifecycle, and U-049 tests legally reset phase
            # before retrying. Only the durable record and its derived
            # projections are checked there. The phase assertion is the sole
            # live_state-gated check because workflow phase may advance after
            # a successful commit without violating any terminal invariant.
            if live_state:
                if self.phase != Phase.SUPPRESSION_COMMITTED:
                    raise ContractViolation(
                        "suppression phase projection mismatch"
                    )

            if self.fence_generation != expected_fence:
                raise ContractViolation(
                    "published Fence projection mismatch"
                )

            if self.inventory_revision != expected_revision:
                raise ContractViolation(
                    "published inventory revision mismatch"
                )

            if self.outbox.get(identity.operation_id) != (
                "SUPPRESSION_COMMITTED"
            ):
                raise ContractViolation("outbox projection mismatch")

            registry = self.operation_registry.get(
                identity.idempotency_key
            )
            if not registry:
                raise ContractViolation("operation registry entry missing")

            if registry.get("request_hash") != identity.request_hash:
                raise ContractViolation(
                    "operation registry request hash mismatch"
                )

            if registry.get("commit") != commit:
                raise ContractViolation(
                    "operation registry commit identity mismatch"
                )

            # Validate the derived projection against its authoritative
            # sources; never treat the projection as the source of truth.
            expected_nonces = self._derive_nonce_registry()
            if self.nonce_registry != expected_nonces:
                raise ContractViolation(
                    "authorization nonce registry projection mismatch"
                )

            if authorization.nonce not in expected_nonces:
                raise ContractViolation(
                    "authorization nonce registry projection missing"
                )

        else:
            # Staged-state validation intentionally does not require
            # self.atomic_commit == commit. The authority point has not run.
            if self.atomic_commit == commit:
                raise ContractViolation(
                    "staged commit unexpectedly already authoritative"
                )

            if self.atomic_tuple != expected_tuple:
                raise ContractViolation(
                    "staged atomic tuple projection mismatch"
                )

            if self.fence_generation != expected_fence:
                raise ContractViolation(
                    "staged Fence projection mismatch"
                )

            if self.inventory_revision != expected_revision:
                raise ContractViolation(
                    "staged inventory revision mismatch"
                )

            if self.outbox.get(identity.operation_id) != (
                "SUPPRESSION_COMMITTED"
            ):
                raise ContractViolation(
                    "staged outbox projection mismatch"
                )

            registry = self.operation_registry.get(
                identity.idempotency_key
            )
            if not registry:
                raise ContractViolation(
                    "staged operation registry entry missing"
                )

            if registry.get("request_hash") != identity.request_hash:
                raise ContractViolation(
                    "staged operation registry request hash mismatch"
                )

            if registry.get("commit") != commit:
                raise ContractViolation(
                    "staged operation registry commit identity mismatch"
                )

            if self.lifecycle != Lifecycle.FORGOTTEN:
                raise ContractViolation(
                    "staged Forgotten lifecycle projection missing"
                )

            if self.phase != Phase.SUPPRESSION_COMMITTED:
                raise ContractViolation(
                    "staged suppression phase projection mismatch"
                )

    def forgotten_transition(
        self,
        trigger: str,
        authorization_reference: AuthorizationReference | None = None,
        suppression_proof: SuppressionProof | None = None,
    ) -> None:
        with self._commit_lock:
            if self.lifecycle == Lifecycle.FORGOTTEN:
                raise ContractViolation("Forgotten is terminal")

            if self.atomic_commit is None:
                raise ContractViolation("no committed atomic tuple")

            committed = self.atomic_commit
            self._validate_atomic_commit(
                committed,
                expected_nonce=committed.authorization_reference.nonce,
                expected_revision=committed.suppression_proof.inventory_revision,
                expected_fence=committed.fence_tombstone.fence_generation,
                published=True,
            )
            self._validate_forgotten_candidate(
                trigger,
                authorization_reference,
                suppression_proof,
                committed,
            )
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

    def set_required_targets(
        self,
        targets,
        required_actions: dict | None = None,
    ) -> None:
        self.required_targets = set(targets)
        self.target_results = {}
        self.target_evidence = {}
        self.unknown_required_targets = set()
        self.target_required_actions = dict(required_actions or {})
        self.evidence_registry = {}
        self.inventory_revision += 1
        self.d_completion = False

    def register_evidence(
        self,
        target: str,
        operation_id: str,
        evidence_ref: str,
        evidence_kind: str,
        evidence_generation: int,
        capability: str,
        state: str,
    ) -> bool:
        """Explicitly register evidence metadata for one target.

        mark_target does not call this method. Registration is a distinct
        operation and duplicate evidence references are rejected.
        """
        if target not in self.required_targets:
            raise ContractViolation(
                "evidence target absent from sealed inventory"
            )

        if not isinstance(operation_id, str) or not operation_id.strip():
            raise ContractViolation("evidence operation_id required")

        if not isinstance(evidence_ref, str) or not evidence_ref.strip():
            raise ContractViolation("evidence_ref required")

        if not isinstance(evidence_kind, str) or not evidence_kind.strip():
            raise ContractViolation("evidence_kind required")

        if (
            isinstance(evidence_generation, bool)
            or not isinstance(evidence_generation, int)
        ):
            raise ContractViolation("evidence_generation must be an integer")

        if capability != "supported":
            raise ContractViolation("evidence capability is not supported")

        if state not in {"SUCCEEDED", "ERASED", "CLEANED"}:
            raise ContractViolation("evidence state is not terminal success")

        required_action = self.target_required_actions.get(target)
        if not required_action:
            raise ContractViolation(
                "target required_action is not registered"
            )

        if evidence_ref in self.evidence_registry:
            raise ContractViolation("evidence_ref already registered")

        record = EvidenceRecord(
            evidence_ref=evidence_ref,
            target_id=target,
            operation_id=operation_id,
            required_action=required_action,
            evidence_generation=evidence_generation,
            evidence_kind=evidence_kind,
            capability=capability,
            state=state,
        )

        self.evidence_registry[evidence_ref] = record
        return True

    def mark_target(
        self,
        target: str,
        result: str,
        evidence_ref: str | None = None,
        evidence_kind: str | None = None,
    ) -> None:
        """Record a target result only; evidence registration is separate.

        evidence_ref/evidence_kind remain in the signature for compatibility
        with existing callers, but are intentionally ignored.
        """
        if target not in self.required_targets:
            raise ContractViolation("target absent from sealed inventory")

        self.target_results[target] = result

        # Legacy evidence arguments are intentionally not trusted or stored.
        self.target_evidence.pop(target, None)

        if result in {
            "UNKNOWN", "UNSUPPORTED", "NOT_EVIDENCED", "FAILED"
        }:
            self.unknown_required_targets.add(target)
        else:
            self.unknown_required_targets.discard(target)

    def _has_valid_evidence(self, target: str) -> bool:
        """Resolve and validate evidence against the current operation/fence."""
        required_action = self.target_required_actions.get(target)
        if not required_action:
            return False

        committed = self.atomic_commit
        if committed is None:
            return False

        operation_id = committed.idempotency_identity.operation_id
        if not operation_id:
            return False

        # Evidence references are resolved only through the explicit registry.
        # target_evidence is not an authority source.
        candidates = [
            record
            for record in self.evidence_registry.values()
            if (
                isinstance(record, EvidenceRecord)
                and record.target_id == target
            )
        ]
        if len(candidates) != 1:
            return False

        record = candidates[0]
        registered = self.evidence_registry.get(record.evidence_ref)
        if registered is not record:
            return False

        return canonical_evidence_valid(
            evidence_record=record,
            target_id=target,
            operation_id=operation_id,
            required_action=required_action,
            current_generation=self.fence_generation,
        )

    def domain_complete(self) -> bool:
        """Completion requires successful results and canonical evidence."""
        complete = (
            bool(self.required_targets)
            and not self.unknown_required_targets
        )

        complete = complete and all(
            self.target_results.get(target) in {
                "SUCCEEDED", "ERASED", "CLEANED"
            }
            and self._has_valid_evidence(target)
            for target in self.required_targets
        )

        self.d_completion = complete
        return complete

    def completion_projection_allowed(self) -> bool:
        """Do not project completion unless canonical evidence still passes."""
        evidence_complete = (
            bool(self.required_targets)
            and not self.unknown_required_targets
            and all(
                self.target_results.get(target) in {
                    "SUCCEEDED", "ERASED", "CLEANED"
                }
                and self._has_valid_evidence(target)
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
        request_hash: str = "",
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
                    request_hash=request_hash,
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
                request_hash=request_hash,
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
                    request_hash=request_hash,
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
