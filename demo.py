import socket

HOST = '127.0.0.1'   # Standard loopback interface address (localhost)
PORT = 65432         # Port to listen on (non-privileged ports > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Server is listening, waiting for connection (SYN)...")
    conn, addr = s.accept()
    with conn:
        print(f"SYN received from {addr}. Sending SYN-ACK...")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print("ACK and data received from client:", data.decode())
            conn.sendall(b"Hello Client, connection established.")
            