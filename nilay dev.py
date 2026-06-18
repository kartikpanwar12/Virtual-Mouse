import socket
import threading
import sqlite3
from datetime import datetime

HOST = "0.0.0.0"
PORT = 5000

# Database setup
conn = sqlite3.connect("chat.db", check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS messages
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              sender TEXT,
              message TEXT,
              timestamp TEXT,
              direction TEXT)''')
conn.commit()

# Simple Caesar cipher decryption
def decrypt(msg):
    return "".join(chr(ord(ch) - 3) for ch in msg)

# Encryption for server reply
def encrypt(msg):
    return "".join(chr(ord(ch) + 3) for ch in msg)

def log_message(sender, message, direction):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO messages (sender, message, timestamp, direction) VALUES (?, ?, ?, ?)",
              (sender, message, ts, direction))
    conn.commit()

def handle_client(client_socket, addr):
    print(f"[+] Connection from {addr}")
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            # decrypt incoming message
            message = decrypt(data)
            print(f"[Client {addr}] {message}")
            log_message(f"Client {addr}", message, "received")

            # reply from server
            reply = f"Server got your message: {message}"
            enc_reply = encrypt(reply)
            client_socket.send(enc_reply.encode())
            log_message("Server", reply, "sent")
        except:
            break
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[*] Server listening on {HOST}:{PORT}")
    while True:
        client_socket, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
