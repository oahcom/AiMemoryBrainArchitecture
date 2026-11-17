# Issue #20 — I Role Simulation: Global Producer/Recipient Inventory and Target Seal

**Status:** COORDINATOR-AUTHORED ROLE SIMULATION / PROPOSED / NOT I OWNER DECISION  
**Exact Storage review target:** commit `a65973093bb33c7c06ae503f421e096fadb5796b`, Blob `6f4b003b0a398c15b1f22a03c612f2c58afa3e7d`  
**Authority boundary:** This draft proposes I-owned governance and inventory semantics for I Owner review. It is not I approval, external governance approval, Global Forget authorization, implementation, or production evidence.

## 1. Inventory authority and producer identity

I owns the authoritative registry of producer domains, producer identities/instances, recipients, onward-copy paths, backups, replicas, restore sources and external delivery routes within the governed PolicyDomain. Each registry entry uses a typed immutable identity:
`(PolicyDomainId, ProducerDomainId, ProducerId, ProducerInstanceId, RouteOrRecipientId, IdentityGeneration)`.

The registry separately records enrollment state, operator/control owner, capability set, declared data classes, upstream/downstream routes, backup/replication relationships, retention class, last attestation and revocation state. Transport names and hostnames are attributes, not authority identities.

Unknown or unauthenticated producer/recipient/route is not silently excluded: classify it UNKNOWN, deny or quarantine the affected operation, and open an inventory discrepancy.

## 2. Independent completeness evidence

A TargetInventorySeal cannot be self-certified solely from the same producer list it is intended to prove complete. I must define a source-of-truth and reconciliation graph including:
- authoritative enrollment/control-plane registries;
- deployment and workload inventory;
- egress/recipient and onward-copy registries;
- backup, replication, snapshot and restore catalogs;
- external provider/processor contracts;
- independently observed telemetry or reconciliation evidence.

For each source, record source identity, authority, query/snapshot boundary, watermark, extraction digest, signer, freshness/expiry, coverage and known blind spots. A missing source, stale source, incomplete shard/page or unbounded onward-copy path makes the seal incomplete.

## 3. ProducerDomainInventoryEpoch

I's epoch is a monotonically increasing version within a canonical PolicyDomain scope. It advances on enrollment, de-enrollment, identity-generation change, route/recipient change, capability change, backup/restore topology change, revocation, retention-policy change and any source-of-truth correction affecting the target universe.

Epoch is not comparable to D's admission sequence or FenceGeneration. The D/I join is a typed relation over exact PolicyDomain, ProducerDomain/Producer/Instance identity generations and declared coverage, not numeric high-water arithmetic.

## 4. TargetInventorySeal

Seal preimage MUST canonically bind:
- PolicyDomainId and ForgetOperationId;
- InventoryEpoch and inventory-policy/schema version;
- canonical sorted target entries and explicit category counts;
- per-source snapshot boundary, source watermark and extraction digest;
- coverage matrix across producer, recipient, onward-copy, backup, replica, restore and external processor categories;
- explicit empty-category attestations;
- unknown/unreachable/unattested entries and discrepancy set;
- validity interval, revocation/invalidation generation and signer identity.

Seal digest/signature covers the complete canonical preimage. Pagination/sharding must provide deterministic shard IDs, shard count, ordered shard digests/Merkle root and a final root binding; omitted pages, duplicate identities, count/root mismatch or unavailable shards fail verification.

Empty category is valid only with positive evidence that the authoritative source was queried at the declared boundary and returned empty. NotApplicable requires a policy reason and accountable signer. Neither can be represented by omission/null.

## 5. D/I typed join proof

For each D-covered producer instance and scope:
- I supplies enrolled identity generation, authority/capability, inventory epoch and target inclusion/exclusion disposition;
- D supplies D registry generation, admission/fence semantics and producer-work identity relation;
- a join proof binds exact typed identities and both source digests.

Every I inventory target that can produce D-covered data must map to a D producer identity or an explicit D-exempt classification approved by D. Every D registered producer must map to an I inventory identity or an explicitly governed exception. Unmatched, stale-generation or ambiguous rows fail closed.

This join does not make I the owner of D work closure, nor D the owner of global inventory completeness.

## 6. Authorization, revocation and invalidation

Any change to producer identity, recipient route, inventory source, capability, policy, retention, legal hold, restore topology or revocation state invalidates the affected seal and all dependent completion evidence. Authorization is checked at operation admission, target enumeration, each external handoff and final completion. PermissionEpoch/revocation generation is bound into each authorization receipt.

Global Forget completion is prohibited while target inventory is incomplete, unknown recipients remain, a required source is stale/unreachable, a D/I join is unresolved, or an exception lacks an authorized governance decision. This draft does not grant legal authority or decide policy exceptions.

## 7. I-local release and negative tests

I may release its own inventory/authorization gate only when:
- the target set and all category counts are sealed;
- every required source is fresh and complete;
- all discrepancy/unknown sets are empty or explicitly dispositioned by an authorized decision;
- D/I join is complete;
- no revocation/PermissionEpoch change occurred after seal;
- a compare-and-swap confirms unchanged InventoryEpoch, seal generation and policy version.

Tests: empty category with and without positive attestation; omitted page/shard; stale source watermark; duplicate identity; identity generation rollover; unknown recipient; unbounded onward copy; backup catalog unavailable; seal revoked mid-operation; PermissionEpoch change; D/I orphan on either side; restore topology change; NotApplicable without reason; signature/canonicalization mismatch.

## 8. Open Owner decisions

I must decide authoritative source set, freshness thresholds, scope of onward-copy discovery, seal expiry/invalidation, exception authority, signer/audience model, and exact join cardinality. These are I-owned governance decisions; a Storage manifest or coordinator checklist cannot substitute for them.
