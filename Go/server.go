package main

import (
	"bufio"
	"fmt"
	"net"
	"time"
)

func main() {
	ln, err := net.Listen("tcp", ":9999")
	if err != nil {
		panic(err)
	}

	fmt.Println("[SERVER] Đang lắng nghe trên cổng 9999...")

	for {
		conn, err := ln.Accept()
		if err != nil {
			fmt.Println("Accept error:", err)
			continue
		}

		tcpConn := conn.(*net.TCPConn)

		// Lấy địa chỉ client
		clientAddr := tcpConn.RemoteAddr().String()
		fmt.Println(" [SERVER] Client vừa kết nối từ:", clientAddr)

		// Tối ưu TCP
		tcpConn.SetNoDelay(false)
		tcpConn.SetKeepAlive(true)
		tcpConn.SetKeepAlivePeriod(20 * time.Second)
		tcpConn.SetReadBuffer(256 * 1024)
		tcpConn.SetWriteBuffer(256 * 1024)

		go handleConn(tcpConn, clientAddr)
	}
}

func handleConn(conn *net.TCPConn, clientAddr string) {
	defer func() {
		fmt.Println(" [SERVER] Client ngắt kết nối:", clientAddr)
		conn.Close()
	}()

	reader := bufio.NewReader(conn)

	for {
		msg, err := reader.ReadString('\n')
		if err != nil {
			return // client ngắt kết nối
		}

		fmt.Printf("[SERVER RECEIVED từ %s]: %s", clientAddr, msg)
	}
}
