package main

import (
	"fmt"
	"net"
	"time"
)

func main() {
	time.Sleep(1 * time.Second) // đợi server bật trước

	conn, err := net.Dial("tcp", "127.0.0.1:9999")
	if err != nil {
		panic(err)
	}

	fmt.Println(" Đã kết nối tới server 127.0.0.1:9999 thành công!")

	tcpConn := conn.(*net.TCPConn)

	// Tối ưu TCP phía client
	tcpConn.SetNoDelay(true)
	tcpConn.SetKeepAlive(true)
	tcpConn.SetReadBuffer(128 * 1024)
	tcpConn.SetWriteBuffer(128 * 1024)

	// gửi 3 gói nhỏ liên tục
	for i := 1; i <= 3; i++ {
		msg := fmt.Sprintf("Ping %d\n", i)
		tcpConn.Write([]byte(msg))
		fmt.Println("[CLIENT SENT]:", msg)
		time.Sleep(100 * time.Millisecond)
	}
}
