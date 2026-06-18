import tkinter as tk
import sqlite3

DB_FILE = "chat.db"

def load_messages():
    """Load messages into the dashboard only when button is clicked."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT sender, message, timestamp, direction FROM messages ORDER BY id ASC")
    rows = c.fetchall()
    conn.close()

    # Clear previous text
    client_area.config(state="normal")
    server_area.config(state="normal")
    client_area.delete(1.0, tk.END)
    server_area.delete(1.0, tk.END)

    for sender, message, ts, direction in rows:
        entry = f"[{ts}] {sender}: {message}\n"
        if direction == "received":  # client -> server
            client_area.insert(tk.END, entry, "client")
        else:  # server -> client
            server_area.insert(tk.END, entry, "server")

    client_area.config(state="disabled")
    server_area.config(state="disabled")

def clear_messages():
    """Clear history from dashboard (but not delete from DB)."""
    client_area.config(state="normal")
    server_area.config(state="normal")
    client_area.delete(1.0, tk.END)
    server_area.delete(1.0, tk.END)
    client_area.config(state="disabled")
    server_area.config(state="disabled")

# Setup GUI
root = tk.Tk()
root.title("Chat Dashboard")
root.geometry("850x500")
root.configure(bg="black")

# Title
title = tk.Label(root, text="Chat Dashboard",
                 font=("Arial", 16, "bold"), fg="white", bg="black")
title.pack(pady=10)

# Frames for two columns
frame = tk.Frame(root, bg="black")
frame.pack(expand=True, fill="both", padx=10, pady=10)

# Left column (Client Messages)
client_frame = tk.Frame(frame, bg="lightgreen", bd=2, relief="groove")
client_frame.pack(side="left", expand=True, fill="both", padx=5)

client_label = tk.Label(client_frame, text="Client Messages",
                        font=("Arial", 14, "bold"), bg="darkgreen", fg="white")
client_label.pack(fill="x")

client_area = tk.Text(client_frame, wrap="word", font=("Arial", 12),
                      bg="honeydew", fg="black", state="disabled")
client_area.pack(expand=True, fill="both", padx=5, pady=5)
client_area.tag_config("client", foreground="darkgreen")

# Right column (Server Messages)
server_frame = tk.Frame(frame, bg="lightblue", bd=2, relief="groove")
server_frame.pack(side="right", expand=True, fill="both", padx=5)

server_label = tk.Label(server_frame, text="Server Messages",
                        font=("Arial", 14, "bold"), bg="darkblue", fg="white")
server_label.pack(fill="x")

server_area = tk.Text(server_frame, wrap="word", font=("Arial", 12),
                      bg="aliceblue", fg="black", state="disabled")
server_area.pack(expand=True, fill="both", padx=5, pady=5)
server_area.tag_config("server", foreground="navy")

# Control buttons
btn_frame = tk.Frame(root, bg="black")
btn_frame.pack(pady=10)

show_btn = tk.Button(btn_frame, text="📜 Show History", command=load_messages,
                     font=("Arial", 12, "bold"), bg="orange", fg="black")
show_btn.pack(side="left", padx=10)

clear_btn = tk.Button(btn_frame, text="❌ Clear", command=clear_messages,
                      font=("Arial", 12, "bold"), bg="red", fg="white")
clear_btn.pack(side="right", padx=10)

root.mainloop()
