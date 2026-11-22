use std::collections::HashMap;

use crate::{ClaimRevision, ClaimRevisionRef, DomainError};

/// Stores claim revisions and enforces uniqueness of revision references.
///
/// A revision reference can be registered only once. Non-initial revisions
/// must reference a previously registered parent revision belonging to the
/// same claim.
#[derive(Clone, Debug, Default)]
pub struct ClaimRevisionRegistry {
    revisions: HashMap<ClaimRevisionRef, ClaimRevision>,
}

impl ClaimRevisionRegistry {
    /// Creates an empty claim revision registry.
    pub fn new() -> Self {
        Self {
            revisions: HashMap::new(),
        }
    }

    /// Registers a claim revision.
    ///
    /// Registration validates the revision, rejects reused revision
    /// references, and verifies that any parent revision has already been
    /// registered and belongs to the same claim.
    pub fn register_revision(&mut self, revision: ClaimRevision) -> Result<(), DomainError> {
        revision.validate()?;

        if self.revisions.contains_key(revision.revision_ref()) {
            return Err(DomainError::StaleVersion);
        }

        match revision.parent_revision_ref() {
            Some(parent_ref) => {
                let parent = self
                    .revisions
                    .get(parent_ref)
                    .ok_or(DomainError::InvalidParent)?;

                revision.validate_parent(Some(parent))?;
            }
            None => {
                revision.validate_parent(None)?;
            }
        }

        self.revisions
            .insert(revision.revision_ref().clone(), revision);

        Ok(())
    }

    /// Returns the revision associated with the given reference, if present.
    pub fn get(&self, revision_ref: &ClaimRevisionRef) -> Option<&ClaimRevision> {
        self.revisions.get(revision_ref)
    }

    /// Returns whether the given revision reference has been registered.
    pub fn contains(&self, revision_ref: &ClaimRevisionRef) -> bool {
        self.revisions.contains_key(revision_ref)
    }

    /// Returns the number of registered revisions.
    pub fn len(&self) -> usize {
        self.revisions.len()
    }

    /// Returns whether the registry contains no revisions.
    pub fn is_empty(&self) -> bool {
        self.revisions.is_empty()
    }
}
