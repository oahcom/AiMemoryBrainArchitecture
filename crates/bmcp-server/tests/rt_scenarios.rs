use bmcp_server::{handle_request_body, RequestOutcome, RunningServer, ServerConfig, StartError};
use std::io::{BufRead, BufReader, Read, Write};
use std::net::{TcpListener, TcpStream};
use std::process::{Command, Stdio};
use std::thread;
use std::time::{Duration, Instant};

fn initialize_request(id: u64) -> String {
    format!("{{\"jsonrpc\":\"2.0\",\"id\":{id},\"method\":\"initialize\",\"params\":{{}}}}\n")
}

fn send_request(address: std::net::SocketAddr, request: &str) -> String {
    let mut stream = TcpStream::connect(address).expect("connect to BMCP server");
    stream.write_all(request.as_bytes()).expect("write request");
    stream
        .shutdown(std::net::Shutdown::Write)
        .expect("half-close request stream");

    let mut response = String::new();
    stream.read_to_string(&mut response).expect("read response");
    response
}

#[test]
fn rt_01_readiness_only_after_bind() {
    // Exercise the actual binary, not just RunningServer::start().
    let mut child = Command::new(env!("CARGO_BIN_EXE_bmcp-server"))
        .args(["--bind", "127.0.0.1:0"])
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .expect("spawn bmcp-server binary");

    let stdout = child.stdout.take().expect("capture child stdout");
    let mut reader = BufReader::new(stdout);
    let mut line = String::new();

    let read_result = reader
        .read_line(&mut line)
        .expect("read readiness line from child");

    assert_ne!(read_result, 0, "server exited without readiness output");
    assert!(
        line.starts_with("listening on "),
        "unexpected readiness output: {line:?}"
    );

    let address_text = line
        .trim()
        .strip_prefix("listening on ")
        .expect("readiness line must contain the bound address");

    let address: std::net::SocketAddr = address_text
        .parse()
        .expect("readiness output must contain a socket address");

    assert_ne!(address.port(), 0, "ephemeral bind must use a real port");

    // The address printed by the process must already be connectable.
    TcpStream::connect_timeout(&address, Duration::from_secs(2))
        .expect("printed readiness address must already accept connections");

    let _ = child.kill();
    let _ = child.wait();
}

#[test]
fn rt_01_bind_failure_does_not_print_readiness() {
    let occupied = TcpListener::bind("127.0.0.1:0").expect("reserve an ephemeral port");
    let address = occupied.local_addr().expect("read reserved address");

    let output = Command::new(env!("CARGO_BIN_EXE_bmcp-server"))
        .args(["--bind", &address.to_string()])
        .output()
        .expect("run bmcp-server against occupied address");

    assert!(
        !output.status.success(),
        "binding an occupied address must fail"
    );
    assert!(
        output.stdout.is_empty(),
        "failed bind must not print readiness; stdout was: {:?}",
        String::from_utf8_lossy(&output.stdout)
    );
}

#[test]
fn rt_02_bind_failure_is_actionable() {
    let occupied = TcpListener::bind("127.0.0.1:0").expect("reserve an ephemeral port");
    let address = occupied.local_addr().expect("read reserved address");
    let address_text = address.to_string();

    let result = RunningServer::start(ServerConfig::new(address_text.clone()));

    match result {
        Err(error @ StartError::Bind { .. }) => {
            assert!(
                error.to_string().contains(&address_text),
                "actual bind error should contain {address_text}: {error}"
            );

            if let StartError::Bind { addr, .. } = error {
                assert_eq!(addr, address_text);
            }
        }
        Err(other) => panic!("expected StartError::Bind, got: {other}"),
        Ok(server) => {
            server
                .shutdown()
                .expect("unexpected server should shut down");
            panic!("binding an occupied port should fail");
        }
    }
}

#[test]
fn rt_04_initialize_handshake() {
    let request = br#"{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}"#;

    match handle_request_body(request) {
        RequestOutcome::Responded { body } => {
            assert!(body.contains("\"protocolVersion\":\"2024-11-05\""));
            assert!(body.contains("\"id\":1"));
            // tools/list and tools/call are served, so the capability is claimed.
            assert!(body.contains("\"capabilities\":{\"tools\":{\"listChanged\":false}}"));
        }
        other => panic!("expected initialize response, got: {other:?}"),
    }
}

#[test]
fn rt_04_unknown_method() {
    let request = br#"{"jsonrpc":"2.0","id":2,"method":"no/such/method","params":{}}"#;

    match handle_request_body(request) {
        RequestOutcome::Responded { body } => {
            assert!(body.contains("\"code\":-32601"));
            assert!(body.contains("\"message\":\"Method not found\""));
            assert!(body.contains("\"id\":2"));
        }
        other => panic!("expected MethodNotFound response, got: {other:?}"),
    }
}

#[test]
fn rt_08_concurrency_isolated() {
    const CONCURRENCY: usize = 4;
    const CONNECTIONS: usize = 8;
    const SERVER_READ_TIMEOUT_MS: u64 = 700;
    const SERIAL_FAILURE_THRESHOLD: Duration = Duration::from_millis(3_500);

    let server = RunningServer::start(
        ServerConfig::new("127.0.0.1:0")
            .with_max_concurrency(CONCURRENCY)
            .with_request_deadline_ms(SERVER_READ_TIMEOUT_MS),
    )
    .expect("server should start");

    let address = server.local_addr();

    // Keep every connection open without sending a request. Each accepted
    // server worker must remain occupied in its socket read until the real
    // server-side read timeout expires.
    let started = Instant::now();

    let streams: Vec<TcpStream> = (0..CONNECTIONS)
        .map(|_| TcpStream::connect(address).expect("connect concurrent client"))
        .collect();

    // Read each connection to EOF concurrently. The server closes each
    // connection when its configured socket read timeout expires.
    let readers: Vec<_> = streams
        .into_iter()
        .map(|mut stream| {
            thread::spawn(move || {
                let mut response = Vec::new();
                stream
                    .read_to_end(&mut response)
                    .expect("read until server closes timed-out connection");
                response
            })
        })
        .collect();

    for reader in readers {
        let response = reader.join().expect("reader thread should not panic");
        assert!(
            response.is_empty(),
            "an idle connection should not receive a response"
        );
    }

    let elapsed = started.elapsed();

    assert!(
        elapsed < SERIAL_FAILURE_THRESHOLD,
        "8 connections with a 700ms server read timeout took {elapsed:?}; \
         this is consistent with a concurrency limit collapsed to 1"
    );

    // Also retain the original request/response isolation assertion.
    let workers: Vec<_> = (1..=CONCURRENCY)
        .map(|id| {
            thread::spawn(move || {
                let request = initialize_request(id as u64);
                let response = send_request(address, &request);
                (id, response)
            })
        })
        .collect();

    for worker in workers {
        let (id, response) = worker.join().expect("client thread should not panic");

        assert!(
            response.contains(&format!("\"id\":{id}")),
            "response for id {id} did not contain its own id: {response}"
        );
        assert!(
            response.contains("\"protocolVersion\":\"2024-11-05\""),
            "response for id {id} was not an initialize response: {response}"
        );

        for other_id in 1..=CONCURRENCY {
            if other_id != id {
                assert!(
                    !response.contains(&format!("\"id\":{other_id}")),
                    "response for id {id} was contaminated by id {other_id}: {response}"
                );
            }
        }
    }

    server.shutdown().expect("server should shut down");
}

#[test]
fn rt_09_deadline_yields_unknown() {
    let request = br#"{
        "jsonrpc":"2.0",
        "id":9,
        "method":"initialize",
        "params":{"deadline_probe_ms":5001}
    }"#;

    match handle_request_body(request) {
        RequestOutcome::Unknown { reason } => {
            assert!(reason.contains("deadline"));
        }
        RequestOutcome::Rejected { reason } => {
            panic!("deadline probe must not be rejected: {reason}");
        }
        RequestOutcome::Responded { body } => {
            panic!("deadline probe should be Unknown, got response: {body}");
        }
    }
}

#[test]
fn rt_11_shutdown_releases_port() {
    let first =
        RunningServer::start(ServerConfig::new("127.0.0.1:0")).expect("first server should start");
    let address = first.local_addr();
    first.shutdown().expect("first server should shut down");

    let second = RunningServer::start(ServerConfig::new(address.to_string()))
        .expect("same port should be available after shutdown");

    assert_eq!(second.local_addr().port(), address.port());
    second.shutdown().expect("second server should shut down");
}

#[test]
fn rt_12_idle_connection_survives_until_deadline() {
    let server =
        RunningServer::start(ServerConfig::new("127.0.0.1:0").with_request_deadline_ms(1_000))
            .expect("server should start");

    let mut stream = TcpStream::connect(server.local_addr()).expect("connect to server");

    stream
        .set_read_timeout(Some(Duration::from_secs(3)))
        .expect("set client read timeout");

    let started = Instant::now();
    let mut received = Vec::new();

    stream
        .read_to_end(&mut received)
        .expect("read until server closes idle connection");

    let elapsed = started.elapsed();

    assert!(
        received.is_empty(),
        "idle connection must not receive response bytes: {received:?}"
    );

    assert!(
        elapsed >= Duration::from_millis(800),
        "server closed idle connection too early: {elapsed:?}"
    );

    server.shutdown().expect("server should shut down");
}

#[test]
fn rt_13_fragmented_request_is_served() {
    let server =
        RunningServer::start(ServerConfig::new("127.0.0.1:0").with_request_deadline_ms(2_000))
            .expect("server should start");

    let mut stream = TcpStream::connect(server.local_addr()).expect("connect to server");

    stream
        .set_read_timeout(Some(Duration::from_secs(3)))
        .expect("set client read timeout");

    stream
        .write_all(br#"{"jsonrpc":"2.0","#)
        .expect("write first request fragment");
    stream.flush().expect("flush first request fragment");

    thread::sleep(Duration::from_millis(30));

    stream
        .write_all(b"\"id\":13,\"method\":\"initialize\",\"params\":{}}\n")
        .expect("write second request fragment");
    stream.flush().expect("flush second request fragment");

    let mut response = String::new();
    stream
        .read_to_string(&mut response)
        .expect("read initialize response");

    assert!(
        response.contains(r#""jsonrpc":"2.0""#),
        "response must contain JSON-RPC version: {response}"
    );
    assert!(
        response.contains(r#""id":13"#),
        "response must echo request id 13: {response}"
    );

    server.shutdown().expect("server should shut down");
}
#[test]
fn rt_14_slow_drip_is_closed_at_absolute_deadline() {
    let server =
        RunningServer::start(ServerConfig::new("127.0.0.1:0").with_request_deadline_ms(1_000))
            .expect("server should start");

    let mut stream = TcpStream::connect(server.local_addr()).expect("connect to server");
    stream
        .set_read_timeout(Some(Duration::from_secs(5)))
        .expect("set client read timeout");

    let drip_stream = stream.try_clone().expect("clone client stream");
    let (stop_tx, stop_rx) = std::sync::mpsc::channel();

    let dripper = thread::spawn(move || {
        let mut drip_stream = drip_stream;

        loop {
            if drip_stream.write_all(b"x").is_err() {
                break;
            }

            match stop_rx.recv_timeout(Duration::from_millis(150)) {
                Err(std::sync::mpsc::RecvTimeoutError::Timeout) => {}
                Ok(()) | Err(std::sync::mpsc::RecvTimeoutError::Disconnected) => break,
            }
        }
    });

    let started = Instant::now();
    let mut response = Vec::new();

    stream
        .read_to_end(&mut response)
        .expect("server should close the slow-drip connection before client timeout");

    let elapsed = started.elapsed();

    let _ = stop_tx.send(());
    dripper.join().expect("dripper thread should not panic");

    assert!(
        response.is_empty(),
        "slow-drip connection received response bytes: {response:?}, elapsed: {elapsed:?}"
    );
    assert!(
        (Duration::from_millis(1_000)..=Duration::from_millis(1_800)).contains(&elapsed),
        "slow-drip connection closed outside the expected deadline window: {elapsed:?}"
    );

    server.shutdown().expect("server should shut down");
}

#[test]
fn rt_15_fragmented_request_within_deadline_succeeds() {
    let server =
        RunningServer::start(ServerConfig::new("127.0.0.1:0").with_request_deadline_ms(2_000))
            .expect("server should start");

    let mut stream = TcpStream::connect(server.local_addr()).expect("connect to server");
    stream
        .set_read_timeout(Some(Duration::from_secs(3)))
        .expect("set client read timeout");

    thread::sleep(Duration::from_millis(200));

    stream
        .write_all(br#"{"jsonrpc":"2.0","#)
        .expect("write first request fragment");
    stream.flush().expect("flush first request fragment");

    thread::sleep(Duration::from_millis(200));

    stream
        .write_all(br#""id":15,"method":"initialize","#)
        .expect("write second request fragment");
    stream.flush().expect("flush second request fragment");

    thread::sleep(Duration::from_millis(200));

    stream
        .write_all(b"\"params\":{}}\n")
        .expect("write third request fragment");
    stream.flush().expect("flush third request fragment");

    let mut response = String::new();
    stream
        .read_to_string(&mut response)
        .expect("read initialize response");

    assert!(
        response.contains(r#""jsonrpc":"2.0""#),
        "fragmented request response lacks JSON-RPC version: {response}"
    );
    assert!(
        response.contains(r#""id":15"#),
        "fragmented request response did not echo id 15: {response}"
    );
    assert!(
        response.contains(r#""protocolVersion":"2024-11-05""#),
        "fragmented request did not receive initialize success: {response}"
    );

    server.shutdown().expect("server should shut down");
}

#[test]
fn rt_16_request_after_deadline_is_rejected() {
    let server =
        RunningServer::start(ServerConfig::new("127.0.0.1:0").with_request_deadline_ms(1_000))
            .expect("server should start");

    let mut stream = TcpStream::connect(server.local_addr()).expect("connect to server");
    let started = Instant::now();

    stream
        .set_read_timeout(Some(Duration::from_secs(3)))
        .expect("set client read timeout");

    thread::sleep(Duration::from_millis(1_300));

    let request = initialize_request(16);
    let write_result = stream.write_all(request.as_bytes());

    if write_result.is_ok() {
        let _ = stream.shutdown(std::net::Shutdown::Write);
    }

    let mut response = String::new();
    let read_result = stream.read_to_string(&mut response);
    let elapsed = started.elapsed();

    let read_kind = read_result.as_ref().err().map(|error| error.kind());

    let server_closed = match &read_result {
        Ok(_) => true,
        Err(error)
            if matches!(
                error.kind(),
                std::io::ErrorKind::ConnectionAborted
                    | std::io::ErrorKind::ConnectionReset
                    | std::io::ErrorKind::UnexpectedEof
            ) =>
        {
            true
        }
        Err(error) if error.kind() == std::io::ErrorKind::TimedOut => {
            panic!(
                "server did not close the connection; client read timed out; \
                 elapsed: {elapsed:?}, write_result: {write_result:?}, \
                 read kind: {:?}",
                error.kind()
            );
        }
        Err(error) => {
            panic!(
                "unexpected error while reading late-request connection: {error}; \
                 elapsed: {elapsed:?}, write_result: {write_result:?}, \
                 read kind: {:?}",
                error.kind()
            );
        }
    };

    assert!(
        server_closed,
        "server did not close the connection; elapsed: {elapsed:?}, \
         write_result: {write_result:?}, read kind: {read_kind:?}"
    );
    assert!(
        response.is_empty() || !response.contains(r#""protocolVersion""#),
        "late request received a successful initialize response: {response}, \
         elapsed: {elapsed:?}, write_result: {write_result:?}, \
         read kind: {read_kind:?}"
    );
    assert!(
        elapsed <= Duration::from_millis(1_600),
        "connection remained open beyond deadline plus 600ms: {elapsed:?}, \
         response: {response:?}, write_result: {write_result:?}, \
         read kind: {read_kind:?}"
    );

    server.shutdown().expect("server should shut down");
}

#[test]
fn rt_17_parallel_connections_have_independent_deadlines() {
    let server =
        RunningServer::start(ServerConfig::new("127.0.0.1:0").with_request_deadline_ms(1_000))
            .expect("server should start");

    let address = server.local_addr();

    // Establish all three connections before starting any drip sender.
    let mut clients = Vec::with_capacity(3);
    let mut connect_times = Vec::with_capacity(3);

    for _ in 0..3 {
        let stream = TcpStream::connect(address).expect("connect slow-drip client");
        connect_times.push(Instant::now());
        stream
            .set_read_timeout(Some(Duration::from_secs(5)))
            .expect("set client read timeout");
        clients.push(stream);
    }

    let connect_span = connect_times
        .last()
        .expect("three connection timestamps")
        .duration_since(*connect_times.first().expect("first connection timestamp"));

    assert!(
        connect_span < Duration::from_millis(100),
        "connections were not established close together: span {connect_span:?}"
    );

    let drip_delays = [
        Duration::ZERO,
        Duration::from_millis(400),
        Duration::from_millis(800),
    ];

    let workers: Vec<_> = clients
        .into_iter()
        .zip(connect_times)
        .zip(drip_delays)
        .enumerate()
        .map(|(index, ((mut stream, connected_at), drip_delay))| {
            thread::spawn(move || {
                let drip_stream = stream.try_clone().expect("clone client stream");
                let (stop_tx, stop_rx) = std::sync::mpsc::channel();

                let dripper = thread::spawn(move || {
                    let mut drip_stream = drip_stream;
                    thread::sleep(drip_delay);

                    loop {
                        if drip_stream.write_all(b"x").is_err() {
                            break;
                        }

                        match stop_rx.recv_timeout(Duration::from_millis(150)) {
                            Err(std::sync::mpsc::RecvTimeoutError::Timeout) => {}
                            Ok(()) | Err(std::sync::mpsc::RecvTimeoutError::Disconnected) => {
                                break;
                            }
                        }
                    }
                });

                let mut response = Vec::new();
                stream
                    .read_to_end(&mut response)
                    .expect("server should close slow-drip connection");

                let elapsed = connected_at.elapsed();

                let _ = stop_tx.send(());
                dripper.join().expect("dripper thread should not panic");

                (index + 1, elapsed, response)
            })
        })
        .collect();

    for worker in workers {
        let (index, elapsed, response) = worker.join().expect("client worker should not panic");

        assert!(
            response.is_empty(),
            "slow-drip connection {index} received response bytes: {response:?}, \
             elapsed: {elapsed:?}"
        );
        assert!(
            (Duration::from_millis(950)..=Duration::from_millis(1_600)).contains(&elapsed),
            "slow-drip connection {index} did not close near its own connection deadline: \
             elapsed {elapsed:?}"
        );
    }

    server.shutdown().expect("server should shut down");
}
