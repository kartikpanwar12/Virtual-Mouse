import socket

HOST = '127.0.0.1'  # Localhost
PORT = 65432        # Port to listen on

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server is listening on {HOST}:{PORT} (waiting for SYN)...")

    while True:
        conn, addr = s.accept()
        with conn:
            print(f"SYN received from {addr}. Sending SYN-ACK...")
            while True:
                data = conn.recv(1024)
                if not data:
                    print(f"Connection closed by client {addr}")
                    break
                print("ACK and data received from client:", data.decode())
                conn.sendall(b"Hello Client, connection established.")
