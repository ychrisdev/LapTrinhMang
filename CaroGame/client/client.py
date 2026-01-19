# client/client.py
import socket
import threading
from protocol import encode, decode
from ui_app import App

class Client:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        self.app = None
        self.running = True
        threading.Thread(target=self.listen_server, daemon=True).start()

    def set_app(self, app):
        self.app = app

    def send(self, msg_type, data):
        if not self.running:
            return
        try:
            self.sock.sendall(encode(msg_type, data))
        except:
            print("Send failed")
            self.running = False

    def listen_server(self):
        while self.running:
            try:
                data = self.sock.recv(4096)
                if not data:
                    break

                msg = decode(data)
                print("[Server] ->", msg)

                if self.app:
                    self.app.handle_message(msg)

            except Exception as e:
                print("Listen error:", e)
                break

        self.running = False
        self.sock.close()

def main():
    client = Client("127.0.0.1", 5000)
    app = App(client)
    client.set_app(app)
    app.mainloop()


if __name__ == "__main__":
    main()
