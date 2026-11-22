use std::io::{self, Write};
use std::net::TcpStream;
use std::time::{Duration, Instant};

pub(super) trait DeadlineWriter: Write {
    fn set_write_timeout(&self, timeout: Option<Duration>) -> io::Result<()>;
}

impl DeadlineWriter for TcpStream {
    fn set_write_timeout(&self, timeout: Option<Duration>) -> io::Result<()> {
        TcpStream::set_write_timeout(self, timeout)
    }
}

fn remaining_until(deadline: Instant, now: Instant) -> io::Result<Duration> {
    match deadline.checked_duration_since(now) {
        Some(remaining) if !remaining.is_zero() => Ok(remaining),
        _ => Err(io::Error::new(
            io::ErrorKind::TimedOut,
            "response write deadline expired",
        )),
    }
}

fn write_all_until<W, F>(
    writer: &mut W,
    bytes: &[u8],
    deadline: Instant,
    now: &mut F,
) -> io::Result<()>
where
    W: DeadlineWriter,
    F: FnMut() -> Instant,
{
    let mut written = 0;

    while written < bytes.len() {
        // Recompute the remaining budget immediately before every
        // underlying write attempt. A partial write consumes this budget.
        let remaining = remaining_until(deadline, now())?;
        writer.set_write_timeout(Some(remaining))?;

        match writer.write(&bytes[written..]) {
            Ok(0) => {
                return Err(io::Error::new(
                    io::ErrorKind::WriteZero,
                    "failed to write the complete response",
                ));
            }
            Ok(count) => written += count,
            Err(error) if error.kind() == io::ErrorKind::Interrupted => continue,
            Err(error) => return Err(error),
        }
    }

    Ok(())
}

pub(super) fn write_response_until<W, F>(
    writer: &mut W,
    body: &[u8],
    deadline: Instant,
    mut now: F,
) -> io::Result<()>
where
    W: DeadlineWriter,
    F: FnMut() -> Instant,
{
    write_all_until(writer, body, deadline, &mut now)?;
    write_all_until(writer, b"\n", deadline, &mut now)?;

    // Flush is also bounded by the same absolute deadline. In particular,
    // do not flush after either body or newline writing has failed.
    let remaining = remaining_until(deadline, now())?;
    writer.set_write_timeout(Some(remaining))?;
    writer.flush()
}

#[cfg(test)]
mod tests {
    use super::{write_response_until, DeadlineWriter};
    use std::cell::{Cell, RefCell};
    use std::io::{self, Write};
    use std::rc::Rc;
    use std::time::{Duration, Instant};

    struct FakeWriter {
        bytes: Vec<u8>,
        max_chunk: usize,
        write_calls: usize,
        fail_on_call: Option<usize>,
        flush_calls: usize,
        timeouts: RefCell<Vec<Duration>>,
        clock: Rc<Cell<Duration>>,
        advance_per_write: Duration,
    }

    impl FakeWriter {
        fn new(
            max_chunk: usize,
            clock: Rc<Cell<Duration>>,
            advance_per_write: Duration,
            fail_on_call: Option<usize>,
        ) -> Self {
            Self {
                bytes: Vec::new(),
                max_chunk: max_chunk.max(1),
                write_calls: 0,
                fail_on_call,
                flush_calls: 0,
                timeouts: RefCell::new(Vec::new()),
                clock,
                advance_per_write,
            }
        }
    }

    impl Write for FakeWriter {
        fn write(&mut self, bytes: &[u8]) -> io::Result<usize> {
            self.write_calls += 1;

            if self.fail_on_call == Some(self.write_calls) {
                return Err(io::Error::other("injected write failure"));
            }

            self.clock
                .set(self.clock.get().saturating_add(self.advance_per_write));

            let count = bytes.len().min(self.max_chunk);
            self.bytes.extend_from_slice(&bytes[..count]);
            Ok(count)
        }

        fn flush(&mut self) -> io::Result<()> {
            self.flush_calls += 1;
            Ok(())
        }
    }

    impl DeadlineWriter for FakeWriter {
        fn set_write_timeout(&self, timeout: Option<Duration>) -> io::Result<()> {
            if let Some(timeout) = timeout {
                self.timeouts.borrow_mut().push(timeout);
            }
            Ok(())
        }
    }

    fn fake_now(start: Instant, clock: Rc<Cell<Duration>>) -> impl FnMut() -> Instant {
        move || {
            start
                .checked_add(clock.get())
                .expect("fake clock duration should fit in Instant")
        }
    }

    #[test]
    fn cumulative_budget_exhaustion_stops_before_another_write_or_flush() {
        let start = Instant::now();
        let deadline = start
            .checked_add(Duration::from_millis(10))
            .expect("test deadline should fit in Instant");

        let clock = Rc::new(Cell::new(Duration::ZERO));
        let mut writer = FakeWriter::new(2, Rc::clone(&clock), Duration::from_millis(6), None);

        let result = write_response_until(
            &mut writer,
            b"abcdef",
            deadline,
            fake_now(start, Rc::clone(&clock)),
        );

        assert_eq!(
            result
                .expect_err("cumulative write budget must expire")
                .kind(),
            io::ErrorKind::TimedOut
        );

        // Two partial writes consume 6ms each. The third attempt is
        // rejected before calling the writer because the 10ms deadline
        // has already expired.
        assert_eq!(writer.bytes, b"abcd");
        assert_eq!(writer.write_calls, 2);
        assert_eq!(writer.flush_calls, 0);

        // The timeout must be recalculated: 10ms for the first attempt,
        // then 4ms for the second. A stale-timeout implementation fails.
        assert_eq!(
            *writer.timeouts.borrow(),
            vec![Duration::from_millis(10), Duration::from_millis(4)]
        );

        // Neither the rest of the body nor the response newline was written.
        assert!(!writer.bytes.contains(&b'\n'));
    }

    #[test]
    fn write_failure_stops_without_further_writes_or_flush() {
        let start = Instant::now();
        let deadline = start
            .checked_add(Duration::from_secs(1))
            .expect("test deadline should fit in Instant");

        let clock = Rc::new(Cell::new(Duration::ZERO));
        let mut writer = FakeWriter::new(2, Rc::clone(&clock), Duration::ZERO, Some(2));

        let result = write_response_until(
            &mut writer,
            b"abcdef",
            deadline,
            fake_now(start, Rc::clone(&clock)),
        );

        assert_eq!(
            result
                .expect_err("injected write failure must be returned")
                .to_string(),
            "injected write failure"
        );
        assert_eq!(writer.write_calls, 2);
        assert_eq!(writer.bytes, b"ab");
        assert_eq!(writer.flush_calls, 0);
        assert!(!writer.bytes.contains(&b'\n'));
    }

    #[test]
    fn normal_path_writes_body_newline_and_flushes() {
        let start = Instant::now();
        let deadline = start
            .checked_add(Duration::from_secs(1))
            .expect("test deadline should fit in Instant");

        let clock = Rc::new(Cell::new(Duration::ZERO));
        let mut writer = FakeWriter::new(1, Rc::clone(&clock), Duration::ZERO, None);

        write_response_until(
            &mut writer,
            b"ok",
            deadline,
            fake_now(start, Rc::clone(&clock)),
        )
        .expect("normal response write should succeed");

        assert_eq!(writer.bytes, b"ok\n");
        assert_eq!(writer.write_calls, 3);
        assert_eq!(writer.flush_calls, 1);

        // One timeout update per underlying write, plus one for flush.
        assert_eq!(writer.timeouts.borrow().len(), 4);
    }
}
