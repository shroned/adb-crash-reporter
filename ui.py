import subprocess
import re
import os
import threading
import tkinter as tk
from tkinter import scrolledtext
from playsound3 import playsound
from plyer import notification


class LogMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ADB Log Monitor")
        self.root.config(bg='lightblue')  # Set the background color of the main window

        self.keyword_label = tk.Label(root, text="Enter Keyword to monitor(Use Comma to seperate incase of multiple keywords):", bg='lightblue', fg='black')
        self.keyword_label.pack(pady=5)

        self.keyword_entry = tk.Entry(root, width=50, bg='white', fg='black')
        self.keyword_entry.pack(pady=5)

        self.start_button = tk.Button(root, text="Start Monitoring", command=self.start_monitoring, bg='green', fg='white')
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(root, text="Stop Monitoring", command=self.stop_monitoring, state=tk.DISABLED, bg='red', fg='white')
        self.stop_button.pack(pady=5)

        self.log_display = scrolledtext.ScrolledText(root, width=80, height=20, bg='black', fg='white')
        self.log_display.pack(pady=10)

        self.clear_button = tk.Button(root, text="Clear Console", command=self.clear_console, bg='yellow', fg='black')
        self.clear_button.pack(pady=5)

        self.log_file_label = tk.Label(root, text="Log file name:", bg='lightblue', fg='black')
        self.log_file_label.pack(pady=5)

        self.log_file_entry = tk.Entry(root, width=30, bg='white', fg='black')
        self.log_file_entry.pack(pady=5)

        self.record_button = tk.Button(root, text="Start Recording", command=self.start_recording, bg='blue', fg='white')
        self.record_button.pack(pady=5)

        self.stop_record_button = tk.Button(root, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED, bg='orange', fg='white')
        self.stop_record_button.pack(pady=5)

        self.monitoring_thread = None
        self.recording_thread = None
        self.adb_monitor_process = None
        self.adb_record_process = None
        self.stop_monitor_event = threading.Event()
        self.stop_record_event = threading.Event()
        self.is_recording = False
        self.log_file = None

    def check_device_connected(self):
        result = subprocess.run(['adb', 'devices'], stdout=subprocess.PIPE)
        output = result.stdout.decode('utf-8')
        devices = [line for line in output.split('\n') if '\tdevice' in line]
        return len(devices) > 0

    def start_monitoring(self):
        if not self.check_device_connected():
            self.log_display.insert(tk.END, "No device connected. Please connect a device and try again.\n")
            return

        keywords = self.keyword_entry.get().strip()
        if keywords:
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.stop_monitor_event.clear()
            self.monitoring_thread = threading.Thread(target=self.monitor_logs, args=(keywords,))
            self.monitoring_thread.start()
            self.log_display.insert(tk.END, "Log monitoring started.\n")
        else:
            self.log_display.insert(tk.END, "Please enter keywords to monitor.\n")

    def stop_monitoring(self):
        self.stop_monitor_event.set()
        if self.adb_monitor_process:
            self.adb_monitor_process.kill()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.log_display.insert(tk.END, "Stopped log monitoring.\n")

    def start_recording(self):
        if not self.check_device_connected():
            self.log_display.insert(tk.END, "No device connected. Please connect a device and try again.\n")
            return

        log_file_name = self.log_file_entry.get().strip()
        if log_file_name:
            log_file_path = os.path.join(os.getcwd(), f"{log_file_name}.txt")
            self.log_file = open(log_file_path, "w")
            self.is_recording = True
            self.record_button.config(state=tk.DISABLED)
            self.stop_record_button.config(state=tk.NORMAL)
            self.log_display.insert(tk.END, f"Recording logs to {log_file_path}\n")
            self.stop_record_event.clear()
            self.recording_thread = threading.Thread(target=self.record_logs)
            self.recording_thread.start()
            self.log_display.insert(tk.END, "Log recording started.\n")
        else:
            self.log_display.insert(tk.END, "Please enter a log file name.\n")

    def stop_recording(self):
        self.stop_record_event.set()
        self.is_recording = False
        if self.adb_record_process:
            self.adb_record_process.kill()
        if self.log_file:
            self.log_file.close()
            self.log_file = None
        self.record_button.config(state=tk.NORMAL)
        self.stop_record_button.config(state=tk.DISABLED)
        self.log_display.insert(tk.END, "Log recording stopped.\n")

    def monitor_logs(self, keywords):
        keywords_list = [keyword.strip() for keyword in keywords.split(",")]
        self.adb_monitor_process = subprocess.Popen(['adb', 'logcat'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            for line in iter(self.adb_monitor_process.stdout.readline, b''):
                if self.stop_monitor_event.is_set():
                    break
                line = line.decode('utf-8').strip()
                if any(re.search(keyword, line) for keyword in keywords_list):
                    self.log_display.insert(tk.END, f"Found keyword in log: {line}\n")
                    self.log_display.see(tk.END)
                    notification.notify(
                        title="Log Keyword Found",
                        message=f"Keyword found in log: {line}",
                        app_name="ADB Log Monitor",
                        timeout=5  # Notification timeout in seconds
                    )
                    self.play_sound()
        except KeyboardInterrupt:
            self.log_display.insert(tk.END, "Stopping log monitoring...\n")
        finally:
            if self.adb_monitor_process:
                self.adb_monitor_process.kill()

    def record_logs(self):
        self.adb_record_process = subprocess.Popen(['adb', 'logcat'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            for line in iter(self.adb_record_process.stdout.readline, b''):
                if self.stop_record_event.is_set():
                    break
                line = line.decode('utf-8').strip()
                if self.is_recording and self.log_file:
                    self.log_file.write(f"{line}\n")
        except KeyboardInterrupt:
            self.log_display.insert(tk.END, "Stopping log recording...\n")
        finally:
            if self.adb_record_process:
                self.adb_record_process.kill()

    def play_sound(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        sound_file = os.path.join(script_dir, "warning.mp3")
        if os.path.exists(sound_file):
            playsound(sound_file)
        else:
            self.log_display.insert(tk.END, "Sound file 'warning.mp3' not found in script directory.\n")

    def clear_console(self):
        self.log_display.delete('1.0', tk.END)
        self.log_display.insert(tk.END, "Console cleared.\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = LogMonitorApp(root)
    root.mainloop()

