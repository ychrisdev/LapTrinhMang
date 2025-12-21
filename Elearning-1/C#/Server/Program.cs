using System;
using System.Net;
using System.Net.Sockets;
using System.Diagnostics;
using System.Text;
using System.Threading;

class Program
{
    static bool EnableNagle = true;
    static bool EnableKeepAlive = true;
    static bool EnableWindowScaling = true;
    static bool EnableCongestionSimulation = false;
    static bool EnableFastOpen = false;

    static void Main()
    {
        Console.WriteLine("===== TCP SERVER — PING MODE =====");

        TcpListener server = new TcpListener(IPAddress.Any, 5000);
        server.Start();
        Console.WriteLine("[OK] Server started on port 5000");

        TcpClient client = server.AcceptTcpClient();
        Console.WriteLine("[OK] Client connected");

        Socket socket = client.Client;

        socket.NoDelay = !EnableNagle;
        socket.SetSocketOption(SocketOptionLevel.Socket, SocketOptionName.KeepAlive, EnableKeepAlive);

        if (EnableWindowScaling)
        {
            socket.ReceiveBufferSize = 256 * 1024;
            socket.SendBufferSize = 256 * 1024;
        }

        NetworkStream ns = client.GetStream();
        byte[] buffer = new byte[1024];

        Console.WriteLine("=== Server is listening for PING ===");

        while (true)
        {
            int bytes = ns.Read(buffer, 0, buffer.Length);
            if (bytes == 0)
                break;

            string msg = Encoding.UTF8.GetString(buffer, 0, bytes);
            Console.WriteLine($"[RECV] {msg}");
        }

        client.Close();
        server.Stop();
    }
}
