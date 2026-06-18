import tkinter as tk
import time

class TCPHandshakeAnimation:
    def __init__(self, root):
        self.root = root
        self.root.title("TCP 3-Way Handshake Animation")
        self.root.geometry("800x500")
        self.root.configure(bg="black")

        # Title
        tk.Label(root, text="TCP 3-Way Handshake Simulation",
                 font=("Arial", 18, "bold"), fg="white", bg="black").pack(pady=10)

        # Canvas for animation
        self.canvas = tk.Canvas(root, width=760, height=350, bg="black", highlightthickness=0)
        self.canvas.pack(pady=20)

        # Server Box
        self.server_box = self.canvas.create_rectangle(50, 120, 200, 200, fill="red")
        self.canvas.create_text(125, 160, text="SERVER", font=("Arial", 12, "bold"), fill="white")

        # Client Box
        self.client_box = self.canvas.create_rectangle(600, 120, 750, 200, fill="green")
        self.canvas.create_text(675, 160, text="CLIENT", font=("Arial", 12, "bold"), fill="white")

        # Start Button
        self.start_btn = tk.Button(root, text="Start Handshake", font=("Arial", 12, "bold"),
                                   bg="blue", fg="white", command=self.start_animation)
        self.start_btn.pack()

        # Status Log
        self.log_box = tk.Text(root, width=90, height=7, bg="black", fg="lime", font=("Consolas", 11))
        self.log_box.pack(pady=10)

    def log(self, msg):
        self.log_box.insert(tk.END, msg + "\n")
        self.log_box.see(tk.END)
        self.root.update()

    def animate_packet(self, text, start_x, start_y, end_x, end_y, color, delay=15):
        packet = self.canvas.create_oval(start_x-15, start_y-15, start_x+15, start_y+15, fill=color)
        label = self.canvas.create_text(start_x, start_y, text=text, fill="white", font=("Arial", 10, "bold"))

        dx = (end_x - start_x) / 40
        dy = (end_y - start_y) / 40

        for _ in range(40):
            self.canvas.move(packet, dx, dy)
            self.canvas.move(label, dx, dy)
            self.root.update()
            time.sleep(delay / 1000)

        self.canvas.delete(packet)
        self.canvas.delete(label)

    def start_animation(self):
        self.start_btn.config(state="disabled")
        self.log("[CLIENT] Sending SYN → Server")
        self.animate_packet("SYN", 675, 200, 125, 200, "yellow")

        self.log("[SERVER] Received SYN. Sending SYN-ACK → Client")
        self.animate_packet("SYN-ACK", 125, 200, 675, 200, "orange")

        self.log("[CLIENT] Received SYN-ACK. Sending ACK → Server")
        self.animate_packet("ACK", 675, 200, 125, 200, "lime")

        self.log("[SYSTEM] TCP 3-Way Handshake Completed ✅")

        # Final success text
        self.canvas.create_text(400, 80,
                                text="🔗 CONNECTION ESTABLISHED 🔗",
                                font=("Arial", 16, "bold"),
                                fill="lime")

if __name__ == "__main__":
    root = tk.Tk()
    app = TCPHandshakeAnimation(root)
    root.mainloop()
