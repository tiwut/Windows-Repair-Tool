# -*- coding: utf-8 -*-

import sys
import ctypes
import os
import subprocess
import threading
import queue
import re
import time

def is_admin():
    """Returns True if the script is running with administrative privileges, False otherwise."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_the_app():
    """Initializes and runs the main Tkinter application window."""
    import tkinter as tk
    from tkinter import scrolledtext
    from tkinter import ttk

    class WindowsRepairTool:
        def __init__(self, root):
            self.root = root
            self.root.title("Windows Repair Tool (Admin)")
            self.root.geometry("650x550")
            self.root.minsize(500, 400)
            
            self.start_time = None

            button_frame = tk.Frame(root)
            button_frame.pack(pady=10, padx=10, fill=tk.X)

            self.sfc_button = tk.Button(button_frame, text="Run System File Checker (sfc /scannow)", command=lambda: self.start_command_thread("sfc /scannow"))
            self.sfc_button.pack(pady=5, fill=tk.X)

            self.dism_check_button = tk.Button(button_frame, text="Check Windows Image Health (DISM ScanHealth)", command=lambda: self.start_command_thread("DISM /Online /Cleanup-Image /ScanHealth"))
            self.dism_check_button.pack(pady=5, fill=tk.X)

            self.dism_restore_button = tk.Button(button_frame, text="Restore Windows Image Health (DISM RestoreHealth)", command=lambda: self.start_command_thread("DISM /Online /Cleanup-Image /RestoreHealth"))
            self.dism_restore_button.pack(pady=5, fill=tk.X)
            
            self.buttons = [self.sfc_button, self.dism_check_button, self.dism_restore_button]

            progress_frame = ttk.Frame(root)
            progress_frame.pack(pady=5, padx=10, fill=tk.X)
            
            self.status_label = ttk.Label(progress_frame, text="Status: Idle", font=("Segoe UI", 9))
            self.status_label.pack(fill=tk.X)

            self.progress_bar = ttk.Progressbar(progress_frame, orient="horizontal", length=100, mode="determinate")
            self.progress_bar.pack(pady=5, fill=tk.X)
            
            self.time_label = ttk.Label(progress_frame, text="Time Remaining: N/A", font=("Segoe UI", 9))
            self.time_label.pack(fill=tk.X)

            self.output_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, bg="black", fg="lime green", font=("Consolas", 10), relief="sunken", borderwidth=2)
            self.output_area.pack(pady=10, padx=10, expand=True, fill=tk.BOTH)

            self.command_queue = queue.Queue()
            self.process_queue()

        def toggle_buttons(self, enabled):
            """Aktiviert oder deaktiviert alle Befehls-Buttons."""
            for button in self.buttons:
                button.config(state="normal" if enabled else "disabled")

        def start_command_thread(self, command):
            """Startet einen neuen Thread, um einen Befehl auszuführen."""
            self.toggle_buttons(enabled=False)
            self.output_area.delete('1.0', tk.END)
            self.output_area.insert(tk.END, f"--> Starting command: {command}\n\n")
            self.status_label.config(text=f"Status: Running {command.split()[0]}...")
            self.time_label.config(text="Time Remaining: Calculating...")
            self.progress_bar["value"] = 0
            self.start_time = time.time()
            
            thread = threading.Thread(target=self.run_command_worker, args=(command, self.command_queue))
            thread.daemon = True
            thread.start()

        def process_queue(self):
            """Überwacht die Queue auf Nachrichten vom Worker-Thread und aktualisiert die GUI."""
            try:
                message = self.command_queue.get_nowait()
                
                if message.startswith("PROGRESS:"):
                    progress = int(message.split(":")[1])
                    self.progress_bar["value"] = progress
                    self.update_estimated_time(progress)
                elif message.startswith("EXITCODE:"):
                    return_code = message.split(":")[1]
                    self.progress_bar["value"] = 100
                    self.output_area.insert(tk.END, f"\n--> Command finished with exit code: {return_code}\n" + "="*50 + "\n\n")
                    self.status_label.config(text="Status: Idle")
                    self.time_label.config(text="Time Remaining: N/A")
                    self.toggle_buttons(enabled=True)
                    self.start_time = None
                else:
                    self.output_area.insert(tk.END, message)
                    self.output_area.see(tk.END)

            except queue.Empty:
                pass
            finally:
                self.root.after(100, self.process_queue)

        def update_estimated_time(self, current_progress):
            """Berechnet und aktualisiert die geschätzte verbleibende Zeit."""
            if self.start_time is None or current_progress < 3:
                return

            elapsed_time = time.time() - self.start_time
            total_estimated_time = (elapsed_time / current_progress) * 100
            remaining_time_sec = total_estimated_time - elapsed_time

            if remaining_time_sec > 0:
                self.time_label.config(text=f"Time Remaining: approx. {self.format_time(remaining_time_sec)}")

        @staticmethod
        def format_time(seconds):
            """Formatiert Sekunden in einen lesbaren String (Minuten und Sekunden)."""
            if seconds < 60:
                return f"{int(seconds)} sec"
            minutes = int(seconds / 60)
            secs = int(seconds % 60)
            return f"{minutes} min, {secs} sec"

        def run_command_worker(self, command_to_run, q):
            """Diese Funktion läuft im Hintergrund-Thread und führt den Befehl aus."""
            try:
                progress_regex = re.compile(r"(\d{1,2}(?:\.\d)?|\d{3})%")
                
                process = subprocess.Popen(
                    command_to_run,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True, shell=True,
                    creationflags=subprocess.CREATE_NO_WINDOW,
                    encoding='utf-8', errors='ignore'
                )
                
                for line in iter(process.stdout.readline, ''):
                    q.put(line)
                    match = progress_regex.search(line)
                    if match:
                        progress = float(match.group(1))
                        q.put(f"PROGRESS:{int(progress)}")

                process.stdout.close()
                return_code = process.wait()
                
                error_output = process.stderr.read()
                if error_output:
                    q.put(f"\n--- ERROR OUTPUT ---\n{error_output}\n")
                
                q.put(f"EXITCODE:{return_code}")

            except Exception as e:
                q.put(f"\n--- FATAL ERROR ---\n{e}\n\n")
                q.put("EXITCODE:1")

    root = tk.Tk()
    app = WindowsRepairTool(root)
    root.mainloop()

if __name__ == "__main__":
    if '--elevated' in sys.argv:
        run_the_app()
    else:
        if is_admin():
            run_the_app()
        else:
            print("INFO: Admin rights not found. Requesting elevation...")
            command_to_execute = f'"{sys.executable}" "{__file__}" --elevated"'
            print(f"Command to be executed by admin shell: {command_to_execute}")
            full_cmd_argument = f'/k ""{sys.executable}" "{__file__}" --elevated"'
            ctypes.windll.shell32.ShellExecuteW(None, "runas", "cmd.exe", full_cmd_argument, None, 1)