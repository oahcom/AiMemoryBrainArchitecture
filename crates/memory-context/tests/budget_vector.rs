//! The budget is a vector of independent limits, not a single Top-K.
//!
//! Spec: `06-memory-context/context-budget-and-sufficiency.md` §1–§2, §7.
//! Every dimension fails closed with its own typed error carrying
//! `actual`/`limit`, an exactly-at-limit usage fits (inclusive, matching the
//! existing entry/byte behaviour), and an unset limit is unbounded.

use memory_context::{
    BudgetUsage, BudgetVector, BudgetVectorError, ContextBudget, ContextError, ContextTier,
};

fn usage() -> BudgetUsage {
    BudgetUsage::default()
}

#[test]
fn token_budget_rejects_overflow_and_admits_exact_estimate() {
    let budget = BudgetVector {
        tokens: Some(100),
        ..BudgetVector::default()
    };

    assert_eq!(
        budget.check(&BudgetUsage {
            tokens: 101,
            ..usage()
        }),
        Err(BudgetVectorError::TokenBudgetExceeded {
            actual: 101,
            limit: 100
        })
    );
    assert_eq!(
        budget.check(&BudgetUsage {
            tokens: 100,
            ..usage()
        }),
        Ok(())
    );
    assert_eq!(
        BudgetVector::default().check(&BudgetUsage {
            tokens: u64::MAX,
            ..usage()
        }),
        Ok(())
    );
}

#[test]
fn fan_out_budget_rejects_overflow_and_admits_exact_fan_out() {
    let budget = BudgetVector {
        relation_fan_out: Some(8),
        ..BudgetVector::default()
    };

    assert_eq!(
        budget.check(&BudgetUsage {
            relation_fan_out: 9,
            ..usage()
        }),
        Err(BudgetVectorError::FanOutBudgetExceeded {
            actual: 9,
            limit: 8
        })
    );
    assert_eq!(
        budget.check(&BudgetUsage {
            relation_fan_out: 8,
            ..usage()
        }),
        Ok(())
    );
    assert_eq!(
        BudgetVector::default().check(&BudgetUsage {
            relation_fan_out: u64::MAX,
            ..usage()
        }),
        Ok(())
    );
}

#[test]
fn provenance_depth_budget_rejects_overflow_and_admits_exact_depth() {
    let budget = BudgetVector {
        provenance_depth: Some(3),
        ..BudgetVector::default()
    };

    assert_eq!(
        budget.check(&BudgetUsage {
            provenance_depth: 4,
            ..usage()
        }),
        Err(BudgetVectorError::ProvenanceDepthBudgetExceeded {
            actual: 4,
            limit: 3
        })
    );
    assert_eq!(
        budget.check(&BudgetUsage {
            provenance_depth: 3,
            ..usage()
        }),
        Ok(())
    );
    assert_eq!(
        BudgetVector::default().check(&BudgetUsage {
            provenance_depth: u64::MAX,
            ..usage()
        }),
        Ok(())
    );
}

#[test]
fn latency_budget_rejects_overflow_and_admits_exact_allowance() {
    let budget = BudgetVector {
        latency_micros: Some(500),
        ..BudgetVector::default()
    };

    assert_eq!(
        budget.check(&BudgetUsage {
            latency_micros: 501,
            ..usage()
        }),
        Err(BudgetVectorError::LatencyBudgetExceeded {
            actual: 501,
            limit: 500
        })
    );
    assert_eq!(
        budget.check(&BudgetUsage {
            latency_micros: 500,
            ..usage()
        }),
        Ok(())
    );
    assert_eq!(
        BudgetVector::default().check(&BudgetUsage {
            latency_micros: u64::MAX,
            ..usage()
        }),
        Ok(())
    );
}

#[test]
fn cpu_budget_rejects_overflow_and_admits_exact_allowance() {
    let budget = BudgetVector {
        cpu_micros: Some(250),
        ..BudgetVector::default()
    };

    assert_eq!(
        budget.check(&BudgetUsage {
            cpu_micros: 251,
            ..usage()
        }),
        Err(BudgetVectorError::CpuBudgetExceeded {
            actual: 251,
            limit: 250
        })
    );
    assert_eq!(
        budget.check(&BudgetUsage {
            cpu_micros: 250,
            ..usage()
        }),
        Ok(())
    );
    assert_eq!(
        BudgetVector::default().check(&BudgetUsage {
            cpu_micros: u64::MAX,
            ..usage()
        }),
        Ok(())
    );
}

#[test]
fn tier_reserve_rejects_overflow_and_admits_exact_reserved_capacity() {
    let budget = BudgetVector {
        tier_entries: vec![(ContextTier::P0, 2)],
        ..BudgetVector::default()
    };

    assert_eq!(
        budget.check(&BudgetUsage {
            tier_entries: vec![(ContextTier::P0, 3)],
            ..usage()
        }),
        Err(BudgetVectorError::TierReserveExceeded {
            tier: ContextTier::P0,
            actual: 3,
            limit: 2
        })
    );
    assert_eq!(
        budget.check(&BudgetUsage {
            tier_entries: vec![(ContextTier::P0, 2)],
            ..usage()
        }),
        Ok(())
    );
    assert_eq!(
        BudgetVector::default().check(&BudgetUsage {
            tier_entries: vec![
                (ContextTier::P0, u64::MAX),
                (ContextTier::P1, u64::MAX),
                (ContextTier::P2, u64::MAX),
            ],
            ..usage()
        }),
        Ok(())
    );
}

#[test]
fn unlisted_tier_is_unbounded_while_a_listed_tier_is_capped() {
    let budget = BudgetVector {
        tier_entries: vec![(ContextTier::P0, 1)],
        ..BudgetVector::default()
    };

    assert_eq!(
        budget.check(&BudgetUsage {
            tier_entries: vec![(ContextTier::P0, 1), (ContextTier::P2, 99)],
            ..usage()
        }),
        Ok(())
    );
}

#[test]
fn an_exhausted_budget_of_zero_is_not_unbounded() {
    assert_eq!(
        BudgetVector {
            tokens: Some(0),
            ..BudgetVector::default()
        }
        .check(&BudgetUsage {
            tokens: 1,
            ..usage()
        }),
        Err(BudgetVectorError::TokenBudgetExceeded {
            actual: 1,
            limit: 0
        })
    );
}

#[test]
fn dimensions_are_independent_so_satisfying_one_does_not_mask_another_overflow() {
    let budget = BudgetVector {
        tokens: Some(100),
        relation_fan_out: Some(8),
        provenance_depth: Some(3),
        latency_micros: Some(500),
        cpu_micros: Some(250),
        tier_entries: vec![(ContextTier::P0, 2)],
    };
    let within_every_limit = BudgetUsage {
        tokens: 100,
        relation_fan_out: 8,
        provenance_depth: 3,
        latency_micros: 500,
        cpu_micros: 250,
        tier_entries: vec![(ContextTier::P0, 2)],
    };
    assert_eq!(budget.check(&within_every_limit), Ok(()));

    // Satisfying all other dimensions never hides the overflowing one.
    let overflows = [
        BudgetUsage {
            tokens: 101,
            ..within_every_limit.clone()
        },
        BudgetUsage {
            relation_fan_out: 9,
            ..within_every_limit.clone()
        },
        BudgetUsage {
            provenance_depth: 4,
            ..within_every_limit.clone()
        },
        BudgetUsage {
            latency_micros: 501,
            ..within_every_limit.clone()
        },
        BudgetUsage {
            cpu_micros: 251,
            ..within_every_limit.clone()
        },
        BudgetUsage {
            tier_entries: vec![(ContextTier::P0, 3)],
            ..within_every_limit.clone()
        },
    ];
    let expected = [
        BudgetVectorError::TokenBudgetExceeded {
            actual: 101,
            limit: 100,
        },
        BudgetVectorError::FanOutBudgetExceeded {
            actual: 9,
            limit: 8,
        },
        BudgetVectorError::ProvenanceDepthBudgetExceeded {
            actual: 4,
            limit: 3,
        },
        BudgetVectorError::LatencyBudgetExceeded {
            actual: 501,
            limit: 500,
        },
        BudgetVectorError::CpuBudgetExceeded {
            actual: 251,
            limit: 250,
        },
        BudgetVectorError::TierReserveExceeded {
            tier: ContextTier::P0,
            actual: 3,
            limit: 2,
        },
    ];
    for (observed, expected) in overflows.iter().zip(expected.iter()) {
        assert_eq!(budget.check(observed), Err(expected.clone()));
        assert_eq!(budget.violations(observed), vec![expected.clone()]);
    }

    // Two simultaneous overflows are both reported, not collapsed into one.
    let double = BudgetUsage {
        tokens: 101,
        cpu_micros: 251,
        ..within_every_limit
    };
    assert_eq!(
        budget.violations(&double),
        vec![
            BudgetVectorError::TokenBudgetExceeded {
                actual: 101,
                limit: 100
            },
            BudgetVectorError::CpuBudgetExceeded {
                actual: 251,
                limit: 250
            },
        ]
    );
}

#[test]
fn entry_and_byte_limits_stay_inclusive_and_separate_from_the_vector() {
    // The pre-existing dimensions keep their own behaviour: exactly at limit
    // fits, and their errors are distinct from every vector dimension.
    let exact = ContextBudget {
        max_entries: 2,
        max_rendered_bytes: 3,
    };
    assert_eq!(exact.validate(), Ok(()));
    assert_ne!(
        ContextError::EntryBudgetExceeded {
            actual: 3,
            limit: 2
        },
        ContextError::ByteBudgetExceeded {
            actual: 3,
            limit: 2
        }
    );
}
