import subprocess
import re
import time

students_db = {
    "192.168.1.10": "Roll006",
    "192.168.1.14": "Roll002",
    "192.168.137.38": "chandan Yadav roll no 55",
    "192.168.137.196": "Roll024",
    "192.168.137.38": "chandan Yadav roll no 55",
}

def scan_network():
    try:
        output = subprocess.check_output(["arp", "-a"]).decode()
    except FileNotFoundError:
        raise Exception("ARP command not found. This script requires 'arp' utility installed.")
    ip_addresses = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', output)
    return ip_addresses

attendance_log = {}

def mark_attendance():
    ip_addresses = scan_network()
    for ip in ip_addresses:
        if ip in students_db:
            roll_number = students_db[ip]
            attendance_log[roll_number] = time.strftime("%Y-%m-%d %H:%M:%S")

if __name__ == "__main__":
    print("Starting IP-based WiFi Attendance System...\n")
    try:
        while True:
            mark_attendance()
            print("Attendance so far:")
            for roll, timestamp in attendance_log.items():
                print(f"{roll} - {timestamp}")
            # Ask user if they want to continue
            choice = input("\nPress Enter to rescan or type 'q' to quit: ").strip().lower()
            if choice == 'q':
                print("Attendance system stopped.")
                break
    except KeyboardInterrupt:
        print("\nAttendance system stopped by user.")

