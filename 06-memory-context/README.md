# Session G — Memory Context package

**Publication status:** candidate architecture and historical review evidence; not a frozen cross-owner contract.

This package contains G's proposed Memory Context architecture, G-owned semantic decisions and delegated review records. It is published as a bounded design baseline for continued integration, not as evidence of production implementation or a global Applied/Forget acceptance.

## Authority and evidence boundary

- G owns desired Context membership, ordering, eligibility, budget, immutable Context versions, reconciliation and delivery intent.
- D owns Canonical Memory and ForgetFence; F owns retrieval/archive; I owns identity, permission and global governance; C owns the final request boundary and provider outcome; H owns transport/Adapter evidence; Storage owns durable serialization and recovery.
- No G document in this package overrides another Owner's authority or substitutes for that Owner's exact-version acceptance.
- Role-based/delegated G reviews and acceptance records were prepared centrally under the user's instruction. They are not independent human Owner signatures and must not be represented as such.
- Some review artifacts pin historical branch HEADs and Blob SHAs. Before relying on a decision for current integration, refresh the exact source branch and re-review the exact current artifact.
- The Phase 3.8.22 contract is a normative design draft only: implementation NOT VERIFIED; crash/restart/restore tests NOT RUN; C/G/H Applied freeze NO; production egress NOT AUTHORIZED.
- The earlier main-branch three-party review remains preserved as a historical FAIL snapshot. The follow-up review is stored separately and does not erase that history.

## Current package disposition

**CANDIDATE FOR CONTINUED CROSS-OWNER INTEGRATION — NOT FROZEN.** Generic Scope, cross-module wire details, global Forget completion, production Applied evidence, durable replay, Storage linearization and exact current Owner acceptances remain open.
