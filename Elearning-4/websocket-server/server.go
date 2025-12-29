package main

import (
	"fmt"
	"log"
	"net/http"
	"sync"

	"github.com/gorilla/websocket"
)

var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool {
		return true // cho phép mọi client
	},
}

var clients = make(map[*websocket.Conn]bool)
var mutex = sync.Mutex{}

func handleClient(w http.ResponseWriter, r *http.Request) {
	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Println("Upgrade error:", err)
		return
	}

	mutex.Lock()
	clients[conn] = true
	mutex.Unlock()

	log.Println("Client connected")

	defer func() {
		mutex.Lock()
		delete(clients, conn)
		mutex.Unlock()
		conn.Close()
		log.Println("Client disconnected")
	}()

	for {
		_, msg, err := conn.ReadMessage()
		if err != nil {
			return
		}

		log.Printf("Received: %s\n", msg)

		// Broadcast
		mutex.Lock()
		for c := range clients {
			c.WriteMessage(websocket.TextMessage, msg)
		}
		mutex.Unlock()
	}
}

func main() {
	http.HandleFunc("/ws", handleClient)

	fmt.Println("WebSocket server running at :9090")
	log.Fatal(http.ListenAndServe(":9090", nil))
}
