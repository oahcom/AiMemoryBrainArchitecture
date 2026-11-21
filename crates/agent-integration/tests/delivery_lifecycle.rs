//! Executable checks for the §5 delivery lifecycle and §6 Applied attestation.

use agent_integration::{
    AdapterError, AppliedAttestation, DeliveryRecord, DeliveryState, DeliveryState::*,
};

fn attestation(version: u64) -> AppliedAttestation {
    AppliedAttestation {
        context_id: "ctx-1".into(),
        context_session_id: "sess-1".into(),
        target_context_version: version,
        adapter_id: "adapter-1".into(),
        adapter_instance_id: "adapter-instance-1".into(),
        agent_instance_id: "agent-1".into(),
        boundary_id: "boundary-1".into(),
        inference_request_id: Some("req-1".into()),
        applied_at: "2026-11-21T00:00:00Z".into(),
    }
}

/// Walk a fresh record to `state` through legal edges only.
fn record_at(state: DeliveryState) -> DeliveryRecord {
    let mut record = DeliveryRecord::new(1);
    record.set_attestation(attestation(1));
    for step in [Received, Accepted] {
        if record.state() == state {
            return record;
        }
        record.transition(step).unwrap();
    }
    if record.state() != state {
        record.transition(state).unwrap(); // Applied / Rejected / Expired / Superseded
    }
    assert_eq!(record.state(), state, "could not reach {state:?}");
    record
}

// ---------------------------------------------------------------- legal paths

#[test]
fn legal_delivered_to_received() {
    let mut record = DeliveryRecord::new(1);
    assert_eq!(record.state(), Delivered);
    assert_eq!(record.transition(Received), Ok(()));
    assert_eq!(record.state(), Received);
}

#[test]
fn legal_received_to_accepted() {
    let mut record = record_at(Received);
    assert_eq!(record.transition(Accepted), Ok(()));
    assert_eq!(record.state(), Accepted);
}

#[test]
fn legal_accepted_to_applied_with_matching_attestation() {
    let mut record = DeliveryRecord::new(7);
    record.transition(Received).unwrap();
    record.transition(Accepted).unwrap();
    record.set_attestation(attestation(7));
    assert_eq!(record.transition(Applied), Ok(()));
    assert_eq!(record.state(), Applied);
    assert_eq!(record.attestation().unwrap().target_context_version, 7);
}

#[test]
fn legal_received_to_rejected() {
    let mut record = record_at(Received);
    assert_eq!(record.transition(Rejected), Ok(()));
    assert_eq!(record.state(), Rejected);
}

#[test]
fn legal_accepted_to_rejected() {
    let mut record = record_at(Accepted);
    assert_eq!(record.transition(Rejected), Ok(()));
    assert_eq!(record.state(), Rejected);
}

#[test]
fn legal_pending_states_expire() {
    for from in [Delivered, Received, Accepted] {
        let mut record = record_at(from);
        assert_eq!(record.transition(Expired), Ok(()), "{from:?} -> Expired");
        assert_eq!(record.state(), Expired);
    }
}

#[test]
fn legal_pending_states_are_superseded() {
    for from in [Delivered, Received, Accepted] {
        let mut record = record_at(from);
        assert_eq!(
            record.transition(Superseded),
            Ok(()),
            "{from:?} -> Superseded"
        );
        assert_eq!(record.state(), Superseded);
    }
}

// -------------------------------------------------------------- illegal paths

#[test]
fn illegal_delivered_to_applied_shortcut() {
    let mut record = DeliveryRecord::new(1);
    record.set_attestation(attestation(1));
    assert_eq!(
        record.transition(Applied),
        Err(AdapterError::IllegalStateTransition {
            from: Delivered,
            to: Applied
        })
    );
    assert_eq!(record.state(), Delivered);
}

#[test]
fn illegal_received_to_applied_shortcut() {
    // §5: "Adapter MUST NOT report Applied merely because it received ... it".
    let mut record = record_at(Received);
    assert_eq!(
        record.transition(Applied),
        Err(AdapterError::IllegalStateTransition {
            from: Received,
            to: Applied
        })
    );
    assert_eq!(record.state(), Received);
}

#[test]
fn received_only_delivery_cannot_report_applied() {
    // Covers received/parsed/queued/cached: none of these is Accepted, so none
    // can reach Applied, even with a perfect attestation present.
    let mut record = DeliveryRecord::new(3);
    record.transition(Received).unwrap();
    record.set_attestation(attestation(3));
    assert!(record.transition(Applied).is_err());
    assert_eq!(record.state(), Received);
    assert_ne!(record.state(), Applied);
}

#[test]
fn illegal_delivered_to_accepted_skips_receipt() {
    let mut record = DeliveryRecord::new(1);
    assert_eq!(
        record.transition(Accepted),
        Err(AdapterError::IllegalStateTransition {
            from: Delivered,
            to: Accepted
        })
    );
    assert_eq!(record.state(), Delivered);
}

#[test]
fn illegal_backwards_transitions() {
    for (from, to) in [
        (Accepted, Received),
        (Accepted, Delivered),
        (Received, Delivered),
    ] {
        let mut record = record_at(from);
        assert_eq!(
            record.transition(to),
            Err(AdapterError::IllegalStateTransition { from, to }),
            "{from:?} -> {to:?}"
        );
        assert_eq!(record.state(), from);
    }
}

#[test]
fn illegal_terminal_states_cannot_transition() {
    let all = [
        Delivered, Received, Accepted, Applied, Rejected, Expired, Superseded,
    ];
    for from in [Applied, Rejected, Expired, Superseded] {
        for to in all {
            let mut record = record_at(Accepted);
            record.transition(from).unwrap(); // Accepted -> any terminal is legal
            assert_eq!(
                record.transition(to),
                Err(AdapterError::IllegalStateTransition { from, to }),
                "terminal {from:?} -> {to:?}"
            );
            assert_eq!(record.state(), from);
        }
    }
}

#[test]
fn can_transition_to_matches_the_transition_guard() {
    let all = [
        Delivered, Received, Accepted, Applied, Rejected, Expired, Superseded,
    ];
    for from in all {
        for to in all {
            let allowed = from.can_transition_to(to);
            let mut record = record_at(from);
            assert_eq!(
                allowed,
                record.transition(to).is_ok(),
                "can_transition_to disagrees with transition() for {from:?} -> {to:?}"
            );
        }
    }
}

// ------------------------------------------------- attestation enforcement

#[test]
fn applied_requires_attestation() {
    let mut record = DeliveryRecord::new(1);
    record.transition(Received).unwrap();
    record.transition(Accepted).unwrap();
    assert_eq!(
        record.transition(Applied),
        Err(AdapterError::AppliedRequiresAttestation)
    );
    assert_eq!(record.state(), Accepted);
}

#[test]
fn applied_rejects_attestation_for_a_different_version() {
    let mut record = DeliveryRecord::new(5);
    record.transition(Received).unwrap();
    record.transition(Accepted).unwrap();
    record.set_attestation(attestation(4));
    assert_eq!(
        record.transition(Applied),
        Err(AdapterError::AppliedVersionMismatch {
            expected: 5,
            received: 4
        })
    );
    assert_eq!(record.state(), Accepted);
}

#[test]
fn applied_rejects_newer_attestation_version() {
    let mut record = DeliveryRecord::new(5);
    record.transition(Received).unwrap();
    record.transition(Accepted).unwrap();
    record.set_attestation(attestation(6));
    assert_eq!(
        record.transition(Applied),
        Err(AdapterError::AppliedVersionMismatch {
            expected: 5,
            received: 6
        })
    );
    assert_eq!(record.state(), Accepted);
}

#[test]
fn attestation_may_omit_inference_request_id() {
    let mut record = DeliveryRecord::new(2);
    record.transition(Received).unwrap();
    record.transition(Accepted).unwrap();
    let mut attestation = attestation(2);
    attestation.inference_request_id = None;
    record.set_attestation(attestation);
    assert_eq!(record.transition(Applied), Ok(()));
}

#[test]
fn terminal_states_are_declared_terminal() {
    for state in [Applied, Rejected, Expired, Superseded] {
        assert!(state.is_terminal(), "{state:?}");
        assert!(!state.can_transition_to(state), "{state:?} self-transition");
    }
    for state in [Delivered, Received, Accepted] {
        assert!(!state.is_terminal(), "{state:?}");
    }
}
