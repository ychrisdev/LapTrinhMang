using System;
using System.Net.Sockets;
using System.Text;
using System.Threading;

class Program
{
    static bool EnableNagle = true;
    static bool EnableKeepAlive = true;
    static bool EnableWindowScaling = true;

    static void Main()
    {
        Console.WriteLine("===== TCP CLIENT — PING MODE =====");

        TcpClient client = new TcpClient();
        Socket socket = client.Client;

        socket.NoDelay = !EnableNagle;
        socket.SetSocketOption(SocketOptionLevel.Socket, SocketOptionName.KeepAlive, EnableKeepAlive);

        if (EnableWindowScaling)
        {
            socket.ReceiveBufferSize = 256 * 1024;
            socket.SendBufferSize = 256 * 1024;
        }

        client.Connect("127.0.0.1", 5000);
        Console.WriteLine("[OK] Connected to server");

        NetworkStream ns = client.GetStream();

        for (int i = 1; i <= 10; i++)
        {
            string ping = $"ping #{i}";
            byte[] data = Encoding.UTF8.GetBytes(ping);

            ns.Write(data, 0, data.Length);
            Console.WriteLine($"[SEND] ping #{i}");

            Thread.Sleep(1000);
        }

        client.Close();
        Console.WriteLine("Finished sending 10 pings.");
    }
}
