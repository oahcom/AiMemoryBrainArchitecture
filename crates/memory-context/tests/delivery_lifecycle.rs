use memory_context::{
    AckOutcome, ContextError, DeliveryAck, DeliveryAttempt, DeliveryAttemptId, DeliveryId,
    DeliveryLifecycle, DeliveryState,
};

fn delivery(raw: &str) -> DeliveryId {
    DeliveryId::new(raw).unwrap()
}

fn attempt_id(raw: &str) -> DeliveryAttemptId {
    DeliveryAttemptId::new(raw).unwrap()
}

fn first(delivery_id: &DeliveryId, attempt: &str) -> DeliveryAttempt {
    DeliveryAttempt::first(delivery_id.clone(), attempt_id(attempt))
}

fn ack(delivery_id: &DeliveryId, attempt: &str) -> DeliveryAck {
    DeliveryAck::new(delivery_id.clone(), attempt_id(attempt))
}

fn setup(max_attempts: u32, id: &str) -> (DeliveryLifecycle, DeliveryId) {
    let mut lifecycle = DeliveryLifecycle::new(max_attempts).unwrap();
    let id = delivery(id);
    lifecycle.enqueue(id.clone()).unwrap();
    (lifecycle, id)
}

#[test]
fn zero_max_attempts_is_rejected() {
    assert!(DeliveryLifecycle::new(0).is_err());
}

#[test]
fn duplicate_enqueue_is_rejected() {
    let (mut lifecycle, id) = setup(3, "delivery-1");
    assert!(lifecycle.enqueue(id).is_err());
}

#[test]
fn normal_delivery_acknowledgement_path() {
    let (mut lifecycle, id) = setup(3, "delivery-1");

    lifecycle.record_attempt(first(&id, "attempt-1")).unwrap();
    assert_eq!(lifecycle.state(&id), Some(&DeliveryState::Pending));

    lifecycle.mark_delivered(&id).unwrap();

    assert_eq!(lifecycle.state(&id), Some(&DeliveryState::Delivered));

    assert_eq!(
        lifecycle.consume_ack(&ack(&id, "attempt-1")).unwrap(),
        AckOutcome::Accepted
    );

    assert_eq!(lifecycle.state(&id), Some(&DeliveryState::Acknowledged));

    assert!(lifecycle.state(&id).unwrap().is_terminal());
}

#[test]
fn unknown_delivery_ack_is_not_an_error() {
    let mut lifecycle = DeliveryLifecycle::new(3).unwrap();

    let outcome = lifecycle
        .consume_ack(&ack(&delivery("unknown"), "attempt-unknown"))
        .unwrap();

    assert_eq!(outcome, AckOutcome::UnknownDelivery);
}

#[test]
fn duplicate_ack_is_idempotent_and_counted() {
    let (mut lifecycle, id) = setup(3, "delivery-1");

    lifecycle.record_attempt(first(&id, "attempt-1")).unwrap();
    lifecycle.mark_delivered(&id).unwrap();

    assert_eq!(
        lifecycle.consume_ack(&ack(&id, "attempt-1")).unwrap(),
        AckOutcome::Accepted
    );

    assert_eq!(
        lifecycle.consume_ack(&ack(&id, "attempt-1")).unwrap(),
        AckOutcome::Duplicate
    );

    let record = lifecycle.record(&id).unwrap();

    assert_eq!(record.state(), &DeliveryState::Acknowledged);
    assert_eq!(record.ack_count(), 2);
    assert_eq!(record.late_ack_count(), 0);
}

#[test]
fn late_ack_after_supersession_is_recorded() {
    let (mut lifecycle, old) = setup(3, "delivery-old");
    let new = delivery("delivery-new");

    lifecycle.enqueue(new.clone()).unwrap();

    lifecycle
        .record_attempt(first(&old, "attempt-old"))
        .unwrap();
    lifecycle.mark_delivered(&old).unwrap();

    lifecycle
        .record_attempt(first(&new, "attempt-new"))
        .unwrap();
    lifecycle.mark_delivered(&new).unwrap();

    lifecycle.supersede(&old, new.clone()).unwrap();

    assert_eq!(
        lifecycle.consume_ack(&ack(&old, "attempt-old")).unwrap(),
        AckOutcome::Late {
            superseded_by: new.clone()
        }
    );

    let record = lifecycle.record(&old).unwrap();

    assert_eq!(record.state(), &DeliveryState::Superseded);
    assert_eq!(record.late_ack_count(), 1);
    assert_eq!(record.ack_count(), 1);
    assert_eq!(record.superseded_by(), Some(&new));
}

#[test]
fn acknowledged_delivery_cannot_record_another_attempt() {
    let (mut lifecycle, id) = setup(3, "delivery-1");

    lifecycle.record_attempt(first(&id, "attempt-1")).unwrap();
    lifecycle.mark_delivered(&id).unwrap();
    lifecycle.consume_ack(&ack(&id, "attempt-1")).unwrap();

    let retry = DeliveryAttempt::retry(&first(&id, "attempt-1"), attempt_id("attempt-2")).unwrap();

    assert!(lifecycle.record_attempt(retry).is_err());
    assert_eq!(lifecycle.state(&id), Some(&DeliveryState::Acknowledged));
}

#[test]
fn superseded_delivery_cannot_be_marked_delivered() {
    let (mut lifecycle, old) = setup(3, "delivery-old");
    let new = delivery("delivery-new");

    lifecycle.enqueue(new.clone()).unwrap();
    lifecycle.supersede(&old, new).unwrap();

    assert!(lifecycle.mark_delivered(&old).is_err());
    assert_eq!(lifecycle.state(&old), Some(&DeliveryState::Superseded));
}

#[test]
fn retry_exhaustion_abandons_delivery() {
    let (mut lifecycle, id) = setup(2, "delivery-1");

    let first_attempt = first(&id, "attempt-1");
    lifecycle.record_attempt(first_attempt.clone()).unwrap();
    lifecycle.mark_delivered(&id).unwrap();

    // One attempt left: state is still Delivered and a retry is allowed.
    assert_eq!(lifecycle.state(&id), Some(&DeliveryState::Delivered));
    assert!(lifecycle.can_retry(&id));

    let second_attempt = DeliveryAttempt::retry(&first_attempt, attempt_id("attempt-2")).unwrap();
    lifecycle.record_attempt(second_attempt).unwrap();

    // Reaching the limit is the terminal event, not exceeding it.
    assert_eq!(lifecycle.state(&id), Some(&DeliveryState::Abandoned));
    assert!(lifecycle.state(&id).unwrap().is_terminal());
    assert!(!lifecycle.can_retry(&id));
    assert_eq!(lifecycle.ledger().attempt_count(&id), 2);
}

#[test]
fn supersede_success_records_replacement_identity() {
    let (mut lifecycle, old) = setup(3, "delivery-old");
    let new = delivery("delivery-new");

    lifecycle.enqueue(new.clone()).unwrap();
    lifecycle.supersede(&old, new.clone()).unwrap();

    assert_eq!(lifecycle.state(&old), Some(&DeliveryState::Superseded));
    assert_eq!(lifecycle.record(&old).unwrap().superseded_by(), Some(&new));
}

#[test]
fn acknowledged_delivery_cannot_be_superseded() {
    let (mut lifecycle, old) = setup(3, "delivery-old");
    let new = delivery("delivery-new");

    lifecycle.enqueue(new.clone()).unwrap();

    lifecycle.record_attempt(first(&old, "attempt-1")).unwrap();
    lifecycle.mark_delivered(&old).unwrap();
    lifecycle.consume_ack(&ack(&old, "attempt-1")).unwrap();

    assert!(lifecycle.supersede(&old, new).is_err());
    assert_eq!(lifecycle.state(&old), Some(&DeliveryState::Acknowledged));
}

#[test]
fn already_superseded_delivery_cannot_be_superseded_again() {
    let (mut lifecycle, old) = setup(3, "delivery-old");
    let first_replacement = delivery("delivery-new-1");
    let second_replacement = delivery("delivery-new-2");

    lifecycle.enqueue(first_replacement.clone()).unwrap();
    lifecycle.enqueue(second_replacement.clone()).unwrap();

    lifecycle
        .supersede(&old, first_replacement.clone())
        .unwrap();

    assert!(lifecycle.supersede(&old, second_replacement).is_err());

    assert_eq!(
        lifecycle.record(&old).unwrap().superseded_by(),
        Some(&first_replacement)
    );
}

#[test]
fn pending_delivery_cannot_be_marked_delivered_without_attempt() {
    let (mut lifecycle, id) = setup(3, "delivery-1");

    assert!(lifecycle.mark_delivered(&id).is_err());
    assert_eq!(lifecycle.state(&id), Some(&DeliveryState::Pending));
}

#[test]
fn obsolete_attempt_ack_is_counted_as_stale() {
    let (mut lifecycle, id) = setup(3, "delivery-1");

    let first_attempt = first(&id, "attempt-1");
    lifecycle.record_attempt(first_attempt.clone()).unwrap();
    lifecycle.mark_delivered(&id).unwrap();

    let second_attempt = DeliveryAttempt::retry(&first_attempt, attempt_id("attempt-2")).unwrap();

    lifecycle.record_attempt(second_attempt).unwrap();

    assert_eq!(
        lifecycle.consume_ack(&ack(&id, "attempt-1")).unwrap(),
        AckOutcome::StaleAttempt
    );

    let record = lifecycle.record(&id).unwrap();

    assert_eq!(record.late_ack_count(), 1);
    assert_eq!(record.ack_count(), 1);
    assert_eq!(record.state(), &DeliveryState::Delivered);
}

#[test]
fn abandoned_delivery_cannot_transition_back_to_delivered() {
    let (mut lifecycle, id) = setup(1, "delivery-1");

    let first_attempt = first(&id, "attempt-1");
    lifecycle.record_attempt(first_attempt).unwrap();

    assert_eq!(lifecycle.state(&id), Some(&DeliveryState::Abandoned));
    assert!(lifecycle.state(&id).unwrap().is_terminal());
    assert!(!lifecycle.can_retry(&id));
    assert!(lifecycle.mark_delivered(&id).is_err());
}

#[test]
fn abandoned_delivery_rejects_ack_for_current_attempt() {
    let (mut lifecycle, id) = setup(1, "delivery-1");
    let attempt = first(&id, "attempt-1");
    lifecycle.record_attempt(attempt.clone()).unwrap();
    assert_eq!(lifecycle.state(&id), Some(&DeliveryState::Abandoned));

    let ack = DeliveryAck::new(id.clone(), attempt.attempt_id().clone());
    let outcome = lifecycle.consume_ack(&ack);
    assert!(matches!(outcome, Err(ContextError::IneligibleLifecycle)));
    assert_eq!(lifecycle.state(&id), Some(&DeliveryState::Abandoned));
}

#[test]
fn abandoned_delivery_rejects_ack_for_obsolete_attempt() {
    // max_attempts = 2: attempt-1 then attempt-2 lands the delivery in Abandoned.
    let (mut lifecycle, id) = setup(2, "delivery-1");
    let first_attempt = first(&id, "attempt-1");
    lifecycle.record_attempt(first_attempt.clone()).unwrap();
    let second_attempt = DeliveryAttempt::retry(&first_attempt, attempt_id("attempt-2")).unwrap();
    lifecycle.record_attempt(second_attempt).unwrap();
    assert_eq!(lifecycle.state(&id), Some(&DeliveryState::Abandoned));

    let stale_ack = DeliveryAck::new(id.clone(), attempt_id("attempt-1"));
    let outcome = lifecycle.consume_ack(&stale_ack);
    assert!(matches!(outcome, Err(ContextError::IneligibleLifecycle)));
    assert_eq!(lifecycle.state(&id), Some(&DeliveryState::Abandoned));
}

#[test]
fn retry_is_not_allowed_for_unknown_delivery() {
    let lifecycle = DeliveryLifecycle::new(3).unwrap();

    assert!(!lifecycle.can_retry(&delivery("unknown")));
}

#[test]
fn supersede_requires_existing_replacement() {
    let (mut lifecycle, old) = setup(3, "delivery-old");

    assert!(lifecycle.supersede(&old, delivery("missing")).is_err());
    assert_eq!(lifecycle.state(&old), Some(&DeliveryState::Pending));
}
