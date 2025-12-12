use socket2::{Socket, Domain, Type, Protocol};
use std::io::Write;
use std::net::{TcpStream, SocketAddr};
use std::time::Duration;

#[derive(Debug)]
struct TcpOptions {
    window_scaling: bool,
    congestion_control: bool,
    fast_open: bool,
    nagle: bool,
    keep_alive: bool,
}

impl TcpOptions {
    fn apply(&self, socket: &Socket) {
        // Nagle (true = bật, false = tắt)
        socket.set_nodelay(!self.nagle).unwrap();

        // Keep-Alive
        socket.set_keepalive(self.keep_alive).unwrap();

        // mô phỏng
        if self.window_scaling {
            println!("[CLIENT] Window Scaling ENABLED (simulation)");
        }
        if self.congestion_control {
            println!("[CLIENT] Congestion Control ENABLED (simulation)");
        }
        if self.fast_open {
            println!("[CLIENT] TCP Fast Open ENABLED (simulation)");
        }
    }
}

fn main() {
    let options = TcpOptions {
        window_scaling: true,
        congestion_control: true,
        fast_open: true,
        nagle: true,
        keep_alive: true,
    };

    println!("CLIENT TCP Options: {:?}", options);

    let socket = Socket::new(Domain::IPV4, Type::STREAM, Some(Protocol::TCP)).unwrap();
    options.apply(&socket);

    socket.set_recv_buffer_size(512 * 1024).unwrap();
    socket.set_send_buffer_size(512 * 1024).unwrap();

    let addr: SocketAddr = "127.0.0.1:5000".parse().unwrap();
    socket.connect(&addr.into()).unwrap();

    let mut stream: TcpStream = socket.into();

    // gửi 10 ping
    for i in 1..=10 {
        let msg = format!("Ping {}", i);
        stream.write_all(msg.as_bytes()).unwrap();
        println!("Sent: {}", msg);
        std::thread::sleep(Duration::from_millis(500));
    }
}
