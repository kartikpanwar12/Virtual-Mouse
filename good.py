import tkinter as tk
from datetime import datetime
import os
import csv
import platform
import subprocess

# Student names
students = ["Kartik Panwar", "Chandan Yadav", "Nishant"]

# Folder to store individual attendance files
folder = "attendance"
if not os.path.exists(folder):
    os.makedirs(folder)

def mark_attendance(name):
    date = datetime.now().strftime("%Y-%m-%d")
    time_now = datetime.now().strftime("%H:%M:%S")

    filename = os.path.join(folder, f"{name}.csv")

    # If file does not exist, create with headers
    if not os.path.exists(filename):
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Time"])

    # Append today's attendance
    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([date, time_now])

    status_label.config(text=f"{name} marked present at {time_now}")

def open_attendance_folder():
    path = os.path.abspath(folder)
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":  # macOS
        subprocess.Popen(["open", path])
    else:  # Linux
        subprocess.Popen(["xdg-open", path])

# GUI
root = tk.Tk()
root.title("Attendance System")
root.geometry("400x350")

tk.Label(root, text="Attendance System", font=("Arial", 16)).pack(pady=10)

for student in students:
    tk.Button(root, text=f"Mark {student}", font=("Arial", 12),
              command=lambda s=student: mark_attendance(s)).pack(pady=5)

status_label = tk.Label(root, text="", fg="green", font=("Arial", 12))
status_label.pack(pady=20)

# Open attendance folder button
tk.Button(root, text="Open Attendance Folder", font=("Arial", 12),
          bg="blue", fg="white", command=open_attendance_folder).pack(pady=10)

root.mainloop()
