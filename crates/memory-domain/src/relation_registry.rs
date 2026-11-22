use std::collections::BTreeMap;

use crate::{DomainError, RelationDefinition, RelationExtension};

/// A registry of relation definitions, each associated with a vocabulary version.
///
/// Relation types are unique within a registry, regardless of version.
#[derive(Clone, Debug, Default)]
pub struct RelationTypeRegistry {
    definitions: BTreeMap<String, VersionedRelationDefinition>,
}

/// A relation definition together with the vocabulary version in which it is registered.
#[derive(Clone, Debug)]
struct VersionedRelationDefinition {
    version: u64,
    definition: RelationDefinition,
}

impl RelationTypeRegistry {
    /// Creates an empty relation type registry.
    pub fn new() -> Self {
        Self {
            definitions: BTreeMap::new(),
        }
    }

    /// Registers a relation definition with its vocabulary version.
    ///
    /// A version number of zero is invalid. Registering a relation type that
    /// already exists in this registry is rejected, even if the new definition
    /// specifies a different version.
    pub fn register(
        &mut self,
        version: u64,
        definition: RelationDefinition,
    ) -> Result<(), DomainError> {
        if version == 0 {
            return Err(DomainError::InvalidVersionNumber);
        }

        if definition.relation_type.is_empty() {
            return Err(DomainError::EmptyRequiredField("relation_type"));
        }

        if self.definitions.contains_key(&definition.relation_type) {
            return Err(DomainError::DuplicateRelationType);
        }

        self.definitions.insert(
            definition.relation_type.clone(),
            VersionedRelationDefinition {
                version,
                definition,
            },
        );

        Ok(())
    }

    /// Returns whether the given relation type is registered.
    pub fn contains_relation_type(&self, relation_type: &str) -> bool {
        self.definitions.contains_key(relation_type)
    }

    /// Looks up a registered relation definition by its relation type.
    pub fn lookup(&self, relation_type: &str) -> Option<&RelationDefinition> {
        self.definitions
            .get(relation_type)
            .map(|entry| &entry.definition)
    }

    /// Returns the vocabulary version associated with a registered relation type.
    pub fn version(&self, relation_type: &str) -> Option<u64> {
        self.definitions
            .get(relation_type)
            .map(|entry| entry.version)
    }

    /// Validates that the given relation type is registered and that the
    /// extension's endpoints satisfy its registered definition.
    ///
    /// `RelationExtension` carries no `relation_type` field, so the type must be
    /// supplied explicitly rather than inferred from endpoints or qualifiers.
    pub fn validate_against_registry(
        &self,
        relation_type: &str,
        extension: &RelationExtension,
    ) -> Result<(), DomainError> {
        let definition = self
            .lookup(relation_type)
            .ok_or(DomainError::UnregisteredRelationType)?;

        extension.validate(definition)
    }
}
