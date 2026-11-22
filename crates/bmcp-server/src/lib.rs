use std::fmt;
use std::io::{self, Read};
use std::net::{SocketAddr, TcpListener, TcpStream};
use std::sync::atomic::{AtomicBool, AtomicUsize, Ordering};
use std::sync::Arc;
use std::thread::{self, JoinHandle};
use std::time::Duration;

mod response_writer;

pub const DEFAULT_MAX_CONCURRENCY: usize = 4;
pub const DEFAULT_REQUEST_DEADLINE_MS: u64 = 5_000;

const MAX_REQUEST_BYTES: usize = 1024 * 1024;

#[derive(Clone, Debug)]
pub struct ServerConfig {
    pub bind_addr: String,
    pub max_concurrency: usize,
    pub request_deadline_ms: u64,
}

impl ServerConfig {
    pub fn new(bind_addr: impl Into<String>) -> Self {
        Self {
            bind_addr: bind_addr.into(),
            max_concurrency: DEFAULT_MAX_CONCURRENCY,
            request_deadline_ms: DEFAULT_REQUEST_DEADLINE_MS,
        }
    }

    pub fn with_max_concurrency(mut self, n: usize) -> Self {
        self.max_concurrency = n;
        self
    }

    pub fn with_request_deadline_ms(mut self, ms: u64) -> Self {
        self.request_deadline_ms = ms;
        self
    }
}

#[derive(Debug, PartialEq, Eq)]
pub enum RequestOutcome {
    Responded { body: String },
    Unknown { reason: String },
    Rejected { reason: String },
}

#[derive(Debug)]
pub enum StartError {
    Bind { addr: String, source: io::Error },
    Io(io::Error),
}

impl fmt::Display for StartError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Bind { addr, source } => {
                write!(f, "failed to bind BMCP server to {addr}: {source}")
            }
            Self::Io(source) => write!(f, "BMCP server I/O error: {source}"),
        }
    }
}

impl std::error::Error for StartError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            Self::Bind { source, .. } | Self::Io(source) => Some(source),
        }
    }
}

pub struct RunningServer {
    local_addr: SocketAddr,
    shutdown: Arc<AtomicBool>,
    accept_thread: Option<JoinHandle<()>>,
}

impl RunningServer {
    pub fn start(config: ServerConfig) -> Result<Self, StartError> {
        let listener = TcpListener::bind(&config.bind_addr).map_err(|source| StartError::Bind {
            addr: config.bind_addr.clone(),
            source,
        })?;

        let local_addr = listener.local_addr().map_err(StartError::Io)?;
        listener.set_nonblocking(true).map_err(StartError::Io)?;

        let shutdown = Arc::new(AtomicBool::new(false));
        let thread_shutdown = Arc::clone(&shutdown);

        // A zero concurrency limit would otherwise prevent every connection
        // from being accepted. Treat it as a single worker.
        let max_concurrency = config.max_concurrency.max(1);
        let request_deadline_ms = config.request_deadline_ms.max(1);

        let accept_thread = thread::Builder::new()
            .name("bmcp-server-accept".to_owned())
            .spawn(move || {
                accept_loop(
                    listener,
                    thread_shutdown,
                    max_concurrency,
                    request_deadline_ms,
                );
            })
            .map_err(StartError::Io)?;

        // The listener has been bound and the accept loop has been started.
        // Callers may safely use local_addr() after this point.
        Ok(Self {
            local_addr,
            shutdown,
            accept_thread: Some(accept_thread),
        })
    }

    pub fn local_addr(&self) -> SocketAddr {
        self.local_addr
    }

    pub fn shutdown(mut self) -> Result<(), StartError> {
        self.shutdown.store(true, Ordering::Release);

        if let Some(handle) = self.accept_thread.take() {
            handle.join().map_err(|_| {
                StartError::Io(io::Error::other("BMCP server accept thread panicked"))
            })?;
        }

        Ok(())
    }
}

impl Drop for RunningServer {
    fn drop(&mut self) {
        self.shutdown.store(true, Ordering::Release);

        if let Some(handle) = self.accept_thread.take() {
            let _ = handle.join();
        }
    }
}

fn accept_loop(
    listener: TcpListener,
    shutdown: Arc<AtomicBool>,
    max_concurrency: usize,
    request_deadline_ms: u64,
) {
    let active = Arc::new(AtomicUsize::new(0));
    let mut workers: Vec<JoinHandle<()>> = Vec::new();

    while !shutdown.load(Ordering::Acquire) {
        if active.load(Ordering::Acquire) >= max_concurrency {
            thread::sleep(Duration::from_millis(5));
            continue;
        }

        match listener.accept() {
            Ok((stream, _peer_addr)) => {
                if shutdown.load(Ordering::Acquire) {
                    drop(stream);
                    break;
                }

                // Windows accepted sockets inherit the listener's nonblocking
                // mode. The listener must stay nonblocking for this accept
                // loop, but client sockets must be blocking or the configured
                // read/write timeouts below never take effect.
                //
                // ponytail: Linux does not inherit O_NONBLOCK on accept, so
                // this is a no-op there; it is unconditional to keep the two
                // platforms on one code path.
                let stream = match stream.set_nonblocking(false) {
                    Ok(()) => stream,
                    Err(_) => continue,
                };

                active.fetch_add(1, Ordering::AcqRel);

                let worker_active = Arc::clone(&active);
                let worker_deadline_ms = request_deadline_ms;

                match thread::Builder::new()
                    .name("bmcp-server-client".to_owned())
                    .spawn(move || {
                        let _guard = ActiveConnectionGuard(worker_active);
                        handle_connection(stream, worker_deadline_ms);
                    }) {
                    Ok(handle) => workers.push(handle),
                    Err(_) => {
                        active.fetch_sub(1, Ordering::AcqRel);
                    }
                }
            }
            Err(error) if error.kind() == io::ErrorKind::WouldBlock => {
                thread::sleep(Duration::from_millis(5));
            }
            Err(_) => {
                thread::sleep(Duration::from_millis(10));
            }
        }
    }

    // Shutdown drains all accepted connections before the accept thread exits.
    for worker in workers {
        let _ = worker.join();
    }
}

struct ActiveConnectionGuard(Arc<AtomicUsize>);

impl Drop for ActiveConnectionGuard {
    fn drop(&mut self) {
        self.0.fetch_sub(1, Ordering::AcqRel);
    }
}

fn handle_connection(mut stream: TcpStream, request_deadline_ms: u64) {
    let timeout = Duration::from_millis(request_deadline_ms);
    let deadline = match std::time::Instant::now().checked_add(timeout) {
        Some(deadline) => deadline,
        None => return,
    };

    let mut body = Vec::new();
    let mut buffer = [0_u8; 4096];

    loop {
        let now = std::time::Instant::now();
        let remaining = match deadline.checked_duration_since(now) {
            Some(remaining) if !remaining.is_zero() => remaining,
            _ => return,
        };

        if stream.set_read_timeout(Some(remaining)).is_err() {
            return;
        }

        let read_result = stream.read(&mut buffer);

        // A socket read timeout does not guarantee that read returns before
        // the absolute deadline: the thread may be descheduled after data
        // becomes available. Recheck here so a complete buffered request
        // cannot be dispatched after the connection deadline.
        //
        // This is a real race, not defensive filler, but it has no stable
        // black-box trigger: it needs the thread to be descheduled between
        // set_read_timeout and read. Verified by mutation that no test covers
        // it; documented rather than papered over with a flaky sleep test.
        if std::time::Instant::now() >= deadline {
            return;
        }

        match read_result {
            Ok(0) => break,
            Ok(count) => {
                if body.len().saturating_add(count) > MAX_REQUEST_BYTES {
                    return;
                }

                body.extend_from_slice(&buffer[..count]);

                if body.contains(&b'\n') {
                    break;
                }
            }
            Err(error) if error.kind() == io::ErrorKind::Interrupted => continue,
            Err(error)
                if error.kind() == io::ErrorKind::WouldBlock
                    || error.kind() == io::ErrorKind::TimedOut =>
            {
                return;
            }
            Err(_) => return,
        }
    }

    if let Some(newline) = body.iter().position(|byte| *byte == b'\n') {
        body.truncate(newline);
    }

    let outcome = handle_request_body_with_deadline(&body, request_deadline_ms);

    if let RequestOutcome::Responded { body } = outcome {
        // Response writing uses the same absolute connection deadline as
        // accept/read and request processing. Every underlying write and
        // flush recomputes its remaining budget inside the write helper.
        let _ = response_writer::write_response_until(
            &mut stream,
            body.as_bytes(),
            deadline,
            std::time::Instant::now,
        );
    }
}

/// Handles a single JSON-RPC request using the default request deadline.
pub fn handle_request_body(body: &[u8]) -> RequestOutcome {
    handle_request_body_with_deadline(body, DEFAULT_REQUEST_DEADLINE_MS)
}

fn handle_request_body_with_deadline(body: &[u8], request_deadline_ms: u64) -> RequestOutcome {
    let request = match parse_request(body) {
        Ok(request) => request,
        Err(reason) => return RequestOutcome::Rejected { reason },
    };

    let method = match request.method {
        Some(method) => method,
        None => {
            return RequestOutcome::Rejected {
                reason: "JSON-RPC request is missing a string method".to_owned(),
            };
        }
    };

    if let Some(probe_ms) = request.deadline_probe_ms {
        if probe_ms > request_deadline_ms {
            return RequestOutcome::Unknown {
                reason: format!(
                    "request deadline probe ({probe_ms} ms) exceeds configured deadline ({request_deadline_ms} ms)"
                ),
            };
        }
    }

    let id = request.id_raw.unwrap_or_else(|| "null".to_owned());

    match method.as_str() {
        "initialize" => RequestOutcome::Responded {
            body: format!(
                "{{\"jsonrpc\":\"2.0\",\"id\":{id},\"result\":{{\"protocolVersion\":\"2024-11-05\",\"capabilities\":{{\"tools\":{{\"listChanged\":false}}}},\"serverInfo\":{{\"name\":\"bmcp-server\",\"version\":\"0.1.0\"}}}}}}"
            ),
        },
        "tools/list" => RequestOutcome::Responded {
            body: format!(
                "{{\"jsonrpc\":\"2.0\",\"id\":{id},\"result\":{{\"tools\":[{}]}}}}",
                tools_catalog()
            ),
        },
        "tools/call" => handle_tool_call(&id, request.params_range.map(|(s, e)| &body[s..e])),
        _ => RequestOutcome::Responded {
            body: format!(
                "{{\"jsonrpc\":\"2.0\",\"id\":{id},\"error\":{{\"code\":-32601,\"message\":\"Method not found\"}}}}"
            ),
        },
    }
}

const VALIDATE_TOOL: &str = "validate_applied_delivery_evidence";
const DIGEST_TOOL: &str = "digest_applied_delivery_evidence";

const EVIDENCE_INPUT_SCHEMA: &str =
    r#"{"type":"object","properties":{"evidence":{"type":"object"}},"required":["evidence"]}"#;

fn tools_catalog() -> String {
    format!(
        concat!(
            r#"{{"name":"{}","description":"Parse and validate an AppliedDeliveryEvidence record; returns validity and its p0 digest.","inputSchema":{}}}"#,
            ",{{\"name\":\"{}\",\"description\":\"Compute the p0 digest of a valid AppliedDeliveryEvidence record.\",\"inputSchema\":{}}}"
        ),
        VALIDATE_TOOL, EVIDENCE_INPUT_SCHEMA, DIGEST_TOOL, EVIDENCE_INPUT_SCHEMA
    )
}

fn handle_tool_call(id: &str, params: Option<&[u8]>) -> RequestOutcome {
    let params = match params {
        Some(params) => params,
        None => return invalid_params(id, "tools/call requires params"),
    };

    let name = match object_value(params, "name").and_then(json_string) {
        Some(name) => name,
        None => return invalid_params(id, "tools/call requires a string name"),
    };

    // Preserve the raw evidence bytes so parse_and_validate can reject
    // duplicate keys rather than silently accepting a reconstructed object.
    let evidence =
        object_value(params, "arguments").and_then(|arguments| object_value(arguments, "evidence"));

    let evidence = match evidence {
        Some(evidence) => evidence,
        None => return invalid_params(id, "tools/call requires arguments.evidence"),
    };

    match name.as_str() {
        VALIDATE_TOOL => match bmcp_protocol::parse_and_validate(evidence) {
            Ok(parsed) => match bmcp_protocol::digest::p0_digest(&parsed) {
                Ok(digest) => tool_result(
                    id,
                    &format!("{{\"valid\":true,\"digest\":\"{digest}\"}}"),
                    false,
                ),
                Err(error) => invalid_evidence_result(id, &error, false),
            },
            Err(error) => invalid_evidence_result(id, &error, false),
        },
        DIGEST_TOOL => match bmcp_protocol::parse_and_validate(evidence) {
            Ok(parsed) => match bmcp_protocol::digest::p0_digest(&parsed) {
                Ok(digest) => tool_result(id, &format!("{{\"digest\":\"{digest}\"}}"), false),
                Err(error) => invalid_evidence_result(id, &error, true),
            },
            Err(error) => invalid_evidence_result(id, &error, true),
        },
        other => invalid_params(id, &format!("unknown tool: {other}")),
    }
}

fn invalid_evidence_result(
    id: &str,
    error: &bmcp_protocol::validate::EvidenceError,
    is_error: bool,
) -> RequestOutcome {
    let description = describe(error);
    let payload = format!(
        "{{\"valid\":false,\"error\":\"{}\"}}",
        json_escape(&description)
    );

    // tool_result performs the separate outer-envelope escaping for the text
    // content block. The description above is escaped only for the inner JSON.
    tool_result(id, &payload, is_error)
}

fn tool_result(id: &str, text: &str, is_error: bool) -> RequestOutcome {
    RequestOutcome::Responded {
        body: format!(
            "{{\"jsonrpc\":\"2.0\",\"id\":{id},\"result\":{{\"content\":[{{\"type\":\"text\",\"text\":\"{}\"}}],\"isError\":{is_error}}}}}",
            json_escape(text)
        ),
    }
}

fn invalid_params(id: &str, message: &str) -> RequestOutcome {
    RequestOutcome::Responded {
        body: format!(
            "{{\"jsonrpc\":\"2.0\",\"id\":{id},\"error\":{{\"code\":-32602,\"message\":\"{}\"}}}}",
            json_escape(message)
        ),
    }
}

/// Returns the raw byte slice of `key`'s value inside a JSON object.
fn object_value<'a>(object: &'a [u8], key: &str) -> Option<&'a [u8]> {
    let mut parser = JsonParser::new(object);
    parser.skip_whitespace();

    if parser.peek() != Some(b'{') {
        return None;
    }

    parser.position += 1;
    parser.skip_whitespace();

    if parser.peek() == Some(b'}') {
        return None;
    }

    loop {
        parser.skip_whitespace();
        let current = parser.parse_string().ok()?;
        parser.skip_whitespace();
        parser.expect(b':').ok()?;
        parser.skip_whitespace();

        let start = parser.position;
        parser.skip_value().ok()?;
        let end = parser.position;

        if current == key {
            return Some(&object[start..end]);
        }

        parser.skip_whitespace();

        match parser.peek() {
            Some(b',') => parser.position += 1,
            _ => return None,
        }
    }
}

/// Decodes a raw JSON string slice into a `String`.
fn json_string(raw: &[u8]) -> Option<String> {
    let mut parser = JsonParser::new(raw);
    parser.parse_string().ok()
}

fn json_escape(value: &str) -> String {
    let mut output = String::with_capacity(value.len());

    for character in value.chars() {
        match character {
            '"' => output.push_str("\\\""),
            '\\' => output.push_str("\\\\"),
            '\n' => output.push_str("\\n"),
            '\r' => output.push_str("\\r"),
            '\t' => output.push_str("\\t"),
            c if (c as u32) < 0x20 => {
                use std::fmt::Write;
                let _ = write!(output, "\\u{:04x}", c as u32);
            }
            c => output.push(c),
        }
    }

    output
}

struct ParsedRequest {
    id_raw: Option<String>,
    method: Option<String>,
    deadline_probe_ms: Option<u64>,
    /// Byte range of the raw `params` value inside the request body.
    ///
    /// `tools/call` hands the `evidence` sub-slice straight to
    /// `parse_and_validate`, so duplicate-key rejection still works; rebuilding
    /// the object through a `Value` would silently drop duplicates.
    params_range: Option<(usize, usize)>,
}

fn parse_request(body: &[u8]) -> Result<ParsedRequest, String> {
    let mut parser = JsonParser::new(body);
    parser.skip_whitespace();

    if parser.peek() != Some(b'{') {
        return Err("JSON-RPC request must be a JSON object".to_owned());
    }

    parser.position += 1;

    let mut request = ParsedRequest {
        id_raw: None,
        method: None,
        deadline_probe_ms: None,
        params_range: None,
    };

    parser.skip_whitespace();

    if parser.peek() == Some(b'}') {
        parser.position += 1;
    } else {
        loop {
            parser.skip_whitespace();
            let key = parser.parse_string()?;
            parser.skip_whitespace();
            parser.expect(b':')?;
            parser.skip_whitespace();

            let value_start = parser.position;

            match key.as_str() {
                "id" => {
                    parser.skip_value()?;
                    let value_end = parser.position;
                    let raw = std::str::from_utf8(&body[value_start..value_end])
                        .map_err(|_| "JSON-RPC id is not valid UTF-8".to_owned())?;
                    request.id_raw = Some(raw.to_owned());
                }
                "method" => {
                    request.method = Some(parser.parse_string()?);
                }
                "params" => {
                    parser.skip_value()?;
                    let value_end = parser.position;
                    request.deadline_probe_ms =
                        parse_deadline_probe(&body[value_start..value_end])?;
                    request.params_range = Some((value_start, value_end));
                }
                _ => parser.skip_value()?,
            }

            parser.skip_whitespace();

            match parser.peek() {
                Some(b',') => {
                    parser.position += 1;
                }
                Some(b'}') => {
                    parser.position += 1;
                    break;
                }
                _ => {
                    return Err("expected ',' or '}' in JSON object".to_owned());
                }
            }
        }
    }

    parser.skip_whitespace();

    if parser.position != body.len() {
        return Err("unexpected trailing bytes after JSON-RPC request".to_owned());
    }

    Ok(request)
}

fn parse_deadline_probe(params: &[u8]) -> Result<Option<u64>, String> {
    let mut parser = JsonParser::new(params);
    parser.skip_whitespace();

    if parser.peek() != Some(b'{') {
        return Ok(None);
    }

    parser.position += 1;
    parser.skip_whitespace();

    if parser.peek() == Some(b'}') {
        parser.position += 1;
        parser.skip_whitespace();

        if parser.position != params.len() {
            return Err("invalid trailing data in params".to_owned());
        }

        return Ok(None);
    }

    let mut result = None;

    loop {
        parser.skip_whitespace();
        let key = parser.parse_string()?;
        parser.skip_whitespace();
        parser.expect(b':')?;
        parser.skip_whitespace();

        if key == "deadline_probe_ms" {
            let number = parser.parse_number()?;
            result = number.parse::<u64>().ok();
        } else {
            parser.skip_value()?;
        }

        parser.skip_whitespace();

        match parser.peek() {
            Some(b',') => parser.position += 1,
            Some(b'}') => {
                parser.position += 1;
                break;
            }
            _ => return Err("expected ',' or '}' in params object".to_owned()),
        }
    }

    parser.skip_whitespace();

    if parser.position != params.len() {
        return Err("invalid trailing data in params".to_owned());
    }

    Ok(result)
}

struct JsonParser<'a> {
    bytes: &'a [u8],
    position: usize,
}

impl<'a> JsonParser<'a> {
    fn new(bytes: &'a [u8]) -> Self {
        Self { bytes, position: 0 }
    }

    fn peek(&self) -> Option<u8> {
        self.bytes.get(self.position).copied()
    }

    fn skip_whitespace(&mut self) {
        while matches!(self.peek(), Some(b' ' | b'\n' | b'\r' | b'\t')) {
            self.position += 1;
        }
    }

    fn expect(&mut self, expected: u8) -> Result<(), String> {
        match self.peek() {
            Some(actual) if actual == expected => {
                self.position += 1;
                Ok(())
            }
            _ => Err(format!(
                "expected '{}' at byte {}",
                expected as char, self.position
            )),
        }
    }

    fn parse_string(&mut self) -> Result<String, String> {
        self.expect(b'"')?;
        let mut output = String::new();

        loop {
            let byte = self
                .peek()
                .ok_or_else(|| "unterminated JSON string".to_owned())?;

            match byte {
                b'"' => {
                    self.position += 1;
                    return Ok(output);
                }
                b'\\' => {
                    self.position += 1;
                    let escaped = self
                        .peek()
                        .ok_or_else(|| "unterminated JSON escape".to_owned())?;
                    self.position += 1;

                    match escaped {
                        b'"' => output.push('"'),
                        b'\\' => output.push('\\'),
                        b'/' => output.push('/'),
                        b'b' => output.push('\u{0008}'),
                        b'f' => output.push('\u{000c}'),
                        b'n' => output.push('\n'),
                        b'r' => output.push('\r'),
                        b't' => output.push('\t'),
                        b'u' => {
                            let first = self.parse_hex4()?;

                            let codepoint = if (0xD800..=0xDBFF).contains(&first) {
                                if self.peek() != Some(b'\\')
                                    || self.bytes.get(self.position + 1) != Some(&b'u')
                                {
                                    return Err(
                                        "high surrogate is missing a low surrogate".to_owned()
                                    );
                                }

                                self.position += 2;
                                let second = self.parse_hex4()?;

                                if !(0xDC00..=0xDFFF).contains(&second) {
                                    return Err("invalid low surrogate".to_owned());
                                }

                                0x10000
                                    + (((first as u32 - 0xD800) << 10) | (second as u32 - 0xDC00))
                            } else if (0xDC00..=0xDFFF).contains(&first) {
                                return Err("unexpected low surrogate".to_owned());
                            } else {
                                first as u32
                            };

                            let character = char::from_u32(codepoint)
                                .ok_or_else(|| "invalid Unicode escape".to_owned())?;
                            output.push(character);
                        }
                        _ => return Err("invalid JSON string escape".to_owned()),
                    }
                }
                0x00..=0x1f => {
                    return Err("unescaped control character in JSON string".to_owned());
                }
                _ => {
                    let remaining = std::str::from_utf8(&self.bytes[self.position..])
                        .map_err(|_| "invalid UTF-8 in JSON string".to_owned())?;
                    let character = remaining
                        .chars()
                        .next()
                        .ok_or_else(|| "invalid UTF-8 in JSON string".to_owned())?;
                    self.position += character.len_utf8();
                    output.push(character);
                }
            }
        }
    }

    fn parse_hex4(&mut self) -> Result<u16, String> {
        let mut value = 0_u16;

        for _ in 0..4 {
            let digit = self
                .peek()
                .ok_or_else(|| "incomplete Unicode escape".to_owned())?;

            let nibble = match digit {
                b'0'..=b'9' => digit - b'0',
                b'a'..=b'f' => digit - b'a' + 10,
                b'A'..=b'F' => digit - b'A' + 10,
                _ => return Err("invalid hexadecimal digit in Unicode escape".to_owned()),
            };

            value = (value << 4) | nibble as u16;
            self.position += 1;
        }

        Ok(value)
    }

    fn parse_number(&mut self) -> Result<String, String> {
        let start = self.position;

        if self.peek() == Some(b'-') {
            self.position += 1;
        }

        match self.peek() {
            Some(b'0') => self.position += 1,
            Some(b'1'..=b'9') => {
                self.position += 1;
                while matches!(self.peek(), Some(b'0'..=b'9')) {
                    self.position += 1;
                }
            }
            _ => return Err("invalid JSON number".to_owned()),
        }

        if self.peek() == Some(b'.') {
            self.position += 1;

            if !matches!(self.peek(), Some(b'0'..=b'9')) {
                return Err("invalid fraction in JSON number".to_owned());
            }

            while matches!(self.peek(), Some(b'0'..=b'9')) {
                self.position += 1;
            }
        }

        if matches!(self.peek(), Some(b'e' | b'E')) {
            self.position += 1;

            if matches!(self.peek(), Some(b'+' | b'-')) {
                self.position += 1;
            }

            if !matches!(self.peek(), Some(b'0'..=b'9')) {
                return Err("invalid exponent in JSON number".to_owned());
            }

            while matches!(self.peek(), Some(b'0'..=b'9')) {
                self.position += 1;
            }
        }

        let raw = std::str::from_utf8(&self.bytes[start..self.position])
            .map_err(|_| "invalid UTF-8 in JSON number".to_owned())?;

        Ok(raw.to_owned())
    }

    fn skip_value(&mut self) -> Result<(), String> {
        self.skip_whitespace();

        match self.peek() {
            Some(b'"') => {
                self.parse_string()?;
                Ok(())
            }
            Some(b'{') => {
                self.position += 1;
                self.skip_whitespace();

                if self.peek() == Some(b'}') {
                    self.position += 1;
                    return Ok(());
                }

                loop {
                    self.skip_whitespace();
                    self.parse_string()?;
                    self.skip_whitespace();
                    self.expect(b':')?;
                    self.skip_value()?;
                    self.skip_whitespace();

                    match self.peek() {
                        Some(b',') => self.position += 1,
                        Some(b'}') => {
                            self.position += 1;
                            return Ok(());
                        }
                        _ => {
                            return Err("expected ',' or '}' while parsing JSON object".to_owned());
                        }
                    }
                }
            }
            Some(b'[') => {
                self.position += 1;
                self.skip_whitespace();

                if self.peek() == Some(b']') {
                    self.position += 1;
                    return Ok(());
                }

                loop {
                    self.skip_value()?;
                    self.skip_whitespace();

                    match self.peek() {
                        Some(b',') => self.position += 1,
                        Some(b']') => {
                            self.position += 1;
                            return Ok(());
                        }
                        _ => {
                            return Err("expected ',' or ']' while parsing JSON array".to_owned());
                        }
                    }
                }
            }
            Some(b'-' | b'0'..=b'9') => {
                self.parse_number()?;
                Ok(())
            }
            Some(b't') => self.parse_literal(b"true"),
            Some(b'f') => self.parse_literal(b"false"),
            Some(b'n') => self.parse_literal(b"null"),
            _ => Err(format!("invalid JSON value at byte {}", self.position)),
        }
    }

    fn parse_literal(&mut self, literal: &[u8]) -> Result<(), String> {
        let end = self.position.saturating_add(literal.len());

        if self.bytes.get(self.position..end) == Some(literal) {
            self.position = end;
            Ok(())
        } else {
            Err(format!("invalid JSON literal at byte {}", self.position))
        }
    }
}

// EvidenceError's Display/Error implementations are intentionally not assumed.
fn describe(error: &bmcp_protocol::validate::EvidenceError) -> String {
    format!("{error:?}")
}
