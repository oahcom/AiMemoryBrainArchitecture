//! The Compact operation and its lineage-safe output.
//!
//! `context-edit-operations.md` §2 Compact and
//! `context-budget-and-sufficiency.md` §5/§9.3 define compaction as a G-owned
//! derivative: it may shorten the rendering, but it must keep exact source
//! membership, provenance, evidence, epistemic qualifiers, uncertainty and any
//! declared loss, and it must never create or update Canonical Memory.
//!
//! Because "compact this" has no safe default, the caller declares what it
//! retained and what it dropped ([`CompactionOutput`]). This module then refuses
//! the result unless every declared retention is a superset of what the sources
//! actually carry, and every source that is not literally present in the new
//! rendering has an explicit, reasoned omission record. A compacted group that
//! passes is a typed artifact ([`CompactedGroup`]) that can be turned into a
//! Context entry without losing the ability to expand it back to its sources.

use crate::{stable_digest, ContextEntry, ContextError, ContextTier, OpaqueId};
use serde::{Deserialize, Serialize};
use std::collections::HashSet;

/// Algorithm/model/profile identity of one compaction.
///
/// §9.3 requires the profile to be recorded with the artifact so a later
/// validation can be reproduced and a semantic regression attributed.
#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct CompactionProfile {
    pub profile_id: String,
    pub algorithm: String,
    pub algorithm_version: String,
}

impl CompactionProfile {
    /// Validate the profile identity itself.
    pub fn validate(&self) -> Result<(), ContextError> {
        for (field, value) in [
            ("profile_id", &self.profile_id),
            ("algorithm", &self.algorithm),
            ("algorithm_version", &self.algorithm_version),
        ] {
            if value.trim().is_empty() {
                return Err(ContextError::EmptyField(field));
            }
        }
        Ok(())
    }
}

/// One source entry whose content is not literally present in the compacted
/// rendering, together with the reason it was lossy.
#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct CompactionOmission {
    pub entry_id: OpaqueId,
    pub note: String,
}

/// What the compactor claims about its own output.
#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct CompactionOutput {
    /// Identity of the compacted Context entry.
    pub group_id: OpaqueId,
    pub rendered_content: String,
    pub content_hash: String,
    /// Canonical source refs the compactor kept.
    pub retained_source_refs: Vec<OpaqueId>,
    /// Evidence refs the compactor kept.
    pub retained_evidence_refs: Vec<OpaqueId>,
    /// Epistemic qualifiers the compactor kept.
    pub retained_qualifiers: Vec<String>,
    /// Declared loss, one record per source that is not literally present.
    pub declared_omissions: Vec<CompactionOmission>,
}

/// A validated compacted projection with full source membership.
#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct CompactedGroup {
    pub group_id: OpaqueId,
    pub rendered_content: String,
    pub content_hash: String,
    pub tier: ContextTier,
    pub priority: i32,
    pub source_entry_ids: Vec<OpaqueId>,
    pub source_memory_ids: Vec<OpaqueId>,
    pub source_memory_version_ids: Vec<OpaqueId>,
    pub source_refs: Vec<OpaqueId>,
    pub evidence_refs: Vec<OpaqueId>,
    pub epistemic_qualifiers: Vec<String>,
    pub declared_omissions: Vec<CompactionOmission>,
    pub profile: CompactionProfile,
    /// Digest of the exact input source set.
    pub input_digest: String,
    /// Digest of the exact output rendering plus retained lineage.
    pub output_digest: String,
    /// Compacted bytes as a per-mille ratio of the source bytes.
    pub byte_ratio_permille: u32,
}

impl CompactedGroup {
    /// The Context entry this group materializes.
    ///
    /// A compacted projection has no single canonical Memory, so the entry's
    /// `memory_id`/`memory_version_id` are the group identity and the exact
    /// canonical refs travel in `source_refs` plus `compacted_from`. This is a
    /// Context artifact: no Canonical Memory is created or updated.
    pub fn to_entry(&self) -> ContextEntry {
        ContextEntry {
            entry_id: self.group_id.clone(),
            memory_id: self.group_id.clone(),
            memory_version_id: self.group_id.clone(),
            tier: self.tier,
            priority: self.priority,
            activation_reason: format!(
                "compacted by {} v{} ({})",
                self.profile.algorithm, self.profile.algorithm_version, self.profile.profile_id
            ),
            rendered_content: self.rendered_content.clone(),
            source_refs: self.source_refs.clone(),
            evidence_refs: self.evidence_refs.clone(),
            epistemic_qualifiers: self.epistemic_qualifiers.clone(),
            content_hash: self.content_hash.clone(),
            rendered_bytes: self.rendered_content.len(),
            compacted_from: self.source_entry_ids.clone(),
        }
    }
}

/// Validate fidelity and build the compacted group.
///
/// # Errors
///
/// Returns [`ContextError::CompactionFidelity`] when provenance, evidence or a
/// qualifier would be dropped, when verified language would be introduced, when a
/// lossy source has no declared omission, or when an omission names a non-source.
pub fn compact_entries(
    sources: &[ContextEntry],
    output: CompactionOutput,
    profile: &CompactionProfile,
) -> Result<CompactedGroup, ContextError> {
    profile.validate()?;
    if sources.is_empty() {
        return Err(ContextError::CompactionFidelity(
            "compaction requires at least one source entry".into(),
        ));
    }
    let mut source_ids: HashSet<&OpaqueId> = HashSet::new();
    for source in sources {
        if !source_ids.insert(&source.entry_id) {
            return Err(ContextError::CompactionFidelity(format!(
                "source entry {} appears twice",
                source.entry_id.as_str()
            )));
        }
    }
    if source_ids.contains(&output.group_id) {
        return Err(ContextError::CompactionFidelity(
            "compacted group id must differ from every source entry id".into(),
        ));
    }
    if output.rendered_content.trim().is_empty() {
        return Err(ContextError::EmptyField("rendered_content"));
    }
    if output.content_hash.trim().is_empty() {
        return Err(ContextError::EmptyField("content_hash"));
    }

    // Provenance must survive: the retained refs are a superset of the sources'.
    let required_source_refs =
        union_of(sources.iter().flat_map(|source| source.source_refs.iter()));
    for reference in &required_source_refs {
        if !output
            .retained_source_refs
            .iter()
            .any(|retained| retained == reference)
        {
            return Err(ContextError::CompactionFidelity(format!(
                "source lineage dropped: {}",
                reference.as_str()
            )));
        }
    }
    let required_evidence_refs = union_of(
        sources
            .iter()
            .flat_map(|source| source.evidence_refs.iter()),
    );
    for reference in &required_evidence_refs {
        if !output
            .retained_evidence_refs
            .iter()
            .any(|retained| retained == reference)
        {
            return Err(ContextError::CompactionFidelity(format!(
                "evidence ref dropped: {}",
                reference.as_str()
            )));
        }
    }

    // Uncertainty and qualifiers must survive, and must not be strengthened.
    let required_qualifiers = qualifier_union(sources);
    for qualifier in &required_qualifiers {
        if !output
            .retained_qualifiers
            .iter()
            .any(|retained| retained.eq_ignore_ascii_case(qualifier))
        {
            return Err(ContextError::CompactionFidelity(format!(
                "epistemic qualifier dropped: {qualifier}"
            )));
        }
    }
    let sources_are_verified = sources
        .iter()
        .all(|source| has_qualifier(source, "verified"));
    if !sources_are_verified
        && output
            .retained_qualifiers
            .iter()
            .any(|retained| retained.eq_ignore_ascii_case("verified"))
    {
        return Err(ContextError::CompactionFidelity(
            "compaction introduced verified language for a reported or inferred source".into(),
        ));
    }

    // Every lossy source needs an explicit, reasoned omission record.
    for source in sources {
        if output.rendered_content.contains(&source.rendered_content) {
            continue;
        }
        let declared = output
            .declared_omissions
            .iter()
            .find(|omission| omission.entry_id == source.entry_id);
        match declared {
            Some(omission) if !omission.note.trim().is_empty() => {}
            Some(_) => {
                return Err(ContextError::CompactionFidelity(format!(
                    "omission for entry {} has an empty reason",
                    source.entry_id.as_str()
                )));
            }
            None => {
                return Err(ContextError::CompactionFidelity(format!(
                    "undeclared omission for entry {}",
                    source.entry_id.as_str()
                )));
            }
        }
    }
    for omission in &output.declared_omissions {
        if !source_ids.contains(&omission.entry_id) {
            return Err(ContextError::CompactionFidelity(format!(
                "omission names a non-source entry {}",
                omission.entry_id.as_str()
            )));
        }
    }

    let mut source_entry_ids: Vec<OpaqueId> = sources
        .iter()
        .map(|source| source.entry_id.clone())
        .collect();
    source_entry_ids.sort();
    let mut source_memory_ids: Vec<OpaqueId> = sources
        .iter()
        .map(|source| source.memory_id.clone())
        .collect();
    source_memory_ids.sort();
    source_memory_ids.dedup();
    let mut source_memory_version_ids: Vec<OpaqueId> = sources
        .iter()
        .map(|source| source.memory_version_id.clone())
        .collect();
    source_memory_version_ids.sort();
    source_memory_version_ids.dedup();

    let mut source_refs = union_of(sources.iter().flat_map(|source| source.source_refs.iter()));
    source_refs.sort();
    let mut evidence_refs = union_of(
        sources
            .iter()
            .flat_map(|source| source.evidence_refs.iter()),
    );
    evidence_refs.sort();
    let mut epistemic_qualifiers = required_qualifiers;
    epistemic_qualifiers.sort();
    epistemic_qualifiers.dedup();
    let mut declared_omissions = output.declared_omissions.clone();
    declared_omissions.sort_by(|left, right| left.entry_id.cmp(&right.entry_id));

    let tier = sources
        .iter()
        .map(|source| source.tier)
        .min()
        .unwrap_or(ContextTier::P3);
    let priority = sources
        .iter()
        .map(|source| source.priority)
        .max()
        .unwrap_or(0);

    let input_digest = digest_of_source_set(sources)?;
    let output_digest =
        digest_of_output(&output, &source_refs, &evidence_refs, &epistemic_qualifiers)?;
    let source_bytes: usize = sources.iter().map(|source| source.rendered_bytes).sum();
    let byte_ratio_permille = output
        .rendered_content
        .len()
        .saturating_mul(1000)
        .checked_div(source_bytes)
        // A zero-byte source set has no ratio to report; 1000 is "unchanged".
        .map_or(1000, |ratio| u32::try_from(ratio).unwrap_or(u32::MAX));

    Ok(CompactedGroup {
        group_id: output.group_id,
        rendered_content: output.rendered_content,
        content_hash: output.content_hash,
        tier,
        priority,
        source_entry_ids,
        source_memory_ids,
        source_memory_version_ids,
        source_refs,
        evidence_refs,
        epistemic_qualifiers,
        declared_omissions,
        profile: profile.clone(),
        input_digest,
        output_digest,
        byte_ratio_permille,
    })
}

fn has_qualifier(entry: &ContextEntry, wanted: &str) -> bool {
    entry
        .epistemic_qualifiers
        .iter()
        .any(|qualifier| qualifier.eq_ignore_ascii_case(wanted))
}

fn qualifier_union(sources: &[ContextEntry]) -> Vec<String> {
    let mut seen: Vec<String> = Vec::new();
    for source in sources {
        for qualifier in &source.epistemic_qualifiers {
            let trimmed = qualifier.trim();
            if trimmed.is_empty() {
                continue;
            }
            if seen
                .iter()
                .any(|existing| existing.eq_ignore_ascii_case(trimmed))
            {
                continue;
            }
            seen.push(trimmed.to_owned());
        }
    }
    seen
}

fn union_of<'a, I>(references: I) -> Vec<OpaqueId>
where
    I: IntoIterator<Item = &'a OpaqueId>,
{
    let mut out: Vec<OpaqueId> = Vec::new();
    for reference in references {
        if !out.iter().any(|existing| existing == reference) {
            out.push(reference.clone());
        }
    }
    out
}

fn digest_of_source_set(sources: &[ContextEntry]) -> Result<String, ContextError> {
    let mut canonical: Vec<(&str, &str, usize)> = sources
        .iter()
        .map(|source| {
            (
                source.entry_id.as_str(),
                source.content_hash.as_str(),
                source.rendered_bytes,
            )
        })
        .collect();
    canonical.sort_unstable();
    let bytes = serde_json::to_vec(&canonical)
        .map_err(|error| ContextError::Serialization(error.to_string()))?;
    Ok(stable_digest(&bytes))
}

fn digest_of_output(
    output: &CompactionOutput,
    source_refs: &[OpaqueId],
    evidence_refs: &[OpaqueId],
    qualifiers: &[String],
) -> Result<String, ContextError> {
    let payload = (
        &output.rendered_content,
        &output.content_hash,
        source_refs,
        evidence_refs,
        qualifiers,
    );
    let bytes = serde_json::to_vec(&payload)
        .map_err(|error| ContextError::Serialization(error.to_string()))?;
    Ok(stable_digest(&bytes))
}

#[cfg(test)]
mod tests {
    use super::*;

    fn id(value: &str) -> OpaqueId {
        OpaqueId::new(value).unwrap()
    }

    fn source(entry: &str, content: &str, qualifier: &str) -> ContextEntry {
        ContextEntry {
            entry_id: id(entry),
            memory_id: id(&format!("memory-{entry}")),
            memory_version_id: id(&format!("version-{entry}")),
            tier: ContextTier::P1,
            priority: 5,
            activation_reason: "compaction source".into(),
            rendered_content: content.into(),
            source_refs: vec![id(&format!("source-{entry}"))],
            evidence_refs: vec![id(&format!("evidence-{entry}"))],
            epistemic_qualifiers: vec![qualifier.into()],
            content_hash: format!("sha256:{entry}"),
            rendered_bytes: content.len(),
            compacted_from: Vec::new(),
        }
    }

    fn profile() -> CompactionProfile {
        CompactionProfile {
            profile_id: "profile-1".into(),
            algorithm: "extractive".into(),
            algorithm_version: "1".into(),
        }
    }

    fn output(sources: &[ContextEntry], rendered: &str) -> CompactionOutput {
        CompactionOutput {
            group_id: id("group"),
            rendered_content: rendered.into(),
            content_hash: "sha256:group".into(),
            retained_source_refs: sources
                .iter()
                .flat_map(|entry| entry.source_refs.iter().cloned())
                .collect(),
            retained_evidence_refs: sources
                .iter()
                .flat_map(|entry| entry.evidence_refs.iter().cloned())
                .collect(),
            retained_qualifiers: sources
                .iter()
                .flat_map(|entry| entry.epistemic_qualifiers.iter().cloned())
                .collect(),
            declared_omissions: sources
                .iter()
                .filter(|entry| !rendered.contains(&entry.rendered_content))
                .map(|entry| CompactionOmission {
                    entry_id: entry.entry_id.clone(),
                    note: "paraphrased under the declared profile".into(),
                })
                .collect(),
        }
    }

    #[test]
    fn compaction_preserves_lineage_and_expands_back_to_its_sources() {
        let sources = vec![
            source("a", "alpha", "reported"),
            source("b", "beta", "inferred"),
        ];
        let group =
            compact_entries(&sources, output(&sources, "alpha and beta"), &profile()).unwrap();
        assert_eq!(group.source_entry_ids, vec![id("a"), id("b")]);
        // Tier and priority are inherited rather than invented.
        assert_eq!(group.tier, ContextTier::P1);
        assert_eq!(group.priority, 5);
        // The entry can be expanded back to the exact membership it replaced.
        let entry = group.to_entry();
        assert_eq!(entry.compacted_from, vec![id("a"), id("b")]);
        assert_eq!(entry.entry_id, id("group"));
        // Both source refs and both evidence refs survived.
        assert_eq!(entry.source_refs.len(), 2);
        assert_eq!(entry.evidence_refs.len(), 2);
    }

    #[test]
    fn dropping_a_source_qualifier_is_a_fidelity_error() {
        let sources = vec![source("a", "alpha", "reported")];
        let mut declared = output(&sources, "alpha");
        declared.retained_qualifiers.clear();
        assert!(matches!(
            compact_entries(&sources, declared, &profile()),
            Err(ContextError::CompactionFidelity(reason)) if reason.contains("qualifier")
        ));
    }

    #[test]
    fn introducing_verified_language_for_an_unverified_source_is_refused() {
        let sources = vec![source("a", "alpha", "inferred")];
        let mut declared = output(&sources, "alpha");
        declared.retained_qualifiers.push("verified".into());
        assert!(matches!(
            compact_entries(&sources, declared, &profile()),
            Err(ContextError::CompactionFidelity(reason)) if reason.contains("verified")
        ));
    }

    #[test]
    fn a_lossy_source_without_a_declared_omission_is_refused() {
        let sources = vec![source("a", "alpha", "reported")];
        let mut declared = output(&sources, "completely different rendering");
        declared.declared_omissions.clear();
        assert!(matches!(
            compact_entries(&sources, declared, &profile()),
            Err(ContextError::CompactionFidelity(reason)) if reason.contains("undeclared omission")
        ));
    }
}
