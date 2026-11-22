use std::collections::HashMap;

use crate::{ClaimRef, ClaimRevision, ClaimRevisionRef, ClaimRevisionRegistry, DomainError};

/// Resolves claim revisions by their exact references.
///
/// The resolver also tracks the current head for each claim. A successor can
/// advance a claim's head only when its parent is the currently registered
/// head of that claim.
#[derive(Clone, Debug, Default)]
pub struct ClaimRevisionResolver {
    registry: ClaimRevisionRegistry,
    heads: HashMap<ClaimRef, ClaimRevisionRef>,
}

impl ClaimRevisionResolver {
    /// Creates an empty claim revision resolver.
    pub fn new() -> Self {
        Self {
            registry: ClaimRevisionRegistry::new(),
            heads: HashMap::new(),
        }
    }

    /// Registers a revision and updates the head of its claim.
    ///
    /// An initial revision is rejected if the claim already has a head.
    /// A successor is accepted only if its parent is the current head.
    pub fn register_revision(&mut self, revision: ClaimRevision) -> Result<(), DomainError> {
        let claim_ref = revision.claim_ref().clone();
        let revision_ref = revision.revision_ref().clone();

        match revision.parent_revision_ref() {
            Some(parent_ref) => {
                let current_head = self
                    .heads
                    .get(&claim_ref)
                    .ok_or(DomainError::InvalidParent)?;

                if parent_ref != current_head {
                    return Err(DomainError::InvalidParent);
                }
            }
            None => {
                if self.heads.contains_key(&claim_ref) {
                    return Err(DomainError::InvalidParent);
                }
            }
        }

        self.registry.register_revision(revision)?;
        self.heads.insert(claim_ref, revision_ref);

        Ok(())
    }

    /// Resolves exactly the supplied revision reference.
    ///
    /// This method never substitutes the current claim head for the supplied
    /// revision reference.
    pub fn resolve(&self, revision_ref: &ClaimRevisionRef) -> Result<&ClaimRevision, DomainError> {
        self.registry
            .get(revision_ref)
            .ok_or(DomainError::MissingClaimRevision)
    }

    /// Resolves the current head of the supplied claim.
    ///
    /// This is an explicit claim-head lookup. It does not accept a
    /// `ClaimRevisionRef` and is not used as a fallback by `resolve`.
    pub fn resolve_head(&self, claim_ref: &ClaimRef) -> Result<&ClaimRevision, DomainError> {
        let head_ref = self
            .heads
            .get(claim_ref)
            .ok_or(DomainError::MissingClaimRevision)?;

        self.resolve(head_ref)
    }

    /// Resolves a pinned revision while checking the caller's current-head
    /// reference for the same claim.
    ///
    /// The supplied head is validated but is never returned as a substitute
    /// for `pinned`. If `pinned` identifies an older revision, that older
    /// revision is returned.
    pub fn resolve_exact(
        &self,
        pinned: &ClaimRevisionRef,
        claim_head: &ClaimRevisionRef,
    ) -> Result<&ClaimRevision, DomainError> {
        let pinned_revision = self.resolve(pinned)?;
        let head_revision = self.resolve(claim_head)?;

        if pinned_revision.claim_ref() != head_revision.claim_ref() {
            return Err(DomainError::InvalidParent);
        }

        let current_head = self
            .heads
            .get(pinned_revision.claim_ref())
            .ok_or(DomainError::MissingClaimRevision)?;

        if current_head != claim_head {
            return Err(DomainError::InvalidParent);
        }

        // Deliberately return the pinned revision, not the supplied head.
        Ok(pinned_revision)
    }

    /// Returns whether the exact revision reference has been registered.
    pub fn contains(&self, revision_ref: &ClaimRevisionRef) -> bool {
        self.registry.contains(revision_ref)
    }

    /// Returns the number of registered revisions.
    pub fn len(&self) -> usize {
        self.registry.len()
    }

    /// Returns whether no revisions have been registered.
    pub fn is_empty(&self) -> bool {
        self.registry.is_empty()
    }
}
