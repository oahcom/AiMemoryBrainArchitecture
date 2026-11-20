#!/usr/bin/env python3
"""Non-normative local cross-agent exchange proof for REQ-08.

This is an isolated experiment, not BMCP, an authentication provider, a
production authorization mechanism, or a frozen portable-exchange format.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess, sys
from dataclasses import asdict, dataclass
from typing import Any

@dataclass(frozen=True)
class Grant:
    grant_id: str
    issuer_principal: str
    grantee_agent: str
    tenant_id: str
    resource_id: str
    action: str
    audience: str
    delegation_chain: tuple[str, ...]
    revoked: bool = False

@dataclass(frozen=True)
class Agent:
    agent_id: str
    provider_id: str
    model_id: str
    tenant_id: str

@dataclass(frozen=True)
class Memory:
    resource_id: str
    content: str
    source_agent: str
    source_provider: str
    source_model: str
    source_tenant: str
    source_record_id: str

def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")

def authorize(grant: Grant, recipient: Agent, memory: Memory, action: str = "share") -> None:
    checks = (
        (not grant.revoked, "GRANT_REVOKED"),
        (grant.grantee_agent == recipient.agent_id, "GRANTEE_MISMATCH"),
        (grant.tenant_id == recipient.tenant_id == memory.source_tenant, "TENANT_MISMATCH"),
        (grant.audience == recipient.agent_id, "AUDIENCE_MISMATCH"),
        (grant.resource_id == memory.resource_id, "RESOURCE_MISMATCH"),
        (grant.action == action, "ACTION_NOT_GRANTED"),
        (bool(grant.issuer_principal), "MISSING_ISSUER"),
        (bool(grant.delegation_chain) and grant.delegation_chain[-1] == grant.issuer_principal, "INVALID_DELEGATION_CHAIN"),
    )
    for passed, reason in checks:
        if not passed:
            raise PermissionError(reason)

def make_fixture():
    sender = Agent("agent.alpha", "provider-a", "model-alpha", "tenant.red")
    receiver = Agent("agent.beta", "provider-b", "model-beta", "tenant.red")
    memory = Memory("memory.demo.001",
        "The project decision is to preserve source attribution across agent handoff.",
        sender.agent_id, sender.provider_id, sender.model_id, sender.tenant_id, "record.alpha.001")
    grant = Grant("grant.fixture.001", "human.fixture.owner", receiver.agent_id,
        "tenant.red", memory.resource_id, "share", receiver.agent_id,
        ("human.fixture.owner",))
    return sender, receiver, memory, grant

def build_envelope(sender: Agent, memory: Memory, grant: Grant):
    body = asdict(memory)
    return {"experiment_only": True, "experiment_schema": "req08-local-proof/0",
        "grant": asdict(grant), "memory": body,
        "payload_sha256": hashlib.sha256(canonical_bytes(body)).hexdigest(),
        "transport_sender": sender.agent_id}

def receive(envelope, recipient: Agent):
    if envelope.get("experiment_only") is not True or envelope.get("experiment_schema") != "req08-local-proof/0":
        raise ValueError("UNSUPPORTED_EXPERIMENT_ENVELOPE")
    body = envelope.get("memory")
    if not isinstance(body, dict):
        raise ValueError("MISSING_MEMORY")
    digest = hashlib.sha256(canonical_bytes(body)).hexdigest()
    if digest != envelope.get("payload_sha256"):
        raise ValueError("PAYLOAD_DIGEST_MISMATCH")
    memory = Memory(**body)
    grant_data = dict(envelope.get("grant", {}))
    grant_data["delegation_chain"] = tuple(grant_data.get("delegation_chain", ()))
    grant = Grant(**grant_data)
    if envelope.get("transport_sender") != memory.source_agent:
        raise ValueError("TRANSPORT_SOURCE_MISMATCH")
    authorize(grant, recipient, memory)
    return {"status": "ACCEPTED", "recipient_agent": recipient.agent_id,
        "recipient_provider": recipient.provider_id, "recipient_model": recipient.model_id,
        "source_agent": memory.source_agent, "source_provider": memory.source_provider,
        "source_model": memory.source_model, "source_record_id": memory.source_record_id,
        "payload_sha256": digest, "content": memory.content}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sender", action="store_true")
    parser.add_argument("--receiver", action="store_true")
    args = parser.parse_args()
    if args.sender:
        sender, _, memory, grant = make_fixture()
        print(json.dumps(build_envelope(sender, memory, grant), ensure_ascii=False), end="")
        return 0
    if args.receiver:
        _, recipient, _, _ = make_fixture()
        result = receive(json.load(sys.stdin), recipient)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    sender = subprocess.run([sys.executable, __file__, "--sender"], check=True, capture_output=True, text=True)
    receiver = subprocess.run([sys.executable, __file__, "--receiver"], input=sender.stdout, check=True, capture_output=True, text=True)
    result = json.loads(receiver.stdout)
    print("LOCAL_CROSS_AGENT_EXCHANGE=PASS")
    print(f"ROUTE={result['source_agent']}({result['source_provider']}/{result['source_model']}) -> {result['recipient_agent']}({result['recipient_provider']}/{result['recipient_model']})")
    print(f"PROVENANCE={result['source_record_id']} PRESERVED")
    print(f"PAYLOAD_SHA256={result['payload_sha256']}")
    print("AUTHORIZATION=ACCEPTED (fixture grant; not production authentication)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
