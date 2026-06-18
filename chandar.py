import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading
import time
import json
import os
import uuid
from datetime import datetime, date

# ---------- CONFIG: put your sender accounts here ----------
# Key is display name used in dropdown, value is (email, app_password)
senders = {
    "Account 1 (example)": ("cy3863622@gmail.com", "splb rbsj htpl nyks"),
    "Account 2 (example)": ("your_email2@gmail.com", "app_password2"),
    # Add more accounts here
}
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SCHEDULES_FILE = "schedules.json"
CHECK_INTERVAL_SECONDS = 30  # check every 30 seconds
# -----------------------------------------------------------


def safe_load_schedules():
    if not os.path.exists(SCHEDULES_FILE):
        return []
    try:
        with open(SCHEDULES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def safe_save_schedules(schedules):
    with open(SCHEDULES_FILE, "w", encoding="utf-8") as f:
        json.dump(schedules, f, indent=2, ensure_ascii=False)


class SchedulerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Email Scheduler Dashboard")
        self.geometry("950x520")
        self.resizable(False, False)

        # In-memory schedules and last sent tracker (to avoid multiple sends in same day)
        self.schedules = safe_load_schedules()  # list of dicts
        # map schedule_id -> last_sent_date_str (YYYY-MM-DD) in memory
        self.last_sent = {}

        # Left frame: create a new schedule
        left = tk.Frame(self, padx=10, pady=10)
        left.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(left, text="Create New Schedule", font=("Arial", 14, "bold")).pack(anchor="w")

        # Sender dropdown
        tk.Label(left, text="Select Sender:").pack(anchor="w", pady=(8, 0))
        self.sender_var = tk.StringVar()
        if senders:
            self.sender_var.set(list(senders.keys())[0])
        self.sender_menu = ttk.Combobox(left, textvariable=self.sender_var, values=list(senders.keys()), state="readonly", width=40)
        self.sender_menu.pack(anchor="w", pady=2)

        # Time entry (HH:MM)
        tk.Label(left, text="Send Time (HH:MM, 24-hour):").pack(anchor="w", pady=(8, 0))
        self.time_entry = tk.Entry(left, width=15)
        self.time_entry.pack(anchor="w", pady=2)
        tk.Label(left, text="Example: 09:00 or 18:30").pack(anchor="w", pady=(0, 6))

        # Subject
        tk.Label(left, text="Subject:").pack(anchor="w", pady=(6, 0))
        self.subject_entry = tk.Entry(left, width=60)
        self.subject_entry.pack(anchor="w", pady=2)

        # Body
        tk.Label(left, text="Body:").pack(anchor="w", pady=(6, 0))
        self.body_text = tk.Text(left, height=8, width=60)
        self.body_text.pack(anchor="w", pady=2)

        # Receivers list for this schedule (temporary until saved)
        tk.Label(left, text="Receivers for this schedule:").pack(anchor="w", pady=(6, 0))
        receivers_frame = tk.Frame(left)
        receivers_frame.pack(anchor="w", pady=2)
        self.receiver_entry = tk.Entry(receivers_frame, width=40)
        self.receiver_entry.grid(row=0, column=0, padx=(0, 6))
        add_rec_btn = tk.Button(receivers_frame, text="Add", command=self.add_receiver_temp)
        add_rec_btn.grid(row=0, column=1)
        remove_rec_btn = tk.Button(receivers_frame, text="Remove Selected", command=self.remove_receiver_temp)
        remove_rec_btn.grid(row=0, column=2, padx=(6, 0))

        self.temp_receiver_listbox = tk.Listbox(left, height=6, width=60, selectmode=tk.SINGLE)
        self.temp_receiver_listbox.pack(anchor="w", pady=4)

        # Add schedule button
        self.add_schedule_btn = tk.Button(left, text="Save Schedule", bg="#4CAF50", fg="white", command=self.save_schedule)
        self.add_schedule_btn.pack(pady=(8, 0))

        # Status label
        self.status_var = tk.StringVar(value="Ready")
        tk.Label(left, textvariable=self.status_var, fg="blue").pack(anchor="w", pady=(8, 0))

        # Right frame: show saved schedules and manage them
        right = tk.Frame(self, padx=10, pady=10)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(right, text="Saved Schedules", font=("Arial", 14, "bold")).pack(anchor="w")

        self.schedules_listbox = tk.Listbox(right, width=60, height=20)
        self.schedules_listbox.pack(side=tk.LEFT, pady=6)
        self.schedules_listbox.bind("<<ListboxSelect>>", self.on_schedule_select)

        # Buttons to remove and view details
        right_controls = tk.Frame(right)
        right_controls.pack(side=tk.LEFT, padx=10, anchor="n")

        tk.Button(right_controls, text="Remove Selected", fg="white", bg="#d9534f", width=18, command=self.remove_selected_schedule).pack(pady=(6, 4))
        tk.Button(right_controls, text="View Details", width=18, command=self.view_selected_details).pack(pady=4)
        tk.Button(right_controls, text="Send Now (Immediate)", width=18, command=self.send_selected_now).pack(pady=4)
        tk.Button(right_controls, text="Refresh", width=18, command=self.reload_schedules).pack(pady=(14, 4))

        # Fill initial listbox
        self.reload_schedules()

        # Start background checker thread
        self.stop_flag = threading.Event()
        self.checker_thread = threading.Thread(target=self.background_checker, daemon=True)
        self.checker_thread.start()

        # Handle graceful close
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    # -------------------- UI helpers --------------------
    def add_receiver_temp(self):
        email = self.receiver_entry.get().strip()
        if not email:
            messagebox.showerror("Input Error", "Enter receiver email first.")
            return
        # Basic validation
        if "@" not in email or "." not in email:
            if not messagebox.askyesno("Confirm", "Email looks unusual. Add anyway?"):
                return
        # Prevent duplicates
        existing = self.temp_receiver_listbox.get(0, tk.END)
        if email in existing:
            messagebox.showinfo("Info", "Email already in list.")
            return
        self.temp_receiver_listbox.insert(tk.END, email)
        self.receiver_entry.delete(0, tk.END)

    def remove_receiver_temp(self):
        sel = self.temp_receiver_listbox.curselection()
        if not sel:
            messagebox.showinfo("Info", "Select a receiver to remove.")
            return
        self.temp_receiver_listbox.delete(sel[0])

    def save_schedule(self):
        # Gather inputs
        sender_key = self.sender_var.get()
        time_str = self.time_entry.get().strip()
        subject = self.subject_entry.get().strip()
        body = self.body_text.get("1.0", tk.END).strip()
        receivers = list(self.temp_receiver_listbox.get(0, tk.END))

        # Validate
        if not sender_key:
            messagebox.showerror("Input Error", "Select a sender account.")
            return
        if sender_key not in senders:
            messagebox.showerror("Input Error", "Selected sender not configured in senders dict.")
            return
        if not time_str:
            messagebox.showerror("Input Error", "Enter time in HH:MM format.")
            return
        try:
            datetime.strptime(time_str, "%H:%M")
        except ValueError:
            messagebox.showerror("Input Error", "Time must be in HH:MM (24-hour) format.")
            return
        if not receivers:
            messagebox.showerror("Input Error", "Add at least one receiver.")
            return
        if not subject:
            if not messagebox.askyesno("Confirm", "Subject is empty. Save anyway?"):
                return

        # Build schedule dict
        schedule = {
            "id": str(uuid.uuid4()),
            "time": time_str,
            "sender_key": sender_key,
            "subject": subject,
            "body": body,
            "receivers": receivers
        }
        # Save
        self.schedules.append(schedule)
        safe_save_schedules(self.schedules)
        self.reload_schedules()
        # Clear form
        self.time_entry.delete(0, tk.END)
        self.subject_entry.delete(0, tk.END)
        self.body_text.delete("1.0", tk.END)
        self.temp_receiver_listbox.delete(0, tk.END)
        self.status_var.set(f"Schedule saved for {time_str} ({len(receivers)} receivers).")

    def reload_schedules(self):
        self.schedules = safe_load_schedules()
        self.schedules_listbox.delete(0, tk.END)
        for s in self.schedules:
            summary = f"{s['time']}  |  {s['sender_key']}  |  {s['subject'][:40] or '<no-subject>'}  |  {len(s.get('receivers', []))} receivers"
            self.schedules_listbox.insert(tk.END, summary)

    def on_schedule_select(self, event):
        pass  # placeholder, could be used later

    def view_selected_details(self):
        sel = self.schedules_listbox.curselection()
        if not sel:
            messagebox.showinfo("Info", "Select a schedule to view.")
            return
        idx = sel[0]
        s = self.schedules[idx]
        details = (
            f"Time: {s['time']}\nSender: {s['sender_key']}\nSubject: {s['subject']}\n\n"
            f"Body:\n{s['body']}\n\nReceivers:\n" + "\n".join(s.get("receivers", []))
        )
        # Show in a read-only dialog
        d = tk.Toplevel(self)
        d.title("Schedule Details")
        d.geometry("600x420")
        txt = tk.Text(d, wrap=tk.WORD)
        txt.pack(fill=tk.BOTH, expand=True)
        txt.insert(tk.END, details)
        txt.config(state=tk.DISABLED)
        tk.Button(d, text="Close", command=d.destroy).pack(pady=6)

    def remove_selected_schedule(self):
        sel = self.schedules_listbox.curselection()
        if not sel:
            messagebox.showinfo("Info", "Select a schedule to remove.")
            return
        idx = sel[0]
        s = self.schedules[idx]
        if not messagebox.askyesno("Confirm", f"Remove schedule at {s['time']} with subject '{s['subject'][:30]}'?"):
            return
        # Remove and save
        del self.schedules[idx]
        safe_save_schedules(self.schedules)
        # Also remove its last_sent tracker if exists
        self.last_sent.pop(s.get("id"), None)
        self.reload_schedules()
        self.status_var.set("Schedule removed.")

    # -------------------- Sending logic --------------------
    def send_email_for_schedule(self, schedule):
        # Run actual sending in a separate thread to keep UI responsive.
        def _send():
            sender_key = schedule["sender_key"]
            if sender_key not in senders:
                self._notify(f"Sender {sender_key} not configured. Skipping schedule {schedule.get('id')}.")
                return
            sender_email, sender_pass = senders[sender_key]
            receivers = schedule.get("receivers", [])
            subject = schedule.get("subject", "")
            body = schedule.get("body", "")

            try:
                server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30)
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(sender_email, sender_pass)

                for r in receivers:
                    msg = MIMEMultipart()
                    msg["From"] = sender_email
                    msg["To"] = r
                    msg["Subject"] = subject
                    msg.attach(MIMEText(body, "plain"))
                    server.sendmail(sender_email, r, msg.as_string())
                server.quit()
                # Mark as sent for today
                self.last_sent[schedule["id"]] = date.today().isoformat()
                self._notify(f"Schedule {schedule['time']} sent to {len(receivers)} receiver(s).")
            except Exception as e:
                self._notify(f"Failed to send schedule at {schedule['time']}: {e}")

        threading.Thread(target=_send, daemon=True).start()

    def send_selected_now(self):
        sel = self.schedules_listbox.curselection()
        if not sel:
            messagebox.showinfo("Info", "Select a schedule to send now.")
            return
        idx = sel[0]
        s = self.schedules[idx]
        if not messagebox.askyesno("Confirm", f"Send schedule now? This will send to {len(s.get('receivers', []))} recipients."):
            return
        self.send_email_for_schedule(s)

    def _notify(self, msg):
        # Update status label from main thread using after
        def upd():
            self.status_var.set(msg)
        self.after(0, upd)

    # -------------------- Background checker --------------------
    def background_checker(self):
        # Run until stop_flag is set
        while not self.stop_flag.is_set():
            try:
                now = datetime.now()
                current_time = now.strftime("%H:%M")
                today_str = date.today().isoformat()
                # reload schedules each check in case file changed externally
                # (keeps app responsive to external edits)
                self.schedules = safe_load_schedules()
                for s in list(self.schedules):
                    schedule_id = s.get("id")
                    sched_time = s.get("time")
                    # If time matches and not already sent today, send
                    if sched_time == current_time:
                        last = self.last_sent.get(schedule_id)
                        if last != today_str:
                            # Mark last_sent now (to avoid duplicate triggers while sending)
                            self.last_sent[schedule_id] = today_str
                            self._notify(f"Triggering schedule {sched_time} ...")
                            self.send_email_for_schedule(s)
                # Sleep until next check
                for _ in range(int(CHECK_INTERVAL_SECONDS / 2)):
                    if self.stop_flag.is_set():
                        break
                    time.sleep(0.5)
            except Exception as e:
                self._notify(f"Background checker error: {e}")
                time.sleep(2)

    def on_close(self):
        if messagebox.askyesno("Quit", "Exit the scheduler?"):
            self.stop_flag.set()
            # wait briefly for thread to stop
            time.sleep(0.3)
            self.destroy()


# ---------- Run the app ----------
if __name__ == "__main__":
    app = SchedulerApp()
    app.mainloop()
    
