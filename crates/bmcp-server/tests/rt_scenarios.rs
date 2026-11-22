use bmcp_server::{handle_request_body, RequestOutcome, RunningServer, ServerConfig, StartError};
use std::io::{Read, Write};
use std::net::{TcpListener, TcpStream};
use std::thread;

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
    let server = RunningServer::start(ServerConfig::new("127.0.0.1:0"))
        .expect("server should bind successfully");

    assert_ne!(server.local_addr().port(), 0);

    server.shutdown().expect("server should shut down");
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
    let concurrency = 4;
    let server =
        RunningServer::start(ServerConfig::new("127.0.0.1:0").with_max_concurrency(concurrency))
            .expect("server should start");

    let address = server.local_addr();

    let workers: Vec<_> = (1..=concurrency)
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

        for other_id in 1..=concurrency {
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
