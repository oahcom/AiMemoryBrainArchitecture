use memory_context::{
    AckDisposition, DeliveryAck, DeliveryAttempt, DeliveryAttemptId, DeliveryId, DeliveryLedger,
};

fn delivery(value: &str) -> DeliveryId {
    DeliveryId::new(value).expect("delivery id should be valid")
}

fn attempt_id(value: &str) -> DeliveryAttemptId {
    DeliveryAttemptId::new(value).expect("attempt id should be valid")
}

#[test]
fn attempt_id_rejects_empty_and_whitespace() {
    assert!(DeliveryAttemptId::new("").is_err());
    assert!(DeliveryAttemptId::new("   ").is_err());
}

#[test]
fn retry_increments_attempt_number_and_links_previous() {
    let delivery = delivery("delivery-1");
    let first = DeliveryAttempt::first(delivery.clone(), attempt_id("attempt-1"));
    let second =
        DeliveryAttempt::retry(&first, attempt_id("attempt-2")).expect("retry should succeed");
    let third = DeliveryAttempt::retry(&second, attempt_id("attempt-3")).unwrap();

    assert_eq!(first.attempt_number(), 1);
    assert_eq!(second.attempt_number(), 2);
    assert_eq!(third.attempt_number(), 3);
    assert_eq!(second.previous_attempt_id(), Some(first.attempt_id()));
    assert_eq!(third.previous_attempt_id(), Some(second.attempt_id()));
    assert_eq!(first.delivery_id(), second.delivery_id());
    assert_eq!(second.delivery_id(), third.delivery_id());
}

#[test]
fn ledger_tracks_multiple_attempts_per_delivery() {
    let delivery = delivery("delivery-1");
    let first = DeliveryAttempt::first(delivery.clone(), attempt_id("attempt-1"));
    let second = DeliveryAttempt::retry(&first, attempt_id("attempt-2")).unwrap();
    let third = DeliveryAttempt::retry(&second, attempt_id("attempt-3")).unwrap();

    let mut ledger = DeliveryLedger::new();

    ledger.record(first).unwrap();
    ledger.record(second).unwrap();
    ledger.record(third).unwrap();

    assert_eq!(ledger.attempt_count(&delivery), 3);
    assert_eq!(
        ledger.current_attempt(&delivery).unwrap().attempt_id(),
        &attempt_id("attempt-3")
    );
}

#[test]
fn ledger_rejects_duplicate_attempt_id() {
    let delivery = delivery("delivery-1");
    let first = DeliveryAttempt::first(delivery.clone(), attempt_id("attempt-1"));
    let duplicate = DeliveryAttempt::first(delivery, attempt_id("attempt-1"));

    let mut ledger = DeliveryLedger::new();

    ledger.record(first).unwrap();
    assert_eq!(
        ledger.record(duplicate),
        Err(memory_context::ContextError::DuplicateOperationId)
    );
}

#[test]
fn ledger_rejects_forked_attempt_chain() {
    let delivery = delivery("delivery-1");
    let first = DeliveryAttempt::first(delivery.clone(), attempt_id("attempt-1"));
    let second = DeliveryAttempt::retry(&first, attempt_id("attempt-2")).unwrap();
    let fork = DeliveryAttempt::retry(&first, attempt_id("attempt-2-fork")).unwrap();

    let mut ledger = DeliveryLedger::new();

    ledger.record(first).unwrap();
    ledger.record(second).unwrap();

    assert_eq!(
        ledger.record(fork),
        Err(memory_context::ContextError::ContextMismatch)
    );
}

#[test]
fn ack_for_current_attempt_is_current() {
    let delivery = delivery("delivery-1");
    let first = DeliveryAttempt::first(delivery.clone(), attempt_id("attempt-1"));

    let mut ledger = DeliveryLedger::new();
    ledger.record(first).unwrap();

    let ack = DeliveryAck::new(delivery, attempt_id("attempt-1"));

    assert_eq!(ledger.classify_ack(&ack), AckDisposition::Current);
}

#[test]
fn ack_for_superseded_attempt_is_late() {
    let delivery = delivery("delivery-1");
    let first = DeliveryAttempt::first(delivery.clone(), attempt_id("attempt-1"));
    let second = DeliveryAttempt::retry(&first, attempt_id("attempt-2")).unwrap();

    let mut ledger = DeliveryLedger::new();
    ledger.record(first).unwrap();
    ledger.record(second).unwrap();

    let ack = DeliveryAck::new(delivery, attempt_id("attempt-1"));

    assert_eq!(ledger.classify_ack(&ack), AckDisposition::Late);
}

#[test]
fn ack_for_unknown_delivery_is_unknown() {
    let ledger = DeliveryLedger::new();
    let ack = DeliveryAck::new(delivery("unknown-delivery"), attempt_id("attempt-1"));

    assert_eq!(ledger.classify_ack(&ack), AckDisposition::UnknownDelivery);
}

#[test]
fn ack_targets_delivery_not_attempt() {
    let delivery = delivery("delivery-1");
    let first = DeliveryAttempt::first(delivery.clone(), attempt_id("attempt-1"));
    let second = DeliveryAttempt::retry(&first, attempt_id("attempt-2")).unwrap();

    let mut ledger = DeliveryLedger::new();
    ledger.record(first).unwrap();
    ledger.record(second).unwrap();

    let first_ack = DeliveryAck::new(delivery.clone(), attempt_id("attempt-1"));
    let second_ack = DeliveryAck::new(delivery.clone(), attempt_id("attempt-2"));

    assert_eq!(first_ack.delivery_id(), second_ack.delivery_id());
    assert_ne!(
        first_ack.acknowledged_attempt_id(),
        second_ack.acknowledged_attempt_id()
    );
}
