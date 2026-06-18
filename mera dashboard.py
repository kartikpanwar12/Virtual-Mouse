import tkinter as tk
from tkinter import messagebox
import subprocess
import re
import time
import csv
import os

# ==========================
# Attendance Save Location
# ==========================
SAVE_FOLDER = r"C:\Users\Kartik Panwar\Documents\Attendance"
os.makedirs(SAVE_FOLDER, exist_ok=True)

# ==========================
# Student Database (MAC -> Name)
# Replace with actual MAC addresses
# ==========================
students_db = {
    "82:37:8f:56:25:63": "Chandan Yadav",
    "82:37:8f:56:25:63": "Roll002",
    "E8-9F-6D-88-77-55": "Roll024",
    "90-AB-CD-12-34-56": "Roll006",
}

attendance_log = {}


# ==========================
# Scan Network and Get MACs
# ==========================
def scan_network():
    try:
        output = subprocess.check_output(
            ["arp", "-a"],
            stderr=subprocess.DEVNULL
        ).decode(errors="ignore")

    except FileNotFoundError:
        raise Exception(
            "ARP command not found."
        )

    devices = {}

    lines = output.splitlines()

    for line in lines:

        match = re.search(
            r'(\d+\.\d+\.\d+\.\d+)\s+([0-9a-fA-F\-]{17})',
            line
        )

        if match:
            ip = match.group(1)
            mac = match.group(2).upper()

            devices[mac] = ip

    return devices


# ==========================
# Mark Attendance
# ==========================
def mark_attendance():

    devices = scan_network()

    for mac in devices:

        if mac in students_db:

            student = students_db[mac]

            if student not in attendance_log:

                attendance_log[student] = time.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                


# ==========================
# GUI Application
# ==========================
class AttendanceApp:

    def __init__(self, root):

        self.root = root
        self.root.title("Student Attendance Dashboard")
        self.root.geometry("650x500")

        # Attendance List
        self.listbox = tk.Listbox(
            root,
            font=("Arial", 12)
        )

        self.listbox.pack(
            fill=tk.BOTH,
            expand=True,
            padx=10,
            pady=10
        )

        # Statistics
        self.total_label = tk.Label(
            root,
            text="Total Students: 0",
            font=("Arial", 11)
        )
        self.total_label.pack()

        self.present_label = tk.Label(
            root,
            text="Present: 0",
            font=("Arial", 11)
        )
        self.present_label.pack()

        self.absent_label = tk.Label(
            root,
            text="Absent: 0",
            font=("Arial", 11)
        )
        self.absent_label.pack()

        self.percent_label = tk.Label(
            root,
            text="Attendance: 0%",
            font=("Arial", 11, "bold")
        )
        self.percent_label.pack(pady=5)

        # Buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        self.refresh_button = tk.Button(
            button_frame,
            text="Refresh Attendance",
            command=self.manual_refresh,
            width=18
        )
        self.refresh_button.grid(
            row=0,
            column=0,
            padx=5
        )

        self.save_button = tk.Button(
            button_frame,
            text="Save Attendance",
            command=self.save_attendance,
            width=18
        )
        self.save_button.grid(
            row=0,
            column=1,
            padx=5
        )

        self.open_folder_button = tk.Button(
            button_frame,
            text="Open Attendance Folder",
            command=self.open_attendance_folder,
            width=22
        )
        self.open_folder_button.grid(
            row=0,
            column=2,
            padx=5
        )

        self.running = True

        self.update_attendance_periodically()

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.on_closing
        )

    # ==========================
    # Auto Update Every 30 sec
    # ==========================
    def update_attendance_periodically(self):

        if not self.running:
            return

        try:
            mark_attendance()
            self.refresh_attendance()

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )

        self.root.after(
            30000,
            self.update_attendance_periodically
        )

    # ==========================
    # Manual Refresh
    # ==========================
    def manual_refresh(self):

        try:
            mark_attendance()
            self.refresh_attendance()

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )

    # ==========================
    # Update Dashboard
    # ==========================
    def refresh_attendance(self):

        self.listbox.delete(
            0,
            tk.END
        )

        present_students = sorted(
            attendance_log.keys()
        )

        for idx, student in enumerate(
                present_students,
                start=1):

            self.listbox.insert(
                tk.END,
                f"{idx}. {student}"
            )

        total_students = len(
            students_db
        )

        present_count = len(
            attendance_log
        )

        absent_count = (
            total_students
            - present_count
        )

        percentage = 0

        if total_students > 0:
            percentage = (
                present_count
                / total_students
            ) * 100

        self.total_label.config(
            text=f"Total Students: {total_students}"
        )

        self.present_label.config(
            text=f"Present: {present_count}"
        )

        self.absent_label.config(
            text=f"Absent: {absent_count}"
        )

        self.percent_label.config(
            text=f"Attendance: {percentage:.2f}%"
        )

    # ==========================
    # Save Attendance
    # ==========================
    def save_attendance(self):

        if not attendance_log:

            messagebox.showwarning(
                "No Data",
                "No attendance records found."
            )
            return

        filename = os.path.join(
            SAVE_FOLDER,
            f"attendance_{time.strftime('%Y%m%d_%H%M%S')}.csv"
        )

        try:

            with open(
                filename,
                "w",
                newline=""
            ) as file:

                writer = csv.writer(file)

                writer.writerow(
                    ["Student", "Timestamp"]
                )

                for student, timestamp in attendance_log.items():

                    writer.writerow(
                        [student, timestamp]
                    )

            messagebox.showinfo(
                "Saved",
                f"Attendance saved successfully!\n\n{filename}"
            )

        except Exception as e:

            messagebox.showerror(
                "Save Error",
                str(e)
            )

    # ==========================
    # Open Folder
    # ==========================
    def open_attendance_folder(self):

        try:
            os.startfile(
                SAVE_FOLDER
            )

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )

    # ==========================
    # Close App
    # ==========================
    def on_closing(self):

        self.running = False
        self.root.destroy()


# ==========================
# Main Program
# ==========================
if __name__ == "__main__":

    root = tk.Tk()

    app = AttendanceApp(root)

    root.mainloop()