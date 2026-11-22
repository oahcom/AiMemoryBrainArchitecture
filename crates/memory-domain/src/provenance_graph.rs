use std::collections::{BTreeMap, BTreeSet, HashMap, HashSet};

use crate::{DomainError, Provenance, ProvenanceRef};

/// A directed derivation edge from an upstream provenance to a derived one.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct DerivationEdge {
    pub from: ProvenanceRef,
    pub to: ProvenanceRef,
}

/// A deterministic provenance derivation graph.
///
/// Edge direction: parent -> child.
///
/// Unregistered parents are retained as dangling references and resolved
/// whenever a new provenance node is registered.
#[derive(Clone, Debug, Default)]
pub struct ProvenanceGraph {
    nodes: BTreeMap<String, Provenance>,
    edges: BTreeSet<(String, String)>,
    dangling: BTreeSet<(String, String)>,
}

impl ProvenanceGraph {
    pub fn new() -> Self {
        Self::default()
    }

    /// Registers a provenance node and its explicitly declared parents.
    ///
    /// `parents` is the sole source of derivation edges.
    /// `Provenance::source_refs` is intentionally not interpreted as lineage.
    ///
    /// The operation is atomic: if cycle detection fails, the original graph
    /// remains unchanged.
    pub fn add(
        &mut self,
        provenance: Provenance,
        parents: &[ProvenanceRef],
    ) -> Result<(), DomainError> {
        let node_id = provenance.provenance_id.as_str().to_owned();

        if self.nodes.contains_key(&node_id) {
            return Err(DomainError::InvalidParent);
        }

        // Work on a candidate graph so every failure leaves `self` unchanged.
        let mut candidate = self.clone();

        candidate.nodes.insert(node_id.clone(), provenance);

        for parent in parents {
            let parent_id = parent.as_str().to_owned();

            if candidate.nodes.contains_key(&parent_id) {
                candidate
                    .edges
                    .insert((parent_id, node_id.clone()));
            } else {
                candidate
                    .dangling
                    .insert((parent_id, node_id.clone()));
            }
        }

        // Re-resolve every dangling parent reference.
        //
        // A dangling edge is stored as (parent, child).
        // Its child is already registered; only its parent may be missing.
        let resolved: Vec<(String, String)> = candidate
            .dangling
            .iter()
            .filter(|(parent, _)| candidate.nodes.contains_key(parent))
            .cloned()
            .collect();

        for edge in resolved {
            candidate.dangling.remove(&edge);
            candidate.edges.insert(edge);
        }

        // Reject cycles across the complete resolved graph.
        if !candidate.is_acyclic() {
            return Err(DomainError::InvalidParent);
        }

        // Commit only after all validation succeeds.
        *self = candidate;

        Ok(())
    }

    /// Returns all transitive ancestors of a registered provenance node.
    ///
    /// The result excludes `of` itself and is sorted lexicographically
    /// by ProvenanceRef::as_str().
    pub fn ancestors(
        &self,
        of: &ProvenanceRef,
    ) -> Result<Vec<ProvenanceRef>, DomainError> {
        // Empty graphs have no known ancestry.
        if self.nodes.is_empty() {
            return Ok(Vec::new());
        }

        let start = of.as_str();

        if !self.nodes.contains_key(start) {
            return Err(DomainError::InvalidParent);
        }

        let mut visited: HashSet<String> = HashSet::new();
        let mut pending: Vec<String> = vec![start.to_owned()];

        while let Some(current) = pending.pop() {
            // Traverse incoming edges: parent -> current.
            for (parent, child) in &self.edges {
                if child == &current && visited.insert(parent.clone()) {
                    pending.push(parent.clone());
                }
            }
        }

        visited.remove(start);

        let mut result: Vec<ProvenanceRef> = visited
            .into_iter()
            .map(|id| {
                ProvenanceRef::new(id)
                    .expect("registered provenance identifiers are non-empty")
            })
            .collect();

        result.sort_by(|left, right| left.as_str().cmp(right.as_str()));

        Ok(result)
    }

    /// Returns whether two provenance nodes share a common ancestor.
    ///
    /// A direct ancestor/descendant relationship also counts as shared
    /// lineage, even when the intersection of the strict ancestor sets
    /// would otherwise be empty.
    pub fn shares_ancestor(
        &self,
        left: &ProvenanceRef,
        right: &ProvenanceRef,
    ) -> Result<bool, DomainError> {
        if self.nodes.is_empty() {
            return Ok(false);
        }

        let left_ancestors = self.ancestors(left)?;
        let right_ancestors = self.ancestors(right)?;

        let left_ids: HashSet<&str> = left_ancestors
            .iter()
            .map(ProvenanceRef::as_str)
            .collect();

        let right_ids: HashSet<&str> = right_ancestors
            .iter()
            .map(ProvenanceRef::as_str)
            .collect();

        // Strict ancestor-set intersection.
        if left_ids.iter().any(|id| right_ids.contains(id)) {
            return Ok(true);
        }

        // Include direct and transitive ancestor/descendant relationships.
        if left_ids.contains(right.as_str())
            || right_ids.contains(left.as_str())
        {
            return Ok(true);
        }

        Ok(false)
    }

    /// Checks whether the registered graph is acyclic.
    ///
    /// DFS colors:
    ///   0 = white (unvisited)
    ///   1 = gray  (currently on recursion stack)
    ///   2 = black (fully processed)
    ///
    /// An edge to a gray node indicates a cycle.
    fn is_acyclic(&self) -> bool {
        let mut adjacency: BTreeMap<String, Vec<String>> = BTreeMap::new();

        for node in self.nodes.keys() {
            adjacency.entry(node.clone()).or_default();
        }

        for (from, to) in &self.edges {
            adjacency
                .entry(from.clone())
                .or_default()
                .push(to.clone());
        }

        for children in adjacency.values_mut() {
            children.sort();
            children.dedup();
        }

        let mut colors: HashMap<String, u8> = HashMap::new();

        for node in self.nodes.keys() {
            if colors.get(node).copied().unwrap_or(0) == 0
                && !Self::visit(node, &adjacency, &mut colors)
            {
                return false;
            }
        }

        true
    }

    fn visit(
        node: &str,
        adjacency: &BTreeMap<String, Vec<String>>,
        colors: &mut HashMap<String, u8>,
    ) -> bool {
        // Gray: revisiting a node on the active DFS path means a cycle.
        if colors.get(node).copied() == Some(1) {
            return false;
        }

        // Black: this subtree has already been completely checked.
        if colors.get(node).copied() == Some(2) {
            return true;
        }

        colors.insert(node.to_owned(), 1);

        if let Some(children) = adjacency.get(node) {
            for child in children {
                if !Self::visit(child, adjacency, colors) {
                    return false;
                }
            }
        }

        colors.insert(node.to_owned(), 2);

        true
    }
}

/// Validates whether two provenance references represent independent evidence.
pub struct EvidenceIndependence;

impl EvidenceIndependence {
    pub fn validate_independent(
        graph: &ProvenanceGraph,
        left: &ProvenanceRef,
        right: &ProvenanceRef,
    ) -> Result<(), DomainError> {
        if left == right {
            return Err(DomainError::InvalidParent);
        }

        if graph.shares_ancestor(left, right)? {
            return Err(DomainError::InvalidParent);
        }

        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::{ActorRef, OpaqueId};

    fn provenance(id: &str) -> Provenance {
        Provenance {
            provenance_id: OpaqueId::new(id).unwrap(),
            source_refs: Vec::new(),
            derivation_kind: "test".into(),
            actor_ref: ActorRef {
                actor_id: OpaqueId::new("actor-test").unwrap(),
            },
            created_at: "2026-01-01T00:00:00Z".into(),
        }
    }

    fn reference(id: &str) -> ProvenanceRef {
        ProvenanceRef::new(id).unwrap()
    }

    fn add(
        graph: &mut ProvenanceGraph,
        id: &str,
        parents: &[&str],
    ) -> Result<(), DomainError> {
        let parents: Vec<ProvenanceRef> =
            parents.iter().map(|id| reference(id)).collect();

        graph.add(provenance(id), &parents)
    }

    fn ancestor_ids(
        graph: &ProvenanceGraph,
        id: &str,
    ) -> Vec<String> {
        graph
            .ancestors(&reference(id))
            .unwrap()
            .into_iter()
            .map(|reference| reference.as_str().to_owned())
            .collect()
    }

    // 1. Empty graph.
    #[test]
    fn empty_graph_has_no_ancestors_or_shared_ancestry() {
        let graph = ProvenanceGraph::new();

        assert_eq!(graph.ancestors(&reference("A")).unwrap(), Vec::new());

        assert!(!graph
            .shares_ancestor(&reference("A"), &reference("B"))
            .unwrap());
    }

    // 2. Single chain A -> B -> C.
    #[test]
    fn single_chain_returns_sorted_transitive_ancestors() {
        let mut graph = ProvenanceGraph::new();

        add(&mut graph, "A", &[]).unwrap();
        add(&mut graph, "B", &["A"]).unwrap();
        add(&mut graph, "C", &["B"]).unwrap();

        assert_eq!(
            ancestor_ids(&graph, "C"),
            vec!["A".to_owned(), "B".to_owned()]
        );
    }

    // 3. Diamond A -> B, A -> C, B -> D, C -> D.
    #[test]
    fn diamond_graph_returns_unique_ancestors() {
        let mut graph = ProvenanceGraph::new();

        add(&mut graph, "A", &[]).unwrap();
        add(&mut graph, "B", &["A"]).unwrap();
        add(&mut graph, "C", &["A"]).unwrap();
        add(&mut graph, "D", &["B", "C"]).unwrap();

        let ancestors = ancestor_ids(&graph, "D");

        assert_eq!(
            ancestors,
            vec![
                "A".to_owned(),
                "B".to_owned(),
                "C".to_owned()
            ]
        );

        let unique: HashSet<&str> =
            ancestors.iter().map(String::as_str).collect();

        assert_eq!(unique.len(), ancestors.len());
    }

    // 4. Cycle detection A -> B -> A.
    #[test]
    fn cycle_is_rejected() {
        let mut graph = ProvenanceGraph::new();

        add(&mut graph, "A", &[]).unwrap();
        add(&mut graph, "B", &["A"]).unwrap();

        assert_eq!(
            add(&mut graph, "A", &["B"]),
            Err(DomainError::InvalidParent)
        );
    }

    // 5. Failed add rolls back all candidate state.
    #[test]
    fn failed_add_rolls_back_graph_state() {
        let mut graph = ProvenanceGraph::new();

        add(&mut graph, "A", &[]).unwrap();
        add(&mut graph, "B", &["A"]).unwrap();

        let result = add(&mut graph, "A", &["B"]);

        assert_eq!(result, Err(DomainError::InvalidParent));

        // The original graph still contains A and B.
        assert!(graph.nodes.contains_key("A"));
        assert!(graph.nodes.contains_key("B"));
        assert_eq!(graph.nodes.len(), 2);

        // The only formal edge is still A -> B.
        assert_eq!(
            graph.edges,
            BTreeSet::from([("A".to_owned(), "B".to_owned())])
        );

        // No dangling state was introduced by the failed operation.
        assert!(graph.dangling.is_empty());

        assert_eq!(
            ancestor_ids(&graph, "B"),
            vec!["A".to_owned()]
        );
    }

    // 6. An unresolved parent is resolved when it is registered later.
    #[test]
    fn dangling_parent_is_resolved_after_out_of_order_registration() {
        let mut graph = ProvenanceGraph::new();

        add(&mut graph, "A", &["B"]).unwrap();

        assert!(graph.edges.is_empty());
        assert_eq!(
            graph.dangling,
            BTreeSet::from([("B".to_owned(), "A".to_owned())])
        );

        add(&mut graph, "B", &[]).unwrap();

        assert_eq!(
            ancestor_ids(&graph, "A"),
            vec!["B".to_owned()]
        );

        assert!(graph.dangling.is_empty());

        assert_eq!(
            graph.edges,
            BTreeSet::from([("B".to_owned(), "A".to_owned())])
        );
    }

    // 7. Shared ancestry rejects independence; isolated nodes are independent.
    #[test]
    fn independence_checks_shared_and_separate_lineage() {
        let mut graph = ProvenanceGraph::new();

        add(&mut graph, "ROOT", &[]).unwrap();
        add(&mut graph, "LEFT", &["ROOT"]).unwrap();
        add(&mut graph, "RIGHT", &["ROOT"]).unwrap();

        add(&mut graph, "ISOLATED_A", &[]).unwrap();
        add(&mut graph, "ISOLATED_B", &[]).unwrap();

        assert_eq!(
            EvidenceIndependence::validate_independent(
                &graph,
                &reference("LEFT"),
                &reference("RIGHT"),
            ),
            Err(DomainError::InvalidParent)
        );

        assert_eq!(
            EvidenceIndependence::validate_independent(
                &graph,
                &reference("ISOLATED_A"),
                &reference("ISOLATED_B"),
            ),
            Ok(())
        );
    }

    // 8. A provenance node cannot be independent from itself.
    #[test]
    fn same_node_is_not_independent_from_itself() {
        let mut graph = ProvenanceGraph::new();

        add(&mut graph, "A", &[]).unwrap();

        assert_eq!(
            EvidenceIndependence::validate_independent(
                &graph,
                &reference("A"),
                &reference("A"),
            ),
            Err(DomainError::InvalidParent)
        );
    }

    // Additional: a direct ancestor/descendant pair is not independent.
    #[test]
    fn ancestor_and_descendant_are_not_independent() {
        let mut graph = ProvenanceGraph::new();

        add(&mut graph, "A", &[]).unwrap();
        add(&mut graph, "B", &["A"]).unwrap();

        assert_eq!(
            graph.shares_ancestor(&reference("A"), &reference("B")),
            Ok(true)
        );

        assert_eq!(
            EvidenceIndependence::validate_independent(
                &graph,
                &reference("A"),
                &reference("B"),
            ),
            Err(DomainError::InvalidParent)
        );
    }

    // Additional: duplicate registration is rejected without mutation.
    #[test]
    fn duplicate_registration_is_rejected() {
        let mut graph = ProvenanceGraph::new();

        add(&mut graph, "A", &[]).unwrap();

        assert_eq!(
            add(&mut graph, "A", &[]),
            Err(DomainError::InvalidParent)
        );

        assert_eq!(graph.nodes.len(), 1);
        assert!(graph.edges.is_empty());
        assert!(graph.dangling.is_empty());
    }
}
