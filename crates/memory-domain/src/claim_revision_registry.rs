use std::collections::{HashMap, HashSet};

use crate::{ClaimRef, ClaimRevision, ClaimRevisionRef, DomainError};

#[derive(Debug, Default)]
pub struct ClaimRevisionRegistry {
    revisions: HashMap<ClaimRevisionRef, ClaimRevision>,
    accepted: HashSet<ClaimRevisionRef>,
    heads: HashMap<ClaimRef, ClaimRevisionRef>,
}

pub trait ClaimRevisionResolver {
    fn resolve_exact(&self, revision_ref: &ClaimRevisionRef) -> Option<&ClaimRevision>;
    fn resolve_head(&self, claim_ref: &ClaimRef) -> Option<&ClaimRevision>;
}

impl ClaimRevisionRegistry {
    pub fn register(&mut self, revision: ClaimRevision) -> Result<(), DomainError> {
        let revision_ref = revision.revision_ref().clone();

        if self.revisions.contains_key(&revision_ref) {
            return Err(DomainError::DuplicateClaimRevisionRef);
        }

        self.revisions.insert(revision_ref, revision);
        Ok(())
    }

    pub fn accept(&mut self, revision_ref: &ClaimRevisionRef) -> Result<(), DomainError> {
        let revision = self
            .revisions
            .get(revision_ref)
            .ok_or(DomainError::UnknownClaimRevision)?;

        if self.accepted.contains(revision_ref) {
            return Ok(());
        }

        if let Some(parent_ref) = revision.parent_revision_ref() {
            if !self.accepted.contains(parent_ref) {
                return Err(DomainError::InvalidParent);
            }
        }

        let claim_ref = revision.claim_ref().clone();

        self.accepted.insert(revision_ref.clone());
        self.heads.insert(claim_ref, revision_ref.clone());

        Ok(())
    }

    pub fn is_accepted(&self, revision_ref: &ClaimRevisionRef) -> bool {
        self.accepted.contains(revision_ref)
    }

    pub fn revision(&self, revision_ref: &ClaimRevisionRef) -> Option<&ClaimRevision> {
        self.revisions.get(revision_ref)
    }

    pub fn resolve_head(&self, claim_ref: &ClaimRef) -> Option<&ClaimRevision> {
        self.heads
            .get(claim_ref)
            .and_then(|revision_ref| self.revisions.get(revision_ref))
    }

    pub fn resolve_exact(&self, revision_ref: &ClaimRevisionRef) -> Option<&ClaimRevision> {
        self.revision(revision_ref)
    }
}

impl ClaimRevisionResolver for ClaimRevisionRegistry {
    fn resolve_exact(&self, revision_ref: &ClaimRevisionRef) -> Option<&ClaimRevision> {
        self.resolve_exact(revision_ref)
    }

    fn resolve_head(&self, claim_ref: &ClaimRef) -> Option<&ClaimRevision> {
        self.resolve_head(claim_ref)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::{EpistemicStatus, OpaqueId, ScopeKind, ScopeRef, TimeValue};

    fn scope() -> ScopeRef {
        ScopeRef {
            scope_id: OpaqueId::new("scope-1").unwrap(),
            scope_kind: ScopeKind::User,
            namespace_key: "user:scope-1".into(),
        }
    }

    fn initial(revision: &str, claim: &str) -> ClaimRevision {
        ClaimRevision::initial(
            ClaimRevisionRef::new(revision).unwrap(),
            ClaimRef::new(claim).unwrap(),
            "subject".into(),
            "predicate".into(),
            "object".into(),
            "affirm".into(),
            vec![],
            EpistemicStatus::Observed,
            TimeValue::Unknown,
            vec![],
            vec![],
            "2026-01-01T00:00:00Z".into(),
            "initial".into(),
            vec![scope()],
        )
        .unwrap()
    }

    fn successor(revision: &str, parent: &ClaimRevision) -> ClaimRevision {
        ClaimRevision::successor(
            ClaimRevisionRef::new(revision).unwrap(),
            parent.claim_ref().clone(),
            parent,
            "subject".into(),
            "predicate".into(),
            "updated object".into(),
            "affirm".into(),
            vec![],
            EpistemicStatus::Observed,
            TimeValue::Unknown,
            vec![],
            vec![],
            "2026-01-02T00:00:00Z".into(),
            "correction".into(),
            vec![scope()],
        )
        .unwrap()
    }

    #[test]
    fn duplicate_revision_ref_is_rejected_and_first_value_survives() {
        let first = initial("revision-1", "claim-1");
        let duplicate = ClaimRevision::initial(
            ClaimRevisionRef::new("revision-1").unwrap(),
            ClaimRef::new("claim-1").unwrap(),
            "subject".into(),
            "predicate".into(),
            "first value".into(),
            "affirm".into(),
            vec![],
            EpistemicStatus::Observed,
            TimeValue::Unknown,
            vec![],
            vec![],
            "2026-01-01T00:00:00Z".into(),
            "initial".into(),
            vec![scope()],
        )
        .unwrap();

        let mut registry = ClaimRevisionRegistry::default();
        registry.register(first).unwrap();

        assert_eq!(
            registry.register(duplicate),
            Err(DomainError::DuplicateClaimRevisionRef)
        );

        assert_eq!(
            registry
                .revision(&ClaimRevisionRef::new("revision-1").unwrap())
                .unwrap()
                .object(),
            "object"
        );
    }

    #[test]
    fn child_cannot_be_accepted_before_parent() {
        let parent = initial("revision-parent", "claim-1");
        let child = successor("revision-child", &parent);

        let mut registry = ClaimRevisionRegistry::default();
        registry.register(child).unwrap();
        registry.register(parent).unwrap();

        let parent_ref = ClaimRevisionRef::new("revision-parent").unwrap();
        let child_ref = ClaimRevisionRef::new("revision-child").unwrap();

        assert_eq!(registry.accept(&child_ref), Err(DomainError::InvalidParent));
        assert!(!registry.is_accepted(&child_ref));

        registry.accept(&parent_ref).unwrap();
        registry.accept(&child_ref).unwrap();

        assert!(registry.is_accepted(&parent_ref));
        assert!(registry.is_accepted(&child_ref));
    }

    #[test]
    fn accepting_twice_is_idempotent_and_does_not_move_head() {
        let parent = initial("revision-parent", "claim-1");
        let child = successor("revision-child", &parent);

        let mut registry = ClaimRevisionRegistry::default();
        registry.register(parent).unwrap();
        registry.register(child).unwrap();

        let parent_ref = ClaimRevisionRef::new("revision-parent").unwrap();
        let child_ref = ClaimRevisionRef::new("revision-child").unwrap();
        let claim_ref = ClaimRef::new("claim-1").unwrap();

        registry.accept(&parent_ref).unwrap();
        registry.accept(&child_ref).unwrap();

        assert_eq!(
            registry.resolve_head(&claim_ref).unwrap().revision_ref(),
            &child_ref
        );

        registry.accept(&parent_ref).unwrap();

        assert_eq!(
            registry.resolve_head(&claim_ref).unwrap().revision_ref(),
            &child_ref
        );
    }

    #[test]
    fn resolve_exact_refuses_head_substitution() {
        let parent = initial("revision-parent", "claim-1");

        let mut registry = ClaimRevisionRegistry::default();
        registry.register(parent).unwrap();

        let parent_ref = ClaimRevisionRef::new("revision-parent").unwrap();
        let unknown_ref = ClaimRevisionRef::new("revision-unregistered").unwrap();
        let claim_ref = ClaimRef::new("claim-1").unwrap();

        registry.accept(&parent_ref).unwrap();

        assert!(registry.resolve_head(&claim_ref).is_some());
        assert!(registry.resolve_exact(&unknown_ref).is_none());
    }

    #[test]
    fn head_resolves_child_while_exact_parent_remains_available() {
        let parent = initial("revision-parent", "claim-1");
        let child = successor("revision-child", &parent);

        let mut registry = ClaimRevisionRegistry::default();
        registry.register(parent).unwrap();
        registry.register(child).unwrap();

        let parent_ref = ClaimRevisionRef::new("revision-parent").unwrap();
        let child_ref = ClaimRevisionRef::new("revision-child").unwrap();
        let claim_ref = ClaimRef::new("claim-1").unwrap();

        registry.accept(&parent_ref).unwrap();
        registry.accept(&child_ref).unwrap();

        assert_eq!(
            registry.resolve_head(&claim_ref).unwrap().revision_ref(),
            &child_ref
        );

        assert_eq!(
            registry.resolve_exact(&parent_ref).unwrap().revision_ref(),
            &parent_ref
        );
    }
}
