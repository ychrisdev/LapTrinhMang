import java.net.Socket;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;

public class TcpClient {

    public static void main(String[] args) {
        try {
            Socket socket = new Socket("localhost", 8080);
            System.out.println("Client connected to server.");

            // ===== TCP OPTIONS =====
            socket.setTcpNoDelay(true); // Disable Nagle’s Algorithm
            socket.setKeepAlive(true);  // Enable TCP Keep-Alive

            PrintWriter out = new PrintWriter(
                    new OutputStreamWriter(socket.getOutputStream(), "UTF-8"),
                    true
            );

            BufferedReader in = new BufferedReader(
                    new InputStreamReader(socket.getInputStream(), "UTF-8")
            );

            // ===== PING 1 =====
            System.out.println("Client sending: Ping 1");
            out.println("Ping 1");

            String response1 = in.readLine();
            System.out.println("Client received: " + response1);

            // ===== PING 2 =====
            System.out.println("Client sending: Ping 2");
            out.println("Ping 2");

            String response2 = in.readLine();
            System.out.println("Client received: " + response2);

            socket.close();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
