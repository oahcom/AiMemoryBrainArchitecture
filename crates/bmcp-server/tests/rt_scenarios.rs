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
