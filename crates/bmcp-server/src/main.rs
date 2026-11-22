use bmcp_server::{RunningServer, ServerConfig};
use std::env;
use std::process;

fn main() {
    if let Err(error) = run() {
        eprintln!("bmcp-server: {error}");
        process::exit(1);
    }
}

fn run() -> Result<(), Box<dyn std::error::Error>> {
    let mut bind = "127.0.0.1:0".to_owned();
    let mut max_concurrency = None;
    let mut request_deadline_ms = None;

    let mut args = env::args().skip(1);

    while let Some(argument) = args.next() {
        match argument.as_str() {
            "--bind" => {
                bind = args.next().ok_or("--bind requires an address")?;
            }
            "--max-concurrency" => {
                let value = args.next().ok_or("--max-concurrency requires an integer")?;
                max_concurrency = Some(value.parse::<usize>()?);
            }
            "--request-deadline-ms" => {
                let value = args
                    .next()
                    .ok_or("--request-deadline-ms requires an integer")?;
                request_deadline_ms = Some(value.parse::<u64>()?);
            }
            "--help" | "-h" => {
                println!(
                    "Usage: bmcp-server [--bind ADDRESS] \
                     [--max-concurrency N] [--request-deadline-ms MS]"
                );
                return Ok(());
            }
            other => {
                return Err(format!("unknown argument: {other}").into());
            }
        }
    }

    let mut config = ServerConfig::new(bind);

    if let Some(value) = max_concurrency {
        config = config.with_max_concurrency(value);
    }

    if let Some(value) = request_deadline_ms {
        config = config.with_request_deadline_ms(value);
    }

    // Do not print readiness until start() has successfully bound the socket
    // and started the accept loop.
    let server = RunningServer::start(config)?;
    println!("listening on {}", server.local_addr());

    // Keep the server alive until the process receives termination.
    // The OS closes the listener and process-owned sockets on process exit.
    loop {
        std::thread::park();
    }
}
