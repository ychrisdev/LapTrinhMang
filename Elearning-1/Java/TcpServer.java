import java.net.ServerSocket;
import java.net.Socket;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;

public class TcpServer {

    public static void main(String[] args) {
        try {
            ServerSocket serverSocket = new ServerSocket(8080);
            System.out.println("Server is listening on port 8080...");

            Socket clientSocket = serverSocket.accept();
            System.out.println("Server accepted a connection from client.");

            // ===== TCP OPTIONS =====
            clientSocket.setTcpNoDelay(true); // Disable Nagle’s Algorithm
            clientSocket.setKeepAlive(true);  // Enable TCP Keep-Alive

            BufferedReader in = new BufferedReader(
                    new InputStreamReader(clientSocket.getInputStream(), "UTF-8")
            );

            PrintWriter out = new PrintWriter(
                    new OutputStreamWriter(clientSocket.getOutputStream(), "UTF-8"),
                    true
            );

            String message;
            while ((message = in.readLine()) != null) {
                System.out.println("Server received: " + message);
                out.println("ACK: " + message);
            }

            clientSocket.close();
            serverSocket.close();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
