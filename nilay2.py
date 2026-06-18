import socket

SERVER_HOST = "127.0.0.1"  # Change to server IP if needed
SERVER_PORT = 5000

def encrypt(msg):
    return "".join(chr(ord(ch) + 3) for ch in msg)

def decrypt(msg):
    return "".join(chr(ord(ch) - 3) for ch in msg)

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_HOST, SERVER_PORT))
    print("Connected to server. Type messages, 'exit' to quit.")
    
    while True:
        msg = input("> ")
        if msg.lower() == "exit":
            break
        enc_msg = encrypt(msg)
        client.send(enc_msg.encode())
        reply = client.recv(1024).decode()
        print("[Server]:", decrypt(reply))
    client.close()

if __name__ == "__main__":
    main()
