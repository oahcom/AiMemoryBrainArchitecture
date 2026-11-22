use crate::{ClaimRevision, DomainError};

/// An accepted claim revision.
///
/// The wrapped revision is exposed only through an immutable reference.
/// Corrections must be appended as successor revisions; an accepted revision
/// cannot be modified through this type.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct AcceptedRevisionState {
    revision: ClaimRevision,
}

impl AcceptedRevisionState {
    /// Accepts an initial claim revision.
    ///
    /// A successor must be accepted through `append_successor`, where its
    /// parent can be checked against an existing accepted revision.
    pub fn accept(revision: ClaimRevision) -> Result<Self, DomainError> {
        revision.validate()?;
        revision.validate_parent(None)?;

        Ok(Self { revision })
    }

    /// Returns an immutable reference to the accepted revision.
    pub fn revision(&self) -> &ClaimRevision {
        &self.revision
    }

    /// Appends a successor without modifying the accepted revision.
    ///
    /// The successor must reference this revision as its parent and must
    /// belong to the same claim. The returned tuple contains the preserved
    /// previous state followed by the newly accepted successor state.
    pub fn append_successor(
        &self,
        successor: ClaimRevision,
    ) -> Result<(AcceptedRevisionState, AcceptedRevisionState), DomainError> {
        successor.validate()?;
        successor.validate_parent(Some(&self.revision))?;

        let previous = self.clone();
        let next = Self {
            revision: successor,
        };

        Ok((previous, next))
    }
}
