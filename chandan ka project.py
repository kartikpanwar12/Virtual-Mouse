import tkinter as tk
from tkinter import messagebox
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email sender credentials
smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_email = "cy3863622@gmail.com"  # Replace with your email
password = "splb rbsj htpl nyks"          # Use app password or OAuth2 token

class EmailDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Send Email via SMTP")
        self.geometry("400x200")

        tk.Label(self, text="Receiver's Gmail Address:").pack(pady=5)
        self.receiver_email_entry = tk.Entry(self, width=50)
        self.receiver_email_entry.pack(pady=5)

        tk.Label(self, text="Email Subject:").pack(pady=5)
        self.subject_entry = tk.Entry(self, width=50)
        self.subject_entry.pack(pady=5)

        tk.Label(self, text="Email Body:").pack(pady=5)
        self.body_entry = tk.Text(self, height=5, width=50)
        self.body_entry.pack(pady=5)

        self.send_button = tk.Button(self, text="Send Email", command=self.send_email)
        self.send_button.pack(pady=10)

    def send_email(self):
        receiver_email = self.receiver_email_entry.get().strip()
        subject = self.subject_entry.get().strip()
        body = self.body_entry.get("1.0", tk.END).strip()

        if not receiver_email:
            messagebox.showerror("Input Error", "Please enter the receiver's email address.")
            return
        if not subject:
            messagebox.showerror("Input Error", "Please enter the subject.")
            return
        if not body:
            messagebox.showerror("Input Error", "Please enter the email body.")
            return

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            server.quit()
            messagebox.showinfo("Success", "Email sent successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send email.\n\n{e}")

if __name__ == "__main__":
    app = EmailDashboard()
    app.mainloop()
