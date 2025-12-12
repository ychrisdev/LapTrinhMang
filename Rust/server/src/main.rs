use socket2::{Socket, Domain, Type, Protocol};
use std::net::{TcpListener, SocketAddr};
use std::io::Read;

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

        // Các chế độ mô phỏng
        if self.window_scaling {
            println!("[SERVER] Window Scaling ENABLED (simulation)");
        }
        if self.congestion_control {
            println!("[SERVER] Congestion Control ENABLED (simulation)");
        }
        if self.fast_open {
            println!("[SERVER] TCP Fast Open ENABLED (simulation)");
        }
    }
}

fn main() {
    let options = TcpOptions {
        window_scaling: true,
        congestion_control: true,
        fast_open: false,
        nagle: false,
        keep_alive: true,
    };

    println!("SERVER TCP Options: {:?}", options);

    let socket = Socket::new(Domain::IPV4, Type::STREAM, Some(Protocol::TCP)).unwrap();

    // áp dụng các tuỳ chọn
    options.apply(&socket);

    socket.set_recv_buffer_size(1024 * 1024).unwrap();
    socket.set_send_buffer_size(1024 * 1024).unwrap();

    let addr: SocketAddr = "0.0.0.0:5000".parse().unwrap();
    socket.bind(&addr.into()).unwrap();
    socket.listen(128).unwrap();

    let listener: TcpListener = socket.into();
    let (mut stream, addr) = listener.accept().unwrap();
    println!("Client connected from {}", addr);

    let mut buf = [0u8; 2048];
    loop {
        match stream.read(&mut buf) {
            Ok(0) => break,
            Ok(n) => println!("Recv: {}", String::from_utf8_lossy(&buf[..n])),
            Err(_) => break,
        }
    }
}
