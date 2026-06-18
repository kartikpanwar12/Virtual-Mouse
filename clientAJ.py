import socket

HOST = '127.0.0.1'  # Loopback address (server must use same IP)
PORT = 65432        # Must match the server's port

try:
    # Create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("[CLIENT] Attempting to connect to server...")
        s.connect((HOST, PORT))
        print("[CLIENT] Connected. Sending message (simulated ACK)...")
        # Send a message to simulate the ACK step
        s.sendall(b"Hello from client (ACK packet simulated)")
        # Wait for a response from the server
        data = s.recv(1024)
        print("[CLIENT] Response from server:", data.decode())
except ConnectionRefusedError:
    print("[ERROR] Connection was refused. Is the server running?")
except Exception as e:
    print(f"[ERROR] An exception occurred: {e}")
