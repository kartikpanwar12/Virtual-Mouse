import tkinter as tk
from tkinter import messagebox
import subprocess
import re
import time
import threading

# Database mapping IP addresses to student roll numbers (or names)
students_db = {
    "192.168.137.102": "Kartik Panwar",
    "192.168.137.76": "Kartik Panwar Gurjar",
    "192.168.137.130": "Chandan Yadav",
    "192.168.137.36": "Archit006",
    "192.168.137.36" : "Archit006",
}
import tkinter as tk
from tkinter import messagebox, simpledialog
import subprocess
import re
import time
import threading

# Database mapping IP addresses to student names
students_db = {
    "192.168.137.102": "Kartik Panwar",
    "192.168.137.76": "Kartik Panwar Gurjar",
    "192.168.137.85": "Chandan Yadav",
    "192.168.137.251": "Nishant",
}

attendance_log = {}

def scan_network():
    try:
        output = subprocess.check_output(["arp", "-a"]).decode()
    except FileNotFoundError:
        raise Exception("ARP command not found. This script requires 'arp' utility installed.")
    ip_addresses = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', output)
    return ip_addresses

def mark_attendance():
    ip_addresses = scan_network()
    new_marks = []
    for ip in ip_addresses:
        if ip in students_db:
            name = students_db[ip]
            if name not in attendance_log:
                new_marks.append(name)
            attendance_log[name] = time.strftime("%Y-%m-%d %H:%M:%S")
    return new_marks

class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Attendance Dashboard")
        self.root.geometry("500x450")
        self.root.resizable(False, False)

        # Header
        self.header = tk.Label(root, text="WiFi Attendance System", font=("Helvetica", 16, "bold"),
                               bg="#8B0000", fg="white", padx=10, pady=10)
        self.header.pack(fill=tk.X)

        # Attendance List
        self.listbox = tk.Listbox(root, font=("Arial", 14), width=35, height=10)
        self.listbox.pack(padx=10, pady=10)

        # Stats label
        self.stats_label = tk.Label(root, text="Total Present: 0", font=("Arial", 12), fg="green")
        self.stats_label.pack(pady=5)

        # Last updated label
        self.last_updated = tk.Label(root, text="Last Updated: N/A", font=("Arial", 10), fg="#8B0000")
        self.last_updated.pack(pady=2)

        # Control Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        self.start_stop_button = tk.Button(btn_frame, text="Start Scanning ▶", font=("Arial", 12),
                                           bg="green", fg="white", width=15, command=self.toggle_scanning)
        self.start_stop_button.grid(row=0, column=0, padx=5)

        self.highlight_button = tk.Button(btn_frame, text="Highlight Student ✨", font=("Arial", 12),
                                          bg="blue", fg="white", width=18, command=self.manual_highlight)
        self.highlight_button.grid(row=0, column=1, padx=5)

        self.tick_button = tk.Button(btn_frame, text="Mark Attendance ✔️", font=("Arial", 12),
                                     bg="orange", fg="white", width=18, command=self.manual_mark)
        self.tick_button.grid(row=1, column=0, columnspan=2, pady=5)

        self.running = False

    def highlight_new(self, item_idx):
        # Flash new item in green
        self.listbox.itemconfig(item_idx, bg="green")
        self.root.after(800, lambda: self.listbox.itemconfig(item_idx, bg="white"))

    def toggle_scanning(self):
        if not self.running:
            self.running = True
            self.start_stop_button.config(text="Stop Scanning ⏹", bg="red")
            self.update_attendance_periodically()
        else:
            self.running = False
            self.start_stop_button.config(text="Start Scanning ▶", bg="green")

    def update_attendance_periodically(self):
        if not self.running:
            return
        try:
            new_marks = mark_attendance()
            self.refresh_attendance(new_marks)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        # Update every 30 seconds
        self.root.after(30000, self.update_attendance_periodically)

    def refresh_attendance(self, new_marks=[]):
        self.listbox.delete(0, tk.END)
        for idx, name in enumerate(sorted(attendance_log.keys()), start=1):
            self.listbox.insert(tk.END, f"{idx}. {name}")
            if name in new_marks:
                self.highlight_new(idx - 1)

        # Update stats and timestamp
        self.stats_label.config(text=f"Total Present: {len(attendance_log)}")
        self.last_updated.config(text=f"Last Updated: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    def manual_highlight(self):
        try:
            selected_idx = self.listbox.curselection()[0]
            self.highlight_new(selected_idx)
        except IndexError:
            messagebox.showwarning("No Selection", "Please select a student to highlight.")

    def manual_mark(self):
        name = simpledialog.askstring("Manual Attendance", "Enter student name to mark present:")
        if name:
            if name not in attendance_log:
                attendance_log[name] = time.strftime("%Y-%m-%d %H:%M:%S")
                self.refresh_attendance([name])
                messagebox.showinfo("Success", f"{name} marked as present ✔️")
            else:
                messagebox.showinfo("Info", f"{name} is already marked present.")

    def on_closing(self):
        self.running = False
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

attendance_log = {}

def scan_network():
    try:
        output = subprocess.check_output(["arp", "-a"]).decode()
    except FileNotFoundError:
        raise Exception("ARP command not found. This script requires 'arp' utility installed.")
    ip_addresses = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', output)
    return ip_addresses

def mark_attendance():
    ip_addresses = scan_network()
    new_marks = []
    for ip in ip_addresses:
        if ip in students_db:
            roll_number = students_db[ip]
            if roll_number not in attendance_log:
                new_marks.append(roll_number)
            attendance_log[roll_number] = time.strftime("%Y-%m-%d %H:%M:%S")
    return new_marks

class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Attendance Dashboard")
        self.root.geometry("450x350")
        self.root.resizable(False, False)

        # Header
        self.header = tk.Label(root, text="WiFi Attendance System", font=("Helvetica", 16, "bold"),
                               bg="#8B0000", fg="white", padx=10, pady=10)
        self.header.pack(fill=tk.X)

        # Attendance List
        self.listbox = tk.Listbox(root, font=("Arial", 14), width=30, height=10)
        self.listbox.pack(padx=10, pady=10)

        # Stats label
        self.stats_label = tk.Label(root, text="Total Present: 0", font=("Arial", 12), fg="green")
        self.stats_label.pack(pady=5)

        # Last updated label
        self.last_updated = tk.Label(root, text="Last Updated: N/A", font=("Arial", 10), fg="#8B0000")
        self.last_updated.pack(pady=2)

        # Refresh button
        self.refresh_button = tk.Button(root, text="Refresh Attendance", font=("Arial", 12),
                                        bg="#FF4500", activebackground="#8B0000", fg="white",
                                        command=self.refresh_attendance)
        self.refresh_button.pack(pady=5)

        self.running = True
        self.update_attendance_periodically()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def highlight_new(self, item_idx):
        # Flash new item in green
        self.listbox.itemconfig(item_idx, bg="green")
        self.root.after(500, lambda: self.listbox.itemconfig(item_idx, bg="white"))

    def update_attendance_periodically(self):
        if not self.running:
            return
        try:
            new_marks = mark_attendance()
            self.refresh_attendance(new_marks)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        # Update every 30 seconds
        self.root.after(30000, self.update_attendance_periodically)

    def refresh_attendance(self, new_marks=[]):
        self.listbox.delete(0, tk.END)
        for idx, roll in enumerate(sorted(attendance_log.keys()), start=1):
            self.listbox.insert(tk.END, f"{idx}. {roll}")
            if roll in new_marks:
                self.highlight_new(idx-1)
        # Update stats and timestamp
        self.stats_label.config(text=f"Total Present: {len(attendance_log)}")
        self.last_updated.config(text=f"Last Updated: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    def on_closing(self):
        self.running = False
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceApp(root)
    root.mainloop()
